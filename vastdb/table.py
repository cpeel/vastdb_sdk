from . import errors, schema
from .internal_commands import serialize_record_batch, build_query_data_request, parse_query_data_response, TABULAR_INVALID_ROW_ID


import pyarrow as pa
import ibis

from dataclasses import dataclass, field
from typing import List, Union
import logging
import os

log = logging.getLogger(__name__)



INTERNAL_ROW_ID = "$row_id"

@dataclass
class TableStats:
    num_rows: int
    size: int


@dataclass
class QueryConfig:
    num_sub_splits: int = 4
    num_splits: int = 1
    data_endpoints: [str] = None
    limit_rows_per_sub_split: int = 128 * 1024
    num_row_groups_per_sub_split: int = 8
    use_semi_sorted_projections: bool = True
    rows_per_split: int = 4000000

@dataclass
class Table:
    name: str
    schema: "schema.Schema"
    handle: int
    stats: TableStats
    properties: dict = None
    arrow_schema: pa.Schema = field(init=False, compare=False)
    _ibis_table: ibis.Schema = field(init=False, compare=False)

    def __post_init__(self):
        self.properties = self.properties or {}
        self.arrow_schema = self.columns()

        table_path = f'{self.schema.bucket.name}/{self.schema.name}/{self.name}'
        self._ibis_table = ibis.table(ibis.Schema.from_pyarrow(self.arrow_schema), table_path)

    @property
    def tx(self):
        return self.schema.tx

    @property
    def bucket(self):
        return self.schema.bucket

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name})"

    def columns(self) -> pa.Schema:
        cols = self.tx._rpc.api._list_table_columns(self.bucket.name, self.schema.name, self.name, txid=self.tx.txid)
        self.arrow_schema = pa.schema([(col[0], col[1]) for col in cols])
        return self.arrow_schema

    def projection(self, name: str) -> "Projection":
        projs = self.projections(projection_name=name)
        if not projs:
            raise errors.NotFoundError(f"Projection '{name}' was not found under table: {self.name}")
        assert len(projs) == 1, f"Expected to receive only a single projection, but got: {len(projs)}. projections: {projs}"
        log.debug("Found projection: %s", projs[0])
        return projs[0]

    def projections(self, projection_name=None) -> ["Projection"]:
        projections = []
        next_key = 0
        name_prefix = projection_name if projection_name else ""
        exact_match = bool(projection_name)
        while True:
            bucket_name, schema_name, table_name, curr_projections, next_key, is_truncated, _ = \
                self.tx._rpc.api.list_projections(
                    bucket=self.bucket.name, schema=self.schema.name, table=self.name, next_key=next_key, txid=self.tx.txid,
                    exact_match=exact_match, name_prefix=name_prefix)
            if not curr_projections:
                break
            projections.extend(curr_projections)
            if not is_truncated:
                break
        return [_parse_projection_info(projection, self) for projection in projections]

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
        self.tx._rpc.api.import_data(
            self.bucket.name, self.schema.name, self.name, source_files, txid=self.tx.txid)

    def select(self, columns: [str] = None,
               predicate: ibis.expr.types.BooleanColumn = None,
               config: "QueryConfig" = None,
               *,
               internal_row_id = False) -> pa.RecordBatchReader:
        if config is None:
            config = QueryConfig()

        num_rows, size_in_bytes, _ = self.tx._rpc.api.get_table_stats(
            bucket=self.bucket.name, schema=self.schema.name, name=self.name, txid=self.tx.txid)
        self.stats = TableStats(num_rows=num_rows, size=size_in_bytes)
        if self.stats.num_rows > config.rows_per_split:
            config.num_splits = self.stats.num_rows // config.rows_per_split
        log.debug(f"num_rows={self.stats.num_rows} rows_per_splits={config.rows_per_split} num_splits={config.num_splits} ")

        query_schema = self.arrow_schema
        if internal_row_id:
            queried_fields = [pa.field(INTERNAL_ROW_ID, pa.uint64())]
            queried_fields.extend(column for column in self.arrow_schema)
            query_schema = pa.schema(queried_fields)
            columns.append(INTERNAL_ROW_ID)

        query_data_request = build_query_data_request(
            schema=query_schema,
            predicate=predicate,
            field_names=columns)


        splits = [(i, config.num_splits, config.num_row_groups_per_sub_split) for i in range(config.num_splits)]
        response_row_id = False
        def batches_iterator(for_split):
            while not all(row_id == TABULAR_INVALID_ROW_ID for row_id in start_row_ids.values()):
                response = self.tx._rpc.api.query_data(
                    bucket=self.bucket.name,
                    schema=self.schema.name,
                    table=self.name,
                    params=query_data_request.serialized,
                    split=for_split,
                    num_sub_splits=config.num_sub_splits,
                    response_row_id=response_row_id,
                    txid=self.tx.txid,
                    limit_rows=config.limit_rows_per_sub_split,
                    sub_split_start_row_ids=start_row_ids.items(),
                    enable_sorted_projections=config.use_semi_sorted_projections)

                pages_iter = parse_query_data_response(
                    conn=response.raw,
                    schema=query_data_request.response_schema,
                    start_row_ids=start_row_ids)

                for page in pages_iter:
                    for batch in page.to_batches():
                        if len(batch) > 0:
                            yield batch

        record_batches = []
        for split in splits:
            start_row_ids = {i: 0 for i in range(config.num_sub_splits)}
            curr_record_batch = pa.RecordBatchReader.from_batches(query_data_request.response_schema.arrow_schema, batches_iterator(split))
            record_batches.extend(curr_record_batch)

        return pa.RecordBatchReader.from_batches(query_data_request.response_schema.arrow_schema, record_batches)

    def _combine_chunks(self, col):
        if hasattr(col, "combine_chunks"):
            return col.combine_chunks()
        else:
            return col


    def insert(self, rows: pa.RecordBatch) -> pa.RecordBatch:
        blob = serialize_record_batch(rows)
        res = self.tx._rpc.api.insert_rows(self.bucket.name, self.schema.name, self.name, record_batch=blob, txid=self.tx.txid)
        (batch,) = pa.RecordBatchStreamReader(res.raw)
        return batch

    def update(self, rows: Union[pa.RecordBatch, pa.Table], columns: list = None) -> None:
        if columns is not None:
            update_fields = [(INTERNAL_ROW_ID, pa.uint64())]
            update_values = [self._combine_chunks(rows[INTERNAL_ROW_ID])]
            for col in columns:
                update_fields.append(rows.field(col))
                update_values.append(self._combine_chunks(rows[col]))

            update_rows_rb = pa.record_batch(schema=pa.schema(update_fields), data=update_values)
        else:
            update_rows_rb = rows

        blob = serialize_record_batch(update_rows_rb)
        self.tx._rpc.api.update_rows(self.bucket.name, self.schema.name, self.name, record_batch=blob, txid=self.tx.txid)

    def delete(self, rows: Union[pa.RecordBatch, pa.Table]) -> None:
        delete_rows_rb = pa.record_batch(schema=pa.schema([(INTERNAL_ROW_ID, pa.uint64())]),
                                         data=[self._combine_chunks(rows[INTERNAL_ROW_ID])])

        blob = serialize_record_batch(delete_rows_rb)
        self.tx._rpc.api.delete_rows(self.bucket.name, self.schema.name, self.name, record_batch=blob, txid=self.tx.txid)

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

    def create_projection(self, projection_name: str, sorted_columns: List[str], unsorted_columns: List[str]) -> "Projection":
        columns = [(sorted_column, "Sorted") for sorted_column in sorted_columns] + [(unsorted_column, "Unorted") for unsorted_column in unsorted_columns]
        self.tx._rpc.api.create_projection(self.bucket.name, self.schema.name, self.name, projection_name, columns=columns, txid=self.tx.txid)
        log.info("Created projectin: %s", projection_name)
        return self.projection(projection_name)

    def __getitem__(self, col_name):
        return self._ibis_table[col_name]


@dataclass
class Projection:
    name: str
    table: Table
    handle: int
    stats: TableStats
    properties: dict = None

    @property
    def bucket(self):
        return self.table.schema.bucket

    @property
    def schema(self):
        return self.table.schema

    @property
    def tx(self):
        return self.table.schema.tx

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name})"

    def columns(self) -> pa.Schema:
        columns = []
        next_key = 0
        while True:
            curr_columns, next_key, is_truncated, count, _ = \
                self.tx._rpc.api.list_projection_columns(
                    self.bucket.name, self.schema.name, self.table.name, self.name, txid=self.table.tx.txid, next_key=next_key)
            if not curr_columns:
                break
            columns.extend(curr_columns)
            if not is_truncated:
                break
        self.arrow_schema = pa.schema([(col[0], col[1]) for col in columns])
        return self.arrow_schema

    def rename(self, new_name) -> None:
        self.tx._rpc.api.alter_projection(self.bucket.name, self.schema.name,
                                                self.table.name, self.name, txid=self.tx.txid, new_name=new_name)
        log.info("Renamed projection from %s to %s ", self.name, new_name)
        self.name = new_name

    def drop(self) -> None:
        self.tx._rpc.api.drop_projection(self.bucket.name, self.schema.name, self.table.name,
                                         self.name, txid=self.tx.txid)
        log.info("Dropped projection: %s", self.name)


def _parse_projection_info(projection_info, table: "Table"):
    log.info("Projection info %s", str(projection_info))
    stats = TableStats(num_rows=projection_info.num_rows, size=projection_info.size_in_bytes)
    return Projection(name=projection_info.name, table=table, stats=stats, handle=int(projection_info.handle))


def _parse_bucket_and_object_names(path: str) -> (str, str):
    if not path.startswith('/'):
        raise errors.InvalidArgumentError(f"Path {path} must start with a '/'")
    components = path.split(os.path.sep)
    bucket_name = components[1]
    object_path = os.path.sep.join(components[2:])
    return bucket_name, object_path


def _serialize_record_batch(record_batch: pa.RecordBatch) -> pa.lib.Buffer:
    sink = pa.BufferOutputStream()
    with pa.ipc.new_stream(sink, record_batch.schema) as writer:
        writer.write(record_batch)
    return sink.getvalue()