import pandas as pd
import requests
import io
import base64
import os
from datetime import datetime
import json

timenow = datetime.now().strftime("%Y-%m-%d %H:%M")

username = os.getenv("KHIS_USERNAME", "")
password = os.getenv("KHIS_PASSWORD", "")

print(f" Username: {username} - Password: {password}")
domain_name = "hiskenya.org"

post_systems = [
    {
        "name": "JPHES",
        "url": "jphesportal.uonbi.ac.ke",
        "username": "JPHES_USERNAME",
        "password": "JPHES_PASSWORD",
    }
    ,
    {
        "name": "PPMS",
        "url": "partnermanagementsystem.uonbi.ac.ke",
        "username": "ppms_username",
        "password": "ppms_password",
    }
    # ,
    # {
    #     "name": "Histracker",
    #     "url": "histracker.health.go.ke",
    #     "username": "tracker_username",
    #     "password": "tracker_password",
    # }
    # ,
    # {
    #     "name": "GBV",
    #     "url": "gbv.health.go.ke",
    #     "username": "GBV_USERNAME",
    #     "password": "GBV_PASSWORD",
    # }
    # ,
    # {
    #     "name": "Play Instance",
    #     "url": "play.im.dhis2.org/stable-2-40-5",
    #     "username": "",
    #     "password": "",
    # },
]


credentials = f"{username}:{password}"
auth_coded = base64.b64encode(credentials.encode()).decode("utf-8")


facilities = ['DU6DGtcP1dw','F0Cf9OoAo8T','pPrPliol4o1','dn2MyD4YMN1']
base_url = "https://hiskenya.org/api/29/organisationUnits/{}.json?fields=id,name,level,displayName,,phoneNumber,email,contactPerson,openingDate,parent[id,name,parent[name,id]],shortName,code,created,lastUpdated"

payload = {}
headers = {
    "Authorization": f"Basic {auth_coded}",
    "Cookie": "JSESSIONID=800106A351A3EEE49B4C6223AA7F4822",
}


def fetchFacility(facilityuid):
    url = base_url.format(facilityuid)
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    except Exception as e:
        print(f"Error fetching facility {facilityuid}, Error is : {e}")



base_create_url = "https://{}/api/organisationUnits"

# structure of system {"name":"","username": "","password": "", "url": ""}
def createFacility(system, payload_send):
    p_username = os.getenv(f"{system['username']}", "")
    p_password = os.getenv(f"{system['password']}", "")
    post_credentials = f"{p_username}:{p_password}"
    auth_coded_post = base64.b64encode(post_credentials.encode()).decode("utf-8")
    p_headers = {
        "Authorization": f"Basic {auth_coded_post}",
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'content-type': 'application/json',
        'Connection': 'keep-alive',
    }
    
    url = base_create_url.format(system['url'])
    print(f"{system['name']} Username: {p_username} - Password: {p_password}, url: {url}")
    
    
    try:
        resp = requests.post(url=url, data=json.dumps(payload_send), headers=p_headers)

        if resp.status_code == 200:
            print(f"Data posted Successfully")
            resp_json = resp.json()
            print(resp_json)
        else:
            print(f"Error: {resp.text}")
    except Exception as e:
        print(f"Error posting data to {system['name']}, Error is : {e}")

for facility in facilities:
    resp = fetchFacility(facility)
    if resp != None:
        print(resp)
        for post_system in post_systems:
            post_resp = createFacility(post_system, resp)
            print(f"Posted facility: {post_resp}")
            