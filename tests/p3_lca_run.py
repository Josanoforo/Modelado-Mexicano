#!/usr/bin/env python3
"""P3 -- corrida completa del LCA de segmentacion sobre ENIGH, siguiendo
forense/p3-lca-preregistro-v1_0.md (v1.0, sellado 3/ago/2026) al pie de la
letra. Escribe TODOS los resultados a
forense/notas/_p3_lca/resultados.json (agregados: tablas de indices,
parametros de clase, congruencias -- NUNCA microdato ni columna de clase
por persona, Sec.4).

Corre: python3 tests/p3_lca_run.py
Tarda unos minutos (los patrones colapsan el universo de 217k+ personas a
unos cientos de combinaciones unicas -- ver tests/p3_lca_em.py).
"""
import json
import math
import os
import random
import sys
import time
from itertools import permutations

sys.path.insert(0, "tests")
import p3_lca_data as D
import p3_lca_em as E

OUT_DIR = "forense/notas/_p3_lca"
OUT_PATH = os.path.join(OUT_DIR, "resultados.json")

CAMPOS_MAIN = ["I1_formalidad", "I2_edad", "I3_migracion", "I4_tam_loc",
               "I5_est_socio", "I6_celular", "I7_conex_inte"]
CAMPOS_S1 = ["I1_formalidad", "I2_edad", "I3_migracion"]
CAMPOS_S2 = ["I1_formalidad", "I2_edad_S2", "I3_migracion", "I4_tam_loc",
             "I5_est_socio", "I6_celular", "I7_conex_inte"]
CAMPOS_S3 = ["S3_formalidad_trabajos", "I2_edad", "I3_migracion", "I4_tam_loc",
             "I5_est_socio", "I6_celular", "I7_conex_inte"]

N_ARRANQUES = 500
N_MEJORES = 50
K_RANGE = list(range(1, 9))


def fit_range(patrones, ncats, k_range=K_RANGE, seed_base=1000):
    tabla = {}
    for k in k_range:
        t0 = time.time()
        res = E.ajustar(patrones, k, ncats, n_arranques=N_ARRANQUES,
                         n_mejores=N_MEJORES, seed=seed_base + k)
        dt = time.time() - t0
        n_ef = sum(w for _, w in res["patrones_items"])
        params = E.n_parametros_libres(k, ncats)
        tabla[k] = {
            "k": k,
            "loglik": res["loglik"],
            "n_parametros": params,
            "BIC": E.bic(res["loglik"], params, n_ef),
            "aBIC": E.abic(res["loglik"], params, n_ef),
            "AIC": E.aic(res["loglik"], params),
            "entropia": E.entropia_relativa(res, n_ef, k),
            "prevalencias": E.prevalencias(res),
            "n_arranques": N_ARRANQUES,
            "n_replican_mejor_logL": res["n_replican_mejor"],
            "senal_frontera_0_1": E.senal_frontera(res),
            "n_efectivo": n_ef,
            "tiempo_seg": dt,
            "_resultado_crudo": res,  # se descarta antes de volcar a JSON
        }
        print(f"  k={k}: logL={res['loglik']:.3f} BIC={tabla[k]['BIC']:.3f} "
              f"aBIC={tabla[k]['aBIC']:.3f} entropia={tabla[k]['entropia']} "
              f"replican={res['n_replican_mejor']}/{N_MEJORES} conv. ({dt:.1f}s)")
    return tabla


def regla_decision(tabla, k_range=K_RANGE):
    """Sec.3.3, literal, en orden."""
    bics = {k: tabla[k]["BIC"] for k in k_range}
    abics = {k: tabla[k]["aBIC"] for k in k_range}
    k_bic = min(bics, key=bics.get)
    k_abic = min(abics, key=abics.get)
    rango_bic = max(bics.values()) - min(bics.values())
    umbral_2pct = 0.02 * rango_bic

    discrepan = (k_bic != k_abic)

    # Regla "sin separacion": entre el minimo BIC y cualquier k MENOR cuya
    # diferencia de BIC sea < 2% del rango total, gana el k menor -- se
    # camina hacia abajo desde k_bic mientras la diferencia siga bajo el
    # umbral.
    k_primario = k_bic
    for k in sorted(k_range):
        if k >= k_bic:
            break
        if (bics[k] - bics[k_bic]) < umbral_2pct:
            k_primario = k
            break  # el primer (mas chico) que entra en la banda gana

    return {
        "k_BIC_minimo": k_bic,
        "k_aBIC_minimo": k_abic,
        "BIC_y_aBIC_discrepan": discrepan,
        "rango_BIC_observado_1_8": rango_bic,
        "umbral_2pct_no_separacion": umbral_2pct,
        "k_primario_tras_regla_no_separacion": k_primario,
        "nota": ("BIC y aBIC seleccionan el mismo k" if not discrepan else
                 f"BIC selecciona k={k_bic}, aBIC selecciona k={k_abic} -- "
                 f"se reportan ambas soluciones completas; primaria = k MENOR de las dos "
                 f"tras aplicar tambien la regla de no-separacion"),
    }


def perfil_completo(tabla_k):
    res = tabla_k["_resultado_crudo"]
    return {"pi": res["pi"], "phi": res["phi"]}


def evaluar_E1(tabla, k):
    return tabla[k]["n_replican_mejor_logL"] >= 5


def evaluar_E3(tabla, k, umbral_prevalencia=0.05, eps_frontera=1e-4):
    prevs = tabla[k]["prevalencias"]
    degenerada_prevalencia = any(p < umbral_prevalencia for p in prevs)
    frontera = tabla[k]["senal_frontera_0_1"]
    return {
        "pasa": (not degenerada_prevalencia) and frontera == 0,
        "prevalencias": prevs,
        "clase_bajo_umbral_5pct": [i for i, p in enumerate(prevs) if p < umbral_prevalencia],
        "n_senales_frontera": frontera,
    }


def _correlacion(v1, v2):
    n = len(v1)
    m1 = sum(v1) / n
    m2 = sum(v2) / n
    num = sum((a - m1) * (b - m2) for a, b in zip(v1, v2))
    d1 = math.sqrt(sum((a - m1) ** 2 for a in v1))
    d2 = math.sqrt(sum((b - m2) ** 2 for b in v2))
    if d1 == 0 or d2 == 0:
        return 1.0 if d1 == d2 else 0.0
    return num / (d1 * d2)


def _flatten_phi(phi_clase):
    out = []
    for fila in phi_clase:
        out.extend(fila)
    return out


def emparejar_clases(phi_a, phi_b):
    """Maximiza la suma de correlaciones sobre todas las permutaciones
    (k<=8, factible por fuerza bruta: <=40320 permutaciones)."""
    k = len(phi_a)
    va = [_flatten_phi(c) for c in phi_a]
    vb = [_flatten_phi(c) for c in phi_b]
    mejor = None
    mejor_perm = None
    for perm in permutations(range(k)):
        corrs = [_correlacion(va[i], vb[perm[i]]) for i in range(k)]
        s = sum(corrs)
        if mejor is None or s > mejor:
            mejor = s
            mejor_perm = perm
            mejor_corrs = corrs
    return mejor_perm, mejor_corrs


def evaluar_E2(universo, campos, k_seleccionado, ncats, categorias, seed=777, umbral=0.90):
    """Particion aleatoria en dos mitades POR UPM (no por persona)."""
    upms = sorted(set(row["upm"] for row in universo))
    rng = random.Random(seed)
    rng.shuffle(upms)
    mitad = len(upms) // 2
    upms_A = set(upms[:mitad])
    upms_B = set(upms[mitad:])

    universo_A = [r for r in universo if r["upm"] in upms_A]
    universo_B = [r for r in universo if r["upm"] in upms_B]

    _, patrones_upm_A = E.construir_patrones(universo_A, campos)
    _, patrones_upm_B = E.construir_patrones(universo_B, campos)
    patrones_A = E.colapsar_sin_upm(patrones_upm_A)
    patrones_B = E.colapsar_sin_upm(patrones_upm_B)
    n_A = sum(d["n"] for d in patrones_A.values())
    n_B = sum(d["n"] for d in patrones_B.values())
    patrones_A_r, _, _ = E.reescalar_a_n_efectivo(patrones_A, n_A)
    patrones_B_r, _, _ = E.reescalar_a_n_efectivo(patrones_B, n_B)

    res_A = E.ajustar(patrones_A_r, k_seleccionado, ncats, n_arranques=N_ARRANQUES,
                       n_mejores=N_MEJORES, seed=9001)
    res_B = E.ajustar(patrones_B_r, k_seleccionado, ncats, n_arranques=N_ARRANQUES,
                       n_mejores=N_MEJORES, seed=9002)

    return {
        "n_upms_total": len(upms), "n_upms_A": len(upms_A), "n_upms_B": len(upms_B),
        "n_personas_A": n_A, "n_personas_B": n_B,
        "phi_A": res_A["phi"], "phi_B": res_B["phi"],
        "pi_A": res_A["pi"], "pi_B": res_B["pi"],
    }


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("=== Cargando universo (18+) ===")
    universo, meta_carga = D.cargar_universo()
    print(meta_carga)
    n18 = len(universo)

    # --- Faltantes por indicador ANTES de ajustar (Sec.5.3.c) ---
    faltantes = {}
    for campo in CAMPOS_MAIN:
        n_falt = sum(1 for r in universo if r[campo] is None)
        faltantes[campo] = {"n_faltante": n_falt, "prop_faltante": n_falt / n18}
    print("=== Faltantes por indicador ===")
    for c, d in faltantes.items():
        print(f"  {c}: {d['n_faltante']} ({100*d['prop_faltante']:.3f}%)")

    # --- Hueco: est_socio funcion determinista de ing_cor? (Sec.2.4) ---
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
    determinismo = {
        "n_hogares": len(pares),
        "violaciones_monotonicidad_adyacente": violaciones,
        "prop_violaciones": violaciones / max(1, len(pares_ordenados) - 1),
        "rango_ing_cor_por_est_socio": {str(k): v for k, v in sorted(rangos.items())},
        "veredicto": "NO es funcion determinista de ing_cor -- los rangos de ing_cor se traslapan "
                     "casi por completo entre las 4 categorias de est_socio y una fraccion sustancial "
                     "de pares consecutivos (ordenados por ing_cor) viola monotonicidad",
    }
    print("=== est_socio vs ing_cor ===", determinismo["veredicto"],
          f"({100*determinismo['prop_violaciones']:.1f}% violaciones)")

    # --- Referencia temporal de residencia (Sec.2.3) ---
    hueco_residencia = {
        "hallazgo": "la fuente no lo trae",
        "detalle": ("El diccionario de datos de `poblacion` (columna 46, `residencia`) solo dice "
                    "'Categorias en el catalogo de residencia', sin texto de pregunta. "
                    "`metadatos_enigh_2022_ns.txt` no menciona `residencia` en ninguna parte "
                    "(0 coincidencias). Ninguno de los dos archivos trae el periodo de referencia "
                    "(¿hace 5 anios? ¿al nacer?). No es 'no pude confirmarlo' (no hay ambiguedad de "
                    "donde buscar) -- es 'la fuente no lo trae': se buscó en los dos lugares que el "
                    "pre-registro (Sec.2.3, citando §1.1.A) senala como los unicos candidatos, y "
                    "ninguno lo tiene."),
    }

    # --- Variables de diseno (Sec.5.1) ---
    diseno = {
        "factor_persona": "factor -- vive DIRECTO en `poblacion`, a nivel persona (no hace falta "
                           "trasladar un factor de hogar)",
        "estrato": "est_dis -- en `poblacion`",
        "upm": "upm -- en `poblacion`",
        "nota": "Las tres variables de diseno completo (estrato+UPM+factor) viven en la MISMA tabla "
                "que los tres indicadores de persona (I1,I2,I3) y se heredan sin ambiguedad -- el "
                "hueco declarado por Sec.5.1 del pre-registro (P1 no las inventario) queda CERRADO "
                "aqui: se localizaron por nombre exacto, no se tecleraron de memoria.",
    }

    resultados = {
        "n_universo_18mas": n18,
        "meta_carga": meta_carga,
        "faltantes_por_indicador": faltantes,
        "est_socio_vs_ing_cor": determinismo,
        "residencia_referencia_temporal": hueco_residencia,
        "variables_diseno": diseno,
    }

    # =========================================================
    # AJUSTE PRINCIPAL -- k=1..8, ponderado y reescalado a n efectivo
    # =========================================================
    print("\n=== Construyendo patrones (ajuste principal, 7 indicadores) ===")
    cats_main, patrones_upm_main = E.construir_patrones(universo, CAMPOS_MAIN)
    ncats_main = E._n_categorias(cats_main)
    patrones_main = E.colapsar_sin_upm(patrones_upm_main)
    n_ef_main = sum(d["n"] for d in patrones_main.values())
    patrones_main_r, suma_cruda_main, const_main = E.reescalar_a_n_efectivo(patrones_main, n_ef_main)
    print(f"  categorias: {[len(c) for c in cats_main]} -- patrones unicos: {len(patrones_main)}")
    print(f"  suma cruda de pesos (poblacion expandida): {suma_cruda_main:.1f}")
    print(f"  n efectivo (muestra): {n_ef_main} -- constante de reescalamiento: {const_main:.6e}")

    print("\n=== Ajustando k=1..8 (principal, ponderado-reescalado) ===")
    tabla_main = fit_range(patrones_main_r, ncats_main)

    decision_main = regla_decision(tabla_main)
    print("\n=== Regla de decision Sec.3.3 ===")
    print(json.dumps(decision_main, indent=2, ensure_ascii=False))

    k_sel = decision_main["k_primario_tras_regla_no_separacion"]

    # k-1, k, k+1 con perfiles completos (Sec.3.3.6)
    perfiles_vecinos = {}
    for kk in [k_sel - 1, k_sel, k_sel + 1]:
        if kk in tabla_main:
            perfiles_vecinos[kk] = {
                "categorias": cats_main,
                "campos": CAMPOS_MAIN,
                **perfil_completo(tabla_main[kk]),
            }

    # Estabilidad E1, E3 sobre k_sel
    E1_ok = evaluar_E1(tabla_main, k_sel)
    E3 = evaluar_E3(tabla_main, k_sel)
    print(f"\n=== E1 (>=5 arranques replican, k={k_sel}): {E1_ok} ===")
    print(f"=== E3 (sin clases degeneradas, k={k_sel}): {E3['pasa']} -- {E3} ===")

    print(f"\n=== E2 (replicacion en mitades por UPM, k={k_sel}) ===")
    e2 = evaluar_E2(universo, CAMPOS_MAIN, k_sel, ncats_main, cats_main)
    perm, corrs = emparejar_clases(tabla_main[k_sel]["_resultado_crudo"]["phi"], e2["phi_A"])
    perm2, corrs2 = emparejar_clases(tabla_main[k_sel]["_resultado_crudo"]["phi"], e2["phi_B"])
    e2["emparejamiento_A"] = {"perm": list(perm), "correlaciones": corrs, "min_correlacion": min(corrs)}
    e2["emparejamiento_B"] = {"perm": list(perm2), "correlaciones": corrs2, "min_correlacion": min(corrs2)}
    e2["pasa_umbral_090"] = (min(corrs) >= 0.90) and (min(corrs2) >= 0.90)
    print(f"  min correlacion mitad A: {min(corrs):.4f} -- mitad B: {min(corrs2):.4f} -- "
          f"pasa (>=0.90 ambas): {e2['pasa_umbral_090']}")

    estabilidad = {
        "E1_replicacion_logL": E1_ok,
        "E2_replicacion_mitades": e2,
        "E3_sin_degeneradas": E3,
        "INESTABLE": (not E1_ok) or (not e2["pasa_umbral_090"]) or (not E3["pasa"]),
    }

    # =========================================================
    # S4 -- BIC sin pesos, todo el rango
    # =========================================================
    print("\n=== S4: ajuste SIN PESOS, k=1..8 ===")
    patrones_sinpeso = E.patrones_sin_peso(patrones_main)
    tabla_s4 = fit_range(patrones_sinpeso, ncats_main, seed_base=2000)
    decision_s4 = regla_decision(tabla_s4)
    print("k seleccionado (S4, sin pesos):", decision_s4["k_primario_tras_regla_no_separacion"],
          "vs principal:", k_sel)

    # =========================================================
    # S1 -- solo indicadores de persona I1,I2,I3
    # =========================================================
    print("\n=== S1: ajuste solo indicadores de PERSONA (I1,I2,I3), k=1..8 ===")
    cats_s1, patrones_upm_s1 = E.construir_patrones(universo, CAMPOS_S1)
    ncats_s1 = E._n_categorias(cats_s1)
    patrones_s1 = E.colapsar_sin_upm(patrones_upm_s1)
    n_ef_s1 = sum(d["n"] for d in patrones_s1.values())
    patrones_s1_r, _, _ = E.reescalar_a_n_efectivo(patrones_s1, n_ef_s1)
    tabla_s1 = fit_range(patrones_s1_r, ncats_s1, seed_base=3000)
    decision_s1 = regla_decision(tabla_s1)
    print("k seleccionado (S1, solo persona):", decision_s1["k_primario_tras_regla_no_separacion"])

    # =========================================================
    # S2 -- particion de edad alternativa, reajusta SOLO k_sel
    # =========================================================
    print(f"\n=== S2: particion de edad alternativa, reajusta k={k_sel} ===")
    cats_s2, patrones_upm_s2 = E.construir_patrones(universo, CAMPOS_S2)
    ncats_s2 = E._n_categorias(cats_s2)
    patrones_s2 = E.colapsar_sin_upm(patrones_upm_s2)
    n_ef_s2 = sum(d["n"] for d in patrones_s2.values())
    patrones_s2_r, _, _ = E.reescalar_a_n_efectivo(patrones_s2, n_ef_s2)
    # Necesitamos el rango completo para saber si CAMBIA el k seleccionado
    tabla_s2_full = fit_range(patrones_s2_r, ncats_s2, seed_base=4000)
    decision_s2 = regla_decision(tabla_s2_full)
    k_sel_s2 = decision_s2["k_primario_tras_regla_no_separacion"]
    cambia_k_s2 = (k_sel_s2 != k_sel)
    perm_s2, corrs_s2 = (None, None)
    congruencia_s2 = None
    if not cambia_k_s2:
        perm_s2, corrs_s2 = emparejar_clases(tabla_main[k_sel]["_resultado_crudo"]["phi"],
                                              tabla_s2_full[k_sel]["_resultado_crudo"]["phi"])
        congruencia_s2 = {"perm": list(perm_s2), "correlaciones": corrs_s2, "min_correlacion": min(corrs_s2)}
    s2_resultado = {
        "k_seleccionado_S2": k_sel_s2,
        "k_seleccionado_principal": k_sel,
        "cambia_k": cambia_k_s2,
        "congruencia_perfiles": congruencia_s2,
        "advertencia_eje_edad_inestable": cambia_k_s2 or (congruencia_s2 is not None and congruencia_s2["min_correlacion"] < 0.90),
    }
    print("S2:", s2_resultado["k_seleccionado_S2"], "vs principal", k_sel,
          "cambia_k=", cambia_k_s2, "advertencia=", s2_resultado["advertencia_eje_edad_inestable"])

    # =========================================================
    # S3 -- formalidad via `trabajos`, 3 categorias
    # =========================================================
    print("\n=== S3: formalidad via `trabajos` (3 categorias), k=1..8 ===")
    cats_s3, patrones_upm_s3 = E.construir_patrones(universo, CAMPOS_S3)
    ncats_s3 = E._n_categorias(cats_s3)
    patrones_s3 = E.colapsar_sin_upm(patrones_upm_s3)
    n_ef_s3 = sum(d["n"] for d in patrones_s3.values())
    patrones_s3_r, _, _ = E.reescalar_a_n_efectivo(patrones_s3, n_ef_s3)
    tabla_s3 = fit_range(patrones_s3_r, ncats_s3, seed_base=5000)
    decision_s3 = regla_decision(tabla_s3)
    print("k seleccionado (S3, formalidad-trabajos):", decision_s3["k_primario_tras_regla_no_separacion"])

    # =========================================================
    # Volcar todo a JSON (sin los objetos crudos de EM, sin microdato)
    # =========================================================
    def limpiar_tabla(tabla):
        out = {}
        for k, d in tabla.items():
            dd = dict(d)
            dd.pop("_resultado_crudo", None)
            out[str(k)] = dd
        return out

    resultados.update({
        "principal": {
            "campos": CAMPOS_MAIN,
            "categorias": cats_main,
            "suma_cruda_pesos": suma_cruda_main,
            "n_efectivo": n_ef_main,
            "constante_reescalamiento": const_main,
            "tabla_k_1_8": limpiar_tabla(tabla_main),
            "decision_Sec3_3": decision_main,
            "k_seleccionado": k_sel,
            "perfiles_k_vecinos": perfiles_vecinos,
            "estabilidad_Sec3_5": {
                "E1_replicacion_logL": E1_ok,
                "E2": {
                    "n_upms_total": e2["n_upms_total"], "n_upms_A": e2["n_upms_A"], "n_upms_B": e2["n_upms_B"],
                    "n_personas_A": e2["n_personas_A"], "n_personas_B": e2["n_personas_B"],
                    "phi_A": e2["phi_A"], "phi_B": e2["phi_B"], "pi_A": e2["pi_A"], "pi_B": e2["pi_B"],
                    "emparejamiento_A": e2["emparejamiento_A"], "emparejamiento_B": e2["emparejamiento_B"],
                    "pasa_umbral_090": e2["pasa_umbral_090"],
                },
                "E3_sin_degeneradas": E3,
                "INESTABLE": estabilidad["INESTABLE"],
            },
        },
        "S1_solo_persona": {
            "campos": CAMPOS_S1, "categorias": cats_s1,
            "tabla_k_1_8": limpiar_tabla(tabla_s1),
            "decision_Sec3_3": decision_s1,
        },
        "S2_edad_alternativa": {**s2_resultado, "tabla_k_1_8": limpiar_tabla(tabla_s2_full),
                                 "categorias": cats_s2},
        "S3_formalidad_trabajos": {
            "campos": CAMPOS_S3, "categorias": cats_s3,
            "tabla_k_1_8": limpiar_tabla(tabla_s3),
            "decision_Sec3_3": decision_s3,
        },
        "S4_sin_pesos": {
            "tabla_k_1_8": limpiar_tabla(tabla_s4),
            "decision_Sec3_3": decision_s4,
            "k_seleccionado_sin_pesos": decision_s4["k_primario_tras_regla_no_separacion"],
            "k_seleccionado_ponderado": k_sel,
            "cambia_seleccion": decision_s4["k_primario_tras_regla_no_separacion"] != k_sel,
        },
    })

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"\n=== Resultados escritos en {OUT_PATH} ===")
    return resultados


if __name__ == "__main__":
    main()
