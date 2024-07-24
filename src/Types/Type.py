# -*- coding: utf-8 -*-

from Liquirizia.DataModelObject import DataAttributeObject

from abc import abstractmethod

from Liquirizia.DataModelObject.DataModelObjectHandler import DataModelObjectHandler
from Liquirizia.Validator.Validator import Validator

__all__ = (
	'Type'
)


class Type(DataAttributeObject):
	def __init__(
			self, 
			name: str, 
			va: Validator = Validator(),
			fn: DataModelObjectHandler = None
		):
		super().__init__(va, fn)
		self.name = name
		return
	
	@abstractmethod
	def __str__(self):
		pass
