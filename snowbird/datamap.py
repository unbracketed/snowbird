"""
DataMap
"""
from collections import namedtuple
import logging

LOG = logging.getLogger()


class MissingSourceError(Exception):
    """Raised when a DataMap is missing the source attribute"""
    def __init__(self, inst):
        self.msg = "%s is missing required source attribute" %inst.__class__.__name__
    def __str__(self):
        return self.msg


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
    def __init__(self, **options):
        if not getattr(self, 'source', False):
            raise MissingSourceError
        else:
            kwargs = options.get('source', {})
            self.IN = self.source(**kwargs)

        if not getattr(self, 'destination', False):
            self.OUT = None
        else:
            kwargs = options.get('destination', {})
            self.OUT = self.destination(**kwargs)

    def get_extract_jobs(self):
        """Returns a list of DataJobs that will use this DataMap"""
        metrics = self.IN.get_metrics()
        num_jobs = (metrics['rows'] / DEFAULT_BATCH_SIZE) \
                    + (1 if metrics['rows'] % DEFAULT_BATCH_SIZE else 0)
        return [DataJob(self.__class__, offset*DEFAULT_BATCH_SIZE, 1000) \
                for offset in range(num_jobs)]
    
    def run_job(self):
        #match up src/dst fields
        if self.OUT:
            #TODO
            pass

        for row in self.IN:
            mapped = self.process_row(row)
            if self.OUT:
            	pass
            else:
            	LOG.info(str(row))

    def process_row(self, row):
        return row


class DjangoSourceMap(DataMap):
    """
    A DataMap for use with DataMaps that specify a DjangoModel as the source
    """
    
    def run_job(self):
        pass
