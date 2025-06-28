import requests
import json
import os
import pandas as pd
import base64

def encodePassword(username,password):
    cred_string = f"{username}:{password}"
    encoded_credentials = base64.b64encode(cred_string.encode('utf-8')).decode('utf-8')   
    print(f" Username & password : {cred_string} and endoded : {encoded_credentials}")

    headers = {
            "Authorization": f"Basic {encoded_credentials}"
        }
    return encoded_credentials



# Fetching credentials from environment variables
sys_1_url = os.environ.get("HISTRACKER")
sys_1_username = os.environ.get("HISTRACKER_USERNAME")
sys_1_password = os.environ.get("HISTRACKER_PASSWORD")


sys_2_url = os.environ.get("KHIS")
sys_2_username = os.environ.get("KHIS_USERNAME")
sys_2_password = os.environ.get("KHIS_PASSWORD")

sys_1_encoded = encodePassword(sys_1_username, sys_1_password)
sys_2_encoded = encodePassword(sys_2_username, sys_2_password)

orgunitgroupid = "bWGLt3Soqkm"



def fetch_org_unit_groups(orgunitgroup_id):
    url = f"https://{sys_1_url}/api/organisationUnitGroups/{orgunitgroup_id}.json?fields=id,name,displayName,shortName,organisationUnits[id,name,code]"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {sys_1_encoded}"
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        # print(f"Fetched {data} organisation unit groups from {sys_1_url}")
        response.raise_for_status()  # Raise an error for bad responses
        return data
    except Exception as e:
        print(f"Error fetching organisation unit groups: {e}")
        return None
    
    


def create_org_unit_group():
    url = f"https://{sys_2_url}/api/organisationUnitGroups.json"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {sys_2_encoded}"
    }
    groupData = fetch_org_unit_groups(orgunitgroupid)
    data = {
        "organisationUnitGroup": {
            "id": groupData.get('id', ''),
            "name": groupData.get('name', ''),
            "shortName": groupData.get('shortName', ''),
            "displayName": groupData.get('displayName', ''),
            # "dataDimension": groupData.get('dataDimension', False),
            # "compulsory": True,
            "organisationUnits": groupData.get('organisationUnits', []),
        }
    }
    payload = data
    print(f"Payload to be sent: {payload}")
    try:
        response = requests.post(url, headers=headers, json=groupData)
        print("-------------------__________________--------------------")
        print(f"Creating organisation unit group with data: {data}")
        response.raise_for_status()  # Raise an error for bad responses
        print(f"Successfully created organisation unit group: {response.json()}")
    except Exception as e:
        print(f"Error creating organisation unit group: {e}")
        
        
if __name__ == "__main__":
    create_org_unit_group()
    print("Script executed successfully.")