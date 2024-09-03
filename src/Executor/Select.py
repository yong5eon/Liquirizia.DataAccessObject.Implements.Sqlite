# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Model import Executor, Fetchable

from ..Model import Table
from ..Type import Type
from .Expr import Expr

__all__ = (
	'Select'
)


class Select(Executor, Fetchable):
	def __init__(self, o: type[Table]):
		self.obj = o
		self.table = o.__properties__['name']
		self.kwargs = {}
		self.joins = None
		self.conds = None
		self.grps = None
		self.havs = None
		self.ords = None
		self.vals = None
		self.offset = None
		self.size = None
		return

	def join(self, *args):
		self.joins = args
		return self

	def where(self, *args: type[list[Expr]]):
		self.conds = args
		return self

	def groupBy(self, *args):
		self.grps = args
		return self
	
	def having(self, *args: type[list[Expr]]):
		self.havs = args
		return self

	def orderBy(self, *args: type[list[Expr]]):
		self.ords = args
		return self

	def limit(self, size: int = None, offset: int = 0):
		self.size = size
		self.offset = offset
		return self
	
	def values(self, *args):
		self.vals = args
		return self
	
	@property
	def model(self):
		return self.obj
	
	@property
	def query(self):
		args = []
		if not self.vals:
			for k, v in self.obj.__dict__.items():
				if isinstance(v, Type):
					args.append('{}.{}'.format(self.table, v.key))
		else:
			for v in self.vals:
				if isinstance(v, Type):
					args.append('{}.{}'.format(v.model.__properties__['name'], v.key))
					continue
				if isinstance(v, Expr):
					args.append(str(v))
					continue
		sql = 'SELECT {} FROM {}{}{}{}{}{}{}'.format(
			', '.join(args),
			self.table,
			''.join([' {}'.format(str(join)) for join in self.joins]) if self.joins else '',
			' WHERE {}'.format(' AND '.join([str(cond) for cond in self.conds])) if self.conds else '',
			' GROUP BY {}'.format(', '.join([str(grp) for grp in self.grps])) if self.grps else '',
			' HAVING {}'.format(' AND '.join([str(hav) for hav in self.havs])) if self.havs else '',
			' ORDER BY {}'.format(', '.join([str(order) for order in self.ords])) if self.ords else '',
			' LIMIT {}, {}'.format(self.offset, self.size) if self.size else '',
		)
		return sql

	@property	
	def args(self):
		return list(self.kwargs.values())

	def fetch(self, con, rows):
		_ = []
		if self.joins or self.grps or self.vals:
			for i, row in enumerate(rows):
				_.append(dict(row))
		else:
			for i, row in enumerate(rows):
				obj = self.obj(**dict(row))
				obj.__connection__ = con
				_.append(obj)
		return _