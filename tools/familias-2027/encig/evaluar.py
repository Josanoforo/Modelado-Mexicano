"""Entrada COMMIT-3 futura: verificación material antes de cualquier ZIP.

No concede autorización ni descubre un descriptor. No ejecutado con datos reales
en COMMIT-1/2. El operador del circuito de mesa debe aportar el asiento firmado.
"""
import argparse
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
AREA = ROOT / "forense/analisis/familias-2027/astra6-encig"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--payload", required=True)
    parser.add_argument("--salida", required=True)
    args = parser.parse_args()
    target = Path(args.salida).resolve()
    canonical = ROOT / "data/corrida0/CALC-FAMILIA-2027-ENCIG-APERTURA-0001/resultado.json"
    if target != canonical:
        raise SystemExit("SALIDA-FUERA-DE-APERTURA-UNICA:" + str(canonical))
    if target.exists():
        raise SystemExit("APERTURA-EXISTENTE: no sustituir ni repetir COMMIT-3")
    inventory = json.loads((AREA / "commit-1-hashes.json").read_text())
    for file, sha in inventory["archivos"].items():
        if hashlib.sha256((ROOT / file).read_bytes()).hexdigest() != sha:
            raise SystemExit("CODIGO-O-SPEC-DISCREPA:" + file)
    src = ROOT / "tools/familias-2027/encig/lector.py"
    spec = yaml.safe_load(src.with_name("evaluacion-spec.yaml").read_text())
    rules = yaml.safe_load((ROOT / spec["reglas_normativas_ruta"]).read_text())["parametros"]
    data = src.read_bytes()
    if hashlib.sha256(data).hexdigest() != spec["codigo_sha256"]:
        raise SystemExit("LECTOR-DISCREPA")
    # Compila exactamente los bytes comprobados; no importa contenido mutable.
    module = {"__file__": str(src), "__name__": "encig_congelado"}
    exec(compile(data, str(src), "exec"), module)
    pisos = json.loads((AREA / "pisos.json").read_text())
    metadata = json.loads(Path(args.metadata).read_text())
    # Una sola ejecución del paquete, incluso si un error ocurre tras abrir.
    # Un fallo conserva el asiento; no se habilitan reintentos automáticos.
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.with_name("apertura-iniciada.json").open("x") as opening:
        json.dump({"metadata": args.metadata, "estado": "INTENTO-UNICO",
                   "ola": "encig_2027"}, opening)
    payload = module["abrir_futuro"](args.payload, metadata, rules, pisos)
    scalar = module["resultados_futuros"](payload)
    # Persistir primer resultado, vector R_k y diferencias frente a p0.
    for name, f in payload.get("familias", {}).items():
        p0 = pisos["familias"][name]["p0"]
        f["d_replicas"] = [None if r is None else r - p0 for r in f["replicas"]]
    result = {"resultados": scalar, "evidencia": payload, "codigo_sha256": spec["codigo_sha256"],
              "metadata_sha256": hashlib.sha256(Path(args.metadata).read_bytes()).hexdigest()}
    # Exclusivo: ni siquiera un segundo proceso puede reemplazar el primero.
    with target.open("x") as handle:
        json.dump(result, handle, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print("COMMIT-3-PROPUESTO: resultado guardado; sellar por circuito autorizado")


if __name__ == "__main__":
    main()
