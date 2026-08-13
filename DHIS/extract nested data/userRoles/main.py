import json
from tokenize import group
import pandas as pd

INPUT = "userRoles_authorities.json"      # change if your file name is different
OUTPUT = "user_roles_authorities.xlsx"

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

user_roles = data.get("userRoles", [])

rows = []
for role in user_roles:
    role_name = role.get("name", "")
    role_id = role.get("id", "")

    authorities = role.get("authorities") or []

    # If you want at least 1 row even when a role has no authorities, keep this block.
    # If you want 0 rows for such roles, delete this block.
    if not authorities:
        rows.append({
            "userRoleName": role_name,
            "userRoleId": role_id,
            "authority": "",
        })
        continue

    # One line per authority tied to the role
    for a in authorities:
        rows.append({
            "userRoleName": role_name,
            "userRoleId": role_id,
            "authority": a,
        })

df = pd.DataFrame(rows, columns=["userRoleName", "userRoleId", "authority"])
df.to_excel(OUTPUT, index=False)
print(f"Wrote {OUTPUT} with {len(df)} rows")