#!/usr/bin/env python3
"""Asienta la evidencia aislada del sucesor ENCUCI, tras validar su identidad."""
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCIA = Path(__file__).with_name("evidencia-replay-dirigido-v1_1.json")
TSV = ROOT / "forense" / "replay-evidencia.tsv"
CALC = "CALC-ENCUCI2020-RESPUESTA-POR-CONTACTO-0001-v1_1"
HEAD = [
    "calc_id", "corrida_id", "resultado_replay", "contexto_replay", "razones",
    "spec_yaml_sha256", "script_blob_sha256", "input_sha256_efectivos",
    "codigo_commit", "fecha_verificacion", "entorno", "procedencia", "alcance", "nota",
]


def main():
    evidencia = json.loads(EVIDENCIA.read_text(encoding="utf-8"))
    if len(evidencia) != 1 or evidencia[0].get("calc_id") != CALC:
        raise SystemExit("evidencia dirigida inesperada")
    x = evidencia[0]
    if (x.get("exit_code"), x.get("resultado_replay"), x.get("contexto_replay")) != (0, "REPRODUCE", "IDENTICO"):
        raise SystemExit("el replay dirigido no acredita REPRODUCE/IDENTICO")

    ejecucion = json.loads((ROOT / "data" / "corrida0" / CALC / "ejecucion.json").read_text(encoding="utf-8"))
    identidad = x["identidad"]
    for campo in ("spec_yaml_sha256", "script_blob_sha256"):
        if ejecucion.get(campo) != identidad.get(campo):
            raise SystemExit(f"identidad {campo} no coincide con la corrida sellada")
    insumos = ",".join(f"{k}={v}" for k, v in sorted(ejecucion.get("input_sha256", {}).items()))
    if insumos != identidad.get("input_sha256_efectivos"):
        raise SystemExit("identidad input_sha256_efectivos no coincide con la corrida sellada")

    with TSV.open(encoding="utf-8", newline="") as archivo:
        filas = list(csv.DictReader(archivo, delimiter="\t"))
    if not filas or list(filas[0]) != HEAD:
        raise SystemExit("esquema replay-evidencia.tsv inesperado")
    previas = [fila for fila in filas if fila["calc_id"] == CALC]
    nueva = {
        "calc_id": CALC,
        "corrida_id": ejecucion["corrida_id"],
        "resultado_replay": x["resultado_replay"],
        "contexto_replay": x["contexto_replay"],
        "razones": "verify aislado REPRODUCE; CONTEXTO=IDENTICO; 12/12 RESULT; 1/1 input COINCIDE",
        "spec_yaml_sha256": identidad["spec_yaml_sha256"],
        "script_blob_sha256": identidad["script_blob_sha256"],
        "input_sha256_efectivos": identidad["input_sha256_efectivos"],
        "codigo_commit": ejecucion["git_commit"],
        "fecha_verificacion": x["fecha_verificacion"],
        "entorno": "CAJA (Ubuntu/WSL2) con corpus montado",
        "procedencia": "VERIFY-DIRIGIDO · GEN2-ENCUCI2020-RESPUESTA-POR-CONTACTO-CLI-2",
        "alcance": "Sucesor v1_1; 12 RESULT sellados; validaciones de diez contactos; sin adopción",
        "nota": "forense/analisis/encuci2020-respuesta-por-contacto-cli-2/evidencia-replay-dirigido-v1_1.json",
    }
    if previas:
        if previas != [nueva]:
            raise SystemExit("ya existe un asiento propio distinto; no se sobrescribe")
        print("asiento_existente=1")
        return
    with TSV.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=HEAD, delimiter="\t", lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(filas + [nueva])
    print("asientos_nuevos=1")


if __name__ == "__main__":
    main()
