# -*- coding: utf-8 -*-

from ..Expr import Expr
from ...Type import Object

__all__ = (
	'IsEqualTo',
	'IsNotEqualTo',
	'IsGreaterThan',
	'IsGreaterEqualTo',
	'IsLessEqualTo',
	'IsLessThan',
)


class IsEqualTo(Expr):
	"""Is Equal Filter Class"""

	def __init__(self, attr: Object, other) -> None:
		self.attr = attr
		self.other = other
		return

	def __str__(self):
		return '{} = {}'.format(
			str(self.attr),
			'{}.{}'.format(self.other.model.__properties__['name'], self.other.key) if isinstance(self.other, Object) else self.encode(self.other),
		)


class IsNotEqualTo(Expr):
	"""Is Not Equal Filter Class"""

	def __init__(self, attr: Object, other) -> None:
		self.attr = attr
		self.other = other
		return

	def __str__(self):
		return '{} != {}'.format(
			str(self.attr),
			str(self.other) if isinstance(self.other, Object) else self.encode(self.other),
		)


class IsGreaterEqualTo(Expr):
	"""Is Greater Equal Filter Class"""

	def __init__(self, attr: Object, other) -> None:
		self.attr = attr
		self.other = other
		return

	def __str__(self):
		return '{} >= {}'.format(
			str(self.attr),
			str(self.other) if isinstance(self.other, Object) else self.encode(self.other),
		)

class IsGreaterThan(Expr):
	"""Is Greater Than Filter Class"""

	def __init__(self, attr, other) -> None:
		self.attr = attr
		self.other = other
		return

	def __str__(self):
		return '{} > {}'.format(
			str(self.attr) if isinstance(self.attr, Object) else self.attr,
			str(self.other) if isinstance(self.other, Object) else self.encode(self.other),
		)



class IsLessEqualTo(Expr):
	"""Is Less Equal Filter Class"""

	def __init__(self, attr: Object, other) -> None:
		self.attr = attr
		self.other = other
		return

	def __str__(self):
		return '{} <= {}'.format(
			str(self.attr),
			str(self.other) if isinstance(self.other, Object) else self.encode(self.other),
		)
	

class IsLessThan(Expr):
	"""Is Less Than Filter Class"""

	def __init__(self, attr: Object, other) -> None:
		self.attr = attr
		self.other = other
		return

	def __str__(self):
		return '{} < {}'.format(
			str(self.attr),
			str(self.other) if isinstance(self.other, Object) else self.encode(self.other),
		)
