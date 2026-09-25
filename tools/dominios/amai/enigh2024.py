"""NSE AMAI en ENIGH 2024 · apertura acotada por firma C7 (FIRMAS-16, 24/sep/2026).

Contrato: `forense/prereg-caja/AMAI-NSE-ENIGH2024-spec-v1_0.md`. El primer
resultado que produzca este procedimiento es el que se reporta.

Firma C7, verbatim: «mesa levanta por escrito la reserva solo para los seis
componentes AMAI y la distribución NSE nacional por hogares, con el medidor
congelado de CLASE-AMAI-1 y guardia de una sola variable de agrupación;
ninguna conducta se abre.»

Tres guardias, todas por código:
1. LISTA BLANCA de columnas (`COLUMNAS`): `lee_acotado` sólo parsea las
   columnas de la lista (`usecols`) y lanza `GuardiaColumnas` si alguien le
   pide otra. Cada columna parseada queda en `LEIDAS`, que el medidor compara
   contra `parametros.columnas_leidas` (así `ejecucion.json` las lista).
2. UNA SOLA VARIABLE DE AGRUPACIÓN: `agrega` sólo agrupa por `nivel` o
   `grupo` (NSE); cualquier otra lanza `GuardiaAgrupacion`. La salida pasa
   por `guardia_salida`: sólo ids de distribución/validación NSE nacional.
3. AUDITORÍA ESTÁTICA (`tools/dominios/amai/auditoria_enigh2024.py`): antes
   de abrir, verifica que este módulo no importa otro lector ni menciona una
   columna fuera de la lista.

La regla, la distribución y la validación son las del medidor congelado de
CLASE-AMAI-1 (`regla.py`, `medidor.distribucion`, `medidor.validacion`),
importadas, no copiadas ni editadas.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from tools.dominios.amai import medidor as M
from tools.dominios.amai import regla as R

# Miembro del zip -> columnas autorizadas. Nombres y preguntas citados del
# «Descripción de la base de datos» ENIGH 2024 NS (manifiesto
# enigh2024_descripcion_base_pdf); ver spec §2.
MIEMBROS = {
    "viviendas": "conjunto_de_datos_viviendas_enigh2024_ns.csv",
    "hogares": "conjunto_de_datos_hogares_enigh2024_ns.csv",
    "concentrado": "conjunto_de_datos_concentradohogar_enigh2024_ns.csv",
}
COLUMNAS = {
    "viviendas": ("folioviv", "cuart_dorm", "bano_comp"),
    "hogares": ("folioviv", "foliohog", "conex_inte", "num_auto", "num_van", "num_pick"),
    "concentrado": ("folioviv", "foliohog", "educa_jefe", "ocupados", "factor",
                    "est_dis", "upm"),
}
AGRUPACIONES = ("nivel", "grupo")
RAIZ = Path(__file__).resolve().parents[3]   # igual desde tools/ y desde el CALC
LEIDAS: list[str] = []


class GuardiaColumnas(RuntimeError):
    pass


class GuardiaAgrupacion(RuntimeError):
    pass


def lista_blanca() -> list[str]:
    return [f"{t}.{c}" for t in COLUMNAS for c in COLUMNAS[t]]


def _norm(c: str) -> str:
    return str(c).strip().strip('"').lstrip("﻿").lstrip("ï»¿")


def lee_acotado(ruta, tabla: str, columnas: tuple[str, ...]) -> pd.DataFrame:
    """Parsea SÓLO `columnas` del miembro `tabla`; todo como texto."""
    if tabla not in COLUMNAS:
        raise GuardiaColumnas(f"tabla no autorizada: {tabla}")
    fuera = [c for c in columnas if c not in COLUMNAS[tabla]]
    if fuera:
        raise GuardiaColumnas(f"columnas fuera de la lista blanca ({tabla}): {fuera}")
    quiero = set(columnas)
    with zipfile.ZipFile(ruta) as z:
        nombres = [n for n in z.namelist() if n.lower().endswith(MIEMBROS[tabla])
                   and "/conjunto_de_datos/" in n]
        if len(nombres) != 1:
            raise RuntimeError(f"{MIEMBROS[tabla]}: {len(nombres)} miembros")
        for enc in ("utf-8-sig", "latin-1"):
            try:
                with z.open(nombres[0]) as fh:
                    df = pd.read_csv(io.TextIOWrapper(fh, encoding=enc, newline=""),
                                     dtype=str, keep_default_na=False, na_filter=False,
                                     usecols=lambda c: _norm(c) in quiero)
                break
            except UnicodeDecodeError:
                continue
    df.columns = [_norm(c) for c in df.columns]
    if set(df.columns) != quiero:
        raise RuntimeError(f"{tabla}: faltan {sorted(quiero - set(df.columns))}")
    LEIDAS.extend(f"{tabla}.{c}" for c in columnas if f"{tabla}.{c}" not in LEIDAS)
    return df[list(columnas)].apply(lambda s: s.astype(str).str.strip())


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.strip(), errors="coerce")


def componentes(ruta) -> pd.DataFrame:
    """Réplica del Anexo AMAI: CONCENTRADO ⋈ HOGARES por (folioviv, foliohog)
    ⋈ VIVIENDAS por folioviv. autos = num_auto + num_van + num_pick."""
    v = lee_acotado(ruta, "viviendas", COLUMNAS["viviendas"])
    h = lee_acotado(ruta, "hogares", COLUMNAS["hogares"])
    c = lee_acotado(ruta, "concentrado", COLUMNAS["concentrado"])
    for df, ll, q in ((h, ["folioviv", "foliohog"], "hogares"),
                      (c, ["folioviv", "foliohog"], "concentrado"),
                      (v, ["folioviv"], "viviendas")):
        if df.duplicated(ll).any():
            raise RuntimeError(f"{q}: llave {ll} no única")
    d = c.merge(h, on=["folioviv", "foliohog"], how="left", validate="1:1")
    d = d.merge(v, on="folioviv", how="left", validate="m:1")
    conex = _num(d["conex_inte"])
    return pd.DataFrame({
        "llave": d["folioviv"] + "-" + d["foliohog"],
        "educa_jefe": _num(d["educa_jefe"]),
        "banos": _num(d["bano_comp"]),
        "autos": _num(d["num_auto"]) + _num(d["num_van"]) + _num(d["num_pick"]),
        "internet": np.where(conex.isna(), np.nan, (conex == 1).astype(float)),
        "ocupados": _num(d["ocupados"]),
        "dormitorios": _num(d["cuart_dorm"]),
        "factor": _num(d["factor"]),
        "EST_DIS": d["est_dis"], "UPM_DIS": d["upm"],
    })


def agrega(comp: pd.DataFrame, por: str) -> pd.DataFrame:
    """Masa de factor (`sum`) y hogares sin ponderar (`size`) por la ÚNICA
    variable de agrupación autorizada (NSE)."""
    if por not in AGRUPACIONES:
        raise GuardiaAgrupacion(f"agrupación no autorizada: {por}")
    return comp.groupby(por)["factor"].agg(["sum", "size"])


_SALIDA = re.compile(
    r"^RESULT-AMAI-NSE-ENIGH-2024-(JSON|COLUMNAS-LEIDAS|N-HOGARES-(CON|SIN)-NSE|"
    r"VALIDACION-ESTADO|DESVIO-MAX-(GRUPO|NIVEL)-PP|MASA-PUNTAJE-CERO-P|"
    r"DIST-(E|D|D\+|C-|C|C\+|A/B|BAJO|MEDIO|ALTO)-P)$")


def guardia_salida(out: dict) -> None:
    malos = [k for k in out if not _SALIDA.match(k)]
    if malos:
        raise GuardiaAgrupacion(f"salida fuera de la distribución NSE nacional: {malos}")


def _tabla(texto: str, par: dict) -> str:
    """El JSON (> 1 KB) va a `data/corrida0/<calc_id>/tablas/` y el RESULT lo
    cita por `REF:<ruta>#sha256:<hex>` (regla VALOR-LARGO del conducto)."""
    rel = f"data/corrida0/{par['calc_id']}/tablas/nse-enigh2024.json"
    ruta = RAIZ / rel
    datos = texto.encode("utf-8")
    ruta.parent.mkdir(parents=True, exist_ok=True)
    if not ruta.exists() or ruta.read_bytes() != datos:
        ruta.write_bytes(datos)
    return f"REF:{rel}#sha256:{hashlib.sha256(datos).hexdigest()}"


def medir(inputs: dict, contrato: dict) -> dict:
    par = contrato["parametros"]
    if list(par["columnas_leidas"]) != lista_blanca():
        raise GuardiaColumnas("parametros.columnas_leidas distinto de la lista blanca")
    LEIDAS.clear()
    ruta = inputs[par["input_id"]]["ruta_absoluta"]
    comp = componentes(ruta)
    if sorted(LEIDAS) != sorted(par["columnas_leidas"]):
        raise GuardiaColumnas(f"columnas leídas {LEIDAS} != declaradas")
    pts = R.puntos(comp[list(R.COMPONENTES)])
    puntaje = pts.sum(axis=1, min_count=len(R.COMPONENTES))
    puntaje[pts.isna().any(axis=1)] = np.nan
    comp = comp.assign(puntaje=puntaje)
    comp["nivel"] = R.nivel(comp["puntaje"])
    comp["grupo"] = R.grupo(comp["nivel"])
    dist = M.distribucion(comp)
    ok = comp["nivel"].notna() & comp["factor"].gt(0)
    masa = {por: agrega(comp[ok], por) for por in AGRUPACIONES}
    tot = float(comp.loc[ok, "factor"].sum())
    for n in R.NIVELES:  # la agregación guardada coincide con la del medidor congelado
        m = float(masa["nivel"]["sum"].get(n, 0.0))
        if tot > 0 and abs(m / tot - dist["niveles"][n]) > 1e-12:
            raise RuntimeError("agregación guardada != medidor.distribucion")
    # Supresión F-U5-2 (spec §3): nivel o grupo con < n_min hogares sin ponderar.
    n_min = int(par["n_min"])
    n_celda = {por: {k: int(masa[por]["size"].get(k, 0)) for k in claves}
               for por, claves in (("nivel", R.NIVELES), ("grupo", R.ORDEN_GRUPOS))}
    suprimidas = sorted(k for por in n_celda for k, v in n_celda[por].items() if v < n_min)
    # Validación del medidor congelado, rama de aproximación (umbral por grupo).
    val = M.validacion("ENIGH-2024", dist, par)
    faltantes = {c: int(comp[c].isna().sum()) for c in R.COMPONENTES}
    modulos = {"regla": hashlib.sha256(Path(R.__file__).read_bytes()).hexdigest(),
               "medidor_clase_amai_1": hashlib.sha256(Path(M.__file__).read_bytes()).hexdigest(),
               "enigh2024": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    pref = "RESULT-AMAI-NSE-ENIGH-2024"
    doc = {"instrumento": "ENIGH", "ola": "2024", "columnas_leidas": list(LEIDAS),
           "construccion": {"componentes_faltantes": faltantes}, "distribucion": dist,
           "n_hogares_por_celda": n_celda, "suprimidas_n": suprimidas,
           "validacion": val, "modulos_sha256": modulos}
    texto = json.dumps(doc, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                       allow_nan=False)
    out = {pref + "-JSON": _tabla(texto, par), pref + "-COLUMNAS-LEIDAS": ",".join(LEIDAS)}
    for n in R.NIVELES:
        out[f"{pref}-DIST-{n}-P"] = None if n in suprimidas else dist["niveles"][n]
    for g in R.ORDEN_GRUPOS:
        out[f"{pref}-DIST-{g}-P"] = None if g in suprimidas else dist["grupos"][g]
    out[pref + "-MASA-PUNTAJE-CERO-P"] = dist["masa_puntaje_cero"]
    out[pref + "-N-HOGARES-CON-NSE"] = dist["n_hogares_con_nse"]
    out[pref + "-N-HOGARES-SIN-NSE"] = dist["n_hogares_sin_nse"]
    out[pref + "-VALIDACION-ESTADO"] = val["estado"]
    out[pref + "-DESVIO-MAX-GRUPO-PP"] = val["desvio_max_grupo_pp"]
    out[pref + "-DESVIO-MAX-NIVEL-PP"] = val["desvio_max_nivel_pp"]
    guardia_salida(out)
    return out
