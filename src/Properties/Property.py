# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

__all__ = (
	'Property'
)


class Property(metaclass=ABCMeta):
	@abstractmethod
	def __str__(self):
		pass
