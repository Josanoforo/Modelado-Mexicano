#!/usr/bin/env python3
r"""Extractor congelado de `valor_extraido` para las 224 capturas reales de
`forense/prereg-duelo-v2/corridas-L/*__v1_3.json` (marco v1.3, `ACTO
GEN2-F5-RECAPTURA-L`, `PR #669`).

ACTO: GEN2-F5-EXTRACTOR-L-v1 (nube). Este es el sucesor de
`tools/extrae_l_v1_1.py` para el formato real de estas capturas -- prosa
libre, sin encabezados fijos, mayoritariamente rechazos explícitos de
estimación que citan cifras de contexto ("cifra negra" de la ENVIPE) como
conocimiento general, NO como respuesta. `extrae_l_v1_1.py` no se edita: su
regla (encabezado "estimaci" -> si no hay, primer número del documento
completo) no está calibrada contra este formato y, medido a mano por `ACTO
GEN2-F5-DUELO-CALC` (`PR #674`, `NC-0142`), captura esas cifras de contexto
como si fueran la estimación pedida en el 61% de las 96 capturas de las 6
celdas con árbitro.

*** Este script NO edita ninguna captura. *** Solo lee
`corridas-L/*__v1_3.json` y el manifiesto de capturas
(`manifiesto-capturas-P3-v1_0.json`). No llama a ningún modelo. No re-corre
L. No abre `CALC-R-*/`, `corridas-R/`, ningún resultado del duelo
(`CALC-DUELO-*/`) ni ningún archivo de error contra R -- la regla de
extracción no depende del valor de R, de M, ni del error resultante
(control de independencia, P2 del encargo).

────────────────────────────────────────────────────────────────────────
REGLA DE EXTRACCIÓN, CONGELADA (P1, COMMIT-1 -- no se edita después de ver
el resultado sobre las 224 capturas; ver
`forense/prereg-duelo-v2/regla-extraccion-L-v1_3.md` para la prosa completa
de esta misma regla, con ejemplos).
────────────────────────────────────────────────────────────────────────

Prohibido, por diseño de esta regla: el fallback "primer número del
documento completo". Toda cifra que este extractor emite está ligada, por
estructura (un encabezado Markdown de sección "## ... estimaci ...") o por
texto (una de un conjunto fijo de frases-ancla: "estimación puntual", "mi
punto", "punto central"), a la respuesta/estimación solicitada -- nunca a
la posición en el documento.

Paso 0 -- IDENTIDAD (antes de cualquier extracción). El nombre de archivo
codifica `id_celda`, `variante` e `índice` (`L-<id_celda>-M__<variante>__
<índice>__v1_3.json`). Se verifica que: (a) el archivo aparece en el
manifiesto sellado de `F5-RECAPTURA-L`; (b) su sha256 coincide con el que
el manifiesto declara; (c) `id_celda`/`variante`/`indice` dentro del JSON
coinciden con lo que el nombre de archivo y el manifiesto declaran. Un
fallo en (a)/(b)/(c) es `estado = ERROR-IDENTIDAD` -- un fallo material
distinto de "no se pudo extraer", y no se intenta extracción sobre ese
archivo.

Paso 1 -- ANCLAS. Se buscan, en todo `texto_crudo`, dos familias de ancla,
sin preferencia mecánica de una sobre otra (se combinan, nunca se usa
"la primera que aparece" como criterio de desempate):

  Familia H (encabezado). Todo encabezado Markdown (`^#+\s*...`) cuyo
  título contenga "estimaci" (insensible a mayúsculas/acentos). La sección
  que gobierna es el texto entre el fin de ese encabezado y el siguiente
  encabezado de nivel igual o menor (o el fin del documento). Dentro de la
  sección, se examina párrafo por párrafo (split por línea en blanco):
  un párrafo que contenga alguna de las frases de EXCLUSIÓN POR
  INCERTIDUMBRE (§ abajo) se descarta como candidato de punto -- es banda,
  no estimación puntual. De los párrafos no descartados, se extrae el
  primer número con `≈`, o el primer porcentaje/rango/decimal-en-[0,1]
  (§ normalización). Si ningún párrafo trae número pero alguno trae una
  palabra de RECHAZO (§ abajo), la sección es un candidato de rechazo.

  Familia F (frase-ancla). Toda ocurrencia de una de las frases fijas:
  "estimación puntual", "mi punto", "punto central" (insensible a
  acentos/mayúsculas, tolera markdown `**`/`:`/`|` interpuesto). Se toma
  una ventana de los 140 caracteres siguientes a la frase, limpiando
  marcadores de markdown/tabla al inicio. Si la ventana trae, dentro de
  sus primeros ~90 caracteres, una palabra de RECHAZO sin número
  precedente, es un candidato de rechazo. Si trae un número (dentro de
  los primeros ~50 caracteres), es un candidato numérico -- si la MISMA
  ventana trae además un sub-valor etiquetado "mi punto: N%", ese
  sub-valor gana sobre cualquier rango en la misma ventana (regla
  congelada de desempate intra-ventana, no post-hoc: una frase-ancla que
  da un rango Y un punto declarado usa el punto declarado).

Paso 2 -- VEREDICTO, combinando TODAS las anclas encontradas (ambas
familias, todas las ocurrencias):

  - Ninguna ancla con contenido evaluable -> `NO-EXTRAIBLE`,
    regla = `SIN-ANCLA` (nunca se cae al documento completo).
  - Todas las anclas informativas son de RECHAZO (una o más, sin ningún
    candidato numérico) -> `NO-EXTRAIBLE`, regla = `ANCLA-RECHAZO`.
  - Todas las anclas informativas son NUMÉRICAS y coinciden en el mismo
    valor (tolerancia 1e-6) -> `EXTRAIBLE`, regla = `ANCLA-HEADER-PUNTO` o
    `ANCLA-FRASE-PUNTO` según cuál familia aportó el valor citado como
    evidencia (se cita la última ancla informativa, por ser típicamente la
    respuesta final estructurada del documento).
  - Cualquier mezcla de RECHAZO + NUMÉRICO, o dos o más NUMÉRICOS que
    difieren, o una ventana con dos números no resueltos por la regla de
    desempate -> `AMBIGUA`, regla = `ANCLAS-EN-CONFLICTO` -- el formato no
    permite decidir mecánicamente cuál es la respuesta (regla explícita del
    encargo: no se elige entre candidatos después de verlos).

Normalización de porcentajes/probabilidades (congelada, única): un
porcentaje `NN(.N)?%` -> valor/100. Un rango `A%-B%`/`A%–B%`/`A%—B%` sin
sub-valor de punto explícito en la misma ventana/párrafo -> punto medio
((A+B)/2)/100. Un decimal ya en `[0,1]` sin signo `%` (p.ej. `0.42`) -> se
usa tal cual, siempre que sea `<= 1.0` (un decimal `> 1.0` sin `%` no es
una proporción válida bajo esta escala y no se acepta como candidato
numérico de esta regla).

EXCLUSIÓN POR INCERTIDUMBRE (un párrafo/ventana que las contenga no es un
candidato de punto, es banda): "rango subjetivo", "intervalo subjetivo",
"rango de incertidumbre", "intervalo de incertidumbre", "banda de
incertidumbre", "ic subjetivo", "ic95", "ic 95", "intervalo de confianza",
"confianza del", "margen de error".

RECHAZO (lista fija, subcadenas insensibles a mayúsculas/acentos): ver
`_RECHAZO_KW` abajo -- incluye "ninguna", "no estimad", "no proporcionad",
"no disponible", "no emitid", "no la doy", "no lo doy", "no doy una",
"no verificable", "sin estimar", "dato desconocido", "no confirmable",
"no confirmad", "no definid", "sin datos suficientes", "n/a", "no aplica",
"no cuento con", "abstenci", "no ofrezco", "no ofrec", "no defendible",
"no puedo dar", "sin base", "no la tengo", "no lo tengo", "no disponemos",
"sin dato", "no hay estimaci", "no existe estimaci", "sin cifra".

Nada de esta regla depende del valor de R, de M, ni del error resultante:
opera exclusivamente sobre `texto_crudo` y la identidad declarada de la
captura.

Uso:
    python3 tools/extrae_l_v1_3.py
        -- aplica la regla a las 224 capturas `corridas-L/*__v1_3.json`,
           verifica identidad contra el manifiesto, escribe
           `forense/prereg-duelo-v2/L-extraido-v1_3.tsv` y el manifiesto de
           extracción `forense/prereg-duelo-v2/manifiesto-extraccion-L-
           v1_3.json`, e imprime el resumen de cobertura (P2).
    python3 tools/extrae_l_v1_3.py --solo-reporte
        -- igual, pero no escribe archivos (para inspección).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR_PAQUETE = ROOT / "forense" / "prereg-duelo-v2"
CORRIDAS_L = DIR_PAQUETE / "corridas-L"
MANIFIESTO_CAPTURAS = DIR_PAQUETE / "manifiesto-capturas-P3-v1_0.json"
SALIDA_TSV = DIR_PAQUETE / "L-extraido-v1_3.tsv"
SALIDA_MANIFIESTO = DIR_PAQUETE / "manifiesto-extraccion-L-v1_3.json"

CELDAS_ESPERADAS = 14
VARIANTES_ESPERADAS = ("L-solo", "L+corpus")
REPLICAS_ESPERADAS = 8
TOTAL_ESPERADO = CELDAS_ESPERADAS * len(VARIANTES_ESPERADAS) * REPLICAS_ESPERADAS  # 224

# --- vocabulario congelado --------------------------------------------------

_RECHAZO_KW = [
    "ninguna", "no estimad", "no proporcionad", "no disponible", "no emitid",
    "no la doy", "no lo doy", "no doy una", "no verificable", "sin estimar",
    "dato desconocido", "no confirmable", "no confirmad", "no definid",
    "sin datos suficientes", "n/a", "no aplica", "no cuento con", "abstenci",
    "no ofrezco", "no ofrec", "no defendible", "no puedo dar", "sin base",
    "no la tengo", "no lo tengo", "no disponemos", "sin dato",
    "no hay estimaci", "no existe estimaci", "sin cifra",
    "no voy a inventar", "no voy a fabricar", "no la voy a inventar",
    "no la voy a fabricar", "no lo voy a inventar", "no lo voy a fabricar",
    "no debe registrarse", "no debe usarse", "no debe convertirse",
    "no debe tratarse", "no debe sustituir",
    "me abstengo", "nos abstenemos",
]

_EXCLUSION_INCERTIDUMBRE_KW = [
    "rango subjetivo", "intervalo subjetivo", "rango de incertidumbre",
    "intervalo de incertidumbre", "banda de incertidumbre", "ic subjetivo",
    "ic95", "ic 95", "intervalo de confianza", "confianza del",
    "margen de error",
]

# ENMIENDA (misma sesión, tras correr sobre el universo real de 224 y
# encontrar dos falsos-AMBIGUA: FAM-M-05__L+corpus__{01,08}). La sección de
# un encabezado "estimaci..." trae, de forma consistente en el corpus, un
# patrón "punto -> banda -> razonamiento/fuente -> nota" -- los párrafos de
# razonamiento citan cifras HISTÓRICAS/de contexto ("las estimaciones
# oscilan entre ~4% y ~7%") que no son un segundo punto del modelo, y el
# extractor viejo (v1_1) ya había fallado por confundir contexto con
# respuesta -- no se repite ese defecto aquí solo con otro nombre. Un
# párrafo cuyo contenido (sin marcadores markdown) EMPIEZA con una de estas
# etiquetas fijas cierra el escaneo de la sección: los párrafos posteriores
# nunca se examinan en busca de un candidato de punto. No es una regla
# elegida después de ver el resultado sobre R/M -- ninguna de las dos se ha
# abierto en este acto -- es una corrección de la regla de identificación
# de FORMATO, igual que las líneas de arriba.
_ETIQUETAS_FIN_DE_PUNTO = [
    "razonamiento", "sonda canario", "fuente", "nota", "declaracion",
    "advertencia", "advertencias", "base del calculo", "base del razonamiento",
    "recomendacion", "recomendaciones",
]


def _empieza_con_etiqueta_fin(parrafo_norm: str) -> bool:
    limpio = parrafo_norm.lstrip("*_# \t-").strip()
    return any(limpio.startswith(etq) for etq in _ETIQUETAS_FIN_DE_PUNTO)

_FRASES_ANCLA = [
    r"estimaci[oó]n\s+puntual",
    r"\bmi\s+punto\b",
    r"\bpunto\s+central\b",
]

_NUM = r"\d{1,3}(?:[.,]\d+)?"
RE_ENCABEZADO = re.compile(r"^(#+)\s*(.+?)\s*$", re.MULTILINE)
RE_FRASE_ANCLA = re.compile("(?:" + "|".join(_FRASES_ANCLA) + ")", re.IGNORECASE)
RE_MI_PUNTO_VALOR = re.compile(rf"mi\s+punto\s*[:\*\s]*({_NUM})\s*%", re.IGNORECASE)
RE_APROX_PCT = re.compile(rf"[≈~]\s*({_NUM})\s*%")
RE_RANGO_PCT = re.compile(rf"({_NUM})\s*%?\s*[-–—]\s*({_NUM})\s*%")
RE_PCT_SIMPLE = re.compile(rf"({_NUM})\s*%")
RE_DECIMAL01 = re.compile(rf"(0[.,]\d+)(?!\s*%)")


def _sin_acentos(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def _norm(s: str) -> str:
    return _sin_acentos(s).lower()


def _contiene_alguna(texto_norm: str, palabras: list[str]) -> bool:
    return any(p in texto_norm for p in palabras)


def _parsear_numero_de_parrafo(parrafo: str) -> float | None:
    """Aplica la normalización congelada a UN párrafo/ventana ya filtrado
    de exclusiones de incertidumbre. Devuelve el valor en [0,1] o None."""
    m = RE_MI_PUNTO_VALOR.search(parrafo)
    if m:
        return float(m.group(1).replace(",", ".")) / 100.0
    m = RE_APROX_PCT.search(parrafo)
    if m:
        return float(m.group(1).replace(",", ".")) / 100.0
    m = RE_RANGO_PCT.search(parrafo)
    if m:
        a = float(m.group(1).replace(",", "."))
        b = float(m.group(2).replace(",", "."))
        return ((a + b) / 2.0) / 100.0
    m = RE_PCT_SIMPLE.search(parrafo)
    if m:
        return float(m.group(1).replace(",", ".")) / 100.0
    m = RE_DECIMAL01.search(parrafo)
    if m:
        val = float(m.group(1).replace(",", "."))
        if val <= 1.0:
            return val
    return None


@dataclass
class Ancla:
    familia: str  # "H" o "F"
    tipo: str  # "NUMERO" | "RECHAZO" | "CONFLICTO"
    valor: float | None
    evidencia: str


def _anclas_familia_h(texto: str) -> list[Ancla]:
    anclas: list[Ancla] = []
    encabezados = list(RE_ENCABEZADO.finditer(texto))
    for i, m in enumerate(encabezados):
        nivel, titulo = m.group(1), m.group(2)
        if "estimaci" not in _norm(titulo):
            continue
        inicio = m.end()
        fin = len(texto)
        for m2 in encabezados[i + 1:]:
            if len(m2.group(1)) <= len(nivel):
                fin = m2.start()
                break
        seccion = texto[inicio:fin]
        parrafos = [p.strip() for p in seccion.split("\n\n") if p.strip()]
        valores: list[tuple[float, str]] = []
        hubo_rechazo = False
        evidencia_rechazo = ""
        for parrafo in parrafos:
            parrafo_norm = _norm(parrafo)
            if _empieza_con_etiqueta_fin(parrafo_norm):
                break
            if _contiene_alguna(parrafo_norm, _EXCLUSION_INCERTIDUMBRE_KW):
                continue
            val = _parsear_numero_de_parrafo(parrafo)
            if val is not None:
                valores.append((val, _fragmento(parrafo)))
            elif _contiene_alguna(parrafo_norm, _RECHAZO_KW):
                hubo_rechazo = True
                evidencia_rechazo = _fragmento(parrafo)
        distintos = sorted({round(v, 6) for v, _ in valores})
        if len(distintos) > 1:
            anclas.append(Ancla("H", "CONFLICTO", None, _fragmento(seccion)))
        elif len(distintos) == 1:
            evidencia = next(frag for v, frag in valores if round(v, 6) == distintos[0])
            anclas.append(Ancla("H", "NUMERO", distintos[0], evidencia))
        elif hubo_rechazo:
            anclas.append(Ancla("H", "RECHAZO", None, evidencia_rechazo))
    return anclas


def _fragmento(s: str) -> str:
    return " ".join(s.split())[:220]


def _anclas_familia_f(texto: str) -> list[Ancla]:
    anclas: list[Ancla] = []
    for m in RE_FRASE_ANCLA.finditer(texto):
        ventana_cruda = texto[m.end(): m.end() + 140]
        ventana = ventana_cruda.lstrip(" \t\n*|:_-")
        ventana_norm = _norm(ventana)
        val = _parsear_numero_de_parrafo(ventana[:60])
        rechazo = _contiene_alguna(ventana_norm[:90], _RECHAZO_KW)
        if val is not None and rechazo:
            anclas.append(Ancla("F", "CONFLICTO", None, _fragmento(m.group(0) + ventana)))
        elif val is not None:
            anclas.append(Ancla("F", "NUMERO", val, _fragmento(m.group(0) + ventana)))
        elif rechazo:
            anclas.append(Ancla("F", "RECHAZO", None, _fragmento(m.group(0) + ventana)))
        # ninguna de las dos: ancla no informativa, se descarta (no se cuenta)
    return anclas


@dataclass
class Extraccion:
    estado: str  # EXTRAIBLE | NO-EXTRAIBLE | AMBIGUA
    valor_extraido: float | None
    evidencia_textual: str
    regla_de_extraccion: str
    razon_no_extraible: str


def extraer_valor(texto_crudo: str) -> Extraccion:
    anclas = _anclas_familia_h(texto_crudo) + _anclas_familia_f(texto_crudo)
    informativas = [a for a in anclas if a.tipo in ("NUMERO", "RECHAZO", "CONFLICTO")]

    if not informativas:
        return Extraccion(
            "NO-EXTRAIBLE", None, "",
            "SIN-ANCLA",
            "ningun encabezado 'estimaci...' ni frase-ancla "
            "(estimacion puntual / mi punto / punto central) con "
            "contenido evaluable (numero o rechazo explicito)",
        )

    if any(a.tipo == "CONFLICTO" for a in informativas):
        ev = "; ".join(a.evidencia for a in informativas if a.tipo == "CONFLICTO")
        return Extraccion("AMBIGUA", None, ev, "ANCLAS-EN-CONFLICTO",
                           "una ventana/seccion trae mas de un candidato numerico "
                           "sin regla de desempate, o numero y rechazo a la vez")

    numericas = [a for a in informativas if a.tipo == "NUMERO"]
    rechazos = [a for a in informativas if a.tipo == "RECHAZO"]

    if numericas and rechazos:
        ev = "; ".join(a.evidencia for a in informativas)
        return Extraccion("AMBIGUA", None, ev, "ANCLAS-EN-CONFLICTO",
                           "al menos una ancla numerica y al menos una ancla de "
                           "rechazo, el formato no permite decidir mecanicamente")

    if numericas:
        distintos = sorted({round(a.valor, 6) for a in numericas})
        if len(distintos) > 1:
            ev = "; ".join(a.evidencia for a in numericas)
            return Extraccion("AMBIGUA", None, ev, "ANCLAS-EN-CONFLICTO",
                               "dos o mas anclas numericas distintas sin regla de "
                               "desempate mecanico")
        valor = distintos[0]
        ultima = numericas[-1]
        regla = "ANCLA-HEADER-PUNTO" if ultima.familia == "H" else "ANCLA-FRASE-PUNTO"
        return Extraccion("EXTRAIBLE", valor, ultima.evidencia, regla, "")

    # solo rechazos
    ultima = rechazos[-1]
    return Extraccion("NO-EXTRAIBLE", None, ultima.evidencia, "ANCLA-RECHAZO",
                       "rechazo explicito de estimacion en un encabezado o frase-"
                       "ancla de estimacion puntual")


# --- identidad ---------------------------------------------------------------

@dataclass
class Identidad:
    ok: bool
    id_celda: str
    variante: str
    indice: int
    razon: str = ""


def _parsear_nombre(nombre: str) -> tuple[str, str, int] | None:
    if not nombre.endswith("__v1_3.json"):
        return None
    stem = nombre[: -len("__v1_3.json")]
    partes = stem.split("__")
    if len(partes) != 3:
        return None
    tag_id, variante, idx_txt = partes
    if not (tag_id.startswith("L-") and tag_id.endswith("-M")):
        return None
    id_celda = tag_id[2:-2]
    if not idx_txt.isdigit():
        return None
    return id_celda, variante, int(idx_txt)


def verificar_identidad(ruta: Path, datos: dict, manifiesto_capturas: dict) -> Identidad:
    parsed = _parsear_nombre(ruta.name)
    if parsed is None:
        return Identidad(False, "", "", -1, f"nombre de archivo no reconoce el patron v1_3: {ruta.name}")
    id_fn, var_fn, idx_fn = parsed

    entrada = manifiesto_capturas.get(ruta.name)
    if entrada is None:
        return Identidad(False, id_fn, var_fn, idx_fn,
                          f"{ruta.name} no aparece en el manifiesto sellado de F5-RECAPTURA-L")

    sha_real = hashlib.sha256(ruta.read_bytes()).hexdigest()
    sha_manifiesto = entrada.get("sha256_archivo")
    if sha_real != sha_manifiesto:
        return Identidad(False, id_fn, var_fn, idx_fn,
                          f"sha256 no coincide con el manifiesto ({sha_real[:12]}... vs {str(sha_manifiesto)[:12]}...)")

    if (entrada.get("id_celda"), entrada.get("variante"), entrada.get("indice")) != (id_fn, var_fn, idx_fn):
        return Identidad(False, id_fn, var_fn, idx_fn,
                          "id_celda/variante/indice del manifiesto no coinciden con el nombre de archivo")

    if (datos.get("id_celda"), datos.get("variante"), datos.get("indice")) != (id_fn, var_fn, idx_fn):
        return Identidad(False, id_fn, var_fn, idx_fn,
                          f"id_celda/variante/indice DENTRO del JSON "
                          f"({datos.get('id_celda')!r},{datos.get('variante')!r},{datos.get('indice')!r}) "
                          f"no coinciden con el nombre de archivo ({id_fn!r},{var_fn!r},{idx_fn!r})")

    return Identidad(True, id_fn, var_fn, idx_fn)


# --- corrida sobre el universo ------------------------------------------------

def _fragmento_tsv(s: str) -> str:
    return s.replace("\t", " ").replace("\n", " ").strip()


def procesar_224(rutas: list[Path], manifiesto_capturas: dict) -> tuple[list[dict], dict]:
    filas: list[dict] = []
    for ruta in sorted(rutas):
        with ruta.open(encoding="utf-8") as fh:
            datos = json.load(fh)
        ident = verificar_identidad(ruta, datos, manifiesto_capturas)
        if not ident.ok:
            filas.append({
                "archivo": ruta.name,
                "id_celda": ident.id_celda,
                "variante": ident.variante,
                "replica": ident.indice,
                "estado": "ERROR-IDENTIDAD",
                "valor_extraido": "",
                "evidencia_textual": "",
                "regla_de_extraccion": "",
                "razon_no_extraible": ident.razon,
            })
            continue
        ext = extraer_valor(datos["texto_crudo"])
        filas.append({
            "archivo": ruta.name,
            "id_celda": ident.id_celda,
            "variante": ident.variante,
            "replica": ident.indice,
            "estado": ext.estado,
            "valor_extraido": "" if ext.valor_extraido is None else f"{ext.valor_extraido:.4f}",
            "evidencia_textual": _fragmento_tsv(ext.evidencia_textual),
            "regla_de_extraccion": ext.regla_de_extraccion,
            "razon_no_extraible": ext.razon_no_extraible,
        })

    resumen = _resumen(filas)
    return filas, resumen


def _resumen(filas: list[dict]) -> dict:
    total = len(filas)
    por_estado: dict[str, int] = {}
    por_regla: dict[str, int] = {}
    por_brazo: dict[str, dict[str, int]] = {}
    por_celda: dict[str, dict[str, int]] = {}
    por_replica: dict[str, dict[str, int]] = {}

    for fila in filas:
        estado = fila["estado"]
        por_estado[estado] = por_estado.get(estado, 0) + 1
        regla = fila["regla_de_extraccion"] or "(ninguna -- ERROR-IDENTIDAD)"
        por_regla[regla] = por_regla.get(regla, 0) + 1

        brazo = fila["variante"] or "(desconocido)"
        por_brazo.setdefault(brazo, {}).setdefault(estado, 0)
        por_brazo[brazo][estado] += 1

        celda = fila["id_celda"] or "(desconocido)"
        por_celda.setdefault(celda, {}).setdefault(estado, 0)
        por_celda[celda][estado] += 1

        replica = str(fila["replica"])
        por_replica.setdefault(replica, {}).setdefault(estado, 0)
        por_replica[replica][estado] += 1

    return {
        "total_capturas": total,
        "por_estado": por_estado,
        "por_regla_de_extraccion": por_regla,
        "cobertura_por_brazo": por_brazo,
        "cobertura_por_celda": por_celda,
        "cobertura_por_replica": por_replica,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--solo-reporte", action="store_true",
                         help="corre y reporta pero no escribe TSV ni manifiesto")
    args = parser.parse_args()

    with MANIFIESTO_CAPTURAS.open(encoding="utf-8") as fh:
        manifiesto = json.load(fh)
    manifiesto_capturas = manifiesto["capturas"]

    rutas = sorted(CORRIDAS_L.glob("*__v1_3.json"))
    assert len(rutas) == TOTAL_ESPERADO, (
        f"esperaba {TOTAL_ESPERADO} capturas *__v1_3.json, encontre {len(rutas)}"
    )

    filas, resumen = procesar_224(rutas, manifiesto_capturas)

    print(f"total capturas examinadas: {resumen['total_capturas']}")
    print("por estado:")
    for k in ("EXTRAIBLE", "NO-EXTRAIBLE", "AMBIGUA", "ERROR-IDENTIDAD"):
        print(f"  {k}: {resumen['por_estado'].get(k, 0)}")
    print("distribucion de regla_de_extraccion:")
    for k, v in sorted(resumen["por_regla_de_extraccion"].items()):
        print(f"  {k}: {v}")
    print("cobertura por brazo (variante):")
    for brazo, d in sorted(resumen["cobertura_por_brazo"].items()):
        print(f"  {brazo}: {d}")
    print("cobertura por celda:")
    for celda, d in sorted(resumen["cobertura_por_celda"].items()):
        print(f"  {celda}: {d}")
    print("cobertura por replica:")
    for r, d in sorted(resumen["cobertura_por_replica"].items(), key=lambda t: int(t[0]) if t[0].isdigit() else -1):
        print(f"  {r}: {d}")

    if args.solo_reporte:
        return 0

    with SALIDA_TSV.open("w", encoding="utf-8") as fh:
        cols = ["id_celda", "variante", "replica", "estado", "valor_extraido",
                "evidencia_textual", "regla_de_extraccion", "razon_no_extraible", "archivo"]
        fh.write("\t".join(cols) + "\n")
        for fila in filas:
            fh.write("\t".join(str(fila[c]) for c in cols) + "\n")
    print(f"OK -- TSV escrito en {SALIDA_TSV.relative_to(ROOT)}")

    extractor_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    manifiesto_extraccion = {
        "acto": "GEN2-F5-EXTRACTOR-L-v1",
        "extractor": "tools/extrae_l_v1_3.py",
        "extractor_sha256": extractor_sha256,
        "manifiesto_capturas_insumo": str(MANIFIESTO_CAPTURAS.relative_to(ROOT)),
        "manifiesto_capturas_sha256": hashlib.sha256(MANIFIESTO_CAPTURAS.read_bytes()).hexdigest(),
        "resumen": resumen,
        "capturas": {
            fila["archivo"]: {
                "id_celda": fila["id_celda"],
                "variante": fila["variante"],
                "replica": fila["replica"],
                "estado": fila["estado"],
                "valor_extraido": fila["valor_extraido"],
                "regla_de_extraccion": fila["regla_de_extraccion"],
            }
            for fila in filas
        },
    }
    with SALIDA_MANIFIESTO.open("w", encoding="utf-8") as fh:
        json.dump(manifiesto_extraccion, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    print(f"OK -- manifiesto de extraccion escrito en {SALIDA_MANIFIESTO.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
