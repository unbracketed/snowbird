import os

from django.db import connections
from MySQLdb import OperationalError

#from itertools import count
#
#
#
#
#class BaseMap(object):
#    """
#    BaseMap
#    
#    Maps attempt to provide a declarative way to describe a self-contained
#    ETL operation.
#    
#    At its most basic, a Map specifies a data source, and a destination for
#    the data.
#    
#    Maps will be consumed by Jobs. An optimal Map will be as general as possible,
#    making it possible for the higher-level code to handle all the heavy lifting
#    of doing the data extraction, tranformation, and copy to destination. This
#    reduces a lot of repetitive code. Naturally, many situations will require
#    special handling - making it more difficult to generalize - so the framework
#    aims to make it easy to use some common mapping patterns.
#    
#    Attributes:
#        
#        
#            
#    
#    class Articles(BaseMap):
#        source = LegacyModel
#        destination = DestinationModel
#        
#        tree_id = Counter()
#        
#        authors = M2M(to=LegacyAuthors, allow_null=False)
#        
#    In this case you'll have
#    a = Articles()
#    a.tree_id
#    1
#    a.tree_id
#    2
#    
#    
#    """
#    
#    _counters = {}
#    model = None
#    legacy_model = None
#    batch_size = 1000
#    _batches = []
#    _insert_sql = ""
#    _select_sql = ""
#    
#    
#    def __init__(self, *args, **kwargs):
#        pass
#    
#    def process_row(self, row):
#        """
#        Process a single row at a time.
#        
#        Data can be returned in a few different formats:
#        
#        1. self.destination()
#        2. As a dict: {'field1': row.field1}
#        3. As a tuple (row.field1, row.field2, )
#        """
#        raise NotImplementedError
#    
#    def process_queryset(self, qs):
#        """
#        Process a queryset
#        """
#        raise NotImplementedError
#    
#    def handle(self):
#        """
#        If you need to manage aspects of the migration that can't be
#        handled by the runner, you can override `handle`. This allows you to
#        handle all aspects of the migration, at the cost of more code to write.
#        
#        """
#        raise NotImplementedError
#    
#    def 
#    
#    
#    
##class BaseSource(object):
##    """
##    A Source is an abstraction of a set of data. This will most commonly be
##    something like a database table, 
##    
##    """
#
#
#"""
#table filter
#row filter
#field filter
#"""
#
#class MissingDataSourceException(Exception):
#	"Thrown when a Job cannot find valid Reader and Writer channels"
#
#
#class DataMap(object):
#
#    def __init__(self):
#        
#        #check for src, dest models
#        self.get_data_source()
#        
#        #any related fields?
#
#        self.inspect_source()
#
#        #batch size
#        try:
#            self.filters
#        except:
#            pass
#        
#        self.batch_size = self.calculate_batch_size()
#
#    
#	def get_data_source(self):
#		if not hasattr(self, source):
#			raise MissingDataSourceException
#

E_DIR = '/tmp'

def extract_for_model(model, db='default', fields=[]):
    """
    Writes the contents of the database table for a
    Django model to a .csv file
    """

    #TODO mysql writes output files with mysql user acl
    cur = connections[db].cursor()
    
    table = model._meta.db_table
    if not fields:
    	fields = model._meta.fields

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


