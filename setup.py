import re
from setuptools import setup, find_packages


setup(
    name='metapipe',
    version='1.0',
    packages=find_packages(),
    description='A pipeline for building analysis pipelines.',
    url='https://github.com/TorkamaniLab/metapipe',
    entry_points = {
        "console_scripts": ['metapipe = metapipe.app:main']
        },
    install_requires = ['pyparsing']
)
