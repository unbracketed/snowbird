Managing Migrations
====================


Mapping Data
-------------

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



Running and Customizing Migration Jobs
---------------------------------------

A primary focus of Snowbird is providing control, flexibility, and feedback
so the developer can craft effective workflows with minimal effort. Taking advantage
of the following features will help you build, test, debug, and execute your migrations
with improved productivity.

1. Pause / Graceful Stop
2. Resume
3. Timing
4. Logging
5. Partial Jobs
6. Strict Mode vs. Continue on Fail


Graceful Stop
~~~~~~~~~~~~~~

The ability to cancel the process and leave data in a consistent state.


Resume
~~~~~~

The ability to restart the process from a specific point.


Timing
~~~~~~

The ability to record how long a job takes.


Logging
~~~~~~~

The ability to record what was done, and what went wrong


Partial Jobs
~~~~~~~~~~~~

The ability to run a job against a single row, a ranges of rows, or a single table


Strict Mode
~~~~~~~~~~~

The ability to have the migration ignore errors (log them of course) or stop on any exception
