# -*- coding: utf-8 -*-

from .Join import Join

from ..Expr import Expr
from ...Model import Table

__all__ = (
	'LeftOuter'
)


class LeftOuter(Join):
	"""Left Outer Class"""

	def __init__(self, table: Table, *args: type[list[Expr]]) -> None:
		super(LeftOuter, self).__init__('LEFT OUTER', table, *args)
		return
