# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: vast_protobuf/substrait/function.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from vast_protobuf.substrait import parameterized_types_pb2 as vast__protobuf_dot_substrait_dot_parameterized__types__pb2
from vast_protobuf.substrait import type_pb2 as vast__protobuf_dot_substrait_dot_type__pb2
from vast_protobuf.substrait import type_expressions_pb2 as vast__protobuf_dot_substrait_dot_type__expressions__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&vast_protobuf/substrait/function.proto\x12\tsubstrait\x1a\x31vast_protobuf/substrait/parameterized_types.proto\x1a\"vast_protobuf/substrait/type.proto\x1a.vast_protobuf/substrait/type_expressions.proto\"\xc1\x15\n\x11\x46unctionSignature\x1a\x9d\x02\n\x10\x46inalArgVariadic\x12\x10\n\x08min_args\x18\x01 \x01(\x03\x12\x10\n\x08max_args\x18\x02 \x01(\x03\x12W\n\x0b\x63onsistency\x18\x03 \x01(\x0e\x32\x42.substrait.FunctionSignature.FinalArgVariadic.ParameterConsistency\"\x8b\x01\n\x14ParameterConsistency\x12%\n!PARAMETER_CONSISTENCY_UNSPECIFIED\x10\x00\x12$\n PARAMETER_CONSISTENCY_CONSISTENT\x10\x01\x12&\n\"PARAMETER_CONSISTENCY_INCONSISTENT\x10\x02\x1a\x10\n\x0e\x46inalArgNormal\x1a\xda\x03\n\x06Scalar\x12\x38\n\targuments\x18\x02 \x03(\x0b\x32%.substrait.FunctionSignature.Argument\x12\x0c\n\x04name\x18\x03 \x03(\t\x12=\n\x0b\x64\x65scription\x18\x04 \x01(\x0b\x32(.substrait.FunctionSignature.Description\x12\x15\n\rdeterministic\x18\x07 \x01(\x08\x12\x19\n\x11session_dependent\x18\x08 \x01(\x08\x12\x34\n\x0boutput_type\x18\t \x01(\x0b\x32\x1f.substrait.DerivationExpression\x12\x41\n\x08variadic\x18\n \x01(\x0b\x32-.substrait.FunctionSignature.FinalArgVariadicH\x00\x12=\n\x06normal\x18\x0b \x01(\x0b\x32+.substrait.FunctionSignature.FinalArgNormalH\x00\x12\x44\n\x0fimplementations\x18\x0c \x03(\x0b\x32+.substrait.FunctionSignature.ImplementationB\x19\n\x17\x66inal_variable_behavior\x1a\xab\x04\n\tAggregate\x12\x38\n\targuments\x18\x02 \x03(\x0b\x32%.substrait.FunctionSignature.Argument\x12\x0c\n\x04name\x18\x03 \x01(\t\x12=\n\x0b\x64\x65scription\x18\x04 \x01(\x0b\x32(.substrait.FunctionSignature.Description\x12\x15\n\rdeterministic\x18\x07 \x01(\x08\x12\x19\n\x11session_dependent\x18\x08 \x01(\x08\x12\x34\n\x0boutput_type\x18\t \x01(\x0b\x32\x1f.substrait.DerivationExpression\x12\x41\n\x08variadic\x18\n \x01(\x0b\x32-.substrait.FunctionSignature.FinalArgVariadicH\x00\x12=\n\x06normal\x18\x0b \x01(\x0b\x32+.substrait.FunctionSignature.FinalArgNormalH\x00\x12\x0f\n\x07ordered\x18\x0e \x01(\x08\x12\x0f\n\x07max_set\x18\x0c \x01(\x04\x12*\n\x11intermediate_type\x18\r \x01(\x0b\x32\x0f.substrait.Type\x12\x44\n\x0fimplementations\x18\x0f \x03(\x0b\x32+.substrait.FunctionSignature.ImplementationB\x19\n\x17\x66inal_variable_behavior\x1a\xde\x05\n\x06Window\x12\x38\n\targuments\x18\x02 \x03(\x0b\x32%.substrait.FunctionSignature.Argument\x12\x0c\n\x04name\x18\x03 \x03(\t\x12=\n\x0b\x64\x65scription\x18\x04 \x01(\x0b\x32(.substrait.FunctionSignature.Description\x12\x15\n\rdeterministic\x18\x07 \x01(\x08\x12\x19\n\x11session_dependent\x18\x08 \x01(\x08\x12:\n\x11intermediate_type\x18\t \x01(\x0b\x32\x1f.substrait.DerivationExpression\x12\x34\n\x0boutput_type\x18\n \x01(\x0b\x32\x1f.substrait.DerivationExpression\x12\x41\n\x08variadic\x18\x10 \x01(\x0b\x32-.substrait.FunctionSignature.FinalArgVariadicH\x00\x12=\n\x06normal\x18\x11 \x01(\x0b\x32+.substrait.FunctionSignature.FinalArgNormalH\x00\x12\x0f\n\x07ordered\x18\x0b \x01(\x08\x12\x0f\n\x07max_set\x18\x0c \x01(\x04\x12\x43\n\x0bwindow_type\x18\x0e \x01(\x0e\x32..substrait.FunctionSignature.Window.WindowType\x12\x44\n\x0fimplementations\x18\x0f \x03(\x0b\x32+.substrait.FunctionSignature.Implementation\"_\n\nWindowType\x12\x1b\n\x17WINDOW_TYPE_UNSPECIFIED\x10\x00\x12\x19\n\x15WINDOW_TYPE_STREAMING\x10\x01\x12\x19\n\x15WINDOW_TYPE_PARTITION\x10\x02\x42\x19\n\x17\x66inal_variable_behavior\x1a-\n\x0b\x44\x65scription\x12\x10\n\x08language\x18\x01 \x01(\t\x12\x0c\n\x04\x62ody\x18\x02 \x01(\t\x1a\xa6\x01\n\x0eImplementation\x12>\n\x04type\x18\x01 \x01(\x0e\x32\x30.substrait.FunctionSignature.Implementation.Type\x12\x0b\n\x03uri\x18\x02 \x01(\t\"G\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\x15\n\x11TYPE_WEB_ASSEMBLY\x10\x01\x12\x12\n\x0eTYPE_TRINO_JAR\x10\x02\x1a\xb5\x03\n\x08\x41rgument\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x44\n\x05value\x18\x02 \x01(\x0b\x32\x33.substrait.FunctionSignature.Argument.ValueArgumentH\x00\x12\x42\n\x04type\x18\x03 \x01(\x0b\x32\x32.substrait.FunctionSignature.Argument.TypeArgumentH\x00\x12\x42\n\x04\x65num\x18\x04 \x01(\x0b\x32\x32.substrait.FunctionSignature.Argument.EnumArgumentH\x00\x1aM\n\rValueArgument\x12*\n\x04type\x18\x01 \x01(\x0b\x32\x1c.substrait.ParameterizedType\x12\x10\n\x08\x63onstant\x18\x02 \x01(\x08\x1a:\n\x0cTypeArgument\x12*\n\x04type\x18\x01 \x01(\x0b\x32\x1c.substrait.ParameterizedType\x1a\x31\n\x0c\x45numArgument\x12\x0f\n\x07options\x18\x01 \x03(\t\x12\x10\n\x08optional\x18\x02 \x01(\x08\x42\x0f\n\rargument_kindBW\n\x12io.substrait.protoP\x01Z*github.com/substrait-io/substrait-go/proto\xaa\x02\x12Substrait.Protobufb\x06proto3')



_FUNCTIONSIGNATURE = DESCRIPTOR.message_types_by_name['FunctionSignature']
_FUNCTIONSIGNATURE_FINALARGVARIADIC = _FUNCTIONSIGNATURE.nested_types_by_name['FinalArgVariadic']
_FUNCTIONSIGNATURE_FINALARGNORMAL = _FUNCTIONSIGNATURE.nested_types_by_name['FinalArgNormal']
_FUNCTIONSIGNATURE_SCALAR = _FUNCTIONSIGNATURE.nested_types_by_name['Scalar']
_FUNCTIONSIGNATURE_AGGREGATE = _FUNCTIONSIGNATURE.nested_types_by_name['Aggregate']
_FUNCTIONSIGNATURE_WINDOW = _FUNCTIONSIGNATURE.nested_types_by_name['Window']
_FUNCTIONSIGNATURE_DESCRIPTION = _FUNCTIONSIGNATURE.nested_types_by_name['Description']
_FUNCTIONSIGNATURE_IMPLEMENTATION = _FUNCTIONSIGNATURE.nested_types_by_name['Implementation']
_FUNCTIONSIGNATURE_ARGUMENT = _FUNCTIONSIGNATURE.nested_types_by_name['Argument']
_FUNCTIONSIGNATURE_ARGUMENT_VALUEARGUMENT = _FUNCTIONSIGNATURE_ARGUMENT.nested_types_by_name['ValueArgument']
_FUNCTIONSIGNATURE_ARGUMENT_TYPEARGUMENT = _FUNCTIONSIGNATURE_ARGUMENT.nested_types_by_name['TypeArgument']
_FUNCTIONSIGNATURE_ARGUMENT_ENUMARGUMENT = _FUNCTIONSIGNATURE_ARGUMENT.nested_types_by_name['EnumArgument']
_FUNCTIONSIGNATURE_FINALARGVARIADIC_PARAMETERCONSISTENCY = _FUNCTIONSIGNATURE_FINALARGVARIADIC.enum_types_by_name['ParameterConsistency']
_FUNCTIONSIGNATURE_WINDOW_WINDOWTYPE = _FUNCTIONSIGNATURE_WINDOW.enum_types_by_name['WindowType']
_FUNCTIONSIGNATURE_IMPLEMENTATION_TYPE = _FUNCTIONSIGNATURE_IMPLEMENTATION.enum_types_by_name['Type']
FunctionSignature = _reflection.GeneratedProtocolMessageType('FunctionSignature', (_message.Message,), {

  'FinalArgVariadic' : _reflection.GeneratedProtocolMessageType('FinalArgVariadic', (_message.Message,), {
    'DESCRIPTOR' : _FUNCTIONSIGNATURE_FINALARGVARIADIC,
    '__module__' : 'vast_protobuf.substrait.function_pb2'
    # @@protoc_insertion_point(class_scope:substrait.FunctionSignature.FinalArgVariadic)
    })
  ,

  'FinalArgNormal' : _reflection.GeneratedProtocolMessageType('FinalArgNormal', (_message.Message,), {
    'DESCRIPTOR' : _FUNCTIONSIGNATURE_FINALARGNORMAL,
    '__module__' : 'vast_protobuf.substrait.function_pb2'
    # @@protoc_insertion_point(class_scope:substrait.FunctionSignature.FinalArgNormal)
    })
  ,

  'Scalar' : _reflection.GeneratedProtocolMessageType('Scalar', (_message.Message,), {
    'DESCRIPTOR' : _FUNCTIONSIGNATURE_SCALAR,
    '__module__' : 'vast_protobuf.substrait.function_pb2'
    # @@protoc_insertion_point(class_scope:substrait.FunctionSignature.Scalar)
    })
  ,

  'Aggregate' : _reflection.GeneratedProtocolMessageType('Aggregate', (_message.Message,), {
    'DESCRIPTOR' : _FUNCTIONSIGNATURE_AGGREGATE,
    '__module__' : 'vast_protobuf.substrait.function_pb2'
    # @@protoc_insertion_point(class_scope:substrait.FunctionSignature.Aggregate)
    })
  ,

  'Window' : _reflection.GeneratedProtocolMessageType('Window', (_message.Message,), {
    'DESCRIPTOR' : _FUNCTIONSIGNATURE_WINDOW,
    '__module__' : 'vast_protobuf.substrait.function_pb2'
    # @@protoc_insertion_point(class_scope:substrait.FunctionSignature.Window)
    })
  ,

  'Description' : _reflection.GeneratedProtocolMessageType('Description', (_message.Message,), {
    'DESCRIPTOR' : _FUNCTIONSIGNATURE_DESCRIPTION,
    '__module__' : 'vast_protobuf.substrait.function_pb2'
    # @@protoc_insertion_point(class_scope:substrait.FunctionSignature.Description)
    })
  ,

  'Implementation' : _reflection.GeneratedProtocolMessageType('Implementation', (_message.Message,), {
    'DESCRIPTOR' : _FUNCTIONSIGNATURE_IMPLEMENTATION,
    '__module__' : 'vast_protobuf.substrait.function_pb2'
    # @@protoc_insertion_point(class_scope:substrait.FunctionSignature.Implementation)
    })
  ,

  'Argument' : _reflection.GeneratedProtocolMessageType('Argument', (_message.Message,), {

    'ValueArgument' : _reflection.GeneratedProtocolMessageType('ValueArgument', (_message.Message,), {
      'DESCRIPTOR' : _FUNCTIONSIGNATURE_ARGUMENT_VALUEARGUMENT,
      '__module__' : 'vast_protobuf.substrait.function_pb2'
      # @@protoc_insertion_point(class_scope:substrait.FunctionSignature.Argument.ValueArgument)
      })
    ,

    'TypeArgument' : _reflection.GeneratedProtocolMessageType('TypeArgument', (_message.Message,), {
      'DESCRIPTOR' : _FUNCTIONSIGNATURE_ARGUMENT_TYPEARGUMENT,
      '__module__' : 'vast_protobuf.substrait.function_pb2'
      # @@protoc_insertion_point(class_scope:substrait.FunctionSignature.Argument.TypeArgument)
      })
    ,

    'EnumArgument' : _reflection.GeneratedProtocolMessageType('EnumArgument', (_message.Message,), {
      'DESCRIPTOR' : _FUNCTIONSIGNATURE_ARGUMENT_ENUMARGUMENT,
      '__module__' : 'vast_protobuf.substrait.function_pb2'
      # @@protoc_insertion_point(class_scope:substrait.FunctionSignature.Argument.EnumArgument)
      })
    ,
    'DESCRIPTOR' : _FUNCTIONSIGNATURE_ARGUMENT,
    '__module__' : 'vast_protobuf.substrait.function_pb2'
    # @@protoc_insertion_point(class_scope:substrait.FunctionSignature.Argument)
    })
  ,
  'DESCRIPTOR' : _FUNCTIONSIGNATURE,
  '__module__' : 'vast_protobuf.substrait.function_pb2'
  # @@protoc_insertion_point(class_scope:substrait.FunctionSignature)
  })
_sym_db.RegisterMessage(FunctionSignature)
_sym_db.RegisterMessage(FunctionSignature.FinalArgVariadic)
_sym_db.RegisterMessage(FunctionSignature.FinalArgNormal)
_sym_db.RegisterMessage(FunctionSignature.Scalar)
_sym_db.RegisterMessage(FunctionSignature.Aggregate)
_sym_db.RegisterMessage(FunctionSignature.Window)
_sym_db.RegisterMessage(FunctionSignature.Description)
_sym_db.RegisterMessage(FunctionSignature.Implementation)
_sym_db.RegisterMessage(FunctionSignature.Argument)
_sym_db.RegisterMessage(FunctionSignature.Argument.ValueArgument)
_sym_db.RegisterMessage(FunctionSignature.Argument.TypeArgument)
_sym_db.RegisterMessage(FunctionSignature.Argument.EnumArgument)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\022io.substrait.protoP\001Z*github.com/substrait-io/substrait-go/proto\252\002\022Substrait.Protobuf'
  _FUNCTIONSIGNATURE._serialized_start=189
  _FUNCTIONSIGNATURE._serialized_end=2942
  _FUNCTIONSIGNATURE_FINALARGVARIADIC._serialized_start=211
  _FUNCTIONSIGNATURE_FINALARGVARIADIC._serialized_end=496
  _FUNCTIONSIGNATURE_FINALARGVARIADIC_PARAMETERCONSISTENCY._serialized_start=357
  _FUNCTIONSIGNATURE_FINALARGVARIADIC_PARAMETERCONSISTENCY._serialized_end=496
  _FUNCTIONSIGNATURE_FINALARGNORMAL._serialized_start=498
  _FUNCTIONSIGNATURE_FINALARGNORMAL._serialized_end=514
  _FUNCTIONSIGNATURE_SCALAR._serialized_start=517
  _FUNCTIONSIGNATURE_SCALAR._serialized_end=991
  _FUNCTIONSIGNATURE_AGGREGATE._serialized_start=994
  _FUNCTIONSIGNATURE_AGGREGATE._serialized_end=1549
  _FUNCTIONSIGNATURE_WINDOW._serialized_start=1552
  _FUNCTIONSIGNATURE_WINDOW._serialized_end=2286
  _FUNCTIONSIGNATURE_WINDOW_WINDOWTYPE._serialized_start=2164
  _FUNCTIONSIGNATURE_WINDOW_WINDOWTYPE._serialized_end=2259
  _FUNCTIONSIGNATURE_DESCRIPTION._serialized_start=2288
  _FUNCTIONSIGNATURE_DESCRIPTION._serialized_end=2333
  _FUNCTIONSIGNATURE_IMPLEMENTATION._serialized_start=2336
  _FUNCTIONSIGNATURE_IMPLEMENTATION._serialized_end=2502
  _FUNCTIONSIGNATURE_IMPLEMENTATION_TYPE._serialized_start=2431
  _FUNCTIONSIGNATURE_IMPLEMENTATION_TYPE._serialized_end=2502
  _FUNCTIONSIGNATURE_ARGUMENT._serialized_start=2505
  _FUNCTIONSIGNATURE_ARGUMENT._serialized_end=2942
  _FUNCTIONSIGNATURE_ARGUMENT_VALUEARGUMENT._serialized_start=2737
  _FUNCTIONSIGNATURE_ARGUMENT_VALUEARGUMENT._serialized_end=2814
  _FUNCTIONSIGNATURE_ARGUMENT_TYPEARGUMENT._serialized_start=2816
  _FUNCTIONSIGNATURE_ARGUMENT_TYPEARGUMENT._serialized_end=2874
  _FUNCTIONSIGNATURE_ARGUMENT_ENUMARGUMENT._serialized_start=2876
  _FUNCTIONSIGNATURE_ARGUMENT_ENUMARGUMENT._serialized_end=2925
# @@protoc_insertion_point(module_scope)
