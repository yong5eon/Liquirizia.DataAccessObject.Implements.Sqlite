from Liquirizia.DataAccessObject.Implements.Sqlite.Types import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Properties import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Executors import *

from Liquirizia.DataModel import Model

from Liquirizia.Util import PrettyPrint, PrettyDump


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
	# metadata = Buffer(name='METADATA')
	atCreated = DateTime(name='AT_CREATED', default='"NOW"')
	atUpdated = Timestamp(name='AT_UPDATED', null=True)
	isDeleted = Text(name='IS_DELETED', default='"N"', check='IS_DELETED IN ("Y", "N")')

for sql in Create(Student):
	PrettyPrint(sql)
	print(sql)

o = Student(
	id=1,
	code='18238232',
)
PrettyPrint(o)
print(o)