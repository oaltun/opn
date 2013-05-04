# coding=utf-8

from distutils.core import setup

setup(
    name='PyMeta',
    version='0.1.0',
    author='Oğuz Altun',
    author_email='oguz211@gmail.com',
    packages=['pymeta', 'pymeta.algorithm','pymeta.problem','pymeta.test','pymeta.utils','pymeta.visualiser'],
    scripts=['bin/experiment.py'],
    url='http://pypi.python.org/pypi/PyMeta',
    license='LICENSE.txt',
    description='A Metaheuristic Optimization package, written using Python and Numpy',
    long_description=open('README.txt').read(),
    install_requires=[],
)