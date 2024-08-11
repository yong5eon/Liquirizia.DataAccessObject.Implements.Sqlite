# -*- coding: utf-8 -*-

from ..Join import Join

from ..Expr import Expr
from ...Model import Table

__all__ = (
	'Inner'
)


class Inner(Join):
	"""Inner Join Class"""

	def __init__(self, table: Table, *args: type[list[Expr]]) -> None:
		super(Inner, self).__init__('INNER', table, *args)
		return
