#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA35-L9 · REGLAS-ACTIVOS-L3 — pieza (d).

R1.5 `dinero.ahorro.seguro_deposito_atenua_aversion` — ENIF 2024.
    "SI existe seguro de deposito visible o marca confiable ENTONCES se atenua
     la aversion" — PORQUE G1 + diseno — [MEDIA].

El moderador que el `SI` de la regla nombra ya estaba identificado en el propio
modelo (`canon/modelo-decision-v4_0.md:283`): ENIF `P5_23`/`P5_24` mide
conocimiento de la proteccion de depositos (IPAB). Lo que ese pasaje descarto
fue usarlo como medida de AVERSION — aqui se usa como lo que es, el moderador.

    P5_23  Los bancos ... pueden cerrar o quebrar, ¿sabe si en ese caso
           [sus ahorros estan protegidos]?     1 = Si   2 = No
    P5_24_1 ... ¿nombres de las instituciones que aseguran los ahorros? IPAB
           0 = No se menciono  1 = Si se menciono  b = Blanco por secuencia
    P5_20  ¿Cual es la razon principal por la que no tiene una cuenta o tarjeta?
           03 = No confia en instituciones financieras o le dan mal servicio
           05 = Prefiere otras formas de ahorro (tanda, guardar en su casa)

Cobertura censada (P0): `P5_23` se pregunta al universo COMPLETO (13 502 / 100 %)
y `P5_20` a los 2 970 sin cuenta — el cruce no es degenerado. `P5_24_*` SI esta
anidada dentro del "Si" de `P5_23` (4 136), asi que va como sensibilidad, nunca
como moderador principal.

Diseno: `FAC_PER`, `EST_DIS`, `UPM_DIS` en la misma tabla `TMODULO.csv`.

Uso:
    python3 tools/medidor_seguro_deposito_enif24.py --censo
"""
import argparse, csv, hashlib, io, json, os, sys, zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ZIP = "data/raw/enif_2024_bd_csv.zip"
TABLA = "TMODULO.csv"
PAYLOAD_ID = "enif_2024_enif_2024_bd_csv"
CAMPOS = ["FAC_PER", "EST_DIS", "UPM_DIS", "P5_20", "P5_23",
          "P5_24_1", "P5_24_9"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def carga():
    """Lee TMODULO.csv con el modulo csv de la biblioteca estandar sobre un CSV
    de verdad (coma, latin-1). El aviso de la casa sobre `csv` aplica a los TSV
    del programa, no a este payload — aqui el delimitador es el nativo."""
    z = zipfile.ZipFile(ZIP)
    with z.open(TABLA) as f:
        texto = io.TextIOWrapper(f, encoding="latin-1", newline="")
        r = csv.DictReader(texto)
        faltan = [c for c in CAMPOS if c not in r.fieldnames]
        if faltan:
            raise SystemExit(f"PARO: {TABLA} no trae {faltan}")
        return [{c: (row[c] or "").strip() for c in CAMPOS} for row in r]


def censo():
    filas = carga()
    print(f"ENIF 2024 · {PAYLOAD_ID}")
    print(f"  zip sha256 : {sha256(ZIP)}")
    print(f"  {TABLA}: {len(filas)} filas (unidad = persona de 18 a 70 anios)")
    for c in ("P5_23", "P5_20", "P5_24_1", "P5_24_9"):
        marg = {}
        for f in filas:
            marg[f[c] or "(vacio)"] = marg.get(f[c] or "(vacio)", 0) + 1
        nv = sum(v for k, v in marg.items() if k != "(vacio)")
        print(f"    {c:9s} n_val={nv:6d} ({nv / len(filas):5.1%})  "
              f"marginal={dict(sorted(marg.items()))}")
    est = {f["EST_DIS"] for f in filas}
    upm = {(f["EST_DIS"], f["UPM_DIS"]) for f in filas}
    ws = [float(f["FAC_PER"]) for f in filas if f["FAC_PER"]]
    print(f"  diseno: estratos={len(est)}  UPM={len(upm)}  "
          f"FAC_PER min={min(ws):.0f} max={max(ws):.0f} "
          f"poblacion_expandida={sum(ws):,.0f}")
    # GUARDIA de universo, la que evita la spec degenerada: ¿tiene el universo
    # del desenlace (sin cuenta) un moderador no vacio?
    sinc = [f for f in filas if f["P5_20"]]
    con_mod = sum(1 for f in sinc if f["P5_23"] in ("1", "2"))
    print(f"\n  GUARDIA DE COBERTURA (§ spec): universo del desenlace = {len(sinc)} "
          f"sin cuenta; de esos, con moderador P5_23 valido = {con_mod} "
          f"({con_mod / len(sinc):.1%})")
    if con_mod < 0.9 * len(sinc):
        print("  ⚠ el moderador no cubre el universo: la spec seria degenerada.")
    anid = sum(1 for f in sinc if f["P5_24_1"] in ("0", "1"))
    print(f"  sensibilidad IPAB (P5_24_1) disponible en {anid} de los {len(sinc)} "
          f"({anid / len(sinc):.1%}) — anidada en el 'Si' de P5_23, por eso no es principal")
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
