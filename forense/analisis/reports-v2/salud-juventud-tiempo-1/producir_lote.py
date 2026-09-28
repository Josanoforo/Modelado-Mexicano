#!/usr/bin/env python3
"""Deriva conteos e índice local de los dictámenes editoriales explícitos."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CUT = "7748208614570a50a97c1ba830aee72a972185f9"
PIECES = (
    ("Salud física", "salud/afirmaciones.tsv", "dictamen", 39,
     "Health__Body__Food_and_Substance_Use_in_Mexico__The_Behavioral_Layer_of_Decisions__Environment_and_Structure.md",
     "RESULT ENSANUT/ENCODAT de olas permitidas y estudios primarios; compras, ingesta y prevalencia separadas"),
    ("Juventud", "juventud/tabla.tsv", "dictamen_v2", 32,
     "Psicología_de_la_Juventud_Mexicana_Contemporánea__Gen_Z_y_Millennials_Jóvenes_como_Cohorte_Divergente.md",
     "Cortes y literatura primaria; inferencias de edad, periodo y cohorte auditadas"),
    ("Tiempo", "tiempo/afirmaciones.tsv", "dictamen_v2", 38,
     "El_Mexicano_y_el_Tiempo__Estructura__no_Cultura__en_la_Planeación_y_el_Compromiso_Temporal.md",
     "Cuatro RESULT ENIF y tabulados externos identificados como tales; causalidad de formalización retirada"),
)
ORDER = ("CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA")


def produce():
    rows = []
    totals = Counter()
    for title, table, verdict, mapped, report, evidence in PIECES:
        with (HERE / table).open(newline="", encoding="utf-8") as stream:
            decisions = list(csv.DictReader(stream, delimiter="\t"))
        assert all((d.get("id") or d.get("id_afirmacion")) and d.get(verdict) in ORDER for d in decisions), table
        counts = Counter(d[verdict] for d in decisions)
        assert len(decisions) >= mapped, table
        totals.update(counts)
        totals["mapa"] += mapped
        totals["adicionales"] += len(decisions) - mapped
        label = f"[{title}](../../../../corpus/reports-v2/{report})"
        nums = [mapped, len(decisions) - mapped, *(counts[x] for x in ORDER)]
        rows.append("| " + label + " | " + " | ".join(map(str, nums)) + f" | {evidence} |")
    summary = {"corte": CUT, "unidad": "decision_editorial_registrada", "mapa": totals["mapa"],
               "adicionales": totals["adicionales"], "dictamenes": {k: totals[k] for k in ORDER},
               "total": totals["mapa"] + totals["adicionales"]}
    rows.append("| **Total de registros** | " + " | ".join(
        f"**{x}**" for x in (summary["mapa"], summary["adicionales"],
                              *(summary["dictamenes"][k] for k in ORDER))) +
        f" | **{summary['total']} decisiones editoriales; cero RESULT creados o adoptados** |")
    body = f"""# Índice local · salud física, juventud y tiempo

Corte de redacción: `{CUT}`. La unidad de la tabla es una **decisión editorial registrada**, no una persona, una medición independiente ni una tesis confirmada. Las filas adicionales cubren afirmaciones materiales del original ausentes del mapa.

| Report v2 | Mapa | Adicionales | CONFIRMA | MATIZA | ROMPE | SIN-CIFRA | Evidencia decisiva |
|---|---:|---:|---:|---:|---:|---:|---|
{chr(10).join(rows)}

Cada pieza conserva su tabla de afirmaciones, productor y verificador en `salud/`, `juventud/` y `tiempo/`. Los dictámenes `ROMPE` se refieren a inferencias concretas inválidas, no a falta de datos. `SIN-CIFRA` conserva razones diferenciadas y no equivale a refutación. Las reglas propuestas no están adoptadas en el motor.

Las restricciones documentales, fuentes y límites figuran en los expedientes por pieza y en el [recibo](recibo-para-claude.md). La firma original «Acordado» está asentada en `forense/encargos/2026-09-26-ASTRA6-C3-CONSUMO-FAMILIA-1.md:26`; este lote la cita sin repetir el asiento.
"""
    identity_paths = ["forense/encargos/2026-09-27-ASTRA6-C3-SALUD-JUVENTUD-TIEMPO-1.md"]
    identity_paths += [f"corpus/reports-v2/{item[4]}" for item in PIECES]
    identity_paths += [f"forense/analisis/reports-v2/salud-juventud-tiempo-1/{item[1]}" for item in PIECES]
    hashes = "ruta\tsha256\n" + "".join(
        f"{name}\t{hashlib.sha256((ROOT / name).read_bytes()).hexdigest()}\n"
        for name in identity_paths)
    return body, json.dumps(summary, ensure_ascii=False, indent=2) + "\n", hashes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for path, content in zip((HERE / "indice-local.md", HERE / "resumen-lote.json", HERE / "identidades-producto.tsv"), produce()):
        if args.check:
            assert path.read_text(encoding="utf-8") == content, path
        else:
            path.write_text(content, encoding="utf-8")
    print("OK: índice y resumen derivados de decisiones editoriales")
