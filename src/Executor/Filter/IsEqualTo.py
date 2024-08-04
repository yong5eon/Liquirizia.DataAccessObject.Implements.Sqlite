# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Type
from ...Encoder import Encoder

__all__ = (
	'IsEqualTo'
)


class IsEqualTo(Expr):
	"""Is Equal Filter Class"""

	def __init__(self, attr: Type, other) -> None:
		self.attr = attr
		self.other = other
		self.encoder = Encoder()
		return

	def __str__(self):
		return '{} = {}'.format(
			str(self.attr),
			'{}.{}'.format(self.other.model.__properties__['name'], self.other.key) if isinstance(self.other, Type) else self.encoder(self.other),
		)
