from django.test import TestCase
from snowbird.datamap import DataJob, DataMap
from snowbird.io import DjangoModel
from snowbird.tests.datamaps import TestModelDataMap
from snowbird.tests.models import TestModel2

from django.test.utils import setup_test_environment
setup_test_environment()


class TestDataMap(TestCase):
    fixtures = ['testmodel']

    def setUp(self):
        self.tm = TestModelDataMap()

    def test_get_extract_jobs(self):
        "make sure get_extract_jobs works"
        dj = DataJob(self.tm.__class__, 0, 10)
        jobs = self.tm.get_extract_jobs()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0], dj)

        TestModelDataMap.batch_size = 3
        tm = TestModelDataMap()
        jobs = tm.get_extract_jobs()
        self.assertEqual(len(jobs), 4)
        self.assertEqual([3,3,3,1], [j.num_rows for j in jobs])
        self.assertEqual([0,3,6,9], [j.offset for j in jobs])

        class DM2(DjangoModel):
            model = TestModel2
        class TM2(DataMap):
            source = DM2
        tm2 = TM2()
        jobs = tm2.get_extract_jobs()
        print jobs 
        self.assertEqual(len(jobs), 0)
