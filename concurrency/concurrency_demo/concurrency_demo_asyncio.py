"""Demo script for testing concurrency using asyncio"""

import asyncio
import time

import aiohttp


async def download_site(session, url):
    """Download the site data from the specified URL.

    Args:
        session: The session to connect to the URL
        url: The URL to download from
    """
    async with session.get(url) as response:
        print(f"Read {response.content_length} from {url}")


async def download_all_sites(sites):
    """Download the information from all sites in the received list.

    You only need to use one session because all the tasks are running on the
    same thread. All the tasks are created first and stored in the event pool.
    Then asyncio.gather keeps the session context alive until all the tasks
    have completed.
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.ensure_future(download_site(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    websites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(download_all_sites(websites))
    # asyncio.run(download_all_sites(websites))
    duration = time.time() - start_time
    print(f"Downloaded {len(websites)} in {duration} seconds")
