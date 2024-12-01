import pandas as pd
import requests
import io
import base64
import os
from datetime import datetime
import json
import certifi

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
    # ,
    # {
    #     "name": "PPMS",
    #     "url": "partnermanagementsystem.uonbi.ac.ke",
    #     "username": "ppms_username",
    #     "password": "ppms_password",
    # }
    # ,
    # {
    #     "name": "Histracker",
    #     "url": "histracker.health.go.ke",
    #     "username": "Tracker_username",
    #     "password": "Tracker_password",
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


def fetchNewFacilities():
    pass


facilities = [
   'TCdh15iUFXg',
'PEb8BZW2ziu',
'BDuZCU59CxZ',
'is8Ufsq3KGl',
'prE5hsoV8H6',
'lmR9ogNtSEc',
'UlRf4kjQmSx',
'fBecBcyGAzh',
'ildgwkoH4Ao',
'pMXH6YIN9RO',
'FIcdZgZRBEN',
'BCaEfrQW9LL',
'TBA5r7aCUN5',
'QxwoBAZjFtC',
'UaVCwwsTtPy',
'N9Np8tQvoG2',
'zdqrcIoHhzb',
'eUaWT4B0dhy',
'mlHL2HP7LD0',
'czTiQzpJBm0',
'rSbnOkxQ4Qq',
'K0Kj5Y0NQwO',
'QLUqB0z21XE',
'UdVgB8pVaKd',
'VQ7GShr4P1l',
'GUowNhmKNvt',
'kov4giRgD4e',
'NkDiME62bAG',
'grlyT4w5ZSG',
'JUBPnE7M0he',
'gqxrvUoLoOo',
'VZQhOoop4Ot',
'HZNucg3esnL',
'c2RfQcsfAEL',
'Z0KyOqEohxa',
's3ly3dAGBf1',
'gbkBDAbFArf',
'ZYoasZOy2YF',
'fcIgUtcR8Nm',
'tryqC8rqyAN'
]

# facilities = fetchNewFacilities()
base_url = "https://hiskenya.org/api/29/organisationUnits/{}.json?fields=id,name,level,displayName,coordinates,phoneNumber,email,contactPerson,openingDate,parent[id,name,parent[name,id]],shortName,code,created,lastUpdated"

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

update_base_create_url = "https://{}/api/organisationUnits/{}"


# structure of system {"name":"","username": "","password": "", "url": ""}
def createFacility(system, payload_send):
    p_username = os.getenv(f"{system['username']}", "")
    p_password = os.getenv(f"{system['password']}", "")
    post_credentials = f"{p_username}:{p_password}"
    auth_coded_post = base64.b64encode(post_credentials.encode()).decode("utf-8")
    p_headers = {
        "Authorization": f"Basic {auth_coded_post}",
        "Accept": "*/*",
        "Accept-Language": "en,en-US;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Cookie": "JSESSIONID=B4C5226F366CCA42E45D57FB428D671E",
    }

    url = base_create_url.format(system["url"])
    # print(f"Data being sent before edit: {payload_send}")
    # url = update_base_create_url.format(system['url'],payload_send['id'])

    # modify payload dates
    payload_send["openingDate"] = payload_send["openingDate"].split("T")[0]
    payload_send["lastUpdated"] = payload_send["lastUpdated"].split("T")[0]
    payload_send["created"] = payload_send["created"].split("T")[0]

    print(
        f"{system['name']} Username: {p_username} - Password: {p_password}, url: {url}, encoded _password: {auth_coded_post}"
    )

    print(f"Data being sent: {payload_send}")

    try:
        # Always change the line below to post or put
        resp = requests.post(
            url=url, data=json.dumps(payload_send), headers=p_headers, verify=False
        )

        # resp = requests.put(url=url, data=json.dumps(payload_send), headers=p_headers, verify=False)

        if resp.status_code == 200 or resp.status_code == 201:
            print(f"Data posted Successfully")
            resp_json = resp.json()
            return resp_json
        else:
            print(f"Error: {resp.text}")
            return {"msg": "Error"}
    except Exception as e:
        print(f"Error posting data to {system['name']}, Error is : {e}")


for facility in facilities:
    resp = fetchFacility(facility)
    if resp != None:
        for post_system in post_systems:
            post_resp = createFacility(post_system, resp)
            print(f"Posted facility: {post_resp}")
        # if (post_resp['msg']=="Error"):
        #     break
