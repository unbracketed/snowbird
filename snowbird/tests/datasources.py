from django.db import connections
from snowbird.datastores.djangomodel import DjangoModelSource
from snowbird.tests.models import TestModel


class TestModelSource(DjangoModelSource):
    model = TestModel


class TestModelSource2(DjangoModelSource):
    model = TestModel
    connection = connections['number_two']
