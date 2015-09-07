try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='benu',
      description='python plotting tool',
      packages=['benu'],
      version="0.1.0",
      )
