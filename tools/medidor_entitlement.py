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
from medidor_clientelismo_lapop import _celda, _dif, REPLICAS, SEED  # noqa: E402

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
                                                  "UPM_DIS", "SEXO", "EDAD", "NIV"]):
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
                      "ap6_11": _n(r["AP6_11"]), "sexo": _n(d["SEXO"]),
                      "edad": _n(d["EDAD"]), "niv": str(d["NIV"]).strip()})
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


# ─────────────────────── P1 · medicion (COMMIT-2) ───────────────────────
# Ejecuta la spec congelada §5. Nada se decide aqui.

# spec §0.5, guardias de lectura con valor esperado
GUARDIA_FILAS = 21519
GUARDIA_AP6_9 = {1: 8685, 2: 12183, 3: 299, 9: 352}

# spec §1.5, tramos de escolaridad de ENCUCI
TRAMO_NIV = {"00": "hasta primaria", "01": "hasta primaria", "02": "hasta primaria",
             "03": "secundaria",
             "04": "media superior", "05": "media superior",
             "06": "media superior", "07": "media superior",
             "08": "superior", "09": "superior"}


def _tramo_edad(e):
    if e is None:
        return None
    return "15-29" if e <= 29 else "30-44" if e <= 44 else "45-59" if e <= 59 else "60+"


def mide(ruta_json=None):
    filas, sin_par, _a, _b = carga()
    if len(filas) != GUARDIA_FILAS or sin_par != 0:
        raise SystemExit(f"PARO (guardia §0.5): {len(filas)} emparejadas, {sin_par} sin par; "
                         f"esperado {GUARDIA_FILAS} y 0.")
    marg = {}
    for f in filas:
        marg[f["ap6_9"]] = marg.get(f["ap6_9"], 0) + 1
    if {k: v for k, v in marg.items() if k in GUARDIA_AP6_9} != GUARDIA_AP6_9:
        raise SystemExit(f"PARO (guardia §0.5): marginal AP6_9 = {marg}, "
                         f"esperado {GUARDIA_AP6_9}")
    print("guardias de lectura §0.5: OK")

    # universo del desenlace: AP6_9 in {1,2}; 3 y 9 quedan fuera (spec §5)
    univ = [f for f in filas if f["ap6_9"] in (1, 2)]
    cobertura = len(univ) / len(filas)

    def tup(sub):
        return [(f["est"], f["upm"], f["w"], 1 if f["ap6_9"] == 2 else 0) for f in sub]

    ben = tup([f for f in univ if f["ap6_10"] == 1])
    nob = tup([f for f in univ if f["ap6_10"] == 2])
    c_ben, c_nob = _celda(ben, "derecho | beneficiario"), _celda(nob, "derecho | no beneficiario")
    delta = _dif(ben, nob, "Δ_entitlement", c_ben, c_nob)

    # eje ANIDADO: AP6_11, solo dentro de AP6_10 == 1 (spec §5)
    ped = tup([f for f in univ if f["ap6_10"] == 1 and f["ap6_11"] == 1])
    nped = tup([f for f in univ if f["ap6_10"] == 1 and f["ap6_11"] == 2])
    c_ped, c_nped = _celda(ped, "derecho | le pidieron algo"), _celda(nped, "derecho | no le pidieron")
    d_anid = _dif(ped, nped, "Δ_condicionalidad (ANIDADO)", c_ped, c_nped)

    # ejes secundarios no anidados
    sec = {}
    sec["sexo"] = {lab: _celda(tup([f for f in univ if f["sexo"] == k]), f"sexo={lab}")
                   for k, lab in ((1, "hombre"), (2, "mujer"))}
    sec["edad"] = {lab: _celda(tup([f for f in univ if _tramo_edad(f["edad"]) == lab]),
                               f"edad={lab}")
                   for lab in ("15-29", "30-44", "45-59", "60+")}
    sec["escolaridad"] = {lab: _celda(tup([f for f in univ if TRAMO_NIV.get(f["niv"]) == lab]),
                                      f"escolaridad={lab}")
                          for lab in ("hasta primaria", "secundaria", "media superior", "superior")}

    out = {"acto": "MAESTRA35-L9 · REGLAS-ACTIVOS-L3", "pieza": "c",
           "reglas": ["R7.8"], "id_modelo": ["civico.transferencia.entitlement_derecho"],
           "fuente": "ENCUCI 2020", "spec": "§5",
           "payload": {"id": PAYLOAD_ID, "sha256_zip": sha256(ZIP)},
           "estimador": f"proporcion ponderada (FAC_SEL); IC95 bootstrap de conglomerado, "
                        f"{REPLICAS} replicas, seed {SEED}, UPM_DIS dentro de EST_DIS",
           "universo": "AP6_9 in {1,2}; se excluyen 3=Ninguna y 9=NS/NR",
           "n_universo": len(univ), "cobertura": cobertura,
           "universo_restringido": cobertura < 0.90,
           "desenlace": "AP6_9 == 2 (los programas sociales son un derecho de los ciudadanos)",
           "eje_principal": {"beneficiario": c_ben, "no_beneficiario": c_nob, "delta": delta},
           "eje_anidado_AP6_11": {"le_pidieron": c_ped, "no_le_pidieron": c_nped,
                                  "delta": d_anid,
                                  "nota": "anidado dentro de AP6_10==1; no puede voltear "
                                          "el veredicto del eje principal (spec §5.1)"},
           "ejes_secundarios": sec,
           "reserva": "asociacion transversal: no separa que el programa cambie la "
                      "percepcion de que quien ya pensaba asi se inscribiera mas"}
    if ruta_json:
        json.dump(out, open(ruta_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("escrito", ruta_json)

    def f(c):
        if c.get("estado") != "ESTIMADA":
            return f"NO-ESTIMABLE ({c.get('motivo')})"
        if "p" in c:
            return f"p={c['p']:.6f} IC95=[{c['ic95'][0]:.6f},{c['ic95'][1]:.6f}] n={c['n']} num={c['numerador']}"
        return (f"d={c['d']:+.6f} IC95=[{c['ic95'][0]:+.6f},{c['ic95'][1]:+.6f}] "
                f"{'EXCLUYE 0' if c['excluye_cero'] else 'contiene 0'}")

    print(f"\n{'=' * 74}\nPIEZA c · R7.8 · ENCUCI 2020")
    print(f"  universo {len(univ)} · cobertura {cobertura:.4%} · restringido={cobertura < 0.90}")
    print(f"  {'beneficiario':24s} {f(c_ben)}")
    print(f"  {'no beneficiario':24s} {f(c_nob)}")
    print(f"  {'Δ_entitlement':24s} {f(delta)}")
    print(f"  ANIDADO AP6_11:")
    print(f"    {'le pidieron algo':22s} {f(c_ped)}")
    print(f"    {'no le pidieron':22s} {f(c_nped)}")
    print(f"    {'Δ_condicionalidad':22s} {f(d_anid)}")
    for eje, cs in sec.items():
        print(f"  eje {eje}")
        for lab, c in cs.items():
            print(f"    {lab:18s} {f(c)}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--censo", action="store_true")
    ap.add_argument("--mide", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.censo:
        censo()
        return
    if a.mide:
        mide(a.json)
        return
    ap.print_help()


if __name__ == "__main__":
    main()
