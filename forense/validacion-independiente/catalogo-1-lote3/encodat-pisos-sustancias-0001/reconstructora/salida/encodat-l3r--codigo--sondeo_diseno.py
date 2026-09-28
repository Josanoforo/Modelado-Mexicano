"""Sondeo de diseño: solo conteos del join y de la estructura estrato/UPM. No estima conductas.

Uso: python3 salida/codigo/sondeo_diseno.py (desde el directorio de trabajo).
"""
import numpy as np
import pandas as pd

IND = "paquete/datos/ENCODAT_2016_2017_Individual.dta"
HOG = "paquete/datos/ENCODAT_2016_2017_Hogar.dta"

ind = pd.read_stata(IND, columns=["id_pers", "ds3", "ponde_ss"], convert_categoricals=False)
hog = pd.read_stata(HOG, columns=["id_hogar", "est_var", "code_upm", "estrato"], convert_categoricals=False)

print("ind filas", len(ind), "id_pers duplicados", int(ind.id_pers.duplicated(keep=False).sum()))
print("id_pers longitudes", ind.id_pers.str.len().value_counts().to_dict())
print("hog filas", len(hog), "id_hogar duplicados", int(hog.id_hogar.duplicated(keep=False).sum()))
print("id_hogar longitudes", hog.id_hogar.str.len().value_counts().to_dict())
print("est_var nulos", int(hog.est_var.isna().sum()), "no enteros",
      int((hog.est_var.dropna() != np.floor(hog.est_var.dropna())).sum()))
print("code_upm vacíos", int((hog.code_upm == "").sum()), "longitudes", hog.code_upm.str.len().value_counts().to_dict())
print("estrato", hog.estrato.value_counts(dropna=False).to_dict())

base = ind[(ind.ds3 >= 12) & (ind.ds3 <= 65)]
print("base edad", len(base), "ds3 nulos", int(ind.ds3.isna().sum()))
pw = np.isfinite(base.ponde_ss) & (base.ponde_ss > 0)
print("peso válido", int(pw.sum()), "inválido", int((~pw).sum()))
b = base[pw].copy()
b["id_hogar"] = b.id_pers.str[:20]
m = b.merge(hog, on="id_hogar", how="left", indicator=True)
print("join", m["_merge"].value_counts().to_dict())
ok = m[(m["_merge"] == "both") & m.est_var.notna() & (m.code_upm != "")]
pares = ok[["est_var", "code_upm"]].drop_duplicates()
nh = pares.groupby("est_var").size()
print("n pares", len(pares), "n estratos", len(nh), "singletons", int((nh == 1).sum()),
      "n_h distribución", nh.value_counts().sort_index().to_dict())
print("UPM en más de un estrato", int((pares.groupby("code_upm").size() > 1).sum()))
