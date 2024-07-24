from Liquirizia.DataAccessObject.Implements.Sqlite.Properties import *
from Liquirizia.DataAccessObject.Implements.Sqlite.Types import *
from Liquirizia.DataModelObject import DataModelObject

from Liquirizia.Util import PrettyPrint, PrettyDump

@Table('SampleTable')
class Model(DataModelObject):
	id = Integer('ID', autoincrement=True)
	pass

o = Model()

for sql in Model.ToString():
	print(sql)
PrettyPrint(o)