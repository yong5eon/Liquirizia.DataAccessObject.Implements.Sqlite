# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Object

__all__ = (
	'IfNull'
)


class IfNull(Expr):
	def __init__(self, attr: Object, value: any):
		self.attr = attr
		self.value = value
		return
	def __str__(self):
		return 'IFNULL({}, {})'.format(
			str(self.attr),
			self.value,
		)