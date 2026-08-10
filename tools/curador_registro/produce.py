#!/usr/bin/env python3
"""Ejecuta una especificación descriptiva opaca sin interpretación semántica."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import shutil
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Any


MATERIAL_FIELDS = (
    "poblacion", "dominio", "unidad_observacion", "ponderador", "incertidumbre",
    "edicion", "periodo_levantamiento", "hash_microdato", "evidencia_ref",
    "evidencia_neutral_ref", "hash_evidencia_neutral",
)
FORBIDDEN = {"necesidad_id", "relacion_id", "objeto_modelo_origen", "decision_pendiente", "interpretacion_deseada", "signo_esperado", "resultado_favorable", "supervisor_link"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_records(spec: dict[str, Any]) -> list[dict[str, str]]:
    path = Path(spec["input_path"])
    member = spec.get("input_member", "")
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive, archive.open(member) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8-sig", errors="strict", newline="")
            return list(csv.DictReader(text))
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def reference_period(spec: dict[str, Any], variable: str) -> str:
    """Return the question's reference window, never the survey edition."""
    by_variable = spec.get("periodo_referencia_por_variable", {})
    return by_variable.get(variable, "NO_DETERMINADO")


def taylor_distribution(records: list[dict[str, str]], variable: str, categories: list[dict[str, str]], weight_field: str, stratum_field: str, psu_field: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int, float, str]:
    allowed = {entry["codigo"] for entry in categories}
    unexpected = sorted({(row.get(variable) or "").strip() for row in records if (row.get(variable) or "").strip() not in allowed and (row.get(variable) or "").strip()})
    if unexpected:
        raise ValueError(f"CODIGOS_INESPERADOS:{variable}:{unexpected}")
    required = {variable, weight_field, stratum_field, psu_field}
    missing_columns = required - set(records[0]) if records else required
    if missing_columns:
        raise ValueError(f"COLUMNAS_FALTANTES:{sorted(missing_columns)}")
    valid: list[tuple[str, float, str, str]] = []
    missing_n = 0
    for row in records:
        code = (row.get(variable) or "").strip()
        if not code:
            missing_n += 1
            continue
        try:
            weight = float((row.get(weight_field) or "").strip())
        except ValueError as exc:
            raise ValueError(f"PESO_INVALIDO:{weight_field}") from exc
        stratum = (row.get(stratum_field) or "").strip()
        psu = (row.get(psu_field) or "").strip()
        if not stratum or not psu or not math.isfinite(weight) or weight <= 0:
            raise ValueError("DISENO_O_PESO_INVALIDO")
        valid.append((code, weight, stratum, psu))
    total_weight = sum(weight for _, weight, _, _ in valid)
    if not valid or total_weight <= 0:
        raise ValueError("SIN_OBSERVACIONES_VALIDAS")
    estimates: list[dict[str, Any]] = []
    uncertainties: list[dict[str, Any]] = []
    empty_cells: list[str] = []
    for category in categories:
        code = category["codigo"]
        category_n = sum(value == code for value, _, _, _ in valid)
        category_weight = sum(weight for value, weight, _, _ in valid if value == code)
        if category_n == 0:
            empty_cells.append(code)
            estimates.append({
                "codigo": code, "etiqueta": category["etiqueta"],
                "n_categoria": 0, "suma_pesos_categoria": 0,
                "proporcion": "NO_ESTIMABLE",
                "estado_celda": "SIN_OBSERVACIONES_ESTIMACION_NO_SUSTENTADA",
            })
            uncertainties.append({
                "codigo": code, "error_estandar": "NO_ESTIMABLE",
                "ic95_inferior": "NO_ESTIMABLE", "ic95_superior": "NO_ESTIMABLE",
                "estado_celda": "SIN_OBSERVACIONES_ESTIMACION_NO_SUSTENTADA",
            })
            continue
        proportion = category_weight / total_weight
        psu_z: dict[tuple[str, str], float] = defaultdict(float)
        psus_by_stratum: dict[str, set[str]] = defaultdict(set)
        for value, weight, stratum, psu in valid:
            psu_z[(stratum, psu)] += weight * ((1.0 if value == code else 0.0) - proportion)
            psus_by_stratum[stratum].add(psu)
        variance_total = 0.0
        singleton_strata: set[str] = set()
        for stratum, psus in psus_by_stratum.items():
            m = len(psus)
            if m < 2:
                singleton_strata.add(stratum)
                continue
            values = [psu_z[(stratum, psu)] for psu in psus]
            mean = sum(values) / m
            variance_total += (m / (m - 1)) * sum((value - mean) ** 2 for value in values)
        if singleton_strata:
            raise ValueError(f"ESTRATOS_UNA_UPM:{sorted(singleton_strata)}")
        se = math.sqrt(max(0.0, variance_total / (total_weight ** 2)))
        estimates.append({
            "codigo": code, "etiqueta": category["etiqueta"],
            "n_categoria": category_n,
            "suma_pesos_categoria": round(category_weight, 6), "proporcion": round(proportion, 10),
            "estado_celda": "ESTIMACION_SUSTENTADA",
        })
        uncertainties.append({
            "codigo": code, "error_estandar": round(se, 10),
            "ic95_inferior": round(max(0.0, proportion - 1.96 * se), 10),
            "ic95_superior": round(min(1.0, proportion + 1.96 * se), 10),
            "estado_celda": "ESTIMACION_SUSTENTADA",
        })
    empty_note = ",".join(empty_cells) if empty_cells else "ninguna"
    reserve = (
        f"faltantes_blancos={missing_n}; todas las categorías oficiales se conservaron; "
        f"celdas_sin_observaciones={empty_note}"
    )
    return estimates, uncertainties, len(valid), total_weight, reserve


RESULT_FIELDS = [
    "especificacion_id", "variable", "tipo_producto", "estimando", "estimacion", "incertidumbre",
    "poblacion", "dominio", "unidad", "periodo", "periodo_referencia", "edicion", "periodo_levantamiento",
    "n", "suma_pesos", "ponderacion_diseno", "transformacion", "tipo_inferencia", "input_path",
    "input_member", "hash_microdato", "hash_especificacion_input", "evidencia_ref", "estado", "reserva",
]


def execute(spec_path: Path, output_dir: Path) -> dict[str, Any]:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    forbidden = FORBIDDEN.intersection(spec)
    if forbidden:
        raise ValueError(f"contexto semántico prohibido: {sorted(forbidden)}")
    output_dir.mkdir(parents=True, exist_ok=True)
    received = output_dir / "especificacion-recibida.json"
    if received.resolve() != spec_path.resolve():
        shutil.copy2(spec_path, received)
    input_path = Path(spec.get("input_path", ""))
    input_hash = sha256(input_path) if input_path.is_file() else "NO_DETERMINADO"
    expected_input_hash = spec.get("hash_microdato", "NO_DETERMINADO")
    if expected_input_hash not in {"", "NO_DETERMINADO"} and input_hash != expected_input_hash:
        raise ValueError(
            f"HASH_MICRODATO_NO_COINCIDE:{input_path}:{expected_input_hash}:{input_hash}"
        )
    specification_hash = sha256(received)
    rows: list[dict[str, str]] = []
    material_missing = [field for field in MATERIAL_FIELDS if spec.get(field) in {None, "", "NO_DETERMINADO"}]
    design = spec.get("diseno_muestral", {})
    for key in ("estrato", "conglomerado"):
        if design.get(key) in {None, "", "NO_DETERMINADO"}: material_missing.append(f"diseno_muestral.{key}")
    if spec.get("input_member") in {None, "", "NO_DETERMINADO"}: material_missing.append("input_member")
    if input_hash == "NO_DETERMINADO": material_missing.append("input_path")
    for variable in spec.get("variables", []):
        if reference_period(spec, variable) in {None, "", "NO_DETERMINADO"}:
            material_missing.append(f"periodo_referencia_por_variable.{variable}")
    if material_missing:
        for variable in spec["variables"]:
            period = reference_period(spec, variable)
            rows.append({
                "especificacion_id": spec["especificacion_id"], "variable": variable,
                "tipo_producto": "DISTRIBUCION_DESCRIPTIVA", "estimando": spec["estimando"],
                "estimacion": "NO_DETERMINADO", "incertidumbre": "NO_DETERMINADO",
                "poblacion": spec.get("poblacion", "NO_DETERMINADO"),
                "dominio": spec.get("dominio", "NO_DETERMINADO"),
                "unidad": spec.get("unidad_observacion", "NO_DETERMINADO"),
                "periodo": period, "periodo_referencia": period,
                "edicion": spec.get("edicion", "NO_DETERMINADO"),
                "periodo_levantamiento": spec.get("periodo_levantamiento", "NO_DETERMINADO"),
                "n": "NO_DETERMINADO", "suma_pesos": "NO_DETERMINADO", "ponderacion_diseno": stable_json(design),
                "transformacion": spec["transformacion"], "tipo_inferencia": spec["tipo_inferencia"],
                "input_path": str(input_path), "input_member": spec.get("input_member", "NO_DETERMINADO"),
                "hash_microdato": input_hash, "hash_especificacion_input": specification_hash,
                "evidencia_ref": spec["evidencia_ref"], "estado": "NO_DETERMINADO",
                "reserva": "campos_materiales_faltantes:" + ",".join(sorted(set(material_missing))),
            })
    else:
        records = load_records(spec)
        for variable in spec["variables"]:
            period = reference_period(spec, variable)
            try:
                estimates, uncertainty, n, total_weight, reserve = taylor_distribution(records, variable, spec["codificacion"][variable], spec["ponderador"], design["estrato"], design["conglomerado"])
                rows.append({
                    "especificacion_id": spec["especificacion_id"], "variable": variable,
                    "tipo_producto": "DISTRIBUCION_DESCRIPTIVA", "estimando": spec["estimando"],
                    "estimacion": stable_json(estimates), "incertidumbre": stable_json(uncertainty),
                    "poblacion": spec["poblacion"], "dominio": spec["dominio"],
                    "unidad": spec["unidad_observacion"], "periodo": period, "periodo_referencia": period,
                    "edicion": spec["edicion"], "periodo_levantamiento": spec["periodo_levantamiento"], "n": str(n),
                    "suma_pesos": f"{total_weight:.6f}", "ponderacion_diseno": stable_json(design),
                    "transformacion": spec["transformacion"], "tipo_inferencia": spec["tipo_inferencia"],
                    "input_path": str(input_path), "input_member": spec["input_member"],
                    "hash_microdato": input_hash, "hash_especificacion_input": specification_hash,
                    "evidencia_ref": spec["evidencia_ref"], "estado": "CALCULO_REPRODUCIBLE", "reserva": reserve,
                })
            except ValueError as exc:
                rows.append({
                    "especificacion_id": spec["especificacion_id"], "variable": variable,
                    "tipo_producto": "DISTRIBUCION_DESCRIPTIVA", "estimando": spec["estimando"],
                    "estimacion": "NO_DETERMINADO", "incertidumbre": "NO_DETERMINADO",
                    "poblacion": spec["poblacion"], "dominio": spec["dominio"], "unidad": spec["unidad_observacion"],
                    "periodo": period, "periodo_referencia": period, "edicion": spec["edicion"],
                    "periodo_levantamiento": spec["periodo_levantamiento"],
                    "n": "NO_DETERMINADO", "suma_pesos": "NO_DETERMINADO",
                    "ponderacion_diseno": stable_json(design), "transformacion": spec["transformacion"],
                    "tipo_inferencia": spec["tipo_inferencia"], "evidencia_ref": spec["evidencia_ref"],
                    "input_path": str(input_path), "input_member": spec["input_member"],
                    "hash_microdato": input_hash, "hash_especificacion_input": specification_hash,
                    "estado": "NO_DETERMINADO", "reserva": str(exc),
                })
    result_path = output_dir / "resultado.tsv"
    with result_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESULT_FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    launcher = output_dir / "analisis-reproducible.py"
    launcher.write_text(
        "import json\n"
        "import sys\n"
        "from pathlib import Path\n"
        "\n"
        "root = Path(__file__).resolve().parent\n"
        "repo_root = next(parent for parent in root.parents if (parent / 'tools/curador_registro/produce.py').is_file())\n"
        "sys.path.insert(0, str(repo_root))\n"
        "from tools.curador_registro.produce import execute\n\n"
        "if __name__ == '__main__':\n"
        "    result = execute(root / 'especificacion-recibida.json', root)\n"
        "    print(json.dumps({'ok': True, **result}, ensure_ascii=False, indent=2, sort_keys=True))\n",
        encoding="utf-8",
    )
    summary = {
        "especificacion_id": spec["especificacion_id"],
        "variables": len(rows),
        "calculos_reproducibles": sum(row["estado"] == "CALCULO_REPRODUCIBLE" for row in rows),
        "no_determinado": sum(row["estado"] == "NO_DETERMINADO" for row in rows),
        "cegado": True,
        "motor": "tools/curador_registro/produce.py",
        "hash_microdato_verificado": input_hash,
        "hash_especificacion_recibida": specification_hash,
    }
    (output_dir / "resumen.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    hashes = {path.name: sha256(path) for path in (received, result_path, launcher, output_dir / "resumen.json")}
    (output_dir / "hashes.json").write_text(json.dumps(hashes, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = execute(args.spec.resolve(), args.output_dir.resolve())
    print(json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
