#!/usr/bin/env python3
"""Publica la tabla consultable y portada desde el inventario verificado."""
from __future__ import annotations

import collections
import csv
import hashlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
SOURCE = ROOT / "forense/analisis/catalogo/inventario-consumo-gen2.tsv"
TSV = ROOT / "canon/catalogo-del-mexicano-v1_0.tsv"
MD = ROOT / "canon/catalogo-del-mexicano-v1_0.md"

GROUP = {
    "dinero": "Dinero y crédito",
    "tramite": "Trámites y Estado",
    "civico": "Seguridad y norma",
    "tiempo-y-cuidado": "Tiempo, cuidado y vínculos",
    "familia": "Tiempo, cuidado y vínculos",
    "trabajo": "Tiempo, cuidado y vínculos",
    "salud": "Tiempo, cuidado y vínculos",
    "ingreso-y-gasto": "Ingreso y gasto",
}
EXAMPLES = {
    "Dinero y crédito": "RESULT-DIN-CREDITO-PISOS-ENIF2012-K1-NACIONAL-TODOS-P",
    "Trámites y Estado": "RESULT-ENCIG-MOR-A-P-SOL1",
    "Seguridad y norma": "RESULT-ENVIPE-DEN-P-C2-U4",
    "Tiempo, cuidado y vínculos": "RESULT-B-ENIGH-2022-P",
    "Ingreso y gasto": "RESULT-ENIGH16-REMINT-PARTICIPACION-AGREGADA",
}


def main() -> None:
    data = SOURCE.read_bytes()
    with SOURCE.open(newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(rows) != len({r["llave"] for r in rows}):
        raise ValueError("llave duplicada")
    if any(r["dominio"] not in GROUP for r in rows):
        raise ValueError("dominio sin grupo")
    by_id = {r["llave"]: r for r in rows}
    TSV.write_bytes(data)
    counts = collections.Counter(GROUP[r["dominio"]] for r in rows)
    states = collections.Counter(r["estado_adopcion"] for r in rows)
    sections = [
        "# Benchmark auditable del comportamiento del mexicano · catálogo v1.0",
        "",
        f"**{len(rows)} filas de estimando/segmento/ola en cinco áreas de consulta.** "
        "Es un censo de lecturas con estado, no un conteo de adopciones. La tesis de estabilidad "
        "se restringe a estimandos, olas, población y umbrales efectivamente evaluados; "
        "la tabla incluye series históricas y propuestas que no prueban estabilidad.",
        "",
        "La tabla [TSV](catalogo-del-mexicano-v1_0.tsv) permite buscar por conducta, "
        "instrumento, ola, segmento y llave. Cada fila conserva universo/denominador, "
        "escala, punto, límites de IC, naturaleza del IC, estado, firma, temporalidad, "
        "RESULT de punto y límites, CALC, hashes verificados, uso y reserva.",
        "",
        f"**Integridad:** SHA-256 del inventario fuente `{hashlib.sha256(data).hexdigest()}`; "
        "`python3 forense/analisis/catalogo/genera.py` valida sellos de CALC y "
        "`python3 forense/analisis/catalogo/publica.py` regenera esta portada y el TSV.",
        "",
        "## Cómo leerlo",
        "",
        "1. Busque el tema en la columna `conducta` y filtre `dominio`. Lea el "
        "`instrumento_ola` y `universo_denominador` antes de comparar filas.",
        "2. Interprete el punto en `unidad_escala`; un 0.25 en proporción equivale a "
        "25 %, mientras que minutos e importes conservan sus propias unidades. "
        "Los límites vacíos significan IC no identificado, nunca cero.",
        "3. Filtre `estado_adopcion`. `CONSUMO-GEN2-ACTIVO` y "
        "`ADOPTADO-POR-FIRMA` no son lo mismo que un piso histórico, un resultado "
        "sellado sin adopción, una firma de adoptar aún no consumida o un veto.",
        "4. Resuelva `result_punto` en `calc/resultados.json` bajo `data/corrida0/` "
        "y compare el hash con `sha256_resultados`. El hash de `sello.json` "
        "figura en `sha256_sello`.",
        "",
        "## Cobertura del censo",
        "",
        "El conteo siguiente es de **filas**, no de personas ni de estudios "
        "independientes. Una conducta por segmento y ola ocupa una fila; sus dos "
        "límites de IC no añaden filas. La llave RESULT impide contar otra vez una "
        "aparición documental.",
        "",
        "| Área | Filas |",
        "|---|---:|",
    ]
    for area in EXAMPLES:
        sections.append(f"| {area} | {counts[area]} |")
    sections += ["", "### Estado operativo", "", "| Estado | Filas |", "|---|---:|"]
    for state, n in sorted(states.items()):
        sections.append(f"| {state} | {n} |")
    sections += [
        "", "El bloque histórico de crédito 2012–2021 se incluye como contexto "
        "sellado, separado de la adopción GEN2. Nueve celdas-D del PR #1058 "
        "permanecen propuestas mientras el PR esté abierto. El bloque "
        "Banxico/LAPOP/MOTRAL firmado para adoptar conserva el rótulo de "
        "consumo pendiente hasta que exista asiento mecánico en consumidor.",
        "", "## Ejemplos trazables", "",
        "Estos ejemplos son entradas a la tabla, no una media entre áreas. "
        "La escala y el denominador en cada fila gobiernan la interpretación.",
        "", "| Área | Lectura de muestra | Estado | RESULT / CALC |",
        "|---|---|---|---|",
    ]
    for area, rid in EXAMPLES.items():
        r = by_id[rid]
        value = r["punto"] or "sin punto"
        bounds = f"[{r['ic95_inf']}, {r['ic95_sup']}]" if r["ic95_inf"] else "IC no identificado"
        sections.append(
            f"| {area} | {r['instrumento_ola']}; {value} {bounds}; "
            f"{r['unidad_escala'].replace('|', '/')} | {r['estado_adopcion']} | "
            f"`{rid}` / `{r['calc']}` |"
        )
    sections += [
        "", "## Interpretación y límites", "",
        "La columna `oferta_compatible` distingue las medidas de oferta asociables "
        "de la ausencia de una medida compatible. Una cifra de oferta de otra ola "
        "es contexto; restarla de un marginal no identifica preferencia. Los IC "
        "muestrales no se presentan como cobertura calibrada. La comparación "
        "2012–2021 de crédito debe mantener el recorte de 18–70 años y el mismo "
        "denominador; K2 entre tenedores y K2 poblacional son series distintas. "
        "La reserva K1 de predicción 2024 permanece.",
        "", "La tabla es retrospectiva donde así se marca. No identifica efectos "
        "causales, psicología individual, preferencias frente a ausencia de oferta "
        "ni cambios futuros. No usa NSE AMAI calculado. La "
        "[matriz de calculabilidad](../forense/analisis/catalogo/matriz-amai-2024.md) "
        "documenta qué componentes ofrecen los cuestionarios.",
        "", "**Auditoría de rigor:** sin promediar escalas heterogéneas; sin "
        "atribuir propuesta a main; sin convertir un IC de muestra en calibración; "
        "sin predicción prospectiva a partir de una lectura retrospectiva.",
        "",
    ]
    MD.write_text("\n".join(sections))
    print(f"filas={len(rows)} areas={len(counts)} sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
