from ossearch.utils import load_config
from setuptools import setup, find_packages

setup(
    name='ossearch',
    version=load_config()['version'],
    description='searches for open source projects within directories',
    author='JeffJerseyCow',
    author_email='jeffjerseycow@gmail.com',
    url='https://github.com/JeffJerseyCow/ossearch',
    install_requires=['gremlinpython', 'docker'],
    packages=find_packages(),
    entry_points={'console_scripts': ['ossearch=ossearch.__main__:main']},
)
