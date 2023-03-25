from setuptools import setup, find_packages
import codecs
import os

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

VERSION = '1.0.3'
DESCRIPTION = 'Tiny Data Analysis Library'

setup(
    name="ickle",
    version=VERSION,
    author="Karishma Shukla",
    author_email="karishmashuklaa@gmail.com",
    url="https://github.com/karishmashuklaa/ickle",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description= readme(),
    packages=find_packages(),
    install_requires=['numpy', 'pytest'],
    keywords=['data-analysis', 'numpy', 'data', 'python', 'library', 'pandas', 'ickle', 'datascience'],
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)