# -*- coding: utf-8 -*-

from typing import Any
from Liquirizia.DataModel import (
	ModelFactory,
	Model,
	Attribute,
)

from .Property import Property

from .PrimaryKey import PrimaryKey
from .ForeignKey import ForeignKey
from .Index import Index
from .IndexUnique import IndexUnique

__all__ = (
	'Table'
)


class Table(ModelFactory):
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
		return obj
	