# -*- coding: utf-8 -*-

from Liquirizia.DataModel import Handler

from ..Model import Table
from ..Type import Type

__all__ = (
	'Update'
)


class Update(Handler):
	def __call__(self, table: Table, attr: Type, value: any, prev: any):
		pks = {}
		if table.__properties__['primaryKey']:
			pkcs = table.__properties__['primaryKey'].columns
			for k, v in table.__class__.__dict__.items():
				if isinstance(v, Type) and v.key in pkcs:
					pks[v.key] = table.__object__.__getitem__(k)
		else:
			for k, v in table.__class__.__dict__.items():
				if isinstance(v, Type):
					if v.primaryKey:
						pks[v.key] = table.__object__.__getitem__(v.name)
		print('{}.{} is changed {} to {}'.format(table.__properties__['name'], attr.key, prev, value))
		table.__connection__.execute('UPDATE {} SET {}=? WHERE {}'.format(
			table.__properties__['name'],
			attr.key,
			' AND '.join(['{} = ?'.format(pk) for pk in pks.keys()])
		), 
		value,
		*[v for k, v in pks.items()]
		)
		return
