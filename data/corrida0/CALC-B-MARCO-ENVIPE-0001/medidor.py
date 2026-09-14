"""Medidor de la familia `B-MARCO` -- la linea base temporal `B` extendida, por
serie, a las celdas del marco-M que su fuente permite.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-B-MARCO`, ANTES DE LEER UN
SOLO BYTE DE MICRODATO. Spec sellada que lo gobierna:
`forense/prereg-caja/B-MARCO-spec-v1_0.md` (`prereg-caja-B-MARCO`), sucesora
por extension -- no por reescritura -- de `prereg-caja-B-REMESAS`.

El MISMO archivo se deposita byte a byte en los CALC de las tres series
(ENVIPE, ENCIG, ENIGH). Formato, miembro, columnas, codificacion, olas y
objetivos entran por `contrato["parametros"]`; el codigo no distingue series.

Sucesion de familia, no reescritura: la regla es la MISMA que `CALC-B-0001`
-- persistencia de la ultima ola de la MISMA serie disponible al corte, via
`tools/baseline_temporal.py` sin modificarlo, dos brazos (OPERATIVO /
PERSISTENCIA) que difieren SOLO en `disponible_desde` -- y el bootstrap del
IC es el de `CALC-B-0001` (copiado verbatim), para que la ola ENIGH 2016
reproduzca punto E IC del ensayo original como control positivo.

Lo que este medidor NO hace: no lee R, M ni L -- ni para elegir reglas ni
para comparar. Es B puro (GEN2 limpio, como `CALC-B-0001`): la comparacion
contra el arbitro `R` de cada celda (control positivo y `err_pp`) vive en
`CALC-B-MARCO-MAE-0001`, que es el UNICO de la familia que declara insumos
de `corridas-R` y por tanto el unico envuelto por la regla E.1. No promedia
olas, no ajusta tendencia, no imputa, no rellena celdas sin serie. NINGUNA
cifra suya entra a un veredicto de regla (T9).
"""
from __future__ import annotations

import io
import struct
import sys
import types
import zipfile

import numpy as np
import pandas as pd

BORRADO = 0x2A  # '*' -- registro DBF marcado como borrado


# ── utilidades ────────────────────────────────────────────────────────────

def _num(v):
    """`NO-ESTIMABLE` viaja como `null`, nunca como NaN ni como cadena."""
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _norm(col: str) -> str:
    """BOM fuera, espacios fuera, MAYUSCULAS: ENIGH viene en minusculas,
    ENVIPE en mayusculas y ENCIG cambia de ola en ola. La identidad de una
    columna es su nombre, no su caja."""
    return col.lstrip("﻿").lstrip("ï»¿").strip().strip('"').upper()


def _selector(inputs):
    """Modulo del selector, ejecutado desde los bytes verificados por sha256
    (`origen: repo`). Se registra en `sys.modules` ANTES del `exec`:
    `@dataclass` resuelve anotaciones via `sys.modules[cls.__module__]`
    (COMMIT-1-bis de `GEN2-C0-B`, heredado aqui para no repetirlo)."""
    crudo = inputs["IN-B-SELECTOR"]["bytes"]
    nombre = "baseline_temporal_calc_b_marco"
    mod = types.ModuleType(nombre)
    sys.modules[nombre] = mod
    exec(compile(crudo, "tools/baseline_temporal.py", "exec"), mod.__dict__)
    return mod


def _codigo(s):
    """Texto -> entero, o None si blanco / no numerico. `'01'`, `' 1'` y
    `'1'` son el mismo codigo; el blanco (puros espacios) y `'nan'` no son
    ningun codigo. Nada se imputa."""
    if s is None:
        return None
    t = str(s).strip()
    if not t or t.lower() == "nan":
        return None
    try:
        return int(t)
    except ValueError:
        try:
            f = float(t)
        except ValueError:
            return None
        return int(f) if f == int(f) else None


# ── lectores: DBF desde su descriptor, CSV con BOM y CR normalizados ─────

def _lee_dbf(crudo: bytes, columnas: list[str]) -> pd.DataFrame:
    """Lee un DBF de ancho fijo desde bytes. El ancho y el orden de los campos
    salen del DESCRIPTOR DEL ARCHIVO (32 bytes de cabecera + 32 por campo),
    no del FD: esa es la autoridad. Todo valor se devuelve como TEXTO
    latin-1 SIN recortar -- para llaves opacas (estrato, UPM) el ancho es
    parte de la identidad. Registros BORRADOS (`*`) no entran."""
    nrec, hlen, rlen = struct.unpack("<IHH", crudo[4:12])
    campos, pos, desplazamiento = [], 32, 1
    while pos + 32 <= hlen and crudo[pos] != 0x0D:
        b = crudo[pos:pos + 32]
        nombre = b[0:11].split(b"\x00")[0].decode("latin-1").strip().upper()
        largo = b[16]
        campos.append((nombre, desplazamiento, largo))
        desplazamiento += largo
        pos += 32
    mapa = {n: (o, l) for n, o, l in campos}
    faltan = [c for c in columnas if c.upper() not in mapa]
    if faltan:
        raise RuntimeError(f"DBF: faltan columnas {faltan}; presentes={sorted(mapa)[:40]}…")
    cols = {c: [] for c in columnas}
    for i in range(nrec):
        a = hlen + i * rlen
        reg = crudo[a:a + rlen]
        if len(reg) < rlen:
            break
        if reg[0] == BORRADO:
            continue
        for c in columnas:
            o, l = mapa[c.upper()]
            cols[c].append(reg[o:o + l].decode("latin-1"))
    return pd.DataFrame(cols, dtype=str)


def _lee_csv(ruta_zip: str, directorio: str, columnas: list[str]) -> pd.DataFrame:
    """Un solo CSV de datos por ola bajo `<directorio>/conjunto_de_datos/`.
    Si no hay exactamente uno, la corrida PARA: elegir cual seria elegir el
    dato. Los CSV de datos abiertos de INEGI vienen con BOM y, en ENVIPE,
    con terminador de linea `\\r` SOLO: se normaliza a `\\n` antes de leer.
    Se lee en latin-1 (total sobre bytes; todo campo usado es ASCII)."""
    with zipfile.ZipFile(ruta_zip) as z:
        cand = [n for n in z.namelist()
                if n.startswith(directorio + "/conjunto_de_datos/")
                and n.lower().endswith(".csv") and "bitacora" not in n.lower()]
        if len(cand) != 1:
            raise RuntimeError(
                f"{ruta_zip}: se esperaba UN csv de datos bajo "
                f"{directorio}/conjunto_de_datos/, hay {len(cand)}: {cand}")
        crudo = z.read(cand[0])
    texto = crudo.decode("latin-1").replace("\r\n", "\n").replace("\r", "\n")
    cabecera = [_norm(c) for c in texto.split("\n", 1)[0].strip().split(",")]
    quiero = {c.upper() for c in columnas}
    faltan = sorted(quiero - set(cabecera))
    if faltan:
        raise RuntimeError(f"{ruta_zip}/{directorio}: faltan columnas {faltan}")
    df = pd.read_csv(io.StringIO(texto), dtype=str, low_memory=False,
                     usecols=lambda c: _norm(c) in quiero)
    df.columns = [_norm(c) for c in df.columns]
    # se devuelven con los nombres que la spec declara (caja de la spec)
    return df.rename(columns={c.upper(): c for c in columnas})[list(columnas)]


def _tabla(inputs, ficha, columnas):
    ruta = inputs[ficha["payload_id"]]["ruta_absoluta"]
    if ficha["formato"] == "DBF":
        with zipfile.ZipFile(ruta) as z:
            cand = [n for n in z.namelist() if n.lower() == ficha["miembro"].lower()
                    or n.lower().endswith("/" + ficha["miembro"].lower())]
            if len(cand) != 1:
                raise RuntimeError(f"{ruta}: miembro {ficha['miembro']!r} -> {cand}")
            crudo = z.read(cand[0])
        return _lee_dbf(crudo, columnas)
    if ficha["formato"] == "CSV":
        return _lee_csv(ruta, ficha["directorio"], columnas)
    raise RuntimeError(f"formato no declarado: {ficha.get('formato')!r}")


# ── IC: bootstrap de UPM dentro de estrato, VERBATIM de CALC-B-0001 ──────

def _boot_ic(y, w, est, upm, replicas, semilla, n_min):
    """Bootstrap de UPM CON REEMPLAZO DENTRO DE CADA ESTRATO, conservando el
    numero de UPM por estrato; percentiles 2.5/97.5. Copiado verbatim de
    `data/corrida0/CALC-B-0001/medidor.py` para que la ola ENIGH 2016
    reproduzca sus extremos con la misma semilla (control positivo)."""
    if y.size < n_min:
        return None, None
    clave = np.char.add(np.char.add(est, "|"), upm)
    u_cl, inv = np.unique(clave, return_inverse=True)
    sy = np.bincount(inv, weights=y * w, minlength=u_cl.size)
    sw = np.bincount(inv, weights=w, minlength=u_cl.size)
    est_cl = np.array([c.rsplit("|", 1)[0] for c in u_cl])
    _u_est, inv_est = np.unique(est_cl, return_inverse=True)
    orden = np.argsort(inv_est, kind="stable")
    cuenta = np.bincount(inv_est)
    inicio = np.concatenate(([0], np.cumsum(cuenta)[:-1]))
    ini_slot = inicio[inv_est]
    cnt_slot = cuenta[inv_est]
    rng = np.random.Generator(np.random.PCG64(semilla))
    reps = np.empty(replicas, dtype="float64")
    for i in range(replicas):
        sel = orden[ini_slot + rng.integers(0, cnt_slot)]
        d = sw[sel].sum()
        reps[i] = sy[sel].sum() / d if d > 0 else np.nan
    reps = reps[np.isfinite(reps)]
    if reps.size < replicas // 2:
        return None, None
    return float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5))


# ── dicotomizacion pre-registrada: dos ramas y solo dos ──────────────────

def _dicotomiza(serie_txt: pd.Series, cod: dict):
    """Devuelve (y float64 con NaN = fuera, n_fuera_codigo).

    `tipo: codigos` -- y=1 si el codigo esta en `uno`, y=0 si esta en `cero`,
    todo lo demas (NS/NR, blanco, otros) FUERA. `tipo: umbral` -- y=1 si el
    valor numerico es > `umbral`, y=0 en otro caso finito, nulo FUERA (es la
    regla de `CALC-B-0001` tal como su codigo la ejecuta: `y = rem > 0`; un
    valor negativo, que no se espera, cae en la rama 0 igual que alli)."""
    if cod["tipo"] == "codigos":
        uno = {int(c) for c in cod["uno"]}
        cero = {int(c) for c in cod["cero"]}
        codigos = [_codigo(v) for v in serie_txt.tolist()]
        y = np.array([1.0 if c in uno else (0.0 if c in cero else np.nan)
                      for c in codigos], dtype="float64")
        return y, int(np.sum(~np.isfinite(y)))
    if cod["tipo"] == "umbral":
        v = pd.to_numeric(serie_txt, errors="coerce").to_numpy("float64")
        u = float(cod["umbral"])
        y = np.where(np.isfinite(v), np.where(v > u, 1.0, 0.0), np.nan)
        return y.astype("float64"), int(np.sum(~np.isfinite(y)))
    raise RuntimeError(f"codificacion.tipo no declarada: {cod.get('tipo')!r}")


# ── medicion ──────────────────────────────────────────────────────────────

def medir(inputs, contrato):
    p = contrato["parametros"]
    B = _selector(inputs)
    S = str(p["serie_rotulo"])
    replicas = int(p["bootstrap_replicas"])
    n_min = int(p["n_minimo_celda"])
    semilla = int(contrato["seed"]["valor"])
    cod = p["codificacion"]
    out: dict[str, object] = {}
    obs: dict[str, dict] = {}

    # ── 1 · una ola a la vez, jamas agrupadas ─────────────────────────────
    for ficha in p["olas"]:
        ola = str(ficha["ola"])
        pre = f"RESULT-BM-{S}-{ola}"
        col = ficha["columnas"]
        columnas = [col["desenlace"], col["ponderador"], col["estrato"], col["upm"]]
        df = _tabla(inputs, ficha, columnas)
        out[f"{pre}-METADATO-VERSION"] = str(ficha["metadato_version_verbatim"])
        out[f"{pre}-METADATO-TEMPORAL"] = str(ficha["temporal_verbatim"])
        out[f"{pre}-N-FILAS-LEIDAS"] = int(len(df))

        y_all, n_fuera = _dicotomiza(df[col["desenlace"]], cod)
        w = pd.to_numeric(df[col["ponderador"]], errors="coerce").to_numpy("float64")
        est = df[col["estrato"]].fillna("").astype(str).to_numpy()
        upm = df[col["upm"]].fillna("").astype(str).to_numpy()
        sin_diseno = np.array([(e.strip() == "" or e.strip().lower() == "nan"
                                or u.strip() == "" or u.strip().lower() == "nan")
                               for e, u in zip(est, upm)])
        valido = np.isfinite(w) & (w > 0) & np.isfinite(y_all)
        out[f"{pre}-N-FUERA-CODIGO"] = n_fuera
        out[f"{pre}-N-SIN-PONDERADOR"] = int(np.sum(~(np.isfinite(w) & (w > 0)) & np.isfinite(y_all)))
        out[f"{pre}-N-SIN-DISENO"] = int(np.sum(sin_diseno & valido))
        out[f"{pre}-N"] = int(np.sum(valido))
        out[f"{pre}-EXPANDIDOS"] = _num(np.sum(w[valido])) if valido.any() else None

        # guardia §umbral: la rama NA no existe para `umbral` (CALC-B-0001 §1.1)
        if cod["tipo"] == "umbral" and n_fuera > 0:
            out[f"{pre}-P"] = out[f"{pre}-IC-LO"] = out[f"{pre}-IC-HI"] = None
            out[f"{pre}-VEREDICTO"] = "NO-ESTIMABLE-NULOS-INESPERADOS"
            obs[ola] = {"p": None}
            continue

        y = y_all[valido]
        wv = w[valido]
        punto = float(np.sum(y * wv) / np.sum(wv)) if wv.size and np.sum(wv) > 0 else None
        out[f"{pre}-P"] = _num(punto)
        if punto is None or wv.size < n_min:
            lo = hi = None
            veredicto = "NO-ESTIMABLE"
        elif int(np.sum(sin_diseno & valido)) > 0:
            lo = hi = None
            veredicto = "NO-ESTIMABLE-DISENO-INCOMPLETO"
        else:
            lo, hi = _boot_ic(y, wv, est[valido], upm[valido], replicas, semilla, n_min)
            veredicto = "SERIE-REPORTADA"
        # guardia de PRODUCTO (feedback MAESTRA35-L6): una proporcion que
        # satura no es una medicion, es una definicion mal puesta.
        if punto is not None and (punto == 0.0 or punto == 1.0):
            veredicto = "NO-ESTIMABLE-P-DEGENERADA"
            lo = hi = None
        out[f"{pre}-IC-LO"] = _num(lo)
        out[f"{pre}-IC-HI"] = _num(hi)
        out[f"{pre}-VEREDICTO"] = veredicto
        # B solo consume una ola con punto reportable: sin punto, con n < n_min
        # o degenerada, la ola existe en el historial con p = null y el
        # selector la excluye por VALOR_NO_ESTIMABLE -- no se fabrica nada.
        reportable = veredicto in ("SERIE-REPORTADA", "NO-ESTIMABLE-DISENO-INCOMPLETO")
        obs[ola] = {"p": _num(punto) if reportable else None,
                    "lo": _num(lo), "hi": _num(hi)}

    # ── 2 · el selector B, dos brazos, sin tocarlo ────────────────────────
    serie = dict(p["serie"])
    n_pred = {b: 0 for b in p["brazos"]}
    dentro = {b: [] for b in p["brazos"]}
    for objetivo in p["objetivos"]:
        obj = str(objetivo["ola"])
        celda = str(objetivo["celda"])
        out[f"RESULT-BM-{S}-{obj}-CELDA"] = celda
        for brazo in p["brazos"]:
            pre = f"RESULT-BM-{S}-{brazo}-{obj}"
            historial = []
            for ficha in p["olas"]:
                ola = str(ficha["ola"])
                if ola == obj:
                    continue
                # OPERATIVO: la fecha de version de la ola en corpus. El selector
                # valida `disponible_desde >= periodo_fin`, y una version puede
                # llevar fecha ANTERIOR al cierre del anio calendario de su ola
                # (ENVIPE se publica en septiembre del anio de encuesta): se
                # acota por abajo al cierre de la ola. La acotacion nunca cambia
                # la seleccion: periodo_fin <= fecha_corte de todo objetivo
                # posterior, asi que una version anterior al cierre sigue
                # disponible al corte. Se declara en la spec sellada §3.
                cierre = f"{ola}-12-31"
                disp = (max(str(ficha["disponible_desde_operativo"]), cierre)
                        if brazo == "OPERATIVO" else cierre)
                historial.append({
                    "serie": serie,
                    "periodo_inicio": f"{ola}-01-01",
                    "periodo_fin": f"{ola}-12-31",
                    "disponible_desde": disp,
                    "publicada": True,
                    "p": obs.get(ola, {}).get("p"),
                    "resultado_id": f"RESULT-BM-{S}-{ola}-P",
                    "fuente": str(ficha["payload_id"]),
                })
            doc = {
                "objetivo": {
                    "serie": serie,
                    "periodo_inicio": f"{obj}-01-01",
                    "periodo_fin": f"{obj}-12-31",
                    "fecha_corte": f"{int(obj) - 1}-12-31",
                },
                "historial": historial,
            }
            r = B.desde_documento(doc)
            out[f"{pre}-ESTADO"] = r["estado"]
            out[f"{pre}-METODO"] = r["metodo"]
            out[f"{pre}-FUENTE"] = r.get("resultado_id") or "SIN-BASELINE"
            pb = _num(r.get("p"))
            out[f"{pre}-P"] = pb
            o = obs.get(obj, {})
            po, lo, hi = o.get("p"), o.get("lo"), o.get("hi")
            if pb is None or po is None:
                out[f"{pre}-ERROR"] = None
                out[f"{pre}-ERROR-ABS"] = None
                out[f"{pre}-DENTRO-IC"] = "SIN-BASELINE" if pb is None else "SIN-OBSERVADA"
                out[f"{pre}-MARGEN-AL-BORDE"] = None
                continue
            n_pred[brazo] += 1
            out[f"{pre}-ERROR"] = _num(pb - po)
            out[f"{pre}-ERROR-ABS"] = _num(abs(pb - po))
            if lo is None or hi is None:
                out[f"{pre}-DENTRO-IC"] = "SIN-IC"
                out[f"{pre}-MARGEN-AL-BORDE"] = None
            else:
                adentro = lo <= pb <= hi
                out[f"{pre}-DENTRO-IC"] = "SI" if adentro else "NO"
                out[f"{pre}-MARGEN-AL-BORDE"] = _num(min(pb - lo, hi - pb))
                dentro[brazo].append(bool(adentro))

    for brazo in p["brazos"]:
        out[f"RESULT-BM-{S}-N-PREDICCIONES-{brazo}"] = int(n_pred[brazo])
        d = dentro[brazo]
        if not d:
            lectura = "SIN-PREDICCIONES"
        elif all(d):
            lectura = "PISO-ALTO"
        elif not any(d):
            lectura = "PISO-BAJO"
        else:
            lectura = "MIXTO"
        out[f"RESULT-BM-{S}-BIS-LECTURA-{brazo}"] = lectura
    return out
