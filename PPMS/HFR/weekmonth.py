import requests
import json
import pandas as pd
import numpy as np
import io
import base64
import os



# month_attribute = [hfr_month, activeyear - annual, dhismonth_to_be_updated] chnage this to the month being updated, next month
# month_attribute = [5, 2023, "202301", "202302"]
# month_attribute = [11, 2024, "202407", "202408"]
month_attribute = [12, 2024, "202408", "202409"]
month_attribute = [1, 2025, "202409", "202410"]

url = 'https://partnermanagementsystem.uonbi.ac.ke/api/29/analytics.json?dimension=dx:{}&dimension=lRp2LBbTuM5&dimension=ou:LEVEL-5&dimension=pe:{}&displayProperty=NAME'
importUrl = 'https://partnermanagementsystem.uonbi.ac.ke/api/dataValueSets'

payload={}

username = os.getenv("ppms_username",'')
password = os.getenv("ppms_password",'')

credentials = f"{username}:{password}"

auth_encoded = base64.b64encode(credentials.encode()).decode("utf-8")

# credentials for user healthit
headers = {
  'Authorization': f'Basic {auth_encoded}',
  'Cookie': 'JSESSIONID=10CD6CA777D1A4AE44A00FD25B72753F',
  'Accept': 'application/json', 'Content-Type': 'application/json'
}

push_template =  {"dataValues": [ ] }

data_val_temp = {
      "dataElement": {},
      "period": {},
      "orgUnit": {},
      "categoryOptionCombo": {},
      "attributeOptionCombo": {},
      "value": {},
    }

def callApi(url):
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(response.content)
        # print(response)
    except Exception as e:
        print(f"Error in callApi is {e}")

    return response


with open('weekly_monthly.json') as weekly:
    dataelements_swap = json.load(weekly)
weekly.close()

hfr_period = open('hfr_periods_id.json')
hfrperiods = json.load(hfr_period)
hfr_period.close()


cotocco = open('cotocco.json')
cotoccos = json.load(cotocco)
cotocco.close()

# for hfr in hfrperiods:
#     print(type(hfr))

# filter the month in the hfr period calendar
def filters(array, keyvalue, valued, returnvalue):
    result_filter = []
    for arr in array:
        if arr[keyvalue]==valued and arr["year"]==month_attribute[1]:
            print(arr)
            result_filter.append(arr[returnvalue])
    
    return result_filter


current_month = filters(hfrperiods, "hfrmonth", month_attribute[0] , "queryvar")

current_month_string = ";".join(current_month)

print(current_month)
dx = dataelements_swap[0]['dataele_weekly']

def getMonDataele(weeklydataele, columntoget):
    for weekdataele in dataelements_swap:
        if weekdataele["dataele_weekly"] == weeklydataele:
            mondataele = weekdataele[columntoget]
    
    return mondataele

def getCco(weeklydataele, columntoget):
    cco = ""
    for co in cotoccos:
        if co["couid"] == weeklydataele:
            cco = co[columntoget]
    
    return cco

def getData(url):
    print(f"Fetching url: {url}")
    try:
        request_resp = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(request_resp.text)
        return response
    except Exception as err:
        print(f"Error fetching data: {err}")



def createJson(data, filename):
    with open(filename+'.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def postData(url, jsonFile):    
    try:
        res = requests.post(url, headers = headers, data=jsonFile) 
        res  = json.loads(res.content)
        # push_data= request.request("POST", url, headers=headers, data=payload)
        print(res)
        # createJson(res,dataele_proc+'response')
    except Exception as error:
        print(f"Data did not submit, Error is: {error}")
        


def getUniqueRows(rowws, arrindex):
    u_list = []
    for roww in rowws:
        if roww[arrindex] not in u_list:
            u_list.append(roww[arrindex])

    return u_list




def convert(dx):
    c_url = url.format(dx, current_month_string)

    data_resp = getData(c_url)

    rows = data_resp["rows"]
    print(f" Processing {len(rows)} records")
    # orgunits = data_resp["metaData"]["dimensions"]["ou"]
    # attrcombos = data_resp["metaData"]["dimensions"]["lRp2LBbTuM5"]

    orgunits = getUniqueRows(rows,2)
    attrcombos = getUniqueRows(rows,1)

    dxm = getMonDataele(dx, "dataele_monthly")
    value=0


    data_val_temp = {}
    for orgunit in orgunits:
        for attrcombo in attrcombos:
            for row in rows:
                if row[1] == attrcombo and row[2] == orgunit:
                    # print(row[4])
                    if float(row[4]) > 0:
                        value += float(row[4])


            dataele = dx.split('.')[0]
            catcombo = dx.split('.')[1]
            m_dataele = dxm.split('.')[0]
            m_catcombo = dxm.split('.')[1]
            if value >0 :
                print(f"orgunit: {orgunit} attrcombo: {attrcombo} dataele: {m_dataele} catcombo: {m_catcombo} periodid: {month_attribute[2]} value: {value}")
                data_val_temp =  {
                                "dataElement": m_dataele,
                                "period": month_attribute[2],
                                "orgUnit": orgunit,
                                "categoryOptionCombo": m_catcombo,
                                "attributeOptionCombo": getCco(attrcombo,"ccouid"),
                                "value": str(int(value))
                                }

                push_template["dataValues"].append(data_val_temp)
                value=0     

    dataele_proc = getMonDataele(dx, "name_monthly")
    dataele_proc = (dataele_proc).split(' ')[0]+(dataele_proc).split(' ')[1]+(dataele_proc).split(' ')[2]+month_attribute[2]
    if len(rows)> 0:
        createJson(push_template, dataele_proc)
        data_json = io.BytesIO(push_template.encode('utf-8'))
        # amcfile = open(dataele_proc+'.json', 'rb')
        postData(importUrl, data_json)
        print(f"Success {dataele_proc}")
    else:
        print(f"Skipping {dataele_proc} : no data")

    push_template["dataValues"] = []
    return push_template
        #         break
        #     break
        # break



def previousMonth():
    indicators = [
                {'name': 'MV_HFR_TX_CURR',
                    'uid': 'fPZoJ5MwbN1.alMMbxnPh3n',
                    'type': 'data element',
                    'uid_2': 'MN0qBblAtxk.alMMbxnPh3n',
                    'name_2': 'MV_HFR_TX_CURR x-1',
                },
                {'name': 'MV_HFR_TX_CURR',
                    'uid': 'fPZoJ5MwbN1.kX4BLp2Wskc',
                    'type': 'data element',
                    'uid_2': 'MN0qBblAtxk.kX4BLp2Wskc',
                    'name_2': 'MV_HFR_TX_CURR x-1',
                },
                {'name': 'MV_HFR_TX_CURR',
                    'uid': 'fPZoJ5MwbN1.FM340uJtNY1',
                    'type': 'data element',
                    'uid_2': 'MN0qBblAtxk.FM340uJtNY1',
                    'name_2': 'MV_HFR_TX_CURR x-1',
                },
                {'name': 'MV_HFR_TX_CURR',
                    'uid': 'fPZoJ5MwbN1.V30Om65Tj8L',
                    'type': 'data element',
                    'uid_2': 'MN0qBblAtxk.V30Om65Tj8L',
                    'name_2': 'MV_HFR_TX_CURR x-1',
                }
                ,
                {'name': 'MV_TX_NEW_BALANCE',
                    'uid': 'bEnZU8ZzR5v',
                    'type': 'indicator',
                    'uid_2': 'voRkhmFrwP9.alMMbxnPh3n',
                    'name_2': 'HFR:Floating Target x-1',
                    'defination': '15+, Female'
                }
                ,
                {'name': 'MV_TX_NEW_BALANCE',
                    'uid': 'hTqE0bfXibl',
                    'type': 'indicator',
                    'uid_2': 'voRkhmFrwP9.kX4BLp2Wskc',
                    'name_2': 'HFR:Floating Target x-1',
                    'defination': '15+, Male'
                },
                {'name': 'MV_TX_NEW_BALANCE',
                    'uid': 'hvkVYc5c0h5',
                    'type': 'indicator',
                    'uid_2': 'voRkhmFrwP9.FM340uJtNY1',
                    'name_2': 'HFR:Floating Target x-1',
                    'defination': '<15, Female'
                },
                {'name': 'MV_TX_NEW_BALANCE',
                    'uid': 'Hu6U5udxIsv',
                    'type': 'indicator',
                    'uid_2': 'voRkhmFrwP9.V30Om65Tj8L',
                    'name_2': 'HFR:Floating Target x-1',
                    'defination': '<15, Male'
                }
                ]
    for indicator in indicators:
        mx_url = url.format(indicator['uid'], month_attribute[2])
        response = getData(mx_url)
        print(response)
        next_month  = month_attribute[3]
        rows = response["rows"]
        indicator_name = indicator['name'] + ' '+ month_attribute[2] + ' - '+ next_month
        for row in rows:
            if row[3]==month_attribute[2]:
                data_val_temp =  {
                                "dataElement": indicator["uid_2"].split('.')[0],
                                'categoryOptionCombo': indicator["uid_2"].split('.')[1],
                                "period": month_attribute[3],
                                "orgUnit": row[2],
                                "attributeOptionCombo": getCco(row[1],"ccouid"),
                                "value": str(int(float(row[4])))
                                }
            

                push_template["dataValues"].append(data_val_temp)
        print(push_template["dataValues"])
        if len(push_template["dataValues"]) > 0:
            createJson(push_template, indicator_name)
            # amcfile = open(indicator_name+'.json', 'rb')
            push_template1 = json.dumps(push_template)
            push_template2 = push_template1.encode('utf-8')
            amcfile = io.BytesIO(push_template2)
            postData(importUrl, amcfile)
            print(f"Success {indicator_name}")
        else:
            print(f"Skipping {indicator_name} : no data")


"""  <----- Weekly - Monthly conversion script ----->"""
# for onedataelements_swap in dataelements_swap:
#     dx = onedataelements_swap["dataele_weekly"]
#     convert(dx)

previousMonth()