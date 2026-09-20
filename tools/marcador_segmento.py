#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tools/marcador_segmento.py` -- deriva `data/corrida0/marcador-segmento.tsv`.

ACTO GEN2-MARCADOR-REDISENO-1 (encargo + adenda de dirección, 19/sep/2026),
sobre el diseño de mesa `MARCADOR-SEGMENTO-diseno-direccion-v1_0` +
delta v1.1 (firma de mesa 17/sep/2026, §9).

CERO CIFRAS NUEVAS. Este tool no mide nada: lee valores YA SELLADOS en
cuatro fuentes y los proyecta a una tabla derivada:

  1. `forense/notas/2026-09-16-GEN2-EMISOR-ESTADO-1-censo.tsv` (ADR-536) --
     97 celdas NACIONALES/compuestas del censo de identidad emisor<->arbitro.
  2. `milpa/tramite-ola5-propuesta-v0.yaml`, los SIETE ids con sufijo
     `_ejes_` -- celdas MARGINALES del árbitro por eje.
  3. `data/curacion-registro/celdas-d/*.yaml` con `champion_actual: C2` --
     las 20 celdas de CRUCE piloteadas (ADR-538/ADR-542), con sus RESULT
     sellados leídos de `data/corrida0/CALC-*-EMISIONES-0001/resultados.json`.
  4. `data/corrida0/decisiones.tsv` -- el veto de mesa a los cuatro
     `CALC-PISOS-*-EJES-0001` (objeto `veto:pisos-866`, 19/sep/2026): esos
     cuatro directorios se EXCLUYEN POR NOMBRE como fuente de piso,
     incondicionalmente, sin leer su contenido.
  5. `forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv` -- la
     TABLA DE IDENTIDAD de la rejilla (`GEN2-PISOS-REJILLA-CLI-1`, PR #871):
     `cell_id` -> `consumer`/`axis`/`category`/`outcome`/`unit`/`status`.
     Es la fuente del enlace piso<->celda marginal; el `cell_id` ES el id
     del RESULT, no se reconstruye ni se adivina.

Piso: el diseño (§9(2)) dicta MARGINAL-SIN-INTERACCION para las celdas de
cruce ya piloteadas (así lo declara `regla_composicion` en la celda-D misma)
y PERSISTENCIA(t-1) por eje para las marginales, leído de los tres CALC que
`GEN2-PISOS-REJILLA-CLI-1` selló (`CALC_PISOS_SELLADOS`) A TRAVÉS de la
tabla de identidad. El veto `veto:pisos-866` sigue vigente y sigue siendo
POR NOMBRE sobre los cuatro `-EJES-0001`: su propio texto lo condiciona
"hasta que GEN2-PISOS-REJILLA-CLI-1 entregue sucesores", y esos sucesores
son justamente los tres de `CALC_PISOS_SELLADOS`.

ACTO GEN2-MARCADOR-PISOS-ENLACE-1 (19/sep/2026) · P1: sustituye el lector
por patrón de id (`_id_piso_v2`/`_lee_piso_v2`, borrado) por el enlace
contra la tabla de identidad, y corrige `unidad_dato` leyéndola del
`payload` del árbitro en vez de inferirla del prefijo del id de la regla.
Cierra NC-0342.

Salida: `data/corrida0/marcador-segmento.tsv` (`# DERIVADO -- NO EDITAR`)
y, en P2, `milpa/estimadores-por-segmento.yaml` con las celdas adoptadas.

Uso:
    python3 tools/marcador_segmento.py            # deriva e imprime resumen
    python3 tools/marcador_segmento.py --escribe   # además escribe los TSV/YAML
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
CENSO_TSV = RAIZ / "forense" / "notas" / "2026-09-16-GEN2-EMISOR-ESTADO-1-censo.tsv"
PROPUESTA_OLA5 = RAIZ / "milpa" / "tramite-ola5-propuesta-v0.yaml"
CELDAS_D_DIR = RAIZ / "data" / "curacion-registro" / "celdas-d"
DECISIONES_TSV = RAIZ / "data" / "corrida0" / "decisiones.tsv"
CORRIDA0_DIR = RAIZ / "data" / "corrida0"
MARCADOR_TSV = CORRIDA0_DIR / "marcador-segmento.tsv"
# ── LAS TABLAS DE IDENTIDAD, EN UN SOLO SITIO ────────────────────────────
# ACTO GEN2-MARCADOR-ENLACE-2 (20/sep/2026) · P1. Antes había una constante
# por tabla y una tupla literal dentro de `lee_tabla_identidad()`; registrar
# una tabla nueva tocaba dos sitios y no declaraba ningún orden. Ahora la
# lista vive AQUÍ y sólo aquí, **en orden cronológico de sello, de la más
# antigua a la más reciente**, y ese orden ES la regla de precedencia:
# si dos tablas hablan de la misma celda `(consumer, outcome, axis,
# category)`, manda la MÁS RECIENTE y el marcador lo dice en `piso_fuente`
# (`· SUCEDE-A:<cell_id de la sucedida>`). Ninguna tabla se edita nunca:
# una fila sellada se SUCEDE, no se corrige (A.10).
#
# Contrato de columnas (idéntico en las tres): `cell_id · input_id ·
# outcome · source_* · target_* · unit · axis · category · status ·
# reason · consumer · metadata_source · metadata_source_sha256`.
# `data/INFRAESTRUCTURA-v1_0.md` documenta la lista; esta constante la
# gobierna.
PREREG = RAIZ / "forense" / "prereg-caja"
TABLAS_IDENTIDAD = [
    # (1) la rejilla del árbitro -- `GEN2-PISOS-REJILLA-CLI-1`, PR #871.
    PREREG / "PISOS-REJILLA-arbitro-metadatos-v1_0.tsv",
    # (2) `GEN2-PISOS-ENUT2019-EJES-1` (19/sep/2026, PR #908): 11 filas
    #     NO-CONSTRUIBLE con causa (dictamen P0 por texto,
    #     forense/notas/2026-09-19-GEN2-PISOS-ENUT2019-EJES-1-dictamen.md).
    PREREG / "PISOS-ENUT2019-ejes-metadatos-v1_0.tsv",
    # (3) `GEN2-PISOS-ENIF2021-FORMALIDAD-1` (19/sep/2026, PR #915): 6 filas
    #     CONSTRUIBLE con RESULT sellado. Cuatro de ellas SUCEDEN a cuatro
    #     filas NO-CONSTRUIBLE de (1) cuya causa (`P3_13 comparable no
    #     existe en ENIF 2021`) el dictamen de #908 §2.1 refutó por texto y
    #     #915 refutó además sobre el dato. Va al final: es la más reciente.
    PREREG / "PISOS-ENIF2021-formalidad-metadatos-v1_0.tsv",
]
COLS_TABLA_IDENTIDAD = ("cell_id", "outcome", "unit", "axis", "category",
                         "status", "reason", "consumer")

# Compatibilidad de nombre para lectores externos; la lista manda.
TABLA_IDENTIDAD = TABLAS_IDENTIDAD[0]
TABLA_IDENTIDAD_ENUT2019 = TABLAS_IDENTIDAD[1]
TABLA_IDENTIDAD_ENIF2021_FORMALIDAD = TABLAS_IDENTIDAD[2]
# P2: el error del piso y su clase se DERIVAN de este CALC, no se
# recalculan aquí. Si el CALC no está sellado, las dos columnas salen
# vacías -- el marcador nunca estima.
CALC_ERROR_PISO = CORRIDA0_DIR / "CALC-PISO-PERSISTENCIA-ERROR-0001"
ESTIMADORES_YAML = RAIZ / "milpa" / "estimadores-por-segmento.yaml"

# Los cuatro CALC-PISOS-* que el veto de mesa 19/sep/2026 (objeto
# `veto:pisos-866`) excluye por nombre -- ver decisiones.tsv.
CALC_PISOS_VETADOS = [
    "CALC-PISOS-ENVIPE2024-EJES-0001",
    "CALC-PISOS-ENCIG2023-EJES-0001",
    "CALC-PISOS-ENCIG2023-EJES-0001-v1_1",
    "CALC-PISOS-ENIF2021-EJES-0001",
]

# Los TRES CALC sellados por `GEN2-PISOS-REJILLA-CLI-1` (PR #871/#874) que
# la tabla de identidad referencia con su `cell_id`. Se nombran, no se
# globbean: `CALC-PISOS-ENIF2021-EJES-0002` existe en el árbol pero es
# spec-only (sin `resultados.json`) y un glob lo tomaría como fuente.
CALC_PISOS_SELLADOS = [
    "CALC-PISOS-ENVIPE2024-EJES-0002",
    "CALC-PISOS-ENCIG2023-EJES-0002",
    "CALC-PISOS-ENIF2021-EJES-0003",
    # ACTO GEN2-MARCADOR-ENLACE-2 (20/sep/2026) · P1: el CALC que
    # `GEN2-PISOS-ENIF2021-FORMALIDAD-1` selló (PR #915, REPRODUCE/IDENTICO,
    # 6 celdas + 3 de universo). Sin él, sus 6 filas CONSTRUIBLE saldrían
    # `CONSTRUIBLE-EN-TABLA-SIN-RESULT-SELLADO`.
    "CALC-PISOS-ENIF2021-FORMALIDAD-0001",
]

# NC-0328: "edad x dominio" dentro de tramite.evasion_norma_ejes_envipe2025
# corrió exploratoriamente sin COMMIT-1 -- reserva consumida sin piloto.
NC_0328_PAR_CONSUMIDO = ("tramite.evasion_norma_ejes_envipe2025",
                          frozenset({"edad", "dominio_urbano_rural"}))

COLS = [
    "celda_id", "tipo", "regla_o_eje_origen", "instrumento",
    "eje_o_par", "categoria", "unidad_dato", "unidad_objetivo",
    "estado", "emision", "piso_tipo", "piso", "piso_ic95", "piso_fuente",
    "error_piso_pp", "clase_persistencia",
    "R", "R_ic95inf", "R_ic95sup",
    "M", "IC95_inf", "IC95_sup", "tipo_incertidumbre",
    "resultado_id", "decision_ref", "emisor_vs_arbitro", "fuente",
]


def _yaml(ruta: Path):
    return yaml.safe_load(ruta.read_text(encoding="utf-8"))


def _lee_decisiones() -> dict:
    if not DECISIONES_TSV.exists():
        return {}
    out = {}
    with DECISIONES_TSV.open(encoding="utf-8") as fh:
        for f in csv.DictReader(fh, delimiter="\t"):
            out[f["objeto"]] = f
    return out


# ── (2) universo NACIONAL/compuesto -- censo ADR-536 (97 filas) ───────────

def filas_nacionales() -> list[dict]:
    filas = []
    with CENSO_TSV.open(encoding="utf-8") as fh:
        lineas = [l for l in fh if not l.startswith("#")]
    for f in csv.DictReader(lineas, delimiter="\t"):
        veredicto = f["veredicto"]
        emisor_vs_arbitro = "EMISOR=ARBITRO" if veredicto == "IDENTICO" else veredicto
        filas.append({
            "celda_id": f"NAC::{f['regla']}::{f['salida']}::{f['celda']}",
            "tipo": "NACIONAL",
            "regla_o_eje_origen": f["regla"],
            "instrumento": f["instrumento_ola_arbitro"],
            "eje_o_par": "NACIONAL",
            "categoria": f["celda"],
            "unidad_dato": "NO-DECLARADO-EN-CENSO",
            "unidad_objetivo": "persona",
            "estado": "IDENTICO" if veredicto == "IDENTICO" else "DIAGNOSTICO",
            "piso_tipo": "NO-APLICA", "piso": "", "piso_ic95": "",
            "piso_fuente": "",
            "R": f["p_arbitro"], "R_ic95inf": "", "R_ic95sup": "",
            "M": f["p_emisor"] if veredicto == "IDENTICO" else "",
            "IC95_inf": "", "IC95_sup": "",
            "tipo_incertidumbre": "NO-DECLARADO-EN-CENSO",
            "resultado_id": "",
            "decision_ref": "marcador:emisor-fuera",
            "emisor_vs_arbitro": emisor_vs_arbitro,
            "fuente": f["origen_linea"],
        })
    return filas


# ── (1) universo MARGINAL -- los 7 ids `_ejes_` de la propuesta ola5 ──────

def _camina_ejes(nodo, desenlace: str = ""):
    """Genérico: cualquier dict con `eje` + `celdas` es un eje marginal,
    sin importar la profundidad de anidamiento (`ejes:` plano o
    `desenlaces: {principal, secundario}: {nombre, ejes: [...]}`).

    Rinde `(desenlace, bloque)`. El DESENLACE es parte de la identidad de la
    celda: `dinero.ahorro.via_informal_ejes_enif2024` declara dos
    (`ahorra_solo_informal` y `informal_cualquiera`, yaml:1421/1494) sobre
    los MISMOS ejes y categorías, con R distintos. Perderlo colapsaba 32
    filas marginales en 16 `celda_id` duplicados y hacía imposible un enlace
    1:1 con la tabla de identidad, que sí distingue por `outcome`."""
    if isinstance(nodo, dict):
        if "eje" in nodo and "celdas" in nodo:
            yield desenlace, nodo
        hijo = nodo.get("nombre") if ("nombre" in nodo and "ejes" in nodo) else None
        for clave, v in nodo.items():
            if clave == "nombre":
                continue
            yield from _camina_ejes(v, hijo or desenlace)
    elif isinstance(nodo, list):
        for e in nodo:
            yield from _camina_ejes(e, desenlace)


# ── P1 · MAPA DE IDENTIDAD REJILLA <-> MARCADOR (UN SOLO SITIO) ───────────
# ACTO GEN2-MARCADOR-PISOS-ENLACE-1 (19/sep/2026). Cierra NC-0342.
#
# El enlace NO adivina ids ni compara cadenas por similitud: lee la tabla de
# identidad del árbitro (`TABLA_IDENTIDAD`), que ya trae el `cell_id` exacto
# del RESULT por celda. Lo único que este mapa resuelve es que los DOS
# VOCABULARIOS -- el del árbitro en la tabla y el de
# `milpa/tramite-ola5-propuesta-v0.yaml` que alimenta al marcador -- nombran
# distinto las mismas reglas, ejes y categorías. Cada entrada cita archivo y
# línea de AMBOS lados. Toda discrepancia NO listada aquí no se resuelve: la
# celda se queda sin enlace y la guardia D-14 `T-ENLACE-BIYECTIVO` hace
# fallar la suite. Nunca se enlaza por parecido de cadena.

# regla del marcador (`milpa/tramite-ola5-propuesta-v0.yaml`, campo `id`)
# -> `consumer` de la tabla (`…PISOS-REJILLA-arbitro-metadatos-v1_0.tsv`,
# columna 15).
MAPA_CONSUMER = {
    # yaml:1672                                tabla:2
    "tramite.evasion_norma_ejes_envipe2025":
        "tramite.evasion_norma.segmentacion_ejes_envipe2025",
    # yaml:1993                                tabla:15
    # cambia hasta el prefijo de dominio (`civico.` vs `familia.`): mismo
    # objeto, dos vocabularios. Por esto el mapa es explícito.
    "civico.denuncia.con_seguro_ejes_envipe2025":
        "familia.seguro.denuncia.segmentacion_envipe2025",
    # yaml:1600                                tabla:17
    "tramite.gobierno_digital.util_sin_coercion_ejes_encig2025":
        "tramite.gobierno_digital.util_sin_coercion.segmentacion_ejes_encig2025",
    # yaml:1415                                tabla:27
    "dinero.ahorro.via_informal_ejes_enif2024":
        "dinero.ahorro.tiene_ahorros.segmentacion_ejes_enif2024",
    # yaml:2089                                PISOS-ENUT2019-ejes-metadatos-v1_0.tsv:2-12
    # mismo id en ambos lados; ACTO GEN2-PISOS-ENUT2019-EJES-1 dictaminó las
    # 11 celdas NO-CONSTRUIBLE por texto (sin tvar_crea en 2019), así que el
    # enlace sólo transporta la causa, nunca un piso.
    "familia.cuidado.reparto_mujeres40_ejes_enut2024":
        "familia.cuidado.reparto_mujeres40_ejes_enut2024",
    # yaml:2159       PISOS-ENIF2021-formalidad-metadatos-v1_0.tsv:6-7
    # ACTO GEN2-MARCADOR-ENLACE-2 (20/sep/2026) · P1: mismo id en ambos
    # lados. Hasta #915 no había tabla con este `consumer` y las dos celdas
    # salían `SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD`; ahora `CALC-PISOS-ENIF2021-
    # FORMALIDAD-0001` las selló (`HORIZONTE-CORTO × {sin,con} seguridad
    # social`) y el enlace existe.
    "dinero.ahorro.horizonte_corto_ejes_enif2024":
        "dinero.ahorro.horizonte_corto_ejes_enif2024",
    # `familia.union.libre_ejes_eder2017` (yaml:2041) NO aparece como
    # `consumer` en ninguna tabla: la rejilla no midió piso para ella y
    # `GEN2-PISOS-ENUT2019-EJES-1` la dictaminó SIN-PISO-POR-DISEÑO
    # (forense/notas/2026-09-19-GEN2-PISOS-ENUT2019-EJES-1-dictamen.md §2.2)
    # SIN escribir filas: `SIN-PISO-POR-DISEÑO` no existe en el vocabulario
    # `status` de la tabla e inventarlo es decisión de vocabulario, de mesa.
    # Queda SIN-PISO por AUSENCIA DE FUENTE, no por fallo de enlace.
}

# (`consumer` de la tabla, eje del marcador) -> `axis` de la tabla
# (columna 11). Sólo las tres que difieren; el resto es identidad.
MAPA_EJE = {
    # yaml:1705 `escolaridad_proxy` (proxy: ENVIPE no pregunta escolaridad al
    # delito, la hereda de la víctima) ; tabla:8 `escolaridad`
    ("tramite.evasion_norma.segmentacion_ejes_envipe2025", "escolaridad_proxy"):
        "escolaridad",
    # yaml:1719 `dominio_urbano_rural` ; tabla:12 `dominio`
    ("tramite.evasion_norma.segmentacion_ejes_envipe2025", "dominio_urbano_rural"):
        "dominio",
    # yaml:1486 `cuenta_formal` ; tabla:41 `cuenta`
    ("dinero.ahorro.tiene_ahorros.segmentacion_ejes_enif2024", "cuenta_formal"):
        "cuenta",
}

# (`axis` de la tabla, categoría del marcador) -> `category` de la tabla
# (columna 12). Sólo las que difieren.
MAPA_CATEGORIA = {
    # el yaml rotula con la etiqueta legible; la tabla guarda el código crudo
    # del árbitro.  yaml:1437 / tabla:2-3
    ("sexo", "1 Hombre"): "1",
    ("sexo", "2 Mujer"): "2",
    # espacio vs guion bajo.  yaml:1460,1462 / tabla:8,10
    ("escolaridad", "hasta primaria"): "hasta_primaria",
    ("escolaridad", "media superior"): "media_superior",
    # yaml:2012 / tabla:15
    ("cobertura_seguro", "no asegurado"): "no_asegurado",
}

# `unidad` declarada en el `payload` del árbitro -> rótulo normalizado del
# marcador. La unidad NO se infiere del prefijo del id de la regla (ése era
# el defecto de la vieja `_unidad_dato`, que rotulaba `persona` todo lo que
# no empezara con `tramite.evasion_norma`, contradiciendo al propio árbitro
# en ENCIG 2025 -- `unidad = TRÁMITE`, yaml:1604 -- y en la denuncia con
# seguro de ENVIPE 2025 -- `unidad = DELITO`, yaml:1997). Se LEE del payload.
NORMALIZA_UNIDAD = {
    "DELITO": "delito",
    "TRÁMITE": "tramite",
    "TRAMITE": "tramite",
    "PERSONA ELEGIDA 18+": "persona_elegida_18mas",
    "PERSONA": "persona",
    "HOGAR": "hogar",
}

# `unit` de la tabla (columna 10) -> el mismo rótulo normalizado, para que
# la comparación piso<->R sea entre dos etiquetas del mismo vocabulario.
# prefijo del id de celda-D -> regla de `tramite-ola5-propuesta-v0.yaml` de
# la que hereda su unidad. Mismo par que `pares_piloteados` ya fija abajo en
# `filas_cruce_reservadas`; aquí sirve para que la unidad de una fila CRUCE
# también salga del `payload` del árbitro y no de un prefijo de id.
MAPA_CELDA_D_A_REGLA = {
    "DIN.": "dinero.ahorro.via_informal_ejes_enif2024",       # yaml:1415
    "TRA.": "tramite.evasion_norma_ejes_envipe2025",           # yaml:1672
}

NORMALIZA_UNIT_TABLA = {
    "DELITO": "delito",
    "TRAMITE": "tramite",
    "TRÁMITE": "tramite",
    "PERSONA ELEGIDA 18+": "persona_elegida_18mas",
    "PERSONA": "persona",
}

_RE_UNIDAD = re.compile(r"unidad\s*=\s*(.+?)\s*$", re.IGNORECASE)


def _unidad_dato(regla: dict) -> str:
    """Rótulo de unidad del dato, LEÍDO del `payload` que el árbitro
    escribió (`milpa/tramite-ola5-propuesta-v0.yaml`, campo `payload`),
    nunca inferido del id. Si el payload no declara `unidad = …`, o declara
    algo que no está en `NORMALIZA_UNIDAD`, se devuelve el verbatim
    rotulado -- nunca un valor inventado."""
    payload = str(regla.get("payload") or "")
    m = _RE_UNIDAD.search(payload)
    if not m:
        return "NO-DECLARADA-EN-PAYLOAD"
    crudo = m.group(1).strip()
    # El payload puede traer una glosa (`PERSONA elegida 18+`), un paréntesis
    # explicativo (`TRÁMITE (quien pagó doce veces…)`) o DOS unidades a la vez
    # (`HOGAR (D2) y PERSONA (D1)`, yaml:2093). Se barre por clave más larga
    # primero, consumiendo lo ya reconocido, para que `PERSONA ELEGIDA 18+` no
    # cuente además como `PERSONA`.
    resto = crudo.upper()
    halladas: list[str] = []
    for clave in sorted(NORMALIZA_UNIDAD, key=len, reverse=True):
        if clave in resto:
            resto = resto.replace(clave, " ")
            val = NORMALIZA_UNIDAD[clave]
            if val not in halladas:
                halladas.append(val)
    if not halladas:
        return f"NO-NORMALIZADA:{crudo}"
    if len(halladas) > 1:
        # dos unidades en un solo payload: no se elige una. Una celda así
        # nunca compara contra un piso (A-bis 3-4).
        return f"MIXTA:{crudo}"
    return halladas[0]


# ── enlace piso <-> celda marginal, por la tabla de identidad ─────────────

def _regla_ola5(regla_id: str) -> dict:
    d = _yaml(PROPUESTA_OLA5)
    for r in d.get("reglas_propuestas", []):
        if r.get("id") == regla_id:
            return r
    return {}


def _unidad_de_celda_d(celda_id: str) -> str:
    for prefijo, regla_id in MAPA_CELDA_D_A_REGLA.items():
        if celda_id.startswith(prefijo):
            return _unidad_dato(_regla_ola5(regla_id))
    return "NO-MAPEADA-A-REGLA-DE-OLA5"


def _resultados_sellados() -> dict:
    """Une los `resultados` de los TRES CALC sellados, por nombre. Un
    directorio vetado por `veto:pisos-866` jamás entra aquí: el veto es por
    nombre y `CALC_PISOS_SELLADOS` no lo contiene."""
    out: dict[str, tuple] = {}
    for nombre in CALC_PISOS_SELLADOS:
        if nombre in CALC_PISOS_VETADOS:   # cinturón: el veto manda siempre
            continue
        rj = CORRIDA0_DIR / nombre / "resultados.json"
        if not rj.exists():
            continue
        try:
            res = json.loads(rj.read_text(encoding="utf-8")).get("resultados", {})
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(res, dict):
            for k, v in res.items():
                out.setdefault(k, (v, nombre))
    return out


def _clave_identidad(f: dict) -> tuple:
    """La ÚNICA llave de enlace piso<->celda: `(consumer, outcome, axis,
    category)`. Vive en una función para que el índice, la precedencia y
    el test de enlace usen literalmente la misma."""
    return (f["consumer"], f["outcome"], f["axis"], f["category"])


def lee_tabla_identidad() -> list[dict]:
    """Filas de TODAS las tablas de `TABLAS_IDENTIDAD`, tal cual y en el
    orden declarado (más antigua primero). Se LEE; este acto no escribe
    ninguna tabla (perímetro). Cada fila sale rotulada con `_tabla`, la
    ruta relativa de la que vino, y `_orden`, su posición en la lista:
    de ahí sale la precedencia, no de ninguna heurística sobre el
    contenido."""
    filas: list[dict] = []
    for orden, tabla in enumerate(TABLAS_IDENTIDAD):
        if not tabla.exists():
            continue
        with tabla.open(encoding="utf-8") as fh:
            lineas = [l for l in fh if not l.startswith("#")]
        for f in csv.DictReader(lineas, delimiter="\t"):
            faltan = [c for c in COLS_TABLA_IDENTIDAD if c not in f]
            if faltan:
                # contrato de columnas: una tabla que no lo cumple no se
                # interpreta a medias ni se rellena -- se declara y se cae.
                raise ValueError(
                    f"{tabla.relative_to(RAIZ)}: la tabla de identidad no "
                    f"trae las columnas {faltan} del contrato "
                    f"{list(COLS_TABLA_IDENTIDAD)}")
            f["_tabla"] = str(tabla.relative_to(RAIZ))
            f["_orden"] = orden
            filas.append(f)
    return filas


def sucesiones_identidad() -> dict:
    """`cell_id` de la fila SUCEDIDA -> `cell_id` de la que la sucede.
    Dos tablas que hablan de la misma celda no son un defecto: la más
    reciente manda (ACTO GEN2-MARCADOR-ENLACE-2, P1). Lo que sí sería
    defecto es una clave repetida DENTRO de una misma tabla, y eso se
    reporta aparte."""
    por_clave: dict[tuple, dict] = {}
    sucedidas: dict[str, str] = {}
    for f in lee_tabla_identidad():
        clave = _clave_identidad(f)
        previa = por_clave.get(clave)
        if previa is not None and previa["_orden"] != f["_orden"]:
            sucedidas[previa["cell_id"]] = f["cell_id"]
        por_clave[clave] = f
    return sucedidas


def colisiones_dentro_de_una_tabla() -> list[tuple]:
    """Claves repetidas DENTRO de una misma tabla. Eso sí es defecto de la
    tabla: no hay orden que las desempate. Se reporta, no se elige una."""
    vistas: dict[tuple, str] = {}
    malas: list[tuple] = []
    for f in lee_tabla_identidad():
        k = (f["_orden"],) + _clave_identidad(f)
        if k in vistas:
            malas.append((f["_tabla"], vistas[k], f["cell_id"]))
        vistas[k] = f["cell_id"]
    return malas


def indice_identidad() -> dict:
    """(`consumer`, `outcome`, `axis`, `category`) -> fila que MANDA.

    Manda la de la tabla más reciente de `TABLAS_IDENTIDAD` (asignación,
    no `setdefault`: el último de la lista gana). La fila sucedida no se
    borra ni se edita -- sigue sellada en su tabla y `sucesiones_identidad()`
    la nombra; el marcador lo transporta a `piso_fuente`."""
    idx: dict[tuple, dict] = {}
    for f in lee_tabla_identidad():
        idx[_clave_identidad(f)] = f
    return idx


def clave_de_marcador(regla_id: str, desenlace: str, eje: str, categoria: str,
                       idx: dict) -> tuple | None:
    """Traduce las coordenadas del marcador al vocabulario de la tabla,
    SÓLO por los tres mapas explícitos de arriba. Devuelve `None` si la
    regla no tiene `consumer` en la tabla (ausencia de fuente)."""
    consumer = MAPA_CONSUMER.get(regla_id)
    if consumer is None:
        return None
    axis = MAPA_EJE.get((consumer, eje), eje)
    category = MAPA_CATEGORIA.get((axis, categoria), categoria)
    if desenlace:
        return (consumer, desenlace, axis, category)
    # Reglas sin bloque `desenlaces:`: el consumer tiene un solo `outcome`
    # en la tabla, y ese es el desenlace. Si tuviera más de uno, no se
    # adivina: se devuelve None y la celda queda sin enlace.
    outcomes = {k[1] for k in idx if k[0] == consumer}
    if len(outcomes) != 1:
        return None
    return (consumer, next(iter(outcomes)), axis, category)


def _piso_de_fila(clave: tuple, idx: dict, res: dict,
                   suc: dict | None = None) -> dict | None:
    """Piso de persistencia t-1 de una celda marginal, o `None` si la clave
    no está en la tabla. Para una fila `NO-CONSTRUIBLE` devuelve el motivo
    sin valor: un piso que la rejilla declaró inconstruible no se fabrica."""
    fila = idx.get(clave)
    if fila is None:
        return None
    # ACTO GEN2-MARCADOR-ENLACE-2 · P1: si esta fila SUCEDE a otra de una
    # tabla anterior, el marcador lo dice. La sucedida sigue sellada.
    sucede_a = {v: k for k, v in (suc or {}).items()}.get(fila["cell_id"], "")
    if fila["status"] != "CONSTRUIBLE":
        return {"construible": False, "causa": fila.get("reason") or fila["status"],
                "unit": fila.get("unit", ""), "cell_id": fila["cell_id"],
                "sucede_a": sucede_a, "tabla": fila.get("_tabla", "")}
    base = fila["cell_id"]
    if base.endswith("-P"):
        base = base[:-2]
    ids = {s: f"{base}-{s}" for s in ("P", "IC-LO", "IC-HI", "N", "DEN-W")}
    if any(i not in res for i in (ids["P"], ids["IC-LO"], ids["IC-HI"])):
        # la tabla declara CONSTRUIBLE pero el RESULT no está sellado: no se
        # fuerza el parseo ni se inventa un piso.
        return {"construible": False,
                "causa": f"CONSTRUIBLE-EN-TABLA-SIN-RESULT-SELLADO:{ids['P']}",
                "unit": fila.get("unit", ""), "cell_id": fila["cell_id"],
                "sucede_a": sucede_a, "tabla": fila.get("_tabla", "")}
    punto, calc = res[ids["P"]]
    lo, _ = res[ids["IC-LO"]]
    hi, _ = res[ids["IC-HI"]]
    n = res.get(ids["N"], ("", ""))[0]
    den = res.get(ids["DEN-W"], ("", ""))[0]
    return {
        "construible": True,
        "sucede_a": sucede_a,
        "tabla": fila.get("_tabla", ""),
        "punto": punto, "ic95inf": lo, "ic95sup": hi, "n": n, "den_w": den,
        "unit": fila.get("unit", ""),
        "unit_normalizada": NORMALIZA_UNIT_TABLA.get(
            (fila.get("unit") or "").strip().upper(),
            f"NO-NORMALIZADA:{fila.get('unit')}"),
        "outcome": fila.get("outcome", ""),
        "source_instrument": fila.get("source_instrument", ""),
        "source_edition": fila.get("source_edition", ""),
        "source_reference_period": fila.get("source_reference_period", ""),
        "target_instrument": fila.get("target_instrument", ""),
        "target_edition": fila.get("target_edition", ""),
        "target_reference_period": fila.get("target_reference_period", ""),
        "resultado_id": ids["P"],
        "calc": calc,
        "fuente": f"{calc}/{ids['P']}",
    }


def _slug_result(v) -> str:
    """Mismo slug que `medidor.py` de `CALC-PISO-PERSISTENCIA-ERROR-0001`
    usa para armar el id del RESULT. Vive duplicado a propósito: el marcador
    no importa el medidor (sería un ciclo -- el medidor sí importa este
    módulo), y `T-ERROR-PISO-DERIVADO` prueba que los dos coinciden contra
    los ids realmente sellados."""
    return "".join(c if c.isalnum() else "-" for c in str(v)).strip("-").upper()


def _error_de_piso_por_celda(idx_por_cell_id: dict) -> dict:
    """`celda_id` -> (`error_piso_pp`, `clase_persistencia`) LEÍDOS de los
    RESULT sellados de `CALC-PISO-PERSISTENCIA-ERROR-0001`. El marcador no
    recalcula nada: si el CALC no está sellado, las dos columnas van
    vacías."""
    rj = CALC_ERROR_PISO / "resultados.json"
    if not rj.exists():
        return {}
    try:
        res = json.loads(rj.read_text(encoding="utf-8")).get("resultados", {})
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(res, dict):
        return {}
    return res


def _columnas_error(res: dict, tabla: dict, eje: str, categoria: str) -> tuple:
    if not res or not tabla:
        return ("", "")
    base = ("RESULT-PISO-ERR-"
            f"{_slug_result(tabla.get('source_instrument'))}-"
            f"{_slug_result(tabla.get('outcome'))}-"
            f"{_slug_result(eje)}-{_slug_result(categoria)}")
    return (res.get(f"{base}-D-PP", ""), res.get(f"{base}-CLASE", ""))


def filas_marginales(vetados: bool) -> tuple[list[dict], dict]:
    """Universo (i): las celdas marginales por eje de los siete ids `_ejes_`.

    `vetados` conserva su semántica de nombre -- los cuatro
    `CALC-PISOS-*-EJES-0001` NUNCA se leen -- pero ya no apaga el lector:
    el veto `veto:pisos-866` se condicionó a sí mismo "hasta que
    `GEN2-PISOS-REJILLA-CLI-1` entregue sucesores en la rejilla y el
    universo del árbitro" (`data/corrida0/decisiones.tsv:126`), y esos
    sucesores son `CALC_PISOS_SELLADOS`, que es lo único que se lee aquí.
    """
    d = _yaml(PROPUESTA_OLA5)
    reglas_ejes = [r for r in d["reglas_propuestas"] if "_ejes_" in r.get("id", "")]
    idx = indice_identidad()
    suc = sucesiones_identidad()
    res = _resultados_sellados()
    err = _error_de_piso_por_celda(idx)
    por_cell_id = {f["cell_id"]: f for f in lee_tabla_identidad()}
    filas = []
    n_ejes = 0
    for r in reglas_ejes:
        unidad = _unidad_dato(r)
        for desenlace, bloque in _camina_ejes(r):
            n_ejes += 1
            eje = bloque.get("eje")
            for c in (bloque.get("celdas") or []):
                categoria = c.get("celda")
                clave = clave_de_marcador(r["id"], desenlace, eje, categoria, idx)
                piso = _piso_de_fila(clave, idx, res, suc) if clave else None

                piso_tipo = piso_val = piso_ic95 = piso_fuente = ""
                resultado_id = ""
                tipo_inc = "SIN-PISO"
                if piso is None:
                    estado = "SIN-PISO"
                    piso_tipo = "SIN-PISO"
                    piso_fuente = ("SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD"
                                   if clave is None
                                   else "SIN-FILA-EN-TABLA-DE-IDENTIDAD")
                elif not piso["construible"]:
                    estado = "SIN-PISO"
                    piso_tipo = "SIN-PISO"
                    # la causa la escribe la tabla, no este tool.
                    piso_fuente = f"NO-CONSTRUIBLE:{piso['causa']}"
                    if piso["sucede_a"]:
                        piso_fuente += f" · SUCEDE-A:{piso['sucede_a']}"
                else:
                    estado = "SOLO-PISO"
                    piso_tipo = "PERSISTENCIA(t-1)"
                    piso_val = piso["punto"]
                    piso_ic95 = f"[{piso['ic95inf']}, {piso['ic95sup']}]"
                    piso_fuente = piso["fuente"]
                    if piso["sucede_a"]:
                        # dos tablas hablan de esta celda; manda la más
                        # reciente y el marcador nombra a la sucedida.
                        piso_fuente += f" · SUCEDE-A:{piso['sucede_a']}"
                    resultado_id = piso["resultado_id"]
                    tipo_inc = "PERSISTENCIA-T1-BOOTSTRAP-UPM-ESTRATIFICADO"
                    # A-bis 3-4: la unidad del piso y la del R deben coincidir
                    # o la celda no es comparable. No se tira: se rotula.
                    if piso["unit_normalizada"] != unidad:
                        estado = "NO-COMPARABLE"
                        piso_fuente += (f" · UNIDAD-DISCREPANTE:"
                                        f"tabla={piso['unit']}/marcador={unidad}")

                sufijo = f"{desenlace}::" if desenlace else ""
                celda_id = f"MARG::{r['id']}::{sufijo}{eje}::{categoria}"
                error_pp, clase = _columnas_error(
                    err, por_cell_id.get(resultado_id, {}), eje, categoria)
                filas.append({
                    "celda_id": celda_id,
                    "tipo": "MARGINAL",
                    "regla_o_eje_origen": r["id"],
                    "instrumento": r.get("payload", ""),
                    "eje_o_par": eje,
                    "categoria": categoria,
                    "unidad_dato": unidad,
                    "unidad_objetivo": "persona",
                    "estado": estado,
                    "piso_tipo": piso_tipo,
                    "piso": piso_val,
                    "piso_ic95": piso_ic95,
                    "piso_fuente": piso_fuente,
                    "error_piso_pp": error_pp,
                    "clase_persistencia": clase,
                    "R": c.get("p"), "R_ic95inf": (c.get("ic95") or [None, None])[0],
                    "R_ic95sup": (c.get("ic95") or [None, None])[1],
                    # El piso NO es M: acota a los retadores, no identifica
                    # nada y no sustituye a R en la ola que R ya midió
                    # (firma de mesa, GEN2-MARCADOR-PISOS-ENLACE-1). M queda
                    # vacía en toda fila marginal.
                    "M": "", "IC95_inf": "", "IC95_sup": "",
                    "tipo_incertidumbre": tipo_inc,
                    "resultado_id": resultado_id,
                    "decision_ref": "veto:pisos-866" if vetados else "",
                    "emisor_vs_arbitro": "N/A-MARGINAL",
                    "fuente": f"{PROPUESTA_OLA5.name}:{r['id']}",
                })
    universo = {"n_reglas_ejes": len(reglas_ejes), "n_ejes": n_ejes, "n_celdas": len(filas)}
    return filas, universo


# ── (3) universo de CRUCE -- 20 celdas C2 piloteadas + reservadas ─────────

def _celda_d(ruta: Path) -> dict:
    """Todas las celdas-D reales anidan bajo la clave `celda_d:`."""
    return (_yaml(ruta) or {}).get("celda_d") or {}


def _celdas_d_c2() -> list[Path]:
    return [p for p in sorted(CELDAS_D_DIR.glob("*.yaml"))
            if _celda_d(p).get("champion_actual") == "C2"]


def filas_cruce_adoptadas(decisiones: dict) -> list[dict]:
    filas = []
    tiene_adopcion = "adopcion:piso-C2-20-celdas" in decisiones
    for ruta in _celdas_d_c2():
        d = _celda_d(ruta)
        celda_id_base = d["id"]
        # el bloque de sub-celdas vive en `adjudicacion_por_celda`
        # (esquema real de las dos celdas-D con champion C2).
        sub = d.get("adjudicacion_por_celda")
        if not isinstance(sub, dict):
            continue
        calc_ids = {v.get("calc") for v in sub.values() if isinstance(v, dict)}
        resultados: dict[str, float] = {}
        for calc_id in calc_ids:
            if not calc_id:
                continue
            rj = CORRIDA0_DIR / calc_id / "resultados.json"
            if rj.exists():
                resultados.update(json.loads(rj.read_text(encoding="utf-8"))
                                   .get("resultados", {}))
        for sub_celda, info in sub.items():
            if not isinstance(info, dict) or info.get("id_candidato") != "C2":
                continue
            rid_p = info.get("resultado_puntual")
            rid_inf = info.get("ic95inf")
            rid_sup = info.get("ic95sup")
            filas.append({
                "celda_id": f"CRUCE::{celda_id_base}::{sub_celda}",
                "tipo": "CRUCE",
                "regla_o_eje_origen": celda_id_base,
                "instrumento": info.get("calc", ""),
                "eje_o_par": sub_celda,
                "categoria": sub_celda,
                "unidad_dato": _unidad_de_celda_d(celda_id_base),
                "unidad_objetivo": "persona",
                "estado": ("ADOPTADO-POR-FIRMA" if tiene_adopcion
                           else "PISO-ADMISIBLE-NO-ADOPTADO"),
                "piso_tipo": "MARGINAL-SIN-INTERACCION", "piso": "",
                "piso_ic95": "", "piso_fuente": "",
                "R": "", "R_ic95inf": "", "R_ic95sup": "",
                "M": resultados.get(rid_p, ""),
                "IC95_inf": resultados.get(rid_inf, ""),
                "IC95_sup": resultados.get(rid_sup, ""),
                "tipo_incertidumbre": "IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS",
                "resultado_id": rid_p or "",
                "decision_ref": info.get("decision_ref", ""),
                "emisor_vs_arbitro": "N/A-CRUCE",
                "fuente": str(ruta.relative_to(RAIZ)),
            })
    return filas


# ── emision C2 compuesta -- ACTO GEN2-C2-COMPUESTO-RESERVADAS-1 ─────────
# El estado `EMITIDA-SIN-EVALUAR` vive en COLUMNA PROPIA (`emision`), NUNCA
# en `estado`: un cruce emitido sigue `RESERVADA` para evaluacion. Emitir no
# consume la reserva, y por eso las dos cosas son ciertas a la vez y se
# escriben en celdas distintas. Firma de mesa 19/sep/2026, verbatim en
# forense/encargos/2026-09-19-GEN2-C2-COMPUESTO-RESERVADAS-1.md.
EMITIDA = "EMITIDA-SIN-EVALUAR"


def _emisiones_c2():
    """`{celda_id_de_grupo: [fila de emision, ...]}`, o `{}` si el modulo
    de emision no esta. Se importa en vez de leerse del TSV derivado para
    que haya UNA sola fuente de verdad y ningun orden de derivacion que
    respetar."""
    try:
        sys.path.insert(0, str(RAIZ / "tools"))
        import c2_compuesto
    except Exception:
        return {}
    por_grupo: dict[str, list] = {}
    for f in c2_compuesto.emisiones():
        por_grupo.setdefault(f["celda_id_marcador"], []).append(f)
    return por_grupo


# ── IC de las emisiones C2 compuestas -- ACTO GEN2-MARCADOR-ENLACE-2 · P3 ──
# Dos CALC sellados traen IC RÉPLICA POR RÉPLICA con marginales compartidas
# para las emisiones compuestas, y el marcador no se había enterado: las 206
# seguían `NO-PROPAGADA-COVARIANZA-NO-SELLADA` con `ic95_*` vacíos.
#
#   `CALC-C2-COMPUESTO-IC-ENIF2024-0001`  (PR #911)
#   `CALC-C2-COMPUESTO-IC-ENVIPE2025-0001` (PR #916)
#
# El enlace es por IDENTIDAD EXACTA DE CELDA: el sufijo del `resultado_id`
# de la emisión (`RESULT-C2COMP-<sufijo>`) es el mismo sufijo que cada CALC
# usa. NO se empareja por parecido ni por orden: se arma el id y se busca.
# Las dos plantillas difieren y cada una se cita de la spec de su CALC:
#   ENIF   `RESULT-C2IC-ENIF2024-<sufijo>-{IC95INF|IC95SUP|IC-ESTADO}`
#          (data/corrida0/CALC-C2-COMPUESTO-IC-ENIF2024-0001/spec.md:86)
#   ENVIPE `RESULT-C2IC25-{IC95INF|IC95SUP}-<sufijo>`
#          (data/corrida0/CALC-C2-COMPUESTO-IC-ENVIPE2025-0001/spec.md:103)
# ENCIG 2025 no tiene CALC de IC: sus emisiones CONSERVAN `NO-PROPAGADA`.
# Cada entrada: (nombre del CALC, plantilla de id). La plantilla recibe el
# sufijo de celda y el campo (`IC95INF` · `IC95SUP` · `IC-ESTADO`) y rinde
# el id exacto; se declara una vez y sirve para armar y para desarmar.
CALCS_IC_EMISIONES = [
    # spec.md:86 -- el punto `…-P` debe reproducir `RESULT-C2COMP-<sufijo>`,
    # así que el sufijo es literalmente el mismo objeto.
    ("CALC-C2-COMPUESTO-IC-ENIF2024-0001", "RESULT-C2IC-ENIF2024-{suf}-{campo}"),
    # spec.md:103 -- aquí el campo va ANTES del sufijo. Dos formas distintas
    # para el mismo contenido: por eso la plantilla es explícita por CALC y
    # no una regla común inventada aquí.
    ("CALC-C2-COMPUESTO-IC-ENVIPE2025-0001", "RESULT-C2IC25-{campo}-{suf}"),
]
IC_PROPAGADO = "IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS"
IC_NO_PROPAGADO = "NO-PROPAGADA-COVARIANZA-NO-SELLADA"
PREFIJO_EMISION = "RESULT-C2COMP-"


def _sufijos_de_ic(res: dict, plantilla: str) -> set:
    """Sufijos de celda presentes en `res` bajo `plantilla`, desarmados con
    la MISMA plantilla que los arma (nada de recortes a mano)."""
    izq, der = plantilla.format(suf="\x00", campo="IC95INF").split("\x00")
    return {k[len(izq):len(k) - len(der)] for k in res
            if k.startswith(izq) and k.endswith(der) and len(k) > len(izq) + len(der)}


def ic_de_emisiones() -> dict:
    """`resultado_id` de emisión -> `{"ic95_inf", "ic95_sup", "calc",
    "tipo_incertidumbre"}`, SÓLO para las emisiones cuyo IC un CALC selló.

    Una emisión ausente del diccionario conserva `NO-PROPAGADA`: este tool
    no propaga nada, sólo transporta lo sellado. Si un CALC declara un
    `IC-ESTADO` que no es el bootstrap réplica-por-réplica (p. ej. un
    `IC-NO-CONSTRUIBLE`), la celda tampoco entra."""
    out: dict[str, dict] = {}
    for nombre, plantilla in CALCS_IC_EMISIONES:
        rj = CORRIDA0_DIR / nombre / "resultados.json"
        if not rj.exists():
            continue
        try:
            res = json.loads(rj.read_text(encoding="utf-8")).get("resultados", {})
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(res, dict):
            continue
        for suf in _sufijos_de_ic(res, plantilla):
            id_inf = plantilla.format(suf=suf, campo="IC95INF")
            id_sup = plantilla.format(suf=suf, campo="IC95SUP")
            if id_sup not in res:
                continue
            # `IC-ESTADO` es opcional: el CALC de ENVIPE no lo sella. Cuando
            # está y no es el bootstrap réplica-por-réplica, la celda NO entra.
            estado = res.get(plantilla.format(suf=suf, campo="IC-ESTADO"))
            if estado is not None and estado != IC_PROPAGADO:
                continue
            rid = f"{PREFIJO_EMISION}{suf}"
            previo = out.get(rid)
            if previo is not None and previo["calc"] != nombre:
                # dos CALC reclaman la misma celda: no se elige uno.
                out[rid] = {"ic95_inf": "", "ic95_sup": "",
                            "calc": f"COLISION:{previo['calc']}+{nombre}",
                            "tipo_incertidumbre": IC_NO_PROPAGADO}
                continue
            out[rid] = {"ic95_inf": res[id_inf], "ic95_sup": res[id_sup],
                        "calc": nombre, "tipo_incertidumbre": IC_PROPAGADO}
    return out


def _marca_emitidas(filas: list[dict]) -> None:
    """Escribe `emision` sin tocar `estado`. Idempotente."""
    por_grupo = _emisiones_c2()
    for f in filas:
        if f["celda_id"] in por_grupo:
            assert f["estado"] == "RESERVADA", (
                f"{f['celda_id']}: emitir no consume -- una celda emitida debe "
                f"seguir RESERVADA, y esta dice {f['estado']!r}")
            f["emision"] = EMITIDA
            f["decision_ref"] = (f["decision_ref"]
                                 or "emision:c2-compuesto-reservadas")


def filas_cruce_reservadas() -> tuple[list[dict], dict]:
    """Combinaciones de eje-par que los 7 ids `_ejes_` habilitan pero que
    NO están piloteadas (no tienen celda-D con champion C2). Se agrupan por
    par de ejes -- no se enumera celda por celda -- porque el diseño exige
    que TODA celda de cruce no piloteada de las siete entradas `_ejes_`
    nazca RESERVADA sin R (§9(3)); las tres ya consumidas por NC-0328 se
    marcan aparte."""
    d = _yaml(PROPUESTA_OLA5)
    reglas_ejes = [r for r in d["reglas_propuestas"] if "_ejes_" in r.get("id", "")]
    piloteadas = {r["regla_o_eje_origen"] for r in filas_cruce_adoptadas(_lee_decisiones())}
    # pares de ejes ya piloteados (por regla): se infieren de las celdas-D
    pares_piloteados = set()
    for p in _celdas_d_c2():
        cid = _celda_d(p)["id"]
        if cid.startswith("DIN."):
            pares_piloteados.add(("dinero.ahorro.via_informal_ejes_enif2024",
                                  frozenset({"localidad", "edad"})))
        elif cid.startswith("TRA."):
            pares_piloteados.add(("tramite.evasion_norma_ejes_envipe2025",
                                  frozenset({"escolaridad_proxy", "dominio_urbano_rural"})))
    filas = []
    total_reservadas = 0
    total_consumidas = 0
    for r in reglas_ejes:
        ejes_por_bloque: dict[str, int] = {}
        for _desenlace, bloque in _camina_ejes(r):
            eje = bloque.get("eje")
            n = len(bloque.get("celdas") or [])
            ejes_por_bloque[eje] = max(ejes_por_bloque.get(eje, 0), n)
        nombres = sorted(ejes_por_bloque)
        for i in range(len(nombres)):
            for j in range(i + 1, len(nombres)):
                a, b = nombres[i], nombres[j]
                par = frozenset({a, b})
                n_celdas = ejes_por_bloque[a] * ejes_por_bloque[b]
                clave = (r["id"], par)
                if clave in pares_piloteados:
                    continue
                if clave == NC_0328_PAR_CONSUMIDO:
                    estado = "CONSUMIDA-SIN-PILOTO"
                    total_consumidas += n_celdas
                    decision = "NC-0328"
                else:
                    estado = "RESERVADA"
                    total_reservadas += n_celdas
                    decision = ""
                filas.append({
                    "celda_id": f"CRUCE-GRUPO::{r['id']}::{a}x{b}",
                    "tipo": "CRUCE",
                    "regla_o_eje_origen": r["id"],
                    "instrumento": r.get("payload", ""),
                    "eje_o_par": f"{a}x{b}",
                    "categoria": f"{n_celdas} celdas agrupadas",
                    "unidad_dato": _unidad_dato(r),
                    "unidad_objetivo": "persona",
                    "estado": estado,
                    "piso_tipo": "SIN-PISO", "piso": "", "piso_ic95": "",
                    "piso_fuente": "",
                    "R": "", "R_ic95inf": "", "R_ic95sup": "",
                    "M": "", "IC95_inf": "", "IC95_sup": "",
                    "tipo_incertidumbre": "RESERVADA-SIN-R",
                    "resultado_id": "",
                    "decision_ref": decision,
                    "emisor_vs_arbitro": "N/A-CRUCE",
                    "fuente": f"{PROPUESTA_OLA5.name}:{r['id']}",
                })
    _marca_emitidas(filas)
    universo = {"n_grupos_reservados": sum(1 for f in filas if f["estado"] == "RESERVADA"),
                "n_celdas_reservadas": total_reservadas,
                "n_grupos_consumidos": sum(1 for f in filas if f["estado"] == "CONSUMIDA-SIN-PILOTO"),
                "n_celdas_consumidas": total_consumidas}
    return filas, universo


# ── ensamblado + cuatro números derivados al pie ──────────────────────────

def deriva() -> dict:
    decisiones = _lee_decisiones()
    veto_activo = "veto:pisos-866" in decisiones

    nacionales = filas_nacionales()
    marginales, uni_marginal = filas_marginales(vetados=veto_activo)
    cruce_adoptadas = filas_cruce_adoptadas(decisiones)
    cruce_reservadas, uni_reservadas = filas_cruce_reservadas()

    todas = nacionales + marginales + cruce_adoptadas + cruce_reservadas

    # cuatro números derivados al pie del diseño §4
    # cobertura de piso = filas con un piso REAL detrás (no "NO-APLICA",
    # no "SIN-PISO"): las 20 de cruce con MARGINAL-SIN-INTERACCION más las
    # marginales enlazadas a un PERSISTENCIA(t-1) sellado.
    n_con_piso = sum(1 for f in todas
                      if f["piso_tipo"] not in ("", "NO-APLICA", "SIN-PISO"))
    n_evaluadas = len(cruce_adoptadas)  # las que tienen M sellado (== 20)
    n_universo_117 = uni_marginal["n_celdas"] + len(cruce_adoptadas) + \
        uni_reservadas["n_grupos_reservados"] + uni_reservadas["n_grupos_consumidos"]
    n_con_valor_anadido = 0  # M vs R: hoy sin comparación legítima (FP-383)
    n_adoptadas = sum(1 for f in cruce_adoptadas if f["estado"] == "ADOPTADO-POR-FIRMA")
    n_sin_piso = sum(1 for f in todas if f["estado"] == "SIN-PISO")

    resumen = {
        "veto_pisos_activo": veto_activo,
        "universo_i_marginal_ejes": uni_marginal,
        "universo_ii_nacional_censo": len(nacionales),
        "universo_iii_cruce": {
            "adoptadas_c2": len(cruce_adoptadas),
            **uni_reservadas,
        },
        "cobertura_de_piso": n_con_piso,
        "evaluadas": n_evaluadas,
        "universo_marginal_mas_cruce_grupos": n_universo_117,
        "valor_anadido": n_con_valor_anadido,
        "estimador_adoptado": n_adoptadas,
        "sin_piso": n_sin_piso,
        "total_filas": len(todas),
    }
    return {"filas": todas, "resumen": resumen, "decisiones": decisiones}


def escribe_tsv(filas: list[dict]) -> None:
    MARCADOR_TSV.parent.mkdir(parents=True, exist_ok=True)
    with MARCADOR_TSV.open("w", encoding="utf-8", newline="") as fh:
        fh.write("# DERIVADO — NO EDITAR (tools/marcador_segmento.py, "
                 "ACTO GEN2-MARCADOR-REDISENO-1)\n")
        w = csv.DictWriter(fh, fieldnames=COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for f in filas:
            w.writerow({k: f.get(k, "") for k in COLS})
    print(f"ESCRITO {MARCADOR_TSV.relative_to(RAIZ)}: {len(filas)} filas")


def escribe_estimadores_yaml(filas: list[dict]) -> None:
    """P2 (adenda): SOLO las celdas con `champion_actual` C2 y RESULT
    sellado -- nunca desde CALC-PISOS vetados ni desde la rama reservada."""
    adoptadas = [f for f in filas if f["tipo"] == "CRUCE"
                 and f["estado"] == "ADOPTADO-POR-FIRMA" and f["resultado_id"]]
    emitidas = [e for g in _emisiones_c2().values() for e in g]
    # ACTO GEN2-MARCADOR-ENLACE-2 · P3: el IC de la emisión sale del CALC
    # que lo selló, por identidad exacta de celda. Las que ningún CALC
    # cubre (ENCIG 2025 hoy) conservan `NO-PROPAGADA` y `ic95_*` vacíos.
    ic = ic_de_emisiones()
    payload = {
        "_comentario": ("DERIVADO por tools/marcador_segmento.py — NO EDITAR. "
                        "ACTO GEN2-MARCADOR-REDISENO-1 (19/sep/2026). Fuente: "
                        "celdas-D con champion_actual=C2 y sus RESULT sellados; "
                        "cita adopcion:piso-C2-20-celdas de decisiones.tsv."),
        "decision_ref": "adopcion:piso-C2-20-celdas",
        "n_celdas": len(adoptadas),
        # ── clave SEPARADA, y ese es el punto ────────────────────────────
        # Las emitidas NO entran a `celdas`. Viven en su propia clave, con
        # su propio espacio de nombres de id (`CRUCE-EMITIDA::…`, que no
        # puede colisionar con un `CRUCE::…` adoptado), para que la via por
        # defecto del lector no pueda devolverlas ni por accidente ni por
        # un merge de diccionarios mal escrito. Firma de mesa 19/sep/2026:
        # "excluida de la estimacion adoptada del motor y de toda decision
        # automatica"; "una emision no pasa a adoptada por uso".
        "n_emitidas_sin_evaluar": len(emitidas),
        "n_emitidas_con_ic_sellado": sum(1 for e in emitidas
                                          if e["resultado_id"] in ic),
        "emitidas_sin_evaluar": {
            e["resultado_id"].replace(
                "RESULT-C2COMP-", "CRUCE-EMITIDA::", 1): {
                "grupo_marcador": e["celda_id_marcador"],
                "regla_origen": e["regla"],
                "desenlace_id": e["desenlace_id"],
                "par": e["par"],
                "celda_a": e["celda_a"],
                "celda_b": e["celda_b"],
                "resultado_id": e["resultado_id"],
                "punto": e["p_c2"],
                "ic95_inf": ic.get(e["resultado_id"], {}).get("ic95_inf", ""),
                "ic95_sup": ic.get(e["resultado_id"], {}).get("ic95_sup", ""),
                "ic95_fuente": ic.get(e["resultado_id"], {}).get("calc", ""),
                "unidad_dato": e["unidad_dato"],
                # el rótulo de escala manda sobre lo que trae la emisión:
                # `c2_compuesto` nació antes que los dos CALC de IC.
                "tipo_incertidumbre": ic.get(e["resultado_id"], {}).get(
                    "tipo_incertidumbre", e["tipo_incertidumbre"]),
                "supuesto": e["supuesto"],
                "estado": EMITIDA,
                "diagnostico_rango_inf": e["diagnostico_rango_inf"],
                "diagnostico_rango_sup": e["diagnostico_rango_sup"],
                "diagnostico_rango_es_ic": "NO",
            }
            for e in emitidas
        },
        "celdas": {
            f["celda_id"]: {
                "regla_origen": f["regla_o_eje_origen"],
                "resultado_id": f["resultado_id"],
                "punto": f["M"],
                "ic95_inf": f["IC95_inf"],
                "ic95_sup": f["IC95_sup"],
                "unidad_dato": f["unidad_dato"],
                "tipo_incertidumbre": f["tipo_incertidumbre"],
            }
            for f in adoptadas
        },
    }
    ESTIMADORES_YAML.write_text(
        "# DERIVADO — NO EDITAR (tools/marcador_segmento.py, "
        "ACTO GEN2-MARCADOR-REDISENO-1)\n" +
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8")
    print(f"ESCRITO {ESTIMADORES_YAML.relative_to(RAIZ)}: {len(adoptadas)} celdas "
          f"adoptadas + {len(emitidas)} EMITIDA-SIN-EVALUAR (clave aparte)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--escribe", action="store_true",
                     help="escribe marcador-segmento.tsv y estimadores-por-segmento.yaml; "
                          "sin la bandera, solo deriva e imprime el resumen")
    ap.add_argument("--json", action="store_true", help="resumen en JSON")
    args = ap.parse_args()

    v = deriva()
    if args.escribe:
        escribe_tsv(v["filas"])
        escribe_estimadores_yaml(v["filas"])
    if args.json:
        print(json.dumps(v["resumen"], ensure_ascii=False, indent=2, sort_keys=True))
    else:
        r = v["resumen"]
        print(f"veto_pisos_activo={r['veto_pisos_activo']}")
        print(f"universo (i) marginal _ejes_: {r['universo_i_marginal_ejes']}")
        print(f"universo (ii) nacional/compuesto (censo ADR-536): {r['universo_ii_nacional_censo']}")
        print(f"universo (iii) cruce: {r['universo_iii_cruce']}")
        print(f"cobertura_de_piso={r['cobertura_de_piso']}")
        print(f"valor_anadido={r['valor_anadido']}")
        print(f"estimador_adoptado={r['estimador_adoptado']}")
        print(f"sin_piso={r['sin_piso']}")
        print(f"total_filas={r['total_filas']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
