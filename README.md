# ECOINDEX PYTHON

![Quality check](https://github.com/cnumr/ecoindex_python/workflows/Quality%20checks/badge.svg)
[![PyPI version](https://badge.fury.io/py/ecoindex.svg)](https://badge.fury.io/py/ecoindex)

This basic module provides a simple interface to get the [Ecoindex](http://www.ecoindex.fr) based on 3 parameters:

- The number of DOM elements in the page
- The size of the page
- The number of external requests of the page

## Requirements

- Python ^3.8 with [pip](https://pip.pypa.io/en/stable/installation/)
- Google Chrome installed on your computer

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

Get ecoindex from DOM elements, size of page and requests of the page
ecoindex = asyncio.run(get_ecoindex(dom=100, size=100, requests=100))
pprint(ecoindex)

Result example:
```python
Ecoindex(grade='B', score=67, ges=1.66, water=2.49)
```

### Get a page analysis

You can run a page analysis by calling the function `get_page_analysis()`:

```python
(function) get_page_analysis: (url: HttpUrl, window_size: WindowSize | None = WindowSize(width=1920, height=1080), wait_before_scroll: int | None = 1, wait_after_scroll: int | None = 1) -> Coroutine[Any, Any, Result]
```

Example:

```python
import asyncio
from pprint import pprint

from ecoindex import get_page_analysis

page_analysis = asyncio.run(get_page_analysis(url="http://ecoindex.fr"))
pprint(page_analysis)
```

Result example:

```python
Result(width=1920, height=1080, url=HttpUrl('http://ecoindex.fr', scheme='http', host='ecoindex.fr', tld='fr', host_type='domain'), size=422.126, nodes=54, requests=12, grade='A', score=86.0, ges=1.28, water=1.92, date=datetime.datetime(2021, 10, 8, 10, 20, 14, 73831), page_type=None)
```

> **Default behaviour:** By default, the page analysis simulates:
>
> - Window size of **1920x1080** pixels (can be set with parameter `window_size`)
> - Wait for **1 second when page is loaded** (can be set with parameter `wait_before_scroll`)
> - Scroll to the bottom of the page (if it is possible)
> - Wait for **1 second after** having scrolled to the bottom of the page (can be set with parameter `wait_after_scroll`)

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
