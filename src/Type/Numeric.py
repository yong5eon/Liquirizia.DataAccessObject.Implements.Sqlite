# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsToNone,
	IsInteger,
	IsFloat,
	If,
	ToInteger,
	ToFloat,
)

from .Object import Object

from typing import Union, Tuple, List

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
			vaps: Union[Pattern, Tuple[Pattern], List[Pattern]] = [],
			fn: Handler = None,
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsInteger(*vaps)))
		else:
			patterns.append(IsInteger(*vaps))
		super().__init__(
			key=name, 
			type='INTEGER',
			null=null,
			default=default,
			va=Validator(*patterns), 
		)
		return


class Float(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: float = None,
			vaps: Tuple[Pattern, Tuple[Pattern], List[Pattern]] = [],
			fn: Handler = None,
		):
		if not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(
				IsToNone(
					If(IsInteger(ToFloat())),
					IsFloat(*vaps),
				)
			)
		else:
			patterns.append(
				If(IsInteger(ToFloat())),
				IsFloat(*vaps),
			)
		super().__init__(
			key=name, 
			type='REAL',
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		return

