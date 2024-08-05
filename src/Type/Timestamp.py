# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsAbleToNone,
	IsInteger
)
from Liquirizia.DataModel import Handler

from .Type import Type
from ..Handler import Update

from datetime import datetime

__all__ = (
	'Timestamp'
)


class Timestamp(Type):
	def __init__(
			self, 
			name: str, 
			null=False,
			default=None,
			vaps: tuple[Pattern, tuple[Pattern], list[Pattern]] = [],
			fn: Handler = Update(),
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsAbleToNone(IsInteger(*vaps)))
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
