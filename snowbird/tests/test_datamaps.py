from django.test import TestCase
from snowbird.datamap import DataJob
from snowbird.tests.datamaps import TestModelDataMap

from django.test.utils import setup_test_environment
setup_test_environment()


class TestDataMap(TestCase):
    fixtures = ['testmodel.json']

    def setUp(self):
        self.tm = TestModelDataMap()

    def test_create_datamap(self):
        pass

    def test_get_extract_jobs(self):
        print self.tm.get_extract_jobs()
        dj = DataJob(self.tm.__class__, 0, 10)
        #[DataJob(source=<class 'snowbird.tests.datamaps.TestModelDataMap'>, offset=0, num_rows=1000)]
        jobs = self.tm.get_extract_jobs()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0], dj)

        TestModelDataMap.batch_size = 3
        tm = TestModelDataMap()
        jobs = tm.get_extract_jobs()
        print jobs
        self.assertEqual(len(jobs), 4)
        self.assertEqual([3,3,3,1], [j.num_rows for j in jobs])
        self.assertEqual([0,3,6,9], [j.offset for j in jobs])
