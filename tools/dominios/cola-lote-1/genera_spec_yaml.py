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
        "seed": {"aplica": True, "valor": 20260925, "rng": "numpy.PCG64"},
        "parametros": {"bootstrap_replicas": 1000,
                       "metodo_ic": "bootstrap UPM con reposicion dentro de estrato; singleton de certeza; "
                                    "percentiles 2.5/97.5; bloques de 50; contrato conservador",
                       **c["parametros"]},
        "tolerancia": {"tipo": "flotante", "abs": 1.0e-10,
                       "razon": "bootstrap determinista por semilla; mismo payload y sumas float64"},
        "resultados": m.esquema_resultados(),
    }
    cab = (f"# {c['calc']} -- contrato ejecutable de la spec humana (D-15). COMMIT-1, antes de abrir microdato.\n"
           "# El primer resultado que produzca este procedimiento es el que se reporta.\n")
    out = ROOT / "data/corrida0" / c["calc"] / "spec.yaml"
    out.write_text(cab + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    print(f"{out.relative_to(ROOT)}: {len(doc['resultados'])} resultados")


if __name__ == "__main__":
    genera(sys.argv[1])
