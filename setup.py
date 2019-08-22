import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
    version = f.read().strip()

setup(
    name='ossearch',
    version=version,
    description='searches for open source projects within directories',
    author='JeffJerseyCow',
    author_email='jeffjerseycow@gmail.com',
    url='https://github.com/JeffJerseyCow/ossearch',
    install_requires=['gremlinpython', 'docker'],
    packages=find_packages(),
    entry_points={'console_scripts': ['ossearch=ossearch.__main__:main']},
)
