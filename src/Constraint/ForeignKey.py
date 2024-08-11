# -*- coding: utf-8 -*-

from .Constraint import Constraint

__all__ = (
	'ForeignKey'
)


class ForeignKey(Constraint):
	def __init__(self, columns, table, references):
		self.columns = columns if isinstance(columns, (tuple, list)) else [columns]
		self.table = table
		self.references = columns if isinstance(references, (tuple, list)) else [references]
		return
	