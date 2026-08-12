#!/usr/bin/env python3
"""Estimador de conglomerado ultimo (ultimate cluster) en Python puro.

Reimplementado en la sesion CAL-CONF Fase B / segunda ola (03/ago/2026):
el svystat.py de la primera ola no esta commiteado (vivia en el scratch
de aquella sesion). No hay numpy/scipy instalados en este entorno -- se
implementa con listas y el modulo estandar `math` unicamente.

Formula (Wolter, "Introduction to Variance Estimation", ultimate cluster,
un solo nivel de conglomerado -- la UPM primaria que cada instrumento
declara, no un diseno multietapico completo):

  Sobre una proporcion ponderada p_hat = sum(w*y) / sum(w),
  agregada primero a nivel de UPM dentro de cada estrato:
    t_h_i  = sum de (w*y) en la UPM i del estrato h      (total ponderado del numerador)
    n_h_i  = sum de w       en la UPM i del estrato h      (total ponderado del denominador)
    e_h_i  = t_h_i - p_hat * n_h_i                          (residual de la UPM)

  var(p_hat) = (1 / N_hat^2) * sum_h [ (n_h / (n_h - 1)) * sum_i (e_h_i - mean_i(e_h_i))^2 ]

  donde N_hat = sum(w) (total poblacional estimado) y n_h = numero de UPM
  en el estrato h. Estratos con una sola UPM no aportan varianza estimable
  con este metodo (grados de libertad insuficientes) -- se reportan aparte,
  no se fuerzan a cero silenciosamente.

Caso degenerado de validacion (SRS, pesos uniformes, un conglomerado por
observacion): con una UPM por observacion y un solo estrato, la formula de
arriba colapsa exactamente a p(1-p)/(n-1), la varianza muestral estandar de
una proporcion. Es la prueba de §2.

Anadido ENCARGO B (12/ago/2026): diff_ultimate_cluster (contraste T-C
dentro de una ola) y did_ultimate_cluster (diferencias-en-diferencias
entre dos olas independientes) -- derivacion completa en
forense/notas/2026-08-12-estimador-contraste.md. prop_ultimate_cluster
arriba no se modifica.
"""
import math


def prop_ultimate_cluster(rows):
    """rows: iterable de (estrato, upm, peso, y) con y en {0,1}.

    Devuelve dict con p_hat, se, ic95 (lo, hi), n_upm_total, n_estratos_singleton.
    """
    rows = list(rows)  # se recorre dos veces (aqui y en el bloque de UPM abajo) --
    # un generador se agotaria en el primer recorrido y fallaria en silencio
    N_hat = 0.0
    num = 0.0
    for _est, _upm, w, y in rows:
        N_hat += w
        num += w * y
    if N_hat == 0:
        return None
    p_hat = num / N_hat

    # Agregar por (estrato, upm)
    upm_totals = {}   # (estrato,upm) -> [t_h_i, n_h_i]
    estrato_upms = {}  # estrato -> set(upm)
    for est, upm, w, y in rows:
        key = (est, upm)
        if key not in upm_totals:
            upm_totals[key] = [0.0, 0.0]
        upm_totals[key][0] += w * y
        upm_totals[key][1] += w
        estrato_upms.setdefault(est, set()).add(upm)

    var = 0.0
    singleton_estratos = 0
    for est, upms in estrato_upms.items():
        n_h = len(upms)
        e_list = []
        for upm in upms:
            t_h_i, n_h_i = upm_totals[(est, upm)]
            e_h_i = t_h_i - p_hat * n_h_i
            e_list.append(e_h_i)
        if n_h < 2:
            singleton_estratos += 1
            continue
        mean_e = sum(e_list) / n_h
        ss = sum((e - mean_e) ** 2 for e in e_list)
        var += (n_h / (n_h - 1)) * ss

    var = var / (N_hat ** 2)
    se = math.sqrt(var) if var > 0 else 0.0
    lo = p_hat - 1.959963985 * se
    hi = p_hat + 1.959963985 * se
    return {
        "p_hat": p_hat,
        "se": se,
        "ic95": (max(0.0, lo), min(1.0, hi)),
        "n_estratos": len(estrato_upms),
        "n_upm_total": len(upm_totals),
        "n_estratos_singleton": singleton_estratos,
    }


def diff_ultimate_cluster(rows):
    """rows: iterable de (estrato, upm, peso, y, grupo) con y en {0,1} y
    grupo en {"T", "C", None}. T y C mutuamente excluyentes; unidades
    fuera de grupo (grupo=None) permanecen en el archivo y aportan
    residual cero -- no se filtran (cambiar la estructura de estratos/UPM
    del diseno alteraria los grados de libertad; esto es estimacion de
    dominio, no submuestreo).

    Estima d_hat = p_T - p_C dentro de UNA ola, con conglomerado ultimo
    sobre el residual linealizado de la diferencia (Wolter, "Introduction
    to Variance Estimation", ultimate cluster; misma agregacion por UPM
    que prop_ultimate_cluster arriba, aplicada al residual de d en vez de
    al de p):

      p_T = sum(w*y | grupo=T) / N_hat_T      p_C analogo sobre C
      z_i = 1{i en T}*w_i*(y_i-p_T)/N_hat_T - 1{i en C}*w_i*(y_i-p_C)/N_hat_C

      var(d_hat) = sum_h [ (m_h/(m_h-1)) * sum_i (z_hi - mean_i(z_hi))^2 ]

    donde z_hi es z_i agregado por UPM dentro de estrato (misma forma que
    e_h_i arriba) y m_h es el numero de UPM del estrato h. z_i captura la
    covarianza entre p_T y p_C inducida por compartir estrato/UPM -- es
    la razon de ser de esta funcion: T y C salen de la misma muestra
    dentro de una ola, así que var(p_T-p_C) != var(p_T)+var(p_C) en
    general (ver did_ultimate_cluster para el caso de dos olas, donde esa
    suma si es valida).

    Cuatro decisiones de diseno, declaradas (derivacion completa en
    forense/notas/2026-08-12-estimador-contraste.md):

      1. Singleton: un estrato de una sola UPM salta (no aporta a
         var(d_hat)) y se cuenta en n_estratos_singleton -- misma
         politica que prop_ultimate_cluster arriba. El llamador DEBE leer
         ese contador: un singleton no detectado baja el SE en silencio.
         tools/curador_registro/produce.py::taylor_distribution adopta la
         politica contraria (lanza ESTRATOS_UNA_UPM y aborta) -- dos
         politicas para la misma condicion en el mismo programa, anotado
         y no unificado en este acto.
      2. Cuantil normal 1.959963985, igual que prop_ultimate_cluster, no
         1.96 (taylor_distribution usa 1.96 -- los IC95 de las dos vias
         no coincidiran en los ultimos digitos, esperado).
      3. rows = list(rows): se recorre dos veces (N_hat_T/N_hat_C, y
         despues el bloque de UPM), mismo motivo que prop_ultimate_cluster
         (un generador se agotaria en el primer recorrido y fallaria en
         silencio en el segundo).
      4. Grupo vacio: si N_hat_T=0 o N_hat_C=0, devuelve None -- igual
         que prop_ultimate_cluster con N_hat=0. No lanza excepcion, no
         devuelve cero.

    Devuelve dict con d_hat, p_T, p_C, se, ic95, n_upm_total, n_estratos,
    n_estratos_singleton.
    """
    rows = list(rows)  # se recorre dos veces -- ver decision 3 arriba

    N_hat_T = 0.0
    num_T = 0.0
    N_hat_C = 0.0
    num_C = 0.0
    for _est, _upm, w, y, grupo in rows:
        if grupo == "T":
            N_hat_T += w
            num_T += w * y
        elif grupo == "C":
            N_hat_C += w
            num_C += w * y
    if N_hat_T == 0 or N_hat_C == 0:
        return None
    p_T = num_T / N_hat_T
    p_C = num_C / N_hat_C
    d_hat = p_T - p_C

    # Agregar z_i por (estrato, upm). Unidades fuera de grupo aportan 0.
    upm_z = {}
    estrato_upms = {}
    for est, upm, w, y, grupo in rows:
        key = (est, upm)
        if grupo == "T":
            z_i = w * (y - p_T) / N_hat_T
        elif grupo == "C":
            z_i = -w * (y - p_C) / N_hat_C
        else:
            z_i = 0.0
        upm_z[key] = upm_z.get(key, 0.0) + z_i
        estrato_upms.setdefault(est, set()).add(upm)

    var = 0.0
    singleton_estratos = 0
    for est, upms in estrato_upms.items():
        m_h = len(upms)
        z_list = [upm_z[(est, upm)] for upm in upms]
        if m_h < 2:
            singleton_estratos += 1
            continue
        mean_z = sum(z_list) / m_h
        ss = sum((z - mean_z) ** 2 for z in z_list)
        var += (m_h / (m_h - 1)) * ss

    se = math.sqrt(var) if var > 0 else 0.0
    lo = d_hat - 1.959963985 * se
    hi = d_hat + 1.959963985 * se
    return {
        "d_hat": d_hat,
        "p_T": p_T,
        "p_C": p_C,
        "se": se,
        "ic95": (lo, hi),
        "n_estratos": len(estrato_upms),
        "n_upm_total": len(upm_z),
        "n_estratos_singleton": singleton_estratos,
    }


def did_ultimate_cluster(rows_pre, rows_post):
    """rows_pre, rows_post: cada uno un iterable de (estrato, upm, peso,
    y, grupo), formato identico al de diff_ultimate_cluster -- una ola
    cada uno. Estima theta_hat = d_post - d_pre (diferencias-en-
    diferencias entre dos olas).

    var(theta_hat) = var(d_post) + var(d_pre) -- la suma es valida SOLO
    porque las dos olas son muestras transversales independientes, no
    panel (misma persona medida dos veces). Cita literal,
    forense/r5-1-diseno-por-regla-preregistro-v1_0.md:72 (S4): "No es
    panel. ENIGH es transversal repetida -- 2018 y 2022 son muestras
    independientes, no las mismas personas." LIMITE DECLARADO: si esta
    funcion se aplicara a un panel, la suma deja de valer -- un panel
    induce covarianza entre d_pre y d_post via la misma unidad medida dos
    veces, que esta funcion no captura. No se verifica en codigo (no hay
    forma de saberlo desde rows_pre/rows_post solos); es responsabilidad
    de quien llama.

    rows_pre y rows_post se pasan una sola vez, completos, a
    diff_ultimate_cluster (que ya materializa cada uno con list(rows) por
    dentro) -- no hace falta una segunda materializacion aqui.

    Si diff_ultimate_cluster devuelve None para cualquiera de las dos
    olas (grupo vacio en esa ola), did_ultimate_cluster tambien devuelve
    None -- extension de la misma regla de grupo vacio, no se puede
    construir un DiD con una sola pata.

    Devuelve dict con theta_hat, d_pre, d_post, se, ic95, y los
    contadores de singleton de cada ola por separado
    (n_estratos_singleton_pre, n_estratos_singleton_post), sin colapsar
    -- un singleton en una sola ola no debe quedar escondido detras de un
    total sumado.
    """
    out_pre = diff_ultimate_cluster(rows_pre)
    out_post = diff_ultimate_cluster(rows_post)
    if out_pre is None or out_post is None:
        return None

    theta_hat = out_post["d_hat"] - out_pre["d_hat"]
    var_theta = out_pre["se"] ** 2 + out_post["se"] ** 2
    se = math.sqrt(var_theta) if var_theta > 0 else 0.0
    lo = theta_hat - 1.959963985 * se
    hi = theta_hat + 1.959963985 * se
    return {
        "theta_hat": theta_hat,
        "d_pre": out_pre["d_hat"],
        "d_post": out_post["d_hat"],
        "se": se,
        "ic95": (lo, hi),
        "n_estratos_singleton_pre": out_pre["n_estratos_singleton"],
        "n_estratos_singleton_post": out_post["n_estratos_singleton"],
    }


def _caso_conocido():
    """SRS degenerado: n=200, k=80 exitos, peso uniforme=1, un conglomerado
    (UPM) por observacion, un solo estrato de diseno.

    Bajo ese caso, ultimate cluster con n_h UPMs de un solo elemento cada
    una, en un solo estrato, colapsa a la varianza muestral estandar de una
    proporcion: p(1-p)/(n-1).
    """
    n, k = 200, 80
    rows = []
    for i in range(n):
        y = 1 if i < k else 0
        rows.append(("estrato_unico", f"upm_{i}", 1.0, y))

    out = prop_ultimate_cluster(rows)
    p_esperado = k / n
    se_esperado = math.sqrt(p_esperado * (1 - p_esperado) / (n - 1))

    print("OK -- caso conocido (SRS, n=200, k=80, PSU=persona):")
    print(f"  p_hat calculado = {out['p_hat']:.6f} (esperado {p_esperado:.6f})")
    print(f"  se calculado    = {out['se']:.6f} (formula SRS p(1-p)/(n-1) = {se_esperado:.6f})")

    assert abs(out["p_hat"] - p_esperado) < 1e-9, "p_hat no coincide"
    assert abs(out["se"] - se_esperado) < 1e-9, "se no coincide con la formula SRS"
    print("Coincide a 9 decimales. Validado.")


if __name__ == "__main__":
    _caso_conocido()
