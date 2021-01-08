# ECOINDEX PYTHON

This basic module provides a simple interface to get the [Ecoindex](http://www.ecoindex.fr) based on 3 parameters:

- The number of DOM elements in the page
- The size of the page
- The number of external requests of the page

## Requirements

- Python ^3.8

## Install

```shell
pip install ecoindex
```

## Use

```python
from ecoindex import get_ecoindex
from pprint import pprint

result = get_ecoindex(dom=100, size=100, requests=100)
pprint(result)
```

```python
Ecoindex(grade='B', score=67, ges=1.66, water=2.49)
```

## Tests

```shell
pytest
```
