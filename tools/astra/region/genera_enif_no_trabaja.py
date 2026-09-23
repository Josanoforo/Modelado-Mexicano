"""Congela contrato regional de horizonte ENIF sin trabajo."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
CALC = "CALC-REGION-ENIF-NO-TRABAJA-2024-0001"
P = ROOT / "data/corrida0" / CALC
MD = ROOT / "forense/prereg-caja/REGION-ENIF-NO-TRABAJA-spec-v1_0.md"
CODE = ROOT / "tools/astra/region/enif_no_trabaja.py"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    P.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CODE, P / "medidor.py")
    template = ROOT / "data/corrida0/CALC-REGION-ENIF-PORTAFOLIO-2024-0001/spec.yaml"
    spec = yaml.safe_load(template.read_text(encoding="utf-8"))
    spec.update(calc_id=CALC, spec_md="../../../forense/prereg-caja/" + MD.name,
                spec_md_sha256=sha(MD), script=f"data/corrida0/{CALC}/medidor.py",
                universo="personas elegidas ENIF 2024 18+ sin trabajo y P4_10 válido",
                filtros="P3_8/P3_9 no trabajan con partición exacta del CALC nacional; P4_10 en {1..5}",
                transformacion="razón ponderada regional, IC bootstrap compartido y R2",
                estimando="proporción regional de horizonte corto entre personas que no trabajan",
                variables=[dict(archivo="TMODULO.csv", variable=x, rol=rol) for x, rol in
                    (("REGION", "geografía"), ("P3_8/P3_9", "trabajo"),
                     ("P4_10", "horizonte"), ("FAC_PER", "factor"),
                     ("EST_DIS", "estrato"), ("UPM_DIS", "UPM"))])
    spec["etiquetas"]["tipo"] = "REGION-ENIF-NO-TRABAJA"
    spec["inputs"][1].update(id="REGION-ENIF-NO-TRABAJA-CODIGO",
                              ruta=str(CODE.relative_to(ROOT)), sha256=sha(CODE))
    spec["parametros"].pop("conductas")
    spec["parametros"]["conducta"] = "horizonte_corto_no_trabaja"
    prefix = "RESULT-REGION-ENIF-2024-horizonte_corto_no_trabaja"
    results = [dict(id=prefix+"-JSON", tipo="texto", unidad="JSON con réplicas conjuntas")]
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
