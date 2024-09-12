# -*- coding: utf-8 -*-

from typing import Any
from .Configuration import Configuration
from .Connection import Connection
from .Cursor import Cursor
from .Session import Session
from .Context import Context

from sqlite3 import register_adapter
from datetime import datetime

__all__ = (
	'Configuration',
	'Connection',
	'Cursor',
	'Session',
	'Context',
)


class DateTimeAdator(object):
	def __call__(self, o: datetime):
		return o.isoformat()

register_adapter(datetime, DateTimeAdator())
