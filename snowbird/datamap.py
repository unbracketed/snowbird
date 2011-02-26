class MissingSourceError(Exception):
    """Raised when a DataMap is missing the source attribute"""


class DataMap(object):
    """
    DataMap is a pairing of an input source and an output destination

    You must specify the following attributes:
    source

    Optional:
    destination
    """
    
    def __init__(self):
        if getattr(self, 'source', False):
            raise MissingSourceError

    def get_extract_jobs(self):
        #query the source for batches

        metrics = self.source.get_metrics()

        qs = self.source.get_queryset()

    def run_job(self):
        #execute a job
        if hasattr(self, 'process_row'):
        	pass

