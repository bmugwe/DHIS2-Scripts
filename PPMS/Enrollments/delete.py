"""
This script deletes all Enrollment the data from an instance
"""


import requests
import base64
import os

instance = "https://ento.uonbi.ac.ke"
programids = ['Oj5hUu2m0gP','Mk9ocCvATwK','JdBxRPxRWpD','wWNCJjNQDGq','GNIPmRNe57d']

fetch_url = "{}/api/enrollments?ou=HfVjCurKxh2&ouMode=ACCESSIBLE&program={}"
delete_enrollment = "{}/api/enrollments/{}"

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


def fetchEnrollments(instance, headers,programid):
    url = fetch_url.format(instance, programid)
    payload = {}
    print(url)

    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response)
    if response.status_code == 200: 
        data = response.json()
        return data['enrollments']
    else:
        print(f"Error: {response.status_code}")
        return []

# enrollments


def deleteEnrollments(instance,headers,uid):
    url = delete_enrollment.format(instance,uid)
    payload = {}
    response = requests.request("DELETE", url, headers=headers, data=payload)
    response_json = response.json()
    
    return response_json




for programid in programids:
    enrollments = fetchEnrollments(instance,headers,programid)
    # print(enrollments)
    if len(enrollments)>0:
        for enrollment in enrollments:
            delete_resp = deleteEnrollments(instance, headers, enrollment['enrollment'])
            print(delete_resp['response']['description'])
            # break
    else:
        print(f"No data to delete")


