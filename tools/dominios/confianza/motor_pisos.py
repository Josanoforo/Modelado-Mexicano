#!/usr/bin/env python3
"""Motor común de pisos por segmento · ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1.

Lo consumen los cuatro medidores del acto (CALC-WVS-PISOS-2018-0001,
CALC-LATINOBAROMETRO-PISOS-2023-0001, CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001,
CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001) como input `origen: repo` fijado por sha256 y
ejecutado desde sus bytes. La estimación (razón ponderada, bootstrap de UPM dentro de
estrato, contrato conservador, τ² e IC calibrado de persistencia) NO vive aquí: vive en la
receta de GEN2-SALUD-Y-BIENESTAR-PISOS-1 (`tools/dominios/salud/pisos_diseno.py`), que
cada medidor carga también por sha256 y pasa como `R`.

QUÉ AÑADE, y nada más:
  · lectura de un .dta suelto o dentro de un ZIP, o de un .sav dentro de un ZIP, con
    filtro de filas por país ANTES de devolver (el resto de países nunca sale de aquí);
  · recodificación declarativa: `("bin", col, uno, cero)` → 1/0/NaN; `("media", col, lo, hi)`
    → valor en [lo, hi] o NaN. Todo código fuera de `uno ∪ cero` (o del rango) es NaN:
    no sabe, no responde, no aplica y faltantes extendidos de Stata quedan fuera;
  · ejes: sexo, edad (18–29/30–44/45–59/60+), categorías por mapa de códigos;
  · diseño: si el medidor no declara estrato o UPM, estrato único y cada entrevista su
    propia UPM (bootstrap ponderado de individuos, «MAS-PONDERADO»); se reporta cuál;
  · ids RESULT `<P>-<CONDUCTA>-<OLA>-<EJE>-<CAT>-<Q>` y el esquema que los declara.
"""
from __future__ import annotations

import math
import os
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

EDADES = (("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 130))
QS = (("P", "p"), ("EE", "ee"), ("IC-LO", "lo"), ("IC-HI", "hi"))


# ═══════════════════════════ lectura ═══════════════════════════

def _lee(ruta_local, columnas, sufijo, encoding):
    import pyreadstat

    lector = pyreadstat.read_sav if sufijo == ".sav" else pyreadstat.read_dta
    kw = {"encoding": encoding} if encoding else {}
    _, meta = lector(str(ruta_local), metadataonly=True, **kw)
    reales = {c.lower(): c for c in meta.column_names}
    faltan = [c for c in columnas if c.lower() not in reales]
    if faltan:
        raise KeyError(f"columnas ausentes: {faltan}")
    df, _ = lector(str(ruta_local), usecols=[reales[c.lower()] for c in columnas],
                   apply_value_formats=False, **kw)
    df.columns = [c.lower() for c in df.columns]
    return df


def lee(ruta, columnas, miembro_sufijo=None, miembro=None, pais=None, encoding=None):
    """DataFrame con `columnas` (minúsculas). `pais=(col, codigo)` filtra filas antes de devolver.

    `ruta` es un .dta suelto, o un ZIP del que se extrae el único miembro que termina en
    `miembro_sufijo` (o el `miembro` nombrado) a un directorio temporal que se borra.
    """
    ruta = Path(ruta)
    cols = list(dict.fromkeys(list(columnas) + ([pais[0]] if pais else [])))
    if ruta.suffix.lower() == ".zip":
        with zipfile.ZipFile(ruta) as z:
            if miembro is None:
                cand = [n for n in z.namelist() if n.lower().endswith(miembro_sufijo.lower())
                        and not n.startswith("__MACOSX")]
                if len(cand) != 1:
                    raise ValueError(f"{ruta.name}: se esperaba 1 miembro *{miembro_sufijo}, hay {cand}")
                miembro = cand[0]
            suf = Path(miembro).suffix.lower()
            with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as tmp:
                destino = Path(tmp) / f"m{suf}"
                destino.write_bytes(z.read(miembro))
                df = _lee(destino, cols, suf, encoding)
    else:
        df = _lee(ruta, cols, ruta.suffix.lower(), encoding)
    if pais:
        v = pd.to_numeric(df[pais[0].lower()], errors="coerce").to_numpy()
        df = df[v == pais[1]].reset_index(drop=True)
    return df


def num(serie):
    return pd.to_numeric(serie, errors="coerce").to_numpy(dtype=float)


# ═══════════════════════════ recodificación ═══════════════════════════

def recodifica(frame, regla):
    tipo, col = regla[0], regla[1].lower()
    v = num(frame[col])
    if tipo == "bin":
        uno, cero = regla[2], regla[3]
        out = np.full(len(v), np.nan)
        out[np.isin(v, uno)] = 1.0
        out[np.isin(v, cero)] = 0.0
        return out
    if tipo == "media":
        lo, hi = regla[2], regla[3]
        return np.where((v >= lo) & (v <= hi), v, np.nan)
    raise ValueError(f"regla desconocida: {regla}")


def eje_mapa(frame, col, mapa):
    """Categoría (texto) por mapa {cat: códigos}; lo no mapeado queda None."""
    v = num(frame[col.lower()])
    out = np.full(len(v), None, dtype=object)
    for cat, cods in mapa.items():
        out[np.isin(v, cods)] = cat
    return out


def eje_rango(frame, col, rangos):
    """Categoría por rangos cerrados [(cat, lo, hi)] sobre una variable numérica."""
    v = num(frame[col.lower()])
    out = np.full(len(v), None, dtype=object)
    for cat, lo, hi in rangos:
        out[(v >= lo) & (v <= hi)] = cat
    return out


def edad(frame, col):
    return eje_rango(frame, col, EDADES)


# ═══════════════════════════ diseño y estimación ═══════════════════════════

def prepara_diseno(frame, peso=None, estrato=None, upm=None):
    """Añade `_w`, `_est`, `_upm`; devuelve (frame válido, etiqueta de diseño, n descartadas).

    peso None → 1. estrato None → '1'. upm None → índice de fila (cada entrevista su UPM).
    `upm` puede ser tupla de columnas: se concatenan (p. ej. estado × sección).
    Válido: peso finito > 0; estrato y UPM no vacíos.
    """
    f = frame.copy()
    w = np.ones(len(f)) if peso is None else num(f[peso.lower()])
    est = (pd.Series(["1"] * len(f)) if estrato is None
           else f[estrato.lower()].astype(str).str.strip())
    if upm is None:
        u = pd.Series([f"r{i}" for i in range(len(f))])
    else:
        cols = (upm,) if isinstance(upm, str) else tuple(upm)
        u = f[cols[0].lower()].astype(str).str.strip()
        for c in cols[1:]:
            u = u + "|" + f[c.lower()].astype(str).str.strip()
    vacio = {"", "nan", "None", "NaN"}
    ok = (np.isfinite(w) & (w > 0) & ~est.isin(vacio).to_numpy() & ~u.isin(vacio).to_numpy()
          & ~u.str.contains(r"(?:^|\|)(?:nan|None)(?:$|\|)", regex=True).to_numpy())
    f["_w"] = w
    f["_est"] = est.to_numpy()
    f["_upm"] = u.to_numpy()
    etiqueta = ("CONGLOMERADOS" if upm is not None else "MAS-PONDERADO") + \
               ("-ESTRATIFICADO" if estrato is not None else "-SIN-ESTRATO")
    return f[ok].reset_index(drop=True), etiqueta, int((~ok).sum())


def rid(P, conducta, ola, eje, cat, q):
    return f"{P}-{conducta}-{ola}-{eje}-{cat}-{q}"


def fin(x):
    if x is None:
        return None
    x = float(x)
    return x if math.isfinite(x) else None


def mide_ola(R, frame, conductas, ejes, P, ola, replicas, semilla, universo=None):
    """Pisos de una ola. `conductas` {nombre: regla}; `ejes` {eje: (serie, cats)}.

    `universo`: máscara bool (p. ej. edad ≥ 18); fuera → NaN en toda conducta.
    Devuelve dict id → valor para P, EE, IC-LO, IC-HI, N de cada (conducta, eje, cat).
    """
    ys = {}
    for nom, regla in conductas.items():
        y = recodifica(frame, regla)
        if universo is not None:
            y[~universo] = np.nan
        ys[nom] = y
    res = R.marginales(frame, ys, ejes, frame["_w"].to_numpy(), "_est", "_upm", replicas, semilla)
    out = {}
    for nom in conductas:
        for eje, cats in [("TOTAL", ("TODOS",))] + [(e, c) for e, (_, c) in ejes.items()]:
            for cat in cats:
                r = res.get((nom, eje, cat)) or {}
                for q, k in QS:
                    out[rid(P, nom, ola, eje, cat, q)] = fin(r.get(k))
                out[rid(P, nom, ola, eje, cat, "N")] = int(r.get("n", 0))
    return out


def persistencia_icc(R, out, P, conducta, olas, eje, cats):
    """τ² sobre olas consecutivas (logit, sin centrar) y IC calibrado aplicado a la ÚLTIMA ola.

    Devuelve {id: valor} con -ICC-LO/-ICC-HI de la última ola por categoría, más -TAU2 y
    -NDELTAS del grupo (conducta, eje).
    """
    serie = {o: {c: out.get(rid(P, conducta, o, eje, c, "P")) for c in cats} for o in olas}
    t2, nd = R.persistencia(serie, list(olas), list(cats))
    ult = olas[-1]
    extra = {f"{P}-{conducta}-PERSISTENCIA-{eje}-TAU2": fin(t2),
             f"{P}-{conducta}-PERSISTENCIA-{eje}-NDELTAS": int(nd)}
    for c in cats:
        p = out.get(rid(P, conducta, ult, eje, c, "P"))
        lo = out.get(rid(P, conducta, ult, eje, c, "IC-LO"))
        hi = out.get(rid(P, conducta, ult, eje, c, "IC-HI"))
        a, b = R.ic_calibrado(p, lo, hi, t2)
        extra[rid(P, conducta, ult, eje, c, "ICC-LO")] = fin(a)
        extra[rid(P, conducta, ult, eje, c, "ICC-HI")] = fin(b)
    return extra


# ═══════════════════════════ esquema ═══════════════════════════

def fila(i, tipo, unidad):
    f = {"id": i, "tipo": tipo, "unidad": unidad}
    if tipo in ("flotante", "proporcion"):
        f["permite_no_estimable"] = True
    return f


def esquema_ola(P, ola, conductas, ejes_cats):
    """`conductas` {nombre: regla}; `ejes_cats` {eje: cats} (sin TOTAL)."""
    f = []
    for nom, regla in conductas.items():
        media = regla[0] == "media"
        t = "flotante" if media else "proporcion"
        u = (f"media ponderada escala {regla[2]}-{regla[3]}" if media else "proporción ponderada")
        for eje, cats in [("TOTAL", ("TODOS",))] + list(ejes_cats.items()):
            for cat in cats:
                f += [fila(rid(P, nom, ola, eje, cat, "P"), t, u),
                      fila(rid(P, nom, ola, eje, cat, "EE"), "flotante", "error estándar bootstrap"),
                      fila(rid(P, nom, ola, eje, cat, "IC-LO"), t, "IC95 diseño, inferior"),
                      fila(rid(P, nom, ola, eje, cat, "IC-HI"), t, "IC95 diseño, superior"),
                      fila(rid(P, nom, ola, eje, cat, "N"), "entero", "personas sin ponderar")]
    return f


def esquema_persistencia(P, conducta, ult, eje, cats):
    f = [fila(f"{P}-{conducta}-PERSISTENCIA-{eje}-TAU2", "flotante", "τ² logit, media de Δ² sin centrar"),
         fila(f"{P}-{conducta}-PERSISTENCIA-{eje}-NDELTAS", "entero", "Δ definidos")]
    for c in cats:
        f += [fila(rid(P, conducta, ult, eje, c, "ICC-LO"), "proporcion", "IC calibrado de persistencia, inferior"),
              fila(rid(P, conducta, ult, eje, c, "ICC-HI"), "proporcion", "IC calibrado de persistencia, superior")]
    return f
