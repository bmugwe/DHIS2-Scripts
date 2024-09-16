import os, requests, io, base64
import pandas as pd

# credentials 
username = os.getenv('HISTRACKER_USERNAME', 'admin')
password = os.getenv('HISTRACKER_PASSWORD', '')

credentials = f"{username}:{password}"

encode_auth = base64.b64encode(credentials.encode()).decode('utf-8')

target_system = 'ento.uonbi.ac.ke'
t_url = 'https://{}/api/events.json?program={}&orgUnit=HfVjCurKxh2&skipPaging=true&ouMode=DESCENDANTS' # &trackedEntityInstance

payload = {}

headers = {
    "Authorization": f"Basic {encode_auth}"
}


# fetch program data
def fetchData(target_system, programid, period):
    url = t_url.format(target_system, programid)
    try:
        responsedata = requests.get(url,headers=headers, data=payload)
        if responsedata.status_code == 200:
            return responsedata.json()
        else:
            return responsedata.status_code
        
    except Exception as e:
        print(f"Error fetching data: {e}")

def deleteEvent(target_system, eventid):
    url = 'https://{}/api/events/{}'.format(target_system, eventid)
    try:
        responseData = requests.delete(url, headers=headers, data=payload)
        if responseData.status_code == 200:
            return responseData.json()
        else:
            return {"error": responseData.status_code}
    except Exception as e:
        print(f"Error fetching data: {e}")
        
programs = [
    {
        'uid': 'GNIPmRNe57d',
        'name': 'ENTO- Mosquito Field & Lab'
    }
]

# Instantiate
for program in programs:
    response  = fetchData(target_system=target_system, programid=program['uid'], period='')
    events = response['events']
    print(len(events))
    if len(events)> 0:
        for event in events:
            delete_resp = deleteEvent(target_system=target_system, eventid=event['event'])
            print(delete_resp)
            # break