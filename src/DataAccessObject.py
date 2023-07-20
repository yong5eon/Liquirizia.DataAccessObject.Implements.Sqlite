# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import DataAccessObject as DataAccessObjectBase
from Liquirizia.DataAccessObject.Properties.Database import Database

from Liquirizia.DataAccessObject import DataAccessObjectError
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from .DataAccessObjectConfiguration import DataAccessObjectConfiguration
from .DataAccessObjectFormatter import DataAccessObjectFormatter

from sqlite3 import connect, Row
from sqlite3 import DatabaseError, IntegrityError, ProgrammingError, OperationalError, NotSupportedError

__all__ = (
	'DatabaseAccessObject'
)


class DataAccessObject(DataAccessObjectBase, Database):
	"""
	Data Access Object Class for Sqlite

	# TODO :
		* LIKE 검색 시 문자열 포메팅 오류 발생
	"""

	def __init__(self, conf: DataAccessObjectConfiguration):
		self.conf = conf
		self.connection = None
		self.cursor = None
		return

	def __del__(self):
		if not self.connection:
			return
		self.close()
		return

	def connect(self):
		try:
			self.connection = connect(
				self.conf.path,
				isolation_level=None if self.conf.autocommit else 'DEFERRED',
				check_same_thread=False,
			)
			self.connection.row_factory = Row
			self.cursor = self.connection.cursor()
		except (DatabaseError) as e:
			raise DataAccessObjectConnectionError(error=e)
		except Exception as e:
			raise DataAccessObjectError(str(e), error=e)
		return

	def close(self):
		try:
			if self.conf.autocommit:
				self.commit()

			if not self.cursor:
				self.cursor.close()
				del self.cursor
				self.cursor = None

			if not self.connection:
				self.connection.close()
				del self.connection
				self.connection = None
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise DataAccessObjectExecuteError(error=e)
		except OperationalError as e:
			raise DataAccessObjectConnectionClosedError(error=e)
		except Exception as e:
			raise DataAccessObjectError(str(e), error=e)
		return

	def begin(self):
		pass

	def execute(self, sql, *args, **kwargs):
		try:
			query = str(DataAccessObjectFormatter(sql, *args, **kwargs))
			self.cursor.execute(query)
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise DataAccessObjectExecuteError(str(e), sql=str(DataAccessObjectFormatter(sql, *args, **kwargs)), error=e)
		except OperationalError as e:
			raise DataAccessObjectConnectionClosedError(error=e)
		except Exception as e:
			raise DataAccessObjectError(str(e), error=e)
		return

	def affected(self):
		return self.connection.total_changes

	def rows(self):
		def transform(rows):
			li = []  # the dictionary to be filled with the row data and to be returned
			for i, row in enumerate(rows):  # iterate throw the sqlite3.Row objects
				li.append(dict(row))
			return li
		try:
			return transform(self.cursor.fetchall())
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise DataAccessObjectCursorError(error=e)
		except OperationalError as e:
			raise DataAccessObjectConnectionClosedError(error=e)
		except Exception as e:
			raise DataAccessObjectError(str(e), error=e)

	def count(self):
		raise DataAccessObjectNotSupportedError('Sqlite is not support row count')

	def commit(self):
		try:
			self.connection.commit()
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise DataAccessObjectCommitError(error=e)
		except OperationalError as e:
			raise DataAccessObjectConnectionClosedError(error=e)
		except Exception as e:
			raise DataAccessObjectError(str(e), error=e)
		return

	def rollback(self):
		try:
			self.connection.rollback()
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise DataAccessObjectRollBackError(error=e)
		except OperationalError as e:
			raise DataAccessObjectConnectionClosedError(error=e)
		except Exception as e:
			raise DataAccessObjectError(str(e), error=e)
		return
