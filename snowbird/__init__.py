import logging

class NullHandler(logging.Handler):
    def emit(self, record):
    	pass

logging.getLogger('snowbird').addHandler(NullHandler())
