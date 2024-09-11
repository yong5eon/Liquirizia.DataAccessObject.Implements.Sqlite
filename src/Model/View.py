# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Model
from Liquirizia.DataAccessObject.Model import Executor

from .Type import Type

from ..Type import Object

__all__ = (
	'View'
)


class View(object):
	def __init__(
		self, 
		name: str, 
		executor: Executor,
	):
		self.name = name
		self.executor = executor
		return
	
	def __call__(self, obj: Model):
		obj.__properties__ = {
			'type': Type.View,
			'name': self.name,
			'executor': self.executor,
		}
		def __new__(cls, **kwargs):
			o = object.__new__(cls)
			o.__object__ = dict()
			for k, v in cls.__dict__.items():
				if not isinstance(v, Object): continue
				v.__init_object__(o, kwargs[v.key] if v.key in kwargs.keys() else None)
			return o
		obj.__new__ = __new__
		return obj
