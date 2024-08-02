# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject.Model import Executors
from Liquirizia.DataModel.Model import Model, Attribute

from ..Constraint import PrimaryKey,ForeignKey
from ..Index import Index, IndexUnique

from typing import overload

__all__ = (
	'Create'
)


class Create(Executors):
	def __init__(self, o: type[Model], notexist: bool = False):
		self.model = o
		self.executors = []
		_ = []
		for k, v in o.__dict__.items():
			if isinstance(v, Attribute):
				_.append(self.toStringAttribute(v))
		if o.__properties__['primaryKey']:
			_.append(self.toStringPrimaryKey(o.__properties__['primaryKey']))
		_.extend([self.toStringForeignKey(foreignKey) for foreignKey in o.__properties__['foreignKeys']] if o.__properties__['foreignKeys'] else [])
		self.executors.append(('CREATE TABLE {}{}({})'.format(
			' IF NOT EXISTS ' if notexist else '',
			o.__properties__['name'],
			', '.join(_)
		), ()))
		for index in o.__properties__['indexes'] if o.__properties__['indexes'] else []:
			if isinstance(index, IndexUnique):
				self.executors.append((self.toStringIndexUnique(index), ()))
				continue
			if isinstance(index, Index):
				self.executors.append((self.toStringIndex(index), ()))
				continue
		return
	
	def __iter__(self):
		return self.executors.__iter__()

	def toStringAttribute(self, attr: Attribute):
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

	def toStringPrimaryKey(self, primaryKey: PrimaryKey):
		return 'PRIMARY KEY({})'.format(
			', '.join(primaryKey.columns)
		)

	def toStringForeignKey(self, foreignKey: ForeignKey):
		return 'FOREIGN KEY({}) REFERENCES {}({})'.format(
			', '.join(foreignKey.columns),
			foreignKey.table,
			', '.join(foreignKey.references)
		)

	def toStringIndex(self, index: Index):
		return 'CREATE INDEX {}{} ON {}({}){}'.format(
			'IF NOT EXISTS ' if index.notexists else '',
			index.name,
			index.table,
			', '.join(index.colexprs),
			' WHERE {}'.format(index.expr) if index.expr else '',
		)
	
	def toStringIndexUnique(self, index: IndexUnique):
		return 'CREATE UNIQUE INDEX {}{} ON {}({}){}'.format(
			'IF NOT EXISTS ' if index.notexists else '',
			index.name,
			index.table,
			', '.join(index.colexprs),
			' WHERE {}'.format(index.expr) if index.expr else '',
		)
