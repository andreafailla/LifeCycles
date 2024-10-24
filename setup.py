from codecs import open
from os import path

from setuptools import setup, find_packages

__author__ = "Andrea Failla"
__license__ = "MIT"
__email__ = "andrea.failla@phd.unipi.it"


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    requirements = f.read().splitlines()


setup(
    name="lifecycles",
    version="0.0.1",
    license="",
    description="Package to analyze the temporal dynamics of (groups of) entities/nodes",
    url="https://github.com/andreafailla/lifecycles",
    author="Andrea Failla",
    author_email="andrea.failla@phd.unipi.it",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    keywords="clusters communities analysis",
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={"flag": []},
    packages=find_packages(
        exclude=[
            "*.test",
            "*.test.*",
            "test.*",
            "test",
            "lifecycles.test",
            "lifecycles.test.*",
        ]
    ),
)
