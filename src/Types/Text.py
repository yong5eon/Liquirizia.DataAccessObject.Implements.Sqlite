# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator

from .Type import Type

__all__ = (
	'Text'
)


class Text(Type):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: str = None,
			check: str = None,
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
		return

	def __str__(self):
		return '{} TEXT{}{}{}{}'.format(
			self.key,
			' NOT NULL' if not self.null else '',
			' DEFAULT {}'.format(self.default) if self.default else '',
			' CHECK({})'.format(self.check) if self.check else '',
			' PRIMARY KEY' if self.primaryKey else '',
			' DESC' if self.primaryKey and self.primaryKeyDesc else '',
		)
