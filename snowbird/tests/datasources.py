from django.db import connections
from snowbird.io import DjangoModel
from snowbird.tests.models import TestModel


class TestModelSource(DjangoModel):
    model = TestModel


class TestModelSource2(DjangoModel):
    model = TestModel
    connection = connections['number_two']
