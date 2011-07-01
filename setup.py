"""
snowbird
--------

Tools for migrating data
"""
from setuptools import setup


setup(
    name='snowbird',
    version='0.1',
    url='http://github.com/unbracketed/snowbird/',
    license='BSD',
    author='Brian Luft',
    packages=['snowbird'],
    #namespace_packages=['snowbird'],
    zip_safe=False,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)
