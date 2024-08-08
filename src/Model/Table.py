# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Model, Handler

from .Type import Type as ModelType

from ..Connection import Connection
from ..Type import Type
from ..Constraint import (
	PrimaryKey,
	ForeignKey,
)
from ..Index import (
	Index,
	IndexUnique,
)
from ..Handler import Update

__all__ = (
	'Table'
)


class Table(object):
	def __init__(
		self, 
		name: str, 
		primaryKey: PrimaryKey = None,
		foreignKeys: list[ForeignKey] = None,
		indexes: list[Index|IndexUnique] = None,
		fn: Handler = Update(),
	):
		self.name = name
		self.primaryKey = primaryKey
		self.foreignKeys = foreignKeys
		self.indexes = indexes
		for index in self.indexes if self.indexes else []: index.table = name
		self.fn = fn
		return
	
	def __call__(self, obj: Model):
		obj.__properties__ = {
			'type': ModelType.Table,
			'name': self.name,
			'primaryKey': self.primaryKey,
			'foreignKeys': self.foreignKeys,
			'indexes': self.indexes,
		}
		def __new__(cls, con: Connection, **kwargs):
			o = object.__new__(cls)
			o.__object__ = dict()
			o.__connection__ = con
			for k, v in cls.__dict__.items():
				if isinstance(v, Type):
					v.__init_object__(o, kwargs[v.key] if v.key in kwargs.keys() else None)
					v.callback = self.fn
			return o
		obj.__new__ = __new__
		return obj
