from asyncio import run
from json import dumps
from os import getcwd

from aiofile import async_open
from requests import get


async def update_values_async() -> None:
    response = get(
        "https://raw.githubusercontent.com/cnumr/ecoindex_reference/main/ecoindex_reference.json",
    )

    data = response.json()
    data_folder = f"{getcwd()}/ecoindex/data/"

    async with async_open(f"{data_folder}grades.py", "w") as grades_file, async_open(
        f"{data_folder}medians.py", "w"
    ) as median_file, async_open(
        f"{data_folder}colors.py", "w"
    ) as colors_file, async_open(
        f"{data_folder}targets.py", "w"
    ) as target_file, async_open(
        f"{data_folder}quantiles.py", "w"
    ) as quantile_file:
        # Update medians
        medians = f"median_dom = {dumps(data['medians']['dom_size'])}\n"
        medians += f"median_req = {dumps(data['medians']['nb_request'])}\n"
        medians += f"median_size = {dumps(data['medians']['response_size'])}\n"

        # Update grades
        grades = ""
        colors = ""

        for grade in data["grades"]:
            grades += f"{grade['grade']} = {grade['value']}\n"
            colors += f"{grade['grade']} = {dumps(grade['color'])}\n"

        # Update targets
        targets = f"target_dom = {dumps(data['targets']['dom_size'])}\n"
        targets += f"target_req = {dumps(data['targets']['nb_request'])}\n"
        targets += f"target_size = {dumps(data['targets']['response_size'])}\n"

        # Update quantiles
        quantiles = f"quantiles_dom = {dumps(data['quantiles']['dom_size'])}\n"
        quantiles += f"quantiles_req = {dumps(data['quantiles']['nb_request'])}\n"
        quantiles += f"quantiles_size = {dumps(data['quantiles']['response_size'])}\n"

        await quantile_file.write(quantiles)
        await target_file.write(targets)
        await colors_file.write(colors)
        await median_file.write(medians)
        await grades_file.write(grades)

    print("Values updated")


def main():
    run(update_values_async())


if __name__ == "__main__":
    main()
