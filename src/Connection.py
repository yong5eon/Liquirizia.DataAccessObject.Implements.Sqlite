# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Connection as BaseConnection
from Liquirizia.DataAccessObject.Properties.Database import Database

from Liquirizia.DataAccessObject import Error
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from Liquirizia.DataAccessObject.Model import (
	Executors,
	Executor,
	Run,
	Fetch,
)

from .Configuration import Configuration
from .Context import Context
from .Cursor import Cursor
from .Session import Session

from sqlite3 import connect, Row
from sqlite3 import DatabaseError, IntegrityError, ProgrammingError, OperationalError, NotSupportedError

from typing import Union

__all__ = (
	'DatabaseAccessObject'
)


class Connection(BaseConnection, Database, Run):
	"""Connection Class for Sqlite"""

	def __init__(self, conf: Configuration):
		self.conf = conf
		self.connection = None
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
			cursor = self.connection.cursor()
			cursor.execute(sql, args)
			return Context(cursor)
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise ExecuteError(str(e), error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return
	
	def executes(self, sql, *args):
		try:
			cursor = self.connection.cursor()
			cursor.executemany(sql, args)
			return Context(cursor)
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise ExecuteError(str(e), error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		return

	def run(self, executor: Union[Executor,Executors]):
		try:
			cursor = self.connection.cursor()
			def execs(execs: Executors):
				__ = []
				for query, args in executor:
					cursor.execute(query, args)
					if not isinstance(executor, Fetch): continue
					rows = executor.fetch(Cursor(cursor))
					__.extend(rows)
				return __
			def exec(exec: Executor):
				cursor.execute(executor.query, executor.args)
				if not isinstance(exec, Fetch): return
				return exec.fetch(Cursor(cursor))
			if isinstance(executor, Executors): return execs(executor)
			if isinstance(executor, Executor): return exec(executor)
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise ExecuteError(str(e), error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)
		
	def cursor(self) -> Cursor:
		return Cursor(self.connection.cursor())
		
	def session(self) -> Session:
		return Session(self.connection)

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
