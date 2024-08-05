# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsAbleToNone,
	IsDateTime,
)
from Liquirizia.DataModel import Handler

from .Type import Type
from ..Handler import Update


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
			fmt: str = '%Y-%m-%d %H:%M:%S',
			fn: Handler = Update(),
		):
		class StrToDateTime(Pattern):
			def __init__(self, fmt):
				self.fmt = fmt
				return
			def __call__(self, parameter):
				return datetime.strptime(parameter, self.fmt)
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsAbleToNone(StrToDateTime(fmt), IsDateTime(*vaps)))
		else:
			patterns.append(StrToDateTime(fmt))
			patterns.append(IsDateTime(*vaps))
		self.fmt = fmt
		super().__init__(
			key=name, 
			type='DATETIME',
			null=null,
			reference=reference,
			default=default,
			va=Validator(*patterns), 
			fn=fn,
		)
		return
