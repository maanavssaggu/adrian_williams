import os
from setuptools import setup


# Read the contents of the Pipfile.lock file
pipfile_lock = os.path.join(os.path.dirname(__file__), 'Pipfile.lock')
requirements = []
if os.path.exists(pipfile_lock):
    import json
    with open(pipfile_lock) as f:
        pipfile_data = json.load(f)
        if 'default' in pipfile_data:
            requirements = [package[0] + package[1]['version'] for package in pipfile_data['default'].items()]


# Perform the setup
setup(
    name='adrian-william-wsr',
    version='1.0',
    description='Weekly Service Report App',
    author='Adrian William',
    install_requires=requirements,
    packages=['AdrianWilliamsWSR'],
)

