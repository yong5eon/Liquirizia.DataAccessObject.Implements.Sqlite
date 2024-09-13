# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Model
from Liquirizia.DataAccessObject.Model import Executors

from ..Model import Type as ModelType, Index
from ..Type import Object
from ..Constraint import PrimaryKey,ForeignKey, Unique

from typing import Type

__all__ = (
	'Create'
)


class TypeToSQL(object):
	def __call__(self, attr: Object) -> str:
		return '{} {}{}{}'.format(
			attr.key,
			attr.type,
			' NOT NULL' if not attr.null else '',
			' DEFAULT {}'.format(attr.default) if attr.default else '',
		)

class PrimaryKeyToSQL(object):
	def __call__(self, key: PrimaryKey) -> str:
		return 'PRIMARY KEY({}{})'.format(
			', '.join(key.cols),
			' AUTOINCREMENT' if key.autoincrement else '',
		)

class ForeignKeyToSQL(object):
	def __call__(self, key: ForeignKey) -> str:
		return 'FOREIGN KEY({}) REFERENCES {}({})'.format(
			', '.join(key.cols),
			key.reference,
			', '.join(key.referenceCols)
		)

class UniqueToSQL(object):
	def __call__(self, index: Unique) -> str:
		return 'CREATE UNIQUE INDEX {}{} ON {}({}){}'.format(
			'IF NOT EXISTS ' if index.notexists else '',
			index.name,
			index.table,
			', '.join(index.colexprs),
			' WHERE {}'.format(index.expr) if index.expr else '',
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


class TableToSQL(object):

	TypeToSQL = TypeToSQL()
	PrimaryKeyToSQL = PrimaryKeyToSQL()
	ForeignKeyToSQL = ForeignKeyToSQL()
	UniqueToSQL = UniqueToSQL()
	IndexToSQL = IndexToSQL()

	def __call__(self, o: Type[Model], notexist) -> str:
		__ = []
		_ = []
		for k, v in o.__dict__.items():
			if isinstance(v, Object):
				_.append(self.TypeToSQL(v))
		for constraint in o.__properties__['constraints'] if o.__properties__['constraints'] else []:
			if isinstance(constraint, PrimaryKey):
				_.append(self.PrimaryKeyToSQL(constraint))
				continue
			if isinstance(constraint, ForeignKey):
				_.append(self.ForeignKeyToSQL(constraint))
		__.append(('CREATE TABLE {}{}({})'.format(
			'IF NOT EXISTS ' if notexist else '',
			o.__properties__['name'],
			', '.join(_)
		), ()))
		for constraint in o.__properties__['constraints'] if o.__properties__['constraints'] else []:
			if isinstance(constraint, Unique):
				__.append((self.UniqueToSQL(constraint), ()))
				continue
		for index in o.__properties__['indexes'] if o.__properties__['indexes'] else []:
			if isinstance(index, Index):
				__.append((self.IndexToSQL(index), ()))
				continue
		return __
	

class ViewToSQL(object):
	def __call__(self, o: Type[Model], notexist) -> str:
		return [('CREATE VIEW {}{} AS {}'.format(
			'IF NOT EXISTS ' if notexist else '',
			o.__properties__['name'],
			o.__properties__['executor'].query,
		), ())]


class Create(Executors):

	TableToSQL = TableToSQL()
	ViewToSQL = ViewToSQL()

	def __init__(self, o: Type[Model], notexist: bool = True):
		self.model = o
		self.executors = []
		fn = {
			ModelType.Table : Create.TableToSQL,
			ModelType.View  : Create.ViewToSQL,
		}.get(o.__properties__['type'], None)
		if fn:
			self.executors = fn(o, notexist)
		return
	
	def __iter__(self):
		return self.executors.__iter__()
	

