#!/usr/bin/env python3
"""El primer resultado que produzca este procedimiento es el que se reporta.

CALC-ARBITRO-MARGINALES-ENIF2024-0001 · ACTO GEN2-ARBITRO-MARGINALES-1 (P-ENIF).

QUÉ ESTIMA (spec §1, primera línea): la realidad de la ola nueva -- los
MARGINALES POR EJE de ENIF 2024 para los dos desenlaces de ahorro del árbitro
(`ahorra_solo_informal` = D9 e `informal_cualquiera`), unidad = PERSONA
elegida 18+, escala = proporción ponderada en [0, 1], IC95 por bootstrap de
UPM estratificado con réplicas compartidas. Es el mismo procedimiento del
piso sellado (`CALC-PISOS-ENIF2021-EJES-0003` + `…-FORMALIDAD-0001`)
apuntado a la ola nueva: el remuestreo, la rejilla y las conductas se
IMPORTAN del medidor sellado del piso (input `MEDIDOR-PISO-EJES-0003`, por
sha256); aquí sólo vive el mapa de nemónicos por ola y la guardia.

OLA COMO PARÁMETRO (D-22 ampliada): `contrato["parametros"]["ola"]` decide el
mapa de variables. Con `ola=2021` sobre `enif2021_csv` el MISMO punto de
entrada reproduce los pisos sellados (prueba de oro,
`tests/test_arbitro_marginales_enif2024.py`). Con `ola=2024` mide la
realidad. Nunca las dos en una corrida.

MAPA DE NEMÓNICOS 2021 -> 2024 (A.15, por texto de pregunta; fuentes en la
spec §2): `conjunto_de_datos_tmodulo_enif_2021.csv` -> `TMODULO.csv` ·
`FAC_ELE` -> `FAC_PER` · `EDAD` -> `EDAD_V` · `P3_1_1` (0-9) -> `NIV` (00-11;
09 especialidad, 10 maestría, 11 doctorado -> superior) · `P5_7_i` -> `P5_6_i`
(«ahorró en esa cuenta») · `P3_10` (1-5 con / 6 sin) -> `P3_13` (1-6 con / 7
sin). Sin cambio: `SEXO`, `TLOC`, `P5_1_i`, `P5_4_i`, `EST_DIS`, `UPM_DIS`.

GUARDIA DE UNA SOLA VARIABLE DE AGRUPACIÓN (firma 3D, 21/sep/2026 -- misma
semántica que el guardián de `tools/celda_d/marginales_reproduccion.py`):
  · `marginal(m, prefijo, y, eje, grupos, categorias)` recibe UN `str` de eje de
    la lista blanca `EJES`; una lista, dos ejes o un eje fuera de lista es
    `ValueError`. No existe función de cruce.
  · `auditoria_ast()` recorre el AST de ESTE archivo al arrancar `medir()`,
    antes de abrir el zip: importa sólo la lista blanca; ningún
    `groupby`/`crosstab`/`pivot`/`merge`; toda llamada a `marginal(` lleva un
    eje literal de `EJES`; `_cells` del piso sólo se llama dentro de
    `marginal`; ningún constructor de eje (`_eje_*`) combina dos
    comparaciones; ninguna constante nombra otro instrumento ni un archivo
    fuera de la lista. Probada por mutación en el test.
  · RESERVA: con `ola != 2024` ningún input cuyo id nombre 2024 entra; la
    sección de crédito de ENIF 2024 (RESERVADA) no se lee: ninguna variable
    `P6_*`/`P7_*` figura en las columnas cargadas.
Este archivo no ve, no deriva y no imprime ningún cruce. No adopta nada.
"""
from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

OLA_OBJETIVO = "2024"
EJES = ("total", "sexo", "edad", "escolaridad", "localidad", "formalidad", "cuenta")
DESENLACES = ("D9", "INFORMAL-CUALQUIERA")
EDADES = ("18-29", "30-44", "45-59", "60+")
ESCOLARIDAD = ("hasta_primaria", "secundaria", "media_superior", "superior")
LOCALIDAD = ("menor de 15 000", "15 000 y mas")
FORMALIDAD = ("sin seguridad social", "con seguridad social")
CUENTA = ("sin cuenta", "con cuenta")
TOTAL = ("todos",)

# Un mapa por ola. Claves = rol; valores = nemónico en esa ola.
# 2021 es el piso sellado (spec v2.1 + formalidad v1.0); 2024 es la ola nueva.
VARIABLES = {
    "2021": {
        "payload_id": "enif2021_csv",
        "miembro": "conjunto_de_datos_tmodulo_enif_2021.csv",
        "ponderador": "FAC_ELE", "estrato": "EST_DIS", "upm": "UPM_DIS",
        "sexo": "SEXO", "edad": "EDAD", "escolaridad": "P3_1_1", "localidad": "TLOC",
        "formalidad": "P3_10", "formalidad_con": ("1", "2", "3", "4", "5"), "formalidad_sin": ("6",),
        "informal": tuple(f"P5_1_{i}" for i in range(1, 7)),
        "cuentas": tuple(f"P5_4_{i}" for i in range(1, 10)),
        "ahorro_formal": tuple(f"P5_7_{i}" for i in range(1, 10)),
        "escolaridad_superior_extra": (),
    },
    "2024": {
        "payload_id": "enif_2024_enif_2024_bd_csv",
        "miembro": "TMODULO.csv",
        "ponderador": "FAC_PER", "estrato": "EST_DIS", "upm": "UPM_DIS",
        "sexo": "SEXO", "edad": "EDAD_V", "escolaridad": "NIV", "localidad": "TLOC",
        "formalidad": "P3_13", "formalidad_con": ("1", "2", "3", "4", "5", "6"), "formalidad_sin": ("7",),
        "informal": tuple(f"P5_1_{i}" for i in range(1, 7)),
        "cuentas": tuple(f"P5_4_{i}" for i in range(1, 10)),
        "ahorro_formal": tuple(f"P5_6_{i}" for i in range(1, 10)),
        # NIV 2024 (FD xlsx, 2 dígitos): 09 Especialidad · 10 Maestría · 11 Doctorado
        # (forense/notas/2026-09-02-MAESTRA35-L1-P0-censo.md §4.1). `_school` del
        # piso cubre 0-9; 10 y 11 son «superior» por texto.
        "escolaridad_superior_extra": ("10", "11"),
    },
}
INPUT_MEDIDOR_PISO = "MEDIDOR-PISO-EJES-0003"


class ParoDeGuardia(RuntimeError):
    """Una guardia no está satisfecha. El módulo no mide."""


# ══════════════════════════ auditoría del AST (E.6 como código) ═══════════

_AUDIT_IMPORTS = ("__future__", "ast", "importlib.util", "sys", "pathlib", "numpy", "pandas")
_AUDIT_PROHIBIDOS = ("groupby", "crosstab", "pivot", "pivot_table", "unstack", "stack",
                     "merge", "concat", "cruce", "eval", "exec", "compile",
                     "__import__", "getattr", "globals", "locals", "query", "agg",
                     "aggregate", "transform", "iterrows", "itertuples", "MultiIndex")
_AUDIT_OTROS_INSTRUMENTOS = ("encig", "envipe", "enut", "enigh", "enoe", "ensanut", "endutih",
                             "encuci", "endireh", "enasem", "mociba", "ensafi", "eder2017", "eder_", "lapop",
                             "ennvih", "mxfls", "enadid", "encup")
_AUDIT_EXT = (".zip", ".csv", ".xlsx", ".xls", ".dbf", ".sav", ".dta", ".pdf")
_AUDIT_ARCHIVOS = ("conjunto_de_datos_tmodulo_enif_2021.csv", "TMODULO.csv")
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
        if isinstance(nodo, ast.Call) and _nombre_llamado(nodo) in _AUDIT_PROHIBIDOS:
            viol.append(f"R2 llamada prohibida `{_nombre_llamado(nodo)}()` en {fn}")
        # R3 · `marginal(` lleva UN eje literal de EJES; `_cells` sólo dentro de `marginal`
        if isinstance(nodo, ast.Call):
            nom = _nombre_llamado(nodo)
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
            if OLA_OBJETIVO in str(iid) or "enif_2024" in str(iid).lower():
                raise ParoDeGuardia(f"RESERVA: insumo `{iid}` de {OLA_OBJETIVO} con ola={ola}")
    if INPUT_MEDIDOR_PISO not in inputs:
        raise ParoDeGuardia(f"falta el input `{INPUT_MEDIDOR_PISO}` (medidor sellado del piso)")
    return v


def _piso(inputs: dict):
    """Importa POR RUTA el medidor sellado del piso (bytes verificados por sha256
    en el runner): `_csv`, `_code`, `_age`, `_school`, `_slug`, `_cells`,
    `_estimate`, `_known_any`, `_formal` -- el remuestreo y las conductas son
    literalmente los del piso."""
    ruta = Path(inputs[INPUT_MEDIDOR_PISO]["ruta_absoluta"])
    spec = importlib.util.spec_from_file_location("medidor_piso_enif2021_ejes_0003", ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


# ══════════════════════════════ ejes (una variable cada uno) ══════════════

def _eje_sexo(m, d, v):
    return m._code(d[v["sexo"]])


def _eje_edad(m, d, v):
    return m._age(d[v["edad"]])


def _eje_escolaridad(m, d, v):
    base = m._school(d[v["escolaridad"]])
    extra = m._code(d[v["escolaridad"]]).isin(list(v["escolaridad_superior_extra"]))
    base = base.where(~extra, "superior")
    return base


def _eje_localidad(m, d, v):
    return m._code(d[v["localidad"]]).map({"1": LOCALIDAD[1], "2": LOCALIDAD[1],
                                            "3": LOCALIDAD[0], "4": LOCALIDAD[0]})


def _eje_formalidad(m, d, v):
    c = m._code(d[v["formalidad"]])
    out = pd.Series(pd.NA, index=d.index, dtype="object")
    out.loc[c.isin(list(v["formalidad_con"]))] = FORMALIDAD[1]
    out.loc[c.isin(list(v["formalidad_sin"]))] = FORMALIDAD[0]
    return out


def _eje_cuenta(m, d, v):
    a = d[list(v["cuentas"])].apply(m._code)
    out = pd.Series(pd.NA, index=d.index, dtype="object")
    out.loc[a.eq("1").any(axis=1)] = CUENTA[1]
    out.loc[a.eq("2").all(axis=1)] = CUENTA[0]
    return out


def _eje_total(m, d, v):
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
    pref = f"ARBITRO-ENIF{ola}"
    reps = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])

    inf = list(v["informal"]); accounts = list(v["cuentas"]); savings = list(v["ahorro_formal"])
    cols = inf + accounts + savings + [v["sexo"], v["edad"], v["escolaridad"], v["localidad"],
                                       v["formalidad"], v["ponderador"], v["estrato"], v["upm"]]
    z = inputs[v["payload_id"]]["ruta_absoluta"]
    d = m._csv(z, v["miembro"], cols)
    d["_w"] = pd.to_numeric(d[v["ponderador"]], errors="coerce")
    d["_est"] = d[v["estrato"]].str.strip(); d["_upm"] = d[v["upm"]].str.strip()

    # Conductas: literalmente las del piso (spec v2.1: pares por posición).
    informal = m._known_any(d, inf); formal = m._formal(d, accounts, savings)
    any_inf = informal.astype("Float64")
    only = pd.Series(pd.NA, index=d.index, dtype="Float64")
    only.loc[informal.eq(False) | formal.eq(True)] = 0.0
    only.loc[informal.eq(True) & formal.eq(False)] = 1.0
    desenlaces = {"D9": only, "INFORMAL-CUALQUIERA": any_inf}

    ejes = {
        "total": (_eje_total(m, d, v), TOTAL),
        "sexo": (_eje_sexo(m, d, v), ("1", "2")),
        "edad": (_eje_edad(m, d, v), EDADES),
        "escolaridad": (_eje_escolaridad(m, d, v), ESCOLARIDAD),
        "localidad": (_eje_localidad(m, d, v), LOCALIDAD),
        "formalidad": (_eje_formalidad(m, d, v), FORMALIDAD),
        "cuenta": (_eje_cuenta(m, d, v), CUENTA),
    }
    cells = []
    for des, y in desenlaces.items():
        p = f"{pref}-{des}"
        cells += marginal(m, p, y, "total", ejes["total"][0], ejes["total"][1])
        cells += marginal(m, p, y, "sexo", ejes["sexo"][0], ejes["sexo"][1])
        cells += marginal(m, p, y, "edad", ejes["edad"][0], ejes["edad"][1])
        cells += marginal(m, p, y, "escolaridad", ejes["escolaridad"][0], ejes["escolaridad"][1])
        cells += marginal(m, p, y, "localidad", ejes["localidad"][0], ejes["localidad"][1])
        cells += marginal(m, p, y, "formalidad", ejes["formalidad"][0], ejes["formalidad"][1])
        cells += marginal(m, p, y, "cuenta", ejes["cuenta"][0], ejes["cuenta"][1])
    out = m._estimate(d, cells, reps, seed)

    # Diagnóstico de universo y de ejes (enteros; nunca nulos).
    design = d["_w"].notna() & (d["_w"] > 0) & d["_est"].ne("") & d["_upm"].ne("")
    out[f"RESULT-{pref}-G-FILAS-PERSONAS"] = int(len(d))
    out[f"RESULT-{pref}-G-FILAS-DISENO-VALIDO"] = int(design.sum())
    out[f"RESULT-{pref}-G-REPLICAS"] = int(reps)
    out[f"RESULT-{pref}-G-OLA"] = str(ola)
    for des, y in desenlaces.items():
        out[f"RESULT-{pref}-{des}-G-N-UNIVERSO"] = int(y.notna().sum())
        out[f"RESULT-{pref}-{des}-G-DESENLACE-INDEFINIDO"] = int(y.isna().sum())
    for eje in EJES:
        g = ejes[eje][0]
        out[f"RESULT-{pref}-G-EJE-{m._slug(eje)}-FUERA"] = int(g.isna().sum())
    fcode = m._code(d[v["formalidad"]])
    out[f"RESULT-{pref}-G-FORMALIDAD-NO-SABE"] = int(fcode.eq("9").sum())
    out[f"RESULT-{pref}-G-FORMALIDAD-BLANCO"] = int(fcode.eq("").sum())
    ecode = m._code(d[v["escolaridad"]])
    out[f"RESULT-{pref}-G-ESCOLARIDAD-SUPERIOR-EXTRA-N"] = int(
        ecode.isin(list(v["escolaridad_superior_extra"])).sum())
    return out


# ══════════════════════════════ esquema de resultados ═════════════════════

def esquema_resultados(ola: str = OLA_OBJETIVO) -> list[dict]:
    """Los ids que `medir()` emite para una ola, con tipo y unidad -- de aquí
    sale el bloque `resultados:` de `spec.yaml` (generado, no tecleado)."""
    pref = f"ARBITRO-ENIF{ola}"
    cats = {"total": TOTAL, "sexo": ("1", "2"), "edad": EDADES, "escolaridad": ESCOLARIDAD,
            "localidad": LOCALIDAD, "formalidad": FORMALIDAD, "cuenta": CUENTA}

    def slug(x):
        return (str(x).upper().replace("Á", "A").replace("É", "E").replace("Í", "I")
                .replace("Ó", "O").replace("Ú", "U").replace("+", "-MAS")
                .replace("_", "-").replace(" ", "-"))
    rows = []
    for des in DESENLACES:
        for eje in EJES:
            for cat in cats[eje]:
                b = f"RESULT-{pref}-{des}-{slug(eje)}-{slug(cat)}"
                rows.append({"id": f"{b}-P", "tipo": "proporcion", "unidad": "proporción ponderada [0,1]",
                             "permite_no_estimable": True})
                rows.append({"id": f"{b}-IC-LO", "tipo": "proporcion", "unidad": "límite inferior IC95",
                             "permite_no_estimable": True})
                rows.append({"id": f"{b}-IC-HI", "tipo": "proporcion", "unidad": "límite superior IC95",
                             "permite_no_estimable": True})
                rows.append({"id": f"{b}-N", "tipo": "entero", "unidad": "n sin ponderar"})
                rows.append({"id": f"{b}-DEN-W", "tipo": "flotante", "unidad": "denominador ponderado"})
                rows.append({"id": f"{b}-B-VALIDAS", "tipo": "entero", "unidad": "réplicas bootstrap definidas"})
        rows.append({"id": f"RESULT-{pref}-{des}-G-N-UNIVERSO", "tipo": "entero", "unidad": "personas con desenlace definido"})
        rows.append({"id": f"RESULT-{pref}-{des}-G-DESENLACE-INDEFINIDO", "tipo": "entero", "unidad": "personas con desenlace indefinido"})
    rows.append({"id": f"RESULT-{pref}-G-FILAS-PERSONAS", "tipo": "entero", "unidad": "filas del módulo"})
    rows.append({"id": f"RESULT-{pref}-G-FILAS-DISENO-VALIDO", "tipo": "entero", "unidad": "filas con ponderador > 0 y diseño"})
    rows.append({"id": f"RESULT-{pref}-G-REPLICAS", "tipo": "entero", "unidad": "réplicas bootstrap"})
    rows.append({"id": f"RESULT-{pref}-G-OLA", "tipo": "texto", "unidad": "ola medida"})
    for eje in EJES:
        rows.append({"id": f"RESULT-{pref}-G-EJE-{slug(eje)}-FUERA", "tipo": "entero", "unidad": "personas fuera del eje (código inválido o blanco)"})
    rows.append({"id": f"RESULT-{pref}-G-FORMALIDAD-NO-SABE", "tipo": "entero", "unidad": "código 9 en el ítem de formalidad"})
    rows.append({"id": f"RESULT-{pref}-G-FORMALIDAD-BLANCO", "tipo": "entero", "unidad": "blanco por secuencia en el ítem de formalidad"})
    rows.append({"id": f"RESULT-{pref}-G-ESCOLARIDAD-SUPERIOR-EXTRA-N", "tipo": "entero", "unidad": "personas con código de escolaridad 10/11 (2024) mapeado a superior"})
    return rows
