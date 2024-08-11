# -*- coding: utf-8 -*-

from enum import Enum, unique, auto

__all__ = (
	'Type'
)


@unique
class Type(Enum):
	Table = auto()
	View  = auto()
