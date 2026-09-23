"""Genera los tres contratos ejecutables del primer lote regional U5."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "tools/astra/region/medidor.py"
ESTADISTICA = ROOT / "tools/astra/region/estadistica.py"
COMPARTIDAS = ROOT / "tools/celda_d/marginales_reproduccion.py"
CONFIG = {
    "ENVIPE": ("2024", "envipe2024_csv", "delito", [f"{i:02d}" for i in range(1, 33)],
               "FAC_DEL", "entidad de residencia", "evade_norma_envipe2025"),
    "ENCIG": ("2023", "encig23_base_datos_csv", "trámite", [f"{i:02d}" for i in range(1, 33)],
              "FAC_TRA", "entidad de residencia en marco urbano 100 mil+", "canal_digital_luz"),
    "ENIF": ("2024", "enif_2024_enif_2024_bd_csv", "persona", [str(i) for i in range(1, 7)],
             "FAC_PER", "región oficial de diseño", "tiene_ahorros_enif2024"),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def genera():
    for instrumento, (ola, payload, unidad, geografias, factor, ambito, conducta) in CONFIG.items():
        calc = f"CALC-REGION-{instrumento}-{ola}-0001"
        carpeta = ROOT / "data/corrida0" / calc
        carpeta.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(CORE, carpeta / "medidor.py")
        md = ROOT / "forense/prereg-caja" / f"REGION-{instrumento}-spec-v1_0.md"
        pref = f"RESULT-REGION-{instrumento}-{ola}"
        resultados = [{"id": pref + "-JSON", "tipo": "texto",
                       "unidad": "JSON regional sin identificadores individuales"}]
        for geo in geografias:
            base = pref + "-" + geo
            for suf, tipo, uni in (("P", "proporcion", "proporción [0,1]"),
                                   ("IC-LO", "proporcion", "límite inferior IC95"),
                                   ("IC-HI", "proporcion", "límite superior IC95"),
                                   ("N", "entero", f"{unidad}s del denominador, no ponderado"),
                                   ("ESTADO", "texto", "estado de publicación"),
                                   ("N-EFECTIVO-KISH", "flotante", "diagnóstico Kish")):
                fila = {"id": base + "-" + suf, "tipo": tipo, "unidad": uni}
                if suf in ("P", "IC-LO", "IC-HI", "N-EFECTIVO-KISH"):
                    fila["permite_no_estimable"] = True
                resultados.append(fila)
        spec = {
            "calc_id": calc,
            "spec_md": f"../../../forense/prereg-caja/{md.name}",
            "spec_md_sha256": sha(md),
            "script": f"data/corrida0/{calc}/medidor.py",
            "etiquetas": {"generacion": "GEN2", "tipo": "REGION-RETROSPECTIVA",
                          "rotulo": "RETROSPECTIVA", "cuenta_gen2": "SI",
                          "adopta": "NO", "acto": "ASTRA4-U5-EJE-REGIONAL",
                          "origen_numerico": "NUEVO"},
            "inputs": [
                {"id": payload, "origen": "manifiesto"},
                {"id": "REGION-ESTADISTICA", "origen": "repo", "funcion": "CODIGO",
                 "ruta": "tools/astra/region/estadistica.py", "sha256": sha(ESTADISTICA)},
                {"id": "REPLICAS-COMPARTIDAS", "origen": "repo", "funcion": "CODIGO",
                 "ruta": "tools/celda_d/marginales_reproduccion.py", "sha256": sha(COMPARTIDAS)},
            ],
            "variables": [{"archivo": "microdato de la spec humana", "variable": v,
                           "rol": r} for v, r in ((factor, "factor de expansión"),
                                                  ("EST_DIS", "estrato de diseño"),
                                                  ("UPM_DIS", "UPM de diseño"))],
            "universo": f"{unidad}; {conducta}; {ambito}; ola {ola}",
            "filtros": "Códigos y denominador de la spec humana; no filtrar marco antes de réplicas",
            "ponderador": factor,
            "transformacion": "razón de masas ponderadas por geografía; IC percentil de UPM estratificadas compartidas; supresión R2",
            "estimando": f"proporción regional de {conducta}, {unidad}, ola {ola}",
            "parametros": {"instrumento": instrumento, "input_id": payload,
                           "bootstrap_replicas": 1000, "n_min": 200,
                           "geografias": geografias, "nivel_geografico": "REGION" if instrumento == "ENIF" else "ENTIDAD"},
            "seed": {"aplica": True, "valor": 20260923, "rng": "numpy.PCG64"},
            "dependencias_materiales": ["numpy", "pandas"],
            "tolerancia": {"tipo": "flotante", "abs": 1e-10,
                           "razon": "mismo payload, mismo orden de filas y semilla"},
            "resultados": resultados,
        }
        (carpeta / "spec.yaml").write_text(yaml.safe_dump(spec, allow_unicode=True,
                                                          sort_keys=False), encoding="utf-8")


if __name__ == "__main__":
    genera()
