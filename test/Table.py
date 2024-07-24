from Liquirizia.DataAccessObject.Implements.Sqlite.Properties import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Types import *
from Liquirizia.DataModel import Model

from Liquirizia.Util import PrettyPrint, PrettyDump

@Table('SampleTable')
class SampleModel(Model):
	id = Integer('ID', autoincrement=True)
	pass

o = Model()

for sql in Model.ToString():
	print(sql)
PrettyPrint(o)