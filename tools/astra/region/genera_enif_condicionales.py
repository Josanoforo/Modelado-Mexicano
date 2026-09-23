"""Congela contrato ENIF condicionales antes de su primera corrida."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import yaml

from tools.astra.region.enif_condicionales import CONDUCTAS

ROOT = Path(__file__).resolve().parents[3]
CALC = "CALC-REGION-ENIF-CONDICIONALES-2024-0001"
P = ROOT / "data/corrida0" / CALC
MD = ROOT / "forense/prereg-caja/REGION-ENIF-CONDICIONALES-spec-v1_0.md"
CODE = ROOT / "tools/astra/region/enif_condicionales.py"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    P.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CODE, P / "medidor.py")
    base = ROOT / "data/corrida0/CALC-REGION-ENIF-PORTAFOLIO-2024-0001/spec.yaml"
    spec = yaml.safe_load(base.read_text(encoding="utf-8"))
    spec.update(calc_id=CALC,
        spec_md="../../../forense/prereg-caja/" + MD.name,
        spec_md_sha256=sha(MD), script=f"data/corrida0/{CALC}/medidor.py",
        universo="personas elegidas ENIF 2024 18+ en seis dominios condicionales separados",
        filtros="P4_10 válido y P3_13 por seguridad social; P5_20 válido y P5_23 por conocimiento; guardias G-C1/G-C2",
        transformacion="razón ponderada por dominio y región oficial, IC bootstrap compartido y R2",
        estimando="tasas regionales condicionales de horizonte y desconfianza",
        variables=[dict(archivo="TMODULO.csv", variable=x, rol=rol) for x, rol in
                   (("REGION", "geografía"), ("EDAD_V", "edad 18+"),
                    ("FAC_PER", "factor"), ("EST_DIS", "estrato"), ("UPM_DIS", "UPM"),
                    ("P4_10", "horizonte"), ("P3_13", "seguridad social"),
                    ("P5_20", "razón principal"), ("P5_23", "conocimiento"),
                    ("P5_4_1..9", "guardia de cuenta"))])
    spec["etiquetas"]["tipo"] = "REGION-ENIF-CONDICIONALES"
    spec["inputs"][1].update(id="REGION-ENIF-CONDICIONALES-CODIGO",
                              ruta=str(CODE.relative_to(ROOT)), sha256=sha(CODE))
    spec["parametros"]["conductas"] = list(CONDUCTAS)
    results = []
    for conducta in CONDUCTAS:
        prefix = f"RESULT-REGION-ENIF-COND-2024-{conducta}"
        results.append(dict(id=prefix+"-JSON", tipo="texto",
                            unidad="JSON con réplicas conjuntas, sin filas individuales"))
        for geo in range(1, 7):
            for suffix, tipo, unidad in (("P", "proporcion", "proporción [0,1]"),
                 ("IC-LO", "proporcion", "límite inferior IC95"),
                 ("IC-HI", "proporcion", "límite superior IC95"),
                 ("N", "entero", "personas no ponderadas del denominador"),
                 ("ESTADO", "texto", "estado de publicación"),
                 ("N-EFECTIVO-KISH", "flotante", "diagnóstico Kish")):
                row = dict(id=f"{prefix}-{geo}-{suffix}", tipo=tipo, unidad=unidad)
                if suffix in ("P", "IC-LO", "IC-HI", "N-EFECTIVO-KISH"):
                    row["permite_no_estimable"] = True
                results.append(row)
    spec["resultados"] = results
    (P / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding="utf-8")
    MD.with_suffix(".sha256").write_text(f"{sha(MD)}  {MD.name}\n", encoding="utf-8")
    print(CALC, len(results))


if __name__ == "__main__":
    main()
