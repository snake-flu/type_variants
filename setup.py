from setuptools import setup, find_packages
import glob
import os
import pkg_resources

setup(name='type_variants',
      version=1.0,
      packages=find_packages(),
      scripts=['type_variants.py',
                ],
      install_requires=[
            "biopython>=1.70",
        ],
      description='Sars-Cov-2 variant typing command line tool',
      url='https://github.com/cov-ert/type_variants',
      author='Ben Jackson',
      entry_points="""
      [console_scripts]
      """,
      keywords=[],
      zip_safe=False)
