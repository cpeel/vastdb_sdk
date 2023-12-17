# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatbuf

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# ----------------------------------------------------------------------
# Arrow File metadata
#
class Footer(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Footer()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsFooter(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # Footer
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Footer
    def Version(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int16Flags, o + self._tab.Pos)
        return 0

    # Footer
    def Schema(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from vast_flatbuf.org.apache.arrow.flatbuf.Schema import Schema
            obj = Schema()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Footer
    def Dictionaries(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 24
            from vast_flatbuf.org.apache.arrow.flatbuf.Block import Block
            obj = Block()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Footer
    def DictionariesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Footer
    def DictionariesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        return o == 0

    # Footer
    def RecordBatches(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 24
            from vast_flatbuf.org.apache.arrow.flatbuf.Block import Block
            obj = Block()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Footer
    def RecordBatchesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Footer
    def RecordBatchesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        return o == 0

    # User-defined metadata
    # Footer
    def CustomMetadata(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from vast_flatbuf.org.apache.arrow.flatbuf.KeyValue import KeyValue
            obj = KeyValue()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Footer
    def CustomMetadataLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Footer
    def CustomMetadataIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        return o == 0

def Start(builder): builder.StartObject(5)
def FooterStart(builder):
    """This method is deprecated. Please switch to Start."""
    return Start(builder)
def AddVersion(builder, version): builder.PrependInt16Slot(0, version, 0)
def FooterAddVersion(builder, version):
    """This method is deprecated. Please switch to AddVersion."""
    return AddVersion(builder, version)
def AddSchema(builder, schema): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(schema), 0)
def FooterAddSchema(builder, schema):
    """This method is deprecated. Please switch to AddSchema."""
    return AddSchema(builder, schema)
def AddDictionaries(builder, dictionaries): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(dictionaries), 0)
def FooterAddDictionaries(builder, dictionaries):
    """This method is deprecated. Please switch to AddDictionaries."""
    return AddDictionaries(builder, dictionaries)
def StartDictionariesVector(builder, numElems): return builder.StartVector(24, numElems, 8)
def FooterStartDictionariesVector(builder, numElems):
    """This method is deprecated. Please switch to Start."""
    return StartDictionariesVector(builder, numElems)
def AddRecordBatches(builder, recordBatches): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(recordBatches), 0)
def FooterAddRecordBatches(builder, recordBatches):
    """This method is deprecated. Please switch to AddRecordBatches."""
    return AddRecordBatches(builder, recordBatches)
def StartRecordBatchesVector(builder, numElems): return builder.StartVector(24, numElems, 8)
def FooterStartRecordBatchesVector(builder, numElems):
    """This method is deprecated. Please switch to Start."""
    return StartRecordBatchesVector(builder, numElems)
def AddCustomMetadata(builder, customMetadata): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(customMetadata), 0)
def FooterAddCustomMetadata(builder, customMetadata):
    """This method is deprecated. Please switch to AddCustomMetadata."""
    return AddCustomMetadata(builder, customMetadata)
def StartCustomMetadataVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def FooterStartCustomMetadataVector(builder, numElems):
    """This method is deprecated. Please switch to Start."""
    return StartCustomMetadataVector(builder, numElems)
def End(builder): return builder.EndObject()
def FooterEnd(builder):
    """This method is deprecated. Please switch to End."""
    return End(builder)