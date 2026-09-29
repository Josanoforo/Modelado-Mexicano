"""Conteos agregados de códigos (sin imprimir filas) de las columnas autorizadas."""
import pandas as pd

COLS = ["P8_1", "P9_1", "P7_1", "P7_1A", "NIV", "P4_2", "P4_7", "P4_4", "ENT",
        "P4_1", "FACTOR", "EST_DIS", "UPM_DIS"]
d = pd.read_csv("paquete/datos/tmodulo.csv", usecols=COLS, dtype=str,
                keep_default_na=False)
print("filas", len(d))
for c in COLS:
    vc = d[c].str.strip().value_counts(dropna=False)
    if c in ("FACTOR", "UPM_DIS", "EST_DIS", "P4_1"):
        print(c, "distintos", vc.size, "vacios", int((d[c].str.strip() == "").sum()),
              "longitudes", d[c].str.len().value_counts().to_dict())
    else:
        print(c, vc.sort_index().to_dict())
e = pd.to_numeric(d["P4_1"], errors="coerce")
print("P4_1 min/max", e.min(), e.max(), "fuera 15-96", int(((e < 15) | (e > 96) | e.isna()).sum()))
f = pd.to_numeric(d["FACTOR"], errors="coerce")
print("FACTOR<=0 o NA", int(((f <= 0) | f.isna()).sum()))
