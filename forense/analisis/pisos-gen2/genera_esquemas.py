#!/usr/bin/env python3
"""Escribe los cuatro `spec.yaml` de ACTO GEN2-PISOS-GEN2-2 (P2/P3), COMMIT-1.

Los campos se declaran aquí, antes de abrir ENIF 2024 / ENVIPE 2025. El bloque
`resultados:` sale de una corrida SINTÉTICA de cada medidor (payloads fabricados de
`tests/test_pisos_gen2_2.py`), nunca del dato: para los -0002 cada id heredado conserva
la fila (tipo, unidad, `permite_no_estimable`) del `spec.yaml` sellado del -0001,
renombrada; los ids nuevos se tipan por regla declarada abajo.

Uso:  python3 forense/analisis/pisos-gen2/genera_esquemas.py [--sha-piso]
      --sha-piso  (COMMIT-3a) sólo rellena el sha256 de `piso_c2_resultados` y
                  `piso_c2_sello` en los dos -0002 desde los pisos sellados.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import sys
import tempfile
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[3]
C0 = RAIZ / "data" / "corrida0"
PRE = RAIZ / "forense" / "prereg-caja"
CABECERA = "# El primer resultado que produzca este procedimiento es el que se reporta.\n"
ENCARGO = "forense/encargos/2026-09-24-GEN2-PISOS-GEN2-2.md"
FIRMAS = ("Decision 1 de ADOPCION-2 (mesa 24/sep/2026) extendida a todas las celdas-D por el encargo "
          "GEN2-PISOS-GEN2-2 §2 (INTERPRETACION-DECLARADA); E.1; firma 17/sep; regla 6")
SIN_SHA = "PENDIENTE-COMMIT-3a"


def _sha(ruta):
    return hashlib.sha256((RAIZ / ruta).read_bytes()).hexdigest()


def _repo(iid, ruta, funcion, nota, sha=None):
    return {"id": iid, "origen": "repo", "ruta": ruta,
            "sha256": sha if sha is not None else _sha(ruta), "funcion": funcion, "nota": nota}


def _spec_md(nombre):
    ruta = PRE / nombre
    return {"spec_md": f"../../../forense/prereg-caja/{nombre}",
            "spec_md_sha256": hashlib.sha256(ruta.read_bytes()).hexdigest()}


def _etiquetas(tipo, unidad, fuente_extra):
    e = {"generacion": "GEN2", "unidad_transferencia": unidad, "uso_motor": "NO-ADOPTA-NADA",
         "cuenta_gen2": "SI",
         "cuenta_gen2_nota": f"CONTADOR del encargo GEN2-PISOS-GEN2-2 (cuenta_gen2: SI, adopta: NO) -- {ENCARGO}:6",
         "fuente_acto": "GEN2-PISOS-GEN2-2", "tipo": tipo, "firmas": FIRMAS}
    e.update(fuente_extra)
    return e


# ══ los dos pisos ═════════════════════════════════════════════════════════════

def spec_piso_din():
    E = "data/corrida0/CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001"
    A = "data/corrida0/CALC-ARBITRO-MARGINALES-ENIF2024-0001"
    par_e = yaml.safe_load((RAIZ / E / "spec.yaml").read_text(encoding="utf-8"))["parametros"]
    return {
        "calc_id": "CALC-ENIF2024-PISOS-AHORRO-INFORMAL-LXE-0001",
        **_spec_md("ENIF2024-PISOS-AHORRO-INFORMAL-LXE-spec-v1_0.md"),
        "script": "data/corrida0/CALC-ENIF2024-PISOS-AHORRO-INFORMAL-LXE-0001/medidor.py",
        "dependencias_materiales": ["numpy", "pandas"],
        "etiquetas": _etiquetas("PISO-C2-COMPUESTO-DESDE-MICRODATO", "PERSONA-ELEGIDA-18MAS", {
            "agrupacion": "UNA-SOLA-VARIABLE",
            "marca": "RETROSPECTIVA -- sellado despues de que el -0001 derivo R (cruce visto, E.6); formula fija, no lee R",
            "relevo_de": "el -C2-P de CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001 (parametros.marginales_sellados_D9 -> milpa/)",
            "celda_d": "DIN.ahorro_solo_informal.enif2024.localidad_x_edad"}),
        "inputs": [
            {"id": "enif2024_csv", "origen": "manifiesto",
             "sha256": "a3507b4038888247f565f1640a718ef552bb8fc363378e3372a5bf2796bb2e4c",
             "funcion": "DATO", "nota": "ENIF 2024; se agrupa SOLO por una variable (marginales), nunca el cruce"},
            _repo("medidor_emisiones", f"{E}/medidor.py", "CODIGO",
                  "_lee_miembro, _universo, _desenlaces, _replicas, _agrega_por_upm, _punto_e_ic, _matriz y DESENLACE_D9 ejecutados desde estos bytes"),
            _repo("funcion_c2", "tests/test_celda_d_c2.py", "CODIGO", "piso_log_aditivo (el mismo objeto que usaron las emisiones)"),
            _repo("extrae_l", "tools/extrae_l_v1_1.py", "CODIGO", "dependencia de import del medidor de las emisiones; no se llama"),
            _repo("emisiones_resultados", f"{E}/resultados.json", "CONTROL-HISTORICO",
                  "control 1 (oro a 1e-10: marginales, C2-P-REDERIVADO, C2-IC) y control 3 (C2 legacy, descriptivo); no es insumo del piso"),
            _repo("emisiones_sello", f"{E}/sello.json", "METADATO", "el sha de emisiones_resultados debe estar en este sello"),
            _repo("arbitro_enif2024_resultados", f"{A}/resultados.json", "CONTROL-HISTORICO",
                  "control 2: E1-E3 a 1e-10 y -N exacto; L1, L2, E4 y NAC descriptivos (universo propio, spec §3)"),
            _repo("arbitro_enif2024_sello", f"{A}/sello.json", "METADATO", "el sha de arbitro_enif2024_resultados debe estar en este sello"),
        ],
        "variables": [{"archivo": "conjunto_de_datos_tmodulo_enif2024.csv", "variable": v, "rol": r}
                      for v, r in ([(c, "ahorro-informal") for c in par_e["codigos_informal_2024"]]
                                   + [(c, "via-formal-D9") for c in par_e["codigos_formal_D9_2024"]]
                                   + [("tloc", "eje-localidad"), ("edad_v", "eje-edad"), ("fac_per", "ponderador"),
                                      ("est_dis", "estrato"), ("upm_dis", "upm")])],
        "universo": ("Identico al de las emisiones (DIN-ahorro-solo-informal-lxe8-spec-v1_2 §3.1): personas elegidas de 18 "
                     "anos y mas de TMODULO ENIF 2024 con 18 <= edad_v <= 97 (sin 98/99), tloc en {1,2,3,4}, fac_per > 0; "
                     "los siete grupos comparten ese universo."),
        "filtros": "Los tres de las emisiones, en el mismo orden, ejecutados desde sus bytes (_universo).",
        "ponderador": "fac_per",
        "transformacion": ("D9 = alguna via informal (p5_1_1..6 = 1) y ninguna de las nueve formales (p5_6_1..9 = 1). "
                           "L1 = tloc {3,4}; L2 = tloc {1,2}; E1..E4 = 18-29/30-44/45-59/60-97; NAC = todos."),
        "estimando": ("C2(l,e) = expit(logit p24(l) + logit p24(e) - logit p24) en las 8 celdas localidad x edad; "
                      "marginales de un eje de ENIF 2024; IC 2.5/97.5 de la composicion replica a replica."),
        "seed": {"aplica": True, "valor": 42, "rng": "numpy.random.PCG64"},
        "tolerancia": {"tipo": "bootstrap", "exacto_por_seed": True, "abs": 1.0e-10,
                       "razon": "misma semilla, mismo generador y mismo orden de consumo que las emisiones"},
        "parametros": {
            "bootstrap_replicas": 10000,
            "codigos_informal_2024": par_e["codigos_informal_2024"],
            "codigos_formal_D9_2024": par_e["codigos_formal_D9_2024"],
            "localidad_L1_tloc": par_e["localidad_L1_tloc"],
            "localidad_L2_tloc": par_e["localidad_L2_tloc"],
            "edad_tramos": par_e["edad_tramos"],
            "tol_control_emisiones": 1.0e-10,
            "tol_control_arbitro": 1.0e-10,
            "control_arbitro_mismo_universo": ["E1", "E2", "E3"],
        },
    }


def spec_piso_tra():
    E = "data/corrida0/CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001"
    A = "data/corrida0/CALC-ARBITRO-MARGINALES-ENVIPE2025-0001"
    par_e = yaml.safe_load((RAIZ / E / "spec.yaml").read_text(encoding="utf-8"))["parametros"]
    return {
        "calc_id": "CALC-ENVIPE2025-PISOS-EVADE-NORMA-SXD-0001",
        **_spec_md("ENVIPE2025-PISOS-EVADE-NORMA-SXD-spec-v1_0.md"),
        "script": "data/corrida0/CALC-ENVIPE2025-PISOS-EVADE-NORMA-SXD-0001/medidor.py",
        "dependencias_materiales": ["numpy", "pandas"],
        "etiquetas": _etiquetas("PISO-C2-COMPUESTO-DESDE-MICRODATO", "DELITO", {
            "agrupacion": "UNA-SOLA-VARIABLE (ola cargada reservada=True: el cruce lanza ReservaRota)",
            "marca": "RETROSPECTIVA -- sellado despues de que el -0001 derivo R (cruce visto, E.6); formula fija, no lee R",
            "relevo_de": "el -C2-P de CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001 (parametros.marginales_sellados -> milpa/)",
            "celda_d": "TRA.evade_norma.envipe2025.escolaridad_x_dominio"}),
        "inputs": [
            {"id": "envipe2025_csv", "origen": "manifiesto",
             "sha256": "8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa",
             "funcion": "DATO", "nota": "ENVIPE 2025; SOLO marginales de un eje"},
            _repo("receta_marginales", "tools/celda_d/marginales_reproduccion.py", "CODIGO",
                  "carga_ola, replicas_compartidas, marginal, cruce (guardia) ejecutados desde estos bytes"),
            _repo("ejes_l1", "tools/ejes_maestra35_l1.py", "CODIGO", "construccion de ejes del arbitro, importada por la receta"),
            _repo("calibracion_ic", "tools/calibracion_mordida_encig_serie.py", "CODIGO", "wprop_ic_conglomerado, importada por la receta"),
            _repo("funcion_c2", "tests/test_celda_d_c2.py", "CODIGO", "piso_log_aditivo (el mismo objeto que usaron las emisiones)"),
            _repo("emisiones_resultados", f"{E}/resultados.json", "CONTROL-HISTORICO",
                  "control 1 (oro a 1e-10: M25 marginales, C2-P-REDERIVADO, C2-IC) y control 3 (C2 legacy, descriptivo); no es insumo del piso"),
            _repo("emisiones_sello", f"{E}/sello.json", "METADATO", "el sha de emisiones_resultados debe estar en este sello"),
            _repo("arbitro_envipe2025_resultados", f"{A}/resultados.json", "CONTROL-HISTORICO",
                  "control 2: los 8 marginales -P a 1e-10 y -N exacto"),
            _repo("arbitro_envipe2025_sello", f"{A}/sello.json", "METADATO", "el sha de arbitro_envipe2025_resultados debe estar en este sello"),
        ],
        "variables": [
            {"archivo": "conjunto_de_datos_tmod_vic_envipe2025.csv", "variable": v, "rol": r}
            for v, r in (("BP1_20", "universo-y-desenlace"), ("BP1_23", "desenlace"), ("FAC_DEL", "ponderador"),
                         ("EST_DIS", "estrato"), ("UPM_DIS", "upm"), ("ID_PER", "llave-delito-persona"),
                         ("DOMINIO", "eje-dominio"))] + [
            {"archivo": "conjunto_de_datos_tsdem_envipe2025.csv", "variable": "ID_PER", "rol": "llave-persona"},
            {"archivo": "conjunto_de_datos_tsdem_envipe2025.csv", "variable": "NIV", "rol": "eje-escolaridad-proxy"}],
        "universo": "DELITOS de tmod_vic ENVIPE 2025 con BP1_20 in {1,2} (el de las emisiones y el arbitro); cada eje sobre su denominador valido.",
        "filtros": "Los de mr.carga_ola (FAC_DEL > 0, EST_DIS/UPM_DIS no vacios, ID_PER unica en tsdem), ejecutados desde sus bytes.",
        "ponderador": "FAC_DEL",
        "transformacion": "evade_norma = BP1_20 == 2 y BP1_23 in {04,05,06,08}; S1..S4 escolaridad_proxy (NIV), D1..D3 = Rural/Complemento urbano/Urbano.",
        "estimando": ("C2(s,d) = expit(logit p25(s) + logit p25(d) - logit p25) en las 12 celdas escolaridad x dominio; "
                      "marginales de un eje de ENVIPE 2025; IC 2.5/97.5 de la composicion replica a replica."),
        "seed": {"aplica": True, "valor": 42,
                 "rng": "numpy.random.PCG64 (replicas compartidas) + numpy.random.default_rng (wprop_ic_conglomerado)"},
        "tolerancia": {"tipo": "bootstrap", "exacto_por_seed": True, "abs": 1.0e-10,
                       "razon": "misma semilla y mismo modulo congelado que las emisiones"},
        "parametros": {
            "bootstrap_replicas": 10000,
            "c2_desenlace_id": par_e["c2_desenlace_id"],
            "tol_control_emisiones": 1.0e-10,
            "tol_control_arbitro": 1.0e-10,
        },
    }


# ══ los dos -0002 ═════════════════════════════════════════════════════════════

def _spec_adj2(a1_dir, calc_id, md, piso_calc, extras_inputs, celda_d, unidad):
    s1 = yaml.safe_load((RAIZ / a1_dir / "spec.yaml").read_text(encoding="utf-8"))
    emis = next(i for i in s1["inputs"] if i["id"] == "emisiones_selladas")
    emis_dir = str(Path(emis["ruta"]).parent)
    manif = next(i for i in s1["inputs"] if i.get("origen") == "manifiesto")
    piso_dir = f"data/corrida0/{piso_calc}"

    def _pis(f):
        ruta = RAIZ / piso_dir / f
        return _sha(f"{piso_dir}/{f}") if ruta.exists() else SIN_SHA

    s = {
        "calc_id": calc_id,
        **_spec_md(md),
        "script": f"data/corrida0/{calc_id}/medidor.py",
        "dependencias_materiales": s1.get("dependencias_materiales", ["numpy", "pandas"]),
        "etiquetas": _etiquetas("RE-ADJUDICACION-CELDA-D-PISO-DE-CADENA-LIMPIA", unidad, {
            "celda_d": celda_d,
            "sucesor_de": f"{Path(a1_dir).name} (queda SELLADA como evidencia historica; no es repite_de: la fuente de C2 cambia)",
            "hereda_por_sha": {"medidor": f"{a1_dir}/medidor.py {_sha(a1_dir + '/medidor.py')}",
                               "spec_md": f"{a1_dir}/spec.md {_sha(a1_dir + '/spec.md')}",
                               "parametros_y_seed": f"{a1_dir}/spec.yaml {_sha(a1_dir + '/spec.yaml')} (copiados verbatim)"},
            "orden_de_commits": "COMMIT-1 (specs+codigo+D22) -> COMMIT-2 piso sellado -> COMMIT-3a sha del piso -> COMMIT-3 re-adjudicacion",
            "marca": "C2 RETROSPECTIVA (piso sellado despues de R); los demas contendientes conservan su marca del -0001",
            "condicion": ("SE NIEGA A CORRER sin los sellos de emisiones, -0001 y piso (sha verificado), si el piso no "
                          "declara ORIGEN NUEVO, control de emisiones REPRODUCE e IC EMITIDO, o con un input fuera de la lista")}),
        "inputs": [
            {k: v for k, v in manif.items()},
            _repo("emisiones_selladas", emis["ruta"], "DATO",
                  "las emisiones selladas del -0001 (C1, C3, C6, C7, soporte); su -C2-P se sustituye por el del piso antes de adjudicar"),
            _repo("emisiones_sello", f"{emis_dir}/sello.json", "METADATO", "el sha de emisiones_selladas debe estar en este sello"),
            _repo("medidor_0001", f"{a1_dir}/medidor.py", "CODIGO", "el medidor del -0001, ejecutado sin editar"),
            *extras_inputs,
            _repo("adjudicacion_0001_resultados", f"{a1_dir}/resultados.json", "CONTROL-HISTORICO",
                  "oro (E.5): todo id que no depende de C2 reproduce a tol_oro_0001"),
            _repo("adjudicacion_0001_sello", f"{a1_dir}/sello.json", "METADATO", "el sha del -0001 debe estar en este sello"),
            _repo("piso_c2_resultados", f"{piso_dir}/resultados.json", "DATO",
                  "EL UNICO CAMBIO: fuente del punto C2 (por id); NO EXISTE en COMMIT-1; sha256 se fija en COMMIT-3a",
                  sha=_pis("resultados.json")),
            _repo("piso_c2_sello", f"{piso_dir}/sello.json", "METADATO",
                  "NO EXISTE en COMMIT-1; sha256 se fija en COMMIT-3a", sha=_pis("sello.json")),
        ],
        "variables": s1["variables"],
        "universo": s1["universo"],
        "filtros": s1["filtros"],
        "ponderador": s1["ponderador"],
        "transformacion": s1["transformacion"],
        "estimando": (f"Re-adjudicacion del {Path(a1_dir).name} con C2 := RESULT -C2-P (y su IC) de {piso_calc}, por id. "
                      "Todo lo demas: el estimando del -0001, verbatim: " + str(s1["estimando"])),
        "precision": s1.get("precision"),
        "seed": s1["seed"],
        "tolerancia": s1["tolerancia"],
        "parametros": {**copy.deepcopy(s1["parametros"]), "tol_oro_0001": 1.0e-10},
        "secuencia_commits": {
            "commit_2": f"corrida0 run de {piso_calc}; sello; asiento de replay; commit y push.",
            "commit_3a": "commit aparte: rellena el sha256 de piso_c2_resultados y piso_c2_sello; preflight VERDE. Ninguna otra linea cambia.",
            "commit_3": "corrida0 run de este CALC; sello; celda-D; decisiones.tsv; asientos.",
            "preflight_esperado_antes_del_commit_3a": "BLOQUEADO exactamente por los dos inputs del piso -- y por nada mas."},
    }
    return s, s1


def spec_adj2_din():
    E = "data/corrida0/CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001"
    extras = [_repo("medidor_emisiones", f"{E}/medidor.py", "CODIGO", "importado por el medidor del -0001 (motor de bootstrap)"),
              _repo("funcion_c2", "tests/test_celda_d_c2.py", "CODIGO", "importada por el medidor de las emisiones"),
              _repo("extrae_l", "tools/extrae_l_v1_1.py", "CODIGO", "importada por el medidor de las emisiones")]
    return _spec_adj2("data/corrida0/CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001",
                      "CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002",
                      "DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002-spec-v1_0.md",
                      "CALC-ENIF2024-PISOS-AHORRO-INFORMAL-LXE-0001", extras,
                      "DIN.ahorro_solo_informal.enif2024.localidad_x_edad", "PERSONA-ELEGIDA-18MAS")


def spec_adj2_tra():
    extras = [_repo("receta_marginales", "tools/celda_d/marginales_reproduccion.py", "CODIGO", "importada por el medidor del -0001 (R)"),
              _repo("ejes_l1", "tools/ejes_maestra35_l1.py", "CODIGO", "importada por la receta"),
              _repo("calibracion_ic", "tools/calibracion_mordida_encig_serie.py", "CODIGO", "importada por la receta")]
    return _spec_adj2("data/corrida0/CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001",
                      "CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002",
                      "TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002-spec-v1_0.md",
                      "CALC-ENVIPE2025-PISOS-EVADE-NORMA-SXD-0001", extras,
                      "TRA.evade_norma.envipe2025.escolaridad_x_dominio", "DELITO")


# ══ esquema desde la corrida sintética ═══════════════════════════════════════

def _fila_por_regla(k, v):
    if isinstance(v, bool) or v is None and False:
        raise AssertionError(k)
    if isinstance(v, int):
        return {"id": k, "tipo": "entero", "unidad": "conteo"}
    if isinstance(v, str):
        return {"id": k, "tipo": "texto", "unidad": "categoria / trazabilidad"}
    es_prop = any(t in k for t in ("-MARG-", "-C2-P-", "-C2-IC95", "-P-EMISION-0001-")) and "DELTA" not in k
    if es_prop:
        return {"id": k, "tipo": "proporcion", "unidad": "proporcion ponderada [0,1]", "permite_no_estimable": True}
    return {"id": k, "tipo": "flotante", "unidad": "diferencia de proporcion (con signo) o maximo absoluto",
            "permite_no_estimable": "DELTA-LEGACY" in k}


def esquema_piso(out):
    return [_fila_por_regla(k, out[k]) for k in sorted(out)]


def esquema_adj2(out, s1, p1, p2):
    previas = {r["id"]: r for r in s1["resultados"]}
    filas = []
    for k in sorted(out):
        k1 = p1 + k[len(p2):] if k.startswith(p2) else None
        if k1 in previas and not any(t in k for t in ("-C2-P-", "-C2-IC95", "-G-CTRL-ORO-", "-G-FUENTE-C2",
                                                      "-G-PISO-C2-SHA256", "-G-DICTAMEN-", "-P-EMISION-0001-")):
            f = dict(previas[k1])
            f["id"] = k
            filas.append(f)
        else:
            filas.append(_fila_por_regla(k, out[k]))
    return filas


def _escribe(calc_id, spec):
    d = C0 / calc_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "spec.yaml").write_text(CABECERA + yaml.safe_dump(spec, allow_unicode=True, sort_keys=False, width=110),
                                 encoding="utf-8")


def _test():
    s = importlib.util.spec_from_file_location("test_pisos_gen2_2", RAIZ / "tests" / "test_pisos_gen2_2.py")
    m = importlib.util.module_from_spec(s)
    sys.modules["test_pisos_gen2_2"] = m
    s.loader.exec_module(m)
    return m


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--sha-piso", action="store_true")
    a = ap.parse_args(argv)
    if a.sha_piso:
        for calc_id, gen in (("CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002", spec_adj2_din),
                             ("CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002", spec_adj2_tra)):
            ruta = C0 / calc_id / "spec.yaml"
            texto = ruta.read_text(encoding="utf-8")
            nuevo, _s1 = gen()
            for i in nuevo["inputs"]:
                if i["id"] in ("piso_c2_resultados", "piso_c2_sello"):
                    assert i["sha256"] != SIN_SHA, f"{calc_id}: piso sin sellar"
                    marca = f"  sha256: {SIN_SHA}\n  funcion: {i['funcion']}\n  nota: {i['nota'][:20]}"
                    assert texto.count(marca) == 1, (calc_id, i["id"])
                    texto = texto.replace(marca, f"  sha256: {i['sha256']}\n  funcion: {i['funcion']}\n  nota: {i['nota'][:20]}", 1)
            ruta.write_text(texto, encoding="utf-8")
            print(f"{calc_id}: sha256 del piso escrito")
        return 0

    # 1) specs sin esquema (el medidor lee sólo `parametros` y `seed`)
    specs = {"CALC-ENIF2024-PISOS-AHORRO-INFORMAL-LXE-0001": spec_piso_din(),
             "CALC-ENVIPE2025-PISOS-EVADE-NORMA-SXD-0001": spec_piso_tra()}
    adj2 = {"CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002": spec_adj2_din(),
            "CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002": spec_adj2_tra()}
    for k, v in specs.items():
        _escribe(k, {**v, "resultados": []})
    for k, (v, _s1) in adj2.items():
        _escribe(k, {**v, "resultados": []})

    # 2) corrida sintética -> esquema
    T = _test()
    with tempfile.TemporaryDirectory() as tmp:
        din = T.cadena_din(tmp)
        tra = T.cadena_tra(tmp)
        o_din = din["ADJ2"].medir(din["inp2"], din["ctr2"])
        o_tra = tra["ADJ2"].medir(tra["inp2"], tra["ctr2"])
    _escribe("CALC-ENIF2024-PISOS-AHORRO-INFORMAL-LXE-0001",
             {**specs["CALC-ENIF2024-PISOS-AHORRO-INFORMAL-LXE-0001"], "resultados": esquema_piso(din["piso"])})
    _escribe("CALC-ENVIPE2025-PISOS-EVADE-NORMA-SXD-0001",
             {**specs["CALC-ENVIPE2025-PISOS-EVADE-NORMA-SXD-0001"], "resultados": esquema_piso(tra["piso"])})
    s, s1 = adj2["CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002"]
    _escribe("CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002",
             {**s, "resultados": esquema_adj2(o_din, s1, "RESULT-DIN-LXE8-ARB", "RESULT-DIN-LXE8-ARB2")})
    s, s1 = adj2["CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002"]
    _escribe("CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002",
             {**s, "resultados": esquema_adj2(o_tra, s1, "RESULT-TRA-SXD12-ARB", "RESULT-TRA-SXD12-ARB2")})
    print("piso DIN", len(din["piso"]), "· piso TRA", len(tra["piso"]),
          "· -0002 DIN", len(o_din), "· -0002 TRA", len(o_tra))
    return 0


if __name__ == "__main__":
    sys.exit(main())
