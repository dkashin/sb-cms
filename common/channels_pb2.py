# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: channels.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
import services_pb2 as services__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='channels.proto',
  package='stabox',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0e\x63hannels.proto\x12\x06stabox\x1a\x1cgoogle/api/annotations.proto\x1a\x0eservices.proto\"*\n\x07\x43hannel\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x12\n\nchannel_id\x18\x02 \x01(\r\"\x85\x01\n\x07Program\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x12\n\nprogram_id\x18\x02 \x01(\r\x12\x12\n\nchannel_id\x18\x03 \x01(\r\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x11\n\tstarts_at\x18\x06 \x01(\r\x12\x0f\n\x07\x65nds_at\x18\x07 \x01(\r\"w\n\x06Stream\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x11\n\tstream_id\x18\x02 \x01(\r\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x11\n\x07\x65nabled\x18\x04 \x01(\x08H\x00\x12 \n\x07service\x18\x05 \x01(\x0b\x32\x0f.stabox.ServiceB\n\n\x08\x65nabled_2\xab\x01\n\x08\x43hannels\x12:\n\x13getAvailableStreams\x12\x0f.stabox.Channel\x1a\x0e.stabox.Stream\"\x00\x30\x01\x12\x30\n\ngetProgram\x12\x0f.stabox.Program\x1a\x0f.stabox.Program\"\x00\x12\x31\n\x0b\x66indProgram\x12\x0f.stabox.Program\x1a\x0f.stabox.Program\"\x00\x62\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,services__pb2.DESCRIPTOR,])




_CHANNEL = _descriptor.Descriptor(
  name='Channel',
  full_name='stabox.Channel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='_id', full_name='stabox.Channel._id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='channel_id', full_name='stabox.Channel.channel_id', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=72,
  serialized_end=114,
)


_PROGRAM = _descriptor.Descriptor(
  name='Program',
  full_name='stabox.Program',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='_id', full_name='stabox.Program._id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='program_id', full_name='stabox.Program.program_id', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='channel_id', full_name='stabox.Program.channel_id', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='stabox.Program.name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='stabox.Program.description', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='starts_at', full_name='stabox.Program.starts_at', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ends_at', full_name='stabox.Program.ends_at', index=6,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=117,
  serialized_end=250,
)


_STREAM = _descriptor.Descriptor(
  name='Stream',
  full_name='stabox.Stream',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='_id', full_name='stabox.Stream._id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stream_id', full_name='stabox.Stream.stream_id', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='stabox.Stream.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enabled', full_name='stabox.Stream.enabled', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='service', full_name='stabox.Stream.service', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
    _descriptor.OneofDescriptor(
      name='enabled_', full_name='stabox.Stream.enabled_',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=252,
  serialized_end=371,
)

_STREAM.fields_by_name['service'].message_type = services__pb2._SERVICE
_STREAM.oneofs_by_name['enabled_'].fields.append(
  _STREAM.fields_by_name['enabled'])
_STREAM.fields_by_name['enabled'].containing_oneof = _STREAM.oneofs_by_name['enabled_']
DESCRIPTOR.message_types_by_name['Channel'] = _CHANNEL
DESCRIPTOR.message_types_by_name['Program'] = _PROGRAM
DESCRIPTOR.message_types_by_name['Stream'] = _STREAM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Channel = _reflection.GeneratedProtocolMessageType('Channel', (_message.Message,), {
  'DESCRIPTOR' : _CHANNEL,
  '__module__' : 'channels_pb2'
  # @@protoc_insertion_point(class_scope:stabox.Channel)
  })
_sym_db.RegisterMessage(Channel)

Program = _reflection.GeneratedProtocolMessageType('Program', (_message.Message,), {
  'DESCRIPTOR' : _PROGRAM,
  '__module__' : 'channels_pb2'
  # @@protoc_insertion_point(class_scope:stabox.Program)
  })
_sym_db.RegisterMessage(Program)

Stream = _reflection.GeneratedProtocolMessageType('Stream', (_message.Message,), {
  'DESCRIPTOR' : _STREAM,
  '__module__' : 'channels_pb2'
  # @@protoc_insertion_point(class_scope:stabox.Stream)
  })
_sym_db.RegisterMessage(Stream)



_CHANNELS = _descriptor.ServiceDescriptor(
  name='Channels',
  full_name='stabox.Channels',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=374,
  serialized_end=545,
  methods=[
  _descriptor.MethodDescriptor(
    name='getAvailableStreams',
    full_name='stabox.Channels.getAvailableStreams',
    index=0,
    containing_service=None,
    input_type=_CHANNEL,
    output_type=_STREAM,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='getProgram',
    full_name='stabox.Channels.getProgram',
    index=1,
    containing_service=None,
    input_type=_PROGRAM,
    output_type=_PROGRAM,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='findProgram',
    full_name='stabox.Channels.findProgram',
    index=2,
    containing_service=None,
    input_type=_PROGRAM,
    output_type=_PROGRAM,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CHANNELS)

DESCRIPTOR.services_by_name['Channels'] = _CHANNELS

# @@protoc_insertion_point(module_scope)
