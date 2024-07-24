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
			va: Validator = Validator(),
			null=False,
			default=None,
			autoincrement = False,
			primaryKey = False,
			desc = False,
		):
		super().__init__(name, va, None)
		self.null = null
		self.default = default
		self.autoincrement = autoincrement
		self.primaryKey = primaryKey
		self.desc = desc
		return
	
	def toString(self):
		return '{} INTEGER{}{}{}{}{}'.format(
			self.name,
			' NOT NULL' if not self.null else '',
			' DEFAULT {}'.format(self.default) if self.default else '',
			' AUTOINCREMENT' if self.autoincrement else '',
			' PRIMARY KEY' if self.primaryKey else '',
			' DESC' if self.primaryKey and self.desc else ''
		)
