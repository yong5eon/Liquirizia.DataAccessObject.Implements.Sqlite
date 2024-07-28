# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsAbleToNone,
	IsNotToNone,
	IsDateTime,
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
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsAbleToNone())
		else:
			patterns.append(IsNotToNone())
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
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
