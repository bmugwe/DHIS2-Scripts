import json
import pandas as pd

INPUT = "programs.json"
OUTPUT = "programs.xlsx"

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

programs = data.get("programs", [])

rows = []
for p in programs:
    name = p.get("name", "")
    pid = p.get("id", "")

    sharing_obj = p.get("sharing", {}) or {}
    owner = sharing_obj.get("owner", "")
    external = sharing_obj.get("external", "")
    public = sharing_obj.get("public", "")

    sharing_line = f"owner={owner}; external={external}; public={public}"

    # userGroups is a dict/map: { "<id>": {access, displayName, id}, ... }
    user_groups = sharing_obj.get("userGroups") or {}

    if not user_groups:
        # 1 row when there are no userGroups
        rows.append({
            "name": name,
            "id": pid,
            "sharing": sharing_line,
            "access": "",
            "displayName": "",
            "userGroupId": "",
        })
        continue

    # Otherwise: duplicate per userGroup
    for ug in user_groups.values():
        rows.append({
            "name": name,
            "id": pid,
            "sharing": sharing_line,
            "access": ug.get("access", ""),
            "displayName": ug.get("displayName", ""),
            "userGroupId": ug.get("id", ""),
        })

df = pd.DataFrame(rows, columns=["name", "id", "sharing", "access", "displayName", "userGroupId"])
df.to_excel(OUTPUT, index=False)
print(f"Wrote {OUTPUT} with {len(df)} rows")