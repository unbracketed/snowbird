"""
Snowbird Tests
"""
import unittest
from snowbird.io import (DjangoModel, ModelMissingError, InvalidModelError)
from snowbird.tests.models import TestModel


class TestDjangoModel(unittest.TestCase):
    """
    Tests for DjangoModel 
    """
    def test_djangomodel_missing_model(self): 
        """test that declaring a DjangoModel without specifying a model
        attribute fails"""
        class IOTest(DjangoModel):
            pass
        self.assertRaises(ModelMissingError, IOTest)

    def test_djangomodel_invalid_model(self):
        """test that passing something that is not a Django Model to the model
        attribute fails"""
        class IOTest(DjangoModel):
            model = dict
        self.assertRaises(InvalidModelError, IOTest)

    def test_djangomodel(self):
        """test that a minimal DjangoModel can be declared and instantiated"""
        class IOTest(DjangoModel):
            model = TestModel
        dm = IOTest()
        self.assertTrue(isinstance(dm, DjangoModel))
        self.assertTrue(issubclass(dm.model, TestModel))
