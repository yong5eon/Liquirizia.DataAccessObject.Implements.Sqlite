# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsToNone,
	IsString
)

from .Object import Object

from typing import Union, Tuple, List

__all__ = (
	'Text'
)


class Text(Object):
	def __init__(
			self, 
			name: str, 
			null: bool = False,
			default: str = None,
			vaps: Union[Pattern, Tuple[Pattern], List[Pattern]] = [],
			fn: Handler = None
		):
		if vaps and not isinstance(vaps, (tuple, list)): vaps = [vaps]
		patterns = []
		if default:
			patterns.append(SetDefault(default))
		if null:
			patterns.append(IsToNone(IsString(*vaps)))
		else:
			patterns.append(IsString(*vaps))
		super().__init__(
			key=name, 
			type='TEXT',
			null=null,
			default=default,
			va=Validator(*patterns),
			fn=fn,
		)
		return
