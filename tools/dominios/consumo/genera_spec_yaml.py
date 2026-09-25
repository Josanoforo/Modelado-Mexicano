#!/usr/bin/env python3
"""Genera el `spec.yaml` (D-15) de los dos CALC de ACTO GEN2-CONSUMO-Y-GASTO-PISOS-1.

Uso: python3 tools/dominios/consumo/genera_spec_yaml.py {ENIGH|ENGASTO}

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
ACTO = "GEN2-CONSUMO-Y-GASTO-PISOS-1"


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


CONF = {
    "ENIGH": {
        "calc": "CALC-ENIGH-CONSUMO-PISOS-0001",
        "spec_md": "forense/prereg-caja/CONSUMO-ENIGH-PISOS-spec-v1_0.md",
        "payloads": {f"enigh{o}_nc_csv": f"ENIGH {o} nueva serie, CSV (concentradohogar, hogares, gastoshogar)"
                     for o in ("2016", "2018", "2020", "2022")},
        "extra_etiquetas": {"unidad_transferencia": "HOGAR",
                            "olas": "2016, 2018, 2020, 2022 abiertas; 2024 RESERVADA (E.6), no es input",
                            "cita_sin_remedir": "CALC-ENIGH{2016,2018,2020,2022}-REMESAS-CONTEXTO-0001, "
                                                "-INTENSIDAD-REMESAS-0001"},
        "variables": [("concentradohogar", c, "reactivo, eje o diseno") for c in
                      ["folioviv", "foliohog", "tam_loc", "est_dis", "upm", "factor", "sexo_jefe", "edad_jefe",
                       "educa_jefe", "ing_cor", "gasto_mon", "alimentos", "vesti_calz", "vivienda", "limpieza",
                       "salud", "transporte", "educa_espa", "personales", "transf_gas", "ali_fuera", "bebidas",
                       "comunica", "prestamos", "pago_tarje", "deudas"]]
                     + [("hogares", c, "reactivo o llave") for c in
                        ["folioviv", "foliohog", "celular", "conex_inte", "tarjeta", "pagotarjet"]]
                     + [("gastoshogar", c, "reactivo o llave") for c in
                        ["folioviv", "foliohog", "clave", "tipo_gasto", "forma_pag1", "forma_pag2", "forma_pag3",
                         "lugar_comp", "gasto_tri"]],
        "universo": "Hogares de CONCENTRADOHOGAR con factor>0, est_dis y upm no vacios; partidas G1 de "
                    "GASTOSHOGAR agregadas por folioviv+foliohog; universo de cada conducta en "
                    "lista-cerrada-P1 §2.",
        "filtros": "Un eje a la vez (TOTAL, SEXO-JEFE, EDAD-JEFE, ESCOLARIDAD-JEFE, TLOC, DECIL; ENTIDAD solo "
                   "en 5 conductas); nunca cruces.",
        "ponderador": "factor (hogar); PART-* con peso factor*denominador e y=num/den (razon de totales)",
        "transformacion": "Por texto: lista-cerrada-P1 §2 y §5; spec §1-§3.",
        "estimando": "Pisos por segmento ENIGH 2016-2022 de 35 conductas de consumo y gasto (20 participaciones, "
                     "14 proporciones de hogares, 1 media) con IC de diseno; IC calibrado de persistencia sobre "
                     "el piso 2022 para PART-* y HOG-*.",
        "parametros": {"ola_piso": "2022", "olas": ["2016", "2018", "2020", "2022"]},
    },
    "ENGASTO": {
        "calc": "CALC-ENGASTO-CONSUMO-PISOS-0001",
        "spec_md": "forense/prereg-caja/CONSUMO-ENGASTO-PISOS-spec-v1_0.md",
        "payloads": {
            "engasto2012_hogar_dta": "ENGASTO 2012 HOGAR (161 campos, casa con engasto12_fd.pdf)",
            "engasto_2012_vivienda_dta": "ENGASTO 2012 VIVIENDA (diseno)",
            "engasto_2012_lugar_compra_dta": "ENGASTO 2012 LUGAR_COMPRA",
            "engasto2012_gasto_de_consumo_ajustado_dta": "ENGASTO 2012 GASTO_DE_CONSUMO_AJUSTADO (jefe)",
        },
        "extra_etiquetas": {"unidad_transferencia": "HOGAR",
                            "olas": "2012 abierta; 2013 (carpeta engasto2013/) RESERVADA (E.6), no es input"},
        "variables": [("hogar", c, "reactivo, llave o ponderador") for c in
                      ["anio_reg", "trimestre", "folio", "hog_ent_1", "hog_ent_2", "num_cel", "conex_inte",
                       "factor_hog"]]
                     + [("vivienda", c, "llave, eje o diseno") for c in
                        ["anio_reg", "trimestre", "folio", "tam_loc", "est_dis", "upm"]]
                     + [("lugar_compra", "lc_* (76 campos, lista en el medidor)", "reactivo")]
                     + [("gasto_de_consumo_ajustado", c, "eje o llave") for c in ["sexo_je", "edad_je", "ned_je"]],
        "universo": "Hogares de HOGAR con factor_hog>0, est_dis y upm (VIVIENDA) no vacios; universo de cada "
                    "conducta en lista-cerrada-P1 §3.",
        "filtros": "Un eje a la vez (TOTAL, SEXO-JEFE, EDAD-JEFE, ESCOLARIDAD-JEFE, TLOC); nunca cruces.",
        "ponderador": "factor_hog",
        "transformacion": "Por texto: lista-cerrada-P1 §3 y §5; spec §1-§3.",
        "estimando": "Pisos por segmento ENGASTO 2012 de 22 proporciones de hogares (lugar de compra, compra "
                     "por internet, celular, internet) con IC de diseno; sin persistencia (una ola abierta).",
        "parametros": {"ola": "2012"},
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
        "dependencias_materiales": ["numpy", "pandas", "pyreadstat"] if clave == "ENGASTO" else ["numpy", "pandas"],
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
            "firmas": "F-ASTRA-5-4, regla 6, E.6, §3 v2.16 (oferta antes que preferencia) (encargo §2, verbatim)",
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
