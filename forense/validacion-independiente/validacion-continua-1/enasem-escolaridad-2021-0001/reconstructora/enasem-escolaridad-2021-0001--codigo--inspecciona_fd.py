"""Inspección del descriptor (FD): imprime las filas que documentan las seis variables usadas."""
import re
import pandas as pd

FD = "paquete/docs/enasem_2021_fd.xlsx"
VARS = r"\b(YRSCHOOL|SEX_21|AGE_21|FACTORI_21|EST_DIS_21|UPM_DIS_21)\b"

hojas = pd.read_excel(FD, sheet_name=None, header=None)
print(list(hojas))
for nombre, df in hojas.items():
    for i, r in df.iterrows():
        t = " | ".join(str(v) for v in r.values if pd.notna(v))
        if re.search(VARS, t):
            print(nombre, i, t[:400])
