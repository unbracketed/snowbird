import logging
from django.db import connections

LOG = logging.getLogger()


class NoSourceFieldsDefinedError(Exception):
    """Raised when a source cannot determine any fields to query"""

class InvalidSourceFieldError(Exception):
    """Raised when a field is declared on the Source that cannot
    be resolved via the reader"""


class DjangoModel(object):
    """
    A Django Model interface to a dataset.
    """
    def __init__(self, **options):

        self._fields = []

        if hasattr(self, 'fields'):
            for field in self.fields:
                if not field in self.get_default_fields():
                    raise InvalidSourceFieldError
            self._fields = self.fields
        else:
            self._fields = self.get_default_fields()

        if hasattr(self, 'exclude'):
            self._fields = [f for f in self._fields if f in self.exclude]

        if not self._fields:
            raise NoSourceFieldsDefinedError

    @property
    def values_placeholder(self):
        """Generates a string of a list of string placeholders. For example:

            '%s,%s,%s'

        This is used to build the column specification part of the INSERT
        query. The generated string will contain one placeholder for each
        field in use by this I/O object.
        """
        numph = len(self._fields)
        return ','.join(['%s']*numph)

    @property
    def insert_stmt(self):
        """
        Generate an INSERT statement using the columns specified for this
        instance.
        """
        return "INSERT INTO %s (%s) VALUES (%s)" % (self.model._meta.db_table,
                                                    ','.join(self._fields),
                                                    self.values_placeholder, )

    def get_default_fields(self):
        """
        Returns all fields for a model.
        """
        if not hasattr(self, '_default_fields'):
            setattr(self, '_default_fields',
                [f.name for f in self.model._meta.fields])
        return self._default_fields

    def do_insert(self, values, query=None):
        """
        Performs an INSERT query using the list of values.
        """

        if not values:
            LOG.warning("insert called with no values")
            return

        _q = query if query else self.insert_stmt

        #get application DB cursor
        cursor = connections['default'].cursor()
        #turn off FK checks (MySQL)
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")

        result = cursor.executemany(_q, values)
        cursor.connection.commit()
        cursor.close()
        return result

    def insert_dict_list(self, data, model=None, table=None):
        """
        Insert a list of dicts into this model.

        Optional args:
            model -
        """
        #TODO validate columns against fields
        if not cols:
            cols = values[0].keys()

        sql = "INSERT INTO %s (%s) VALUES (%s)" \
                % (self.model._meta.db_table,
                   ','.join(cols),
                   ','.join(['%s']*len(cols)))

        inserts = [[row[c] for c in cols] for row in values]
        return self.do_insert(inserts, sql)
