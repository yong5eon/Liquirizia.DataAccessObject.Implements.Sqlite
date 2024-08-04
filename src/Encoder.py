# -*- coding: utf-8 -*-

from datetime import datetime
import json

__all__ = (
	'Encoder'
)


class Encoder(object):
	def __call__(self, v):
		if isinstance(v, str): return "'{}'".format(v)
		return v
