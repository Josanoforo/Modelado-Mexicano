"""Congela contrato regional de denuncia por seguro ENVIPE 2025."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import yaml

from tools.astra.region.envipe_seguro import CONDUCTAS

ROOT = Path(__file__).resolve().parents[3]
CALC = "CALC-REGION-ENVIPE-SEGURO-2025-0001"
P = ROOT / "data/corrida0" / CALC
MD = ROOT / "forense/prereg-caja/REGION-ENVIPE2025-SEGURO-spec-v1_0.md"
CODE = ROOT / "tools/astra/region/envipe_seguro.py"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    P.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CODE, P / "medidor.py")
    template = ROOT / "data/corrida0/CALC-REGION-ENVIPE-2024-0001/spec.yaml"
    spec = yaml.safe_load(template.read_text(encoding="utf-8"))
    spec.update(calc_id=CALC, spec_md="../../../forense/prereg-caja/" + MD.name,
        spec_md_sha256=sha(MD), script=f"data/corrida0/{CALC}/medidor.py",
        universo="delitos ENVIPE 2025 BPCOD=01 con BP2_1 y BP1_20 válidos",
        filtros="BP2_1=1 o 2; BP1_20=1 o 2; cuatro tasas condicionadas",
        ponderador="FAC_DEL; unidad delito",
        transformacion="razón ponderada por entidad de residencia, IC bootstrap compartido y R2",
        estimando="denuncia y no denuncia contadas dentro de con/sin seguro",
        variables=[dict(archivo=archivo, variable=x, rol=rol) for archivo,x,rol in
            (("TMOD_VIC", "ID_PER/BPCOD/BP2_1/BP1_20", "universo, seguro, denuncia"),
             ("TMOD_VIC", "FAC_DEL", "factor delito"),
             ("TMOD_VIC", "EST_DIS/UPM_DIS", "diseño"),
             ("TSDEM", "ID_PER/CVE_ENT", "residencia"))])
    spec["etiquetas"]["tipo"] = "REGION-ENVIPE-SEGURO"
    spec["inputs"][0] = dict(id="envipe2025_csv", origen="manifiesto")
    spec["inputs"][1].update(id="REGION-ENVIPE-SEGURO-CODIGO",
                              ruta=str(CODE.relative_to(ROOT)), sha256=sha(CODE))
    spec["parametros"].update(input_id="envipe2025_csv", instrumento="ENVIPE",
        conductas=list(CONDUCTAS), nivel_geografico="ENTIDAD",
        geografias=[f"{i:02}" for i in range(1, 33)])
    results = []
    for conducta in CONDUCTAS:
        pref = f"RESULT-REGION-ENVIPE-SEG-2025-{conducta}"
        results.append(dict(id=pref+"-JSON", tipo="texto", unidad="JSON con réplicas conjuntas"))
        for i in range(1, 33):
            geo = f"{i:02}"
            for suf, tipo, unidad in (("P", "proporcion", "proporción [0,1]"),
                 ("IC-LO", "proporcion", "límite inferior IC95"),
                 ("IC-HI", "proporcion", "límite superior IC95"),
                 ("N", "entero", "delitos no ponderados del denominador"),
                 ("ESTADO", "texto", "estado de publicación"),
                 ("N-EFECTIVO-KISH", "flotante", "diagnóstico Kish")):
                row = dict(id=f"{pref}-{geo}-{suf}", tipo=tipo, unidad=unidad)
                if suf in ("P", "IC-LO", "IC-HI", "N-EFECTIVO-KISH"):
                    row["permite_no_estimable"] = True
                results.append(row)
    spec["resultados"] = results
    (P / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding="utf-8")
    MD.with_suffix(".sha256").write_text(f"{sha(MD)}  {MD.name}\n", encoding="utf-8")
    print(CALC, len(results))


if __name__ == "__main__":
    main()
