from brewery.nodes import base


class DjangoModelSourceNode(base.SourceNode):
    """Source node that reads data from a Django Model
    """
    __node_info__ = {
        "label" : "Django Model Source",
        "description" : "Read data from a Django Model",
        "attributes" : [
            {
                 "name": "connection",
                 "description": "a connection in the DATABASES setting",
                 "default": "default"
            },
            {
                 "name": "model",
                 "description": "A Django Model class" 
            }
        ]
    }
    def __init__(self, *args, **kwargs):
        super(DjangoModelSourceNode, self).__init__()
        self.kwargs = kwargs
        self.args = args
        self.stream = None
        self.fields = None

#TODO determine how many output streams based on related


    @property
    def output_fields(self):
        if not self.stream:
            raise ValueError("Stream is not initialized")

        if not self.stream.fields:
            raise ValueError("Fields are not initialized")

        return self.stream.fields

    def initialize(self):
        self.stream = DjangoModelDataSource(*self.args, **self.kwargs)

        self.stream.fields = self.fields
        self.stream.initialize()

    def run(self):
        for row in self.stream.rows():
            self.put(row)

    def finalize(self):
        self.stream.finalize()


class DjangoModelTargetNode(base.TargetNode):
	pass
