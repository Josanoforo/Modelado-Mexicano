#!/usr/bin/env python3
"""Falsadores de CALC-DIN-CREDITO-PISOS-ENIF2021-0001
(ACTO GEN2-DIN-CREDITO-PISOS-ENIF2021-1).

Dos bloques, ninguno abre microdato:

1. **Sintético (D-22).** Fabrica un ZIP con la forma de `TMODULO` 2021
   (columnas declaradas, valores inventados con los saltos del cuestionario)
   y corre `medir()` con los inputs REALES del repo (medidor sellado de
   -0003, tablas de identidad GEN2, tabla de comparabilidad). Prueba que:
   cada conducta emite su unidad (P/PR) y nunca se mezclan; cada celda trae
   `-SOPORTE`; los controles de coherencia por eje cierran a cero; la base de
   K4 es «nunca ha tenido»; K6-PR cuenta productos y no personas; y que el
   medidor PARA si la tabla de comparabilidad no trae el reactivo.
2. **Sellado.** Si `resultados.json` existe: la tabla de identidad emitida
   (`forense/prereg-caja/DIN-CREDITO-PISOS-ENIF2021-metadatos-v1_0.tsv`)
   coincide uno a uno con los RESULT `-P` de las celdas por eje, con su
   unidad; el sidecar de la spec y el `spec_md_sha256` del yaml coinciden.

Corre standalone (`python3 tests/test_din_credito_pisos_enif2021.py`) y
expone `corre()`.
"""
from __future__ import annotations

import hashlib
import io
import json
import tempfile
import types
import zipfile
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "data/corrida0/CALC-DIN-CREDITO-PISOS-ENIF2021-0001"
SPEC_MD = ROOT / "forense/prereg-caja/DIN-CREDITO-PISOS-ENIF2021-spec-v1_0.md"
TABLA = ROOT / "forense/prereg-caja/DIN-CREDITO-PISOS-ENIF2021-metadatos-v1_0.tsv"
MIEMBRO = "conjunto_de_datos_tmodulo_enif_2021/conjunto_de_datos/conjunto_de_datos_tmodulo_enif_2021.csv"
REPS = 120


def _modulo():
    src = (CALC / "medidor.py").read_bytes()
    mod = types.ModuleType("medidor_din_credito")
    exec(compile(src, str(CALC / "medidor.py"), "exec"), mod.__dict__)
    return mod


def _inputs_repo(spec: dict) -> dict:
    out = {}
    for ent in spec["inputs"]:
        if ent.get("origen") == "repo":
            p = ROOT / ent["ruta"]
            out[ent["id"]] = {"ruta_absoluta": str(p), "bytes": p.read_bytes()}
    return out


def payload_sintetico(n: int = 2400, semilla: int = 7) -> bytes:
    """ZIP con un TMODULO inventado: 12 estratos × 4 UPM, códigos con los
    saltos de la sección 6 (6.4 sólo por producto tenido, 6.15 sólo si nunca
    tuvo, 6.7 sólo tenedores, 3.10 en blanco para quien no trabaja)."""
    rng = np.random.default_rng(semilla)
    cols = ([f"P6_2_{k}" for k in range(1, 10)] + [f"P6_4_{k}" for k in range(1, 10)]
            + [f"P6_1_{k}" for k in range(1, 6)] + [f"P5_4_{k}" for k in range(1, 10)]
            + ["P6_7", "P6_14", "P6_15", "P6_17", "P3_10", "SEXO", "EDAD", "TLOC",
               "P3_1_1", "FAC_ELE", "EST_DIS", "UPM_DIS", "RELLENO"])
    filas = []
    for i in range(n):
        est = 1 + i % 12
        upm = est * 10 + rng.integers(0, 4)
        prod = ["1" if rng.random() < p else "2" for p in
                (0.20, 0.12, 0.06, 0.08, 0.02, 0.05, 0.02, 0.01, 0.01)]
        tenedor = "1" in prod
        atr = ["" if pk != "1" else rng.choice(["1", "2", "2", "2", "8", "9"], p=[.2, .6, .1, .06, .02, .02])
               for pk in prod]
        inf = [rng.choice(["1", "2"], p=[q, 1 - q]) for q in (.05, .04, .15, .2, .01)]
        cta = [rng.choice(["1", "2"], p=[q, 1 - q]) for q in (.4, .1, .05, .05, .03, .02, .02, .01, .01)]
        p614 = "" if tenedor else rng.choice(["1", "2"], p=[.3, .7])
        p615 = str(rng.integers(1, 10)) if (not tenedor and p614 == "2") else ""
        p617 = rng.choice(["1", "2", "3"], p=[.12, .38, .5])
        p67 = (rng.choice(list("1234569"), p=[.5, .1, .05, .25, .05, .03, .02]) if tenedor else "")
        trabaja = rng.random() < 0.65
        p310 = rng.choice(list("1234569"), p=[.35, .05, .02, .03, .02, .5, .03]) if trabaja else ""
        filas.append(prod + atr + inf + cta + [
            p67, p614, p615, p617, p310, str(rng.integers(1, 3)),
            str(rng.integers(18, 97)), str(rng.integers(1, 5)),
            f"{rng.integers(0, 10):02d}", str(rng.integers(500, 5000)),
            f"{est:03d}", f"{upm:07d}", "x"])
    csv = ",".join(cols) + "\n" + "\n".join(",".join(f) for f in filas) + "\n"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(MIEMBRO, csv.encode("utf-8"))
    return buf.getvalue()


def _corre_sintetico(errores: list[str]) -> dict | None:
    spec = yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))
    mod = _modulo()
    inputs = _inputs_repo(spec)
    with tempfile.TemporaryDirectory() as td:
        z = Path(td) / "enif2021_sintetico.zip"
        z.write_bytes(payload_sintetico())
        inputs["enif2021_csv"] = {"ruta_absoluta": str(z), "bytes": None}
        contrato = {"parametros": {"bootstrap_replicas": REPS}, "seed": {"valor": 42}}
        try:
            out = mod.medir(inputs, contrato)
        except Exception as exc:  # noqa: BLE001
            errores.append(f"medir() sobre el sintético reventó: {exc!r}")
            return None

        # El medidor PARA si la tabla de comparabilidad no trae el reactivo.
        rota = dict(inputs)
        txt = inputs["CREDITO-COMPARABILIDAD-TEXTO"]["bytes"].decode("utf-8")
        rota["CREDITO-COMPARABILIDAD-TEXTO"] = {"ruta_absoluta": "", "bytes": txt.replace("P6_17", "P6_XX").encode("utf-8")}
        try:
            mod.medir(rota, contrato)
            errores.append("el medidor no PARÓ con una tabla de comparabilidad sin el reactivo de K5")
        except RuntimeError:
            pass
    return out


def _falsa_sintetico(out: dict, errores: list[str], mod) -> None:
    pref = f"RESULT-{mod.PREFIJO}"
    conductas = [c[0] for c in mod.CONDUCTAS]
    unidad = {c[0]: c[1] for c in mod.CONDUCTAS}
    if len(conductas) != 20:
        errores.append(f"{len(conductas)} conductas, esperaba 20")
    puntos = [k for k in out if k.endswith("-P") and k.startswith(pref)]
    # 18 celdas por conducta: nacional + 2+4+4+2+2 ejes + 2 formalidad + universo
    if len(puntos) != 20 * 18:
        errores.append(f"{len(puntos)} celdas -P, esperaba {20 * 18}")
    for k in puntos:
        base = k[:-2]
        for s in ("IC-LO", "IC-HI", "N", "DEN-W", "B-VALIDAS", "SOPORTE"):
            if f"{base}-{s}" not in out:
                errores.append(f"{base}-{s} ausente")
        n = out.get(f"{base}-N")
        sop = out.get(f"{base}-SOPORTE")
        if isinstance(n, int) and sop not in (("OK",) if n >= 200 else (f"BAJO-N-MENOR-{mod.N_SOPORTE}",)):
            errores.append(f"{base}: N={n} pero SOPORTE={sop!r}")
        # cada celda pertenece a exactamente una conducta
        dueños = [c for c in conductas if base.startswith(f"{pref}-{c}-")]
        dueños = [c for c in dueños if not any(o != c and o.startswith(c + "-") and base.startswith(f"{pref}-{o}-") for o in dueños)]
        if len(dueños) != 1:
            errores.append(f"{base}: pertenece a {dueños}, no a una sola conducta")
    for c in conductas:
        if out.get(f"{pref}-{c}-UNIDAD") != unidad[c]:
            errores.append(f"{c}: UNIDAD={out.get(f'{pref}-{c}-UNIDAD')!r}, esperaba {unidad[c]!r}")
        for e in ("SEXO", "EDAD", "ESCOLARIDAD", "LOCALIDAD", "CUENTA", "FORMALIDAD"):
            for s in ("NUM", "DEN"):
                v = out.get(f"{pref}-{c}-COHERENCIA-{e}-DELTA-{s}-W")
                if v is None or abs(v) > 1e-6:
                    errores.append(f"{c}×{e}: DELTA-{s}-W={v!r}")
    # unidades: P suma personas, PR suma productos
    n_pr = out[f"{pref}-K6-PR-NACIONAL-TODOS-N"]
    n_pt = out[f"{pref}-K6-P-TENEDORES-NACIONAL-TODOS-N"]
    if not (n_pr > n_pt > 0):
        errores.append(f"K6-PR N={n_pr} debería superar a K6-P-TENEDORES N={n_pt}")
    if out[f"{pref}-K6-PR-NACIONAL-TODOS-N"] > out[f"{pref}-FILAS-PRODUCTO"]:
        errores.append("K6-PR cuenta más filas que productos tenidos")
    # K4 sobre «nunca ha tenido»: su universo es esa base, no «sin crédito hoy»
    if out[f"{pref}-K4A-AUTOEXCLUSION-N-UNIVERSO"] > out[f"{pref}-NUNCA-HA-TENIDO-N"]:
        errores.append("K4 se midió fuera de la base «nunca ha tenido»")
    if out[f"{pref}-K4A-AUTOEXCLUSION-N-UNIVERSO"] >= out[f"{pref}-SIN-PRODUCTO-N"]:
        errores.append("K4 no excluye a los ex-usuarios (6.14 = 1)")
    # K7 sólo tenedores; K5 toda persona
    if out[f"{pref}-K7-SUCURSAL-N-UNIVERSO"] > out[f"{pref}-TENEDORES-N"]:
        errores.append("K7 se midió fuera de los tenedores")
    if out[f"{pref}-K5-N-UNIVERSO"] <= out[f"{pref}-K5-ENTRE-SOLICITANTES-N-UNIVERSO"]:
        errores.append("K5 (toda persona) debería tener universo mayor que K5 entre solicitantes")
    # formalidad: celdas sólo dentro del universo de quien trabaja
    for c in conductas:
        u = out[f"{pref}-{c}-UNIVERSO-UNIVERSO-TRABAJA-N"]
        s = out[f"{pref}-{c}-FORMALIDAD-SIN-SEGURIDAD-SOCIAL-N"] + out[f"{pref}-{c}-FORMALIDAD-CON-SEGURIDAD-SOCIAL-N"]
        if u != s:
            errores.append(f"{c}: formalidad {s} != universo trabaja {u}")


def _falsa_sellado(errores: list[str], mod) -> None:
    rj = CALC / "resultados.json"
    if not rj.exists():
        return
    res = json.loads(rj.read_text(encoding="utf-8")).get("resultados", {})
    pref = f"RESULT-{mod.PREFIJO}"
    if not TABLA.exists():
        errores.append(f"CALC sellado sin tabla de identidad {TABLA.relative_to(ROOT)}")
        return
    with TABLA.open(encoding="utf-8") as fh:
        lineas = [l.rstrip("\n") for l in fh if l.strip() and not l.startswith("#")]
    cab = lineas[0].split("\t")
    filas = [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]
    ids_tabla = {f["cell_id"] for f in filas}
    esperados = {k for k in res if k.startswith(pref) and k.endswith("-P")
                 and "-NACIONAL-" not in k and "-UNIVERSO-" not in k}
    if ids_tabla != esperados:
        errores.append(f"tabla de identidad: {len(ids_tabla - esperados)} sobran, {len(esperados - ids_tabla)} faltan")
    if len(ids_tabla) != len(filas):
        errores.append("cell_id duplicado en la tabla")
    unidad = {c[0]: c[1] for c in mod.CONDUCTAS}
    for f in filas:
        base = f["cell_id"][:-2]
        for s in ("IC-LO", "IC-HI", "N", "DEN-W", "SOPORTE"):
            if f"{base}-{s}" not in res:
                errores.append(f"{base}-{s}: no está sellado")
        c = f["outcome"]
        if c not in unidad:
            errores.append(f"{f['cell_id']}: outcome {c!r} no es conducta del medidor")
        elif res.get(f"{pref}-{c}-UNIDAD") != unidad[c] or not f["unit"].startswith(unidad[c] + " "):
            errores.append(f"{f['cell_id']}: unit {f['unit']!r} vs {unidad[c]!r}")
        if f["status"] != "CONSTRUIBLE":
            errores.append(f"{f['cell_id']}: status {f['status']!r}")
        if (f["source_instrument"], f["source_edition"], f["target_edition"]) != ("ENIF", "2021", "2024"):
            errores.append(f"{f['cell_id']}: olas {f['source_edition']}->{f['target_edition']}")
    for ruta, sha in {(f["metadata_source"], f["metadata_source_sha256"]) for f in filas}:
        p = ROOT / ruta
        if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != sha:
            errores.append(f"metadata_source_sha256 no coincide con {ruta}")
    side = Path(str(TABLA) + ".sha256")
    if not side.exists() or side.read_text().split()[0] != hashlib.sha256(TABLA.read_bytes()).hexdigest():
        errores.append("sidecar de la tabla de identidad ausente o discordante")


def corre() -> list[str]:
    errores: list[str] = []
    for p in (CALC / "medidor.py", CALC / "spec.yaml", SPEC_MD, Path(str(SPEC_MD) + ".sha256")):
        if not p.exists():
            errores.append(f"falta {p.relative_to(ROOT)}")
    if errores:
        return errores
    spec = yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))
    sha_md = hashlib.sha256(SPEC_MD.read_bytes()).hexdigest()
    if spec.get("spec_md_sha256") != sha_md:
        errores.append("spec_md_sha256 del yaml no coincide con la spec humana")
    if Path(str(SPEC_MD) + ".sha256").read_text().split()[0] != sha_md:
        errores.append("sidecar .sha256 de la spec humana discordante")
    if any("milpa/" in str(e.get("ruta", "")) for e in spec["inputs"]):
        errores.append("la spec declara un input bajo milpa/ (FP-395/396/397)")
    src = (CALC / "medidor.py").read_text(encoding="utf-8")
    if "milpa/tramite" in src or "import yaml" in src:
        errores.append("el medidor lee el trámite (milpa/) o carga yaml")
    mod = _modulo()
    out = _corre_sintetico(errores)
    if out is not None:
        _falsa_sintetico(out, errores, mod)
        declarados = {r["id"] for r in spec.get("resultados") or []}
        if declarados != set(out):
            errores.append(f"resultados declarados en spec.yaml: {len(declarados - set(out))} sobran, {len(set(out) - declarados)} faltan")
    _falsa_sellado(errores, mod)
    return errores


def main() -> int:
    errores = corre()
    for e in errores:
        print("FALLA --", e)
    if not errores:
        print("PASA -- tests/test_din_credito_pisos_enif2021.py (sintético D-22: 20 conductas × 18 celdas, unidad, soporte, coherencia; sellado si existe)")
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
