# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	IsAbleToNone,
	IsNotToNone,
	SetDefault,
	IsBytes,
	IsByteStream,
)

from .Type import Type

__all__ = (
	'ByteStream'
)


class ByteStream(Type):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			reference: Type = None,
			vaps: tuple[Pattern, tuple[Pattern], list[Pattern]] = [],
		):
		patterns = []
		if null:
			patterns.append(IsAbleToNone())
		else:
			patterns.append(IsNotToNone())
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
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
