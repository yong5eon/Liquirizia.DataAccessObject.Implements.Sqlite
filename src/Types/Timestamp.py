# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsAbleToNone,
	IsNotToNone,
	IsInteger
)

from .Type import Type

__all__ = (
	'Timestamp'
)


class Timestamp(Type):
	def __init__(
			self, 
			name: str, 
			null=False,
			default=None,
			primaryKey: bool  = False,
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
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns.append(IsInteger(*vaps))
		super().__init__(
			name,
			type='TIMESTAMP',
			null=null,
			default=default,
			primaryKey=primaryKey,
			primaryKeyDesc=primaryKeyDesc,
			reference=reference,
			va=Validator(*patterns), 
			fn=None,
		)
		return
