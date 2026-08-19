#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO FICHA-R51-D3 · COMMIT B — corrida del diseño R5.1-D3.

Ejecuta, sin desviarse, la especificación congelada en
`forense/bbis-r5-1-d3-v1_0.md` (COMMIT A, 19/ago/2026):

  · umbral PRIMARIO deflactado  (2018 $3,276.00/trim -- su propia base;
    2022 $4,034.74/trim -- INPC nov-2018=102.303 -> nov-2022=125.997)
  · umbral SENSIBILIDAD (i) nominal ($3,276.00/trim en ambas olas)
  · U1 (primario, corresidencia): hogares con >=1 persona 65+ clasificada
    y SIN mezcla T/C -- hogar T si TODAS sus 65+ clasificadas son T, C si
    TODAS son C, EXCLUIDO si hay de las dos
  · U2 (sensibilidad ii, corresidencia): universo completo, regla
    any-member -- hogar T si tiene >=1 persona T; C si tiene >=1 C y
    ninguna T
  · U3 (transferencia, P040): personas 65+ clasificadas, intocado por la
    regla de hogar

Estimador: `tests/svystat.py`, reutilizado SIN modificar. Regla de uso
heredada (E4c Commit 3 §3.2): se pasan TODAS las unidades de la ola, con
grupo=None para las no clasificadas -- filtrar antes de estimar fabrica
estratos singleton que la especificación correcta no tiene.

Salida: bloques marcados en stdout. No escribe ningún archivo.
"""

import csv
import io
import math
import os
import sys
import zipfile
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svystat import diff_ultimate_cluster, did_ultimate_cluster  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")

OLAS = {2018: "enigh_2018_ns", 2022: "enigh2022_ns"}
ZIP = {2018: "enigh2018_nc_csv.zip", 2022: "enigh2022_nc_csv.zip"}

# Umbrales sobre `ing_tri` (trimestral), COMMIT A §4 -- no se recalculan aquí.
UMBRAL = {
    "deflactado": {2018: 3276.00, 2022: 4034.74},
    "nominal": {2018: 3276.00, 2022: 3276.00},
}

CLAVE_PENSION = "P032"      # jubilaciones/pensiones originadas dentro del país
CLAVE_DONATIVO = "P040"     # donativos en dinero de otros hogares
CLAVE_BIENESTAR = {2018: "P044", 2022: "P104"}
CORRESIDENCIA = {"3", "4"}  # clase_hog: 3 Ampliado, 4 Compuesto


def _tabla(ola, nombre):
    pat = OLAS[ola]
    ruta = ("conjunto_de_datos_%s_%s/conjunto_de_datos/"
            "conjunto_de_datos_%s_%s.csv" % (nombre, pat, nombre, pat))
    z = zipfile.ZipFile(os.path.join(RAW, ZIP[ola]))
    with z.open(ruta) as f:
        # utf-8-sig: los CSV de INEGI traen BOM. latin-1 lo leería como
        # 'ï»¿folioviv' y rompería el índice de columna en silencio.
        for fila in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            yield fila


def _num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return 0.0


def carga(ola):
    """Devuelve (hogares, personas) de una ola, con las llaves ya
    normalizadas al ancho que declara `concentradohogar` (mecanismo de
    ACTO J -- ancho derivado, no zfill(10) fijo)."""
    hogares = {}
    ancho_fv = None
    for r in _tabla(ola, "concentradohogar"):
        fv = r["folioviv"]
        if ancho_fv is None:
            ancho_fv = len(fv)
        hogares[(fv, r["foliohog"])] = {
            "est_dis": r["est_dis"],
            "upm": r["upm"],
            "factor": _num(r["factor"]),
            "clase_hog": r["clase_hog"],
            "gasto_mon": _num(r["gasto_mon"]),
            "tot_integ": _num(r["tot_integ"]),
        }

    personas = {}
    ancho_nr = None
    for r in _tabla(ola, "poblacion"):
        fv = r["folioviv"].zfill(ancho_fv)
        nr = r["numren"]
        if ancho_nr is None:
            ancho_nr = len(nr)
        personas[(fv, r["foliohog"], nr.zfill(ancho_nr))] = {
            "edad": int(_num(r["edad"])),
            "p032": 0.0,
            "p040": 0.0,
            "bienestar": 0.0,
            "n_filas_ing": 0,
        }

    for r in _tabla(ola, "ingresos"):
        k = (r["folioviv"].zfill(ancho_fv), r["foliohog"],
             r["numren"].zfill(ancho_nr))
        p = personas.get(k)
        if p is None:
            continue
        p["n_filas_ing"] += 1
        cl = r["clave"]
        v = _num(r["ing_tri"])
        if cl == CLAVE_PENSION:
            p["p032"] += v
        elif cl == CLAVE_DONATIVO:
            p["p040"] += v
        elif cl == CLAVE_BIENESTAR[ola]:
            p["bienestar"] += v

    return hogares, personas, ancho_fv, ancho_nr


def clasifica(personas, umbral):
    """T/C por persona 65+ con >=1 fila en `ingresos` (COMMIT A §3)."""
    grupo = {}
    sin_fila = 0
    for k, p in personas.items():
        if p["edad"] < 65:
            continue
        if p["n_filas_ing"] == 0:
            sin_fila += 1
            continue
        grupo[k] = "T" if p["p032"] > umbral else "C"
    return grupo, sin_fila


def hogares_por_regla(grupo):
    """Devuelve (u1, u2, diag) -- dos diccionarios hogar->grupo y el
    diagnóstico de composición."""
    por_hogar = defaultdict(list)
    for (fv, fh, _nr), g in grupo.items():
        por_hogar[(fv, fh)].append(g)

    u1, u2 = {}, {}
    n_1, n_2mas, n_mixto = 0, 0, 0
    for h, gs in por_hogar.items():
        tiene_t = "T" in gs
        tiene_c = "C" in gs
        if len(gs) == 1:
            n_1 += 1
        else:
            n_2mas += 1
        if tiene_t and tiene_c:
            n_mixto += 1
            u2[h] = "T"          # any-member: >=1 T => hogar T
            continue             # U1: mixto => fuera del universo
        u1[h] = "T" if tiene_t else "C"
        u2[h] = "T" if tiene_t else "C"

    diag = {
        "hogares_con_clasificada": len(por_hogar),
        "con_exactamente_1": n_1,
        "con_2_o_mas": n_2mas,
        "mixtos": n_mixto,
        "pct_mixtos_sobre_2mas": (100.0 * n_mixto / n_2mas) if n_2mas else float("nan"),
    }
    return u1, u2, diag


def filas_hogar(hogares, asig):
    """(estrato, upm, peso, y, grupo) por HOGAR -- todos los hogares de la
    ola, grupo=None fuera del universo (contrato de svystat)."""
    for h, d in hogares.items():
        y = 1 if d["clase_hog"] in CORRESIDENCIA else 0
        yield (d["est_dis"], d["upm"], d["factor"], y, asig.get(h))


def filas_persona(hogares, personas, grupo):
    """(estrato, upm, peso, y, grupo) por PERSONA -- todas las personas de
    la ola, y = recibe P040 > 0."""
    for k, p in personas.items():
        d = hogares.get((k[0], k[1]))
        if d is None:
            continue
        y = 1 if p["p040"] > 0 else 0
        yield (d["est_dis"], d["upm"], d["factor"], y, grupo.get(k))


def marginal(hogares, universo):
    """Proporción ponderada de clase_hog in {3,4} sobre el universo dado
    (None = universo completo de hogares de la ola). A-bis regla 4."""
    num = den = 0.0
    for h, d in hogares.items():
        if universo is not None and h not in universo:
            continue
        den += d["factor"]
        if d["clase_hog"] in CORRESIDENCIA:
            num += d["factor"]
    return (num / den if den else float("nan")), den


def razon_ultimate_cluster(filas):
    """R = X_hat / Y_hat con varianza por conglomerado último sobre el
    residual linealizado z_i = w_i*(x_i - R*y_i)/Y_hat (Wolter, razón).
    filas: (estrato, upm, peso, x, y). EXPLORATORIA -- el IC de una razón
    no está en la lista cerrada de COMMIT A §5.6."""
    filas = list(filas)
    X = sum(w * x for _, _, w, x, _ in filas)
    Y = sum(w * y for _, _, w, _, y in filas)
    if Y <= 0:
        return None
    R = X / Y
    por_upm = defaultdict(float)
    for est, upm, w, x, y in filas:
        por_upm[(est, upm)] += w * (x - R * y) / Y
    por_est = defaultdict(list)
    for (est, _upm), z in por_upm.items():
        por_est[est].append(z)
    var = 0.0
    singleton = 0
    for est, zs in por_est.items():
        m = len(zs)
        if m < 2:
            singleton += 1
            continue
        media = sum(zs) / m
        var += (m / (m - 1.0)) * sum((z - media) ** 2 for z in zs)
    se = math.sqrt(var) if var > 0 else 0.0
    return {"R": R, "se": se, "ic95": (R - 1.959963985 * se, R + 1.959963985 * se),
            "n_estratos_singleton": singleton, "X": X, "Y": Y}


def media_ponderada(pares):
    num = den = 0.0
    for w, v in pares:
        num += w * v
        den += w
    return (num / den if den else float("nan")), den


def mediana_ponderada(pares):
    pares = sorted((v, w) for w, v in pares)
    tot = sum(w for _v, w in pares)
    if tot <= 0:
        return float("nan")
    acum = 0.0
    for v, w in pares:
        acum += w
        if acum >= tot / 2.0:
            return v
    return pares[-1][0]


def pp(x):
    return "%+.2fpp" % (100.0 * x)


def main():
    datos = {}
    print("=" * 72)
    print("BLOQUE 0 · Carga y chequeos de consistencia (COMMIT A §5.7)")
    print("=" * 72)
    for ola in (2018, 2022):
        hog, per, afv, anr = carga(ola)
        datos[ola] = (hog, per)
        n65 = sum(1 for p in per.values() if p["edad"] >= 65)
        clas = sum(1 for p in per.values() if p["edad"] >= 65 and p["n_filas_ing"] > 0)
        print("  %d · ancho folioviv derivado de concentradohogar = %d · "
              "ancho numren derivado de poblacion = %d" % (ola, afv, anr))
        print("      hogares=%d  personas=%d  65+=%d  65+ clasificables=%d  "
              "65+ excluidas (0 filas en ingresos)=%d"
              % (len(hog), len(per), n65, clas, n65 - clas))

    print()
    print("=" * 72)
    print("BLOQUE 1 · Hogares mixtos (COMMIT A §5.1) y universos (§5.2)")
    print("=" * 72)
    asignaciones = {}
    for nombre_u in ("deflactado", "nominal"):
        print("  --- umbral %s ---" % nombre_u)
        for ola in (2018, 2022):
            hog, per = datos[ola]
            grupo, sinf = clasifica(per, UMBRAL[nombre_u][ola])
            u1, u2, diag = hogares_por_regla(grupo)
            asignaciones[(nombre_u, ola)] = (grupo, u1, u2)
            nT = sum(1 for g in grupo.values() if g == "T")
            nC = len(grupo) - nT
            print("   %d  personas T=%-6d C=%-6d  (65+ sin fila en ingresos=%d)"
                  % (ola, nT, nC, sinf))
            print("       hogares con >=1 65+ clasificada=%-6d  con exactamente 1=%-6d  "
                  "con >=2=%-5d  MIXTOS=%-5d (%.1f%% de los de >=2)"
                  % (diag["hogares_con_clasificada"], diag["con_exactamente_1"],
                     diag["con_2_o_mas"], diag["mixtos"], diag["pct_mixtos_sobre_2mas"]))
            nu1T = sum(1 for g in u1.values() if g == "T")
            nu2T = sum(1 for g in u2.values() if g == "T")
            print("       U1 (ACOTADO, sin mezcla): %d hogares  T=%d  C=%d   |   "
                  "U2 (completo, any-member): %d hogares  T=%d  C=%d"
                  % (len(u1), nu1T, len(u1) - nu1T, len(u2), nu2T, len(u2) - nu2T))

    print()
    print("=" * 72)
    print("BLOQUE 2 · Corresidencia -- 4 corridas (COMMIT A §5.3)")
    print("        desenlace: clase_hog in {3 Ampliado, 4 Compuesto}")
    print("=" * 72)
    for uni in ("U1", "U2"):
        for nombre_u in ("deflactado", "nominal"):
            rows = {}
            for ola in (2018, 2022):
                hog, _per = datos[ola]
                _g, u1, u2 = asignaciones[(nombre_u, ola)]
                asig = u1 if uni == "U1" else u2
                rows[ola] = list(filas_hogar(hog, asig))
            out = did_ultimate_cluster(rows[2018], rows[2022])
            marca = "  <== PRIMARIA" if (uni == "U1" and nombre_u == "deflactado") else ""
            print("  %s x %-11s  d_pre=%s  d_post=%s  DiD=%s  SE=%.4fpp  "
                  "IC95=(%s, %s)  singleton pre/post=%d/%d%s"
                  % (uni, nombre_u, pp(out["d_pre"]), pp(out["d_post"]),
                     pp(out["theta_hat"]), 100 * out["se"],
                     pp(out["ic95"][0]), pp(out["ic95"][1]),
                     out["n_estratos_singleton_pre"], out["n_estratos_singleton_post"], marca))

    print()
    print("=" * 72)
    print("BLOQUE 3 · Marginal recalculado -- 3 universos (COMMIT A §5.4, A-bis r4)")
    print("=" * 72)
    for ola in (2018, 2022):
        hog, _per = datos[ola]
        _g, u1, u2 = asignaciones[("deflactado", ola)]
        m1, d1 = marginal(hog, u1)
        m2, d2 = marginal(hog, u2)
        m3, d3 = marginal(hog, None)
        print("  %d  U1 (ACOTADO)=%.4f  [N_hat=%.0f, n=%d]   "
              "U2 (any-member)=%.4f  [N_hat=%.0f, n=%d]   "
              "completo=%.4f  [N_hat=%.0f, n=%d]"
              % (ola, m1, d1, len(u1), m2, d2, len(u2), m3, d3, len(hog)))
    print("  (tres universos distintos -- se reportan juntos y NO se restan"
          " uno de otro)")

    print()
    print("=" * 72)
    print("BLOQUE 4 · Transferencia P040 -- 2 corridas (COMMIT A §5.5), intocado")
    print("=" * 72)
    for nombre_u in ("deflactado", "nominal"):
        rows = {}
        for ola in (2018, 2022):
            hog, per = datos[ola]
            g, _u1, _u2 = asignaciones[(nombre_u, ola)]
            rows[ola] = list(filas_persona(hog, per, g))
        out = did_ultimate_cluster(rows[2018], rows[2022])
        print("  U3 x %-11s  d_pre=%s  d_post=%s  DiD=%s  SE=%.4fpp  "
              "IC95=(%s, %s)  singleton pre/post=%d/%d"
              % (nombre_u, pp(out["d_pre"]), pp(out["d_post"]),
                 pp(out["theta_hat"]), 100 * out["se"],
                 pp(out["ic95"][0]), pp(out["ic95"][1]),
                 out["n_estratos_singleton_pre"], out["n_estratos_singleton_post"]))

    print()
    print("=" * 72)
    print("BLOQUE 5 · Monto/gasto -- la compuerta (COMMIT A §5.6), ola 2022")
    print("        razon = media_ponderada(P104) / media_ponderada(gasto_mon per capita)")
    print("        trimestral/trimestral, pesos corrientes, factor de concentradohogar")
    print("=" * 72)
    hog, per = datos[2022]
    g, u1, _u2 = asignaciones[("deflactado", 2022)]
    poblaciones = {
        "(a) R5.1-D2  personas T (todas)": lambda k: g.get(k) == "T",
        "(b) R5.1-D3  personas T en hogar T de U1": lambda k: (
            g.get(k) == "T" and u1.get((k[0], k[1])) == "T"),
    }
    for etiqueta, cond in poblaciones.items():
        elegibles = [k for k in per if cond(k)]
        recibe = [k for k in elegibles if per[k]["bienestar"] > 0]
        pares_m, pares_g, filas_r = [], [], []
        for k in recibe:
            d = hog[(k[0], k[1])]
            w = d["factor"]
            gpc = d["gasto_mon"] / d["tot_integ"] if d["tot_integ"] else 0.0
            pares_m.append((w, per[k]["bienestar"]))
            pares_g.append((w, gpc))
            filas_r.append((d["est_dis"], d["upm"], w, per[k]["bienestar"], gpc))
        mm, _ = media_ponderada(pares_m)
        mg, _ = media_ponderada(pares_g)
        razon = mm / mg if mg else float("nan")
        med_m = mediana_ponderada(pares_m)
        med_g = mediana_ponderada(pares_g)
        r = razon_ultimate_cluster(filas_r)
        print("  %s" % etiqueta)
        print("      n elegibles=%-6d  n con P104>0=%-6d  (%.1f%% de recepcion efectiva)"
              % (len(elegibles), len(recibe), 100.0 * len(recibe) / len(elegibles)))
        print("      P104 medio (trim)=$%.2f  gasto_mon per capita medio (trim)=$%.2f"
              % (mm, mg))
        print("      RAZON (media ponderada) = %.2f%%   [piso heredado: 33%%]" % (100 * razon))
        print("      mediana P104=$%.2f  mediana gasto pc=$%.2f  razon de medianas=%.2f%% "
              "(secundaria, no promovida)" % (med_m, med_g, 100.0 * med_m / med_g))
        if r:
            print("      EXPLORATORIA (no pre-declarada): IC95%% de la razon por "
                  "conglomerado ultimo = (%.2f%%, %.2f%%)  SE=%.2fpp  singleton=%d"
                  % (100 * r["ic95"][0], 100 * r["ic95"][1], 100 * r["se"],
                     r["n_estratos_singleton"]))

    print()
    print("=" * 72)
    print("FIN -- ninguna cantidad fuera de la lista cerrada de COMMIT A §5,")
    print("       salvo las dos marcadas EXPLORATORIA arriba.")
    print("=" * 72)


if __name__ == "__main__":
    main()
