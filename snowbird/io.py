from django.db import connections, models

from snowbird.db import DBMixin

import logging
LOG = logging.getLogger()


class NoSourceFieldsDefinedError(Exception):
    """Raised when a source cannot determine any fields to query"""
    def __init__(self, klass):
        self.msg = "No fields/columns to query for " %(klass.__name__)
    def __str__(self):
        return self.msg


class InvalidSourceFieldError(Exception):
    """Raised when a field is declared on the Source that cannot
    be resolved"""
    def __init__(self, field, klass):
        self.msg = "Field %s not found on %s" %(field, klass.__name__)
    def __str__(self):
        return self.msg


class ModelMissingError(Exception):
    """Raised when the Django model class isn't specified"""
    def __init__(self, klass):
        self.msg = "%s is missing required model attribute" %klass.__class__.__name__
    def __str__(self):
        return self.msg


class InvalidModelError(Exception):
    """Raised when model is not a Django Model"""
    def __init__(self, klass):
        self.msg = "%s is not a Django Model" %klass.__name__
    def __str__(self):
        return self.msg


class DjangoModel(DBMixin):
    """
    A Django Model interface to a dataset.
    """
    def __init__(self, **options):

        if not getattr(self, 'model', False):
            raise ModelMissingError(self)
        elif not issubclass(self.model, models.Model):
            raise InvalidModelError(self.model)
        
        self._fields = []

        if hasattr(self, 'fields'):
            for field in self.fields:
                if not field in self.get_default_fields():
                    raise InvalidSourceFieldError(field, self.model)
            self._fields = self.fields
        else:
            self._fields = self.get_default_fields()

        if hasattr(self, 'exclude'):
            self._fields = [f for f in self._fields if not f in self.exclude]

        if not self._fields:
            raise NoSourceFieldsDefinedError(self.model)

        self.table = self.model._meta.db_table

    def get_default_fields(self):
        """
        Returns all fields for a model.
        """
        if not hasattr(self, '_default_fields'):
            setattr(self, '_default_fields',
                [f.name for f in self.model._meta.fields])
        return self._default_fields

    def get_connection(self):
        """
        Returns the DB connection to use
        """
        return connections['default']
