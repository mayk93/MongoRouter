#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path

current_path = path.abspath(path.dirname(__file__))

with open(path.join(current_path, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='MongoRouter',
    version='0.1.2',
    description='A routing package for Mongo DB',
    long_description=long_description,

    author='Michael',
    author_email='mihai@mandrescu.co',
    url='http://www.mandrescu.co',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License'
    ],

    keywords='mongo pymongo database nosql',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['pymongo', 'dnspython']
)