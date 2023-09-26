from asyncio import run
from sys import version

from faker import Faker
from faker_enum import EnumProvider
from typer import Typer, confirm, progressbar

from ecoindex.backend.api.utils.generate_uuid import new_uuid
from ecoindex.backend.database.engine import prisma
from ecoindex.compute.ecoindex import get_ecoindex

app = Typer()


async def create_data(count: int = 10):
    await prisma.connect()

    faker = Faker()
    faker.add_provider(EnumProvider)

    with progressbar(range(count)) as progress:
        for _ in progress:
            id = await new_uuid()
            base_url = faker.url()[8:-1]
            url = f"https://{base_url}/{id}"
            initial_ranking = faker.pyint(min_value=0, max_value=100)
            ecoindex_version = version

            nb_requests = faker.pyint(min_value=1, max_value=5)

            size = faker.pyfloat(min_value=100, max_value=10000)
            nodes = faker.pyint(min_value=10, max_value=1000)
            requests = nb_requests
            requests_details = [
                {
                    "url": faker.url(),
                    "type": faker.random_element(
                        elements=(
                            "image",
                            "script",
                            "stylesheet",
                            "font",
                            "document",
                            "other",
                        )
                    ),
                    "size": faker.pyfloat(min_value=0.5, max_value=3000),
                }
                for _ in range(nb_requests)
            ]
            ecoindex = await get_ecoindex(size=size, dom=nodes, requests=requests)

            data = {
                "id": str(id),
                "version": 1,
                "width": faker.pyint(min_value=300, max_value=3000, step=10),
                "height": faker.pyint(min_value=200, max_value=2000, step=10),
                "host": base_url,
                "date": faker.date_time_this_year(),
                "page_type": "",
                "size": size,
                "nodes": nodes,
                "requests": requests,
                "grade": ecoindex.grade,
                "score": ecoindex.score,
                "ges": ecoindex.ges,
                "water": ecoindex.water,
                "url": url,
                "initial_ranking": initial_ranking,
                "initial_total_results": faker.pyint(min_value=initial_ranking),
                "ecoindex_version": ecoindex_version,
                "requests_details": {"create": requests_details},
            }

            await prisma.ecoindex.create(data=data)

    await prisma.disconnect()


@app.command()
def populate_data(count: int = 10):
    confirm(f"You are about to generate {count} results, are you OK?", abort=True)
    run(create_data(count=count))


if __name__ == "__main__":
    app()
