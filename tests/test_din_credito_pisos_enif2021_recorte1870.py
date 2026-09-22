#!/usr/bin/env python3
"""Falsadores de CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001
(ACTO GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1, pieza P0-a).

Tres bloques, ninguno abre microdato:

1. **Oro (D-22, spec.md §4).** El wrapper con `EDAD_MIN=18, EDAD_MAX=96`
   (el rango completo de la variable en 2021) debe reproducir, RESULT por
   RESULT, la salida del medidor sellado de `#943`
   (`CALC-DIN-CREDITO-PISOS-ENIF2021-0001`) sobre el MISMO payload
   sintético y la misma semilla -- porque es literalmente el mismo código,
   sólo con el marco pre-filtrado a un rango que no excluye a nadie. Si
   difiere, el wrapper rompió algo del procedimiento que dice reusar.
2. **Recorte real (D-22, sintético).** Con `EDAD_MIN=18, EDAD_MAX=70`, el
   número de filas-persona debe ser estrictamente menor que con el rango
   completo (el payload sintético trae edades `randint(18, 97)`, así que
   el recorte SIEMPRE excluye algo), coherencia/soporte/unidad siguen
   cerrando, y ningún `RESULT-` del prefijo nuevo colisiona con el
   prefijo de `#943`.
3. **Sellado.** Si `resultados.json` existe: `EDAD-RECORTE-MIN/MAX`
   sellados son 18/70; el sidecar de la spec humana coincide.

Corre standalone (`python3 tests/test_din_credito_pisos_enif2021_recorte1870.py`)
y expone `corre()`.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
import types
from pathlib import Path

import yaml

import test_din_credito_pisos_enif2021 as base  # payload_sintetico, patrón compartido

ROOT = base.ROOT
CALC = ROOT / "data/corrida0/CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001"
CALC_943 = ROOT / "data/corrida0/CALC-DIN-CREDITO-PISOS-ENIF2021-0001"
SPEC_MD = ROOT / "forense/prereg-caja/DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-spec-v1_0.md"
REPS = 120


def _modulo(ruta: Path, nombre: str):
    src = ruta.read_bytes()
    mod = types.ModuleType(nombre)
    exec(compile(src, str(ruta), "exec"), mod.__dict__)
    return mod


def _inputs_repo(spec: dict) -> dict:
    out = {}
    for ent in spec["inputs"]:
        if ent.get("origen") == "repo":
            p = ROOT / ent["ruta"]
            out[ent["id"]] = {"ruta_absoluta": str(p), "bytes": p.read_bytes()}
    return out


def _corre(errores: list[str]) -> tuple[dict | None, dict | None, object | None]:
    """Devuelve (out_oro, out_recorte, mod_wrapper) sobre el payload sintético."""
    spec = yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))
    mod = _modulo(CALC / "medidor.py", "medidor_recorte1870")
    mod943 = _modulo(CALC_943 / "medidor.py", "medidor_943_directo")
    inputs = _inputs_repo(spec)
    with tempfile.TemporaryDirectory() as td:
        z = Path(td) / "enif2021_sintetico.zip"
        z.write_bytes(base.payload_sintetico())
        inputs["enif2021_csv"] = {"ruta_absoluta": str(z), "bytes": None}
        contrato = {"parametros": {"bootstrap_replicas": REPS}, "seed": {"valor": 42}}

        try:
            out_943 = mod943.medir(inputs, contrato)
        except Exception as exc:  # noqa: BLE001
            errores.append(f"medir() de #943 directo sobre el sintético reventó: {exc!r}")
            return None, None, mod

        mod.EDAD_MIN, mod.EDAD_MAX = 18, 96
        try:
            out_oro = mod.medir(inputs, contrato)
        except Exception as exc:  # noqa: BLE001
            errores.append(f"medir() del wrapper (oro, 18-96) reventó: {exc!r}")
            return None, None, mod
        diffs = []
        for k, v in out_943.items():
            nk = k.replace(mod943.PREFIJO, mod.PREFIJO)
            if nk not in out_oro:
                diffs.append(f"falta en oro: {nk}")
            elif out_oro[nk] != v:
                diffs.append(f"{k}: {v!r} vs {out_oro[nk]!r}")
        if diffs:
            errores.append(f"oro (18-96) NO reproduce a #943: {len(diffs)} diffs, ej. {diffs[:3]}")

        mod.EDAD_MIN, mod.EDAD_MAX = 18, 70
        try:
            out_rec = mod.medir(inputs, contrato)
        except Exception as exc:  # noqa: BLE001
            errores.append(f"medir() del wrapper (recorte 18-70) reventó: {exc!r}")
            return out_oro, None, mod
    return out_oro, out_rec, mod


def _falsa_recorte(out_oro: dict, out_rec: dict, mod, errores: list[str]) -> None:
    pref = f"RESULT-{mod.PREFIJO}"
    n_oro = out_oro[f"{pref}-FILAS-PERSONAS"]
    n_rec = out_rec[f"{pref}-FILAS-PERSONAS"]
    if not (0 < n_rec < n_oro):
        errores.append(f"el recorte 18-70 no redujo FILAS-PERSONAS: oro={n_oro} recorte={n_rec}")
    if out_rec.get(f"{pref}-EDAD-RECORTE-MIN") != 18 or out_rec.get(f"{pref}-EDAD-RECORTE-MAX") != 70:
        errores.append("EDAD-RECORTE-MIN/MAX no son 18/70 en la corrida de recorte")
    # ningún RESULT- del prefijo nuevo debe colisionar con el de #943 directo
    pref_943 = "RESULT-DIN-CREDITO-PISOS-ENIF2021-"
    colisiones = [k for k in out_rec if k.startswith(pref_943) and not k.startswith(pref)]
    if colisiones:
        errores.append(f"RESULT- del recorte colisiona con el prefijo de #943: {colisiones[:5]}")
    # guardias heredadas siguen cerrando: coherencia, soporte, unidad
    conductas = [c[0] for c in mod943_conductas(mod)]
    unidad = {c[0]: c[1] for c in mod943_conductas(mod)}
    for c in conductas:
        for e in ("SEXO", "EDAD", "ESCOLARIDAD", "LOCALIDAD", "CUENTA", "FORMALIDAD"):
            for s in ("NUM", "DEN"):
                v = out_rec.get(f"{pref}-{c}-COHERENCIA-{e}-DELTA-{s}-W")
                if v is None or abs(v) > 1e-6:
                    errores.append(f"recorte {c}×{e}: DELTA-{s}-W={v!r}")
        if out_rec.get(f"{pref}-{c}-UNIDAD") != unidad[c]:
            errores.append(f"recorte {c}: UNIDAD={out_rec.get(f'{pref}-{c}-UNIDAD')!r}, esperaba {unidad[c]!r}")


def mod943_conductas(mod_wrapper):
    """CONDUCTAS es del módulo #943 importado; el wrapper no lo redeclara.
    Se carga aparte para no acoplar el test al mecanismo interno del wrapper."""
    mod943 = _modulo(CALC_943 / "medidor.py", "medidor_943_conductas")
    return mod943.CONDUCTAS


def _falsa_sellado(errores: list[str]) -> None:
    rj = CALC / "resultados.json"
    if not rj.exists():
        return
    res = json.loads(rj.read_text(encoding="utf-8")).get("resultados", {})
    pref = "RESULT-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870"
    if res.get(f"{pref}-EDAD-RECORTE-MIN") != 18 or res.get(f"{pref}-EDAD-RECORTE-MAX") != 70:
        errores.append("sellado: EDAD-RECORTE-MIN/MAX no son 18/70")


def corre() -> list[str]:
    errores: list[str] = []
    for p in (CALC / "medidor.py", CALC / "spec.yaml", SPEC_MD, Path(str(SPEC_MD).rsplit(".md", 1)[0] + ".sha256")):
        if not p.exists():
            errores.append(f"falta {p.relative_to(ROOT)}")
    if errores:
        return errores
    spec = yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))
    sha_md = hashlib.sha256(SPEC_MD.read_bytes()).hexdigest()
    if spec.get("spec_md_sha256") != sha_md:
        errores.append("spec_md_sha256 del yaml no coincide con la spec humana")
    sidecar = Path(str(SPEC_MD).rsplit(".md", 1)[0] + ".sha256")
    if sidecar.read_text().split()[0] != sha_md:
        errores.append("sidecar .sha256 de la spec humana discordante")
    if any("milpa/" in str(e.get("ruta", "")) for e in spec["inputs"]):
        errores.append("la spec declara un input bajo milpa/ (FP-395/396/397)")

    out_oro, out_rec, mod = _corre(errores)
    if out_oro is not None and out_rec is not None and mod is not None:
        _falsa_recorte(out_oro, out_rec, mod, errores)
        declarados = {r["id"] for r in spec.get("resultados") or []}
        if declarados != set(out_rec):
            errores.append(
                f"resultados declarados en spec.yaml: {len(declarados - set(out_rec))} sobran, "
                f"{len(set(out_rec) - declarados)} faltan"
            )
    _falsa_sellado(errores)
    return errores


def main() -> int:
    errores = corre()
    for e in errores:
        print("FALLA --", e)
    if not errores:
        print(
            "PASA -- tests/test_din_credito_pisos_enif2021_recorte1870.py "
            "(oro 18-96 reproduce #943 byte a byte; recorte 18-70 reduce el universo, "
            "coherencia/soporte/unidad cierran, sin colisión de RESULT-; sellado si existe)"
        )
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
