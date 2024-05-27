# -*- coding: utf-8 -*-
# Copyright (c) 2017, 2024, Oracle and/or its affiliates.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2.0, as
# published by the Free Software Foundation.
#
# This program is designed to work with certain software (including
# but not limited to OpenSSL) that is licensed under separate terms,
# as designated in a particular file or component or in included license
# documentation. The authors of MySQL hereby grant you an
# additional permission to link the program and your derivative works
# with the separately licensed software that they have either included with
# the program or referenced in the documentation.
#
# Without limiting anything contained in the foregoing, this file,
# which is part of MySQL Connector/Python, is also subject to the
# Universal FOSS Exception, version 1.0, a copy of which can be found at
# http://oss.oracle.com/licenses/universal-foss-exception.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License, version 2.0, for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA

# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mysqlx_connection.proto

# type: ignore

"""Generated protocol buffer code."""
from google.protobuf import (
    descriptor as _descriptor,
    descriptor_pool as _descriptor_pool,
    symbol_database as _symbol_database,
)
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mysqlx.protobuf import (
    mysqlx_datatypes_pb2 as mysqlx__datatypes__pb2,
    mysqlx_pb2 as mysqlx__pb2,
)

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x17mysqlx_connection.proto\x12\x11Mysqlx.Connection\x1a\x16mysqlx_datatypes.proto\x1a\x0cmysqlx.proto"@\n\nCapability\x12\x0c\n\x04name\x18\x01 \x02(\t\x12$\n\x05value\x18\x02 \x02(\x0b\x32\x15.Mysqlx.Datatypes.Any"C\n\x0c\x43\x61pabilities\x12\x33\n\x0c\x63\x61pabilities\x18\x01 \x03(\x0b\x32\x1d.Mysqlx.Connection.Capability"\x11\n\x0f\x43\x61pabilitiesGet"H\n\x0f\x43\x61pabilitiesSet\x12\x35\n\x0c\x63\x61pabilities\x18\x01 \x02(\x0b\x32\x1f.Mysqlx.Connection.Capabilities"\x07\n\x05\x43lose"\xa5\x01\n\x0b\x43ompression\x12\x19\n\x11uncompressed_size\x18\x01 \x01(\x04\x12\x34\n\x0fserver_messages\x18\x02 \x01(\x0e\x32\x1b.Mysqlx.ServerMessages.Type\x12\x34\n\x0f\x63lient_messages\x18\x03 \x01(\x0e\x32\x1b.Mysqlx.ClientMessages.Type\x12\x0f\n\x07payload\x18\x04 \x02(\x0c\x42\x1b\n\x17\x63om.mysql.cj.x.protobufH\x03'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "mysqlx_connection_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\n\027com.mysql.cj.x.protobufH\003"
    _CAPABILITY._serialized_start = 84
    _CAPABILITY._serialized_end = 148
    _CAPABILITIES._serialized_start = 150
    _CAPABILITIES._serialized_end = 217
    _CAPABILITIESGET._serialized_start = 219
    _CAPABILITIESGET._serialized_end = 236
    _CAPABILITIESSET._serialized_start = 238
    _CAPABILITIESSET._serialized_end = 310
    _CLOSE._serialized_start = 312
    _CLOSE._serialized_end = 319
    _COMPRESSION._serialized_start = 322
    _COMPRESSION._serialized_end = 487
# @@protoc_insertion_point(module_scope)
