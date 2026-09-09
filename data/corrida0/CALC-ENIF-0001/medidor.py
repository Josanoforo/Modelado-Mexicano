"""`CALC-ENIF-0001` — horizonte de ahorro, vía formal/informal y desconfianza
en la protección de depósitos, ENIF 2024.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-LOTE-ENIF-1`, ANTES DE LEER
UN SOLO BYTE DE MICRODATO. Spec sellada que lo gobierna:
`forense/prereg-caja/ENIF-AHORRO-spec-v1_0.md`
(`prereg-caja-ENIF-AHORRO`, sha `697ab9e8…`).

Lo unico abierto al escribir este archivo: `data/manifiesto.yaml`, el
descriptor `enif_2024_fd.xlsx`, el cuestionario `enif_2024_cuestionario.pdf`,
la lista de miembros del ZIP, `milpa/tramite.yaml` y
`data/corrida0/demanda-*.tsv`. NINGUN `*.csv` del microdato.

Releva la demanda `CORR-0009` (los 8 RESULT que el encargo nombra). NO toca
`RES-0031`/`RES-0032`. NO cambia ninguna cifra de `milpa/tramite.yaml`: la
adopcion de P3 es CITA.
"""
from __future__ import annotations

import csv
import io
import zipfile

import numpy as np

# ── constantes de la spec congelada ───────────────────────────────────────

ZIP_ID = "enif_2024_enif_2024_bd_csv"
P = "RESULT-ENIF-AHO-"

M_MOD = "TMODULO.csv"

INFORMAL = ["P5_1_1", "P5_1_2", "P5_1_3", "P5_1_4", "P5_1_5", "P5_1_6"]
FORMAL = ["P5_6_1", "P5_6_2", "P5_6_3", "P5_6_4", "P5_6_5", "P5_6_6",
          "P5_6_7", "P5_6_8", "P5_6_9"]
TIENE_CUENTA = ["P5_4_1", "P5_4_2", "P5_4_3", "P5_4_4", "P5_4_5", "P5_4_6",
                "P5_4_7", "P5_4_8", "P5_4_9"]

COLS = (["P4_10", "P3_13", "P5_20", "P5_23", "FILTRO_S5_1",
         "FAC_PER", "EST_DIS", "UPM_DIS", "EDAD_V"]
        + INFORMAL + FORMAL + TIENE_CUENTA)

# familia A — el corte, declarado en la spec, NO heredado
A_CORTO = {"1", "2"}
A_NOCORTO = {"3", "4", "5"}
A_CORTO_S1 = {"1"}
A_NOCORTO_S1 = {"2", "3", "4", "5"}
A_P410_VALIDOS = A_CORTO | A_NOCORTO
A_P410_FALTA = {"8", "9"}
A_CON_SS = {"1", "2", "3", "4"}
A_SIN_SS = {"7"}
A_FUERA = {"5", "6", "9"}

B_SI = {"1"}

C_DESCONFIA = {"03"}
C_OTRAS = {"01", "02", "04", "05", "06", "07", "08", "09", "10"}
C_P520_VALIDOS = C_DESCONFIA | C_OTRAS
C_CONOCE = {"1"}
C_NO_CONOCE = {"2"}

# dominios que el FD declara (guardia G-D5); '' y 'b' se permiten aparte
DOMINIO = {
    "P4_10": {"1", "2", "3", "4", "5", "8", "9"},
    "P3_13": {"1", "2", "3", "4", "5", "6", "7", "9"},
    "P5_20": {"01", "02", "03", "04", "05", "06", "07", "08", "09", "10"},
    "P5_23": {"1", "2"},
}
for _c in INFORMAL + FORMAL + TIENE_CUENTA:
    DOMINIO[_c] = {"1", "2"}

REPLICAS = 1000
SEED = 20260909
GRANO = 6


# ── utilidades ────────────────────────────────────────────────────────────

def _norm(col: str) -> str:
    """Encabezado sin BOM (utf-8-sig o su mojibake latin-1) y en mayusculas."""
    return col.lstrip("﻿").lstrip("ï»¿").strip().upper()


def _cod(s):
    """Codigo como CADENA CRUDA. Nunca int: '03' != 3 y 'b' no es NaN."""
    if s is None:
        return ""
    return str(s).strip()


def _peso(s):
    """FAC_PER a float. None si no es finito o <= 0 (G-D2)."""
    if s is None:
        return None
    t = str(s).strip().replace(",", "")
    if not t:
        return None
    try:
        f = float(t)
    except ValueError:
        return None
    if f != f or f in (float("inf"), float("-inf")) or f <= 0:
        return None
    return f


def _llave(s):
    """EST_DIS / UPM_DIS como CADENA CRUDA (llaves opacas, G-D4)."""
    if s is None:
        return None
    t = str(s).strip()
    return t or None


def _abre(zf, miembro, cols):
    """Lee `miembro` probando utf-8-sig y cayendo a latin-1.

    Devuelve (filas, n_filas, columnas_ausentes, encoding_usado).
    Toda celda se entrega como CADENA: dtype=str de facto.
    """
    crudo = zf.read(miembro)
    enc = "utf-8-sig"
    try:
        txt = crudo.decode("utf-8-sig")
    except UnicodeDecodeError:
        txt = crudo.decode("latin-1")
        enc = "latin-1"
    r = csv.reader(io.StringIO(txt, newline=""))
    try:
        cab = [_norm(c) for c in next(r)]
    except StopIteration:
        return [], 0, list(cols), enc
    idx = {c: cab.index(c) for c in cols if c in cab}
    ausentes = [c for c in cols if c not in idx]
    filas, n = [], 0
    for row in r:
        if not row:
            continue
        n += 1
        filas.append([row[idx[c]] if (c in idx and idx[c] < len(row)) else None
                      for c in cols])
    return filas, n, ausentes, enc


def _p(w, d):
    """p = sum(w*d)/sum(w), sumas en ORDEN FIJO DE FILA."""
    sw = 0.0
    swd = 0.0
    for wi, di in zip(w, d):
        sw += wi
        if di:
            swd += wi
    return ((swd / sw) if sw > 0 else None), sw


def _ic(w, d, est, upm, replicas=REPLICAS, seed=SEED):
    """Bootstrap de UPM_DIS con reemplazo DENTRO de EST_DIS.

    Devuelve (lo, hi, n_est, n_upm, n_estratos_upm_unica, metodo, n_sin_diseno).
    """
    n_sin = sum(1 for e, u in zip(est, upm) if e is None or u is None)
    grupos = {}
    for i, (e, u) in enumerate(zip(est, upm)):
        if e is None or u is None:
            continue
        grupos.setdefault(e, {}).setdefault(u, []).append(i)
    if not grupos:
        return None, None, 0, 0, 0, "NO-ESTIMABLE-DISENO-INCOMPLETO", n_sin
    n_est = len(grupos)
    n_upm = sum(len(v) for v in grupos.values())
    n_unica = sum(1 for v in grupos.values() if len(v) == 1)
    rng = np.random.default_rng(seed)
    claves = {e: list(v.keys()) for e, v in grupos.items()}
    reps = []
    for _ in range(replicas):
        sw = 0.0
        swd = 0.0
        for e, ks in claves.items():
            k = len(ks)
            for j in rng.integers(0, k, size=k):
                for i in grupos[e][ks[int(j)]]:
                    sw += w[i]
                    if d[i]:
                        swd += w[i]
        if sw > 0:
            reps.append(swd / sw)
    if not reps:
        return None, None, n_est, n_upm, n_unica, \
            "NO-ESTIMABLE-DISENO-INCOMPLETO", n_sin
    a = np.asarray(reps, dtype=float)
    met = ("IC-CON-ESTRATOS-DE-UPM-UNICA" if n_unica > 0
           else "BOOTSTRAP-UPM-EN-ESTRATO")
    return (float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5)),
            n_est, n_upm, n_unica, met, n_sin)


def _redondea(v):
    return None if v is None else round(v, GRANO)


# ── el medidor ────────────────────────────────────────────────────────────

def medir(inputs, contrato):
    R = {}

    def put(suf, val):
        R[P + suf] = val

    zf = zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"])
    mod, n_mod, ausentes, enc = _abre(zf, M_MOD, COLS)
    ix = {c: i for i, c in enumerate(COLS)}

    put("G-N-FILAS-TMODULO", n_mod)
    put("G-ENCODING-USADO", enc)
    put("G-COLUMNAS-AUSENTES", ";".join(ausentes) if ausentes else "NINGUNA")

    def falta(c):
        return c in ausentes

    def col(r, c):
        return _cod(r[ix[c]]) if not falta(c) else ""

    # ── G-D5 · dominio de codigos ────────────────────────────────────────
    fuera_total = 0
    for c, dom in DOMINIO.items():
        if falta(c):
            continue
        malos = {}
        for r in mod:
            v = col(r, c)
            if v and v != "b" and v not in dom:
                malos[v] = malos.get(v, 0) + 1
        fuera_total += sum(malos.values())
        put(f"G-D5-FUERA-DE-DOMINIO-{c}",
            ";".join(f"{k}={v}" for k, v in sorted(malos.items())) or "NINGUNO")
    put("G-D5-N-CELDAS-FUERA-DE-DOMINIO", fuera_total)

    # ── G-P1 · la poblacion es 18+, no 18-70 ─────────────────────────────
    if falta("EDAD_V"):
        put("G-P1-POBLACION", "NO-ESTIMABLE-COLUMNA-AUSENTE:EDAD_V")
        put("G-P1-EDAD-MIN", None)
        put("G-P1-EDAD-MAX", None)
    else:
        eds = []
        for r in mod:
            v = col(r, "EDAD_V")
            if v.isdigit():
                eds.append(int(v))
        reales = [e for e in eds if e <= 95]
        put("G-P1-EDAD-MIN", min(reales) if reales else None)
        put("G-P1-EDAD-MAX", max(reales) if reales else None)
        put("G-P1-N-CODIGO-97", sum(1 for e in eds if e == 97))
        put("G-P1-N-CODIGO-98", sum(1 for e in eds if e == 98))
        if not reales:
            put("G-P1-POBLACION", "NO-ESTIMABLE-COLUMNA-VACIA:EDAD_V")
        elif max(reales) > 70:
            put("G-P1-POBLACION", "18-Y-MAS · PREMISA-18-70-REFUTADA")
        else:
            put("G-P1-POBLACION", "18-70 · PREMISA-18-70-CONFIRMADA")

    # ── G-D4 · las llaves de diseno son texto opaco ──────────────────────
    if falta("EST_DIS") or falta("UPM_DIS"):
        put("G-D4-LLAVES-OPACAS", "NO-ESTIMABLE-COLUMNA-AUSENTE")
    else:
        ceros = sum(1 for r in mod
                    if col(r, "EST_DIS").startswith("0")
                    or col(r, "UPM_DIS").startswith("0"))
        put("G-D4-LLAVES-OPACAS", "TEXTO-CRUDO")
        put("G-D4-N-FILAS-CON-CERO-A-LA-IZQUIERDA", ceros)

    # ── G-C1 · P5_23 no debe traer 'b' ni vacio ──────────────────────────
    if falta("P5_23"):
        put("G-C1-EJE-ES-PARTICION", "NO-ESTIMABLE-COLUMNA-AUSENTE:P5_23")
        c1_ok = False
    else:
        n_b = sum(1 for r in mod if col(r, "P5_23") in ("", "b"))
        put("G-C1-N-P523-BLANCO-O-B", n_b)
        c1_ok = (n_b == 0)
        put("G-C1-EJE-ES-PARTICION",
            "SI" if c1_ok else "NO · NO-ESTIMABLE-EJE-NO-ES-PARTICION")

    # ── G-C2 · quien contesta 5.20 no tiene ninguna cuenta ───────────────
    faltan_54 = [c for c in TIENE_CUENTA if falta(c)]
    if falta("P5_20") or faltan_54:
        put("G-C2-DENOMINADOR-C-VERIFICADO",
            "NO-ESTIMABLE-COLUMNA-AUSENTE:" + ";".join(
                ([("P5_20")] if falta("P5_20") else []) + faltan_54))
        c2_ok = False
    else:
        viol = 0
        for r in mod:
            if col(r, "P5_20") in ("", "b"):
                continue
            if any(col(r, c) in B_SI for c in TIENE_CUENTA):
                viol += 1
        put("G-C2-N-FILAS-CON-520-Y-CUENTA", viol)
        c2_ok = (viol == 0)
        put("G-C2-DENOMINADOR-C-VERIFICADO",
            "SI" if c2_ok else "NO · NO-ESTIMABLE-DENOMINADOR-C-NO-VERIFICADO")

    # ── ponderador ───────────────────────────────────────────────────────
    if falta("FAC_PER"):
        put("G-D2-PONDERADOR", "NO-ESTIMABLE-COLUMNA-AUSENTE:FAC_PER")
        pes = [None] * len(mod)
    else:
        pes = [_peso(r[ix["FAC_PER"]]) for r in mod]
        put("G-D2-PONDERADOR", "OK")
        put("G-D2-N-SIN-PONDERADOR", sum(1 for p in pes if p is None))

    ests = ([None] * len(mod) if falta("EST_DIS")
            else [_llave(r[ix["EST_DIS"]]) for r in mod])
    upms = ([None] * len(mod) if falta("UPM_DIS")
            else [_llave(r[ix["UPM_DIS"]]) for r in mod])

    def emite(suf, sel, dfun, nombre_den):
        """Estima p, IC y embudo sobre las filas que `sel` marca."""
        w, d, e, u = [], [], [], []
        for i, r in enumerate(mod):
            if pes[i] is None or not sel(r):
                continue
            w.append(pes[i])
            d.append(dfun(r))
            e.append(ests[i])
            u.append(upms[i])
        put(f"{suf}-N-DENOMINADOR", len(w))
        put(f"{suf}-DENOMINADOR", nombre_den)
        if not w:
            put(f"{suf}-P", "NO-ESTIMABLE-UNIVERSO-VACIO")
            put(f"{suf}-IC-LO", None)
            put(f"{suf}-IC-HI", None)
            put(f"{suf}-METODO-IC", "NO-ESTIMABLE-UNIVERSO-VACIO")
            return None
        p, sw = _p(w, d)
        lo, hi, n_e, n_u, n_1, met, n_sd = _ic(w, d, e, u)
        put(f"{suf}-P", _redondea(p))
        put(f"{suf}-IC-LO", _redondea(lo))
        put(f"{suf}-IC-HI", _redondea(hi))
        put(f"{suf}-METODO-IC", met)
        put(f"{suf}-N-ESTRATOS", n_e)
        put(f"{suf}-N-UPM", n_u)
        put(f"{suf}-N-ESTRATOS-UPM-UNICA", n_1)
        put(f"{suf}-N-SIN-DISENO", n_sd)
        put(f"{suf}-PESO-DENOMINADOR", round(sw, 3))
        return p

    # ══ FAMILIA A ════════════════════════════════════════════════════════
    a_ok = not (falta("P4_10") or falta("P3_13"))
    if not a_ok:
        for s in ("A-P-CORTO-SIN", "A-P-NOCORTO-SIN",
                  "A-P-CORTO-CON", "A-P-NOCORTO-CON",
                  "A-P-CORTO-SIN-S1", "A-P-CORTO-CON-S1"):
            put(f"{s}-P", "NO-ESTIMABLE-COLUMNA-AUSENTE")
    else:
        def sel_a(ss):
            return lambda r: (col(r, "P3_13") in ss
                              and col(r, "P4_10") in A_P410_VALIDOS)

        d_corto = lambda r: col(r, "P4_10") in A_CORTO          # noqa: E731
        d_nocorto = lambda r: col(r, "P4_10") in A_NOCORTO      # noqa: E731
        d_corto_s1 = lambda r: col(r, "P4_10") in A_CORTO_S1    # noqa: E731

        den_sin = ("personas 18+ con trabajo SIN seguridad social "
                   "(P3_13='7') y P4_10 valido")
        den_con = ("personas 18+ con trabajo CON seguridad social "
                   "(P3_13 in {1,2,3,4}) y P4_10 valido")

        emite("A-P-CORTO-SIN", sel_a(A_SIN_SS), d_corto, den_sin)
        emite("A-P-NOCORTO-SIN", sel_a(A_SIN_SS), d_nocorto, den_sin)
        emite("A-P-CORTO-CON", sel_a(A_CON_SS), d_corto, den_con)
        emite("A-P-NOCORTO-CON", sel_a(A_CON_SS), d_nocorto, den_con)
        # sensibilidad S1 — el corte de GEN1, declarado, NO el reportado
        emite("A-P-CORTO-SIN-S1", sel_a(A_SIN_SS), d_corto_s1, den_sin)
        emite("A-P-CORTO-CON-S1", sel_a(A_CON_SS), d_corto_s1, den_con)

        # complementos de §5.2 — con denominador escrito, sin rango medido
        tot = sum(p for p in pes if p is not None)
        put("A-C-PESO-TOTAL-18MAS", round(tot, 3))
        for nom, cj in (("FUERA-DEL-EJE", A_FUERA), ("SIN-EJE-BLANCO", None)):
            pw = 0.0
            nn = 0
            for i, r in enumerate(mod):
                if pes[i] is None:
                    continue
                v = col(r, "P3_13")
                hit = (v in cj) if cj is not None else (v in ("", "b"))
                if hit:
                    pw += pes[i]
                    nn += 1
            put(f"A-C-{nom}-N", nn)
            put(f"A-C-{nom}-PESO", round(pw, 3))
            put(f"A-C-{nom}-FRACCION",
                _redondea(pw / tot) if tot > 0 else None)
            put(f"A-C-{nom}-DENOMINADOR", "personas 18+ con FAC_PER valido")
        for ss, et in ((A_SIN_SS, "SIN"), (A_CON_SS, "CON")):
            nn = sum(1 for i, r in enumerate(mod)
                     if pes[i] is not None
                     and col(r, "P3_13") in ss
                     and col(r, "P4_10") in A_P410_FALTA)
            put(f"A-C-FALTANTE-P410-{et}-N", nn)

    # ══ FAMILIA B ════════════════════════════════════════════════════════
    faltan_b = [c for c in INFORMAL + FORMAL if falta(c)]
    if faltan_b:
        put("B-P-FORMAL-P", "NO-ESTIMABLE-COLUMNA-AUSENTE:"
                            + ";".join(faltan_b))
        put("B-P-INFORMAL-P", "NO-ESTIMABLE-COLUMNA-AUSENTE:"
                              + ";".join(faltan_b))
    else:
        d_for = lambda r: any(col(r, c) in B_SI for c in FORMAL)   # noqa: E731
        d_inf = lambda r: any(col(r, c) in B_SI for c in INFORMAL)  # noqa: E731
        den_b = "TODA la poblacion 18+ con FAC_PER valido (denominador COMPARTIDO)"
        pf = emite("B-P-FORMAL", lambda r: True, d_for, den_b)
        pi = emite("B-P-INFORMAL", lambda r: True, d_inf, den_b)

        # la suma se REPORTA, jamas se corrige (Astra §2.4)
        if pf is not None and pi is not None:
            put("B-SUMA-FORMAL-MAS-INFORMAL", _redondea(pf + pi))
            put("B-SUMA-EXCEDE-1", "SI" if (pf + pi) > 1.0 else "NO")
        else:
            put("B-SUMA-FORMAL-MAS-INFORMAL", None)
            put("B-SUMA-EXCEDE-1", "NO-ESTIMABLE")
        put("B-NOTA-COEXISTENCIA",
            "formal e informal COEXISTEN; la suma NO se fuerza a 1, no se "
            "normaliza y no se re-escala. Una suma > 1 es coexistencia, no "
            "defecto.")

        # complementos: ambas vias / ninguna via
        tot = sum(p for p in pes if p is not None)
        for nom, f in (("AMBAS-VIAS", lambda r: d_for(r) and d_inf(r)),
                       ("NINGUNA-VIA",
                        lambda r: (not d_for(r)) and (not d_inf(r)))):
            pw = 0.0
            nn = 0
            for i, r in enumerate(mod):
                if pes[i] is None:
                    continue
                if f(r):
                    pw += pes[i]
                    nn += 1
            put(f"B-C-{nom}-N", nn)
            put(f"B-C-{nom}-PESO", round(pw, 3))
            put(f"B-C-{nom}-FRACCION",
                _redondea(pw / tot) if tot > 0 else None)
            put(f"B-C-{nom}-DENOMINADOR", den_b)

        # control interno contra FILTRO_S5_1 — no es fuente
        if falta("FILTRO_S5_1"):
            put("B-CONTROL-FILTRO-S5-1", "NO-ESTIMABLE-COLUMNA-AUSENTE")
        else:
            disc = sum(1 for r in mod
                       if (col(r, "FILTRO_S5_1") == "1") != d_for(r))
            put("B-CONTROL-FILTRO-S5-1-N-DISCREPANTES", disc)
            put("B-CONTROL-FILTRO-S5-1",
                "COINCIDE" if disc == 0 else "DISCREPA · NO SE AJUSTA NINGUNA")

    # ══ FAMILIA C ════════════════════════════════════════════════════════
    if falta("P5_20") or falta("P5_23"):
        put("C-P-DESCONFIA-CONOCE-P", "NO-ESTIMABLE-COLUMNA-AUSENTE")
        put("C-P-DESCONFIA-NOCONOCE-P", "NO-ESTIMABLE-COLUMNA-AUSENTE")
    elif not c1_ok:
        put("C-P-DESCONFIA-CONOCE-P", "NO-ESTIMABLE-EJE-NO-ES-PARTICION")
        put("C-P-DESCONFIA-NOCONOCE-P", "NO-ESTIMABLE-EJE-NO-ES-PARTICION")
    elif not c2_ok:
        put("C-P-DESCONFIA-CONOCE-P", "NO-ESTIMABLE-DENOMINADOR-C-NO-VERIFICADO")
        put("C-P-DESCONFIA-NOCONOCE-P",
            "NO-ESTIMABLE-DENOMINADOR-C-NO-VERIFICADO")
    else:
        def sel_c(eje):
            return lambda r: (col(r, "P5_20") in C_P520_VALIDOS
                              and col(r, "P5_23") in eje)

        d_desc = lambda r: col(r, "P5_20") in C_DESCONFIA  # noqa: E731
        emite("C-P-DESCONFIA-CONOCE", sel_c(C_CONOCE), d_desc,
              "personas 18+ SIN CUENTA que SI conocen la proteccion "
              "(P5_20 valido y P5_23='1')")
        emite("C-P-DESCONFIA-NOCONOCE", sel_c(C_NO_CONOCE), d_desc,
              "personas 18+ SIN CUENTA que NO conocen la proteccion "
              "(P5_20 valido y P5_23='2')")
        for eje, et in ((C_CONOCE, "CONOCE"), (C_NO_CONOCE, "NOCONOCE")):
            pw = 0.0
            nn = 0
            for i, r in enumerate(mod):
                if pes[i] is None or not sel_c(eje)(r):
                    continue
                if col(r, "P5_20") in C_OTRAS:
                    pw += pes[i]
                    nn += 1
            put(f"C-C-OTRAS-RAZONES-{et}-N", nn)
            put(f"C-C-OTRAS-RAZONES-{et}-PESO", round(pw, 3))
        put("C-NOTA-NO-SUMAR",
            "C-P-DESCONFIA-CONOCE y C-P-DESCONFIA-NOCONOCE tienen "
            "DENOMINADORES DISTINTOS: su suma no significa nada.")

    # ── razon principal vs cualquier razon (el encargo lo pide) ──────────
    put("C-CUALQUIER-RAZON", "NO-APLICA")
    put("C-CUALQUIER-RAZON-JUSTIFICACION",
        "P5_20 es de RESPUESTA UNICA (FD: Alfanumerico tamanio 2, codigos "
        "01-10). ENIF 2024 no trae bateria de menciones multiples para 5.20 "
        "(contraste: 5.7, 5.8, 5.15 y 5.17 si lo son). NO-APLICA es un valor, "
        "no un hueco.")

    # ── recordatorio A-bis.3, en el propio resultado ─────────────────────
    put("G-NOTA-IC-NO-COMPARABLE",
        "Fase 1 (FP-201) midio SIN diseno; esta corrida SI lo estima. Los IC "
        "NO son comparables con los de fase 1 y no se comparan: el control "
        "positivo compara SOLO el punto (A-bis.3).")
    put("G-NOTA-FP-201",
        "FP-201 declaro «sin campo de diseno UPM/estrato reproducible» para "
        "ENIF. El FD de ENIF 2024 trae EST_DIS, UPM_DIS y FAC_PER en TMODULO: "
        "FP-201 es FALSO tambien para ENIF. Cierra la parte ENIF de NC-0086.")

    return R
