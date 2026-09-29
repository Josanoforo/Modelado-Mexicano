"""Exploración del esquema de llaves (solo esquema, sin microdato)."""
import pandas as pd

d = pd.read_csv("paquete/esquema-identidades.tsv", sep="\t", dtype=str, keep_default_na=False)
print(d.shape, d.llave.is_unique)
for c in ["unidad", "instrumento", "ola", "conducta", "eje", "dominio"]:
    print(c, d[c].value_counts().to_dict())
for (c, e), g in d.groupby(["conducta", "eje"]):
    print(c, e, len(g), sorted(g.segmento.unique()), sorted(g.ola.unique()))
bad = [r.llave for r in d.itertuples()
       if r.llave != f"RESULT-EDR-SUICIDIO-PISOS-{r.conducta.upper()}-{r.ola}-{r.eje}-{r.segmento}-P"]
print(len(bad), bad[:10])
