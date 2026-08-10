#!/usr/bin/env python3
"""Emite decisiones supervisoras reproducibles para acciones de adquisición T0."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


FIELDS = [
    "decision_adquisicion_id", "activo_id", "familia_logica_id", "accion",
    "razon", "beneficio_informativo", "costo", "riesgo",
    "autoridad_requerida", "criterio_parada", "estado",
]


def stable_id(*parts: str) -> str:
    material = "\x1f".join(parts).encode("utf-8")
    return "DADQ-" + hashlib.sha256(material).hexdigest()[:24]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def build(universe_path: Path, discovered_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    not_acquired = sorted(
        asset["activo_id"] for asset in read_tsv(universe_path)
        if asset["estado_adquisicion"] == "DECLARADO_NO_ADQUIRIDO"
    )
    if not_acquired:
        scope_hash = hashlib.sha256("\n".join(not_acquired).encode("utf-8")).hexdigest()
        scope = f"CONJUNTO_T0_NO_ADQUIRIDO:n={len(not_acquired)}:sha256={scope_hash}"
        rows.append({
            "decision_adquisicion_id": stable_id(scope, "NO_ADQUIRIR_AHORA"),
            "activo_id": scope,
            "familia_logica_id": "NO_APLICA_CONJUNTO_EXACTO",
            "accion": "NO_ADQUIRIR_AHORA",
            "razon": "No existe una carencia concreta autorizada que justifique adquirir en masa el conjunto exacto; sus miembros son las filas DECLARADO_NO_ADQUIRIDO de universo-declarado-t0.tsv, reconciliadas por el hash del alcance.",
            "beneficio_informativo": "NO_DETERMINADO hasta vincular una carencia concreta sin revelar contexto a Nivel 1",
            "costo": "Descarga, almacenamiento, verificación e inspección no evaluados individualmente",
            "riesgo": "Ampliar el alcance y mezclar activos posteriores con el denominador T0",
            "autoridad_requerida": "SUPERVISOR",
            "criterio_parada": "Mantener sin adquirir hasta una decisión supervisora fundada en una carencia concreta y máximo dos intentos.",
            "estado": "VIGENTE",
        })
    for discovered in read_tsv(discovered_path):
        locator = discovered["localizador"]
        asset_ref = discovered["activo_descubierto_id"]
        rows.append({
            "decision_adquisicion_id": stable_id(asset_ref, "BUSQUEDA_DIRIGIDA"),
            "activo_id": asset_ref,
            "familia_logica_id": "NO_DETERMINADO",
            "accion": "BUSQUEDA_DIRIGIDA",
            "razon": "Verificar población, unidad y diseño material de una especificación descriptiva ya delimitada.",
            "beneficio_informativo": "Determinar si la especificación puede ejecutarse sin inventar campos materiales.",
            "costo": "Un intento dirigido en catálogo o documento oficial previamente localizado",
            "riesgo": "Bajo; no se descargó ni incorporó el activo a T0",
            "autoridad_requerida": "SUPERVISOR",
            "criterio_parada": "Cerrar al localizar evidencia oficial o al agotar el intento dirigido; no hacer discovery panorámico.",
            "estado": "EVIDENCIA_LOCALIZADA" if discovered["estado"] == "EVIDENCIA_LOCALIZADA" else discovered["estado"],
        })
    return sorted(rows, key=lambda row: row["decision_adquisicion_id"])


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--universe", type=Path, required=True)
    parser.add_argument("--discovered", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = build(args.universe.resolve(), args.discovered.resolve())
    write_tsv(args.output.resolve(), rows)
    print(f"decisiones={len(rows)} no_adquirir={sum(row['accion'] == 'NO_ADQUIRIR_AHORA' for row in rows)} busqueda_dirigida={sum(row['accion'] == 'BUSQUEDA_DIRIGIDA' for row in rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
