from django.db import connections, models

from snowbird.db import DBMixin

import logging
LOG = logging.getLogger()


class ModelMissingError(Exception):
    """Raised when the Django model class isn't specified"""
    def __init__(self, inst):
        self.msg = "%s is missing required model attribute" %inst.__class__.__name__
    def __str__(self):
        return self.msg


class InvalidModelError(Exception):
    """Raised when model is not a Django Model"""
    def __init__(self, klass):
        self.msg = "%s is not a Django Model" %klass.__name__
    def __str__(self):
        return self.msg


class NoSourceFieldsDefinedError(Exception):
    """Raised when a source cannot determine any fields to query"""
    def __init__(self, klass):
        self.msg = "No fields/columns to query for " %(klass.__name__)
    def __str__(self):
        return self.msg


class InvalidSourceFieldError(Exception):
    """Raised when a field is declared on the Source that cannot
    be resolved"""
    def __init__(self, fields, klass):
        self.msg = "Fields %s not found on %s" %(repr(fields), klass.__name__)
    def __str__(self):
        return self.msg


class DjangoModel(DBMixin):
    """
    A Django Model interface to a dataset.
    """
    connection = connections['default']

    def __init__(self, **options):
        if not getattr(self, 'model', False):
            raise ModelMissingError(self)
        elif not issubclass(self.model, models.Model):
            raise InvalidModelError(self.model)
        
        self._fields = []

        if hasattr(self, 'fields'):
            if not set(self.fields).issubset(set(self.get_default_fields())):
                raise InvalidSourceFieldError(
                        set(self.fields)-set(self.get_default_fields()),
                        self.model)
            self._fields = self.fields
        else:
            self._fields = self.get_default_fields()

        if hasattr(self, 'exclude'):
            if not set(self.exclude).issubset(set(self._fields)):
                raise InvalidSourceFieldError(
                        set(self.exclude)-set(self._fields),
                        self.model)
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
        return self.connection

    def get_queryset(self):
        """
        Returns a QuerySet that will evaluate to all
        rows in the table, with columns corresponding to
        the specified fields
        """
        return self.model.objects.all()

    def get_data(self):
        """
        Executes the calculated query and returns a list
        of dicts
        """
        return self.get_queryset()
