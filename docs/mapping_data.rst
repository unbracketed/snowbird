Mapping Data Developer Guide
=============================

A Map ties together a source and destination for data. As a general rule of thumb,
the more minimal your Map is, the more likely it is that the runner will be able
to process them at optimal speeds. Of course, it is often the case that the data will
require special handling at the transform step and consequently more or all of the
processing logic will have to be explicitly included by the developer in the Map.

The preferred order for mapping technique is:

1. Field map
You provide a dict describing which fields should map to which between the source
and destination, Snowbird does the rest. You can also specify related fields and Snowbird
will take care of matching the destination related rows to their correct rows in the
source database.

2. process_row
If you need to perform any logic on the source rows before inserting them into
the destination datastore, you can override process_row. Each row in source will
be passed to processed_row. You return the data for source in one of a few different
formats:

...


3. process_queryset
In some cases the transform logic may depend on non-trivial operations, or you may need to
populate additional tables like intermediate tables after the primary destination rows have been
created. process_queryset lets you still take advantage of the built-in batching facilities
while giving more control over the mapping logic for each batch. You can still have Snowbird
handle the insert for you.



4. process
If some aspect of the transform logic for a particular job requires that you manage
some state across processing all rows, you'll need to override process. 

