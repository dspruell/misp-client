"""MISP client tooling."""

from os import path
from codecs import open
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="misp-client",
    version="0.4.1",
    description="Client interface for interacting with MISP instances",
    long_description=long_description,
    url="https://github.com/dspruell/misp-client",
    author="Darren Spruell",
    author_email="phatbuckett@gmail.com",
    license="ISC",
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: System :: Networking :: Monitoring",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pymisp",
        "PyYAML",
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "misp-client = misp_client.cli:main",
        ],
    },
)
