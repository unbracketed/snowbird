from snowbird.io import DjangoModel
from snowbird.tests.models import TestModel


class TestModelSource(DjangoModel):
    model = TestModel
