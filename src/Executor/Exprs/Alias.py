# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Object

__all__ = (
	'Alias'
)


class Alias(Expr):
	def __init__(self, attr: Object, name: str):
		self.attr = attr
		self.name = name
		return
	def __str__(self):
		return '{} AS {}'.format(
			str(self.attr),
			self.name,
		)