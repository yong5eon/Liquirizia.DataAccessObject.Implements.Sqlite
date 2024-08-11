# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Type
from ...Encoder import Encoder

__all__ = (
	'IsGreaterThan'
)


class IsGreaterThan(Expr):
	"""Is Greater Than Filter Class"""

	def __init__(self, attr, other) -> None:
		self.attr = attr
		self.other = other
		self.encoder = Encoder()
		return

	def __str__(self):
		return '{} > {}'.format(
			str(self.attr) if isinstance(self.attr, Type) else self.attr,
			str(self.other) if isinstance(self.other, Type) else self.encoder(self.other),
		)
