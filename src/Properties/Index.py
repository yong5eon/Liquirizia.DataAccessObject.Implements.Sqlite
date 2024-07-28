# -*- coding: utf-8 -*-

from .Property import Property

__all__ = (
	'Index'
)


class Index(Property):
	def __init__(
		self, 
		name: str,
		colexprs: list[str],
		expr: str = None,
		notexists: bool = True,
	):
		self.name = name
		self.table = None
		self.colexprs = colexprs if isinstance(colexprs, (tuple, list)) else [colexprs]
		self.expr = expr
		self.notexists = notexists
		return
	
	def __str__(self):
		return 'CREATE INDEX {}{} ON {}({}){}'.format(
			'IF NOT EXISTS ' if self.notexists else '',
			self.name,
			self.table,
			', '.join(self.colexprs),
			' WHERE {}'.format(self.expr) if self.expr else '',
		)
