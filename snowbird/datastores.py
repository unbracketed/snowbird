from brewery.ds import base


class DjangoModelSource(base.DataSource):
	"""
	Use a Django Model as a DataSource
	"""

    def __init__(self, connection, model):
        self.connection = connections[connection]
        self.model = model
        self._fields = None

    def initialize(self):
    	pass

    def finalize(self):
    	pass

    @property
    def fields(self):
    	#calculate fields and convert to brewery

    def read_fields(self):
        #FIXME
    	self._fields = self.get_fields()

    def rows(self):
        #FIXME
    	return self.model.objects.all()

    def records(self):
    	return self.model.objects.all().values()


class DjangoModelTarget(base.DataTarget):
	"""
	Use a Django Model as a DataTarget
	"""

    def __init__(self, connection, model):
    	self.connection = connections[connection]
    	self.model = model
    	self._fields = None
    	self.buffer_size = 1000

    @property
    def fields(self):
    	 pass

    def initialize(self):
        self._buffer = []

    def finalize(self):
    	pass

    def append(self, obj):
        if type(obj) == dict:
            record = obj
        else:
            record = dict(zip(self.field_names, obj))

        self._buffer.append(record)
        if len(self._buffer) >= self.buffer_size:
            self._flush()

    def _flush(self):
        if len(self._buffer) > 0:
            #FIXME
            self.datastore.connection.execute(self.insert_command, self._buffer)
            self._buffer = []
