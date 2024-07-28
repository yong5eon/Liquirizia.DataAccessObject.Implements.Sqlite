# -*- coding: utf-8 -*-

from .Property import Property

__all__ = (
	'PrimaryKey'
)


class PrimaryKey(Property):
	def __init__(self, columns):
		self.columns = columns if isinstance(columns, (tuple, list)) else [columns]
		return
	
	def __str__(self):
		return 'PRIMARY KEY({})'.format(
			', '.join(self.columns)
		)
