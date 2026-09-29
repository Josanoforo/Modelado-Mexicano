#!/usr/bin/env python3
"""Medidor de APERTURA de los cruces reservados de ENIF 2024 — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (29/sep/2026).

Spec humana: `APERTURA-ENIF-2024-spec-v1_0.md`; contrato: `APERTURA-ENIF-2024-spec.yaml`; receta:
`RECETA-APERTURA-ENIF-2024.md`. NO SE HA CORRIDO sobre ENIF 2024: corre sólo en caja, en el commit de
apertura que mesa autorice.

Alcance (spec §0-§1): las 68 celdas del desenlace SECUNDARIO `informal_cualquiera` en los 9 pares que
`data/corrida0/marcador-segmento.tsv` marca RESERVADA + EMITIDA-SIN-EVALUAR. Las 68 celdas del desenlace
PRINCIPAL `ahorra_solo_informal` de esos mismos pares NO están aquí: su R ya está sellada en
`CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001` (E.5: lo sellado se cita, no se re-mide).

Al abrir: R = Σw·y/Σw de `informal_cualquiera` en ENIF 2024 por celda de cruce, con el universo, el desenlace
y los ejes del árbitro (`tools/medidor_ahorro_enif24.py`, sha fijado, el mismo que usó el contendiente);
cobertura de R en el IC por réplica del piso C2 (`CALC-C2-COMPUESTO-IC-ENIF2024-0001`), punto del piso de
`CALC-C2-COMPUESTO-RESERVADAS-0001`. Guardia E.6: auditoría AST de este archivo antes de leer un byte; el
cruce se agrega con UNA variable de agrupación (etiqueta de celda construida) por
`guardia_apertura.proporcion_por_grupo`, y sólo sobre `CELDAS_AUTORIZADAS`.
"""
from __future__ import annotations

import os
import re
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
X = "ENIF-2024"
P = "RESULT-APERTURA-ENIF-2024"
DESENLACE = "informal_cualquiera (SECUNDARIO)"
UMBRAL_SOPORTE_N = 200  # DIN-lote-enif2024-spec-v1_0.md:175 · CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001/spec.yaml:163


def _comun():
    import importlib.util
    s = importlib.util.spec_from_file_location("expediente_apertura", os.path.join(os.path.dirname(AQUI), "expediente_apertura.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = _comun()
G = E.G

ARBITRO = ("arbitro_medidor", "tools/medidor_ahorro_enif24.py",
           "58c429598c3cedd6d1f8927e8854bbb6f4461f04a94d4a92568a388c7f1f2c95")
ARBITRO_EJES = ("arbitro_ejes", "tools/ejes_maestra35_l1.py",
                "502f5a4138c6733677f9472947cfe8c112dd04618e6ac325dd816758f7206c4d")
ARBITRO_WPROP = ("arbitro_wprop", "tools/calibracion_mordida_encig_serie.py",
                 "b2e636b059538e43c57f4f1a288e028c796ef34965186c5bbb771bea5a462bd3")
PISO_PUNTO = ("piso_c2_emisiones", "data/corrida0/CALC-C2-COMPUESTO-RESERVADAS-0001/resultados.json",
              "be24d879d22d28a05c36441b471976a6b0b3d40f2877efa2cd514a13e5bae3cb")
PISO_IC = ("piso_c2_ic", "data/corrida0/CALC-C2-COMPUESTO-IC-ENIF2024-0001/resultados.json",
           "6d3e449ed3156410777f49fac06ad0d3faecf9397bfa60eb9430117ab993fcb7")
GUARDIA = ("guardia_apertura", "forense/prereg-aperturas/guardia_apertura.py")
COMUN = ("expediente_apertura", "forense/prereg-aperturas/expediente_apertura.py")
PAYLOAD = "enif_2024_enif_2024_bd_csv"
CODIGO_ARBITRO = (ARBITRO, ARBITRO_EJES, ARBITRO_WPROP)

# Par (prefijo del id sellado) -> (eje a, eje b) del árbitro. Nueve pares = las nueve filas
# CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::<a>x<b> con estado RESERVADA y
# emision EMITIDA-SIN-EVALUAR del marcador.
PARES = {
    "CUENTA-FORMALXEDAD": ("cuenta_formal", "edad"),
    "CUENTA-FORMALXESCOLARIDAD": ("cuenta_formal", "escolaridad"),
    "CUENTA-FORMALXLOCALIDAD": ("cuenta_formal", "localidad"),
    "CUENTA-FORMALXSEXO": ("cuenta_formal", "sexo"),
    "EDADXESCOLARIDAD": ("edad", "escolaridad"),
    "EDADXSEXO": ("edad", "sexo"),
    "ESCOLARIDADXLOCALIDAD": ("escolaridad", "localidad"),
    "ESCOLARIDADXSEXO": ("escolaridad", "sexo"),
    "LOCALIDADXSEXO": ("localidad", "sexo"),
}

# Lista CERRADA: las 68 celdas `informal_cualquiera` con IC por réplica en CALC-C2-COMPUESTO-IC-ENIF2024-0001
# (ids RESULT-C2IC-ENIF2024-INFORMAL-CUALQUIERA-<celda>-IC95INF). Ninguna otra se computa.
CELDAS_AUTORIZADAS = (
    "CUENTA-FORMALXEDAD-CON-CUENTA-X-18-29", "CUENTA-FORMALXEDAD-CON-CUENTA-X-30-44",
    "CUENTA-FORMALXEDAD-CON-CUENTA-X-45-59", "CUENTA-FORMALXEDAD-CON-CUENTA-X-60",
    "CUENTA-FORMALXEDAD-SIN-CUENTA-X-18-29", "CUENTA-FORMALXEDAD-SIN-CUENTA-X-30-44",
    "CUENTA-FORMALXEDAD-SIN-CUENTA-X-45-59", "CUENTA-FORMALXEDAD-SIN-CUENTA-X-60",
    "CUENTA-FORMALXESCOLARIDAD-CON-CUENTA-X-HASTA-PRIMARIA", "CUENTA-FORMALXESCOLARIDAD-CON-CUENTA-X-MEDIA-SUPERIOR",
    "CUENTA-FORMALXESCOLARIDAD-CON-CUENTA-X-SECUNDARIA", "CUENTA-FORMALXESCOLARIDAD-CON-CUENTA-X-SUPERIOR",
    "CUENTA-FORMALXESCOLARIDAD-SIN-CUENTA-X-HASTA-PRIMARIA", "CUENTA-FORMALXESCOLARIDAD-SIN-CUENTA-X-MEDIA-SUPERIOR",
    "CUENTA-FORMALXESCOLARIDAD-SIN-CUENTA-X-SECUNDARIA", "CUENTA-FORMALXESCOLARIDAD-SIN-CUENTA-X-SUPERIOR",
    "CUENTA-FORMALXLOCALIDAD-CON-CUENTA-X-15-000-Y-MAS", "CUENTA-FORMALXLOCALIDAD-CON-CUENTA-X-MENOR-DE-15-000",
    "CUENTA-FORMALXLOCALIDAD-SIN-CUENTA-X-15-000-Y-MAS", "CUENTA-FORMALXLOCALIDAD-SIN-CUENTA-X-MENOR-DE-15-000",
    "CUENTA-FORMALXSEXO-CON-CUENTA-X-1-HOMBRE", "CUENTA-FORMALXSEXO-CON-CUENTA-X-2-MUJER",
    "CUENTA-FORMALXSEXO-SIN-CUENTA-X-1-HOMBRE", "CUENTA-FORMALXSEXO-SIN-CUENTA-X-2-MUJER",
    "EDADXESCOLARIDAD-18-29-X-HASTA-PRIMARIA", "EDADXESCOLARIDAD-18-29-X-MEDIA-SUPERIOR",
    "EDADXESCOLARIDAD-18-29-X-SECUNDARIA", "EDADXESCOLARIDAD-18-29-X-SUPERIOR",
    "EDADXESCOLARIDAD-30-44-X-HASTA-PRIMARIA", "EDADXESCOLARIDAD-30-44-X-MEDIA-SUPERIOR",
    "EDADXESCOLARIDAD-30-44-X-SECUNDARIA", "EDADXESCOLARIDAD-30-44-X-SUPERIOR",
    "EDADXESCOLARIDAD-45-59-X-HASTA-PRIMARIA", "EDADXESCOLARIDAD-45-59-X-MEDIA-SUPERIOR",
    "EDADXESCOLARIDAD-45-59-X-SECUNDARIA", "EDADXESCOLARIDAD-45-59-X-SUPERIOR",
    "EDADXESCOLARIDAD-60-X-HASTA-PRIMARIA", "EDADXESCOLARIDAD-60-X-MEDIA-SUPERIOR",
    "EDADXESCOLARIDAD-60-X-SECUNDARIA", "EDADXESCOLARIDAD-60-X-SUPERIOR",
    "EDADXSEXO-18-29-X-1-HOMBRE", "EDADXSEXO-18-29-X-2-MUJER", "EDADXSEXO-30-44-X-1-HOMBRE",
    "EDADXSEXO-30-44-X-2-MUJER", "EDADXSEXO-45-59-X-1-HOMBRE", "EDADXSEXO-45-59-X-2-MUJER",
    "EDADXSEXO-60-X-1-HOMBRE", "EDADXSEXO-60-X-2-MUJER",
    "ESCOLARIDADXLOCALIDAD-HASTA-PRIMARIA-X-15-000-Y-MAS", "ESCOLARIDADXLOCALIDAD-HASTA-PRIMARIA-X-MENOR-DE-15-000",
    "ESCOLARIDADXLOCALIDAD-MEDIA-SUPERIOR-X-15-000-Y-MAS", "ESCOLARIDADXLOCALIDAD-MEDIA-SUPERIOR-X-MENOR-DE-15-000",
    "ESCOLARIDADXLOCALIDAD-SECUNDARIA-X-15-000-Y-MAS", "ESCOLARIDADXLOCALIDAD-SECUNDARIA-X-MENOR-DE-15-000",
    "ESCOLARIDADXLOCALIDAD-SUPERIOR-X-15-000-Y-MAS", "ESCOLARIDADXLOCALIDAD-SUPERIOR-X-MENOR-DE-15-000",
    "ESCOLARIDADXSEXO-HASTA-PRIMARIA-X-1-HOMBRE", "ESCOLARIDADXSEXO-HASTA-PRIMARIA-X-2-MUJER",
    "ESCOLARIDADXSEXO-MEDIA-SUPERIOR-X-1-HOMBRE", "ESCOLARIDADXSEXO-MEDIA-SUPERIOR-X-2-MUJER",
    "ESCOLARIDADXSEXO-SECUNDARIA-X-1-HOMBRE", "ESCOLARIDADXSEXO-SECUNDARIA-X-2-MUJER",
    "ESCOLARIDADXSEXO-SUPERIOR-X-1-HOMBRE", "ESCOLARIDADXSEXO-SUPERIOR-X-2-MUJER",
    "LOCALIDADXSEXO-15-000-Y-MAS-X-1-HOMBRE", "LOCALIDADXSEXO-15-000-Y-MAS-X-2-MUJER",
    "LOCALIDADXSEXO-MENOR-DE-15-000-X-1-HOMBRE", "LOCALIDADXSEXO-MENOR-DE-15-000-X-2-MUJER",
)
_AUTORIZADAS = frozenset(CELDAS_AUTORIZADAS)

CONTRATO = {
    "x": X, "programa": "ENIF", "ola": "2024", "unidad": "PERSONA",
    "contendientes": ["CALC-C2-COMPUESTO-RESERVADAS-0001", "CALC-C2-COMPUESTO-IC-ENIF2024-0001"],
    "payloads": [(PAYLOAD, "ENIF 2024 bd csv (TMODULO.csv) -- el que leyó el árbitro y el contendiente; payload sin "
                           "estado_reserva: la reserva es de CELDA (marcador), y sólo este medidor cruza "
                           "informal_cualquiera por par")],
    "repo": [(ARBITRO[0], ARBITRO[1], "árbitro: carga() (universo y guardias), desenlaces(), EJES_P2, EJE_CUENTA_SECUNDARIO"),
             (ARBITRO_EJES[0], ARBITRO_EJES[1], "Eje, tramos_edad, codificaciones (importado por el árbitro)"),
             (ARBITRO_WPROP[0], ARBITRO_WPROP[1], "wprop_ic_conglomerado (importado por el árbitro; aquí no se usa)"),
             (PISO_PUNTO[0], PISO_PUNTO[1], "punto sellado del piso C2 por celda (RESULT-C2COMP-INFORMAL-CUALQUIERA-*)"),
             (PISO_IC[0], PISO_IC[1], "IC95 por réplica sellado del piso C2 por celda (RESULT-C2IC-ENIF2024-INFORMAL-CUALQUIERA-*)"),
             (GUARDIA[0], GUARDIA[1], "auditoría AST, agregador de una variable, adjudicación"),
             (COMUN[0], COMUN[1], "esquema, salida y contrato comunes")],
    "universo": "Personas elegidas de 18 años y más de TMODULO de ENIF 2024, universo de carga() del árbitro "
                "(EDAD_V numérica >= 18, FAC_PER > 0, alguna de las 15 variables de la sección 5 no en blanco; "
                "cualquier violación PARA). Una fila por persona.",
    "filtros": "Ninguno adicional al árbitro. Por par, la persona entra a la celda si sus dos ejes caen en categorías "
               "de la rejilla ((fuera) en cualquiera de los dos -> fuera de ese par) y la celda está en "
               "CELDAS_AUTORIZADAS. Soporte: celda con n < 200 personas sin ponderar -> R NO-ESTIMABLE (no puntúa).",
    "ponderador": "FAC_PER",
    "transformacion": "informal_cualquiera = alguna P5_1_1..P5_1_6 == '1' (árbitro desenlaces(), SECUNDARIO). Ejes del "
                      "árbitro: sexo SEXO; edad EDAD_V en 18-29/30-44/45-59/60+ (60-96; 97+ fuera); escolaridad NIV por "
                      "ESC_ENIF (99 fuera); localidad TLOC {1,2}=15 000 y mas, {3,4}=menor de 15 000; cuenta_formal "
                      "alguna P5_4_k == '1' vs ninguna (todas en blanco fuera). Etiqueta de celda = "
                      "<PAR>-<slug(a)>-X-<slug(b)>, UNA variable de agrupación.",
    "estimando": "R(a,b) = Σ FAC_PER·informal_cualquiera / Σ FAC_PER por celda de los 9 pares (68 celdas), proporción "
                 "[0,1] de personas elegidas 18+; cobertura de R en el IC95 por réplica del piso C2 (primaria); error "
                 "absoluto medio punto-del-piso vs R (descriptivo)",
    "variables": [{"nombre": v, "definicion": d} for v, d in (
        ("P5_1_1..P5_1_6", "vías informales de ahorro; desenlace informal_cualquiera"),
        ("P5_6_1..P5_6_9", "vías formales (sólo para las guardias de carga() del árbitro)"),
        ("P5_4_1..P5_4_9", "tenencia de cuenta; eje cuenta_formal"),
        ("SEXO", "eje sexo"), ("EDAD_V", "eje edad y guardia >= 18"), ("NIV", "eje escolaridad"),
        ("TLOC", "eje localidad"), ("FAC_PER", "ponderador"), ("EST_DIS", "estrato (sólo identidad)"),
        ("UPM_DIS", "UPM (sólo identidad)"))],
}


# ── rejilla y piso sellado ──────────────────────────────────────────────────
def slug(s) -> str:
    """Misma regla que `tools/c2_compuesto.py::_slug` (la que acuñó los ids sellados)."""
    return re.sub(r"[^A-Z0-9]+", "-", str(s).upper()).strip("-")


def esquema_resultados():
    return E.esquema(P, list(CELDAS_AUTORIZADAS))


def piso_sellado(inputs=None) -> dict:
    """{celda: (punto, lo, hi)} del piso C2, de los dos resultados.json sellados (sha fijado)."""
    punto = E.json_repo(inputs, *PISO_PUNTO)["resultados"]
    ic = E.json_repo(inputs, *PISO_IC)["resultados"]
    out = {}
    for c in CELDAS_AUTORIZADAS:
        base = f"RESULT-C2IC-ENIF2024-INFORMAL-CUALQUIERA-{c}"
        out[c] = (punto.get(f"RESULT-C2COMP-INFORMAL-CUALQUIERA-{c}"), ic.get(f"{base}-IC95INF"), ic.get(f"{base}-IC95SUP"))
    return out


def filas(piso: dict, r: dict) -> list[dict]:
    return [{"id": c, "conglomerado": _par_de(c),
             "punto": piso[c][0], "lo": piso[c][1], "hi": piso[c][2], "r": r.get(c)} for c in CELDAS_AUTORIZADAS]


def _par_de(celda: str) -> str:
    for par in PARES:
        if celda.startswith(par + "-"):
            return par
    raise G.ParoDeGuardia(f"celda sin par conocido: {celda}")


# ── código del árbitro (sha fijado; se importa desde su ruta para que sus imports resuelvan) ─────────
def arbitro(inputs=None):
    for clave, rel, sha in CODIGO_ARBITRO:
        E.bytes_repo(inputs, clave, rel, sha)
        if E.sha256_de(rel) != sha:
            raise G.ParoDeGuardia(f"sha discordante en disco: {rel}")
    tools = os.path.join(E.RAIZ, "tools")
    if tools not in sys.path:
        sys.path.insert(0, tools)
    return E.carga(os.path.join(E.RAIZ, ARBITRO[1]), "medidor_ahorro_enif24_apertura")


def columnas_usadas(A) -> list[str]:
    """Las únicas columnas que sobreviven a la lectura (spec §2). Ninguna del módulo 7 (firma R06: RESERVADA)."""
    return list(A.INFORMAL) + list(A.FORMAL) + list(A.CUENTAS) + [
        "SEXO", "EDAD_V", "NIV", "TLOC", "FAC_PER", "EST_DIS", "UPM_DIS", "_w", "_edad"]


def lee_payload_reservado(A, ruta):
    """Única lectura de la ola: `carga()` del árbitro sobre el zip que corrida0 resolvió (la auditoría AST lo exige);
    sólo sobreviven `columnas_usadas` — el resto de TMODULO (módulo 7 incluido) se descarta sin agregarse."""
    A.ZIP = ruta
    try:
        df = A.carga()
    except SystemExit as e:  # las guardias del árbitro PARAN con SystemExit
        raise G.ParoDeGuardia(f"guardia del árbitro: {e}") from None
    faltan = [c for c in columnas_usadas(A) if c not in df.columns]
    if faltan:
        raise G.ParoDeGuardia(f"faltan columnas de eje en TMODULO.csv: {faltan}")
    return df[columnas_usadas(A)].copy()


# ── R con UNA variable de agrupación ────────────────────────────────────────
def etiquetas_de_par(par: str, va, vb, fuera: str) -> np.ndarray:
    """Vector 1-D de etiquetas de celda del par; None si algún eje es (fuera) o la celda no está autorizada."""
    sa = {v: slug(v) for v in set(va)}
    sb = {v: slug(v) for v in set(vb)}
    out = np.empty(len(va), dtype=object)
    for i, (a, b) in enumerate(zip(va, vb)):
        lab = None if (a == fuera or b == fuera) else f"{par}-{sa[a]}-X-{sb[b]}"
        out[i] = lab if lab in _AUTORIZADAS else None
    return out


def r_por_celda(y, w, etiquetas, pedidas) -> dict:
    """{celda: R} sólo para `pedidas` ⊆ CELDAS_AUTORIZADAS (otra -> ParoDeGuardia); n < 200 -> None."""
    ajenas = sorted(set(pedidas) - _AUTORIZADAS)
    if ajenas:
        raise G.ParoDeGuardia(f"celdas fuera de CELDAS_AUTORIZADAS: {ajenas}")
    agregado = G.proporcion_por_grupo(y, w, etiquetas)
    out = {}
    for c in pedidas:
        a = agregado.get(c)
        out[c] = a["p"] if a and a["n"] >= UMBRAL_SOPORTE_N else None
    return out


def mide_r(A, df, pedidas=CELDAS_AUTORIZADAS) -> dict:
    ejes = {e.nombre: e for e in A.EJES_P2}
    ejes["cuenta_formal"] = A.EJE_CUENTA_SECUNDARIO
    y = np.asarray(A.desenlaces(df)[DESENLACE], dtype=float)
    w = np.asarray(df["_w"], dtype=float)
    vals = {n: [str(v) for v in ejes[n].deriva(df).tolist()] for n in ("sexo", "edad", "escolaridad", "localidad", "cuenta_formal")}
    out = {}
    for par, (a, b) in PARES.items():
        del_par = [c for c in pedidas if c.startswith(par + "-")]
        if del_par:
            out.update(r_por_celda(y, w, etiquetas_de_par(par, vals[a], vals[b], A.FUERA), del_par))
    return out


def ramas_sinteticas() -> list[dict]:
    """Salida de cada rama terminal, con el piso sellado y R sintética (no abre dato): todas con soporte,
    parcial, cero puntuadas, réplica degenerada (IC del piso ausente)."""
    piso = piso_sellado()
    rng = np.random.default_rng(2024)
    todas = {c: float(rng.uniform(0.2, 0.8)) for c in CELDAS_AUTORIZADAS}
    parcial = {c: (v if i % 3 else None) for i, (c, v) in enumerate(todas.items())}
    degenerado = {c: (None, None, None) if i % 2 else v for i, (c, v) in enumerate(piso.items())}
    return [E.salida(P, filas(piso, todas)), E.salida(P, filas(piso, parcial)),
            E.salida(P, filas(piso, {})), E.salida(P, filas(degenerado, todas))]


def medir(inputs, contrato):
    G.exige_auditoria(open(os.path.abspath(__file__), encoding="utf-8").read())
    esperados = {PAYLOAD} | {k for k, _r, _n in CONTRATO["repo"]}
    if set(inputs) != esperados:
        raise G.ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    for clave, rel, sha in (GUARDIA + (E.sha256_de(GUARDIA[1]),), COMUN + (E.sha256_de(COMUN[1]),)):
        E.bytes_repo(inputs, clave, rel, sha)
    piso = piso_sellado(inputs)
    A = arbitro(inputs)
    df = lee_payload_reservado(A, inputs[PAYLOAD]["ruta_absoluta"])
    return E.salida(P, filas(piso, mide_r(A, df)))
