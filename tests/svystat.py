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
"""
import math


def prop_ultimate_cluster(rows):
    """rows: iterable de (estrato, upm, peso, y) con y en {0,1}.

    Devuelve dict con p_hat, se, ic95 (lo, hi), n_upm_total, n_estratos_singleton.
    """
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
