# -*- coding: utf-8 -*-

from typing import Any
from Liquirizia.DataModelObject import (
	DataModelObjectFactory,
	DataModelObject,
	DataAttributeObject,
)

from .Property import Property

from .PrimaryKey import PrimaryKey
from .ForeignKey import ForeignKey
from .Index import Index
from .IndexUnique import IndexUnique

__all__ = (
	'Table'
)


class Table(DataModelObjectFactory):
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
		self.obj = None
		return
	
	def __call__(self, obj):
		self.obj = obj
		obj.ToString = self.toString
		return obj
	
	def toString(self):
		_ = []
		# TODO : Add Columns
		for k, v in self.obj.__dict__.items():
			if isinstance(v, DataAttributeObject):
				_.append(v.toString())
		if self.primaryKey:
			_.append(str(self.primaryKey))
		_.extend([str(foreignKey) for foreignKey in self.foreignKeys] if self.foreignKeys else [])
		__ = ['CREATE TABLE {}({})'.format(
			self.name,
			',\n'.join(_)
		)]
		__.extend([str(index) for index in self.indexes] if self.indexes else [])
		return __
	