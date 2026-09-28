"""Reproducción GEN2 del abridor GEN1 de R8.3 (eje 2, WVS 7 México 2018).

El primer resultado que produzca este procedimiento es el que se reporta.
Gobernado por la spec humana que cita `spec_md`. Definiciones verbatim de
`forense/hitoD-R8_3-especificacion-v1_0.md` §4 (dicotomizaciones, estimando
principal SIN PUENTE, eje 2 por entidad con n>=30 y corte en la mediana) y
varianza de conglomerado último con `tests/svystat.py::diff_ultimate_cluster`
(un solo estrato, UPM `I_PSU`), ambos fijados por sha256. El veredicto
REPRODUCE / NO-REPRODUCE se decide contra las cifras del abridor
(`forense/hitoD-R8_3-abridor-v1_0.md` §2) con la tolerancia de la spec.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def _ref(objeto, nombre="tabla.json"):
    """COMMIT-1-bis (conducto D-22 COMMIT-C): la tabla va a `tablas/` de ESTE
    CALC y el RESULT la cita por REF con su sha256. No cambia qué se mide."""
    calc = Path(__file__).resolve().parent
    carpeta = calc / "tablas"
    if carpeta.is_symlink():
        raise PermissionError("tablas no puede ser enlace")
    carpeta.mkdir(exist_ok=True)
    destino = carpeta / nombre
    raw = (json.dumps(objeto, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False) + "\n").encode("utf-8")
    if destino.exists() and destino.read_bytes() != raw:
        raise PermissionError("tabla existente discordante: no reescribir")
    destino.write_bytes(raw)
    return f"REF:data/corrida0/{calc.name}/tablas/{nombre}#sha256:{hashlib.sha256(raw).hexdigest()}"



def _mod(rel, sha, nombre):
    ruta = RAIZ / rel
    if _sha(ruta) != sha:
        raise ValueError(f"GUARDIA: sha256 de {rel} no es el fijado")
    s = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _int(s):
    return pd.to_numeric(s.astype(object).map(lambda v: None if v is None or v is pd.NA else str(v).strip() or None),
                         errors="coerce")


def medir(inputs, contrato):
    par = contrato["parametros"]
    cl = _mod("tools/corpus_loader.py", par["corpus_loader_sha256"], "corpus_loader_fijado")
    sv = _mod("tests/svystat.py", par["svystat_sha256"], "svystat_fijado")
    pid = par["payload_id"]
    if _sha(inputs[pid]["ruta_absoluta"]) != par["hash_payload_sha256"]:
        raise ValueError("GUARDIA: sha256 del payload no es el fijado")
    v = par["variables"]
    df = cl.cargar(pid, par["tabla"], columnas=sorted(v.values()))
    fuente = df.attrs.get("fuente", "")
    q60, q61, q70 = _int(df[v["puente"]]), _int(df[v["desenlace"]]), _int(df[v["enforcement"]])
    w = _int(df[v["peso"]]).astype(float)
    ent = df[v["entidad"]].astype(str).str.strip()
    upm = df[v["upm"]].astype(str).str.strip()
    alto_si, alto_esc = set(par["enforcement_alto"]), set(par["escala_4"])
    conf_si = set(par["confia"])
    puente_si = set(par["tiene_puente"])
    # eje 2: contexto por entidad (n = filas del archivo en la entidad)
    n_ent = ent.value_counts()
    elegibles = sorted(e for e, n in n_ent.items() if n >= int(par["n_minimo_entidad"]))
    prop = {}
    for e in elegibles:
        m = (ent == e) & q70.isin(alto_esc) & (w > 0)
        prop[e] = float((w[m] * q70[m].isin(alto_si)).sum() / w[m].sum())
    vals = sorted(prop.values())
    k = len(vals)
    mediana = vals[k // 2] if k % 2 else (vals[k // 2 - 1] + vals[k // 2]) / 2
    ctx = {e: ("ALTO" if p > mediana else "BAJO") for e, p in prop.items()}
    nivel = ent.map(ctx)
    sin_puente = q60.isin(set(par["escala_4"]) - puente_si)
    y_ok = q61.isin(alto_esc)
    y = q61.isin(conf_si).astype(int)

    def rows(filtro):
        out = []
        for i in range(len(df)):
            g = None
            if filtro[i] and y_ok[i] and isinstance(nivel[i], str):
                g = "T" if nivel[i] == "ALTO" else "C"
            out.append(("UNICO", upm[i], float(w[i]) if math.isfinite(w[i]) else 0.0, int(y[i]), g))
        return out

    principal = sv.diff_ultimate_cluster(rows(sin_puente.to_numpy()))
    secundaria = sv.diff_ultimate_cluster(rows(pd.Series(True, index=df.index).to_numpy()))
    ref = par["referencia_abridor"]
    tol = float(par["tolerancia_reproduccion"])
    chk = {
        "entidades_elegibles": len(elegibles) == int(ref["entidades_elegibles"]),
        "mediana": abs(mediana - float(ref["mediana"])) <= tol,
        "p_alto": abs(principal["p_T"] - float(ref["p_alto"])) <= tol,
        "p_bajo": abs(principal["p_C"] - float(ref["p_bajo"])) <= tol,
        "d": abs(principal["d_hat"] - float(ref["d"])) <= tol,
    }
    veredicto = "REPRODUCE" if all(chk.values()) else "NO-REPRODUCE"
    tabla = {
        "_fuente_lectura": fuente, "n_filas": int(len(df)),
        "entidades_en_archivo": int(len(n_ent)), "entidades_elegibles": len(elegibles),
        "mediana_enforcement_alto": mediana,
        "entidades_alto": sum(1 for c in ctx.values() if c == "ALTO"),
        "entidades_bajo": sum(1 for c in ctx.values() if c == "BAJO"),
        "principal_sin_puente": {k2: (list(v2) if isinstance(v2, tuple) else v2) for k2, v2 in principal.items()},
        "secundaria_universo": {k2: (list(v2) if isinstance(v2, tuple) else v2) for k2, v2 in secundaria.items()},
        "chequeos": chk, "veredicto": veredicto,
    }
    return {par["result_filas"]: int(len(df)),
            par["result_veredicto"]: veredicto,
            par["result_tabla"]: _ref(tabla)}
