# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Helper, Error
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from Liquirizia.DataAccessObject.Implements.Sqlite import Configuration, Connection

import sys

if __name__ == '__main__':

	con = None

	try:
		# Set connection
		Helper.Set(
			'Sample',
			Connection,
			Configuration(
				path='tmp/Sample.DB',  # File Path for SQLite Database File
				autocommit=False
			)
		)

		# Get Connection
		con = Helper.Get('Sample')
	except Error as e:
		print(str(e), file=sys.stderr)
		exit(-1)
	except Exception as e:
		print(str(e), file=sys.stderr)
		exit(-1)

	try:
		con.begin()

		con.execute('DROP TABLE IF EXISTS LOG')
		con.execute(
			'''
			CREATE TABLE IF NOT EXISTS LOG (
				ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				TEXT TEXT NOT NULL,
				CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
			)
			'''
			)
		con.execute("INSERT INTO LOG(TEXT) VALUES(?)", ('TEXT1'))
		con.execute("INSERT INTO LOG(TEXT) VALUES(?)", ('TEXT2'))
		con.execute("INSERT INTO LOG(TEXT) VALUES(?)", ('TEXT3'))

		con.commit()
	except ExecuteError as e:
		con.rollback()
		print(str(e), file=sys.stderr)
	except CommitError as e:
		print(str(e), file=sys.stderr)
	except RollBackError as e:
		print(str(e), file=sys.stderr)
	except ConnectionClosedError as e:
		print(str(e), file=sys.stderr)
		exit(-1)
	except Exception as e:
		print(str(e), file=sys.stderr)

	try:
		ctx = con.execute('SELECT * FROM LOG')

		for i, row in enumerate(ctx.rows()):
			print('{} : {}'.format(i, row), file=sys.stdout)

		con.execute('DROP TABLE IF EXISTS LOG')
	except ExecuteError as e:
		print(str(e), file=sys.stderr)
	except ConnectionClosedError as e:
		print(str(e), file=sys.stderr)
		exit(-1)
	except Exception as e:
		print(str(e), file=sys.stderr)
