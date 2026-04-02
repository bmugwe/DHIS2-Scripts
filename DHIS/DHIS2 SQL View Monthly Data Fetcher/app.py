#!/usr/bin/env python3
import os
import csv
import time
import json
import logging
import calendar
from io import StringIO
from pathlib import Path
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, jsonify, render_template, request, send_file


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.update(
        DHIS2_BASE_URL=os.getenv("KHIS", ""),  # no protocol; matches existing script
        DHIS2_USERNAME=os.getenv("KHIS_USERNAME", ""),
        DHIS2_PASSWORD=os.getenv("KHIS_PASSWORD", ""),
        OUTPUT_DIR=os.getenv("DHIS2_SQLVIEW_OUTPUT_DIR", "output"),
        MAX_WORKERS=int(os.getenv("DHIS2_SQLVIEW_MAX_WORKERS", "6")),
        TIMEOUT=int(os.getenv("DHIS2_SQLVIEW_TIMEOUT", "120")),
        PAGE_SIZE=int(os.getenv("DHIS2_SQLVIEW_PAGE_SIZE", "100000")),
        MAX_RETRIES=int(os.getenv("DHIS2_SQLVIEW_MAX_RETRIES", "3")),
        RETRY_DELAY_SECONDS=int(os.getenv("DHIS2_SQLVIEW_RETRY_DELAY_SECONDS", "5")),
    )

    @app.get("/")
    def index():
        return render_template("index.html")

    def _auth() -> HTTPBasicAuth:
        return HTTPBasicAuth(app.config["DHIS2_USERNAME"], app.config["DHIS2_PASSWORD"])

    def _api_base() -> str:
        base = app.config["DHIS2_BASE_URL"].strip().rstrip("/")
        if not base:
            raise ValueError("Missing KHIS base URL (set env var KHIS)")
        return f"https://{base}/api"

    @app.get("/api/datasets")
    def list_datasets():
        """
        Returns datasets: [{id, name}, ...]
        """
        url = f"{_api_base()}/dataSets.json"
        params = {"fields": "id,name", "paging": "false"}
        resp = requests.get(url, params=params, auth=_auth(), timeout=app.config["TIMEOUT"])
        resp.raise_for_status()
        payload = resp.json()
        data_sets = payload.get("dataSets", [])
        data_sets = sorted(data_sets, key=lambda d: (d.get("name") or "").lower())
        return jsonify({"dataSets": data_sets})

    @app.post("/api/dataelements")
    def dataelements_for_datasets():
        """
        Body: { "datasetIds": ["abc","def"] }
        Returns unique data elements across selected datasets:
          [{id, name}, ...]
        """
        body = request.get_json(force=True, silent=False) or {}
        dataset_ids = body.get("datasetIds") or []
        if not isinstance(dataset_ids, list) or not dataset_ids:
            return jsonify({"dataElements": []})

        api = _api_base()
        all_des: dict[str, dict] = {}
        for ds_id in dataset_ids:
            ds_url = f"{api}/dataSets/{ds_id}.json"
            params = {"fields": "id,name,dataSetElements[dataElement[id,name]]"}
            resp = requests.get(ds_url, params=params, auth=_auth(), timeout=app.config["TIMEOUT"])
            resp.raise_for_status()
            ds = resp.json()
            for dse in ds.get("dataSetElements", []) or []:
                de = (dse or {}).get("dataElement") or {}
                de_id = de.get("id")
                if de_id:
                    all_des[de_id] = {"id": de_id, "name": de.get("name") or de_id}

        data_elements = sorted(all_des.values(), key=lambda d: (d.get("name") or "").lower())
        return jsonify({"dataElements": data_elements})

    def _sqlview_url(sqlview_uid: str) -> str:
        base = app.config["DHIS2_BASE_URL"].strip().rstrip("/")
        return f"https://{base}/api/sqlViews/{sqlview_uid}/data.csv"

    def _fetch_month(
        *,
        url: str,
        auth: HTTPBasicAuth,
        year: int,
        month: int,
        date_start_var: str,
        date_end_var: str,
        dataelements_var: str | None,
        dataelements_value: str | None,
        cfg: dict,
    ) -> tuple[str, list[dict], list[str]]:
        last_day = calendar.monthrange(year, month)[1]
        date_start = date(year, month, 1).strftime("%Y-%m-%d")
        date_end = date(year, month, last_day).strftime("%Y-%m-%d")
        label = f"{year}-{month:02d}"

        var_list = [f"{date_start_var}:{date_start}", f"{date_end_var}:{date_end}"]
        if dataelements_var and dataelements_value:
            var_list.append(f"{dataelements_var}:{dataelements_value}")

        params = {
            "var": var_list,
            "pageSize": cfg["page_size"],
            "paging": "false",
        }

        for attempt in range(1, cfg["max_retries"] + 1):
            try:
                log.info(f"  → Fetching {label} (attempt {attempt})")
                resp = requests.get(url, params=params, auth=auth, timeout=cfg["timeout"])
                resp.raise_for_status()

                reader = csv.DictReader(StringIO(resp.text))
                rows = list(reader)
                fieldnames = reader.fieldnames or []
                for row in rows:
                    row.setdefault("_fetch_period", label)

                log.info(f"  ✓ {label} → {len(rows):,} rows")
                return label, rows, list(fieldnames)
            except requests.exceptions.HTTPError as e:
                status = getattr(e.response, "status_code", "unknown")
                log.warning(f"  ✗ {label} HTTP {status}: {e}")
            except requests.exceptions.RequestException as e:
                log.warning(f"  ✗ {label} Request error: {e}")

            if attempt < cfg["max_retries"]:
                time.sleep(cfg["retry_delay_seconds"])

        log.error(f"  ✗ {label} FAILED after {cfg['max_retries']} attempts — skipped.")
        return label, [], []

    def _fetch_year(
        *,
        url: str,
        auth: HTTPBasicAuth,
        year: int,
        date_start_var: str,
        date_end_var: str,
        dataelements_var: str | None,
        dataelements_value: str | None,
        cfg: dict,
    ) -> tuple[list[dict], list[str]]:
        year_rows: list[dict] = []
        all_fields: list[str] = []
        month_buffer: dict[str, list[dict]] = {}

        with ThreadPoolExecutor(max_workers=cfg["max_workers"]) as executor:
            futures = {
                executor.submit(
                    _fetch_month,
                    url=url,
                    auth=auth,
                    year=year,
                    month=month,
                    date_start_var=date_start_var,
                    date_end_var=date_end_var,
                    dataelements_var=dataelements_var,
                    dataelements_value=dataelements_value,
                    cfg=cfg,
                ): month
                for month in range(1, 13)
            }

            for future in as_completed(futures):
                label, rows, fields = future.result()
                month_buffer[label] = rows
                if fields and not all_fields:
                    all_fields = fields

        for month in range(1, 13):
            label = f"{year}-{month:02d}"
            year_rows.extend(month_buffer.get(label, []))

        return year_rows, all_fields

    def _save_csv(filepath: Path, rows: list[dict], fieldnames: list[str]) -> None:
        if not rows:
            return

        if "_fetch_period" in fieldnames:
            fieldnames = [f for f in fieldnames if f != "_fetch_period"] + ["_fetch_period"]
        elif rows and "_fetch_period" in rows[0]:
            fieldnames = list(fieldnames) + ["_fetch_period"]

        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

    @app.post("/api/run")
    def run_fetch():
        """
        Runs the SQL view fetch and writes per-year CSVs.

        Body:
          {
            "sqlviewUid": "m8oTYQH2MA3",
            "datasetIds": ["..."],            // not used in fetch; used for UI linking only
            "dataElementIds": ["...","..."],  // multiselect; used for variable substitution
            "dataElementsVarName": "dataelement_uids",
            "dataElementsDelimiter": ",",
            "dateStartVarName": "date_start",
            "dateEndVarName": "date_end",
            "yearStart": 2024,
            "yearEnd": 2026,
            "outputFilename": "my_output.csv"
          }
        """
        body = request.get_json(force=True, silent=False) or {}

        sqlview_uid = (body.get("sqlviewUid") or "").strip()
        if not sqlview_uid:
            return jsonify({"ok": False, "error": "sqlviewUid is required"}), 400

        year_start = int(body.get("yearStart"))
        year_end = int(body.get("yearEnd"))
        if year_end < year_start:
            return jsonify({"ok": False, "error": "yearEnd must be >= yearStart"}), 400

        output_filename = (body.get("outputFilename") or "").strip()
        if not output_filename:
            return jsonify({"ok": False, "error": "outputFilename is required"}), 400
        if "/" in output_filename or "\\" in output_filename:
            return jsonify({"ok": False, "error": "outputFilename must be a simple filename"}), 400
        if not output_filename.lower().endswith(".csv"):
            output_filename = f"{output_filename}.csv"

        date_start_var = (body.get("dateStartVarName") or "date_start").strip()
        date_end_var = (body.get("dateEndVarName") or "date_end").strip()

        data_elements_var = (body.get("dataElementsVarName") or "").strip() or None
        delimiter = body.get("dataElementsDelimiter") or ","
        if not isinstance(delimiter, str) or delimiter == "":
            delimiter = ","

        data_element_ids = body.get("dataElementIds") or []
        if not isinstance(data_element_ids, list):
            data_element_ids = []

        dataelements_value = None
        if data_elements_var and data_element_ids:
            # user asked: "pass a string of dataelement uids selected"
            # We send exactly this string as a SQL view variable value.
            dataelements_value = delimiter.join([str(x).strip() for x in data_element_ids if str(x).strip()])

        cfg = {
            "max_workers": app.config["MAX_WORKERS"],
            "max_retries": app.config["MAX_RETRIES"],
            "retry_delay_seconds": app.config["RETRY_DELAY_SECONDS"],
            "timeout": app.config["TIMEOUT"],
            "page_size": app.config["PAGE_SIZE"],
        }

        url = _sqlview_url(sqlview_uid)
        auth = _auth()

        out_dir = Path(app.config["OUTPUT_DIR"])
        per_year_files: list[str] = []

        combined_rows: list[dict] = []
        combined_fields: list[str] = []

        for year in range(year_start, year_end + 1):
            year_rows, fields = _fetch_year(
                url=url,
                auth=auth,
                year=year,
                date_start_var=date_start_var,
                date_end_var=date_end_var,
                dataelements_var=data_elements_var,
                dataelements_value=dataelements_value,
                cfg=cfg,
            )

            if fields and not combined_fields:
                combined_fields = fields

            year_path = out_dir / f"{Path(output_filename).stem}_{year}.csv"
            _save_csv(year_path, year_rows, list(combined_fields))
            per_year_files.append(str(year_path))
            combined_rows.extend(year_rows)

        combined_path = out_dir / output_filename
        _save_csv(combined_path, combined_rows, list(combined_fields))

        return jsonify(
            {
                "ok": True,
                "combinedFile": str(combined_path),
                "perYearFiles": per_year_files,
                "totalRows": len(combined_rows),
            }
        )

    @app.get("/api/download")
    def download_file():
        rel_path = (request.args.get("path") or "").strip()
        if not rel_path:
            return jsonify({"ok": False, "error": "path is required"}), 400

        # Only allow downloads from OUTPUT_DIR
        out_dir = Path(app.config["OUTPUT_DIR"]).resolve()
        target = Path(rel_path).expanduser()
        if not target.is_absolute():
            target = (Path.cwd() / target).resolve()
        else:
            target = target.resolve()

        try:
            target.relative_to(out_dir)
        except ValueError:
            return jsonify({"ok": False, "error": "download restricted to output dir"}), 403

        if not target.exists():
            return jsonify({"ok": False, "error": "file not found"}), 404

        return send_file(target, as_attachment=True, download_name=target.name)

    @app.get("/api/config")
    def get_config():
        # Safe subset so the UI can show if base URL is set
        return jsonify(
            {
                "baseUrlSet": bool(app.config["DHIS2_BASE_URL"].strip()),
                "usernameSet": bool(app.config["DHIS2_USERNAME"].strip()),
                "outputDir": app.config["OUTPUT_DIR"],
                "maxWorkers": app.config["MAX_WORKERS"],
            }
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=True)
