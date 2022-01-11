from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Tiny Data Analysis Library'
LONG_DESCRIPTION = 'A tiny data analysis library written using Python and Numpy.'

setup(
    name="ickle",
    version=VERSION,
    author="Karishma Shukla",
    author_email="<karishmashuklaa@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['python', 'pytest'],
    keywords=['data-analysis', 'numpy', 'data', 'python', 'library', 'pandas', 'ickle'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)