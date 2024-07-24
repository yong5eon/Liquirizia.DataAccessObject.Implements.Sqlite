# -*- coding: utf-8 -*-

from .Property import Property

__all__ = (
	'PrimaryKey'
)


class PrimaryKey(Property):
	def __init__(self, columns, desc=False):
		self.columns = columns if isinstance(columns, (tuple, list)) else (columns)
		self.desc = desc
		return
	
	def __str__(self):
		return 'PRIMARY KEY({} {})'.format(
			', '.join(self.columns),
			'ASC' if not self.desc else 'DESC'
		)
