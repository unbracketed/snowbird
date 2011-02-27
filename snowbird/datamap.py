"""
DataMap
"""
from collections import namedtuple


class MissingSourceError(Exception):
    """Raised when a DataMap is missing the source attribute"""


DataJob = namedtuple('DataJob', 'source offset num_rows')

#use 1000 rows as a totally arbitrary, mostly
#sensible default
DEFAULT_BATCH_SIZE = 1000


class DataMap(object):
    """
    DataMap is a pairing of an input source and an output destination

    You must specify the following attributes:
    source

    Optional:
    destination
    """
    def __init__(self):
        if not getattr(self, 'source', False):
            raise MissingSourceError
        else:
            self.IOIN = self.source()

    def get_extract_jobs(self):
        """Returns a list of DataJobs that will use this DataMap"""
        metrics = self.IOIN.get_metrics()
        num_jobs = (metrics['rows'] / DEFAULT_BATCH_SIZE) \
                    + (1 if metrics['rows'] % DEFAULT_BATCH_SIZE else 0)
        return [DataJob(self.__class__, offset*DEFAULT_BATCH_SIZE, 1000) \
                for offset in range(num_jobs)]
