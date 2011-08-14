Introduction
=============

Overview
--------

The goal of Snowbird is to provide a declarative framework for moving data
in and out of Django projects.  The framework takes care of structuring the
read and write operations so that in many cases the rules for mapping the data
can be specified with minimal code, relying on the framework to handle the heavy
lifting of the read, transform/map, write cycle. The goal is to offload aspects like
batching operations, mapping foreign key relationships, and handling hierarchical data
to the framework. The framework will attempt to run operations with reasonable
tradeoffs between I/O performance and memory constraints,
while allowing for easy override of default runtime characteristics.


Running Tests
-------------

pip install -r dependencies/required.pip

export DJANGO_SETTINGS_MODULE='snowbird.tests.settings'

django-admin.py test
