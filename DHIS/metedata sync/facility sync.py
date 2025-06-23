import pandas as pd
import requests
import io
import base64
import os
from datetime import datetime
import json
import certifi

timenow = datetime.now().strftime("%Y-%m-%d %H:%M")

# username = os.getenv("KHIS_USERNAME", "")
# password = os.getenv("KHIS_PASSWORD", "")


username = os.getenv("KHIS_USERNAME", "")
password = os.getenv("KHIS_PASSWORD", "")



print(f" Username: {username} - Password: {password}")
domain_name = "hiskenya.org"

post_systems = [
    # {
    #     "name": "JPHES",
    #     "url": "jphesportal.uonbi.ac.ke",
    #     "username": "JPHES_USERNAME",
    #     "password": "JPHES_PASSWORD",
    # }
    # ,
    # {
    #     "name": "PPMS",
    #     "url": "partnermanagementsystem.uonbi.ac.ke",
    #     "username": "ppms_username",
    #     "password": "ppms_password",
    # }
    # ,
    {
        "name": "Histracker",
        "url": "histracker.health.go.ke",
        "username": "",
        "password": "",
    }
    # ,
    # {
    #     "name": "GBV",
    #     "url": "gbv.health.go.ke",
    #     "username": "GBV_USERNAME",
    #     "password": "GBV_PASSWORD",
    # }
    # ,
    # {
    #     "name": "Entomology Database",
    #     "url": "ento.uonbi.ac.ke",
    #     "username": "Ento_user",
    #     "password": "Ento_password",
    # }
    # ,
    # {
    #     "name": "Bush",
    #     "url": "43.205.46.180:8080",
    #     "username": "admin",
    #     "password": "district",
    # },
    # {
    #     "name": "EBSME",
    #     "url": "dhis.atsl.co.ke",
    #     "username": "admin",
    #     "password": "123456@Ab",
    # },
]


credentials = f"{username}:{password}" 
auth_coded = base64.b64encode(credentials.encode()).decode("utf-8")

credentials_2 = ":" 
auth_coded_2 = base64.b64encode(credentials_2.encode()).decode("utf-8")


def fetchNewFacilities():
    pass


facilities = ["HfVjCurKxh2"]

# facilities = fetchNewFacilities()
base_url = "https://hiskenya.org/api/29/organisationUnits/{}.json?fields=id,name,displayName,coordinates,phoneNumber,email,contactPerson,openingDate,parent[id,name,parent[name,id]],shortName,code,created,lastUpdated,geometry,level"

base_url_2 = "https://histracker.health.go.ke/api/organisationUnits/{}.json"

# base_url = "https://test.hiskenya.org/api/29/organisationUnits/{}.json?fields=id,name,level,displayName,coordinates,phoneNumber,email,contactPerson,openingDate,parent[id,name,parent[name,id]],shortName,code,created,lastUpdated"

payload = {}
headers = {
    "Authorization": f"Basic {auth_coded}",
    "Cookie": "JSESSIONID=800106A351A3EEE49B4C6223AA7F4822",
}

headers_2 = {
    "Authorization": f"Basic {auth_coded_2}",
    "Cookie": "JSESSIONID=800106A351A3EEE49B4C6223AA7F4822",
}


def fetchFacility(facilityuid):
    url = base_url.format(facilityuid)
    print(f"Fetching facility {facilityuid} from {url}")
    payload = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        print(f"Response status code: {response}")
        if response.status_code == 200 or response.status_code == 201:
            print(f"Fetched facility {facilityuid} successfully")
            return response.json()
        else:
            return None

    except Exception as e:
        print(f"Error fetching facility {facilityuid}, Error is : {e}")
        
def fetchFacility_2(facilityuid):
    url_2 = base_url_2.format(facilityuid)
    print(f"Fetching facility {facilityuid} from {url_2}")
    payload = {}
    try:
        # breakpoint()
        response = requests.request("GET", url_2, headers=headers_2, data=payload)
        print(f"Response status code: {response}")
        if response.status_code == 200 or response.status_code == 201:
            print(f"Fetched facility {facilityuid} successfully")
            return response.json()
        else:
            return None

    except Exception as e:
        print(f"Error fetching facility in fetchFacility_2 {facilityuid}, Error is : {e}")


base_create_url = "https://{}/api/29/organisationUnits"

update_base_create_url = "https://{}/api/organisationUnits/{}"


# structure of system {"name":"","username": "","password": "", "url": ""}
def createFacility(system, payload_send, current_payload):
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
    }

    url = base_create_url.format(system["url"])
    print(f"Data being sent before edit: {payload_send}")
    update_url = update_base_create_url.format(system['url'],payload_send['id'])
    print(f"current_payload: {current_payload}")
    print(f"update url: {update_url}")

    # modify payload dates
    if current_payload is not None and payload_send is not None:
        current_payload["geometry"] = payload_send["geometry"]
    else:
        print(f"current_payload: {current_payload is None} or payload_send: {payload is None}, skipping geometry update")
        exit(1)
    # payload_send["lastUpdated"] = payload_send["lastUpdated"].split("T")[0]
    # payload_send["created"] = payload_send["created"].split("T")[0]

    print(
        f"{system['name']} Username: {p_username} - Password: {p_password}, url: {update_url}, encoded _password: {auth_coded_post}"
    )

    print(f"Data being sent: {payload_send}")

    try:
        # Always change the line below to post or put
        # resp = requests.post(
        #     url=url, data=json.dumps(payload_send), headers=p_headers, verify=False
        # )
        # if the org is in system, make an update
        # if resp.status_code == 409:
        #     print(f"Conflict detected, trying to update {system['name']} facility")
        resp = requests.put(url=update_url, data=json.dumps(payload_send), headers=p_headers, verify=False)
        print(f"Response status code: {resp.text}")
        # breakpoint()
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
    current_payload = fetchFacility_2(facility)
    if resp != None:
        for post_system in post_systems:
            post_resp = createFacility(post_system, resp, current_payload)
            print(f"Posted facility: {post_resp}")
    else:
        print(f"Facility {facility} not found or could not be fetched.")
        
    # break
