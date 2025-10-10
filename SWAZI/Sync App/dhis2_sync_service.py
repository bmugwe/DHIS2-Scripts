# file: dhis2_sync_service.py
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pyodbc
import requests
from datetime import datetime
import random
import os

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
DHIS2_URL = "https://play.dhis2.org/2.39.0/api/dataValueSets"
DHIS2_USER = "admin"
DHIS2_PASS = "district"

DATA_ELEMENT_MAP = {
    "ANC": {
        "first_anc_visits": "DE_ANC1",
        "completed_4_visits": "DE_ANC4",
        "completed_8_visits": "DE_ANC8",
        "gestation_12_13_weeks": "DE_GEST12",
        "hb_result": "DE_HB",
        "bp_risk": "DE_BP_RISK"
    },
    "PMTCT": {
        "tested_hiv": "DE_PMTCT_HIVT",
        "positive_hiv": "DE_PMTCT_HIVP"
    }
}

# ----------------------------
# INIT APP
# ----------------------------
app = FastAPI(title="EMR → DHIS2 Aggregation Sync")
templates = Jinja2Templates(directory="templates")


# ----------------------------
# DATABASE UTILS
# ----------------------------
def get_connection():
    return pyodbc.connect(DB_CONN_STRING)


def get_facilities():
    # Ideally: SELECT FacilityCode, FacilityName FROM Facilities
    # Simulated:
    return [
        {"FacilityCode": "FAC001", "FacilityName": "Nairobi Clinic"},
        {"FacilityCode": "FAC002", "FacilityName": "Mombasa Hospital"},
        {"FacilityCode": "FAC003", "FacilityName": "Kisumu Health Centre"}
    ]


def get_programs():
    return list(DATA_ELEMENT_MAP.keys())


def aggregate_program_data(program: str, period: str, facility_code: str | None = None):
    """
    Replace this simulated function with actual SQL or stored procedure.
    """
    # Example pseudo SQL call:
    # with get_connection() as conn:
    #     cursor = conn.cursor()
    #     cursor.execute("EXEC sp_AggregateANC ?, ?", (period, facility_code))
    #     result = cursor.fetchone()

    # Simulated aggregation result:
    if program == "ANC":
        return {
            "first_anc_visits": random.randint(20, 80),
            "completed_4_visits": random.randint(10, 40),
            "completed_8_visits": random.randint(5, 20),
            "gestation_12_13_weeks": random.randint(5, 30),
            "hb_result": random.randint(40, 100),
            "bp_risk": random.randint(2, 10)
        }
    elif program == "PMTCT":
        return {
            "tested_hiv": random.randint(50, 120),
            "positive_hiv": random.randint(1, 5)
        }
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
    facility_code: str = Form("ALL"),
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
