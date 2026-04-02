# Flask app: DHIS2 SQL View Data Fetcher

This adds a small Flask web UI to:

- Fetch and multi-select **Datasets**
- Fetch and multi-select **Data Elements** for the selected datasets
- Run a **SQL View** query for each month across a year range
- Pass selected data elements as a **single string variable** to the SQL View
- Write **per-year** CSVs plus a **combined** CSV

## Setup

From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure

Set env vars (required):

- `KHIS`: DHIS2 host (no protocol). Example: `hiskenya.org`
- `KHIS_USERNAME`
- `KHIS_PASSWORD`

Optional:

- `DHIS2_SQLVIEW_OUTPUT_DIR` (default: `output`)
- `DHIS2_SQLVIEW_MAX_WORKERS` (default: `6`)
- `DHIS2_SQLVIEW_TIMEOUT` (default: `120`)
- `DHIS2_SQLVIEW_PAGE_SIZE` (default: `100000`)

## Run

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

## Notes

- **Data element key**: the UI uses the DHIS2 **dataElement `id`** as the option value (as requested).
- **SQL View variable for data elements**: set `data elements var` to match your SQL View variable name, and choose a delimiter (default `,`).
- The SQL View must accept the variables `date_start` and `date_end` (or whatever you set in the UI).

