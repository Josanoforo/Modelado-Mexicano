#!/usr/bin/env python3
"""Genera los `spec.yaml` de los CALC del lote ENIF 2024 desde UNA fuente:
la rejilla se LEE del árbitro (`milpa/tramite-ola5-propuesta-v0.yaml`, regla
`dinero.ahorro.via_informal_ejes_enif2024`) y de los ids sellados de
`CALC-ARBITRO-MARGINALES-ENIF2024-0001`; el catálogo de RESULT lo deriva
`enif_lote.catalogo_resultados()` -- la misma enumeración que `medir()`
recorre. Nada se teclea dos veces.

ACTO `GEN2-DIN-LOTE-ENIF2024-COMMIT-1`. Uso:
    python3 tools/lote_enif2024/genera_specs.py [--escribe]
Sin `--escribe` imprime qué escribiría. Con `--escribe` deposita spec.yaml y
medidor.py (byte a byte `enif_lote.py`) en cada CALC; no toca sellos.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]


def _importa(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


EL = _importa("enif_lote", RAIZ / "tools" / "lote_enif2024" / "enif_lote.py")

SPEC_MD = "forense/prereg-caja/DIN-lote-enif2024-spec-v1_0.md"
ARBITRO_YAML = RAIZ / "milpa" / "tramite-ola5-propuesta-v0.yaml"
REGLA = "dinero.ahorro.via_informal_ejes_enif2024"
CALC_971 = "CALC-ARBITRO-MARGINALES-ENIF2024-0001"
CALC_C2IC = "CALC-C2-COMPUESTO-IC-ENIF2024-0001"
CALC_P1_EM = "CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001"
CALC_P1_ARB = "CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001"

EJE_971 = {"sexo": "SEXO", "edad": "EDAD", "escolaridad": "ESCOLARIDAD",
           "localidad": "LOCALIDAD", "formalidad": "FORMALIDAD", "cuenta_formal": "CUENTA"}
CAT_971 = {"1 Hombre": "1", "2 Mujer": "2", "18-29": "18-29", "30-44": "30-44", "45-59": "45-59",
           "60+": "60-MAS", "hasta primaria": "HASTA-PRIMARIA", "secundaria": "SECUNDARIA",
           "media superior": "MEDIA-SUPERIOR", "superior": "SUPERIOR",
           "menor de 15 000": "MENOR-DE-15-000", "15 000 y mas": "15-000-Y-MAS",
           "sin seguridad social": "SIN-SEGURIDAD-SOCIAL", "con seguridad social": "CON-SEGURIDAD-SOCIAL",
           "sin cuenta": "SIN-CUENTA", "con cuenta": "CON-CUENTA"}

# Los 14 pares, con su grupo (spec §3) y el dictamen sellado de C2
# (`data/corrida0/c2-compuesto-dictamen-v1_0.tsv`, ENIF 2024, principal).
PARES = {
    "edadxsexo": ("edad", "sexo", "PRIMARIO"),
    "escolaridadxsexo": ("escolaridad", "sexo", "PRIMARIO"),
    "localidadxsexo": ("localidad", "sexo", "PRIMARIO"),
    "edadxescolaridad": ("edad", "escolaridad", "PRIMARIO"),
    "escolaridadxlocalidad": ("escolaridad", "localidad", "PRIMARIO"),
    "formalidadxsexo": ("formalidad", "sexo", "FORMALIDAD"),
    "edadxformalidad": ("edad", "formalidad", "FORMALIDAD"),
    "escolaridadxformalidad": ("escolaridad", "formalidad", "FORMALIDAD"),
    "formalidadxlocalidad": ("formalidad", "localidad", "FORMALIDAD"),
    "cuenta_formalxsexo": ("cuenta_formal", "sexo", "CUENTA-FORMAL"),
    "cuenta_formalxedad": ("cuenta_formal", "edad", "CUENTA-FORMAL"),
    "cuenta_formalxescolaridad": ("cuenta_formal", "escolaridad", "CUENTA-FORMAL"),
    "cuenta_formalxlocalidad": ("cuenta_formal", "localidad", "CUENTA-FORMAL"),
    "cuenta_formalxformalidad": ("cuenta_formal", "formalidad", "CUENTA-FORMAL"),
}
# Nombres y orden (a, b) tal cual los usa el marcador (`celda_id_marcador
# = CRUCE-GRUPO::<regla>::<par>`) y el dictamen sellado de C2.
NO_EMITIBLE = ("NO-EMITIBLE:A-BIS-4 UNIVERSO-RESTRINGIDO -- formalidad cubre 0.689676 del "
               "universo (universo_restringido: true en el árbitro); C2 no compone contra "
               "ejes de universo completo (c2-compuesto-dictamen-v1_0.tsv, ENIF 2024)")

COLUMNAS = {
    "2021": {"tabla_sufijo": "conjunto_de_datos_tmodulo_enif_2021.csv", "edad": "EDAD", "tloc": "TLOC",
             "peso": "FAC_ELE", "est": "EST_DIS", "upm": "UPM_DIS", "sexo": "SEXO",
             "escolaridad": "P3_1_1", "formalidad": "P3_10",
             "cuentas": [f"P5_4_{i}" for i in range(1, 10)],
             "informal": [f"P5_1_{i}" for i in range(1, 7)],
             "formal": [f"P5_7_{i}" for i in range(1, 10)]},
    "2024": {"tabla_sufijo": "conjunto_de_datos_tmodulo_enif2024.csv", "edad": "EDAD_V", "tloc": "TLOC",
             "peso": "FAC_PER", "est": "EST_DIS", "upm": "UPM_DIS", "sexo": "SEXO",
             "escolaridad": "NIV", "formalidad": "P3_13",
             "cuentas": [f"P5_4_{i}" for i in range(1, 10)],
             "informal": [f"P5_1_{i}" for i in range(1, 7)],
             "formal": [f"P5_6_{i}" for i in range(1, 10)]},
}
# Catálogos por ETIQUETA (spec §2): 2021 de `catalogos/p3_1_1.csv` del
# payload enif2021_csv; 2024 del FD `enif_2024_fd.xlsx` hoja TMODULO filas 30-42.
ESC_CAT = {
    "2021": {"0": "Ninguno", "1": "Preescolar o kínder", "2": "Primaria", "3": "Secundaria",
             "4": "Estudios técnicos con secundaria terminada", "5": "Normal básica",
             "6": "Preparatoria o bachillerato", "7": "Estudios técnicos con preparatoria terminada",
             "8": "Licenciatura o ingeniería (profesional)", "9": "Maestría o doctorado", "99": "No sabe"},
    "2024": {"0": "Ninguno", "1": "Preescolar o kínder", "2": "Primaria", "3": "Secundaria",
             "4": "Normal básica", "5": "Estudios técnicos con secundaria terminada",
             "6": "Preparatoria o bachillerato", "7": "Estudios técnicos con preparatoria terminada",
             "8": "Licenciatura o ingeniería (profesional)", "9": "Especialidad", "10": "Maestría",
             "11": "Doctorado", "99": "No sabe"},
}
ESC_TRAMO = {"Ninguno": "hasta primaria", "Preescolar o kínder": "hasta primaria", "Primaria": "hasta primaria",
             "Secundaria": "secundaria",
             "Estudios técnicos con secundaria terminada": "media superior", "Normal básica": "media superior",
             "Preparatoria o bachillerato": "media superior",
             "Estudios técnicos con preparatoria terminada": "media superior",
             "Licenciatura o ingeniería (profesional)": "superior", "Maestría o doctorado": "superior",
             "Especialidad": "superior", "Maestría": "superior", "Doctorado": "superior"}
FORMALIDAD_MAP = {
    "2021": {**{k: "con seguridad social" for k in "12345"}, "6": "sin seguridad social"},
    "2024": {**{k: "con seguridad social" for k in "123456"}, "7": "sin seguridad social"},
}
LOCALIDAD_MAP = {"1": "15 000 y mas", "2": "15 000 y mas", "3": "menor de 15 000", "4": "menor de 15 000"}
REGLA_V03 = ("v0.3: dMAE = MAE(C2) - MAE(R2) en pp sobre las celdas PUNTUADAS de los 5 pares primarios, "
             "IC95 por réplica (misma réplica k en R, C2 y R2); VENCE-RETADOR si IC95inf > 0.5 pp; "
             "PROPUESTA-CON-RESERVA si 0 < IC95inf <= 0.5; NADIE-VENCE si incluye 0. Retador primario R2 "
             "(lambda = 1/2 fija); P2, R1, R3, L1, L2 y los 9 pares no primarios se adjudican con la misma "
             "regla rotulados SECUNDARIA. El conteo de 3/4 se reporta, no adjudica.")


def rejilla_del_arbitro() -> dict:
    """{eje: {"orden": [categorías]}} leído de la regla del árbitro."""
    doc = yaml.safe_load(ARBITRO_YAML.read_text(encoding="utf-8"))
    regla = next(r for r in doc["reglas_propuestas"] if isinstance(r, dict) and r.get("id") == REGLA)
    ejes = {}
    for e in regla["desenlaces"]["principal"]["ejes"]:
        ejes[e["eje"]] = {"orden": [c["celda"] for c in e["celdas"]],
                          "universo_restringido": bool(e.get("universo_restringido", False)),
                          "cobertura_arbitro": float(e["cobertura"])}
    return ejes


def ids_971(ejes: dict) -> tuple:
    res = json.loads((RAIZ / "data" / "corrida0" / CALC_971 / "resultados.json").read_text())["resultados"]
    puntos, masa = {}, {}
    for eje, cfg in ejes.items():
        puntos[eje], masa[eje] = {}, {}
        for cat in cfg["orden"]:
            base = f"RESULT-ARBITRO-ENIF2024-D9-{EJE_971[eje]}-{CAT_971[cat]}"
            for rid in (f"{base}-P", f"{base}-DEN-W"):
                if rid not in res:
                    raise SystemExit(f"id ausente en {CALC_971}: {rid}")
            puntos[eje][cat] = f"{base}-P"
            masa[eje][cat] = f"{base}-DEN-W"
    return puntos, masa, "RESULT-ARBITRO-ENIF2024-D9-TOTAL-TODOS-P", "RESULT-ARBITRO-ENIF2024-D9-TOTAL-TODOS-DEN-W"


def base_parametros(regimen: str, edad_max: int) -> dict:
    ejes = rejilla_del_arbitro()
    puntos, masa, nac_p, nac_w = ids_971(ejes)
    tramos = {"18-29": [18, 29], "30-44": [30, 44], "45-59": [45, 59], "60+": [60, int(edad_max)]}
    if regimen == "PILOTO-1":
        reg = {"tipo": "PILOTO-1", "edad_min": 18, "edad_max": 97, "edad_centinelas": ["98", "99"],
               "tloc": ["1", "2", "3", "4"]}
    else:
        reg = {"tipo": "ARBITRO-2024", "edad_min": 18, "edad_centinelas": ["98", "99"]}
    return {
        "bootstrap_replicas": 10000, "umbral_soporte_n": 200, "lambda_r2": 0.5,
        "universo_regimen": reg,
        "ola_nueva": "2024", "ola_anterior": "2021",
        "olas_zip": {"2021": "enif2021_csv", "2024": "enif2024_csv"},
        "columnas": COLUMNAS, "edad_tramos": tramos,
        "escolaridad_catalogo": ESC_CAT, "escolaridad_tramo_por_etiqueta": ESC_TRAMO,
        "escolaridad_fuera_etiquetas": ["No sabe"],
        "localidad_map": LOCALIDAD_MAP, "formalidad_map": FORMALIDAD_MAP,
        "ejes": {e: {"orden": c["orden"], "universo_restringido": c["universo_restringido"],
                     "cobertura_arbitro": c["cobertura_arbitro"]} for e, c in ejes.items()},
        "pares": {n: {"a": a, "b": b, "grupo": g,
                      "c2": "EMITIBLE" if "formalidad" not in (a, b) else NO_EMITIBLE}
                  for n, (a, b, g) in PARES.items()},
        "grupo_primario": "PRIMARIO",
        "marginales_sellados": {
            "puntos": {"input": "arbitro_marginales_2024", "formato": "resultados-json",
                       "ids": puntos, "nacional_id": nac_p},
            "masa": {"input": "arbitro_marginales_2024", "formato": "resultados-json",
                     "ids": masa, "nacional_id": nac_w}},
        "r3_ipf": {"tol": 1e-12, "max_iter": 2000},
        "umbral_vence_pp": 0.5, "umbral_reserva_pp": 0.0,
        "regla_v0_3": REGLA_V03,
        "m_estado": ("NO-DERIVABLE -- firma F2: no existe una theta calibrada que emita esta celda; la "
                     "matriz no es estimador por defecto de una celda que no adjudico (A-bis 5, ADR-68). "
                     "El silencio se escribe."),
        "l_estado": ("NO-ENTRA-EN-ESTE-CALC -- L1/L2 los corre mesa por CLI (FP-228) con el paquete "
                     "PAQUETE-L-LOTE-ENIF2024-v1_0; las capturas se sellan antes del COMMIT-2 mecanico"),
    }


def _sha(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def input_repo(iid: str, ruta: str, nota: str = "", sha: str | None = None) -> dict:
    d = {"id": iid, "origen": "repo", "ruta": ruta}
    if sha is not None or (RAIZ / ruta).exists():
        d["sha256"] = sha if sha is not None else _sha(RAIZ / ruta)
    if nota:
        d["nota"] = nota
    return d


INPUTS_COMUNES = [
    {"id": "enif2021_csv", "origen": "manifiesto", "nota": "ENIF 2021 datos abiertos, TMODULO (ola de desarrollo, abierta)"},
    {"id": "enif2024_csv", "origen": "manifiesto",
     "nota": "ENIF 2024 datos abiertos, TMODULO -- en emisiones SOLO marginales de UN eje (guardia); contenido "
             "identico a enif_2024_bd_csv (cotejado por multiconjunto de columnas en este acto)"},
]


def inputs_lote() -> list:
    return INPUTS_COMUNES + [
        input_repo("arbitro_marginales_2024", f"data/corrida0/{CALC_971}/resultados.json",
                   "marginales D9 de ENIF 2024 por eje, SELLADOS (#971): puntos y masa ponderada; no se re-miden"),
        input_repo("cruces_familia_py", "tools/duelo/cruces_familia.py",
                   "codigo generico del duelo (#968), importado por ruta; ajeno, no se edita"),
        input_repo("lote_familia_py", "tools/lote_enif2024/lote_familia.py",
                   "modulo propio del lote (R3, cobertura, 3/4, B-bis), importado por ruta"),
    ]


def dimensiones(regimen_txt: str) -> dict:
    return {
        "variables": [
            {"archivo": "conjunto_de_datos_tmodulo_enif_2021.csv", "variable": v, "rol": r} for v, r in (
                ("P5_1_1..P5_1_6", "desenlace-informal-2021"), ("P5_7_1..P5_7_9", "desenlace-formal-2021 (nueve cuentas)"),
                ("P5_4_1..P5_4_9", "eje-cuenta_formal-2021"), ("SEXO", "eje-sexo-2021"), ("EDAD", "eje-edad-2021 y filtro"),
                ("P3_1_1", "eje-escolaridad-2021 (catalogo por etiqueta)"), ("TLOC", "eje-localidad-2021 y filtro"),
                ("P3_10", "eje-formalidad-2021"), ("FAC_ELE", "ponderador-2021"), ("EST_DIS", "estrato-2021"), ("UPM_DIS", "upm-2021"))
        ] + [
            {"archivo": "conjunto_de_datos_tmodulo_enif2024.csv", "variable": v, "rol": r} for v, r in (
                ("P5_1_1..P5_1_6", "desenlace-informal-2024"), ("P5_6_1..P5_6_9", "desenlace-formal-2024 (nueve cuentas)"),
                ("P5_4_1..P5_4_9", "eje-cuenta_formal-2024"), ("SEXO", "eje-sexo-2024"), ("EDAD_V", "eje-edad-2024 y filtro"),
                ("NIV", "eje-escolaridad-2024 (catalogo por etiqueta)"), ("TLOC", "eje-localidad-2024 y filtro"),
                ("P3_13", "eje-formalidad-2024"), ("FAC_PER", "ponderador-2024"), ("EST_DIS", "estrato-2024"), ("UPM_DIS", "upm-2024"))
        ],
        "universo": ("Personas ELEGIDAS de 18 anos y mas de TMODULO de ENIF, una fila por persona. " + regimen_txt),
        "filtros": ("PILOTO-1 (spec v1_0 §1): (1) 18 <= edad <= 97 en las dos olas, 98/99 centinelas fuera y contados; "
                    "(2) TLOC en {1,2,3,4}; (3) ponderador presente y > 0. Nada mas. Sobre ENIF 2024 en emisiones: "
                    "una sola variable de agrupacion por lectura (guardia probada en cada corrida); el cruce solo en "
                    "adjudicacion, por la unica funcion cruce() y solo sobre pares autorizados por el contrato."),
        "ponderador": "ENIF 2021 = FAC_ELE (factor del elegido; FAC_PER no existe en 2021); ENIF 2024 = FAC_PER. Toda proporcion es razon de totales ponderados.",
        "transformacion": ("D9 := alguna P5_1_k == '1' (k=1..6) Y ninguna via formal == '1' (2021: P5_7_1..9; 2024: P5_6_1..9). "
                           "Ejes: sexo (1/2); edad en 4 tramos del arbitro; escolaridad por ETIQUETA del catalogo de cada ola "
                           "(codigo sin etiqueta declarada -> PARO; 'No sabe' -> fuera); localidad TLOC {1,2} vs {3,4}; "
                           "formalidad P3_10 (2021: 1-5 con, 6 sin) / P3_13 (2024: 1-6 con, 7 sin), blanco y 9 fuera; "
                           "cuenta_formal alguna P5_4_k == '1' vs ninguna (todas en blanco -> fuera). "
                           "Contendientes (spec v1_0 §4): C2 = expit(logit m24(a) + logit m24(b) - logit m24) con m24 SELLADOS (#971) "
                           "e IC replica a replica; P2 = cruce 2021; R1 = expit(logit C2 + delta21); R2 = expit(logit C2 + 1/2 delta21); "
                           "R3 = raking a tres vias de la tabla ponderada 2021 (a,b,D) a los margenes (a,D),(b,D) de 2024 sellados."),
        "estimando": ("p(ahorra_solo_informal | eje_A, eje_B) -- proporcion ponderada [0,1] de personas elegidas 18+ de ENIF 2024, "
                      "en las 96 celdas de los 14 pares reservados, bajo D9; error en pp."),
        "precision": ("Replicas compartidas por ola: n_h UPM con reemplazo por estrato, PCG64(42), estratos y UPM en orden "
                      "lexicografico, 10 000 replicas; IC95 = percentiles 2.5/97.5 de las replicas definidas; C2/R1/R2/R3 "
                      "combinan replica k con k (2024 con 2021, muestras independientes, sin covarianzas inventadas); "
                      "delta-MAE por replica. No cubre el error de especificacion de ningun candidato."),
        "dependencias_materiales": ["numpy", "pandas", "yaml"],
        "seed": {"aplica": True, "valor": 42, "rng": "numpy.random.PCG64 (replicas compartidas por ola)"},
        "tolerancia": {"tipo": "bootstrap", "exacto_por_seed": True, "abs": 1e-10,
                       "razon": "seed 42 + orden de consumo fijado por replicas() (un generador por ola, estratos y UPM lexicograficos, "
                                "replicas 0..9999); enteros exactos, flotantes abs 1e-10"},
    }


def etiquetas(tipo: str, extra: dict | None = None) -> dict:
    e = {"generacion": "GEN2", "unidad_transferencia": "PERSONA-ELEGIDA-18MAS", "uso_motor": "NO-ADOPTA-NADA",
         "cuenta_gen2": "SI",
         "fuente_acto": "GEN2-DIN-LOTE-ENIF2024-COMMIT-1 (21/sep/2026)",
         "spec_humana": "forense/prereg-caja/DIN-lote-enif2024-spec-v1_0.md (sucede a DIN-lote-enif2024-spec-v0_1-PROPUESTA.md, intacta)",
         "firmas": "F1 FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-01 · F2 -02 · D-22 ampliada -05 · enmienda v0.3 FP-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-01 · opcion A de direccion (lambda = 1/2 en los 14 pares, 21/sep/2026)",
         "medidor_ejecutado_al_congelar": "sintetico (tests/test_lote_enif2024.py, zips fabricados, cada rama terminal) y los dos oros sobre datos ya abiertos; NUNCA un cruce reservado de ENIF 2024",
         "tipo": tipo}
    if extra:
        e.update(extra)
    return e


def _spec_base(calc_id: str, par: dict, inputs: list, tipo: str, extra_etq: dict | None = None,
               regimen_txt: str = "") -> dict:
    d = dimensiones(regimen_txt)
    spec = {"calc_id": calc_id, "spec_md": "../../../" + SPEC_MD,
            "spec_md_sha256": _sha(RAIZ / SPEC_MD) if (RAIZ / SPEC_MD).exists() else "PENDIENTE",
            "script": f"data/corrida0/{calc_id}/medidor.py",
            "etiquetas": etiquetas(tipo, extra_etq),
            "inputs": inputs}
    spec.update({k: d[k] for k in ("variables", "universo", "filtros", "ponderador", "transformacion",
                                   "estimando", "precision", "dependencias_materiales", "seed", "tolerancia")})
    spec["parametros"] = par
    spec["resultados"] = EL.catalogo_resultados(par, [i["id"] for i in inputs])
    return spec


def piloto1_control_ids() -> tuple:
    """Mapas de control contra los sellos del piloto 1 (localidad x edad)."""
    cod = {"menor de 15 000": "L1", "15 000 y mas": "L2", "18-29": "E1", "30-44": "E2", "45-59": "E3", "60+": "E4"}
    em, arb = {}, {}
    for l in ("menor de 15 000", "15 000 y mas"):
        for e in ("18-29", "30-44", "45-59", "60+"):
            c = f"{cod[l]}x{cod[e]}"
            k = f"localidadxedad|{l}|{e}"
            em[k] = {"P2-P": f"RESULT-DIN-LXE8-C1-D9-P-{c}", "P2-IC95INF": f"RESULT-DIN-LXE8-C1-D9-IC95INF-{c}",
                     "P2-IC95SUP": f"RESULT-DIN-LXE8-C1-D9-IC95SUP-{c}", "P2-N": f"RESULT-DIN-LXE8-C1-D9-N-{c}",
                     "C2-P": f"RESULT-DIN-LXE8-C2-P-{c}", "C2-IC95INF": f"RESULT-DIN-LXE8-C2-IC95INF-{c}",
                     "C2-IC95SUP": f"RESULT-DIN-LXE8-C2-IC95SUP-{c}"}
            arb[k] = {"R-P": f"RESULT-DIN-LXE8-ARB-R-D9-P-{c}", "R-IC95INF": f"RESULT-DIN-LXE8-ARB-R-D9-IC95INF-{c}",
                      "R-IC95SUP": f"RESULT-DIN-LXE8-ARB-R-D9-IC95SUP-{c}", "R-N": f"RESULT-DIN-LXE8-ARB-R-D9-N-{c}"}
    return em, arb


def c2ic_ids(par: dict) -> dict:
    """Ids del C2-IC sellado por celda del lote (9 pares EMITIBLE, D9)."""
    res = json.loads((RAIZ / "data" / "corrida0" / CALC_C2IC / "resultados.json").read_text())["resultados"]
    ids = {}
    for nombre, p in par["pares"].items():
        if p["c2"] != "EMITIBLE":
            continue
        for ka in par["ejes"][p["a"]]["orden"]:
            for kb in par["ejes"][p["b"]]["orden"]:
                base = f"RESULT-C2IC-ENIF2024-AHORRA-SOLO-INFORMAL-{EL._slug(nombre)}-{EL._slug(ka)}-X-{EL._slug(kb)}"
                for s in ("P", "IC95INF", "IC95SUP", "REPLICAS-VALIDAS"):
                    if f"{base}-{s}" not in res:
                        raise SystemExit(f"id ausente en {CALC_C2IC}: {base}-{s}")
                ids[f"{nombre}|{ka}|{kb}"] = {s: f"{base}-{s}" for s in ("P", "IC95INF", "IC95SUP", "REPLICAS-VALIDAS")}
    return ids


def specs() -> dict:
    """{calc_id: spec}. Cinco CALC: los dos del lote (COMMIT-2 y COMMIT-3, otra
    sesion) y los tres oros (se corren y sellan en este acto)."""
    out = {}
    reg_txt_p1 = "Regimen PILOTO-1 (spec v1_0 §1): filtros globales; ENIF 2021 completa; ENIF 2024 segun el punto de entrada."
    # ── lote · emisiones (COMMIT-2) ────────────────────────────────────────
    par = base_parametros("PILOTO-1", 97)
    par.update({"punto_de_entrada": "emisiones", "prefijo_result": "RESULT-DIN-LOTE24-EM"})
    out["CALC-DIN-LOTE-ENIF2024-EMISIONES-0001"] = _spec_base(
        "CALC-DIN-LOTE-ENIF2024-EMISIONES-0001", par, inputs_lote(),
        "EMISIONES-DE-CANDIDATOS-14-PARES (COMMIT-2, otra sesion)",
        {"commit": "COMMIT-2", "celda_d": "DIN.ahorra_solo_informal.enif2024.14-pares (SPEC-CONGELADA)",
         "orden_de_commits": "COMMIT-1 (este acto: congela) -> COMMIT-2 emisiones (otra sesion, F3) -> COMMIT-3a fija sha -> COMMIT-3 R y adjudicacion"},
        reg_txt_p1)
    # ── lote · adjudicacion (COMMIT-3) ─────────────────────────────────────
    par = base_parametros("PILOTO-1", 97)
    par.update({"punto_de_entrada": "adjudicacion", "prefijo_result": "RESULT-DIN-LOTE24-ADJ",
                "prefijo_emisiones": "RESULT-DIN-LOTE24-EM", "tol_reproduccion_emisiones": 1e-10,
                "pares_cruce_autorizados_2024": [[a, b] for a, b, _g in PARES.values()],
                "par_vetado_probar": {"a": "localidad", "b": "edad"}})
    ins = inputs_lote() + [
        {"id": "emisiones_selladas", "origen": "repo", "ruta": "data/corrida0/CALC-DIN-LOTE-ENIF2024-EMISIONES-0001/resultados.json",
         "nota": "NO EXISTE en COMMIT-1; lo crea el COMMIT-2. El COMMIT-3a escribe aqui su sha256 antes de correr.",
         "sha256": "PENDIENTE-COMMIT-3A"},
        {"id": "emisiones_sello", "origen": "repo", "ruta": "data/corrida0/CALC-DIN-LOTE-ENIF2024-EMISIONES-0001/sello.json",
         "nota": "NO EXISTE en COMMIT-1; lo crea el COMMIT-2.", "sha256": "PENDIENTE-COMMIT-3A"},
    ]
    out["CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001"] = _spec_base(
        "CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001", par, ins,
        "ARBITRO-14-CRUCES-Y-ADJUDICACION-V0-3 (COMMIT-3, otra sesion)",
        {"commit": "COMMIT-3", "celda_d": "DIN.ahorra_solo_informal.enif2024.14-pares (SPEC-CONGELADA)",
         "condicion": "SE NIEGA A CORRER sin el sello de CALC-DIN-LOTE-ENIF2024-EMISIONES-0001 y sin reproducir sus emisiones a 1e-10",
         "orden_de_commits": "COMMIT-2 emisiones -> COMMIT-3a fija sha de emisiones_selladas/emisiones_sello en ESTE spec.yaml -> COMMIT-3 corrida0 run"},
        reg_txt_p1)
    out["CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001"]["secuencia_commits"] = {
        "fuente": "spec v1_0 §12 y §15; precedente: piloto 3 (FP-407 b) y piloto 1 (c169edc9 -> 39bf1af3 -> 18b99142). E.6 se conserva: R se deriva DESPUES de fijar el arbitro.",
        "commit_2": "OTRA sesion (F3): corrida0 run CALC-DIN-LOTE-ENIF2024-EMISIONES-0001; sella; registro/replay (E.7); commit y push; git ls-remote confirma el sello en origin antes de seguir. Las capturas L1/L2 de mesa se sellan ANTES de este paso.",
        "commit_3a": "La misma sesion del COMMIT-2, en commit aparte y ANTES de derivar R: escribe en ESTE spec.yaml el sha256 de emisiones_selladas y emisiones_sello (huellas de los archivos recien sellados), y verifica corrida0 preflight CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001 = VERDE. Ninguna otra linea cambia.",
        "commit_3": "corrida0 run CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001: reproduce las emisiones, abre los 14 cruces por la guardia, R por celda, soporte, regla v0.3 primaria (44 celdas pooled) y secundarias, cobertura, lectura B-bis; sella; registro/replay.",
        "preflight_esperado_antes_del_commit_3a": "BLOQUEADO exactamente por input_repo_ausente=emisiones_selladas:<ruta> input_repo_no_commiteado=emisiones_selladas input_repo_ausente=emisiones_sello:<ruta> input_repo_no_commiteado=emisiones_sello -- y por nada mas (medido en este acto, 21/sep/2026).",
    }
    # ── oro (i) · piloto 1, emisiones ──────────────────────────────────────
    em_ids, arb_ids = piloto1_control_ids()
    par = base_parametros("PILOTO-1", 97)
    par["pares"] = {"localidadxedad": {"a": "localidad", "b": "edad", "grupo": "ORO-PILOTO-1", "c2": "EMITIBLE"}}
    par["grupo_primario"] = "ORO-PILOTO-1"
    par["marginales_sellados"]["puntos"] = {
        "input": "piloto1_spec_yaml", "formato": "spec-yaml",
        "ids": {"localidad": {"menor de 15 000": "parametros.marginales_sellados_D9.L1.p",
                              "15 000 y mas": "parametros.marginales_sellados_D9.L2.p"},
                "edad": {"18-29": "parametros.marginales_sellados_D9.E1.p", "30-44": "parametros.marginales_sellados_D9.E2.p",
                         "45-59": "parametros.marginales_sellados_D9.E3.p", "60+": "parametros.marginales_sellados_D9.E4.p"}},
        "nacional_id": "parametros.marginales_sellados_D9.NAC.p"}
    par.update({"punto_de_entrada": "emisiones", "prefijo_result": "RESULT-DIN-LOTE24-ORO1-EM",
                "control_sellado": {"input": "piloto1_emisiones", "tol": 1e-9, "celdas": em_ids}})
    ins_oro1 = INPUTS_COMUNES + [
        input_repo("arbitro_marginales_2024", f"data/corrida0/{CALC_971}/resultados.json", "masa ponderada por categoria para R3 (no cotejado en el oro)"),
        input_repo("piloto1_spec_yaml", f"data/corrida0/{CALC_P1_EM}/spec.yaml", "los marginales SELLADOS que el piloto 1 uso (6 decimales de milpa): el oro reproduce su C2 con SUS insumos"),
        input_repo("piloto1_emisiones", f"data/corrida0/{CALC_P1_EM}/resultados.json", "emisiones selladas del piloto 1: C1 (=P2) y C2 por celda"),
        input_repo("cruces_familia_py", "tools/duelo/cruces_familia.py"),
        input_repo("lote_familia_py", "tools/lote_enif2024/lote_familia.py"),
    ]
    out["CALC-DIN-LOTE-ORO-PILOTO1-EMISIONES-0001"] = _spec_base(
        "CALC-DIN-LOTE-ORO-PILOTO1-EMISIONES-0001", par, ins_oro1,
        "RETROSPECTIVA -- oro (i): el codigo generico reproduce las emisiones selladas del piloto 1 (localidad x edad) a 1e-9",
        {"commit": "ORO-COMMIT-1", "adjudica": "NO -- retrospectiva sobre un par ya abierto; no mueve adoptados_activos",
         "celda_d": "DIN.ahorro_solo_informal.enif2024.localidad_x_edad (ya adjudicada por el piloto 1; aqui solo control)"},
        reg_txt_p1)
    # ── oro (i) · piloto 1, adjudicacion (R) ───────────────────────────────
    par = json.loads(json.dumps(par))
    par.update({"punto_de_entrada": "adjudicacion", "prefijo_result": "RESULT-DIN-LOTE24-ORO1-ADJ",
                "prefijo_emisiones": "RESULT-DIN-LOTE24-ORO1-EM", "tol_reproduccion_emisiones": 1e-10,
                "pares_cruce_autorizados_2024": [["localidad", "edad"]],
                "par_vetado_probar": {"a": "sexo", "b": "edad"},
                "control_sellado_R": {"input": "piloto1_arbitro", "tol": 1e-9, "celdas": arb_ids}})
    par.pop("control_sellado", None)
    ins = ins_oro1 + [
        input_repo("piloto1_arbitro", f"data/corrida0/{CALC_P1_ARB}/resultados.json", "R sellado del piloto 1 (COMMIT-3), el oro de la R"),
        {"id": "emisiones_selladas", "origen": "repo", "ruta": "data/corrida0/CALC-DIN-LOTE-ORO-PILOTO1-EMISIONES-0001/resultados.json",
         "nota": "lo crea la corrida del oro de emisiones en este mismo acto; su sha se fija antes de correr este CALC", "sha256": "PENDIENTE-ORO"},
    ]
    out["CALC-DIN-LOTE-ORO-PILOTO1-ADJUDICACION-0001"] = _spec_base(
        "CALC-DIN-LOTE-ORO-PILOTO1-ADJUDICACION-0001", par, ins,
        "RETROSPECTIVA -- oro (i): el codigo generico reproduce la R sellada del piloto 1 (localidad x edad) a 1e-9 y prueba la guardia sobre un par vetado",
        {"commit": "ORO-COMMIT-1", "adjudica": "NO -- retrospectiva; el veredicto v0.3 que emite es ilustrativo y no adjudica nada",
         "celda_d": "DIN.ahorro_solo_informal.enif2024.localidad_x_edad (ya adjudicada por el piloto 1; aqui solo control)"},
        reg_txt_p1)
    # ── oro (ii) · C2-IC, regimen del arbitro ──────────────────────────────
    par = base_parametros("ARBITRO-2024", 96)
    par["olas_zip"] = {"2024": "enif2024_csv"}
    par["pares"] = {n: p for n, p in par["pares"].items() if p["c2"] == "EMITIBLE"}
    par.update({"punto_de_entrada": "oro_c2ic", "prefijo_result": "RESULT-DIN-LOTE24-ORO2",
                "oro_c2ic": {"input": "c2ic_resultados", "ids": c2ic_ids(par), "umbral_replicas_validas": 9000,
                             "tol_ic": 1e-10, "tol_p": 1e-5,
                             "causa_delta_p": ("el C2-IC tomo los puntos de milpa/tramite-ola5-propuesta-v0.yaml (6 decimales); "
                                               "este oro los toma de #971 a precision completa (el mismo numero antes de redondear)")}})
    ins = [INPUTS_COMUNES[1],
           input_repo("arbitro_marginales_2024", f"data/corrida0/{CALC_971}/resultados.json", "puntos sellados a precision completa"),
           input_repo("c2ic_resultados", f"data/corrida0/{CALC_C2IC}/resultados.json", "el C2 con IC sellado: segundo oro"),
           input_repo("cruces_familia_py", "tools/duelo/cruces_familia.py"),
           input_repo("lote_familia_py", "tools/lote_enif2024/lote_familia.py")]
    out["CALC-DIN-LOTE-ORO-C2IC-0001"] = _spec_base(
        "CALC-DIN-LOTE-ORO-C2IC-0001", par, ins,
        "RETROSPECTIVA -- oro (ii): el C2 del lote reproduce replica a replica el C2 con IC sellado (9 pares EMITIBLE, 68 celdas) bajo el regimen del arbitro",
        {"commit": "ORO-COMMIT-1", "adjudica": "NO", "regimen": "ARBITRO-2024: todo TMODULO con edad >= 18 y FAC_PER > 0; fuera por eje (edad 60-96, escolaridad 99, formalidad blanco/9); sin filtro de TLOC -- el de tools/medidor_ahorro_enif24.py::carga()"},
        "Regimen ARBITRO-2024 (el de #971 y del C2-IC): todo TMODULO con EDAD_V >= 18 y FAC_PER > 0; fuera POR EJE. Solo ENIF 2024, un eje por lectura.")
    return out


def main(argv=None) -> int:
    escribe = "--escribe" in (argv or sys.argv[1:])
    for calc_id, spec in specs().items():
        d = RAIZ / "data" / "corrida0" / calc_id
        texto = "# El primer resultado que produzca este procedimiento es el que se reporta.\n" + yaml.safe_dump(
            spec, allow_unicode=True, sort_keys=False, width=110)
        print(f"{calc_id}: {len(spec['resultados'])} RESULT, {len(spec['inputs'])} inputs"
              + ("" if escribe else " (no se escribe)"))
        if escribe:
            d.mkdir(parents=True, exist_ok=True)
            if (d / "sello.sha256").exists():
                print(f"  {calc_id}: ya sellado, no se toca")
                continue
            (d / "spec.yaml").write_text(texto, encoding="utf-8")
            shutil.copyfile(RAIZ / "tools" / "lote_enif2024" / "enif_lote.py", d / "medidor.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
