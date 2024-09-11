# -*- coding: utf-8 -*-

from .Select import Select

from ..Cursor import Cursor

__all__ = (
	'Get'
)


class Get(Select):
	def fetch(self, cursor: Cursor):
		rows = super().fetch(cursor)
		if rows:
			return rows[0]
		return None