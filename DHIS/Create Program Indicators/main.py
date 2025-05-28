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

url = "https://xxxxx.xxxxx.co.ke/api/29/programIndicators"


data_to_create = [
  {
    "Inidicator_Name": "NTD - Primary Rk39 Positive Female",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "1" && #{k7U9lO69hVm.z0pyJKadFIV} == "1" && A{CcCaXXa1WBy} == "Op_Gender_Female"'
  },
  {
    "Inidicator_Name": "NTD - Primary Dat Negative Female",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "1" && #{k7U9lO69hVm.zZ4xphv4pEA} == "2" && A{CcCaXXa1WBy} == "Op_Gender_Female"'
  },
  {
    "Inidicator_Name": "NTD - Primary Aspirate Positive Female",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "1" && #{k7U9lO69hVm.RjNdkEgEHzO} == "Negative" && A{CcCaXXa1WBy} == "Op_Gender_Female"'
  },
  {
    "Inidicator_Name": "NTD - Primary Rk39 Negative Female",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "1" && #{k7U9lO69hVm.z0pyJKadFIV} == "2" && A{CcCaXXa1WBy} == "Op_Gender_Female"'
  },
  {
    "Inidicator_Name": "NTD - Primary Dat Positive Female",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "1" && #{k7U9lO69hVm.zZ4xphv4pEA} == "1" && A{CcCaXXa1WBy} == "Op_Gender_Female"'
  },
  {
    "Inidicator_Name": "NTD - Primary Aspirate Negative Female",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "1" && #{k7U9lO69hVm.RjNdkEgEHzO} == "Neg" && A{CcCaXXa1WBy} == "Op_Gender_Female"'
  },
  {
    "Inidicator_Name": "NTD - Primary Rk39 Positive Male",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "1" && #{k7U9lO69hVm.z0pyJKadFIV} == "1" && A{CcCaXXa1WBy} == "Op_Gender_Male"'
  },
  {
    "Inidicator_Name": "NTD - Primary Dat Negative Male",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "1" && #{k7U9lO69hVm.zZ4xphv4pEA} == "2" && A{CcCaXXa1WBy} == "Op_Gender_Male"'
  },
  {
    "Inidicator_Name": "NTD - Primary Aspirate Positive Male",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "1" && #{k7U9lO69hVm.RjNdkEgEHzO} == "Negative" && A{CcCaXXa1WBy} == "Op_Gender_Male"'
  },
  {
    "Inidicator_Name": "NTD - Primary Rk39 Negative Male",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "1" && #{k7U9lO69hVm.z0pyJKadFIV} == "2" && A{CcCaXXa1WBy} == "Op_Gender_Male"'
  },
  {
    "Inidicator_Name": "NTD - Primary Dat Positive Male",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "1" && #{k7U9lO69hVm.zZ4xphv4pEA} == "1" && A{CcCaXXa1WBy} == "Op_Gender_Male"'
  },
  {
    "Inidicator_Name": "NTD - Primary Aspirate Negative Male",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "1" && #{k7U9lO69hVm.RjNdkEgEHzO} == "Neg" && A{CcCaXXa1WBy} == "Op_Gender_Male"'
  },
  {
    "Inidicator_Name": "NTD - Relapse Aspirate Positive Female",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "2" && #{k7U9lO69hVm.RjNdkEgEHzO} == "Negative" && A{CcCaXXa1WBy} == "Op_Gender_Female"'
  },
  {
    "Inidicator_Name": "NTD - Relapse Aspirate Positive Male",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "2" && #{k7U9lO69hVm.RjNdkEgEHzO} == "Negative" && A{CcCaXXa1WBy} == "Op_Gender_Male"'
  },
  {
    "Inidicator_Name": "NTD - Relapse Aspirate Negative Female",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "2" && #{k7U9lO69hVm.RjNdkEgEHzO} == "Neg" && A{CcCaXXa1WBy} == "Op_Gender_Female"'
  },
  {
    "Inidicator_Name": "NTD - Relapse Aspirate Negative Male",
    "filter": '#{k7U9lO69hVm.D8rx2OvdV1M} == "2" && #{k7U9lO69hVm.RjNdkEgEHzO} == "Neg" && A{CcCaXXa1WBy} == "Op_Gender_Male"'
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
username = "xxxxxx"
password = "xxxxxx"

headers['Authorization'] = "Basic " + encodePassword(username, password)

i = 0
for data in data_to_create:
    try:
        pay_load["name"] = data["Inidicator_Name"]
        pay_load["filter"] = data["filter"]
        pay_load["shortName"] = data['Inidicator_Name']

        payload = json.dumps(pay_load)
        print(payload)
        print("_________--------------------------------------------------------")
        print(pay_load)

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        # breakpoint()
        if response.status_code == 200:
            i += 1
            print("Program Indicator created successfully.")
        else:
            print(f"Failed to create Program Indicator. Status code: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    print(f"Processed {i} indicators so far.")
        
    # break
