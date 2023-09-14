"""Demo script for testing concurrency. This version contains threads"""

import concurrent.futures
import threading
import time

import requests

# Create an object that looks global but is specific to each individual
# thread. One of these objects can be used for all threads in the script.
thread_local = threading.local()

MAX_WORKERS = 40


def get_session():
    """Return a session for each thread.

    Check the current thread for a session. If no session exists, one is
    created and then returned. Otherwise the already existing session is
    returned. There is a separate session for each thread, hence the use of
    'thread_local'.
    """
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    """Download the data from the specified URL.

    We create a new session for each thread. Then we use the session to
    download from the URL.

    Args:
        url: The URL we want to download data from
    """
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites(sites):
    """Download the data from all specified web sites.

    The download of data from the individual sites is handled within multiple
    threads.

    Args:
        sites: The list of websites to download from
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(download_site, sites)


if __name__ == "__main__":
    websites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(websites)
    duration = time.time() - start_time
    print(
        f"Downloaded {len(websites)} in {duration} seconds using {MAX_WORKERS} threads"
    )
