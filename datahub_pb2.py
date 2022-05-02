"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='datahub.proto',
  package='feed',
  syntax='proto3',
  serialized_options=b'\n\024com.isharp.grpc.feedB\tFeedProtoP\001\242\002\003HLW',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rdatahub.proto\x12\x04\x66\x65\x65\x64\"F\n\nPricePoint\x12\x0c\n\x04year\x18\x01 \x01(\x05\x12\r\n\x05month\x18\x02 \x01(\x05\x12\x0c\n\x04\x64\x61te\x18\x03 \x01(\x05\x12\r\n\x05price\x18\x04 \x01(\x01\"Z\n\x05Patch\x12\"\n\tpatchtype\x18\x01 \x01(\x0e\x32\x0f.feed.PatchType\x12\x1c\n\x02pp\x18\x02 \x01(\x0b\x32\x10.feed.PricePoint\x12\x0f\n\x07\x63omment\x18\x03 \x01(\t\"Z\n\x0cPatchRequest\x12\x0c\n\x04safe\x18\x01 \x01(\x08\x12\x0b\n\x03url\x18\x02 \x01(\t\x12\x1a\n\x05patch\x18\x03 \x01(\x0b\x32\x0b.feed.Patch\x12\x13\n\x0b\x66orceCreate\x18\x04 \x01(\x08\" \n\rPatchResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08*#\n\tPatchType\x12\n\n\x06INSERT\x10\x00\x12\n\n\x06\x44\x45LETE\x10\x01\x32\x45\n\nApplyPatch\x12\x37\n\nApplyPatch\x12\x12.feed.PatchRequest\x1a\x13.feed.PatchResponse\"\x00\x42)\n\x14\x63om.isharp.grpc.feedB\tFeedProtoP\x01\xa2\x02\x03HLWb\x06proto3'
)

_PATCHTYPE = _descriptor.EnumDescriptor(
  name='PatchType',
  full_name='feed.PatchType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INSERT', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DELETE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=313,
  serialized_end=348,
)
_sym_db.RegisterEnumDescriptor(_PATCHTYPE)

PatchType = enum_type_wrapper.EnumTypeWrapper(_PATCHTYPE)
INSERT = 0
DELETE = 1



_PRICEPOINT = _descriptor.Descriptor(
  name='PricePoint',
  full_name='feed.PricePoint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='year', full_name='feed.PricePoint.year', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='month', full_name='feed.PricePoint.month', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='date', full_name='feed.PricePoint.date', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='price', full_name='feed.PricePoint.price', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_end=93,
)


_PATCH = _descriptor.Descriptor(
  name='Patch',
  full_name='feed.Patch',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='patchtype', full_name='feed.Patch.patchtype', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pp', full_name='feed.Patch.pp', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='comment', full_name='feed.Patch.comment', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=95,
  serialized_end=185,
)


_PATCHREQUEST = _descriptor.Descriptor(
  name='PatchRequest',
  full_name='feed.PatchRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='safe', full_name='feed.PatchRequest.safe', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='feed.PatchRequest.url', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='patch', full_name='feed.PatchRequest.patch', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='forceCreate', full_name='feed.PatchRequest.forceCreate', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=187,
  serialized_end=277,
)


_PATCHRESPONSE = _descriptor.Descriptor(
  name='PatchResponse',
  full_name='feed.PatchResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='feed.PatchResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=279,
  serialized_end=311,
)

_PATCH.fields_by_name['patchtype'].enum_type = _PATCHTYPE
_PATCH.fields_by_name['pp'].message_type = _PRICEPOINT
_PATCHREQUEST.fields_by_name['patch'].message_type = _PATCH
DESCRIPTOR.message_types_by_name['PricePoint'] = _PRICEPOINT
DESCRIPTOR.message_types_by_name['Patch'] = _PATCH
DESCRIPTOR.message_types_by_name['PatchRequest'] = _PATCHREQUEST
DESCRIPTOR.message_types_by_name['PatchResponse'] = _PATCHRESPONSE
DESCRIPTOR.enum_types_by_name['PatchType'] = _PATCHTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PricePoint = _reflection.GeneratedProtocolMessageType('PricePoint', (_message.Message,), {
  'DESCRIPTOR' : _PRICEPOINT,
  '__module__' : 'datahub_pb2'
  # @@protoc_insertion_point(class_scope:feed.PricePoint)
  })
_sym_db.RegisterMessage(PricePoint)

Patch = _reflection.GeneratedProtocolMessageType('Patch', (_message.Message,), {
  'DESCRIPTOR' : _PATCH,
  '__module__' : 'datahub_pb2'
  # @@protoc_insertion_point(class_scope:feed.Patch)
  })
_sym_db.RegisterMessage(Patch)

PatchRequest = _reflection.GeneratedProtocolMessageType('PatchRequest', (_message.Message,), {
  'DESCRIPTOR' : _PATCHREQUEST,
  '__module__' : 'datahub_pb2'
  # @@protoc_insertion_point(class_scope:feed.PatchRequest)
  })
_sym_db.RegisterMessage(PatchRequest)

PatchResponse = _reflection.GeneratedProtocolMessageType('PatchResponse', (_message.Message,), {
  'DESCRIPTOR' : _PATCHRESPONSE,
  '__module__' : 'datahub_pb2'
  # @@protoc_insertion_point(class_scope:feed.PatchResponse)
  })
_sym_db.RegisterMessage(PatchResponse)


DESCRIPTOR._options = None

_APPLYPATCH = _descriptor.ServiceDescriptor(
  name='ApplyPatch',
  full_name='feed.ApplyPatch',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=350,
  serialized_end=419,
  methods=[
  _descriptor.MethodDescriptor(
    name='ApplyPatch',
    full_name='feed.ApplyPatch.ApplyPatch',
    index=0,
    containing_service=None,
    input_type=_PATCHREQUEST,
    output_type=_PATCHRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_APPLYPATCH)

DESCRIPTOR.services_by_name['ApplyPatch'] = _APPLYPATCH

# @@protoc_insertion_point(module_scope)
