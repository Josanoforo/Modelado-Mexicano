#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA35-L9 · REGLAS-ACTIVOS-L3 — pieza (b).

R7.4 `civico.protesta.agravio_urbano` — LAPOP Mexico 2019.
Participacion en protesta (`prot3`) por ambito (`ur`) x agravio (`vic1ext`).

NO re-abre el veredicto `D` que `ADR-158` archivo para `R7.4` en el Hito D: ese
corrio el falsador COMPARTIDO con `R7.5` sobre datos de EVENTO (Mass
Mobilization, UCDP, GDELT) y su `D` dice que ninguna de esas tres codifica
entorno y forma de respuesta sobre el mismo caso. Esta pieza mide otra cosa,
sobre otra unidad: la PERSONA que se auto-reporta en una encuesta con diseno
muestral. Un dato descriptivo para la regla del modelo, no una fila de Hito D.

Uso:
    python3 tools/medidor_protesta_lapop.py --censo
"""
import argparse, json, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medidor_clientelismo_lapop import (carga, sha_manifiesto, _cod, PAYLOADS,  # noqa: E402
                                        _celda, _dif, _filas, _guardia, GUARDIAS,
                                        REPLICAS, SEED)


def censo():
    salida = []
    # 2019: la ola con prot3 binario y ungateado.
    df, meta, path, sha = carga("2019")
    pid = PAYLOADS["2019"][0]
    print(f"LAPOP 2019 · {pid}\n  sha256 {sha} -> "
          f"{'COINCIDE' if sha == sha_manifiesto(pid) else 'DIFIERE'}")
    for var in ["prot3", "ur", "vic1ext", "estratosec", "tamano", "wt", "upm",
                "estratopri"]:
        s = [_cod(v) for v in df[var]]
        marg = {}
        for c in s:
            if c is not None:
                marg[c] = marg.get(c, 0) + 1
        print(f"    {var:12s} n_val={sum(1 for c in s if c is not None):5d}  "
              f"marginal={dict(sorted(marg.items()))}  "
              f"{str(meta.column_names_to_labels.get(var, ''))[:44]}")
        salida.append({"ola": "2019", "var": var, "marginal": marg})

    # Denominadores del eje (ambito x agravio). NO es el desenlace: prot3 no entra.
    den = {}
    for u, v in zip(df["ur"], df["vic1ext"]):
        cu, cv = _cod(u), _cod(v)
        if cu is not None and cv is not None:
            den[(cu, cv)] = den.get((cu, cv), 0) + 1
    print("\n  DENOMINADORES del eje (ur x vic1ext), sin tocar prot3:")
    nom = {(1, 1): "urbano-victima", (1, 2): "urbano-no-victima",
           (2, 1): "rural-victima", (2, 2): "rural-no-victima"}
    for k in sorted(den):
        print(f"    {nom.get(k, k):22s} n={den[k]}")
    salida.append({"ola": "2019", "eje": "ur x vic1ext",
                   "denominadores": {nom.get(k, str(k)): v for k, v in den.items()}})

    # 2006, que el encargo pide "como contraste".
    d6, m6, p6, s6 = carga("2006")
    pid6 = PAYLOADS["2006"][0]
    print(f"\nLAPOP 2006 (contraste) · {pid6}\n  sha256 {s6} -> "
          f"{'COINCIDE' if s6 == sha_manifiesto(pid6) else 'DIFIERE'}")
    for var in ["PROT1", "PROT2"]:
        s = [_cod(v) for v in d6[var]]
        marg = {}
        for c in s:
            if c is not None:
                marg[c] = marg.get(c, 0) + 1
        print(f"    {var:8s} n_val={sum(1 for c in s if c is not None):5d}  "
              f"marginal={dict(sorted(marg.items()))}")
        print(f"             etiqueta: {str(m6.column_names_to_labels.get(var, ''))[:90]}")
        print(f"             codigos : {m6.variable_value_labels.get(var, {})}")
        salida.append({"ola": "2006", "var": var, "marginal": marg})
    return salida


# ─────────────────────── P1 · medicion (COMMIT-2) ───────────────────────
# Ejecuta la spec congelada §4. Nada se decide aqui.

def _tramo_edad(e):
    return "18-29" if e <= 29 else "30-44" if e <= 44 else "45-59" if e <= 59 else "60+"


def mide(ruta_json=None):
    df, _m, _p, sha = carga("2019")
    pid = PAYLOADS["2019"][0]
    g = GUARDIAS["2019"]
    _guardia("2019 filas", len(df), g["filas"])
    _guardia("2019 prot3 validos",
             sum(1 for v in df["prot3"] if _cod(v) is not None), g["prot3_val"])
    _guardia("2019 prot3 si",
             sum(1 for v in df["prot3"] if _cod(v) == 1), g["prot3_si"])
    print("guardias de lectura §0.5: OK")

    y = lambda v: 1 if v["prot3"] == 1 else 0

    # eje principal: ur x vic1ext, cuatro celdas
    celdas, filas_por_celda = {}, {}
    nom = {(1, 1): "urbano-victima", (1, 2): "urbano-no-victima",
           (2, 1): "rural-victima", (2, 2): "rural-no-victima"}
    for (u, vv), lab in nom.items():
        f = _filas(df, ["prot3", "ur", "vic1ext"], y,
                   lambda v, u=u, vv=vv: v["ur"] == u and v["vic1ext"] == vv)
        filas_por_celda[lab] = f
        celdas[lab] = _celda(f, lab)

    contrastes = {
        "C1_entorno_con_agravio": _dif(filas_por_celda["urbano-victima"],
                                       filas_por_celda["rural-victima"],
                                       "C1 = urbano-victima - rural-victima",
                                       celdas["urbano-victima"], celdas["rural-victima"]),
        "C2_agravio_en_urbano": _dif(filas_por_celda["urbano-victima"],
                                     filas_por_celda["urbano-no-victima"],
                                     "C2 = urbano-victima - urbano-no-victima",
                                     celdas["urbano-victima"], celdas["urbano-no-victima"]),
    }

    # ejes secundarios: estratosec, sexo, edad
    sec = {}
    for eje, col, etq in (
            ("estratosec", "estratosec", {1: "grande >100k", 2: "mediana 25k-100k",
                                          3: "pequena <25k"}),
            ("sexo", "q1", {1: "hombre", 2: "mujer"})):
        sec[eje] = {}
        for k, lab in etq.items():
            f = _filas(df, ["prot3", col], y, lambda v, k=k: v[col] == k)
            sec[eje][lab] = _celda(f, f"{eje}={lab}")
    sec["edad"] = {}
    for lab in ("18-29", "30-44", "45-59", "60+"):
        f = _filas(df, ["prot3", "q2"], y, lambda v, l=lab: _tramo_edad(v["q2"]) == l)
        sec["edad"][lab] = _celda(f, f"edad={lab}")

    out = {"acto": "MAESTRA35-L9 · REGLAS-ACTIVOS-L3", "pieza": "b",
           "reglas": ["R7.4"], "id_modelo": ["civico.protesta.agravio_urbano"],
           "fuente": "LAPOP Mexico 2019", "spec": "§4",
           "payload": {"id": pid, "sha256": sha,
                       "coincide_manifiesto": sha == sha_manifiesto(pid)},
           "estimador": f"proporcion ponderada; IC95 bootstrap de conglomerado, "
                        f"{REPLICAS} replicas, seed {SEED}",
           "aviso_ponderador": "wt constante = 1 (spec §1.2)",
           "no_dice_nada_sobre": "R7.5 (autodefensa) ni el veredicto D de ADR-158, "
                                 "que corrio sobre datos de evento; aqui la unidad es "
                                 "la persona auto-reportada",
           "antecedentes_no_medidos": ["red previa", "falla estatal palpable"],
           "eje_principal": celdas, "contrastes": contrastes,
           "ejes_secundarios": sec}
    if ruta_json:
        json.dump(out, open(ruta_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("escrito", ruta_json)

    print(f"\n{'=' * 74}\nPIEZA b · R7.4 · LAPOP Mexico 2019")
    for lab, c in celdas.items():
        if c.get("estado") == "ESTIMADA":
            print(f"  {lab:20s} p={c['p']:.6f}  IC95=[{c['ic95'][0]:.6f},{c['ic95'][1]:.6f}]  "
                  f"n={c['n']} num={c['numerador']}")
        else:
            print(f"  {lab:20s} NO-ESTIMABLE ({c.get('motivo')})")
    for k, d in contrastes.items():
        if d.get("estado") == "ESTIMADA":
            print(f"  {k:26s} d={d['d']:+.6f} IC95=[{d['ic95'][0]:+.6f},{d['ic95'][1]:+.6f}] "
                  f"{'EXCLUYE 0' if d['excluye_cero'] else 'contiene 0'}")
        else:
            print(f"  {k:26s} NO-ESTIMABLE ({d.get('motivo')})")
    for eje, cs in sec.items():
        print(f"  eje {eje}")
        for lab, c in cs.items():
            if c.get("estado") == "ESTIMADA":
                print(f"    {lab:18s} p={c['p']:.6f} IC95=[{c['ic95'][0]:.6f},{c['ic95'][1]:.6f}] n={c['n']}")
            else:
                print(f"    {lab:18s} NO-ESTIMABLE ({c.get('motivo')})")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--censo", action="store_true")
    ap.add_argument("--mide", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.censo:
        filas = censo()
        if a.json:
            json.dump(filas, open(a.json, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
        return
    if a.mide:
        mide(a.json)
        return
    ap.print_help()


if __name__ == "__main__":
    main()
