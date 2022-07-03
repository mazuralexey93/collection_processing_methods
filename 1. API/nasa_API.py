# 6q8xxm0h9YsNKMGHeEFBNsXdWLcai3IUhIEY6ltX

"""
One of the most popular websites at NASA is the Astronomy Picture of the Day.
This endpoint structures the APOD imagery and associated metadata so that it can be repurposed for other applications.
"""
import os
import requests
import json
from pprint import pprint

url = 'https://api.nasa.gov/planetary/apod'

params = {
    # 'date': '2022-05-01',       # The date of the APOD image to retrieve
    'start_date': '2022-06-01',   # The start of a date range. Cannot be used with date.
    'end_date': '2022-07-01',     # The end of the date range, when used with start_date.
    'api_key': os.environ['api_key'],

}

response = requests.get(url=url, params=params)
j_data = response.json()
pprint(j_data)

with open('nasa.json', 'w') as outfile:
    json.dump(j_data, outfile, indent=2)
