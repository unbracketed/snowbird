from snowbird.datamap import DataMap
from snowbird.tests.datasources import TestModelSource, TestModelSource2


class TestModelDataMap(DataMap):
    source = TestModelSource
    destination = TestModelSource2

#class TestModelDataMap(DataMap):
    #source = TestModelSource2
