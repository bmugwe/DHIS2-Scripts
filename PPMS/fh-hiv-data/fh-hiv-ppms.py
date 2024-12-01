from requests import request
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from password import encodePassword

periods = [ "2024-09-01", "2024-09-30"]

dataVar = [
    {
        "name": "FH",
        "groupuid": "LTkSzGmmsiU"
    },
    {
        "name": "HIV",
        "groupuid": "lzENxYwEV4Z"
    }
]

khis_creds = encodePassword(os.getenv("KHIS_USERNAME"), os.getenv("KHIS_PASSWORD"))
ppms_creds = encodePassword(os.getenv("ppms_username"), os.getenv("ppms_password"))

def fetchData(uid, creds,period=[]):
    params = {}
    urls = "https://hiskenya.org/api/sqlViews/bEz5t8O8JWi/data.json?var=groupuid:{}&var=pstart:{}&var=pend:{}".format(uid, period[0], period[1])
    try:
        data = request("GET", url=urls, params=params, headers=creds)
        print(data.text)
        if data.status_code == 200:
            datajson=data.json()
            print(datajson)
            return datajson
    except Exception as e:
        print(f"Error fetching data: {e}")
        
        
fetchData(dataVar[0]['groupuid'], khis_creds, periods)
        
        