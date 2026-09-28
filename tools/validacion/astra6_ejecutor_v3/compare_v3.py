#!/usr/bin/env python3
"""Freeze an anchored v3 export before opening a reference, then compare it.

The caller retains the SHA-256 printed by `freeze` outside the mutable freeze
directory. `compare` requires that exact SHA; it never derives its expectation
from the directory it checks.
"""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
from decimal import localcontext

try:
    from . import contract, runtime
except ImportError:
    import contract  # type: ignore
    import runtime  # type: ignore

v2 = contract._v2
FIELDS = ("punto", "ic95_inf", "ic95_sup")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_new(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


def _tolerance(path):
    value = v2.read_json(path)
    if type(value) is not dict or set(value) != {"abs", "rel"}:
        raise ValueError("tolerancia v2 invalida")
    absolute, relative = v2.number(value["abs"]), v2.number(value["rel"])
    if absolute < 0 or relative < 0:
        raise ValueError("tolerancia negativa")
    return value, absolute, relative


def _normalized(path):
    result = contract.validate(v2.read_json(path))
    return {key: result[key] for key in ("version", "identidad", "filas")}


def freeze(export_dir, export_anchor, tolerance_path, destination):
    """Copy and freeze every exported byte and the tolerance before reference."""
    verified = runtime.verify_export(export_dir, export_anchor)
    export_dir, export_anchor = Path(export_dir), Path(export_anchor)
    tolerance_path, destination = Path(tolerance_path), Path(destination)
    _tolerance(tolerance_path)
    if destination.exists() or destination.is_symlink():
        raise ValueError("destino de congelacion debe ser nuevo")
    if destination.resolve(strict=False).is_relative_to(export_dir.resolve()):
        raise ValueError("congelacion dentro de exportacion mutable")
    identity = verified["anchor"]["package_identity"]
    if _normalized(export_dir / "resultado.json")["identidad"] != identity:
        raise ValueError("identidad de resultado distinta del ancla")
    destination.mkdir(mode=0o700)
    files = {}
    for item in verified["export"]["files"]:
        name = item["path"]
        target = destination / "export" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(export_dir / name, target)
        files[f"export/{name}"] = sha(target)
    fixed = {
        "export/export-manifest.json": export_dir / "export-manifest.json",
        "export-anchor.json": export_anchor,
        "tolerancia.json": tolerance_path,
        "contract.py": Path(contract.__file__),
        "compare_v3.py": Path(__file__),
        "runtime.py": Path(runtime.__file__),
        "adaptador-v2.py": Path(v2.__file__),
    }
    for name, source in fixed.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        files[name] = sha(target)
    manifest = {"version": 1, "package_identity": identity,
                "export_manifest_sha256": verified["anchor"]["export_manifest_sha256"],
                "input_manifest_sha256": verified["anchor"]["input_manifest_sha256"],
                "files": dict(sorted(files.items()))}
    write_new(destination / "freeze-manifest.json", manifest)
    return sha(destination / "freeze-manifest.json")


def verify_freeze(destination, expected_sha256):
    destination = Path(destination)
    if destination.is_symlink() or destination.resolve(strict=True) != destination.absolute():
        raise ValueError("directorio de congelacion inseguro")
    freeze_manifest = destination / "freeze-manifest.json"
    if (freeze_manifest.is_symlink() or not freeze_manifest.is_file() or
            not runtime.SHA.fullmatch(expected_sha256) or sha(freeze_manifest) != expected_sha256):
        raise ValueError("sello externo de congelacion no coincide")
    manifest = v2.read_json(destination / "freeze-manifest.json")
    if (type(manifest) is not dict or set(manifest) != {"version", "package_identity",
            "export_manifest_sha256", "input_manifest_sha256", "files"} or manifest["version"] != 1):
        raise ValueError("manifiesto de congelacion invalido")
    files = manifest["files"]
    if type(files) is not dict or not files:
        raise ValueError("archivos congelados invalidos")
    for name, expected in files.items():
        if str(runtime.safe_path(name)) != name or not runtime.SHA.fullmatch(expected):
            raise ValueError("ruta o SHA congelado invalido")
        path = destination / name
        if path.is_symlink() or not path.is_file() or sha(path) != expected:
            raise ValueError("archivo congelado alterado: " + name)
    paths = list(destination.rglob("*"))
    if any(path.is_symlink() or not (path.is_file() or path.is_dir()) for path in paths):
        raise ValueError("miembro de congelacion inseguro")
    actual = {p.relative_to(destination).as_posix() for p in paths if p.is_file()}
    if actual != set(files) | {"freeze-manifest.json"}:
        raise ValueError("archivos de congelacion faltantes o extra")
    for name, source in {"contract.py": Path(contract.__file__),
                         "compare_v3.py": Path(__file__),
                         "runtime.py": Path(runtime.__file__),
                         "adaptador-v2.py": Path(v2.__file__)}.items():
        if sha(source) != files[name]:
            raise ValueError("codigo comparador activo distinto del congelado: " + name)
    verified = runtime.verify_export(destination / "export", destination / "export-anchor.json")
    if (verified["anchor"]["package_identity"] != manifest["package_identity"] or
            verified["anchor"]["input_manifest_sha256"] != manifest["input_manifest_sha256"] or
            verified["anchor"]["export_manifest_sha256"] != manifest["export_manifest_sha256"]):
        raise ValueError("ancla de exportacion incompatible con congelacion")
    _tolerance(destination / "tolerancia.json")
    return manifest


def compare(destination, expected_sha256, reference_path, expected_reference_sha256):
    """Verify all frozen objects before the first reference read."""
    manifest = verify_freeze(destination, expected_sha256)
    if not runtime.SHA.fullmatch(expected_reference_sha256) or sha(reference_path) != expected_reference_sha256:
        raise ValueError("SHA externo de referencia no coincide")
    destination = Path(destination)
    actual = _normalized(destination / "export/resultado.json")
    reference = _normalized(reference_path)
    if actual["identidad"] != reference["identidad"] or actual["identidad"] != manifest["package_identity"]:
        raise ValueError("identidad de referencia incompatible")
    rows_a = {row["llave"]: row for row in actual["filas"]}
    rows_b = {row["llave"]: row for row in reference["filas"]}
    if set(rows_a) != set(rows_b):
        raise ValueError("conjunto de llaves incompatible")
    tolerance, absolute, relative = _tolerance(destination / "tolerancia.json")
    results = []
    for key, row in rows_a.items():
        target = rows_b[key]
        if row["unidad"] != target["unidad"]:
            raise ValueError("unidad incompatible: " + key)
        fields = {}
        for field in FIELDS:
            present_a, present_b = field in row, field in target
            item = {"estado_actual": "NUMERO" if present_a else "AUSENTE",
                    "estado_referencia": "NUMERO" if present_b else "AUSENTE",
                    "dentro": present_a == present_b}
            if present_a and present_b:
                da, db = v2.number(row[field]), v2.number(target[field])
                with localcontext() as context:
                    values = (da, db, absolute, relative)
                    context.prec = max(64, sum(len(v.as_tuple().digits) + abs(v.as_tuple().exponent) for v in values) + 8)
                    delta = da - db
                    item.update(delta=str(delta), dentro=abs(delta) <= max(absolute, relative * max(abs(da), abs(db))))
            fields[field] = item
        state_match = row["estado"] == target["estado"]
        ic_match = row.get("estado_ic") == target.get("estado_ic")
        match = state_match and ic_match and all(item["dentro"] for item in fields.values())
        results.append({"llave": key, "estado": "COINCIDE" if match else "DISCREPA",
                        "estado_actual": row["estado"], "estado_referencia": target["estado"],
                        "estado_ic_actual": row.get("estado_ic"), "estado_ic_referencia": target.get("estado_ic"),
                        "causas": ([] if state_match else ["estado_fila"]) +
                                  ([] if ic_match else ["estado_ic"]) +
                                  [field for field, item in fields.items() if not item["dentro"]],
                        "campos": fields})
    return {"version": 3, "identidad": actual["identidad"],
            "congelacion_sha256": expected_sha256,
            "referencia_sha256": expected_reference_sha256,
            "tolerancia_sha256": manifest["files"]["tolerancia.json"],
            "tolerancia": tolerance, "resultados": results,
            "estado": "COINCIDE" if all(row["estado"] == "COINCIDE" for row in results) else "DISCREPA"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    one = sub.add_parser("freeze")
    one.add_argument("--export", required=True)
    one.add_argument("--export-anchor", required=True)
    one.add_argument("--tolerance", required=True)
    one.add_argument("--output", required=True)
    two = sub.add_parser("compare")
    two.add_argument("--frozen", required=True)
    two.add_argument("--expected-sha256", required=True)
    two.add_argument("--reference", required=True)
    two.add_argument("--reference-sha256", required=True)
    two.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.command == "freeze":
        print(freeze(args.export, args.export_anchor, args.tolerance, args.output))
    else:
        write_new(args.output, compare(args.frozen, args.expected_sha256, args.reference, args.reference_sha256))


if __name__ == "__main__":
    main()
