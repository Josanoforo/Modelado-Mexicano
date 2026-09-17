"""Medidor derivado sobre el CSV sellado de ENCRIGE descriptiva."""
from __future__ import annotations

import hashlib
import json

from tools.encrige_carga_intensidad import build_artifacts, sha256


IN_CSV = "IN-ENCRIGE-DES-CSV"
IN_RESULTS = "IN-ENCRIGE-DES-RESULTADOS"
IN_SPEC = "IN-ENCRIGE-DES-SPEC"
IN_SEAL = "IN-ENCRIGE-DES-SELLO"
IN_SEAL_SHA = "IN-ENCRIGE-DES-SELLO-SHA256"
PREFIX = "RESULT-ENCRIGE-CARGA-"


def _bytes(inputs: dict, input_id: str) -> bytes:
    item = inputs[input_id]
    if item.get("bytes") is not None:
        return item["bytes"]
    with open(item["ruta_absoluta"], "rb") as handle:
        return handle.read()


def _verify_parent(inputs: dict) -> bytes:
    csv_bytes = _bytes(inputs, IN_CSV)
    results_bytes = _bytes(inputs, IN_RESULTS)
    spec_bytes = _bytes(inputs, IN_SPEC)
    seal_bytes = _bytes(inputs, IN_SEAL)
    sidecar_bytes = _bytes(inputs, IN_SEAL_SHA)
    try:
        seal = json.loads(seal_bytes.decode("utf-8"))
        results = json.loads(results_bytes.decode("utf-8"))
        sidecar = sidecar_bytes.decode("utf-8").split()[0]
    except (ValueError, UnicodeDecodeError, IndexError) as exc:
        raise RuntimeError(f"PADRE-CADENA-ILEGIBLE:{exc}") from exc
    if sidecar != hashlib.sha256(seal_bytes).hexdigest():
        raise RuntimeError("PADRE-SELLO-SIDECAR-NO-COINCIDE")
    expected = {
        "resultados.json": hashlib.sha256(results_bytes).hexdigest(),
        "spec.yaml": hashlib.sha256(spec_bytes).hexdigest(),
    }
    for name, actual in expected.items():
        if seal.get(name) != actual:
            raise RuntimeError(f"PADRE-SELLO-NO-CUBRE-{name}")
    if results.get("spec_id") != "CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001":
        raise RuntimeError("PADRE-SPEC-ID-INCORRECTO")
    published = (results.get("resultados") or {}).get("RESULT-ENCRIGE-DES-G-CSV-SHA256")
    if published != sha256(csv_bytes):
        raise RuntimeError("PADRE-RESULTADO-NO-IDENTIFICA-CSV")
    return csv_bytes


def medir(inputs: dict, contrato: dict) -> dict:
    csv_bytes = _verify_parent(inputs)
    derived, artifacts = build_artifacts(csv_bytes)
    domains = derived["domains"]
    contrasts = {row["dominio"]: row for row in derived["contrasts"]}
    output = {
        PREFIX + "G-PADRE-CSV-SHA256": sha256(csv_bytes),
        PREFIX + "G-N-DOMINIOS": len(domains),
        PREFIX + "G-N-TAMANOS": len(derived["shares"]),
        PREFIX + "G-N-CONTRASTES": len(derived["contrasts"]),
        PREFIX + "G-MAX-RESIDUO-IDENTIDAD": float(max(abs(x.residuo_identidad or 0) for x in domains.values())),
        PREFIX + "G-MAX-RESIDUO-DESCOMPOSICION": float(max(abs(x["residuo_descomposicion"]) for x in derived["contrasts"])),
        PREFIX + "G-RESIDUO-N-NACIONAL": float(derived["residuals"]["N"]),
        PREFIX + "G-RESIDUO-A-NACIONAL": float(derived["residuals"]["A"]),
        PREFIX + "G-RESIDUO-T-NACIONAL": float(derived["residuals"]["T"]),
        PREFIX + "NACIONAL-P": float(domains["Estados Unidos Mexicanos"].p),
        PREFIX + "NACIONAL-M": float(domains["Estados Unidos Mexicanos"].m),
        PREFIX + "NACIONAL-R": float(domains["Estados Unidos Mexicanos"].r),
        PREFIX + "G-INCERTIDUMBRE": "NO-DISPONIBLE-EN-REPRESENTACION-CSV",
        PREFIX + "G-VEREDICTO": "DERIVADO-DESCRIPTIVO-DE-PADRE-SELLADO-SIN-INFORMACION-MUESTRAL-INDEPENDIENTE",
    }
    for domain, slug in (("Pequeña", "PEQUENA"), ("Mediana", "MEDIANA"), ("Grande", "GRANDE")):
        row = contrasts[domain]
        output[PREFIX + slug + "-DELTA-M-VS-MICRO"] = float(row["diferencia_m"])
        output[PREFIX + slug + "-CONTRIB-PREVALENCIA"] = float(row["contribucion_prevalencia"])
        output[PREFIX + slug + "-CONTRIB-INTENSIDAD"] = float(row["contribucion_intensidad_condicional"])
        output[PREFIX + slug + "-DOMINA"] = row["componente_dominante_abs"]
    artifact_slugs = {
        "tabla-ampliada.csv": "TABLA-AMPLIADA",
        "participaciones-por-tamano.csv": "PARTICIPACIONES",
        "contrastes-vs-micro.csv": "CONTRASTES",
        "controles.json": "CONTROLES",
        "participaciones-por-tamano.svg": "FIGURA-SVG",
    }
    for name, data in artifacts.items():
        output[PREFIX + "ARTEFACTO-" + artifact_slugs[name] + "-SHA256"] = sha256(data)
    return output
