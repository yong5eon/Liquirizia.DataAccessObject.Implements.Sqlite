# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Attribute, ModelHandler
from Liquirizia.Validator.Validator import Validator

from abc import abstractmethod

__all__ = (
	'Type'
)


class Type(Attribute):
	def __init__(
			self, 
			key: str,
			null: bool = False,
			default: str = None,
			check: str = None,
			primaryKey: bool = False,
			primaryKeyDesc: bool = False,
			va: Validator = Validator(),
			fn: ModelHandler = None
		):
		super().__init__(va, fn)
		self.key = key
		self.null = null
		self.default = default
		self.check = check
		self.primaryKey = primaryKey
		self.primaryKeyDesc = primaryKeyDesc
		return
	
	@abstractmethod
	def __str__(self):
		pass
