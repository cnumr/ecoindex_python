# ECOINDEX PYTHON

![Quality check](https://github.com/cnumr/ecoindex_python/workflows/Quality%20checks/badge.svg)
[![PyPI version](https://badge.fury.io/py/ecoindex.svg)](https://badge.fury.io/py/ecoindex)

This basic module provides a simple interface to get the [Ecoindex](http://www.ecoindex.fr) based on 3 parameters:

- The number of DOM elements in the page
- The size of the page
- The number of external requests of the page

## Requirements

- Python ^3.10 with [pip](https://pip.pypa.io/en/stable/installation/)

## Install

```shell
pip install ecoindex
```

## Use

### Get ecoindex

You can easily get the ecoindex by calling the function `get_ecoindex()`:

```python
(function) get_ecoindex: (dom: int, size: float, requests: int) -> Coroutine[Any, Any, Ecoindex]
```

Example:

```python
import asyncio
from pprint import pprint

from ecoindex import get_ecoindex

# Get ecoindex from DOM elements, size of page and requests of the page
ecoindex = asyncio.run(get_ecoindex(dom=100, size=100, requests=100))
pprint(ecoindex)
```

Result example:

```python
Ecoindex(grade='B', score=72.0, ges=1.56, water=2.34, ecoindex_version='3.0.0')
```

## Contribute

You need [poetry](https://python-poetry.org/) to install and manage dependencies. Once poetry installed, run :

```bash
poetry install
```

## Tests

```shell
poetry run pytest
```

## Disclaimer

The LCA values used by [ecoindex](https://github.com/cnumr/ecoindex_python) to evaluate environmental impacts are not under free license - ©Frédéric Bordage
Please also refer to the mentions provided in the code files for specifics on the IP regime.

## [License](LICENSE)

## [Contributing](CONTRIBUTING.md)

## [Code of conduct](CODE_OF_CONDUCT.md)
