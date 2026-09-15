"""`CALC-ENSANUT-0001` -- Rama B de `prereg-caja-S7-L17` v1.1 sobre ENSANUT 2024
adultos: proporcion ponderada de MENCIONES de no-vacunacion cuya razon es
logistica (no habia vacunas / no estaba quien aplica), con IC de diseno
(`est_sel`, `upm`), complemento CONTADO, rama B por PERSONA y desglose por
razon y por vacuna.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO POR `ACTO GEN2-MEDICION-DEMANDA-1` (CAJA, 15/sep/2026) EN
UN COMMIT PROPIO, ANTES DE ABRIR UN SOLO BYTE DE MICRODATO, contra el contrato
que `ACTO GEN2-SPECS-DEMANDA-1` (tanda 2) congelo en NUBE. Probado solo contra
un payload SINTETICO (.dta fabricado con pandas, dentro de un ZIP).

Lo que decide el CODIGO y no la spec, declarado aqui: (1) el `.dta` se
extrae del ZIP a un archivo temporal para `pyreadstat.read_dta` (que no lee
bytes en memoria); (2) la «mencion afirmativa» es el codigo `1` de cada
columna `a0927{a..e}{1..4}` -- la etiqueta de valor del propio `.dta` es
`{1: 'Si', 2: 'No'}` (codebook, leido con `metadataonly=True`) y es el mismo
criterio del script GEN1 (`tools/medidor_l17_vacunacion_disponible.py`,
`df[col] == 1`); se aplica DESPUES de emitir el soporte observado del bloque
como RESULT, y un codigo fuera de `{1, 2}` produce
`NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA`; las llaves opacas (`est_sel`, `upm`,
`estrato`, `FOLIO_I`) se toman como texto: un double entero `12.0` es `'12'`; (3) «respuesta ausente» = celda NaN/vacia del bloque: se cuenta en
`A-N-MENCION-AUSENTE` y no entra a ningun lado; (4) el folio de persona es
`FOLIO_I` (el que usa GEN1), leido como texto; (5) el orden fijo de sumas es
`(FOLIO_I, columna)`; (6) la cota de n (10) se aplica al NUMERADOR de la
primaria (menciones logisticas) y, en `C-P-POR-VACUNA`, al numerador de cada
vacuna; (7) el IC se calcula sobre las menciones del universo CON diseno; (8)
una guardia ESTRUCTURAL deja punto e IC en `null`, escribe el codigo
`NO-ESTIMABLE-…` en los RESULT de texto que dependen del punto y devuelve los
conteos alcanzados. Las referencias GEN1 llegan por `contrato["parametros"]`.
"""
# ── bloque comun de los cuatro medidores de ACTO GEN2-MEDICION-DEMANDA-1 ──
# (se deposita byte a byte en cada medidor: cada CALC es autocontenido)
from __future__ import annotations

import io
import re
import zipfile

import numpy as np
import pandas as pd

SEP = "␟"  # separador de la clave (estrato, upm); nunca aparece en un id INEGI


def _num(v):
    """`NO-ESTIMABLE` viaja como `null`, nunca como NaN ni como cadena."""
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _perfil(valores) -> str:
    """'ancho=k:n_filas;...' sobre el TEXTO CRUDO de una llave opaca."""
    anchos: dict[int, int] = {}
    for v in valores:
        anchos[len(v)] = anchos.get(len(v), 0) + 1
    return ";".join(f"ancho={k}:{anchos[k]}" for k in sorted(anchos)) or "vacio"


def _norm(col: str) -> str:
    """BOM (ya decodificado en latin-1 o no), comillas y espacios fuera. La
    caja se conserva: la identidad de la columna la resuelve `_col`."""
    return col.lstrip("﻿").lstrip("ï»¿").strip().strip('"').strip()


def _miembro(zf: zipfile.ZipFile, nombre: str):
    """Miembro del ZIP: ruta exacta, o -- si `nombre` no trae directorio --
    el UNICO miembro cuyo nombre base coincide sin distinguir caja. Dos
    candidatos no se desempatan: elegir seria elegir el dato."""
    nombres = zf.namelist()
    if nombre in nombres:
        return nombre
    if "/" not in nombre:
        cand = [n for n in nombres if n.rsplit("/", 1)[-1].lower() == nombre.lower()]
        if len(cand) == 1:
            return cand[0]
    return None


def _lee_csv(zf: zipfile.ZipFile, miembro: str, columnas: list[str],
             dtype_str=()):
    """Lee SOLO `columnas` de un CSV del ZIP. Bytes normalizados (`\\r\\n` y
    `\\r` -> `\\n`: los CSV de datos abiertos de INEGI traen terminadores
    mixtos), decodificados en latin-1 (total sobre bytes; todo campo usado es
    ASCII). Devuelve `(df, faltantes, n_columnas)`; si falta una columna
    declarada, `df` es None y `faltantes` la nombra. Las columnas se
    resuelven por nombre exacto y, si no, por sufijo (BOM pegado al primer
    nombre); la caja se compara en MAYUSCULAS."""
    crudo = zf.read(miembro).replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    cabecera = [_norm(c) for c in crudo.split(b"\n", 1)[0].decode("latin-1").split(",")]
    mapa, faltantes = {}, []
    for c in columnas:
        exactos = [h for h in cabecera if h.upper() == c.upper()]
        if not exactos:
            exactos = [h for h in cabecera if h.upper().endswith(c.upper())]
        if len(exactos) != 1:
            faltantes.append(c)
        else:
            mapa[exactos[0]] = c
    if faltantes:
        return None, faltantes, len(cabecera)
    inverso = {v: k for k, v in mapa.items()}
    df = pd.read_csv(io.BytesIO(crudo), encoding="latin-1", low_memory=False,
                     dtype=str, keep_default_na=False)
    df.columns = [_norm(c) for c in df.columns]
    df = df[[inverso[c] for c in columnas]].rename(columns=mapa)
    return df, [], len(cabecera)


def _texto(serie: pd.Series) -> np.ndarray:
    """Texto crudo con `strip()`; el vacio queda vacio (nunca 'nan')."""
    return serie.fillna("").astype(str).str.strip().to_numpy()


def _flotante(serie: pd.Series) -> np.ndarray:
    """Texto -> float64; vacio o no numerico -> NaN. Nada se imputa."""
    return pd.to_numeric(serie.replace("", np.nan), errors="coerce").to_numpy("float64")


def _claves_diseno(estrato, upm):
    claves = np.array([f"{e}{SEP}{u}" for e, u in zip(estrato, upm)])
    upm_unicas, inverso = np.unique(claves, return_inverse=True)
    estr_de_upm = np.array([k.split(SEP)[0] for k in upm_unicas])
    return upm_unicas, inverso, estr_de_upm


def _bootstrap(num, den, estrato, upm, replicas, semilla):
    """Bootstrap de UPM CON REEMPLAZO dentro de cada estrato, conservando el
    numero de UPM por estrato; un estrato con UNA sola UPM se re-muestrea a
    si mismo (varianza cero, contado en `n_una`). Devuelve la serie de
    replicas de `sum(num)/sum(den)` sobre conglomerados ya agregados
    (numerador y denominador DE LA MISMA replica), y los conteos
    (n_estratos, n_upm, n_estratos_de_upm_unica). `num` y `den` ya vienen
    multiplicados por el ponderador."""
    n = len(estrato)
    if n == 0:
        return None, 0, 0, 0
    upm_unicas, inverso, estr_de_upm = _claves_diseno(estrato, upm)
    n_upm = len(upm_unicas)
    estratos = np.unique(estr_de_upm)
    s_num = np.bincount(inverso, weights=num, minlength=n_upm)
    s_den = np.bincount(inverso, weights=den, minlength=n_upm)
    rng = np.random.Generator(np.random.PCG64(semilla))
    a_num, a_den = np.zeros(replicas), np.zeros(replicas)
    n_una = 0
    for e in estratos:
        pos = np.flatnonzero(estr_de_upm == e)
        k = len(pos)
        if k == 1:
            n_una += 1
            a_num += s_num[pos[0]]
            a_den += s_den[pos[0]]
            continue
        elegidas = rng.integers(0, k, size=(replicas, k))
        a_num += s_num[pos][elegidas].sum(axis=1)
        a_den += s_den[pos][elegidas].sum(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        serie = np.where(a_den > 0, a_num / np.where(a_den > 0, a_den, 1.0), np.nan)
    return serie, len(estratos), n_upm, n_una


def _ic(serie, replicas):
    if serie is None:
        return None, None
    fin = serie[np.isfinite(serie)]
    if fin.size < replicas // 2:
        return None, None
    return float(np.percentile(fin, 2.5)), float(np.percentile(fin, 97.5))


def _conteo_upm_unica(estrato, upm):
    if len(estrato) == 0:
        return 0, 0, 0
    _u, _i, estr_de_upm = _claves_diseno(estrato, upm)
    _e, cuenta = np.unique(estr_de_upm, return_counts=True)
    return len(_e), len(_u), int(np.sum(cuenta == 1))
import os
import tempfile

import pyreadstat


def _llave(v) -> str:
    """Llave opaca desde un valor del .dta: NaN/None -> ''; un double entero
    (12.0) -> '12' (es como lo escribe Stata en su etiqueta); lo demas, texto
    con strip()."""
    if v is None:
        return ""
    if isinstance(v, float):
        if v != v:
            return ""
        return str(int(v)) if v == int(v) else repr(v)
    t = str(v).strip()
    return "" if t.lower() == "nan" else t


def _codigo(v):
    if v is None:
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        t = str(v).strip()
        if not t or t.lower() == "nan":
            return None
        try:
            f = float(t)
        except ValueError:
            return None
    if f != f:
        return None
    return int(f) if f == int(f) else None


# ── medicion ──────────────────────────────────────────────────────────────

P = "RESULT-ENSANUT-"
ZIP_ID = "adultos_ensanut2024_w_stata_stata__v2026_09_01"
RAZONES = {"a": "no_habia_vacunas", "b": "no_derechohabiente",
           "c": "no_estaba_quien_aplica", "d": "enfermo", "e": "otra_razon"}
LOGISTICA = {"a", "c"}
VACUNAS = ["1", "2", "3", "4"]
FOLIO = "FOLIO_I"
ORDEN_DESGLOSE = ["no_habia_vacunas", "no_estaba_quien_aplica", "no_derechohabiente",
                  "enfermo", "otra_razon"]


def medir(inputs, contrato):
    p = contrato["parametros"]
    replicas = int(p["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    tol = 1.0e-10  # espejo de `tolerancia.abs` de la spec
    cota = int(p["cota_n_minima"])
    g1 = p["valores_gen1_referencia"]
    n1 = p["n_gen1_referencia"]
    grano = int(p["grano_gen1_decimales"])
    miembro_decl = p["miembros_zip_declarados"][0]
    vac_nombre = {str(k): str(v) for k, v in p["vacunas"].items()}
    cols = [f"a0927{l}{v}" for l in RAZONES for v in VACUNAS]

    out: dict[str, object] = {}

    def no_estimable(codigo: str):
        for k in ("A-P-LOGISTICA", "A-P-NO-LOGISTICA", "A-IC-LO", "A-IC-HI",
                  "A-DELTA-VS-GEN1", "B-P-PERSONA", "B-DELTA-MENCION-VS-PERSONA"):
            out.setdefault(P + k, None)
        for k in ("A-SUMA-UNO", "A-METODO-IC", "A-REPRODUCE-GEN1", "G-SOPORTE-A0927",
                  "G-PERFIL-EST-SEL", "G-PERFIL-ESTRATO", "G-PERFIL-UPM",
                  "A-DESGLOSE-RAZONES", "A-DESGLOSE-COINCIDE-GEN1", "C-P-POR-VACUNA"):
            out.setdefault(P + k, codigo)
        for k in ("G-N-FILAS-ADULTOS", "G-N-COLUMNAS-A0927", "G-N-ESTRATOS-UPM-UNICA",
                  "A-N-MENCIONES", "A-N-PERSONAS", "A-N-PERSONAS-MULTIMENCION",
                  "A-N-SIN-PONDERADOR", "A-N-SIN-DISENO", "A-N-MENCION-AUSENTE"):
            out.setdefault(P + k, 0)
        out[P + "A-ADOPCION"] = "NO-ADOPTABLE-NO-ESTIMABLE"
        return out

    # ── G · estructura ────────────────────────────────────────────────────
    zf = zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"])
    out[P + "G-N-MIEMBROS-ZIP"] = len(zf.namelist())
    miembro = _miembro(zf, miembro_decl)
    if miembro is None:
        return no_estimable(f"NO-ESTIMABLE-MIEMBRO-AUSENTE:{miembro_decl}")
    with tempfile.TemporaryDirectory() as td:
        ruta = os.path.join(td, "adultos.dta")
        with open(ruta, "wb") as fh:
            fh.write(zf.read(miembro))
        _df0, meta = pyreadstat.read_dta(ruta, metadataonly=True)
        presentes = {c.lower(): c for c in meta.column_names}
        out[P + "G-N-COLUMNAS-A0927"] = sum(1 for c in cols if c in presentes)
        faltan = [c for c in cols if c not in presentes]
        if faltan:
            return no_estimable(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{faltan[0]}")
        for c in (FOLIO.lower(), "ponde_f", "estrato", "est_sel", "upm"):
            if c not in presentes:
                return no_estimable(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{c}")
        usar = [presentes[c] for c in [FOLIO.lower(), "ponde_f", "estrato", "est_sel", "upm"] + cols]
        df, _meta = pyreadstat.read_dta(ruta, usecols=usar)
    df.columns = [c.lower() for c in df.columns]
    out[P + "G-N-FILAS-ADULTOS"] = int(len(df))
    if len(df) == 0:
        return no_estimable("NO-ESTIMABLE-UNIVERSO-VACIO")
    folio = np.array([_llave(v) for v in df[FOLIO.lower()].to_numpy()])
    est_sel = np.array([_llave(v) for v in df["est_sel"].to_numpy()])
    estrato = np.array([_llave(v) for v in df["estrato"].to_numpy()])
    upm = np.array([_llave(v) for v in df["upm"].to_numpy()])
    w = pd.to_numeric(df["ponde_f"], errors="coerce").to_numpy("float64")

    # soporte del bloque, ANTES del mapa
    bloque = {c: np.array([_codigo(v) for v in df[c].to_numpy()], dtype=object) for c in cols}
    conteo: dict[str, int] = {}
    n_ausente = 0
    for c in cols:
        for v in bloque[c]:
            if v is None:
                n_ausente += 1
            else:
                conteo[str(v)] = conteo.get(str(v), 0) + 1
    out[P + "G-SOPORTE-A0927"] = ";".join(f"{k}:{conteo[k]}" for k in sorted(conteo, key=lambda x: (len(x), x))) or "vacio"
    out[P + "A-N-MENCION-AUSENTE"] = int(n_ausente)
    if not set(conteo) <= {"1", "2"}:
        # el codebook del .dta etiqueta el bloque {1: Si, 2: No}; otro codigo
        # no se adivina: se declara y la corrida no estima
        return no_estimable("NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA")

    # ── A · una fila = una mencion (persona x razon x vacuna) ─────────────
    filas = []
    for l, nombre in RAZONES.items():
        for v in VACUNAS:
            c = f"a0927{l}{v}"
            m = np.array([x == 1 for x in bloque[c]])
            for i in np.flatnonzero(m):
                filas.append((folio[i], c, nombre, l in LOGISTICA, v, w[i], est_sel[i], upm[i], estrato[i]))
    men = pd.DataFrame(filas, columns=["folio", "col", "razon", "log", "vac", "w", "est", "upm", "estrato"])
    men = men.sort_values(["folio", "col"], kind="stable").reset_index(drop=True)
    out[P + "A-N-MENCIONES"] = int(len(men))
    out[P + "A-N-PERSONAS"] = int(men["folio"].nunique())
    por_persona = men.groupby("folio").size()
    out[P + "A-N-PERSONAS-MULTIMENCION"] = int((por_persona > 1).sum())
    cnt = men["razon"].value_counts().to_dict()
    out[P + "A-DESGLOSE-RAZONES"] = ";".join(f"{r}:{int(cnt.get(r, 0))}" for r in ORDEN_DESGLOSE)
    difs = []
    for r in ORDEN_DESGLOSE:
        d = int(cnt.get(r, 0)) - int(n1[r])
        if d != 0:
            difs.append(f"{r}{d:+d}")
    dt = int(len(men)) - int(n1["menciones"])
    if dt != 0:
        difs.append(f"menciones{dt:+d}")
    dp = int(men["folio"].nunique()) - int(n1["personas"])
    if dp != 0:
        difs.append(f"personas{dp:+d}")
    out[P + "A-DESGLOSE-COINCIDE-GEN1"] = "COINCIDE" if not difs else "DIFIERE:" + ",".join(difs)
    if len(men) == 0:
        return no_estimable("NO-ESTIMABLE-UNIVERSO-VACIO")

    wm = men["w"].to_numpy("float64")
    con_w = np.isfinite(wm) & (wm > 0)
    out[P + "A-N-SIN-PONDERADOR"] = int(np.sum(~con_w))
    u = con_w
    est = men["est"].to_numpy(); upmm = men["upm"].to_numpy()
    con_dis = (est != "") & (upmm != "")
    out[P + "A-N-SIN-DISENO"] = int(np.sum(u & ~con_dis))
    out[P + "G-PERFIL-EST-SEL"] = _perfil(est[u])
    out[P + "G-PERFIL-UPM"] = _perfil(upmm[u])
    ev, ec = np.unique(men["estrato"].to_numpy()[u], return_counts=True)
    out[P + "G-PERFIL-ESTRATO"] = ";".join(f"{a if a else '<vacio>'}:{b}" for a, b in zip(ev, ec)) or "vacio"
    _e, _n, n_una = _conteo_upm_unica(est[u & con_dis], upmm[u & con_dis])
    out[P + "G-N-ESTRATOS-UPM-UNICA"] = n_una
    if not u.any():
        return no_estimable("NO-ESTIMABLE-UNIVERSO-VACIO")
    dl = men["log"].to_numpy().astype("float64")
    dn = (~men["log"].to_numpy()).astype("float64")
    n_log = int(np.sum(dl[u]))
    if n_log < cota:
        return no_estimable("NO-ESTIMABLE-N-INSUFICIENTE")
    sw = float(np.sum(wm[u]))
    pl = float(np.sum(wm[u] * dl[u]) / sw)
    pn = float(np.sum(wm[u] * dn[u]) / sw)
    out[P + "A-P-LOGISTICA"] = _num(pl)
    out[P + "A-P-NO-LOGISTICA"] = _num(pn)
    residuo = pl + pn - 1.0
    out[P + "A-SUMA-UNO"] = "SI" if abs(residuo) <= tol else f"NO:{residuo!r}"
    m = u & con_dis
    if not m.any():
        lo = hi = None
        metodo = "NO-ESTIMABLE-DISENO-INCOMPLETO"
    else:
        serie, _e, _n, una = _bootstrap(wm[m] * dl[m], wm[m], est[m], upmm[m], replicas, semilla)
        lo, hi = _ic(serie, replicas)
        metodo = "IC-DE-DISENO" if una == 0 else "IC-CON-ESTRATOS-DE-UPM-UNICA"
    out[P + "A-IC-LO"] = _num(lo)
    out[P + "A-IC-HI"] = _num(hi)
    out[P + "A-METODO-IC"] = metodo
    out[P + "A-DELTA-VS-GEN1"] = _num(pl - float(g1["A_P_LOGISTICA"]))
    reproduce = round(pl, grano) == round(float(g1["A_P_LOGISTICA"]), grano)
    out[P + "A-REPRODUCE-GEN1"] = "REPRODUCE" if reproduce else "NO-REPRODUCE"
    out[P + "A-ADOPCION"] = ("LISTADO-PARA-MESA-REPRODUCE" if reproduce
                             else "LISTADO-PARA-MESA-NO-REPRODUCE")

    # ── B · persona: alguna mencion logistica ─────────────────────────────
    per = men[u].groupby("folio", sort=True).agg(log=("log", "max"), w=("w", "first"))
    swp = float(np.sum(per["w"].to_numpy("float64")))
    pb = float(np.sum(per["w"].to_numpy("float64") * per["log"].to_numpy().astype("float64")) / swp) if swp > 0 else None
    out[P + "B-P-PERSONA"] = _num(pb)
    out[P + "B-DELTA-MENCION-VS-PERSONA"] = _num(pl - pb) if pb is not None else None

    # ── C · por vacuna ────────────────────────────────────────────────────
    partes = []
    for v in VACUNAS:
        mv = u & (men["vac"].to_numpy() == v)
        nv = int(np.sum(dl[mv]))
        if nv < cota:
            partes.append(f"{vac_nombre.get(v, v)}=NO-ESTIMABLE-N-INSUFICIENTE:{int(np.sum(mv))}")
            continue
        pv = float(np.sum(wm[mv] * dl[mv]) / np.sum(wm[mv]))
        partes.append(f"{vac_nombre.get(v, v)}={pv:.6f}:{int(np.sum(mv))}")
    out[P + "C-P-POR-VACUNA"] = ";".join(partes)
    return out
