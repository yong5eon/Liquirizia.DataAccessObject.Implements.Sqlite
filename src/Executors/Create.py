# -*- coding: utf-8 -*-

from Liquirizia.DataModel import ModelExecutors
from Liquirizia.DataModel.Model import Model, Attribute

__all__ = (
	'Create'
)


class Create(ModelExecutors):
	def __init__(self, o: type[Model], notexist: bool = False):
		_ = []
		for k, v in o.__dict__.items():
			if isinstance(v, Attribute):
				_.append(str(v))
		if o.__properties__['primaryKey']:
			_.append(str(o.__properties__['primaryKey']))
		_.extend([str(foreignKey) for foreignKey in o.__properties__['foreignKeys']] if o.__properties__['foreignKeys'] else [])
		self.executors = ['CREATE TABLE {}{}({})'.format(
			' IF NOT EXISTS ' if notexist else '',
			o.__properties__['name'],
			', '.join(_)
		)]
		self.executors.extend([str(index) for index in o.__properties__['indexes']] if o.__properties__['indexes'] else [])
		return
	
	def __iter__(self):
		return self.executors.__iter__()
	
	def __str__(self):
		return ';'.join(self.executors)
