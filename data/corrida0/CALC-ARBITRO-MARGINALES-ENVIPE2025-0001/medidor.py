#!/usr/bin/env python3
"""El primer resultado que produzca este procedimiento es el que se reporta.

CALC-ARBITRO-MARGINALES-ENVIPE2025-0001 · ACTO GEN2-ARBITRO-MARGINALES-1 (P-ENVIPE).

QUÉ ESTIMA (spec §1, primera línea): la realidad de la ola nueva -- los
MARGINALES POR EJE de ENVIPE 2025 para los dos desenlaces del árbitro:
`evasion` (evasión de norma: BP1_20=2 y BP1_23 en 04/05/06/08, universo
BP1_20 en 1/2) por sexo, edad, escolaridad (proxy) y dominio; y `denuncia`
(BP1_20=1, universo BPCOD=01 y BP2_1 en 1/2) por cobertura de seguro. Unidad
= DELITO, escala = proporción ponderada (FAC_DEL) en [0, 1], IC95 por
bootstrap de UPM estratificado con réplicas compartidas. Es el mismo
procedimiento del piso sellado (`CALC-PISOS-ENVIPE2024-EJES-0002`) apuntado
a la ola nueva: el remuestreo, la rejilla y las conductas se IMPORTAN del
medidor sellado del piso (input `MEDIDOR-PISO-EJES-0002`, por sha256); aquí
sólo vive el mapa de nemónicos por ola y la guardia.

OLA COMO PARÁMETRO (D-22 ampliada): `contrato["parametros"]["ola"]` decide el
mapa. Con `ola=2024` sobre `envipe2024_csv` el MISMO punto de entrada
reproduce el piso sellado (prueba de oro,
`tests/test_arbitro_marginales_envipe2025.py`). Con `ola=2025` mide la
realidad. Nunca las dos en una corrida.

MAPA DE NEMÓNICOS 2024 -> 2025 (A.15): sólo cambia el nombre de los
miembros (`…_envipe2024.csv` -> `…_envipe2025.csv`). Las variables (BP1_20,
BP1_23, BP2_1, BPCOD, FAC_DEL, EST_DIS, UPM_DIS, ID_PER, SEXO, EDAD,
DOMINIO, NIV) y sus catálogos son los mismos que el árbitro GEN1 ya usó
sobre 2025 (`milpa/tramite-ola5-propuesta-v0.yaml`, entradas
`tramite.evasion_norma_ejes_envipe2025` y `civico.denuncia.con_seguro_ejes_envipe2025`).

GUARDIA DE UNA SOLA VARIABLE DE AGRUPACIÓN (firma 3D, 21/sep/2026 -- misma
semántica que el guardián de `tools/celda_d/marginales_reproduccion.py`):
  · `marginal(m, prefijo, y, eje, grupos, categorias)` recibe UN `str` de eje
    de la lista blanca `EJES`; una lista, dos ejes o un eje fuera de lista es
    `ValueError`. No existe función de cruce.
  · `auditoria_ast()` recorre el AST de ESTE archivo al arrancar `medir()`,
    antes de abrir el zip: importa sólo la lista blanca; ningún
    `groupby`/`crosstab`/`pivot`; el único `merge` es la unión delito<-persona
    por `ID_PER` con `validate="m:1"` (no agrupa: adjunta atributos); toda
    llamada a `marginal(` lleva un eje literal de `EJES`; `_cells` del piso
    sólo se llama dentro de `marginal`; ningún constructor de eje (`_eje_*`)
    combina dos comparaciones; ninguna constante nombra otro instrumento ni
    un archivo fuera de la lista. Probada por mutación en el test.
  · RESERVA: con `ola != 2025` ningún input cuyo id nombre 2025 entra;
    `envipe2026*` no figura en ninguna constante ni input.
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
EJES = ("total", "sexo", "edad", "escolaridad", "dominio", "cobertura_seguro")
EDADES = ("18-29", "30-44", "45-59", "60+")
ESCOLARIDAD = ("hasta_primaria", "secundaria", "media_superior", "superior")
DOMINIO = ("Rural", "Complemento urbano", "Urbano")
COBERTURA = ("no_asegurado", "asegurado")
TOTAL = ("todos",)
EJES_EVASION = ("total", "sexo", "edad", "escolaridad", "dominio")
EJES_DENUNCIA = ("total", "cobertura_seguro")

VARIABLES = {
    "2024": {
        "payload_id": "envipe2024_csv",
        "vic": "conjunto_de_datos_tmod_vic_envipe2024.csv",
        "dem": "conjunto_de_datos_tsdem_envipe2024.csv",
    },
    "2025": {
        "payload_id": "envipe2025_csv",
        "vic": "conjunto_de_datos_tmod_vic_envipe2025.csv",
        "dem": "conjunto_de_datos_tsdem_envipe2025.csv",
    },
}
COLS_VIC = ["BP1_20", "BP1_23", "BP2_1", "BPCOD", "FAC_DEL", "EST_DIS", "UPM_DIS",
            "ID_PER", "SEXO", "EDAD", "DOMINIO"]
COLS_DEM = ["ID_PER", "NIV"]
INPUT_MEDIDOR_PISO = "MEDIDOR-PISO-EJES-0002"


class ParoDeGuardia(RuntimeError):
    """Una guardia no está satisfecha. El módulo no mide."""


# ══════════════════════════ auditoría del AST (E.6 como código) ═══════════

_AUDIT_IMPORTS = ("__future__", "ast", "importlib.util", "sys", "pathlib", "numpy", "pandas")
_AUDIT_PROHIBIDOS = ("groupby", "crosstab", "pivot", "pivot_table", "unstack", "stack",
                     "concat", "cruce", "eval", "exec", "compile",
                     "__import__", "getattr", "globals", "locals", "query", "agg",
                     "aggregate", "transform", "iterrows", "itertuples", "MultiIndex")
_AUDIT_OTROS_INSTRUMENTOS = ("encig", "enif", "enut", "enigh", "enoe", "ensanut", "endutih",
                             "encuci", "endireh", "enasem", "mociba", "ensafi", "eder2017", "eder_", "lapop",
                             "ennvih", "mxfls", "enadid", "encup", "envipe2026", "envipe_2026")
_AUDIT_EXT = (".zip", ".csv", ".xlsx", ".xls", ".dbf", ".sav", ".dta", ".pdf")
_AUDIT_ARCHIVOS = ("conjunto_de_datos_tmod_vic_envipe2024.csv", "conjunto_de_datos_tsdem_envipe2024.csv",
                   "conjunto_de_datos_tmod_vic_envipe2025.csv", "conjunto_de_datos_tsdem_envipe2025.csv")
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
            # R2b · el único merge: delito<-persona por ID_PER, m:1, en `_carga`
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
            if OLA_OBJETIVO in str(iid):
                raise ParoDeGuardia(f"RESERVA: insumo `{iid}` de {OLA_OBJETIVO} con ola={ola}")
    for iid in inputs:
        if "2026" in str(iid):
            raise ParoDeGuardia(f"RESERVA: insumo `{iid}` de 2026 (ola entera reservada)")
    if INPUT_MEDIDOR_PISO not in inputs:
        raise ParoDeGuardia(f"falta el input `{INPUT_MEDIDOR_PISO}` (medidor sellado del piso)")
    return v


def _piso(inputs: dict):
    """Importa POR RUTA el medidor sellado del piso (bytes verificados por sha256
    en el runner): `_csv`, `_code`, `_age`, `_school`, `_slug`, `_cells`,
    `_estimate` -- el remuestreo y la rejilla son literalmente los del piso."""
    ruta = Path(inputs[INPUT_MEDIDOR_PISO]["ruta_absoluta"])
    spec = importlib.util.spec_from_file_location("medidor_piso_envipe2024_ejes_0002", ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _carga(m, inputs: dict, v: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    z = inputs[v["payload_id"]]["ruta_absoluta"]
    vic = m._csv(z, v["vic"], COLS_VIC)
    dem = m._csv(z, v["dem"], COLS_DEM)
    d = vic.merge(dem, on="ID_PER", how="left", validate="m:1", indicator=True)
    return vic, d


# ══════════════════════════════ ejes (una variable cada uno) ══════════════

def _eje_sexo(m, d):
    return m._code(d["SEXO"])


def _eje_edad(m, d):
    return m._age(d["EDAD"])


def _eje_escolaridad(m, d):
    return m._school(d["NIV"])


def _eje_dominio(m, d):
    return d["DOMINIO"].str.strip().map({"R": DOMINIO[0], "C": DOMINIO[1], "U": DOMINIO[2]})


def _eje_cobertura(m, d):
    return m._code(d["BP2_1"]).map({"1": COBERTURA[1], "2": COBERTURA[0]})


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
    pref = f"ARBITRO-ENVIPE{ola}"
    reps = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])

    vic, d = _carga(m, inputs, v)
    d["_w"] = pd.to_numeric(d["FAC_DEL"], errors="coerce")
    d["_est"] = d["EST_DIS"].str.strip(); d["_upm"] = d["UPM_DIS"].str.strip()

    # Conductas: literalmente las del piso (spec v2.0 ENVIPE 2024).
    b = m._code(d["BP1_20"]); ev_ok = b.isin(["1", "2"])
    ev = pd.Series(pd.NA, index=d.index, dtype="Float64")
    ev.loc[ev_ok] = (b.loc[ev_ok].eq("2") &
                     m._code(d.loc[ev_ok, "BP1_23"]).isin(["4", "5", "6", "8"])).astype(float)
    den_ok = m._code(d["BPCOD"]).eq("1") & b.isin(["1", "2"]) & m._code(d["BP2_1"]).isin(["1", "2"])
    den = pd.Series(pd.NA, index=d.index, dtype="Float64")
    den.loc[den_ok] = b.loc[den_ok].eq("1").astype(float)

    ejes = {
        "total": (_eje_total(m, d), TOTAL),
        "sexo": (_eje_sexo(m, d), ("1", "2")),
        "edad": (_eje_edad(m, d), EDADES),
        "escolaridad": (_eje_escolaridad(m, d), ESCOLARIDAD),
        "dominio": (_eje_dominio(m, d), DOMINIO),
        "cobertura_seguro": (_eje_cobertura(m, d), COBERTURA),
    }
    pe = f"{pref}-EVASION"; pdn = f"{pref}-DENUNCIA"
    cells = []
    cells += marginal(m, pe, ev, "total", ejes["total"][0], ejes["total"][1])
    cells += marginal(m, pe, ev, "sexo", ejes["sexo"][0], ejes["sexo"][1])
    cells += marginal(m, pe, ev, "edad", ejes["edad"][0], ejes["edad"][1])
    cells += marginal(m, pe, ev, "escolaridad", ejes["escolaridad"][0], ejes["escolaridad"][1])
    cells += marginal(m, pe, ev, "dominio", ejes["dominio"][0], ejes["dominio"][1])
    cells += marginal(m, pdn, den, "total", ejes["total"][0], ejes["total"][1])
    cells += marginal(m, pdn, den, "cobertura_seguro", ejes["cobertura_seguro"][0], ejes["cobertura_seguro"][1])
    out = m._estimate(d, cells, reps, seed)

    # Diagnóstico (enteros; nunca nulos).
    design = d["_w"].notna() & (d["_w"] > 0) & d["_est"].ne("") & d["_upm"].ne("")
    out[f"RESULT-{pref}-G-FILAS-VICTIMIZACION"] = int(len(vic))
    out[f"RESULT-{pref}-G-FILAS-DISENO-VALIDO"] = int(design.sum())
    out[f"RESULT-{pref}-G-JOIN-SIN-DEMOGRAFIA"] = int(d["_merge"].ne("both").sum())
    out[f"RESULT-{pref}-G-REPLICAS"] = int(reps)
    out[f"RESULT-{pref}-G-OLA"] = str(ola)
    out[f"RESULT-{pref}-EVASION-G-N-UNIVERSO"] = int(ev_ok.sum())
    out[f"RESULT-{pref}-EVASION-G-BP1-20-FUERA"] = int((~b.isin(["1", "2"])).sum())
    out[f"RESULT-{pref}-DENUNCIA-G-N-UNIVERSO"] = int(den_ok.sum())
    for eje in EJES:
        out[f"RESULT-{pref}-G-EJE-{m._slug(eje)}-FUERA"] = int(ejes[eje][0].isna().sum())
    return out


# ══════════════════════════════ esquema de resultados ═════════════════════

def esquema_resultados(ola: str = OLA_OBJETIVO) -> list[dict]:
    pref = f"ARBITRO-ENVIPE{ola}"
    cats = {"total": TOTAL, "sexo": ("1", "2"), "edad": EDADES, "escolaridad": ESCOLARIDAD,
            "dominio": DOMINIO, "cobertura_seguro": COBERTURA}

    def slug(x):
        return (str(x).upper().replace("Á", "A").replace("É", "E").replace("Í", "I")
                .replace("Ó", "O").replace("Ú", "U").replace("+", "-MAS")
                .replace("_", "-").replace(" ", "-"))
    rows = []
    for des, ejes in (("EVASION", EJES_EVASION), ("DENUNCIA", EJES_DENUNCIA)):
        for eje in ejes:
            for cat in cats[eje]:
                b = f"RESULT-{pref}-{des}-{slug(eje)}-{slug(cat)}"
                rows.append({"id": f"{b}-P", "tipo": "proporcion", "unidad": "proporción ponderada [0,1]",
                             "permite_no_estimable": True})
                rows.append({"id": f"{b}-IC-LO", "tipo": "proporcion", "unidad": "límite inferior IC95",
                             "permite_no_estimable": True})
                rows.append({"id": f"{b}-IC-HI", "tipo": "proporcion", "unidad": "límite superior IC95",
                             "permite_no_estimable": True})
                rows.append({"id": f"{b}-N", "tipo": "entero", "unidad": "n sin ponderar (delitos)"})
                rows.append({"id": f"{b}-DEN-W", "tipo": "flotante", "unidad": "denominador ponderado"})
                rows.append({"id": f"{b}-B-VALIDAS", "tipo": "entero", "unidad": "réplicas bootstrap definidas"})
    rows.append({"id": f"RESULT-{pref}-G-FILAS-VICTIMIZACION", "tipo": "entero", "unidad": "filas de tmod_vic"})
    rows.append({"id": f"RESULT-{pref}-G-FILAS-DISENO-VALIDO", "tipo": "entero", "unidad": "filas con ponderador > 0 y diseño"})
    rows.append({"id": f"RESULT-{pref}-G-JOIN-SIN-DEMOGRAFIA", "tipo": "entero", "unidad": "delitos sin persona en tsdem"})
    rows.append({"id": f"RESULT-{pref}-G-REPLICAS", "tipo": "entero", "unidad": "réplicas bootstrap"})
    rows.append({"id": f"RESULT-{pref}-G-OLA", "tipo": "texto", "unidad": "ola medida"})
    rows.append({"id": f"RESULT-{pref}-EVASION-G-N-UNIVERSO", "tipo": "entero", "unidad": "delitos con BP1_20 en 1/2"})
    rows.append({"id": f"RESULT-{pref}-EVASION-G-BP1-20-FUERA", "tipo": "entero", "unidad": "delitos con BP1_20 fuera de 1/2"})
    rows.append({"id": f"RESULT-{pref}-DENUNCIA-G-N-UNIVERSO", "tipo": "entero", "unidad": "delitos BPCOD=01 con BP1_20 y BP2_1 válidos"})
    for eje in EJES:
        rows.append({"id": f"RESULT-{pref}-G-EJE-{slug(eje)}-FUERA", "tipo": "entero", "unidad": "delitos fuera del eje (código inválido o blanco)"})
    return rows
