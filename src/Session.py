# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Properties.Database import Session as BaseSession
from Liquirizia.DataAccessObject.Model import (
    Run,
    Fetch,
    Executor,
    Executors,
)

from Liquirizia.DataAccessObject import Error
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from .Context import Context
from .Cursor import Cursor

from sqlite3 import Connection as SqliteConnection
from sqlite3 import DatabaseError, IntegrityError, ProgrammingError, OperationalError, NotSupportedError

from typing import Union

__all__ = (
	'Session'
)


class Session(BaseSession, Run):
	"""Session Interface for Database"""

	def __init__(self, connection: SqliteConnection) -> None:
		self.connnection = connection
		self.cursor = self.connnection.cursor()
		return
	
	def __del__(self) -> None:
		self.cursor.close()
		self.connnection.commit()
		return
	
	def execute(self, sql, *args):
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
	
	def executes(self, sql, *args):
		try:
			self.cursor.executemany(sql, args)
			return Context(self.cursor)
		except (DatabaseError, IntegrityError, ProgrammingError, NotSupportedError) as e:
			raise ExecuteError(str(e), error=e)
		except OperationalError as e:
			raise ConnectionClosedError(error=e)
		except Exception as e:
			raise Error(str(e), error=e)

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
			def exec(exec: Executor, cb: callable = None):
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
		raise NotSupportedError('Sqlite is not support row count')
