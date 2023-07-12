import os
from setuptools import setup

def read_requirements():
    with open('Pipfile.lock') as f:
        requirements = f.readlines()
    return [req.strip() for req in requirements]

setup(
    name='adrian-william-wsr',
    version='1.0',
    install_requires=read_requirements(),
)