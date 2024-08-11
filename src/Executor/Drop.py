# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Model import Executors
from Liquirizia.DataModel import Model
from Liquirizia.DataAccessObject.Implements.Sqlite.Model import Type

__all__ = (
	'Drop'
)


class Drop(Executors):
	def __init__(self, o: type[Model], exist: bool = True):
		self.executors = []
		if o.__properties__['type'] == Type.Table:
			self.executors.append(('DROP TABLE {}{}'.format(
				' IF EXISTS ' if exist else '',
				o.__properties__['name'],
			), ()))
		if o.__properties__['type'] == Type.View:
			self.executors.append(('DROP VIEW {}{}'.format(
				' IF EXISTS ' if exist else '',
				o.__properties__['name'],
			), ()))
		return
	
	def __iter__(self):
		return self.executors.__iter__()

