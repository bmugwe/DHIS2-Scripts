import requests
import json
import os
# This script creates a Program Indicator in DHIS2 using the provided API endpoint.
# Ensure you have the requests library installed: pip install requests
import base64

def encodePassword(username,password):
    cred_string = f"{username}:{password}"
    encoded_credentials = base64.b64encode(cred_string.encode('utf-8')).decode('utf-8')   
    print(f" Username & password : {cred_string} and endoded : {encoded_credentials}")

    headers = {
            "Authorization": f"Basic {encoded_credentials}"
        }
    return encoded_credentials

url = "https://xxxxxxxxxxxxxxxxx.health.go.ke/api/29/programIndicators"
url = "https://xxxxx.xxxxx.co.ke/api/29/programIndicators"


data_to_create = [
  {
    "Inidicator_Name": "NTD - Primary I.T.O. Initial Cure Ssg+Pm",
    "id": "Z5XtptcfcnX",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "1")'
  },
  {
    "Inidicator_Name": "NTD - Primary I.T.O. Non Response Ssg+Pm",
    "id": "iwVlVpE48pz",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "2" || #{YAqgg6142Nn.BIzredhqtbr} == "3")'
  },
  {
    "Inidicator_Name": "NTD - Primary I.T.O. Defaulted Ssg+Pm",
    "id": "Ji24Mus6pHr",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "4")'
  },
  {
    "Inidicator_Name": "NTD - Primary I.T.O. Death Ssg+Pm",
    "id": "ItAcWopRgvM",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "5")'
  },
  {
    "Inidicator_Name": "NTD - Relapse I.T.O. Initial Cure Ssg+Pm",
    "id": "dNTrJadnoWG",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "1")'
  },
  {
    "Inidicator_Name": "NTD - Relapse I.T.O. Non Response Ssg+Pm",
    "id": "NRowmfW01Z3",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "2" || #{YAqgg6142Nn.BIzredhqtbr} == "3")'
  },
  {
    "Inidicator_Name": "NTD - Relapse I.T.O. Defaulted Ssg+Pm",
    "id": "WEmxZDVSDcA",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "4")'
  },
  {
    "Inidicator_Name": "NTD - Relapse I.T.O. Death Ssg+Pm",
    "id": "x32XQjtnLUh",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "5")'
  },
  {
    "Inidicator_Name": "NTD - Others I.T.O. Initial Cure Ssg+Pm",
    "id": "wfdevrOzuxf",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "1")'
  },
  {
    "Inidicator_Name": "NTD - Others I.T.O. Non Response Ssg+Pm",
    "id": "Wa5eURg28MW",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "2" || #{YAqgg6142Nn.BIzredhqtbr} == "3")'
  },
  {
    "Inidicator_Name": "NTD - Others I.T.O. Defaulted Ssg+Pm",
    "id": "SVN0aqYSJrk",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "4")'
  },
  {
    "Inidicator_Name": "NTD - Others I.T.O. Death Ssg+Pm",
    "id": "SNYD1WC5Gtx",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && #{YAqgg6142Nn.Jjv8uLxHS80} == "2" && (#{YAqgg6142Nn.BIzredhqtbr} == "5")'
  },
  {
    "Inidicator_Name": "NTD - Primary I.T.O. Initial Cure Ssg",
    "id": "ZE0QoJBIhDG",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "1")'
  },
  {
    "Inidicator_Name": "NTD - Primary I.T.O. Non Response Ssg",
    "id": "Fpwdk46ejB8",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "2" || #{YAqgg6142Nn.BIzredhqtbr} == "3")'
  },
  {
    "Inidicator_Name": "NTD - Primary I.T.O. Defaulted Ssg",
    "id": "rMgqYlJUVtW",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "4")'
  },
  {
    "Inidicator_Name": "NTD - Primary I.T.O. Death Ssg",
    "id": "GPl5ou54Jpr",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "5")'
  },
  {
    "Inidicator_Name": "NTD - Relapse I.T.O. Initial Cure Ssg",
    "id": "d9qM9qRAZbR",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "1")'
  },
  {
    "Inidicator_Name": "NTD - Relapse I.T.O. Non Response Ssg",
    "id": "n1hxfgaK3iu",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "2" || #{YAqgg6142Nn.BIzredhqtbr} == "3")'
  },
  {
    "Inidicator_Name": "NTD - Relapse I.T.O. Defaulted Ssg",
    "id": "ovtPLRt1XYl",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "4")'
  },
  {
    "Inidicator_Name": "NTD - Relapse I.T.O. Death Ssg",
    "id": "nn5FvqcABcs",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "5")'
  },
  {
    "Inidicator_Name": "NTD - Pkdl I.T.O. Initial Cure Ssg",
    "id": "lcMHWCnk5fZ",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "3" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "1")'
  },
  {
    "Inidicator_Name": "NTD - Pkdl I.T.O. Non Response Ssg",
    "id": "J2tLUvMdsaT",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "3" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "2" || #{YAqgg6142Nn.BIzredhqtbr} == "3")'
  },
  {
    "Inidicator_Name": "NTD - Pkdl I.T.O. Defaulted Ssg",
    "id": "veZqksAPVQM",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "3" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "4")'
  },
  {
    "Inidicator_Name": "NTD - Pkdl I.T.O. Death Ssg",
    "id": "kkiTOOa7Nk0",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "3" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "5")'
  },
  {
    "Inidicator_Name": "NTD - Others I.T.O. Initial Cure Ssg",
    "id": "BYCiW98oo4X",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "1")'
  },
  {
    "Inidicator_Name": "NTD - Others I.T.O. Non Response Ssg",
    "id": "LT0Io2FNRbZ",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "2" || #{YAqgg6142Nn.BIzredhqtbr} == "3")'
  },
  {
    "Inidicator_Name": "NTD - Others I.T.O. Defaulted Ssg",
    "id": "N067vdL6PM4",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "4")'
  },
  {
    "Inidicator_Name": "NTD - Others I.T.O. Death Ssg",
    "id": "f5iwaLbeXAs",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && #{YAqgg6142Nn.Jjv8uLxHS80} == "7" && (#{YAqgg6142Nn.BIzredhqtbr} == "5")'
  },
  {
    "Inidicator_Name": "NTD - Primary I.T.O. Initial Cure Ambisome",
    "id": "RRk8SMCPnd9",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "9" && (#{YAqgg6142Nn.BIzredhqtbr} == "1")'
  },
  {
    "Inidicator_Name": "NTD - Primary I.T.O. Non Response Ambisome",
    "id": "Z7wcB80zd29",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "9" && (#{YAqgg6142Nn.BIzredhqtbr} == "2" || #{YAqgg6142Nn.BIzredhqtbr} == "3")'
  },
  {
    "Inidicator_Name": "NTD - Primary I.T.O. Defaulted Ambisome",
    "id": "yBOTzzLrgtg",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "9" && (#{YAqgg6142Nn.BIzredhqtbr} == "4")'
  },
  {
    "Inidicator_Name": "NTD - Primary I.T.O. Death Ambisome",
    "id": "Ltes8TbmTFk",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && #{YAqgg6142Nn.Jjv8uLxHS80} == "9" && (#{YAqgg6142Nn.BIzredhqtbr} == "5")'
  },
  {
    "Inidicator_Name": "NTD - Relapse I.T.O. Initial Cure Ambisome",
    "id": "wPRJBpPC6DZ",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "9" && (#{YAqgg6142Nn.BIzredhqtbr} == "1")'
  },
  {
    "Inidicator_Name": "NTD - Relapse I.T.O. Non Response Ambisome",
    "id": "esXrCNWRCPv",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "9" && (#{YAqgg6142Nn.BIzredhqtbr} == "2" || #{YAqgg6142Nn.BIzredhqtbr} == "3")'
  },
  {
    "Inidicator_Name": "NTD - Relapse I.T.O. Defaulted Ambisome",
    "id": "XBDrGidi0Eh",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "9" && (#{YAqgg6142Nn.BIzredhqtbr} == "4")'
  },
  {
    "Inidicator_Name": "NTD - Relapse I.T.O. Death Ambisome",
    "id": "Gv3sOiqWgyS",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && #{YAqgg6142Nn.Jjv8uLxHS80} == "9" && (#{YAqgg6142Nn.BIzredhqtbr} == "5")'
  },
  {
    "Inidicator_Name": "NTD - Others I.T.O. Initial Cure Ambisome",
    "id": "ABXKCK2hZUP",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && #{YAqgg6142Nn.Jjv8uLxHS80} == "9" && (#{YAqgg6142Nn.BIzredhqtbr} == "1")'
  },
  {
    "Inidicator_Name": "NTD - Others I.T.O. Non Response Ambisome",
    "id": "u0JBKqEKhRy",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && #{YAqgg6142Nn.Jjv8uLxHS80} == "9" && (#{YAqgg6142Nn.BIzredhqtbr} == "2" || #{YAqgg6142Nn.BIzredhqtbr} == "3")'
  },
  {
    "Inidicator_Name": "NTD - Others I.T.O. Defaulted Ambisome",
    "id": "m7d5pkqhP8m",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && #{YAqgg6142Nn.Jjv8uLxHS80} == "9" && (#{YAqgg6142Nn.BIzredhqtbr} == "4")'
  },
  {
    "Inidicator_Name": "NTD - Others I.T.O. Death Ambisome",
    "id": "zxEkaYNoROZ",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && #{YAqgg6142Nn.Jjv8uLxHS80} == "9" && (#{YAqgg6142Nn.BIzredhqtbr} == "5")'
  },
  {
    "Inidicator_Name": "NTD - Primary F.T.O. # Follow-Up At 6 Months",
    "id": "hfdyApbK6dn",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && (#{FnNVNqQvesu.rKUnWEvkP0v} !="")'
  },
  {
    "Inidicator_Name": "NTD - Primary F.T.O. Final Definitive Cure",
    "id": "dgb5ywnMgGM",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && (#{FnNVNqQvesu.rKUnWEvkP0v} =="1")'
  },
  {
    "Inidicator_Name": "NTD - Primary F.T.O. Relapse",
    "id": "U4mUEPwZ0MN",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && (#{FnNVNqQvesu.rKUnWEvkP0v} =="2")'
  },
  {
    "Inidicator_Name": "NTD - Primary F.T.O. Death",
    "id": "wNM0vdUAUox",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && (#{FnNVNqQvesu.rKUnWEvkP0v} =="3")'
  },
  {
    "Inidicator_Name": "NTD - Primary F.T.O. Lost To Follow-Up",
    "id": "hS2Jsof1cpS",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "1" && (#{FnNVNqQvesu.rKUnWEvkP0v} =="4")'
  },
  {
    "Inidicator_Name": "NTD - Relapse F.T.O. # Follow-Up At 6 Months",
    "id": "uKxVBqMZelr",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && (#{FnNVNqQvesu.rKUnWEvkP0v} !="")'
  },
  {
    "Inidicator_Name": "NTD - Relapse F.T.O. Final Definitive Cure",
    "id": "WmC4yh44K2L",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && (#{FnNVNqQvesu.rKUnWEvkP0v} =="1")'
  },
  {
    "Inidicator_Name": "NTD - Relapse F.T.O. Relapse",
    "id": "luO70jELg4R",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && (#{FnNVNqQvesu.rKUnWEvkP0v} =="2")'
  },
  {
    "Inidicator_Name": "NTD - Relapse F.T.O. Death",
    "id": "P3yCdYBSB5D",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && (#{FnNVNqQvesu.rKUnWEvkP0v} =="3")'
  },
  {
    "Inidicator_Name": "NTD - Relapse F.T.O. Lost To Follow-Up",
    "id": "hk5fHt0GsRY",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "2" && (#{FnNVNqQvesu.rKUnWEvkP0v} =="4")'
  },
  {
    "Inidicator_Name": "NTD - Others F.T.O. # Follow-Up At 6 Months",
    "id": "bBRKCfbiqo1",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && (#{FnNVNqQvesu.rKUnWEvkP0v} !="")'
  },
  {
    "Inidicator_Name": "NTD - Others F.T.O. Final Definitive Cure",
    "id": "fX2orhdZA40",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && (#{FnNVNqQvesu.rKUnWEvkP0v} =="1")'
  },
  {
    "Inidicator_Name": "NTD - Others F.T.O. Relapse",
    "id": "Xw8KYNSMmjp",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && (#{FnNVNqQvesu.rKUnWEvkP0v} =="2")'
  },
  {
    "Inidicator_Name": "NTD - Others F.T.O. Death",
    "id": "MSWsNLxJFnQ",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && (#{FnNVNqQvesu.rKUnWEvkP0v} =="3")'
  },
  {
    "Inidicator_Name": "NTD - Others F.T.O. Lost To Follow-Up",
    "id": "HjxKe2dHXTE",
    "filter": '#{k7U9lO69hVm.Tlj4JRxaFbV} == "4" && (#{FnNVNqQvesu.rKUnWEvkP0v} =="4")'
  }
]


pay_load = {
  "aggregationType": "COUNT",
  "publicAccess": "rw------",
  "lastUpdated": "2025-02-21T11:27:33.748",
  "expression": "1",
  "filter": "",
  "name": "",
  "analyticsType": "ENROLLMENT",
  "shortName": "",
  "program": {
    "id": "tYDQn4Gb0Ij"
  },
  "analyticsPeriodBoundaries": [
    {
      "lastUpdated": "2025-02-21T11:27:33.750",
      "created": "2025-02-21T11:27:33.750",
      "externalAccess": False,
      "analyticsPeriodBoundaryType": "BEFORE_END_OF_REPORTING_PERIOD",
      "boundaryTarget": "ENROLLMENT_DATE",
      "favorite": False,
      "offsetPeriods": 0,
      "access": {
        "read": True,
        "update": True,
        "externalize": True,
        "delete": True,
        "write": True,
        "manage": True
      },
    },
    {
      "lastUpdated": "2025-02-21T11:27:33.750",
      "created": "2025-02-21T11:27:33.750",
      "externalAccess": False,
      "analyticsPeriodBoundaryType": "AFTER_START_OF_REPORTING_PERIOD",
      "boundaryTarget": "ENROLLMENT_DATE",
      "favorite": False,
      "offsetPeriods": 0,
      "access": {
        "read": True,
        "update": True,
        "externalize": True,
        "delete": True,
        "write": True,
        "manage": True
      }
    }
  ]
}



headers = {  
  'Content-Type': 'application/json',
    'Accept': '*/*',
    'Accept-Language': 'en,en-US;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://histracker.health.go.ke/dhis-web-maintenance/index.html',
    'content-type': 'application/json',
    'Origin': 'https://histracker.health.go.ke',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
    'TE': 'Trailers',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    # 'Authorization': 'Bearer '
}
# Replace with your actual username and password
username = "xxxxxxxxxxx"
password = "xxxxxxxxxxx"

headers['Authorization'] = "Basic " + encodePassword(username, password)

i = 0
for data in data_to_create:
    urls=url + f"/{data['id']}"
    try:
        pay_load["name"] = data["Inidicator_Name"]
        pay_load["filter"] = data["filter"]
        pay_load["shortName"] = data['Inidicator_Name']

        payload = json.dumps(pay_load)
        print(payload)
        print("_________--------------------------------------------------------")
        print(pay_load)

        response = requests.request("PUT", urls, headers=headers, data=payload)

        print(response.text)
        # breakpoint()
        if response.status_code == 201 or response.status_code == 200:
            i += 1
            print("Program Indicator created successfully.")
        else:
            print(f"Failed to create Program Indicator. Status code: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    print(f"Processed {i} indicators so far.")
        
    # break
