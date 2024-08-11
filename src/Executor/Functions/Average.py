# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Type

__all__ = (
	'Average'
)


class Average(Expr):
	def __init__(self, attr: Type, name:str = None):
		self.attr = attr
		self.name = name
		return
	def __str__(self):
		return 'AVG({}){}'.format(
			str(self.attr),
			' AS {}'.format(self.name) if self.name else '',
		)