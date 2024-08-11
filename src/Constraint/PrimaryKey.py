# -*- coding: utf-8 -*-

from .Constraint import Constraint

__all__ = (
	'PrimaryKey'
)


class PrimaryKey(Constraint):
	def __init__(self, columns):
		self.columns = columns if isinstance(columns, (tuple, list)) else [columns]
		return
	