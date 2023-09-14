"""Demo script for testing concurrency using multiprocessing."""

import multiprocessing
import time

import requests

session = None  # pylint: disable=invalid-name


def set_global_session():
    """Set a global session as a singleton.

    If the session does not exist, then a new one is created. If it already
    exists, nothing is done. A separate session object is required for each
    process.
    """
    global session  # pylint: disable=global-statement
    if not session:
        session = requests.Session()


def download_site(url):
    """Download the site data.

    We print out the name of the current process each time, to track the
    different processes.

    Args:
        url: The URL where we want to download from
    """
    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f"{name}:Read {len(response.content)} from {url}")


def download_all_sites(sites):
    """Download all site data within a Multiprocessing Pool.

    Each process in the pool is assigned it's own session, that is reused
    while the process continues to run.

    Args:
        sites: The list of URLs to download data from
    """
    with multiprocessing.Pool(initializer=set_global_session) as pool:
        pool.map(download_site, sites)


if __name__ == "__main__":
    websites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(websites)
    duration = time.time() - start_time
    print(f"Downloaded {len(websites)} in {duration} seconds")
