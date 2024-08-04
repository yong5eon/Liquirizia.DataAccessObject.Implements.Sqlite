# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsAbleToNone,
	IsInteger
)

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
			autoincrement: bool = False,
			primaryKey: bool = False,
			primaryKeyDesc: bool = False,
			reference: Type = None,
			vaps: tuple[Pattern, tuple[Pattern], list[Pattern]] = [],
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsAbleToNone(IsInteger(*vaps)))
		else:
			if autoincrement:
				patterns.append(IsAbleToNone(IsInteger(*vaps)))
			else:
				patterns.append(IsInteger(*vaps))
		super().__init__(
			key=name, 
			type='INTEGER',
			null=null,
			default=default,
			autoincrement=autoincrement,
			primaryKey=primaryKey,
			primaryKeyDesc=primaryKeyDesc,
			reference=reference,
			va=Validator(*patterns), 
			fn=None
		)
		return
