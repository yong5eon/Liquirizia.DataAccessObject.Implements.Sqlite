
from Liquirizia.DataAccessObject.Implements.Sqlite import *

from Liquirizia.DataAccessObject.Implements.Sqlite.Model import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Type import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Constraint import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Index import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executor import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executor.Filter import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executor.Order import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executor.Join import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executor.Exprs import *

from Liquirizia.DataModel import Model

from Liquirizia.Validator.Patterns import IsIn

from Liquirizia.Util import *

from random import randrange
from datetime import datetime


@Table(
	name = 'STUDENT',
	indexes=(
		IndexUnique('IDX_UNIQUE_STUDENT_CODE', colexprs='CODE'),
		Index(name='IDX_STUDENT_IS_DELETED', colexprs='IS_DELETED'),
		Index(name='IDX_STUDENT_AT_CREATED', colexprs='AT_CREATED DESC'),
		Index(name='IDX_STUDENT_AT_UPDATED', colexprs='AT_UPDATED DESC'),
	)
)
class Student(Model):
	id = Integer('ID', primaryKey=True, autoincrement=True)
	code = Text('CODE')
	name = Text(name='NAME')
	metadata = BLOB(name='METADATA')
	atCreated = DateTime(name='AT_CREATED', default='CURRENT_TIMESTAMP')
	atUpdated = Timestamp(name='AT_UPDATED', null=True)
	isDeleted = Text(name='IS_DELETED', default='"N"', vaps=IsIn('Y', 'N'))

@Table(
	name='CLASS',
	indexes=(
		IndexUnique(name='IDX_CLASS_CODE', colexprs='CODE'),
		Index(name='IDX_CLASS_IS_DELETED', colexprs='IS_DELETED'),
		Index(name='IDX_CLASS_AT_CREATED', colexprs='AT_CREATED DESC'),
		Index(name='IDX_CLASS_AT_UPDATED', colexprs='AT_UPDATED DESC'),
	)
)
class Class(Model):
	id = Integer(name='ID', primaryKey=True, autoincrement=True)
	code = Text(name='CODE')
	name = Text(name='NAME')
	atCreated = DateTime(name='AT_CREATED', default='CURRENT_TIMESTAMP')
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
		Index(name='IDX_STUDENT_CLASS_SCORE', colexprs='SCORE'),
		Index(name='IDX_STUDENT_CLASS_AT_CREATED', colexprs='AT_CREATED DESC'),
		Index(name='IDX_STUDENT_CLASS_AT_UPDATED', colexprs='AT_UPDATED DESC'),
	)
)
class StudentOfClass(Model):
	studentId = Integer(name='STUDENT')
	studentName = Text(name='STUDENT_NAME', reference=Student.name)
	classId = Integer(name='CLASS')
	className = Text(name='CLASS_NAME', reference=Class.name)
	score = Float(name='SCORE', null=True)
	atCreated = DateTime(name='AT_CREATED', default='CURRENT_TIMESTAMP')
	atUpdated = Timestamp(name='AT_UPDATED', null=True)

for sql in Create(Student):
	PrettyPrint(sql)

for sql in Create(Class):
	PrettyPrint(sql)

for sql in Create(StudentOfClass):
	PrettyPrint(sql)

con = Connection(Configuration(
	path='tmp/Sample.DB',  # File Path for SQLite Database File
	autocommit=False
))

con.connect()

con.runs(Drop(StudentOfClass))
con.runs(Drop(Class))
con.runs(Drop(Student))
con.runs(Create(Student))
con.runs(Create(Class))
con.runs(Create(StudentOfClass))

STUDENT = [
	['SU970001', 'Koo Hayoon', 'VERSION'],
	['SU970002', 'Ma Youngin', 'VERSION'],
	['SU970003', 'Kang Miran', 'VERSION'],
	['SU970004', 'Song Hahee', 'VERSION'],
]
students = []
for _ in STUDENT:
	students.append(con.run(
		Insert(Student).values(
			code=_[0],
			name=_[1],
			metadata=open(_[2], mode='rb').read(),
		),
		cb=Student
	)[0])

PrettyPrint(students)

students = con.run(Select(Student), cb=Student)
PrettyPrint(students)

CLASS = [
	['CS000', 'What is Computer Science'],
	['CS100', 'Programming Language'],
	['CS101', 'C'],
	['CS102', 'C++'],
	['CS103', 'Java'],
	['CS104', 'JavaScript'],
	['CS105', 'Python'],
	['CS120', 'Operating System'],
	['CS130', 'Network'],
	['CS131', 'TCP/IP'],
	['CS132', 'HTTP'],
	['CS140', 'Database'],
	['CS141', 'Practice of RDBMS with MySQL'],
	['CS142', 'Practice of RDBMS with PostgreSQL'],
	['CS150', 'Distributed System'],
	['CS160', 'AI(Artificial Intelligence)'],
]

classes = []
for _ in CLASS:
	classes.append(con.run(
		Insert(Class).values(
			code=_[0],
			name=_[1],
		)
	, cb=Class)[0])

for _ in classes:
	PrettyPrint(_)

classes = con.run(Select(Class), cb=Class)
PrettyPrint(classes)

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

for scode, ccode in STUDENT_OF_CLASS:
	s = con.run(Select(Student).where(IsEqualTo(Student.code, scode)), cb=Student)[0]
	c = con.run(Select(Class).where(IsEqualTo(Class.code, ccode)), cb=Class)[0]
	con.run(Insert(StudentOfClass).values(
		studentId=s.id,
		studentName=s.name,
		classId=c.id,
		className=c.name,
	))

studentsOfClasses = con.run(Select(StudentOfClass), cb=StudentOfClass)
PrettyPrint(studentsOfClasses)

for _ in studentsOfClasses:
	o = con.run(
		Update(StudentOfClass).set(
			score=(randrange(10, 45)/10),
			atUpdated=int(round(datetime.now().timestamp()*1000)),
		).where(
			IsEqualTo(StudentOfClass.studentId, _.studentId),
			IsEqualTo(StudentOfClass.classId, _.classId),
		),
		cb=StudentOfClass
	)
	PrettyPrint(o[0])

studentsOfClasses = con.run(Select(StudentOfClass), cb=StudentOfClass)
PrettyPrint(studentsOfClasses)

exec = 	Select(StudentOfClass).join(
		LeftOuter(Student, IsEqualTo(StudentOfClass.studentId, Student.id)),
		LeftOuter(Class, IsEqualTo(StudentOfClass.classId, Class.id)),
	).values(
		Alias(Student.id, 'STUDENT_ID'),
		Alias(Student.name, 'STUDENT_NAME'),
		Alias(Class.id, 'CLASS_ID'),
		Alias(Class.name, 'CLASS_NAME'),
		Count(StudentOfClass.score, 'COUNT'),
		Sum(StudentOfClass.score, 'SUM'),
		Average(StudentOfClass.score, 'AVG'),
		Alias(Student.atCreated, 'STUDENT_AT_CREATED'),
		Alias(StudentOfClass.atCreated, 'STUDENT_OF_CLASS_AT_CREATED'),
		Alias(StudentOfClass.atUpdated, 'STUDENT_OF_CLASS_AT_UPDATED'),
	).where(
		IsGreaterThan(StudentOfClass.score, 1)
	).groupBy(
		Student.id,
	).having(
		IsGreaterEqualTo('AVG', 3)
	).orderBy(
		Ascend('SUM'),
		Descend('AVG')
	).limit(3, 1)

PrettyPrintSQL(exec.query)
PrettyPrint(con.run(exec))

con.close()
