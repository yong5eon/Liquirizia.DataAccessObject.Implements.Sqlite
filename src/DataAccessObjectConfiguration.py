# -*- coding: utf-8 -*-

from Liquirizia.DataAccessObject import DataAccessObjectConfiguration as DataAccessObjectConfigurationBase

__all__ = (
	'DataAccessObjectConfiguration'
)


class DataAccessObjectConfiguration(DataAccessObjectConfigurationBase):
	"""
	Data Access Object Configuration Class for Sqlite
	"""
	def __init__(self, path: str, autocommit: bool = False):
		self.path = path
		self.autocommit = autocommit
		return
