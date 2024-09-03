# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Connection as BaseConnection
from Liquirizia.DataAccessObject.Types import Database

from Liquirizia.DataAccessObject import Error
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Types.Database.Errors import *

from Liquirizia.DataAccessObject.Model import (
	Executors,
	Executor,
	Executable,
	Fetchable,
)

from .Configuration import Configuration

from sqlite3 import connect, Row
from sqlite3 import DatabaseError, IntegrityError, ProgrammingError, OperationalError, NotSupportedError

__all__ = (
	'DatabaseAccessObject'
)


class Connection(BaseConnection, Database, Executable):
	"""Connection Class for Sqlite"""

	def __init__(self, conf: Configuration):
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
			raise ConnectionError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
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
			raise ExecuteError(error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return

	def begin(self):
		pass

	def execute(self, sql, *args):
		try:
			self.cursor.execute(sql, args)
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise ExecuteError(str(e), error=e, sql=sql, args=args)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return
	
	def run(self, executor: type[Executor|Executors]):
		cursor = None
		try:
			cursor = self.connection.cursor()
			def execs(execs: Executors):
				__ = []
				for query, args in executor:
					cursor.execute(query, args)
					if not isinstance(executor, Fetchable): continue
					rows = executor.fetch(self, cursor.fetchall())
					__.extend(rows)
				return __
			def exec(exec: Executor, cb: callable = None):
				cursor.execute(executor.query, executor.args)
				if not isinstance(exec, Fetchable): return
				return exec.fetch(self, cursor.fetchall())
			if isinstance(executor, Executors): return execs(executor)
			if isinstance(executor, Executor): return exec(executor)
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise ExecuteError(str(e), error=e, sql=executor.query, args=executor.args)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
	
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
			raise CursorError(error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)

	def count(self):
		raise NotSupportedError('Sqlite is not support row count')

	def commit(self):
		try:
			self.connection.commit()
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise CommitError(error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return

	def rollback(self):
		try:
			self.connection.rollback()
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise RollBackError(error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return
