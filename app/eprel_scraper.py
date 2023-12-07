import asyncio

import aiohttp

from core.settings import settings


def eprel_id_generator():
    for id in range(settings.eprel_id_min, settings.eprel_id_max+1):
        yield id


async def get_eprel_category(session, eprel_id):
    url_short = settings.eprel_url_shart.format(eprel_id=eprel_id)
    async with session.get(url_short) as response:
        return response.url.path.split('/')[-2]


async def scrap_eprel_id(session, eprel_id, eprel_category):
    url_api = settings.eprel_url_api.format(
        eprel_id=eprel_id, eprel_category=eprel_category
    )
    async with session.get(
        url_api,
        headers={'x-api-key': '3PR31D3F4ULTU1K3Y2020'},
    ) as response:
        print(await response.json())
        print()


async def gather_eprel(get_eprel_id):
    for eprel_id in get_eprel_id:
        async with aiohttp.ClientSession() as session:
            eprel_category = await get_eprel_category(session, eprel_id)
            if eprel_category in settings.category_exceptional:
                pass
            elif eprel_category == settings.category_error:
                pass
            elif eprel_category not in settings.category_to_scrap:
                pass
            else:
                await scrap_eprel_id(session, eprel_id, eprel_category)


async def main():
    get_eprel_id = eprel_id_generator()
    tasks = []
    for _ in range(settings.eprel_maximum_connections+1):
        tasks.append(asyncio.create_task(gather_eprel(get_eprel_id)))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
