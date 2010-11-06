class Counter(object):
    """
    Provides a counter for map objects
    """


class Relation(object):
    """
    Represents a relation
    """


class BaseMap(object):
    """
    BaseMap
    
    Maps attempt to provide a declarative way to describe a self-contained
    ETL operation.
    
    At its most basic, a Map specifies a data source, and a destination for
    the data.
    
    Maps will be consumed by Jobs. An optimal Map will be as general as possible,
    making it possible for the higher-level code to handle all the heavy lifting
    of doing the data extraction, tranformation, and copy to destination. This
    reduces a lot of repetitive code. Naturally, many situations will require
    special handling - making it more difficult to generalize - so the framework
    aims to make it easy to use some common mapping patterns.
    
    Attributes:
        
        
            
    
    class Articles(BaseMap):
        source = LegacyModel
        destination = DestinationModel
        
        tree_id = Counter()
        
        authors = M2M(to=LegacyAuthors, allow_null=False)
        
    In this case you'll have
    a = Articles()
    a.tree_id
    1
    a.tree_id
    2
    
    
    """
    
    _counters = {}
    model = None
    legacy_model = None
    batch_size = 1000
    _batches = []
    _insert_sql = ""
    _select_sql = ""
    
    
    def __init__(self, *args, **kwargs):
        pass
    
    def process_row(self, row):
        """
        Process a single row at a time.
        
        Data can be returned in a few different formats:
        
        1. self.destination()
        2. As a dict: {'field1': row.field1}
        3. As a tuple (row.field1, row.field2, )
        """
        raise NotImplementedError
    
    def process_queryset(self, qs):
        """
        Process a queryset
        """
        raise NotImplementedError
    
    def handle(self):
        """
        If you need to manage aspects of the migration that can't be
        handled by the runner, you can override `handle`. This allows you to
        handle all aspects of the migration, at the cost of more code to write.
        
        """
        raise NotImplementedError
    
    def 
    
    
    
#class BaseSource(object):
#    """
#    A Source is an abstraction of a set of data. This will most commonly be
#    something like a database table, 
#    
#    """


"""
table filter
row filter
field filter
"""

class Job(object):
    """
    Job dcclreas source 
    """
    def __init__(self):
        
        #check for src, dest models
        self.source



        try:
            self.filters
        except:
            pass
        
        self.batch_size = self.calculate_batch_size()

    
    def calculate_batch_size(self):
        pass


	def batches(self):
	    pass

	def get_batch_related(self):
	    pass

	def process_queryset(self):
	    pass

    def insert_batch(self, data, query=None):
        pass


    def run(self):
        pass


