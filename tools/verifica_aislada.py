#!/usr/bin/env python3
"""Ejecuta ``corrida0 verify`` en un intérprete nuevo por CALC.

La salida JSON separa el resultado del replay, su contexto y la identidad.
No interpreta un exit code como ``REPRODUCE``: conserva stdout/stderr y marca
las limitaciones del proceso hijo como tales.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _sha(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def verificar(calc_id: str, *, root: Path = ROOT) -> dict:
    """Verifica un CALC en un proceso nuevo y devuelve evidencia serializable."""
    calc = root / "data" / "corrida0" / calc_id
    spec = calc / "spec.yaml"
    script = calc / "medidor.py"
    # No se usa el CLI para inferir el veredicto de texto: el hijo importa la
    # misma función y serializa su objeto estructurado. Así cada invocación
    # empieza sin módulos de otro CALC y conserva resultado/contexto/deltas.
    codigo = (
        "import json; import tools.corrida0 as c; "
        "e=json.load(open('data/corrida0/'+__import__('sys').argv[1]+'/ejecucion.json')); "
        "r=c.verify(__import__('sys').argv[1], imprime=False); "
        "i=c._identidad_replay(e); "
        "print(json.dumps({'verify':r,'identidad':{'spec_yaml_sha256':i[0],"
        "'script_blob_sha256':i[1],'input_sha256_efectivos':i[2]}},ensure_ascii=False))"
    )
    cmd = [sys.executable, "-c", codigo, calc_id]
    hijo = subprocess.run(cmd, cwd=root, text=True, capture_output=True, check=False)
    texto = hijo.stdout + ("\n" if hijo.stdout and hijo.stderr else "") + hijo.stderr
    try:
        payload = json.loads(hijo.stdout)
        ver = payload["verify"]
        resultado = ver["veredicto"]
        contexto = ver.get("contexto", "NO-VERIFICABLE")
        identidad = payload["identidad"]
    except (ValueError, KeyError, TypeError):
        resultado, contexto = "NO-EJECUTABLE", "NO-VERIFICABLE"
        identidad = {"spec_yaml_sha256": _sha(spec),
                     "script_blob_sha256": _sha(script),
                     "input_sha256_efectivos": None}
        ver = {"razones_contexto": ["hijo_no_serializo_verify"]}
    return {
        "calc_id": calc_id,
        "fecha_verificacion": date.today().isoformat(),
        "proceso_aislado": True,
        "comando": cmd,
        "exit_code": hijo.returncode,
        "resultado_replay": resultado,
        "contexto_replay": contexto,
        "identidad": identidad,
        "detalle_verify": ver,
        "salida_cruda": texto,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("calc_id", nargs="+")
    p.add_argument("--salida", type=Path)
    ns = p.parse_args()
    filas = [verificar(i) for i in ns.calc_id]
    texto = json.dumps(filas, ensure_ascii=False, indent=2) + "\n"
    if ns.salida:
        ns.salida.parent.mkdir(parents=True, exist_ok=True)
        ns.salida.write_text(texto, encoding="utf-8")
    else:
        print(texto, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
