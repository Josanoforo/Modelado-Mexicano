#!/usr/bin/env python3
"""Escritor acotado del consumo GEN2 de trámite, desde pin firmado y RESULT.

V1 admite solo el caso revisado RES-0028. No firma pines ni decide adopción.
Uso: python3 tools/escribe_relevo_consumo.py [--apply]. Por defecto imprime
el diff seco. El merge de mesa del PR materializa la adopción.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import subprocess
import sys
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "milpa/tramite.yaml"
EXPECTED_TARGET_SHA = "0bb0ba70dba1c8e77b8dc2676d09be3546327ac526bd0a362d8e62e9359659fe"
SLOT = "RES-0028"
CONSUMER = "milpa/tramite.yaml:civico.denuncia.miedo_desconfianza:denuncia_por_otra_razon"
KEY = "tramite::civico.denuncia.miedo_desconfianza::denuncia_por_otra_razon"
CALC = "CALC-ENVIPE-RES0028-U4-DERIVADO-0001"
RESULT = "RESULT-ENVIPE-RES0028-Q-C2-U4"
OLD_P = "0.705687"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence() -> str:
    sys.path.insert(0, str(ROOT / "tools"))
    import pines_mesa  # noqa: PLC0415

    pins = [p for p in pines_mesa.lee_pines() if p["llave_logica"] == KEY]
    if len(pins) != 1:
        raise ValueError("falta pin único de mesa para la llave exacta")
    pin = pins[0]
    if (pin["calc_gen2"], pin["result_gen2"], pin["via"]) != (
        CALC, RESULT, pines_mesa.VIA_DERIVADO
    ):
        raise ValueError("pin firmado cambió de identidad o vía")
    if not pin["firma"].strip() or not any(
        word in pin["nota"].lower() for word in ("replay", "contexto")
    ):
        raise ValueError("pin sin firma o sin declaración de replay/contexto")

    rows = json.loads(subprocess.run(
        [sys.executable, str(ROOT / "tools/relevo_usos.py"), "--json"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout)
    matches = [r for r in rows if r["resultado_id"] == SLOT]
    if len(matches) != 1:
        raise ValueError("slot posicional cambió; revisar llave lógica")
    row = matches[0]
    if (row["consumidor"], row["veredicto"], row["calc_candidato"],
            row["result_gen2_candidato"], row["valor_legacy"]) != (
            CONSUMER, "RELEVADO-POR-PIN-DE-MESA", CALC, RESULT, OLD_P):
        raise ValueError("relevo no validó pin, identidad o valor legacy")
    if "paso las cuatro guardas" not in row["razon"]:
        raise ValueError("faltó verificación de las guardas del pin")

    folder = ROOT / "data/corrida0" / CALC
    seal_line = (folder / "sello.sha256").read_text().split()
    if seal_line != [sha(folder / "sello.json"), "sello.json"]:
        raise ValueError("sello de CALC no coincide")
    value = json.loads((folder / "resultados.json").read_text())["resultados"][RESULT]
    if not isinstance(value, (int, float)) or not 0 <= value <= 1:
        raise ValueError("RESULT fuera de escala proporción [0,1]")
    if str(row["valor_gen2"]) != str(value):
        raise ValueError("oferta y RESULT discrepan")
    rendered = f"{value:.6f}"
    if rendered != OLD_P:
        raise ValueError("el RESULT no coincide con el literal al grano de seis decimales")
    return rendered


def transform(source: str, rendered: str) -> str:
    lines = source.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines)
               if re.search(r"\bconducta: denuncia_por_otra_razon\b", line)]
    if len(matches) != 1:
        raise ValueError("conducta no es única")
    i = matches[0]
    line = lines[i]
    citation = f", corrida0_resultado_id: {RESULT}, corrida0_generacion: GEN2"
    if citation in line:
        if f"p: {rendered}" not in line or "PROPUESTA-NO-ADOPTADA-NC-0085" in line:
            raise ValueError("cita aplicada con valor o estado editorial inconsistente")
        return source
    if "corrida0_resultado_id:" in line or "corrida0_generacion:" in line:
        raise ValueError("cita parcial o distinta; rechazo atómico")
    if line.count("p: " + OLD_P) != 1:
        raise ValueError("literal previo no coincide")
    if line.count("}") < 1 or "rol_uso: complemento_dependiente" not in line:
        raise ValueError("estructura o rol de consumo cambió")
    before, marker, after = line.partition(", clase:")
    if not marker:
        raise ValueError("no se halló límite de campo p")
    if not before.endswith("p: " + OLD_P):
        raise ValueError("p no está en posición esperada")
    updated = before + citation + marker + after
    old_status = "PROPUESTA-NO-ADOPTADA-NC-0085: "
    if updated.count(old_status) != 1:
        raise ValueError("estado editorial previo cambió")
    lines[i] = updated.replace(old_status, "GEN2-RELEVADO-POR-PIN: ")
    return "".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    old = TARGET.read_text()
    if transform(old, OLD_P) == old:
        print("SIN-DIFF: ya aplicado")
        return
    if sha(TARGET) != EXPECTED_TARGET_SHA:
        raise ValueError("hash previo del consumidor cambió; revisar antes de aplicar")
    rendered = evidence()
    new = transform(old, rendered)
    if new == old:
        print("SIN-DIFF: ya aplicado")
        return
    diff = "".join(difflib.unified_diff(old.splitlines(keepends=True),
                                        new.splitlines(keepends=True),
                                        fromfile="a/milpa/tramite.yaml",
                                        tofile="b/milpa/tramite.yaml"))
    print(diff)
    if args.apply:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=TARGET.parent,
            prefix=".relevo-consumo-", delete=False,
        ) as handle:
            temp = Path(handle.name)
            handle.write(new)
        try:
            os.replace(temp, TARGET)
        finally:
            temp.unlink(missing_ok=True)
        print("APLICADO: una conducta, mismo p a seis decimales, cita GEN2")


if __name__ == "__main__":
    main()
