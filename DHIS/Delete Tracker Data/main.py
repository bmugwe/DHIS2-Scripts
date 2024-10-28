import os, requests, io, base64
import pandas as pd

# credentials 
username = os.getenv('Tracker_username', '')
password = os.getenv('Tracker_password', '')

credentials = f"{username}:{password}"
print(f"Credentials:  {credentials}")
encode_auth = base64.b64encode(credentials.encode()).decode('utf-8')

target_system = 'gbv.health.go.ke'


t_url = 'https://{}/api/events.json?program={}&orgUnit=HfVjCurKxh2&skipPaging=true&ouMode=DESCENDANTS' # &trackedEntityInstance
enr_url = "https://{}/api/trackedEntityInstances/query.json?ou=HfVjCurKxh2&ouMode=DESCENDANTS&order=created:desc&program={}&skipPaging=true"

payload = {}

headers = {
    "Authorization": f"Basic {encode_auth}"
}


# fetch program data
def fetchData(target_system, programid, period):
    url = enr_url.format(target_system, programid)
    try:
        responsedata = requests.get(url,headers=headers, data=payload)
        if responsedata.status_code == 200:
            return responsedata.json()
        else:
            print(responsedata)
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
        
# https://ento.uonbi.ac.ke/api/enrollments/ss81fEwVeJU




def deleteEnrollments(target_system, eventid):
    url = 'https://{}/api/enrollments/{}'.format(target_system, eventid)
    try:
        responseData = requests.delete(url, headers=headers, data=payload)
        
        if responseData.status_code == 200:
            return responseData.json()
        else:
            
            return {"error": responseData.status_code}
    except Exception as e:
        print(f"Error fetching data: {e}")
        
programs = [
    # {
    #     'uid': 'GNIPmRNe57d',
    #     'name': 'ENTO- Mosquito Field & Lab'
    # }
     {
        'uid': 'd5mJRTBeXMW',
        'name': 'SGBV Quality Assessment Tool '
    }
]

# Instantiate
for program in programs:
    response  = fetchData(target_system=target_system, programid=program['uid'], period='')
    print(response['rows'])

    events = response
    print(len(events))
    if len(events)> 0:
        for event in events:
            delete_resp = deleteEnrollments(target_system=target_system, eventid=event[6])
            print(delete_resp)
            # break