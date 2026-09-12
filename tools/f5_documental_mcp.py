#!/usr/bin/env python3
"""MCP minimo para analizar un TSV sin exponer el resto del sistema de archivos."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path


def _respuesta(req_id, result=None, error=None):
    out = {"jsonrpc": "2.0", "id": req_id}
    if error is not None:
        out["error"] = error
    else:
        out["result"] = result
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _ruta_segura(root: Path, relativa: str) -> Path:
    candidato = (root / relativa).resolve()
    try:
        candidato.relative_to(root)
    except ValueError as exc:
        raise ValueError("ruta fuera del paquete aislado") from exc
    if candidato.suffix.lower() != ".tsv" or not candidato.is_file():
        raise ValueError("el TSV solicitado no existe en el paquete")
    return candidato


def distribucion_ponderada(root: Path, args: dict) -> dict:
    ruta = _ruta_segura(root, str(args.get("path", "")))
    valor = str(args.get("value_column", ""))
    peso = str(args.get("weight_column", ""))
    acumulado = defaultdict(float)
    conteo = defaultdict(int)
    filas = 0
    omitidas = 0
    with ruta.open(encoding="utf-8", newline="") as f:
        lector = csv.DictReader(f, delimiter="\t")
        columnas = lector.fieldnames or []
        if valor not in columnas or peso not in columnas:
            raise ValueError(f"columnas invalidas; disponibles={columnas}")
        for fila in lector:
            filas += 1
            categoria = fila.get(valor, "")
            bruto = fila.get(peso, "")
            if categoria == "" or bruto == "":
                omitidas += 1
                continue
            try:
                w = float(bruto)
            except ValueError:
                omitidas += 1
                continue
            if w < 0:
                raise ValueError("ponderador negativo")
            conteo[categoria] += 1
            acumulado[categoria] += w
    total = sum(acumulado.values())
    return {
        "path": ruta.name,
        "sha256": hashlib.sha256(ruta.read_bytes()).hexdigest(),
        "rows_read": filas,
        "rows_omitted_missing_or_invalid": omitidas,
        "value_column": valor,
        "weight_column": peso,
        "distribution": [
            {
                "value": k,
                "unweighted_n": conteo[k],
                "weighted_sum": acumulado[k],
                "weighted_share_of_nonmissing": (acumulado[k] / total if total else None),
            }
            for k in sorted(acumulado)
        ],
        "weighted_total_nonmissing": total,
    }


HERRAMIENTA = {
    "name": "weighted_distribution",
    "description": (
        "Lee por completo un TSV del paquete aislado y devuelve la distribucion de una "
        "columna por otra columna de ponderacion. No puede abrir rutas fuera del paquete."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "value_column": {"type": "string"},
            "weight_column": {"type": "string"},
        },
        "required": ["path", "value_column", "weight_column"],
        "additionalProperties": False,
    },
}


def servir(root: Path) -> int:
    root = root.resolve()
    for linea in sys.stdin:
        try:
            req = json.loads(linea)
            metodo = req.get("method")
            req_id = req.get("id")
            if metodo == "initialize":
                _respuesta(req_id, {
                    "protocolVersion": req.get("params", {}).get("protocolVersion", "2025-06-18"),
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "f5-documental-aislado", "version": "1.0.0"},
                })
            elif metodo == "tools/list":
                _respuesta(req_id, {"tools": [HERRAMIENTA]})
            elif metodo == "tools/call":
                params = req.get("params", {})
                if params.get("name") != HERRAMIENTA["name"]:
                    raise ValueError("herramienta no permitida")
                resultado = distribucion_ponderada(root, params.get("arguments", {}))
                _respuesta(req_id, {"content": [{"type": "text", "text": json.dumps(resultado, ensure_ascii=False)}]})
            elif metodo in {"notifications/initialized", "notifications/cancelled"}:
                continue
            elif req_id is not None:
                _respuesta(req_id, error={"code": -32601, "message": "metodo no soportado"})
        except Exception as exc:  # la frontera MCP debe devolver el error, no filtrar trazas
            if "req_id" in locals() and req_id is not None:
                _respuesta(req_id, error={"code": -32000, "message": str(exc)})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    args = ap.parse_args()
    return servir(args.root)


if __name__ == "__main__":
    raise SystemExit(main())
