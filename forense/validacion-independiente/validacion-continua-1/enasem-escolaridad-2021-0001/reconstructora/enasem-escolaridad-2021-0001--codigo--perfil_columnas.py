"""Perfil de dominio de las seis columnas autorizadas (solo conteos y agregados, sin filas ni estimaciones)."""
import pandas as pd

CSV = "paquete/datos/sect_a_2021.csv"
COLS = ["YRSCHOOL", "SEX_21", "AGE_21", "FACTORI_21", "EST_DIS_21", "UPM_DIS_21"]

df = pd.read_csv(CSV, usecols=COLS, dtype=str, keep_default_na=False)
print("filas", len(df))
for c in COLS:
    s = df[c].str.strip()
    num = pd.to_numeric(s, errors="coerce")
    print(c, "vacios", int((s == "").sum()), "no_numericos", int(num.isna().sum() - (s == "").sum()),
          "min", num.min(), "max", num.max(), "distintos", s.nunique())
print(df["SEX_21"].str.strip().value_counts(dropna=False).sort_index().to_dict())
print(df["EST_DIS_21"].str.strip().value_counts(dropna=False).sort_index().to_dict())
ys = df["YRSCHOOL"].str.strip()
print("YRSCHOOL lexemas", sorted(ys.unique().tolist())[:60])
a = pd.to_numeric(df["AGE_21"].str.strip(), errors="coerce")
print("AGE_21 >120:", a[a > 120].value_counts().to_dict(), "<50:", int((a < 50).sum()))
upm = df[["EST_DIS_21", "UPM_DIS_21"]].apply(lambda s: s.str.strip())
upm = upm[(upm.EST_DIS_21 != "") & (upm.UPM_DIS_21 != "")]
print("UPM en >1 estrato:", int((upm.groupby("UPM_DIS_21").EST_DIS_21.nunique() > 1).sum()))
print("UPM por estrato:", upm.groupby("EST_DIS_21").UPM_DIS_21.nunique().to_dict())
w = pd.to_numeric(df["FACTORI_21"].str.strip(), errors="coerce")
print("FACTORI_21 <=0:", int((w <= 0).sum()), "NaN:", int(w.isna().sum()))
