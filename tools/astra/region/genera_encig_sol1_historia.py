"""Congela dos CALC de solicitud ENCIG antes de abrir sus olas."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
MD = ROOT / "forense/prereg-caja/REGION-ENCIG-SOL1-HIST-spec-v1_0.md"
CODE = ROOT / "tools/astra/region/encig_sol1_historia.py"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    template = ROOT / "data/corrida0/CALC-REGION-HIST-ENCIG-2021-0001/spec.yaml"
    for year, input_id in ((2021, "encig2021_csv"), (2023, "encig23_base_datos_csv")):
        calc = f"CALC-REGION-ENCIG-SOL1-{year}-0001"
        path = ROOT / "data/corrida0" / calc
        path.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(CODE, path / "medidor.py")
        spec = yaml.safe_load(template.read_text(encoding="utf-8"))
        spec.update(calc_id=calc, spec_md="../../../forense/prereg-caja/" + MD.name,
            spec_md_sha256=sha(MD), script=f"data/corrida0/{calc}/medidor.py",
            universo=f"personas ENCIG {year} 18+ con P8_3_1 en 1/2; marco urbano 100 mil+",
            filtros="P8_3_1=1 numerador; 1/2 denominador; excluye 9 y blanco",
            ponderador="FAC_P18; unidad persona",
            transformacion="razón ponderada estatal, IC bootstrap compartido y R2",
            estimando="proporción regional del primer inciso de solicitud P8_3_1",
            variables=[dict(archivo="SEC1_A_3_4_5_8_9_10", variable=x, rol=rol)
                       for x,rol in (("P8_3_1", "solicitud primer inciso"),
                           ("FAC_P18", "factor persona"), ("EST_DIS", "estrato"),
                           ("UPM_DIS", "UPM"),
                           ("ENT" if year == 2021 else "CVE_ENT", "residencia"))])
        spec["etiquetas"]["tipo"] = "REGION-ENCIG-SOL1-HIST"
        spec["inputs"][0] = dict(id=input_id, origen="manifiesto")
        spec["inputs"][1].update(id="REGION-ENCIG-SOL1-CODIGO",
                                  ruta=str(CODE.relative_to(ROOT)), sha256=sha(CODE))
        spec["parametros"].update(ola=year, input_id=input_id,
                                  conducta="paga_mordida_encig2025")
        pref = f"RESULT-REGION-ENCIG-SOL1-{year}"
        results = [dict(id=pref+"-JSON", tipo="texto", unidad="JSON con réplicas conjuntas")]
        for i in range(1, 33):
            geo = f"{i:02}"
            for suf,tipo,unidad in (("P", "proporcion", "proporción [0,1]"),
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
        (path / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding="utf-8")
        print(calc, len(results))
    MD.with_suffix(".sha256").write_text(f"{sha(MD)}  {MD.name}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
