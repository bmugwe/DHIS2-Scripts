
import pandas as pd
import requests
import os
import base64
import time
import json
from datetime import datetime

# data = pd.read_csv("mpdsr with data only 2023-2024 unpivot.csv")

ppms_url = 'https://partnermanagementsystem.uonbi.ac.ke/api/dataValueSets'

his_payload = {
  "dataValues": []
}
dx_1 = "DNBBwlpebZw;BZwn7wgZc3V;bMBmhuOSEVI;UmsZBd6ATQn"

his_ppms_maps_2 = {
    "DNBBwlpebZw": "dZzm76ecChR",
    "BZwn7wgZc3V": "HXDZ1b1dCBO",
    "bMBmhuOSEVI": "Y6NJJ4zMEd9",
    "UmsZBd6ATQn": "akCNCmmaBbb",
}

dx_ = "ylZH6tH8WOH;IzqbXoSOMfv;NnOrzt7x74u;FwzCwehmM1l;Qs5YOJL94Xv;UeTTbMKHmV2;ycX1Tf0yEEq;v02HIKYr96y;CqEaliAiiPB;AvDmF3XMyzF;q5WGKgtb9Ek;BKeTGPOfVgy;rJ76lWNJGyx;Dsu3gCECwGF;I3GmRuCvcqz;yMd2XgO3AiM;DNBBwlpebZw;BZwn7wgZc3V;bMBmhuOSEVI;UmsZBd6ATQn"

his_ppms_maps = {
  'ylZH6tH8WOH' : 'dF4XP7NlXZK.dNnRMgjTb5U',
  'IzqbXoSOMfv' : 'dF4XP7NlXZK.drY5kYNnRX4',
  'NnOrzt7x74u' : 'MTrxHv4gTaW.G8E262DUEEY',
  'FwzCwehmM1l' : 'MTrxHv4gTaW.oteUDu8KNFg',
  'Qs5YOJL94Xv' : 'MTrxHv4gTaW.OV4Yn4SYOR2',
  'UeTTbMKHmV2' : 'MTrxHv4gTaW.syMXHBm7ZxQ',
  'ycX1Tf0yEEq' : 'MTrxHv4gTaW.WkarWtkR1aM',
  'v02HIKYr96y' : 'MTrxHv4gTaW.z4qWeyZQYg3',
  'CqEaliAiiPB' : 'Rrw1g9R2Z18.jFCf2UA0Ul1',
  'AvDmF3XMyzF' : 'Rrw1g9R2Z18.M3y01GZ6HeX',
  'q5WGKgtb9Ek' : 'Rrw1g9R2Z18.NkddIM7dhTo',
  'BKeTGPOfVgy' : 'Rrw1g9R2Z18.nR2gfNigfZ0',
  'rJ76lWNJGyx' : 'Rrw1g9R2Z18.qJX1Bvp0tT3',
  'Dsu3gCECwGF' : 'Rrw1g9R2Z18.rluhzo9yzWB',
  'I3GmRuCvcqz' : 'Rrw1g9R2Z18.y7jpY5THPqn',
  'yMd2XgO3AiM' : 'Rrw1g9R2Z18.YIHb50x9KLh',
  "DNBBwlpebZw" : "dZzm76ecChR.HllvX50cXC0",
  "BZwn7wgZc3V" : "HXDZ1b1dCBO.HllvX50cXC0",
  "bMBmhuOSEVI" : "Y6NJJ4zMEd9.HllvX50cXC0",
  "UmsZBd6ATQn" : "akCNCmmaBbb.HllvX50cXC0",
}
#   'jOLX7zOxZMH' : 'Rrw1g9R2Z18.RpOqJT7iwgo',

# elements = data[['dataid', 'dataname']].drop_duplicates()
# print(elements)

Tracker_username = os.getenv('Tracker_username', '')
Tracker_password = os.getenv('Tracker_password', '')

# ptime = "2023W1;2023W2;2023W3;2023W4;2023W5;2023W6;2023W7;2023W8;2023W9;2023W10;2023W11;2023W12;2023W13;2023W14;2023W152023W15;2023W16;2023W17;2023W18;2023W19;2023W20;2023W21;2023W22;2023W23;2023W24;2023W25;2023W26;2023W27;2023W28" # ;2023W29;2023W30;2023W31;2023W32;2023W33;2023W34;2023W35;2023W36;2023W37;2023W38;2023W39;2023W40;2023W41;2023W42;2023W43;2023W44;2023W45;2023W46;2023W47;2023W48;2023W49;2023W50;2023W51;2023W52;

# ptime = "2024W1;2024W2;2024W3;2024W4;2024W5;2024W6;2024W7;2024W8;2024W9;2024W10;2024W11;2024W12;2024W13;2024W14;2024W15;2024W16;2024W17;2024W18;2024W19;2024W20;2024W21;2024W22;2024W23;2024W24;2024W25;2024W26;2024W27;2024W28;2024W29;2024W30;2024W31;2024W32;2024W33;2024W34;2024W35;2024W36;2024W37;2024W38"

ptime = "2024W39"
# ptime = "2024W37;2024W38"


def readTracker(period, orguni, data_elements):
    url = f"https://histracker.health.go.ke/api/32/analytics.json?dimension=ou:HfVjCurKxh2;LEVEL-t9kwHRyMyOC&dimension=dx:{data_elements}&dimension=pe:{period}&outputIdScheme=UID"
    # url = f"http://144.91.119.106:8084/api/32/analytics.json?dimension=ou:HfVjCurKxh2;LEVEL-t9kwHRyMyOC&dimension=dx:{data_elements}&dimension=pe:{period}&outputIdScheme=UID"
    
    print(url)
    credentials = Tracker_username + ':' + Tracker_password

    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }
    print(f"heades: {headers}")
    payload = {}
    try:
        data = requests.request("GET", url,data=payload, headers=headers)
        time.sleep(5)
        print(data.status_code)
        if data.status_code == 200 and data.json()['height']:
            datajson = data.json()        
            return datajson
        else:
            print(data.status_code)
    except Exception as e:
        print(f"Error fetching data: {e}")
        
def tranformData(data):
    try:
        resp_df = pd.DataFrame(data['rows'])
        resp_df2 = resp_df.rename(columns={0: 'dataElement_cc', 1: 'orgUnit', 2: 'period', 3: 'value'})
        resp_df3 = resp_df2.replace({"dataElement_cc": his_ppms_maps})
        print(f"Before handling coc: {resp_df3.head}")
        # handle categoryOptionCombo occurence from dataelement
        resp_df3[['dataElement', 'categoryOptionCombo']] = resp_df3['dataElement_cc'].str.split('.', expand=True)

        print(f"While handling coc: {resp_df3.head}")
        # Drop the original column2 if needed
        resp_df3.drop(columns=['dataElement_cc'], inplace=True)
        print(f"After handling coc: {resp_df3.head}")
        
        resp_df3['value'] = resp_df3['value'].astype(float).astype(int).astype(str)
        resp_df3['attributeOptionCombo'] = 'vxj0USPdpGx'
        tojson = resp_df3.to_dict(orient='records')
        
        print(f"Data to send ----- : {tojson}")
        
        with open('dataSent'+datetime.now().time().strftime("%H:%M:%S")+'.json', 'w') as f:
            f.write(f"{tojson}")
        
        return tojson
    except Exception as e:
        print(f"Error Transforming data: {e}")
        
        return None
    
# post data

def PostData(data):
    his_payload_refresh = his_payload
    url = ppms_url
    credentials = os.getenv("ppms_username","") + ':' + os.getenv("ppms_password","")
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    headers = {
        "Authorization": f'Basic {encoded_credentials}',
        'Content-Type': 'application/json',
    }
    his_payload_refresh['dataValues'] = data
    # print(f"Data b4 payload ---->>  {data}")
    payload = json.dumps(his_payload_refresh)
    # print(f"POST payload ---->>  {payload}")
    transaction_time = time.strftime("%d:%m:%y %H:%M:%S",time.localtime())
    try:
        response = requests.post(url,data=payload, headers=headers )
        if response.status_code != 200:
            with open('logs.txt', 'a+') as f:
                f.write(f"{ transaction_time } : {response.text}\n")
        else:
            with open('success.txt', 'a+') as f:
                f.write(f"{ transaction_time } : {response.text}\n")
                
    except Exception as e:
        print(f"Error posting data: {e}")
    

weeks = ptime

# for week in  weeks:
if weeks:
    print(f" Processing {weeks} weeks")
    
    response = readTracker(weeks, 'Nairobi', dx_1)
    
    tr_resp = tranformData(response)
    
    PostData(tr_resp)



