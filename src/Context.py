# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import Context as BaseContext

from Liquirizia.DataAccessObject import Error
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from sqlite3 import DatabaseError, IntegrityError, ProgrammingError, OperationalError, NotSupportedError

__all__ = (
	'Context'
)


class Context(BaseContext):
	"""Context for Sqlite"""

	def __init__(self, cursor):
		self.cursor = cursor
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
			raise CursorError(error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)

	def row(self):
		try:
			return dict(self.cursor.fetchone())
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise CursorError(error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
	
	def count(self):
		return self.cursor.connection.total_changes

	@property
	def query(self):
		return self.cursor.query