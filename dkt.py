from asyncio import run
from pprint import pprint

from ecoindex import get_page_analysis

urls = [
    "https://www.decathlon.fr",
    "https://www.leroymerlin.fr",
    "https://www.bricoman.fr",
    # "https://bot.sannysoft.com/"
]

for url in urls:
    pprint(run(get_page_analysis(url=url)))
