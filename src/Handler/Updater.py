# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from ..Model import Table
from ..Type import Object
from ..Constraint import PrimaryKey

__all__ = (
	'Updater'
)


class Updater(Handler):
	def __call__(self, table, obj, attr, value, prev):
		pks = {}
		for constraint in obj.__properties__['constraints'] if obj.__properties__['constraints'] else []:
			if not isinstance(constraint, PrimaryKey): continue
			pkcs = constraint.cols
			for k, v in obj.__class__.__dict__.items():
				if isinstance(v, Object) and v.key in pkcs:
					pks[v.key] = obj.__object__.__getitem__(k)
		obj.__cursor__.execute('UPDATE {} SET {}=? WHERE {}'.format(
			table.__properties__['name'],
			attr.key,
			' AND '.join(['{} = ?'.format(pk) for pk in pks.keys()])
		), 
		value,
		*[v for k, v in pks.items()]
		)
		return
