#!/usr/bin/env python3
"""Medidor de `CALC-C2-COMPUESTO-IC-ENIF2024-0001` (COMMIT-2).

ACTO `GEN2-C2-COMPUESTO-IC-ENIF2024-1` (19/sep/2026, CAJA). Contrato humano:
`forense/prereg-caja/C2-COMPUESTO-IC-ENIF2024-spec-v1_0.md`, congelado en el
COMMIT-1 junto con este archivo, ANTES de abrir una sola respuesta de ENIF
2024. Interfaz del plan v2.0 §4 (B-1): `medir(inputs, contrato) -> dict`; el
medidor no abre `spec.yaml`.

QUE HACE
--------
Da IC95 a las emisiones C2 compuestas de ENIF 2024 que
`CALC-C2-COMPUESTO-RESERVADAS-0001` sello sin IC (el conteo se deriva del
dictamen, no se copia). Metodo de la casa (pilotos 1 y 2): UN remuestreo de
UPM por estrato compartido por toda la ola (seed 42, 10 000 replicas, PCG64),
y en cada replica k

    C2_k = expit( logit p_k(a) + logit p_k(b) - logit p_k )

con p_k(a), p_k(b), p_k marginales de UN eje cada uno, obtenidos por
`marginal_enif(ola, grupo)` -- una variable por llamada. IC95 = percentiles
2.5 / 97.5 de las replicas definidas. El PUNTO no se re-deriva: es el
`piso_log_aditivo` de los marginales SELLADOS del arbitro (el mismo numero que
`CALC-C2-COMPUESTO-RESERVADAS-0001` publico), y el control 1 lo verifica.

DESVIACION ESCRITA (mesa, 19/sep/2026, en respuesta al hallazgo P0)
----------------------------------------------------------------------
`tools/celda_d/marginales_reproduccion.py` -- el "modulo guardado" que el
encargo manda importar -- es ENVIPE-only por construccion: `carga_ola()` lee
`tmod_vic`/`tsdem`, universo `BP1_20`, `FAC_DEL`; `EJES` admite tres ejes de
ENVIPE y NINGUNO de los cinco del dictamen para ENIF 2024. `medir()` lo
prueba mecanicamente (RESULT `G-P0-MODULO-GUARDADO-*`). Mesa autorizo que
este medidor lleve SU PROPIA guardia de una variable, con la MISMA semantica
que la del modulo (str posicional unico · whitelist de ejes · huella de la
ola · sin `cruce()`), e importe del arbitro (`tools/medidor_ahorro_enif24.py`)
el universo, los desenlaces y la construccion de cada eje -- el mismo objeto
de codigo que sello los R marginales de `milpa/tramite-ola5-propuesta-v0.yaml`.
El modulo guardado NO se modifica; de el se importa `cotejo()` (control 2).

GUARDIA DE RESERVA -- codigo, no prosa (E.6; NC-0328)
------------------------------------------------------
1. `marginal_enif(ola, grupo)`: `grupo` es UN `str` posicional; una lista o
   dos argumentos lanzan `TypeError`; un eje fuera de `EJES_ENIF` lanza
   `ValueError`; la ola se re-huella antes de contar y una ola filtrada o
   reordenada lanza `ReservaRota`. No existe `cruce()`.
2. `auditoria_ast(ruta)` recorre el AST de ESTE archivo al arrancar `medir()`
   (y en `tests/test_c2_ic_enif2024_guardia.py`, con controles positivos):
   ninguna agrupacion por mas de una variable (ningun nodo combina dos
   comparaciones; `groupby`/`crosstab`/`pivot`/... prohibidos), el microdato
   (`.df`) solo es alcanzable dentro del nucleo guardado, y ninguna lectura
   de payload fuera de ENIF 2024 (TMODULO). Si falla, `medir()` PARA antes de
   abrir el zip.

Este archivo no ve, no deriva y no imprime ningun cruce. Los pares siguen
`RESERVADA`. No adopta nada.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import importlib.util
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[3]

# ══ importaciones: el mismo objeto de codigo, nunca una copia ═══════════════

def _importa(nombre: str, ruta: Path):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


# El arbitro de ENIF 2024: universo (`carga()`), desenlaces (`desenlaces()`),
# construccion de cada eje (`EJES_P2`, `EJE_CUENTA_PRINCIPAL`) y el IC de la
# receta del arbitro (`wprop_ic_conglomerado`, seed 42, 10 000).
_ARB = _importa("medidor_ahorro_enif24", RAIZ / "tools" / "medidor_ahorro_enif24.py")
# El modulo guardado: `cotejo()` para el control 2 y `marginal()` como sonda
# del hallazgo P0. No se modifica.
_MR = _importa("marginales_reproduccion",
               RAIZ / "tools" / "celda_d" / "marginales_reproduccion.py")
# La forma de C2, pinada por contrato: importada, no reimplementada.
_C2 = _importa("test_celda_d_c2", RAIZ / "tests" / "test_celda_d_c2.py")
# La misma serializacion de ids y el mismo partidor de pares que uso el CALC
# de emisiones, y sus nacionales citados (no recalculados).
_CC = _importa("c2_compuesto", RAIZ / "tools" / "c2_compuesto.py")

piso_log_aditivo = _C2.piso_log_aditivo
MarginalDegenerado = _C2.MarginalDegenerado
FUERA = _ARB.FUERA

P = "RESULT-C2IC-ENIF2024"
REGLA = "dinero.ahorro.via_informal_ejes_enif2024"
OLA = "ENIF 2024"
PAYLOAD_ID = "enif_2024_enif_2024_bd_csv"
PAYLOAD_ARCHIVO = "enif_2024_bd_csv.zip"
PAYLOAD_TABLA = "TMODULO.csv"
INPUTS_PERMITIDOS = (
    PAYLOAD_ID, "IN-DICTAMEN", "IN-ARBITRO-MARGINALES", "IN-PUNTOS-SELLADOS",
    "IN-SPEC-SELLADA", "IN-ARBITRO-MEDIDOR", "IN-ARBITRO-EJES",
    "IN-MODULO-GUARDADO", "IN-FORMA-C2-SELLADA", "IN-C2-COMPUESTO",
    "IN-WPROP-ARBITRO",
)
# Ejes que este medidor ADMITE: los cinco de los pares EMITIBLE del dictamen
# mas el nacional. `formalidad` queda fuera a proposito (NO-EMITIBLE,
# universo restringido; el encargo: "no intentes rescatarla").
EJES_ENIF = ("sexo", "edad", "escolaridad", "localidad", "cuenta_formal", "nacional")
DESENLACES = {
    "ahorra_solo_informal": "ahorra_solo_informal (PRINCIPAL)",
    "informal_cualquiera": "informal_cualquiera (SECUNDARIO)",
}
ROTULO_SUPUESTO = "ausencia de interaccion en escala logit"
IC_ROTULO = "IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS"
_slug = _CC._slug


class ReservaRota(RuntimeError):
    """Se intento cruzar, filtrar o alterar la ola fuera de lo autorizado."""


class Paro(RuntimeError):
    """Premisa de la spec falsa en el archivo: se PARA, no se reporta cifra."""


# ══ nucleo guardado: las UNICAS funciones que tocan el microdato (`.df`) ════

@dataclass(frozen=True)
class OlaEnif:
    df: pd.DataFrame = field(repr=False, compare=False)
    huella: str = ""
    meta: dict = field(default_factory=dict, compare=False)


def _ejes_del_arbitro() -> dict:
    ejes = {e.nombre: e for e in _ARB.EJES_P2}
    ejes["cuenta_formal"] = _ARB.EJE_CUENTA_PRINCIPAL   # misma `deriva` que el SECUNDARIO
    return ejes


def _huella(df: pd.DataFrame) -> str:
    """sha256 de las columnas que definen la ola, en orden de archivo: una
    fila filtrada, reordenada o alterada cambia la huella."""
    h = hashlib.sha256()
    h.update(str(len(df)).encode())
    for c in ("EST_DIS", "UPM_DIS", "_w", *EJES_ENIF[:-1],
              *[f"_y_{d}" for d in DESENLACES]):
        h.update(b"\x1f")
        h.update("\n".join(df[c].astype(str).tolist()).encode("utf-8"))
    return h.hexdigest()


def _ola_desde_df(df: pd.DataFrame) -> OlaEnif:
    """Construye la ola desde el DataFrame que `carga()` del arbitro devuelve:
    universo del arbitro, desenlaces del arbitro, un eje por columna derivado
    por el `Eje.deriva` del arbitro. Cada columna nace de UN eje."""
    ejes = _ejes_del_arbitro()
    des = _ARB.desenlaces(df)
    d = pd.DataFrame(index=df.index)
    d["EST_DIS"] = df["EST_DIS"].astype(str).str.strip()
    d["UPM_DIS"] = df["UPM_DIS"].astype(str).str.strip()
    d["_w"] = df["_w"].astype(float)
    for nombre in EJES_ENIF[:-1]:
        d[nombre] = ejes[nombre].deriva(df).astype(str)
    d["nacional"] = "NAC"
    for corto, etiqueta in DESENLACES.items():
        d[f"_y_{corto}"] = des[etiqueta].astype(float)
    d = d.reset_index(drop=True)
    if (d["EST_DIS"] == "").any():
        raise Paro("ENIF 2024: EST_DIS con faltantes")
    if (d["UPM_DIS"] == "").any():
        raise Paro("ENIF 2024: UPM_DIS con faltantes")
    meta = {
        "filas_universo": int(len(d)),
        "estratos": int(d["EST_DIS"].nunique()),
        "upm": int((d["EST_DIS"] + "\x1f" + d["UPM_DIS"]).nunique()),
        "poblacion_expandida": float(d["_w"].sum()),
        "fuera_por_eje": {e: int((d[e] == FUERA).sum()) for e in EJES_ENIF[:-1]},
        "numerador": {c: int(d[f"_y_{c}"].sum()) for c in DESENLACES},
    }
    return OlaEnif(df=d, huella=_huella(d), meta=meta)


def _carga_ola_enif(inputs: dict) -> OlaEnif:
    """UNICA lectura de payload de este medidor: `carga()` del arbitro, sobre
    el MISMO archivo que el manifiesto resuelve (guardia por sha256, no por
    nombre). Si el arbitro apunta a otro archivo, PARA antes de leer."""
    ent = inputs[PAYLOAD_ID]
    ruta_arb = Path(str(_ARB.ZIP))
    if ruta_arb.name != PAYLOAD_ARCHIVO:
        raise Paro(f"el arbitro apunta a {ruta_arb.name!r}, no a {PAYLOAD_ARCHIVO!r}")
    if str(_ARB.TABLA) != PAYLOAD_TABLA:
        raise Paro(f"el arbitro lee la tabla {_ARB.TABLA!r}, no {PAYLOAD_TABLA!r}")
    sha_arb = _ARB.sha256(str(ruta_arb))
    if sha_arb != str(ent["sha256"]):
        raise Paro("el zip que lee el arbitro no es el payload resuelto por el "
                   f"manifiesto: {sha_arb[:12]} != {str(ent['sha256'])[:12]}")
    df = _ARB.carga()
    faltan = [c for c in ["SEXO", "NIV", "TLOC", "P3_13", *_ARB.CUENTAS]
              if c not in df.columns]
    if faltan:
        raise Paro(f"faltan columnas de eje en {PAYLOAD_TABLA}: {faltan}")
    return _ola_desde_df(df)


def _verifica(ola: OlaEnif) -> None:
    if not isinstance(ola, OlaEnif):
        raise TypeError("se esperaba una OlaEnif producida por _carga_ola_enif()")
    if _huella(ola.df) != ola.huella:
        raise ReservaRota("ENIF 2024: la ola fue filtrada, reordenada o alterada "
                          "tras cargarla -- agrupar sobre un subconjunto es "
                          "cruzar por otra via")


@dataclass(frozen=True)
class ReplicasEnif:
    huella_ola: str
    seed: int
    n_rep: int
    counts: np.ndarray = field(repr=False, compare=False)   # (n_rep, n_upm)
    pos_fila: np.ndarray = field(repr=False, compare=False)  # fila -> upm
    n_upm: int = 0
    estratos_upm_unica: int = 0


def replicas_enif(ola: OlaEnif, seed: int, n_rep: int) -> ReplicasEnif:
    """UN remuestreo por ola, compartido por todos los grupos y celdas. Misma
    receta que `tools/celda_d/marginales_reproduccion.py::replicas_compartidas`
    (lineas 256-286): `n_h` UPM con reemplazo dentro de cada estrato, UN
    generador `numpy.random.PCG64(seed)`, estratos en orden lexicografico de
    `EST_DIS` y UPM en orden lexicografico de `UPM_DIS`. Se re-escribe aqui
    porque aquella firma exige una `Ola` de ENVIPE (huella por `ID_DEL`)."""
    _verifica(ola)
    est = ola.df["EST_DIS"].to_numpy()
    upm = ola.df["UPM_DIS"].to_numpy()
    claves = np.array([f"{e}\t{u}" for e, u in zip(est, upm)])
    unicas, primeras, pos_fila = np.unique(claves, return_index=True,
                                           return_inverse=True)
    upm_est = est[primeras]
    pos_por_estrato: dict[str, list[int]] = {}
    for pos, e in enumerate(upm_est):
        pos_por_estrato.setdefault(e, []).append(pos)
    n_upm = len(unicas)
    rng = np.random.Generator(np.random.PCG64(seed))
    bloques = []
    for e in sorted(pos_por_estrato):
        pos = np.asarray(pos_por_estrato[e], dtype=np.int64)
        bloques.append(pos[rng.integers(0, len(pos), size=(n_rep, len(pos)))])
    idx = np.concatenate(bloques, axis=1)
    counts = np.empty((n_rep, n_upm), dtype=np.int32)
    for r in range(n_rep):
        counts[r] = np.bincount(idx[r], minlength=n_upm)
    unica = sum(1 for e in pos_por_estrato if len(pos_por_estrato[e]) == 1)
    return ReplicasEnif(huella_ola=ola.huella, seed=int(seed), n_rep=int(n_rep),
                        counts=counts, pos_fila=pos_fila.astype(np.int64),
                        n_upm=int(n_upm), estratos_upm_unica=int(unica))


def _reps_de_mascara(ola: OlaEnif, rep: ReplicasEnif, mask: np.ndarray,
                     y_col: str) -> np.ndarray:
    """p^(r) del grupo `mask` en cada replica; NaN si el denominador es 0."""
    w = ola.df["_w"].to_numpy() * mask
    y = w * ola.df[y_col].to_numpy()
    W = np.bincount(rep.pos_fila, weights=w, minlength=rep.n_upm)
    Y = np.bincount(rep.pos_fila, weights=y, minlength=rep.n_upm)
    out = np.empty(rep.n_rep, dtype=float)
    for a in range(0, rep.n_rep, 1000):
        c = rep.counts[a:a + 1000].astype(np.float64)
        den = c @ W
        num = c @ Y
        with np.errstate(invalid="ignore", divide="ignore"):
            out[a:a + 1000] = np.where(den > 0, num / den, np.nan)
    return out


def _orden(grupo: str) -> list[str]:
    if grupo == "nacional":
        return ["NAC"]
    return list(_ejes_del_arbitro()[grupo].orden)


def marginal_enif(ola: OlaEnif, grupo: str, *, desenlace: str,
                  replicas: ReplicasEnif | None = None) -> dict:
    """Celdas de UN eje de la ola. `grupo` es un `str` POSICIONAL UNICO -- no
    hay `*grupos`, no hay lista; el eje ya viene derivado por el arbitro en
    su propia columna y solo puede ser uno de `EJES_ENIF`. `desenlace`
    selecciona la variable de desenlace, no agrupa."""
    if not isinstance(grupo, str):
        raise TypeError(f"grupo debe ser UN str, llego {type(grupo).__name__}: "
                        "una sola variable de agrupacion por firma")
    if grupo not in EJES_ENIF:
        raise ValueError(f"grupo {grupo!r} no es un eje autorizado {EJES_ENIF}")
    if desenlace not in DESENLACES:
        raise ValueError(f"desenlace {desenlace!r} no es uno de {tuple(DESENLACES)}")
    _verifica(ola)
    if replicas is not None:
        if replicas.huella_ola != ola.huella:
            raise ReservaRota("las replicas no son de esta ola")
    y_col = f"_y_{desenlace}"
    celda = ola.df[grupo].to_numpy()
    dentro = celda != FUERA
    w_all = ola.df["_w"].to_numpy()
    y_all = ola.df[y_col].to_numpy()
    est_all = ola.df["EST_DIS"].to_numpy()
    upm_all = ola.df["UPM_DIS"].to_numpy()
    out = {"eje": grupo, "desenlace": desenlace, "n_universo": int(len(celda)),
           "n_fuera": int((~dentro).sum()),
           "cobertura": float(dentro.mean()) if len(celda) else 0.0,
           "celdas": {}}
    for k in _orden(grupo):
        mask = celda == k
        n = int(mask.sum())
        fila = {"n": n, "numerador": int(y_all[mask].sum()),
                "poblacion": float(w_all[mask].sum())}
        if n == 0:
            fila.update({"p": None, "ic95": None, "estratos": 0, "upm": 0,
                         "replicas": None})
        else:
            p_, lo, hi, _n, n_est, n_cl = _ARB.wprop_ic_conglomerado(
                y_all[mask].astype(float), w_all[mask].astype(float),
                est_all[mask].tolist(), upm_all[mask].tolist())
            fila.update({"p": float(p_), "ic95": [float(lo), float(hi)],
                         "estratos": int(n_est), "upm": int(n_cl)})
            fila["replicas"] = (_reps_de_mascara(ola, replicas, mask, y_col)
                                if replicas is not None else None)
        out["celdas"][k] = fila
    return out


# ══ auditoria del AST de este archivo: la guardia E.6 como codigo ══════════

NUCLEO = ("_huella", "_ola_desde_df", "_carga_ola_enif", "_verifica",
          "replicas_enif", "_reps_de_mascara", "marginal_enif")
_AUDIT_PROHIBIDOS = (
    "groupby", "crosstab", "pivot", "pivot_table", "unstack", "stack", "merge",
    "concat", "read_csv", "read_excel", "read_table", "read_sav", "read_dta",
    "ZipFile", "open", "getattr", "setattr", "vars", "globals", "locals",
    "eval", "exec", "__dict__", "asdict", "query", "apply", "applymap",
    "transform", "agg", "aggregate", "iterrows", "itertuples", "MultiIndex",
    "cruce", "compile", "__import__",
)
_AUDIT_IMPORTS = ("__future__", "ast", "csv", "dataclasses", "hashlib",
                  "importlib.util", "json", "sys", "pathlib", "numpy", "pandas",
                  "yaml")
_AUDIT_MODULOS_IMPORTADOS = ("medidor_ahorro_enif24.py", "marginales_reproduccion.py",
                             "test_celda_d_c2.py", "c2_compuesto.py")
_AUDIT_ARCHIVOS = (PAYLOAD_ARCHIVO, PAYLOAD_TABLA) + _AUDIT_MODULOS_IMPORTADOS
_AUDIT_OTROS_INSTRUMENTOS = ("encig", "envipe", "enut", "enigh", "enoe", "ensanut",
                             "endutih", "encuci", "endireh", "enasem", "mociba",
                             "enaproce", "ensafi", "eder2017", "eder_", "lapop", "issp", "wbes",
                             "ennvih", "mxfls", "enadid", "encup", "enif2021",
                             "enif_2021", "enif2018", "enif_2018", "enif2015",
                             "enif_2015", "enif2012", "enif_2012")
_AUDIT_EXT = (".zip", ".csv", ".xlsx", ".xls", ".dbf", ".sav", ".dta", ".txt", ".pdf")
_AUDIT_COMPARADORES = (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
                       ast.In, ast.NotIn)


def _nombre_llamado(call: ast.Call) -> str:
    f = call.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return ""


def _tiene_comparacion(nodo: ast.AST) -> bool:
    for sub in ast.walk(nodo):
        if isinstance(sub, ast.Compare):
            if any(isinstance(op, _AUDIT_COMPARADORES) for op in sub.ops):
                return True
    return False


def auditoria_ast(ruta: Path) -> list[str]:
    """Recorre el AST del medidor y devuelve la lista de violaciones (vacia =
    PASA). Reglas, una por una, en `tests/test_c2_ic_enif2024_guardia.py`
    con un control positivo (mutacion) por regla."""
    fuente = Path(ruta).read_text(encoding="utf-8")
    return auditoria_ast_fuente(fuente)


def auditoria_ast_fuente(fuente: str) -> list[str]:
    arbol = ast.parse(fuente)
    viol: list[str] = []

    # docstrings y constantes `_AUDIT_*` quedan fuera del escrutinio textual
    exentos: set[int] = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.Module, ast.FunctionDef, ast.ClassDef,
                             ast.AsyncFunctionDef)):
            cuerpo = nodo.body
            if cuerpo and isinstance(cuerpo[0], ast.Expr) \
                    and isinstance(cuerpo[0].value, ast.Constant):
                exentos.add(id(cuerpo[0].value))
        if isinstance(nodo, ast.Assign):
            nombres = [t.id for t in nodo.targets if isinstance(t, ast.Name)]
            if any(n.startswith("_AUDIT_") for n in nombres):
                for sub in ast.walk(nodo.value):
                    if isinstance(sub, ast.Constant):
                        exentos.add(id(sub))

    # funcion que contiene cada nodo
    padre_fn: dict[int, str] = {}

    def _marca(nodo, fn):
        for hijo in ast.iter_child_nodes(nodo):
            nombre = fn
            if isinstance(hijo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                nombre = hijo.name
            padre_fn[id(hijo)] = nombre
            _marca(hijo, nombre)
    _marca(arbol, "<modulo>")

    # R1 · imports: solo la lista blanca
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            for a in nodo.names:
                if a.name not in _AUDIT_IMPORTS:
                    viol.append(f"R1 import prohibido: {a.name}")
        elif isinstance(nodo, ast.ImportFrom):
            if (nodo.module or "") not in _AUDIT_IMPORTS:
                viol.append(f"R1 import prohibido: from {nodo.module}")

    for nodo in ast.walk(arbol):
        fn = padre_fn.get(id(nodo), "<modulo>")
        # R2 · nombres prohibidos (atributo, nombre o funcion llamada)
        if isinstance(nodo, ast.Attribute) and nodo.attr in _AUDIT_PROHIBIDOS:
            viol.append(f"R2 atributo prohibido `.{nodo.attr}` en {fn}")
        if isinstance(nodo, ast.Name) and nodo.id in _AUDIT_PROHIBIDOS:
            viol.append(f"R2 nombre prohibido `{nodo.id}` en {fn}")
        if isinstance(nodo, ast.Call) and _nombre_llamado(nodo) in _AUDIT_PROHIBIDOS:
            viol.append(f"R2 llamada prohibida `{_nombre_llamado(nodo)}()` en {fn}")
        # R3 · el microdato (`.df`) solo dentro del nucleo guardado
        if isinstance(nodo, ast.Attribute) and nodo.attr == "df":
            if fn not in NUCLEO:
                viol.append(f"R3 acceso a `.df` fuera del nucleo guardado: {fn}")
        # R4 · ningun nodo combina dos comparaciones (una agrupacion por dos
        #      variables es `mask_a & mask_b`, `mask_a * mask_b`, `a and b`)
        if isinstance(nodo, ast.BinOp) and isinstance(
                nodo.op, (ast.BitAnd, ast.BitOr, ast.BitXor, ast.Mult)):
            if _tiene_comparacion(nodo.left) and _tiene_comparacion(nodo.right):
                viol.append(f"R4 dos comparaciones combinadas por operador en {fn} "
                            f"(linea {nodo.lineno})")
        if isinstance(nodo, ast.BoolOp):
            con = [v for v in nodo.values if _tiene_comparacion(v)]
            if len(con) >= 2:
                viol.append(f"R4 dos comparaciones combinadas por and/or en {fn} "
                            f"(linea {nodo.lineno})")
        # R5 · constructores y lecturas del arbitro solo donde la spec los pone
        if isinstance(nodo, ast.Call):
            nom = _nombre_llamado(nodo)
            if nom == "OlaEnif":
                if fn != "_ola_desde_df":
                    viol.append(f"R5 `OlaEnif(` fuera de _ola_desde_df: {fn}")
            if nom == "carga":
                if fn != "_carga_ola_enif":
                    viol.append(f"R5 `carga()` del arbitro fuera de _carga_ola_enif: {fn}")
            if nom in ("desenlaces", "deriva"):
                if fn != "_ola_desde_df":
                    viol.append(f"R5 `{nom}()` fuera de _ola_desde_df: {fn}")
            if nom == "_importa":
                arg = nodo.args[1] if len(nodo.args) > 1 else None
                consts = ([c.value for c in ast.walk(arg) if isinstance(c, ast.Constant)]
                          if arg is not None else [])
                if not any(str(c) in _AUDIT_MODULOS_IMPORTADOS for c in consts):
                    viol.append(f"R5 `_importa` de un modulo no autorizado en {fn}")
            # R6 · marginal_enif: UN grupo posicional, nombre o literal str
            if nom == "marginal_enif":
                if len(nodo.args) != 2:
                    viol.append(f"R6 marginal_enif con {len(nodo.args)} posicionales en {fn}")
                elif not isinstance(nodo.args[1], (ast.Name, ast.Constant)):
                    viol.append(f"R6 marginal_enif con grupo no atomico en {fn}")
                elif isinstance(nodo.args[1], ast.Constant) \
                        and not isinstance(nodo.args[1].value, str):
                    viol.append(f"R6 marginal_enif con grupo literal no str en {fn}")
                for kw in nodo.keywords:
                    if kw.arg not in ("desenlace", "replicas"):
                        viol.append(f"R6 marginal_enif con keyword `{kw.arg}` en {fn}")
        # R7 · ninguna funcion de cruce
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                and "cruce" in nodo.name.lower():
            viol.append(f"R7 funcion de cruce definida: {nodo.name}")
        # R8 · constantes: ningun payload ni instrumento fuera de ENIF 2024
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
          if id(nodo) not in exentos:
            s = nodo.value
            bajo = s.lower()
            if any(bajo.endswith(ext) for ext in _AUDIT_EXT):
                if s not in _AUDIT_ARCHIVOS:
                    viol.append(f"R8 archivo no autorizado en constante {s!r} ({fn})")
            if any(tok in bajo for tok in _AUDIT_OTROS_INSTRUMENTOS):
                viol.append(f"R8 otro instrumento en constante {s!r} ({fn})")
        if isinstance(nodo, ast.Subscript) and isinstance(nodo.value, ast.Name):
            if nodo.value.id == "inputs" and isinstance(nodo.slice, ast.Constant):
                if nodo.slice.value not in INPUTS_PERMITIDOS:
                    viol.append(f"R8 input no declarado {nodo.slice.value!r} en {fn}")
    return viol


# ══ lectura de los insumos del repo (bytes verificados por el runner) ═══════

def _bytes(inputs: dict, iid: str) -> bytes:
    ent = inputs[iid]
    b = ent.get("bytes")
    if b is None:
        b = Path(ent["ruta_absoluta"]).read_bytes()
    return b


def _dictamen_enif(inputs: dict) -> list[dict]:
    """Filas de ENIF 2024 del dictamen sellado (leidas, no tecleadas)."""
    texto = _bytes(inputs, "IN-DICTAMEN").decode("utf-8")
    lineas = [l for l in texto.splitlines() if not l.startswith("#")]
    filas = []
    for r in csv.DictReader(lineas, delimiter="\t"):
        if r["ola"] != OLA:
            continue
        if r["regla"] != REGLA:
            continue
        filas.append(r)
    return filas


def _ejes_arbitro(inputs: dict) -> dict[str, dict[str, dict]]:
    """`{bloque: {eje: {celdas: [...], cobertura, universo_restringido},
    _nombre}}` de la regla del arbitro, del yaml sellado."""
    doc = yaml.safe_load(_bytes(inputs, "IN-ARBITRO-MARGINALES").decode("utf-8"))
    reglas = doc["reglas_propuestas"]          # misma clave que c2_compuesto._reglas_ejes
    regla = None
    for r in reglas:
        if isinstance(r, dict) and r.get("id") == REGLA:
            regla = r
            break
    if regla is None:
        raise Paro(f"regla {REGLA} ausente en el yaml del arbitro")
    out = {}
    for bloque, cuerpo in regla["desenlaces"].items():
        out[bloque] = {e["eje"]: e for e in cuerpo["ejes"]}
        out[bloque]["_nombre"] = cuerpo["nombre"]
    return out


def _sellados_de(eje: dict) -> dict:
    return {c["celda"]: {"p": c["p"], "ic95": c.get("ic95"), "n": c["n"]}
            for c in eje["celdas"]}


def _pct(v, q):
    return float(np.percentile(v, q)) if len(v) else None


def _marg(p, d):
    return {"desenlace_id": d, "p": float(p)}


def _plan(inputs: dict) -> tuple[list, list, dict, dict]:
    """(filas ENIF del dictamen, plan de pares EMITIBLE, ejes usados por
    desenlace, ejes del arbitro por bloque). Guardias que PARAN si el
    dictamen y el yaml no cuadran."""
    filas = _dictamen_enif(inputs)
    ejes_b = _ejes_arbitro(inputs)
    plan, usados = [], {}
    for r in filas:
        if r["veredicto"] != "EMITIBLE":
            continue
        ejes = ejes_b[r["bloque_desenlace"]]
        nombres = [k for k in ejes if not k.startswith("_")]
        a, b = _CC._parte_el_par(r["par"], nombres)
        d = r["desenlace_id"]
        if d not in DESENLACES:
            raise Paro(f"desenlace {d!r} del dictamen no es uno de {tuple(DESENLACES)}")
        if ejes["_nombre"] != d:
            raise Paro(f"bloque {r['bloque_desenlace']} nombra {ejes['_nombre']!r}, "
                       f"el dictamen {d!r}")
        for e in (a, b):
            if e not in EJES_ENIF:
                raise Paro(f"eje {e!r} del par {r['par']} no es admitido por marginal_enif")
            if ejes[e].get("universo_restringido"):
                raise Paro(f"eje {e!r} es de universo restringido: no compone")
        esperadas = len(ejes[a]["celdas"]) * len(ejes[b]["celdas"])
        if esperadas != int(r["n_celdas"]):
            raise Paro(f"{r['par']}: {esperadas} celdas por yaml, {r['n_celdas']} por dictamen")
        usados.setdefault(d, set()).update({a, b, "nacional"})
        plan.append((r, d, a, b, ejes))
    return filas, plan, usados, ejes_b


# ══ catalogo de RESULT: la spec lo declara, el test lo coteja ═══════════════

def catalogo_resultados(inputs: dict) -> list[dict]:
    """Todos los RESULT que `medir()` emite, con tipo y unidad, derivados del
    dictamen y del yaml -- la misma enumeracion que `medir()` recorre."""
    cat: list[dict] = []

    def add(rid, tipo, unidad, nulo=False):
        e = {"id": rid, "tipo": tipo, "unidad": unidad}
        if nulo:
            e["permite_no_estimable"] = True
        cat.append(e)

    for iid in INPUTS_PERMITIDOS:
        add(f"{P}-G-INPUT-{_slug(iid)}-SHA256", "texto", f"sha256 del input {iid}")
    for e in EJES_ENIF:
        add(f"{P}-G-P0-MODULO-GUARDADO-{_slug(e)}", "texto",
            "que lanza tools/celda_d/marginales_reproduccion.py::marginal() con este eje (sonda P0)")
    add(f"{P}-G-P0-MODULO-GUARDADO-EJES-ADMITIDOS", "entero",
        "ejes de ENIF 2024 que marginal() del modulo guardado admite por nombre (de 6)")
    add(f"{P}-G-P0-MODULO-GUARDADO-CARGA-ENIF", "texto",
        "si el modulo guardado puede cargar ENIF 2024 (carga_ola exige tmod_vic/tsdem)")
    add(f"{P}-G-GUARDIA-AST", "texto", "PASA si auditoria_ast() no reporta violaciones")
    add(f"{P}-G-GUARDIA-AST-VIOLACIONES", "entero", "violaciones reportadas por auditoria_ast()")
    add(f"{P}-G-DESVIACION-AUTORIZADA", "texto", "quien autorizo la guardia propia y cuando")
    add(f"{P}-G-N-FILAS-DICTAMEN-ENIF2024", "entero", "filas del dictamen con ola ENIF 2024 (A.13)")
    add(f"{P}-G-N-FILAS-EMITIBLES", "entero", "de ellas, EMITIBLE (un par x desenlace por fila)")
    add(f"{P}-G-N-CELDAS-EMITIBLES", "entero", "celdas de los pares EMITIBLE (re-derivado, no copiado)")
    add(f"{P}-G-EJES-USADOS", "texto", "ejes distintos que los pares EMITIBLE usan")
    add(f"{P}-G-FILAS-UNIVERSO", "entero", "personas elegidas 18+ en TMODULO tras las guardias del arbitro")
    add(f"{P}-G-ESTRATOS", "entero", "EST_DIS distintos")
    add(f"{P}-G-UPM", "entero", "UPM distintas (EST_DIS, UPM_DIS)")
    add(f"{P}-G-ESTRATOS-UPM-UNICA", "entero", "estratos con una sola UPM (no remuestrean)")
    add(f"{P}-G-POBLACION-EXPANDIDA", "flotante", "suma de FAC_PER")
    add(f"{P}-G-REPLICAS", "entero", "replicas compartidas por ola")
    add(f"{P}-G-SEED", "entero", "semilla PCG64 de las replicas compartidas")
    add(f"{P}-G-CONTROL-1-PUNTO-VEREDICTO", "texto",
        "REPRODUCE si cada punto = el sellado en CALC-C2-COMPUESTO-RESERVADAS-0001 a la tolerancia declarada")
    add(f"{P}-G-CONTROL-1-DELTA-MAX-ABS", "flotante", "peor |delta| punto re-derivado - sellado")
    add(f"{P}-G-CONTROL-1-N-CELDAS", "entero", "celdas cotejadas contra el CALC sellado")
    add(f"{P}-G-CONTROL-2-ARBITRO-VEREDICTO", "texto",
        "REPRODUCE si todos los marginales de la replica base reproducen los R sellados (p, IC y n a tolerancia)")
    add(f"{P}-G-CONTROL-2-DELTA-P-MAX", "flotante", "peor |delta p| marginal re-derivado - sellado")
    add(f"{P}-G-CONTROL-2-DELTA-IC-MAX", "flotante", "peor |delta IC95| marginal re-derivado - sellado")
    add(f"{P}-G-CONTROL-2-DELTA-N-MAX", "entero", "peor |delta n| marginal re-derivado - sellado")
    add(f"{P}-G-CONTROL-2-N-GRUPOS", "entero", "celdas marginales cotejadas (todas las de los ejes usados, por desenlace)")
    add(f"{P}-G-IC-PUBLICADO", "texto", "SI solo si los dos controles REPRODUCE; NO deja todos los IC en null")
    add(f"{P}-G-N-CELDAS-CON-IC", "entero", "celdas con IC95 publicado")
    add(f"{P}-G-N-CELDAS-IC-NO-CONSTRUIBLE", "entero", "celdas sin IC (causa en su IC-ESTADO)")
    add(f"{P}-G-REPLICAS-SIN-DEFINIR-TOTAL", "entero", "replicas con algun marginal en {0,1} o sin denominador, sumadas sobre celdas")
    add(f"{P}-G-C2-VECTORIZADO-VS-REFERENCIA-DELTA-MAX", "flotante",
        "peor |delta| entre el C2 vectorizado de la primera replica valida y piso_log_aditivo sobre esos mismos marginales")
    add(f"{P}-G-TIPO-INCERTIDUMBRE", "texto", "rotulo del IC")
    add(f"{P}-G-ROTULO-SUPUESTO", "texto", "supuesto del estimador")
    add(f"{P}-G-ESTADO-EMISION", "texto", "estado de las emisiones a las que este IC acompaña")
    add(f"{P}-G-ADOPTA", "texto", "NO")
    add(f"{P}-G-CRUCE-DERIVADO", "texto", "NO: no existe cruce() y la auditoria AST lo prueba")
    add(f"{P}-G-UNIDAD-DATO", "texto", "unidad del dato")
    add(f"{P}-G-PONDERADOR", "texto", "ponderador")
    add(f"{P}-G-DESENLACES", "texto", "desenlaces medidos")

    _filas, plan, usados, _ejes_b = _plan(inputs)
    for r, d, a, b, ejes in plan:
        for ca in ejes[a]["celdas"]:
            for cb in ejes[b]["celdas"]:
                base = f"{P}-{_slug(d)}-{_slug(r['par'])}-{_slug(ca['celda'])}-X-{_slug(cb['celda'])}"
                add(f"{base}-P", "proporcion", "punto C2 sobre marginales SELLADOS (= CALC-C2-COMPUESTO-RESERVADAS-0001)", True)
                add(f"{base}-P-REDERIVADO", "proporcion", "C2 sobre marginales re-derivados de la replica base (informativo)", True)
                add(f"{base}-IC95INF", "proporcion", "percentil 2.5 de C2_k sobre replicas definidas", True)
                add(f"{base}-IC95SUP", "proporcion", "percentil 97.5 de C2_k sobre replicas definidas", True)
                add(f"{base}-REPLICAS-VALIDAS", "entero", "replicas con los tres marginales en (0,1)")
                add(f"{base}-IC-ESTADO", "texto", "IC95-BOOTSTRAP-... o IC-NO-CONSTRUIBLE:<causa> o IC-NO-PUBLICADO:<causa>")
                add(f"{base}-CONTROL-1-DELTA", "flotante", "punto re-derivado - punto sellado", True)
    for d in sorted(usados):
        for e in sorted(usados[d]):
            pref = f"{P}-G-MARG-{_slug(d)}-{_slug(e)}"
            add(f"{pref}-COBERTURA", "proporcion", "filas dentro del eje / universo")
            add(f"{pref}-N-FUERA", "entero", "filas (fuera) del eje")
            add(f"{pref}-CONTROL-2-VEREDICTO", "texto", "cotejo() del modulo guardado contra los R sellados, y n exacto")
            add(f"{pref}-CONTROL-2-DELTA-P-MAX", "flotante", "peor |delta p| del eje")
            add(f"{pref}-CONTROL-2-DELTA-IC-MAX", "flotante", "peor |delta IC95| del eje")
            for k in _orden(e):
                c = f"{pref}-{_slug(k)}"
                add(f"{c}-N", "entero", "personas en la celda")
                add(f"{c}-NUMERADOR", "entero", "personas con el desenlace en la celda")
                add(f"{c}-P", "proporcion", "razon de totales ponderados", True)
                add(f"{c}-IC95INF", "proporcion", "wprop_ic_conglomerado (receta del arbitro)", True)
                add(f"{c}-IC95SUP", "proporcion", "wprop_ic_conglomerado (receta del arbitro)", True)
                add(f"{c}-DELTA-P", "flotante", "p re-derivado - p sellado", True)
                add(f"{c}-DELTA-N", "entero", "n re-derivado - n sellado", True)
                add(f"{c}-DELTA-IC95INF", "flotante", "IC95inf re-derivado - sellado (null si el sellado no trae IC)", True)
                add(f"{c}-DELTA-IC95SUP", "flotante", "IC95sup re-derivado - sellado (null si el sellado no trae IC)", True)
    return cat


# ══ el medidor ═════════════════════════════════════════════════════════════

def medir(inputs: dict, contrato: dict) -> dict:
    par = contrato["parametros"]
    n_rep = int(par["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    tol_p = float(par["control_arbitro_tol_p"])
    tol_ic = float(par["control_arbitro_tol_ic"])
    tol_punto = float(par["control_punto_tol"])
    umbral_validas = int(par["umbral_replicas_validas"])
    out: dict[str, object] = {}

    for iid in INPUTS_PERMITIDOS:
        out[f"{P}-G-INPUT-{_slug(iid)}-SHA256"] = str(inputs[iid]["sha256"])

    # ── P0 · sonda mecanica del modulo guardado: no admite ENIF 2024 ────
    admitidos = 0
    for e in EJES_ENIF:
        try:
            _MR.marginal(None, e)
            estado = "ADMITE-EJE-Y-OLA (inesperado)"
        except ValueError as exc:
            estado = f"NO-ADMITE-EJE · ValueError: {exc}"
        except TypeError as exc:
            admitidos += 1
            estado = f"ADMITE-EJE-POR-NOMBRE pero NO-ADMITE-OLA · TypeError: {exc}"
        out[f"{P}-G-P0-MODULO-GUARDADO-{_slug(e)}"] = estado[:300]
    out[f"{P}-G-P0-MODULO-GUARDADO-EJES-ADMITIDOS"] = admitidos
    out[f"{P}-G-P0-MODULO-GUARDADO-CARGA-ENIF"] = (
        "NO: carga_ola() exige conjunto_de_datos_tmod_vic_<ola>.csv y tsdem, "
        "universo BP1_20 y FAC_DEL; EJES=" + repr(tuple(_MR.EJES)))
    out[f"{P}-G-DESVIACION-AUTORIZADA"] = str(par["desviacion_autorizada"])

    # ── guardia AST antes de abrir el zip ────────────────────────────────
    viol = auditoria_ast(Path(__file__))
    out[f"{P}-G-GUARDIA-AST-VIOLACIONES"] = len(viol)
    out[f"{P}-G-GUARDIA-AST"] = "PASA" if not viol else "FALLA"
    if viol:
        raise SystemExit("PARO · guardia AST: " + " | ".join(viol[:10]))

    # ── dictamen y yaml del arbitro: pares, categorias y sellados ────────
    filas, plan, usados, ejes_b = _plan(inputs)
    out[f"{P}-G-N-FILAS-DICTAMEN-ENIF2024"] = len(filas)
    out[f"{P}-G-N-FILAS-EMITIBLES"] = len(plan)
    out[f"{P}-G-N-CELDAS-EMITIBLES"] = sum(
        len(ejes[a]["celdas"]) * len(ejes[b]["celdas"]) for _r, _d, a, b, ejes in plan)
    out[f"{P}-G-EJES-USADOS"] = " | ".join(
        sorted({e for s in usados.values() for e in s if e != "nacional"}))
    puntos_sellados = json.loads(
        _bytes(inputs, "IN-PUNTOS-SELLADOS").decode("utf-8"))["resultados"]

    # ── la ola, una vez; las replicas, una vez ───────────────────────────
    ola = _carga_ola_enif(inputs)
    rep = replicas_enif(ola, seed, n_rep)
    m = ola.meta
    out[f"{P}-G-FILAS-UNIVERSO"] = m["filas_universo"]
    out[f"{P}-G-ESTRATOS"] = m["estratos"]
    out[f"{P}-G-UPM"] = m["upm"]
    out[f"{P}-G-ESTRATOS-UPM-UNICA"] = rep.estratos_upm_unica
    out[f"{P}-G-POBLACION-EXPANDIDA"] = m["poblacion_expandida"]
    out[f"{P}-G-REPLICAS"] = n_rep
    out[f"{P}-G-SEED"] = seed

    # ── marginales de UN eje, por desenlace, con control 2 ───────────────
    marg: dict[tuple[str, str], dict] = {}
    peor_p, peor_ic, peor_n, n_grupos, todos_reproducen = 0.0, 0.0, 0, 0, True
    for d in sorted(usados):
        bloque = [b_ for b_, cuerpo in ejes_b.items() if cuerpo["_nombre"] == d][0]
        for e in sorted(usados[d]):
            r_ = marginal_enif(ola, e, desenlace=d, replicas=rep)
            marg[(d, e)] = r_
            if e == "nacional":
                nac = _CC.NACIONALES[d]
                sellados = {"NAC": {"p": nac["p"], "ic95": nac["ic95"], "n": nac["n"]}}
            else:
                sellados = _sellados_de(ejes_b[bloque][e])
            cot = _MR.cotejo(r_, sellados, tol_p, tol_ic)
            pref = f"{P}-G-MARG-{_slug(d)}-{_slug(e)}"
            out[f"{pref}-COBERTURA"] = r_["cobertura"]
            out[f"{pref}-N-FUERA"] = r_["n_fuera"]
            out[f"{pref}-CONTROL-2-DELTA-P-MAX"] = float(cot["delta_p_max"])
            out[f"{pref}-CONTROL-2-DELTA-IC-MAX"] = float(cot["delta_ic_max"])
            dn_eje = 0
            for k in _orden(e):
                c = r_["celdas"][k]
                cid = f"{pref}-{_slug(k)}"
                out[f"{cid}-N"] = c["n"]
                out[f"{cid}-NUMERADOR"] = c["numerador"]
                out[f"{cid}-P"] = c["p"]
                out[f"{cid}-IC95INF"] = c["ic95"][0] if c["ic95"] else None
                out[f"{cid}-IC95SUP"] = c["ic95"][1] if c["ic95"] else None
                f_ = cot["filas"].get(k, {})
                out[f"{cid}-DELTA-P"] = f_.get("delta_p")
                out[f"{cid}-DELTA-N"] = f_.get("delta_n")
                out[f"{cid}-DELTA-IC95INF"] = f_.get("delta_ic95inf")
                out[f"{cid}-DELTA-IC95SUP"] = f_.get("delta_ic95sup")
                if f_.get("delta_n") is not None:
                    dn_eje = max(dn_eje, abs(int(f_["delta_n"])))
                if f_.get("estado") == "NO-ESTIMABLE":
                    dn_eje = max(dn_eje, 1)          # celda sellada sin estimar aqui
                n_grupos += 1
            veredicto = cot["veredicto"] if dn_eje == 0 else "NO-REPRODUCE"
            out[f"{pref}-CONTROL-2-VEREDICTO"] = veredicto
            peor_p = max(peor_p, float(cot["delta_p_max"]))
            peor_ic = max(peor_ic, float(cot["delta_ic_max"]))
            peor_n = max(peor_n, dn_eje)
            if veredicto != "REPRODUCE":
                todos_reproducen = False
    out[f"{P}-G-CONTROL-2-ARBITRO-VEREDICTO"] = "REPRODUCE" if todos_reproducen else "NO-REPRODUCE"
    out[f"{P}-G-CONTROL-2-DELTA-P-MAX"] = peor_p
    out[f"{P}-G-CONTROL-2-DELTA-IC-MAX"] = peor_ic
    out[f"{P}-G-CONTROL-2-DELTA-N-MAX"] = int(peor_n)
    out[f"{P}-G-CONTROL-2-N-GRUPOS"] = n_grupos

    # ── C2 por celda: punto sellado (control 1) + IC replica por replica ─
    celdas_out = []
    delta1_max, n_ctrl1, ctrl1_ok = 0.0, 0, True
    delta_vec_max = 0.0
    for r, d, a, b, ejes in plan:
        nac_p = _CC.NACIONALES[d]["p"]
        for ca in ejes[a]["celdas"]:
            for cb in ejes[b]["celdas"]:
                base = f"{P}-{_slug(d)}-{_slug(r['par'])}-{_slug(ca['celda'])}-X-{_slug(cb['celda'])}"
                try:
                    punto = piso_log_aditivo(_marg(ca["p"], d), _marg(cb["p"], d),
                                             _marg(nac_p, d))["p"]
                except MarginalDegenerado:
                    punto = None
                out[f"{base}-P"] = punto
                sid = (f"RESULT-C2COMP-{_slug(d)}-{_slug(r['par'])}"
                       f"-{_slug(ca['celda'])}-X-{_slug(cb['celda'])}")
                sellado = puntos_sellados.get(sid)
                if punto is None:
                    out[f"{base}-CONTROL-1-DELTA"] = None
                    ctrl1_ok = False
                elif sellado is None:
                    out[f"{base}-CONTROL-1-DELTA"] = None
                    ctrl1_ok = False
                else:
                    dl = float(punto) - float(sellado)
                    out[f"{base}-CONTROL-1-DELTA"] = dl
                    delta1_max = max(delta1_max, abs(dl))
                    n_ctrl1 += 1
                ma = marg[(d, a)]["celdas"][ca["celda"]]
                mb = marg[(d, b)]["celdas"][cb["celda"]]
                mn = marg[(d, "nacional")]["celdas"]["NAC"]
                try:
                    out[f"{base}-P-REDERIVADO"] = float(piso_log_aditivo(
                        _marg(ma["p"], d), _marg(mb["p"], d), _marg(mn["p"], d))["p"])
                except (MarginalDegenerado, TypeError):
                    out[f"{base}-P-REDERIVADO"] = None
                ra, rb, rn = ma["replicas"], mb["replicas"], mn["replicas"]
                # replica valida <=> los tres marginales en (0,1): |p-0.5|<0.5
                # (NaN queda fuera); las validaciones se MULTIPLICAN, no se
                # combinan por comparaciones (R4 de la auditoria).
                va = np.abs(ra - 0.5) < 0.5
                vb = np.abs(rb - 0.5) < 0.5
                vn = np.abs(rn - 0.5) < 0.5
                ok = (va * vb * vn).astype(bool)
                n_ok = int(ok.sum())
                with np.errstate(all="ignore"):
                    lc2 = (np.log(ra / (1 - ra)) + np.log(rb / (1 - rb))
                           - np.log(rn / (1 - rn)))
                    c2r = 1.0 / (1.0 + np.exp(-lc2[ok]))
                if n_ok:
                    k0 = int(np.flatnonzero(ok)[0])
                    ref = piso_log_aditivo(_marg(ra[k0], d), _marg(rb[k0], d),
                                           _marg(rn[k0], d))["p"]
                    delta_vec_max = max(delta_vec_max, abs(float(c2r[0]) - float(ref)))
                celdas_out.append((base, n_ok, c2r, punto))
    out[f"{P}-G-CONTROL-1-PUNTO-VEREDICTO"] = (
        "REPRODUCE" if ctrl1_ok and delta1_max <= tol_punto else "NO-REPRODUCE")
    out[f"{P}-G-CONTROL-1-DELTA-MAX-ABS"] = delta1_max
    out[f"{P}-G-CONTROL-1-N-CELDAS"] = n_ctrl1
    out[f"{P}-G-C2-VECTORIZADO-VS-REFERENCIA-DELTA-MAX"] = delta_vec_max

    # ── publicacion: los dos controles, o ningun IC ──────────────────────
    causa_no = []
    if out[f"{P}-G-CONTROL-1-PUNTO-VEREDICTO"] != "REPRODUCE":
        causa_no.append("CONTROL-1-NO-REPRODUCE")
    if out[f"{P}-G-CONTROL-2-ARBITRO-VEREDICTO"] != "REPRODUCE":
        causa_no.append("CONTROL-2-NO-REPRODUCE")
    publica = not causa_no
    con_ic, sin_ic, sin_definir = 0, 0, 0
    for base, n_ok, c2r, punto in celdas_out:
        sin_definir += n_rep - n_ok
        out[f"{base}-REPLICAS-VALIDAS"] = n_ok
        if not publica:
            estado = "IC-NO-PUBLICADO:" + "+".join(causa_no)
            lo = hi = None
        elif punto is None:
            estado = "IC-NO-CONSTRUIBLE:PUNTO-SIN-DEFINIR"
            lo = hi = None
        elif n_ok < umbral_validas:
            estado = f"IC-NO-CONSTRUIBLE:REPLICAS-VALIDAS-{n_ok}<{umbral_validas}"
            lo = hi = None
        else:
            estado = IC_ROTULO
            lo, hi = _pct(c2r, 2.5), _pct(c2r, 97.5)
        out[f"{base}-IC95INF"] = lo
        out[f"{base}-IC95SUP"] = hi
        out[f"{base}-IC-ESTADO"] = estado
        if lo is None:
            sin_ic += 1
        else:
            con_ic += 1
    out[f"{P}-G-IC-PUBLICADO"] = "SI" if publica else "NO"
    out[f"{P}-G-N-CELDAS-CON-IC"] = con_ic
    out[f"{P}-G-N-CELDAS-IC-NO-CONSTRUIBLE"] = sin_ic
    out[f"{P}-G-REPLICAS-SIN-DEFINIR-TOTAL"] = int(sin_definir)
    out[f"{P}-G-TIPO-INCERTIDUMBRE"] = IC_ROTULO if publica else "NO-PUBLICADA"
    out[f"{P}-G-ROTULO-SUPUESTO"] = ROTULO_SUPUESTO
    out[f"{P}-G-ESTADO-EMISION"] = "EMITIDA-SIN-EVALUAR"
    out[f"{P}-G-ADOPTA"] = "NO"
    out[f"{P}-G-CRUCE-DERIVADO"] = "NO"
    out[f"{P}-G-UNIDAD-DATO"] = "PERSONA elegida 18+"
    out[f"{P}-G-PONDERADOR"] = "FAC_PER"
    out[f"{P}-G-DESENLACES"] = " | ".join(sorted(usados))
    return out
