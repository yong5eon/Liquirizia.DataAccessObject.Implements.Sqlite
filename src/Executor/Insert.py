# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Model import Executor
from Liquirizia.DataModel.Model import Model

__all__ = (
	'Insert'
)


class Insert(Executor):
	def __init__(self, o: type[Model]):
		self.obj = o
		self.table = o.__properties__['name']
		self.sql = 'INSERT INTO {}'.format(self.table)
		self.kwargs = {}
		return
	
	def values(self, **kwargs):
		for k, v in self.obj.__dict__.items():
			if k not in kwargs.keys(): continue
			self.kwargs[v.key] = v.validator(kwargs[k])
		self.sql += '({}) VALUES({}) RETURNING *'.format(
			', '.join(self.kwargs.keys()),
			', '.join(['?' for k in self.kwargs.keys()])
		)
		return self
	
	@property
	def model(self):
		return self.obj
	
	@property
	def query(self):
		return self.sql

	@property	
	def args(self):
		return list(self.kwargs.values())
	