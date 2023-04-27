import asyncio
from pprint import pprint

from ecoindex import get_ecoindex

# Get ecoindex from DOM elements, size of page and requests of the page
ecoindex = asyncio.run(get_ecoindex(dom=2240, size=310182.902, requests=254))
pprint(ecoindex)
