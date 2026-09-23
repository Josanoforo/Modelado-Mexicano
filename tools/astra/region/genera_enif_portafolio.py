"""Genera el contrato ejecutable ENIF portafolio antes de la corrida."""
from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from tools.astra.region.enif_portafolio import CONDUCTAS

CALC = "CALC-REGION-ENIF-PORTAFOLIO-2024-0001"
P = ROOT / "data/corrida0" / CALC
MD = ROOT / "forense/prereg-caja/REGION-ENIF-PORTAFOLIO-spec-v1_0.md"
SCRIPT = ROOT / "tools/astra/region/enif_portafolio.py"
BASE = ROOT / "tools/astra/region/medidor.py"
STATS = ROOT / "tools/astra/region/estadistica.py"
SHARED = ROOT / "tools/celda_d/marginales_reproduccion.py"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def genera():
    P.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SCRIPT, P / "medidor.py")
    results = []
    for conducta in CONDUCTAS:
        pref = f"RESULT-REGION-ENIF-PORT-2024-{conducta}"
        results.append({"id": pref + "-JSON", "tipo": "texto",
                        "unidad": "JSON con réplicas conjuntas, sin filas individuales"})
        for geo in range(1, 7):
            base = f"{pref}-{geo}"
            for suffix, tipo, unidad in (
                ("P", "proporcion", "proporción [0,1]"),
                ("IC-LO", "proporcion", "límite inferior IC95"),
                ("IC-HI", "proporcion", "límite superior IC95"),
                ("N", "entero", "personas no ponderadas del denominador"),
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
        "etiquetas": {"generacion": "GEN2", "tipo": "REGION-ENIF-PORTAFOLIO",
                      "rotulo": "RETROSPECTIVA", "cuenta_gen2": "SI", "adopta": "NO",
                      "acto": "ASTRA4-U5-EJE-REGIONAL", "origen_numerico": "NUEVO"},
        "inputs": [
            {"id": "enif_2024_enif_2024_bd_csv", "origen": "manifiesto"},
            {"id": "REGION-ENIF-PORTAFOLIO-CODIGO", "origen": "repo", "funcion": "CODIGO",
             "ruta": "tools/astra/region/enif_portafolio.py", "sha256": sha(SCRIPT)},
            {"id": "REGION-BASE-CODIGO", "origen": "repo", "funcion": "CODIGO",
             "ruta": "tools/astra/region/medidor.py", "sha256": sha(BASE)},
            {"id": "REGION-ESTADISTICA", "origen": "repo", "funcion": "CODIGO",
             "ruta": "tools/astra/region/estadistica.py", "sha256": sha(STATS)},
            {"id": "REPLICAS-COMPARTIDAS", "origen": "repo", "funcion": "CODIGO",
             "ruta": "tools/celda_d/marginales_reproduccion.py", "sha256": sha(SHARED)},
        ],
        "variables": [{"archivo": "TMODULO.csv", "variable": x, "rol": role}
                      for x, role in (("REGION", "geografía"), ("FAC_PER", "factor"),
                                      ("EST_DIS", "estrato"), ("UPM_DIS", "UPM"),
                                      ("P5_1_1..6", "ahorro informal"),
                                      ("P5_6_1..9", "ahorro formal"))],
        "universo": "personas elegidas ENIF 2024 18+ con respuesta sustantiva en las baterías P5_1/P5_6",
        "filtros": "denominador y desenlaces exactos de spec humana; diseño completo antes del dominio",
        "ponderador": "FAC_PER",
        "transformacion": "razón ponderada por región oficial, IC bootstrap percentil compartido y R2",
        "estimando": "proporción regional de cada categoría del portafolio de ahorro",
        "parametros": {"input_id": "enif_2024_enif_2024_bd_csv", "bootstrap_replicas": 1000,
                       "n_min": 200, "nivel_geografico": "REGION",
                       "geografias": [str(i) for i in range(1, 7)],
                       "conductas": list(CONDUCTAS)},
        "seed": {"aplica": True, "valor": 20260923, "rng": "numpy.PCG64"},
        "dependencias_materiales": ["numpy", "pandas"],
        "tolerancia": {"tipo": "flotante", "abs": 1e-10,
                       "razon": "mismo payload, orden, código y semilla"},
        "resultados": results,
    }
    (P / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False),
                                  encoding="utf-8")


if __name__ == "__main__":
    genera()
