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
			name: str, 
			va: Validator = Validator(),
			fn: ModelHandler = None
		):
		super().__init__(va, fn)
		self.name = name
		return
	
	@abstractmethod
	def __str__(self):
		pass
