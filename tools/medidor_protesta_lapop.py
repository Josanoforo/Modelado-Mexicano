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
from medidor_clientelismo_lapop import carga, sha_manifiesto, _cod, PAYLOADS  # noqa: E402


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
    ap.print_help()


if __name__ == "__main__":
    main()
