# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Object

__all__ = (
	'IsNull',
	'IsNotNull',
)


class IsNull(Expr):
	def __init__(self, attr: Object):
		self.attr = attr
		return
	def __str__(self):
		return '{} IS NULL'.format(
			str(self.attr),
		)


class IsNotNull(Expr):
	def __init__(self, attr: Object):
		self.attr = attr
		return
	def __str__(self):
		return '{} IS NOT NULL'.format(
			str(self.attr),
		)