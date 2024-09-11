# -*- coding: utf-8 -*-

from .Constraint import Constraint

__all__ = (
	'PrimaryKey'
)


class PrimaryKey(Constraint):
	def __init__(self, cols, autoincrement=False):
		self.cols = cols if isinstance(cols, (tuple, list)) else [cols]
		self.autoincrement = autoincrement
		return
	