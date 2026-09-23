"""Contrata cuatro consumidores ENCIG 2025 antes de abrir su payload U5."""
from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from tools.astra.region.encig2025_consumidores import CONDUCTAS  # noqa: E402

CALC = "CALC-REGION-ENCIG-CONSUMIDORES-2025-0001"
P = ROOT / "data/corrida0" / CALC
MD = ROOT / "forense/prereg-caja/REGION-ENCIG2025-CONSUMIDORES-spec-v1_0.md"
SCRIPT = ROOT / "tools/astra/region/encig2025_consumidores.py"
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
        pref = f"RESULT-REGION-ENCIG-2025-{conducta}"
        results.append({"id": pref + "-JSON", "tipo": "texto",
                        "unidad": "JSON con réplicas conjuntas, unidad y guardias"})
        for geo in range(1, 33):
            base = f"{pref}-{geo:02d}"
            for suffix, tipo, unidad in (
                ("P", "proporcion", "proporción [0,1]"),
                ("IC-LO", "proporcion", "límite inferior IC95"),
                ("IC-HI", "proporcion", "límite superior IC95"),
                ("N", "entero", "unidad no ponderada del denominador"),
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
        "etiquetas": {"generacion": "GEN2", "tipo": "REGION-ENCIG2025-CONSUMIDORES",
                      "rotulo": "RETROSPECTIVA", "cuenta_gen2": "SI", "adopta": "NO",
                      "acto": "ASTRA4-U5-EJE-REGIONAL", "origen_numerico": "NUEVO"},
        "inputs": [
            {"id": "encig25_base_datos_csv", "origen": "manifiesto"},
            {"id": "REGION-ENCIG2025-CODIGO", "origen": "repo", "funcion": "CODIGO",
             "ruta": "tools/astra/region/encig2025_consumidores.py", "sha256": sha(SCRIPT)},
            {"id": "REGION-BASE-CODIGO", "origen": "repo", "funcion": "CODIGO",
             "ruta": "tools/astra/region/medidor.py", "sha256": sha(BASE)},
            {"id": "REGION-ESTADISTICA", "origen": "repo", "funcion": "CODIGO",
             "ruta": "tools/astra/region/estadistica.py", "sha256": sha(STATS)},
            {"id": "REPLICAS-COMPARTIDAS", "origen": "repo", "funcion": "CODIGO",
             "ruta": "tools/celda_d/marginales_reproduccion.py", "sha256": sha(SHARED)},
        ],
        "variables": [{"archivo": "SEC1/SEC7/SEC8 según spec humana", "variable": v, "rol": rol}
                      for v, rol in (("CVE_ENT", "geografía de residencia"),
                                     ("P8_3_1/P8_4/P7_3/N_TRA", "desenlace y filtro"),
                                     ("FAC_P18/FAC_TRA", "factor por unidad"),
                                     ("EST_DIS", "estrato"), ("UPM_DIS", "UPM"),
                                     ("ID_TRA", "join SEC7-SEC8"))],
        "universo": "ENCIG 2025, marco urbano 100 mil+, dominios por persona/trámite/registro según spec",
        "filtros": "códigos y pesos válidos exactos de spec humana; diseño elegible completo antes del dominio",
        "ponderador": "FAC_P18 en persona; FAC_TRA en SEC7",
        "transformacion": "razón ponderada por CVE_ENT, IC bootstrap compartido y R2",
        "estimando": "proporción regional de cuatro consumidores ENCIG 2025",
        "parametros": {"input_id": "encig25_base_datos_csv", "bootstrap_replicas": 1000,
                       "n_min": 200, "nivel_geografico": "ENTIDAD",
                       "geografias": [f"{i:02d}" for i in range(1, 33)],
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
