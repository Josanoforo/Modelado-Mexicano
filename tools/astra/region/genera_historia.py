"""Contratos por ola para historia regional comparable, antes del dato."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
CODIGO = ROOT / "tools/astra/region/historia.py"
BASE = ROOT / "tools/astra/region/medidor.py"
ESTADISTICA = ROOT / "tools/astra/region/estadistica.py"
COMPARTIDAS = ROOT / "tools/celda_d/marginales_reproduccion.py"
CONFIG = {
    "ENVIPE": {2023: "envipe2023_csv", 2025: "envipe2025_csv"},
    "ENCIG": {2017: "encig2017_csv", 2019: "encig2019_csv", 2021: "encig2021_csv"},
    "ENIF": {2018: "enif2018_csv", 2021: "enif2021_csv",
             2024: "enif_2024_enif_2024_bd_csv"},
}
CONDUCTA = {"ENVIPE": "evade_norma_envipe2025", "ENCIG": "canal_digital_luz",
            "ENIF": "informal_cualquiera_18a70"}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def genera():
    for inst, olas in CONFIG.items():
        md = ROOT / "forense/prereg-caja" / f"REGION-HIST-{inst}-spec-v1_0.md"
        for ola, payload in olas.items():
            calc = f"CALC-REGION-HIST-{inst}-{ola}-0001"
            carpeta = ROOT / "data/corrida0" / calc
            carpeta.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(CODIGO, carpeta / "medidor.py")
            geos = [str(i) for i in range(1, 7)] if inst == "ENIF" else [f"{i:02d}" for i in range(1, 33)]
            pref = f"RESULT-REGION-HIST-{inst}-{ola}"
            unidad = "persona" if inst == "ENIF" else "delito" if inst == "ENVIPE" else "trámite"
            resultados = [{"id": pref + "-JSON", "tipo": "texto",
                           "unidad": "JSON con réplicas conjuntas, sin filas individuales"}]
            for geo in geos:
                b = pref + "-" + geo
                for suf, tipo, unit in (("P", "proporcion", "proporción [0,1]"),
                                        ("IC-LO", "proporcion", "límite inferior IC95"),
                                        ("IC-HI", "proporcion", "límite superior IC95"),
                                        ("N", "entero", f"{unidad}s no ponderados del denominador"),
                                        ("ESTADO", "texto", "estado de publicación"),
                                        ("N-EFECTIVO-KISH", "flotante", "diagnóstico Kish")):
                    r = {"id": b + "-" + suf, "tipo": tipo, "unidad": unit}
                    if suf in ("P", "IC-LO", "IC-HI", "N-EFECTIVO-KISH"):
                        r["permite_no_estimable"] = True
                    resultados.append(r)
            factor = "FAC_DEL" if inst == "ENVIPE" else "FAC_TRA" if inst == "ENCIG" else "FAC_ELE" if ola == 2021 else "FAC_PER"
            spec = {
                "calc_id": calc,
                "spec_md": f"../../../forense/prereg-caja/{md.name}",
                "spec_md_sha256": sha(md),
                "script": f"data/corrida0/{calc}/medidor.py",
                "etiquetas": {"generacion": "GEN2", "tipo": "REGION-HIST-RETROSPECTIVA",
                              "rotulo": "RETROSPECTIVA", "cuenta_gen2": "SI",
                              "adopta": "NO", "acto": "ASTRA4-U5-EJE-REGIONAL",
                              "origen_numerico": "NUEVO"},
                "inputs": [
                    {"id": payload, "origen": "manifiesto"},
                    {"id": "REGION-HISTORIA-CODIGO", "origen": "repo", "funcion": "CODIGO",
                     "ruta": "tools/astra/region/historia.py", "sha256": sha(CODIGO)},
                    {"id": "REGION-BASE-CODIGO", "origen": "repo", "funcion": "CODIGO",
                     "ruta": "tools/astra/region/medidor.py", "sha256": sha(BASE)},
                    {"id": "REGION-ESTADISTICA", "origen": "repo", "funcion": "CODIGO",
                     "ruta": "tools/astra/region/estadistica.py", "sha256": sha(ESTADISTICA)},
                    {"id": "REPLICAS-COMPARTIDAS", "origen": "repo", "funcion": "CODIGO",
                     "ruta": "tools/celda_d/marginales_reproduccion.py", "sha256": sha(COMPARTIDAS)},
                ],
                "variables": [{"archivo": "tabla declarada en spec humana", "variable": v, "rol": rol}
                              for v, rol in ((factor, "factor"), ("EST_DIS", "estrato"),
                                             ("UPM_DIS", "UPM"), ("REGION" if inst == "ENIF" else "ENT/CVE_ENT", "geografía"))],
                "universo": f"{CONDUCTA[inst]}; ola {ola}; {unidad}; marco de spec humana",
                "filtros": "códigos de spec humana; el marco se replica completo antes del dominio",
                "ponderador": factor,
                "transformacion": "razón de masas ponderadas por geografía, IC percentil compartido y supresión R2",
                "estimando": f"proporción regional retrospectiva de {CONDUCTA[inst]}",
                "parametros": {"instrumento": inst, "ola": ola, "input_id": payload,
                               "bootstrap_replicas": 1000, "n_min": 200,
                               "nivel_geografico": "REGION" if inst == "ENIF" else "ENTIDAD",
                               "geografias": geos},
                "seed": {"aplica": True, "valor": 20260923, "rng": "numpy.PCG64"},
                "dependencias_materiales": ["numpy", "pandas"],
                "tolerancia": {"tipo": "flotante", "abs": 1e-10,
                               "razon": "mismo payload, orden, código y semilla"},
                "resultados": resultados,
            }
            (carpeta / "spec.yaml").write_text(
                yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding="utf-8")


if __name__ == "__main__":
    genera()
