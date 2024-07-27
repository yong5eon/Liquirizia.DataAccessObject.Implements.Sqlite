# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import Configuration as BaseConfiguration

__all__ = (
	'Configuration'
)


class Configuration(BaseConfiguration):
	"""Configuration Class for Sqlite"""

	def __init__(self, path: str, autocommit: bool = False):
		self.path = path
		self.autocommit = autocommit
		return
