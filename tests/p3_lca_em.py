#!/usr/bin/env python3
"""P3 -- motor de LCA (mixtura finita de indicadores categoricos, FIML bajo
independencia local condicional a la clase) en Python puro -- sin numpy,
sin scipy (no estan instalados en este entorno, ver tests/svystat.py).

Optimizacion central: en vez de correr EM sobre cada persona, se colapsa
el universo a PATRONES unicos (combinacion de categorias observadas +
`None` donde falta un indicador) agregados por (UPM, patron), con su peso
sumado y su conteo. El EM opera sobre esa tabla de patrones -- el numero
de patrones unicos es varios ordenes de magnitud menor que n, así que 500
arranques por valor de k (pre-registro Sec.3.4) son factibles en minutos,
no en horas.

Missing (`None`) se maneja como el pre-registro exige (Sec.5.3.b, FIML
bajo MAR): la persona con un indicador faltante NO se excluye ni se le
inventa una categoria "faltante" -- el E-step multiplica solo sobre los
indicadores SI observados en ese patron. Esto es la verosimilitud marginal
correcta bajo independencia local condicional a la clase, exacta y no
aproximada.
"""
import math
import random
from collections import Counter, defaultdict


def construir_patrones(universo, campos, peso_campo="factor"):
    """campos: lista ordenada de claves de universo[i] a usar como
    indicadores. Devuelve:
      - categorias: lista de listas, categorias[j] = valores unicos
        observados del campo j (orden estable, sin None)
      - patrones: dict {(upm, patron_tuple): {'w': peso_sumado, 'n': conteo}}
        patron_tuple[j] es el INDICE en categorias[j], o None si falta.
    """
    valores_unicos = [set() for _ in campos]
    for row in universo:
        for j, campo in enumerate(campos):
            v = row[campo]
            if v is not None:
                valores_unicos[j].add(v)
    categorias = [sorted(vs) for vs in valores_unicos]
    idx_map = [{v: i for i, v in enumerate(cat)} for cat in categorias]

    patrones = defaultdict(lambda: {"w": 0.0, "n": 0})
    for row in universo:
        patron = tuple(
            (idx_map[j][row[campo]] if row[campo] is not None else None)
            for j, campo in enumerate(campos)
        )
        upm = row["upm"]
        key = (upm, patron)
        d = patrones[key]
        d["w"] += row[peso_campo]
        d["n"] += 1
    return categorias, dict(patrones)


def colapsar_sin_upm(patrones_con_upm):
    """Para el ajuste principal (no necesita UPM, solo E2 lo necesita).
    Devuelve dict {patron_tuple: {'w':..., 'n':...}}."""
    out = defaultdict(lambda: {"w": 0.0, "n": 0})
    for (upm, patron), d in patrones_con_upm.items():
        o = out[patron]
        o["w"] += d["w"]
        o["n"] += d["n"]
    return dict(out)


def reescalar_a_n_efectivo(patrones, n_efectivo):
    """Sec.5.2: los pesos se reescalan para sumar el n de muestra
    efectivo (conteo de personas), no el total expandido. Devuelve nueva
    tabla de patrones con 'w' reescalado y la constante usada."""
    suma_cruda = sum(d["w"] for d in patrones.values())
    n_muestra = sum(d["n"] for d in patrones.values())
    assert n_muestra == n_efectivo, (n_muestra, n_efectivo)
    constante = n_efectivo / suma_cruda
    reescalados = {p: {"w": d["w"] * constante, "n": d["n"]} for p, d in patrones.items()}
    return reescalados, suma_cruda, constante


def patrones_sin_peso(patrones):
    """Sec.5.2 S4: tabla no ponderada -- cada persona pesa 1.0."""
    return {p: {"w": float(d["n"]), "n": d["n"]} for p, d in patrones.items()}


def _n_categorias(categorias):
    return [len(c) for c in categorias]


def _init_aleatorio(k, ncats, rng):
    pi = [rng.random() + 0.01 for _ in range(k)]
    s = sum(pi)
    pi = [x / s for x in pi]
    phi = []
    for kk in range(k):
        fila = []
        for c in ncats:
            vals = [rng.random() + 0.01 for _ in range(c)]
            s = sum(vals)
            fila.append([v / s for v in vals])
        phi.append(fila)
    return pi, phi


def _em_paso(patrones_items, k, ncats, pi, phi):
    """Un paso E+M. patrones_items: lista de (patron, w). Devuelve
    (pi_nuevo, phi_nuevo, loglik, resp_por_patron)."""
    J = len(ncats)
    # Acumuladores M-step
    resp_total = [0.0] * k
    conteo_cat = [[[0.0] * c for c in ncats] for _ in range(k)]
    peso_obs_cat = [[0.0 for _ in ncats] for _ in range(k)]
    loglik = 0.0
    resp_por_patron = []

    for patron, w in patrones_items:
        dens = [0.0] * k
        for kk in range(k):
            p = pi[kk]
            for j in range(J):
                c = patron[j]
                if c is not None:
                    p *= phi[kk][j][c]
            dens[kk] = p
        s = sum(dens)
        if s <= 0.0 or s != s:  # cero o NaN -- patron con densidad nula bajo esta init
            # Reparto uniforme para no romper el algoritmo; esto solo pasa
            # con inicializaciones degeneradas que luego se descartan por
            # baja logL frente a otros arranques.
            resp = [1.0 / k] * k
            s = 1e-300
        else:
            resp = [d / s for d in dens]
            loglik += w * math.log(s)
        resp_por_patron.append(resp)

        for kk in range(k):
            rw = resp[kk] * w
            resp_total[kk] += rw
            for j in range(J):
                c = patron[j]
                if c is not None:
                    conteo_cat[kk][j][c] += rw
                    peso_obs_cat[kk][j] += rw

    n_total = sum(resp_total)
    pi_nuevo = [rt / n_total for rt in resp_total]
    phi_nuevo = []
    for kk in range(k):
        fila = []
        for j, c in enumerate(ncats):
            denom = peso_obs_cat[kk][j]
            if denom <= 0:
                fila.append([1.0 / c] * c)
            else:
                fila.append([conteo_cat[kk][j][cc] / denom for cc in range(c)])
        phi_nuevo.append(fila)
    return pi_nuevo, phi_nuevo, loglik, resp_por_patron


def loglik_de(patrones_items, k, ncats, pi, phi):
    J = len(ncats)
    ll = 0.0
    for patron, w in patrones_items:
        s = 0.0
        for kk in range(k):
            p = pi[kk]
            for j in range(J):
                c = patron[j]
                if c is not None:
                    p *= phi[kk][j][c]
            s += p
        if s > 0:
            ll += w * math.log(s)
        else:
            ll += w * -700.0  # log(~0), penaliza sin romper
    return ll


def ajustar(patrones, k, ncats, n_arranques=500, n_mejores=50,
            iters_rank=15, iters_final=300, tol=1e-8, seed=0):
    """Implementa Sec.3.4: >=500 arranques, las 50 mejores soluciones
    iniciales (por logL tras `iters_rank` iteraciones cortas) se llevan a
    convergencia final. Devuelve el mejor resultado y cuantos arranques
    replican la mejor logL final (tolerancia 1e-6 absoluta) -- para
    aplicar la regla NO REPLICADA de Sec.3.4."""
    patrones_items = [(p, d["w"]) for p, d in patrones.items()]
    rng = random.Random(seed)

    candidatos = []
    for a in range(n_arranques):
        pi, phi = _init_aleatorio(k, ncats, rng)
        for _ in range(iters_rank):
            pi, phi, ll, _ = _em_paso(patrones_items, k, ncats, pi, phi)
        candidatos.append((ll, pi, phi))

    candidatos.sort(key=lambda t: t[0], reverse=True)
    top = candidatos[:n_mejores]

    finales = []
    for ll0, pi, phi in top:
        ll_prev = ll0
        for it in range(iters_final):
            pi, phi, ll, resp = _em_paso(patrones_items, k, ncats, pi, phi)
            if abs(ll - ll_prev) < tol:
                break
            ll_prev = ll
        finales.append((ll, pi, phi))

    finales.sort(key=lambda t: t[0], reverse=True)
    mejor_ll, mejor_pi, mejor_phi = finales[0]

    # Cuantos de los N_ARRANQUES (no solo los 50 finales) llegan cerca del
    # optimo global -- para eso comparamos la logL de los candidatos de
    # rango corto tras converger cada uno de los `n_mejores` a fondo, y
    # ademas contamos cuantos arranques (de TODOS) ya estaban a <1e-6 de
    # discrepancia relativa del mejor tras el ranking corto Y llevados a
    # convergencia. Aplicamos el criterio sobre los arranques finalizados
    # (los unicos con logL de convergencia real).
    replican = sum(1 for ll, _, _ in finales if abs(ll - mejor_ll) < 1e-6 * max(1.0, abs(mejor_ll)) + 1e-6)

    _, _, _, resp_final = _em_paso(patrones_items, k, ncats, mejor_pi, mejor_phi)

    return {
        "k": k,
        "loglik": mejor_ll,
        "pi": mejor_pi,
        "phi": mejor_phi,
        "n_replican_mejor": replican,
        "n_arranques": n_arranques,
        "n_mejores_llevados_a_convergencia": n_mejores,
        "resp_por_patron": resp_final,
        "patrones_items": patrones_items,
    }


def n_parametros_libres(k, ncats):
    return (k - 1) + k * sum(c - 1 for c in ncats)


def bic(loglik, params, n):
    return -2.0 * loglik + params * math.log(n)


def abic(loglik, params, n):
    n_star = (n + 2) / 24.0
    return -2.0 * loglik + params * math.log(n_star)


def aic(loglik, params):
    return -2.0 * loglik + 2.0 * params


def entropia_relativa(resultado, n_efectivo, k):
    if k <= 1:
        return None
    patrones_items = resultado["patrones_items"]
    resp = resultado["resp_por_patron"]
    suma = 0.0
    for (patron, w), r in zip(patrones_items, resp):
        for rk in r:
            if rk > 0:
                suma += w * (-rk * math.log(rk))
    denom = n_efectivo * math.log(k)
    if denom <= 0:
        return None
    return 1.0 - suma / denom


def prevalencias(resultado):
    return list(resultado["pi"])


def senal_frontera(resultado, eps=1e-4):
    """Cuenta probabilidades condicionales pegadas a 0 o 1 (frontera)."""
    cuenta = 0
    for fila in resultado["phi"]:
        for cats in fila:
            for p in cats:
                if p < eps or p > 1 - eps:
                    cuenta += 1
    return cuenta
