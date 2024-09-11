# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Object

__all__ = (
	'IsLike'
)


class IsLike(Expr):
	"""Is Like Filter Class"""

	def __init__(self, attr: Object, other) -> None:
		self.attr = attr
		self.other = other
		return

	def __str__(self):
		return '{} LIKE {}'.format(
			str(self.attr),
			self.encode(self.other),
		)
