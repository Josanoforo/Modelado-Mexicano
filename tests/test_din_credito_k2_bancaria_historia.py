#!/usr/bin/env python3
"""Falsadores de CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001 (ACTO GEN2-DIN-CREDITO-HISTORIA-1, P4).

Sintético (D-22) sobre los cuatro payloads inventados de los tests hermanos
(2012/2015/2018 de `test_din_credito_pisos_historia`, 2021 de
`test_din_credito_pisos_enif2021`): por ola, dos niveles nacionales (toda
persona y entre tenedores) con IC, N, DEN-W, SOPORTE; el nivel entre
tenedores nunca es menor que el nivel general; 2024 sale como texto
RESERVADA-NO-MEDIDA y `DIFERENCIA-2021-2024` empieza por NO-SE-COMPARA; el
medidor PARA si la tabla de comparabilidad no declara K2·2024
CAMBIO-DE-INSTRUMENTO o si el mapa no trae `k2_bancaria`. Los ids declarados
en spec.yaml son exactamente los producidos. Corre standalone; expone `corre()`.
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import types
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
import test_din_credito_pisos_historia as TH  # noqa: E402
import test_din_credito_pisos_enif2021 as T21  # noqa: E402

CALC = ROOT / "data/corrida0/CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001"
SPEC_MD = ROOT / "forense/prereg-caja/DIN-CREDITO-K2-BANCARIA-HISTORIA-spec-v1_0.md"
MAPA = ROOT / "forense/prereg-caja/DIN-CREDITO-PISOS-HISTORIA-mapa-v1_1.tsv"
REPS = 120


def _modulo():
    mod = types.ModuleType("medidor_k2_bancaria")
    exec(compile((CALC / "medidor.py").read_bytes(), str(CALC / "medidor.py"), "exec"), mod.__dict__)
    return mod


def _inputs_repo(spec):
    return {e["id"]: {"ruta_absoluta": str(ROOT / e["ruta"]), "bytes": (ROOT / e["ruta"]).read_bytes()}
            for e in spec["inputs"] if e.get("origen") == "repo"}


def _sintetico(errores):
    spec = yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))
    mod = _modulo()
    inputs = _inputs_repo(spec)
    contrato = {"parametros": {"bootstrap_replicas": REPS}, "seed": {"valor": 42}}
    with tempfile.TemporaryDirectory() as td:
        for ola, (pid, fab) in TH.PAYLOADS.items():
            z = Path(td) / f"{ola}.zip"; z.write_bytes(fab()); inputs[pid] = {"ruta_absoluta": str(z), "bytes": None}
        z = Path(td) / "2021.zip"; z.write_bytes(T21.payload_sintetico()); inputs["enif2021_csv"] = {"ruta_absoluta": str(z), "bytes": None}
        try:
            out = mod.medir(inputs, contrato)
        except Exception as exc:  # noqa: BLE001
            errores.append(f"medir() sobre los sintéticos reventó: {exc!r}")
            return None, spec
        txt = inputs["CREDITO-COMPARABILIDAD-TEXTO"]["bytes"].decode("utf-8")
        lineas = txt.split("\n"); cab = lineas[0].split("\t")
        ik, io_, iv = cab.index("conducta"), cab.index("ola"), cab.index("veredicto")
        rota = []
        for l in lineas:
            c = l.split("\t")
            if len(c) == len(cab) and c[ik] == "K2" and c[io_] == "2024":
                c[iv] = "CAMBIO-MENOR"
            rota.append("\t".join(c))
        r = dict(inputs); r["CREDITO-COMPARABILIDAD-TEXTO"] = {"ruta_absoluta": "", "bytes": "\n".join(rota).encode("utf-8")}
        try:
            mod.medir(r, contrato); errores.append("no PARÓ con K2·2024 degradado a CAMBIO-MENOR (frontera FP-404)")
        except RuntimeError:
            pass
        mtxt = inputs["MAPA"]["bytes"].decode("utf-8")
        r = dict(inputs); r["MAPA"] = {"ruta_absoluta": "", "bytes": "\n".join(l for l in mtxt.split("\n") if "\tk2_bancaria\t" not in l).encode("utf-8")}
        try:
            mod.medir(r, contrato); errores.append("no PARÓ con el mapa sin k2_bancaria")
        except RuntimeError:
            pass
    return out, spec


def corre():
    errores = []
    for p in (CALC / "medidor.py", CALC / "spec.yaml", SPEC_MD, Path(str(SPEC_MD) + ".sha256"), MAPA, Path(str(MAPA) + ".sha256")):
        if not p.exists():
            errores.append(f"falta {p.relative_to(ROOT)}")
    if errores:
        return errores
    sha_md = hashlib.sha256(SPEC_MD.read_bytes()).hexdigest()
    if Path(str(SPEC_MD) + ".sha256").read_text().split()[0] != sha_md:
        errores.append("sidecar de la spec discordante")
    if Path(str(MAPA) + ".sha256").read_text().split()[0] != hashlib.sha256(MAPA.read_bytes()).hexdigest():
        errores.append("sidecar del mapa v1.1 discordante")
    spec = yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))
    if spec.get("spec_md_sha256") != sha_md:
        errores.append("spec_md_sha256 discordante")
    if any("2024" in str(e.get("id", "")) for e in spec["inputs"]):
        errores.append("la spec declara un payload de 2024 (PARO a)")
    out, spec = _sintetico(errores)
    if out is None:
        return errores
    P = "RESULT-DIN-CREDITO-K2-BANCARIA-HISTORIA"
    for ola in ("2012", "2015", "2018", "2021"):
        for c in ("BANCARIA", "BANCARIA-ENTRE-TENEDORES"):
            b = f"{P}-{ola}-{c}-NACIONAL-TODOS"
            for s in ("P", "IC-LO", "IC-HI", "N", "DEN-W", "B-VALIDAS", "SOPORTE"):
                if f"{b}-{s}" not in out:
                    errores.append(f"{b}-{s} ausente")
        if out[f"{P}-{ola}-BANCARIA-ENTRE-TENEDORES-NACIONAL-TODOS-P"] < out[f"{P}-{ola}-BANCARIA-NACIONAL-TODOS-P"]:
            errores.append(f"{ola}: el nivel entre tenedores es menor que el general")
        if out[f"{P}-{ola}-BANCARIA-ENTRE-TENEDORES-NACIONAL-TODOS-N"] != out[f"{P}-{ola}-TENEDORES-N"]:
            errores.append(f"{ola}: la base entre tenedores no es TENEDORES-N")
    if not str(out.get(f"{P}-2024-BANCARIA", "")).startswith("RESERVADA-NO-MEDIDA"):
        errores.append("2024 debería salir como RESERVADA-NO-MEDIDA")
    if not str(out.get(f"{P}-DIFERENCIA-2021-2024", "")).startswith("NO-SE-COMPARA"):
        errores.append("DIFERENCIA-2021-2024 debería empezar por NO-SE-COMPARA")
    declarados = {r["id"] for r in spec.get("resultados") or []}
    if declarados != set(out):
        errores.append(f"resultados declarados: {len(declarados - set(out))} sobran, {len(set(out) - declarados)} faltan")
    rj = CALC / "resultados.json"
    if rj.exists():
        res = json.loads(rj.read_text(encoding="utf-8")).get("resultados", {})
        if set(res) != declarados:
            errores.append("sellado: ids != declarados")
    return errores


def main():
    errores = corre()
    for e in errores:
        print("FALLA --", e)
    if not errores:
        print("PASA -- tests/test_din_credito_k2_bancaria_historia.py (sintético D-22 × 4 olas; frontera FP-404; 2024 no medida)")
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
