# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

__all__ = (
	'Expr'
)


class Expr(metaclass=ABCMeta):
	"""Filter Interface"""

	@abstractmethod
	def __str__(self):
		raise NotImplementedError('{} must be implemented __str__'.format(self.__class__.__name__))