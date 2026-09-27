#!/usr/bin/env python3
"""Genera los spec.yaml de los CALC de GEN2-COLA-COMPLETA-1.

Se corre en el COMMIT-1, antes de abrir microdato: toma el sha256 de cada payload del manifiesto
(por id), el de la receta, el motor y la spec humana del árbol, y la lista `resultados:` de
`esquema_resultados()` de cada medidor. No lee ningún dato.

    python3 tools/dominios/cola-completa/genera_spec_yaml.py
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
RECETA = "tools/dominios/salud/pisos_diseno.py"
MOTOR = "tools/dominios/confianza/motor_pisos.py"
ACTO = "GEN2-COLA-COMPLETA-1"
ENCARGO = "forense/encargos/2026-09-26-GEN2-COLA-COMPLETA-1.md"
REPLICAS = 2000

# calc → (spec humana, semilla, universo, ponderador, diseño, estimando, nota de ola, unidad,
#         {variable: miembro del zip} — `archivo` exacto para `corrida0 spec-check`)
CALCS = {
    "CALC-ENDISEG-PISOS-2021-0001": dict(
        spec="COLA-ENDISEG-PISOS-spec-v1_0.md", seed=20260926, ola="2021",
        universo="Persona seleccionada de 15+ (P4_1 15-96), ENDISEG 2021, tabla TMODULO; FACTOR>0, EST_DIS y UPM_DIS no vacios.",
        ponderador="FACTOR (TMODULO: persona seleccionada)", disenio="UPM UPM_DIS dentro de estrato EST_DIS",
        estimando="Pisos por segmento ENDISEG 2021 de 8 conductas (LGBT+, orientacion, identidad, variacion intersexual, escolaridad y situacion conyugal); ola unica",
        nota_ola="ENDISEG 2021 (unica ola del instrumento; ENDISEG web 2022 es otro instrumento y no es input)",
        unidad="PERSONA", miembro=lambda m: {c: "TMODULO.csv" for c in m.columnas()}),
    "CALC-MMSI-PISOS-2016-0001": dict(
        spec="COLA-MMSI-PISOS-spec-v1_0.md", seed=20260927, ola="2016",
        universo="Persona informante de 25-64 anos (P1_2), MMSI 2016; Factor_Per>0, est_dis_ENH y upm_ENH no vacios.",
        ponderador="Factor_Per", disenio="UPM upm_ENH dentro de estrato est_dis_ENH",
        estimando="Pisos por segmento MMSI 2016 de 5 conductas (educacion superior, ocupacion directiva, mejora socioeconomica percibida) con ejes de tono de piel y origen autoadscrito como marcador de trato; ola unica",
        nota_ola="MMSI 2016 (unica ola del modulo en corpus; se abre, E.6)",
        unidad="PERSONA", miembro=lambda m: {c: "MMSI_2016.csv" for c in m.columnas()}),
    "CALC-LATINOBAROMETRO-COLA-2023-0001": dict(
        spec="COLA-LATINOBAROMETRO-PISOS-spec-v1_0.md", seed=20260928, ola="2023",
        universo="Persona 18+ (edad>=18) de Mexico (idenpa=484), Latinobarometro 2023; wt>0.",
        ponderador="wt", disenio="sin estrato ni UPM en el archivo: bootstrap ponderado de entrevistas (MAS-PONDERADO)",
        estimando="Pisos por segmento Latinobarometro 2023 Mexico de 3 conductas nuevas mas ORO-CONFIA-GOBIERNO; 2024 RESERVADA",
        nota_ola="2023 abierta; 2024 RESERVADA (E.6), no es input",
        unidad="PERSONA", miembro=lambda m: {c: "Latinobarometro_2023_Esp_Stata_v1_0.dta" for c in m.columnas()}),
    "CALC-EIC-HOGARES-2015-0001": dict(
        spec="COLA-EIC-HOGARES-spec-v1_0.md", seed=20260929, ola="2015",
        universo="Vivienda particular habitada con tipo de hogar conocido (TIPOHOG 1,2,3,5,6), Encuesta Intercensal 2015; FACTOR>0, ESTRATO y UPM no vacios.",
        ponderador="FACTOR (vivienda)", disenio="UPM UPM dentro de estrato ESTRATO",
        estimando="Distribucion de tipo de hogar (ampliado, nuclear, unipersonal; ampliado entre familiares) por sexo de la jefatura, tamano de localidad y entidad; ola unica; CCPV 2020 RESERVADO",
        nota_ola="Intercensal 2015 (unica ola del instrumento); Censo 2020 RESERVADO (E.6), no es input",
        unidad="HOGAR", miembro=lambda m: {c: "TR_VIVIENDA15.CSV" for c in m.columnas()}),
    "CALC-ENASEM-ESCOLARIDAD-2021-0001": dict(
        spec="COLA-ENASEM-ESCOLARIDAD-spec-v1_0.md", seed=20260930, ola="2021",
        universo="Persona entrevistada de 50+ (AGE_21>=50), ENASEM 2021; FACTORI_21>0, EST_DIS_21 y UPM_DIS_21 no vacios.",
        ponderador="FACTORI_21 (factor individual transversal 2021)", disenio="UPM UPM_DIS_21 dentro de estrato EST_DIS_21",
        estimando="Proporcion sin escolaridad y con 6 anos o menos de escolaridad por sexo y edad; 2024 RESERVADA",
        nota_ola="2021 abierta; 2024 RESERVADA (E.6), no es input",
        unidad="PERSONA", miembro=lambda m: {c: "SECT_A_C_D_E_PC_F_H_I_2021.csv" for c in m.columnas()}),
    "CALC-ENADID-COLA-2018-0001": dict(
        spec="COLA-ENADID-PISOS-spec-v1_0.md", seed=20261001, ola="2018",
        universo="(a) Mujeres elegibles de 15-54 (TMujer2), fac_per>0; (b) hogares (renglon de jefatura de TSdem), fac_viv>0; est_dis y upm_dis no vacios.",
        ponderador="fac_per (mujeres) / fac_viv (hogares)", disenio="UPM upm_dis dentro de estrato est_dis, por marco",
        estimando="Disolucion segun tipo de union actual o ultima y jefatura femenina en hogares con/sin emigrante varon en el extranjero; 2023 RESERVADA para estas conductas",
        nota_ola="2018 abierta; 2023 RESERVADA (E.6), no es input",
        unidad="PERSONA (mujeres) y HOGAR (jefatura)", miembro=None),
    "CALC-PEW-RELIGION-2024-0001": dict(
        spec="COLA-PEW-RELIGION-spec-v1_0.md", seed=20261002, ola="2024",
        universo="Persona 18+ de Mexico (country=35), PEW Global Attitudes 2024; weight>0.",
        ponderador="weight", disenio="sin estrato ni UPM en el archivo 2024: bootstrap ponderado de entrevistas (MAS-PONDERADO)",
        estimando="Afiliacion catolica, sin religion, cambio de religion y creencia en Dios, Mexico 2024; 2025 RESERVADA",
        nota_ola="2024 abierta; 2025 RESERVADA (E.6), no es input",
        unidad="PERSONA", miembro=lambda m: {c: "Pew Research Center Global Attitudes Spring 2024 Dataset.sav"
                                              for c in m.columnas()}),
    "CALC-ENVIPE-PERCEPCION-2024-0001": dict(
        spec="COLA-ENVIPE-PERCEPCION-spec-v1_0.md", seed=20261003, ola="2024",
        universo="Persona elegida de 18+ (EDAD 18-97), ENVIPE 2024, tabla tper_vic1; FAC_ELE>0, EST_DIS y UPM_DIS no vacios.",
        ponderador="FAC_ELE", disenio="UPM UPM_DIS dentro de estrato EST_DIS",
        estimando="Percepcion de inseguridad en el estado, al caminar de noche y restriccion a menores por temor; ENVIPE 2026 RESERVADA",
        nota_ola="2024 abierta; 2026 RESERVADA (E.6), no es input",
        unidad="PERSONA", miembro=None),
    "CALC-ENOE-PARTICIPACION-2024T4-0001": dict(
        spec="COLA-ENOE-PARTICIPACION-spec-v1_0.md", seed=20261004, ola="2024T4",
        universo="Residente habitual o nuevo (c_res 1,3) con entrevista completa (r_def 0), 15+, ENOE 2024T4 (SDEMT); fac_tri>0, est_d_tri y upm no vacios.",
        ponderador="fac_tri", disenio="UPM upm dentro de estrato est_d_tri",
        estimando="Tasa de participacion economica por sexo y jovenes 18-24 que no estudian ni estan ocupados; 2026T2 RESERVADA y boletin 2026T1 consumido (C4)",
        nota_ola="2024T4 abierta; 2026T2 RESERVADA y 2026T1 consumido para informalidad (C4), no son input",
        unidad="PERSONA", miembro=lambda m: {c: "ENOE_SDEMT424.csv" for c in m.columnas()}),
}
MIEMBROS_MULTI = {
    "CALC-ENADID-COLA-2018-0001": lambda m: (
        [("TMujer2.csv", c) for c in m.COLS_MUJ] + [("TSdem.csv", c) for c in m.COLS_HOG]
        + [("TMigrante.csv", c) for c in m.COLS_MIG]),
    "CALC-ENVIPE-PERCEPCION-2024-0001": lambda m: (
        [(m.MIEMBRO_PER, c) for c in m.COLS_PER] + [(m.MIEMBRO_SDEM, c) for c in m.COLS_SDEM]),
}


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def manifiesto():
    with open(ROOT / "data/manifiesto.yaml") as f:
        m = yaml.safe_load(f)
    ents = m if isinstance(m, list) else next(v for v in m.values() if isinstance(v, list))
    return {e["id"]: e for e in ents if isinstance(e, dict) and "id" in e}


def carga(calc):
    s = importlib.util.spec_from_file_location(f"m_{calc}", ROOT / "data/corrida0" / calc / "medidor.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def variables(calc, m, d):
    if calc in MIEMBROS_MULTI:
        pares = MIEMBROS_MULTI[calc](m)
    else:
        mapa = d["miembro"](m)
        pares = [(mapa[c], c) for c in m.columnas()]
    return [{"archivo": a, "variable": v, "rol": "reactivo o diseno"} for a, v in dict.fromkeys(pares)]


def spec_de(calc, d, man):
    m = carga(calc)
    spec_md = f"forense/prereg-caja/{d['spec']}"
    inputs = [{"id": m.PAY, "origen": "manifiesto", "sha256": man[m.PAY]["sha256"], "funcion": "DATO",
               "nota": Path(man[m.PAY].get("archivo", m.PAY)).name}]
    inputs += [
        {"id": "receta_pisos_salud", "origen": "repo", "ruta": RECETA, "sha256": sha(RECETA),
         "funcion": "CODIGO", "nota": "marginales, bootstrap, resumen, lee_csv_zip (GEN2-SALUD-Y-BIENESTAR-PISOS-1) ejecutados desde estos bytes"},
        {"id": "motor_pisos_confianza", "origen": "repo", "ruta": MOTOR, "sha256": sha(MOTOR),
         "funcion": "CODIGO", "nota": "lectura .dta/.sav con filtro de pais, recodificacion, ejes, diseno, ids (GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1) ejecutados desde estos bytes"},
    ]
    return {
        "calc_id": calc,
        "spec_md": f"../../../{spec_md}",
        "spec_md_sha256": sha(spec_md),
        "script": f"data/corrida0/{calc}/medidor.py",
        "dependencias_materiales": ["numpy", "pandas", "pyreadstat"],
        "etiquetas": {
            "generacion": "GEN2", "uso_motor": "NO-ADOPTA-NADA", "cuenta_gen2": "SI", "adopta": "NO",
            "cuenta_gen2_nota": f"CONTADOR del encargo {ACTO} (cuenta_gen2: SI, adopta: NO)",
            "fuente_acto": ACTO, "encargo": ENCARGO, "tipo": "PISO-POR-SEGMENTO-DESDE-MICRODATO",
            "agrupacion": "UNA-SOLA-VARIABLE",
            "marca": "DESCRIPTIVO -- pisos por segmento; RETROSPECTIVO; nada se evalua contra R en este CALC",
            "firmas": "F-ASTRA-5-2/3/4, regla 6, E.6, §3, §4, C4 de FIRMAS-16 (encargo §2, verbatim)",
            "unidad_transferencia": d["unidad"], "olas": d["nota_ola"],
        },
        "inputs": inputs,
        "variables": variables(calc, m, d),
        "universo": d["universo"],
        "filtros": "Un eje a la vez; nunca cruces. Recodificacion por texto de pregunta: spec humana §2.",
        "ponderador": d["ponderador"],
        "transformacion": "bin(col, UNO, CERO); todo otro codigo fuera (spec humana §2).",
        "estimando": d["estimando"],
        "seed": {"aplica": True, "valor": d["seed"], "rng": "numpy.PCG64"},
        "parametros": {
            "bootstrap_replicas": REPLICAS,
            "metodo_ic": "bootstrap UPM con reposicion dentro de estrato; singleton de certeza; percentiles 2.5/97.5; bloques de 50; contrato conservador",
            "diseno": d["disenio"],
            "ola": d["ola"],
        },
        "tolerancia": {"tipo": "flotante", "abs": 1.0e-10,
                       "razon": "bootstrap determinista por semilla; mismo payload y sumas float64"},
        "resultados": m.esquema_resultados(),
    }


def main():
    man = manifiesto()
    for calc, d in CALCS.items():
        spec = spec_de(calc, d, man)
        cab = (f"# {calc} -- contrato ejecutable de la spec humana (D-15). COMMIT-1, antes de abrir microdato.\n"
               "# El primer resultado que produzca este procedimiento es el que se reporta.\n")
        (ROOT / "data/corrida0" / calc / "spec.yaml").write_text(
            cab + yaml.safe_dump(spec, allow_unicode=True, sort_keys=False, width=100))
        print(calc, len(spec["resultados"]), "RESULT")


if __name__ == "__main__":
    main()
