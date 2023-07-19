"""
This is example code that illustrates how to fetch
Fault History information from Preteckt's API.

https://dash.preteckt.us/api/fault-history/

Note on API Rate limits: Authenticated users 
have a rate limit of 500k requests per day.

This script requires requests (https://pypi.org/project/requests/), 
but otherwise should work with just the standard library.

OPTIONS method returns info about API (methods/content type). 
HEAD method returns info about resource (version/length/type)
daily, csv format, 

"""

import os
import ssl
import certifi
from urllib.request import urlopen

import json

import argparse
import itertools
import time
from typing import Generator, Optional
import os
import requests

# Retrieve your API auth token from: https://dash.preteckt.us/accounts/

fileDir = os.path.dirname(os.path.realpath('__file__'))
fp = os.path.join(fileDir, 'config.json')

with open(fp,'r') as file:
    file_data =json.load(file)
    AUTH_TOKEN = file_data["AUTH_TOKEN"]
    URLS = file_data["URL"]

headers = {"Authorization": f"Token {AUTH_TOKEN}"}
params= {"page_size": 1000}

for key in URLS.keys():
    url=URLS[key]
   
    try:
        data = requests.get(url=url,params=params,headers=headers)
        print(data.status_code)
        if (200 <= data.status_code < 300):
            print(key)
    except Exception as e:
        print(e)
        pass
    # print(json.dumps(f_file_data,indent=4))
    # df = pd.DataFrame(json_data)
    # df2 = pd.Dataframe(df,index=df.unstack(level=0))
    # df2=df.pivot_table(index=['id']).reset_index()
    # df2 =pd.DataFrame(df.tolist(),index=['id'])
    # df2 = pd.DataFrame(df.tolist(),index=df.index).stack().unstack(0).reset_index(level=1,drop=True).rename_axis("id").reset_index()
    # df.to_csv(r'C:\Users\MelissaLu\OneDrive - Metrolinx\Desktop\IAM\json_fault_parsed.csv')

# URL = URLS["fault-history"]

# def fetch_all(
#     start_date: Optional[str] = None, unit_number: Optional[str] = None
# ) -> Generator[list, None, None]:
#     """
#     This function illustrates how to fetch data from Preteckt's Fault Code History
#     API, following paginated results.

#     It implements two of the available filters (from_time & unit_number), but also
#     illustrats how to set a desired number of results per page using the page_size
#     parameter.
#     """
#     # GET parameters for the API request. These correspont to the Filters available on the endpoint.
#     params = {"page_size": PAGE_SIZE}
#     if start_date is not None:
#         params["from_time"] = start_date
#     if unit_number is not None:
#         params["unit_number"] = unit_number

#     # HTTP headers
#     headers = {"Authorization": f"Token {AUTH_TOKEN}"}

#     # Fetch pages of content
#     next_page = URL
#     while next_page is not None:
#         resp = requests.get(URL, params=params, headers=headers,verify=False)
#         if resp.status_code == 200:
#             payload = resp.json()
#             next_page = payload["next"]
#             print(f"Got {len(payload['results'])} items. Next: {next_page}")
#             yield payload["results"]
#         else:
#             print(f"Got {resp.status_code}... trying again in 5s.")
#             time.sleep(5)


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(
#         description="This script allows you to fetch Fault Code History from the Preteckt API"
#     )
#     parser.add_argument("-s", "--start-date", type=str, help="Starting Date")
#     parser.add_argument(
#         "-u",
#         "--unit-number",
#         type=str,
#         help="The Unit number for the device installed in a vehicle",
#     )
#     args = parser.parse_args()

#     # fetch_all will return a list of results per page;
#     # we can use itertools.chain to flatten that into a single list of results.
#     results = list(
#         itertools.chain(
#             *fetch_all(start_date=args.start_date, unit_number=args.unit_number)
#         )
#     )
#     print(f"Got {len(results)} total results.")
