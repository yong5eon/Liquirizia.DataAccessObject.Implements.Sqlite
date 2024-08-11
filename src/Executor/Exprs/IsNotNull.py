# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Type

__all__ = (
	'IsNotNull'
)


class IsNotNull(Expr):
	def __init__(self, attr: Type):
		self.attr = attr
		return
	def __str__(self):
		return '{} IS NOT NULL'.format(
			str(self.attr),
		)