#!/usr/bin/env python3
"""Genera los spec.yaml de CALC-ENSU-PISOS-0001 y CALC-ENSU-SERIE-0001 (COMMIT-1).

ACTO GEN2-SEGURIDAD-ENSU-SERIE-1. Sin valores de microdato: la disponibilidad
de cada conducta por trimestre sale de las CABECERAS (nombres de columna) de la
tabla CB de cada trimestre (`tools/dominios/ensu/cabeceras.py`), y la lista de
RESULT sale de `esquema_resultados()` del propio medidor. Deposita el medidor
byte a byte como `medidor.py` de cada CALC.

    python3 tools/dominios/ensu/genera_spec_yaml.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import shutil
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "tools/dominios/ensu"))
import cabeceras  # noqa: E402

_s = importlib.util.spec_from_file_location("ensu_medidor", RAIZ / "tools/dominios/ensu/ensu_medidor.py")
M = importlib.util.module_from_spec(_s)
_s.loader.exec_module(M)

SPEC_MD = "forense/prereg-caja/ENSU-SERIE-spec-v1_0.md"
MEDIDOR = RAIZ / "tools/dominios/ensu/ensu_medidor.py"
RECETA = "tools/dominios/salud/pisos_diseno.py"
DICTAMEN = "tools/series/dictamen.py"
PAYLOAD_ID = {a: f"cc1_inegi_ensu_{a}__ensu_bd_{a}_{'dbf' if a <= 2020 else 'csv'}" for a in range(2013, 2024)}
PAYLOAD_ID[2024] = "ensu2024_bd_csv_zip"
PAYLOAD_ID[2025] = "ensu2025_bd_csv_zip"
OLAS_PISOS = ["2024T1", "2025T3", "2025T4"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def manifiesto():
    m = yaml.safe_load((RAIZ / "data/manifiesto.yaml").read_text(encoding="utf-8"))
    lista = m if isinstance(m, list) else next(v for v in m.values() if isinstance(v, list))
    return {e["id"]: e for e in lista if isinstance(e, dict) and "id" in e}


def disponibilidad():
    cols = {}
    for (anio, t, ruta), c in cabeceras.inventario().items():
        if not M.RX_CB.match(M._base(ruta)):
            continue
        cols[M.ola_de(ruta, M.RX_CB)] = {x.upper() for x in c}
    olas = sorted(cols)
    disp = {}
    for nom, v16, v13, *_ in M.CONDUCTAS:
        disp[nom] = [o for o in olas if (v13 in cols[o] if o <= M.ERA1_FIN else v16 in cols[o])
                     and (nom not in M.FILTRO or M.FILTRO[nom][0] in cols[o])]
    return olas, disp


def spec(calc, punto, olas, disp, man):
    inputs = []
    for a in M.ANIOS:
        e = man[PAYLOAD_ID[a]]
        inputs.append({"id": PAYLOAD_ID[a], "origen": "manifiesto", "sha256": e["sha256"], "funcion": "DATO",
                       "nota": f"ENSU {a} base de datos ({e['archivo']})"})
    inputs.append({"id": "receta_pisos", "origen": "repo", "ruta": RECETA, "sha256": sha(RAIZ / RECETA),
                   "funcion": "CODIGO", "nota": "receta común de GEN2-SALUD-Y-BIENESTAR-PISOS-1 (num, marginales, "
                   "bootstrap, resumen) ejecutada desde estos bytes, sin editar"})
    inputs.append({"id": "dictamen_series", "origen": "repo", "ruta": DICTAMEN, "sha256": sha(RAIZ / DICTAMEN),
                   "funcion": "CODIGO", "nota": "vocabulario y desempate DONDE-CAMBIO (#1125) ejecutados desde "
                   "estos bytes, sin editar"})
    variables = []
    for nom, v16, v13, si, univ, cad in M.CONDUCTAS:
        variables.append({"archivo": "ENSU_CB_[mm][aa]", "variable": v16, "rol": f"reactivo {nom} (2016+)"})
        if v13:
            variables.append({"archivo": "ENSU_CB_[mm][aa]", "variable": v13, "rol": f"reactivo {nom} (2013-2015)"})
    for v in ("CD", "EST_DIS", "EDIS", "UPM_DIS", "FAC_SEL", "FACTOR", "UPM", "VIV_SEL", "H_MUD", "R_SEL",
              "SEXO", "EDAD", "ENT", "CON", "V_SEL", "N_HOG", "N_REN", "BP3_5"):
        variables.append({"archivo": "ENSU_CB_[mm][aa]", "variable": v, "rol": "llave, eje, diseño o filtro"})
    for v in ("SEX", "EDA", "EDAD", "N_REN"):
        variables.append({"archivo": "ENSU_CS_[mm][aa]", "variable": v, "rol": "eje o llave (hasta 2021T1)"})
    return {
        "calc_id": calc,
        "spec_md": f"../../../{SPEC_MD}",
        "spec_md_sha256": sha(RAIZ / SPEC_MD),
        "script": f"data/corrida0/{calc}/medidor.py",
        "dependencias_materiales": ["numpy", "pandas"],
        "etiquetas": {
            "generacion": "GEN2", "uso_motor": "NO-ADOPTA-NADA", "cuenta_gen2": "SI", "adopta": "NO",
            "cuenta_gen2_nota": "CONTADOR del encargo GEN2-SEGURIDAD-ENSU-SERIE-1 (cuenta_gen2: SI, adopta: NO)",
            "fuente_acto": "GEN2-SEGURIDAD-ENSU-SERIE-1",
            "tipo": "PISO-POR-SEGMENTO-DESDE-MICRODATO" if punto == "pisos" else "SERIE-TRIMESTRAL-Y-DICTAMEN",
            "agrupacion": "UNA-SOLA-VARIABLE",
            "marca": "DESCRIPTIVO/RETROSPECTIVA -- nada se evalúa prospectivamente",
            "firmas": "F-ASTRA-5-3, F-ASTRA-5-4, regla 6, vocabulario DONDE-CAMBIO (#1125) (encargo §2, verbatim)",
            "unidad_transferencia": "PERSONA-18-MAS-URBANA",
            "olas": "2013T3-2025T4 abiertas; 2026 RESERVADA (E.6, F-ASTRA-5-3), no es input",
        },
        "inputs": inputs,
        "variables": variables,
        "universo": "Persona seleccionada de 18+ (tabla CB) con factor > 0, estrato y UPM de diseño no vacíos; "
                    "universo de cada conducta en lista-cerrada-P1 §3.",
        "filtros": "Un eje a la vez; nunca cruces. Ejes por punto de entrada en spec §4.",
        "ponderador": "FAC_SEL (2016+); FACTOR (2013-2015)",
        "transformacion": "Por texto: lista-cerrada-P1 §3; spec §2-§5.",
        "estimando": ("Pisos por segmento ENSU 2024T1, 2025T3, 2025T4 de 15 proporciones de personas con IC de diseño"
                      if punto == "pisos" else
                      "Serie trimestral ENSU 2013T3-2025T4 de 15 proporciones de personas por TOTAL/SEXO/EDAD "
                      "(+CIUDAD para C01), τ² de persistencia por eje y cadencia, dictamen DONDE-CAMBIO por serie"),
        "seed": {"aplica": True, "valor": 20260925, "rng": "numpy.PCG64"},
        "parametros": {
            "punto_de_entrada": punto,
            "bootstrap_replicas": 1000,
            "metodo_ic": "bootstrap UPM con reposición dentro de estrato (CD+estrato); singleton de certeza; "
                         "percentiles 2.5/97.5; bloques de 50; contrato conservador",
            "olas": olas,
            "payloads": {str(a): PAYLOAD_ID[a] for a in M.ANIOS},
            "disponibilidad": {c: [o for o in disp[c] if o in olas] for c in M.NOMBRES},
        },
        "tolerancia": {"tipo": "flotante", "abs": 1.0e-10,
                       "razon": "bootstrap determinista por semilla; mismo payload y sumas float64"},
        "resultados": M.esquema_resultados(punto, olas, {c: [o for o in disp[c] if o in olas] for c in M.NOMBRES}),
    }


def main():
    man = manifiesto()
    olas, disp = disponibilidad()
    for calc, punto, ol in (("CALC-ENSU-PISOS-0001", "pisos", OLAS_PISOS), ("CALC-ENSU-SERIE-0001", "serie", olas)):
        d = RAIZ / "data/corrida0" / calc
        d.mkdir(parents=True, exist_ok=True)
        s = spec(calc, punto, ol, disp, man)
        cab = (f"# {calc} -- contrato ejecutable de {SPEC_MD} (D-15). COMMIT-1, antes de abrir microdato.\n"
               "# GENERADO por tools/dominios/ensu/genera_spec_yaml.py\n"
               "# El primer resultado que produzca este procedimiento es el que se reporta.\n")
        (d / "spec.yaml").write_text(cab + yaml.safe_dump(s, allow_unicode=True, sort_keys=False, width=120),
                                     encoding="utf-8")
        shutil.copyfile(MEDIDOR, d / "medidor.py")
        print(calc, "olas", len(ol), "resultados", len(s["resultados"]))


if __name__ == "__main__":
    main()
