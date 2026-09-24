#!/usr/bin/env python3
"""Árbitro -0002 de ACTO GEN2-ENCIG-PISOS-GEN2-1 (24/sep/2026, CAJA).

HEREDA, POR SHA, el medidor de CALC-ENCIG-DUELO-2025-ADJUDICACION-0001 (74e8aa49…86d4,
= tools/encig/duelo_2025/duelo.py) y cambia SOLO la fuente del punto C2: aquí es el
RESULT `-C2-P` de CALC-ENCIG2025-PISOS-GOBDIGITAL-0001, citado por id (marginales
2025 medidos del manifiesto); allá era el `-C2-P` de las emisiones, copiado de
CALC-C2-COMPUESTO-RESERVADAS-0001 (cadena a milpa/). Contrato humano de este
cambio: forense/prereg-caja/ENCIG-DUELO-2025-ADJUDICACION-0002-spec-v1_0.md.
Añade además, como control, el oro del -0001 (E.5): todo lo que no depende de C2
se reproduce a `tol_oro_0001`. Diff declarado en la spec §2; tests/
test_encig_pisos_gen2.py comprueba que ninguna otra función cambió (AST).

Texto heredado del -0001, sin cambios:
Medidor único de ACTO GEN2-DUELO-ENCIG2025-CIERRE-1 (emisiones y árbitro).

Contrato humano: forense/prereg-caja/ENCIG-DUELO-2025-cierre-spec-v1_0.md,
congelado en COMMIT-1 sin abrir ningún cruce de ENCIG 2025. Este archivo se
deposita byte a byte como `medidor.py` en los tres CALC-ENCIG-DUELO-2025-*;
`medir()` despacha por `parametros.punto_de_entrada`.

  emisiones    (COMMIT-2) sólo insumos sellados del repo; ENCIG 2025 no se lee.
  adjudicacion (COMMIT-3) único código autorizado a cruzar ENCIG 2025, y sólo
               por los dos pares de PARES_AUTORIZADOS.

Lo heredado se ejecuta desde los bytes hasheados de sus inputs: `_lambda_cruce`
(medidor del piloto 4), `_estado_gana` (árbitro del piloto 4) y la receta del
cruce ENCIG (tools/encig_cruces_historicos.py).
"""
from __future__ import annotations

import ast
import json
import math
import types
from pathlib import Path

import numpy as np
import pandas as pd

P = "RESULT-ENCIG-DUELO-2025"
PA = f"{P}-ADJ2"
PA0001 = f"{P}-ADJ"
PISO = "RESULT-ENCIG2025-PISOS-GOBDIGITAL"
FP_FIRMA = "FP-260923-GEN2-DUELO-ENCIG2025-CIERRE-1-657c-01"

EJES = {
    "SEXO": ("1", "2"),
    "EDAD": ("18-29", "30-44", "45-59", "60-96"),
    "ESCOLARIDAD": ("HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"),
}
CRUCES = {"EDADXSEXO": ("EDAD", "SEXO"), "ESCOLARIDADXSEXO": ("ESCOLARIDAD", "SEXO")}
PARES_AUTORIZADOS = frozenset({("EDAD", "SEXO"), ("ESCOLARIDAD", "SEXO")})
HISTORICO_CRUCE = {"EDADXSEXO": "SEXO-EDAD", "ESCOLARIDADXSEXO": "SEXO-ESCOLARIDAD"}

RETADORES = ("C7", "C-ENCOGIDA", "C-ASTRA")
PRIMARIOS = ("C2",) + RETADORES
CANDIDATOS = PRIMARIOS + ("C1",)
CON_IC_PREVIO = ("C1", "C7", "C-ENCOGIDA", "C-ASTRA")
Z = 1.959963984540054
N_MINIMO = 200
TOKENS_2025 = ("encig25", "encig_2025", "encig2025_")

INPUTS_EMISIONES = frozenset({
    "firmas_congeladas", "c2_compuesto_resultados", "historico_2021_resultados",
    "historico_2023_resultados", "astra_resultados", "medidor_piloto4"})
INPUTS_ADJUDICACION_REPO = frozenset({
    "receta_cruce_encig", "adjudicacion_piloto4", "marginales_2025_resultados",
    "emisiones_edadxsexo_resultados", "emisiones_edadxsexo_sello",
    "emisiones_escolaridadxsexo_resultados", "emisiones_escolaridadxsexo_sello",
    "piso_c2_resultados", "piso_c2_sello", "adjudicacion_0001_resultados"})

PRECEDENCIA = ("LIMITA-C2", "LIMITA-C2-SOBRE-CUANTO-ENCOGER", "FALSADOR-DEBIL", "CORROBORADA")


class ParoDeGuardia(RuntimeError):
    pass


class ReservaRota(RuntimeError):
    pass


# ══════════════════════════════ utilidades ══════════════════════════════

def celdas(cruce):
    a, b = CRUCES[cruce]
    return [(ka, kb) for ka in EJES[a] for kb in EJES[b]]


def rotulo(ka, kb):
    return f"{ka}-X-{kb}"


def _fin(x):
    if x is None:
        return None
    x = float(x)
    return x if math.isfinite(x) else None


def _abierto(p):
    return p is not None and math.isfinite(p) and 0.0 < p < 1.0


def _logit(p):
    return math.log(p / (1.0 - p))


def _expit(z):
    return 1.0 / (1.0 + math.exp(-z))


def _pct(v, q):
    return float(np.percentile(v, q)) if len(v) else None


def _wilson(k, n):
    if not n:
        return None, None
    ph = k / n
    den = 1.0 + Z * Z / n
    centro = (ph + Z * Z / (2 * n)) / den
    medio = Z * math.sqrt(ph * (1 - ph) / n + Z * Z / (4 * n * n)) / den
    return max(0.0, centro - medio), min(1.0, centro + medio)


def _bytes(inputs, iid):
    ent = inputs.get(iid)
    if ent is None:
        raise ParoDeGuardia(f"falta el input `{iid}`")
    raw = ent.get("bytes")
    if raw is None:
        raise ParoDeGuardia(f"input `{iid}` sin bytes: se exige origen repo")
    return raw


def _resultados(raw):
    doc = json.loads(raw.decode("utf-8"))
    r = doc.get("resultados", doc) if isinstance(doc, dict) else doc
    if isinstance(r, list):
        r = {x["id"]: x["valor"] for x in r}
    return r


def _sellado(r, rid):
    if rid not in r:
        raise ParoDeGuardia(f"id sellado ausente: {rid}")
    return r[rid]


def _extrae_funcion(fuente, nombre, globales):
    """Una función top-level de un archivo sellado, ejecutada desde SUS bytes."""
    arbol = ast.parse(fuente.decode("utf-8"))
    nodos = [n for n in arbol.body if isinstance(n, ast.FunctionDef) and n.name == nombre]
    if len(nodos) != 1:
        raise ParoDeGuardia(f"`{nombre}` no es única en el archivo heredado ({len(nodos)})")
    ns = dict(globales)
    exec(compile(ast.Module(body=nodos, type_ignores=[]), f"<heredado:{nombre}>", "exec"), ns)
    return ns[nombre]


def _modulo_desde_bytes(nombre, fuente):
    mod = types.ModuleType(nombre)
    mod.__file__ = f"<{nombre}>"
    exec(compile(fuente, mod.__file__, "exec"), mod.__dict__)
    return mod


# ── ids de las fuentes selladas ──────────────────────────────────────────

def id_c2compuesto(cruce, ka, kb):
    a = "60" if ka == "60-96" else ka
    s = {"1": "1-HOMBRE", "2": "2-MUJER"}[kb]
    return f"RESULT-C2COMP-ADOPTA-ENCIG2025-LUZ-{cruce}-{a}-X-{s}"


def id_historico(ola, cruce, ka, kb, q):
    return f"RESULT-ENCIG{ola}-CRUCES-HISTORICOS-{HISTORICO_CRUCE[cruce]}-{kb}-{ka}-{q}"


def id_astra(cruce, ka, kb, q):
    return f"RESULT-ASTRA-ENCIG-{cruce}-{ka}-{kb}-{q}"


def _cat_publica(eje, v):
    return "60-MAS" if (eje == "EDAD" and v == "60-96") else v


def id_marginal_2025(eje, v, q):
    if eje == "TOTAL":
        return f"RESULT-ARBITRO-ENCIG2025-DIGITAL-TOTAL-TODOS-{q}"
    return f"RESULT-ARBITRO-ENCIG2025-DIGITAL-{eje}-{_cat_publica(eje, v)}-{q}"


def id_piso_c2(cruce, ka, kb):
    return f"{PISO}-{cruce}-{rotulo(ka, kb)}-C2-P"


def id_piso_2023(eje, v):
    return f"RESULT-PISOS-ENCIG2023-V2-DIGITAL-{eje}-{_cat_publica(eje, v)}-P"


# ══════════════════════════════ auditoría del código ══════════════════════════════

_LECTURAS_DE_PAYLOAD = {"_load_wave", "_bootstrap", "ZipFile", "read_csv", "_frame_ola",
                        "_modulo_desde_bytes", "_r_y_marginales"}
_GUARDIAS_DE_ENTRADA = {"emisiones": {"_guardia_emisiones", "_guardia_firma"},
                        "adjudicacion": {"auditoria", "_guardia_sellos", "_guardia_payload", "_guardia_piso"}}


def _llamadas(nodo):
    fuera = set()
    for n in ast.walk(nodo):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                fuera.add(f.id)
            elif isinstance(f, ast.Attribute):
                fuera.add(f.attr)
    return fuera


def auditoria(fuente):
    """Lista de problemas del código (vacía = limpio). Spec §5."""
    arbol = ast.parse(fuente.decode("utf-8") if isinstance(fuente, bytes) else fuente)
    funciones = {n.name: n for n in arbol.body if isinstance(n, ast.FunctionDef)}
    problemas = []
    grafo = {nombre: _llamadas(nodo) for nombre, nodo in funciones.items()}

    # (1) desde `emisiones` no se alcanza ninguna lectura de payload
    vistos, pila = set(), ["emisiones"]
    while pila:
        f = pila.pop()
        if f in vistos or f not in grafo:
            continue
        vistos.add(f)
        pila.extend(grafo[f] & set(funciones))
    alcanzadas = set().union(*(grafo[f] for f in vistos)) if vistos else set()
    if "emisiones" not in funciones:
        problemas.append("falta la funcion emisiones")
    prohibidas = (alcanzadas | vistos) & _LECTURAS_DE_PAYLOAD
    if prohibidas:
        problemas.append(f"emisiones alcanza lectura de payload: {sorted(prohibidas)}")

    # (2) toda máscara de cruce sale de `_mascara`; `.eq(` sólo vive ahí
    for nombre, nodo in funciones.items():
        if nombre != "_mascara" and "eq" in grafo[nombre]:
            problemas.append(f"`{nombre}` construye mascaras fuera de _mascara")
    if "_r_y_marginales" in grafo and "_mascara" not in grafo["_r_y_marginales"]:
        problemas.append("_r_y_marginales no usa _mascara")
    llaman_bootstrap = sorted(n for n, g in grafo.items() if "_bootstrap" in g)
    if llaman_bootstrap != ["_r_y_marginales"]:
        problemas.append(f"_bootstrap llamado desde {llaman_bootstrap}")

    # (3) PARES_AUTORIZADOS es exactamente los dos pares
    pares = None
    for n in arbol.body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "PARES_AUTORIZADOS"
                                             for t in n.targets):
            valor = n.value
            if isinstance(valor, ast.Call) and valor.args:
                valor = valor.args[0]
            try:
                pares = set(ast.literal_eval(valor))
            except ValueError:
                pares = None
    if pares != {("EDAD", "SEXO"), ("ESCOLARIDAD", "SEXO")}:
        problemas.append(f"PARES_AUTORIZADOS alterado: {pares}")

    # (4) las guardias se llaman al entrar
    for nombre, exigidas in _GUARDIAS_DE_ENTRADA.items():
        if nombre not in funciones:
            problemas.append(f"falta la funcion {nombre}")
            continue
        faltan = exigidas - grafo[nombre]
        if faltan:
            problemas.append(f"{nombre} no llama {sorted(faltan)}")

    # (5) `_mascara` consulta PARES_AUTORIZADOS y levanta ReservaRota
    m = funciones.get("_mascara")
    nombres_m = {n.id for n in ast.walk(m) if isinstance(n, ast.Name)} if m else set()
    if not m or "PARES_AUTORIZADOS" not in nombres_m or "ReservaRota" not in nombres_m:
        problemas.append("_mascara no aplica la guardia de pares")
    return problemas


def _audita_propio():
    return auditoria(Path(__file__).read_bytes())


# ══════════════════════════════ EMISIONES (COMMIT-2) ══════════════════════════════

def _guardia_emisiones(inputs):
    ids = set(inputs)
    if ids != INPUTS_EMISIONES:
        raise ParoDeGuardia(f"inputs de emisiones fuera de la lista: sobran {sorted(ids - INPUTS_EMISIONES)}, "
                            f"faltan {sorted(INPUTS_EMISIONES - ids)}")
    for iid, ent in inputs.items():
        texto = f"{iid} {ent.get('ruta', '')}".lower()
        if any(t in texto for t in TOKENS_2025):
            raise ParoDeGuardia(f"input `{iid}` nombra ENCIG 2025: la emision no lee 2025")
        if ent.get("origen", "repo") != "repo" or ent.get("bytes") is None:
            raise ParoDeGuardia(f"input `{iid}` no es origen repo con bytes")


def _guardia_firma(inputs):
    texto = _bytes(inputs, "firmas_congeladas").decode("utf-8")
    for linea in texto.splitlines()[1:]:
        campos = linea.split("\t")
        if campos and campos[0] == FP_FIRMA:
            if len(campos) > 5 and campos[5] == "FIRMADA":
                return "FIRMADA"
            raise ParoDeGuardia(f"{FP_FIRMA}: estado={campos[5] if len(campos) > 5 else None!r}")
    raise ParoDeGuardia(f"{FP_FIRMA}: ausente de la copia congelada")


def _prueba_guardia(inputs):
    mutado = dict(inputs)
    mutado["encig25_base_datos_csv"] = {"origen": "manifiesto", "ruta_absoluta": "/prueba", "sha256": "0"}
    try:
        _guardia_emisiones(mutado)
    except ParoDeGuardia as exc:
        return f"ParoDeGuardia: {exc}"
    raise ParoDeGuardia("la guardia de emisiones NO paro ante un input de ENCIG 2025")


def _delta(r, ola, cruce, ka, kb):
    d = _fin(_sellado(r, id_historico(ola, cruce, ka, kb, "DELTA")))
    ee = _fin(_sellado(r, id_historico(ola, cruce, ka, kb, "DELTA-EE")))
    causa = _sellado(r, id_historico(ola, cruce, ka, kb, "CAUSA"))
    ok = causa == "OK" and d is not None and ee is not None and ee > 0
    return (d, ee) if ok else (None, None)


def _admision_astra(astra, cruce):
    faltan, tipos = [], set()
    for ka, kb in celdas(cruce):
        for q in ("P", "IC-LO", "IC-HI", "NIVEL", "TIPO"):
            if id_astra(cruce, ka, kb, q) not in astra:
                faltan.append(id_astra(cruce, ka, kb, q))
        t = astra.get(id_astra(cruce, ka, kb, "TIPO"))
        if t:
            tipos.add(t)
    a = "SI -- 8/8 celdas con los cinco ids" if not faltan else f"NO -- faltan {len(faltan)} ids"
    c = ("SI -- punto, IC, nivel y tipo por celda (" + ",".join(sorted(tipos)) + ")"
         if not faltan and tipos else "NO")
    return a, c, (not faltan and bool(tipos))


def emisiones(inputs, contrato):
    _guardia_emisiones(inputs)
    firma = _guardia_firma(inputs)
    problemas = _audita_propio()
    if problemas:
        raise ParoDeGuardia(f"auditoria del codigo: {problemas}")
    par = contrato["parametros"]
    cruce = str(par["cruce"])
    if cruce not in CRUCES:
        raise ParoDeGuardia(f"cruce fuera de la lista: {cruce}")
    umbral = int(par["n_minimo_celda"])
    pre = f"{P}-{cruce}"
    c2c = _resultados(_bytes(inputs, "c2_compuesto_resultados"))
    h21 = _resultados(_bytes(inputs, "historico_2021_resultados"))
    h23 = _resultados(_bytes(inputs, "historico_2023_resultados"))
    astra = _resultados(_bytes(inputs, "astra_resultados"))
    lambda_cruce = _extrae_funcion(_bytes(inputs, "medidor_piloto4"), "_lambda_cruce", {"np": np})

    out = {f"{pre}-G-CRUCE": cruce, f"{pre}-G-FIRMA-ESTADO": firma,
           f"{pre}-G-RESERVA-ENCIG2025-LEIDA": "NO",
           f"{pre}-G-GUARDIA-PROBADA": _prueba_guardia(inputs),
           f"{pre}-G-AUDITORIA-CODIGO": "LIMPIA"}
    for iid in sorted(INPUTS_EMISIONES):
        out[f"{pre}-G-INPUT-{iid.upper().replace('_', '-')}-SHA256"] = str(inputs[iid].get("sha256"))

    d21, e21, d23, e23 = {}, {}, {}, {}
    fallan = 0
    for ka, kb in celdas(cruce):
        c = rotulo(ka, kb)
        base = f"{pre}-{c}"
        c2 = _fin(_sellado(c2c, id_c2compuesto(cruce, ka, kb)))
        out[f"{base}-C2-P"] = c2 if _abierto(c2) else None
        out[f"{base}-C1-P"] = _fin(_sellado(h23, id_historico("2023", cruce, ka, kb, "P")))
        out[f"{base}-C1-IC-LO"] = _fin(_sellado(h23, id_historico("2023", cruce, ka, kb, "P-IC-LO")))
        out[f"{base}-C1-IC-HI"] = _fin(_sellado(h23, id_historico("2023", cruce, ka, kb, "P-IC-HI")))
        n21 = int(_sellado(h21, id_historico("2021", cruce, ka, kb, "N")))
        n23 = int(_sellado(h23, id_historico("2023", cruce, ka, kb, "N")))
        out[f"{base}-N-2021"], out[f"{base}-N-2023"] = n21, n23
        sop = "SOPORTE-OK" if (n21 >= umbral and n23 >= umbral) else "FUERA-DE-SOPORTE"
        fallan += sop != "SOPORTE-OK"
        out[f"{base}-SOPORTE-HISTORICO"] = sop
        d21[c], e21[c] = _delta(h21, "2021", cruce, ka, kb)
        d23[c], e23[c] = _delta(h23, "2023", cruce, ka, kb)
        out[f"{base}-D21"], out[f"{base}-D21-EE"] = d21[c], e21[c]
        out[f"{base}-D23"], out[f"{base}-D23-EE"] = d23[c], e23[c]
        ok = None not in (d21[c], e21[c], d23[c], e23[c])
        out[f"{base}-DELTA-ESTADO"] = "OK" if ok else "DEGENERADO"
        out[f"{base}-DBAR"] = (d21[c] + d23[c]) / 2.0 if ok else None
        out[f"{base}-DBAR-EE"] = math.sqrt((e21[c] ** 2 + e23[c] ** 2) / 4.0) if ok else None
    out[f"{pre}-G-SOPORTE-HISTORICO-FALLAN"] = int(fallan)

    lam = lambda_cruce(d21, e21, d23, e23, set())
    out[f"{pre}-G-LAMBDA"] = float(lam["lambda"])
    out[f"{pre}-G-LAMBDA-TAU2"] = float(lam["tau2"])
    out[f"{pre}-G-LAMBDA-SIGMA-BAR2"] = float(lam["sigma_bar2"])
    out[f"{pre}-G-LAMBDA-VAR-ENTRE"] = float(lam["var_entre"])
    out[f"{pre}-G-LAMBDA-K"] = int(lam["k"])
    out[f"{pre}-G-LAMBDA-ESTADO"] = str(lam["estado"])
    out[f"{pre}-G-LAMBDA-FUENTE"] = ("_lambda_cruce de CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-EMISIONES-0001/"
                                     f"medidor.py sha256={inputs['medidor_piloto4'].get('sha256')}; "
                                     "pares (2021, 2023)")

    for ka, kb in celdas(cruce):
        base = f"{pre}-{rotulo(ka, kb)}"
        c2, dbar, dee = out[f"{base}-C2-P"], out[f"{base}-DBAR"], out[f"{base}-DBAR-EE"]
        for cid, l in (("C7", 1.0), ("C-ENCOGIDA", float(lam["lambda"]))):
            if c2 is None or dbar is None:
                out[f"{base}-{cid}-P"] = out[f"{base}-{cid}-IC-LO"] = out[f"{base}-{cid}-IC-HI"] = None
                continue
            centro = _logit(c2) + l * dbar
            out[f"{base}-{cid}-P"] = _expit(centro)
            out[f"{base}-{cid}-IC-LO"] = _expit(centro - Z * l * dee)
            out[f"{base}-{cid}-IC-HI"] = _expit(centro + Z * l * dee)

    a, c_, entra = _admision_astra(astra, cruce)
    out[f"{pre}-G-C-ASTRA-A-CELDAS"] = a
    out[f"{pre}-G-C-ASTRA-B"] = str(par["c_astra_b"])
    out[f"{pre}-G-C-ASTRA-C"] = c_
    out[f"{pre}-G-C-ASTRA-ESTADO"] = "ENTRA" if entra else "NO-ENTRA"
    for ka, kb in celdas(cruce):
        base = f"{pre}-{rotulo(ka, kb)}"
        for q in ("P", "IC-LO", "IC-HI"):
            v = _fin(astra.get(id_astra(cruce, ka, kb, q))) if entra else None
            out[f"{base}-C-ASTRA-{q}"] = v if (v is not None and 0.0 <= v <= 1.0) else None
        out[f"{base}-C-ASTRA-TIPO"] = str(astra.get(id_astra(cruce, ka, kb, "TIPO"))) if entra else "NO-ENTRA"

    out[f"{pre}-G-FORMA-C2"] = "expit(logit p25(a) + logit p25(b) - logit p25), marginales publicos; copiado de CALC-C2-COMPUESTO-RESERVADAS-0001"
    out[f"{pre}-G-FORMA-C1"] = "p23(a,b) directo; copiado de CALC-ENCIG2023-CRUCES-HISTORICOS-0002 (referencia, no adjudica)"
    out[f"{pre}-G-FORMA-C7"] = "expit(logit C2 + (d21 + d23)/2)"
    out[f"{pre}-G-FORMA-C-ENCOGIDA"] = "expit(logit C2 + lambda_cruce*(d21 + d23)/2)"
    out[f"{pre}-G-TIPO-IC-CASA"] = "CONDICIONAL-C2-FIJO-SOLO-DELTA-HISTORICO: expit(logit C2 + l*dbar +- z*l*sqrt((EE21^2+EE23^2)/4))"
    out[f"{pre}-G-MARCA"] = "PROSPECTIVA -- sellada antes de que exista R de este cruce"
    return out


_EMI_GLOBALES = (
    ("G-CRUCE", "texto", "identificador"), ("G-FIRMA-ESTADO", "texto", "categoría"),
    ("G-RESERVA-ENCIG2025-LEIDA", "texto", "SI/NO"), ("G-GUARDIA-PROBADA", "texto", "categoría"),
    ("G-AUDITORIA-CODIGO", "texto", "categoría"),
    ("G-SOPORTE-HISTORICO-FALLAN", "entero", "celdas"),
    ("G-LAMBDA", "flotante", "adimensional [0,1]"),
    ("G-LAMBDA-TAU2", "flotante", "varianza en escala logit al cuadrado"),
    ("G-LAMBDA-SIGMA-BAR2", "flotante", "varianza en escala logit al cuadrado"),
    ("G-LAMBDA-VAR-ENTRE", "flotante", "varianza en escala logit al cuadrado"),
    ("G-LAMBDA-K", "entero", "celdas"), ("G-LAMBDA-ESTADO", "texto", "categoría"),
    ("G-LAMBDA-FUENTE", "texto", "procedencia"),
    ("G-C-ASTRA-A-CELDAS", "texto", "categoría"), ("G-C-ASTRA-B", "texto", "categoría"),
    ("G-C-ASTRA-C", "texto", "categoría"), ("G-C-ASTRA-ESTADO", "texto", "categoría"),
    ("G-FORMA-C2", "texto", "fórmula (texto)"), ("G-FORMA-C1", "texto", "fórmula (texto)"),
    ("G-FORMA-C7", "texto", "fórmula (texto)"), ("G-FORMA-C-ENCOGIDA", "texto", "fórmula (texto)"),
    ("G-TIPO-IC-CASA", "texto", "tipo de intervalo"), ("G-MARCA", "texto", "categoría"),
)
_EMI_CELDA = (
    ("C2-P", "proporcion", "proporción de trámites [0,1]"),
    ("C1-P", "proporcion", "proporción de trámites [0,1]"),
    ("C1-IC-LO", "proporcion", "límite inferior IC95"), ("C1-IC-HI", "proporcion", "límite superior IC95"),
    ("N-2021", "entero", "trámites"), ("N-2023", "entero", "trámites"),
    ("SOPORTE-HISTORICO", "texto", "categoría"),
    ("D21", "flotante", "logit"), ("D21-EE", "flotante", "error estándar logit"),
    ("D23", "flotante", "logit"), ("D23-EE", "flotante", "error estándar logit"),
    ("DELTA-ESTADO", "texto", "categoría"),
    ("DBAR", "flotante", "logit"), ("DBAR-EE", "flotante", "error estándar logit"),
    ("C7-P", "proporcion", "proporción de trámites [0,1]"),
    ("C7-IC-LO", "proporcion", "límite inferior, condicional a C2 fijo"),
    ("C7-IC-HI", "proporcion", "límite superior, condicional a C2 fijo"),
    ("C-ENCOGIDA-P", "proporcion", "proporción de trámites [0,1]"),
    ("C-ENCOGIDA-IC-LO", "proporcion", "límite inferior, condicional a C2 fijo"),
    ("C-ENCOGIDA-IC-HI", "proporcion", "límite superior, condicional a C2 fijo"),
    ("C-ASTRA-P", "proporcion", "proporción de trámites [0,1]"),
    ("C-ASTRA-IC-LO", "proporcion", "límite inferior predictivo 95%"),
    ("C-ASTRA-IC-HI", "proporcion", "límite superior predictivo 95%"),
    ("C-ASTRA-TIPO", "texto", "tipo de intervalo"),
)


def _fila(rid, tipo, unidad, deps=None):
    f = {"id": rid, "tipo": tipo, "unidad": unidad}
    if tipo in ("flotante", "proporcion"):
        f["permite_no_estimable"] = True
    if deps is not None:
        f["dependencias_numericas"] = list(deps)
    return f


def esquema_emisiones(cruce):
    pre = f"{P}-{cruce}"
    filas = [_fila(f"{pre}-{s}", t, u) for s, t, u in _EMI_GLOBALES]
    for iid in sorted(INPUTS_EMISIONES):
        filas.append(_fila(f"{pre}-G-INPUT-{iid.upper().replace('_', '-')}-SHA256", "texto", "hash sha256"))
    for ka, kb in celdas(cruce):
        filas += [_fila(f"{pre}-{rotulo(ka, kb)}-{s}", t, u) for s, t, u in _EMI_CELDA]
    return filas


# ══════════════════════════════ ÁRBITRO (COMMIT-3) ══════════════════════════════

def _guardia_sellos(inputs):
    import hashlib
    emis = {}
    for cruce in CRUCES:
        k = cruce.lower()
        raw = _bytes(inputs, f"emisiones_{k}_resultados")
        sello = json.loads(_bytes(inputs, f"emisiones_{k}_sello").decode("utf-8"))
        real = hashlib.sha256(raw).hexdigest()
        if sello.get("resultados.json") != real:
            raise ParoDeGuardia(f"sello de emisiones {cruce} no coincide: {sello.get('resultados.json')} != {real}")
        r = _resultados(raw)
        if r.get(f"{P}-{cruce}-G-CRUCE") != cruce:
            raise ParoDeGuardia(f"emisiones de {cruce} no declaran su cruce")
        emis[cruce] = r
    return emis


def _guardia_piso(inputs):
    """El piso se lee sólo si su sello coincide y su CALC declara origen NUEVO y
    controles REPRODUCE; si no, PARA sin leer el cruce."""
    import hashlib
    raw = _bytes(inputs, "piso_c2_resultados")
    sello = json.loads(_bytes(inputs, "piso_c2_sello").decode("utf-8"))
    real = hashlib.sha256(raw).hexdigest()
    if sello.get("resultados.json") != real:
        raise ParoDeGuardia(f"sello del piso no coincide: {sello.get('resultados.json')} != {real}")
    r = _resultados(raw)
    for campo in ("CTRL-MARGINALES-VEREDICTO", "CTRL-0001-VEREDICTO"):
        if r.get(f"{PISO}-G-{campo}") != "REPRODUCE":
            raise ParoDeGuardia(f"piso: {campo} = {r.get(f'{PISO}-G-{campo}')!r}")
    if not str(r.get(f"{PISO}-G-ORIGEN", "")).startswith("NUEVO"):
        raise ParoDeGuardia("piso sin origen NUEVO declarado")
    return r


def _control_oro_0001(out, oro, tol):
    """E.5: lo que no depende de C2 reproduce el -0001 sellado, id por id."""
    peor, n_cmp, faltan = 0.0, 0, 0
    sufijos = ("-R-P", "-R-IC-LO", "-R-IC-HI", "-R-EE", "-N-2025", "-DELTA-25", "-C2-P-RECALCULADO",
               "-C2-IC-LO", "-C2-IC-HI", "-D-C7", "-D-C-ENCOGIDA", "-D-C-ASTRA", "-D-C1")
    for k, v in out.items():
        if not (k.startswith(f"{PA}-M-") or k.endswith(sufijos)):
            continue
        k0 = PA0001 + k[len(PA):]
        if k0 not in oro:
            faltan += 1
            continue
        a, b = _fin(v), _fin(oro[k0])
        n_cmp += 1
        if a is None or b is None:
            peor = peor if a is None and b is None else math.inf
        else:
            peor = max(peor, abs(a - b))
    out[f"{PA}-G-CTRL-ORO-0001-MAX-ABS"] = peor if math.isfinite(peor) else None
    out[f"{PA}-G-CTRL-ORO-0001-N"] = int(n_cmp)
    out[f"{PA}-G-CTRL-ORO-0001-VEREDICTO"] = ("REPRODUCE" if (peor <= tol and faltan == 0 and n_cmp)
                                             else "NO-REPRODUCE")


def _guardia_payload(inputs, contrato):
    par = contrato["parametros"]
    payload = str(par["payload_id"])
    esperados = INPUTS_ADJUDICACION_REPO | {payload}
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs del arbitro fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    for iid, ent in inputs.items():
        if iid != payload and ent.get("bytes") is None:
            raise ParoDeGuardia(f"input `{iid}` debia ser origen repo con bytes")
    if not inputs[payload].get("ruta_absoluta"):
        raise ParoDeGuardia(f"payload `{payload}` sin ruta resuelta")
    return payload


def _mascara(frame, ejes, par_universo=None):
    """Única constructora de máscaras (E.6). `ejes`: ((eje, valor), ...)."""
    nombres = tuple(e for e, _ in ejes)
    if par_universo is not None and tuple(par_universo) not in PARES_AUTORIZADOS:
        raise ReservaRota(f"universo de par no autorizado: {par_universo}")
    if len(nombres) > 2 or (len(nombres) == 2 and nombres not in PARES_AUTORIZADOS):
        raise ReservaRota(f"agrupacion no autorizada: {nombres}")
    m = pd.Series(True, index=frame.index)
    if par_universo is not None:
        m &= frame[par_universo[0]].notna() & frame[par_universo[1]].notna()
    for eje, valor in ejes:
        m &= frame[eje].eq(valor)
    return m


def _frame_ola(receta, inputs, ola, payload_id):
    return receta._load_wave(inputs, {"parametros": {"ola": str(ola), "payload_id": payload_id}})


def _r_y_marginales(receta, frame, repeticiones, semilla):
    """Máscaras de la receta por celda (ab, a, b, todo sobre el universo común del
    par) + 11 marginales de un eje sobre su propio denominador; UN bootstrap."""
    masks, idx = [], {}
    for cruce, (A, B) in CRUCES.items():
        for ka, kb in celdas(cruce):
            idx[(cruce, ka, kb)] = len(masks)
            masks += [_mascara(frame, ((A, ka), (B, kb)), (A, B)),
                      _mascara(frame, ((A, ka),), (A, B)),
                      _mascara(frame, ((B, kb),), (A, B)),
                      _mascara(frame, (), (A, B))]
    idx_m = {}
    for eje, valores in EJES.items():
        for v in valores:
            idx_m[(eje, v)] = len(masks)
            masks.append(_mascara(frame, ((eje, v),)))
    idx_m[("TOTAL", "TODOS")] = len(masks)
    masks.append(_mascara(frame, ()))
    points, boot, _den = receta._bootstrap(frame, masks, repeticiones, semilla)
    n = [int(m.sum()) for m in masks]
    return {"idx": idx, "idx_m": idx_m, "points": points, "boot": boot, "n": n}


def _ic_c2(ra, rb, rn):
    with np.errstate(all="ignore"):
        z = np.log(ra / (1 - ra)) + np.log(rb / (1 - rb)) - np.log(rn / (1 - rn))
        rep = 1.0 / (1.0 + np.exp(-z))
    return rep


def _b_bis(estado_global, gana, dmae_hi, umbral, activos):
    if estado_global != "CON-SOPORTE":
        return "FUERA-DE-SOPORTE-GLOBAL"
    W = {j for j in activos if gana[j] == "SI"}
    if not W:
        his = [dmae_hi[j] for j in activos]
        if his and all(h is not None and h <= umbral for h in his):
            return "CORROBORADA"
        return "FALSADOR-DEBIL"
    if W in ({"C-ENCOGIDA"}, {"C7"}):
        return "LIMITA-C2-SOBRE-CUANTO-ENCOGER"
    return "LIMITA-C2"


def adjudicar(res, emis, marg25, estado_gana, resumen, par, diag, piso):
    umbral_n = int(par["n_minimo_celda"])
    umbral_pp = float(par["delta_mae_umbral_pp"])
    fraccion = float(par["fraccion_descriptiva"])
    tol_m, tol_c2 = float(par["tol_marginales"]), float(par["tol_c2"])
    pts, boot, n = res["points"], res["boot"], res["n"]
    out = {}
    for k, v in diag.items():
        out[f"{PA}-G-{k}"] = int(v)

    # control 1 · marginales de un eje vs CALC-ARBITRO-MARGINALES-ENCIG2025-0001
    peor, n_disc = 0.0, 0
    for (eje, v), i in res["idx_m"].items():
        p = _fin(pts[i])
        base = f"{PA}-M-{eje}-{_cat_publica(eje, v)}"
        out[f"{base}-P"], out[f"{base}-N"] = p, int(n[i])
        s_p = _fin(marg25.get(id_marginal_2025(eje, v, "P")))
        s_n = marg25.get(id_marginal_2025(eje, v, "N"))
        if p is None or s_p is None:
            peor = math.inf
        else:
            peor = max(peor, abs(p - s_p))
        n_disc += s_n is None or int(s_n) != int(n[i])
    ctrl_m = "REPRODUCE" if (peor <= tol_m and n_disc == 0) else "NO-REPRODUCE"
    out[f"{PA}-G-CTRL-MARGINALES-MAX-ABS-P"] = peor if math.isfinite(peor) else None
    out[f"{PA}-G-CTRL-MARGINALES-N-DISCORDA"] = int(n_disc)
    out[f"{PA}-G-CTRL-MARGINALES-VEREDICTO"] = ctrl_m

    agregado = []
    for cruce, (A, B) in CRUCES.items():
        pc = f"{PA}-{cruce}"
        pe = f"{P}-{cruce}"
        e = emis[cruce]
        astra_entra = e.get(f"{pe}-G-C-ASTRA-ESTADO") == "ENTRA"
        activos = tuple(j for j in RETADORES if j != "C-ASTRA" or astra_entra)
        out[f"{pc}-G-C-ASTRA-ESTADO"] = "ENTRA" if astra_entra else "NO-ENTRA"
        i0 = res["idx"][(cruce,) + celdas(cruce)[0]]
        out[f"{pc}-G-N-COMPLETOS"] = int(n[i0 + 3])
        out[f"{pc}-G-RESIDUO-N"] = int(n[res["idx_m"][("TOTAL", "TODOS")]] - n[i0 + 3])
        ina, inb = res["idx_m"], res["idx_m"][("TOTAL", "TODOS")]

        cand, R, ICR, REP, rep_c2s = {k: {} for k in CANDIDATOS}, {}, {}, {}, {}
        peor_c2 = 0.0
        for ka, kb in celdas(cruce):
            c = rotulo(ka, kb)
            base, be = f"{pc}-{c}", f"{pe}-{c}"
            i = res["idx"][(cruce, ka, kb)]
            r = _fin(pts[i])
            ee, lo, hi, validas = resumen(r, boot[:, i])
            out[f"{base}-N-2025"] = int(n[i])
            out[f"{base}-R-P"] = r
            out[f"{base}-R-IC-LO"], out[f"{base}-R-IC-HI"] = lo, hi
            out[f"{base}-R-EE"] = (hi - lo) / 3.92 if (lo is not None and hi is not None) else None
            out[f"{base}-R-B-VALIDAS"] = int(validas)
            pa_, pb_, pall_ = (_fin(pts[i + 1]), _fin(pts[i + 2]), _fin(pts[i + 3]))
            out[f"{base}-DELTA-25"] = (_logit(r) - _logit(pa_) - _logit(pb_) + _logit(pall_)
                                       if all(_abierto(x) for x in (r, pa_, pb_, pall_)) else None)
            R[c], ICR[c], REP[c] = r, (lo, hi), boot[:, i]
            for k in CANDIDATOS:
                cand[k][c] = _fin(e.get(f"{be}-{k}-P"))
            # ÚNICO cambio de procedimiento del -0002: C2 := RESULT del piso, por id
            out[f"{base}-C2-P-EMISION-0001"] = cand["C2"][c]
            cand["C2"][c] = _fin(_sellado(piso, id_piso_c2(cruce, ka, kb)))
            out[f"{base}-C2-P"] = cand["C2"][c]
            # C2 recompuesto en la ola (control 2) y su IC por réplica
            xa, xb, xn = ina[(A, ka)], ina[(B, kb)], inb
            p_a, p_b, p_n = _fin(pts[xa]), _fin(pts[xb]), _fin(pts[xn])
            c2w = (_expit(_logit(p_a) + _logit(p_b) - _logit(p_n))
                   if all(_abierto(x) for x in (p_a, p_b, p_n)) else None)
            out[f"{base}-C2-P-RECALCULADO"] = c2w
            if c2w is None or cand["C2"][c] is None:
                peor_c2 = math.inf
            else:
                peor_c2 = max(peor_c2, abs(c2w - cand["C2"][c]))
            rep_c2s[c] = _ic_c2(boot[:, xa], boot[:, xb], boot[:, xn])
        ctrl_c2 = "REPRODUCE" if peor_c2 <= tol_c2 else "NO-REPRODUCE"
        out[f"{pc}-G-CTRL-C2-MAX-ABS"] = peor_c2 if math.isfinite(peor_c2) else None
        out[f"{pc}-G-CTRL-C2-VEREDICTO"] = ctrl_c2
        c2_ic_ok = ctrl_m == "REPRODUCE" and ctrl_c2 == "REPRODUCE"
        n_ic_c2 = 0
        for ka, kb in celdas(cruce):
            c = rotulo(ka, kb)
            rep_c2 = rep_c2s[c]
            if c2_ic_ok and np.all(np.isfinite(rep_c2)):
                out[f"{pc}-{c}-C2-IC-LO"] = _pct(rep_c2, 2.5)
                out[f"{pc}-{c}-C2-IC-HI"] = _pct(rep_c2, 97.5)
                n_ic_c2 += 1
            else:
                out[f"{pc}-{c}-C2-IC-LO"] = out[f"{pc}-{c}-C2-IC-HI"] = None
        out[f"{pc}-G-C2-IC-ESTADO"] = (
            f"NACE-CON-R -- {n_ic_c2}/{len(celdas(cruce))} celdas con IC por replica"
            if c2_ic_ok else "NO-EMITIDO -- control de marginales o de C2 NO-REPRODUCE")

        # soporte y PUNTUADA
        puntuadas, fallan = [], 0
        for ka, kb in celdas(cruce):
            c = rotulo(ka, kb)
            be = f"{pe}-{c}"
            n21, n23 = e.get(f"{be}-N-2021"), e.get(f"{be}-N-2023")
            n25 = out[f"{pc}-{c}-N-2025"]
            con_n = all(x is not None and int(x) >= umbral_n for x in (n21, n23, n25))
            fallan += not con_n
            prim_ok = all(cand[k][c] is not None for k in ("C2",) + activos)
            ok = con_n and R[c] is not None and ICR[c][0] is not None and prim_ok
            out[f"{pc}-{c}-SOPORTE"] = ("PUNTUADA" if ok else
                                         "FUERA-DE-SOPORTE" if not con_n else "NO-PUNTUADA")
            if ok:
                puntuadas.append(c)
        umbral_global = round(len(celdas(cruce)) / 3)
        estado_global = ("FUERA-DE-SOPORTE-GLOBAL" if (fallan >= umbral_global or not puntuadas)
                         else "CON-SOPORTE")
        out[f"{pc}-G-PUNTUADAS-N"] = len(puntuadas)
        out[f"{pc}-G-FALLAN-N"] = int(fallan)
        out[f"{pc}-G-FUERA-GLOBAL-UMBRAL"] = int(umbral_global)
        out[f"{pc}-G-SOPORTE-GLOBAL"] = estado_global

        # por celda: d y veredicto descriptivo
        vence = {j: 0 for j in RETADORES}
        indec = {j: 0 for j in RETADORES}
        for ka, kb in celdas(cruce):
            c = rotulo(ka, kb)
            for k in CANDIDATOS:
                v = cand[k][c]
                out[f"{pc}-{c}-D-{k}"] = 100.0 * abs(v - R[c]) if (v is not None and R[c] is not None) else None
            for j in RETADORES:
                if c not in puntuadas or j not in activos:
                    out[f"{pc}-{c}-VEREDICTO-{j}-VS-C2"] = "NO-PUNTUADA" if j in activos else "NO-ENTRA"
                    continue
                lo, hi = ICR[c]
                ee_r = (hi - lo) / 3.92
                dl, dm = out[f"{pc}-{c}-D-{j}"], out[f"{pc}-{c}-D-C2"]
                ambos = lo <= cand[j][c] <= hi and lo <= cand["C2"][c] <= hi
                v = ("INDECIDIBLE" if (ambos or abs(dl - dm) < 0.5 * 100.0 * ee_r) else
                     "GANA-CHALLENGER" if dl < dm else "GANA-PISO")
                out[f"{pc}-{c}-VEREDICTO-{j}-VS-C2"] = v
                vence[j] += v == "GANA-CHALLENGER"
                indec[j] += v == "INDECIDIBLE"

        # MAE, ΔMAE con IC por réplica de R (puntos de candidatos fijos)
        def mae(k):
            v = [out[f"{pc}-{c}-D-{k}"] for c in puntuadas]
            return float(np.mean(v)) if v and all(x is not None for x in v) else None
        maes = {k: mae(k) for k in CANDIDATOS}
        for k in CANDIDATOS:
            out[f"{pc}-G-MAE-{k}"] = maes[k]
        gana, dmae_hi = {}, {}
        for j in RETADORES:
            q = f"{pc}-G-{j}"
            out[f"{q}-VENCE-N"], out[f"{q}-INDECIDIBLE-N"] = int(vence[j]), int(indec[j])
            out[f"{q}-FRACCION-3-4"] = ("SI" if (puntuadas and vence[j] >= math.ceil(fraccion * len(puntuadas)))
                                        else "NO")
            if j in activos and puntuadas and maes["C2"] is not None and maes[j] is not None:
                reps = np.mean([np.abs(cand["C2"][c] - REP[c]) - np.abs(cand[j][c] - REP[c])
                                for c in puntuadas], axis=0) * 100.0
                okr = reps[np.isfinite(reps)]
                ic = (_pct(okr, 2.5), _pct(okr, 97.5))
                out[f"{q}-DELTA-MAE-PP"] = maes["C2"] - maes[j]
                out[f"{q}-DELTA-MAE-IC-LO"], out[f"{q}-DELTA-MAE-IC-HI"] = ic
                out[f"{q}-DELTA-MAE-B-VALIDAS"] = int(len(okr))
                gana[j] = estado_gana(ic, umbral_pp) if estado_global == "CON-SOPORTE" else "NO"
                dmae_hi[j] = ic[1]
            else:
                out[f"{q}-DELTA-MAE-PP"] = out[f"{q}-DELTA-MAE-IC-LO"] = out[f"{q}-DELTA-MAE-IC-HI"] = None
                out[f"{q}-DELTA-MAE-B-VALIDAS"] = 0
                gana[j] = "NO-ENTRA" if j not in activos else "NO"
                dmae_hi[j] = None
            out[f"{q}-GANA"] = gana[j]

        bbis = _b_bis(estado_global, gana, dmae_hi, umbral_pp, activos)
        ganadores = sorted(j for j in activos if gana[j] == "SI")
        reservas = sorted(j for j in activos if gana[j] == "PROPUESTA-CON-RESERVA")
        out[f"{pc}-G-GANADORES"] = ",".join(ganadores) or "NINGUNO"
        out[f"{pc}-G-PROPUESTAS-CON-RESERVA"] = ",".join(reservas) or "NINGUNA"
        out[f"{pc}-G-B-BIS"] = bbis
        out[f"{pc}-G-VEREDICTO-CELDA-D"] = {"CORROBORADA": "SIN-CANDIDATO-SUPERIOR"}.get(bbis, bbis)
        piso_no_vencido = bbis in ("CORROBORADA", "FALSADOR-DEBIL")
        out[f"{pc}-G-CHAMPION-PROPUESTO"] = ("C2" if (piso_no_vencido and c2_ic_ok and
                                                      n_ic_c2 == len(celdas(cruce))) else "NINGUNO")
        if bbis != "FUERA-DE-SOPORTE-GLOBAL":
            agregado.append(bbis)

        # cobertura (sólo IC sellado antes de R) y punto dentro del IC de R
        for k in CON_IC_PREVIO:
            kk = kn = 0
            for c in puntuadas:
                lo_c = _fin(e.get(f"{pe}-{c}-{k}-IC-LO"))
                hi_c = _fin(e.get(f"{pe}-{c}-{k}-IC-HI"))
                if lo_c is None or hi_c is None:
                    continue
                kn += 1
                kk += lo_c <= R[c] <= hi_c
            w = _wilson(kk, kn)
            out[f"{pc}-G-COBERTURA-{k}-K"], out[f"{pc}-G-COBERTURA-{k}-N"] = int(kk), int(kn)
            out[f"{pc}-G-COBERTURA-{k}-IC-LO"], out[f"{pc}-G-COBERTURA-{k}-IC-HI"] = w
        for k in CANDIDATOS:
            out[f"{pc}-G-DENTRO-IC-R-{k}"] = int(sum(
                1 for c in puntuadas if cand[k][c] is not None and ICR[c][0] <= cand[k][c] <= ICR[c][1]))

    out[f"{PA}-G-B-BIS-AGREGADO"] = next((v for v in PRECEDENCIA if v in agregado), "SIN-CRUCES-CON-SOPORTE")
    out[f"{PA}-G-ADOPCION-RETADOR"] = "NINGUNA -- un retador que vence va a FP de adopcion (firma §2)"
    out[f"{PA}-G-FUENTE-C2"] = "CALC-ENCIG2025-PISOS-GOBDIGITAL-0001 (RESULT -C2-P por id; origen NUEVO)"
    out[f"{PA}-G-MARCA-EMISIONES"] = ("C7, C-ENCOGIDA, C-ASTRA y C1 PROSPECTIVA (sellados antes de R); C2 RETROSPECTIVA "
                                      "(piso -0002 sellado despues de R, cruce visto E.6); el IC de C2 NACE-CON-R")
    out[f"{PA}-G-UNIDAD"] = "TRAMITE (pago ordinario de luz, N_TRA=01); no se promedia con cifras por persona"
    out[f"{PA}-G-UMBRAL-PP"] = umbral_pp
    out[f"{PA}-G-INCERTIDUMBRE"] = (
        "R: bootstrap UPM con reposicion dentro de estrato, singleton de certeza, PCG64, percentiles 2.5/97.5, "
        "contrato conservador de la receta; DeltaMAE: puntos de candidatos fijos, replicas de R")
    return out


def adjudicacion(inputs, contrato):
    problemas = auditoria(Path(__file__).read_bytes())
    if problemas:
        raise ParoDeGuardia(f"auditoria del codigo: {problemas}")
    emis = _guardia_sellos(inputs)
    piso = _guardia_piso(inputs)
    payload = _guardia_payload(inputs, contrato)
    par = contrato["parametros"]
    repeticiones = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    receta = _modulo_desde_bytes("receta_cruce_encig", _bytes(inputs, "receta_cruce_encig"))
    estado_gana = _extrae_funcion(_bytes(inputs, "adjudicacion_piloto4"), "_estado_gana", {})
    marg25 = _resultados(_bytes(inputs, "marginales_2025_resultados"))

    def resumen(point, replicas):
        ee, lo, hi, validas = receta._summary(float("nan") if point is None else point, replicas)
        return _fin(ee), _fin(lo), _fin(hi), validas

    frame, diag = _frame_ola(receta, inputs, par["ola"], payload)
    res = _r_y_marginales(receta, frame, repeticiones, semilla)
    out = adjudicar(res, emis, marg25, estado_gana, resumen, par, diag, piso)
    _control_oro_0001(out, _resultados(_bytes(inputs, "adjudicacion_0001_resultados")), float(par["tol_oro_0001"]))
    out[f"{PA}-G-AUDITORIA-CODIGO"] = "LIMPIA"
    out[f"{PA}-G-SELLOS-EMISIONES"] = "COINCIDEN -- " + ",".join(sorted(CRUCES)) + " + piso"
    out[f"{PA}-G-INPUT-PAYLOAD-SHA256"] = str(inputs[payload].get("sha256"))
    for iid in sorted(INPUTS_ADJUDICACION_REPO):
        out[f"{PA}-G-INPUT-{iid.upper().replace('_', '-')}-SHA256"] = str(inputs[iid].get("sha256"))
    out[f"{PA}-G-BOOTSTRAP-REPLICAS"] = repeticiones
    out[f"{PA}-G-SEED"] = semilla
    return out


_DIAG = ("FILAS-EVENTOS", "JOIN-SIN-DEMOGRAFIA", "N-UNIVERSO", "N-DISENO-VALIDO", "P7-3-EXCLUIDAS")


def esquema_adjudicacion():
    f = [_fila(f"{PA}-G-{k}", "entero", "filas") for k in _DIAG]
    f += [_fila(f"{PA}-G-{s}", t, u) for s, t, u in (
        ("CTRL-MARGINALES-MAX-ABS-P", "flotante", "diferencia de proporción"),
        ("CTRL-MARGINALES-N-DISCORDA", "entero", "marginales"),
        ("CTRL-MARGINALES-VEREDICTO", "texto", "categoría"),
        ("B-BIS-AGREGADO", "texto", "veredicto"), ("ADOPCION-RETADOR", "texto", "categoría"),
        ("FUENTE-C2", "texto", "categoría"),
        ("MARCA-EMISIONES", "texto", "categoría"), ("UNIDAD", "texto", "unidad"),
        ("UMBRAL-PP", "flotante", "pp"), ("INCERTIDUMBRE", "texto", "descripción del método"),
        ("AUDITORIA-CODIGO", "texto", "categoría"), ("SELLOS-EMISIONES", "texto", "categoría"),
        ("INPUT-PAYLOAD-SHA256", "texto", "hash sha256"),
        ("BOOTSTRAP-REPLICAS", "entero", "réplicas"), ("SEED", "entero", "semilla"),
        ("CTRL-ORO-0001-MAX-ABS", "flotante", "diferencia absoluta"), ("CTRL-ORO-0001-N", "entero", "ids comparados"),
        ("CTRL-ORO-0001-VEREDICTO", "texto", "categoría"))]
    f += [_fila(f"{PA}-G-INPUT-{iid.upper().replace('_', '-')}-SHA256", "texto", "hash sha256")
          for iid in sorted(INPUTS_ADJUDICACION_REPO)]
    for eje, valores in EJES.items():
        for v in valores:
            b = f"{PA}-M-{eje}-{_cat_publica(eje, v)}"
            f += [_fila(f"{b}-P", "proporcion", "proporción de trámites [0,1]"), _fila(f"{b}-N", "entero", "trámites")]
    f += [_fila(f"{PA}-M-TOTAL-TODOS-P", "proporcion", "proporción de trámites [0,1]"),
          _fila(f"{PA}-M-TOTAL-TODOS-N", "entero", "trámites")]
    for cruce in CRUCES:
        pc = f"{PA}-{cruce}"
        f += [_fila(f"{pc}-G-{s}", t, u) for s, t, u in (
            ("C-ASTRA-ESTADO", "texto", "categoría"), ("N-COMPLETOS", "entero", "trámites"),
            ("RESIDUO-N", "entero", "trámites"), ("CTRL-C2-MAX-ABS", "flotante", "diferencia de proporción"),
            ("CTRL-C2-VEREDICTO", "texto", "categoría"), ("C2-IC-ESTADO", "texto", "categoría"),
            ("PUNTUADAS-N", "entero", "celdas"), ("FALLAN-N", "entero", "celdas"),
            ("FUERA-GLOBAL-UMBRAL", "entero", "celdas"), ("SOPORTE-GLOBAL", "texto", "categoría"),
            ("GANADORES", "texto", "candidatos"), ("PROPUESTAS-CON-RESERVA", "texto", "candidatos"),
            ("B-BIS", "texto", "veredicto"), ("VEREDICTO-CELDA-D", "texto", "veredicto"),
            ("CHAMPION-PROPUESTO", "texto", "candidato"))]
        f += [_fila(f"{pc}-G-MAE-{k}", "flotante", "pp") for k in CANDIDATOS]
        f += [_fila(f"{pc}-G-DENTRO-IC-R-{k}", "entero", "celdas") for k in CANDIDATOS]
        for j in RETADORES:
            q = f"{pc}-G-{j}"
            f += [_fila(f"{q}-{s}", t, u) for s, t, u in (
                ("VENCE-N", "entero", "celdas"), ("INDECIDIBLE-N", "entero", "celdas"),
                ("FRACCION-3-4", "texto", "SI/NO (descriptivo)"),
                ("DELTA-MAE-PP", "flotante", "pp"), ("DELTA-MAE-IC-LO", "flotante", "pp"),
                ("DELTA-MAE-IC-HI", "flotante", "pp"), ("DELTA-MAE-B-VALIDAS", "entero", "réplicas definidas"),
                ("GANA", "texto", "SI/PROPUESTA-CON-RESERVA/NO/NO-ENTRA"))]
        for k in CON_IC_PREVIO:
            q = f"{pc}-G-COBERTURA-{k}"
            f += [_fila(f"{q}-K", "entero", "celdas con R dentro del IC"), _fila(f"{q}-N", "entero", "celdas"),
                  _fila(f"{q}-IC-LO", "proporcion", "Wilson 95% inferior"),
                  _fila(f"{q}-IC-HI", "proporcion", "Wilson 95% superior")]
        for ka, kb in celdas(cruce):
            b = f"{pc}-{rotulo(ka, kb)}"
            f += [_fila(f"{b}-{x[0]}", *x[1:]) for x in (
                ("N-2025", "entero", "trámites"), ("SOPORTE", "texto", "categoría"),
                ("R-P", "proporcion", "proporción de trámites [0,1]"),
                ("R-IC-LO", "proporcion", "límite inferior IC95"), ("R-IC-HI", "proporcion", "límite superior IC95"),
                ("R-EE", "flotante", "(IC95sup - IC95inf)/3.92"), ("R-B-VALIDAS", "entero", "réplicas definidas"),
                ("DELTA-25", "flotante", "logit"),
                ("C2-P", "proporcion", "proporción de trámites [0,1] (punto sellado adoptable)", ["piso_c2_resultados"]),
                ("C2-P-EMISION-0001", "proporcion", "C2 de la emision del -0001 (cadena legacy; descriptiva)"),
                ("C2-IC-LO", "proporcion", "límite inferior por réplica, NACE-CON-R"),
                ("C2-IC-HI", "proporcion", "límite superior por réplica, NACE-CON-R"),
                ("C2-P-RECALCULADO", "proporcion", "control: composición en la ola"))]
            f += [_fila(f"{b}-D-{k}", "flotante", "|candidato - R| pp") for k in CANDIDATOS]
            f += [_fila(f"{b}-VEREDICTO-{j}-VS-C2", "texto", "GANA-CHALLENGER/GANA-PISO/INDECIDIBLE/NO-PUNTUADA/NO-ENTRA")
                  for j in RETADORES]
    return f


# ══════════════════════════════ punto de entrada ══════════════════════════════

def esquema_resultados(punto_de_entrada, cruce=None):
    if punto_de_entrada == "emisiones":
        return esquema_emisiones(cruce)
    if punto_de_entrada == "adjudicacion":
        return esquema_adjudicacion()
    raise ValueError(punto_de_entrada)


def medir(inputs, contrato):
    pde = contrato["parametros"]["punto_de_entrada"]
    if pde == "emisiones":
        return emisiones(inputs, contrato)
    if pde == "adjudicacion":
        return adjudicacion(inputs, contrato)
    raise ParoDeGuardia(f"punto_de_entrada desconocido: {pde}")
