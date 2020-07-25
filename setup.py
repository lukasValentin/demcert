#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools
from os import path

home = path.abspath(path.dirname(__file__))
with open(path.join(home, 'README.md'), encoding='utf-8') as readme:
    long_description = readme.read()


setuptools.setup(name='demcert',
      version = '1.0',
      description = 'A general purpose tool for modelling uncertainty on gridded spatial data',
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      author='Lukas Graf',
      author_email ='graflukas@web.de',
      url = '',
      include_package_data=True,
      packages=setuptools.find_packages(),
      classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
     )