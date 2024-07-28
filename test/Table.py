
from Liquirizia.DataAccessObject.Implements.Sqlite import *

from Liquirizia.DataAccessObject.Implements.Sqlite.Types import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Properties import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executors import *

from Liquirizia.DataModel import Model

from Liquirizia.Validator.Patterns import *

from Liquirizia.Util import PrettyPrint, PrettyDump


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
	metadata = ByteStream(name='METADATA')
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

con.run(Drop(StudentOfClass))
con.run(Drop(Class))
con.run(Drop(Student))
con.run(Create(Student))
con.run(Create(Class))
con.run(Create(StudentOfClass))

STUDENT = [
	['SU970001', 'Koo Hayoon', 'VERSION'],
	['SU970002', 'Ma Youngin', 'VERSION'],
	['SU970003', 'Kang Miran', 'VERSION'],
	['SU970004', 'Song Hahee', 'VERSION'],
]

students = []

for _ in STUDENT:
	students.append(con.run(
		Insert(Student).value(
			code=_[0],
			name=_[1],
			metadata=open(_[2], mode='rb').read(),
		)
	))

for _ in students:
	PrettyPrint(_)

con.close()
