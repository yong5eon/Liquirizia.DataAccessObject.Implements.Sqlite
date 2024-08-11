# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsAbleToNone,
	IsString
)

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
			patterns.append(IsAbleToNone(IsString(*vaps)))
		else:
			patterns.append(IsString(*vaps))
		super().__init__(
			key=name, 
			type='TEXT',
			null=null,
			default=default,
			primaryKey=primaryKey,
			primaryKeyDesc=primaryKeyDesc,
			reference=reference,
			va=Validator(*patterns),
		)
		return
