from collections import namedtuple
from brewery.ds import base
from django.db import connections
import django

#from snowbird.io import DjangoModel

Dj_to_Br = namedtuple('Dj_to_Br', 'Field type meta')
FIELD_TYPE_MAP = (
        Dj_to_Br(django.db.CharField, "text", "typeless"),
        )



class DjangoModelSource(base.DataSource):
    """
    Use a Django Model as a DataSource
    """

    def __init__(self, connection, model):
        self.connection = connections[connection]
        self.django_model = model
        self._fields = None
        _fields = model.get_fields()

    def initialize(self):
        pass

    def finalize(self):
        pass

    @property
    def fields(self):
        if self._fields:
            return self._fields

        fields = []
        for column in self.get_fields():
            field = base.Field(name=column.name)
            field.concrete_storage_type = column.type

            for conv in FIELD_TYPE_MAP:
                if issubclass(column.__class__, conv['Field']):
                    field.storage_type = conv['type']
                    field.analytical_type = conv['meta']
                    break

            if not field.storage_type:
                field.storaget_tpye = "unknown"

            if not field.analytical_type:
                field.analytical_type = "unknown"

            fields.append(field)

        self._fields = fields

        return fields

    def read_fields(self):
        return self.fields

    def rows(self):
        return self.django_model.get_data()

    def records(self):
        return self.django_model.objects.all().values()


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
