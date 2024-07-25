# -*- coding: utf-8 -*-

from Liquirizia.DataModel import ModelExecutor
from Liquirizia.DataModel.Model import Model, Attribute

__all__ = (
	'Create'
)


class Create(ModelExecutor):
	def __init__(self, o: type[Model]):
		_ = []
		for k, v in o.__dict__.items():
			if isinstance(v, Attribute):
				_.append(str(v))
		if o.__properties__['primaryKey']:
			_.append(str(o.__properties__['primaryKey']))
		_.extend([str(foreignKey) for foreignKey in o.__properties__['foreignKeys']] if o.__properties__['foreignKeys'] else [])
		self.executors = ['CREATE TABLE {}({})'.format(
			o.__properties__['name'],
			', '.join(_)
		)]
		self.executors.extend([str(index) for index in o.__properties__['indexes']] if o.__properties__['indexes'] else [])
		return
	
	def __iter__(self):
		return self.executors.__iter__()
