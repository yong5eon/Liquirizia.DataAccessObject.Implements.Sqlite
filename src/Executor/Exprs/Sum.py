# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Type

__all__ = (
	'Sum'
)


class Sum(Expr):
	def __init__(self, attr: Type, name:str = None):
		self.attr = attr
		self.name = name
		return
	def __str__(self):
		return 'SUM({}){}'.format(
			str(self.attr),
			' AS {}'.format(self.name) if self.name else '',
		)