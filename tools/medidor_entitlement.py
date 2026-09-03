#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA35-L9 · REGLAS-ACTIVOS-L3 — pieza (c).

R7.8 `civico.transferencia.entitlement_derecho` — ENCUCI 2020.
La regla dice que la transferencia no condicionada **se vive como derecho**.
Lo que hasta hoy faltaba no era el beneficio sino la PERCEPCION: `MAESTRA33-E18`
descarto ENASEM porque mide afiliacion, no percepcion. ENCUCI 2020 `AP6_9`
pregunta exactamente la dicotomia de la regla:

    6.9 ... respecto a los programas sociales ...
        1 = Los programas sociales son una ayuda que da el gobierno   (favor)
        2 = Los programas sociales son un derecho de los ciudadanos   (derecho)
        3 = Ninguna     9 = No sabe / no responde

y `AP6_10` da el antecedente (beneficiario en los ultimos 12 meses).
`AP6_11` (le pidieron algo a cambio) esta gateada dentro de `AP6_10 == 1`.

Diseno: `FAC_SEL` (persona), `EST_DIS`, `UPM_DIS`, todos en `ENCUCI_2020_SD.dbf`;
se unen a la seccion 6 por `ID_PER`.

Uso:
    python3 tools/medidor_entitlement.py --censo
"""
import argparse, hashlib, json, os, sys, zipfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tests"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dbfmini  # noqa: E402

ZIP = "data/raw/BD_ENCUCI2020_dbf.zip"
SEC = "ENCUCI_2020_SEC_6_7_8.dbf"
SD = "ENCUCI_2020_SD.dbf"
PAYLOAD_ID = "encuci2020_bd_dbf"


def _extrae():
    tmp = os.environ.get("TMPDIR", "/tmp")
    z = zipfile.ZipFile(ZIP)
    for n in (SEC, SD):
        d = os.path.join(tmp, n)
        if not os.path.exists(d):
            z.extract(n, tmp)
    return os.path.join(tmp, SEC), os.path.join(tmp, SD)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _n(v):
    """AP6_* llega como float ('1.000000000000000') o como str. -> int|None."""
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


def carga():
    """Une seccion 6 con el diseno por ID_PER. Devuelve lista de dicts.

    El join se censa, no se supone: si `emparejadas` no es igual al numero de
    filas de la seccion 6, el lector devolvio vacio en silencio y hay que parar
    antes de estimar nada."""
    psec, psd = _extrae()
    dis = {}
    for r in dbfmini.read_dbf(psd, wanted_fields=["ID_PER", "FAC_SEL", "EST_DIS",
                                                  "UPM_DIS", "SEXO", "EDAD"]):
        dis[str(r["ID_PER"]).strip()] = r
    filas, sin_par = [], 0
    for r in dbfmini.read_dbf(psec, wanted_fields=["ID_PER", "AP6_9", "AP6_10", "AP6_11"]):
        k = str(r["ID_PER"]).strip()
        d = dis.get(k)
        if d is None:
            sin_par += 1
            continue
        try:
            w = float(str(d["FAC_SEL"]).strip())
        except (ValueError, TypeError):
            sin_par += 1
            continue
        filas.append({"est": str(d["EST_DIS"]).strip(), "upm": str(d["UPM_DIS"]).strip(),
                      "w": w, "ap6_9": _n(r["AP6_9"]), "ap6_10": _n(r["AP6_10"]),
                      "ap6_11": _n(r["AP6_11"])})
    return filas, sin_par, psec, psd


def censo():
    filas, sin_par, psec, psd = carga()
    print(f"ENCUCI 2020 · {PAYLOAD_ID}")
    print(f"  zip sha256 : {sha256(ZIP)}")
    print(f"  {SEC}: {len(filas) + sin_par} filas leidas · emparejadas con diseno: "
          f"{len(filas)} · sin par: {sin_par}")
    if sin_par:
        print("  ⚠ GUARDIA: hay filas sin diseno; el join NO es total.")
    for var in ("ap6_9", "ap6_10", "ap6_11"):
        marg = {}
        for f in filas:
            marg[f[var]] = marg.get(f[var], 0) + 1
        val = sum(v for k, v in marg.items() if k is not None)
        print(f"    {var:8s} n_val={val:6d}  marginal={dict(sorted(marg.items(), key=lambda x: (x[0] is None, x[0])))}")
    est = {f["est"] for f in filas}
    upm = {(f["est"], f["upm"]) for f in filas}
    print(f"  diseno: estratos={len(est)}  UPM={len(upm)}  "
          f"UPM/estrato mediana={sorted([sum(1 for e, _ in upm if e == x) for x in est])[len(est) // 2]}")
    print(f"  ponderador FAC_SEL: min={min(f['w'] for f in filas):.0f} "
          f"max={max(f['w'] for f in filas):.0f} "
          f"poblacion_expandida={sum(f['w'] for f in filas):,.0f}")
    print("\n  DENOMINADOR del eje (AP6_10), sin tocar AP6_9:")
    for k in (1, 2, 9, None):
        n = sum(1 for f in filas if f["ap6_10"] == k)
        if n:
            print(f"    AP6_10={k}: n={n}")
    return filas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--censo", action="store_true")
    ap.add_argument("--mide", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.censo:
        censo()
        return
    ap.print_help()


if __name__ == "__main__":
    main()
