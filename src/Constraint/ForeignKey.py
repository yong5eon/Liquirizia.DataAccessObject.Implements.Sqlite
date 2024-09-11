# -*- coding: utf-8 -*-

from .Constraint import Constraint

__all__ = (
	'ForeignKey'
)


class ForeignKey(Constraint):
	def __init__(self, cols, reference, referenceCols):
		self.cols = cols if isinstance(cols, (tuple, list)) else [cols]
		self.reference = reference
		self.referenceCols = referenceCols if isinstance(referenceCols, (tuple, list)) else [referenceCols]
		return
	