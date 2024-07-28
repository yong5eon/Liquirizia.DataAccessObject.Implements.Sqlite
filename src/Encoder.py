# -*- coding: utf-8 -*-

from datetime import datetime

__all__ = (
	'Encoder'
)


class Encoder(object):
	def __call__(self, v: any) -> any:
		if isinstance(v, int): return v
		if isinstance(v, float): return v
		if isinstance(v, str): return v
		if isinstance(v, bytes): return v
		if isinstance(v, bytearray): return v
		if isinstance(v, tuple): return '\'{}\''.format(str(v))
		if isinstance(v, list): return '\'{}\''.format(str(v))
		if isinstance(v, dict): return '\'{}\''.format(str(v))
		return None
