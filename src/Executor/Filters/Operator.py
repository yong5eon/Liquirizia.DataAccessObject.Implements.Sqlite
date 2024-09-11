# -*- coding: utf-8 -*-

from ..Expr import Expr

__all__ = (
	'And',
	'Or',
)


class And(Expr):
	def __init__(self, *args) -> None:
		self.args = args
		return

	def __str__(self):
		return ' AND '.join([str(arg) for arg in self.args])


class Or(Expr):
	def __init__(self, *args) -> None:
		self.args = args
		return

	def __str__(self):
		return ' OR '.join([str(arg) for arg in self.args])