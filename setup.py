from setuptools import setup
from os import path
from io import open

# read the contents of README.md
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="benu",
    version="0.1.0",
    description="python plotting tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["benu"],
)
