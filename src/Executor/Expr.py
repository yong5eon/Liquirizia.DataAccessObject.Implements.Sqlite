# -*- coding: utf-8 -*-

from abc import ABC, ABCMeta, abstractmethod

__all__ = (
	'Expr'
)


class Expr(ABC, metaclass=ABCMeta):
	"""Filter Interface"""

	def encode(self, o):
		if isinstance(o, str): return '\'{}\''.format(o)
		return o

	@abstractmethod
	def __str__(self):
		raise NotImplementedError('{} must be implemented __str__'.format(self.__class__.__name__))