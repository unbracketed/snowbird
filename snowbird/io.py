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


    def get_default_fields(self):
        """
        Returns all fields for a model.
        """
        if not hasattr(self, '_default_fields'):
            setattr(self, '_default_fields',
                [f.name for f in self.model._meta.fields])
        return self._default_fields

