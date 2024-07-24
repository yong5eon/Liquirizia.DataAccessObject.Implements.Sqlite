# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

__all__ = (
	'Property'
)


class Property(ABC):
	@abstractmethod
	def __str__(self):
		pass
