import logging


LOG = logging.getLogger()


ENGINE_MODULES = {
    'django.db.backends.postgresql_psycopg2': 'postgresql_psycopg2',
    'django.db.backends.sqlite3': 'sqlite3',
    'django.db.backends.mysql': 'mysql'}


class DatabaseAdapter(object):
    """
    Abstracts read and write operations for the RDBMS supported by Django
    """
    
    def __get__(self, obj, objtype):
        try:
        	ENGINE_MODULES[obj.get_connection().settings_dict['ENGINE']]
        except KeyError:
            #TODO
        	raise "DB not supported"
