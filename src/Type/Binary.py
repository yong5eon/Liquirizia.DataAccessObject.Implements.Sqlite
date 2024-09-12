# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	IsToNone,
	IsByteArray,
)

from .Object import Object

from typing import Union, Tuple, List

__all__ = (
	'ByteArray'
)


class ByteArray(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			vaps: Union[Pattern, Tuple[Pattern], List[Pattern]] = [],
			fn: Handler = None,
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if null:
			patterns.append(IsToNone(IsByteArray(*vaps)))
		else:
			patterns.append(IsByteArray(*vaps))
		super().__init__(
			key=name, 
			type='BLOB',
			null=null,
			va=Validator(*patterns),
			fn=fn,
		)
		return
