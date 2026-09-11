#!/usr/bin/env python3
"""Genera las ocho caras mecánicas del preregistro ENVIPE-SERIE-COMPLETA.

No abre microdatos ni produce resultados. Su única entrada sustantiva es la
tabla CONFIG congelada abajo; escribe spec.md/spec.yaml y deposita una copia
idéntica del medidor en cada CALC antes del COMMIT-1.
"""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FAMILY = ROOT / "forense/prereg-caja/ENVIPE-SERIE-COMPLETA-spec-v1_0.md"
METER = ROOT / "tools/medidor_envipe_serie_completa.py"

CONFIG = {
    2011: dict(payload="envipe_2011_base_de_datos_envipe_2011_dbf", fmt="DBF",
               member="tmod_vic.DBF", response="BP1_21", estrato="EST", upm="UPM",
               personal=list(range(4, 15)), hogar=[1, 2, 3], nsnr=[88, 98, 99], ruptura="SI"),
    2014: dict(payload="envipe_2014_bd_envipe2014_dbf", fmt="DBF",
               member="bd_envipe2014/bd_envipe2014/TMod_Vic.dbf", response="BP1_23",
               estrato="EST", upm="UPM", personal=list(range(5, 16)),
               hogar=[1, 2, 3, 4], nsnr=[99], ruptura="NO"),
    2016: dict(payload="envipe_2016_bd_envipe2016_dbf", fmt="DBF",
               member="TMod_Vic.dbf", response="BP1_23", estrato="EST_DIS", upm="UPM_DIS",
               personal=list(range(5, 16)), hogar=[1, 2, 3, 4], nsnr=[99], ruptura="NO"),
    2017: dict(payload="envipe_2017_bd_envipe2017_dbf", fmt="DBF",
               member="BASE_DE_DATOS_ENVIPE_2017_en/TMod_Vic.dbf", response="BP1_23",
               estrato="EST_DIS", upm="UPM_DIS", personal=list(range(5, 16)),
               hogar=[1, 2, 3, 4], nsnr=[99], ruptura="NO"),
    2018: dict(payload="envipe2018_csv", fmt="CSV",
               member="conjunto_de_datos_tmod_vic_envipe_2018/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe_2018.csv",
               response="BP1_23", estrato="EST_DIS", upm="UPM_DIS",
               personal=list(range(5, 16)), hogar=[1, 2, 3, 4], nsnr=[99], ruptura="NO"),
    2019: dict(payload="envipe2019_csv", fmt="CSV",
               member="conjunto_de_datos_TMod_Vic_ENVIPE_2019/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2019.csv",
               response="BP1_23", estrato="EST_DIS", upm="UPM_DIS",
               personal=list(range(5, 16)), hogar=[1, 2, 3, 4], nsnr=[99], ruptura="NO"),
    2020: dict(payload="envipe2020_csv", fmt="CSV",
               member="conjunto_de_datos_TMod_Vic_ENVIPE_2020/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2020.csv",
               response="BP1_23", estrato="EST_DIS", upm="UPM_DIS",
               personal=list(range(5, 16)), hogar=[1, 2, 3, 4], nsnr=[99], ruptura="NO"),
    2022: dict(payload="envipe2022_csv", fmt="CSV",
               member="conjunto_de_datos_TMod_Vic_ENVIPE_2022/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2022.csv",
               response="BP1_23", estrato="EST_DIS", upm="UPM_DIS",
               personal=list(range(5, 16)), hogar=[1, 2, 3, 4], nsnr=[99], ruptura="NO"),
}

SUFFIXES = [
    "N-FILAS-TABLA", "N-RESPUESTA-01-09", "N-NSNR", "N-BLANCO",
    "N-SIN-PONDERADOR", "N-SIN-DISENO", "N-INCONSISTENTES-BP1-20",
    "N-CODIGO-FUERA-DE-CATALOGO", "N-BPCOD-HOGAR", "N-BPCOD-PERSONALES",
    "MASA-FAC-DEL", "PUNTO", "EE", "IC-LO", "IC-HI", "N", "CV",
    "VEREDICTO-CV", "N-ESTRATOS", "N-UPM", "N-ESTRATOS-UPM-UNICA",
    "METODO-IC", "PERFIL-DISENO", "PERFIL-LECTURA", "PERFIL-BPCOD", "N-U1",
    "MASA-FAC-DEL-U1", "P-C1-U1", "EE-C1-U1", "IC-LO-C1-U1",
    "IC-HI-C1-U1", "IC-BOOT-LO-C1-U1", "IC-BOOT-HI-C1-U1", "P-C2-U1",
    "EE-C2-U1", "IC-BOOT-LO-C2-U1", "IC-BOOT-HI-C2-U1", "DELTA-C2-C1",
    "N-ESTRATOS-UPM-UNICA-U1", "ESTADO",
]

TEXT = {"VEREDICTO-CV", "METODO-IC", "PERFIL-DISENO", "PERFIL-LECTURA",
        "PERFIL-BPCOD", "ESTADO"}
INTEGER = {s for s in SUFFIXES if s.startswith("N-")}
PROPORTION = {"PUNTO", "IC-LO", "IC-HI", "P-C1-U1", "IC-LO-C1-U1",
              "IC-HI-C1-U1", "IC-BOOT-LO-C1-U1", "IC-BOOT-HI-C1-U1",
              "P-C2-U1", "IC-BOOT-LO-C2-U1", "IC-BOOT-HI-C2-U1"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def result_spec(year: int, suffix: str) -> dict:
    if suffix in TEXT:
        tipo = "texto"
    elif suffix in INTEGER:
        tipo = "entero"
    elif suffix in PROPORTION:
        tipo = "proporcion"
    else:
        tipo = "flotante"
    unit = f"ENVIPE {year}, delitos de {year - 1}, unidad DELITO"
    if suffix == "P-C1-U1":
        unit += "; PUNTO DE SERIE: proporción ponderada de U1 con razón 01/02/06; FAC_DEL; escala [0,1]"
    elif suffix.startswith("IC-BOOT-"):
        unit += "; límite IC95 bootstrap de UPM dentro de estrato; con UPM única es límite inferior de anchura"
    elif suffix == "P-C2-U1":
        unit += "; sensibilidad: C1 más código 08; no sustituye al punto de serie"
    elif suffix == "DELTA-C2-C1":
        unit += "; P-C2-U1 menos P-C1-U1, con signo"
    elif suffix == "PUNTO":
        unit += "; diagnóstico R sobre U_R, no es el punto de serie"
    out = {"id": f"RESULT-ENVIPE-SERIE-{year}-{suffix}", "tipo": tipo, "unidad": unit}
    if tipo in {"flotante", "proporcion"}:
        out["permite_no_estimable"] = True
    return out


def main() -> None:
    family_sha = sha(FAMILY)
    for year, cfg in CONFIG.items():
        calc = f"CALC-ENVIPE-SERIE-{year}"
        dest = ROOT / "data/corrida0" / calc
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(METER, dest / "medidor.py")
        md = f"""# {calc} · ENVIPE {year} (delitos de {year - 1})

Cara humana de `spec.yaml`. Gobierna
`prereg-caja-ENVIPE-SERIE-COMPLETA-v1_0` (`sha256 {family_sha}`).

Unidad: delito de `TMod_Vic`; ponderador `FAC_DEL`; diseño
`{cfg['estrato']}`/`{cfg['upm']}`. El punto de serie es `P-C1-U1`.
La ruptura nominal/categorías residuales 2011 se declara: `{cfg['ruptura']}`.
No se interpola, no se atribuye causalidad y no se modifican resultados previos.
El primer resultado que produzca este procedimiento es el que se reporta.
"""
        (dest / "spec.md").write_text(md, encoding="utf-8")
        p = f"RESULT-ENVIPE-SERIE-{year}-"
        contract = {
            "calc_id": calc,
            "spec_md": "spec.md",
            "spec_md_sha256": sha(dest / "spec.md"),
            "script": f"data/corrida0/{calc}/medidor.py",
            "etiquetas": {
                "generacion": "GEN2",
                "tipo": "SERIE-TEMPORAL-DESCRIPTIVA",
                "cuenta_gen2": "SI",
                "cuenta_gen2_firma": "Encargo GEN2-ENVIPE-SERIE-COMPLETA, 10/sep/2026: para CALC científicos nuevos, aplicar cuenta_gen2=SI con objeto y cita explícitos; objeto: punto anual nuevo de la serie p(C1,U1). El merge de mesa perfecciona la firma.",
                "validacion_independiente": "NO-HECHA",
                "spec_sellada": "forense/prereg-caja/ENVIPE-SERIE-COMPLETA-spec-v1_0.md",
                "spec_sellada_sha256": family_sha,
                "decisión": "D12; integra NC-0087/0093/0101",
                "ruptura_comparabilidad": "INSTRUMENTACION-NOMINAL-Y-RESIDUALES" if year == 2011 else "NINGUNA-EN-C1-U1",
            },
            "inputs": [
                {"id": cfg["payload"], "origen": "manifiesto"},
                {"id": "IN-ENVIPE-SERIE-COMPLETA-SPEC", "origen": "repo",
                 "ruta": "forense/prereg-caja/ENVIPE-SERIE-COMPLETA-spec-v1_0.md", "sha256": family_sha},
            ],
            "variables": [
                {"archivo": cfg["member"], "variable": cfg["response"], "rol": "desenlace: razón principal de no denuncia", "codigos": "01..09 sustantivos; NS/NR y blanco excluidos", "direccion": "01/02/06 = 1; 03/04/05/07/08 = 0 en C1"},
                {"archivo": cfg["member"], "variable": "BP1_20", "rol": "filtro no denunció", "codigos": "1 sí, 2 no"},
                {"archivo": cfg["member"], "variable": "BPCOD", "rol": "tipo de delito y filtro personal", "codigos": f"personales {cfg['personal']}"},
                {"archivo": cfg["member"], "variable": "FAC_DEL", "rol": "ponderador de delito"},
                {"archivo": cfg["member"], "variable": cfg["estrato"], "rol": "estrato; llave opaca"},
                {"archivo": cfg["member"], "variable": cfg["upm"], "rol": "UPM; llave opaca"},
            ],
            "universo": f"ENVIPE {year}, delitos de {year - 1}; U1 = delito personal, BP1_20=2, respuesta 01..08 y FAC_DEL válido. Unidad DELITO.",
            "filtros": f"09, {cfg['nsnr']} y blanco fuera de U1 y contados; ponderador no finito o <=0 fuera; sin diseño entra al punto y se declara.",
            "ponderador": "FAC_DEL; no se usa factor de persona ni FAC_DEL_AM",
            "transformacion": "C1=1 para 01/02/06 y 0 para 03/04/05/07/08; C2 añade 08; sum(w*y)/sum(w); IC analítico ultimate-cluster y bootstrap predeclarado",
            "estimando": "DESCRIPTIVO. P-C1-U1 es el punto de serie; PUNTO es diagnóstico R y no se mezcla con la serie.",
            "dependencias_materiales": ["numpy"],
            "parametros": {
                "fuente_acto": f"ACTO GEN2-ENVIPE-SERIE-COMPLETA · {calc}",
                "ola_encuesta": year,
                "anio_hecho": year - 1,
                "payload_id": cfg["payload"],
                "formato": cfg["fmt"],
                "tabla_miembro": cfg["member"],
                "mapa_columnas": {"BP1_23": cfg["response"], "BP1_20": "BP1_20", "BPCOD": "BPCOD", "FAC_DEL": "FAC_DEL", "ESTRATO": cfg["estrato"], "UPM": cfg["upm"]},
                "bootstrap_replicas": 2000,
                "umbral_cv_skip": 0.30,
                "codificacion": {"CR_uno": [1, 2, 6], "CR_cero": [3, 4, 5, 7, 8, 9], "C1_uno": [1, 2, 6], "C1_cero": [3, 4, 5, 7, 8], "C2_uno": [1, 2, 6, 8], "C2_cero": [3, 4, 5, 7], "bpcod_hogar": cfg["hogar"], "bpcod_personales": cfg["personal"], "codigos_nsnr": cfg["nsnr"]},
                "sufijos_result": SUFFIXES,
            },
            "seed": {"aplica": True, "valor": 20260909, "rng": "numpy.PCG64"},
            "tolerancia": {"tipo": "flotante", "abs": 1e-10, "razon": "mismo archivo, orden fijo, semilla y RNG; textos/enteros exactos"},
            "resultados": [result_spec(year, s) for s in SUFFIXES],
        }
        (dest / "spec.yaml").write_text(yaml.safe_dump(contract, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
        print(calc, cfg["fmt"], cfg["payload"])


if __name__ == "__main__":
    main()
