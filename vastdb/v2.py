from contextlib import contextmanager
from dataclasses import dataclass
import logging
import os

import boto3
import botocore
import ibis
import pyarrow as pa
import requests

from vastdb.api import VastdbApi


log = logging.getLogger(__name__)


class VastException(Exception):
    pass


class NotFoundError(VastException):
    pass


class AccessDeniedError(VastException):
    pass


class ImportFilesError(VastException):
    pass


class InvalidArgumentError(VastException):
    pass


class RPC:
    def __init__(self, access=None, secret=None, endpoint=None):
        if access is None:
            access = os.environ['AWS_ACCESS_KEY_ID']
        if secret is None:
            secret = os.environ['AWS_SECRET_ACCESS_KEY']
        if endpoint is None:
            endpoint = os.environ['AWS_S3_ENDPOINT_URL']

        self.api = VastdbApi(endpoint, access, secret)
        self.s3 = boto3.client('s3',
            aws_access_key_id=access,
            aws_secret_access_key=secret,
            endpoint_url=endpoint)

    def __repr__(self):
        return f'RPC(endpoint={self.api.url}, access={self.api.access_key})'

    def transaction(self):
        return Transaction(self)


def connect(*args, **kw):
    return RPC(*args, **kw)


@dataclass
class Transaction:
    _rpc: RPC
    txid: int = None

    def __enter__(self):
        response = self._rpc.api.begin_transaction()
        self.txid = int(response.headers['tabular-txid'])
        log.debug("opened txid=%016x", self.txid)
        return self

    def __exit__(self, *args):
        if args == (None, None, None):
            log.debug("committing txid=%016x", self.txid)
            self._rpc.api.commit_transaction(self.txid)
        else:
            log.exception("rolling back txid=%016x", self.txid)
            self._rpc.api.rollback_transaction(self.txid)

    def __repr__(self):
        return f'Transaction(id=0x{self.txid:016x})'

    def bucket(self, name: str) -> "Bucket":
        try:
            self._rpc.s3.head_bucket(Bucket=name)
            return Bucket(name, self)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 403:
                raise AccessDeniedError(f"Access is denied to bucket: {name}") from e
            else:
                raise NotFoundError(f"Bucket {name} does not exist") from e


@dataclass
class Bucket:
    name: str
    tx: Transaction

    def create_schema(self, path: str) -> None:
        self.tx._rpc.api.create_schema(self.name, path, txid=self.tx.txid)
        log.info("Created schema: %s", path)

    def schema(self, path: str) -> "Schema":
        schema = self.schemas(path)
        log.debug("schema: %s", schema)
        if not schema:
            raise NotFoundError(f"Schema '{path}' was not found in bucket: {self.name}")
        assert len(schema) == 1, f"Expected to receive only a single schema, but got: {len(schema)}. ({schema})"
        log.info("Found schema: %s", schema[0].name)
        return schema[0]

    def schemas(self, schema: str = None) -> ["Schema"]:
        schemas = []
        next_key = 0
        exact_match = bool(schema)
        log.info("list schemas param: schema=%s, exact_match=%s", schema, exact_match)
        while True:
            bucket_name, curr_schemas, next_key, is_truncated, _ = \
                self.tx._rpc.api.list_schemas(bucket=self.name, next_key=next_key, txid=self.tx.txid,
                                               name_prefix=schema, exact_match=exact_match)
            if not curr_schemas:
                break
            schemas.extend(curr_schemas)
            if not is_truncated:
                break

        return [Schema(name=name, bucket=self) for name, *_ in schemas]


@dataclass
class Schema:
    name: str
    bucket: Bucket

    @property
    def tx(self):
        return self.bucket.tx

    def create_table(self, table_name: str, columns: pa.Schema) -> None:
        self.tx._rpc.api.create_table(self.bucket.name, self.name, table_name, columns, txid=self.tx.txid)
        log.info("Created table: %s", table_name)

    def table(self, name: str) -> "Table":
        t = self.tables(table_name=name)
        if not t:
            raise NotFoundError(f"Table '{name}' was not found under schema: {self.name}")
        assert len(t) == 1, f"Expected to receive only a single table, but got: {len(t)}. tables: {t}"
        log.info("Found table: %s", {t[0]})
        return t[0]

    def tables(self, table_name=None) -> ["Table"]:
        tables = []
        next_key = 0
        name_prefix = table_name if table_name else ""
        exact_match = bool(table_name)
        while True:
            bucket_name, schema_name, curr_tables, next_key, is_truncated, _ = \
                self.tx._rpc.api.list_tables(
                    bucket=self.bucket.name, schema=self.name, next_key=next_key, txid=self.tx.txid,
                    exact_match=exact_match, name_prefix=name_prefix)
            if not curr_tables:
                break
            tables.extend(curr_tables)
            if not is_truncated:
                break

        return [_parse_table_info(table, self) for table in tables]

    def drop(self) -> None:
        self.tx._rpc.api.drop_schema(self.bucket.name, self.name, txid=self.tx.txid)
        log.info("Dropped schema: %s", self.name)

    def rename(self, new_name) -> None:
        self.tx._rpc.api.alter_schema(self.bucket.name, self.name, txid=self.tx.txid, new_name=new_name)
        log.info("Renamed schema: %s to %s", self.name, new_name)
        self.name = new_name


class Table:
    def __init__(self, name: str, schema: Schema, properties: dict = None, handle: str = None, num_rows: int = 0,
                 size: int = 0, arrow_schema: pa.Schema = None):
        self.name = name
        self.schema = schema
        self.properties = properties if properties else {}
        self.handle = handle
        self.tx = schema.tx
        self.bucket = schema.bucket
        self.stats = TableStats(num_rows, size)
        self.arrow_schema = arrow_schema or self.columns()
        self._ibis_table = ibis.Schema.from_pyarrow(self.arrow_schema)

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name})"

    def columns(self) -> pa.Schema:
        cols = self.tx._rpc.api._list_table_columns(self.bucket.name, self.schema.name, self.name, txid=self.tx.txid)
        self.arrow_schema = pa.schema([(col[0], col[1]) for col in cols])
        return self.arrow_schema

    def import_files(self, files_to_import: [str]) -> None:
        source_files = {}
        for f in files_to_import:
            bucket_name, object_path = _parse_bucket_and_object_names(f)
            source_files[(bucket_name, object_path)] = b''

        self._execute_import(source_files)

    def import_partitioned_files(self, files_and_partitions: {str: pa.RecordBatch}) -> None:
        source_files = {}
        for f, record_batch in files_and_partitions.items():
            bucket_name, object_path = _parse_bucket_and_object_names(f)
            serialized_batch = _serialize_record_batch(record_batch)
            source_files = {(bucket_name, object_path): serialized_batch.to_pybytes()}

        self._execute_import(source_files)

    def _execute_import(self, source_files):
        try:
            self.tx._rpc.api.import_data(
                self.bucket.name, self.schema.name, self.name, source_files, txid=self.tx.txid)
        except requests.HTTPError as e:
            raise ImportFilesError(f"import_files failed with status: {e.response.status_code}, reason: {e.response.reason}")
        except Exception as e:
            # TODO: investigate and raise proper error in case of failure mid import.
            raise ImportFilesError("import_files failed") from e

    def select(self, column_names: [str], predicates: ibis.expr.types.BooleanColumn, limit: int = None,
               config: "QueryConfig" = None):
        raise NotImplemented

    def insert(self, rows: pa.RecordBatch) -> None:
        self.tx._rpc.api.insert(self.bucket.name, self.schema.name, self.name, record_batch=rows, txid=self.tx.txid)

    def drop(self) -> None:
        self.tx._rpc.api.drop_table(self.bucket.name, self.schema.name, self.name, txid=self.tx.txid)
        log.info("Dropped table: %s", self.name)

    def rename(self, new_name) -> None:
        self.tx._rpc.api.alter_table(
            self.bucket.name, self.schema.name, self.name, txid=self.tx.txid, new_name=new_name)
        log.info("Renamed table from %s to %s ", self.name, new_name)
        self.name = new_name

    def add_column(self, new_column: pa.Schema) -> None:
        self.tx._rpc.api.add_columns(self.bucket.name, self.schema.name, self.name, new_column, txid=self.tx.txid)
        log.info("Added column(s): %s", new_column)
        self.arrow_schema = self.columns()

    def drop_column(self, column_to_drop: pa.Schema) -> None:
        self.tx._rpc.api.drop_columns(self.bucket.name, self.schema.name, self.name, column_to_drop, txid=self.tx.txid)
        log.info("Dropped column(s): %s", column_to_drop)
        self.arrow_schema = self.columns()

    def rename_column(self, current_column_name: str, new_column_name: str) -> None:
        self.tx._rpc.api.alter_column(self.bucket.name, self.schema.name, self.name, name=current_column_name,
                                       new_name=new_column_name, txid=self.tx.txid)
        log.info("Renamed column: %s to %s", current_column_name, new_column_name)
        self.arrow_schema = self.columns()

    def __getitem__(self, col_name):
        return self._ibis_table[col_name]


def _parse_table_info(table_info, schema: "Schema"):
    return Table(name=table_info.name, schema=schema, properties=table_info.properties,
                 handle=table_info.handle, num_rows=table_info.num_rows, size=table_info.size_in_bytes)


def _parse_bucket_and_object_names(path: str) -> (str, str):
    if not path.startswith('/'):
        raise InvalidArgumentError(f"Path {path} must start with a '/'")
    components = path.split(os.path.sep)
    bucket_name = components[1]
    object_path = os.path.sep.join(components[2:])
    return bucket_name, object_path


def _serialize_record_batch(record_batch: pa.RecordBatch) -> pa.lib.Buffer:
    sink = pa.BufferOutputStream()
    with pa.ipc.new_stream(sink, record_batch.schema) as writer:
        writer.write(record_batch)
    return sink.getvalue()


def _parse_endpoint(endpoint):
    if ":" in endpoint:
        endpoint, port = endpoint.split(":")
        port = int(port)
    else:
        port = 80
    log.debug("endpoint: %s, port: %d", endpoint, port)
    return endpoint, port


@dataclass
class TableStats:
    num_rows: int
    size: int


@dataclass
class QueryConfig:
    num_sub_splits: int = 4
    num_splits: int = 16
    data_endpoints: [str] = None
    limit_per_sub_split: int = 128 * 1024
    num_row_groups_per_sub_split: int = 8
