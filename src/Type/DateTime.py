# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsAbleToNone,
	IsNotToNone,
	IsDateTime,
	ToTypeOf,
)

from .Type import Type

from datetime import datetime

__all__ = (
	'DateTime'
)


class DateTime(Type):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			reference: Type = None,
			default: datetime = None,
			vaps: tuple[Pattern, tuple[Pattern], list[Pattern]] = [],
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsAbleToNone(StrToDateTime(), IsDateTime(*vaps)))
		else:
			patterns.append(StrToDateTime())
			patterns.append(IsDateTime(*vaps))
		super().__init__(
			key=name, 
			type='DATETIME',
			null=null,
			reference=reference,
			default=default,
			va=Validator(*patterns), 
			fn=None
		)
		return


class StrToDateTime(Pattern):
	def __init__(self, fmt='%Y-%m-%d %H:%M:%S'):
		self.fmt = fmt
		return
	def __call__(self, parameter):
		return datetime.strptime(parameter, self.fmt)
