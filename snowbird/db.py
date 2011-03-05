import logging
from time import time


LOG = logging.getLogger()


class DBMixin(object):

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

    #def execute_queries(self, queries):
        #for query in queries:
            #self.execute_query(query)

    def execute_query(self, query):

        cursor = self.get_connection().cursor()
        cursor.execute(query)
        cursor.connection.commit()
        results = cursor.fetchall()
        cursor.close()
        return results

    def insert_values_list(self, query, values):
        """
        Performs an INSERT query using the list of values.
        """
        if not values:
            LOG.warning("insert called with no values")
            return

        #TODO get DB from connection
        cursor = self.get_connection().cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        t0 = time()
        result = cursor.executemany(query, values)
        cursor.connection.commit()
        cursor.close()
        LOG.info("[OUT]\t%s\t%s" %(self.__class__.__name__, time() - t0))
        return result

    def insert_dict_list(self, data):
        """
        Insert a list of dicts into this model.
        """
        sql = "INSERT INTO %s (%s) VALUES (%s)" \
                % (self.table,
                    ','.join(self.columns),
                    ','.join(['%s']*len(self.columns)))

        inserts = [[row[col] for col in self.columns] for row in data]
        return self.insert_values_list(sql, inserts)

    def get_metrics(self):
        """Returns row count, avg row size"""
        sql = "SELECT COUNT(*) FROM %s" % self.table

        res = self.execute_query(sql)
        return {'rows': res[0][0]}
