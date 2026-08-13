import os
import requests
import pandas as pd


BASE_URL = os.getenv("KHIS_URL")

USERNAME = os.getenv("KHIS_USERNAME", "")
PASSWORD = os.getenv("KHIS_PASSWORDee", "")

if not USERNAME or not PASSWORD:
    raise ValueError("Set KHIS_USERNAME and KHIS_PASSWORD environment variables.")


DATASETS = [
    {"uid": "Cyus2XHGDaq", "name": "MOH 731 B-Plus Summary for Vulnerable Population Rev 2023"},
    {"uid": "zxyaWpqkTlP", "name": "MOH 731 PLUS PrEP SUMMARY REPORTING TOOL(DICE)"},
    {"uid": "A01SsXzNsbD", "name": "MOH 731 PLUS PrEP SUMMARY REPORTING TOOL(for Facility reporting)"},
    {"uid": "VhX5RAfBVj6", "name": "MOH 731 Plus Summary for Key Populations Rev. 2023"},
    {"uid": "kAofV66isvC", "name": "MOH 731-1 HIV Counselling And Testing"},
    {"uid": "ptIUGFkE6jn", "name": "MOH 731-1 HIV Testing and Prevention services Revision 2018"},
    {"uid": "OaIjkmzEeNO", "name": "MOH 731-1 HIV Testing Services & PreP Revision 2023"},
    {"uid": "L7hIEAumRnQ", "name": "MOH 731-2 Elimination of Mother-to-Child Transmission Revision 2023"},
    {"uid": "yrYwif6R6sH", "name": "MOH 731-2 PMTCT"},
    {"uid": "xUesg8lcmDs", "name": "MOH 731-2 Prevention of Mother-to-Child Transmission Revision 2018"},
    {"uid": "EZtZKxqGoxZ", "name": "MOH 731-3 care and treatment"},
    {"uid": "GGgrU5QkjVs", "name": "MOH 731-3 Care and Treatment"},
    {"uid": "Vo4KDrUFwnA", "name": "MOH 731-3 HIV and TB treatment Revision 2018"},
    {"uid": "gtDFQTNBp7y", "name": "MOH 731-3 HIV and TB treatment Revision 2023"},
    {"uid": "bbMNLyKCnkm", "name": "MOH 731-4 Medical Male Circumcision Revision 2018"},
    {"uid": "SoiOUE3lOJd", "name": "MOH 731-4 Medical Male Circumcision Revision 2023"},
    {"uid": "NJHaY8wlURg", "name": "MOH 731-4 Voluntary Male Circumcision"},
    {"uid": "do43iCbnDrs", "name": "MOH 731-5 Post Exposure Prophylaxis Revision 2018"},
    {"uid": "wBrjU4hqULi", "name": "MOH 731-5 Post Exposure Prophylaxis Revision 2023"},
    {"uid": "UeBJcYEoHeA", "name": "MOH 731-5 Post-Exposure Prophylaxis"},
    {"uid": "IH4pYzRqTSE", "name": "MOH 731-6 Blood Safety"},
    {"uid": "WwALTN8OS22", "name": "MOH 731-6 Medically Assisted Therapy (MAT) REVISION 2023"},
    {"uid": "RRC2sWfhVqF", "name": "MOH 731-6 Methadone Assisted Therapy revision 2018"},
    {"uid": "UQBYJ3QMPZ7", "name": "MOH 731-HIV-TESTING AND COUNSELLING"},
    {"uid": "VBQoIaVHKbk", "name": "MOH 731Plus Key Populations Monthly Summary"},
    {"uid": "FJDCRLr5lAn", "name": "MOH 731Plus Key Populations Monthly Summary (For Facilities)"},
]

PERIODS = ["202601", "202602", "202603"]

OU = (
    "HfVjCurKxh2;Eey8fT4Im3y;R6f9znhg37c;j8o6iO4Njsi;KGHhQ5GLd4k;"
    "sANMZ3lpqGs;mThvosEflAU;ob6SxuRcqU4;ptWVfaCIdVx;uyOrcHZBpW0;"
    "mYZacFNIB3h;NjWSbQTwys4;xuFdFy6t9AH;T4urHM47nlm;t0J75eHKxz5;"
    "MqnLxQBigG0;PFu8alU2KWG;Ulj33KBau7V;vvOK1BxTbet;o36zCRjSd4G;"
    "Y52XNJ50hYb;bzOfj0iwfDH;sPkRcDvhGWA;N7YETT3A9r1;ahwTMNAJvrL;"
    "yhCUgGcCcOo;CeLsrJOH0g9;nK0A12Q7MvS;XWALbfAPa6n;tAbBVBbueqD;"
    "ihZsJ8alvtb;Hsk1YV8kHkT;HMNARUV2CW4;BjC1xL40gHo;Tvf1zgVZ0K4;"
    "pZqQRRW7PHP;BoDytkJQ4Qi;fVra3Pwta0Q;qKzosKQPl6G;uepLTG8wGWJ;"
    "JsH2bnvNt2d;nrI2khZx3d0;QyGNX2DpR4h;kphDeKClFch;jkG3zaihdSs;"
    "kqJ83J2D72s;u4t9H8XyU9P;wsBsC6gjHvn"
)

REPORTING_METRICS = [
    "ACTUAL_REPORTS",
    "EXPECTED_REPORTS",
    "REPORTING_RATE",
    "ACTUAL_REPORTS_ON_TIME",
    "REPORTING_RATE_ON_TIME",
]

FINAL_COLUMNS = [
    "dataset_id",
    "dataset_name",
    "period",
    "organisationunitid",
    "organisationunitname",
    "organisationunitcode",
    "organisationunitdescription",
    "actual_reports",
    "expected_reports",
    "reporting_rate",
    "actual_reports_on_time",
    "reporting_rate_on_time",
]


def build_dx_dimension(dataset_id: str) -> str:
    return ";".join(f"{dataset_id}.{metric}" for metric in REPORTING_METRICS)


def fetch_reporting_rates(session: requests.Session, dataset_id: str, period: str) -> dict:
    params = {
        "dimension": [
            f"dx:{build_dx_dimension(dataset_id)}",
            f"ou:{OU}",
        ],
        "columns": "dx",
        "rows": "ou",
        "tableLayout": "true",
        "hideEmptyRows": "true",
        "displayProperty": "SHORTNAME",
        "includeNumDen": "false",
        "filter": f"pe:{period}",
    }

    response = session.get(
        f"{BASE_URL}/api/analytics.json",
        params=params,
        timeout=60,
    )

    response.raise_for_status()
    return response.json()


def analytics_to_dataframe(data: dict, dataset: dict, period: str) -> pd.DataFrame:
    rows = data.get("rows", [])
    headers = data.get("headers", [])

    if not rows:
        return pd.DataFrame(columns=FINAL_COLUMNS)

    raw_columns = [h.get("column", h.get("name", "")) for h in headers]
    df = pd.DataFrame(rows, columns=raw_columns)

    expected_dhis2_columns_count = 9

    if len(df.columns) != expected_dhis2_columns_count:
        print(
            f"Column mismatch for dataset={dataset['uid']} period={period}. "
            f"Expected {expected_dhis2_columns_count}, got {len(df.columns)}"
        )
        print(df.columns.tolist())
        return pd.DataFrame(columns=FINAL_COLUMNS)

    df.columns = [
        "organisationunitid",
        "organisationunitname",
        "organisationunitcode",
        "organisationunitdescription",
        "actual_reports",
        "expected_reports",
        "reporting_rate",
        "actual_reports_on_time",
        "reporting_rate_on_time",
    ]

    df.insert(0, "period", period)
    df.insert(0, "dataset_name", dataset["name"])
    df.insert(0, "dataset_id", dataset["uid"])

    return df[FINAL_COLUMNS]


def main():
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    session.headers.update({
        "Accept": "application/json",
        "User-Agent": "Python Requests",
    })

    all_frames = []

    for dataset in DATASETS:
        for period in PERIODS:
            print(f"Fetching: {dataset['name']} | {period}")

            try:
                data = fetch_reporting_rates(session, dataset["uid"], period)
                df = analytics_to_dataframe(data, dataset, period)

                if df.empty:
                    print(f"No usable data: {dataset['name']} | {period}")
                    continue

                all_frames.append(df)

            except requests.HTTPError as e:
                print(f"HTTP error: {dataset['name']} | {period} | {e}")

            except requests.RequestException as e:
                print(f"Request error: {dataset['name']} | {period} | {e}")

    final_df = (
        pd.concat(all_frames, ignore_index=True)
        if all_frames
        else pd.DataFrame(columns=FINAL_COLUMNS)
    )

    final_df.to_csv("reporting_rates_all_datasets_all_periods.csv", index=False)

    print("Done.")
    print(final_df.head())


if __name__ == "__main__":
    main()