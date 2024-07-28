# -*- coding: utf-8 -*-

from Liquirizia.DataModel import ModelExecutors
from Liquirizia.DataModel.Model import Model, Attribute

__all__ = (
	'Drop'
)


class Drop(ModelExecutors):
	def __init__(self, o: type[Model], exist: bool = True):
		self.executors = []
		# self.executors.extend([str(index) for index in o.__properties__['indexes']] if o.__properties__['indexes'] else [])
		self.executors.append('DROP TABLE {}{}'.format(
			' IF EXISTS ' if exist else '',
			o.__properties__['name'],
		))
		return
	
	def __iter__(self):
		return self.executors.__iter__()

	def __str__(self):
		return ';'.joinn(self.executors)

