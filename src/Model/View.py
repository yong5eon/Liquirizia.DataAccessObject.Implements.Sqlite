# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Model
from Liquirizia.DataAccessObject.Model import Executor

from .Type import Type as ModelType

from ..Connection import Connection
from ..Type import Type

__all__ = (
	'View'
)


class View(object):
	def __init__(
		self, 
		name: str, 
		executor: Executor
	):
		self.name = name
		self.executor = executor
		return
	
	def __call__(self, obj: Model):
		obj.__properties__ = {
			'type': ModelType.View,
			'name': self.name,
			'executor': self.executor,
		}
		def __new__(cls, con: Connection, **kwargs):
			o = object.__new__(cls)
			o.__object__ = dict()
			o.__connection__ = con
			for k, v in cls.__dict__.items():
				if isinstance(v, Type):
					v.__init_object__(o, kwargs[v.key] if v.key in kwargs.keys() else None)
			return o
		obj.__new__ = __new__
		return obj
