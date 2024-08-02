# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsAbleToNone,
	IsNotToNone,
	IsFloat,
)

from .Type import Type

__all__ = (
	'Float'
)


class Float(Type):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: float = None,
			primaryKey: bool = False,
			primaryKeyDesc: bool = False,
			reference: Type = None,
			vaps: tuple[Pattern, tuple[Pattern], list[Pattern]] = [],
		):
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsAbleToNone())
		else:
			patterns.append(IsNotToNone())
		if not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns.append(IsFloat(*vaps))
		super().__init__(
			key=name, 
			type='REAL',
			null=null,
			default=default,
			primaryKey=primaryKey,
			primaryKeyDesc=primaryKeyDesc,
			reference=reference,
			va=Validator(*patterns), 
			fn=None
		)
		return
