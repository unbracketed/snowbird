from django.db import connections


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
    def columns(self):
        return [f.attname for f in self.model._meta.fields if not f.attname == 'id']

    @property
    def values_placeholder(self):
        numph = len([f for f in self.model._meta.fields if not f.name == 'id'])
        return ','.join(['%s']*numph)
    
    @property
    def insert_stmt(self):
        return "INSERT INTO %s (%s) VALUES (%s)" % (self.model._meta.db_table,
                                                    ','.join(self.columns),
                                                    self.values_placeholder, )

    def do_insert(self, values, query=None):
        
        if not values:
            return
        
        _q = query if query else self.insert_stmt
        logging.debug(msg=_q)
        logging.debug(str(values))

        #get application DB cursor
        cursor = connections['default'].cursor()
        #turn off FK checks (MySQL)
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        
        result = cursor.executemany(_q, values)
        cursor.connection.commit()
        cursor.close()
        return result

    def do_insert_cols(self, values, cols=None):
        """
        a convenience method that accepts a list of dicts to 
        use as insert values

        cols can be used to specify a list of columns. each dict
        in values is assumed to have a key for each item in col
        if col is not specified the cols are generated from the 
        keys of the first dict in values
        """
        if not cols:
            cols = values[0].keys()

        sql = "INSERT INTO %s (%s) VALUES (%s)" \
                % (self.model._meta.db_table,
                   ','.join(cols),
                   ','.join(['%s']*len(cols)))

        inserts = [[row[c] for c in cols] for row in values]
        return self.do_insert(inserts, sql)


    
#class LegacyArticle(DjangoModel):
    #model = Articles
    #fields = (
        #('id', 'legacy_id', ), 
    #)

    ##allows for override of the already selected fields (determined by fields/exclude)
    #field_map = {
            #'id': 'legacy_id'
    #}


#class ArticleMap(DataMap):
    #source = DjangoModel()
    #destination = DjangoModel()

    #related
    #reverse_related

    #counters

    #rejected_rows


