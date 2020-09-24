#!/usr/bin/env python3

from setuptools import setup
import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

long_description = open('README.md').read()

setup(name='verdure',
      version=get_version('verdure'),
      description="Run a program with a given version.",
      long_description=long_description,
      maintainer='Reuben Thomas',
      maintainer_email='rrt@sc3d.org',
      url='https://github.com/rrthomas/verdure',
      license='GPL v3 or later',
      scripts=['verdure'],
      classifiers=[
          'Environment :: Console',
          'Programming Language :: Python :: 3',
      ],
     )
