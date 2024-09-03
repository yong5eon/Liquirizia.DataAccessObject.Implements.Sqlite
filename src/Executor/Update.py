# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Model import Executor, Fetchable

from ..Model import Table
from .Expr import Expr

__all__ = (
	'Update'
)


class Update(Executor, Fetchable):
	def __init__(self, o: type[Table]):
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
	
	def where(self, *args: type[list[Expr]]):
		self.conds = args
		return self
	
	@property
	def model(self):
		return self.obj
	
	@property
	def query(self):
		return 'UPDATE {} SET {}{} RETURNING *'.format(
			self.table,
			', '.join(['{}=?'.format(k) for k in self.kwargs.keys()]),
			' WHERE {}'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
		)

	@property	
	def args(self):
		return list(self.kwargs.values())

	def fetch(self, con, rows):
		_ = []
		for i, row in enumerate(rows):
			obj = self.obj(**dict(row))
			obj.__connection__ = con
			_.append(obj)
		return _[0] if len(_) else None	
