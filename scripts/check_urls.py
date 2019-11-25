# modified fetch function with semaphore

import asyncio
import time
from aiohttp import ClientSession
from dataclasses import dataclass
from influxdb import InfluxDBClient


INFLUX_CLIENT = InfluxDBClient(
    'influxdb', '8086', 'admin', 'admin', 'http_monitor')
STORE_FILE = "/scripts/urls.list"


@dataclass
class Domain_Check:
    domain: str
    status: int
    response_time: float


def send_to_influx(data):
    # fields can be updated with new measurements as desired
    json_body = [
        {
            "measurement": "http_response",
            "tags": {
                "domain": data.domain,
                "status": data.status
            },
            #           "time": data["time"] + "000000000",
            "fields": {
                "response_time": data.response_time,
            }
        }
    ]
    output = INFLUX_CLIENT.write_points(json_body)
    return output


def store_list(store_file):
    f = open(store_file, "r")
    stores = f.readlines()
    stores = ["https://" + store.strip() for store in stores]
    return stores

# ASYNC FUNCTIONS


async def fetch(url, session):
    try:
        start = time.time()
        async with session.get(url, timeout=30) as response:
            await response.read()
            end = time.time()
            return Domain_Check(response.url,
                                response.status,
                                end - start
                                )
    except Exception as e:
        print(e)
        return Domain_Check(url,
                            0,
                            0.0
                            )


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        return await fetch(url, session)


async def run(r):
    store_file = STORE_FILE
    stores = store_list(store_file)

    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for url in stores:
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return responses

###

if __name__ == '__main__':

    """
    hits URLs in batches of 10,000, if you have that many.
    Allows the script to scale for larger use.

    """
    number = 10000
    loop = asyncio.get_event_loop()

    future = asyncio.ensure_future(run(number))
    result = loop.run_until_complete(future)
    for data in result:
        send_to_influx(data)
