from psycopg2.pool import SimpleConnectionPool
import contextlib
import json
import logging

from experiment.storage import json_ser

_log = logging.getLogger('experiment.storage.postgres')

class PostgresStorage(object):

	def __init__(self, connection_string):
		self.pool = SimpleConnectionPool(minconn=0, maxconn=3, dsn=connection_string)

	def store(self, key, dict_value):
		with pooled_cursor(self.pool) as cursor:
				value = json.dumps(dict_value)
				_log.info('About to insert %s', value)
				cursor.execute('INSERT INTO experiment(key, value) VALUES (%s, %s)', (key, value))
				_log.info('Done')

	def update(self, key, dict_value):
		with pooled_cursor(self.pool) as cursor:
			data = json.dumps(dict_value)
			_log.info('About to update %s to %s', key, data)
			cursor.execute('UPDATE experiment SET value = %s WHERE key = %s', (value, key))
			_log.info('Done')

	def get(self, name):
		with pooled_cursor(self.pool) as cursor:
			cursor.execute('SELECT value FROM experiment WHERE key = %s', (key,))
			data = cursor.fetchone()
			if data is None:
				return data
			data = data[0]
			_log.info('Reading experiment got: %s', data)
			return json.loads(data)

	def delete(self, key):
		pass

	@classmethod
	def create(cls):
		return cls(connection_string="'host='localhost' dbname='experiment' user='postgres'")

@contextlib.contextmanager
def pooled_cursor(pool):
	con = pool.getconn()
	try:
		with con.cursor() as cursor:
			yield cursor
	except:
		con.rollback()
		pool.putconn(con, close=True)
		raise
	else:
		con.commit()
		pool.putconn(con)
