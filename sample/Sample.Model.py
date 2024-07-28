# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Helper
from Liquirizia.DataAccessObject.Errors import *
from Liquirizia.DataAccessObject.Properties.Database.Errors import *

from Liquirizia.DataAccessObject.Implements.Sqlite import Configuration, Connection
from Liquirizia.DataAccessObject.Implements.Sqlite.Types import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Properties import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executors import *

from Liquirizia.DataModel import Model

from sys import stdout, stderr
from random import randrange

# Tables
@Table(
	name = 'STUDENT',
	primaryKey=PrimaryKey('ID'),
	indexes=(
		IndexUnique('IDX_UNIQUE_STUDENT_CODE', columns='CODE'),
		Index(name='IDX_STUDENT_IS_DELETED', columns='IS_DELETED'),
		Index(name='IDX_STUDENT_AT_CREATED', columns='AT_CREATED'),
		Index(name='IDX_STUDENT_AT_UPDATED', columns='AT_UPDATED', null='LAST'),
	)
)
class Student(Model):
	id = Integer('ID', autoincrement=True)
	code = Text('CODE')
	name = Text(name='NAME')
	metadata = ByteStream(name='METADATA')
	atCreated = DateTime(name='AT_CREATED', default='"NOW"')
	atUpdated = Timestamp(name='AT_UPDATED', null=True)
	isDeleted = Text(name='IS_DELETED', default='"N"', vaps=IsIn('Y', 'N'))

@Table(
	name='CLASS',
	primaryKey=PrimaryKey('ID'),
	indexes=(
		IndexUnique(name='IDX_CLASS_CODE', columns='CODE'),
		Index(name='IDX_CLASS_IS_DELETED', columns='IS_DELETED'),
		Index(name='IDX_CLASS_AT_CREATED', columns='AT_CREATED'),
		Index(name='IDX_CLASS_AT_UPDATED', columns='AT_UPDATED'),
	)
)
class Class(Model):
	id = Integer(name='ID', autoincrement=True, primaryKey=True)
	code = Text(name='CODE')
	name = Text(name='NAME')
	atCreated = DateTime(name='AT_CREATED', default='"NOW"')
	atUpdated = Timestamp(name='AT_UPDATED', null=True)
	isDeleted = Text(name='IS_DELETED', default='"N"', vaps=IsIn('Y', 'N'))


@Table(
	name='STUDENT_CLASS',
	primaryKey=PrimaryKey(('STUDENT', 'CLASS')),
	foreignKeys=(
		ForeignKey(columns='STUDENT', table='STUDENT', references='ID'),
		ForeignKey(columns='CLASS', table='CLASS', references='ID')
	),
	indexes=(
		Index(name='IDX_STUDENT_CLASS_SCORE', columns='IS_DELETED'),
		Index(name='IDX_STUDENT_CLASS_AT_CREATED', columns='AT_CREATED'),
		Index(name='IDX_STUDENT_CLASS_AT_UPDATED', columns='AT_UPDATED'),
	)
)
class StudentOfClass(Model):
	studentId = Integer(name='STUDENT')
	studentName = Text(name='STUDENT_NAME', reference=Student.name)
	classId = Integer(name='CLASS')
	className = Text(name='CLASS_NAME', reference=Class.name)
	score = Float(name='SCORE', null=True)
	atCreated = DateTime(name='AT_CREATED', default='"NOW"')
	atUpdated = Timestamp(name='AT_UPDATED', null=True)


# View 

# Model for Virtual Table
class StudentsOfClass(Model(
	Select(StudentOfClass).
	joinInner(Student, IsEqual(StudentOfClass.studentId, Student.id)).
	joinLeftOuter(Student, IsEqal(StudentOfClass.classId, Class.id)).
	where(
		IsNotNull(StudentOfClass.score)
	)
)):
	id = Integer(mapping=Student.id)
	name = Text(mapping=Student.name)
	atCreated = DateTime(mapping=Student.atCreated)
	atUpdated = Timestamp(mapping=Student.atUpdated)
	classId = Integer(mapping=Class.id)
	className = Text(mapping=Class.name)
	score = Real(mapping=StudentOfClass.score)
	

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
		con.begin()
		# create table
		con.execute(Create(Student))
		con.execute(Create(Class))
		con.execute(Create(StudentOfClass))
		# drop table
		con.execute(Drop(StudentOfClass))
		con.execute(Drop(Class))
		con.execute(Drop(Student))
		con.commit()

		STUDENT = [
			['SU970001', 'Koo Hayoon', 'VERSION.txt'],
			['SU970002', 'Ma Youngin', 'VERSION.txt'],
			['SU970003', 'Kang Miran', 'VERSION.txt'],
			['SU970004', 'Song Hahee', 'VERSION.txt'],
		]

		CLASS = [
			['CS000', 'Concept of Computer Science'],
			['CS100', 'Concept of Programming Language'],
			['CS101', 'C'],
			['CS102', 'C++'],
			['CS103', 'Java'],
			['CS104', 'JavaScript'],
			['CS105', 'Python'],
			['CS105', 'Python'],
			['CS120', 'Operating System'],
			['CS130', 'Network'],
			['CS131', 'TCP/IP'],
			['CS132', 'HTTP'],
			['CS140', 'Database'],
			['CS141', 'Practice of RDBMS with MySQL'],
			['CS142', 'Practice of RDBMS with PostgreSQL'],
			['CS150', 'Distributed System'],
		]

		STUDENT_OF_CLASS = [
			['SU970001', 'CS000'],
			['SU970001', 'CS100'],
			['SU970001', 'CS120'],
			['SU970001', 'CS130'],
			['SU970002', 'CS000'],
			['SU970002', 'CS100'],
			['SU970002', 'CS101'],
			['SU970002', 'CS102'],
			['SU970003', 'CS000'],
			['SU970003', 'CS120'],
			['SU970003', 'CS130'],
			['SU970003', 'CS140'],
			['SU970003', 'CS150'],
			['SU970004', 'CS000'],
			['SU970004', 'CS130'],
			['SU970004', 'CS132'],
			['SU970004', 'CS140'],
			['SU970004', 'CS142'],
			['SU970004', 'CS150'],
		]

		# with session
		with Session(con) as s:
			s.run(Create(Student))
			s.run(Create(Class))
			s.run(Create(StudentOfClass))

			for _ in STUDENT:
				s.run(
					Insert(Student).value(
						code=_[0],
						name=_[1],
						metadata=open(_[2]).read(),
					)
				)

			for _ in CLASS:
				s.run(
					Insert(Student).value(
						code=_[0],
						name=_[1],
					)
				)

			for _ in STUDENT_OF_CLASS:
				s.run(
					Insert(StudentOfClass).
					value(
						studentId=Select(Student).where(IsEqual(Student.code,_[0]).value(Student.id),
						classId=Select(Class).where(IsEqual(Class.code,_[1]).value(Class.id),
					)
				)
				s.run(
					Update(StudentOfClass).
					set(
						score=randrange(0, 45)/10
					).
					where(
						studentId=Select(Student).where(IsEqual(Student.code,_[0]).value(Student.id),
						classId=Select(Class).where(IsEqual(Class.code,_[1]).value(Class.id),
					)
				)

			# select with model
			__ = s.sync(Student)
			for _ in __:
				print(_)
			__ = s.sync(Class)
			for _ in __:
				print(_)
			__ = s.sync(StudentsOfClass)
			for _ in __:
				print(_)

			# select directly
			__ = s.run(
				Select(StudentOfClass).
				join(
					Class, Inner(StudentOfClass.classId, Class.id)
				).
				join(
					Student, LeftOuter(StudentOfClass.studentId, Student.id)
				).
				where(
					IsIn(Class.code, ('CS000'))
				).
				value(
				)
			)

	except DataAccessObjectExecuteError as e:
		con.rollback()
		print(str(e), file=stderr)
	except DataAccessObjectCommitError as e:
		print(str(e), file=stderr)
	except DataAccessObjectRollBackError as e:
		print(str(e), file=stderr)
	except DataAccessObjectConnectionError as e:
		print(str(e), file=stderr)
	except Exception as e:
		print(str(e), file=stderr)
