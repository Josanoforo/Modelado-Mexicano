#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA38-L18 · `comunicacion.inseguridad.ver_oir_callar` (R10.3)
   — falsador de UNA SOLA OLA, LAPOP Mexico 2004.

Spec sellada: forense/prereg-caja/S8-L18-spec-v1_0.md (verificar su .sha256
antes de tocar este script). Implementa exactamente S8 §1-§5.

Universo: victimas de delincuencia (`vic1==1`) con `aoj1` valido (denuncio o
no). Desenlace de interes: el SILENCIO, `DENUNCIA=0` (aoj1==2, "No lo
denuncio"). Tres proxies alternativos (no conjuntos) del antecedente
"contexto de inseguridad/autoridad no confiable":
    INSEGURO_BARRIO   = aoj11 en {3,4} (algo/muy inseguro)
    DESCONFIA_POLICIA = b18 en la mitad inferior de confianza, escala 1..7
                        confirmada 1=NADA .. 7=MUCHO por el cuestionario 2004
                        (Tarjeta "A", ver reporte). Corte principal {1,2,3};
                        robustez con {1,2,3,4}.
    DESCONFIA_JUSTICIA = aoj12 en {3,4} (poco/nada confiaria en que el
                        sistema judicial castigaria al culpable)
INDICE_CONTEXTO = suma de los tres (0..3); ALTO = 2 o 3; BAJO = 0 o 1.

Diseno 2004: estrato `mestrat`, PSU `msec`, SIN PONDERAR (wt existe pero esta
vacia: 0 validos de 1556, verificado por censo_lote_lapop.py). Bootstrap de
conglomerado (10000 replicas, seed 42) reusado de medidor_clientelismo_lapop.
No se modifica ese modulo: `_filas` de la casa hace `float(df[peso])`, que
revienta cuando el ponderador esta vacio, asi que aqui se escribe una
variante local con peso constante 1.0.

Uso:
    python3 tools/medidor_l18_ver_oir_callar_lapop2004.py --mide --json data/l18-ver-oir-callar-lapop2004-v1_0.json
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medidor_clientelismo_lapop import (sha_manifiesto, _cod, prop_bootstrap,  # noqa: E402
                                        diff_bootstrap, _celda, _dif,
                                        MIN_NUMERADOR, REPLICAS, SEED)
from censo_lote_lapop import carga, resuelve  # noqa: E402

ACTO = "MAESTRA38-L18"
SPEC = "forense/prereg-caja/S8-L18-spec-v1_0.md"

# Marginales congelados por el censo A.4 de este acto (ya commiteado en
# data/l4-l5-l18-censo-v1_0.json) y repetidos en el encargo. Si la corrida no
# los reproduce byte a byte, PARA: el lector no esta leyendo lo que el censo
# ya conto.
GUARDIAS = {
    "filas": 1556,
    "vic1_marginal": {1: 268, 2: 1277, 3: 8, 8: 3},
    "aoj1_marginal": {1: 94, 2: 172},        # ya sobre victimas, ver §0.3
    "aoj11_marginal": {1: 330, 2: 667, 3: 419, 4: 129},
    "aoj12_marginal": {1: 114, 2: 374, 3: 613, 4: 410},
    "b18_marginal": {1: 323, 2: 189, 3: 234, 4: 254, 5: 272, 6: 159, 7: 99},
    "b10a_marginal": {1: 161, 2: 143, 3: 250, 4: 334, 5: 346, 6: 178, 7: 111},
    "mestrat_marginal": {1: 407, 2: 298, 3: 515, 4: 336},
    "n_pares_mestrat_msec": 131,
    "n_msec_distintos": 127,
}


def _marginal(df, col):
    m = {}
    for v in df[col]:
        c = _cod(v)
        if c is not None:
            m[c] = m.get(c, 0) + 1
    return m


def _guardia(nombre, obtenido, esperado):
    if obtenido != esperado:
        raise SystemExit(
            f"PARO (guardia de lectura): {nombre} = {obtenido!r}, "
            f"esperado {esperado!r} (censo A.4 / encargo). El lector no leyo "
            f"lo que el censo ya conto.")
    return True


def _filas_sin_peso(df, cols, y_fn, filtro=None, est="mestrat", upm="msec"):
    """Variante local de `_filas` de la casa: peso constante 1.0 (wt de 2004
    esta vacia — 0 validos de 1556, verificado por censo_lote_lapop.py). No
    se toca medidor_clientelismo_lapop.py, que asume `float(df[peso])` y
    revienta/mete NaN si la ola no trae ponderador."""
    out = []
    for i in range(len(df)):
        v = {c: _cod(df[c].iloc[i]) for c in cols}
        if any(v[c] is None for c in cols):
            continue
        if filtro and not filtro(v):
            continue
        y = y_fn(v)
        if y is None:
            continue
        out.append((int(df[est].iloc[i]), int(df[upm].iloc[i]), 1.0, y))
    return out


# ─────────────────────── proxies (§3) ───────────────────────

def _prox_barrio(v):
    x = v.get("aoj11")
    if x in (1, 2):
        return 0
    if x in (3, 4):
        return 1
    return None


def _prox_policia(v, corte):
    x = v.get("b18")
    if x is None or not (1 <= x <= 7):
        return None
    return 1 if x in corte else 0


def _prox_justicia(v):
    x = v.get("aoj12")
    if x in (1, 2):
        return 0
    if x in (3, 4):
        return 1
    return None


def _prox_justicia_b10a(v):
    """b10a en paralelo, verificacion cruzada de aoj12 (§3), mismo corte de
    escala 1..7 que b18 (mitad inferior de confianza = {1,2,3})."""
    x = v.get("b10a")
    if x is None or not (1 <= x <= 7):
        return None
    return 1 if x in (1, 2, 3) else 0


def _indice(v, corte_policia):
    b = _prox_barrio(v)
    p = _prox_policia(v, corte_policia)
    j = _prox_justicia(v)
    if b is None or p is None or j is None:
        return None
    return b + p + j


def _y_silencio(v):
    """y=1 si DENUNCIA=0 (silencio, aoj1==2); y=0 si DENUNCIA=1 (aoj1==1)."""
    a = v.get("aoj1")
    if a == 2:
        return 1
    if a == 1:
        return 0
    return None


def _fmt(c):
    if c.get("estado") != "ESTIMADA":
        return f"NO-ESTIMABLE ({c.get('motivo')})"
    if "p" in c:
        return (f"p={c['p']:.6f}  IC95=[{c['ic95'][0]:.6f},{c['ic95'][1]:.6f}]  "
                f"n={c['n']} num={c['numerador']}")
    return (f"d={c['d']:+.6f}  IC95=[{c['ic95'][0]:+.6f},{c['ic95'][1]:+.6f}]  "
            f"{'EXCLUYE 0' if c['excluye_cero'] else 'contiene 0'}")


def _celda_indice(df, corte_policia, lado, etiqueta):
    """lado: 'ALTO' (indice 2 o 3) o 'BAJO' (indice 0 o 1)."""
    def filtro(v):
        if v.get("vic1") != 1 or v.get("aoj1") not in (1, 2):
            return False
        idx = _indice(v, corte_policia)
        if idx is None:
            return False
        return idx in (2, 3) if lado == "ALTO" else idx in (0, 1)
    filas = _filas_sin_peso(df, ["vic1", "aoj1", "aoj11", "b18", "aoj12"],
                            _y_silencio, filtro)
    return filas, _celda(filas, etiqueta)


def _celda_binaria(df, cols_extra, prox_fn, valor, etiqueta):
    def filtro(v):
        if v.get("vic1") != 1 or v.get("aoj1") not in (1, 2):
            return False
        return prox_fn(v) == valor
    filas = _filas_sin_peso(df, ["vic1", "aoj1"] + cols_extra, _y_silencio, filtro)
    return filas, _celda(filas, etiqueta)


def mide(ruta_json=None):
    df, meta, path, sha, pid = carga("2004_dta")
    sha_man = sha_manifiesto(pid)
    coincide = sha == sha_man

    # --- verificacion del gemelo .sav (S8 dice que son gemelos byte-a-byte;
    #     se verifica, no se hereda a ciegas) ---
    df_sav, meta_sav, path_sav, sha_sav, pid_sav = carga("2004_sav")
    sha_man_sav = sha_manifiesto(pid_sav)
    gemelos_iguales = True
    for var in ("aoj1", "aoj11", "aoj12", "b18", "b10a", "vic1", "mestrat"):
        ca = resuelve(df, var)
        cs = resuelve(df_sav, var)
        ma = _marginal(df, ca) if ca else None
        ms = _marginal(df_sav, cs) if cs else None
        if ma != ms:
            gemelos_iguales = False

    print(f"payload .dta: {path}\n  sha256={sha} -> "
          f"{'COINCIDE' if coincide else 'DIFIERE'} con manifiesto ({sha_man})")
    print(f"payload .sav: {path_sav}\n  sha256={sha_sav} -> "
          f"{'COINCIDE' if sha_sav == sha_man_sav else 'DIFIERE'} con manifiesto")
    print(f"  marginales .dta == .sav (aoj1/aoj11/aoj12/b18/b10a/vic1/mestrat): "
          f"{gemelos_iguales}")

    # --- guardias de lectura, antes de estimar nada ---
    _guardia("filas", len(df), GUARDIAS["filas"])
    _guardia("vic1 marginal", _marginal(df, "vic1"), GUARDIAS["vic1_marginal"])
    _guardia("aoj11 marginal", _marginal(df, "aoj11"), GUARDIAS["aoj11_marginal"])
    _guardia("aoj12 marginal", _marginal(df, "aoj12"), GUARDIAS["aoj12_marginal"])
    _guardia("b18 marginal", _marginal(df, "b18"), GUARDIAS["b18_marginal"])
    _guardia("b10a marginal", _marginal(df, "b10a"), GUARDIAS["b10a_marginal"])
    _guardia("mestrat marginal", _marginal(df, "mestrat"), GUARDIAS["mestrat_marginal"])

    # --- §0.3: hallazgo — tamano real del subuniverso de victimas 2004 ---
    n_vic = sum(1 for v in df["vic1"] if _cod(v) == 1)
    aoj1_marg = _marginal(df, "aoj1")
    _guardia("aoj1 marginal (sobre victimas)", aoj1_marg, GUARDIAS["aoj1_marginal"])
    n_aoj1_val = sum(aoj1_marg.values())
    n_no_victimas_con_aoj1 = sum(
        1 for i in range(len(df))
        if _cod(df["vic1"].iloc[i]) != 1 and _cod(df["aoj1"].iloc[i]) is not None)
    hallazgo_universo = {
        "n_victimas_vic1_1": n_vic,
        "n_victimas_con_aoj1_valido": n_aoj1_val,
        "n_denuncio": aoj1_marg.get(1, 0),
        "n_no_denuncio": aoj1_marg.get(2, 0),
        "n_no_victimas_con_aoj1_valido": n_no_victimas_con_aoj1,
        "tasa_victimizacion": n_vic / len(df),
        "nota": ("aoj1 esta gateada por vic1=1 en el cuestionario mismo "
                 "('AOJ1. [Si responde “Si” a VIC1] ...', linea 215 del "
                 "PDF 2004): 0 no-victimas con aoj1 valido, confirmado."),
    }

    # --- diseno / conglomerado ---
    n_pares = len({(int(_cod(df["mestrat"].iloc[i])), int(_cod(df["msec"].iloc[i])))
                   for i in range(len(df))
                   if _cod(df["mestrat"].iloc[i]) is not None
                   and _cod(df["msec"].iloc[i]) is not None})
    n_msec = len({int(_cod(df["msec"].iloc[i])) for i in range(len(df))
                  if _cod(df["msec"].iloc[i]) is not None})
    _guardia("n pares (mestrat,msec)", n_pares, GUARDIAS["n_pares_mestrat_msec"])
    _guardia("n msec distintos", n_msec, GUARDIAS["n_msec_distintos"])
    n_wt_validos = sum(1 for v in df["wt"] if _cod(v) is not None) if resuelve(df, "wt") else None
    print(f"guardias de lectura: OK  (wt validos = {n_wt_validos} de {len(df)} — "
          f"sin ponderar, declarado)")

    # --- §3.1 celda principal, corte b18 = {1,2,3} ---
    corte_ppal = (1, 2, 3)
    filas_alto, c_alto = _celda_indice(df, corte_ppal, "ALTO", "silencio | INDICE_CONTEXTO=ALTO")
    filas_bajo, c_bajo = _celda_indice(df, corte_ppal, "BAJO", "silencio | INDICE_CONTEXTO=BAJO")
    c_completo = _dif(filas_alto, filas_bajo, "C_completo", c_alto, c_bajo)

    # --- robustez: corte b18 = {1,2,3,4} ---
    corte_rob = (1, 2, 3, 4)
    filas_alto_r, c_alto_r = _celda_indice(df, corte_rob, "ALTO", "silencio | INDICE_CONTEXTO=ALTO (corte b18<=4)")
    filas_bajo_r, c_bajo_r = _celda_indice(df, corte_rob, "BAJO", "silencio | INDICE_CONTEXTO=BAJO (corte b18<=4)")
    c_completo_rob = _dif(filas_alto_r, filas_bajo_r, "C_completo (corte b18<=4)", c_alto_r, c_bajo_r)

    # --- §3.1 diagnosticas 2x2 ---
    f_barrio1, c_barrio1 = _celda_binaria(df, ["aoj11"], _prox_barrio, 1, "silencio | INSEGURO_BARRIO=1")
    f_barrio0, c_barrio0 = _celda_binaria(df, ["aoj11"], _prox_barrio, 0, "silencio | INSEGURO_BARRIO=0")
    c_barrio = _dif(f_barrio1, f_barrio0, "C_barrio", c_barrio1, c_barrio0)

    prox_pol_ppal = lambda v: _prox_policia(v, corte_ppal)  # noqa: E731
    f_pol1, c_pol1 = _celda_binaria(df, ["b18"], prox_pol_ppal, 1, "silencio | DESCONFIA_POLICIA=1")
    f_pol0, c_pol0 = _celda_binaria(df, ["b18"], prox_pol_ppal, 0, "silencio | DESCONFIA_POLICIA=0")
    c_policia = _dif(f_pol1, f_pol0, "C_policia", c_pol1, c_pol0)

    prox_pol_rob = lambda v: _prox_policia(v, corte_rob)  # noqa: E731
    f_pol1r, c_pol1r = _celda_binaria(df, ["b18"], prox_pol_rob, 1, "silencio | DESCONFIA_POLICIA=1 (corte<=4)")
    f_pol0r, c_pol0r = _celda_binaria(df, ["b18"], prox_pol_rob, 0, "silencio | DESCONFIA_POLICIA=0 (corte<=4)")
    c_policia_rob = _dif(f_pol1r, f_pol0r, "C_policia (corte b18<=4)", c_pol1r, c_pol0r)

    f_jus1, c_jus1 = _celda_binaria(df, ["aoj12"], _prox_justicia, 1, "silencio | DESCONFIA_JUSTICIA=1")
    f_jus0, c_jus0 = _celda_binaria(df, ["aoj12"], _prox_justicia, 0, "silencio | DESCONFIA_JUSTICIA=0")
    c_justicia = _dif(f_jus1, f_jus0, "C_justicia", c_jus1, c_jus0)

    # --- b10a en paralelo, verificacion cruzada de aoj12 (no sustituye) ---
    f_b10a1, c_b10a1 = _celda_binaria(df, ["b10a"], _prox_justicia_b10a, 1, "silencio | DESCONFIA_JUSTICIA_b10a=1")
    f_b10a0, c_b10a0 = _celda_binaria(df, ["b10a"], _prox_justicia_b10a, 0, "silencio | DESCONFIA_JUSTICIA_b10a=0")
    c_justicia_b10a = _dif(f_b10a1, f_b10a0, "C_justicia_b10a (verificacion cruzada, no sustituye a aoj12)", c_b10a1, c_b10a0)

    # --- veredicto §4 ---
    def _signo(d):
        if d.get("estado") != "ESTIMADA":
            return None
        return "+" if d["d"] > 0 else "-"

    if c_completo.get("estado") == "ESTIMADA":
        if c_completo["excluye_cero"] and c_completo["d"] > 0:
            veredicto = "CORROBORADA"
        elif c_completo["excluye_cero"] and c_completo["d"] < 0:
            veredicto = "CONTRARIA"
        else:
            veredicto = "NO-DISCRIMINA"
    else:
        signos = [_signo(c_barrio), _signo(c_policia), _signo(c_justicia)]
        excluyen = [c.get("excluye_cero") for c in (c_barrio, c_policia, c_justicia)]
        if any(c.get("estado") == "ESTIMADA" and c["excluye_cero"] and c["d"] < 0
               for c in (c_barrio, c_policia, c_justicia)):
            veredicto = "CONTRARIA"
        elif all(c.get("estado") == "ESTIMADA" and c["excluye_cero"] and c["d"] > 0
                 for c in (c_barrio, c_policia, c_justicia)):
            veredicto = "CORROBORADA-CONVERGENTE-POR-PROXY"
        else:
            veredicto = "NO-ESTIMABLE"

    out = {
        "acto": ACTO,
        "spec": SPEC,
        "regla": "R10.3",
        "id_modelo": "comunicacion.inseguridad.ver_oir_callar",
        "ola": "2004",
        "payload_medido": "2004_dta",
        "payload": {
            "id": pid, "archivo": path, "sha256": sha, "sha256_manifiesto": sha_man,
            "coincide_manifiesto": coincide,
        },
        "payload_gemelo_sav": {
            "id": pid_sav, "archivo": path_sav, "sha256": sha_sav,
            "sha256_manifiesto": sha_man_sav, "coincide_manifiesto": sha_sav == sha_man_sav,
            "marginales_identicas_al_dta": gemelos_iguales,
        },
        "estimador": (f"proporcion ponderada; IC95 bootstrap de conglomerado, "
                      f"{REPLICAS} replicas, seed {SEED}, remuestreo de UPM (msec) "
                      f"dentro de estrato (mestrat). SIN PONDERAR: wt de 2004 esta "
                      f"vacia (0 validos de {len(df)}), declarado, mismo criterio "
                      f"que S5§2/S2-L2§1.0."),
        "escala_b18_b10a": {
            "hallazgo": ("Cuestionario 2004 (Tarjeta 'A', PDF pag. 89-90): escala "
                         "1='NADA' .. 7='MUCHO' para toda la bateria B (incluye "
                         "B10A y B18). Misma direccion que el .dta 2019 "
                         "(1='Nada', 7='Mucho'). NO se invierte."),
            "corte_principal": "mitad inferior de confianza = {1,2,3} (4 es punto "
                               "medio, no entra); declarado antes de calcular",
            "corte_robustez": "{1,2,3,4}",
        },
        "hallazgo_universo_victimas_2004": hallazgo_universo,
        "diseno": {
            "estrato": "mestrat", "psu": "msec", "ponderador": "ninguno (wt vacia)",
            "n_pares_estrato_psu": n_pares, "n_psu_distintos": n_msec,
            "nota_ic": ("El IC no incorpora efecto de diseno mas alla del "
                        "conglomerado documentado (mestrat x msec); sin "
                        "ponderador no hay ajuste por probabilidad de seleccion "
                        "desigual mas alla de lo que el conglomerado ya captura."),
        },
        "celdas": {
            "silencio_ALTO": c_alto, "silencio_BAJO": c_bajo,
            "silencio_ALTO_corte_b18<=4": c_alto_r, "silencio_BAJO_corte_b18<=4": c_bajo_r,
            "silencio_INSEGURO_BARRIO=1": c_barrio1, "silencio_INSEGURO_BARRIO=0": c_barrio0,
            "silencio_DESCONFIA_POLICIA=1": c_pol1, "silencio_DESCONFIA_POLICIA=0": c_pol0,
            "silencio_DESCONFIA_POLICIA=1_corte<=4": c_pol1r, "silencio_DESCONFIA_POLICIA=0_corte<=4": c_pol0r,
            "silencio_DESCONFIA_JUSTICIA=1": c_jus1, "silencio_DESCONFIA_JUSTICIA=0": c_jus0,
            "silencio_DESCONFIA_JUSTICIA_b10a=1": c_b10a1, "silencio_DESCONFIA_JUSTICIA_b10a=0": c_b10a0,
        },
        "contrastes": {
            "C_completo": c_completo,
            "C_completo_corte_b18<=4": c_completo_rob,
            "C_barrio": c_barrio,
            "C_policia": c_policia,
            "C_policia_corte_b18<=4": c_policia_rob,
            "C_justicia": c_justicia,
            "C_justicia_b10a_verificacion_cruzada": c_justicia_b10a,
        },
        "veredicto_B_bis": veredicto,
    }

    if ruta_json:
        json.dump(out, open(ruta_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\nescrito {ruta_json}")
    _imprime(out)
    return out


def _imprime(out):
    print(f"\n{'=' * 78}\nMAESTRA38-L18 · {out['id_modelo']} ({out['regla']}) · LAPOP Mexico 2004")
    h = out["hallazgo_universo_victimas_2004"]
    print(f"  HALLAZGO §0.3: victimas (vic1=1) = {h['n_victimas_vic1_1']}  "
          f"con aoj1 valido = {h['n_victimas_con_aoj1_valido']} "
          f"(denuncio={h['n_denuncio']} / no denuncio={h['n_no_denuncio']})  "
          f"no-victimas con aoj1 valido = {h['n_no_victimas_con_aoj1_valido']}")
    print(f"  escala b18/b10a: {out['escala_b18_b10a']['hallazgo']}")
    print("\n  CELDA PRINCIPAL (corte b18<=3)")
    for k in ("silencio_ALTO", "silencio_BAJO"):
        print(f"    {k:40s} {_fmt(out['celdas'][k])}")
    print(f"    {'C_completo':40s} {_fmt(out['contrastes']['C_completo'])}")
    print("\n  ROBUSTEZ (corte b18<=4)")
    for k in ("silencio_ALTO_corte_b18<=4", "silencio_BAJO_corte_b18<=4"):
        print(f"    {k:40s} {_fmt(out['celdas'][k])}")
    print(f"    {'C_completo_corte_b18<=4':40s} {_fmt(out['contrastes']['C_completo_corte_b18<=4'])}")
    print("\n  DIAGNOSTICAS 2x2")
    for etq, key in (("C_barrio", "C_barrio"), ("C_policia", "C_policia"),
                     ("C_policia (corte<=4)", "C_policia_corte_b18<=4"),
                     ("C_justicia", "C_justicia"),
                     ("C_justicia_b10a (cruzada)", "C_justicia_b10a_verificacion_cruzada")):
        print(f"    {etq:28s} {_fmt(out['contrastes'][key])}")
    print(f"\n  VEREDICTO B-bis: {out['veredicto_B_bis']}")


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
