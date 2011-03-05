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
            db_module = ENGINE_MODULES[obj.get_connection().settings_dict['ENGINE']]
        except KeyError:
            #TODO better msg
            raise "DB not supported"
        #from nose.tools import set_trace; set_trace()

        module = __import__('snowbird.db.%s' %db_module, {}, {}, [''])
        return module.DatabaseOperations(
                table=obj.model._meta.db_table,
                columns=obj.get_fields(),
                connection=obj.get_connection())
