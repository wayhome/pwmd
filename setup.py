from setuptools import setup, find_packages
import os

version = '0.1'


def read_file(*path):
    base_dir = os.path.dirname(__file__)
    file_path = (base_dir, ) + tuple(path)
    return file(os.path.join(*file_path)).read()

setup(name='pwmd',
      version=version,
      description="Multi Database Support For PeeWee",
      long_description=read_file("README.rst"),
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='multi database orm peewee',
      author='Young King',
      author_email='yanckin@gmail.com',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'peewee>=2.0.4',
      ],
      tests_require=['Nose'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
