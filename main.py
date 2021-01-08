from pprint import pprint

from ecoindex.ecoindex import get_ecoindex

result = get_ecoindex(dom=100, size=100, requests=100)
pprint(result)
