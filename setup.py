#!/usr/bin/env python
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'rjpl',
  packages = ['rjpl'],
  version = '0.3.6',
  license='MIT',
  description = 'Interface with Rejseplanen API',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Thomas Passer Jensen',
  author_email = 'tomatpasser@gmail.com',
  url = 'https://github.com/tomatpasser/python-rejseplanen',
  download_url = 'https://github.com/tomatpasser/python-rejseplanen/archive/v0.3.6.tar.gz',
  keywords = ['transport', 'rejseplanen', 'timetable', 'journey', 'public transport'],
  install_requires=[
          'requests>=2.9.1',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
