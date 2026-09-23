"""Congela U4 regional ENVIPE 2025 antes del microdato."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import yaml

from tools.astra.region.envipe_denuncia_persona import CONDUCTAS

ROOT = Path(__file__).resolve().parents[3]
CALC = "CALC-REGION-ENVIPE-DENUNCIA-U4-2025-0001"
P = ROOT / "data/corrida0" / CALC
MD = ROOT / "forense/prereg-caja/REGION-ENVIPE2025-DENUNCIA-U4-spec-v1_0.md"
CODE = ROOT / "tools/astra/region/envipe_denuncia_persona.py"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    P.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CODE, P / "medidor.py")
    template = ROOT / "data/corrida0/CALC-REGION-ENVIPE-2024-0001/spec.yaml"
    spec = yaml.safe_load(template.read_text(encoding="utf-8"))
    spec.update(calc_id=CALC, spec_md="../../../forense/prereg-caja/" + MD.name,
        spec_md_sha256=sha(MD), script=f"data/corrida0/{CALC}/medidor.py",
        universo="personas víctimas ENVIPE 2025 con al menos un delito personal U1 no denunciado y motivo 01..08",
        filtros="BPCOD 05..15; BP1_20=2; BP1_23 01..08; máximo C2 por ID_PER",
        ponderador="FAC_ELE de TPER_VIC2, unidad persona U4",
        transformacion="dos tasas complementarias U4 por entidad de residencia, IC bootstrap compartido y R2",
        estimando="proporción regional de miedo/desconfianza C2 y su complemento recortado",
        variables=[dict(archivo=archivo, variable=x, rol=rol) for archivo,x,rol in
            (("TMOD_VIC", "ID_PER/BPCOD/BP1_20/BP1_23", "universo y razón"),
             ("TPER_VIC2", "ID_PER/CVE_ENT", "llave y residencia"),
             ("TPER_VIC2", "FAC_ELE", "factor persona"),
             ("TPER_VIC2", "EST_DIS/UPM_DIS", "diseño"))])
    spec["etiquetas"]["tipo"] = "REGION-ENVIPE-DENUNCIA-U4"
    spec["inputs"][0] = dict(id="envipe2025_csv", origen="manifiesto")
    spec["inputs"][1].update(id="REGION-ENVIPE-U4-CODIGO",
                              ruta=str(CODE.relative_to(ROOT)), sha256=sha(CODE))
    par = spec["parametros"]
    par.update(input_id="envipe2025_csv", instrumento="ENVIPE", conductas=list(CONDUCTAS),
               nivel_geografico="ENTIDAD", geografias=[f"{i:02}" for i in range(1, 33)])
    results = []
    for conducta in CONDUCTAS:
        pref = f"RESULT-REGION-ENVIPE-2025-{conducta}"
        results.append(dict(id=pref+"-JSON", tipo="texto", unidad="JSON con réplicas conjuntas"))
        for i in range(1, 33):
            geo = f"{i:02}"
            for suf, tipo, unidad in (("P", "proporcion", "proporción [0,1]"),
                 ("IC-LO", "proporcion", "límite inferior IC95"),
                 ("IC-HI", "proporcion", "límite superior IC95"),
                 ("N", "entero", "personas no ponderadas del denominador"),
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
