"""Inspección del descriptor FD (documentación, no microdato)."""
import pandas as pd

FD = "paquete/docs/endiseg_2021_fd.xlsx"
VARS = {"P4_1", "P4_2", "P4_4", "P4_7", "NIV", "P7_1", "P7_1A", "P8_1", "P9_1",
        "ENT", "EST_DIS", "UPM_DIS", "FACTOR"}

x = pd.read_excel(FD, sheet_name=None, header=None, dtype=str)
print(list(x))
t = x["TMODULO"]
print(t.shape)
print(t.head(6).to_string())
activo = False
for i, r in t.iterrows():
    vals = [str(v).strip() for v in r if pd.notna(v)]
    if not vals:
        continue
    nombres = [v for v in vals if v in VARS]
    col0 = [str(v).strip() for v in r.iloc[:4] if pd.notna(v)]
    if nombres:
        activo = True
    elif activo and any(c.isupper() and "_" in c and c not in VARS for c in col0):
        activo = False
    if activo:
        print(i, " | ".join(vals))
