#!/usr/bin/env python3
"""Preflight ENCO reservado: estructura DBF y fixtures, nunca respuestas.

Los únicos modos son: inspeccionar cabeceras dentro de ZIP, validar tarjetas,
calcular un fixture explícitamente sintético y publicar bytes sin reemplazo.
No existe un modo para leer registros DBF ni para emitir resultados reales.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import BinaryIO, Iterable

import yaml


ESTADO = "PREPARADA-NO-AUTORIZA-RESPUESTAS-NI-EMISIONES"
PERIODOS = {"2025-06", "2026-06"}
CODIGOS = {"1", "2", "3", "4"}
SUSTANTIVOS = {"1", "2", "4"}


def _exige(condicion: bool, mensaje: str) -> None:
    if not condicion:
        raise ValueError(mensaje)


def _read_exact(stream: BinaryIO, size: int) -> bytes:
    data = stream.read(size)
    _exige(len(data) == size, "cabecera_dbf_truncada")
    return data


def parse_dbf_header(stream: BinaryIO, *, member_size: int) -> list[dict]:
    """Lee sólo los bytes declarados como cabecera DBF; nunca toca una fila."""
    prefix = _read_exact(stream, 32)
    header_length = int.from_bytes(prefix[8:10], "little")
    record_length = int.from_bytes(prefix[10:12], "little")
    _exige(33 <= header_length <= member_size, "longitud_cabecera_dbf_invalida")
    _exige(record_length > 0, "longitud_registro_dbf_invalida")
    tail = _read_exact(stream, header_length - 32)
    terminator = tail.find(b"\r")
    _exige(terminator >= 0, "terminador_cabecera_dbf_ausente")
    descriptors = tail[:terminator]
    _exige(len(descriptors) % 32 == 0, "descriptores_dbf_desalineados")
    fields = []
    for offset in range(0, len(descriptors), 32):
        raw = descriptors[offset:offset + 32]
        name = raw[:11].split(b"\0", 1)[0].decode("ascii", errors="strict")
        field_type = chr(raw[11])
        _exige(bool(name), "campo_dbf_sin_nombre")
        fields.append({
            "nombre": name,
            "tipo": field_type,
            "longitud": raw[16],
            "decimales": raw[17],
        })
    _exige(bool(fields), "dbf_sin_campos")
    return fields


def inspect_zip(path: Path) -> dict:
    _exige(path.is_file(), "zip_ausente")
    _exige(zipfile.is_zipfile(path), "contenedor_no_zip")
    members = []
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        _exige(bool(infos), "zip_vacio")
        for info in infos:
            member = Path(info.filename)
            _exige(not member.is_absolute() and ".." not in member.parts,
                   "miembro_zip_ruta_insegura")
            _exige(not info.is_dir(), "directorio_zip_inesperado")
            _exige(member.suffix.lower() == ".dbf", "miembro_no_dbf")
            with archive.open(info, "r") as stream:
                fields = parse_dbf_header(stream, member_size=info.file_size)
            members.append({
                "miembro": info.filename,
                "tamano_descomprimido": info.file_size,
                "campos": fields,
            })
    return {
        "modo": "ESTRUCTURA-SOLA",
        "respondentes_leidos": False,
        "registros_leidos": 0,
        "miembros": members,
    }


def _peso(value, row_number: int) -> float:
    _exige(not isinstance(value, bool), f"peso_invalido_fila_{row_number}")
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"peso_invalido_fila_{row_number}") from None
    _exige(math.isfinite(number) and number > 0,
           f"peso_invalido_fila_{row_number}")
    return number


def synthetic_summary(rows: Iterable[dict]) -> dict:
    numerator = denominator = 0.0
    no_sabe = missing = ineligible = 0
    for index, row in enumerate(rows, start=1):
        _exige(isinstance(row, dict), f"fila_sintetica_invalida_{index}")
        if row.get("elegible") is not True:
            ineligible += 1
            continue
        weight = _peso(row.get("peso"), index)
        response = row.get("p10")
        if response is None or response == "":
            missing += 1
            continue
        response = str(response)
        _exige(response in CODIGOS, f"codigo_p10_invalido_fila_{index}")
        if response == "3":
            no_sabe += 1
            continue
        _exige(response in SUSTANTIVOS, f"codigo_no_sustantivo_fila_{index}")
        denominator += weight
        if response == "1":
            numerator += weight
    _exige(denominator > 0, "denominador_sustantivo_vacio")
    return {
        "naturaleza": "SINTETICO-NO-MEDICION",
        "estimando": "proporcion_ponderada_p10_si",
        "proporcion": numerator / denominator,
        "peso_numerador": numerator,
        "peso_denominador": denominator,
        "no_sabe_filas": no_sabe,
        "faltante_filas": missing,
        "no_elegible_filas": ineligible,
        "codigo_4_en_denominador": True,
    }


def to_percentage_points(value: float, scale: str) -> float:
    number = float(value)
    _exige(math.isfinite(number), "escala_valor_no_finito")
    if scale == "proporcion_0_1":
        _exige(0 <= number <= 1, "proporcion_fuera_de_escala")
        return number * 100
    if scale == "porcentaje_0_100":
        _exige(0 <= number <= 100, "porcentaje_fuera_de_escala")
        return number
    raise ValueError(f"escala_desconocida={scale}")


def preflight(cards: dict) -> dict:
    _exige(isinstance(cards, dict), "tarjetas_no_mapa")
    _exige(cards.get("estado") == ESTADO, "estado_no_protege")
    _exige(cards.get("lectura_respuestas_autorizada") is False,
           "lectura_respuestas_no_debe_autorizarse")
    _exige(cards.get("emisiones_autorizadas") is False,
           "emisiones_no_deben_autorizarse")
    waves = cards.get("olas")
    _exige(isinstance(waves, list) and len(waves) == 2, "se_exigen_dos_olas")
    periods = {wave.get("periodo") for wave in waves if isinstance(wave, dict)}
    _exige(periods == PERIODOS, "periodos_no_reservados")
    required = {
        "id_manifiesto", "periodo", "unidad_respuesta", "universo",
        "variable", "evento", "denominador", "missing", "ponderador",
        "diseno", "rotacion", "reserva", "definicion", "elegibilidad_M",
    }
    for wave in waves:
        _exige(isinstance(wave, dict), "ola_no_mapa")
        missing = sorted(required - set(wave))
        _exige(not missing, "campos_ola_ausentes=" + ",".join(missing))
        _exige(wave["reserva"] == "RESERVADA-NO-ABIERTA",
               "reserva_ola_no_protege")
        _exige(wave["elegibilidad_M"] == "M-NO-ELEGIBLE-PARA-ESTE-ESTIMANDO",
               "enlace_M_no_bloqueado")
    return {
        "estado": ESTADO,
        "olas": sorted(periods),
        "preparacion_completa": True,
        "respuestas_abiertas": False,
        "emisiones_autorizadas": False,
        "elegibilidad_experimental": False,
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def publish_without_replace(source: Path, destination: Path) -> dict:
    _exige(source.is_file(), "origen_ausente")
    destination.parent.mkdir(parents=True, exist_ok=True)
    source_hash = sha256(source)
    if destination.exists():
        _exige(destination.is_file() and sha256(destination) == source_hash,
               "conflicto_destino")
        return {"estado": "DESTINO-IDENTICO", "sha256": source_hash,
                "tamano_bytes": source.stat().st_size}
    fd, temporary_name = tempfile.mkstemp(prefix=".enco-reserva-", dir=destination.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as output, source.open("rb") as input_stream:
            shutil.copyfileobj(input_stream, output, length=1 << 20)
            output.flush()
            os.fsync(output.fileno())
        _exige(sha256(temporary) == source_hash, "copia_temporal_no_coincide")
        try:
            os.link(temporary, destination)
        except FileExistsError:
            _exige(sha256(destination) == source_hash, "conflicto_destino")
            state = "DESTINO-IDENTICO"
        else:
            state = "PUBLICADO-SIN-REEMPLAZO"
        return {"estado": state, "sha256": source_hash,
                "tamano_bytes": source.stat().st_size}
    finally:
        temporary.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    structure = sub.add_parser("structure")
    structure.add_argument("zip", type=Path)
    fixture = sub.add_parser("fixture")
    fixture.add_argument("json", type=Path)
    cards = sub.add_parser("preflight")
    cards.add_argument("yaml", type=Path)
    publish = sub.add_parser("publish")
    publish.add_argument("source", type=Path)
    publish.add_argument("destination", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "structure":
            result = inspect_zip(args.zip)
        elif args.command == "fixture":
            fixture_data = json.loads(args.json.read_text(encoding="utf-8"))
            _exige(fixture_data.get("naturaleza") == "SINTETICO-NO-MEDICION",
                   "fixture_no_sintetico")
            result = synthetic_summary(fixture_data.get("filas", []))
        elif args.command == "preflight":
            result = preflight(yaml.safe_load(args.yaml.read_text(encoding="utf-8")))
        else:
            result = publish_without_replace(args.source, args.destination)
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError,
            zipfile.BadZipFile) as exc:
        print(json.dumps({"estado": "PRECHECK-INVALIDO", "error": str(exc)},
                         ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
