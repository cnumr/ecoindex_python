__version__ = "0.1.0"
from nest_asyncio import apply as nest_asyncio_apply

from .ecoindex import get_ecoindex
from .scrap import get_page_analysis

nest_asyncio_apply()
