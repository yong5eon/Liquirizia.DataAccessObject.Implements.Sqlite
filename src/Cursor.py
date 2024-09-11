# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import Cursor as BaseCursor

from Liquirizia.DataAccessObject import Error
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from .Context import Context

from sqlite3 import Cursor as SqliteCuror
from sqlite3 import DatabaseError, IntegrityError, ProgrammingError, OperationalError, NotSupportedError


__all__ = (
	'Cursor'
)


class Cursor(BaseCursor):
	"""Cursor for Sqlite"""
	def __init__(self, cursor: SqliteCuror):
		self.cursor = cursor
		return

	def execute(self, sql, *args) -> Context:
		try:
			self.cursor.execute(sql, args)
			return Context(self.cursor)
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise ExecuteError(str(e), error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return
	
	def executes(self, sql, *args) -> Context:
		try:
			self.cursor.execute(sql, args)
			return Context(self.cursor)
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise ExecuteError(str(e), error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return
	
	def rows(self):
		def transform(rows):
			li = []  # the dictionary to be filled with the row data and to be returned
			for i, row in enumerate(rows):  # iterate throw the sqlite3.Row objects
				li.append(dict(row))
			return li
		try:
			return transform(self.cursor.fetchall())
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise ExecuteError(str(e))
		except OperationalError as e:
			raise ConnectionError(str(e), error=e)
		except Exception as e:
			raise Error(str(e), error=e)

	def row(self):
		try:
			return dict(self.cursor.fetchone())
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise ExecuteError(str(e))
		except OperationalError as e:
			raise ConnectionError(str(e), error=e)
		except Exception as e:
			raise Error(str(e), error=e)

	def count(self):
		return NotSupportedError('Sqlite is not support row count')
