#!/usr/bin/env python3
"""Genera los spec.yaml de los tres CALC del ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1.

Escribe una sola vez, en el COMMIT-1: `resultados:` = `esquema_resultados()` del medidor;
sha256 de spec humana, receta y lectores leídos del disco; sha256 de payloads leídos de
`data/manifiesto.yaml` por id. No abre ningún payload.

Uso: python3 tools/dominios/familia/genera_spec.py
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
RECETA = "tools/dominios/salud/pisos_diseno.py"
LECTORES = "tools/dominios/familia/lectores.py"
SEED = 20260925
ACTO = "GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1"


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def carga(calc):
    s = importlib.util.spec_from_file_location(calc, ROOT / "data/corrida0" / calc / "medidor.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


MAN = {e["id"]: e for e in yaml.safe_load((ROOT / "data/manifiesto.yaml").read_text(encoding="utf-8"))}


def entrada_payload(pid, nota):
    return {"id": pid, "origen": "manifiesto", "sha256": MAN[pid]["sha256"], "funcion": "DATO", "nota": nota}


def entradas_repo():
    return [
        {"id": "receta_pisos_salud", "origen": "repo", "ruta": RECETA, "sha256": sha(RECETA), "funcion": "CODIGO",
         "nota": "marginales, bootstrap, resumen, persistencia, ic_calibrado ejecutados desde estos bytes"},
        {"id": "lectores_familia", "origen": "repo", "ruta": LECTORES, "sha256": sha(LECTORES), "funcion": "CODIGO",
         "nota": "lee_dbf_zip / lee_csv_zip / lee_sav_zip ejecutados desde estos bytes"},
    ]


def variables(pares):
    return [{"archivo": a, "variable": v.upper(), "rol": "reactivo o diseno"} for a, vs in pares for v in vs]


COMUN = {
    "dependencias_materiales": ["numpy", "pandas", "pyreadstat", "dbfread"],
    "seed": {"aplica": True, "valor": SEED, "rng": "numpy.PCG64"},
    "tolerancia": {"tipo": "flotante", "abs": 1.0e-10, "razon": "bootstrap determinista por semilla; mismo payload y sumas float64"},
}
METODO = ("bootstrap UPM con reposicion dentro de estrato; singleton de certeza; percentiles 2.5/97.5; "
          "bloques de 50; contrato conservador")


def etiquetas(extra):
    e = {"generacion": "GEN2", "uso_motor": "NO-ADOPTA-NADA", "cuenta_gen2": "SI",
         "cuenta_gen2_nota": f"CONTADOR del encargo {ACTO} (cuenta_gen2: SI, adopta: NO)",
         "fuente_acto": ACTO, "tipo": "PISO-POR-SEGMENTO-DESDE-MICRODATO", "agrupacion": "UNA-SOLA-VARIABLE",
         "marca": "DESCRIPTIVO -- pisos por segmento; nada se evalua contra R en este CALC",
         "firmas": "F-ASTRA-5-4, regla 6, E.6, §3 v2.16 (encargo §2, verbatim)"}
    e.update(extra)
    return e


def spec_enadid():
    calc = "CALC-ENADID-FAMILIA-HOGARES-0001"
    M = carga(calc)
    md = "forense/prereg-caja/FAMILIA-ENADID-PISOS-spec-v1_0.md"
    pares = []
    for ola in M.OLAS:
        pares += [(M.HOG[ola]["miembro"], M.columnas_hog(ola)), (M.PER[ola]["miembro"], M.columnas_per(ola))]
    d = {
        "calc_id": calc, "spec_md": f"../../../{md}", "spec_md_sha256": sha(md),
        "script": f"data/corrida0/{calc}/medidor.py", "dependencias_materiales": COMUN["dependencias_materiales"],
        "etiquetas": etiquetas({"unidad_transferencia": "HOGAR y PERSONA (nunca promediadas entre si)",
                                "ola_reservada": "ENADID 2023 (E.6): no es input"}),
        "inputs": [entrada_payload(M.PAYLOADS[o], f"ENADID {o} base de datos") for o in M.OLAS] + entradas_repo(),
        "variables": variables(pares),
        "universo": ("Hogares (tabla de hogares) y personas residentes (tabla sociodemografica) de ENADID 2009/2014/2018; "
                     "FAC_VIV>0; estrato y UPM de diseno no vacios; personas con diseno de su hogar por llave."),
        "filtros": "Un eje a la vez (TOTAL y ejes de lista-cerrada-P1 §3); nunca cruces.",
        "ponderador": "FAC_VIV",
        "transformacion": "Recodificacion por texto: lista-cerrada-P1 §2 (ENADID) y spec §2-§3.",
        "estimando": ("Pisos por segmento ENADID 2009/2014/2018 de 11 conductas (5 hogar, 6 persona) con IC de diseno "
                      "e IC calibrado de persistencia sobre el piso 2018."),
        "seed": COMUN["seed"],
        "parametros": {"bootstrap_replicas": 2000, "metodo_ic": METODO, "olas": list(M.OLAS), "ola_piso": M.OLA_PISO},
        "tolerancia": COMUN["tolerancia"], "resultados": M.esquema_resultados(),
    }
    return calc, d


def spec_enasic():
    calc = "CALC-ENASIC-CUIDADOS-VEJEZ-0001"
    M = carga(calc)
    md = "forense/prereg-caja/FAMILIA-ENASIC-PISOS-spec-v1_0.md"
    d = {
        "calc_id": calc, "spec_md": f"../../../{md}", "spec_md_sha256": sha(md),
        "script": f"data/corrida0/{calc}/medidor.py", "dependencias_materiales": COMUN["dependencias_materiales"],
        "etiquetas": etiquetas({"unidad_transferencia": "HOGAR y PERSONA 60+ (nunca promediadas entre si)",
                                "ola_unica": "ENASIC 2022 (unica ola en corpus; se abre, E.6)"}),
        "inputs": [entrada_payload(M.PAY, "ENASIC 2022 base de datos (THOGAR, TCSDEMPO)")] + entradas_repo(),
        "variables": variables([("THOGAR.csv", M.COLS_HOG), ("TCSDEMPO.csv", M.COLS_PER)]),
        "universo": ("Hogares (THOGAR) con FAC_HOG>0 y EST_DIS/UPM_DIS no vacios; personas de 60+ (TCSDEMPO) con diseno "
                     "de su hogar por LLAVEHOG."),
        "filtros": "Un eje a la vez (TOTAL y ejes de lista-cerrada-P1 §3); nunca cruces.",
        "ponderador": "FAC_HOG",
        "transformacion": "Recodificacion por texto: lista-cerrada-P1 §2 (ENASIC) y spec §2-§3.",
        "estimando": "Pisos por segmento ENASIC 2022 de 7 conductas (2 hogar, 5 persona 60+) con IC de diseno; sin persistencia.",
        "seed": COMUN["seed"],
        "parametros": {"bootstrap_replicas": 2000, "metodo_ic": METODO, "ola": M.OLA},
        "tolerancia": COMUN["tolerancia"], "resultados": M.esquema_resultados(),
    }
    return calc, d


def spec_pew():
    calc = "CALC-PEW-MIGRACION-MEX-0001"
    M = carga(calc)
    md = "forense/prereg-caja/FAMILIA-PEW-PISOS-spec-v1_0.md"
    pares = [(f"pew_gas_spring{o}.zip:.sav", M.columnas(o) + [M.OLA_CFG[o]["pais"][0]]) for o in M.OLAS]
    d = {
        "calc_id": calc, "spec_md": f"../../../{md}", "spec_md_sha256": sha(md),
        "script": f"data/corrida0/{calc}/medidor.py", "dependencias_materiales": COMUN["dependencias_materiales"],
        "etiquetas": etiquetas({"unidad_transferencia": "PERSONA (adulto entrevistado en Mexico)",
                                "evidencia": "(a) -- residentes de Mexico entrevistados en Mexico",
                                "ola_reservada": "Pew GAS Spring 2025 (E.6): no es input"}),
        "inputs": [entrada_payload(M.PAYLOADS[o], f"Pew GAS Spring {o} (.sav)") for o in M.OLAS] + entradas_repo(),
        "variables": variables(pares),
        "universo": "Adultos 18-97 entrevistados en Mexico (codigo de pais por ola); weight>0.",
        "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD); nunca cruces.",
        "ponderador": "weight",
        "transformacion": "Recodificacion por texto: lista-cerrada-P1 §2 (Pew) y spec §2-§3.",
        "estimando": ("Pisos por segmento de 6 conductas de intencion migratoria, lazos y remesas, Pew GAS Mexico "
                      "2013-2023, con IC bootstrap e IC calibrado de persistencia (>= 3 olas)."),
        "seed": COMUN["seed"],
        "parametros": {"bootstrap_replicas": 2000, "metodo_ic": METODO + "; sin PSU (2013, 2023): entrevista = UPM",
                       "olas": list(M.OLAS)},
        "tolerancia": COMUN["tolerancia"], "resultados": M.esquema_resultados(),
    }
    return calc, d


def main():
    for f in (spec_enadid, spec_enasic, spec_pew):
        calc, d = f()
        cab = (f"# {calc} -- contrato ejecutable de la spec humana (D-15). COMMIT-1, antes de abrir microdato.\n"
               "# El primer resultado que produzca este procedimiento es el que se reporta.\n")
        (ROOT / "data/corrida0" / calc / "spec.yaml").write_text(
            cab + yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
        print(calc, len(d["resultados"]), "resultados")


if __name__ == "__main__":
    main()
