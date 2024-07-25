# -*- coding: utf-8 -*-

from .Property import Property

__all__ = (
	'IndexUnique'
)


class IndexUnique(Property):
	def __init__(
		self, 
		name: str,
		columns: list[str],
		exists: bool = None,
		expr: str = None,
		null: str = None,
	):
		self.name = name
		self.table = None
		self.columns = columns if isinstance(columns, (tuple, list)) else [columns]
		self.exists = exists
		self.expr = expr
		self.null = null
		return
	
	def __str__(self):
		return 'CREATE UNIQUE INDEX {}{} ON {}({}){}{}'.format(
			{None:'', False:'IF NOT EXISTS ', True:'IF EXISTS'}.get(self.exists, ''),
			self.name,
			self.table,
			', '.join(self.columns),
			' WHERE {}'.format(self.expr) if self.expr else '',
			' NULL {}'.format(self.null) if self.null else '',
		)
