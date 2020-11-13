###########
photo-sort
###########

.. start short_desc

**A program for sorting photographs into folders.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |travis| |actions_windows| |actions_macos| |codefactor| |pre_commit_ci|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/photo-sort/latest?logo=read-the-docs
	:target: https://photo-sort.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/photo-sort/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/photo-sort/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/photo-sort/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/photo-sort
	:alt: Travis Build Status

.. |actions_windows| image:: https://github.com/domdfcoding/photo-sort/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/photo-sort/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Tests Status

.. |actions_macos| image:: https://github.com/domdfcoding/photo-sort/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/photo-sort/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Tests Status

.. |requires| image:: https://requires.io/github/domdfcoding/photo-sort/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/photo-sort/requirements/?branch=master
	:alt: Requirements Status

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/photo-sort?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/photo-sort
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/photo-sort
	:target: https://pypi.org/project/photo-sort/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/photo-sort?logo=python&logoColor=white
	:target: https://pypi.org/project/photo-sort/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/photo-sort
	:target: https://pypi.org/project/photo-sort/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/photo-sort
	:target: https://pypi.org/project/photo-sort/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/photo-sort
	:target: https://github.com/domdfcoding/photo-sort/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/photo-sort
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/photo-sort/v0.0.0
	:target: https://github.com/domdfcoding/photo-sort/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/photo-sort
	:target: https://github.com/domdfcoding/photo-sort/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/photo-sort/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/photo-sort/master
	:alt: pre-commit.ci status

.. end shields

Installation
--------------

.. start installation

``photo-sort`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install photo-sort

.. end installation

You'll also need ``exiftool`` installed. On Debian/Ubuntu:

.. code-block:: bash

	$ sudo apt install exiftool
