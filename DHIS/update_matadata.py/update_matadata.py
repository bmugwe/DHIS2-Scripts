import requests
import json
from jsondiff import diff
import base64

username=''
password = ''


credentials = f'{username}:{password}'
encoded_password = base64.b64encode(credentials.encode('utf-8')).decode()

system = 'https://xxx.xxx/'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {encoded_password}',
    'Cookie': 'JSESSIONID=EDC9F2053C7D815075F3B8737E63EA1E'
    }


# This can be read from a file and more fields added

chuls = [
        {'uid': 'NU1BeKd6izu', 'code': '710474', 'closedDate': ''},
        # {'uid': 'PhdN0qNP1PF', 'code': '711995', 'closedDate': ''},
        # {'uid': 'Nhthfk3HQLu', 'code': '602959', 'closedDate': ''},
        # {'uid': 'nRNLYFghBIj', 'code': '600101', 'closedDate': ''},
        # {'uid': 'GeQL3ifKrUD', 'code': '711995', 'closedDate': ''},
        # {'uid': 'wpY43rgsEhj', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'uLrFZoYPmOv', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'kTrcUGhlUfW', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'HhkXAQK4uyn', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'BAwY5B8NcOi', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'torPP7IChoI', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'Syg6S7zTxnX', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'EoBS9YUdHYY', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'HOBSOfORNFI', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'dFE1sQ8K6Z2', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'XZ6dSkJUjX9', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'Lyqs6SS0kRO', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'g9Svn6LHojm', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'SwfXuJj8oVg', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'KOfAhct8piJ', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'PHJHQG11nPm', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'vsdsjapAtO6', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'CZQL77SwNk6', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'kRKWbPlCDe8', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'GeKmLzqcIU6', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'fN5PJnuIq0G', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'ys1RoATAcu4', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'hxyJypd71JT', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'SATepGjdMJg', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},
        # {'uid': 'sPjW4tO3fQS', 'code': '', 'closedDate': '2024-07-31T00:00:00.000'},


        #  {'uid': 'sD3LFbLKu0v', 'code': '710462', 'closedDate': ''}
         ]

def fetchData(uid):
    url = "{}/api/29/organisationUnits/{}?fields=name,id,code,created,closedDate,level,shortName,parent[id],openingDate,path".format(system, uid)

    payload = json.dumps({
    "closedDate": "2020-07-31T00:00:00.000"
    })



    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        print(response.text)
        return response.json()


def update_metadata(payload, i={}):
    try:
        if payload:
            url = "{}/api/29/organisationUnits/{}".format(system, payload['id'])
            print(f"Url : {url}")
            
            # Provide the fields you want to edit
            payload['closedDate'] = i['closedDate']
            # payload['code'] = i['code']
            
            print(f"payload : {payload}")
            
            payloads = json.dumps(payload)

            response = requests.request("PUT", url, headers=headers, data=payloads)

            print(response.text)
    except Exception as e:
        print(f"Error updating data: {e}")
    
    
    
for i in chuls:
    response = update_metadata(fetchData(i['uid']),i=i)
    
    
    

