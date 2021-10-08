# ECOINDEX PYTHON

![Quality check](https://github.com/cnumr/ecoindex_python/workflows/Quality%20checks/badge.svg)
[![PyPI version](https://badge.fury.io/py/ecoindex.svg)](https://badge.fury.io/py/ecoindex)

This basic module provides a simple interface to get the [Ecoindex](http://www.ecoindex.fr) based on 3 parameters:

- The number of DOM elements in the page
- The size of the page
- The number of external requests of the page

> **Current limitation:** This does not work well with SPA.

## Requirements

- Python ^3.8 with [pip](https://pip.pypa.io/en/stable/installation/)
- Google Chrome installed on your computer (or you can use [browserless/chrome](https://hub.docker.com/r/browserless/chrome), see [more about configuration](#use-remote-chrome))

## Install

```shell
pip install ecoindex
```

## Use

```python
import asyncio
from pprint import pprint

from ecoindex import get_ecoindex, get_page_analysis

# Get ecoindex from DOM elements, size of page and requests of the page
ecoindex = asyncio.run(get_ecoindex(dom=100, size=100, requests=100))
pprint(ecoindex)

> Ecoindex(grade='B', score=67, ges=1.66, water=2.49)

# Analyse a given webpage with a resolution of 1920x1080 pixel (default)
page_analysis = asyncio.run(get_page_analysis(url="http://ecoindex.fr"))
pprint(page_analysis)

> Result(width=1920, height=1080, url=HttpUrl('http://ecoindex.fr', scheme='http', host='ecoindex.fr', tld='fr', host_type='domain'), size=422.126, nodes=54, requests=12, grade='A', score=86.0, ges=1.28, water=1.92, date=datetime.datetime(2021, 10, 8, 10, 20, 14, 73831), page_type=None)
```

## Use remote chrome

You can use a remote chrome browser such as [browserless/chrome](https://hub.docker.com/r/browserless/chrome). You just have to run the docker image:

```bash
docker run -p 3000:3000 browserless/chrome
```

And then set the environment variable `REMOTE_CHROME_URL` with the url of the remote chrome browser (or set it in the `.env` file):

```bash
export REMOTE_CHROME_URL="http://localhost:3000/webdriver"
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

## [Contributing](CONTRIBUTING.md)

## [Code of conduct](CODE_OF_CONDUCT.md)
