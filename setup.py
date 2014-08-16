#!/usr/bin/env python
from setuptools import setup

setup(
    name = "yums3tools",
    version = "0.1.0",
    description = "Yum S3 Tools",
    author = "Michal Bicz",
    author_email = "michal@bicz.net",
    packages =['yums3tools'], 
    scripts = ['scripts/find-package.py'],
    install_requires = [
        'docopt',
        'boto'
        ]
)
