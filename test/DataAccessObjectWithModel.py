# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.DataAccessObject import Helper
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from Liquirizia.DataAccessObject.Implements.Sqlite import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Model import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Type import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Constraint import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executor import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executor.Filters import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executor.Orders import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executor.Joins import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executor.Exprs import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executor.Functions import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Handler import *

from Liquirizia.DataModel import Model

from datetime import datetime
from time import mktime


@Table(
	name='TEST',
	constraints=(
		PrimaryKey(cols='ID', autoincrement=True),
	),
	indexes=(
		Index(name='IDX_TEST_COL_INTEGER', colexprs='COL_INTEGER'),
	),
	fn=Updater(),
)
class TestModel(Model):
	id = INTEGER(name='ID')
	colInteger = INTEGER(name='COL_INTEGER', null=True)
	colFloat = FLOAT(name='COL_FLOAT', null=True)
	colText = TEXT(name='COL_TEXT', null=True)
	colByteArray = BLOB(name='COL_BLOB', null=True)
	colDateTime = DATETIME(name='COL_DATETIME', null=True)
	colTimestamp = TIMESTAMP(name='COL_TIMESTAMP', null=True)


class TestDataAccessObject(Case):
	@classmethod
	def setUpClass(cls):
		Helper.Set(
			'Sample',
			Connection,
			Configuration(
				path=':memory:',  # File Path for SQLite Database File
				autocommit=False,
			)
		)
		return super().setUpClass()

	@Order(1)
	def testCreate(self):
		con = Helper.Get('Sample')
		con.run(Create(TestModel))
		return

	@Order(2)
	def testDrop(self):
		con = Helper.Get('Sample')
		con.run(Create(TestModel))
		con.run(Drop(TestModel))
		return

	@Order(3)
	def testInsert(self):
		con = Helper.Get('Sample')
		con.run(Create(TestModel))
		row = con.run(Insert(TestModel).values(
			colInteger=1,
			colFloat=2.0,
			colText='Hello Liquirizia',
			colByteArray=open('VERSION', mode='rb').read(),
			colDateTime=datetime.now(),
			colTimestamp=int(mktime(datetime.now().timetuple())),
		))
		ASSERT_IS_NOT_NONE(row)
		ASSERT_IS_EQUAL(row.id, 1)
		ASSERT_IS_EQUAL(row.colInteger, 1)
		ASSERT_IS_EQUAL(row.colFloat, 2.0)
		ASSERT_IS_EQUAL(row.colText, 'Hello Liquirizia')
		ASSERT_IS_EQUAL(row.colByteArray, open('VERSION', mode='rb').read())
		ASSERT_TRUE(isinstance(row.colDateTime, datetime))
		ASSERT_TRUE(isinstance(row.colTimestamp, int))
		return

	@Order(4)
	def testUpdate(self):
		con = Helper.Get('Sample')
		con.run(Create(TestModel))
		inserted = con.run(Insert(TestModel).values(
			colInteger=1,
			colFloat=2.0,
			colText='Hello Liquirizia',
			colByteArray=open('VERSION', mode='rb').read(),
			colDateTime=datetime.now(),
			colTimestamp=int(mktime(datetime.now().timetuple())),
		))
		updated = con.run(Update(TestModel).where(IsEqualTo(TestModel.id, inserted.id)).set(
			colInteger=2,
			colFloat=2.8,
			colText='Hello World',
			colByteArray=open('README.md', mode='rb').read(),
			colDateTime=datetime.now(),
			colTimestamp=int(mktime(datetime.now().timetuple())),
		))

		ASSERT_IS_NOT_NONE(updated)
		ASSERT_IS_EQUAL(updated.id, 1)
		ASSERT_IS_EQUAL(updated.colInteger, 2)
		ASSERT_IS_EQUAL(updated.colFloat, 2.8)
		ASSERT_IS_EQUAL(updated.colText, 'Hello World')
		ASSERT_TRUE(isinstance(updated.colDateTime, datetime))
		ASSERT_TRUE(isinstance(updated.colTimestamp, int))
		ASSERT_IS_NOT_EQUAL(inserted.colInteger, updated.colInteger)
		ASSERT_IS_NOT_EQUAL(inserted.colFloat, updated.colFloat)
		ASSERT_IS_NOT_EQUAL(inserted.colText, updated.colText)
		return

	@Order(5)
	def testUpdateWithAutoUpdater(self):
		con = Helper.Get('Sample')
		con.run(Create(TestModel))
		inserted = con.run(Insert(TestModel).values(
			colInteger=1,
			colFloat=2.0,
			colText='Hello Liquirizia',
			colByteArray=open('VERSION', mode='rb').read(),
			colDateTime=datetime.now(),
			colTimestamp=int(mktime(datetime.now().timetuple())),
		))
		inserted.colInteger = 2
		inserted.colFloat = 2.8
		inserted.colText = 'Hello World'

		updated = con.run(Get(TestModel).where(IsEqualTo(TestModel.id, inserted.id)).to(TestModel))

		ASSERT_IS_NOT_NONE(updated)
		ASSERT_IS_EQUAL(updated.id, 1)
		ASSERT_IS_EQUAL(updated.colInteger, 2)
		ASSERT_IS_EQUAL(updated.colFloat, 2.8)
		ASSERT_IS_EQUAL(updated.colText, 'Hello World')
		ASSERT_TRUE(isinstance(updated.colDateTime, datetime))
		ASSERT_TRUE(isinstance(updated.colTimestamp, int))
		return

	@Order(6)
	def testDelete(self):
		con = Helper.Get('Sample')
		con.run(Create(TestModel))
		inserted = con.run(Insert(TestModel).values(
			colInteger=1,
			colFloat=2.0,
			colText='Hello Liquirizia',
			colByteArray=open('VERSION', mode='rb').read(),
			colDateTime=datetime.now(),
			colTimestamp=int(mktime(datetime.now().timetuple())),
		))
		con.run(Delete(TestModel).where(IsEqualTo(TestModel.id, inserted.id)))
		updated = con.run(Get(TestModel).where(IsEqualTo(TestModel.id, inserted.id)).to(TestModel))
		ASSERT_IS_NONE(updated)
		return
