import asyncio
from pprint import pprint

from ecoindex import get_page_analysis

page_analysis = asyncio.run(get_page_analysis(url="https://meteofrance.com/"))
pprint(page_analysis)
