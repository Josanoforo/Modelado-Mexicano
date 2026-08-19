#!/usr/bin/env python3
"""Trabajador determinista: adjudica exactamente una necesidad N1-N33."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Iterable

CLASSES = {"CONFIRMADA", "NEGATIVA", "CANDIDATA", "NO_ACCESIBLE", "SIN_CANDIDATO", "CONFLICTO_MATERIAL"}
FORBIDDEN_IDS = {
    "SI", "NO", "ESPEJO", "SESION", "PROCEDENCIA_YAML", "REGISTRO_V01",
    "REGISTRO_V02", "VALIDAR_REGISTRO", "PROCEDENCIA", "MANIFIESTO", "INVENTARIO",
}
ARTIFACT_EXTENSIONS = {".py", ".md", ".tsv", ".csv", ".zip", ".yaml", ".yml", ".json", ".sh", ".txt"}
ARTIFACT_WORDS = re.compile(r"(?:SCRIPT|VALIDA(?:DOR|R)?|DOCUMENTO|NOTA|COLECCI[OÓ]N|REGISTRO_V0[12]|PROCEDENCIA_YAML)", re.I)
NEGATIVE_STATES = ("NO-ENCONTRADO", "NO-ACCESIBLE", "NO-SATISFACE", "EXISTE-NO-SATISFACE")

FIELDS = [
    "necesidad_id", "fuente_id_canonico", "fuente_nombre", "tipo_fuente", "objeto_evidencia_id",
    "id_manifiesto", "sha256", "capa1_universo_indexado", "capa2_manifiesto",
    "capa3_disco_real", "capa4_apertura_mapeo", "clasificacion_relacion",
    "reason_code", "evidencia_ref", "evidencia_textual_breve", "confianza",
    "conflicto_material", "nota",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(c for c in value if not unicodedata.combining(c)).upper()
    return re.sub(r"[^A-Z0-9]+", " ", value).strip()


def canonicalize(value: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^A-Z0-9]+", "_", normalize(value))).strip("_")[:96]


def is_sha256(value: str) -> bool:
    return not value or bool(re.fullmatch(r"[0-9a-f]{64}", value))


def is_real_source(source_id: str, name: str = "") -> bool:
    sid, label = (source_id or "").strip(), (name or "").strip()
    if not sid or normalize(sid).replace(" ", "_") in FORBIDDEN_IDS:
        return False
    if sid.isdigit() or re.fullmatch(r"\d+(?:\.\d+)?", sid):
        return False
    for value in (sid, label):
        lower = value.lower().split("?", 1)[0]
        if any(lower.endswith(ext) for ext in ARTIFACT_EXTENSIONS):
            return False
        if ARTIFACT_WORDS.search(value):
            return False
    return True


def needs(value: str) -> set[str]:
    return set(re.findall(r"\bN(?:[1-9]|[12][0-9]|3[0-3])\b", value or ""))


def parse_detail(row: dict[str, str]) -> dict[str, object]:
    try:
        value = json.loads(row.get("detalle_json", "") or "{}")
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        return {}


BRIDGE_FIELDS = [
    "necesidad_id", "fuente_id_canonico", "fuente_nombre", "objeto_evidencia_id",
    "id_manifiesto", "variable", "estado_crudo", "tabla_ref", "detalle_json",
]


def explicit_need_id(raw: str) -> str:
    """Extrae solo la necesidad primaria declarada, nunca etiquetas propagadas."""
    explicit = re.search(r"\bN([1-9]|[12][0-9]|3[0-3])\b", raw or "", re.I)
    if explicit:
        return f"N{int(explicit.group(1))}"
    leading = re.match(r"^\s*([1-9]|[12][0-9]|3[0-3])(?:\b|[.])", raw or "")
    return f"N{int(leading.group(1))}" if leading else ""


def evidence_object_id(source_id: str, detail: dict[str, object]) -> str:
    variable = str(detail.get("variable_encontrada", "") or "").strip()
    manifest = str(detail.get("id_manifiesto", "") or "").strip()
    table = str(detail.get("tabla", "") or "").strip()
    text = str(detail.get("texto_del_reactivo", "") or "").strip()
    material = "\x1f".join(normalize(x) for x in (source_id, manifest, variable, table, text))
    return "OE-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]


def build_opening_bridge(mapa: Path) -> list[dict[str, str]]:
    sources = read_tsv(mapa / "mapa-maestro-fuentes.tsv")
    result: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for opening in read_tsv(mapa / "mapa-maestro-aperturas.tsv"):
        need_id = explicit_need_id(opening.get("necesidad_cruda", ""))
        if not need_id:
            continue
        sid, name = best_source(opening.get("fuente_cruda", ""), sources)
        detail = parse_detail(opening)
        object_id = evidence_object_id(sid, detail)
        key = (need_id, sid, object_id)
        if key in seen:
            continue
        seen.add(key)
        result.append({
            "necesidad_id": need_id, "fuente_id_canonico": sid, "fuente_nombre": name,
            "objeto_evidencia_id": object_id,
            "id_manifiesto": str(detail.get("id_manifiesto", "") or "").strip(),
            "variable": str(detail.get("variable_encontrada", "") or "").strip(),
            "estado_crudo": opening.get("estado_crudo", ""), "tabla_ref": opening.get("tabla_ref", ""),
            "detalle_json": opening.get("detalle_json", ""),
        })
    return sorted(result, key=lambda r: (int(r["necesidad_id"][1:]), r["fuente_id_canonico"], r["objeto_evidencia_id"]))


def write_bridge(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=BRIDGE_FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def compact_evidence(row: dict[str, str]) -> str:
    text = row.get("referencias_evidencia", "")
    refs = [x.strip() for x in text.split(";") if x.strip()]
    authoritative = [x for x in refs if x.startswith("MAIN:")]
    return ";".join((authoritative or refs)[:4])


def source_score(query: str, source: dict[str, str]) -> int:
    q = set(normalize(query).split())
    if not q:
        return 0
    candidate = set(normalize(source.get("fuente_id", "") + " " + source.get("nombres", "")).split())
    common = q & candidate
    score = len(common) * 10
    nq = normalize(query)
    if nq == normalize(source.get("fuente_id", "")):
        score += 100
    if nq and nq in normalize(source.get("nombres", "")):
        score += 50
    return score


def best_source(query: str, sources: Iterable[dict[str, str]]) -> tuple[str, str]:
    ranked = sorted(((source_score(query, s), s) for s in sources), key=lambda x: x[0], reverse=True)
    if ranked and ranked[0][0] >= 20:
        row = ranked[0][1]
        sid = row.get("fuente_id", "")
        name = (row.get("nombres", "").split(";")[0] or query).strip()
        if is_real_source(sid, name):
            return sid, name
    return canonicalize(query), query.strip()


def opening_class(state: str) -> tuple[str, str, str]:
    upper = normalize(state).replace(" ", "-")
    if "NO-ACCESIBLE" in upper:
        return "NO_ACCESIBLE", "APERTURA_NO_ACCESIBLE", "ALTA"
    if any(normalize(x).replace(" ", "-") in upper for x in NEGATIVE_STATES):
        return "NEGATIVA", "APERTURA_NEGATIVA_EXPLICITA", "ALTA"
    if "EXISTE-SATISFACE" in upper:
        return "CONFIRMADA", "APERTURA_EXPLICITA_SATISFACE", "ALTA"
    return "CANDIDATA", "APERTURA_INDETERMINADA", "MEDIA"


def payload_for(detail: dict[str, object], payloads: dict[str, dict[str, str]]) -> tuple[str, str, str]:
    manifest_id = str(detail.get("id_manifiesto", "") or "").strip()
    if not manifest_id:
        return "", "", "NO_REFERENCIADO"
    payload = payloads.get(manifest_id)
    if not payload:
        return manifest_id, "", "REFERENCIA_INEXISTENTE"
    sha = payload.get("sha256_declarado", "").lower()
    return manifest_id, sha if is_sha256(sha) else "", payload.get("capa3_disco_real", "")


def adjudicate_need(mapa: Path, bridge_path: Path, need_id: str) -> list[dict[str, str]]:
    openings = [r for r in read_tsv(bridge_path) if r.get("necesidad_id") == need_id]
    payloads = {r.get("id_payload", ""): r for r in read_tsv(mapa / "mapa-maestro-payloads.tsv")}
    result: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    # Cada apertura es evidencia explícita y se adjudica de manera independiente.
    for opening in openings:
        sid, name = opening["fuente_id_canonico"], opening["fuente_nombre"]
        detail = parse_detail(opening)
        manifest_id, sha, disk = payload_for(detail, payloads)
        classification, reason, confidence = opening_class(opening.get("estado_crudo", ""))
        ref = opening.get("tabla_ref", "").strip()
        # La identidad de la evidencia no depende de la posición de la fila ni
        # de que otra apertura de la misma fuente comparta clasificación/ref.
        key = (sid, opening["objeto_evidencia_id"])
        if key in seen:
            continue
        seen.add(key)
        result.append({
            "necesidad_id": need_id,
            "fuente_id_canonico": sid,
            "fuente_nombre": name,
            "tipo_fuente": "FUENTE_DATOS",
            "objeto_evidencia_id": opening["objeto_evidencia_id"],
            "id_manifiesto": manifest_id,
            "sha256": sha,
            "capa1_universo_indexado": "SI",
            "capa2_manifiesto": "SI" if manifest_id in payloads else ("REFERENCIA_INEXISTENTE" if manifest_id else "NO_REFERENCIADO"),
            "capa3_disco_real": disk,
            "capa4_apertura_mapeo": opening.get("estado_crudo", ""),
            "clasificacion_relacion": classification,
            "reason_code": reason,
            "evidencia_ref": ref,
            "evidencia_textual_breve": str(detail.get("texto_del_reactivo") or detail.get("universo_declarado") or opening.get("estado_crudo", ""))[:500],
            "confianza": confidence,
            "conflicto_material": "NO",
            "nota": "Escala/diseño/universo: " + "; ".join(str(detail.get(k, "")) for k in ("escala", "es_panel", "universo_declarado") if detail.get(k))[:700],
        })

    if not result:
        seed_ref = next((r.get("seed_ref", "") for r in read_tsv(mapa / "mapa-maestro-necesidades.tsv") if r.get("necesidad_id") == need_id), "")
        result.append({
            "necesidad_id": need_id, "fuente_id_canonico": "", "fuente_nombre": "",
            "tipo_fuente": "AUSENCIA_DE_FUENTE", "objeto_evidencia_id": f"OE-SIN-CANDIDATO-{need_id}", "id_manifiesto": "", "sha256": "",
            "capa1_universo_indexado": "SIN_CANDIDATO", "capa2_manifiesto": "NO_APLICA",
            "capa3_disco_real": "NO_APLICA", "capa4_apertura_mapeo": "SIN_CANDIDATO",
            "clasificacion_relacion": "SIN_CANDIDATO", "reason_code": "UNIVERSO_SIN_CANDIDATO",
            "evidencia_ref": seed_ref or f"MAPA:mapa-maestro-necesidades.tsv:{need_id}",
            "evidencia_textual_breve": "No se registró una candidata explícita.", "confianza": "ALTA",
            "conflicto_material": "NO", "nota": "Ausencia conservada sin reducir el universo.",
        })
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapa", type=Path, required=True)
    parser.add_argument("--puente", type=Path)
    parser.add_argument("--necesidad", choices=[f"N{i}" for i in range(1, 34)])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--build-bridge", action="store_true")
    args = parser.parse_args()
    if args.build_bridge:
        rows = build_opening_bridge(args.mapa)
        write_bridge(args.output, rows)
        print(json.dumps({"puente": str(args.output), "filas": len(rows)}))
        return 0
    if not args.necesidad or not args.puente:
        parser.error("--necesidad y --puente son obligatorios para adjudicar")
    rows = adjudicate_need(args.mapa, args.puente, args.necesidad)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows) + "\n", encoding="utf-8")
    print(json.dumps({"necesidad": args.necesidad, "filas": len(rows), "sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
