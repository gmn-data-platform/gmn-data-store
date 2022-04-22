GMN Data Store
==============

|PyPI| |Status| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/gmn-data-store.svg
   :target: https://pypi.org/project/gmn-data-store/
   :alt: PyPI
.. |Status| image:: https://img.shields.io/pypi/status/gmn-data-store.svg
   :target: https://pypi.org/project/gmn-data-store/
   :alt: Status
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/gmn-data-store
   :target: https://pypi.org/project/gmn-data-store
   :alt: Python Version
.. |License| image:: https://img.shields.io/github/license/gmn-data-platform/gmn-data-store
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/gmn-data-store/latest.svg?label=Read%20the%20Docs
   :target: https://gmn-data-store.readthedocs.io/
   :alt: Read the documentation at https://gmn-data-store.readthedocs.io/
.. |Tests| image:: https://github.com/gmn-data-platform/gmn-data-store/workflows/Tests/badge.svg
   :target: https://github.com/gmn-data-platform/gmn-data-store/actions?query=workflow%3ATests+branch%3Amain
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/gmn-data-platform/gmn-data-store/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/gmn-data-platform/gmn-data-store
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black

`Global Meteor Network`_ (GMN) database models, controllers and scripts.

This project stores GMN meteor data in a relational SQLite database where the database schema is generated using the gmn-python-api_ library. The `GMN Data Platform`_ project aims to deploy this on the GMN server. The Python package provided here is used by the `GMN Data Store Ingestion`_ to add/update data in the database. A Datasette_ instance is run for the `GMN Data Portal`_ and it accesses this data to provide user-facing data select querying and a web interface to view the data.

`Database entity relationship diagram`_


The Python package gmn-data-store provides functions for setting up the database, querying data in the database and inserting data into the database. The main insert function is insert_trajectory_summary which takes an AVRO formatted JSON dictionary of meteor trajectory data (more info in the `gmn-python-api docs`_) and inserts the data into the database. The `GMN Data Store Ingestion`_ project inserts trajectory summary Kafka messages using this function.

A Makefile_ is also provided to initially setup the database using Docker. Use the init_all_services Makefile task to create the .db file in the gmn_data_store Docker volume. By default the gmn-data-store package gets the .db file from ~/.gmn_data_store/gmn_data_store.db so mount the volume at ~/gmn_data_store to use the Python package with the .db file in the Docker volume.

Requirements
------------

* Python 3.7.1+, 3.8, 3.9 or 3.10


Installation
------------

You can install *GMN Data Store* via pip_ from `PyPI`_:

.. code:: console

   $ pip install gmn-data-store

Or for the latest development code, through TestPyPI_ or directly from GitHub_ via pip_:

.. code:: console

   $ pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple gmn-data-store==<version>
   Or
   $ pip install git+https://github.com/gmn-data-platform/gmn-data-store


Usage
-----

Refer to the `docs API reference page`_ for function and variable definitions.

Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*GMN Data Store* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

`Hypermodern Python Cookiecutter`_ template.

.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/project/gmn-data-store/
.. _TestPyPI: https://test.pypi.org/project/gmn-data-store/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/rickybassom/gmn-data-store/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://gmn-data-store.readthedocs.io/en/latest/usage.html
.. _Global Meteor Network: https://globalmeteornetwork.org/
.. _GitHub: https://github.com/gmn-data-platform/gmn-data-store
.. _docs API reference page: https://gmn-data-store.readthedocs.io/en/latest/autoapi/gmn_data_store/index.html
.. _gmn-python-api: https://github.com/gmn-data-platform/gmn-python-api
.. _Datasette: https://datasette.io/
.. _GMN Data Portal: https://github.com/gmn-data-platform/gmn-data-endpoints/tree/main/services/gmn_data_portal
.. _GMN Data Store Ingestion: https://github.com/gmn-data-platform/gmn-data-store-ingestion
.. _GMN Data Platform: https://github.com/gmn-data-platform
.. _gmn-python-api docs: https://gmn-python-api.readthedocs.io/en/latest/search.html?q=avro&check_keywords=yes&area=default
.. _functions: https://gmn-python-api.readthedocs.io/en/latest/autoapi/gmn_python_api/meteor_summary_reader/index.html#gmn_python_api.meteor_summary_reader.read_meteor_summary_csv_as_dataframe
.. _Makefile: https://github.com/gmn-data-platform/gmn-data-store/blob/main/Makefile
.. _Database entity relationship diagram: https://github.com/gmn-data-platform/gmn-data-store/blob/main/database_schema.md
