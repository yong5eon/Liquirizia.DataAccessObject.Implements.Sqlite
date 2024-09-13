# -*- coding: utf-8 -*-

from ..Join import Join
from ...Model import Table

__all__ = (
	'FullOuter'
)


class FullOuter(Join):
	"""Full Outer Join Class"""

	def __init__(self, table: Table, *args) -> None:
		super(FullOuter, self).__init__('FULL OUTER', table, *args)
		return
