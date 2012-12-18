from setuptools import setup, find_packages

version = '0.1'

setup(name='pwmd',
      version=version,
      description="Multi Database Support For PeeWee",
      long_description="""\
Multi Database Support For PeeWee""",
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
