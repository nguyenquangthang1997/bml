# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf/data.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor.FileDescriptor(
    name='protobuf/data.proto',
    package='',
    syntax='proto3',
    serialized_options=None,
    serialized_pb=_b(
        '\n\x13protobuf/data.proto\"\x14\n\x04\x44\x61ta\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\'\n\rDataContainer\x12\x16\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\x05.Datab\x06proto3')
)

_DATA = _descriptor.Descriptor(
    name='Data',
    full_name='Data',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='data', full_name='Data.data', index=0,
            number=1, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=_b("").decode('utf-8'),
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
    ],
    extensions=[
    ],
    nested_types=[],
    enum_types=[
    ],
    serialized_options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=23,
    serialized_end=43,
)

_DATACONTAINER = _descriptor.Descriptor(
    name='DataContainer',
    full_name='DataContainer',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='entries', full_name='DataContainer.entries', index=0,
            number=1, type=11, cpp_type=10, label=3,
            has_default_value=False, default_value=[],
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
    ],
    extensions=[
    ],
    nested_types=[],
    enum_types=[
    ],
    serialized_options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[
    ],
    serialized_start=45,
    serialized_end=84,
)

_DATACONTAINER.fields_by_name['entries'].message_type = _DATA
DESCRIPTOR.message_types_by_name['Data'] = _DATA
DESCRIPTOR.message_types_by_name['DataContainer'] = _DATACONTAINER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Data = _reflection.GeneratedProtocolMessageType('Data', (_message.Message,), {
    'DESCRIPTOR': _DATA,
    '__module__': 'protobuf.data_pb2'
    # @@protoc_insertion_point(class_scope:Data)
})
_sym_db.RegisterMessage(Data)

DataContainer = _reflection.GeneratedProtocolMessageType('DataContainer', (_message.Message,), {
    'DESCRIPTOR': _DATACONTAINER,
    '__module__': 'protobuf.data_pb2'
    # @@protoc_insertion_point(class_scope:DataContainer)
})
_sym_db.RegisterMessage(DataContainer)

# @@protoc_insertion_point(module_scope)
