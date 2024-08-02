# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Model import Executors
from Liquirizia.DataModel.Model import Model, Attribute

__all__ = (
	'Drop'
)


class Drop(Executors):
	def __init__(self, o: type[Model], exist: bool = True):
		self.executors = []
		self.executors.append(('DROP TABLE {}{}'.format(
			' IF EXISTS ' if exist else '',
			o.__properties__['name'],
		), ()))
		return
	
	def __iter__(self):
		return self.executors.__iter__()

