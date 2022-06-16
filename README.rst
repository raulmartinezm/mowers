Mowers Challenge
================

|pre-commit| |Black|

.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


Run the tests
--------

Build the Docker image and run it:

..  code: console

    $ docker build -t mowers-challenge:latest .
    ...
    $ docker run -it --rm mowers-challenge:latest


Requirements
------------

* Docker
* Linux (because it hasn't been not tested in Windows).

Python versions
---------------

.. code:: console

   pyenv local 3.10.4 3.9.12 3.8.13 3.7.13


Usage
-----

Please see the `Command-line Reference <Usage_>`_ for details.



Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/raulmartinezm/seat-code-mowers/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://seat-code-mowers.readthedocs.io/en/latest/usage.html
