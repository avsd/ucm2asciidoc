#!/usr/bin/env python
"""
Installation script for installing UseCaseMaker
library for AsciiDoc.

Copyright 2009 David Avsajanishvili
avsd05@gmail.com

The software is released under Modified BSD license
"""

from distutils.core import setup

setup(name='ucm2asciidoc',
      version='0.1',
      description='Tools for converting UseCaseMaker XML file to AsciiDoc source',
      author='David Avsajanishvili',
      author_email='avsd05@gmail.com',
      url='',
      packages=['ucm2asciidoc'],
      scripts=['scripts/ucm2asciidoc'],
      #data_files=[('license', ['LICENSE']),],
      license='BSD')
