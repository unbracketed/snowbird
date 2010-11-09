from itertools import count




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

class MissingDataSourceException(Exception):
	"Thrown when a Job cannot find valid Reader and Writer channels"


class Job(object):
    """
    Job dcclreas source 
    """
    def __init__(self):
        
        #check for src, dest models
        self.get_data_source()
        
        #any related fields?

        self.inspect_source()

        #batch size
        try:
            self.filters
        except:
            pass
        
        self.batch_size = self.calculate_batch_size()

    
	def get_data_source(self):
		if not hasattr(self, source):
			raise MissingDataSourceException


    def inspect_source(self):
        pass


class NoSourceFieldsDefinedError(Exception):
	"""Raised when a source cannot determine any fields to query"""

class InvalidSourceFieldError(Exception):
	"""Raised when a field is declared on the Source that cannot 
	be resolved via the reader"""

class Source:


	def __init__(self, **options):

        self._counters = {}
        self._fields = []

        #look for fields
        if hasattr(self, 'fields'):
            self._fields = self.fields
            _default_fields = self.get_default_fields()
            if filter(lambda x: x not in _default_fields, self._fields):
                raise InvalidSourceFieldError
        else:
        	self._fields = self.get_default_fields()


        #look for exclude
        if hasattr(self, 'exclude'):
        	self._fields = [f for f in self._fields if f in self.exclude]
        
        if not self._fields:
        	raise NoSourceFieldsDefinedError

        #initialize counters
        if 'counters' in options:
            for counter in options['counters']:
            	self._counters[counter] = count() 

        self._default_reader = self.get_reader() 
        
        if not hasattr(self, 'slice_size'):
        	self.slice_size = self._get_default_slice_size()

    def __iter__(self):
		for slice in self.slices():
			slice = self.filter_slice(slice)
			for row in slice:
				yield self.filter(row)

	def get_reader(self):
		raise NotImplementedError

    def get_fields(self):
    	raise NotImplementedError


	def get_batch_related(self):
	    pass

	def process_queryset(self):
	    pass

    def insert_slice(self, data, query=None):
        pass

    def pull_source(self):
    	self._src = self.source.objects.all()

	def filter_source(self):
		for slice in self.slices():
			self.process_slice(slice)

    def filter_slice(self, slice):
		for obj in slice:
			self.filter_object(obj)

	def filter_object(self):
		field_map = self.get_field_map()
	    

	def get_field_map(self):
		pass

    def run(self):
       self.pull_source()
	   self.filter_source()


class DjangoModel(Source):

	def __init__(self, model):
		self.model = model

    def _get_reader_for_model():
        self.

    def get_reader(self):
    	return self._get_reader_for_model()

    def get_default_fields(self):
    	return self.model._meta.fields


    def slices(offset=0, size=1000):
        total = self.model.objects.count()
        for start in range(offset, total, size):
            end = min(start + size, total)
            yield (start, end, total, self.model.objects.iterator()[start:end])

