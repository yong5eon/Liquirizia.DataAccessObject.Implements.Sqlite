# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Type
from ...Encoder import Encoder

__all__ = (
	'IsLike'
)


class IsLike(Expr):
	"""Is Like Filter Class"""

	def __init__(self, attr: Type, other) -> None:
		self.attr = attr
		self.other = other
		self.encoder = Encoder()
		return

	def __str__(self):
		return '{} LIKE {}'.format(
			str(self.attr),
			self.encoder(self.other),
		)