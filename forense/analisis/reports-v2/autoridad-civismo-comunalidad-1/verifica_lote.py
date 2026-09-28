#!/usr/bin/env python3
"""Deriva el índice local de decisiones de las tres piezas y comprueba identidades."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PIECES = ("autoridad", "civismo", "comunalidad")
ENCARGO = Path("forense/encargos/fuentes/ASTRA6-tanda5-20260927/02-ASTRA6-C3-AUTORIDAD-CIVISMO-COMUNALIDAD-1.md")
CORTE = "f0608c7b"
ARCHIVO_INICIAL = "forense/encargos/2026-09-27-ASTRA6-C3-AUTORIDAD-CIVISMO-COMUNALIDAD-1.md"
MANIFIESTO = Path("forense/encargos/fuentes/ASTRA6-tanda5-20260927/ASTRA6-tanda5-SHA256SUMS.txt")
ESTADOS = ("CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA")


def suma_cifras(value):
    if isinstance(value, list):
        return str(len(value))
    if isinstance(value, int):
        return str(value)
    if isinstance(value, dict):
        for key in ("propias_result", "result_propios", "propios_result"):
            if key in value:
                return str(value[key])
    return "véase expediente"


def preparar():
    original = subprocess.check_output(["git", "show", f"{CORTE}:{ENCARGO}"], cwd=ROOT)
    recibido = (ROOT / ENCARGO).read_bytes()
    if not recibido.startswith(original):
        raise SystemExit("ERROR: cuerpo canónico de tanda5 alterado")
    if subprocess.check_output(["git", "show", f"3a1f0be1:{ARCHIVO_INICIAL}"], cwd=ROOT) != original:
        raise SystemExit("ERROR: la fuente del 0-bis propio difiere del archivo canónico")
    digest = hashlib.sha256(original).hexdigest()
    if digest != "8d84587787d00ba3fbeb479dcc749c6e83e47386f6afffa47ed3bb3bbe100124":
        raise SystemExit("ERROR: SHA crudo del cuerpo recibido")
    if f"{digest}  {ENCARGO.name}" not in (ROOT / MANIFIESTO).read_text():
        raise SystemExit("ERROR: falta SHA del encargo en manifiesto de tanda5")

    summaries = {}
    lines = [
        "# Índice local · autoridad, civismo y comunalidad",
        "",
        "Conteos derivados de juicios editoriales explícitos. Los registros y las filas del mapa pueden solaparse; no son tesis independientes ni población de encuesta.",
        "",
        "| Report | Registros | Filas mapa | CONFIRMA | MATIZA | ROMPE | SIN-CIFRA | RESULT propios usados |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for piece in PIECES:
        summary = json.loads((HERE / piece / "resumen.json").read_text())
        counts = summary["dictamenes"]
        if any(key not in counts for key in ESTADOS) or sum(counts[k] for k in ESTADOS) != summary["registros"]:
            raise SystemExit(f"ERROR: conteos inconsistentes de {piece}")
        report = ROOT / summary["report"]
        if not report.is_file() or not report.read_text().strip():
            raise SystemExit(f"ERROR: falta report de {piece}")
        summaries[piece] = summary
        lines.append(
            f"| [{piece}](../../../../{summary['report']}) | {summary['registros']} | "
            f"{summary['mapa_filas']} | " + " | ".join(str(counts[k]) for k in ESTADOS)
            + f" | {suma_cifras(summary.get('cifras'))} |"
        )
    lines += [
        "",
        "Los dictámenes detallados, fuentes, reservas y comandos de reproducción están en las tres carpetas de pieza. "
        "Ningún report adopta reglas ni reemplaza las cifras de un instrumento reservado.",
        "",
    ]
    paths = [ROOT / summaries[p]["report"] for p in PIECES]
    for piece in PIECES:
        paths.extend(p for p in (HERE / piece).rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}
    return {
        HERE / "indice-local.md": "\n".join(lines),
        HERE / "resumen-lote.json": json.dumps(summaries, ensure_ascii=False, indent=2) + "\n",
        HERE / "hashes-producto.json": json.dumps(hashes, ensure_ascii=False, indent=2) + "\n",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for path, expected in preparar().items():
        if args.check:
            if not path.exists() or path.read_text() != expected:
                raise SystemExit(f"ERROR: difiere {path.relative_to(ROOT)}")
        else:
            path.write_text(expected)
    print("VERDE: tres piezas e índice local reproducible")


if __name__ == "__main__":
    main()
