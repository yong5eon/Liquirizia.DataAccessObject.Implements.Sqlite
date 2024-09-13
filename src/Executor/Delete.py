# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Model import Executor

from ..Model import Table
from .Expr import Expr

from typing import Type

__all__ = (
	'Update'
)


class Delete(Executor):
	def __init__(self, o: Type[Table]):
		self.obj = o
		self.table = o.__properties__['name']
		self.kwargs = {}
		self.cond = None
		return
	
	def set(self, **kwargs):
		for k, v in self.obj.__dict__.items():
			if k not in kwargs.keys(): continue
			self.kwargs[v.key] = v.validator(kwargs[k])
		return self
	
	def where(self, *args):
		self.conds = args
		return self
	
	@property
	def model(self):
		return self.obj
	
	@property
	def query(self):
		return 'DELETE FROM {}{}'.format(
			self.table,
			' WHERE {}'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
		)

	@property	
	def args(self):
		return list(self.kwargs.values())
	