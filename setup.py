from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='flybratron_runners',
    version='0.0.1',
    description='A collection of trial runners for working with the flybratron system',
    long_description=__doc__,
    url='https://github.com/willdickson/flybratron_runners',
    author='Will Dickson',
    author_email='will@iorodeo.com',
    license='MIT',
    keywords='Flybraton',
    packages=find_packages(exclude=['examples']),
    install_requires=[
        'numpy',
        # Added repository flybratron, etc. 
        ],
)
