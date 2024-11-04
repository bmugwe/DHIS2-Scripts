import requests
import base64
import os

instance = "https://ento.uonbi.ac.ke"
instances = ['hPK6OJZf7JJ','qIKI1C8qgbn','C58YfJBJfI5','FIWnBUqxAAa']

fetch_url = "{}/api/trackedEntityInstances?trackedEntityType={}&ou=HfVjCurKxh2&ouMode=ACCESSIBLE"
delete_enrollment = "{}/api/trackedEntityInstances/{}"

ento_username = os.getenv("ento_username")
ento_password = os.getenv("ento_password")

def encodePassword(username,password):
    cred_string = f"{username}:{password}"
    encoded_credentials = base64.b64encode(cred_string.encode('utf-8')).decode('utf-8')   
    print(f" Username & password : {cred_string} and endoded : {encoded_credentials}")
    return encoded_credentials

ento_credentials = encodePassword(ento_username, ento_password)
headers = {
        "Authorization": f"Basic {ento_credentials}"
    }


def fetchInstances(instance, headers,programid):
    url = fetch_url.format(instance, programid)
    payload = {}
    print(url)

    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response)
    if response.status_code == 200: 
        data = response.json()
        return data['trackedEntityInstances']
    else:
        print(f"Error: {response.status_code}")
        return []

# enrollments


def deleteInstances(instance,headers,uid):
    url = delete_enrollment.format(instance,uid)
    payload = {}
    response = requests.request("DELETE", url, headers=headers, data=payload)
    response_json = response.json()
    
    return response_json




for programid in instances:
    enrollments = fetchInstances(instance,headers,programid)
    # print(enrollments)
    if len(enrollments)>0:
        for enrollment in enrollments:
            # print(enrollment)
            delete_resp = deleteInstances(instance, headers, enrollment['trackedEntityInstance'])
            print(delete_resp['response']['description'])
            # break
    else:
        print(f"No data to delete")