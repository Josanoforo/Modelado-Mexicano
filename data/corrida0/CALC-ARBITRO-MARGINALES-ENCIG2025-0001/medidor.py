#!/usr/bin/env python3
"""El primer resultado que produzca este procedimiento es el que se reporta.

CALC-ARBITRO-MARGINALES-ENCIG2025-0001 · ACTO GEN2-ARBITRO-MARGINALES-1 (P-ENCIG).

QUÉ ESTIMA (spec §1, primera línea): la realidad de la ola nueva -- los
MARGINALES POR EJE de ENCIG 2025 para el desenlace del árbitro `digital`
(pago ordinario del servicio de luz, N_TRA=01, hecho por canal digital:
P7_3 en 04/05; no adopción 01/02/06; universo P7_3 en 01/02/04/05/06) por
sexo, edad y escolaridad. Unidad = TRÁMITE (quien pagó doce veces
contribuye doce veces), escala = proporción ponderada (FAC_TRA) en [0, 1],
IC95 por bootstrap de UPM estratificado con réplicas compartidas. Es el
mismo procedimiento del piso sellado (`CALC-PISOS-ENCIG2023-EJES-0002`)
apuntado a la ola nueva: el remuestreo, la rejilla y la conducta se
IMPORTAN del medidor sellado del piso (input `MEDIDOR-PISO-EJES-0002`, por
sha256); aquí sólo vive el mapa de nemónicos por ola y la guardia.

OLA COMO PARÁMETRO (D-22 ampliada): `contrato["parametros"]["ola"]` decide el
mapa. Con `ola=2023` sobre `encig23_base_datos_csv` el MISMO punto de
entrada reproduce el piso sellado (prueba de oro,
`tests/test_arbitro_marginales_encig2025.py`). Con `ola=2025` mide la
realidad. Nunca las dos en una corrida.

MAPA DE NEMÓNICOS 2023 -> 2025 (A.15): sólo cambia el nombre de los
miembros (`encig2023_04_sec_7.csv` -> `encig2025_04_sec_7.csv`;
`encig2023_02_residentes_sec_2.csv` -> `encig2025_02_residentes_sec_2.csv`).
Las variables (N_TRA, P7_3, FAC_TRA, EST_DIS, UPM_DIS, ID_PER, SEXO, EDAD,
NIV) y sus catálogos son los que el árbitro GEN1 y el piloto 3
(`CALC-GOB-DIGITAL-EXE-EMISIONES-0002`) ya usaron sobre 2025. Edad 97/98/99
en 2025 (FP-399: 97 es edad real censurada): el piso corta en 18-96, así que
esos trámites quedan FUERA del eje edad y se CUENTAN (RESULT `G-EDAD-97-N`,
`G-EDAD-98-99-N`); no se reinterpretan aquí.

GUARDIA DE UNA SOLA VARIABLE DE AGRUPACIÓN (firma 3D, 21/sep/2026 -- misma
semántica que el guardián de `tools/celda_d/marginales_reproduccion.py`):
  · `marginal(m, prefijo, y, eje, grupos, categorias)` recibe UN `str` de eje
    de la lista blanca `EJES`; una lista, dos ejes o un eje fuera de lista es
    `ValueError`. No existe función de cruce.
  · `auditoria_ast()` recorre el AST de ESTE archivo al arrancar `medir()`,
    antes de abrir el zip: importa sólo la lista blanca; ningún
    `groupby`/`crosstab`/`pivot`; el único `merge` es la unión trámite<-persona
    por `ID_PER` con `validate="m:1"` (no agrupa: adjunta atributos); toda
    llamada a `marginal(` lleva un eje literal de `EJES`; `_cells` del piso
    sólo se llama dentro de `marginal`; ningún constructor de eje (`_eje_*`)
    combina dos comparaciones; ninguna constante nombra otro instrumento ni
    un archivo fuera de la lista. Probada por mutación en el test.
  · RESERVA: con `ola != 2025` ningún input cuyo id nombre 2025 entra.
Este archivo no ve, no deriva y no imprime ningún cruce. No adopta nada.
"""
from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

OLA_OBJETIVO = "2025"
EJES = ("total", "sexo", "edad", "escolaridad")
EDADES = ("18-29", "30-44", "45-59", "60+")
ESCOLARIDAD = ("hasta_primaria", "secundaria", "media_superior", "superior")
TOTAL = ("todos",)

VARIABLES = {
    "2023": {
        "payload_id": "encig23_base_datos_csv",
        "eventos": "encig2023_04_sec_7.csv",
        "personas": "encig2023_02_residentes_sec_2.csv",
    },
    "2025": {
        "payload_id": "encig25_base_datos_csv",
        "eventos": "encig2025_04_sec_7.csv",
        "personas": "encig2025_02_residentes_sec_2.csv",
    },
}
COLS_EVENTOS = ["N_TRA", "P7_3", "FAC_TRA", "EST_DIS", "UPM_DIS", "ID_PER"]
COLS_PERSONAS = ["ID_PER", "SEXO", "EDAD", "NIV"]
INPUT_MEDIDOR_PISO = "MEDIDOR-PISO-EJES-0002"


class ParoDeGuardia(RuntimeError):
    """Una guardia no está satisfecha. El módulo no mide."""


# ══════════════════════════ auditoría del AST (E.6 como código) ═══════════

_AUDIT_IMPORTS = ("__future__", "ast", "importlib.util", "sys", "pathlib", "numpy", "pandas")
_AUDIT_PROHIBIDOS = ("groupby", "crosstab", "pivot", "pivot_table", "unstack", "stack",
                     "concat", "cruce", "eval", "exec", "compile",
                     "__import__", "getattr", "globals", "locals", "query", "agg",
                     "aggregate", "transform", "iterrows", "itertuples", "MultiIndex")
_AUDIT_OTROS_INSTRUMENTOS = ("envipe", "enif", "enut", "enigh", "enoe", "ensanut", "endutih",
                             "encuci", "endireh", "enasem", "mociba", "ensafi", "eder2017", "eder_", "lapop",
                             "ennvih", "mxfls", "enadid", "encup")
_AUDIT_EXT = (".zip", ".csv", ".xlsx", ".xls", ".dbf", ".sav", ".dta", ".pdf")
_AUDIT_ARCHIVOS = ("encig2023_04_sec_7.csv", "encig2023_02_residentes_sec_2.csv",
                   "encig2025_04_sec_7.csv", "encig2025_02_residentes_sec_2.csv")
_AUDIT_COMPARADORES = (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.In, ast.NotIn)


def _nombre_llamado(call: ast.Call) -> str:
    f = call.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return ""


def _tiene_comparacion(nodo: ast.AST) -> bool:
    for sub in ast.walk(nodo):
        if isinstance(sub, ast.Compare) and any(isinstance(o, _AUDIT_COMPARADORES) for o in sub.ops):
            return True
        if isinstance(sub, ast.Call) and _nombre_llamado(sub) in ("isin", "eq", "ne", "map"):
            return True
    return False


def auditoria_ast_fuente(fuente: str) -> list[str]:
    """Lista de violaciones (vacía = PASA). Una regla por línea; cada una con
    control positivo (mutación) en el test."""
    arbol = ast.parse(fuente)
    viol: list[str] = []
    exentos: set[int] = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            cuerpo = nodo.body
            if cuerpo and isinstance(cuerpo[0], ast.Expr) and isinstance(cuerpo[0].value, ast.Constant):
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
            nombre = hijo.name if isinstance(hijo, (ast.FunctionDef, ast.AsyncFunctionDef)) else fn
            padre_fn[id(hijo)] = nombre
            _marca(hijo, nombre)
    _marca(arbol, "<modulo>")

    for nodo in ast.walk(arbol):
        fn = padre_fn.get(id(nodo), "<modulo>")
        # R1 · imports: sólo la lista blanca
        if isinstance(nodo, ast.Import):
            for a in nodo.names:
                if a.name not in _AUDIT_IMPORTS:
                    viol.append(f"R1 import prohibido: {a.name}")
        elif isinstance(nodo, ast.ImportFrom) and (nodo.module or "") not in _AUDIT_IMPORTS:
            viol.append(f"R1 import prohibido: from {nodo.module}")
        # R2 · ninguna agrupación/cruce por nombre
        if isinstance(nodo, ast.Attribute) and nodo.attr in _AUDIT_PROHIBIDOS:
            viol.append(f"R2 atributo prohibido `.{nodo.attr}` en {fn}")
        if isinstance(nodo, ast.Name) and nodo.id in _AUDIT_PROHIBIDOS:
            viol.append(f"R2 nombre prohibido `{nodo.id}` en {fn}")
        if isinstance(nodo, ast.Call):
            nom = _nombre_llamado(nodo)
            if nom in _AUDIT_PROHIBIDOS:
                viol.append(f"R2 llamada prohibida `{nom}()` en {fn}")
            # R2b · el único merge: trámite<-persona por ID_PER, m:1, en `_carga`
            if nom == "merge":
                kws = {k.arg: k.value for k in nodo.keywords}
                ok = (fn == "_carga" and isinstance(kws.get("on"), ast.Constant) and kws["on"].value == "ID_PER"
                      and isinstance(kws.get("validate"), ast.Constant) and kws["validate"].value == "m:1")
                if not ok:
                    viol.append(f"R2b merge fuera de contrato (ID_PER, m:1, en _carga) en {fn}")
            # R3 · `marginal(` lleva UN eje literal de EJES; `_cells` sólo dentro de `marginal`
            if nom == "marginal":
                if len(nodo.args) != 6 or nodo.keywords:
                    viol.append(f"R3 marginal() con {len(nodo.args)} posicionales/keywords en {fn}")
                else:
                    eje = nodo.args[3]
                    if not (isinstance(eje, ast.Constant) and isinstance(eje.value, str) and eje.value in EJES):
                        viol.append(f"R3 marginal() con eje no literal o fuera de EJES en {fn}")
            if nom == "_cells" and fn != "marginal":
                viol.append(f"R3 `_cells` del piso llamado fuera de marginal: {fn}")
        # R4 · ninguna función de cruce
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)) and "cruce" in nodo.name.lower():
            viol.append(f"R4 función de cruce definida: {nodo.name}")
        # R5 · un constructor de eje (`_eje_*`) no combina dos comparaciones
        if fn.startswith("_eje_"):
            if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, (ast.BitAnd, ast.BitOr, ast.BitXor, ast.Mult)):
                if _tiene_comparacion(nodo.left) and _tiene_comparacion(nodo.right):
                    viol.append(f"R5 dos comparaciones combinadas en {fn} (línea {nodo.lineno})")
            if isinstance(nodo, ast.BoolOp) and sum(_tiene_comparacion(v) for v in nodo.values) >= 2:
                viol.append(f"R5 dos comparaciones combinadas por and/or en {fn} (línea {nodo.lineno})")
        # R6 · constantes: ningún otro instrumento ni archivo fuera de la lista
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str) and id(nodo) not in exentos:
            s, bajo = nodo.value, nodo.value.lower()
            if any(bajo.endswith(e) for e in _AUDIT_EXT) and s not in _AUDIT_ARCHIVOS:
                viol.append(f"R6 archivo no autorizado en constante {s!r} ({fn})")
            if any(tok in bajo for tok in _AUDIT_OTROS_INSTRUMENTOS):
                viol.append(f"R6 otro instrumento en constante {s!r} ({fn})")
    return viol


def auditoria_ast(ruta: Path | None = None) -> list[str]:
    return auditoria_ast_fuente(Path(ruta or __file__).read_text(encoding="utf-8"))


# ══════════════════════════════ guardias en tiempo de corrida ═════════════

def _guardia(inputs: dict, contrato: dict) -> dict:
    viol = auditoria_ast()
    if viol:
        raise ParoDeGuardia("auditoría AST: " + " | ".join(viol))
    ola = str(contrato["parametros"]["ola"])
    if ola not in VARIABLES:
        raise ParoDeGuardia(f"ola {ola!r} sin mapa de variables (hay {sorted(VARIABLES)})")
    v = VARIABLES[ola]
    if v["payload_id"] not in inputs:
        raise ParoDeGuardia(f"payload `{v['payload_id']}` de la ola {ola} ausente de inputs")
    if ola != OLA_OBJETIVO:
        for iid in inputs:
            low = str(iid).lower()
            if OLA_OBJETIVO in low or "encig25" in low:
                raise ParoDeGuardia(f"RESERVA: insumo `{iid}` de {OLA_OBJETIVO} con ola={ola}")
    if INPUT_MEDIDOR_PISO not in inputs:
        raise ParoDeGuardia(f"falta el input `{INPUT_MEDIDOR_PISO}` (medidor sellado del piso)")
    return v


def _piso(inputs: dict):
    """Importa POR RUTA el medidor sellado del piso (bytes verificados por sha256
    en el runner): `_csv`, `_code`, `_age`, `_school`, `_slug`, `_cells`,
    `_estimate` -- el remuestreo y la rejilla son literalmente los del piso."""
    ruta = Path(inputs[INPUT_MEDIDOR_PISO]["ruta_absoluta"])
    spec = importlib.util.spec_from_file_location("medidor_piso_encig2023_ejes_0002", ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _carga(m, inputs: dict, v: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    z = inputs[v["payload_id"]]["ruta_absoluta"]
    events = m._csv(z, v["eventos"], COLS_EVENTOS)
    people = m._csv(z, v["personas"], COLS_PERSONAS)
    joined = events.merge(people, on="ID_PER", how="left", validate="m:1", indicator=True)
    return events, joined


# ══════════════════════════════ ejes (una variable cada uno) ══════════════

def _eje_sexo(m, d):
    return m._code(d["SEXO"])


def _eje_edad(m, d):
    return m._age(d["EDAD"])


def _eje_escolaridad(m, d):
    return m._school(d["NIV"])


def _eje_total(m, d):
    return pd.Series(TOTAL[0], index=d.index, dtype="object")


def marginal(m, prefijo: str, y, eje, grupos, categorias):
    """UNA variable de agrupación por llamada. `eje` es un `str` de `EJES`."""
    if not isinstance(eje, str) or eje not in EJES:
        raise ValueError(f"eje no admitido o no atómico: {eje!r}")
    if not isinstance(grupos, pd.Series):
        raise ValueError("grupos debe ser UNA Series (una variable)")
    return m._cells(prefijo, y, {eje: (grupos, tuple(categorias))})


# ══════════════════════════════ medición ══════════════════════════════════

def medir(inputs: dict, contrato: dict) -> dict:
    v = _guardia(inputs, contrato)
    ola = str(contrato["parametros"]["ola"])
    m = _piso(inputs)
    pref = f"ARBITRO-ENCIG{ola}"
    reps = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])

    events, joined = _carga(m, inputs, v)
    # Universo: literalmente el del piso (spec v2.0 ENCIG 2023).
    ntra = m._code(joined["N_TRA"]); p73 = m._code(joined["P7_3"])
    universe = ntra.eq("1") & p73.isin(["1", "2", "4", "5", "6"])
    d = joined.loc[universe].copy()
    d["_w"] = pd.to_numeric(d["FAC_TRA"], errors="coerce")
    d["_est"] = d["EST_DIS"].str.strip(); d["_upm"] = d["UPM_DIS"].str.strip()
    y = m._code(d["P7_3"]).isin(["4", "5"]).astype(float)

    ejes = {
        "total": (_eje_total(m, d), TOTAL),
        "sexo": (_eje_sexo(m, d), ("1", "2")),
        "edad": (_eje_edad(m, d), EDADES),
        "escolaridad": (_eje_escolaridad(m, d), ESCOLARIDAD),
    }
    p = f"{pref}-DIGITAL"
    cells = []
    cells += marginal(m, p, y, "total", ejes["total"][0], ejes["total"][1])
    cells += marginal(m, p, y, "sexo", ejes["sexo"][0], ejes["sexo"][1])
    cells += marginal(m, p, y, "edad", ejes["edad"][0], ejes["edad"][1])
    cells += marginal(m, p, y, "escolaridad", ejes["escolaridad"][0], ejes["escolaridad"][1])
    out = m._estimate(d, cells, reps, seed)

    # Diagnóstico (enteros; nunca nulos).
    design = d["_w"].notna() & (d["_w"] > 0) & d["_est"].ne("") & d["_upm"].ne("")
    edad = pd.to_numeric(d["EDAD"], errors="coerce")
    out[f"RESULT-{pref}-G-FILAS-EVENTOS"] = int(len(events))
    out[f"RESULT-{pref}-G-JOIN-SIN-DEMOGRAFIA"] = int(joined["_merge"].ne("both").sum())
    out[f"RESULT-{pref}-G-FILAS-DISENO-VALIDO"] = int(design.sum())
    out[f"RESULT-{pref}-G-REPLICAS"] = int(reps)
    out[f"RESULT-{pref}-G-OLA"] = str(ola)
    out[f"RESULT-{pref}-DIGITAL-G-N-UNIVERSO"] = int(universe.sum())
    out[f"RESULT-{pref}-DIGITAL-G-P7-3-EXCLUIDAS"] = int((ntra.eq("1") & ~p73.isin(["1", "2", "4", "5", "6"])).sum())
    out[f"RESULT-{pref}-G-EDAD-97-N"] = int(edad.eq(97).sum())
    out[f"RESULT-{pref}-G-EDAD-98-99-N"] = int(edad.isin([98, 99]).sum())
    for eje in EJES:
        out[f"RESULT-{pref}-G-EJE-{m._slug(eje)}-FUERA"] = int(ejes[eje][0].isna().sum())
    return out


# ══════════════════════════════ esquema de resultados ═════════════════════

def esquema_resultados(ola: str = OLA_OBJETIVO) -> list[dict]:
    pref = f"ARBITRO-ENCIG{ola}"
    cats = {"total": TOTAL, "sexo": ("1", "2"), "edad": EDADES, "escolaridad": ESCOLARIDAD}

    def slug(x):
        return (str(x).upper().replace("Á", "A").replace("É", "E").replace("Í", "I")
                .replace("Ó", "O").replace("Ú", "U").replace("+", "-MAS")
                .replace("_", "-").replace(" ", "-"))
    rows = []
    for eje in EJES:
        for cat in cats[eje]:
            b = f"RESULT-{pref}-DIGITAL-{slug(eje)}-{slug(cat)}"
            rows.append({"id": f"{b}-P", "tipo": "proporcion", "unidad": "proporción ponderada [0,1]",
                         "permite_no_estimable": True})
            rows.append({"id": f"{b}-IC-LO", "tipo": "proporcion", "unidad": "límite inferior IC95",
                         "permite_no_estimable": True})
            rows.append({"id": f"{b}-IC-HI", "tipo": "proporcion", "unidad": "límite superior IC95",
                         "permite_no_estimable": True})
            rows.append({"id": f"{b}-N", "tipo": "entero", "unidad": "n sin ponderar (trámites)"})
            rows.append({"id": f"{b}-DEN-W", "tipo": "flotante", "unidad": "denominador ponderado"})
            rows.append({"id": f"{b}-B-VALIDAS", "tipo": "entero", "unidad": "réplicas bootstrap definidas"})
    rows.append({"id": f"RESULT-{pref}-G-FILAS-EVENTOS", "tipo": "entero", "unidad": "filas de sec_7 (trámites)"})
    rows.append({"id": f"RESULT-{pref}-G-JOIN-SIN-DEMOGRAFIA", "tipo": "entero", "unidad": "trámites sin persona en residentes"})
    rows.append({"id": f"RESULT-{pref}-G-FILAS-DISENO-VALIDO", "tipo": "entero", "unidad": "trámites del universo con ponderador > 0 y diseño"})
    rows.append({"id": f"RESULT-{pref}-G-REPLICAS", "tipo": "entero", "unidad": "réplicas bootstrap"})
    rows.append({"id": f"RESULT-{pref}-G-OLA", "tipo": "texto", "unidad": "ola medida"})
    rows.append({"id": f"RESULT-{pref}-DIGITAL-G-N-UNIVERSO", "tipo": "entero", "unidad": "trámites N_TRA=01 con P7_3 en 01/02/04/05/06"})
    rows.append({"id": f"RESULT-{pref}-DIGITAL-G-P7-3-EXCLUIDAS", "tipo": "entero", "unidad": "trámites N_TRA=01 con P7_3 fuera del universo"})
    rows.append({"id": f"RESULT-{pref}-G-EDAD-97-N", "tipo": "entero", "unidad": "trámites del universo con EDAD=97 (FP-399, fuera del eje edad)"})
    rows.append({"id": f"RESULT-{pref}-G-EDAD-98-99-N", "tipo": "entero", "unidad": "trámites del universo con EDAD en 98/99 (fuera del eje edad)"})
    for eje in EJES:
        rows.append({"id": f"RESULT-{pref}-G-EJE-{slug(eje)}-FUERA", "tipo": "entero", "unidad": "trámites del universo fuera del eje (código inválido o blanco)"})
    return rows
