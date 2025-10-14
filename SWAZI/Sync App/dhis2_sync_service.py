# file: dhis2_sync_service.py
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pyodbc
import requests
from datetime import datetime
import random
import os
import pandas as pd
from typing import List

# read FileExistsError
anc_data = pd.read_csv('anc_data.csv')
pmtct_data = pd.read_csv('pmtct_data.csv')

# ----------------------------
# CONFIG
# ----------------------------
DB_CONN_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=EMR;"
    "UID=sa;"
    "PWD=YourPassword123;"
)
DHIS2_URL = "https://swz-testhmis.exhaustivesoln.com/dhis/"
DHIS2_USER = "admin"
DHIS2_PASS = "Swati@4050"


# Load data element mappings api api/dataStore/EMR_DHIS/Mapping
def load_data_element_mappings():
    global DATA_ELEMENT_MAP
    try:
        response = requests.get(
            f"{DHIS2_URL}api/dataStore/EMR_DHIS/Mapping",
            auth=(DHIS2_USER, DHIS2_PASS),
            timeout=10
        )
        response.raise_for_status()
        DATA_ELEMENT_MAP = response.json()
    except Exception as e:
        print(f"Error loading data element mappings: {e}")
        exit(1)
    return DATA_ELEMENT_MAP

DATA_ELEMENT_MAP = load_data_element_mappings()
# ----------------------------
# INIT APP
# ----------------------------
app = FastAPI(title="EMR → DHIS2 Aggregation Sync")
templates = Jinja2Templates(directory="templates")



# 
# Simulated sync log data (you'll later replace this with DB)
sync_history = pd.read_csv('sync_log.csv').to_dict(orient='records')


# ----------------------------
# DATABASE UTILS
# ----------------------------
def get_connection():
    return pyodbc.connect(DB_CONN_STRING)


def get_facilities():
    
    """
    This can be either be stored from the MSSQL Database or fetched from DHIS2 orgUnits API.
    """
    # Fetch from DHIS2:
    try:
        response = requests.get(
            f"{DHIS2_URL}api/organisationUnits?fields=id,displayName&paging=false",
            auth=(DHIS2_USER, DHIS2_PASS),
            timeout=10
        )
        response.raise_for_status()
        org_units = response.json().get("organisationUnits", [])
        # the first item will be all options
        # org_units.insert(0, {"id": "ALL", "displayName": "All Facilities"})
        return [{"FacilityCode": ou["id"], "FacilityName": ou["displayName"]} for ou in org_units]
    except Exception as e:
        print(f"Error fetching org units from DHIS2: {e}")
        # Fallback to hardcoded list or DB fetch



def get_programs():
    return list(DATA_ELEMENT_MAP.keys())


def aggregate_program_data(program, period, facility_code ):
    """
    Fetch the data from the SQL using the passed parameters.
    For demo, we will read from the CSV files.
    """
    # SQL call:
    # with get_connection() as conn:
    #     cursor = conn.cursor()
    #     cursor.execute("EXEC sp_AggregateANC ?, ?", (period, facility_code))
    #     result = cursor.fetchone()
    print(f"Aggregating data for Program: {program}, Period: {period}, Facility: {facility_code}")

    # aggregation result:
    if program == "ANC":
        anc_emr_data = pd.read_csv('anc_data.csv')
        filter_data = anc_emr_data[(anc_emr_data['ReportMonth'] == period) & (anc_emr_data['FacilityCode'].isin(facility_code))]
        if filter_data.empty:
            return {}
        # unmelt the dataframe and combine with data element map on the Indicator column to StoredProcName in mapping
        unmelted = filter_data.melt(id_vars=['Period', 'FacilityCode'], var_name='Indicator', value_name='value')
        # Map Indicator to data element using DATA_ELEMENT_MAP
        unmelted['DataElement'] = unmelted['Indicator'].map(DATA_ELEMENT_MAP['ANC'])
        merged = unmelted.merge(pd.DataFrame.from_dict(DATA_ELEMENT_MAP['ANC'], orient='index', columns=['DataElement']), left_on='Indicator', right_index=True, how='left')
        # Keep only relevant columns
        unmelted = merged[['FacilityCode', 'ReportMonth', 'dataElementId', 'categoryOptionComboId', 'value']]
        # Rename columns to match DHIS2 payload
        unmelted.columns = ['orgUnit', 'period', 'dataElement', 'categoryOptionCombo', 'value']
        # Drop rows where DataElement is NaN (no mapping found)
        unmelted = unmelted.dropna(subset=['DataElement'])
        # Create summary dictionary
        summary = dict(zip(unmelted['Indicator'], unmelted['value']))
        return summary

        


    elif program == "PMTCT":
        pmtct_emr_data = pd.read_csv('pmtct_data.csv')
        
    else:
        return {}


# ----------------------------
# DHIS2 PUSH
# ----------------------------
def push_to_dhis2(program: str, period: str, facility_code: str, summary: dict):
    payload = {
        "dataValues": [
            {
                "dataElement": DATA_ELEMENT_MAP[program][k],
                "period": period.replace("-", ""),
                "orgUnit": facility_code,
                "value": v
            }
            for k, v in summary.items()
        ]
    }
    try:
        response = requests.post(
            DHIS2_URL,
            json=payload,
            auth=(DHIS2_USER, DHIS2_PASS),
            timeout=20
        )
        response.raise_for_status()
        return {"status": "success", "details": response.json()}
    except Exception as e:
        return {"status": "error", "details": str(e)}


# ----------------------------
# ROUTES
# ----------------------------
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    facilities = get_facilities()
    programs = get_programs()
    current_month = datetime.now().strftime("%Y-%m")
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "facilities": facilities,
        "programs": programs,
        "current_month": current_month
    })
    


@app.post("/submit", response_class=HTMLResponse)
async def submit_data(
    request: Request,
    background_tasks: BackgroundTasks,
    month: str = Form(...),
    facility_code: List(str) = Form(...),
    program: str = Form(...)
):
    facilities = [f["FacilityCode"] for f in get_facilities()] if facility_code == "ALL" else [facility_code]

    results = []
    for fac in facilities:
        summary = aggregate_program_data(program, month, fac)
        background_tasks.add_task(push_to_dhis2, program, month, fac, summary)
        results.append({"facility": fac, "summary": summary})

    return templates.TemplateResponse("submitted.html", {
        "request": request,
        "program": program,
        "month": month,
        "facilities": facilities,
        "results": results
    })
    
    
@app.get("/summary", response_class=HTMLResponse)
async def summary(request: Request):
    return templates.TemplateResponse(
        "summary.html",
        {"request": request, "syncs": sync_history},
    )
    

