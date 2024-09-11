# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Object

__all__ = (
	'Descend'
)


class Descend(Expr):
	"""Descend Order Class"""

	def __init__(self, attr: Object, null='LAST') -> None:
		self.attr = attr
		self.null = null
		return

	def __str__(self):
		return '{} DESC{}'.format(
			str(self.attr) if isinstance(self.attr, Object) else self.attr,
			' NULLS {}'.format(self.null) if self.null else '',
		)
