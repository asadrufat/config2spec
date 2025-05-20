#!/usr/bin/env python
import os
from distutils.core import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(name="Config2Spec",
      version="0.1",
      description="Automatic Network Specification Learning",
      author="Ruediger Birkner",
      author_email="rbirkner@ethz.ch",
      install_requires=[
          'pandas', #1.3.5
          'pytricia==1.0.0',
          'requests==2.21.0',
          'networkx==3.4.2',
          'netaddr==0.7.19',
          'numpy==1.26.4',
      ],
      packages=["config2spec"],
      long_description=read("README.md"),
)