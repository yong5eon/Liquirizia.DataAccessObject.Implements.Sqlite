# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Model import Executor
from Liquirizia.DataModel.Model import Model

__all__ = (
	'Select'
)


class Select(Executor):
	def __init__(self, o: type[Model]):
		self.obj = o
		self.table = o.__properties__['name']
		self.kwargs = {}
		self.conds = None
		self.grp = None
		self.ord = None
		self.len = None
		self.vargs = None
		return

	def join(self, *args):
		return self

	def where(self, *args):
		return self

	def groupBy(self, *args):
		return self

	def orderBy(self, *args):
		return self

	def limit(self, limit: int, pos: int = None):
		return self
	
	def values(self, *args):
		return self
	
	@property
	def model(self):
		return self.obj
	
	@property
	def query(self):
		sql = 'SELECT {} FROM {}'.format(
			'*' if not self.vargs else '',
			self.table
		)
		return sql

	@property	
	def args(self):
		return list(self.kwargs.values())
	