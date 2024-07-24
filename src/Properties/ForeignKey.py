# -*- coding: utf-8 -*-

from .Property import Property

__all__ = (
	'ForeignKey'
)


class ForeignKey(Property):
	def __init__(self, columns, table, references):
		self.columns = columns if isinstance(columns, (tuple, list)) else (columns)
		self.table = table
		self.references = columns if isinstance(references, (tuple, list)) else (references)
		return
	
	def __str__(self):
		return 'FOREIGN KEY({}) REFERENCES {}({})'.format(
			', '.join(self.columns),
			self.table,
			', '.join(self.references)
		)
