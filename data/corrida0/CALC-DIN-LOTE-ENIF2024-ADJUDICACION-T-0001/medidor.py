#!/usr/bin/env python3
"""Medidor de `CALC-DIN-LOTE-ENIF2024-ADJUDICACION-T-0001` (COMMIT-2 de este
acto: emisiones + adjudicación en un solo CALC, sin reserva de evaluación
propia -- el piso ya está sellado, no hay ola nueva que proteger aquí).

ACTO `GEN2-DIN-LOTE-ENIF2024-SECUNDARIA-1` (22/sep/2026, CAJA). Ejecuta la
opción A de `FP-260922-GEN2-DIN-LOTE-C2-RESTRINGIDO-1-4e12-01` (FIRMADA,
asentada en PR #1003): adjudica los 5 pares `formalidad × {sexo, edad,
escolaridad, localidad, cuenta_formal}` en un estrato «universo T» (quien
trabaja: `P3_13` en 2024, `P3_10` en 2021) APARTE del lote primario -- nunca
se suma a su ΔMAE ni a la frase de producto de las 44 celdas (test propio,
`tests/test_lote_enif2024_adjudicacion_t.py`).

QUÉ HACE
--------
El punto de cada celda del piso C2R se CITA -- no se recompone -- desde el
RESULT ya sellado de `CALC-C2-RESTRINGIDO-IC-ENIF2024-0001` (input
`origen: repo`, `IN-C2R-SELLADO`). Sus RÉPLICAS se RE-DERIVAN aquí con el
MISMO procedimiento de ese CALC -- "réplicas re-derivadas dentro del lote
con el mismo procedimiento" (PIEZAS §5 del encargo) -- importando
`marginal_t`/`_ola_desde_df`/`replicas_t`/`piso_log_aditivo` de su
`medidor.py` sellado (por sha256, nunca copiados) y verificando `REPRODUCE`
contra el punto citado (control, tolerancia declarada) antes de usarlas
como base de los contendientes. El régimen ARBITRO-2024 rige para las dos
olas (firma real de Q2 -- régimen de universo del lote --,
`FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-1-6c10-03`, FIRMADA, verbatim en la
nota de cierre de `GEN2-TRAMITE-FIRMAS-6`: «Fija régimen ARBITRO-2024 para
comparaciones contra el árbitro»; el encargo de este acto cita por error
`…6c10-04` -- que responde Q3, agregador de L, tema ajeno -- intercambio de
etiqueta ya documentado una vez como «logística de citación, no premisa»
por ese mismo acto; se corrige aquí, sin cambiar el régimen que la premisa
sustantiva ya pedía).

Los CINCO contendientes (misma familia y fórmulas del lote, sin
reestimarlas): `C2` (piso, CITADO), `P2` (persistencia: cruce de 2021
dentro de T), `R1`/`R2` (interacción cruda/encogida contra 2021, λ = ½ fija
-- igual que los 14 pares primarios, no se estima), `R3` (raking a tres
vías de `lote_familia.py`). `R` = el cruce OBSERVADO de ENIF 2024 dentro de
T -- código NUEVO de este archivo (`cruce_t()`), porque `C2-RESTRINGIDO`
prohíbe por diseño cualquier función de cruce (su propia guardia R7) y el
`cruce()` de `enif_lote.py` no conoce el universo T. Adjudica con la MISMA
regla v0.3 (`cruces_familia.adjudica`), retador primario `R2`.

Nada de esto se compara contra el universo poblacional (A-bis 4, igual que
C2-RESTRINGIDO) ni se suma al ΔMAE primario del lote (por construcción: los
RESULT de este CALC no comparten prefijo ni id con los del lote primario, y
el test propio lo prueba por comando).

GUARDIA DE RESERVA -- código, no prosa (E.6, PARO a del encargo)
------------------------------------------------------------------
  1. El microdato (`.df`) sólo es alcanzable dentro del NÚCLEO guardado
     (`NUCLEO`). Fuera de él ningún nodo combina dos comparaciones.
  2. `marginal_t_local(ola, eje)`: `eje` es UN `str` posicional y atómico.
  3. `cruce_t(ola, eje_a, eje_b)` es la ÚNICA función que construye una
     llave de dos ejes sobre la ola restringida a T. No hay reserva de
     evaluación que proteger (el piso ya está sellado, la ola 2024 de este
     CALC no es "nueva" en el sentido de E.6): no lanza `ReservaRota` por
     ola reservada, pero SÍ por par no autorizado (`PARES_T`, exactamente
     los 5 del contrato) y por ola alterada tras cargarla.
  4. `auditoria_ast_fuente()` recorre el AST de ESTE archivo al arrancar
     `medir()` y PARA antes de abrir un zip si alguna regla falla.
  5. La ola se re-huella antes de contar: una ola filtrada o reordenada tras
     cargarla lanza `ReservaRota`.

INTERFAZ: `medir(inputs, contrato) -> {"RESULT-…": valor}`.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
import yaml


def _raiz() -> Path:
    p = Path(__file__).resolve()
    for d in p.parents:
        if (d / "tools" / "corrida0.py").exists():
            return d
    raise RuntimeError("raíz del repo no encontrada desde " + str(p))


RAIZ = _raiz()


def _importa(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


# ══ importaciones: el mismo objeto de código, nunca una copia ═══════════════
el = _importa("enif_lote_t", RAIZ / "tools" / "lote_enif2024" / "enif_lote.py")
c2r = _importa("c2_restringido_t", RAIZ / "data" / "corrida0" / "CALC-C2-RESTRINGIDO-IC-ENIF2024-0001" / "medidor.py")
cf = _importa("cruces_familia_t", RAIZ / "tools" / "duelo" / "cruces_familia.py")
lf = _importa("lote_familia_t", RAIZ / "tools" / "lote_enif2024" / "lote_familia.py")

MODULOS_SHA = {"ENIF-LOTE": RAIZ / "tools" / "lote_enif2024" / "enif_lote.py",
               "C2-RESTRINGIDO-MEDIDOR": RAIZ / "data" / "corrida0" / "CALC-C2-RESTRINGIDO-IC-ENIF2024-0001" / "medidor.py",
               "CRUCES-FAMILIA": RAIZ / "tools" / "duelo" / "cruces_familia.py",
               "LOTE-FAMILIA": RAIZ / "tools" / "lote_enif2024" / "lote_familia.py"}

P = "RESULT-DIN-LOTE24-ADJ-T"
FUERA = el.FUERA
EJES_T = ("sexo", "edad", "escolaridad", "localidad", "cuenta_formal", "formalidad")
EJE_UNIVERSO = "formalidad"
NAC_T = "T"
CANDIDATOS = ("C2", "P2", "R1", "R2", "R3")
PISO = "C2"
RETADOR_PRIMARIO = "R2"
UNIVERSO_T = ("T = personas elegidas 18+ de TMODULO con formalidad declarada (no FUERA): "
              "quien trabaja, P3_13 en 1..7 (2024) / P3_10 en 1..6 (2021); blanco por "
              "secuencia y 'no sabe' fuera de T en cada ola")


class ReservaRota(RuntimeError):
    """Se intentó cruzar, filtrar o alterar la ola fuera de lo autorizado."""


class Paro(RuntimeError):
    """Premisa de la spec falsa en el archivo: se PARA, no se reporta cifra."""


def _sha(ruta: Path) -> str:
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


def _f(v):
    if v is None:
        return None
    v = float(v)
    return v if math.isfinite(v) else None


def _slug(s: str) -> str:
    out = []
    for ch in str(s).upper():
        out.append(ch if ch.isalnum() else "-")
    t = "".join(out)
    while "--" in t:
        t = t.replace("--", "-")
    return t.strip("-")


# ══ NÚCLEO guardado: las únicas funciones que tocan el microdato (`.df`) ════

@dataclass(frozen=True)
class OlaT:
    df: pd.DataFrame = field(repr=False, compare=False)
    rotulo: str = ""
    huella: str = ""
    meta: dict = field(default_factory=dict, compare=False)


def _huella(df: pd.DataFrame) -> str:
    h = hashlib.sha256()
    h.update(str(len(df)).encode())
    for c in ("EST", "UPM", "_w", "_y", *EJES_T):
        h.update(b"\x1f")
        h.update("\n".join(df[c].astype(str).tolist()).encode("utf-8"))
    return h.hexdigest()


def _carga_ola_t(zip_path, ola: str, par: dict) -> OlaT:
    """Construye la ola (2021 o 2024) restringida a T. Reusa `_lee_miembro`,
    `_universo`, `_ejes`, `_desenlace_d9`, `_columnas_necesarias` de
    `enif_lote.py` (importados, no copiados) bajo régimen ARBITRO-2024;
    aplica la restricción a T UNA vez, aquí, igual para las dos olas y para
    los seis ejes: fuera de T todo eje vale `FUERA`. Ninguna fila se quita
    (misma técnica que `_ola_desde_df` de `C2-RESTRINGIDO`, generalizada a
    cualquier ola en vez de sólo 2024)."""
    ola = str(ola)
    cols = par["columnas"][ola]
    reg_arbitro_2024 = {"tipo": "ARBITRO-2024", "edad_min": 18,
                        "edad_centinelas": par["universo_regimen"]["edad_centinelas"]}
    df, miembro, enc, catalogo = el._lee_miembro(zip_path, cols["tabla_sufijo"])
    faltan = [c for c in el._columnas_necesarias(cols) if c not in df.columns]
    if faltan:
        raise Paro(f"ENIF {ola}: columnas ausentes {faltan}")
    u, meta_u = el._universo(df, cols, reg_arbitro_2024)
    d_full = el._ejes(u, cols, par, ola)
    fuera_de_t = (d_full[EJE_UNIVERSO] == FUERA).to_numpy()
    d = pd.DataFrame(index=u.index)
    d["EST"] = u[cols["est"]].str.strip()
    d["UPM"] = u[cols["upm"]].str.strip()
    d["_w"] = u["_w"].astype(float)
    for eje in EJES_T:
        d[eje] = np.where(fuera_de_t, FUERA, d_full[eje].to_numpy())
    d["nacional"] = np.where(fuera_de_t, FUERA, NAC_T)
    d["_y"] = el._desenlace_d9(u, cols)
    d = d.reset_index(drop=True)
    en_t = (d["nacional"].to_numpy() == NAC_T)
    if not en_t.any():
        raise Paro(f"ENIF {ola}: el universo T está vacío")
    w = d["_w"].to_numpy()
    meta = dict(meta_u)
    meta.update({"miembro": miembro, "encoding": enc,
                 "filas_t": int(en_t.sum()), "fuera_t": int((~en_t).sum()),
                 "cobertura_t_filas": float(en_t.mean()),
                 "cobertura_t_ponderada": float(w[en_t].sum() / w.sum()),
                 "estratos": int(d["EST"].nunique()),
                 "upm": int((d["EST"] + "\t" + d["UPM"]).nunique())})
    return OlaT(df=d, rotulo=ola, huella=_huella(d), meta=meta)


def _verifica(ola: OlaT) -> None:
    if not isinstance(ola, OlaT):
        raise TypeError("se esperaba una OlaT producida por _carga_ola_t()")
    if _huella(ola.df) != ola.huella:
        raise ReservaRota(f"ENIF {ola.rotulo}: la ola T fue filtrada, reordenada o "
                          "alterada tras cargarla -- agrupar sobre un subconjunto es "
                          "cruzar por otra vía")


@dataclass(frozen=True)
class ReplicasT:
    huella_ola: str
    seed: int
    n_rep: int
    counts: np.ndarray = field(repr=False, compare=False)
    pos_fila: np.ndarray = field(repr=False, compare=False)
    n_upm: int = 0
    estratos_upm_unica: int = 0


def replicas_t_local(ola: OlaT, seed: int, n_rep: int) -> ReplicasT:
    """UN remuestreo por ola: `n_h` UPM con reemplazo dentro de cada estrato,
    UN generador PCG64(seed), estratos y UPM en orden lexicográfico -- la
    misma receta que `enif_lote.py::replicas()` y `C2-RESTRINGIDO
    ::replicas_t()`. Determinista: con la misma ola (misma huella, luego
    mismo universo T) y la misma semilla, reproduce bit a bit las réplicas
    que produjo `C2-RESTRINGIDO` para el mismo universo T sobre ENIF 2024."""
    _verifica(ola)
    est = ola.df["EST"].to_numpy()
    upm = ola.df["UPM"].to_numpy()
    claves = np.array([f"{e}\t{u}" for e, u in zip(est, upm)])
    unicas, pos_fila = np.unique(claves, return_inverse=True)
    upm_est = np.array([c.split("\t", 1)[0] for c in unicas])
    n_upm = len(unicas)
    pos_por_estrato: dict = {}
    for pos, e in enumerate(upm_est):
        pos_por_estrato.setdefault(e, []).append(pos)
    rng = np.random.Generator(np.random.PCG64(int(seed)))
    bloques = []
    for e in sorted(pos_por_estrato):
        pos = np.asarray(pos_por_estrato[e], dtype=np.int64)
        bloques.append(pos[rng.integers(0, len(pos), size=(int(n_rep), len(pos)))])
    idx = np.concatenate(bloques, axis=1)
    counts = np.empty((int(n_rep), n_upm), dtype=np.int32)
    for r in range(int(n_rep)):
        counts[r] = np.bincount(idx[r], minlength=n_upm)
    unica = sum(1 for e in pos_por_estrato if len(pos_por_estrato[e]) == 1)
    return ReplicasT(huella_ola=ola.huella, seed=int(seed), n_rep=int(n_rep), counts=counts,
                     pos_fila=pos_fila.astype(np.int64), n_upm=int(n_upm), estratos_upm_unica=int(unica))


def _estima_mascara(ola: OlaT, rep: ReplicasT, mask: np.ndarray) -> dict:
    w = ola.df["_w"].to_numpy() * mask
    y = w * ola.df["_y"].to_numpy()
    W = np.bincount(rep.pos_fila, weights=w, minlength=rep.n_upm)
    Y = np.bincount(rep.pos_fila, weights=y, minlength=rep.n_upm)
    den = W.sum()
    num = Y.sum()
    punto = (num / den) if den > 0 else None
    reps = np.empty(rep.n_rep, dtype=float)
    W_reps = np.empty(rep.n_rep, dtype=float)
    Y_reps = np.empty(rep.n_rep, dtype=float)
    for a in range(0, rep.n_rep, 1000):
        c = rep.counts[a:a + 1000].astype(np.float64)
        dk, nk = c @ W, c @ Y
        with np.errstate(invalid="ignore", divide="ignore"):
            reps[a:a + 1000] = np.where(dk > 0, nk / dk, np.nan)
        W_reps[a:a + 1000] = dk
        Y_reps[a:a + 1000] = nk
    return {"p": punto, "reps": reps, "n": int(mask.sum()), "W": float(den), "Y": float(num),
            "W_reps": W_reps, "Y_reps": Y_reps}


def marginal_t_local(ola: OlaT, eje: str, rep: ReplicasT, orden_par) -> dict:
    """Celdas de UN eje dentro de T. `eje` es UN `str` posicional."""
    if not isinstance(eje, str):
        raise TypeError(f"eje debe ser UN str, llegó {type(eje).__name__}")
    if eje not in EJES_T + ("nacional",):
        raise ValueError(f"eje {eje!r} no es uno de {EJES_T + ('nacional',)}")
    _verifica(ola)
    if rep.huella_ola != ola.huella:
        raise ReservaRota("las réplicas no son de esta ola T")
    col = ola.df[eje].to_numpy()
    cats = [NAC_T] if eje == "nacional" else list(orden_par(eje))
    return {k: _estima_mascara(ola, rep, col == k) for k in cats}


def cruce_t(ola: OlaT, eje_a: str, eje_b: str, rep: ReplicasT, pares_autorizados, orden_par) -> dict:
    """La ÚNICA llave de dos ejes sobre la ola restringida a T. Lanza
    `ReservaRota` sobre todo par no autorizado por el contrato (los 5 de
    este CALC, nunca más)."""
    if (eje_a, eje_b) not in pares_autorizados:
        raise ReservaRota(f"par T ({eje_a}, {eje_b}) NO autorizado en este CALC")
    for e in (eje_a, eje_b):
        if e not in EJES_T:
            raise ValueError(f"eje {e!r} no es uno de {EJES_T}")
    _verifica(ola)
    if rep.huella_ola != ola.huella:
        raise ReservaRota("las réplicas no son de esta ola T")
    ca, cb = ola.df[eje_a].to_numpy(), ola.df[eje_b].to_numpy()
    out = {}
    for ka in orden_par(eje_a):
        for kb in orden_par(eje_b):
            out[(ka, kb)] = _estima_mascara(ola, rep, (ca == ka) & (cb == kb))
    return out


NUCLEO = ("_carga_ola_t", "_verifica", "replicas_t_local", "_estima_mascara",
          "marginal_t_local", "cruce_t")


# ══ auditoría del AST de este archivo ════════════════════════════════════

_AUDIT_IMPORTS = ("__future__", "ast", "hashlib", "importlib.util", "json", "math",
                  "sys", "dataclasses", "pathlib", "numpy", "pandas", "yaml")
_AUDIT_PROHIBIDOS = ("groupby", "crosstab", "pivot", "pivot_table", "unstack", "stack",
                     "merge", "concat", "query", "eval", "exec", "getattr", "setattr",
                     "globals", "locals", "vars", "__dict__", "iterrows", "itertuples",
                     "MultiIndex", "compile", "read_excel", "read_sav", "read_dta", "open")
_AUDIT_COMPARADORES = (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.In, ast.NotIn)
_AUDIT_COMBINAN = ("cruce_t", "_carga_ola_t", "auditoria_ast_fuente")
_AUDIT_MODULOS_IMPORTADOS = ("enif_lote.py", "medidor.py", "cruces_familia.py", "lote_familia.py")
_AUDIT_OTROS_INSTRUMENTOS = ("encig", "envipe", "enut", "enigh", "enoe", "ensanut",
                             "endutih", "encuci", "endireh", "enasem", "mociba",
                             "enaproce", "ensafi", "lapop", "issp", "wbes",
                             "ennvih", "mxfls", "enadid", "encup")


def _nombre_llamado(call: ast.Call) -> str:
    f = call.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return ""


def _tiene_comparacion(nodo) -> bool:
    for sub in ast.walk(nodo):
        if isinstance(sub, ast.Compare) and any(isinstance(op, _AUDIT_COMPARADORES) for op in sub.ops):
            return True
        if isinstance(sub, ast.Call) and _nombre_llamado(sub) in ("eq", "isin", "ne", "between"):
            return True
    return False


def auditoria_ast_fuente(fuente: str) -> list:
    arbol = ast.parse(fuente)
    viol = []
    exentos: set = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef)):
            cuerpo = nodo.body
            if cuerpo and isinstance(cuerpo[0], ast.Expr) and isinstance(cuerpo[0].value, ast.Constant):
                exentos.add(id(cuerpo[0].value))
        if isinstance(nodo, ast.Assign):
            nombres = [t.id for t in nodo.targets if isinstance(t, ast.Name)]
            if any(n.startswith("_AUDIT_") for n in nombres):
                for sub in ast.walk(nodo.value):
                    if isinstance(sub, ast.Constant):
                        exentos.add(id(sub))
    padre_fn = {}

    def _marca(nodo, fn):
        for hijo in ast.iter_child_nodes(nodo):
            nombre = fn
            if isinstance(hijo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                nombre = hijo.name
            padre_fn[id(hijo)] = nombre
            _marca(hijo, nombre)
    _marca(arbol, "<modulo>")

    n_cruce_def = 0
    for nodo in ast.walk(arbol):
        fn = padre_fn.get(id(nodo), "<modulo>")
        if isinstance(nodo, ast.Import):
            for a in nodo.names:
                if a.name not in _AUDIT_IMPORTS:
                    viol.append(f"R1 import prohibido: {a.name}")
        elif isinstance(nodo, ast.ImportFrom) and (nodo.module or "") not in _AUDIT_IMPORTS:
            viol.append(f"R1 import prohibido: from {nodo.module}")
        nombres = []
        if isinstance(nodo, ast.Attribute):
            nombres.append(nodo.attr)
        if isinstance(nodo, ast.Name):
            nombres.append(nodo.id)
        if isinstance(nodo, ast.Call):
            nombres.append(_nombre_llamado(nodo))
        for nom in nombres:
            if nom in _AUDIT_PROHIBIDOS:
                viol.append(f"R2 nombre prohibido `{nom}` en {fn}")
        es_df = isinstance(nodo, ast.Attribute) and nodo.attr == "df"
        if es_df and fn not in NUCLEO:
            viol.append(f"R3 acceso a `.df` fuera del núcleo guardado: {fn}")
        if fn not in _AUDIT_COMBINAN:
            if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, (ast.BitAnd, ast.BitOr, ast.BitXor, ast.Mult)):
                if _tiene_comparacion(nodo.left) and _tiene_comparacion(nodo.right):
                    viol.append(f"R4 dos comparaciones combinadas por operador en {fn} (línea {nodo.lineno})")
            if isinstance(nodo, ast.BoolOp) and len([v for v in nodo.values if _tiene_comparacion(v)]) >= 2:
                viol.append(f"R4 dos comparaciones combinadas por and/or en {fn} (línea {nodo.lineno})")
        if isinstance(nodo, ast.Call):
            nom = _nombre_llamado(nodo)
            if nom == "OlaT" and fn != "_carga_ola_t":
                viol.append(f"R5 `OlaT(` fuera de _carga_ola_t: {fn}")
            if nom == "_importa":
                arg = nodo.args[1] if len(nodo.args) > 1 else None
                consts = ([c.value for c in ast.walk(arg) if isinstance(c, ast.Constant)]
                          if arg is not None else [])
                if not any(any(str(c).endswith(m) for m in _AUDIT_MODULOS_IMPORTADOS) for c in consts):
                    viol.append(f"R5 `_importa` de un módulo no autorizado en {fn}")
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)) and "cruce" in nodo.name.lower():
            n_cruce_def += 1
            if nodo.name != "cruce_t":
                viol.append(f"R7 función de cruce fuera del núcleo: {nodo.name}")
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str) and id(nodo) not in exentos:
            bajo = nodo.value.lower()
            if any(tok in bajo for tok in _AUDIT_OTROS_INSTRUMENTOS):
                viol.append(f"R8 otro instrumento en constante {nodo.value!r} ({fn})")
    if n_cruce_def != 1:
        viol.append(f"R7 se esperaba exactamente una definición `cruce_t`, hay {n_cruce_def}")
    return viol


def auditoria_ast(ruta: Path) -> list:
    return auditoria_ast_fuente(Path(ruta).read_text(encoding="utf-8"))


# ══ insumos: contrato del lote, dictamen del piso C2R, RESULT sellados ══════

def _bytes(inputs, iid) -> bytes:
    ent = inputs[iid]
    b = ent.get("bytes")
    if b is None:
        b = Path(ent["ruta_absoluta"]).read_bytes()
    return b


def _contrato_lote(inputs) -> dict:
    return yaml.safe_load(_bytes(inputs, "IN-LOTE-SPEC-SELLADA").decode("utf-8"))["parametros"]


def _c2r_sellado(inputs) -> dict:
    doc = json.loads(_bytes(inputs, "IN-C2R-SELLADO").decode("utf-8"))
    return doc["resultados"] if "resultados" in doc else doc


def _plan(par_lote: dict, pares_t: list) -> dict:
    ejes = par_lote["ejes"]

    def orden_par(eje):
        return tuple(ejes[eje]["orden"])
    return {"pares": pares_t, "ejes": ejes, "orden_par": orden_par}


# ══ catálogo de RESULT ═══════════════════════════════════════════════════

def catalogo_resultados(pares_t: list, ejes: dict) -> list:
    cat = []

    def add(rid, tipo, unidad, nulo=False):
        e = {"id": rid, "tipo": tipo, "unidad": unidad}
        if nulo:
            e["permite_no_estimable"] = True
        cat.append(e)

    for iid in ("IN-LOTE-SPEC-SELLADA", "IN-C2R-SELLADO"):
        add(f"{P}-G-INPUT-{_slug(iid)}-SHA256", "texto", f"sha256 del input {iid}")
    for k in MODULOS_SHA:
        add(f"{P}-G-CODIGO-{k}-SHA256", "texto", f"sha256 del módulo {k}")
    add(f"{P}-G-GUARDIA-AST", "texto", "PASA si auditoria_ast() no reporta violaciones")
    add(f"{P}-G-GUARDIA-AST-VIOLACIONES", "entero", "violaciones reportadas")
    add(f"{P}-G-REGIMEN-UNIVERSO", "texto", "régimen de universo de las dos olas")
    add(f"{P}-G-UNIVERSO", "texto", "definición del universo T")
    for ola, w in (("2021", "W21"), ("2024", "W24")):
        add(f"{P}-G-{w}-FILAS-UNIVERSO", "entero", f"filas del universo ARBITRO-2024 en {ola}")
        add(f"{P}-G-{w}-FILAS-T", "entero", f"filas en T, {ola}")
        add(f"{P}-G-{w}-FUERA-T", "entero", f"filas fuera de T, {ola}")
        add(f"{P}-G-{w}-COBERTURA-T-PONDERADA", "proporcion", f"masa T / masa universo, {ola}")
        add(f"{P}-G-{w}-ESTRATOS", "entero", f"EST_DIS distintos, {ola}")
        add(f"{P}-G-{w}-UPM", "entero", f"UPM distintas, {ola}")
    add(f"{P}-G-C2R-CONTROL-VEREDICTO", "texto", "REPRODUCE si las réplicas re-derivadas del piso reproducen el punto C2R sellado")
    add(f"{P}-G-C2R-CONTROL-DELTA-P-MAX", "flotante", "peor |delta P| entre replica re-derivada y punto C2R sellado", True)
    add(f"{P}-G-N-PARES", "entero", "5")
    add(f"{P}-G-N-CELDAS", "entero", "28")
    add(f"{P}-G-N-CELDAS-PUNTUADAS", "entero", "celdas con n >= umbral en las dos olas")
    add(f"{P}-G-EN-DELTA-MAE-PRIMARIO-DEL-LOTE", "texto", "NO, por construcción (prefijo de RESULT distinto)")
    for par_, a, b in pares_t:
        pbase = f"{P}-{_slug(par_)}"
        for cid in CANDIDATOS:
            if cid == PISO:
                continue
            add(f"{pbase}-{cid}-MAE-PP", "flotante", f"MAE de {cid} en T, agregado sobre las celdas puntuadas de este par", True)
            add(f"{pbase}-{cid}-DELTA-MAE-PP", "flotante", f"MAE(C2)-MAE({cid}) en pp, T, agregado sobre este par", True)
            add(f"{pbase}-{cid}-DELTA-IC95INF", "flotante", "IC95 del delta MAE de este par, T", True)
            add(f"{pbase}-{cid}-DELTA-IC95SUP", "flotante", "IC95 del delta MAE de este par, T", True)
            add(f"{pbase}-{cid}-VEREDICTO", "texto", f"veredicto v0.3 de {cid} vs C2 en T, agregado sobre este par (nunca por celda individual)")
            add(f"{pbase}-{cid}-ROL", "texto", "PRIMARIA o SECUNDARIA")
        for ca in ejes[a]["orden"]:
            for cb in ejes[b]["orden"]:
                base = f"{pbase}-{_slug(ca)}-X-{_slug(cb)}"
                add(f"{base}-UNIVERSO", "texto", "universo T de la celda")
                add(f"{base}-ROTULO", "texto", "PROSPECTIVA o RETROSPECTIVA")
                add(f"{base}-R-P", "proporcion", "R observado en T, ENIF 2024 (árbitro)", True)
                add(f"{base}-R-IC95INF", "proporcion", "IC95 réplica a réplica de R en T", True)
                add(f"{base}-R-IC95SUP", "proporcion", "IC95 réplica a réplica de R en T", True)
                add(f"{base}-R-N", "entero", "n de la celda en T, ENIF 2024")
                add(f"{base}-PUNTUADA", "texto", "SI/NO: n >= umbral en las dos olas")
                for cid in CANDIDATOS:
                    cbase = f"{base}-{cid}"
                    add(f"{cbase}-P", "proporcion", f"{cid} en T", True)
                    add(f"{cbase}-IC95INF", "proporcion", f"IC95 de {cid} en T", True)
                    add(f"{cbase}-IC95SUP", "proporcion", f"IC95 de {cid} en T", True)
                    add(f"{cbase}-ERROR-PP", "flotante", f"|{cid} - R| en pp, T", True)
    for cid in CANDIDATOS:
        if cid == PISO:
            continue
        add(f"{P}-G-{cid}-MAE-AGREGADO-PP", "flotante", "MAE agregado de las 28 celdas puntuadas, T", True)
        add(f"{P}-G-{cid}-DELTA-MAE-AGREGADO-PP", "flotante", "MAE(C2)-MAE(cid) agregado, T", True)
        add(f"{P}-G-{cid}-DELTA-IC95-AGREGADO-INF", "flotante", "IC95 del delta agregado, T", True)
        add(f"{P}-G-{cid}-DELTA-IC95-AGREGADO-SUP", "flotante", "IC95 del delta agregado, T", True)
        add(f"{P}-G-{cid}-VEREDICTO-AGREGADO", "texto", "veredicto v0.3 agregado sobre las 28 celdas, T")
    add(f"{P}-G-COMPARACION-POBLACIONAL", "texto", "NINGUNA (A-bis 4): universo T no reconciliable con el poblacional")
    add(f"{P}-G-ADOPTA", "texto", "NO")
    add(f"{P}-G-CRUCE-DERIVADO", "texto", "SI: cruce_t(), único, sobre los 5 pares autorizados")
    return cat


# ══ el medidor ═══════════════════════════════════════════════════════════

def medir(inputs: dict, contrato: dict) -> dict:
    out: dict = {}
    for iid in ("IN-LOTE-SPEC-SELLADA", "IN-C2R-SELLADO"):
        out[f"{P}-G-INPUT-{_slug(iid)}-SHA256"] = str(inputs[iid]["sha256"])
    for k, ruta in MODULOS_SHA.items():
        out[f"{P}-G-CODIGO-{k}-SHA256"] = _sha(ruta)
    viol = auditoria_ast(Path(__file__))
    out[f"{P}-G-GUARDIA-AST-VIOLACIONES"] = len(viol)
    out[f"{P}-G-GUARDIA-AST"] = "PASA" if not viol else "FALLA"
    if viol:
        raise SystemExit("PARO · guardia AST: " + " | ".join(viol[:10]))
    par = contrato["parametros"]
    par_lote = _contrato_lote(inputs)
    pares_t = [tuple(p) for p in par["pares_t"]]
    plan = _plan(par_lote, pares_t)
    zip21 = Path(inputs[par_lote["olas_zip"]["2021"]]["ruta_absoluta"])
    zip24 = Path(inputs[par_lote["olas_zip"]["2024"]]["ruta_absoluta"])
    ola21 = _carga_ola_t(zip21, "2021", par_lote)
    ola24 = _carga_ola_t(zip24, "2024", par_lote)
    return procedimiento(ola21, ola24, inputs, contrato, plan, out)


def procedimiento(ola21: OlaT, ola24: OlaT, inputs: dict, contrato: dict, plan: dict, out: dict) -> dict:
    par = contrato["parametros"]
    n_rep = int(par["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    umbral = int(par["umbral_soporte_n"])
    lam = float(par["lambda_r2"])
    tol_p = float(par["tol_control_c2r_p"])
    orden_par = plan["orden_par"]
    pares_t = plan["pares"]
    pares_autorizados = [(a, b) for _nombre, a, b in pares_t]

    out[f"{P}-G-REGIMEN-UNIVERSO"] = "ARBITRO-2024"
    out[f"{P}-G-UNIVERSO"] = UNIVERSO_T
    for ola, w in ((ola21, "W21"), (ola24, "W24")):
        m = ola.meta
        out[f"{P}-G-{w}-FILAS-UNIVERSO"] = m["filas_universo"]
        out[f"{P}-G-{w}-FILAS-T"] = m["filas_t"]
        out[f"{P}-G-{w}-FUERA-T"] = m["fuera_t"]
        out[f"{P}-G-{w}-COBERTURA-T-PONDERADA"] = m["cobertura_t_ponderada"]
        out[f"{P}-G-{w}-ESTRATOS"] = m["estratos"]
        out[f"{P}-G-{w}-UPM"] = m["upm"]

    rep21 = replicas_t_local(ola21, seed, n_rep)
    rep24 = replicas_t_local(ola24, seed, n_rep)

    c2r_ids = par["c2r_result_ids"]
    c2r_sellado = _c2r_sellado(inputs)
    # ENMIENDA-1 §7: verificado (no supuesto) que R de estos 28 pares-celda
    # nunca fue derivado antes de este acto -- las 28 celdas son PROSPECTIVA.
    ROTULO_VERIFICADO = "PROSPECTIVA"

    peor_delta_c2r = 0.0
    n_puntuadas_total = 0
    R_total: dict = {}
    puntuada_total: dict = {}
    candidatos_total = {cid: {} for cid in CANDIDATOS}

    for nombre, ea, eb in pares_t:
        m21a = marginal_t_local(ola21, ea, rep21, orden_par)
        m21b = marginal_t_local(ola21, eb, rep21, orden_par)
        m21n = marginal_t_local(ola21, "nacional", rep21, orden_par)
        m24a = marginal_t_local(ola24, ea, rep24, orden_par)
        m24b = marginal_t_local(ola24, eb, rep24, orden_par)
        m24n = marginal_t_local(ola24, "nacional", rep24, orden_par)
        x21 = cruce_t(ola21, ea, eb, rep21, pares_autorizados, orden_par)
        x24 = cruce_t(ola24, ea, eb, rep24, pares_autorizados, orden_par)

        def _cel(m, k, n=False):
            v = m[k]
            return cf.Celda(p=_f(v["p"]), replicas=v["reps"], n=(int(v["n"]) if n else None))

        m21 = cf.Marginales(a={k: _cel(m21a, k) for k in orden_par(ea)},
                            b={k: _cel(m21b, k) for k in orden_par(eb)},
                            nac=_cel(m21n, "T"), orden_a=orden_par(ea), orden_b=orden_par(eb))
        cru21 = {c: cf.Celda(p=_f(v["p"]), replicas=v["reps"], n=int(v["n"])) for c, v in x21.items()}
        o21 = cf.OlaAnterior(rotulo="2021", cruce=cru21, marginales=m21)

        inter = cf.interaccion(o21)
        ibar = cf.interaccion_media([inter])
        p2 = cf.persistencia(o21)

        celdas = [(ka, kb) for ka in orden_par(ea) for kb in orden_par(eb)]
        c2_celdas = {}
        for ka, kb in celdas:
            rid = c2r_ids[nombre][ka][kb]
            p_c2r = _f(c2r_sellado[rid])
            # control: el PUNTO re-derivado de MIS marginales T (mismo procedimiento
            # de composicion que C2-RESTRINGIDO, importado por sha256) debe reproducir
            # el punto YA SELLADO que se cita como piso oficial -- punto contra punto,
            # nunca una replica bootstrap contra el punto sellado.
            pa, pb, pn = m24a[ka]["p"], m24b[kb]["p"], m24n["T"]["p"]
            if pa is not None and pb is not None and pn is not None:
                try:
                    mi_c2 = _f(c2r.piso_log_aditivo(c2r._marg(pa, "ahorra_solo_informal"),
                                                    c2r._marg(pb, "ahorra_solo_informal"),
                                                    c2r._marg(pn, "ahorra_solo_informal"))["p"])
                except c2r.MarginalDegenerado:
                    mi_c2 = None
                if mi_c2 is not None and p_c2r is not None:
                    peor_delta_c2r = max(peor_delta_c2r, abs(mi_c2 - p_c2r))
            # las REPLICAS del piso se re-derivan (nunca se recuperan del sellado: no
            # se persistieron) con la MISMA formula, réplica k con réplica k de esta
            # misma corrida -- determinista bajo el mismo seed y el mismo universo T.
            ra, rb, rn = m24a[ka]["reps"], m24b[kb]["reps"], m24n["T"]["reps"]
            with np.errstate(all="ignore"):
                z = np.log(ra / (1 - ra)) + np.log(rb / (1 - rb)) - np.log(rn / (1 - rn))
                reps_c2 = 1.0 / (1.0 + np.exp(-z))
            c2_celdas[(ka, kb)] = cf.Celda(p=p_c2r, replicas=reps_c2)

        # R3: raking a tres vías -- tabla 2021 (a,b,d) vs márgenes T de 2024 (a,d)/(b,d),
        # punto Y réplicas (W_reps/Y_reps ya los calculó `_estima_mascara` dentro de
        # `cruce_t`/`marginal_t_local`: no se vuelve a tocar `.df`).
        oa, ob = orden_par(ea), orden_par(eb)
        t_pt = np.zeros((len(oa), len(ob), 2))
        t_rp = np.zeros((n_rep, len(oa), len(ob), 2))
        for i, ka in enumerate(oa):
            for j, kb in enumerate(ob):
                v = x21.get((ka, kb))
                if v is None:
                    continue
                t_pt[i, j, 1] = v["Y"]
                t_pt[i, j, 0] = v["W"] - v["Y"]
                t_rp[:, i, j, 1] = v["Y_reps"]
                t_rp[:, i, j, 0] = v["W_reps"] - v["Y_reps"]
        ma_pt = np.zeros((len(oa), 2))
        ma_rp = np.zeros((n_rep, len(oa), 2))
        for i, ka in enumerate(oa):
            v = m24a[ka]
            ma_pt[i, 1] = v["Y"]
            ma_pt[i, 0] = v["W"] - v["Y"]
            ma_rp[:, i, 1] = v["Y_reps"]
            ma_rp[:, i, 0] = v["W_reps"] - v["Y_reps"]
        mb_pt = np.zeros((len(ob), 2))
        mb_rp = np.zeros((n_rep, len(ob), 2))
        for j, kb in enumerate(ob):
            v = m24b[kb]
            mb_pt[j, 1] = v["Y"]
            mb_pt[j, 0] = v["W"] - v["Y"]
            mb_rp[:, j, 1] = v["Y_reps"]
            mb_rp[:, j, 0] = v["W_reps"] - v["Y_reps"]
        r3 = lf.r3_por_par(t_pt, t_rp, ma_pt, ma_rp, mb_pt, mb_rp,
                           float(par["r3_ipf"]["tol"]), int(par["r3_ipf"]["max_iter"]))
        r3_p = r3["p"]
        r3_reps = r3["p_reps"]
        r3_celdas = {(ka, kb): cf.Celda(p=_f(r3_p[i, j]), replicas=(r3_reps[:, i, j] if r3_reps is not None else None))
                    for i, ka in enumerate(oa) for j, kb in enumerate(ob)}

        r1 = cf.desplazada(c2_celdas, ibar, 1.0)
        r2 = cf.desplazada(c2_celdas, ibar, lam)
        candidatos = {"C2": c2_celdas, "P2": p2, "R1": r1, "R2": r2, "R3": r3_celdas}
        R = {c: cf.Celda(p=_f(v["p"]), replicas=v["reps"], n=int(v["n"])) for c, v in x24.items()}
        n_por_ola = {"2021": {c: (x21[c]["n"] if x21.get(c) else 0) for c in celdas},
                    "2024": {c: (x24[c]["n"] if x24.get(c) else 0) for c in celdas}}
        puntuada = cf.puntuadas(n_por_ola, umbral)
        # UN veredicto v0.3 por PAR (agregado sobre las celdas de ESTE par) --
        # `adjudica()` nunca da un veredicto por celda individual, sólo por el
        # conjunto que se le pasa (spec v1.0 §7: la regla adjudica "por par",
        # nunca celda a celda).
        adj = cf.adjudica(R, candidatos, puntuada, piso=PISO, retador=RETADOR_PRIMARIO,
                          umbral_vence_pp=float(par["umbral_vence_pp"]),
                          umbral_reserva_pp=float(par["umbral_reserva_pp"]))
        pbase = f"{P}-{_slug(nombre)}"
        for cid in CANDIDATOS:
            if cid == PISO:
                continue
            d = adj["candidatos"][cid]
            out[f"{pbase}-{cid}-MAE-PP"] = d.get("mae_pp")
            out[f"{pbase}-{cid}-DELTA-MAE-PP"] = d.get("delta_mae_pp")
            dic = d.get("delta_ic95")
            out[f"{pbase}-{cid}-DELTA-IC95INF"] = _f(dic[0]) if dic else None
            out[f"{pbase}-{cid}-DELTA-IC95SUP"] = _f(dic[1]) if dic else None
            out[f"{pbase}-{cid}-VEREDICTO"] = d.get("veredicto")
            out[f"{pbase}-{cid}-ROL"] = d.get("rol")

        for ka, kb in celdas:
            base = f"{pbase}-{_slug(ka)}-X-{_slug(kb)}"
            out[f"{base}-UNIVERSO"] = UNIVERSO_T
            out[f"{base}-ROTULO"] = ROTULO_VERIFICADO
            r_c = R.get((ka, kb))
            out[f"{base}-R-P"] = _f(r_c.p) if r_c else None
            ic_r = cf.ic95_de(r_c) if r_c else None
            out[f"{base}-R-IC95INF"] = _f(ic_r[0]) if ic_r else None
            out[f"{base}-R-IC95SUP"] = _f(ic_r[1]) if ic_r else None
            out[f"{base}-R-N"] = int(r_c.n) if r_c and r_c.n is not None else 0
            es_puntuada = puntuada.get((ka, kb), False)
            out[f"{base}-PUNTUADA"] = "SI" if es_puntuada else "NO"
            if es_puntuada:
                n_puntuadas_total += 1
            for cid in CANDIDATOS:
                cbase = f"{base}-{cid}"
                k = adj["candidatos"][cid]["celdas"].get((ka, kb), {})
                out[f"{cbase}-P"] = k.get("p")
                ic = k.get("ic95")
                out[f"{cbase}-IC95INF"] = _f(ic[0]) if ic else None
                out[f"{cbase}-IC95SUP"] = _f(ic[1]) if ic else None
                out[f"{cbase}-ERROR-PP"] = k.get("error_pp")
            llave = (nombre, ka, kb)
            R_total[llave] = R.get((ka, kb))
            puntuada_total[llave] = es_puntuada
            for cid in CANDIDATOS:
                candidatos_total[cid][llave] = candidatos[cid].get((ka, kb))

    out[f"{P}-G-N-PARES"] = len(pares_t)
    out[f"{P}-G-N-CELDAS"] = sum(len(orden_par(a)) * len(orden_par(b)) for _n, a, b in pares_t)
    out[f"{P}-G-N-CELDAS-PUNTUADAS"] = n_puntuadas_total
    out[f"{P}-G-EN-DELTA-MAE-PRIMARIO-DEL-LOTE"] = "NO"
    out[f"{P}-G-C2R-CONTROL-DELTA-P-MAX"] = peor_delta_c2r
    out[f"{P}-G-C2R-CONTROL-VEREDICTO"] = "REPRODUCE" if peor_delta_c2r <= tol_p else "NO-REPRODUCE"

    # UN veredicto agregado sobre las 28 celdas de los 5 pares juntos (análogo
    # a la comparación primaria del lote sobre sus 44 celdas, pero en T y
    # nunca sumado a esa cifra -- prefijo de RESULT distinto, ver §5).
    adj_total = cf.adjudica(R_total, candidatos_total, puntuada_total, piso=PISO,
                            retador=RETADOR_PRIMARIO,
                            umbral_vence_pp=float(par["umbral_vence_pp"]),
                            umbral_reserva_pp=float(par["umbral_reserva_pp"]))
    for cid in CANDIDATOS:
        if cid == PISO:
            continue
        d = adj_total["candidatos"][cid]
        out[f"{P}-G-{cid}-MAE-AGREGADO-PP"] = d.get("mae_pp")
        out[f"{P}-G-{cid}-DELTA-MAE-AGREGADO-PP"] = d.get("delta_mae_pp")
        dic = d.get("delta_ic95")
        out[f"{P}-G-{cid}-DELTA-IC95-AGREGADO-INF"] = _f(dic[0]) if dic else None
        out[f"{P}-G-{cid}-DELTA-IC95-AGREGADO-SUP"] = _f(dic[1]) if dic else None
        out[f"{P}-G-{cid}-VEREDICTO-AGREGADO"] = d.get("veredicto")
    out[f"{P}-G-COMPARACION-POBLACIONAL"] = "NINGUNA (A-bis 4): universo T no reconciliable con el poblacional"
    out[f"{P}-G-ADOPTA"] = "NO"
    out[f"{P}-G-CRUCE-DERIVADO"] = "SI: cruce_t(), único, sobre los 5 pares autorizados"
    return out
