import requests
import json
import base64
import os
from datetime import datetime

khis_username = os.getenv("KHIS_USERNAME")
khis_password = os.getenv("KHIS_PASSWORD")

khis_credentials = khis_username + ":" + khis_password

khis_encoded_credentials = base64.b64encode(khis_credentials.encode("utf-8")).decode(
    "utf-8"
)

jphes_username = os.getenv("JPHES_USERNAME")
jphes_password = os.getenv("JPHES_PASSWORD")
jphes_credentials = jphes_username + ":" + jphes_password

jphes_encoded_credentials = base64.b64encode(jphes_credentials.encode("utf-8")).decode(
    "utf-8"
)

# url = "https://hiskenya.org/api/dataValueSets?dataElementIdScheme=UID&orgUnitIdScheme=UID&idScheme=UID&includeDeleted=false&children=true&startDate=2024-07-24&endDate=2024-10-24&orgUnit=HfVjCurKxh2&dataSet=EnZokILHOeN&format=json&attachment=dataValueSets.json"


datasets = [
    {
        "id": "EnZokILHOeN",
        "name": "MOH 705 A Outpatient summary < 5 years Revised 2020",
    },
    {"id": "XoHnrLBL1qB", "name": "MOH 710 Vaccines and Immunisation Rev 2020"},
    {
        "id": "UpS2bTVcClZ",
        "name": "MOH 711 Integrated Summary Report",
    },  #: Reproductive & Child Health, Medical & Rehabilitation Services Rev 2020
]


periods = [
    {
        "periodid": 87628028,
        "periodtypeid": 5,
        "startdate": "2023-10-01",
        "enddate": "2023-10-31",
        "name": "Monthly",
        "monthid": 202310,
    },
    {
        "periodid": 87796297,
        "periodtypeid": 5,
        "startdate": "2023-11-01",
        "enddate": "2023-11-30",
        "name": "Monthly",
        "monthid": 202311,
    },
    {
        "periodid": 86614638,
        "periodtypeid": 5,
        "startdate": "2023-12-01",
        "enddate": "2023-12-31",
        "name": "Monthly",
        "monthid": 202312,
    },
    {
        "periodid": 88972558,
        "periodtypeid": 5,
        "startdate": "2024-01-01",
        "enddate": "2024-01-31",
        "name": "Monthly",
        "monthid": 202401,
    },
    {
        "periodid": 89384134,
        "periodtypeid": 5,
        "startdate": "2024-02-01",
        "enddate": "2024-02-29",
        "name": "Monthly",
        "monthid": 202402,
    },
    {
        "periodid": 89021774,
        "periodtypeid": 5,
        "startdate": "2024-03-01",
        "enddate": "2024-03-31",
        "name": "Monthly",
        "monthid": 202403,
    },
    {
        "periodid": 89088839,
        "periodtypeid": 5,
        "startdate": "2024-04-01",
        "enddate": "2024-04-30",
        "name": "Monthly",
        "monthid": 202404,
    },
    {
        "periodid": 89235379,
        "periodtypeid": 5,
        "startdate": "2024-05-01",
        "enddate": "2024-05-31",
        "name": "Monthly",
        "monthid": 202405,
    },
    {
        "periodid": 89379301,
        "periodtypeid": 5,
        "startdate": "2024-06-01",
        "enddate": "2024-06-30",
        "name": "Monthly",
        "monthid": 202406,
    },
    {
        "periodid": 89589792,
        "periodtypeid": 5,
        "startdate": "2024-08-01",
        "enddate": "2024-08-31",
        "name": "Monthly",
        "monthid": 202408,
    },
    {
        "periodid": "",
        "periodtypeid": 5,
        "startdate": "2024-09-01",
        "enddate": "2024-09-30",
        "name": "Monthly",
        "monthid": 202409,
    },
]
urls = "https://hiskenya.org/api/dataValueSets?dataElementIdScheme=UID&orgUnitIdScheme=UID&idScheme=UID&includeDeleted=false&children=true&startDate={}&endDate={}&orgUnit=HfVjCurKxh2&dataSet={}&format=json&attachment=dataValueSets.json"


def getKHISdata(startDate, endDate, dataSet):
    url = urls.format(startDate, endDate, dataSet)
    payload = {}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {khis_encoded_credentials}",
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        print(" response fetch req: ")
        print(response)
        if response.status_code < 300:
            return response.json()
        else:
            return []
    except Exception as e:
        print(f"Error posting data: {e}")


def senddataToJphes(data):
    url = "https://jphesportal.uonbi.ac.ke/api/dataValueSets?orgUnitIdScheme=code"
    print(f"Data being Posyed {data['dataValues'][0]}")

    payload = json.dumps(data)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {jphes_encoded_credentials}",
        "Accept": "*/*",
        "Accept-Language": "en,en-US;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Cookie": "JSESSIONID=B4C5226F366CCA42E45D57FB428D671E",
    }
    try:
        response = requests.request(
            "POST", url, headers=headers, data=payload, verify=False
        )
        print(f" Send response: {response}")
        if response.status_code == 200:
            return response
        else:
            return []
        
    except Exception as e:
        print(f"Error posting data: {e}")


def editData(data):
    for dat in data["dataValues"]:
        if dat["categoryOptionCombo"] == "NhSoXUMPK2K":
            dat["categoryOptionCombo"] = ""
        if dat["attributeOptionCombo"] == "NhSoXUMPK2K":
            dat["attributeOptionCombo"] = ""
    print(f" length of Edited data {len(data['dataValues'])}")
    return data


def split_and_send(data, chunk_size=1000):
    # Assuming data is in the format {'values': [...]}
    records = data['dataValues']
    total_records = len(records)

    for i in range(0, total_records, chunk_size):
        chunk = records[i:i + chunk_size]
        chunk_data = {'dataValues': chunk}

        # Optionally, you can edit the chunk data if needed
        postData = editData(chunk_data)

        # Send the chunk
        postDataResponse = senddataToJphes(postData)
        
        print(postDataResponse)
        return postDataResponse.json()

        # Check response and handle any potential errors
        # if postDataResponse.status_code != 200:
        #     print(f"Error sending chunk {i // chunk_size + 1}: {postDataResponse.text}")
        # else:
        #     print(f"Successfully sent chunk {i // chunk_size + 1}")


for dataset in datasets:
    for period in periods:
        print(
            "Start Data Fetch: "
            + datetime.now().time().strftime("%H:%M:%S")
            + "\nDataset Name: "
            + dataset["name"]
            + "\nPeriod: "
            + str(period["monthid"])
        )
        dataFetched = getKHISdata(period["startdate"], period["enddate"], dataset["id"])
        print("End Data Fetch: " + datetime.now().time().strftime("%H:%M:%S"))
        print(f" length of data {len(dataFetched['dataValues'])}")
        if len(dataFetched) > 0:
            print("Start Data Send: " + datetime.now().time().strftime("%H:%M:%S"))
            postData = editData(dataFetched)
            postDataResponse = split_and_send(postData, 200)
            # print(f"Post Response {postData}")
            print("End Data Send: " + datetime.now().time().strftime("%H:%M:%S"))
        # break
