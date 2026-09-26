#!/usr/bin/env python3
"""Genera el `spec.yaml` (D-15) de los CALC de ACTO GEN2-COLA-LOTE-1.

Uso: python3 tools/dominios/cola-lote-1/genera_spec_yaml.py {CCPV|EMAT|ENPECYT|EDR}

Escribe `data/corrida0/<CALC>/spec.yaml` desde: la cabecera fija de abajo, los sha256 del
manifiesto (por id), el sha256 de la spec humana y de la receta, y `resultados:` =
`esquema_resultados()` del medidor. Se corre ANTES del COMMIT-1; después del COMMIT-1 no se
vuelve a correr (el spec.yaml queda congelado con su medidor).
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
RECETA = "tools/dominios/salud/pisos_diseno.py"
ACTO = "GEN2-COLA-LOTE-1"


def _sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def _manifiesto_sha(ids):
    out, actual = {}, None
    for linea in (ROOT / "data/manifiesto.yaml").read_text(encoding="utf-8").splitlines():
        if linea.startswith("- id: "):
            actual = linea[6:].strip()
        elif actual in ids and linea.startswith("  sha256: ") and actual not in out:
            out[actual] = linea.split(":", 1)[1].strip()
    faltan = set(ids) - set(out)
    if faltan:
        raise SystemExit(f"ids sin sha256 en el manifiesto: {sorted(faltan)}")
    return out


def _medidor(calc):
    p = ROOT / "data/corrida0" / calc / "medidor.py"
    spec = importlib.util.spec_from_file_location(f"m_{calc}", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ENTS = [f"{i:02d}" for i in range(1, 33)]

CONF = {
    "CCPV": {
        "calc": "CALC-CCPV-FAM-PISOS-0001",
        "spec_md": "forense/prereg-caja/CCPV-FAM-PISOS-spec-v1_0.md",
        "payloads": {f"cc1_inegi_ccpv_2010__mc2010_{e}_dta": f"Muestra censal 2010, entidad {e} (viviendas_{e}.dta, "
                     f"personas_{e}.dta)" for e in ENTS},
        "extra_etiquetas": {"unidad_transferencia": "HOGAR (vivienda particular habitada); PERSONA en PER60-*",
                            "olas": "2010 abierta (muestra censal); 2020 RESERVADA (E.6), no es input"},
        "variables": [("viviendas", c, "reactivo, llave, eje o diseno") for c in
                      ["ent", "id_viv", "tipohog", "numpers", "factor", "estrato", "upm", "tam_loc"]]
                     + [("personas", c, "reactivo, llave, eje o diseno") for c in
                        ["ent", "id_viv", "sexo", "edad", "parent", "nivacad", "factor", "estrato", "upm", "tam_loc"]],
        "universo": "Hogares censales (VIVIENDAS) con factor>0, estrato y upm no vacios; personas 60+ (PERSONAS) "
                    "con el mismo filtro para PER60-*; universo de cada conducta en la spec humana §2.",
        "filtros": "Un eje a la vez (hogar: TOTAL, SEXO-JEFE, EDAD-JEFE, ESCOLARIDAD-JEFE, TLOC, ENT; persona: "
                   "TOTAL, SEXO, EDAD, TLOC, ENT); nunca cruces.",
        "ponderador": "factor (VIVIENDAS para hogar; PERSONAS para persona)",
        "transformacion": "Por texto: spec humana §0-§3 (codigos de los .do del ZIP).",
        "estimando": "Pisos por segmento Censo 2010 (muestra) de 13 conductas de hogar (12 proporciones, 1 media) "
                     "y 1 de persona 60+, con IC de diseno; sin persistencia (una ola abierta).",
        "parametros": {"ola": "2010"},
        "dependencias": ["numpy", "pandas", "pyreadstat", "inflate64"],
        "firmas": "F-ASTRA-5-4, regla 6, E.6, §4 (unidades no se promedian: defunciones ≠ personas encuestadas) "
                  "(encargo §2, verbatim)",
    },
}


FIRMAS = ("F-ASTRA-5-4, regla 6, E.6, §4 (unidades no se promedian: defunciones ≠ personas encuestadas) "
          "(encargo §2, verbatim)")

CONF["EMAT"] = {
    "calc": "CALC-EMAT-PAREJA-PISOS-0001",
    "spec_md": "forense/prereg-caja/EMAT-PAREJA-PISOS-spec-v1_0.md",
    "payloads": {"emat2010_2014_bd_dbf_zip": "EMAT 2010-2014 (MATRI10..MATRI14)",
                 "emat2015_2019_bd_dbf_zip": "EMAT 2015-2019 (MATRI15..MATRI19)",
                 "emat2020_bd_dbf_zip": "EMAT 2020 (MATRI20)", "emat2021_bd_dbf_zip": "EMAT 2021 (MATRI21)",
                 "emat2022_bd_dbf_zip": "EMAT 2022 (MATRI22)", "emat2023_bd_dbf_zip": "EMAT 2023 (MATRI23)"},
    "extra_etiquetas": {"unidad_transferencia": "MATRIMONIO REGISTRADO; CONTRAYENTE en C-*",
                        "naturaleza": "REGISTRO ADMINISTRATIVO (sin diseno muestral)",
                        "olas": "2010-2023 abiertas; 2024 RESERVADA (E.6), no es input"},
    "variables": [("MATRIyy", c, "reactivo, eje o diagnostico") for c in
                  ["ENT_REGIS", "TAM_LOC_RE", "ANIO_REGIS", "GENERO", "SEXO_CON1", "EDAD_CON1", "ESCOL_CON1",
                   "CONACTCON1", "SEXO_CON2", "EDAD_CON2", "ESCOL_CON2", "CONACTCON2"]],
    "universo": "Matrimonios registrados (filas vivas de MATRIyy.dbf) por ano de registro 2010-2023; contrayentes = "
                "dos por matrimonio; universo de cada conducta en la spec humana §2.",
    "filtros": "Un eje a la vez (matrimonio: TOTAL, ENT, TLOC; contrayente: TOTAL, SEXO, ESCOLARIDAD, TLOC); nunca cruces.",
    "ponderador": "NO-APLICA (registro completo)",
    "transformacion": "Por texto: spec humana §0-§3 (codigos de los descriptores 2010 y 2023).",
    "estimando": "Pisos por segmento EMAT 2010-2023 de 4 proporciones de matrimonios y 8 conductas de contrayentes "
                 "(7 proporciones, 1 media), exactos del registro, con tau2 e IC calibrado de persistencia sobre 2023.",
    "parametros": {"olas": [str(a) for a in range(2010, 2024)], "piso": "2023",
                   "metodo_icc": "expit(logit p +- 1.959964*sqrt(tau2)); tau2 = media de delta2 logit consecutivas"},
    "registro": True,
    "seed": {"aplica": False, "razon": "registro administrativo completo: sin muestreo ni bootstrap"},
    "dependencias": ["numpy", "pandas"],
    "firmas": FIRMAS,
}

CONF["EDR"] = {
    "calc": "CALC-EDR-SUICIDIO-PISOS-0001",
    "spec_md": "forense/prereg-caja/EDR-SUICIDIO-PISOS-spec-v1_0.md",
    "payloads": {"edr2015_2019_bd_dbf_zip": "EDR 2015-2019 (DEFUN15..DEFUN19)",
                 "cc1_inegi_mortalidad_2020__defunciones_base_datos_2020_dbf": "EDR 2020 (DEFUN20)",
                 "cc1_inegi_edr_2021__defunciones_base_datos_2021_dbf": "EDR 2021 (DEFUN21)",
                 "edr2022_bd_dbf_zip": "EDR 2022 (DEFUN22)",
                 "cc1_inegi_edr_2023__defunciones_base_datos_2023_dbf": "EDR 2023 (DEFUN23)"},
    "extra_etiquetas": {"unidad_transferencia": "DEFUNCION REGISTRADA (nunca persona encuestada)",
                        "naturaleza": "REGISTRO ADMINISTRATIVO (sin diseno muestral; sin tasas)",
                        "olas": "2015-2023 abiertas; 2024 RESERVADA (E.6), no es input"},
    "variables": [("DEFUNyy", c, "reactivo, eje o diagnostico") for c in
                  ["ENT_RESID", "TLOC_RESID", "CAUSA_DEF", "SEXO", "EDAD", "ANIO_OCUR", "ANIO_REGIS", "ESCOLARIDA",
                   "PRESUNTO (2015-2021)", "TIPO_DEFUN (2022-2023)"]],
    "universo": "Defunciones registradas (filas vivas de DEFUNyy.dbf) por ano de registro 2015-2023; universo de cada "
                "conducta en la spec humana §2.",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD, ENT, TLOC, ESCOLARIDAD; ninguno consigo mismo); nunca cruces.",
    "ponderador": "NO-APLICA (registro completo)",
    "transformacion": "Por texto: spec humana §0-§3 (CIE-10 X60-X84; presunto/tipo_defun = 3).",
    "estimando": "Pisos por segmento EDR 2015-2023 de suicidio registrado (dos definiciones) y su composicion por sexo, "
                 "edad y registro tardio, exactos del registro, con tau2 e IC calibrado de persistencia sobre 2023.",
    "parametros": {"olas": [str(a) for a in range(2015, 2024)], "piso": "2023",
                   "metodo_icc": "expit(logit p +- 1.959964*sqrt(tau2)); tau2 = media de delta2 logit consecutivas"},
    "registro": True,
    "seed": {"aplica": False, "razon": "registro administrativo completo: sin muestreo ni bootstrap"},
    "dependencias": ["numpy", "pandas"],
    "firmas": FIRMAS,
}

CONF["ENPECYT"] = {
    "calc": "CALC-ENPECYT-CONOC-PISOS-0001",
    "spec_md": "forense/prereg-caja/ENPECYT-CONOC-PISOS-spec-v1_0.md",
    "payloads": {f"cc1_inegi_enpecyt_{o}__enpecyt{o}_bd_dbf": f"ENPECYT {o} (vivhog, cs, cb1, cb2)"
                 for o in ("2011", "2013", "2015")},
    "extra_etiquetas": {"unidad_transferencia": "PERSONA 18+ elegida (areas urbanas 100 000+)",
                        "olas": "2011, 2013, 2015 abiertas; 2017 RESERVADA (E.6), no es input; 2005-2009 fuera"},
    "variables": [("cb1", "S4P1_3; S4P14_* (por ola, medidor ITEMS); FAC; llave", "reactivo, ponderador o llave"),
                  ("cb2", "S4P26_1/S4P25_1; S4P33_2_1/S4P31_1_1; llave", "reactivo o llave"),
                  ("cs", "SEX, EDA, NIV, EST_DIS, UPM_DIS (2013, 2015); llave", "eje, diseno o llave")],
    "universo": "Persona elegida 18+ con fila en CB1 y FAC>0 (2013 y 2015: ademas estrato y UPM no vacios); universo "
                "de cada conducta en la spec humana §2.",
    "filtros": "Un eje a la vez (TOTAL, SEXO, EDAD, ESCOLARIDAD); nunca cruces.",
    "ponderador": "FAC (CB1)",
    "transformacion": "Por texto: spec humana §0-§2 (cuestionarios 2011 y 2013, FD 2015).",
    "estimando": "Pisos por segmento ENPECYT 2011-2015 de 10 proporciones de actitudes hacia la ciencia con IC de "
                 "diseno (2013, 2015; 2011 sin IC), tau2 e IC calibrado de persistencia sobre 2015.",
    "parametros": {"olas": ["2011", "2013", "2015"], "piso": "2015"},
    "dependencias": ["numpy", "pandas"],
    "firmas": FIRMAS,
}



def genera(clave):
    c = CONF[clave]
    m = _medidor(c["calc"])
    shas = _manifiesto_sha(list(c["payloads"]))
    doc = {
        "calc_id": c["calc"],
        "spec_md": "../../../" + c["spec_md"],
        "spec_md_sha256": _sha(c["spec_md"]),
        "script": f"data/corrida0/{c['calc']}/medidor.py",
        "dependencias_materiales": c["dependencias"],
        "etiquetas": {
            "generacion": "GEN2",
            "uso_motor": "NO-ADOPTA-NADA",
            "cuenta_gen2": "SI",
            "adopta": "NO",
            "cuenta_gen2_nota": f"CONTADOR del encargo {ACTO} (cuenta_gen2: SI, adopta: NO)",
            "fuente_acto": ACTO,
            "tipo": "PISO-POR-SEGMENTO-DESDE-MICRODATO",
            "agrupacion": "UNA-SOLA-VARIABLE",
            "marca": "DESCRIPTIVO -- pisos por segmento; nada se evalua contra R en este CALC",
            "firmas": c["firmas"],
            **c["extra_etiquetas"],
        },
        "inputs": [{"id": pid, "origen": "manifiesto", "sha256": shas[pid], "funcion": "DATO", "nota": nota}
                   for pid, nota in c["payloads"].items()]
        + [{"id": "receta_pisos", "origen": "repo", "ruta": RECETA, "sha256": _sha(RECETA), "funcion": "CODIGO",
            "nota": "receta comun de ACTO GEN2-SALUD-Y-BIENESTAR-PISOS-1 (lee_csv_zip/lee_dta, marginales, "
                    "bootstrap, resumen, persistencia, ic_calibrado) ejecutada desde estos bytes, sin editar"}],
        "variables": [{"archivo": a, "variable": v, "rol": r} for a, v, r in c["variables"]],
        "universo": c["universo"],
        "filtros": c["filtros"],
        "ponderador": c["ponderador"],
        "transformacion": c["transformacion"],
        "estimando": c["estimando"],
        "seed": c.get("seed", {"aplica": True, "valor": 20260925, "rng": "numpy.PCG64"}),
        "parametros": c["parametros"] if c.get("registro") else
        {"bootstrap_replicas": 1000,
         "metodo_ic": "bootstrap UPM con reposicion dentro de estrato; singleton de certeza; "
                      "percentiles 2.5/97.5; bloques de 50; contrato conservador",
         **c["parametros"]},
        "tolerancia": {"tipo": "flotante", "abs": 1.0e-10,
                       "razon": ("registro completo: conteos y sumas float64 deterministas" if c.get("registro")
                                 else "bootstrap determinista por semilla; mismo payload y sumas float64")},
        "resultados": m.esquema_resultados(),
    }
    cab = (f"# {c['calc']} -- contrato ejecutable de la spec humana (D-15). COMMIT-1, antes de abrir microdato.\n"
           "# El primer resultado que produzca este procedimiento es el que se reporta.\n")
    out = ROOT / "data/corrida0" / c["calc"] / "spec.yaml"
    out.write_text(cab + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    print(f"{out.relative_to(ROOT)}: {len(doc['resultados'])} resultados")


if __name__ == "__main__":
    genera(sys.argv[1])
