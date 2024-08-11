# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Type

__all__ = (
	'IsNull'
)


class IsNull(Expr):
	def __init__(self, attr: Type):
		self.attr = attr
		return
	def __str__(self):
		return '{} IS NULL'.format(
			str(self.attr),
		)