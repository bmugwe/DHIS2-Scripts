import os
import base64

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def encodePassword(username, password):
    cred_string = f"{username}:{password}"
    return base64.b64encode(cred_string.encode("utf-8")).decode("utf-8")


khis_username = os.environ.get('KHIS_USERNAME')
khis_password = os.environ.get('KHIS_PASSWORD')

if not khis_username or not khis_password:
    raise ValueError("KHIS_USERNAME and KHIS_PASSWORD environment variables must be set.")

credentials = encodePassword(khis_username, khis_password)

url = "https://hiskenya.dha.go.ke/api/29/indicators"

# Retry failures that happen while establishing the connection (including the
# TLS reset in the traceback). Read retries are disabled because retrying a POST
# after the server has received it could create a duplicate indicator.
retry_policy = Retry(
    total=3,
    connect=3,
    read=0,
    status=0,
    other=3,
    backoff_factor=1,
    allowed_methods={"POST"},
)
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retry_policy))

df = pd.read_excel('indicators.xlsx', sheet_name='sheet')


def create_indicator(name, short_name, quantity_used, physical_count):
    payload = {
        "denominatorDescription": "one",
        "numeratorDescription": "(Quantity Used*4) - Physical count",
        "numerator": f"(#{{{quantity_used}}})*4-#{{{physical_count}}}",
        "denominator": "1",
        "name": f"{name}",
        "shortName": f"{short_name}",
        "indicatorType": {"id": "RoofAsu1276"},
        "legendSets": [],
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:153.0) Gecko/20100101 Firefox/153.0',
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'content-type': 'application/json',
        'Origin': 'https://hiskenya.dha.go.ke',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Priority': 'u=4',
        'TE': 'trailers',
        'Authorization': f'Basic {credentials}'
    }

    response = session.post(
        url,
        headers=headers,
        json=payload,
        timeout=(15, 60),
    )
    response.raise_for_status()
    return response


if df.empty:
    print("The DataFrame is empty. No indicators to create.")
else:
    for index, row in df.iterrows():
        name = row['name']
        short_name = row['shortName']
        quantity_used = row['quantity_used']
        physical_count = row['physical_count']
        try:
            response = create_indicator(name, short_name, quantity_used, physical_count)
            # breakpoint()  # Set a breakpoint here to inspect the response if needed
        except requests.RequestException as exc:
            print(f"Failed to create indicator {name!r}: {exc}")
            # breakpoint()
            break

        print(f"Created indicator {name!r}: HTTP {response.status_code}")
        # break
