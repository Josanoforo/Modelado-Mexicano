#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA38-L4 · `civico.voto.clientelar_si_observable` (R7.6) — LAPOP Mexico 2019.

Spec sellada: forense/prereg-caja/S4-L4-spec-v1_0.md (nombre estable
`prereg-caja-S4-L4` v1.0, 4/sep/2026). NO se edita ese archivo; este script
implementa exactamente su §1-§5.

Reusa el patron de la casa en vez de reinventar el estimador:
  - `tools/medidor_clientelismo_lapop.py` exporta `carga`, `sha256`,
    `sha_manifiesto`, `_cod`, `prop_bootstrap`/`diff_bootstrap` (via
    `_celda`/`_dif`), `MIN_NUMERADOR`, `REPLICAS`, `SEED`.
  - `tools/censo_lote_lapop.py` ya censo esta ola (A.4, commiteado en
    `data/l4-l5-l18-censo-v1_0.json`) — este script no re-deriva el censo,
    solo reproduce la guardia de lectura de §2 antes de estimar nada.

Por que NO se usa `_filas()` de la casa tal cual para EXPUESTO: esa funcion
descarta la fila si CUALQUIERA de las columnas pedidas es faltante
(`any(v[c] is None for c in cols): continue`). La regla de EXPUESTO de esta
spec es una disyuncion (`clien1n==1 OR clien1na==1`): una persona con
`clien1n` faltante y `clien1na==1` SI es EXPUESTO=1, y `_filas()` la
descartaria por el faltante en `clien1n` antes de evaluar la disyuncion. Por
eso este script clasifica primero (`_clasifica`), fila por fila, y arma las
tuplas `(estrato, upm, peso, y)` a mano para pasarlas a `_celda`/`_dif` de la
casa sin tocar `medidor_clientelismo_lapop.py`.

Uso:
    python3 tools/medidor_l4_clientelar_lapop2019.py --mide --json data/l4-clientelar-lapop2019-v1_0.json
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medidor_clientelismo_lapop import (  # noqa: E402
    carga, sha256, sha_manifiesto, _cod, _celda, _dif, MIN_NUMERADOR, REPLICAS, SEED,
)

PID = "mexico_lapop_americasbarometer_2019_v1_0_w"

# Guardia de lectura, spec S4-L4 §2 (heredada de una corrida real, L9 §0.5).
GUARDIA = {"filas": 1580, "clien1na_val": 1578, "clien1na_si": 271}


def _guardia(nombre, obtenido, esperado):
    if obtenido != esperado:
        raise SystemExit(
            f"PARO (guardia de lectura, spec S4-L4 §2): {nombre} = {obtenido}, "
            f"esperado {esperado}. El .dta no reprodujo el marginal que L9 §0.5 "
            f"ya verifico -- no es la misma version del payload.")
    return True


def _mismo_signo(d, otros):
    """True solo si `d` y TODOS los `otros` tienen el mismo signo estricto.
    Compara numeros, no rotulos: es la diferencia entre conjuntos y lexico."""
    if d is None or not otros:
        return None
    s = (d > 0) - (d < 0)
    if s == 0:
        return False
    return all(((o > 0) - (o < 0)) == s for o in otros)


def _clasifica(df):
    """Una fila por persona: codigos + EXPUESTO + pertenencia al universo.

    EXPUESTO=1  si clien1n==1 O clien1na==1               (spec §3)
    EXPUESTO=0  SOLO si clien1n==2 Y clien1na==2           (spec §3, literal:
                una persona con una de las dos en 2 y la otra faltante NO
                cumple "las dos son 2" y queda SIN-CLASIFICAR)
    universo    vb3n valido (no 'a'/'b'/'c', no NaN -- eso ya lo hace `_cod`)
                Y (clien1n valido en {1,2} O clien1na valido en {1,2})  (spec §2)
    """
    filas = []
    for i in range(len(df)):
        c1 = _cod(df["clien1n"].iloc[i])
        c1a = _cod(df["clien1na"].iloc[i])
        vb3n = _cod(df["vb3n"].iloc[i])
        vb10 = _cod(df["vb10"].iloc[i])
        if c1 == 1 or c1a == 1:
            exp = 1
        elif c1 == 2 and c1a == 2:
            exp = 0
        else:
            exp = None
        en_universo = (vb3n is not None) and (c1 in (1, 2) or c1a in (1, 2))
        filas.append({
            "estrato": int(df["estratopri"].iloc[i]),
            "upm": int(df["upm"].iloc[i]),
            "peso": float(df["wt"].iloc[i]),
            "c1": c1, "c1a": c1a, "vb3n": vb3n, "vb10": vb10,
            "expuesto": exp, "en_universo": en_universo,
        })
    return filas


def _tuplas(filas, y_fn):
    """(estrato, upm, peso, y) para las filas que ya pasaron un filtro dado."""
    return [(f["estrato"], f["upm"], f["peso"], y_fn(f)) for f in filas]


def mide(ruta_json=None):
    df, meta, path, sha = carga("2019")
    sha_man = sha_manifiesto(PID)

    # --- guardia de lectura §2, ANTES de estimar nada ---
    _guardia("2019 filas", len(df), GUARDIA["filas"])
    _guardia("2019 clien1na validos",
             sum(1 for v in df["clien1na"] if _cod(v) is not None), GUARDIA["clien1na_val"])
    _guardia("2019 clien1na si",
             sum(1 for v in df["clien1na"] if _cod(v) == 1), GUARDIA["clien1na_si"])
    print("guardia de lectura spec S4-L4 §2: OK "
          f"(filas={GUARDIA['filas']}, clien1na_val={GUARDIA['clien1na_val']}, "
          f"clien1na_si={GUARDIA['clien1na_si']})")

    filas = _clasifica(df)

    # --- reporte de clasificacion, muestra completa (n=1580) ---
    n_exp1_full = sum(1 for f in filas if f["expuesto"] == 1)
    n_exp0_full = sum(1 for f in filas if f["expuesto"] == 0)
    n_sc_full = sum(1 for f in filas if f["expuesto"] is None)

    # --- universo §2 (vb3n valido y clien1n/clien1na con codigo valido) ---
    universo = [f for f in filas if f["en_universo"]]
    n_universo = len(universo)
    n_exp1_uni = sum(1 for f in universo if f["expuesto"] == 1)
    n_exp0_uni = sum(1 for f in universo if f["expuesto"] == 0)
    n_sc_uni = sum(1 for f in universo if f["expuesto"] is None)

    # --- muestra de estimacion: universo Y clasificado (EXPUESTO in {0,1}) ---
    sample = [f for f in universo if f["expuesto"] is not None]
    n_sample = len(sample)
    exp1 = [f for f in sample if f["expuesto"] == 1]
    exp0 = [f for f in sample if f["expuesto"] == 0]

    out = {
        "acto": "MAESTRA38-L4 · civico.voto.clientelar_si_observable (R7.6)",
        "spec": "forense/prereg-caja/S4-L4-spec-v1_0.md (prereg-caja-S4-L4 v1.0)",
        "id_modelo": "civico.voto.clientelar_si_observable",
        "regla": "R7.6",
        "fuente": "LAPOP Mexico AmericasBarometer 2019",
        "payload": {"id": PID, "archivo": path, "sha256": sha,
                    "sha256_manifiesto": sha_man, "coincide_manifiesto": sha == sha_man},
        "estimador": (f"proporcion ponderada; IC95 bootstrap de conglomerado, "
                      f"{REPLICAS} replicas, seed {SEED}, remuestreo de UPM "
                      f"(upm) dentro de estrato (estratopri); ponderador wt "
                      f"(constante = 1 en las {GUARDIA['filas']} filas, verificado)"),
        "diseno": {"estrato": "estratopri", "conglomerado": "upm", "ponderador": "wt",
                   "wt_constante_1": bool((df["wt"] == 1).all()),
                   "n_upm": int(df["upm"].nunique()),
                   "n_estratopri": sorted(int(x) for x in df["estratopri"].unique())},
        "clasificacion_tratamiento": {
            "regla": "EXPUESTO=1 si clien1n==1 O clien1na==1; EXPUESTO=0 solo si "
                     "clien1n==2 Y clien1na==2 (literal spec §3); faltantes "
                     "('a'/'b'/'c', NaN) no se imputan.",
            "muestra_completa_n1580": {"EXPUESTO_1": n_exp1_full, "EXPUESTO_0": n_exp0_full,
                                        "SIN_CLASIFICAR": n_sc_full},
            "dentro_del_universo_sec2": {"n_universo": n_universo,
                                          "EXPUESTO_1": n_exp1_uni, "EXPUESTO_0": n_exp0_uni,
                                          "SIN_CLASIFICAR": n_sc_uni},
        },
        "universo": {
            "definicion": "18+ con codigo valido {1,2} en clien1n O clien1na, "
                          "y vb3n no vacio/no NS-NR (spec §2)",
            "n": n_universo,
            "n_muestra_estimacion_clasificada": n_sample,
        },
    }

    # ---------------- celdas principales: PRI (103) y MORENA (101) ----------
    desenlaces = {"PRI_principal": 103, "MORENA_secundario": 101}
    celdas = {}
    contrastes = {}
    for nom, cod in desenlaces.items():
        fa = _tuplas(exp1, lambda f, c=cod: 1 if f["vb3n"] == c else 0)
        fb = _tuplas(exp0, lambda f, c=cod: 1 if f["vb3n"] == c else 0)
        ca = _celda(fa, f"vb3n={cod} | EXPUESTO=1")
        cb = _celda(fb, f"vb3n={cod} | EXPUESTO=0")
        d = _dif(fa, fb, f"Δ_eleccion_{nom}", ca, cb)
        celdas[nom] = {"expuesto_1": ca, "expuesto_0": cb}
        contrastes[nom] = d
    out["celdas"] = celdas
    out["contrastes"] = contrastes

    # ---------------- veredicto §4.1 -----------------------------------
    d_pri = contrastes["PRI_principal"]
    d_morena = contrastes["MORENA_secundario"]
    if d_pri.get("estado") != "ESTIMADA":
        veredicto = "NO-ESTIMABLE"
        motivo = d_pri.get("motivo", "celda(s) de PRI no estimable(s)")
    elif d_pri["excluye_cero"] and d_pri["d"] > 0:
        veredicto = "CORROBORADA"
        motivo = f"Δ_eleccion(PRI) = {d_pri['d']:+.6f} > 0, IC95 excluye 0"
    elif d_pri["excluye_cero"] and d_pri["d"] < 0:
        veredicto = "CONTRARIA"
        motivo = f"Δ_eleccion(PRI) = {d_pri['d']:+.6f} < 0, IC95 excluye 0"
    else:
        veredicto = "NO-DISCRIMINA"
        motivo = f"IC95 de Δ_eleccion(PRI) = [{d_pri['ic95'][0]:+.6f},{d_pri['ic95'][1]:+.6f}] contiene 0"

    discrepancia_signo = None
    if (d_pri.get("estado") == "ESTIMADA" and d_morena.get("estado") == "ESTIMADA"
            and d_pri["excluye_cero"] and d_morena["excluye_cero"]):
        discrepancia_signo = (d_pri["signo"] != d_morena["signo"])
        if discrepancia_signo:
            motivo += (f" · Δ_eleccion(MORENA) = {d_morena['d']:+.6f} discrepa en signo "
                       f"y tambien es limpio -- manda PRI por precedencia §4.1")

    out["veredicto"] = {"regla": "R7.6", "id_modelo": "civico.voto.clientelar_si_observable",
                        "resultado": veredicto, "justificacion": motivo,
                        "discrepancia_signo_pri_morena": discrepancia_signo}

    # ---------------- control de robustez §3: vb10 --------------------
    robustez_vb10 = {}
    faltan_vb10 = sum(1 for f in sample if f["vb10"] is None)
    for nom, cod in desenlaces.items():
        robustez_vb10[nom] = {}
        for lab, v10 in (("con_partido", 1), ("sin_partido", 2)):
            sub1 = [f for f in exp1 if f["vb10"] == v10]
            sub0 = [f for f in exp0 if f["vb10"] == v10]
            fa = _tuplas(sub1, lambda f, c=cod: 1 if f["vb3n"] == c else 0)
            fb = _tuplas(sub0, lambda f, c=cod: 1 if f["vb3n"] == c else 0)
            ca = _celda(fa, f"vb3n={cod} | EXPUESTO=1, vb10={lab}")
            cb = _celda(fb, f"vb3n={cod} | EXPUESTO=0, vb10={lab}")
            d = _dif(fa, fb, f"Δ_{nom}_{lab}", ca, cb)
            robustez_vb10[nom][lab] = {"expuesto_1": ca, "expuesto_0": cb, "delta": d}
    out["robustez_vb10"] = {
        "nota": "subdivision declarada solo como robustez (spec §3), no como "
                "veredicto adicional -- mismo criterio que L9 §1.4 para ejes "
                "sin signo pre-registrado.",
        "faltan_vb10_en_muestra": faltan_vb10,
        "celdas": robustez_vb10,
    }

    # ---------------- §4.3: comparacion de signo, sin celda conjunta ---
    out["comparacion_otro_brazo_no_celda_conjunta"] = {
        "nota": "spec §0.4/§4.3: no existe una ola LAPOP con oferta clientelar Y "
                "observabilidad percibida sobre la misma persona -- no se fabrica "
                "celda de tres factores. Se cita el OTRO brazo (observabilidad), ya "
                "corrido y sellado, y solo se compara el SIGNO.",
        "esta_pieza_brazo_proximidad_lapop2019": {
            "delta_pri": d_pri.get("d"), "ic95_pri": d_pri.get("ic95"),
            "excluye_cero_pri": d_pri.get("excluye_cero"),
            "veredicto": veredicto,
        },
        "L9_brazo_observabilidad_lapop2023": {
            "delta_secreto_pp": 14.37, "ic95_secreto_pp": [1.43, 27.44],
            "delta_observable_pp": 17.98, "ic95_observable_pp": [10.75, 25.02],
            "veredicto": "CONTRARIA",
        },
        "L11_brazo_observabilidad_encuci2020": {
            "delta_secreto_pp": 6.38, "ic95_secreto_pp": [3.82, 8.89],
            "delta_observable_pp": 11.57, "ic95_observable_pp": [6.57, 16.59],
            "veredicto": "CONTRARIA",
        },
        # OJO: comparar el SIGNO del efecto, no el rotulo del veredicto. Los dos
        # son cosas distintas y aqui van al reves una de la otra: el delta de esta
        # pieza es NEGATIVO (-4.07 pp) y los cuatro de L9/L11 son POSITIVOS. Que
        # las tres piezas caigan en CONTRARIA no las pone en la misma direccion
        # empirica -- cada una refuta la prediccion de SU propio diseno (esta, por
        # efecto directo negativo; L9/L11, porque la separacion SECRETO/OBSERVABLE
        # que su par B-bis exige no aparece, con los dos brazos positivos).
        # Un `veredicto == "CONTRARIA"` aqui compararia el LEXICO, no los conjuntos.
        "mismo_signo_del_efecto_que_L9_L11": _mismo_signo(
            d_pri.get("d"), [14.37, 17.98, 6.38, 11.57]),
        "mismo_rotulo_de_veredicto_que_L9_L11": (veredicto == "CONTRARIA"),
        "por_que_los_dos_campos_difieren": (
            "El signo de esta pieza es NEGATIVO y los cuatro de L9/L11 son POSITIVOS: "
            "no comparten direccion empirica. Comparten el ROTULO CONTRARIA porque cada "
            "pieza refuta la prediccion de su propio diseno, no porque el efecto apunte "
            "al mismo lado. spec §4.3 pide comparar el SIGNO entre piezas: el signo NO "
            "coincide, y lo que sostiene la lectura conjunta es que ninguno de los dos "
            "brazos de la disyuncion muestra la cesion de autonomia que [MEDIA] predice."),
    }

    if ruta_json:
        json.dump(out, open(ruta_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("escrito", ruta_json)
    _imprime(out)
    return out


def _fmt(c):
    if not isinstance(c, dict):
        return str(c)
    if c.get("estado") != "ESTIMADA":
        return f"NO-ESTIMABLE ({c.get('motivo')})"
    if "p" in c:
        return (f"p={c['p']:.6f}  IC95=[{c['ic95'][0]:.6f},{c['ic95'][1]:.6f}]  "
                f"n={c['n']} num={c['numerador']}")
    return (f"d={c['d']:+.6f}  IC95=[{c['ic95'][0]:+.6f},{c['ic95'][1]:+.6f}]  "
            f"{'EXCLUYE 0' if c['excluye_cero'] else 'contiene 0'}")


def _imprime(out):
    print(f"\n{'=' * 78}")
    print(f"{out['acto']}")
    print(f"payload sha256={out['payload']['sha256'][:16]}...  "
          f"coincide_manifiesto={out['payload']['coincide_manifiesto']}")
    ct = out["clasificacion_tratamiento"]
    print("\nCLASIFICACION (muestra completa n=1580):", ct["muestra_completa_n1580"])
    print("CLASIFICACION (dentro del universo §2):", ct["dentro_del_universo_sec2"])
    print(f"\nUNIVERSO §2: n={out['universo']['n']}  "
          f"muestra clasificada para estimar: n={out['universo']['n_muestra_estimacion_clasificada']}")
    for nom in ("PRI_principal", "MORENA_secundario"):
        print(f"\n--- {nom} ---")
        print(f"  EXPUESTO=1  {_fmt(out['celdas'][nom]['expuesto_1'])}")
        print(f"  EXPUESTO=0  {_fmt(out['celdas'][nom]['expuesto_0'])}")
        print(f"  Δ_eleccion  {_fmt(out['contrastes'][nom])}")
    print(f"\nVEREDICTO R7.6: {out['veredicto']['resultado']}")
    print(f"  {out['veredicto']['justificacion']}")
    print("\nROBUSTEZ vb10 (declarada, no veredicto):")
    for nom, blk in out["robustez_vb10"]["celdas"].items():
        for lab, c in blk.items():
            print(f"  {nom} / {lab}: {_fmt(c['delta'])}")
    print(f"\n{'=' * 78}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mide", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.mide:
        mide(a.json)
        return
    ap.print_help()


if __name__ == "__main__":
    main()
