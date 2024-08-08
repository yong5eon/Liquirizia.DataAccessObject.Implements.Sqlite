# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Model
from Liquirizia.DataAccessObject.Model import Executors

from ..Model import Type as ModelType
from ..Type import Type
from ..Constraint import PrimaryKey,ForeignKey
from ..Index import Index, IndexUnique

__all__ = (
	'Create'
)


class TypeToSQL(object):
	def __call__(self, attr:Type) -> str:
		return '{} {}{}{}{}{}{}{}'.format(
			attr.key,
			attr.type,
			' NOT NULL' if not attr.null else '',
			' DEFAULT {}'.format(attr.default) if attr.default else '',
			' PRIMARY KEY' if attr.primaryKey else '',
			' AUTOINCREMENT' if attr.primaryKey and attr.autoincrement else '',
			' DESC' if attr.primaryKey and attr.primaryKeyDesc else '',
			' REFERENCES {}({})'.format(attr.referenceTable, attr.referenceKey) if attr.reference else '',
		)

class PrimaryKeyToSQL(object):
	def __call__(self, key: PrimaryKey) -> str:
		return 'PRIMARY KEY({})'.format(
			', '.join(key.columns)
		)

class ForeignKeyToSQL(object):
	def __call__(self, key: ForeignKey) -> str:
		return 'FOREIGN KEY({}) REFERENCES {}({})'.format(
			', '.join(key.columns),
			key.table,
			', '.join(key.references)
		)

class IndexToSQL(object):
	def __call__(self, index: Index) -> str:
		return 'CREATE INDEX {}{} ON {}({}){}'.format(
			'IF NOT EXISTS ' if index.notexists else '',
			index.name,
			index.table,
			', '.join(index.colexprs),
			' WHERE {}'.format(index.expr) if index.expr else '',
		)

class IndexUniqueToSQL(object):
	def __call__(self, index: IndexUnique) -> str:
		return 'CREATE UNIQUE INDEX {}{} ON {}({}){}'.format(
			'IF NOT EXISTS ' if index.notexists else '',
			index.name,
			index.table,
			', '.join(index.colexprs),
			' WHERE {}'.format(index.expr) if index.expr else '',
		)

class TableToSQL(object):

	TypeToSQL = TypeToSQL()
	PrimaryKeyToSQL = PrimaryKeyToSQL()
	ForeignKeyToSQL = ForeignKeyToSQL()
	IndexToSQL = IndexToSQL()
	IndexUniqueToSQL = IndexUniqueToSQL()

	def __call__(self, o: type[Model], notexist) -> str:
		__ = []
		_ = []
		for k, v in o.__dict__.items():
			if isinstance(v, Type):
				_.append(self.TypeToSQL(v))
		if o.__properties__['primaryKey']:
			_.append(self.PrimaryKeyToSQL(o.__properties__['primaryKey']))
		_.extend([self.ForeignKeyToSQL(foreignKey) for foreignKey in o.__properties__['foreignKeys']] if o.__properties__['foreignKeys'] else [])
		__.append(('CREATE TABLE {}{}({})'.format(
			'IF NOT EXISTS ' if notexist else '',
			o.__properties__['name'],
			', '.join(_)
		), ()))
		for index in o.__properties__['indexes'] if o.__properties__['indexes'] else []:
			if isinstance(index, IndexUnique):
				__.append((self.IndexUniqueToSQL(index), ()))
				continue
			if isinstance(index, Index):
				__.append((self.IndexToSQL(index), ()))
				continue
		return __
	

class ViewToSQL(object):
	def __call__(self, o: type[Model], notexist) -> str:
		return [('CREATE VIEW {}{} AS {}'.format(
			'IF NOT EXISTS ' if notexist else '',
			o.__properties__['name'],
			o.__properties__['executor'].query,
		), ())]

	

class Create(Executors):

	TableToSQL = TableToSQL()
	ViewToSQL = ViewToSQL()

	def __init__(self, o: type[Model], notexist: bool = True):
		self.model = o
		self.executors = []
		fn = {
			ModelType.Table : Create.TableToSQL,
			ModelType.View  : Create.ViewToSQL,
		}.get(o.__properties__['type'], None)
		if fn:
			self.executors = fn(o,  notexist)
		return
	
	def __iter__(self):
		return self.executors.__iter__()
	

