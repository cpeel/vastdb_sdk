# automatically generated by the FlatBuffers compiler, do not modify

# namespace: tabular

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class GetTableStatsResponse(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = GetTableStatsResponse()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsGetTableStatsResponse(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    # GetTableStatsResponse
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # GetTableStatsResponse
    def NumRows(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int64Flags, o + self._tab.Pos)
        return 0

    # GetTableStatsResponse
    def SizeInBytes(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int64Flags, o + self._tab.Pos)
        return 0

    # GetTableStatsResponse
    def IsExternalRowidAlloc(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # GetTableStatsResponse
    def AddressType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # GetTableStatsResponse
    def Vips(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from vast_flatbuf.tabular.VipRange import VipRange
            obj = VipRange()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # GetTableStatsResponse
    def VipsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # GetTableStatsResponse
    def VipsIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        return o == 0

def Start(builder): builder.StartObject(5)
def GetTableStatsResponseStart(builder):
    """This method is deprecated. Please switch to Start."""
    return Start(builder)
def AddNumRows(builder, numRows): builder.PrependInt64Slot(0, numRows, 0)
def GetTableStatsResponseAddNumRows(builder, numRows):
    """This method is deprecated. Please switch to AddNumRows."""
    return AddNumRows(builder, numRows)
def AddSizeInBytes(builder, sizeInBytes): builder.PrependInt64Slot(1, sizeInBytes, 0)
def GetTableStatsResponseAddSizeInBytes(builder, sizeInBytes):
    """This method is deprecated. Please switch to AddSizeInBytes."""
    return AddSizeInBytes(builder, sizeInBytes)
def AddIsExternalRowidAlloc(builder, isExternalRowidAlloc): builder.PrependBoolSlot(2, isExternalRowidAlloc, 0)
def GetTableStatsResponseAddIsExternalRowidAlloc(builder, isExternalRowidAlloc):
    """This method is deprecated. Please switch to AddIsExternalRowidAlloc."""
    return AddIsExternalRowidAlloc(builder, isExternalRowidAlloc)
def AddAddressType(builder, addressType): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(addressType), 0)
def GetTableStatsResponseAddAddressType(builder, addressType):
    """This method is deprecated. Please switch to AddAddressType."""
    return AddAddressType(builder, addressType)
def AddVips(builder, vips): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(vips), 0)
def GetTableStatsResponseAddVips(builder, vips):
    """This method is deprecated. Please switch to AddVips."""
    return AddVips(builder, vips)
def StartVipsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def GetTableStatsResponseStartVipsVector(builder, numElems):
    """This method is deprecated. Please switch to Start."""
    return StartVipsVector(builder, numElems)
def End(builder): return builder.EndObject()
def GetTableStatsResponseEnd(builder):
    """This method is deprecated. Please switch to End."""
    return End(builder)