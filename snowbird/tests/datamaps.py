from snowbird.datamap import DataMap
from snowbird.tests.datasources import TestModelSource


class TestModelDataMap(DataMap):
    source = TestModelSource
