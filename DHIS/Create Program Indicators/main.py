import requests
import json
import os
# This script creates a Program Indicator in DHIS2 using the provided API endpoint.
# Ensure you have the requests library installed: pip install requests
import base64

def encodePassword(username,password):
    cred_string = f"{username}:{password}"
    encoded_credentials = base64.b64encode(cred_string.encode('utf-8')).decode('utf-8')   
    print(f" Username & password : {cred_string} and endoded : {encoded_credentials}")

    headers = {
            "Authorization": f"Basic {encoded_credentials}"
        }
    return encoded_credentials

url = f"https://{os.getenv('HISTRACKER')}/api/29/programIndicators"
# url = "https://xxxxx.xxxxx.co.ke/api/29/programIndicators"


data_to_create = [
  {
    "shortname": "# imported cases Pre-SAC",
    "name": "NTD-VL - # imported cases Pre-SAC",
    "filter": '"#{k7U9lO69hVm.pZzDScBGl3X} == "1" && A{w58pAdWdsWW} == "<5"'
  },
  {
    "shortname": "# imported cases SAC",
    "name": "NTD-VL - # imported cases SAC",
    "filter": '"#{k7U9lO69hVm.pZzDScBGl3X} == "1" && A{w58pAdWdsWW} == ">=5" && A{w58pAdWdsWW} == "<=15"'
  },
  {
    "shortname": "# imported cases Adult",
    "name": "NTD-VL - # imported cases Adult",
    "filter": '"#{k7U9lO69hVm.pZzDScBGl3X} == "1" && A{w58pAdWdsWW} == ">15"'
  },
  {
    "shortname": "# imported cases Unspecified age",
    "name": "NTD-VL - # imported cases Unspecified age",
    "filter": '"#{k7U9lO69hVm.pZzDScBGl3X} == "1" && A{w58pAdWdsWW} == ""'
  },
  {
    "shortname": "# Primary VL patients Pre-SAC",
    "name": "NTD-VL - # Primary VL patients Pre-SAC",
    "filter": '"#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && A{w58pAdWdsWW} == "<5"'
  },
  {
    "shortname": "# Primary VL patients SAC",
    "name": "NTD-VL - # Primary VL patients SAC",
    "filter": '"#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && A{w58pAdWdsWW} == ">=5" && A{w58pAdWdsWW} == "<=15"'
  },
  {
    "shortname": "# Primary VL patients Adult",
    "name": "NTD-VL - # Primary VL patients Adult",
    "filter": '"#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && A{w58pAdWdsWW} == ">15"'
  },
  {
    "shortname": "# Primary VL patients Unspecified age",
    "name": "NTD-VL - # Primary VL patients Unspecified age",
    "filter": '"#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && A{w58pAdWdsWW} == ""'
  },
  {
    "shortname": "# Relapse patients Pre-SAC",
    "name": "NTD-VL - # Relapse patients Pre-SAC",
    "filter": '"#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && A{w58pAdWdsWW} == "<5"'
  },
  {
    "shortname": "# Relapse patients SAC",
    "name": "NTD-VL - # Relapse patients SAC",
    "filter": '"#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && A{w58pAdWdsWW} == ">=5" && A{w58pAdWdsWW} == "<=15"'
  },
  {
    "shortname": "# Relapse patients Adult",
    "name": "NTD-VL - # Relapse patients Adult",
    "filter": '"#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && A{w58pAdWdsWW} == ">15"'
  },
  {
    "shortname": "# Relapse patients Unspecified age",
    "name": "NTD-VL - # Relapse patients Unspecified age",
    "filter": '"#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && A{w58pAdWdsWW} == ""'
  },
  {
    "shortname": "# PKDL patients Pre-SAC",
    "name": "NTD-VL - # PKDL patients Pre-SAC",
    "filter": '"#{k7U9lO69hVm.Tlj4JRxaFbV} == "3" && A{w58pAdWdsWW} == "<5"'
  },
  {
    "shortname": "# PKDL patients SAC",
    "name": "NTD-VL - # PKDL patients SAC",
    "filter": '"#{k7U9lO69hVm.Tlj4JRxaFbV} == "3" && A{w58pAdWdsWW} == ">=5" && A{w58pAdWdsWW} == "<=15"'
  },
  {
    "shortname": "# PKDL patients Adult",
    "name": "NTD-VL - # PKDL patients Adult",
    "filter": '"#{k7U9lO69hVm.Tlj4JRxaFbV} == "3" && A{w58pAdWdsWW} == ">15"'
  },
  {
    "shortname": "# PKDL patients Unspecified age",
    "name": "NTD-VL - # PKDL patients Unspecified age",
    "filter": '"#{k7U9lO69hVm.Tlj4JRxaFbV} == "3" && A{w58pAdWdsWW} == ""'
  },
  {
    "shortname": "Treatment failures Primary, SSG+PM",
    "name": "NTD-VL - Treatment failures Primary, SSG+PM",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2"'
  },
  {
    "shortname": "Treatment failures Primary, SSG only",
    "name": "NTD-VL - Treatment failures Primary, SSG only",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "3"'
  },
  {
    "shortname": "Treatment failures Primary, Ambisome",
    "name": "NTD-VL - Treatment failures Primary, Ambisome",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "5"'
  },
  {
    "shortname": "Treatment failures Primary, Ambisome + Miltefosine",
    "name": "NTD-VL - Treatment failures Primary, Ambisome + Miltefosine",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "1"'
  },
  {
    "shortname": "Treatment failures Primary, Other",
    "name": "NTD-VL - Treatment failures Primary, Other",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "6" && #{YAqgg6142Nn.Jjv8uLxHS80} == "8" && #{YAqgg6142Nn.Jjv8uLxHS80} == "10"'
  },
  {
    "shortname": "Treatment failures Relapse, SSG+PM",
    "name": "NTD-VL - Treatment failures Relapse, SSG+PM",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2"'
  },
  {
    "shortname": "Treatment failures Relapse, SSG only",
    "name": "NTD-VL - Treatment failures Relapse, SSG only",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "3"'
  },
  {
    "shortname": "Treatment failures Relapse, Ambisome",
    "name": "NTD-VL - Treatment failures Relapse, Ambisome",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "5"'
  },
  {
    "shortname": "Treatment failures Relapse, Ambisome + Miltefosine",
    "name": "NTD-VL - Treatment failures Relapse, Ambisome + Miltefosine",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "1"'
  },
  {
    "shortname": "Treatment failures Relapse, Other",
    "name": "NTD-VL - Treatment failures Relapse, Other",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "6" && #{YAqgg6142Nn.Jjv8uLxHS80} == "8" && #{YAqgg6142Nn.Jjv8uLxHS80} == "10"'
  },
  {
    "shortname": "Treatment failures PKDL, SSG+PM",
    "name": "NTD-VL - Treatment failures PKDL, SSG+PM",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "3" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2"'
  },
  {
    "shortname": "Treatment failures PKDL, SSG only",
    "name": "NTD-VL - Treatment failures PKDL, SSG only",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "3" && #{YAqgg6142Nn.Jjv8uLxHS80} == "3"'
  },
  {
    "shortname": "Treatment failures PKDL, Ambisome",
    "name": "NTD-VL - Treatment failures PKDL, Ambisome",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "3" && #{YAqgg6142Nn.Jjv8uLxHS80} == "5"'
  },
  {
    "shortname": "Treatment failures PKDL, Ambisome + Miltefosine",
    "name": "NTD-VL - Treatment failures PKDL, Ambisome + Miltefosine",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "3" && #{YAqgg6142Nn.Jjv8uLxHS80} == "1"'
  },
  {
    "shortname": "Treatment failures PKDL, Other",
    "name": "NTD-VL - Treatment failures PKDL, Other",
    "filter": '"(#{YAqgg6142Nn.BIzredhqtbr} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "3" && #{k7U9lO69hVm.Tlj4JRxaFbV} == "3" && #{YAqgg6142Nn.Jjv8uLxHS80} == "6" && #{YAqgg6142Nn.Jjv8uLxHS80} == "8" && #{YAqgg6142Nn.Jjv8uLxHS80} == "10"'
  }
]


pay_load = {
  "aggregationType": "COUNT",
  "publicAccess": "rw------",
  "lastUpdated": "2025-02-21T11:27:33.748",
  "expression": "1",
  "filter": "",
  "name": "",
  "analyticsType": "ENROLLMENT",
  "shortName": "",
  "program": {
    "id": "tYDQn4Gb0Ij"
  },
  "analyticsPeriodBoundaries": [
    {
      "lastUpdated": "2025-02-21T11:27:33.750",
      "created": "2025-02-21T11:27:33.750",
      "externalAccess": False,
      "analyticsPeriodBoundaryType": "BEFORE_END_OF_REPORTING_PERIOD",
      "boundaryTarget": "ENROLLMENT_DATE",
      "favorite": False,
      "offsetPeriods": 0,
      "access": {
        "read": True,
        "update": True,
        "externalize": True,
        "delete": True,
        "write": True,
        "manage": True
      },
    },
    {
      "lastUpdated": "2025-02-21T11:27:33.750",
      "created": "2025-02-21T11:27:33.750",
      "externalAccess": False,
      "analyticsPeriodBoundaryType": "AFTER_START_OF_REPORTING_PERIOD",
      "boundaryTarget": "ENROLLMENT_DATE",
      "favorite": False,
      "offsetPeriods": 0,
      "access": {
        "read": True,
        "update": True,
        "externalize": True,
        "delete": True,
        "write": True,
        "manage": True
      }
    }
  ]
}



headers = {  
  'Content-Type': 'application/json',
    'Accept': '*/*',
    'Accept-Language': 'en,en-US;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://histracker.health.go.ke/dhis-web-maintenance/index.html',
    'content-type': 'application/json',
    'Origin': 'https://histracker.health.go.ke',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
    'TE': 'Trailers',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    # 'Authorization': 'Bearer '
}

# Replace with your actual username and password
username = os.getenv("HISTRACKER_USERNAME", "")
password = os.getenv("HISTRACKER_PASSWORD", "")

if not username or not password:
    print("Username and password must be set in environment variables HISTRACKER_USERNAME and HISTRACKER_PASSWORD.")
    raise ValueError("Username and password must be set in environment variables HISTRACKER_USERNAME and HISTRACKER_PASSWORD.")
    
headers['Authorization'] = "Basic " + encodePassword(username, password)

i = 0
for data in data_to_create:
    # urls=url + f"/{data['uid']}"
    try:
      # fetch data using the urls and update the fetched payload
      # Uncomment if you want to update the indicators
        """
          response = requests.get(urls, headers=headers)
          if response.status_code != 200:
              print(f"Failed to fetch data for {data['name']}. Status code: {response.status_code}")
              continue
          fetched_data = response.json()
        """
          
        fetched_data = pay_load.copy()  # Create a copy of the payload to modify
        
        fetched_data["name"] = data["name"]
        fetched_data["filter"] = data["filter"]
        fetched_data["shortName"] = data['shortname']
        # Uncomment if you want to update the indicators
        # fetched_data["id"] = data['uid']

        payload = json.dumps(fetched_data)
        print(payload)
        print("_________--------------------------------------------------------")
        print(fetched_data)

        response = requests.request("POST", url, headers=headers, data=payload)
        
        # Uncomment if you want to update the indicators
        # response = requests.request("PUT", urls, headers=headers, data=payload)

        print(response.text)
        # breakpoint()
        if response.status_code == 201 or response.status_code == 200:
            i += 1
            print("Program Indicator created successfully.")
        else:
            print(f"Failed to create Program Indicator. Status code: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    print(f"Processed {i} indicators so far.")
        
    # break
