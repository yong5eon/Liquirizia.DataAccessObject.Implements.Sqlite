# Liquirizia.DataAccessObject.Implements.Sqlite
Database Data Access Object of Liquirizia for Sqlite

## 사용 방법
```python
# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import DataAccessObjectHelper
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from Liquirizia.DataAccessObject.Implements.Sqlite import DataAccessObject, DataAccessObjectConfiguration

import sys

if __name__ == '__main__':

	con = None

	try:
		# Set connection
		DataAccessObjectHelper.Set(
			'Sample',
			DataAccessObject,
			DataAccessObjectConfiguration(
				path='Sample.DB',  # File Path for SQLite Database File
				autocommit=False
			)
		)

		# Get Connection
		con = DataAccessObjectHelper.Get('Sample')
	except DataAccessObjectConnectionError as e:
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
		con.execute("INSERT INTO LOG(TEXT) VALUES('TEST1')")
		con.execute("INSERT INTO LOG(TEXT) VALUES('TEST2')")
		con.execute("INSERT INTO LOG(TEXT) VALUES('TEST3')")

		con.commit()
		print('{} rows inserted'.format(con.affected()), file=sys.stdout)
	except DataAccessObjectExecuteError as e:
		con.rollback()
		print(str(e), file=sys.stderr)
	except DataAccessObjectCommitError as e:
		print(str(e), file=sys.stderr)
	except DataAccessObjectRollBackError as e:
		print(str(e), file=sys.stderr)
	except DataAccessObjectConnectionClosedError as e:
		print(str(e), file=sys.stderr)
		exit(-1)
	except Exception as e:
		print(str(e), file=sys.stderr)

	try:
		con.execute('SELECT * FROM LOG')

		rows = con.rows()

		for i, row in enumerate(rows):
			print('{} : {}'.format(i, row), file=sys.stdout)

		con.execute('DROP TABLE IF EXISTS LOG')
	except DataAccessObjectExecuteError as e:
		print(str(e), file=sys.stderr)
	except DataAccessObjectConnectionClosedError as e:
		print(str(e), file=sys.stderr)
		exit(-1)
	except Exception as e:
		print(str(e), file=sys.stderr)
```
