# -*- coding: utf-8 -*-

from Liquirizia.DataModel import ModelExecutor
from Liquirizia.DataModel.Model import Model

from ..Encoder import Encoder

__all__ = (
	'Insert'
)


class Insert(ModelExecutor):
	def __init__(self, o: type[Model]):
		self.model = o
		self.table = o.__properties__['name']
		self.sql = 'INSERT INTO {}'.format(self.table)
		self.kwargs = {}
		return
	
	def __str__(self):
		return self.sql

	def value(self, **kwargs):
		encoder = Encoder()
		for k, v in self.model.__dict__.items():
			if k not in kwargs.keys(): continue
			self.kwargs[v.key] = encoder(v.validator(kwargs[k]))
		self.sql += '({}) VALUES({}) RETURNING *'.format(
			', '.join(self.kwargs.keys()),
			', '.join(['?' for k in self.kwargs.keys()])
		)
		return self

	@property	
	def args(self):
		return list(self.kwargs.values())
	