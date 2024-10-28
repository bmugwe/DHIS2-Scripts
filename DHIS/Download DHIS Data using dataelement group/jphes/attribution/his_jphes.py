import requests
import json
import base64
import os
from datetime import datetime

# Environment Variables
khis_username = os.getenv("KHIS_USERNAME")
khis_password = os.getenv("KHIS_PASSWORD")
jphes_username = os.getenv("JPHES_USERNAME")
jphes_password = os.getenv("JPHES_PASSWORD")

# Encode credentials
def encode_credentials(username, password):
    credentials = f"{username}:{password}"
    return base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

khis_encoded_credentials = encode_credentials(khis_username, khis_password)
jphes_encoded_credentials = encode_credentials(jphes_username, jphes_password)

# Datasets and periods
datasets = [
    # {"id": "EnZokILHOeN", "name": "MOH 705 A Outpatient summary < 5 years Revised 2020"},
    {"id": "XoHnrLBL1qB", "name": "MOH 710 Vaccines and Immunisation Rev 2020"},
    {"id": "UpS2bTVcClZ", "name": "MOH 711 Integrated Summary Report"},
]

periods = [
    {"periodid": 87628028, "startdate": "2023-10-01", "enddate": "2023-10-31", "monthid": 202310},
    {"periodid": 87796297, "startdate": "2023-11-01", "enddate": "2023-11-30", "monthid": 202311},
    {"periodid": 86614638, "startdate": "2023-12-01", "enddate": "2023-12-31", "monthid": 202312},
    {"periodid": 88972558, "startdate": "2024-01-01", "enddate": "2024-01-31", "monthid": 202401},
    {"periodid": 89384134, "startdate": "2024-02-01", "enddate": "2024-02-29", "monthid": 202402},
    {"periodid": 89021774, "startdate": "2024-03-01", "enddate": "2024-03-31", "monthid": 202403},
    {"periodid": 89088839, "startdate": "2024-04-01", "enddate": "2024-04-30", "monthid": 202404},
    {"periodid": 89235379, "startdate": "2024-05-01", "enddate": "2024-05-31", "monthid": 202405},
    {"periodid": 89379301, "startdate": "2024-06-01", "enddate": "2024-06-30", "monthid": 202406},
    {"periodid": 89589792, "startdate": "2024-08-01", "enddate": "2024-08-31", "monthid": 202408},
    {"periodid": "", "startdate": "2024-09-01", "enddate": "2024-09-30", "monthid": 202409},
]

url_template = "https://hiskenya.org/api/dataValueSets?dataElementIdScheme=UID&orgUnitIdScheme=UID&idScheme=UID&includeDeleted=false&children=true&startDate={}&endDate={}&orgUnit=HfVjCurKxh2&dataSet={}&format=json&attachment=dataValueSets.json"

def get_khis_data(start_date, end_date, data_set):
    url = url_template.format(start_date, end_date, data_set)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {khis_encoded_credentials}",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching KHIS data: {e}")
        return []

def send_data_to_jphes(data):
    url = "https://jphesportal.uonbi.ac.ke/api/dataValueSets?orgUnitIdScheme=code"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {jphes_encoded_credentials}",
        "Accept": "application/json",
    }
    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()  # Raise an error for bad responses
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error posting data to JPHES: {e}")
        return []

def edit_data(data):
    for dat in data["dataValues"]:
        if dat["categoryOptionCombo"] == "NhSoXUMPK2K":
            dat["categoryOptionCombo"] = ""
        if dat["attributeOptionCombo"] == "NhSoXUMPK2K":
            dat["attributeOptionCombo"] = ""
    return data

def split_and_send(data, chunk_size=1000):
    records = data['dataValues']
    total_records = len(records)

    for i in range(0, total_records, chunk_size):
        chunk = records[i:i + chunk_size]
        chunk_data = {'dataValues': chunk}
        post_data = edit_data(chunk_data)
        response = send_data_to_jphes(post_data)

        if response:
            print(f"Successfully sent chunk {i // chunk_size + 1}: {response.status_code}")
        else:
            print(f"Failed to send chunk {i // chunk_size + 1}")

for dataset in datasets:
    for period in periods:
        print(f"Start Data Fetch: {datetime.now().strftime('%H:%M:%S')} - Dataset: {dataset['name']} - Period: {period['monthid']}")
        data_fetched = get_khis_data(period["startdate"], period["enddate"], dataset["id"])
        print(f"End Data Fetch: {datetime.now().strftime('%H:%M:%S')} - Length of data: {len(data_fetched.get('dataValues', []))}")

        if data_fetched and 'dataValues' in data_fetched:
            print("Start Data Send: " + datetime.now().strftime("%H:%M:%S"))
            split_and_send(data_fetched, 200)
            print("End Data Send: " + datetime.now().strftime("%H:%M:%S"))
    