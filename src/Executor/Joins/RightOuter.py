# -*- coding: utf-8 -*-

from ..Join import Join

from ..Expr import Expr
from ...Model import Table

__all__ = (
	'RightOuter'
)


class RightOuter(Join):
	"""Right Outer Join Class"""

	def __init__(self, table: Table, *args: type[list[Expr]]) -> None:
		super(RightOuter, self).__init__('RIGHT OUTER', table, *args)
		return
