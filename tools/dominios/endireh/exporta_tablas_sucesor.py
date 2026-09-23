"""Exporta tablas legibles desde RESULT sellados; nunca recalcula estimandos."""

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "forense/analisis/dominios/genero"
CALCS = {
    "2021-discriminacion": "CALC-ENDIREH-PISOS-2021-DISCRIMINACION-0001",
    "2021-pareja-nofisica-bc": "CALC-ENDIREH-PISOS-2021-NOFISICA-BC-0001",
    "2016-restantes": "CALC-ENDIREH-PISOS-2016-RESTANTES-0001",
    "2011-modulos": "CALC-ENDIREH-PISOS-2011-MODULOS-0001",
    "2006-modulos": "CALC-ENDIREH-PISOS-2006-MODULOS-0002",
}
FIELDS = ("result_id", "calc_id", "resultados_sha256", "resultado", "ventana", "eje",
          "categoria", "estado", "n", "upm", "p", "ic95_lo", "ic95_hi", "se",
          "masa_ponderada", "replicas_n", "causa")


def main():
    for name, calc_id in CALCS.items():
        base = ROOT / "data/corrida0" / calc_id
        raw = (base / "resultados.json").read_bytes()
        payload = json.loads(raw)["resultados"]
        result_id = next(k for k in payload if k.endswith("TABLA"))
        rows = json.loads(payload[result_id])
        path = OUT / f"endireh-{name}-tabla.tsv"
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t")
            writer.writeheader()
            for row in rows:
                ic = row.get("ic95", [])
                writer.writerow({
                    "result_id": result_id,
                    "calc_id": calc_id,
                    "resultados_sha256": hashlib.sha256(raw).hexdigest(),
                    "resultado": row["resultado"],
                    "ventana": row.get("ventana", ""),
                    "eje": row["eje"],
                    "categoria": row["categoria"],
                    "estado": row["estado"],
                    "n": row["n"],
                    "upm": row["upm"],
                    "p": row.get("p", ""),
                    "ic95_lo": ic[0] if ic else "",
                    "ic95_hi": ic[1] if ic else "",
                    "se": row.get("se", ""),
                    "masa_ponderada": row.get("masa_ponderada", ""),
                    "replicas_n": len(row.get("replicas", [])),
                    "causa": row.get("causa", ""),
                })
        print(f"{path.relative_to(ROOT)}: {len(rows)} celdas")


if __name__ == "__main__":
    main()
