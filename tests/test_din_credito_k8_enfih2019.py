#!/usr/bin/env python3
"""Falsadores de CALC-DIN-CREDITO-K8-ENFIH2019-0001 (ACTO GEN2-DIN-CREDITO-HISTORIA-1, P3).

1. **Forma de la tabla** `data/credito-k8-triangulacion-texto-v1_0.tsv`: dos
   filas K8 (ENSAFI 2023 NO-ESTIMABLE con texto buscado; ENFIH 2019
   CAMBIO-DE-INSTRUMENTO con reactivo, texto literal, códigos, flujo, unidad
   PR y «negocio» NO-ESTIMABLE); fuente con sha256/16 y fila/página.
2. **Sintético (D-22).** ZIP con TNOMINA.csv / TPERSONAL.csv de cabecera
   entrecomillada (la forma real) y corre `medir()` con los inputs reales del
   repo: 10 destinos × 3 celdas; coherencia nacional = nómina + personal;
   `-SOPORTE`; unidad PR; los «No sabe» no entran al denominador; el medidor
   PARA si la tabla presenta ENFIH como MISMO-INSTRUMENTO o a ENSAFI como
   estimable.
3. **Sellado.** Si `resultados.json` existe: ids declarados = producidos.

Corre standalone y expone `corre()`.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import tempfile
import types
import zipfile
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "data/corrida0/CALC-DIN-CREDITO-K8-ENFIH2019-0001"
SPEC_MD = ROOT / "forense/prereg-caja/DIN-CREDITO-K8-ENFIH2019-spec-v1_0.md"
TABLA = ROOT / "data/credito-k8-triangulacion-texto-v1_0.tsv"
REPS = 120
RE_SHA16 = re.compile(r"sha256/16(?:\(zip\))?=[0-9a-f]{16}")
RE_PAG_O_FILA = re.compile(r"(pdf-p[aá]gs?\s+\d+|filas?\s+\d+)")


def _modulo():
    src = (CALC / "medidor.py").read_bytes()
    mod = types.ModuleType("medidor_k8_enfih")
    exec(compile(src, str(CALC / "medidor.py"), "exec"), mod.__dict__)
    return mod


def _inputs_repo(spec: dict) -> dict:
    out = {}
    for ent in spec["inputs"]:
        if ent.get("origen") == "repo":
            p = ROOT / ent["ruta"]
            out[ent["id"]] = {"ruta_absoluta": str(p), "bytes": p.read_bytes()}
    return out


def _tabla(errores: list[str]) -> None:
    lineas = TABLA.read_text(encoding="utf-8").split("\n")
    if lineas and lineas[-1] == "":
        lineas.pop()
    cab = lineas[0].split("\t")
    filas = [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]
    if any(len(l.split("\t")) != len(cab) for l in lineas[1:]):
        errores.append("tabla K8: número de celdas distinto de la cabecera")
    por = {(f["fuente"], f["edicion"]): f for f in filas}
    if set(por) != {("ENSAFI", "2023"), ("ENFIH", "2019")}:
        errores.append(f"tabla K8: filas {sorted(por)}")
        return
    s, e = por[("ENSAFI", "2023")], por[("ENFIH", "2019")]
    if s["veredicto"] != "NO-ESTIMABLE" or not s["texto_buscado"].strip():
        errores.append("ENSAFI 2023 debe ser NO-ESTIMABLE con texto_buscado (A.15)")
    if e["veredicto"] != "CAMBIO-DE-INSTRUMENTO":
        errores.append("ENFIH 2019 debe ser CAMBIO-DE-INSTRUMENTO")
    for c in ("reactivo", "texto_literal", "opciones_y_codigos", "filtro_y_flujo"):
        if not e[c].strip():
            errores.append(f"ENFIH 2019 sin {c}")
    if not e["unidad"].startswith("PR") or "negocio" not in e["componentes_no_estimables"]:
        errores.append("ENFIH 2019: unidad PR y «negocio» NO-ESTIMABLE obligatorios")
    for f in filas:
        for c in ("poblacion_base", "periodo_de_referencia", "secciones_recorridas", "nota"):
            if not f[c].strip():
                errores.append(f"{f['fuente']} {f['edicion']}: {c} vacía")
        if not RE_SHA16.search(f["archivo_fuente"]) or not RE_PAG_O_FILA.search(f["archivo_fuente"]):
            errores.append(f"{f['fuente']} {f['edicion']}: archivo_fuente sin sha256/16 o sin página/fila")


def payload_sintetico(n_pers: int = 900, semilla: int = 11) -> bytes:
    rng = np.random.default_rng(semilla)
    def tabla(var, max_consec, p_dest):
        filas = []
        for i in range(n_pers):
            if rng.random() > 0.45:
                continue
            est = 1 + i % 20
            for k in range(1, 1 + int(rng.integers(1, max_consec + 1))):
                filas.append([f"{i:07d}", "01", "1", "01", f"{k:02d}", "x", "x", "x", "x", "x", "x", "x", "x",
                              str(rng.choice(list("123456789"), p=p_dest)), f"{est:03d}", f"{est * 10 + int(rng.integers(0, 5)):07d}",
                              str(int(rng.integers(30, 5000))), "1", "1"])
        return filas
    cab_n = ["FOLIO", "VIV_SEL", "HOGAR", "N_REN", "CONSEC", "P8_24", "P8_25", "P8_26", "P8_27_1", "P8_27_2", "P8_28", "P8_29", "P8_30", "P8_31", "EDIS", "UPM_DIS", "FACTOR", "ESTRATO", "TLOC"]
    cab_p = [c if c not in ("P8_24", "P8_25", "P8_26", "P8_27_1", "P8_27_2", "P8_28", "P8_29", "P8_30", "P8_31") else
             {"P8_24": "P8_40", "P8_25": "P8_41", "P8_26": "P8_42", "P8_27_1": "P8_43_1", "P8_27_2": "P8_43_2", "P8_28": "P8_44", "P8_29": "P8_45", "P8_30": "P8_46", "P8_31": "P8_47"}[c] for c in cab_n]
    def csv(cab, filas):
        return "\r\n".join([",".join(f'"{c}"' for c in cab)] + [",".join(f'"{v}"' for v in f) for f in filas]) + "\r\n"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("TNOMINA.csv", csv(cab_n, tabla("P8_31", 3, [.08, .06, .30, .22, .12, .06, .05, .06, .05])))
        zf.writestr("TPERSONAL.csv", csv(cab_p, tabla("P8_47", 6, [.10, .08, .25, .20, .15, .07, .05, .06, .04])))
        zf.writestr("TMODULO.csv", '"FOLIO"\r\n')
    return buf.getvalue()


def _sintetico(errores: list[str]):
    spec = yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))
    mod = _modulo()
    inputs = _inputs_repo(spec)
    with tempfile.TemporaryDirectory() as td:
        z = Path(td) / "enfih_sintetico.zip"
        z.write_bytes(payload_sintetico())
        inputs["enfih2019_bd_csv_zip"] = {"ruta_absoluta": str(z), "bytes": None}
        contrato = {"parametros": {"bootstrap_replicas": REPS}, "seed": {"valor": 42}}
        try:
            out = mod.medir(inputs, contrato)
        except Exception as exc:  # noqa: BLE001
            errores.append(f"medir() sobre el sintético reventó: {exc!r}")
            return None, spec
        txt = inputs["K8-TRIANGULACION-TEXTO"]["bytes"].decode("utf-8")
        for mal, msg in (("CAMBIO-DE-INSTRUMENTO", "ENFIH como MISMO-INSTRUMENTO"), ("NO-ESTIMABLE", "ENSAFI como estimable")):
            r = dict(inputs)
            r["K8-TRIANGULACION-TEXTO"] = {"ruta_absoluta": "", "bytes": txt.replace(mal, "MISMO-INSTRUMENTO", 1).encode("utf-8")}
            try:
                mod.medir(r, contrato)
                errores.append(f"el medidor no PARÓ con {msg}")
            except RuntimeError:
                pass
    return out, spec


def _falsa(out: dict, errores: list[str], mod) -> None:
    pref = f"RESULT-{mod.PREFIJO}"
    puntos = [k for k in out if k.startswith(pref) and k.endswith("-P")]
    if len(puntos) != len(mod.DESTINOS) * 3:
        errores.append(f"{len(puntos)} celdas -P, esperaba {len(mod.DESTINOS) * 3}")
    for k in puntos:
        base = k[:-2]
        for s in ("IC-LO", "IC-HI", "N", "DEN-W", "B-VALIDAS", "SOPORTE"):
            if f"{base}-{s}" not in out:
                errores.append(f"{base}-{s} ausente")
    for nombre, _u in mod.DESTINOS:
        b = f"{pref}-{nombre}"
        for s in ("NUM", "DEN"):
            v = out.get(f"{b}-COHERENCIA-FAMILIA-DELTA-{s}-W")
            if v is None or abs(v) > 1e-6:
                errores.append(f"{nombre}: DELTA-{s}-W={v!r}")
        if out.get(f"{b}-UNIDAD") != "PR":
            errores.append(f"{nombre}: unidad {out.get(f'{b}-UNIDAD')!r}")
        if out[f"{b}-N-UNIVERSO"] + out[f"{pref}-NO-SABE-N"] + out[f"{pref}-BLANCO-O-FUERA-DE-CATALOGO-N"] != out[f"{pref}-FILAS-CREDITOS"]:
            errores.append(f"{nombre}: los «No sabe» no salen del denominador como declara la spec")
    # la suma de los destinos elementales (1..8) es 1 en cada celda
    for cell in ("NACIONAL-TODOS", "FAMILIA-NOMINA", "FAMILIA-PERSONAL"):
        s = sum(out[f"{pref}-{n}-{cell}-P"] for n in ("VIVIENDA", "VEHICULO", "CONSUMO", "REFINANCIAR-DEUDA", "EMERGENCIA", "SALUD", "EDUCACION", "OTRO"))
        if abs(s - 1.0) > 1e-9:
            errores.append(f"{cell}: los ocho destinos elementales suman {s}, no 1")
    if out[f"{pref}-PERSONAS-CON-CREDITO-N"] >= out[f"{pref}-FILAS-CREDITOS"]:
        errores.append("unidad PR: debería haber más créditos que personas en el sintético")


def corre() -> list[str]:
    errores: list[str] = []
    for p in (CALC / "medidor.py", CALC / "spec.yaml", SPEC_MD, Path(str(SPEC_MD) + ".sha256"), TABLA):
        if not p.exists():
            errores.append(f"falta {p.relative_to(ROOT)}")
    if errores:
        return errores
    _tabla(errores)
    spec = yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))
    sha_md = hashlib.sha256(SPEC_MD.read_bytes()).hexdigest()
    if spec.get("spec_md_sha256") != sha_md or Path(str(SPEC_MD) + ".sha256").read_text().split()[0] != sha_md:
        errores.append("spec_md_sha256 / sidecar de la spec humana discordante")
    if any("milpa/" in str(e.get("ruta", "")) for e in spec["inputs"]):
        errores.append("la spec declara un input bajo milpa/")
    mod = _modulo()
    out, spec = _sintetico(errores)
    if out is not None:
        _falsa(out, errores, mod)
        declarados = {r["id"] for r in spec.get("resultados") or []}
        if declarados != set(out):
            errores.append(f"resultados declarados: {len(declarados - set(out))} sobran, {len(set(out) - declarados)} faltan")
    rj = CALC / "resultados.json"
    if rj.exists():
        res = json.loads(rj.read_text(encoding="utf-8")).get("resultados", {})
        if set(res) != {r["id"] for r in spec.get("resultados") or []}:
            errores.append("sellado: ids de resultados.json != declarados")
        if res.get(f"RESULT-{mod.PREFIJO}-SERIE", "").startswith("SI"):
            errores.append("sellado: la corrida se presenta como serie (PARO d)")
    return errores


def main() -> int:
    errores = corre()
    for e in errores:
        print("FALLA --", e)
    if not errores:
        print("PASA -- tests/test_din_credito_k8_enfih2019.py (tabla K8 fuera de ENIF; sintético D-22: 10 destinos × 3 celdas, PR, sin serie)")
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
