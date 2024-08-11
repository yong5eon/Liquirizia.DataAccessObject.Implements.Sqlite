# -*- coding: utf-8 -*-

__all__ = (
	'IndexUnique'
)


class IndexUnique(object):
	def __init__(
		self, 
		name: str,
		colexprs: list[str],
		expr: str = None,
		notexists: bool = None,
	):
		self.name = name
		self.table = None
		self.colexprs = colexprs if isinstance(colexprs, (tuple, list)) else [colexprs]
		self.expr = expr
		self.notexists = notexists 
		return
	