import logging
LOG = logging.getLogger('snowbird')
LOG.addHandler(logging.FileHandler('snowbird.log'))


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'snowbird_test',                      # Or path to database file if using sqlite3.
    },
    'number_two': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'snowbird_test2',                      # Or path to database file if using sqlite3.
    }
}

INSTALLED_APPS = (
    'django_nose',
    'snowbird.tests',
)
try:
    import django_extensions
    INSTALLED_APPS += ('django_extensions', )
except ImportError:
    pass

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
