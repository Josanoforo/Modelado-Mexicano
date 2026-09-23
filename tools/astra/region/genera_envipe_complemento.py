"""Contrata el complemento regional ENVIPE desde RESULT ya sellados."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
CALC = "CALC-REGION-ENVIPE-COMPLEMENTO-0001"
P = ROOT / "data/corrida0" / CALC
MD = ROOT / "forense/prereg-caja/REGION-ENVIPE-COMPLEMENTO-spec-v1_0.md"
CODE = ROOT / "tools/astra/region/envipe_complemento.py"
SOURCE = {2023: "CALC-REGION-HIST-ENVIPE-2023-0001",
          2024: "CALC-REGION-ENVIPE-2024-0001",
          2025: "CALC-REGION-HIST-ENVIPE-2025-0001"}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def genera():
    P.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CODE, P / "medidor.py")
    inputs = []
    for ola, calc in SOURCE.items():
        ruta = Path("data/corrida0") / calc / "resultados.json"
        inputs.append({"id": f"FUENTE-{ola}", "origen": "repo", "ruta": str(ruta),
                       "sha256": sha(ROOT / ruta), "rol": "RESULT sellado del piso de evasión"})
    inputs.append({"id": "REGION-COMPLEMENTO-CODIGO", "origen": "repo", "funcion": "CODIGO",
                   "ruta": "tools/astra/region/envipe_complemento.py", "sha256": sha(CODE)})
    results = []
    for ola in SOURCE:
        pref = f"RESULT-REGION-ENVIPE-CUMPLE-{ola}"
        results.append({"id": pref + "-JSON", "tipo": "texto",
                        "unidad": "JSON con réplicas regionales complementarias"})
        for geo in range(1, 33):
            base = f"{pref}-{geo:02d}"
            for suffix, tipo, unidad in (
                ("P", "proporcion", "proporción [0,1]"),
                ("IC-LO", "proporcion", "límite inferior IC95"),
                ("IC-HI", "proporcion", "límite superior IC95"),
                ("N", "entero", "delitos no ponderados del denominador"),
                ("ESTADO", "texto", "estado de publicación"),
                ("N-EFECTIVO-KISH", "flotante", "diagnóstico Kish"),
            ):
                r = {"id": base + "-" + suffix, "tipo": tipo, "unidad": unidad}
                if suffix in ("P", "IC-LO", "IC-HI", "N-EFECTIVO-KISH"):
                    r["permite_no_estimable"] = True
                results.append(r)
    spec = {
        "calc_id": CALC,
        "spec_md": f"../../../forense/prereg-caja/{MD.name}",
        "spec_md_sha256": sha(MD),
        "script": f"data/corrida0/{CALC}/medidor.py",
        "etiquetas": {"generacion": "GEN2", "tipo": "REGION-COMPLEMENTO-HEREDADO",
                      "rotulo": "RETROSPECTIVA", "cuenta_gen2": "NO", "adopta": "NO",
                      "acto": "ASTRA4-U5-EJE-REGIONAL", "origen_numerico": "HEREDADO"},
        "inputs": inputs,
        "variables": [{"archivo": "resultados.json", "variable": "P, IC-LO, IC-HI, replicas_p",
                       "rol": "fuente sellada por ola y entidad"}],
        "universo": "delitos ENVIPE 2023/24/25 con BP1_20 en {1,2}; mismo denominador del piso de evasión",
        "filtros": "heredados de los RESULT de fuente; ninguna nueva exclusión",
        "ponderador": "FAC_DEL heredado",
        "transformacion": "p'=1-p; IC'=[1-hi,1-lo]; réplicas'=1-r; estado R2 heredado",
        "estimando": "complemento regional retrospectivo de evade_norma_envipe2025",
        "parametros": {"olas": list(SOURCE), "nivel_geografico": "ENTIDAD",
                       "geografias": [f"{i:02d}" for i in range(1, 33)]},
        "seed": {"aplica": False},
        "dependencias_materiales": [],
        "tolerancia": {"tipo": "flotante", "abs": 1e-12,
                       "razon": "transformación determinista de RESULT sellados"},
        "resultados": results,
    }
    (P / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False),
                                  encoding="utf-8")


if __name__ == "__main__":
    genera()
