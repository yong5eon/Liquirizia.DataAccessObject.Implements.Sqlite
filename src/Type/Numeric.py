# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsToNone,
	IsInteger,
	IsFloat,
)

from .Object import Object

__all__ = (
	'Integer',
	'Float',
)


class Integer(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: str = None,
			autoincrement: bool = False,
			vaps: tuple[Pattern, tuple[Pattern], list[Pattern]] = [],
			fn: Handler = None,
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsInteger(*vaps)))
		else:
			if autoincrement:
				patterns.append(IsToNone(IsInteger(*vaps)))
			else:
				patterns.append(IsInteger(*vaps))
		super().__init__(
			key=name, 
			type='INTEGER',
			null=null,
			default=default,
			autoincrement=autoincrement,
			va=Validator(*patterns), 
		)
		return


class Float(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: float = None,
			vaps: tuple[Pattern, tuple[Pattern], list[Pattern]] = [],
			fn: Handler = None,
		):
		if not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsFloat(*vaps)))
		else:
			patterns.append(IsFloat(*vaps))
		super().__init__(
			key=name, 
			type='REAL',
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		return

