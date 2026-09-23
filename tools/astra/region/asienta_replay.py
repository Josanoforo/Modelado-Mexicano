"""Asienta los verify ya ejecutados de U5, sin repetir filas."""
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REG = ROOT / "forense/replay-evidencia.tsv"
CALCS = ("CALC-REGION-ENIF-2024-0001", "CALC-REGION-ENIF-PORTAFOLIO-2024-0001",
         "CALC-REGION-ENCIG-2023-0001", "CALC-REGION-ENCIG-CONSUMIDORES-2025-0001",
         "CALC-REGION-ENVIPE-2024-0001", "CALC-REGION-ENVIPE-COMPLEMENTO-0001",
         "CALC-REGION-IC-PREDICTIVO-0001", "CALC-REGION-ENIF-CONDICIONALES-2024-0001",
         "CALC-REGION-ENIF-NO-TRABAJA-2024-0001",
         "CALC-REGION-ENVIPE-DENUNCIA-U4-2025-0001",
         "CALC-REGION-ENVIPE-SEGURO-2025-0001",
         *(f"CALC-REGION-HIST-{inst}-{ola}-0001" for inst, olas in
           (("ENVIPE", (2023, 2025)), ("ENCIG", (2017, 2019, 2021)),
            ("ENIF", (2018, 2021, 2024))) for ola in olas))


def main():
    with REG.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fields = reader.fieldnames
        existentes = {r["calc_id"] for r in reader}
    with REG.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        for calc in CALCS:
            if calc in existentes:
                continue
            carpeta = ROOT / "data/corrida0" / calc
            ejec = json.loads((carpeta / "ejecucion.json").read_text())
            row = {
                "calc_id": calc, "corrida_id": ejec["corrida_id"],
                "resultado_replay": "REPRODUCE", "contexto_replay": "IDENTICO",
                "razones": "corrida0 verify: sello, spec, inputs y contexto COINCIDEN; resultado REPRODUCE",
                "spec_yaml_sha256": ejec["spec_yaml_sha256"],
                "script_blob_sha256": ejec["script_blob_sha256"],
                "input_sha256_efectivos": ",".join(f"{k}={v}" for k, v in sorted(ejec["input_sha256"].items())),
                "codigo_commit": ejec["git_commit"],
                "fecha_verificacion": datetime.now(timezone.utc).date().isoformat(),
                "entorno": "CAJA; corpus montado",
                "procedencia": "VERIFY-EJECUTADO · ASTRA4-U5-EJE-REGIONAL",
                "alcance": ("IC predictivo regional retrospectivo, derivado; no adopta"
                            if calc == "CALC-REGION-IC-PREDICTIVO-0001" else
                            "piso regional retrospectivo de una conducta; no adopta"),
                "nota": "forense/analisis/region/HOJA-EJE-REGIONAL-para-mesa.md",
            }
            writer.writerow(row)
            print(calc)


if __name__ == "__main__":
    main()
