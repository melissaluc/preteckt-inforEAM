"""
This is example code that illustrates how to fetch
Fault History information from Preteckt's API.
https://dash.preteckt.us/api/fault-history/
Note on API Rate limits: Authenticated users 
have a rate limit of 500k requests per day.
This script requires requests (https://pypi.org/project/requests/), 
but otherwise should work with just the standard library.
"""

import os
import ssl
import certifi
from urllib.request import urlopen

import argparse
import itertools
import time
from typing import Generator, Optional

import requests

# Retrieve your API auth token from: https://dash.preteckt.us/accounts/
AUTH_TOKEN = "1731a683f8d7dc71426316bb388efa4f35fe055c"
PAGE_SIZE = 100  # Number of items per page of the api, Maximum is 1000
URL = "https://dash.preteckt.us/api/fault-history/"



# urlopen(URL, context=ssl.create_default_context(cafile=certifi.where()))

def fetch_all(
    start_date: Optional[str] = None, unit_number: Optional[str] = None
) -> Generator[list, None, None]:
    """
    This function illustrates how to fetch data from Preteckt's Fault Code History
    API, following paginated results.
    It implements two of the available filters (from_time & unit_number), but also
    illustrats how to set a desired number of results per page using the page_size
    parameter.
    """
    # GET parameters for the API request. These correspont to the Filters available on the endpoint.
    params = {"page_size": PAGE_SIZE}
    if start_date is not None:
        params["from_time"] = start_date
    if unit_number is not None:
        params["unit_number"] = unit_number

    # HTTP headers
    headers = {"Authorization": f"Token {AUTH_TOKEN}"}

    # Fetch pages of content
    next_page = URL
    while next_page is not None:
        resp = requests.get(URL, params=params, headers=headers)
        if resp.status_code == 200:
            payload = resp.json()
            next_page = payload["next"]
            print(f"Got {len(payload['results'])} items. Next: {next_page}")
            yield payload["results"]
        else:
            print(f"Got {resp.status_code}... trying again in 5s.")
            time.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script allows you to fetch Fault Code History from the Preteckt API"
    )
    parser.add_argument("-s", "--start-date", type=str, help="Starting Date")
    parser.add_argument(
        "-u",
        "--unit-number",
        type=str,
        help="The Unit number for the device installed in a vehicle",
    )
    args = parser.parse_args()

    # fetch_all will return a list of results per page;
    # we can use itertools.chain to flatten that into a single list of results.
    results = list(
        itertools.chain(
            *fetch_all(start_date=args.start_date, unit_number=args.unit_number)
        )
    )
    print(f"Got {len(results)} total results.")