#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA38-LOTE-LAPOP · censo A.4 compartido por L4/L5/L18.

Abre los payloads LAPOP Mexico que las tres specs selladas nombran y reporta,
por variable: existencia, etiqueta verbatim, mapa de codigos (value labels),
marginal y n validos. NO cruza ninguna variable contra ningun desenlace: el
censo describe el instrumento, no el resultado.

Las specs (S4/S5/S8) declaran los cortes de dicotomizacion como "pendientes de
codebook". Este censo es el que los resuelve, con el mapa de codigos del propio
.dta/.sav a la vista, ANTES de que ninguna celda se calcule.

Uso:  python3 tools/censo_lote_lapop.py --json data/l4-l5-l18-censo-v1_0.json
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medidor_clientelismo_lapop import raiz, sha256, sha_manifiesto, _cod  # noqa: E402

# id de manifiesto -> (ruta relativa, lector)
PAYLOADS = {
    "2004_sav": ("1658622845mexico_2004_export_version",
                 "Descargas Manuales/1658622845Mexico 2004 Export Version.sav", "sav"),
    "2004_dta": ("642348348mexico_2004_export_version",
                 "Descargas Manuales/642348348mexico 2004 export version.dta", "dta"),
    "2006_sav": ("1008973606mexico_lapop_final_2006_data_set_092906",
                 "Descargas Manuales/1008973606Mexico_LAPOP_final 2006 data set 092906.sav", "sav"),
    "2006_dta": ("518939279mexico_lapop_final_2006_data_set_092906",
                 "Descargas Manuales/518939279mexico_lapop_final 2006 data set 092906.dta", "dta"),
    "2019": ("mexico_lapop_americasbarometer_2019_v1_0_w",
             "Descargas Manuales/Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta", "dta"),
    "2021": ("mex_2021_lapop_americasbarometer_v1_2_w",
             "Descargas Manuales/MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta", "dta"),
    "2023": ("mex_2023_lapop_americasbarometer_v1_0_w",
             "Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta", "dta"),
}

# Lo que cada spec nombra. Se buscan las dos capitalizaciones siempre.
PEDIDO = {
    "2004_sav": ["aoj1", "aoj1a", "aoj1b", "aoj11", "aoj12", "b10a", "b18",
                 "vic1", "cp6", "cp9", "e8", "lapop-e8", "prot1", "prot2",
                 "tamano", "ur", "wt", "mestrat", "estratopri", "upm", "cluster",
                 "q1", "q2", "ed"],
    "2004_dta": ["aoj1", "aoj1a", "aoj1b", "aoj11", "aoj12", "b10a", "b18",
                 "vic1", "cp6", "cp9", "e8", "lapop-e8", "prot1", "prot2",
                 "tamano", "ur", "wt", "mestrat", "estratopri", "upm", "cluster",
                 "q1", "q2", "ed"],
    "2006_sav": ["AOJ1", "AOJ1A", "AOJ1B", "AOJ11", "AOJ12", "B10A", "B18",
                 "VIC1", "CP6", "CP9", "E8", "PROT1", "PROT2", "TAMANO", "UR",
                 "wt", "WT", "ESTRATOPRI", "UPM", "CLUSTER", "Q1", "Q2", "ED"],
    "2006_dta": ["AOJ1", "AOJ1A", "AOJ1B", "AOJ11", "AOJ12", "B10A", "B18",
                 "VIC1", "CP6", "CP9", "E8", "PROT1", "PROT2", "TAMANO", "UR",
                 "wt", "WT", "ESTRATOPRI", "UPM", "CLUSTER", "Q1", "Q2", "ED"],
    "2019": ["clien1n", "clien1na", "clien4a", "clien4b", "vb3n", "vb10", "vb2",
             "vic1ext", "vicbar4a", "aoj1", "aoj11", "aoj12", "b10a", "b18",
             "cp6", "cp9", "e8", "prot3", "tamano", "ur", "estratosec",
             "wt", "estratopri", "upm", "q1", "q2", "ed"],
    "2021": ["aoj1", "aoj11", "aoj12", "b10a", "b18", "vic1ext", "prot3",
             "wt", "estratopri", "upm", "tamano", "ur"],
    "2023": ["aoj1", "aoj11", "aoj12", "b10a", "b18", "vic1ext", "prot3",
             "wt", "estratopri", "upm", "strata", "tamano", "ur"],
}


def carga(clave):
    import pyreadstat
    pid, rel, tipo = PAYLOADS[clave]
    path = os.path.join(raiz(), rel)
    if not os.path.exists(path):
        raise SystemExit(f"PARO: payload ausente en disco: {path} (id {pid})")
    df, meta = (pyreadstat.read_sav(path) if tipo == "sav"
                else pyreadstat.read_dta(path))
    return df, meta, path, sha256(path), pid


def resuelve(df, nombre):
    """Devuelve el nombre real de columna, insensible a mayusculas y a - vs _."""
    def norm(s):
        return s.lower().replace("-", "").replace("_", "")
    objetivo = norm(nombre)
    for c in df.columns:
        if norm(c) == objetivo:
            return c
    return None


def censo(claves=None, verbose=True):
    salida = []
    for clave in (claves or PAYLOADS):
        df, meta, path, sha, pid = carga(clave)
        man = sha_manifiesto(pid)
        cab = {"payload": clave, "id": pid, "archivo": path, "sha256": sha,
               "sha256_manifiesto": man,
               "coincide_manifiesto": sha == man,
               "n_filas": int(len(df)), "n_columnas": int(len(df.columns)),
               "variables": {}}
        if verbose:
            print(f"\n{'=' * 88}\nLAPOP MEXICO {clave} · id {pid}")
            print(f"  archivo : {path}")
            print(f"  sha256  : {sha}  -> "
                  f"{'COINCIDE con manifiesto' if sha == man else 'DIFIERE'}")
            print(f"  filas={len(df)}  columnas={len(df.columns)}")
        for var in PEDIDO[clave]:
            real = resuelve(df, var)
            if real is None:
                cab["variables"][var] = {"estado": "NO-ENCONTRADO"}
                if verbose:
                    print(f"    {var:12s} NO-ENCONTRADO")
                continue
            cods = [_cod(v) for v in df[real]]
            marg = {}
            for c in cods:
                if c is not None:
                    marg[c] = marg.get(c, 0) + 1
            n_val = sum(1 for c in cods if c is not None)
            etq = str(meta.column_names_to_labels.get(real, "") or "")
            vlab = meta.variable_value_labels.get(real, {}) or {}
            cab["variables"][var] = {
                "estado": "EXISTE", "columna_real": real, "etiqueta": etq,
                "n_validos": int(n_val), "n_filas": int(len(df)),
                "marginal": {str(k): int(v) for k, v in sorted(marg.items())},
                "codigos": {str(k): str(v) for k, v in vlab.items()},
                "distintos": len(marg),
            }
            if verbose:
                print(f"    {var:12s} col={real:12s} n_val={n_val:5d}  "
                      f"marg={dict(sorted(marg.items()))}")
                print(f"    {'':12s} etq: {etq[:120]}")
                if vlab:
                    print(f"    {'':12s} cod: { {str(k): str(v) for k, v in sorted(vlab.items(), key=lambda x: str(x[0]))} }")
        salida.append(cab)
    return salida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    ap.add_argument("--payload", action="append")
    a = ap.parse_args()
    out = censo(a.payload)
    if a.json:
        json.dump(out, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"\nescrito {a.json}")


if __name__ == "__main__":
    main()
