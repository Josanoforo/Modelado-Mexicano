#!/usr/bin/env python3
"""Clasifica el residual SIN-CANDIDATO sin inferir equivalencias científicas.

La entrada es la salida viva de ``tools/relevo_usos.py --json``.  Este
programa sólo materializa el diagnóstico local de
GEN2-SIN-CANDIDATO-RUTAS-1 y exige un directorio de salida explícito.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


CAUSAS = {
    "OFERTA-EXISTE-ENLACE-NO-DECLARADO",
    "SPEC-LISTA-EJECUCION-PENDIENTE",
    "SPEC-O-MEDIDOR-FALTANTE",
    "DATO-O-DOCUMENTACION-FALTANTE",
    "DECISION-O-ESTIMANDO-PENDIENTE",
    "RESERVADO-O-YA-ENCARGADO",
    "SIN-RUTA-ACREDITADA",
}

RETIRADOS_PRECEDENCIA = {
    "RES-0084",
    "RES-0090",
    "RES-0091",
    "RES-0093",
    "RES-0094",
}

CELDAS_MEDICION_DEMANDA_3 = {"DIN-M-01", "FAM-M-01", "TRA-M-02", "TRA-M-03"}

FIELDS = [
    "resultado_id",
    "consumidor",
    "tipo_uso",
    "corrida_natural",
    "valor_legacy",
    "estado_relevo",
    "razon_relevo",
    "calc_observado",
    "result_observado",
    "causa_principal",
    "subcausa",
    "grupo_dependencia",
    "disponibilidad_acreditada",
    "siguiente_accion",
    "compuerta",
    "paquete_propuesto",
    "evidencia",
]


def _base(row: dict[str, object]) -> dict[str, str]:
    return {
        "resultado_id": str(row["resultado_id"]),
        "consumidor": str(row["consumidor"]),
        "tipo_uso": str(row["tipo_uso"]),
        "corrida_natural": str(row["corrida_natural"]),
        "valor_legacy": str(row.get("valor_legacy", "")),
        "estado_relevo": str(row["veredicto"]),
        "razon_relevo": str(row["razon"]),
        "calc_observado": str(row.get("calc_candidato", "")),
        "result_observado": str(row.get("result_gen2_candidato", "")),
    }


def _cell_id(consumer: str) -> str:
    parts = consumer.split(":")
    return parts[1] if len(parts) >= 3 and "-M-" in parts[1] else ""


def classify(row: dict[str, object]) -> dict[str, str]:
    out = _base(row)
    rid = out["resultado_id"]
    corrida = out["corrida_natural"]
    consumer = out["consumidor"]
    tipo = out["tipo_uso"]

    if corrida == "CORR-0001":
        if rid in {"RES-0001", "RES-0002"}:
            values = (
                "DECISION-O-ESTIMANDO-PENDIENTE",
                "FAMILIA-A-FUERA-DE-COBERTURA-DEL-CALC",
                "ENCIG2023-CORRESPONDENCIA",
                "payload y CALC existen, pero la spec v1.1 declara que no mide familia A",
                "decidir conservar estos priors o encargar una medición propia; no reutilizar resultados de familia B",
                "DECISION-REQUERIDA",
                "P01-ENCIG2023-CORRESPONDENCIA",
                "CALC-ENCIG-2023-0001-v1_1/spec.yaml demanda_que_releva",
            )
        else:
            values = (
                "DECISION-O-ESTIMANDO-PENDIENTE",
                "CANAL-VS-PARAMETRO-SIN-CANAL",
                "ENCIG2023-CORRESPONDENCIA",
                "payload ENCIG 2023 y CALC sellada v1_1; F-8 acepta CON-RESERVA, pero no fija RESULT por slot",
                "elegir conservar el prior, crear consumidores por canal o especificar un estimando agregado; después declarar enlaces exactos",
                "DECISION-REQUERIDA",
                "P01-ENCIG2023-CORRESPONDENCIA",
                "CALC-ENCIG-2023-0001-v1_1/spec.yaml; NC-0222; F-8",
            )
    elif corrida == "CORR-0004":
        values = (
            "RESERVADO-O-YA-ENCARGADO",
            "MEDICION-DEMANDA-3-CORR-0004",
            "MEDICION-DEMANDA-3",
            "F-9 conserva ASIGNADO como prior SIN-MEDIDO; spec/corrida corta reservada",
            "no duplicar; esperar el acto reservado",
            "ESPERA-MERGE",
            "NINGUNO",
            "enmienda de alcance SPECS-DEMANDA-1; FIRMAS-MESA-2 F-9",
        )
    elif corrida in {"CORR-0005", "CORR-0006"} or rid in RETIRADOS_PRECEDENCIA:
        values = (
            "RESERVADO-O-YA-ENCARGADO",
            "RETIRADO-POR-PRECEDENCIA-DEL-MEDIDO",
            "DECISION-D2A-CONSUMIDA",
            "existe MEDIDO de la misma regla y la firma D2(a) retira el ASIGNADO",
            "ninguna medición; reconciliar la vista sólo en su escritor canónico",
            "YA-DECIDIDO",
            "NINGUNO",
            "mapa-demanda-19-corr-v1_0.tsv; FIRMAS-MESA-1 OBJETO 3",
        )
    elif corrida == "CORR-0008":
        values = (
            "DATO-O-DOCUMENTACION-FALTANTE",
            "DISENO-MUESTRAL-ENNVIH-NO-PUBLICADO-O-NO-LOCALIZADO",
            "ENNVIH-DISENO",
            "tres payloads con sha256 están manifestados; falta pesos replicados o servicio oficial de varianza",
            "ampliar el expediente 03-ENNVIH-DIN-S6 para RES-0029/0030 y G3.horizonte_temporal; titular decide y envía",
            "DECISION-REQUERIDA",
            "P02-ENNVIH-DISENO",
            "NC-0156; sonda CORR-0008; expediente 03-ENNVIH-DIN-S6.md",
        )
    elif corrida == "CORR-0018":
        values = (
            "RESERVADO-O-YA-ENCARGADO",
            "FORMALIZACION-DIFERIDA-POR-F11",
            "COEFICIENTES-CORR-0018",
            "las siete fuentes están identificadas y manifestadas; F-11 mantiene D3(b) y ordena no formalizar ahora",
            "esperar demanda material de consumidor; no abrir CALC ni editar milpa en este lote",
            "YA-DECIDIDO",
            "NINGUNO",
            "sonda CORR-0018; FIRMAS-MESA-2 F-11",
        )
    elif corrida == "CORR-0019":
        values = (
            "DECISION-O-ESTIMANDO-PENDIENTE",
            "PRIOR-ASIGNADO-SIN-MEDICION-DE-LA-MISMA-REGLA",
            "PRIORS-CORR-0019",
            "valor asignado vigente; no hay RESULT sellado de la misma regla que active D2(a)",
            "decidir por consumidor si el prior se conserva, se retira o se convierte en una pregunta de medición delimitada",
            "DECISION-REQUERIDA",
            "NINGUNO",
            "mapa-demanda-19-corr-v1_0.tsv CORR-0019; D2(a)",
        )
    elif "celda_" in tipo and corrida >= "CORR-0020" and corrida <= "CORR-0075":
        cell = _cell_id(consumer)
        if cell in CELDAS_MEDICION_DEMANDA_3:
            values = (
                "RESERVADO-O-YA-ENCARGADO",
                "CELDA-SIN-B-RESERVADA-MEDICION-DEMANDA-3",
                f"MARCADOR-{cell}",
                "el valor legacy/computado existe; no acredita RESULT GEN2 ni B para la celda",
                "no duplicar las cuatro celdas sin B reservadas",
                "ESPERA-MERGE",
                "NINGUNO",
                "enmienda SPECS-DEMANDA-1; perímetro MEDICION-DEMANDA-3",
            )
        else:
            sub = "MARCADOR-SIN-OFERTA-GEN2"
            if out["razon_relevo"].startswith("CORR-CON-CALC-SIN-RESULT-FIJADO"):
                sub = "MARCADOR-CALC-DE-OTRA-CORRESPONDENCIA-SIN-RESULT-FIJADO"
            values = (
                "RESERVADO-O-YA-ENCARGADO",
                sub,
                f"MARCADOR-{cell}",
                "la celda legacy/computada existe; un CALC homónimo o de otro corte no acredita relevo del slot",
                "esperar CELDA-D-PILOTO-1 y el crosswalk firmado; después decidir la ruta de esta celda exacta",
                "ESPERA-MERGE",
                "NINGUNO",
                "NC-0239/NC-0240; reserva de CELDA-D-PILOTO-1 y crosswalk",
            )
    elif corrida == "CORR-0076":
        sub = "CORTE-EDAD-RESERVADO" if rid == "RES-0166" else "CORTE-SIN-RESULT-GEN2"
        values = (
            "RESERVADO-O-YA-ENCARGADO",
            sub,
            "CORTES-PI-PILOTO",
            "CORTES_C1 declara cuatro cortes y deja edad/migración pendientes; no hay RESULT GEN2 por corte",
            "esperar corte de edad, crosswalk y piloto de Opus; no convertir constantes de código en mediciones",
            "ESPERA-MERGE",
            "NINGUNO",
            "milpa/src/celdas.py:CORTES_C1; NC-0240; reserva del encargo",
        )
    elif corrida in {"CORR-0077", "CORR-0078", "CORR-0079"}:
        values = (
            "RESERVADO-O-YA-ENCARGADO",
            "CELDA-D-SIN-ESTIMADOR-ADJUDICADO",
            "CELDA-D-PILOTO",
            "existe contrato YAML de celda-D; no existe estimador/result acreditado",
            "esperar GEN2-CELDA-D-PILOTO-1; reutilizar sólo su contrato de una celda, no generalizar antes del resultado",
            "ESPERA-MERGE",
            "NINGUNO",
            "ADR-531; NC-0239; reserva CELDA-D-PILOTO-1",
        )
    elif corrida == "CORR-0080":
        values = (
            "RESERVADO-O-YA-ENCARGADO",
            "MOMENTO-AJUSTE-DEPENDIENTE-DE-ESTIMADOR-POR-CELDA",
            "MOMENTOS-AJUSTE-PILOTO",
            "catálogo declara ENIGH 2022 como universo, pero instrumentos y universo de candidatos siguen POR DECLARAR",
            "esperar el piloto de celda-D que adjudica estimador/ruta/dato; no escribir un medidor común",
            "ESPERA-MERGE",
            "NINGUNO",
            "milpa/catalogo-momentos-v0_1.tsv M01..M08; ADR-531",
        )
    elif corrida == "CORR-0081":
        values = (
            "DECISION-O-ESTIMANDO-PENDIENTE",
            "HOLDOUT-SIN-INSTRUMENTO-NI-UNIVERSO-FIJADO",
            "MOMENTOS-HOLDOUT",
            "la ficha fija la pregunta, pero instrumento y universo están POR DECLARAR",
            "por ficha, decidir instrumento/universo y sólo entonces escribir spec/medidor; no ensamblar los 14 en una interfaz general",
            "DECISION-REQUERIDA",
            "NINGUNO",
            "milpa/catalogo-momentos-v0_1.tsv M09..M22",
        )
    elif corrida == "CORR-0082":
        values = (
            "RESERVADO-O-YA-ENCARGADO",
            "THETA-SIN-ESTIMADOR-ADJUDICADO-POR-CELDA",
            "D-THETA-PILOTO",
            "la condicional está declarada en procedencia; el diseño E1 no acredita estimación ni RESULT consumible",
            "esperar piloto/careo D-theta de Opus; no cargar theta completa ni crear ensamble E",
            "ESPERA-MERGE",
            "NINGUNO",
            "NC-0239; ADR-531; reserva D-theta/CAREO/piloto",
        )
    else:  # pragma: no cover - una fila nueva debe forzar actualización explícita
        raise ValueError(f"slot SIN-CANDIDATO sin regla local: {rid} {corrida}")

    (
        out["causa_principal"],
        out["subcausa"],
        out["grupo_dependencia"],
        out["disponibilidad_acreditada"],
        out["siguiente_accion"],
        out["compuerta"],
        out["paquete_propuesto"],
        out["evidencia"],
    ) = values
    assert out["causa_principal"] in CAUSAS
    return out


def load_live(repo: Path) -> list[dict[str, object]]:
    proc = subprocess.run(
        [sys.executable, str(repo / "tools" / "relevo_usos.py"), "--json"],
        cwd=repo,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(proc.stdout)


def derive(repo: Path) -> list[dict[str, str]]:
    live = load_live(repo)
    rows = [classify(row) for row in live if row["veredicto"] == "SIN-CANDIDATO"]
    rows.sort(key=lambda row: row["resultado_id"])
    ids = [row["resultado_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("resultado_id duplicado en SIN-CANDIDATO")
    if len(rows) != 153:
        raise ValueError(f"universo vivo inesperado: {len(rows)} (esperado 153 en este corte)")
    return rows


def write_outputs(rows: list[dict[str, str]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "rutas.tsv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    reconciliation = {
        "n_sin_candidato": len(rows),
        "por_tipo_uso": dict(sorted(Counter(row["tipo_uso"] for row in rows).items())),
        "por_causa_principal": dict(
            sorted(Counter(row["causa_principal"] for row in rows).items())
        ),
        "por_compuerta": dict(sorted(Counter(row["compuerta"] for row in rows).items())),
        "por_grupo_dependencia": dict(
            sorted(Counter(row["grupo_dependencia"] for row in rows).items())
        ),
    }
    (output_dir / "reconciliacion.json").write_text(
        json.dumps(reconciliation, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="directorio explícito; nunca escribe vistas canónicas",
    )
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    rows = derive(repo)
    write_outputs(rows, args.output_dir)
    print(json.dumps({"filas": len(rows), "output_dir": str(args.output_dir)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
