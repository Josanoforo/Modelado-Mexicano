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
from medidor_clientelismo_lapop import _celda, _dif, REPLICAS, SEED  # noqa: E402

ZIP = "data/raw/enif_2024_bd_csv.zip"
TABLA = "TMODULO.csv"
PAYLOAD_ID = "enif_2024_enif_2024_bd_csv"
CAMPOS = ["FAC_PER", "EST_DIS", "UPM_DIS", "P5_20", "P5_23",
          "P5_24_1", "P5_24_9", "NIV", "EDAD_V", "TLOC"]


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


# ─────────────────────── P1 · medicion (COMMIT-2) ───────────────────────
# Ejecuta la spec congelada §6. Nada se decide aqui.

GUARDIA_FILAS = 13502
GUARDIA_P5_23 = {"1": 4136, "2": 9366}
GUARDIA_UNIVERSO = 2970

# spec §1.5, tramos de escolaridad de ENIF 2024 (identicos a L1 §1.2)
TRAMO_NIV = {"00": "hasta primaria", "01": "hasta primaria", "02": "hasta primaria",
             "03": "secundaria",
             "04": "media superior", "05": "media superior",
             "06": "media superior", "07": "media superior",
             "08": "superior", "09": "superior", "10": "superior", "11": "superior"}


def _tramo_edad(v):
    try:
        e = int(v)
    except (TypeError, ValueError):
        return None
    return "18-29" if e <= 29 else "30-44" if e <= 44 else "45-59" if e <= 59 else "60+"


def mide(ruta_json=None):
    filas = carga()
    if len(filas) != GUARDIA_FILAS:
        raise SystemExit(f"PARO (guardia §0.5): {len(filas)} filas, esperado {GUARDIA_FILAS}")
    m = {}
    for f in filas:
        if f["P5_23"]:
            m[f["P5_23"]] = m.get(f["P5_23"], 0) + 1
    if m != GUARDIA_P5_23:
        raise SystemExit(f"PARO (guardia §0.5): marginal P5_23 = {m}, esperado {GUARDIA_P5_23}")
    univ = [f for f in filas if f["P5_20"]]
    if len(univ) != GUARDIA_UNIVERSO:
        raise SystemExit(f"PARO (guardia §0.5): universo {len(univ)}, esperado {GUARDIA_UNIVERSO}")
    con_mod = sum(1 for f in univ if f["P5_23"] in ("1", "2"))
    if con_mod != len(univ):
        raise SystemExit(f"PARO (§6): el moderador no cubre el universo "
                         f"({con_mod}/{len(univ)}) — la spec seria degenerada.")
    print("guardias de lectura §0.5: OK · cobertura del moderador 100%")

    def tup(sub, cods):
        return [(f["EST_DIS"], f["UPM_DIS"], float(f["FAC_PER"]),
                 1 if f["P5_20"] in cods else 0) for f in sub]

    res = {}
    for des, cods in (("D1_desconfianza", {"03"}),
                      ("D2_desconfianza_o_efectivo", {"03", "05"})):
        conoce = tup([f for f in univ if f["P5_23"] == "1"], cods)
        nocon = tup([f for f in univ if f["P5_23"] == "2"], cods)
        ca = _celda(conoce, f"{des} | conoce proteccion")
        cb = _celda(nocon, f"{des} | no conoce")
        res[des] = {"conoce_proteccion": ca, "no_conoce": cb,
                    "delta": _dif(conoce, nocon, f"Δ_seguro ({des})", ca, cb)}

    # ejes secundarios sobre D1
    sec = {}
    sec["escolaridad"] = {}
    for lab in ("hasta primaria", "secundaria", "media superior", "superior"):
        sub = [f for f in univ if TRAMO_NIV.get(f["NIV"]) == lab]
        a = tup([f for f in sub if f["P5_23"] == "1"], {"03"})
        b = tup([f for f in sub if f["P5_23"] == "2"], {"03"})
        ca, cb = _celda(a, f"{lab}|conoce"), _celda(b, f"{lab}|no")
        sec["escolaridad"][lab] = {"conoce": ca, "no_conoce": cb,
                                   "delta": _dif(a, b, f"Δ_{lab}", ca, cb)}
    sec["edad"] = {}
    for lab in ("18-29", "30-44", "45-59", "60+"):
        sub = [f for f in univ if _tramo_edad(f["EDAD_V"]) == lab]
        a = tup([f for f in sub if f["P5_23"] == "1"], {"03"})
        b = tup([f for f in sub if f["P5_23"] == "2"], {"03"})
        ca, cb = _celda(a, f"{lab}|conoce"), _celda(b, f"{lab}|no")
        sec["edad"][lab] = {"conoce": ca, "no_conoce": cb,
                            "delta": _dif(a, b, f"Δ_{lab}", ca, cb)}

    # hallazgo marginal de §6: creer que hay proteccion no es saber quien protege
    ipab = sum(1 for f in filas if f["P5_24_1"] == "1")
    nosabe = sum(1 for f in filas if f["P5_24_9"] == "1")
    out = {"acto": "MAESTRA35-L9 · REGLAS-ACTIVOS-L3", "pieza": "d",
           "reglas": ["R1.5"], "id_modelo": ["dinero.ahorro.seguro_deposito_atenua_aversion"],
           "fuente": "ENIF 2024", "spec": "§6",
           "payload": {"id": PAYLOAD_ID, "sha256_zip": sha256(ZIP)},
           "estimador": f"proporcion ponderada (FAC_PER); IC95 bootstrap de conglomerado, "
                        f"{REPLICAS} replicas, seed {SEED}, UPM_DIS dentro de EST_DIS",
           "universo": "las 2 970 personas sin cuenta a las que se pregunta P5_20",
           "n_universo": len(univ), "cobertura_moderador": con_mod / len(univ),
           "desenlaces": res, "ejes_secundarios": sec,
           "eje_no_construible": "tenencia de cuenta: P5_20 solo existe para quien no "
                                 "tiene cuenta, asi que no varia dentro del universo",
           "hallazgo_marginal_ipab": {
               "dicen_conocer_la_proteccion": GUARDIA_P5_23["1"],
               "nombran_IPAB": ipab, "no_saben_nombrarla": nosabe,
               "nota": "creer que hay proteccion no es que el seguro sea visible; "
                       "'visible' es la palabra del SI de R1.5"},
           "reserva": "P5_20 es razon PRINCIPAL: quien desconfie pero elija otra razon "
                      "dominante no cuenta como desconfiado"}
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

    print(f"\n{'=' * 74}\nPIEZA d · R1.5 · ENIF 2024   universo={len(univ)}")
    for des, blk in res.items():
        print(f"  {des}")
        for k in ("conoce_proteccion", "no_conoce"):
            print(f"    {k:20s} {f(blk[k])}")
        print(f"    {'Δ_seguro':20s} {f(blk['delta'])}")
    for eje, cs in sec.items():
        print(f"  eje {eje}")
        for lab, blk in cs.items():
            print(f"    {lab:18s} {f(blk['delta'])}")
    print(f"  IPAB: {ipab} nombran / {nosabe} no saben nombrarla, de {GUARDIA_P5_23['1']} "
          f"que dicen conocer la proteccion")
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
