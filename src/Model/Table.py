# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Model import Type 
from Liquirizia.DataModel import (
	Model,
	Attribute,
)

from ..Constraint import (
	PrimaryKey,
	ForeignKey,
)

from ..Index import (
	Index,
	IndexUnique,
)

__all__ = (
	'Table'
)


class Table(Type):
	def __init__(
		self, 
		name: str, 
		primaryKey: PrimaryKey = None,
		foreignKeys: list[ForeignKey] = None,
		indexes: list[Index|IndexUnique] = None,
	):
		self.name = name
		self.primaryKey = primaryKey
		self.foreignKeys = foreignKeys
		self.indexes = indexes
		for index in self.indexes if self.indexes else []: index.table = name
		return
	
	def __call__(self, obj: Model):
		obj.__properties__ = {
			'name': self.name,
			'primaryKey': self.primaryKey,
			'foreignKeys': self.foreignKeys,
			'indexes': self.indexes,
		}

		def __new__(cls, **kwargs):
			o = object.__new__(cls)
			o.__object__ = dict()
			for k, v in cls.__dict__.items():
				if isinstance(v, Attribute):
					v.__init_object__(o, kwargs[v.key] if v.key in kwargs.keys() else None)
			return o
		obj.__new__ = __new__

		return obj

