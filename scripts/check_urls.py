# modified fetch function with semaphore
import random
import asyncio
from aiohttp import ClientSession


def store_list(store_file):
    f = open(store_file, "r")
    stores = f.readlines()
    stores = ["https://" + store.strip() for store in stores]
    return stores

# ASYNC FUNCTIONS


async def fetch(url, session):
    try:
        async with session.get(url, timeout=5) as response:
            print(response.status)
            await response.read()
            return response.status
    except Exception as e:
        print(e)


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        return await fetch(url, session)


async def run(r):
    store_file = "urls.list"
    stores = store_list(store_file)

    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for url in stores[:500]:
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return responses

###

if __name__ == '__main__':

    number = 10000
    loop = asyncio.get_event_loop()

    future = asyncio.ensure_future(run(number))
    result = loop.run_until_complete(future)
