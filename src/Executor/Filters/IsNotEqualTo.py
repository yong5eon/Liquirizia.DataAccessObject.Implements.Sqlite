# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Type
from ...Encoder import Encoder

__all__ = (
	'IsNotEqualTo'
)


class IsNotEqualTo(Expr):
	"""Is Not Equal Filter Class"""

	def __init__(self, attr: Type, other) -> None:
		self.attr = attr
		self.other = other
		self.encoder = Encoder()
		return

	def __str__(self):
		return '{} != {}'.format(
			str(self.attr),
			str(self.other) if isinstance(self.other, Type) else self.encoder(self.other),
		)
