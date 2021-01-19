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
	  - |actions_linux| |actions_windows| |actions_macos|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy| |pre_commit_ci|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/photo-sort/latest?logo=read-the-docs
	:target: https://photo-sort.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/photo-sort/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/photo-sort/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/photo-sort/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/photo-sort/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/photo-sort/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/photo-sort/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/photo-sort/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/photo-sort/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/photo-sort/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/photo-sort/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/photo-sort/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/photo-sort/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/domdfcoding/photo-sort/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/photo-sort/requirements/?branch=master
	:alt: Requirements Status

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/photo-sort?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/photo-sort
	:alt: CodeFactor Grade

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

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/photo-sort/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/photo-sort/master
	:alt: pre-commit.ci status

.. end shields

Installation
--------------

.. start installation

``photo-sort`` can be installed from GitHub.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install git+https://github.com/domdfcoding/photo-sort

.. end installation

You'll also need ``exiftool`` installed. On Debian/Ubuntu:

.. code-block:: bash

	$ sudo apt install exiftool
