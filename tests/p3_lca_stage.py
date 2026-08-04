#!/usr/bin/env python3
"""Ejecutor por etapas de tests/p3_lca_run.py -- mismo pipeline, partido en
llamadas independientes para correr bajo limites de tiempo por invocacion.
Cada etapa escribe su propio checkpoint JSON en forense/notas/_p3_lca/
(directorio de trabajo, no todo se conserva en el entregable final --
`assemble` consolida). Uso:

  python3 tests/p3_lca_stage.py principal
  python3 tests/p3_lca_stage.py s4
  python3 tests/p3_lca_stage.py s1
  python3 tests/p3_lca_stage.py s2
  python3 tests/p3_lca_stage.py s3
  python3 tests/p3_lca_stage.py e2
  python3 tests/p3_lca_stage.py assemble
"""
import json
import os
import sys
import time

sys.path.insert(0, "tests")
import p3_lca_data as D
import p3_lca_em as E
import p3_lca_run as R

OUT_DIR = R.OUT_DIR
CK = lambda name: os.path.join(OUT_DIR, f"ck_{name}.json")


def limpiar_tabla(tabla):
    out = {}
    for k, d in tabla.items():
        dd = dict(d)
        dd.pop("_resultado_crudo", None)
        out[str(k)] = dd
    return out


def guardar(nombre, obj):
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(CK(nombre), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print(f"[checkpoint] {CK(nombre)} escrito.")


def cargar(nombre):
    with open(CK(nombre), encoding="utf-8") as f:
        return json.load(f)


def existe(nombre):
    return os.path.exists(CK(nombre))


def cargar_universo_cache():
    t0 = time.time()
    universo, meta = D.cargar_universo()
    print(f"universo cargado: n={len(universo)} en {time.time()-t0:.1f}s")
    return universo, meta


def stage_universo_meta(universo, meta):
    n18 = len(universo)
    faltantes = {}
    for campo in R.CAMPOS_MAIN:
        n_falt = sum(1 for r in universo if r[campo] is None)
        faltantes[campo] = {"n_faltante": n_falt, "prop_faltante": n_falt / n18}

    hogares_vistos = set()
    pares = []
    for r in universo:
        hk = (r["folioviv"], r["foliohog"])
        if hk in hogares_vistos:
            continue
        hogares_vistos.add(hk)
        if r["ing_cor_hogar"] is not None and r["est_socio_raw"] is not None:
            pares.append((r["ing_cor_hogar"], int(r["est_socio_raw"])))
    pares_ordenados = sorted(pares)
    violaciones = sum(1 for i in range(1, len(pares_ordenados))
                       if pares_ordenados[i][1] < pares_ordenados[i - 1][1])
    rangos = {}
    for ing, es in pares:
        lo, hi = rangos.get(es, (ing, ing))
        rangos[es] = (min(lo, ing), max(hi, ing))

    out = {
        "n_universo_18mas": n18,
        "meta_carga": meta,
        "faltantes_por_indicador": faltantes,
        "est_socio_vs_ing_cor": {
            "n_hogares": len(pares),
            "violaciones_monotonicidad_adyacente": violaciones,
            "prop_violaciones": violaciones / max(1, len(pares_ordenados) - 1),
            "rango_ing_cor_por_est_socio": {str(k): v for k, v in sorted(rangos.items())},
            "veredicto": "NO es funcion determinista de ing_cor -- los rangos de ing_cor se "
                         "traslapan casi por completo entre las 4 categorias de est_socio y una "
                         "fraccion sustancial de pares consecutivos (ordenados por ing_cor) viola "
                         "monotonicidad",
        },
        "residencia_referencia_temporal": {
            "hallazgo": "la fuente no lo trae",
            "detalle": ("El diccionario de datos de `poblacion` (columna 46, `residencia`) solo dice "
                        "'Categorias en el catalogo de residencia', sin texto de pregunta. "
                        "`metadatos_enigh_2022_ns.txt` no menciona `residencia` en ninguna parte "
                        "(0 coincidencias grep). Ninguno de los dos archivos trae el periodo de "
                        "referencia (¿hace 5 anios? ¿al nacer?)."),
        },
        "variables_diseno": {
            "factor_persona": "factor -- vive DIRECTO en `poblacion`, a nivel persona",
            "estrato": "est_dis -- en `poblacion`",
            "upm": "upm -- en `poblacion`",
            "nota": "El hueco declarado por Sec.5.1 queda CERRADO: las tres variables de diseno "
                    "se localizaron por nombre exacto en la misma tabla que I1/I2/I3.",
        },
    }
    guardar("universo_meta", out)
    return out


def stage_principal(universo):
    cats_main, patrones_upm_main = E.construir_patrones(universo, R.CAMPOS_MAIN)
    ncats_main = E._n_categorias(cats_main)
    patrones_main = E.colapsar_sin_upm(patrones_upm_main)
    n_ef_main = sum(d["n"] for d in patrones_main.values())
    patrones_main_r, suma_cruda_main, const_main = E.reescalar_a_n_efectivo(patrones_main, n_ef_main)
    print(f"principal: patrones unicos={len(patrones_main)} n_ef={n_ef_main}")

    tabla_main = R.fit_range(patrones_main_r, ncats_main)
    decision_main = R.regla_decision(tabla_main)
    k_sel = decision_main["k_primario_tras_regla_no_separacion"]

    perfiles_vecinos = {}
    for kk in [k_sel - 1, k_sel, k_sel + 1]:
        if kk in tabla_main:
            perfiles_vecinos[kk] = {"categorias": cats_main, "campos": R.CAMPOS_MAIN,
                                     **R.perfil_completo(tabla_main[kk])}

    E1_ok = R.evaluar_E1(tabla_main, k_sel)
    E3 = R.evaluar_E3(tabla_main, k_sel)

    out = {
        "campos": R.CAMPOS_MAIN, "categorias": cats_main,
        "suma_cruda_pesos": suma_cruda_main, "n_efectivo": n_ef_main,
        "constante_reescalamiento": const_main,
        "tabla_k_1_8": limpiar_tabla(tabla_main),
        "decision_Sec3_3": decision_main,
        "k_seleccionado": k_sel,
        "perfiles_k_vecinos": perfiles_vecinos,
        "E1_replicacion_logL": E1_ok,
        "E3_sin_degeneradas": E3,
        "phi_k_sel": tabla_main[k_sel]["_resultado_crudo"]["phi"],
        "pi_k_sel": tabla_main[k_sel]["_resultado_crudo"]["pi"],
    }
    guardar("principal", out)
    return out


def stage_s4(universo):
    cats_main, patrones_upm_main = E.construir_patrones(universo, R.CAMPOS_MAIN)
    ncats_main = E._n_categorias(cats_main)
    patrones_main = E.colapsar_sin_upm(patrones_upm_main)
    patrones_sinpeso = E.patrones_sin_peso(patrones_main)
    tabla_s4 = R.fit_range(patrones_sinpeso, ncats_main, seed_base=2000)
    decision_s4 = R.regla_decision(tabla_s4)
    out = {"tabla_k_1_8": limpiar_tabla(tabla_s4), "decision_Sec3_3": decision_s4}
    guardar("s4", out)
    return out


def stage_s1(universo):
    cats_s1, patrones_upm_s1 = E.construir_patrones(universo, R.CAMPOS_S1)
    ncats_s1 = E._n_categorias(cats_s1)
    patrones_s1 = E.colapsar_sin_upm(patrones_upm_s1)
    n_ef_s1 = sum(d["n"] for d in patrones_s1.values())
    patrones_s1_r, _, _ = E.reescalar_a_n_efectivo(patrones_s1, n_ef_s1)
    tabla_s1 = R.fit_range(patrones_s1_r, ncats_s1, seed_base=3000)
    decision_s1 = R.regla_decision(tabla_s1)
    out = {"campos": R.CAMPOS_S1, "categorias": cats_s1,
           "tabla_k_1_8": limpiar_tabla(tabla_s1), "decision_Sec3_3": decision_s1}
    guardar("s1", out)
    return out


def stage_s2(universo):
    cats_s2, patrones_upm_s2 = E.construir_patrones(universo, R.CAMPOS_S2)
    ncats_s2 = E._n_categorias(cats_s2)
    patrones_s2 = E.colapsar_sin_upm(patrones_upm_s2)
    n_ef_s2 = sum(d["n"] for d in patrones_s2.values())
    patrones_s2_r, _, _ = E.reescalar_a_n_efectivo(patrones_s2, n_ef_s2)
    tabla_s2_full = R.fit_range(patrones_s2_r, ncats_s2, seed_base=4000)
    decision_s2 = R.regla_decision(tabla_s2_full)
    out = {"tabla_k_1_8": limpiar_tabla(tabla_s2_full), "decision_Sec3_3": decision_s2,
           "categorias": cats_s2,
           "phi_por_k": {str(k): tabla_s2_full[k]["_resultado_crudo"]["phi"] for k in R.K_RANGE}}
    guardar("s2", out)
    return out


def stage_s3(universo):
    cats_s3, patrones_upm_s3 = E.construir_patrones(universo, R.CAMPOS_S3)
    ncats_s3 = E._n_categorias(cats_s3)
    patrones_s3 = E.colapsar_sin_upm(patrones_upm_s3)
    n_ef_s3 = sum(d["n"] for d in patrones_s3.values())
    patrones_s3_r, _, _ = E.reescalar_a_n_efectivo(patrones_s3, n_ef_s3)
    tabla_s3 = R.fit_range(patrones_s3_r, ncats_s3, seed_base=5000)
    decision_s3 = R.regla_decision(tabla_s3)
    out = {"campos": R.CAMPOS_S3, "categorias": cats_s3,
           "tabla_k_1_8": limpiar_tabla(tabla_s3), "decision_Sec3_3": decision_s3}
    guardar("s3", out)
    return out


def stage_e2(universo):
    principal = cargar("principal")
    k_sel = principal["k_seleccionado"]
    cats_main, _ = E.construir_patrones(universo, R.CAMPOS_MAIN)
    ncats_main = E._n_categorias(cats_main)
    e2 = R.evaluar_E2(universo, R.CAMPOS_MAIN, k_sel, ncats_main, cats_main)
    phi_sel = principal["phi_k_sel"]
    perm, corrs = R.emparejar_clases(phi_sel, e2["phi_A"])
    perm2, corrs2 = R.emparejar_clases(phi_sel, e2["phi_B"])
    out = {
        "k_seleccionado": k_sel,
        "n_upms_total": e2["n_upms_total"], "n_upms_A": e2["n_upms_A"], "n_upms_B": e2["n_upms_B"],
        "n_personas_A": e2["n_personas_A"], "n_personas_B": e2["n_personas_B"],
        "phi_A": e2["phi_A"], "phi_B": e2["phi_B"], "pi_A": e2["pi_A"], "pi_B": e2["pi_B"],
        "emparejamiento_A": {"perm": list(perm), "correlaciones": corrs, "min_correlacion": min(corrs)},
        "emparejamiento_B": {"perm": list(perm2), "correlaciones": corrs2, "min_correlacion": min(corrs2)},
        "pasa_umbral_090": (min(corrs) >= 0.90) and (min(corrs2) >= 0.90),
    }
    guardar("e2", out)
    return out


def stage_assemble():
    universo_meta = cargar("universo_meta")
    principal = cargar("principal")
    s1 = cargar("s1")
    s2 = cargar("s2")
    s3 = cargar("s3")
    s4 = cargar("s4")
    e2 = cargar("e2")

    k_sel = principal["k_seleccionado"]
    k_sel_s2 = s2["decision_Sec3_3"]["k_primario_tras_regla_no_separacion"]
    cambia_k_s2 = (k_sel_s2 != k_sel)
    congruencia_s2 = None
    if not cambia_k_s2:
        phi_main_sel = principal["phi_k_sel"]
        phi_s2_sel = s2["phi_por_k"][str(k_sel)]
        perm, corrs = R.emparejar_clases(phi_main_sel, phi_s2_sel)
        congruencia_s2 = {"perm": list(perm), "correlaciones": corrs, "min_correlacion": min(corrs)}

    resultados = {
        **universo_meta,
        "principal": {
            **{kk: vv for kk, vv in principal.items() if kk != "phi_k_sel" and kk != "pi_k_sel"},
            "estabilidad_Sec3_5": {
                "E1_replicacion_logL": principal["E1_replicacion_logL"],
                "E2": e2,
                "E3_sin_degeneradas": principal["E3_sin_degeneradas"],
                "INESTABLE": (not principal["E1_replicacion_logL"]) or (not e2["pasa_umbral_090"]) or (not principal["E3_sin_degeneradas"]["pasa"]),
            },
        },
        "S1_solo_persona": s1,
        "S2_edad_alternativa": {
            "k_seleccionado_S2": k_sel_s2, "k_seleccionado_principal": k_sel,
            "cambia_k": cambia_k_s2, "congruencia_perfiles": congruencia_s2,
            "advertencia_eje_edad_inestable": cambia_k_s2 or (congruencia_s2 is not None and congruencia_s2["min_correlacion"] < 0.90),
            "tabla_k_1_8": s2["tabla_k_1_8"], "categorias": s2["categorias"],
        },
        "S3_formalidad_trabajos": s3,
        "S4_sin_pesos": {
            **s4,
            "k_seleccionado_sin_pesos": s4["decision_Sec3_3"]["k_primario_tras_regla_no_separacion"],
            "k_seleccionado_ponderado": k_sel,
            "cambia_seleccion": s4["decision_Sec3_3"]["k_primario_tras_regla_no_separacion"] != k_sel,
        },
    }
    with open(R.OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"=== ENSAMBLADO en {R.OUT_PATH} ===")
    print("k_seleccionado principal:", k_sel)
    print("INESTABLE:", resultados["principal"]["estabilidad_Sec3_5"]["INESTABLE"])
    print("S1 k_seleccionado:", s1["decision_Sec3_3"]["k_primario_tras_regla_no_separacion"])
    print("S2 cambia_k:", cambia_k_s2, "advertencia:", resultados["S2_edad_alternativa"]["advertencia_eje_edad_inestable"])
    print("S3 k_seleccionado:", s3["decision_Sec3_3"]["k_primario_tras_regla_no_separacion"])
    print("S4 cambia_seleccion:", resultados["S4_sin_pesos"]["cambia_seleccion"])
    return resultados


STAGES_NEED_UNIVERSO = {"universo_meta", "principal", "s4", "s1", "s2", "s3", "e2"}

if __name__ == "__main__":
    stage = sys.argv[1]
    t0 = time.time()
    if stage in STAGES_NEED_UNIVERSO:
        universo, meta = cargar_universo_cache()
    if stage == "universo_meta":
        stage_universo_meta(universo, meta)
    elif stage == "principal":
        stage_principal(universo)
    elif stage == "s4":
        stage_s4(universo)
    elif stage == "s1":
        stage_s1(universo)
    elif stage == "s2":
        stage_s2(universo)
    elif stage == "s3":
        stage_s3(universo)
    elif stage == "e2":
        stage_e2(universo)
    elif stage == "assemble":
        stage_assemble()
    else:
        print("etapa desconocida:", stage)
        sys.exit(1)
    print(f"[{stage}] terminado en {time.time()-t0:.1f}s")
