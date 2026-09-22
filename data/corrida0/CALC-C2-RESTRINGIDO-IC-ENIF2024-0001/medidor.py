#!/usr/bin/env python3
"""Medidor de `CALC-C2-RESTRINGIDO-IC-ENIF2024-0001` (COMMIT-2).

ACTO `GEN2-DIN-LOTE-C2-RESTRINGIDO-1` (22/sep/2026, CAJA). Contrato humano:
`forense/prereg-caja/C2-RESTRINGIDO-ENIF2024-spec-v1_0.md`, congelado en el
COMMIT-1 junto con este archivo, ANTES de abrir una sola respuesta de ENIF
2024. Interfaz del plan v2.0 §4 (B-1): `medir(inputs, contrato) -> dict`; el
medidor no abre `spec.yaml`.

QUE HACE
--------
Da piso a los cinco pares `formalidad x eje` del lote ENIF 2024 que el C2
compuesto dejo NO-EMITIBLE por universo restringido (A-bis 4): un C2
restringido al universo T de quien trabaja (`P3_13` en 1..7),

    C2R(i, j) = expit( logit p_T(a=i) + logit p_T(b=j) - logit p_T )

con p_T(eje=k) = p(D9 | eje=k, T) -- marginales de UN eje cada uno, dentro de
T -- y p_T = p(D9 | T). El marginal de `formalidad` se CITA del arbitro GEN2
sellado (`CALC-ARBITRO-MARGINALES-ENIF2024-0001`); re-derivarlo aqui es el oro.
IC95 replica por replica con el plan de replicas del arbitro GEN2 (el de
`_estimate` del piso). Nada se compara contra el universo poblacional.

GUARDIA DE RESERVA -- codigo, no prosa (E.6)
---------------------------------------------
1. `marginal_t(ola, grupo)`: `grupo` es UN `str` posicional; una lista o dos
   argumentos lanzan `TypeError`; un eje fuera de `EJES_T` lanza `ValueError`;
   la ola se re-huella antes de contar y una ola filtrada o reordenada lanza
   `ReservaRota`. No existe `cruce()`.
2. `auditoria_ast(ruta)` recorre el AST de ESTE archivo al arrancar `medir()`
   (y en `tests/test_c2_restringido_enif2024_guardia.py`, con controles
   positivos). Si falla, `medir()` PARA antes de abrir el zip.

Este archivo no ve, no deriva y no imprime ningun cruce `formalidad x eje`.
No adopta nada.
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


# El arbitro de ENIF 2024: universo (`carga()`), desenlaces (`desenlaces()`) y
# construccion de cada eje (`EJES_P2`, `EJE_CUENTA_PRINCIPAL`).
_ARB = _importa("medidor_ahorro_enif24", RAIZ / "tools" / "medidor_ahorro_enif24.py")
# La forma de C2, pinada por contrato: importada, no reimplementada.
_C2 = _importa("test_celda_d_c2", RAIZ / "tests" / "test_celda_d_c2.py")
# La misma serializacion de ids y el mismo partidor de pares que el C2 compuesto.
_CC = _importa("c2_compuesto", RAIZ / "tools" / "c2_compuesto.py")

piso_log_aditivo = _C2.piso_log_aditivo
MarginalDegenerado = _C2.MarginalDegenerado
FUERA = _ARB.FUERA

P = "RESULT-C2R-ENIF2024"
OLA = "ENIF 2024"
PAYLOAD_ID = "enif_2024_enif_2024_bd_csv"
PAYLOAD_ARCHIVO = "enif_2024_bd_csv.zip"
PAYLOAD_TABLA = "TMODULO.csv"
INPUTS_PERMITIDOS = (
    PAYLOAD_ID, "IN-DICTAMEN", "IN-LOTE-CONTRATO", "IN-ARBITRO-GEN2",
    "IN-SPEC-SELLADA", "IN-ARBITRO-MEDIDOR", "IN-ARBITRO-EJES",
    "IN-FORMA-C2-SELLADA", "IN-C2-COMPUESTO",
)
# Ejes que este medidor ADMITE, todos dentro de T. `nacional` es T entero.
EJES_T = ("sexo", "edad", "escolaridad", "localidad", "cuenta_formal",
          "formalidad", "nacional")
EJE_UNIVERSO = "formalidad"
NAC_T = "T"
DESENLACE = "ahorra_solo_informal"
DESENLACE_ARBITRO = "ahorra_solo_informal (PRINCIPAL)"
DESENLACES = (DESENLACE,)
ROTULO_SUPUESTO = "ausencia de interaccion en escala logit"
IC_ROTULO = "IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS-UNIVERSO-T"
UNIVERSO_T = ("T = quien trabaja: persona elegida 18+ de ENIF 2024 con P3_13 en 1..7 "
              "(3.13 derecho a servicios medicos por el trabajo); blanco por secuencia "
              "y 9 (no sabe) fuera de T")
_slug = _CC._slug


class ReservaRota(RuntimeError):
    """Se intento cruzar, filtrar o alterar la ola fuera de lo autorizado."""


class Paro(RuntimeError):
    """Premisa de la spec falsa en el archivo: se PARA, no se reporta cifra."""


# ══ nucleo guardado: las UNICAS funciones que tocan el microdato (`.df`) ════

@dataclass(frozen=True)
class OlaT:
    df: pd.DataFrame = field(repr=False, compare=False)
    huella: str = ""
    meta: dict = field(default_factory=dict, compare=False)


def _ejes_del_arbitro() -> dict:
    ejes = {e.nombre: e for e in _ARB.EJES_P2}
    ejes["cuenta_formal"] = _ARB.EJE_CUENTA_PRINCIPAL
    return ejes


def _huella(df: pd.DataFrame) -> str:
    """sha256 de las columnas que definen la ola, en orden de archivo: una
    fila filtrada, reordenada o alterada cambia la huella."""
    h = hashlib.sha256()
    h.update(str(len(df)).encode())
    for c in ("EST_DIS", "UPM_DIS", "_w", *EJES_T, f"_y_{DESENLACE}"):
        h.update(b"\x1f")
        h.update("\n".join(df[c].astype(str).tolist()).encode("utf-8"))
    return h.hexdigest()


def _ola_desde_df(df: pd.DataFrame) -> OlaT:
    """Construye la ola T desde el DataFrame que `carga()` del arbitro
    devuelve. Cada columna nace de UN eje del arbitro; la restriccion al
    universo T (formalidad dentro) se aplica aqui, una vez, igual para todos
    los ejes: fuera de T la columna vale FUERA. Ninguna fila se quita."""
    ejes = _ejes_del_arbitro()
    des = _ARB.desenlaces(df)
    d = pd.DataFrame(index=df.index)
    d["EST_DIS"] = df["EST_DIS"].astype(str).str.strip()
    d["UPM_DIS"] = df["UPM_DIS"].astype(str).str.strip()
    d["_w"] = df["_w"].astype(float)
    universo = ejes[EJE_UNIVERSO].deriva(df).astype(str).to_numpy()
    fuera_de_t = universo == FUERA
    for nombre in EJES_T[:-1]:
        crudo = ejes[nombre].deriva(df).astype(str).to_numpy()
        d[nombre] = np.where(fuera_de_t, FUERA, crudo)
    d["nacional"] = np.where(fuera_de_t, FUERA, NAC_T)
    d[f"_y_{DESENLACE}"] = des[DESENLACE_ARBITRO].astype(float)
    d = d.reset_index(drop=True)
    if (d["EST_DIS"] == "").any():
        raise Paro("ENIF 2024: EST_DIS con faltantes")
    if (d["UPM_DIS"] == "").any():
        raise Paro("ENIF 2024: UPM_DIS con faltantes")
    en_t = d["nacional"].to_numpy() == NAC_T
    if not en_t.any():
        raise Paro("ENIF 2024: el universo T (P3_13 en 1..7) esta vacio")
    w = d["_w"].to_numpy()
    meta = {
        "filas_universo": int(len(d)),
        "filas_t": int(en_t.sum()),
        "fuera_t": int((~en_t).sum()),
        "cobertura_t_filas": float(en_t.mean()),
        "cobertura_t_ponderada": float(w[en_t].sum() / w.sum()),
        "estratos": int(d["EST_DIS"].nunique()),
        "upm": int((d["EST_DIS"] + "\t" + d["UPM_DIS"]).nunique()),
        "upm_con_t": int((d["EST_DIS"] + "\t" + d["UPM_DIS"])[en_t].nunique()),
        "poblacion_expandida": float(w.sum()),
        "poblacion_t": float(w[en_t].sum()),
    }
    return OlaT(df=d, huella=_huella(d), meta=meta)


def _carga_ola_enif(inputs: dict) -> OlaT:
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


def _verifica(ola: OlaT) -> None:
    if not isinstance(ola, OlaT):
        raise TypeError("se esperaba una OlaT producida por _carga_ola_enif()")
    if _huella(ola.df) != ola.huella:
        raise ReservaRota("ENIF 2024: la ola fue filtrada, reordenada o alterada "
                          "tras cargarla -- agrupar sobre un subconjunto es "
                          "cruzar por otra via")


@dataclass(frozen=True)
class ReplicasT:
    huella_ola: str
    seed: int
    n_rep: int
    bloque: int
    counts: np.ndarray = field(repr=False, compare=False)   # (n_rep, n_upm)
    pos_fila: np.ndarray = field(repr=False, compare=False)  # fila -> upm
    n_upm: int = 0
    estratos_upm_unica: int = 0


def replicas_t(ola: OlaT, seed: int, n_rep: int, bloque: int) -> ReplicasT:
    """UN plan de replicas por ola, compartido por todos los grupos y celdas.
    Es el plan de `_estimate` del piso que el arbitro GEN2 importo
    (`data/corrida0/CALC-PISOS-ENIF2021-EJES-0003/medidor.py:57-95`): llaves
    `EST\\tUPM` de todas las filas, ordenadas; estratos ordenados; UN
    generador PCG64(seed); bloques de `bloque` replicas y, dentro de cada
    bloque, estrato por estrato, `integers(0, n_h, size=(bloque, n_h))`."""
    _verifica(ola)
    est = ola.df["EST_DIS"].to_numpy()
    upm = ola.df["UPM_DIS"].to_numpy()
    llaves = np.array([f"{e}\t{u}" for e, u in zip(est, upm)])
    unicas, pos_fila = np.unique(llaves, return_inverse=True)
    n_upm = len(unicas)
    estratos: dict[str, list[int]] = {}
    for pos, llave in enumerate(unicas.tolist()):
        estratos.setdefault(llave.split("\t", 1)[0], []).append(pos)
    rng = np.random.Generator(np.random.PCG64(seed))
    counts = np.zeros((n_rep, n_upm), dtype=np.int32)
    for inicio in range(0, n_rep, bloque):
        tam = min(bloque, n_rep - inicio)
        for h in sorted(estratos):
            ix = np.asarray(estratos[h], dtype=np.int64)
            sorteos = rng.integers(0, len(ix), size=(tam, len(ix)))
            for fila in range(tam):
                counts[inicio + fila] += np.bincount(ix[sorteos[fila]],
                                                     minlength=n_upm).astype(np.int32)
    unica = sum(1 for h in estratos if len(estratos[h]) == 1)
    return ReplicasT(huella_ola=ola.huella, seed=int(seed), n_rep=int(n_rep),
                     bloque=int(bloque), counts=counts,
                     pos_fila=np.asarray(pos_fila, dtype=np.int64).ravel(),
                     n_upm=int(n_upm), estratos_upm_unica=int(unica))


def _reps_de_mascara(ola: OlaT, rep: ReplicasT, mask: np.ndarray,
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


def marginal_t(ola: OlaT, grupo: str, *, desenlace: str,
               replicas: ReplicasT | None = None) -> dict:
    """Celdas de UN eje de la ola, dentro de T. `grupo` es un `str`
    POSICIONAL UNICO -- no hay `*grupos`, no hay lista; el eje ya viene
    derivado por el arbitro y restringido a T en su propia columna, y solo
    puede ser uno de `EJES_T`. `desenlace` selecciona la variable, no agrupa."""
    if not isinstance(grupo, str):
        raise TypeError(f"grupo debe ser UN str, llego {type(grupo).__name__}: "
                        "una sola variable de agrupacion por firma")
    if grupo not in EJES_T:
        raise ValueError(f"grupo {grupo!r} no es un eje autorizado {EJES_T}")
    if desenlace not in DESENLACES:
        raise ValueError(f"desenlace {desenlace!r} no es uno de {DESENLACES}")
    _verifica(ola)
    if replicas is not None:
        if replicas.huella_ola != ola.huella:
            raise ReservaRota("las replicas no son de esta ola")
    y_col = f"_y_{desenlace}"
    celda = ola.df[grupo].to_numpy()
    en_t = ola.df["nacional"].to_numpy() == NAC_T
    dentro = celda != FUERA
    w_all = ola.df["_w"].to_numpy()
    y_all = ola.df[y_col].to_numpy()
    out = {"eje": grupo, "desenlace": desenlace, "n_t": int(en_t.sum()),
           "n_dentro": int(dentro.sum()), "celdas": {}}
    for k in _orden(grupo):
        mask = celda == k
        n = int(mask.sum())
        fila = {"n": n, "numerador": int(y_all[mask].sum()),
                "den_w": float(w_all[mask].sum()), "p": None, "ic95": None,
                "b_validas": 0, "replicas": None}
        if n:
            den = float(w_all[mask].sum())
            fila["p"] = float((w_all[mask] * y_all[mask]).sum() / den) if den > 0 else None
        if replicas is not None:
            reps = _reps_de_mascara(ola, replicas, mask, y_col)
            fin = np.isfinite(reps)
            fila["replicas"] = reps
            fila["b_validas"] = int(fin.sum())
            if fila["p"] is not None:
                if fila["b_validas"]:
                    lo, hi = np.percentile(reps[fin], [2.5, 97.5])
                    fila["ic95"] = [float(lo), float(hi)]
        out["celdas"][k] = fila
    return out


def _orden(grupo: str) -> list[str]:
    if grupo == "nacional":
        return [NAC_T]
    return list(_ejes_del_arbitro()[grupo].orden)


# ══ auditoria del AST de este archivo: la guardia E.6 como codigo ══════════

NUCLEO = ("_huella", "_ola_desde_df", "_carga_ola_enif", "_verifica",
          "replicas_t", "_reps_de_mascara", "marginal_t")
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
_AUDIT_MODULOS_IMPORTADOS = ("medidor_ahorro_enif24.py", "test_celda_d_c2.py",
                             "c2_compuesto.py")
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
    PASA). Reglas, una por una, en `tests/test_c2_restringido_enif2024_guardia.py`
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
            if nom == "OlaT":
                if fn != "_ola_desde_df":
                    viol.append(f"R5 `OlaT(` fuera de _ola_desde_df: {fn}")
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
            # R6 · marginal_t: UN grupo posicional, nombre o literal str
            if nom == "marginal_t":
                if len(nodo.args) != 2:
                    viol.append(f"R6 marginal_t con {len(nodo.args)} posicionales en {fn}")
                elif not isinstance(nodo.args[1], (ast.Name, ast.Constant)):
                    viol.append(f"R6 marginal_t con grupo no atomico en {fn}")
                elif isinstance(nodo.args[1], ast.Constant) \
                        and not isinstance(nodo.args[1].value, str):
                    viol.append(f"R6 marginal_t con grupo literal no str en {fn}")
                for kw in nodo.keywords:
                    if kw.arg not in ("desenlace", "replicas"):
                        viol.append(f"R6 marginal_t con keyword `{kw.arg}` en {fn}")
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


def _dictamen_no_emitibles(inputs: dict) -> list[dict]:
    """Filas del dictamen sellado de ENIF 2024, D9, NO-EMITIBLE (leidas)."""
    texto = _bytes(inputs, "IN-DICTAMEN").decode("utf-8")
    lineas = [l for l in texto.splitlines() if not l.startswith("#")]
    filas = []
    for r in csv.DictReader(lineas, delimiter="\t"):
        if r["ola"] != OLA:
            continue
        if r["desenlace_id"] != DESENLACE:
            continue
        if r["veredicto"] != "NO-EMITIBLE":
            continue
        filas.append(r)
    return filas


def _contrato_lote(inputs: dict) -> dict:
    doc = yaml.safe_load(_bytes(inputs, "IN-LOTE-CONTRATO").decode("utf-8"))
    return doc["parametros"]


def _plan(inputs: dict) -> dict:
    """Pares, categorias e ids sellados, leidos del contrato del lote y del
    dictamen. Guardias que PARAN si no cuadran entre si ni con el arbitro."""
    lote = _contrato_lote(inputs)
    dic = _dictamen_no_emitibles(inputs)
    ejes = lote["ejes"]
    pares = []
    for nombre, cuerpo in lote["pares"].items():
        if not str(cuerpo["c2"]).startswith("NO-EMITIBLE"):
            continue
        if EJE_UNIVERSO not in (cuerpo["a"], cuerpo["b"]):
            continue
        pares.append((nombre, cuerpo["a"], cuerpo["b"]))
    if len(pares) != 5:
        raise Paro(f"el contrato del lote trae {len(pares)} pares NO-EMITIBLE con "
                   f"{EJE_UNIVERSO}, no 5")
    por_par = {r["par"]: r for r in dic}
    if sorted(por_par) != sorted(p for p, _a, _b in pares):
        raise Paro(f"dictamen {sorted(por_par)} != contrato {sorted(p for p, _a, _b in pares)}")
    for nombre, a, b in pares:
        if _CC._parte_el_par(nombre, list(ejes)) != (a, b):
            raise Paro(f"{nombre}: el partidor no da ({a}, {b})")
        for e in (a, b):
            if e not in EJES_T:
                raise Paro(f"eje {e!r} del par {nombre} no es admitido por marginal_t")
            if list(ejes[e]["orden"]) != _orden(e):
                raise Paro(f"eje {e}: orden del contrato {ejes[e]['orden']} != arbitro {_orden(e)}")
        esperadas = len(ejes[a]["orden"]) * len(ejes[b]["orden"])
        if esperadas != int(por_par[nombre]["n_celdas"]):
            raise Paro(f"{nombre}: {esperadas} celdas por contrato, "
                       f"{por_par[nombre]['n_celdas']} por dictamen")
    sellados = lote["marginales_sellados"]["puntos"]["ids"][EJE_UNIVERSO]
    return {"pares": pares, "ejes": {e: list(ejes[e]["orden"]) for e in ejes},
            "cobertura_declarada": float(ejes[EJE_UNIVERSO]["cobertura_arbitro"]),
            "formalidad_ids_p": dict(sellados), "n_filas_dictamen": len(dic)}


# ══ catalogo de RESULT: la spec lo declara, el test lo coteja ═══════════════

def _base_celda(par: str, ca: str, cb: str) -> str:
    return f"{P}-{_slug(DESENLACE)}-{_slug(par)}-{_slug(ca)}-X-{_slug(cb)}"


def _pref_marg(e: str) -> str:
    return f"{P}-G-MARG-T-{_slug(e)}"


def _ejes_usados(plan: dict) -> list[str]:
    usados = {e for _p, a, b in plan["pares"] for e in (a, b)}
    usados.add("nacional")
    return [e for e in EJES_T if e in usados]


def catalogo_resultados(inputs: dict) -> list[dict]:
    """Todos los RESULT que `medir()` emite, con tipo y unidad, derivados del
    contrato del lote y del dictamen -- la misma enumeracion que `medir()`."""
    cat: list[dict] = []
    plan = _plan(inputs)
    u_t = (f"universo T = quien trabaja (P3_13 en 1..7; blanco y 9 fuera), "
           f"cobertura declarada {plan['cobertura_declarada']} (arbitro); "
           "no comparable con el universo poblacional (A-bis 4)")

    def add(rid, tipo, unidad, nulo=False):
        e = {"id": rid, "tipo": tipo, "unidad": unidad}
        if nulo:
            e["permite_no_estimable"] = True
        cat.append(e)

    for iid in INPUTS_PERMITIDOS:
        add(f"{P}-G-INPUT-{_slug(iid)}-SHA256", "texto", f"sha256 del input {iid}")
    add(f"{P}-G-GUARDIA-AST", "texto", "PASA si auditoria_ast() no reporta violaciones")
    add(f"{P}-G-GUARDIA-AST-VIOLACIONES", "entero", "violaciones reportadas por auditoria_ast()")
    add(f"{P}-G-N-FILAS-DICTAMEN-NO-EMITIBLES", "entero",
        "filas del dictamen ENIF 2024, D9, NO-EMITIBLE (A.13)")
    add(f"{P}-G-N-PARES", "entero", "pares con formalidad NO-EMITIBLE en el contrato del lote")
    add(f"{P}-G-N-CELDAS", "entero", "celdas de esos pares (re-derivado, no copiado)")
    add(f"{P}-G-PARES", "texto", "pares, en el orden del contrato del lote")
    add(f"{P}-G-EJES-USADOS", "texto", "ejes cuyos marginales dentro de T se derivan")
    add(f"{P}-G-UNIVERSO", "texto", "definicion del universo T")
    add(f"{P}-G-COBERTURA-DECLARADA", "proporcion", "cobertura de formalidad del arbitro (contrato del lote)")
    add(f"{P}-G-FILAS-UNIVERSO", "entero", "personas elegidas 18+ en TMODULO tras las guardias del arbitro")
    add(f"{P}-G-FILAS-T", "entero", "personas en T")
    add(f"{P}-G-FUERA-T", "entero", "personas fuera de T (P3_13 blanco o 9)")
    add(f"{P}-G-COBERTURA-T-FILAS", "proporcion", "filas de T / filas del universo del arbitro")
    add(f"{P}-G-COBERTURA-T-PONDERADA", "proporcion", "masa FAC_PER de T / masa del universo del arbitro")
    add(f"{P}-G-ESTRATOS", "entero", "EST_DIS distintos (marco entero)")
    add(f"{P}-G-UPM", "entero", "UPM distintas (EST_DIS, UPM_DIS), marco entero que se remuestrea")
    add(f"{P}-G-UPM-CON-T", "entero", "UPM con al menos una persona de T")
    add(f"{P}-G-ESTRATOS-UPM-UNICA", "entero", "estratos con una sola UPM (no remuestrean)")
    add(f"{P}-G-POBLACION-EXPANDIDA", "flotante", "suma de FAC_PER del universo del arbitro")
    add(f"{P}-G-POBLACION-T", "flotante", "suma de FAC_PER de T")
    add(f"{P}-G-REPLICAS", "entero", "replicas del plan compartido")
    add(f"{P}-G-REPLICAS-BLOQUE", "entero", "tamano de bloque del plan de replicas (el del piso)")
    add(f"{P}-G-SEED", "entero", "semilla PCG64 del plan de replicas")
    add(f"{P}-G-CONTROL-ARBITRO-VEREDICTO", "texto",
        "REPRODUCE si formalidad re-derivada en T = R sellados del arbitro GEN2 (P, IC, N, B-VALIDAS, DEN-W) y filas/fuera exactas")
    add(f"{P}-G-CONTROL-ARBITRO-DELTA-P-MAX", "flotante", "peor |delta P| formalidad re-derivada - sellada", True)
    add(f"{P}-G-CONTROL-ARBITRO-DELTA-IC-MAX", "flotante", "peor |delta IC| formalidad re-derivada - sellada", True)
    add(f"{P}-G-CONTROL-ARBITRO-DELTA-DEN-W-MAX", "flotante", "peor |delta DEN-W| formalidad", True)
    add(f"{P}-G-CONTROL-ARBITRO-DELTA-FILAS", "entero", "filas del universo - G-FILAS-PERSONAS sellado")
    add(f"{P}-G-CONTROL-ARBITRO-DELTA-FUERA-T", "entero", "fuera de T - G-EJE-FORMALIDAD-FUERA sellado")
    add(f"{P}-G-IC-PUBLICADO", "texto", "SI solo si el control del arbitro REPRODUCE; NO deja todos los IC en null")
    add(f"{P}-G-N-CELDAS-CON-IC", "entero", "celdas C2R con IC95 publicado")
    add(f"{P}-G-N-CELDAS-SIN-IC", "entero", "celdas C2R sin IC (causa en su IC-ESTADO)")
    add(f"{P}-G-N-CELDAS-SIN-PUNTO", "entero", "celdas C2R con punto null (NO-CONSTRUIBLE)")
    add(f"{P}-G-REPLICAS-SIN-DEFINIR-TOTAL", "entero",
        "replicas con algun marginal en {0,1} o sin denominador, sumadas sobre celdas")
    add(f"{P}-G-C2-VECTORIZADO-VS-REFERENCIA-DELTA-MAX", "flotante",
        "peor |delta| entre el C2R vectorizado de la primera replica valida y piso_log_aditivo", True)
    add(f"{P}-G-CUENTA-FORMALXFORMALIDAD-DEGENERACION", "texto",
        "NO-DEGENERADO o DEGENERADO:<causa> (regla de la spec §8, fijada antes del dato)")
    add(f"{P}-G-TIPO-INCERTIDUMBRE", "texto", "rotulo del IC")
    add(f"{P}-G-ROTULO-SUPUESTO", "texto", "supuesto del estimador")
    add(f"{P}-G-COMPARACION-POBLACIONAL", "texto", "NINGUNA (A-bis 4)")
    add(f"{P}-G-ESTADO-EMISION", "texto", "estado de las emisiones")
    add(f"{P}-G-ADOPTA", "texto", "NO")
    add(f"{P}-G-CRUCE-DERIVADO", "texto", "NO: no existe cruce() y la auditoria AST lo prueba")
    add(f"{P}-G-UNIDAD-DATO", "texto", "unidad del dato")
    add(f"{P}-G-PONDERADOR", "texto", "ponderador")
    add(f"{P}-G-DESENLACE", "texto", "desenlace medido")

    for par, a, b in plan["pares"]:
        for ca in plan["ejes"][a]:
            for cb in plan["ejes"][b]:
                base = _base_celda(par, ca, cb)
                add(f"{base}-P", "proporcion", f"C2 restringido (punto) · {u_t}", True)
                add(f"{base}-IC95INF", "proporcion", f"percentil 2.5 de C2R_k validas · {u_t}", True)
                add(f"{base}-IC95SUP", "proporcion", f"percentil 97.5 de C2R_k validas · {u_t}", True)
                add(f"{base}-REPLICAS-VALIDAS", "entero", f"replicas con los tres marginales en (0,1) · {u_t}")
                add(f"{base}-IC-ESTADO", "texto", f"{IC_ROTULO} o IC-NO-CONSTRUIBLE:<causa> o IC-NO-PUBLICADO:<causa> · {u_t}")
                add(f"{base}-UNIVERSO", "texto", f"universo de la celda y su cobertura · {u_t}")
    for e in _ejes_usados(plan):
        pref = _pref_marg(e)
        add(f"{pref}-N-DENTRO", "entero", f"filas de T dentro del eje · {u_t}")
        add(f"{pref}-N-FUERA-EN-T", "entero", f"filas de T fuera del eje · {u_t}")
        for k in _orden(e):
            c = f"{pref}-{_slug(k)}"
            add(f"{c}-N", "entero", f"personas de T en la celda · {u_t}")
            add(f"{c}-NUMERADOR", "entero", f"personas de T en la celda con D9 · {u_t}")
            add(f"{c}-DEN-W", "flotante", f"suma de FAC_PER en la celda · {u_t}")
            add(f"{c}-P", "proporcion", f"p(D9 | celda, T), razon de totales ponderados · {u_t}", True)
            add(f"{c}-IC95INF", "proporcion", f"percentil 2.5 de replicas finitas (plan del arbitro GEN2) · {u_t}", True)
            add(f"{c}-IC95SUP", "proporcion", f"percentil 97.5 de replicas finitas (plan del arbitro GEN2) · {u_t}", True)
            add(f"{c}-B-VALIDAS", "entero", f"replicas finitas · {u_t}")
            if e == EJE_UNIVERSO:
                for d in ("P", "IC95INF", "IC95SUP", "DEN-W"):
                    add(f"{c}-DELTA-{d}", "flotante", f"re-derivado - sellado arbitro GEN2 ({d}) · {u_t}", True)
                add(f"{c}-DELTA-N", "entero", f"re-derivado - sellado arbitro GEN2 (N) · {u_t}")
                add(f"{c}-DELTA-B-VALIDAS", "entero", f"re-derivado - sellado arbitro GEN2 (B-VALIDAS) · {u_t}")
    return cat


# ══ el medidor ═════════════════════════════════════════════════════════════

def _marg(p, d):
    return {"desenlace_id": d, "p": float(p)}


def _sellado(arbitro: dict, rid: str):
    if rid not in arbitro:
        raise Paro(f"id sellado del arbitro ausente: {rid}")
    return arbitro[rid]


def _dif(a, b):
    if a is None or b is None:
        return None
    return float(a) - float(b)


def medir(inputs: dict, contrato: dict) -> dict:
    out: dict[str, object] = {}
    for iid in INPUTS_PERMITIDOS:
        out[f"{P}-G-INPUT-{_slug(iid)}-SHA256"] = str(inputs[iid]["sha256"])
    # ── guardia AST antes de abrir el zip ────────────────────────────────
    viol = auditoria_ast(Path(__file__))
    out[f"{P}-G-GUARDIA-AST-VIOLACIONES"] = len(viol)
    out[f"{P}-G-GUARDIA-AST"] = "PASA" if not viol else "FALLA"
    if viol:
        raise SystemExit("PARO · guardia AST: " + " | ".join(viol[:10]))
    _plan(inputs)                       # guardias del plan, antes del zip
    ola = _carga_ola_enif(inputs)
    return procedimiento(ola, inputs, contrato, out)


def procedimiento(ola: OlaT, inputs: dict, contrato: dict, out: dict) -> dict:
    """Todo lo que `medir()` hace despues de cargar la ola. Separado para que
    el test lo corra sobre una ola FABRICADA y pase su salida por el conducto
    (`corrida0._valida_outputs`) en cada rama terminal (spec §8)."""
    par = contrato["parametros"]
    n_rep = int(par["bootstrap_replicas"])
    bloque = int(par["replicas_bloque"])
    seed = int(contrato["seed"]["valor"])
    tol_p = float(par["control_arbitro_tol_p"])
    tol_ic = float(par["control_arbitro_tol_ic"])
    tol_w = float(par["control_arbitro_tol_den_w"])
    ids_g = par["control_arbitro_ids"]
    umbral_validas = int(par["umbral_replicas_validas"])

    plan = _plan(inputs)
    arbitro = json.loads(_bytes(inputs, "IN-ARBITRO-GEN2").decode("utf-8"))["resultados"]
    out[f"{P}-G-N-FILAS-DICTAMEN-NO-EMITIBLES"] = plan["n_filas_dictamen"]
    out[f"{P}-G-N-PARES"] = len(plan["pares"])
    out[f"{P}-G-N-CELDAS"] = sum(len(plan["ejes"][a]) * len(plan["ejes"][b])
                                 for _p, a, b in plan["pares"])
    out[f"{P}-G-PARES"] = " | ".join(f"{p}=({a},{b})" for p, a, b in plan["pares"])
    usados = _ejes_usados(plan)
    out[f"{P}-G-EJES-USADOS"] = " | ".join(usados)
    out[f"{P}-G-UNIVERSO"] = UNIVERSO_T
    cob_decl = plan["cobertura_declarada"]
    out[f"{P}-G-COBERTURA-DECLARADA"] = cob_decl

    # ── la ola, una vez; las replicas, una vez ───────────────────────────
    rep = replicas_t(ola, seed, n_rep, bloque)
    m = ola.meta
    out[f"{P}-G-FILAS-UNIVERSO"] = m["filas_universo"]
    out[f"{P}-G-FILAS-T"] = m["filas_t"]
    out[f"{P}-G-FUERA-T"] = m["fuera_t"]
    out[f"{P}-G-COBERTURA-T-FILAS"] = m["cobertura_t_filas"]
    out[f"{P}-G-COBERTURA-T-PONDERADA"] = m["cobertura_t_ponderada"]
    out[f"{P}-G-ESTRATOS"] = m["estratos"]
    out[f"{P}-G-UPM"] = m["upm"]
    out[f"{P}-G-UPM-CON-T"] = m["upm_con_t"]
    out[f"{P}-G-ESTRATOS-UPM-UNICA"] = rep.estratos_upm_unica
    out[f"{P}-G-POBLACION-EXPANDIDA"] = m["poblacion_expandida"]
    out[f"{P}-G-POBLACION-T"] = m["poblacion_t"]
    out[f"{P}-G-REPLICAS"] = n_rep
    out[f"{P}-G-REPLICAS-BLOQUE"] = bloque
    out[f"{P}-G-SEED"] = seed
    universo_celda = (f"{UNIVERSO_T} · cobertura declarada {cob_decl} (arbitro) · "
                      f"cobertura medida {m['cobertura_t_filas']:.6f} de filas, "
                      f"{m['cobertura_t_ponderada']:.6f} ponderada · n_T = {m['filas_t']}")

    # ── marginales de UN eje dentro de T; oro sobre formalidad ───────────
    marg: dict[str, dict] = {}
    peor_p, peor_ic, peor_w, reproduce = 0.0, 0.0, 0.0, True
    for e in usados:
        r_ = marginal_t(ola, e, desenlace=DESENLACE, replicas=rep)
        marg[e] = r_
        pref = _pref_marg(e)
        out[f"{pref}-N-DENTRO"] = r_["n_dentro"]
        out[f"{pref}-N-FUERA-EN-T"] = r_["n_t"] - r_["n_dentro"]
        for k in _orden(e):
            c = r_["celdas"][k]
            cid = f"{pref}-{_slug(k)}"
            out[f"{cid}-N"] = c["n"]
            out[f"{cid}-NUMERADOR"] = c["numerador"]
            out[f"{cid}-DEN-W"] = c["den_w"]
            out[f"{cid}-P"] = c["p"]
            out[f"{cid}-IC95INF"] = c["ic95"][0] if c["ic95"] else None
            out[f"{cid}-IC95SUP"] = c["ic95"][1] if c["ic95"] else None
            out[f"{cid}-B-VALIDAS"] = c["b_validas"]
            if e == EJE_UNIVERSO:
                sid = str(plan["formalidad_ids_p"][k])
                base_s = sid[:-len("-P")]
                s_p = _sellado(arbitro, sid)
                s_lo = _sellado(arbitro, f"{base_s}-IC-LO")
                s_hi = _sellado(arbitro, f"{base_s}-IC-HI")
                s_n = _sellado(arbitro, f"{base_s}-N")
                s_w = _sellado(arbitro, f"{base_s}-DEN-W")
                s_b = _sellado(arbitro, f"{base_s}-B-VALIDAS")
                dp = _dif(c["p"], s_p)
                dlo = _dif(out[f"{cid}-IC95INF"], s_lo)
                dhi = _dif(out[f"{cid}-IC95SUP"], s_hi)
                dw = _dif(c["den_w"], s_w)
                out[f"{cid}-DELTA-P"] = dp
                out[f"{cid}-DELTA-IC95INF"] = dlo
                out[f"{cid}-DELTA-IC95SUP"] = dhi
                out[f"{cid}-DELTA-DEN-W"] = dw
                out[f"{cid}-DELTA-N"] = int(c["n"]) - int(s_n)
                out[f"{cid}-DELTA-B-VALIDAS"] = int(c["b_validas"]) - int(s_b)
                for v, tol, nombre in ((dp, tol_p, "p"), (dlo, tol_ic, "ic"),
                                       (dhi, tol_ic, "ic"), (dw, tol_w, "w")):
                    if v is None:
                        reproduce = False
                        continue
                    if abs(v) > tol:
                        reproduce = False
                    if nombre == "p":
                        peor_p = max(peor_p, abs(v))
                    elif nombre == "ic":
                        peor_ic = max(peor_ic, abs(v))
                    else:
                        peor_w = max(peor_w, abs(v))
                if out[f"{cid}-DELTA-N"] != 0:
                    reproduce = False
                if out[f"{cid}-DELTA-B-VALIDAS"] != 0:
                    reproduce = False
    d_filas = m["filas_universo"] - int(_sellado(arbitro, ids_g["filas_universo"]))
    d_fuera = m["fuera_t"] - int(_sellado(arbitro, ids_g["fuera_t"]))
    out[f"{P}-G-CONTROL-ARBITRO-DELTA-FILAS"] = d_filas
    out[f"{P}-G-CONTROL-ARBITRO-DELTA-FUERA-T"] = d_fuera
    if d_filas != 0:
        reproduce = False
    if d_fuera != 0:
        reproduce = False
    out[f"{P}-G-CONTROL-ARBITRO-DELTA-P-MAX"] = peor_p
    out[f"{P}-G-CONTROL-ARBITRO-DELTA-IC-MAX"] = peor_ic
    out[f"{P}-G-CONTROL-ARBITRO-DELTA-DEN-W-MAX"] = peor_w
    out[f"{P}-G-CONTROL-ARBITRO-VEREDICTO"] = "REPRODUCE" if reproduce else "NO-REPRODUCE"
    publica = reproduce
    if not publica:
        for e in usados:
            for k in _orden(e):
                cid = f"{_pref_marg(e)}-{_slug(k)}"
                out[f"{cid}-IC95INF"] = None
                out[f"{cid}-IC95SUP"] = None

    # ── cuenta_formal x formalidad: regla de degeneracion fijada antes ───
    causas = []
    for par_, a, b in plan["pares"]:
        if sorted((a, b)) != sorted(("cuenta_formal", EJE_UNIVERSO)):
            continue
        for e in (a, b, "nacional"):
            for k in _orden(e):
                c = marg[e]["celdas"][k]
                if c["n"] == 0:
                    causas.append(f"{e}={k}:SIN-FILAS-EN-T")
                elif c["p"] is None:
                    causas.append(f"{e}={k}:SIN-MASA")
                elif abs(c["p"] - 0.5) >= 0.5:
                    causas.append(f"{e}={k}:MARGINAL-EN-0-O-1")
    out[f"{P}-G-CUENTA-FORMALXFORMALIDAD-DEGENERACION"] = (
        "DEGENERADO:" + "+".join(causas) if causas else "NO-DEGENERADO")

    # ── C2R por celda: punto (formalidad citada) + IC replica por replica ─
    con_ic, sin_ic, sin_punto, sin_definir, delta_vec = 0, 0, 0, 0, 0.0
    mn = marg["nacional"]["celdas"][NAC_T]
    for par_, a, b in plan["pares"]:
        for ca in plan["ejes"][a]:
            for cb in plan["ejes"][b]:
                base = _base_celda(par_, ca, cb)
                ma = marg[a]["celdas"][ca]
                mb = marg[b]["celdas"][cb]
                pa = ma["p"]
                pb = mb["p"]
                if a == EJE_UNIVERSO:
                    pa = float(_sellado(arbitro, str(plan["formalidad_ids_p"][ca])))
                if b == EJE_UNIVERSO:
                    pb = float(_sellado(arbitro, str(plan["formalidad_ids_p"][cb])))
                causa_punto = None
                punto = None
                if pa is None or pb is None or mn["p"] is None:
                    causa_punto = "MARGINAL-SIN-DEFINIR"
                else:
                    try:
                        punto = float(piso_log_aditivo(_marg(pa, DESENLACE), _marg(pb, DESENLACE),
                                                       _marg(mn["p"], DESENLACE))["p"])
                    except MarginalDegenerado:
                        causa_punto = "MARGINAL-DEGENERADO"
                out[f"{base}-P"] = punto
                out[f"{base}-UNIVERSO"] = universo_celda
                ra, rb, rn = ma["replicas"], mb["replicas"], mn["replicas"]
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
                    ref = piso_log_aditivo(_marg(ra[k0], DESENLACE), _marg(rb[k0], DESENLACE),
                                           _marg(rn[k0], DESENLACE))["p"]
                    delta_vec = max(delta_vec, abs(float(c2r[0]) - float(ref)))
                sin_definir += n_rep - n_ok
                out[f"{base}-REPLICAS-VALIDAS"] = n_ok
                lo = hi = None
                if punto is None:
                    estado = f"IC-NO-CONSTRUIBLE:PUNTO-SIN-DEFINIR:{causa_punto}"
                    sin_punto += 1
                elif not publica:
                    estado = "IC-NO-PUBLICADO:CONTROL-ARBITRO-NO-REPRODUCE"
                elif n_ok < umbral_validas:
                    estado = f"IC-NO-CONSTRUIBLE:REPLICAS-VALIDAS-{n_ok}<{umbral_validas}"
                else:
                    estado = IC_ROTULO
                    lo, hi = np.percentile(c2r, [2.5, 97.5])
                    lo, hi = float(lo), float(hi)
                out[f"{base}-IC95INF"] = lo
                out[f"{base}-IC95SUP"] = hi
                out[f"{base}-IC-ESTADO"] = estado
                if lo is None:
                    sin_ic += 1
                else:
                    con_ic += 1
    out[f"{P}-G-IC-PUBLICADO"] = "SI" if publica else "NO"
    out[f"{P}-G-N-CELDAS-CON-IC"] = con_ic
    out[f"{P}-G-N-CELDAS-SIN-IC"] = sin_ic
    out[f"{P}-G-N-CELDAS-SIN-PUNTO"] = sin_punto
    out[f"{P}-G-REPLICAS-SIN-DEFINIR-TOTAL"] = int(sin_definir)
    out[f"{P}-G-C2-VECTORIZADO-VS-REFERENCIA-DELTA-MAX"] = delta_vec
    out[f"{P}-G-TIPO-INCERTIDUMBRE"] = IC_ROTULO if publica else "NO-PUBLICADA"
    out[f"{P}-G-ROTULO-SUPUESTO"] = ROTULO_SUPUESTO
    out[f"{P}-G-COMPARACION-POBLACIONAL"] = "NINGUNA (A-bis 4): universo T no reconciliable con el poblacional"
    out[f"{P}-G-ESTADO-EMISION"] = "EMITIDA-SIN-EVALUAR"
    out[f"{P}-G-ADOPTA"] = "NO"
    out[f"{P}-G-CRUCE-DERIVADO"] = "NO"
    out[f"{P}-G-UNIDAD-DATO"] = "PERSONA elegida 18+ de T (quien trabaja)"
    out[f"{P}-G-PONDERADOR"] = "FAC_PER"
    out[f"{P}-G-DESENLACE"] = DESENLACE
    return out
