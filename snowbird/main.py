from brewery.stream import Stream



#load the config file

#calculate jobs for the run

#create a new global run ID

#convert jobs into celery tasks

#every finished task records its results

#tasks should be atomic
#resume can figure out last good task in a run
#delta can reuse



#get the datamaps
for job in jobs:
    stream = Stream()
    for datamap in job.datamaps:
        if issubclass(datamap.source, DjangoModel):
            stream.django_model_source(datamap.source)
            #if related, attach related mapped IDs
        if issubclass(datamap.destination, DjangoModel):
        	stream.django_model_target(datamap.destination)
        stream.run()
