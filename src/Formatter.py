# -*- coding: utf-8 -*-

from datetime import datetime
import json

__all__ = (
	'Formatter'
)


class Formatter(object):
	"""Query Formatter for Sqlite"""

	def __init__(self, sql, *args, **kwargs):
		self.sql = sql

		self.args = []
		self.kwargs = {}

		for arg in args:
			if arg is None:
				self.args.append('NULL')
			elif isinstance(arg, (int, float)):
				self.args.append(arg)
			elif isinstance(arg, str):
				self.args.append(self.fromString(arg))
			elif isinstance(arg, bool):
				self.args.append(arg)
			elif isinstance(arg, (list, tuple)):
				self.args.append(self.fromList(arg))
			elif isinstance(arg, dict):
				self.args.append(self.fromDict(arg))
			elif isinstance(arg, datetime):
				self.args.append(self.fromString(str(arg)))
			else:
				raise RuntimeError('{} is not valid type for SQL formatting'.format(arg))

		for key, arg in kwargs.items():
			if arg is None:
				self.kwargs[key] = 'NULL'
			elif isinstance(arg, (int, float)):
				self.kwargs[key] = arg
			elif isinstance(arg, str):
				self.kwargs[key] = self.fromString(arg)
			elif isinstance(arg, bool):
				self.kwargs[key] = arg
			elif isinstance(arg, (list, tuple)):
				self.kwargs[key] = self.fromList(arg)
			elif isinstance(arg, dict):
				self.kwargs[key] = self.fromDict(arg)
			elif isinstance(arg, datetime):
				self.kwargs[key] = self.fromString(str(arg))
			else:
				raise RuntimeError('{} is not valid type for SQL formatting'.format(arg))

		return

	def __str__(self):
		return self.sql.format(*self.args, **self.kwargs)

	def __repr__(self):
		return self.sql.format(*self.args, **self.kwargs)

	def fromString(self, value, suffix='\''):
		value = value.replace('\'', '\'\'')
		return '{}{}{}'.format(suffix, value, suffix)

	def fromList(self, value):
		ti = None
		list = []
		for item in value:
			if ti and item and not isinstance(item, ti):
				raise RuntimeError('{} is different type in list'.format(item))
			if not ti and item:
				ti = type(item)
			if item is None:
				list.append('NULL')
			elif isinstance(item, (int, float)):
				list.append(item)
			elif isinstance(item, str):
				list.append(self.fromString(item, suffix='"'))
			elif isinstance(item, bool):
				list.append(item)
			elif isinstance(item, datetime):
				list.append(str(item))
			else:
				raise RuntimeError('{} is not valid type for SQL formatting'.format(item))
		return '{}'.format('{}'.format(list).replace('\'', '')).replace('[', '').replace(']', '')

	def fromDict(self, value):
		dict = json.dumps(value, ensure_ascii=False)
		return '{}'.format(dict)
