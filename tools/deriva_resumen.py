#!/usr/bin/env python3
"""Construye el resumen fechado del universo sin confundir adquisición e inspección.

La comparación acepta tanto el T0 histórico (``snapshot_t0_sha256``) como los
resúmenes fechados (``snapshot_sha256_del_dia``).  El cruce de inspecciones se
hace por SHA-256 contra los ledgers existentes; la mera presencia local de un
archivo sólo acredita adquisición.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import tempfile
from pathlib import Path


SHA256 = re.compile(r"^[0-9a-f]{64}$")
CRECE_SIEMPRE = {
    "componentes_declarados_conservadores",
    "cota_superior_activos_declarados",
    "contenidos_locales_sha256_unicos",
    "identidades_locales_verificadas",
    "representaciones_locales",
    "hashes_representaciones_locales_verificados",
    "numerador_adquirido_identidades_locales_verificadas",
    "declaraciones_parseadas",
    "candidatos_reconciliacion",
    "inputs",
}
ALARMA_SI_SUBE = {"discrepancias_hash_local"}


class ResumenError(ValueError):
    pass


def carga_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ResumenError(f"JSON_NO_LEGIBLE:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise ResumenError(f"JSON_NO_ES_OBJETO:{path}")
    return value


def huella_snapshot(doc: dict, path: Path) -> str:
    disponibles = [
        (campo, doc.get(campo))
        for campo in ("snapshot_sha256_del_dia", "snapshot_t0_sha256")
        if doc.get(campo) not in (None, "")
    ]
    if not disponibles:
        raise ResumenError(
            f"HUELLA_AUSENTE:{path}:se esperaba snapshot_sha256_del_dia o snapshot_t0_sha256"
        )
    campo, value = disponibles[0]
    if not isinstance(value, str) or not SHA256.fullmatch(value):
        raise ResumenError(f"HUELLA_INVALIDA:{path}:{campo}={value!r}")
    return value


def hashes_adquiridos(universo_tsv: Path) -> set[str]:
    try:
        with universo_tsv.open(encoding="utf-8", newline="") as fh:
            rows = csv.DictReader(fh, delimiter="\t")
            if "hash_local" not in (rows.fieldnames or []):
                raise ResumenError(f"UNIVERSO_SIN_HASH_LOCAL:{universo_tsv}")
            return {
                row["hash_local"]
                for row in rows
                if SHA256.fullmatch(row.get("hash_local", ""))
            }
    except OSError as exc:
        raise ResumenError(f"UNIVERSO_NO_LEGIBLE:{universo_tsv}:{exc}") from exc


def hashes_inspeccionados(ledgers: list[Path]) -> tuple[set[str], list[dict]]:
    hashes: set[str] = set()
    fuentes: list[dict] = []
    for path in ledgers:
        try:
            with path.open(encoding="utf-8", newline="") as fh:
                rows = csv.DictReader(fh, delimiter="\t")
                campos = set(rows.fieldnames or [])
                if "sha256" not in campos:
                    raise ResumenError(f"LEDGER_SIN_SHA256:{path}")
                validos: set[str] = set()
                for row in rows:
                    # Barrido2 explicita terminalidad; las filas no terminales
                    # no acreditan una inspección acabada. El ledger T0 ya es
                    # por contrato un registro de inspecciones consolidadas.
                    if "estado_terminal" in campos and row.get("estado_terminal") != "SI":
                        continue
                    sha = row.get("sha256", "")
                    if SHA256.fullmatch(sha):
                        validos.add(sha)
                hashes.update(validos)
                fuentes.append({"ruta": str(path), "identidades_sha256": len(validos)})
        except OSError as exc:
            raise ResumenError(f"LEDGER_NO_LEGIBLE:{path}:{exc}") from exc
    return hashes, fuentes


def payload_sustantivo(
    nuevo: dict,
    anterior: dict,
    fecha: str,
    universo_tsv: Path,
    ledgers: list[Path],
) -> tuple[dict, bool]:
    if not isinstance(nuevo.get("conteos"), dict):
        raise ResumenError("SNAPSHOT_NUEVO_SIN_CONTEOS")
    if not isinstance(anterior.get("conteos"), dict):
        raise ResumenError("SNAPSHOT_ANTERIOR_SIN_CONTEOS")
    hash_nuevo = huella_snapshot(nuevo, Path("snapshot-nuevo"))
    hash_anterior = huella_snapshot(anterior, Path("snapshot-anterior"))
    c_nuevo = nuevo["conteos"]
    c_anterior = anterior["conteos"]

    deltas: dict[str, dict] = {}
    material = False
    motivos: list[str] = []
    for key, value in c_nuevo.items():
        previo = c_anterior.get(key)
        numericos = (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and isinstance(previo, (int, float))
            and not isinstance(previo, bool)
        )
        if numericos and value != previo:
            delta = value - previo
            deltas[key] = {"anterior": previo, "nuevo": value, "delta": delta}
            if key in CRECE_SIEMPRE and delta < 0:
                material = True
                motivos.append(f"{key} bajó ({previo}->{value}): activos que desaparecen")
            if key in ALARMA_SI_SUBE and delta > 0:
                material = True
                motivos.append(
                    f"{key} subió ({previo}->{value}): hashes que cambian sobre activos declarados"
                )

    adquiridos = hashes_adquiridos(universo_tsv)
    inspeccionados_ledger, fuentes = hashes_inspeccionados(ledgers)
    inspeccionados_vigentes = adquiridos & inspeccionados_ledger
    declarados = c_nuevo.get("cota_superior_activos_declarados")
    adquirido_reportado = c_nuevo.get(
        "numerador_adquirido_identidades_locales_verificadas",
        c_nuevo.get("identidades_locales_verificadas"),
    )
    if adquirido_reportado != len(adquiridos):
        raise ResumenError(
            "ADQUISICION_NO_RECONCILIA:"
            f"snapshot={adquirido_reportado}:universo_sha256={len(adquiridos)}"
        )

    operativos = {
        "activos_declarados_cota_superior_conservadora": declarados,
        "adquiridos_identidades_sha256": len(adquiridos),
        "inspeccionados_identidades_sha256": len(inspeccionados_vigentes),
        "inspecciones_arrastradas_por": "interseccion_sha256_universo_vigente_con_ledgers",
        "ledgers": fuentes,
        "reserva_denominador": (
            "El universo sólo ofrece una cota superior conservadora mientras haya candidatos "
            "de reconciliación; no se publica porcentaje de inspección. Las cifras de "
            "adquiridos e inspeccionados son identidades de contenido SHA-256 y sí son comparables entre sí."
        ),
    }
    previo_operativo = anterior.get("conteos_operativos")
    cambio = bool(deltas or hash_nuevo != hash_anterior or previo_operativo != operativos)
    payload = {
        "fecha": fecha,
        "conteos": c_nuevo,
        "conteos_operativos": operativos,
        "snapshot_sha256_del_dia": hash_nuevo,
        "hash_anterior": hash_anterior,
        "hash_cambio": hash_nuevo != hash_anterior,
        "deltas": deltas,
        "material": material,
        "motivo_material": motivos,
    }
    return payload, cambio


def escribe_atomico(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nuevo", type=Path, required=True)
    parser.add_argument("--anterior", type=Path, required=True)
    parser.add_argument("--universo-tsv", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, action="append", default=[])
    parser.add_argument("--fecha", required=True)
    parser.add_argument("--salida", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        nuevo = carga_json(args.nuevo)
        anterior = carga_json(args.anterior)
        payload, cambio = payload_sustantivo(
            nuevo, anterior, args.fecha, args.universo_tsv, args.ledger
        )
        # Si el archivo de salida ya representa exactamente este estado, una
        # repetición no lo reescribe. Esto también evita que fecha/mtime sean
        # por sí solos una delta versionable.
        if args.salida.exists() and carga_json(args.salida) == payload:
            print(f"SIN_CAMBIOS:{args.salida}:resumen idéntico")
            return 0
        if not cambio:
            print(f"SIN_CAMBIOS:{args.anterior}:huella, conteos e inspecciones idénticos")
            return 0
        escribe_atomico(args.salida, payload)
        print(
            "ESCRITO:"
            f"{args.salida}:declarados={payload['conteos_operativos']['activos_declarados_cota_superior_conservadora']}:"
            f"adquiridos={payload['conteos_operativos']['adquiridos_identidades_sha256']}:"
            f"inspeccionados={payload['conteos_operativos']['inspeccionados_identidades_sha256']}:"
            f"material={'SI' if payload['material'] else 'NO'}"
        )
        return 0
    except ResumenError as exc:
        print(f"PARO-UNIVERSO-RESUMEN:{exc}", file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
