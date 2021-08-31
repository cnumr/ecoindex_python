# ECOINDEX PYTHON

![Quality check](https://github.com/cnumr/ecoindex_python/workflows/Quality%20checks/badge.svg)
[![PyPI version](https://badge.fury.io/py/ecoindex.svg)](https://badge.fury.io/py/ecoindex)

This basic module provides a simple interface to get the [Ecoindex](http://www.ecoindex.fr) based on 3 parameters:

- The number of DOM elements in the page
- The size of the page
- The number of external requests of the page

> **Current limitation:** This does not work well with SPA.

## Requirements

- Python ^3.8
- [Poetry](https://python-poetry.org/)
- Google Chrome installed on your computer

## Install

```shell
pip install ecoindex
```

## Use

```python
from pprint import pprint

from ecoindex import get_ecoindex
from ecoindex import get_page_analysis

# Get ecoindex from DOM elements, size of page and requests of the page
ecoindex = get_ecoindex(dom=100, size=100, requests=100)
pprint(ecoindex)

> Ecoindex(grade='B', score=67, ges=1.66, water=2.49)

# Analyse a given webpage with a resolution of 1920x1080 pixel (default)
page_analysis = get_page_analysis(url="http://ecoindex.fr")
pprint(page_analysis)

> Result(size=119.292, nodes=45, requests=7, grade='A', score=89.0, ges=1.22, water=1.83, url=HttpUrl('http://ecoindex.fr', scheme='http', host='ecoindex.fr', tld='fr', host_type='domain'), date=datetime.datetime(2021, 7, 29, 13, 46, 54, 396697), height=1080, width=1920, page_type=None)

```

## Use remote chrome

You can use a remote chrome browser such as [browserless/chrome](https://hub.docker.com/r/browserless/chrome). Just set the environment variable `REMOTE_CHROME_URL` with the url of the remote chrome browser:

```bash
export REMOTE_CHROME_URL="http://localhost:3000/webdriver"
```

## Tests

```shell
pytest
```

## [Contributing](CONTRIBUTING.md)

## [Code of conduct](CODE_OF_CONDUCT.md)
