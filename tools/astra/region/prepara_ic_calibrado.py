"""Congela el contrato de IC regional antes de leer sus RESULT numéricos."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import yaml

from tools.astra.region.ic_calibrado import SERIES

ROOT = Path(__file__).resolve().parents[3]
CALC = "CALC-REGION-IC-PREDICTIVO-0001"
DEST = ROOT / "data/corrida0" / CALC
HUMAN = ROOT / "forense/prereg-caja/REGION-IC-PREDICTIVO-spec-v1_0.md"
CODE = ROOT / "tools/astra/region/ic_calibrado.py"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source(instrument, year, kind):
    if kind == "CONSUMIDORES":
        return "CALC-REGION-ENCIG-CONSUMIDORES-2025-0001"
    return f"CALC-REGION-{'HIST-' if kind == 'HIST' else ''}{instrument}-{year}-0001"


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    script = DEST / "medidor.py"
    shutil.copyfile(CODE, script)
    inputs = []
    for inst, (years, kinds) in SERIES.items():
        for year, kind in zip(years, kinds):
            path = ROOT / "data/corrida0" / source(inst, year, kind) / "resultados.json"
            inputs.append(dict(id=f"FUENTE-{inst}-{year}", origen="repo",
                               ruta=str(path.relative_to(ROOT)), sha256=sha(path),
                               rol="RESULT regional sellado de ajuste/piso/evaluación"))
    inputs.append(dict(id="REGION-ICP-CODIGO", origen="repo", funcion="CODIGO",
                       ruta=str(CODE.relative_to(ROOT)), sha256=sha(CODE)))
    results = []
    for inst, (years, _) in SERIES.items():
        geos = [f"{i:02}" for i in range(1, 33)] if inst != "ENIF" else [str(i) for i in range(1, 7)]
        prefix = f"RESULT-REGION-ICP-{inst}"
        results.append(dict(id=prefix+"-JSON", tipo="texto", unidad="intervalos predictivos y cobertura retrospectiva"))
        for g in geos:
            for suffix, tipo, unidad in (("-IC-LO", "proporcion", "límite inferior predictivo"),
                                          ("-IC-HI", "proporcion", "límite superior predictivo"),
                                          ("-CUBIERTA", "entero", "1 si cubre punto posterior, 0 si no")):
                results.append(dict(id=prefix+"-"+g+suffix, tipo=tipo, unidad=unidad,
                                    permite_no_estimable=True))
        for suffix, tipo, unidad in (("-N-COMPARABLE", "entero", "geografías comparables"),
                                     ("-N-CUBIERTA", "entero", "geografías cubiertas"),
                                     ("-TAU2", "flotante", "varianza entre olas en escala logit")):
            row = dict(id=prefix+suffix, tipo=tipo, unidad=unidad)
            if suffix == "-TAU2": row["permite_no_estimable"] = True
            results.append(row)
    contract = dict(calc_id=CALC, spec_md="../../../forense/prereg-caja/REGION-IC-PREDICTIVO-spec-v1_0.md",
        spec_md_sha256=sha(HUMAN), script=str(script.relative_to(ROOT)),
        etiquetas=dict(generacion="GEN2", tipo="REGION-IC-PREDICTIVO-HEREDADO",
                       rotulo="RETROSPECTIVA", cuenta_gen2="NO", adopta="NO",
                       acto="ASTRA4-U5-EJE-REGIONAL", origen_numerico="HEREDADO"),
        inputs=inputs, variables=[dict(archivo="resultados.json", variable="punto, ic_inf, ic_sup, estado",
                                      rol="serie regional sellada")],
        universo="geografías publicables R1/R2 con serie temporal comparable",
        filtros="probabilidad e IC interiores a (0,1); evaluación nunca entra al ajuste",
        ponderador="heredado de cada fuente; ninguna reponderación",
        transformacion="tau2 logit de transiciones previas; IC predictivo heredado y evaluación posterior",
        estimando="intervalo predictivo y cobertura regional retrospectiva",
        parametros=dict(series={k: list(v[0]) for k, v in SERIES.items()}),
        seed=dict(aplica=False), dependencias_materiales=[],
        tolerancia=dict(tipo="flotante", abs=1e-12, razon="derivación determinista de RESULT sellados"),
        resultados=results)
    (DEST / "spec.yaml").write_text(yaml.safe_dump(contract, allow_unicode=True, sort_keys=False), encoding="utf-8")
    sidecar = HUMAN.with_suffix(".sha256")
    sidecar.write_text(f"{sha(HUMAN)}  {HUMAN.name}\n", encoding="utf-8")
    print(CALC, len(inputs), len(results))


if __name__ == "__main__":
    main()
