#!/usr/bin/env python3
"""Cableado ENIF del lote de 14 cruces de ENIF 2024 (`ahorra_solo_informal`):
emisiones (COMMIT-2), adjudicación (COMMIT-3) y los dos oros, parametrizados.

ACTO `GEN2-DIN-LOTE-ENIF2024-COMMIT-1` (21/sep/2026). Contrato humano:
`forense/prereg-caja/DIN-lote-enif2024-spec-v1_0.md` (sucesora de la
PROPUESTA v0.1 de `#967`). Firmas: F1/F2 (`FP-260921-GEN2-TRAMITE-FIRMAS-4-
8a1f-01/-02`), enmienda v0.3 (`FP-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-01`),
D-22 ampliada (`-8a1f-05`), opción A de dirección (λ = ½ en los 14 pares).

Aquí vive TODO lo que sabe de ENIF: qué zip es qué ola, sus nemónicos, cómo
se derivan los seis ejes y el desenlace D9, y la guardia de reserva. Lo
genérico está fuera y se IMPORTA, no se copia:
  · `tools/duelo/cruces_familia.py`  (ajeno, `#968`) — C2, persistencia,
    interacción, encogida (aquí con λ fija), soporte y `adjudica()` v0.3.
  · `tools/lote_enif2024/lote_familia.py` (propio) — R3 (raking a tres
    vías), cobertura por par, conteo ¾ y lectura mecánica del B-bis.
Este archivo se deposita BYTE A BYTE como `medidor.py` en cada CALC del lote
(E.5: el sello cubre el código que mide); el sha256 de los módulos que
importa se emite como RESULT y viaja como input `origen: repo` del contrato.

INTERFAZ: `medir(inputs, contrato) -> {"RESULT-…": valor}`;
`parametros.punto_de_entrada` ∈ {emisiones, adjudicacion, oro_c2ic}.

GUARDIA DE RESERVA — código, no prosa (E.6, PARO a del encargo)
----------------------------------------------------------------
  1. El microdato (`.df`) sólo es alcanzable dentro del NÚCLEO guardado
     (`NUCLEO`). Fuera de él ningún nodo combina dos comparaciones.
  2. `marginal(ola, eje)`: `eje` es UN `str` posicional y atómico; agrupa por
     UNA columna ya derivada de UN eje. No hay `*ejes`, no hay lista.
  3. `cruce(ola, eje_a, eje_b)` es la ÚNICA función que construye una llave
     de dos ejes. Lanza `ReservaRota` si la ola está `reservada` (la ola
     nueva se carga reservada en emisiones y en el oro C2-IC) o si el par
     no está en `pares_cruce_autorizados_2024` del contrato (en el COMMIT-1
     sólo `localidad × edad`, ya abierto por el piloto 1; en el COMMIT-3, los
     14). Un par vetado se prueba en cada corrida y el resultado se emite.
  4. `auditoria_ast_fuente()` recorre el AST de ESTE archivo al arrancar
     `medir()` y PARA antes de abrir un zip si alguna regla falla; cada
     regla tiene control positivo por mutación en
     `tests/test_lote_enif2024.py` (3D: guardia probada por mutación).
  5. La ola se re-huella antes de contar: una ola filtrada o reordenada tras
     cargarla (la otra forma de cruzar) lanza `ReservaRota`.

RÉGIMEN DE UNIVERSO — dos casas conviven, y se declara cuál se usa
-------------------------------------------------------------------
  `PILOTO-1`      filtros globales de la spec §1: 18 ≤ edad ≤ 97 (98/99
                  centinelas fuera, contados), TLOC ∈ {1,2,3,4}, peso > 0.
                  Es el del piloto 1 y el del lote.
  `ARBITRO-2024`  el de `tools/medidor_ahorro_enif24.py::carga()` que selló
                  los marginales (#971, C2-IC): todo TMODULO con edad ≥ 18 y
                  peso > 0; «fuera» POR EJE (edad 97/98, escolaridad 99,
                  formalidad blanco/9), sin filtro de TLOC. Sólo lo usa el oro
                  del C2-IC, para reproducir sus réplicas a la tolerancia.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import io
import json
import math
import sys
import zipfile
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


cf = _importa("cruces_familia", RAIZ / "tools" / "duelo" / "cruces_familia.py")
lf = _importa("lote_familia", RAIZ / "tools" / "lote_enif2024" / "lote_familia.py")

MODULOS_SHA = {
    "CRUCES-FAMILIA": RAIZ / "tools" / "duelo" / "cruces_familia.py",
    "LOTE-FAMILIA": RAIZ / "tools" / "lote_enif2024" / "lote_familia.py",
    "ENIF-LOTE": RAIZ / "tools" / "lote_enif2024" / "enif_lote.py",
}

FUERA = "(fuera)"
NAC = "NAC"
CANDIDATOS = ("C2", "P2", "R1", "R2", "R3")
ROTULO = {"C2": "piso log-aditivo sobre marginales SELLADOS de la ola nueva (IC réplica a réplica)",
          "P2": "persistencia: el cruce de ENIF 2021 tal cual",
          "R1": "interacción histórica cruda: expit(logit C2 + delta_21)",
          "R2": "interacción histórica encogida: expit(logit C2 + lambda*delta_21), lambda fija",
          "R3": "ajuste proporcional iterativo (raking a tres vías de la tabla 2021 a los márgenes 2024)"}
PISO = "C2"
RETADOR_PRIMARIO = "R2"
REGIMENES = ("PILOTO-1", "ARBITRO-2024")
EJES = ("sexo", "edad", "escolaridad", "localidad", "formalidad", "cuenta_formal")


class ReservaRota(RuntimeError):
    """Se intentó cruzar, filtrar o alterar la ola nueva fuera de lo autorizado."""


class Paro(RuntimeError):
    """Premisa de la spec falsa en el archivo: se PARA, no se reporta cifra."""


def _slug(s: str) -> str:
    out = []
    for ch in str(s).upper():
        out.append(ch if ch.isalnum() else "-")
    t = "".join(out)
    while "--" in t:
        t = t.replace("--", "-")
    return t.strip("-")


def _sha(ruta: Path) -> str:
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


def _f(v):
    if v is None:
        return None
    v = float(v)
    return v if math.isfinite(v) else None


def _txt(v) -> str:
    return "NO-CONSTRUIBLE" if v is None else str(v)


def _sino(v) -> str:
    return "NO-CONSTRUIBLE" if v is None else ("SI" if v else "NO")


# ══ NÚCLEO guardado: las únicas funciones que tocan el microdato (`.df`) ═══

@dataclass(frozen=True)
class OlaEnif:
    df: pd.DataFrame = field(repr=False, compare=False)
    rotulo: str = ""
    huella: str = ""
    reservada: bool = True
    pares_autorizados: tuple = ()
    meta: dict = field(default_factory=dict, compare=False)


def _lee_miembro(zip_path, sufijo_miembro):
    """Lee UN miembro del zip por sufijo. Los .zip de INEGI mezclan UTF-8 y
    latin-1: se intenta utf-8 y se cae a latin-1 DECLARANDO la caída."""
    with zipfile.ZipFile(zip_path) as zf:
        cands = [n for n in zf.namelist() if n.lower().endswith(sufijo_miembro.lower())]
        if len(cands) != 1:
            raise Paro(f"{sufijo_miembro}: {len(cands)} miembros en {Path(zip_path).name}")
        crudo = zf.read(cands[0])
        catalogo = None
        cat_n = [n for n in zf.namelist() if n.lower().endswith("catalogos/p3_1_1.csv")]
        if len(cat_n) == 1:
            catalogo = zf.read(cat_n[0])
    for enc in ("utf-8", "latin-1"):
        try:
            texto = crudo.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:                                            # pragma: no cover
        raise Paro(f"{sufijo_miembro}: ni utf-8 ni latin-1")
    df = pd.read_csv(io.StringIO(texto), dtype=str, keep_default_na=False, na_filter=False)
    df.columns = [c.strip().strip('"').upper() for c in df.columns]
    return df, cands[0], enc, catalogo


def _catalogo_zip(crudo: bytes) -> dict:
    """`catalogos/p3_1_1.csv` de 2021: {codigo normalizado: etiqueta}."""
    for enc in ("utf-8", "latin-1"):
        try:
            texto = crudo.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    out = {}
    for linea in texto.splitlines()[1:]:
        if not linea.strip():
            continue
        cve, _, desc = linea.partition(",")
        out[_norm_codigo(cve)] = desc.strip().strip('"')
    return out


def _norm_codigo(c: str) -> str:
    c = str(c).strip().strip('"')
    return str(int(c)) if c.isdigit() else c


def _universo(df, cols, reg: dict):
    """Filtros del régimen, con sus conteos. Devuelve (u, meta)."""
    n_archivo = len(df)
    edad_txt = df[cols["edad"]].str.strip()
    centinela = edad_txt.isin([str(c) for c in reg["edad_centinelas"]])
    edad_num = pd.to_numeric(edad_txt, errors="coerce")
    w_num = pd.to_numeric(df[cols["peso"]].str.strip(), errors="coerce")
    tipo = reg["tipo"]
    if tipo == "PILOTO-1":
        f_edad = (~centinela) & edad_num.between(int(reg["edad_min"]), int(reg["edad_max"]))
        f_tloc = df[cols["tloc"]].str.strip().isin([str(t) for t in reg["tloc"]])
        f_w = w_num.notna() & (w_num > 0)
        keep = f_edad & f_tloc & f_w
    elif tipo == "ARBITRO-2024":
        if edad_num.isna().any() or (edad_num < int(reg["edad_min"])).any():
            raise Paro("EDAD inválida o menor de 18 (régimen ARBITRO-2024)")
        if w_num.isna().any() or (w_num <= 0).any():
            raise Paro("peso no numérico positivo (régimen ARBITRO-2024)")
        keep = pd.Series(True, index=df.index)
    else:
        raise Paro(f"régimen de universo desconocido: {tipo!r}")
    est = df[cols["est"]].str.strip()
    upm = df[cols["upm"]].str.strip()
    if (est[keep] == "").any() or (upm[keep] == "").any():
        raise Paro("EST_DIS/UPM_DIS con faltantes en el universo")
    fuera_dominio = pd.Series(False, index=df.index)
    for c in list(cols["informal"]) + list(cols["formal"]):
        fuera_dominio |= ~df[c].str.strip().isin(["1", "2", ""])
    u = df.loc[keep].copy()
    u["_w"] = w_num.loc[keep].astype(float)
    u["_edad"] = edad_num.loc[keep]
    meta = {"filas_archivo": int(n_archivo), "filas_universo": int(keep.sum()),
            "filas_edad_centinela": int(centinela.sum()),
            "filas_codigo_fuera_de_dominio": int((fuera_dominio & keep).sum()),
            "poblacion_expandida": float(u["_w"].sum())}
    return u, meta


def _desenlace_d9(u, cols):
    informal = np.zeros(len(u), dtype=bool)
    for c in cols["informal"]:
        informal |= u[c].str.strip().eq("1").to_numpy()
    formal = np.zeros(len(u), dtype=bool)
    for c in cols["formal"]:
        formal |= u[c].str.strip().eq("1").to_numpy()
    return (informal & ~formal).astype(float)


def _ejes(u, cols, par: dict, ola: str) -> pd.DataFrame:
    """Una columna por eje, derivada de UN eje cada una. Categoría no
    declarada -> FUERA; código de escolaridad ausente del catálogo -> PARO."""
    d = pd.DataFrame(index=u.index)
    d["sexo"] = u[cols["sexo"]].str.strip().map(lambda s: {"1": "1 Hombre", "2": "2 Mujer"}.get(s, FUERA))
    edad = u["_edad"]
    tr = pd.Series(FUERA, index=u.index, dtype=object)
    for etq, (a, b) in par["edad_tramos"].items():
        tr[(edad >= a) & (edad <= b)] = etq
    d["edad"] = tr
    cat = {_norm_codigo(k): v for k, v in par["escolaridad_catalogo"][ola].items()}
    mapa = par["escolaridad_tramo_por_etiqueta"]
    fuera_etq = set(par["escolaridad_fuera_etiquetas"])
    codigos = u[cols["escolaridad"]].str.strip()
    desconocidos = sorted({c for c in codigos.unique() if c != "" and _norm_codigo(c) not in cat})
    if desconocidos:
        raise Paro(f"escolaridad {ola}: códigos sin etiqueta declarada {desconocidos}")

    def _esc(c):
        if c == "":
            return FUERA
        etq = cat[_norm_codigo(c)]
        if etq in fuera_etq:
            return FUERA
        if etq not in mapa:
            raise Paro(f"escolaridad {ola}: etiqueta {etq!r} sin tramo declarado")
        return mapa[etq]
    d["escolaridad"] = codigos.map(_esc)
    d["localidad"] = u[cols["tloc"]].str.strip().map(lambda s: par["localidad_map"].get(s, FUERA))
    fm = par["formalidad_map"][ola]
    d["formalidad"] = u[cols["formalidad"]].str.strip().map(lambda s: fm.get(s, FUERA))
    cu = u[list(cols["cuentas"])].apply(lambda s: s.str.strip())
    tiene = cu.eq("1").any(axis=1)
    nunca = cu.isin(["1", "2"]).sum(axis=1).eq(0)
    d["cuenta_formal"] = np.where(nunca, FUERA, np.where(tiene, "con cuenta", "sin cuenta"))
    d["nacional"] = NAC
    return d


def _huella(df: pd.DataFrame) -> str:
    h = hashlib.sha256()
    h.update(str(len(df)).encode())
    for c in ("EST", "UPM", "_w", "_y", *EJES):
        h.update(b"\x1f")
        h.update("\n".join(df[c].astype(str).tolist()).encode("utf-8"))
    return h.hexdigest()


def carga_ola(zip_path, ola: str, par: dict, reservada: bool, pares_autorizados) -> OlaEnif:
    """ÚNICA construcción de `OlaEnif`: lee el miembro de la ola, aplica el
    régimen de universo, deriva D9 y los seis ejes."""
    ola = str(ola)
    cols = par["columnas"][ola]
    reg = dict(par["universo_regimen"])
    df, miembro, enc, catalogo = _lee_miembro(zip_path, cols["tabla_sufijo"])
    faltan = [c for c in _columnas_necesarias(cols) if c not in df.columns]
    if faltan:
        raise Paro(f"ENIF {ola}: columnas ausentes {faltan}")
    u, meta = _universo(df, cols, reg)
    d = _ejes(u, cols, par, ola)
    d["EST"] = u[cols["est"]].str.strip()
    d["UPM"] = u[cols["upm"]].str.strip()
    d["_w"] = u["_w"].astype(float)
    d["_y"] = _desenlace_d9(u, cols)
    d = d.reset_index(drop=True)
    meta.update({"miembro": miembro, "encoding": enc,
                 "estratos": int(d["EST"].nunique()),
                 "upm": int((d["EST"] + "\t" + d["UPM"]).nunique()),
                 "numerador_d9": int(d["_y"].sum()),
                 "fuera_por_eje": {e: int((d[e] == FUERA).sum()) for e in EJES},
                 "catalogo_escolaridad": "SIN-CATALOGO-EN-ZIP"})
    if catalogo is not None:
        decl = {_norm_codigo(k): v for k, v in par["escolaridad_catalogo"][ola].items()}
        leido = _catalogo_zip(catalogo)
        meta["catalogo_escolaridad"] = "COINCIDE" if decl == leido else (
            "DISCORDA: " + json.dumps({k: (decl.get(k), leido.get(k)) for k in sorted(set(decl) | set(leido))
                                       if decl.get(k) != leido.get(k)}, ensure_ascii=False)[:300])
    return OlaEnif(df=d, rotulo=ola, huella=_huella(d), reservada=bool(reservada),
                   pares_autorizados=tuple(tuple(p) for p in pares_autorizados), meta=meta)


def _columnas_necesarias(cols: dict) -> list:
    out = [cols[k] for k in ("edad", "tloc", "peso", "est", "upm", "sexo", "escolaridad", "formalidad")]
    return out + list(cols["cuentas"]) + list(cols["informal"]) + list(cols["formal"])


def _verifica(ola: OlaEnif) -> None:
    if not isinstance(ola, OlaEnif):
        raise TypeError("se esperaba una OlaEnif producida por carga_ola()")
    if _huella(ola.df) != ola.huella:
        raise ReservaRota(f"ENIF {ola.rotulo}: la ola fue filtrada, reordenada o alterada "
                          "tras cargarla -- agrupar sobre un subconjunto es cruzar por otra vía")


@dataclass(frozen=True)
class ReplicasEnif:
    huella_ola: str
    seed: int
    n_rep: int
    counts: np.ndarray = field(repr=False, compare=False)
    pos_fila: np.ndarray = field(repr=False, compare=False)
    n_upm: int = 0
    estratos_upm_unica: int = 0


def replicas(ola: OlaEnif, seed: int, n_rep: int) -> ReplicasEnif:
    """UN remuestreo por ola, compartido por todos los grupos y celdas: `n_h`
    UPM con reemplazo dentro de cada estrato, UN generador PCG64(seed),
    estratos en orden lexicográfico de EST_DIS y UPM en orden lexicográfico
    de UPM_DIS -- la receta del piloto 1 (`_replicas`) y del C2-IC
    (`replicas_enif`), que consumen el generador en el mismo orden."""
    _verifica(ola)
    est = ola.df["EST"].to_numpy()
    upm = ola.df["UPM"].to_numpy()
    claves = np.array([f"{e}\t{u}" for e, u in zip(est, upm)])
    unicas, primeras, pos_fila = np.unique(claves, return_index=True, return_inverse=True)
    upm_est = est[primeras]
    pos_por_estrato: dict = {}
    for pos, e in enumerate(upm_est):
        pos_por_estrato.setdefault(e, []).append(pos)
    n_upm = len(unicas)
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
    return ReplicasEnif(huella_ola=ola.huella, seed=int(seed), n_rep=int(n_rep), counts=counts,
                        pos_fila=pos_fila.astype(np.int64), n_upm=int(n_upm), estratos_upm_unica=int(unica))


def _estima_mascara(ola: OlaEnif, rep: ReplicasEnif, mask: np.ndarray) -> dict:
    """Punto, réplicas, masa y numerador del grupo `mask` -- todo agregado por
    UPM y sumado en el orden lexicográfico de las UPM (mismos bits que el
    piloto 1)."""
    w = ola.df["_w"].to_numpy() * mask
    y = w * ola.df["_y"].to_numpy()
    W = np.bincount(rep.pos_fila, weights=w, minlength=rep.n_upm)
    Y = np.bincount(rep.pos_fila, weights=y, minlength=rep.n_upm)
    den = W.sum()
    punto = (Y.sum() / den) if den > 0 else None
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
    return {"p": punto, "reps": reps, "n": int(mask.sum()), "W": float(den), "Y": float(Y.sum()),
            "W_reps": W_reps, "Y_reps": Y_reps}


def marginal(ola: OlaEnif, eje: str, rep: ReplicasEnif) -> dict:
    """Celdas de UN eje. `eje` es UN `str` POSICIONAL: no hay lista ni
    `*ejes`; la columna ya viene derivada de un solo eje."""
    if not isinstance(eje, str):
        raise TypeError(f"eje debe ser UN str, llegó {type(eje).__name__}")
    if eje not in EJES + ("nacional",):
        raise ValueError(f"eje {eje!r} no es uno de {EJES + ('nacional',)}")
    _verifica(ola)
    if rep.huella_ola != ola.huella:
        raise ReservaRota("las réplicas no son de esta ola")
    col = ola.df[eje].to_numpy()
    cats = [NAC] if eje == "nacional" else sorted({c for c in np.unique(col) if c != FUERA})
    return {k: _estima_mascara(ola, rep, col == k) for k in cats}


def cruce(ola: OlaEnif, eje_a: str, eje_b: str, rep: ReplicasEnif) -> dict:
    """La ÚNICA llave de dos ejes. Lanza `ReservaRota` sobre la ola reservada
    y sobre todo par no autorizado por el contrato."""
    if ola.reservada:
        raise ReservaRota(f"ENIF {ola.rotulo} está RESERVADA: no se deriva ningún cruce")
    if (eje_a, eje_b) not in ola.pares_autorizados:
        raise ReservaRota(f"par ({eje_a}, {eje_b}) NO autorizado en ENIF {ola.rotulo}")
    for e in (eje_a, eje_b):
        if e not in EJES:
            raise ValueError(f"eje {e!r} no es uno de {EJES}")
    _verifica(ola)
    if rep.huella_ola != ola.huella:
        raise ReservaRota("las réplicas no son de esta ola")
    ca, cb = ola.df[eje_a].to_numpy(), ola.df[eje_b].to_numpy()
    out = {}
    for ka in sorted({c for c in np.unique(ca) if c != FUERA}):
        for kb in sorted({c for c in np.unique(cb) if c != FUERA}):
            out[(ka, kb)] = _estima_mascara(ola, rep, (ca == ka) & (cb == kb))
    return out


NUCLEO = ("_lee_miembro", "_catalogo_zip", "_universo", "_desenlace_d9", "_ejes",
          "_huella", "carga_ola", "_verifica", "replicas", "_estima_mascara",
          "marginal", "cruce")


# ══ auditoría del AST de este archivo: la guardia como código ═══════════════

_AUDIT_IMPORTS = ("__future__", "ast", "hashlib", "importlib.util", "io", "json", "math",
                  "sys", "zipfile", "dataclasses", "pathlib", "numpy", "pandas", "yaml")
_AUDIT_PROHIBIDOS = ("groupby", "crosstab", "pivot", "pivot_table", "unstack", "stack",
                     "merge", "concat", "query", "eval", "exec", "getattr", "setattr",
                     "globals", "locals", "vars", "__dict__", "iterrows", "itertuples",
                     "MultiIndex", "compile", "__import__", "read_excel", "read_sav",
                     "read_dta", "open")
_AUDIT_SOLO_EN = {"read_csv": ("_lee_miembro",), "ZipFile": ("_lee_miembro",),
                  "apply": ("_ejes",)}
_AUDIT_COMPARADORES = (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.In, ast.NotIn)
_AUDIT_COMBINAN = ("cruce", "_universo", "_desenlace_d9", "_ejes", "auditoria_ast_fuente")


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
    padre_fn = {}

    def _marca(nodo, fn):
        for hijo in ast.iter_child_nodes(nodo):
            nombre = fn
            if isinstance(hijo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                nombre = hijo.name
            padre_fn[id(hijo)] = nombre
            _marca(hijo, nombre)
    _marca(arbol, "<modulo>")

    n_cruce_def, n_olaenif = 0, 0
    for nodo in ast.walk(arbol):
        fn = padre_fn.get(id(nodo), "<modulo>")
        # R1 · imports: sólo la lista blanca
        if isinstance(nodo, ast.Import):
            for a in nodo.names:
                if a.name not in _AUDIT_IMPORTS:
                    viol.append(f"R1 import prohibido: {a.name}")
        elif isinstance(nodo, ast.ImportFrom) and (nodo.module or "") not in _AUDIT_IMPORTS:
            viol.append(f"R1 import prohibido: from {nodo.module}")
        # R2 · nombres prohibidos, y los que sólo caben en una función
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
            permitidas = _AUDIT_SOLO_EN.get(nom)
            if permitidas is not None and fn not in permitidas:
                viol.append(f"R2 `{nom}` fuera de {_AUDIT_SOLO_EN[nom]}: {fn}")
        # R3 · el microdato (`.df`) sólo dentro del núcleo guardado
        es_df = isinstance(nodo, ast.Attribute) and nodo.attr == "df"
        if es_df and fn not in NUCLEO:
            viol.append(f"R3 acceso a `.df` fuera del núcleo guardado: {fn}")
        # R4 · fuera del núcleo que combina, ningún nodo combina dos comparaciones
        if fn not in _AUDIT_COMBINAN:
            if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, (ast.BitAnd, ast.BitOr, ast.BitXor, ast.Mult)):
                if _tiene_comparacion(nodo.left) and _tiene_comparacion(nodo.right):
                    viol.append(f"R4 dos comparaciones combinadas por operador en {fn} (línea {nodo.lineno})")
            if isinstance(nodo, ast.BoolOp) and len([v for v in nodo.values if _tiene_comparacion(v)]) >= 2:
                viol.append(f"R4 dos comparaciones combinadas por and/or en {fn} (línea {nodo.lineno})")
        # R5 · constructores sólo donde la spec los pone
        if isinstance(nodo, ast.Call):
            nom = _nombre_llamado(nodo)
            if nom == "OlaEnif":
                n_olaenif += 1
                if fn != "carga_ola":
                    viol.append(f"R5 `OlaEnif(` fuera de carga_ola: {fn}")
            es_carga = nom == "carga_ola"
            if es_carga and fn != "_carga_olas":
                viol.append(f"R5 `carga_ola()` fuera de _carga_olas: {fn}")
            # R6 · marginal: eje atómico (nombre o literal str); el núcleo con
            #      (ola, eje, rep) y el método de OlaCargada con (eje)
            if nom == "marginal":
                es_nucleo = isinstance(nodo.func, ast.Name)
                pos = 1 if es_nucleo else 0
                esperados = 3 if es_nucleo else 1
                if len(nodo.args) != esperados or nodo.keywords:
                    viol.append(f"R6 marginal con {len(nodo.args)} posicionales en {fn}")
                elif not isinstance(nodo.args[pos], (ast.Name, ast.Constant)):
                    viol.append(f"R6 marginal con eje no atómico en {fn}")
                elif isinstance(nodo.args[pos], ast.Constant) and not isinstance(nodo.args[pos].value, str):
                    viol.append(f"R6 marginal con eje literal no str en {fn}")
        # R7 · sólo dos definiciones llevan `cruce` en el nombre: la del
        #      núcleo y el método de OlaCargada que la llama; ninguna otra
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)) and "cruce" in nodo.name.lower():
            n_cruce_def += 1
            if nodo.name != "cruce":
                viol.append(f"R7 función de cruce fuera del núcleo: {nodo.name}")
    if n_cruce_def != 2:
        viol.append(f"R7 se esperaban exactamente dos definiciones `cruce` (núcleo y método), hay {n_cruce_def}")
    if n_olaenif != 1:
        viol.append(f"R5 se esperaba exactamente una construcción `OlaEnif(`, hay {n_olaenif}")
    return viol


def auditoria_ast(ruta: Path) -> list:
    return auditoria_ast_fuente(Path(ruta).read_text(encoding="utf-8"))


# ══ olas cargadas y lectura de sellados ════════════════════════════════════

class OlaCargada:
    """Una ola abierta por el núcleo con sus réplicas compartidas; marginales
    de UN eje por llamada y cruces sólo por la guardia."""

    def __init__(self, ola_obj: OlaEnif, seed: int, n_rep: int):
        self.ola = ola_obj
        self.rotulo = str(ola_obj.rotulo)
        self.rep = replicas(ola_obj, seed, n_rep)
        self._marg = {}
        self._cruce = {}

    def marginal(self, eje: str) -> dict:
        if eje not in self._marg:
            self._marg[eje] = marginal(self.ola, eje, self.rep)
        return self._marg[eje]

    def cruce(self, eje_a: str, eje_b: str) -> dict:
        k = (eje_a, eje_b)
        if k not in self._cruce:
            self._cruce[k] = cruce(self.ola, eje_a, eje_b, self.rep)
        return self._cruce[k]


def _carga_olas(inputs, par, reservada_nueva: bool, autorizados_nueva) -> dict:
    """Abre las olas del contrato: {rotulo: OlaCargada}. La ola nueva se
    carga `reservada_nueva`; la anterior, abierta. ÚNICO llamador de
    `carga_ola`."""
    seed = int(par["_seed"])
    n_rep = int(par["bootstrap_replicas"])
    olas = {}
    for rot, iid in sorted(par["olas_zip"].items()):
        rot = str(rot)
        es_nueva = rot == str(par["ola_nueva"])
        ola_obj = carga_ola(inputs[iid]["ruta_absoluta"], rot, par,
                            reservada=(reservada_nueva and es_nueva),
                            pares_autorizados=(autorizados_nueva if es_nueva else _todos_los_pares(par)))
        olas[rot] = OlaCargada(ola_obj, seed, n_rep)
    return olas


def _todos_los_pares(par) -> list:
    return [(p["a"], p["b"]) for p in par["pares"].values()]


def _bytes(inputs, iid) -> bytes:
    ent = inputs[iid]
    b = ent.get("bytes")
    if b is None:
        b = Path(ent["ruta_absoluta"]).read_bytes()
    return b


def _lee_json_resultados(inputs, iid) -> dict:
    doc = json.loads(_bytes(inputs, iid).decode("utf-8"))
    return doc["resultados"] if isinstance(doc, dict) and "resultados" in doc else doc


def _lee_yaml_parametros(inputs, iid) -> dict:
    """`spec.yaml` sellado del piloto 1: sus `parametros` (yaml de la casa,
    leído sin PyYAML: sólo se necesitan los escalares anidados bajo
    `marginales_sellados_D9`)."""
    return yaml.safe_load(_bytes(inputs, iid).decode("utf-8"))


def _valor_ruta(doc, ruta: str):
    cur = doc
    for k in ruta.split("."):
        cur = cur[k]
    return cur


def _sellados(inputs, par) -> dict:
    """{eje: {cat: p}} de los marginales SELLADOS de la ola nueva, más
    `nacional` y, si el contrato los trae, las masas ponderadas para R3.
    Formato `resultados-json` (ids) o `spec-yaml` (rutas con punto)."""
    out = {"p": {}, "masa": {}, "origen": {}}
    for bloque in ("puntos", "masa"):
        cfg = par["marginales_sellados"].get(bloque)
        if not cfg:
            continue
        if cfg["formato"] == "resultados-json":
            doc = _lee_json_resultados(inputs, cfg["input"])
            lee = lambda rid: doc[rid]
        elif cfg["formato"] == "spec-yaml":
            doc = _lee_yaml_parametros(inputs, cfg["input"])
            lee = lambda rid: _valor_ruta(doc, rid)
        else:
            raise Paro(f"marginales_sellados.{bloque}.formato desconocido: {cfg['formato']!r}")
        dest = out["p"] if bloque == "puntos" else out["masa"]
        for eje, cats in cfg["ids"].items():
            dest[eje] = {cat: float(lee(rid)) for cat, rid in cats.items()}
        dest["nacional"] = {NAC: float(lee(cfg["nacional_id"]))}
        out["origen"][bloque] = cfg["input"]
    return out


def _celda(v: dict) -> cf.Celda:
    return cf.Celda(p=_f(v["p"]), replicas=v["reps"], n=int(v["n"]))


def _ic(c: cf.Celda):
    return cf.ic95_de(c) if c is not None else None


def _sin_definir(celdas: dict) -> int:
    return int(sum(0 if c.replicas is None else int((~np.isfinite(c.replicas)).sum())
                   for c in celdas.values()))


def _orden(par, eje) -> tuple:
    return tuple(par["ejes"][eje]["orden"])


def _celdas_par(par, nombre) -> list:
    p = par["pares"][nombre]
    return [(ka, kb) for ka in _orden(par, p["a"]) for kb in _orden(par, p["b"])]


def _cid(P, nombre_par, cid, ka, kb) -> str:
    base = f"{P}-{_slug(nombre_par)}"
    if cid:
        base += f"-{cid}"
    return f"{base}-{_slug(ka)}-X-{_slug(kb)}"


# ══ emisiones ══════════════════════════════════════════════════════════════

def _marginales_ola(oc: OlaCargada, par, eje_a, eje_b, sellados=None) -> cf.Marginales:
    """`Marginales` del par: punto SELLADO (si se dan) y réplicas re-derivadas
    de la misma ola. Categoría declarada sin filas: Celda(p=None)."""
    def _dic(eje):
        m = oc.marginal(eje)
        d = {}
        for k in _orden(par, eje):
            v = m.get(k)
            p_sell = None if sellados is None else sellados["p"].get(eje, {}).get(k)
            if v is None:
                d[k] = cf.Celda(p=None if sellados is None else _f(p_sell), replicas=None, n=0)
            else:
                d[k] = cf.Celda(p=_f(v["p"]) if sellados is None else _f(p_sell),
                                replicas=v["reps"], n=int(v["n"]))
        return d
    nac = oc.marginal("nacional")[NAC]
    p_nac = _f(nac["p"]) if sellados is None else _f(sellados["p"]["nacional"][NAC])
    return cf.Marginales(a=_dic(eje_a), b=_dic(eje_b),
                         nac=cf.Celda(p=p_nac, replicas=nac["reps"], n=int(nac["n"])),
                         orden_a=_orden(par, eje_a), orden_b=_orden(par, eje_b))


def _rejilla_abierta(oc: OlaCargada, par, eje_a, eje_b) -> tuple:
    """({celda: Celda}, {celda: dict crudo}) con todas las celdas de la
    rejilla; las que no aparecen en la ola quedan Celda(p=None, n=0)."""
    x = oc.cruce(eje_a, eje_b)
    celdas, crudo = {}, {}
    for ka in _orden(par, eje_a):
        for kb in _orden(par, eje_b):
            v = x.get((ka, kb))
            if v is None:
                celdas[(ka, kb)] = cf.Celda(p=None, replicas=None, n=0)
                crudo[(ka, kb)] = None
            else:
                c = _celda(v)
                celdas[(ka, kb)] = cf.Celda(p=c.p, ic95=_ic(c), replicas=c.replicas, n=c.n)
                crudo[(ka, kb)] = v
    return celdas, crudo


def _margen_masa(oc: OlaCargada, par, eje, sellados, n_rep) -> tuple:
    """Masa por (categoría, d) de la ola nueva: punto desde el sellado
    (masa × p) y réplicas re-derivadas. (A, 2) y (K, A, 2)."""
    orden = _orden(par, eje)
    m = oc.marginal(eje)
    pt = np.zeros((len(orden), 2))
    rp = np.zeros((n_rep, len(orden), 2))
    for i, k in enumerate(orden):
        masa = sellados["masa"].get(eje, {}).get(k)
        p = sellados["p"].get(eje, {}).get(k)
        if masa is not None and p is not None:
            pt[i, 1] = masa * p
            pt[i, 0] = masa * (1.0 - p)
        else:
            pt[i, :] = np.nan
        v = m.get(k)
        if v is not None:
            rp[:, i, 1] = v["Y_reps"]
            rp[:, i, 0] = v["W_reps"] - v["Y_reps"]
    return pt, rp


def _tabla_21(crudo: dict, par, eje_a, eje_b, n_rep) -> tuple:
    oa, ob = _orden(par, eje_a), _orden(par, eje_b)
    pt = np.zeros((len(oa), len(ob), 2))
    rp = np.zeros((n_rep, len(oa), len(ob), 2))
    for i, ka in enumerate(oa):
        for j, kb in enumerate(ob):
            v = crudo.get((ka, kb))
            if v is None:
                continue
            pt[i, j, 1] = v["Y"]
            pt[i, j, 0] = v["W"] - v["Y"]
            rp[:, i, j, 1] = v["Y_reps"]
            rp[:, i, j, 0] = v["W_reps"] - v["Y_reps"]
    return pt, rp


def _familia_par(nombre, par, nueva: OlaCargada, anterior: OlaCargada, sellados) -> dict:
    """Los cinco contendientes del par. Devuelve {"candidatos": {cid: {celda:
    Celda}}, "meta": {...}}. Un par cuyo C2 es NO-EMITIBLE emite sólo P2."""
    p = par["pares"][nombre]
    ea, eb = p["a"], p["b"]
    n_rep = int(par["bootstrap_replicas"])
    c21, crudo21 = _rejilla_abierta(anterior, par, ea, eb)
    m21 = _marginales_ola(anterior, par, ea, eb, sellados=None)
    o21 = cf.OlaAnterior(rotulo=anterior.rotulo, cruce=c21, marginales=m21)
    cand = {"P2": cf.persistencia(o21)}
    meta = {"c2_estado": str(p["c2"]), "lambda": float(par["lambda_r2"]), "ibar": None,
            "r3": None, "n21": {c: c21[c].n for c in c21}}
    vacio = {c: cf.Celda(p=None, replicas=None) for c in c21}
    if str(p["c2"]) == "EMITIBLE":
        m_t = _marginales_ola(nueva, par, ea, eb, sellados=sellados)
        c2 = cf.c2(m_t)
        inter = cf.interaccion(o21)
        ibar = cf.interaccion_media([inter])
        cand["C2"] = c2
        cand["R1"] = cf.desplazada(c2, ibar, 1.0)
        cand["R2"] = cf.desplazada(c2, ibar, float(par["lambda_r2"]))
        meta["ibar"] = ibar
        t_pt, t_rp = _tabla_21(crudo21, par, ea, eb, n_rep)
        ma_pt, ma_rp = _margen_masa(nueva, par, ea, sellados, n_rep)
        mb_pt, mb_rp = _margen_masa(nueva, par, eb, sellados, n_rep)
        if np.isfinite(ma_pt).all() and np.isfinite(mb_pt).all():
            r3 = lf.r3_por_par(t_pt, t_rp, ma_pt, ma_rp, mb_pt, mb_rp,
                               float(par["r3_ipf"]["tol"]), int(par["r3_ipf"]["max_iter"]))
            oa, ob = _orden(par, ea), _orden(par, eb)
            cand["R3"] = {(ka, kb): cf.Celda(p=_f(r3["p"][i, j]), replicas=r3["p_reps"][:, i, j])
                          for i, ka in enumerate(oa) for j, kb in enumerate(ob)}
            meta["r3"] = {k: r3[k] for k in ("iteraciones_punto", "convergio_punto",
                                             "iteraciones_reps", "reps_no_convergen")}
        else:
            cand["R3"] = dict(vacio)
            meta["r3"] = {"estado": "NO-CONSTRUIBLE: masa sellada ausente para algún margen"}
    else:
        for cid in ("C2", "R1", "R2", "R3"):
            cand[cid] = dict(vacio)
    return {"candidatos": cand, "meta": meta}


def _emite_conteos(out, P, w, oc: OlaCargada):
    m = oc.ola.meta
    out[f"{P}-G-{w}-FILAS-ARCHIVO"] = int(m["filas_archivo"])
    out[f"{P}-G-{w}-FILAS-UNIVERSO"] = int(m["filas_universo"])
    out[f"{P}-G-{w}-FILAS-EDAD-CENTINELA"] = int(m["filas_edad_centinela"])
    out[f"{P}-G-{w}-FILAS-CODIGO-FUERA-DE-DOMINIO"] = int(m["filas_codigo_fuera_de_dominio"])
    out[f"{P}-G-{w}-ESTRATOS"] = int(m["estratos"])
    out[f"{P}-G-{w}-UPM"] = int(m["upm"])
    out[f"{P}-G-{w}-ESTRATOS-UPM-UNICA"] = int(oc.rep.estratos_upm_unica)
    out[f"{P}-G-{w}-ENCODING"] = str(m["encoding"])
    out[f"{P}-G-{w}-CATALOGO-ESCOLARIDAD"] = str(m["catalogo_escolaridad"])
    for e in EJES:
        out[f"{P}-G-{w}-FUERA-{_slug(e)}"] = int(m["fuera_por_eje"][e])


def _emite_celda(out, base, c: cf.Celda, con_n=False):
    out[f"{base}-P"] = _f(c.p)
    ic = _ic(c)
    out[f"{base}-IC95INF"] = None if ic is None else _f(ic[0])
    out[f"{base}-IC95SUP"] = None if ic is None else _f(ic[1])
    if con_n:
        out[f"{base}-N"] = None if c.n is None else int(c.n)


def _emite_cabecera(out, P, inputs, par):
    for iid in inputs:
        out[f"{P}-G-INPUT-{_slug(iid)}-SHA256"] = str(inputs[iid]["sha256"])
    for k, ruta in MODULOS_SHA.items():
        out[f"{P}-G-CODIGO-{k}-SHA256"] = _sha(ruta)
    out[f"{P}-G-OLA-NUEVA"] = str(par["ola_nueva"])
    out[f"{P}-G-REGIMEN-UNIVERSO"] = str(par["universo_regimen"]["tipo"])
    viol = auditoria_ast(Path(__file__).resolve())
    out[f"{P}-G-GUARDIA-AST-VIOLACIONES"] = len(viol)
    out[f"{P}-G-GUARDIA-AST"] = "PASA" if not viol else "FALLA"
    if viol:
        raise SystemExit("PARO · guardia AST: " + " | ".join(viol[:10]))


def _emite_marginales_nueva(out, P, nueva: OlaCargada, par, sellados, ejes_usados):
    peor, n_cmp = 0.0, 0
    for eje in sorted(ejes_usados) + ["nacional"]:
        m = nueva.marginal(eje)
        for k in (_orden(par, eje) if eje != "nacional" else (NAC,)):
            base = f"{P}-M24-{_slug(eje)}-{_slug(k)}"
            v = m.get(k)
            out[f"{base}-N"] = 0 if v is None else int(v["n"])
            out[f"{base}-P-REDERIVADO"] = None if v is None else _f(v["p"])
            out[f"{base}-MASA-REDERIVADA"] = None if v is None else _f(v["W"])
            ps = sellados["p"].get(eje, {}).get(k)
            out[f"{base}-P-SELLADO"] = _f(ps)
            d = None if (v is None or v["p"] is None or ps is None) else float(v["p"]) - float(ps)
            out[f"{base}-DELTA-SELLADO"] = _f(d)
            if d is not None:
                peor = max(peor, abs(d))
                n_cmp += 1
    out[f"{P}-G-M24-DELTA-SELLADO-MAX"] = peor
    out[f"{P}-G-M24-N-COTEJADOS"] = n_cmp
    out[f"{P}-G-M24-ORIGEN-SELLADO"] = str(sellados["origen"].get("puntos"))


def _emite_marginales_anterior(out, P, ant: OlaCargada, par, ejes_usados):
    for eje in sorted(ejes_usados) + ["nacional"]:
        m = ant.marginal(eje)
        for k in (_orden(par, eje) if eje != "nacional" else (NAC,)):
            base = f"{P}-M21-{_slug(eje)}-{_slug(k)}"
            v = m.get(k)
            if v is None:
                out[f"{base}-P"] = None
                out[f"{base}-IC95INF"] = None
                out[f"{base}-IC95SUP"] = None
                out[f"{base}-N"] = 0
            else:
                _emite_celda(out, base, _celda(v), con_n=True)


def _emite_familia(out, P, nombre, par, fam, umbral):
    meta = fam["meta"]
    out[f"{P}-{_slug(nombre)}-C2-ESTADO"] = str(meta["c2_estado"])
    out[f"{P}-{_slug(nombre)}-LAMBDA"] = float(meta["lambda"])
    r3 = meta["r3"] or {}
    out[f"{P}-{_slug(nombre)}-R3-ESTADO"] = str(r3.get("estado", "CONSTRUIDO" if r3 else "NO-EMITIBLE"))
    out[f"{P}-{_slug(nombre)}-R3-ITERACIONES-PUNTO"] = int(r3.get("iteraciones_punto", 0))
    out[f"{P}-{_slug(nombre)}-R3-CONVERGIO-PUNTO"] = _sino(r3.get("convergio_punto"))
    out[f"{P}-{_slug(nombre)}-R3-REPS-NO-CONVERGEN"] = int(r3.get("reps_no_convergen", 0))
    for cid in CANDIDATOS:
        celdas = fam["candidatos"][cid]
        out[f"{P}-{_slug(nombre)}-{cid}-REPLICAS-SIN-DEFINIR"] = _sin_definir(celdas)
        for key in _celdas_par(par, nombre):
            _emite_celda(out, _cid(P, nombre, cid, *key), celdas[key], con_n=(cid == "P2"))
    for key in _celdas_par(par, nombre):
        ib = None if meta["ibar"] is None else meta["ibar"][key][0]
        out[f"{_cid(P, nombre, 'IBAR', *key)}"] = _f(ib)
        n21 = meta["n21"][key]
        out[f"{_cid(P, nombre, 'N21', *key)}"] = int(n21)
        out[f"{_cid(P, nombre, 'SOPORTE-2021', *key)}"] = "SI" if n21 >= umbral else "NO"


def _control(out, P, ctrl: dict, inputs) -> None:
    """Coteja P/IC/N emitidos contra un sellado que el contrato cita por id.
    `celdas`: {"par|ka|kb": {"<CID>-<CAMPO>": id}}; tolerancia del contrato."""
    doc = _lee_json_resultados(inputs, ctrl["input"])
    tol = float(ctrl["tol"])
    peor, n, faltan = 0.0, 0, 0
    for llave, campos in ctrl["celdas"].items():
        nombre, ka, kb = llave.split("|")
        for campo, rid in campos.items():
            cid, _, atributo = campo.partition("-")
            base = _cid(P, nombre, cid, ka, kb)
            mio = out.get(f"{base}-{atributo}")
            suyo = doc.get(rid)
            d = None if (mio is None or suyo is None) else float(mio) - float(suyo)
            out[f"{P}-CTRL-{_slug(nombre)}-{cid}-{_slug(ka)}-X-{_slug(kb)}-{atributo}-DELTA"] = _f(d)
            if d is None:
                faltan += 1
            else:
                peor = max(peor, abs(d))
                n += 1
    out[f"{P}-G-CTRL-DELTA-MAX"] = peor
    out[f"{P}-G-CTRL-N-COTEJADOS"] = n
    out[f"{P}-G-CTRL-N-NO-COTEJABLES"] = faltan
    ok = n > 0
    ok = ok and faltan == 0
    ok = ok and peor <= tol
    out[f"{P}-G-CTRL-REPRODUCE"] = "SI" if ok else "NO"
    out[f"{P}-G-CTRL-TOL"] = tol


def _emisiones_core(inputs, par, reservada_nueva: bool, autorizados_nueva):
    """Lo que emisiones y adjudicación comparten: olas, marginales, familia
    por par. Devuelve (olas, sellados, {par: familia})."""
    olas = _carga_olas(inputs, par, reservada_nueva, autorizados_nueva)
    nueva, ant = olas[str(par["ola_nueva"])], olas[str(par["ola_anterior"])]
    sellados = _sellados(inputs, par)
    fam = {nombre: _familia_par(nombre, par, nueva, ant, sellados) for nombre in par["pares"]}
    return olas, sellados, fam


def emisiones(inputs, contrato) -> dict:
    par = contrato["parametros"]
    P = str(par["prefijo_result"])
    umbral = int(par["umbral_soporte_n"])
    out = {}
    _emite_cabecera(out, P, inputs, par)
    olas, sellados, fam = _emisiones_core(inputs, par, reservada_nueva=True, autorizados_nueva=[])
    nueva, ant = olas[str(par["ola_nueva"])], olas[str(par["ola_anterior"])]
    for rot, oc in olas.items():
        _emite_conteos(out, P, f"W{rot}", oc)
    # ── la guardia se PRUEBA en cada corrida ─────────────────────────────
    out[f"{P}-G-RESERVA-OLA-NUEVA-CARGADA-RESERVADA"] = "SI" if nueva.ola.reservada else "NO -- DEFECTO"
    primero = next(iter(par["pares"].values()))
    try:
        nueva.cruce(primero["a"], primero["b"])
        out[f"{P}-G-RESERVA-CRUCE-OLA-NUEVA-DERIVADO"] = "SI -- DEFECTO"
        out[f"{P}-G-RESERVA-GUARDIA-PROBADA"] = "NO-LANZO -- DEFECTO"
    except ReservaRota as exc:
        out[f"{P}-G-RESERVA-CRUCE-OLA-NUEVA-DERIVADO"] = "NO"
        out[f"{P}-G-RESERVA-GUARDIA-PROBADA"] = f"ReservaRota: {exc}"
    ejes_usados = {p["a"] for p in par["pares"].values()} | {p["b"] for p in par["pares"].values()}
    _emite_marginales_nueva(out, P, nueva, par, sellados, ejes_usados)
    _emite_marginales_anterior(out, P, ant, par, ejes_usados)
    for nombre in par["pares"]:
        _emite_familia(out, P, nombre, par, fam[nombre], umbral)
    out[f"{P}-G-M-ESTADO"] = str(par["m_estado"])
    out[f"{P}-G-L-ESTADO"] = str(par["l_estado"])
    out[f"{P}-G-LAMBDA-R2"] = float(par["lambda_r2"])
    out[f"{P}-G-R-EXISTE-EN-ESTE-COMMIT"] = "NO"
    if par.get("control_sellado"):
        _control(out, P, par["control_sellado"], inputs)
    return out


# ══ adjudicación ═══════════════════════════════════════════════════════════

def _reproduce_emisiones(out, P, PE, em_res, par, fam, tol) -> None:
    peor = 0.0
    for nombre in par["pares"]:
        for cid in CANDIDATOS:
            for key in _celdas_par(par, nombre):
                v = fam[nombre]["candidatos"][cid][key].p
                s = em_res.get(f"{_cid(PE, nombre, cid, *key)}-P")
                if v is None and s is None:
                    continue
                if v is None or s is None:
                    peor = float("inf")
                    continue
                peor = max(peor, abs(float(v) - float(s)))
    out[f"{P}-G-EMISIONES-DELTA-P-MAX"] = peor if math.isfinite(peor) else None
    ok = math.isfinite(peor) and peor <= tol
    out[f"{P}-G-EMISIONES-REPRODUCIDAS"] = "SI" if ok else "NO"
    if not ok:
        raise RuntimeError(f"PARO: las emisiones selladas no se reproducen (delta max {peor}); no se abre R")


def _adjudica_bloque(out, P, rotulo, R: dict, cand: dict, punt: dict, par, con_piso: bool):
    """Adjudica un bloque de celdas (un par, o un grupo de pares pooled) con
    la regla v0.3 e imprime MAE/ΔMAE/IC/veredicto/rol/cobertura por candidato."""
    B = f"{P}-{rotulo}"
    n_p = sum(1 for v in punt.values() if v)
    out[f"{B}-CELDAS-PUNTUADAS"] = int(n_p)
    if not con_piso:
        adj = cf.adjudica(R, {"P2": cand["P2"]}, punt, piso="P2", retador="P2",
                          umbral_vence_pp=float(par["umbral_vence_pp"]),
                          umbral_reserva_pp=float(par["umbral_reserva_pp"]))
    else:
        adj = cf.adjudica(R, cand, punt, piso=PISO, retador=RETADOR_PRIMARIO,
                          umbral_vence_pp=float(par["umbral_vence_pp"]),
                          umbral_reserva_pp=float(par["umbral_reserva_pp"]))
    for cid in CANDIDATOS:
        c = adj["candidatos"].get(cid)
        if c is None:
            out[f"{B}-{cid}-MAE-PP"] = None
            out[f"{B}-{cid}-DELTA-MAE-PP"] = None
            out[f"{B}-{cid}-DELTA-IC95INF"] = None
            out[f"{B}-{cid}-DELTA-IC95SUP"] = None
            out[f"{B}-{cid}-VEREDICTO"] = "NO-ADJUDICABLE-SIN-PISO"
            out[f"{B}-{cid}-ROL"] = "PISO" if cid == PISO else ("PRIMARIA" if cid == RETADOR_PRIMARIO else "SECUNDARIA")
            out[f"{B}-{cid}-COBERTURA-R-EN-IC-CAND-N"] = 0
            out[f"{B}-{cid}-COBERTURA-R-EN-IC-CAND-FRAC"] = None
            out[f"{B}-{cid}-COBERTURA-CAND-EN-IC-R-FRAC"] = None
            continue
        out[f"{B}-{cid}-MAE-PP"] = _f(c["mae_pp"])
        out[f"{B}-{cid}-DELTA-MAE-PP"] = _f(c["delta_mae_pp"])
        out[f"{B}-{cid}-DELTA-IC95INF"] = None if c["delta_ic95"] is None else _f(c["delta_ic95"][0])
        out[f"{B}-{cid}-DELTA-IC95SUP"] = None if c["delta_ic95"] is None else _f(c["delta_ic95"][1])
        out[f"{B}-{cid}-VEREDICTO"] = "PISO" if (con_piso and cid == PISO) else (
            "SIN-PISO-SOLO-COBERTURA" if not con_piso else str(c["veredicto"]))
        out[f"{B}-{cid}-ROL"] = "PISO" if cid == PISO else ("PRIMARIA" if cid == RETADOR_PRIMARIO else "SECUNDARIA")
        cob = lf.cobertura_par(c["celdas"])
        out[f"{B}-{cid}-COBERTURA-R-EN-IC-CAND-N"] = int(cob["R_en_ic_cand"]["n"])
        out[f"{B}-{cid}-COBERTURA-R-EN-IC-CAND-FRAC"] = _f(cob["R_en_ic_cand"]["frac"])
        out[f"{B}-{cid}-COBERTURA-CAND-EN-IC-R-FRAC"] = _f(cob["cand_en_ic_R"]["frac"])
    if con_piso:
        tc = lf.conteo_tres_cuartos(adj, PISO, RETADOR_PRIMARIO)
        out[f"{B}-TRES-CUARTOS-N"] = int(tc["n"])
        out[f"{B}-TRES-CUARTOS-GANA-R2"] = int(tc["gana_retador"])
        out[f"{B}-TRES-CUARTOS-FRAC"] = _f(tc["frac"])
        out[f"{B}-VEREDICTO-PRIMARIO"] = str(adj["candidatos"][RETADOR_PRIMARIO]["veredicto"])
    else:
        out[f"{B}-TRES-CUARTOS-N"] = 0
        out[f"{B}-TRES-CUARTOS-GANA-R2"] = 0
        out[f"{B}-TRES-CUARTOS-FRAC"] = None
        out[f"{B}-VEREDICTO-PRIMARIO"] = "NO-ADJUDICABLE-SIN-PISO"
    return adj


def adjudicacion(inputs, contrato) -> dict:
    par = contrato["parametros"]
    P = str(par["prefijo_result"])
    PE = str(par["prefijo_emisiones"])
    umbral = int(par["umbral_soporte_n"])
    out = {}
    _emite_cabecera(out, P, inputs, par)
    em = json.loads(_bytes(inputs, "emisiones_selladas").decode("utf-8"))
    em_res = em["resultados"]
    out[f"{P}-G-EMISIONES-SPEC-ID"] = str(em.get("spec_id"))
    out[f"{P}-G-EMISIONES-RESERVA-CRUCE-DERIVADO"] = str(em_res.get(f"{PE}-G-RESERVA-CRUCE-OLA-NUEVA-DERIVADO"))
    out[f"{P}-G-EMISIONES-R-EXISTIA"] = str(em_res.get(f"{PE}-G-R-EXISTE-EN-ESTE-COMMIT"))
    autorizados = [tuple(x) for x in par["pares_cruce_autorizados_2024"]]
    olas, sellados, fam = _emisiones_core(inputs, par, reservada_nueva=False, autorizados_nueva=autorizados)
    nueva = olas[str(par["ola_nueva"])]
    out[f"{P}-G-OLA-NUEVA-ABIERTA"] = "SI" if not nueva.ola.reservada else "NO -- DEFECTO"
    out[f"{P}-G-PARES-AUTORIZADOS"] = ",".join(f"{a}x{b}" for a, b in autorizados) or "NINGUNO"
    _reproduce_emisiones(out, P, PE, em_res, par, fam, float(par["tol_reproduccion_emisiones"]))
    veto = par.get("par_vetado_probar")
    if veto:
        try:
            nueva.cruce(veto["a"], veto["b"])
            out[f"{P}-G-VETO-PROBADO"] = "NO-LANZO -- DEFECTO"
        except ReservaRota as exc:
            out[f"{P}-G-VETO-PROBADO"] = f"ReservaRota: {exc}"

    R_todo, cand_todo, punt_todo, grupo_de = {}, {c: {} for c in CANDIDATOS}, {}, {}
    vered_par, cob_c2_par, ejes_par = {}, {}, {}
    for nombre, p in par["pares"].items():
        ea, eb = p["a"], p["b"]
        cods = _celdas_par(par, nombre)
        con_piso = str(p["c2"]) == "EMITIBLE"
        try:
            R, _crudo = _rejilla_abierta(nueva, par, ea, eb)
        except ReservaRota as exc:
            out[f"{P}-G-{_slug(nombre)}-ESTADO"] = f"NO-ADJUDICABLE-VETO: {exc}"
            for key in cods:
                b = _cid(P, nombre, "R", *key)
                for s in ("P", "IC95INF", "IC95SUP", "EE"):
                    out[f"{b}-{s}"] = None
                out[f"{b}-N"] = 0
                out[f"{_cid(P, nombre, 'PUNTUADA', *key)}"] = "NO-ADJUDICABLE"
                for cid in CANDIDATOS:
                    out[f"{_cid(P, nombre, cid + '-ERROR-PP', *key)}"] = None
                    out[f"{_cid(P, nombre, cid + '-DENTRO-IC-R', *key)}"] = "NO-ADJUDICABLE"
                    out[f"{_cid(P, nombre, cid + '-R-DENTRO-IC-CAND', *key)}"] = "NO-ADJUDICABLE"
            _adjudica_bloque(out, P, _slug(nombre), {k: cf.Celda(p=None) for k in cods},
                             fam[nombre]["candidatos"], {k: False for k in cods}, par, con_piso)
            out[f"{P}-{_slug(nombre)}-VEREDICTO-PRIMARIO"] = "NO-ADJUDICABLE"
            continue
        out[f"{P}-G-{_slug(nombre)}-ESTADO"] = "ADJUDICADO" if con_piso else "SIN-PISO-SOLO-P2"
        n_hist = {str(par["ola_anterior"]): fam[nombre]["meta"]["n21"],
                  str(par["ola_nueva"]): {k: c.n for k, c in R.items()}}
        punt = cf.puntuadas(n_hist, umbral)
        cand = fam[nombre]["candidatos"]
        adj = _adjudica_bloque(out, P, _slug(nombre), R, cand, punt, par, con_piso)
        for key in cods:
            r = R[key]
            b = _cid(P, nombre, "R", *key)
            _emite_celda(out, b, r, con_n=True)
            ic = _ic(r)
            out[f"{b}-EE"] = None if ic is None else _f((ic[1] - ic[0]) / 3.92)
            out[f"{_cid(P, nombre, 'PUNTUADA', *key)}"] = "SI" if punt[key] else "NO"
            for cid in CANDIDATOS:
                c = adj["candidatos"].get(cid)
                f_ = None if c is None else c["celdas"][key]
                out[f"{_cid(P, nombre, cid + '-ERROR-PP', *key)}"] = None if f_ is None else _f(f_["error_pp"])
                out[f"{_cid(P, nombre, cid + '-DENTRO-IC-R', *key)}"] = "NO-ADJUDICABLE" if f_ is None else _sino(f_["dentro_ic_R"])
                out[f"{_cid(P, nombre, cid + '-R-DENTRO-IC-CAND', *key)}"] = "NO-ADJUDICABLE" if f_ is None else _sino(f_["R_dentro_ic_cand"])
        grupo = str(p["grupo"])
        for key in cods:
            gk = (nombre,) + key
            R_todo[gk] = R[key]
            punt_todo[gk] = punt[key]
            grupo_de[gk] = grupo
            for cid in CANDIDATOS:
                cand_todo[cid][gk] = cand[cid][key]
        vered_par[nombre] = out[f"{P}-{_slug(nombre)}-VEREDICTO-PRIMARIO"]
        ejes_par[nombre] = (ea, eb)
        if con_piso:
            cob_c2_par[nombre] = {"frac": out[f"{P}-{_slug(nombre)}-C2-COBERTURA-R-EN-IC-CAND-FRAC"]}

    # ── bloques agregados: primaria (5 pares), formalidad, cuenta_formal ──
    grupos = sorted({str(p["grupo"]) for p in par["pares"].values()})
    for g in grupos:
        keys = [k for k, gg in grupo_de.items() if gg == g]
        R_g = {k: R_todo[k] for k in keys}
        punt_g = {k: punt_todo[k] for k in keys}
        cand_g = {cid: {k: cand_todo[cid][k] for k in keys} for cid in CANDIDATOS}
        con_piso = all(str(par["pares"][k[0]]["c2"]) == "EMITIBLE" for k in keys) and bool(keys)
        out[f"{P}-G-{_slug(g)}-N-CELDAS"] = len(keys)
        out[f"{P}-G-{_slug(g)}-SIN-SOPORTE-FRAC"] = _f(
            (sum(1 for k in keys if not punt_g[k]) / len(keys)) if keys else None)
        _adjudica_bloque(out, P, f"G-{_slug(g)}", R_g, cand_g, punt_g, par, con_piso)
    prim = str(par["grupo_primario"])
    v_prim = out.get(f"{P}-G-{_slug(prim)}-VEREDICTO-PRIMARIO", "NO-ADJUDICABLE")
    lectura = lf.bbis_lectura(v_prim, out.get(f"{P}-G-{_slug(prim)}-SIN-SOPORTE-FRAC"),
                              {k: v for k, v in cob_c2_par.items() if str(par["pares"][k]["grupo"]) == prim},
                              {k: v for k, v in vered_par.items() if str(par["pares"][k]["grupo"]) == prim},
                              ejes_par)
    out[f"{P}-G-BBIS-FILA"] = str(lectura["fila"])
    out[f"{P}-G-BBIS-RAZON"] = str(lectura["razon"])
    out[f"{P}-G-BBIS-ADJUDICA-SOLO"] = "NO -- lectura mecánica del §10; la lee mesa"
    out[f"{P}-G-REGLA"] = str(par["regla_v0_3"])
    if par.get("control_sellado_R"):
        _control(out, P, par["control_sellado_R"], inputs)
    return out


# ══ oro (ii): reproducir el C2 con IC ya sellado, réplica a réplica ═══════

def oro_c2ic(inputs, contrato) -> dict:
    """Sólo C2 (punto sellado + IC réplica a réplica) sobre los pares EMITIBLE
    del contrato, bajo el régimen del C2-IC, cotejado contra su sello. No
    emite P2/R1/R2/R3 ni abre 2021: no es un COMMIT-2 con otro nombre."""
    par = contrato["parametros"]
    P = str(par["prefijo_result"])
    out = {}
    _emite_cabecera(out, P, inputs, par)
    olas = _carga_olas(inputs, par, reservada_nueva=True, autorizados_nueva=[])
    nueva = olas[str(par["ola_nueva"])]
    _emite_conteos(out, P, f"W{nueva.rotulo}", nueva)
    out[f"{P}-G-RESERVA-OLA-NUEVA-CARGADA-RESERVADA"] = "SI" if nueva.ola.reservada else "NO -- DEFECTO"
    primero = next(iter(par["pares"].values()))
    try:
        nueva.cruce(primero["a"], primero["b"])
        out[f"{P}-G-RESERVA-GUARDIA-PROBADA"] = "NO-LANZO -- DEFECTO"
    except ReservaRota as exc:
        out[f"{P}-G-RESERVA-GUARDIA-PROBADA"] = f"ReservaRota: {exc}"
    sellados = _sellados(inputs, par)
    ejes_usados = {p["a"] for p in par["pares"].values()} | {p["b"] for p in par["pares"].values()}
    _emite_marginales_nueva(out, P, nueva, par, sellados, ejes_usados)
    doc = _lee_json_resultados(inputs, par["oro_c2ic"]["input"])
    ids = par["oro_c2ic"]["ids"]
    umbral_validas = int(par["oro_c2ic"]["umbral_replicas_validas"])
    peor_p, peor_ic, n_cel, n_ic = 0.0, 0.0, 0, 0
    for nombre, p in par["pares"].items():
        if str(p["c2"]) != "EMITIBLE":
            continue
        m_t = _marginales_ola(nueva, par, p["a"], p["b"], sellados=sellados)
        c2 = cf.c2(m_t)
        for key in _celdas_par(par, nombre):
            c = c2[key]
            base = _cid(P, nombre, "C2", *key)
            validas = 0 if c.replicas is None else int(np.isfinite(c.replicas).sum())
            out[f"{base}-P"] = _f(c.p)
            ic = _ic(c) if validas >= umbral_validas else None
            out[f"{base}-IC95INF"] = None if ic is None else _f(ic[0])
            out[f"{base}-IC95SUP"] = None if ic is None else _f(ic[1])
            out[f"{base}-REPLICAS-VALIDAS"] = validas
            ref = ids.get(f"{nombre}|{key[0]}|{key[1]}", {})
            sp = doc.get(ref.get("P", ""))
            slo, shi = doc.get(ref.get("IC95INF", "")), doc.get(ref.get("IC95SUP", ""))
            sv = doc.get(ref.get("REPLICAS-VALIDAS", ""))
            out[f"{base}-P-SELLADO"] = _f(sp)
            dp = None if (c.p is None or sp is None) else float(c.p) - float(sp)
            out[f"{base}-DELTA-P"] = _f(dp)
            dlo = None if (ic is None or slo is None) else float(ic[0]) - float(slo)
            dhi = None if (ic is None or shi is None) else float(ic[1]) - float(shi)
            out[f"{base}-DELTA-IC95INF"] = _f(dlo)
            out[f"{base}-DELTA-IC95SUP"] = _f(dhi)
            out[f"{base}-REPLICAS-VALIDAS-SELLADO"] = None if sv is None else int(sv)
            n_cel += 1
            if dp is not None:
                peor_p = max(peor_p, abs(dp))
            if dlo is not None and dhi is not None:
                peor_ic = max(peor_ic, abs(dlo), abs(dhi))
                n_ic += 1
    out[f"{P}-G-ORO-N-CELDAS"] = n_cel
    out[f"{P}-G-ORO-N-CELDAS-CON-IC-COTEJADO"] = n_ic
    out[f"{P}-G-ORO-DELTA-P-MAX"] = peor_p
    out[f"{P}-G-ORO-DELTA-IC-MAX"] = peor_ic
    tol_ic, tol_p = float(par["oro_c2ic"]["tol_ic"]), float(par["oro_c2ic"]["tol_p"])
    ok_ic = n_ic == n_cel
    ok_ic = ok_ic and n_cel > 0
    ok_ic = ok_ic and peor_ic <= tol_ic
    ok_p = n_cel > 0
    ok_p = ok_p and peor_p <= tol_p
    out[f"{P}-G-ORO-REPRODUCE-IC"] = "SI" if ok_ic else "NO"
    out[f"{P}-G-ORO-REPRODUCE-P"] = "SI" if ok_p else "NO"
    out[f"{P}-G-ORO-TOL-IC"] = tol_ic
    out[f"{P}-G-ORO-TOL-P"] = tol_p
    out[f"{P}-G-ORO-CAUSA-DELTA-P"] = str(par["oro_c2ic"]["causa_delta_p"])
    return out


# ══ catálogo de RESULT: la spec lo declara, el runner lo coteja ════════════

def catalogo_resultados(par: dict, input_ids: list) -> list:
    """Todos los RESULT que `medir()` emite para este contrato, con tipo,
    unidad y `permite_no_estimable` donde el código puede emitir null -- la
    misma enumeración que recorre el punto de entrada."""
    cat = []
    seen = set()

    def add(rid, tipo, unidad, nulo=False):
        if rid in seen:
            return
        seen.add(rid)
        e = {"id": rid, "tipo": tipo, "unidad": unidad}
        if nulo:
            e["permite_no_estimable"] = True
        cat.append(e)

    P = str(par["prefijo_result"])
    pe = str(par["punto_de_entrada"])
    for iid in input_ids:
        add(f"{P}-G-INPUT-{_slug(iid)}-SHA256", "texto", f"sha256 del input {iid}")
    for k in MODULOS_SHA:
        add(f"{P}-G-CODIGO-{k}-SHA256", "texto", f"sha256 del módulo {k} al correr")
    add(f"{P}-G-OLA-NUEVA", "texto", "ola nueva del contrato")
    add(f"{P}-G-REGIMEN-UNIVERSO", "texto", "régimen de universo (PILOTO-1 | ARBITRO-2024)")
    add(f"{P}-G-GUARDIA-AST-VIOLACIONES", "entero", "violaciones de auditoria_ast()")
    add(f"{P}-G-GUARDIA-AST", "texto", "PASA si auditoria_ast() no reporta violaciones")

    def conteos(w):
        add(f"{P}-G-{w}-FILAS-ARCHIVO", "entero", "filas del miembro TMODULO")
        add(f"{P}-G-{w}-FILAS-UNIVERSO", "entero", "filas tras los filtros del régimen")
        add(f"{P}-G-{w}-FILAS-EDAD-CENTINELA", "entero", "filas con edad centinela (98/99)")
        add(f"{P}-G-{w}-FILAS-CODIGO-FUERA-DE-DOMINIO", "entero", "filas del universo con algún código fuera de {1,2,blanco}")
        add(f"{P}-G-{w}-ESTRATOS", "entero", "EST_DIS distintos")
        add(f"{P}-G-{w}-UPM", "entero", "UPM distintas (EST_DIS, UPM_DIS)")
        add(f"{P}-G-{w}-ESTRATOS-UPM-UNICA", "entero", "estratos con una sola UPM (no remuestrean)")
        add(f"{P}-G-{w}-ENCODING", "texto", "codificación con que se leyó el miembro")
        add(f"{P}-G-{w}-CATALOGO-ESCOLARIDAD", "texto", "COINCIDE si el catálogo del zip iguala al declarado; SIN-CATALOGO-EN-ZIP si no viaja")
        for e in EJES:
            add(f"{P}-G-{w}-FUERA-{_slug(e)}", "entero", f"filas del universo (fuera) en el eje {e}")

    def marginales_nueva(ejes_usados):
        for eje in sorted(ejes_usados) + ["nacional"]:
            for k in (_orden(par, eje) if eje != "nacional" else (NAC,)):
                base = f"{P}-M24-{_slug(eje)}-{_slug(k)}"
                add(f"{base}-N", "entero", "personas en la categoría (ola nueva)")
                add(f"{base}-P-REDERIVADO", "proporcion", "marginal re-derivado de UN eje (réplica base)", True)
                add(f"{base}-MASA-REDERIVADA", "flotante", "masa ponderada re-derivada", True)
                add(f"{base}-P-SELLADO", "proporcion", "marginal SELLADO citado por el contrato", True)
                add(f"{base}-DELTA-SELLADO", "flotante", "re-derivado - sellado", True)
        add(f"{P}-G-M24-DELTA-SELLADO-MAX", "flotante", "peor |re-derivado - sellado| (informativo: régimen vs árbitro)")
        add(f"{P}-G-M24-N-COTEJADOS", "entero", "marginales cotejados contra el sellado")
        add(f"{P}-G-M24-ORIGEN-SELLADO", "texto", "input del que salen los puntos sellados")

    ejes_usados = {p["a"] for p in par["pares"].values()} | {p["b"] for p in par["pares"].values()}
    if pe == "emisiones":
        for rot in sorted(par["olas_zip"]):
            conteos(f"W{rot}")
        add(f"{P}-G-RESERVA-OLA-NUEVA-CARGADA-RESERVADA", "texto", "SI si la ola nueva se cargó reservada")
        add(f"{P}-G-RESERVA-CRUCE-OLA-NUEVA-DERIVADO", "texto", "NO si cruce() sobre la ola nueva lanzó")
        add(f"{P}-G-RESERVA-GUARDIA-PROBADA", "texto", "la excepción de la guardia, probada en esta corrida")
        marginales_nueva(ejes_usados)
        for eje in sorted(ejes_usados) + ["nacional"]:
            for k in (_orden(par, eje) if eje != "nacional" else (NAC,)):
                base = f"{P}-M21-{_slug(eje)}-{_slug(k)}"
                add(f"{base}-P", "proporcion", "marginal de la ola anterior", True)
                add(f"{base}-IC95INF", "proporcion", "percentil 2.5 bootstrap", True)
                add(f"{base}-IC95SUP", "proporcion", "percentil 97.5 bootstrap", True)
                add(f"{base}-N", "entero", "personas en la categoría (ola anterior)")
        for nombre in par["pares"]:
            S = _slug(nombre)
            add(f"{P}-{S}-C2-ESTADO", "texto", "EMITIBLE o NO-EMITIBLE:<causa> (dictamen sellado)")
            add(f"{P}-{S}-LAMBDA", "flotante", "lambda de R2 (fija)")
            add(f"{P}-{S}-R3-ESTADO", "texto", "CONSTRUIDO | NO-EMITIBLE | NO-CONSTRUIBLE:<causa>")
            add(f"{P}-{S}-R3-ITERACIONES-PUNTO", "entero", "iteraciones del raking del punto")
            add(f"{P}-{S}-R3-CONVERGIO-PUNTO", "texto", "SI si el raking del punto llegó a la tolerancia")
            add(f"{P}-{S}-R3-REPS-NO-CONVERGEN", "entero", "réplicas cuyo raking no convergió (quedan SIN-DEFINIR)")
            for cid in CANDIDATOS:
                add(f"{P}-{S}-{cid}-REPLICAS-SIN-DEFINIR", "entero", "réplicas NaN sumadas sobre celdas")
                for key in _celdas_par(par, nombre):
                    b = _cid(P, nombre, cid, *key)
                    add(f"{b}-P", "proporcion", f"{ROTULO[cid]}: punto", True)
                    add(f"{b}-IC95INF", "proporcion", "percentil 2.5 de las réplicas definidas", True)
                    add(f"{b}-IC95SUP", "proporcion", "percentil 97.5 de las réplicas definidas", True)
                    if cid == "P2":
                        add(f"{b}-N", "entero", "personas en la celda de la ola anterior")
            for key in _celdas_par(par, nombre):
                add(_cid(P, nombre, "IBAR", *key), "flotante", "delta_21 en logit (interacción 2021)", True)
                add(_cid(P, nombre, "N21", *key), "entero", "n de la celda en 2021")
                add(_cid(P, nombre, "SOPORTE-2021", *key), "texto", "SI si n21 >= umbral")
        add(f"{P}-G-M-ESTADO", "texto", "M: NO-DERIVABLE con su razón (firma F2)")
        add(f"{P}-G-L-ESTADO", "texto", "L1/L2: estado en esta corrida")
        add(f"{P}-G-LAMBDA-R2", "flotante", "lambda fija de R2")
        add(f"{P}-G-R-EXISTE-EN-ESTE-COMMIT", "texto", "NO: ningún R del lote existe al sellar")
        if par.get("control_sellado"):
            for llave, campos in par["control_sellado"]["celdas"].items():
                nombre, ka, kb = llave.split("|")
                for campo in campos:
                    cid, _, atributo = campo.partition("-")
                    add(f"{P}-CTRL-{_slug(nombre)}-{cid}-{_slug(ka)}-X-{_slug(kb)}-{atributo}-DELTA",
                        "flotante", "emitido - sellado del piloto 1", True)
            _cat_control(add, P)
    elif pe == "adjudicacion":
        add(f"{P}-G-EMISIONES-SPEC-ID", "texto", "spec_id de las emisiones selladas")
        add(f"{P}-G-EMISIONES-RESERVA-CRUCE-DERIVADO", "texto", "lo que las emisiones declararon sobre la reserva")
        add(f"{P}-G-EMISIONES-R-EXISTIA", "texto", "lo que las emisiones declararon sobre R")
        add(f"{P}-G-OLA-NUEVA-ABIERTA", "texto", "SI: en este commit la ola nueva se abre")
        add(f"{P}-G-PARES-AUTORIZADOS", "texto", "pares que el contrato autoriza a cruzar en la ola nueva")
        add(f"{P}-G-EMISIONES-DELTA-P-MAX", "flotante", "peor |emisión re-derivada - sellada|", True)
        add(f"{P}-G-EMISIONES-REPRODUCIDAS", "texto", "SI o PARO antes de abrir R")
        if par.get("par_vetado_probar"):
            add(f"{P}-G-VETO-PROBADO", "texto", "la excepción sobre el par vetado, probada")
        for nombre in par["pares"]:
            S = _slug(nombre)
            add(f"{P}-G-{S}-ESTADO", "texto", "ADJUDICADO | SIN-PISO-SOLO-P2 | NO-ADJUDICABLE-VETO")
            for key in _celdas_par(par, nombre):
                b = _cid(P, nombre, "R", *key)
                add(f"{b}-P", "proporcion", "árbitro R del cruce en la ola nueva", True)
                add(f"{b}-IC95INF", "proporcion", "percentil 2.5 bootstrap", True)
                add(f"{b}-IC95SUP", "proporcion", "percentil 97.5 bootstrap", True)
                add(f"{b}-N", "entero", "personas en la celda (ola nueva)")
                add(f"{b}-EE", "flotante", "(IC95SUP - IC95INF)/3.92", True)
                add(_cid(P, nombre, "PUNTUADA", *key), "texto", "SI si n >= umbral en las dos olas")
                for cid in CANDIDATOS:
                    add(_cid(P, nombre, cid + "-ERROR-PP", *key), "flotante", "100*|cand - R|", True)
                    add(_cid(P, nombre, cid + "-DENTRO-IC-R", *key), "texto", "candidato dentro del IC95 de R")
                    add(_cid(P, nombre, cid + "-R-DENTRO-IC-CAND", *key), "texto", "R dentro del IC95 del candidato")
            _cat_bloque(add, P, S)
        for g in sorted({str(p["grupo"]) for p in par["pares"].values()}):
            add(f"{P}-G-{_slug(g)}-N-CELDAS", "entero", "celdas del grupo")
            add(f"{P}-G-{_slug(g)}-SIN-SOPORTE-FRAC", "proporcion", "fracción de celdas sin soporte", True)
            _cat_bloque(add, P, f"G-{_slug(g)}")
        add(f"{P}-G-BBIS-FILA", "texto", "lectura mecánica del §10 (CORROBORADA | ACOTADA | FALSADOR-DEBIL | NO-CAE-EN-NINGUNA-FILA)")
        add(f"{P}-G-BBIS-RAZON", "texto", "por qué")
        add(f"{P}-G-BBIS-ADJUDICA-SOLO", "texto", "NO")
        add(f"{P}-G-REGLA", "texto", "regla v0.3 verbatim")
        if par.get("control_sellado_R"):
            for llave, campos in par["control_sellado_R"]["celdas"].items():
                nombre, ka, kb = llave.split("|")
                for campo in campos:
                    cid, _, atributo = campo.partition("-")
                    add(f"{P}-CTRL-{_slug(nombre)}-{cid}-{_slug(ka)}-X-{_slug(kb)}-{atributo}-DELTA",
                        "flotante", "R emitido - R sellado del piloto 1", True)
            _cat_control(add, P)
    elif pe == "oro_c2ic":
        conteos(f"W{par['ola_nueva']}")
        add(f"{P}-G-RESERVA-OLA-NUEVA-CARGADA-RESERVADA", "texto", "SI si la ola nueva se cargó reservada")
        add(f"{P}-G-RESERVA-GUARDIA-PROBADA", "texto", "la excepción de la guardia, probada")
        marginales_nueva(ejes_usados)
        for nombre, p in par["pares"].items():
            if str(p["c2"]) != "EMITIBLE":
                continue
            for key in _celdas_par(par, nombre):
                base = _cid(P, nombre, "C2", *key)
                add(f"{base}-P", "proporcion", "C2 sobre marginales SELLADOS (#971, precisión completa)", True)
                add(f"{base}-IC95INF", "proporcion", "percentil 2.5 de C2_k", True)
                add(f"{base}-IC95SUP", "proporcion", "percentil 97.5 de C2_k", True)
                add(f"{base}-REPLICAS-VALIDAS", "entero", "réplicas con los tres marginales en (0,1)")
                add(f"{base}-P-SELLADO", "proporcion", "C2 punto del CALC-C2-COMPUESTO-IC-ENIF2024-0001", True)
                add(f"{base}-DELTA-P", "flotante", "punto propio - sellado (redondeo a 6 decimales del yaml)", True)
                add(f"{base}-DELTA-IC95INF", "flotante", "IC95INF propio - sellado", True)
                add(f"{base}-DELTA-IC95SUP", "flotante", "IC95SUP propio - sellado", True)
                add(f"{base}-REPLICAS-VALIDAS-SELLADO", "entero", "réplicas válidas del sellado", True)
        add(f"{P}-G-ORO-N-CELDAS", "entero", "celdas cotejadas")
        add(f"{P}-G-ORO-N-CELDAS-CON-IC-COTEJADO", "entero", "celdas con IC cotejado")
        add(f"{P}-G-ORO-DELTA-P-MAX", "flotante", "peor |delta punto|")
        add(f"{P}-G-ORO-DELTA-IC-MAX", "flotante", "peor |delta IC|")
        add(f"{P}-G-ORO-REPRODUCE-IC", "texto", "SI si todas las celdas reproducen el IC a tol_ic")
        add(f"{P}-G-ORO-REPRODUCE-P", "texto", "SI si todas reproducen el punto a tol_p")
        add(f"{P}-G-ORO-TOL-IC", "flotante", "tolerancia del IC (la del tipo)")
        add(f"{P}-G-ORO-TOL-P", "flotante", "tolerancia del punto (declarada por el redondeo)")
        add(f"{P}-G-ORO-CAUSA-DELTA-P", "texto", "por qué el punto puede diferir del sellado")
    else:
        raise ValueError(f"punto_de_entrada {pe!r}")
    add(f"{P}-G-MEDIDOR-IDENTICO-A-TOOLS", "texto", "SI si medidor.py es byte a byte tools/lote_enif2024/enif_lote.py")
    return cat


def _cat_control(add, P):
    add(f"{P}-G-CTRL-DELTA-MAX", "flotante", "peor |emitido - sellado|")
    add(f"{P}-G-CTRL-N-COTEJADOS", "entero", "valores cotejados")
    add(f"{P}-G-CTRL-N-NO-COTEJABLES", "entero", "valores sin cotejo (null en alguno de los dos lados)")
    add(f"{P}-G-CTRL-REPRODUCE", "texto", "SI si todo cotejado dentro de la tolerancia")
    add(f"{P}-G-CTRL-TOL", "flotante", "tolerancia del control")


def _cat_bloque(add, P, S):
    add(f"{P}-{S}-CELDAS-PUNTUADAS", "entero", "celdas con soporte en las dos olas")
    for cid in CANDIDATOS:
        add(f"{P}-{S}-{cid}-MAE-PP", "flotante", "error absoluto medio en pp sobre puntuadas", True)
        add(f"{P}-{S}-{cid}-DELTA-MAE-PP", "flotante", "MAE(C2) - MAE(cand) en pp", True)
        add(f"{P}-{S}-{cid}-DELTA-IC95INF", "flotante", "IC95 inferior de delta-MAE por réplica", True)
        add(f"{P}-{S}-{cid}-DELTA-IC95SUP", "flotante", "IC95 superior de delta-MAE por réplica", True)
        add(f"{P}-{S}-{cid}-VEREDICTO", "texto", "regla v0.3: VENCE-RETADOR | PROPUESTA-CON-RESERVA | NADIE-VENCE | NO-ADJUDICABLE | PISO")
        add(f"{P}-{S}-{cid}-ROL", "texto", "PISO | PRIMARIA | SECUNDARIA")
        add(f"{P}-{S}-{cid}-COBERTURA-R-EN-IC-CAND-N", "entero", "celdas con comparación definida")
        add(f"{P}-{S}-{cid}-COBERTURA-R-EN-IC-CAND-FRAC", "proporcion", "fracción de celdas con R dentro del IC95 del candidato", True)
        add(f"{P}-{S}-{cid}-COBERTURA-CAND-EN-IC-R-FRAC", "proporcion", "fracción de celdas con el candidato dentro del IC95 de R", True)
    add(f"{P}-{S}-TRES-CUARTOS-N", "entero", "celdas puntuadas con error definido en C2 y R2")
    add(f"{P}-{S}-TRES-CUARTOS-GANA-R2", "entero", "de ellas, R2 yerra menos que C2 (descriptivo)")
    add(f"{P}-{S}-TRES-CUARTOS-FRAC", "proporcion", "fracción (descriptiva, no adjudica)", True)
    add(f"{P}-{S}-VEREDICTO-PRIMARIO", "texto", "veredicto v0.3 de R2 contra C2 en el bloque")


PUNTOS_DE_ENTRADA = {"emisiones": emisiones, "adjudicacion": adjudicacion, "oro_c2ic": oro_c2ic}


def medir(inputs, contrato) -> dict:
    """Interfaz estable del plan v2.0 §4 (B-1)."""
    par = dict(contrato["parametros"])
    par["_seed"] = int(contrato["seed"]["valor"])
    pe = str(par["punto_de_entrada"])
    if pe not in PUNTOS_DE_ENTRADA:
        raise RuntimeError(f"punto_de_entrada {pe!r} no es uno de {sorted(PUNTOS_DE_ENTRADA)}")
    out = PUNTOS_DE_ENTRADA[pe](inputs, {"parametros": par, "seed": contrato["seed"]})
    P = str(par["prefijo_result"])
    out[f"{P}-G-MEDIDOR-IDENTICO-A-TOOLS"] = (
        "SI" if _sha(Path(__file__).resolve()) == _sha(MODULOS_SHA["ENIF-LOTE"]) else "NO -- DEFECTO")
    return out
