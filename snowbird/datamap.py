"""
DataMap
"""
from collections import namedtuple
from django.db import connections
import logging

LOG = logging.getLogger('snowbird')


class MissingSourceError(Exception):
    """Raised when a DataMap is missing the source attribute"""
    def __init__(self, inst):
        self.msg = "%s is missing required source attribute" %inst.__class__.__name__
    def __str__(self):
        return self.msg

class InvalidOutField(Exception):
    """Raised when a row of mapped data contains a field that doesn't
    exist in the output destination"""


DataJob = namedtuple('DataJob', 'source offset num_rows')


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


    def get_field_sets(self):
        "Returns a tuple containing input, output, and matched fields"
        #match up src/dst fields
        if self.OUT:
            out_fields = frozenset(self.OUT.get_fields())
            matches = out_fields.intersection(self.IN.get_fields())
        else:
            out_fields = self.IN.get_fields()
            matches = self.IN.get_fields()
        return (self.IN.get_fields(), out_fields, matches)

    def get_jobs(self):
        return self.get_extract_jobs()

    def get_extract_jobs(self):
        """Returns a list of DataJobs that will use this DataMap"""
        metrics = self.IN.get_metrics()
        if not metrics['rows']:
            LOG.warning("No rows for source %s.%s on connection %s" %(self.__class__.__name__,
                self.IN.__class__.__name__, self.IN.get_connection().alias))
            return []
        num_jobs = (metrics['rows'] / metrics['batch_size'])
        return [DataJob(self.__class__,
                        offset*metrics['batch_size'],
                        metrics['batch_size']) \
                for offset in range(num_jobs)] + \
                [DataJob(self.__class__,
                        num_jobs*metrics['batch_size'],
                        metrics['rows'] % metrics['batch_size']  or metrics['batch_size'])]

    def get_connection(self):
        if not hasattr(self, 'connection'):
        	return connections['default']
        else:
        	return self.connection

    #def run_job(self):
        #"""
        #Performs the action of mapping the source input data to the
        #output destination.
        #"""
        #in_fields, out_fields, matches = self.get_field_sets()
        #for row in self.IN:
            #rowdict = dict([(f, None if not f in matches else row[f]) for f in out_fields])
            #mapped = self.process_row(row, rowdict)

            ##output fields should match OUT fields
            #if not frozenset(mapped.keys()) == frozenset(matches):
                #raise InvalidOutField

            #if self.OUT:
                #self.OUT.append(mapped)
            #else:
                #LOG.info(str(mapped))

        ##notify OUT that no more data is coming
        #if self.OUT:
            #self.OUT.flush()

    def process_row(self, row, mapped):
        """
        Returns a dict with fields matching what is expected
        by the output destination

        The input is a dict with keys for each of the output
        fields
        """
        return mapped


#class DjangoSourceMap(DataMap):
    #"""
    #A DataMap for use with DataMaps that specify a DjangoModel as the source
    #"""

    #def run_job(self):
        #pass
