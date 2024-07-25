# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator

from .Type import Type

__all__ = (
	'Integer'
)


class Integer(Type):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: str = None,
			check: str = None,
			autoincrement: bool = False,
			primaryKey: bool = False,
			primaryKeyDesc: bool = False,
			va: Validator = Validator(),
		):
		super().__init__(
			key=name, 
			null=null,
			default=default,
			check=check,
			primaryKey=primaryKey,
			primaryKeyDesc=primaryKeyDesc,
			va=va, 
			fn=None
		)
		self.autoincrement = autoincrement
		return

	def __str__(self):
		return '{} INTEGER{}{}{}{}{}'.format(
			self.key,
			' NOT NULL' if not self.null else '',
			' DEFAULT {}'.format(self.default) if self.default else '',
			' CHECK({})'.format(self.check) if self.check else '',
			' AUTOINCREMENT' if self.autoincrement else '',
			' PRIMARY KEY' if self.primaryKey else '',
			' DESC' if self.primaryKey and self.desc else ''
		)
