"""P1 · GEN2-PISOS-Y-ADENDAS-1: prueba sintética del medidor antes del COMMIT-1 (no toca el corpus).
ZIP fabricado con los miembros y columnas de la spec; medir() real; corrida0._valida_outputs sobre
(i) caso normal, (ii) entidad 32 sin personas (masa 0 -> P e IC nulos), (iii) estrato con una sola UPM,
(iv) códigos con cero a la izquierda y basura (lectura como entero; N-OTRO los cuenta)."""
import importlib.util, io, sys, tempfile, zipfile
from pathlib import Path
import numpy as np, yaml
RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "tools"))
import corrida0  # noqa: E402
D = RAIZ / "data/corrida0/CALC-ENCIG2023-CONFIANZA-PISOS-0001"
s = importlib.util.spec_from_file_location("m", D / "medidor.py"); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
spec = yaml.safe_load((D / "spec.yaml").read_text(encoding="utf-8"))
contrato = corrida0.contrato_ejecutable(spec)
contrato["parametros"]["bootstrap_replicas"] = 200  # sólo velocidad en la prueba

def fabrica(ruta, n=3000, seed=1):
    rng = np.random.default_rng(seed)
    items = [f"P11_1_{i}" for i in m.ITEMS]
    h11 = ["ID_PER", "ID_VIV", "CVE_ENT", "EST_DIS", "UPM_DIS", "FAC_P18"] + items
    hr = ["ID_PER", "SEXO", "EDAD", "NIV"]
    f11, fr = [",".join(h11)], [",".join(hr)]
    for k in range(n):
        ent = 1 + k % 31                        # entidad 32 sin personas
        est = f"{ent:02d}{k % 3}"
        upm = f"{est}{k % 7:04d}"
        if k % 997 == 0:
            est, upm = "999", "9990001"          # estrato con una sola UPM
        cods = [str(rng.choice([1, 2, 3, 4, 5, 9])) for _ in items]
        if k % 500 == 1: cods[0] = "01"         # cero a la izquierda: mismo código 1
        if k % 500 == 2: cods[1] = "x"          # basura: N-OTRO
        w = "" if k % 1000 == 3 else str(int(rng.integers(50, 900)))  # peso vacío -> fuera del marco
        f11.append(",".join([f"{k:08d}", f"V{k}", f"{ent:02d}", est, upm, w] + cods))
        if k % 800 != 5:                         # algunas personas sin enlace a residentes
            fr.append(",".join([f"{k:08d}", str(1 + k % 2), str([25, 37, 50, 70, 98, 17][k % 6]), str(k % 11)]))
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr(m.M_SEC11, ("﻿" + "\r\n".join(f11) + "\r\n").encode("utf-8"))
        z.writestr(m.M_RES, ("\n".join(fr) + "\n").encode("latin-1"))
        z.writestr("encig2023_03_sec_6.csv", "X\n1\n")

with tempfile.TemporaryDirectory() as t:
    zp = Path(t) / "encig.zip"; fabrica(zp)
    out = m.medir({m.PAYLOAD: {"ruta_absoluta": str(zp)}}, contrato)
    prob = corrida0._valida_outputs(spec, out)
    print("problemas:", prob[:5], "total", len(prob))
    assert prob == [], prob
    assert out["RESULT-ENCIG2023-CONF-I01-ENTIDAD-32-P"] is None and out["RESULT-ENCIG2023-CONF-I01-ENTIDAD-32-IC-LO"] is None
    assert out["RESULT-ENCIG2023-CONF-I01-ENTIDAD-32-N"] == 0
    assert out["RESULT-ENCIG2023-CONF-I02-N-OTRO"] == 6, out["RESULT-ENCIG2023-CONF-I02-N-OTRO"]
    assert out["RESULT-ENCIG2023-CONF-I01-N-OTRO"] == 0
    assert out["RESULT-ENCIG2023-CONF-FILAS-SEC11"] == 3000 and out["RESULT-ENCIG2023-CONF-FILAS-MARCO"] == 2997
    assert out["RESULT-ENCIG2023-CONF-FILAS-SIN-ENLACE-RESIDENTES"] == 4
    # determinismo: misma semilla -> mismos números
    out2 = m.medir({m.PAYLOAD: {"ruta_absoluta": str(zp)}}, contrato)
    assert all((out[k] == out2[k]) for k in out), "no determinista"
    # punto nacional y de una categoría contra cálculo directo, independiente del medidor
    import pandas as pd
    with zipfile.ZipFile(zp) as z:
        a = pd.read_csv(io.BytesIO(z.read(m.M_SEC11)), dtype=str, encoding="utf-8-sig")
        r = pd.read_csv(io.BytesIO(z.read(m.M_RES)), dtype=str, encoding="latin-1")
    a = a[pd.to_numeric(a.FAC_P18, errors="coerce") > 0]
    c = pd.to_numeric(a.P11_1_01, errors="coerce"); w = pd.to_numeric(a.FAC_P18)
    v = c.isin([1, 2, 3, 4])
    p_dir = (w[v] * c[v].isin([1, 2])).sum() / w[v].sum()
    assert abs(p_dir - out["RESULT-ENCIG2023-CONF-I01-NACIONAL-MX-P"]) < 1e-12, p_dir
    b = a.merge(r, on="ID_PER", how="left"); cb = pd.to_numeric(b.P11_1_03, errors="coerce"); wb = pd.to_numeric(b.FAC_P18)
    vb = cb.isin([1, 2, 3, 4]) & (b.SEXO == "2")
    p2 = (wb[vb] * cb[vb].isin([1, 2])).sum() / wb[vb].sum()
    assert abs(p2 - out["RESULT-ENCIG2023-CONF-I03-SEXO-MUJER-P"]) < 1e-12, p2
    assert int(vb.sum()) == out["RESULT-ENCIG2023-CONF-I03-SEXO-MUJER-N"]
    for k in [x for x in out if x.endswith("-P") and out[x] is not None]:
        lo, hi = out[k[:-2] + "-IC-LO"], out[k[:-2] + "-IC-HI"]
        assert lo is None or lo <= out[k] + 1e-9 and out[k] <= hi + 1e-9, k
    print("OK · ids:", len(out), "· I01 nacional P", out["RESULT-ENCIG2023-CONF-I01-NACIONAL-MX-P"],
          "IC", out["RESULT-ENCIG2023-CONF-I01-NACIONAL-MX-IC-LO"], out["RESULT-ENCIG2023-CONF-I01-NACIONAL-MX-IC-HI"],
          "· sin categoría EDAD", out["RESULT-ENCIG2023-CONF-EJE-EDAD-N-SIN-CATEGORIA"])
