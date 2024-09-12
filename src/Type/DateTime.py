# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsToNone,
	IsDateTime,
	IsInteger,
	If,
	IsString,
)

from .Object import Object

from datetime import datetime
from typing import Union, Tuple, List

__all__ = (
	'DateTime',
	'Timestamp',
)


class DateTime(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: datetime = None,
			vaps: Union[Pattern, Tuple[Pattern], List[Pattern]] = [],
			fn: Handler = None,
		):
		class ISOFormatStringToDateTime(Pattern):
			def __call__(self, parameter):
				return datetime.fromisoformat(parameter)
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(
				IsToNone(
					If(IsString(ISOFormatStringToDateTime())),
					IsDateTime(*vaps),
				)
			)
		else:
			patterns.append(IsDateTime(*vaps))
		super().__init__(
			key=name, 
			type='DATETIME',
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		return


class Timestamp(Object):
	def __init__(
			self, 
			name: str, 
			null=False,
			default=None,
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
			name,
			type='TIMESTAMP',
			null=null,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		return
