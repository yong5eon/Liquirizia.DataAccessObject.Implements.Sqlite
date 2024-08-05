# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	IsAbleToNone,
	IsBytes,
)
from Liquirizia.DataModel import Handler

from .Type import Type

from ..Handler import Update

__all__ = (
	'BLOB'
)


class BLOB(Type):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			reference: Type = None,
			vaps: tuple[Pattern, tuple[Pattern], list[Pattern]] = [],
			fn: Handler = Update()
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if null:
			patterns.append(IsAbleToNone(IsBytes(*vaps)))
		else:
			patterns.append(IsBytes(*vaps))
		super().__init__(
			key=name, 
			type='BLOB',
			null=null,
			reference=reference,
			va=Validator(*patterns), 
			fn=fn,
		)
		return
