"""
Snowbird Tests
"""
import unittest
from snowbird.io import (DjangoModel, ModelMissingError, InvalidModelError, 
        InvalidSourceFieldError)
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

    def test_djangomodel_fields(self):
        """test that fields can be specified"""
        class IOTest(DjangoModel):
            model = TestModel
            fields = ('field_1', 'field_3', 'field_5')
        dm = IOTest()
        self.assertEqual(('field_1', 'field_3', 'field_5'), dm._fields)

    def test_djangomodel_bogus_field(self):
        """test that a bogus field raises exception"""
        class IOTest(DjangoModel):
            model = TestModel
            fields = ('giggity', )
        self.assertRaises(InvalidSourceFieldError, IOTest)

    def test_exclude(self):
        """test that fields can be excluded"""
        class IOTest(DjangoModel):
            model = TestModel
            exclude = ('field_3', 'field_4', 'field_5')
        dm = IOTest()
        self.assertEqual(['id', 'field_1', 'field_2'], dm._fields)

    def test_bogus_exclude(self):
        """test that specifying a bogus exclude field generates 
        an exception"""
        class IOTest(DjangoModel):
            model = TestModel
            exclude = ('griffin', )
        self.assertRaises(InvalidSourceFieldError, IOTest)

    def test_fields_and_exclude(self):
        """test that fields and exclude work together properly"""
        class IOTest(DjangoModel):
            model = TestModel
            fields = ('id', 'field_1', 'field_2', 'field_3')
            exclude = ('id', )
        dm = IOTest()
        self.assertEqual(['field_1', 'field_2', 'field_3'], dm._fields)
