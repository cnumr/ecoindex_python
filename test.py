import asyncio
from pprint import pprint

from ecoindex import get_ecoindex

ecoindex = asyncio.run(get_ecoindex(dom=100, size=100, requests=100))
pprint(ecoindex)
