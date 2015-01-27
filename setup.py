#-*- coding: utf-8 -*-
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='opn',
      version='0.1.0',
      description="A global optimization package",
      long_description="README.txt",
      author='Oğuz Altun',
      author_email='oguz211@gmail.com',
      license='TODO',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
			'mayavi>=4.3.1',
			'matplotlib>=1.4.2',
			'numpy>=1.9.1',
          ],
		  
      )