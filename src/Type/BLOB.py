# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	IsAbleToNone,
	IsBytes,
)

from .Type import Type

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
			fn=None
		)
		return
