# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Object

__all__ = (
	'Count',
	'Sum',
	'Average',
)


class Count(Expr):
	def __init__(self, attr: Object, name:str = None):
		self.attr = attr
		self.name = name
		return
	def __str__(self):
		return 'COUNT({}){}'.format(
			str(self.attr),
			' AS {}'.format(self.name) if self.name else '',
		)
	

class Sum(Expr):
	def __init__(self, attr: Object, name:str = None):
		self.attr = attr
		self.name = name
		return
	def __str__(self):
		return 'SUM({}){}'.format(
			str(self.attr),
			' AS {}'.format(self.name) if self.name else '',
		)


class Average(Expr):
	def __init__(self, attr: Object, name:str = None):
		self.attr = attr
		self.name = name
		return
	def __str__(self):
		return 'AVG({}){}'.format(
			str(self.attr),
			' AS {}'.format(self.name) if self.name else '',
		)