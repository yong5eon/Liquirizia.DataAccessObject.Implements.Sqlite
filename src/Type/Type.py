# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Attribute, Handler

from Liquirizia.Validator.Validator import Validator

from abc import abstractmethod

__all__ = (
	'Type'
)


class Type(Attribute): pass

class Type(Attribute):
	def __init__(
			self, 
			key: str,
			type: str,
			null: bool = False,
			default: str = None,
			primaryKey: bool = False,
			primaryKeyDesc: bool = False,
			autoincrement: bool = False,
			reference: Type = None,
			va: Validator = Validator(),
			fn: Handler = None
		):
		super().__init__(va, fn)
		self.key = key
		self.type = type
		self.null = null
		self.default = default
		self.primaryKey = primaryKey
		self.primaryKeyDesc = primaryKeyDesc
		self.autoincrement = autoincrement
		self.reference = None
		self.referenceTable = None
		self.referenceKey = None
		if reference:
			if not isinstance(reference, Type):
				raise RuntimeError('{} must be based {}'.format(reference.__qualname__, Type.__qualname__))
			self.reference = reference
			self.referenceTable = reference.model.__properties__['name']
			self.referenceKey = reference.key
		return
	