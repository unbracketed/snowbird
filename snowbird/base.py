import os

from django.db import connections
from MySQLdb import OperationalError


class ModelMap:

    def __init__(self, model,  sources=[], **options):
        self.model = model
        self.sources = {}
        
        #TODO inspect relations for model

        self.add_source(model)
        for source in sources:
            self.add_source(source)

        self.extract_dir = E_DIR


    def add_source(self, modelsource):
        "Add a data source to the map"

        #TODO is this a relation of the primary model?
        model = modelsource.model
        self.sources[model] = getattr(modelsource, 'fields', 
                [f.name for f in model._meta.fields]

    def get_field_col_map(self, model, fields=[])
        """
        Returns a dict mapping each selected field of a 
        Django model to its DB column name

            {model_field_name: db_column_name}
        """
        #TODO composite fields will break
        if not fields::
        	_fields = dict([(f.name, f.attname, ) \
        	                      for f in self.model._meta.fields])
        else:
        	_fields = dict([(name, 
        	        model._meta.get_field_by_name(name).attname, ) \
        	        for name in options['fields'])


    def extract(self):
        "Do an extract operation for all sources"
        for source in self.sources:
            extract_for_model(source, self.sources[source])

    def extract_for_model(model, fields=[]):
        """
        Writes the contents of the database table for a
        Django model to a .csv file
        """

        #TODO mysql writes output files with mysql user acl
        
        #TODO get correct cursor for model
        db = 'default'
        cur = connections[db].cursor()
        
        table = model._meta.db_table
        if not fields:
    
            colmap = self.get_field_col_map(model, 
                                        getattr(modelsource, 'fields', []))
        field_names = [f.attname for f in model._meta.fields]
        filename = os.path.join(E_DIR, 'e_%s_%s.csv' % (db, table, ))

        MYSQL_OUTFILE_TEMPLATE = \
        """
        SELECT %s INTO OUTFILE '%s' 
        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        FROM %s
        """ % (','.join(field_names),
            filename,
            table, )
                
        try:
            cur.execute(MYSQL_OUTFILE_TEMPLATE)
        except OperationalError:
            raise
        finally:
            cur.close()
        return (filename, table, field_names, )

    def get_reader(filename):
        "Returns an iterator for a Django model extract"
        return csv.reader(open(filename, 'r'))

    def get_as_dict(modelsource):
    	"Converts a Django Model source to a dict"
        _d = {}
        filename, table, fields = modelsource 
        for row in get_reader(filename):
            if len(row) == len(fields):
                _d.update(row)
            else:
                #TODO
                pass

    def cache(model, key='id'):
    	"""Loads an extract into local cache keyed by `key`"""
        pass        
