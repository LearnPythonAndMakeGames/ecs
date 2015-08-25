#!/usr/bin/env python
'''
Installs ecs
'''
from setuptools import setup

ecs_version = __import__('ecs').__version__
ecs_doc = __import__('ecs').__doc__
ecs_license = __import__('ecs').__license__
ecs_url = __import__('ecs').__url__
ecs_author = __import__('ecs').__author__

setup(
    name='ecs',
    version=ecs_version,
    license=ecs_license,
    url=ecs_url,
    author=ecs_author,
    description=ecs_doc,
    packages=[''],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Game Development',
        'Framework :: ecs',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache 2.0 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)