#!/usr/bin/env python3
"""Validacion del motor de LCA (tests/p3_lca_em.py) contra datos sinteticos
de parametros conocidos.

No toca ENIGH ni `data/raw` -- es una prueba del ALGORITMO (`ajustar`, la
seleccion de k por BIC), no del pipeline de datos (eso es
tests/p3_lca_stage.py). Genera un universo desde un modelo generador con
k, pi y phi conocidos, corre el motor real sobre esos datos y comprueba
que los recupera dentro de tolerancia -- mismo patron que
`svystat._caso_conocido()` y `tests/cal_conf_faseb_pos4.py` §2.1.

Corre desde la raiz del repo:
    python3 tests/p3_lca_validacion_sintetica.py
"""
import itertools
import random
import sys

sys.path.insert(0, "tests")
import p3_lca_em as lca  # noqa: E402


def _genera_universo(pi_verdadero, phi_verdadero, ncats, n, seed):
    rng = random.Random(seed)
    k = len(pi_verdadero)
    J = len(ncats)
    universo = []
    clases_verdaderas = []
    for i in range(n):
        u = rng.random()
        acc = 0.0
        clase = k - 1
        for kk in range(k):
            acc += pi_verdadero[kk]
            if u < acc:
                clase = kk
                break
        clases_verdaderas.append(clase)
        row = {"upm": i, "factor": 1.0}
        for j in range(J):
            probs = phi_verdadero[clase][j]
            v = rng.random()
            acc2 = 0.0
            cat = ncats[j] - 1
            for c in range(ncats[j]):
                acc2 += probs[c]
                if v < acc2:
                    cat = c
                    break
            row[f"x{j}"] = cat
        universo.append(row)
    return universo, clases_verdaderas


def _mejor_permutacion(pi_true, phi_true, pi_est, phi_est):
    """Resuelve label-switching: el motor no tiene forma de saber que
    'clase 0' del generador es 'clase 0' de la salida -- prueba las k!
    permutaciones y se queda con la que minimiza la distancia total a
    los parametros verdaderos."""
    k = len(pi_true)
    mejor, mejor_costo = None, None
    for perm in itertools.permutations(range(k)):
        costo = 0.0
        for kk in range(k):
            costo += abs(pi_true[kk] - pi_est[perm[kk]])
            for j in range(len(phi_true[kk])):
                for c in range(len(phi_true[kk][j])):
                    costo += abs(phi_true[kk][j][c] - phi_est[perm[kk]][j][c])
        if mejor_costo is None or costo < mejor_costo:
            mejor_costo, mejor = costo, perm
    return mejor, mejor_costo


def main():
    print("=" * 70)
    print("Validacion del motor LCA contra datos sinteticos -- k y phi conocidos")
    print("=" * 70)

    # Modelo generador: k=3, 4 indicadores de cardinalidad [2,3,2,4] --
    # cardinalidad mixta a proposito, igual que los 7 indicadores reales
    # (2,4,3,4,4,2,2) en tests/p3_lca_run.py. Clases separadas por al
    # menos un indicador cada una para que la recuperacion no dependa de
    # suerte en el arranque aleatorio.
    pi_verdadero = [0.5, 0.3, 0.2]
    phi_verdadero = [
        [[0.85, 0.15], [0.75, 0.15, 0.10], [0.80, 0.20], [0.65, 0.15, 0.10, 0.10]],
        [[0.15, 0.85], [0.10, 0.75, 0.15], [0.20, 0.80], [0.10, 0.15, 0.65, 0.10]],
        [[0.50, 0.50], [0.05, 0.10, 0.85], [0.50, 0.50], [0.10, 0.10, 0.10, 0.70]],
    ]
    ncats = [2, 3, 2, 4]
    n = 8000
    seed_datos = 20260804
    seed_ajuste = 12345

    universo, _clases_verdaderas = _genera_universo(pi_verdadero, phi_verdadero, ncats, n, seed_datos)
    campos = [f"x{j}" for j in range(len(ncats))]
    categorias, patrones_con_upm = lca.construir_patrones(universo, campos)
    patrones = lca.colapsar_sin_upm(patrones_con_upm)
    ncats_obs = lca._n_categorias(categorias)

    print(f"n = {n} personas -- {len(patrones)} patrones de respuesta unicos")
    print(f"cardinalidades observadas = {ncats_obs} (esperadas {ncats})")
    assert ncats_obs == ncats, "una categoria no aparecio en la muestra -- ajustar semilla/n"

    print()
    print("-- Paso 1: el motor recupera k por BIC, corriendo k=1..5 --")
    resultados = {}
    for k in range(1, 6):
        r = lca.ajustar(patrones, k, ncats_obs, seed=seed_ajuste + k)
        p = lca.n_parametros_libres(k, ncats_obs)
        b = lca.bic(r["loglik"], p, n)
        resultados[k] = (r, b)
        print(f"  k={k}: logL={r['loglik']:.4f}  parametros={p}  BIC={b:.4f}")

    k_bic = min(resultados, key=lambda kk: resultados[kk][1])
    print(f"  BIC minimo en k={k_bic} (verdadero k={len(pi_verdadero)})")
    assert k_bic == len(pi_verdadero), f"BIC no selecciono el k verdadero: selecciono {k_bic}"

    print()
    print("-- Paso 2: bajo el k verdadero, compara pi y phi estimados contra los generadores --")
    r3, _ = resultados[len(pi_verdadero)]
    perm, costo_total = _mejor_permutacion(pi_verdadero, phi_verdadero, r3["pi"], r3["phi"])
    print(f"  permutacion de clases que empareja estimado con verdadero: {perm}")
    print(f"  costo total (suma de |diferencias| en pi + phi, tras permutar): {costo_total:.4f}")

    pi_est_perm = [r3["pi"][perm[kk]] for kk in range(len(pi_verdadero))]
    print()
    print("  pi verdadero  vs  pi estimado (ya permutado):")
    max_dif_pi = 0.0
    for kk in range(len(pi_verdadero)):
        dif = abs(pi_verdadero[kk] - pi_est_perm[kk])
        max_dif_pi = max(max_dif_pi, dif)
        print(f"    clase {kk}: {pi_verdadero[kk]:.4f}  vs  {pi_est_perm[kk]:.4f}  (dif {dif:.4f})")

    max_dif_phi = 0.0
    print()
    print("  phi verdadero vs phi estimado (ya permutado), maxima diferencia por clase/indicador:")
    for kk in range(len(pi_verdadero)):
        for j in range(len(ncats)):
            fila_v = phi_verdadero[kk][j]
            fila_e = r3["phi"][perm[kk]][j]
            dif = max(abs(a - b) for a, b in zip(fila_v, fila_e))
            max_dif_phi = max(max_dif_phi, dif)
            v_str = "[" + ", ".join(f"{v:.3f}" for v in fila_v) + "]"
            e_str = "[" + ", ".join(f"{v:.3f}" for v in fila_e) + "]"
            print(f"    clase {kk} indicador x{j}: verdadero={v_str}  estimado={e_str}  dif_max={dif:.4f}")

    print()
    print(f"  Maxima diferencia absoluta en pi:  {max_dif_pi:.4f}")
    print(f"  Maxima diferencia absoluta en phi: {max_dif_phi:.4f}")

    TOL_PI = 0.02
    TOL_PHI = 0.05
    assert max_dif_pi < TOL_PI, f"pi no se recupera dentro de tolerancia {TOL_PI}: {max_dif_pi}"
    assert max_dif_phi < TOL_PHI, f"phi no se recupera dentro de tolerancia {TOL_PHI}: {max_dif_phi}"

    print()
    print(f"OK -- el motor recupera k={len(pi_verdadero)} por BIC, y pi/phi dentro de tolerancia")
    print(f"  (tol pi<{TOL_PI}, tol phi<{TOL_PHI}; n={n}, {len(patrones)} patrones unicos).")
    print("Validado.")


if __name__ == "__main__":
    main()
