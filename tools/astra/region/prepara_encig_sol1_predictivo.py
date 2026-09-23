"""Congela derivación predictiva SOL1 antes de leer RESULT de evaluación."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
CALC = "CALC-REGION-ENCIG-SOL1-IC-PRED-0001"
P = ROOT / "data/corrida0" / CALC
MD = ROOT / "forense/prereg-caja/REGION-ENCIG-SOL1-IC-PRED-spec-v1_0.md"
CODE = ROOT / "tools/astra/region/encig_sol1_predictivo.py"
SHARED = ROOT / "tools/astra/region/ic_calibrado.py"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    P.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CODE, P / "medidor.py")
    inputs = []
    for year, calc in ((2021, "CALC-REGION-ENCIG-SOL1-2021-0001"),
                       (2023, "CALC-REGION-ENCIG-SOL1-2023-0001"),
                       (2025, "CALC-REGION-ENCIG-CONSUMIDORES-2025-0001")):
        path = ROOT / "data/corrida0" / calc / "resultados.json"
        inputs.append(dict(id=f"FUENTE-{year}", origen="repo",
                           ruta=str(path.relative_to(ROOT)), sha256=sha(path),
                           rol="RESULT regional sellado de ajuste/piso/evaluación"))
    for label,path in (("REGION-SOL1-ICP-CODIGO", CODE), ("REGION-ICP-COMPARTIDO", SHARED)):
        inputs.append(dict(id=label, origen="repo", funcion="CODIGO",
                           ruta=str(path.relative_to(ROOT)), sha256=sha(path)))
    prefix = "RESULT-REGION-ENCIG-SOL1-ICP"
    results = [dict(id=prefix+"-JSON", tipo="texto", unidad="intervalos predictivos regionales")]
    for i in range(1, 33):
        geo = f"{i:02}"
        for suf,tipo,unidad in (("-IC-LO", "proporcion", "límite predictivo inferior"),
                                ("-IC-HI", "proporcion", "límite predictivo superior"),
                                ("-CUBIERTA", "entero", "1 si cubre punto posterior")):
            results.append(dict(id=f"{prefix}-{geo}{suf}", tipo=tipo, unidad=unidad,
                                permite_no_estimable=True))
    for suf,tipo,unidad in (("-TAU2", "flotante", "varianza entre olas en logit"),
                            ("-N-COMPARABLE", "entero", "entidades comparables"),
                            ("-N-CUBIERTA", "entero", "entidades cubiertas")):
        row = dict(id=prefix+suf, tipo=tipo, unidad=unidad)
        if suf == "-TAU2": row["permite_no_estimable"] = True
        results.append(row)
    spec = dict(calc_id=CALC, spec_md="../../../forense/prereg-caja/"+MD.name,
        spec_md_sha256=sha(MD), script=f"data/corrida0/{CALC}/medidor.py",
        etiquetas=dict(generacion="GEN2", tipo="REGION-ENCIG-SOL1-IC-PRED",
                       rotulo="RETROSPECTIVA", cuenta_gen2="NO", adopta="NO",
                       acto="ASTRA4-U5-EJE-REGIONAL", origen_numerico="HEREDADO"),
        inputs=inputs, variables=[dict(archivo="resultados.json", variable="punto, ic_inf, ic_sup, estado",
                                      rol="fuentes regionales selladas")],
        universo="entidades publicables R1/R2 con P8_3_1 comparable",
        filtros="ajuste 2021→2023 antes de leer evaluación 2025",
        ponderador="heredado FAC_P18; ninguna reponderación",
        transformacion="IC predictivo logit heredado y cobertura retrospectiva",
        estimando="IC predictivo regional SOL1 del piso 2023 para evaluación 2025",
        parametros=dict(calendario=[2021,2023,2025]), seed=dict(aplica=False),
        dependencias_materiales=[],
        tolerancia=dict(tipo="flotante", abs=1e-12, razon="derivación determinista"),
        resultados=results)
    (P / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding="utf-8")
    MD.with_suffix(".sha256").write_text(f"{sha(MD)}  {MD.name}\n", encoding="utf-8")
    print(CALC, len(results))


if __name__ == "__main__":
    main()
