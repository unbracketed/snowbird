class BaseMap(object):
    """
    BaseMap
    
    Maps attempt to provide a declarative way to describe a self-contained
    ETL operation.
    
    At its most basic, a Map specifies a data source, and a destination for
    the data.
    
    Maps will be consumed by Jobs. An optimal Map will be as general as possible,
    making it possible for the higher-level code to handle all the heavy lifting
    of doing the data extraction, tranformation, and copy to destination. This
    reduces a lot of repetitive code. Naturally, many situations will require
    special handling - making it more difficult to generalize - so the framework
    aims to make it easy to use some common mapping patterns.
    
    
    """
    
class BaseSource(object):
    """
    A Source is an abstraction of a set of data. This will most commonly be
    something like a database table, 
    """

