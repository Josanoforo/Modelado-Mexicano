#!/usr/bin/env python3
"""Canal de PINES DE MESA -- ACTO GEN2-RELEVO-TANDA-3, P1 y P2.

Por que existe
==============
`dependencias_numericas_legacy_activas` mide que mediciones de GEN1 ya se
re-hicieron en GEN2 CON TRAZABILIDAD (proposito del contador, firma de mesa
20/sep/2026). Hoy SUBCUENTA: la unica via por la que una lectura sale de
legacy es que el ARCHIVO CONSUMIDOR escriba `corrida0_generacion: GEN2`
(`corrida0._ids_corrida0_declarados`). Hay consumidores que NO PUEDEN
escribirla:

  · `forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv` esta SELLADO -- es un
    TSV de pre-registro bajo `forense/prereg-duelo-v2/**`, perimetro ajeno a
    todo acto de relevo, y escribirle una columna seria reescribir un sello.
  · las specs de los CALC tambien estan selladas: un pin escrito ahi es
    editar una spec congelada (D-18).

Sin un tercer lugar donde escribir, una lectura re-hecha con trazabilidad
sigue contando como legacy por una razon de FONTANERIA, no de evidencia. Este
modulo es ese tercer lugar: un archivo versionado, gobernado por FIRMA DE
MESA, que ni el marco ni las specs pueden cargar.

Que NO es
=========
No mide, no adopta por si solo, no escribe en `milpa/` ni en
`forense/prereg-duelo-v2/**`, y no descubre candidatos. Un pin es una CITA
FIRMADA que este modulo se limita a VALIDAR contra el arbol: si la validacion
falla, el pin se rechaza con codigo y mensaje, y el contador no se mueve.
La adopcion la ejecuta el merge de mesa del PR que trae el pin (E.2).

La regla 4.1 (firma de mesa 21/sep/2026), verbatim
==================================================
  «Una lectura sale de legacy solo por una de dos vias: (i) su cifra la
  produce codigo GEN2 desde un insumo crudo con hash -- microdato o capturas
  selladas --; o (ii) es la lectura de una conducta del motor que ya tiene
  procedencia GEN2, y entonces el pin cita el RESULT de esa conducta, no una
  foto. Ingerir un numero GEN1 como insumo, con hash o sin el, no cuenta
  nunca. El contador muestra las clases sin fundirlas.»

Las cuatro guardas de `valida_pin` son esa regla EN CODIGO. Son lo RIGIDO de
este modulo: ninguna se relaja por conveniencia de un pin concreto.

  (a) SELLO      el CALC citado esta `SELLADA`/`SUPERADO`, `cuenta_gen2 = SI`
                 y su replay dice `REPRODUCE`. Un CALC sin sellar, envuelto
                 legacy, o que no reproduce, no acredita nada.
  (b) CRUDO      `via = i-CRUDO` exige al menos un input `origen: manifiesto`
                 (microdato del corpus) o un manifiesto de capturas selladas.
                 Un CALC que solo lee el repo no produce una cifra desde
                 crudo.
  (c) CONDUCTA   `via = ii-CONDUCTA-GEN2` exige que la conducta citada lleve
                 HOY `corrida0_generacion: GEN2` en `milpa/tramite.yaml` Y
                 que el RESULT pineado sea EXACTAMENTE el que esa conducta
                 declara. Citar el RESULT de otra conducta es un pin a un
                 resultado ajeno.
  (d) INGESTION  el RESULT pineado no puede venir de un CALC que INGIERE: un
                 snapshot de valores, o los `resultados.json` de otra
                 corrida. `RESULT-TRIADA-*-M` es el caso testigo --
                 `CALC-TRIADA-0001` toma los 14 valores M de
                 `snapshot-M-triada-v1_0.json`, y por 4.1 eso no cuenta
                 NUNCA, tenga hash o no.

La llave logica
===============
El pin NO cita `RES-####`: esos ids son POSICIONALES (`corrida0.py:702, :855`)
y se mueven cuando la demanda se re-deriva. Tampoco cita la ruta con version
del consumidor: la mesa TUBERIA midio (caso sintetico de rotacion, 20/sep) que
la unica forma de cita que sobrevive a una rotacion de version es la llave
logica SIN RUTA NI VERSION. `llave_logica()` es el UNICO sitio donde vive esa
traduccion, y `tests/test_pines_mesa.py` la ejerce de ida y vuelta sobre TODOS
los consumidores que el registro deriva hoy.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RUTA_PINES = RAIZ / "data" / "corrida0" / "pines-de-mesa.tsv"

COLUMNAS = ["llave_logica", "result_gen2", "calc_gen2", "via", "firma", "nota"]

VIA_CRUDO = "i-CRUDO"
VIA_CONDUCTA = "ii-CONDUCTA-GEN2"
VIAS = (VIA_CRUDO, VIA_CONDUCTA)

ACEPTADO = "ACEPTADO"

# Prefijos de llave logica, por ARCHIVO consumidor. La version se recorta del
# nombre del archivo, no del contenido: `marco-M-sorteado-v1_3.tsv` y un
# hipotetico `-v1_4` producen la MISMA llave, que es justo el punto.
_ESPACIOS = (
    (re.compile(r"^forense/prereg-duelo-v2/marco-M-sorteado-v\d+_\d+\.tsv$"),
     "marco-M"),
    (re.compile(r"^milpa/tramite\.yaml$"), "tramite"),
    (re.compile(r"^milpa/procedencia\.yaml$"), "procedencia"),
    (re.compile(r"^milpa/catalogo-momentos-v\d+_\d+\.tsv$"),
     "catalogo-momentos"),
    (re.compile(r"^data/curacion-registro/celdas-d/(?P<resto>.+)\.yaml$"),
     "celda-D"),
    (re.compile(r"^marcador$"), "marcador"),
)

SEP = "::"


class PinInvalido(ValueError):
    """Una fila de pines que no se puede ni leer ni traducir."""


def llave_logica(consumidor: str) -> str:
    """`<archivo>:<campo>[:<campo>…]` -> `<espacio>::<campo>[::<campo>…]`.

    UNICO sitio donde vive la traduccion consumidor -> llave. No lleva ruta,
    no lleva version y no lleva `RES-####`, las tres cosas que el encargo
    prohibe y que la mesa TUBERIA midio como fragiles ante una rotacion.

    Un consumidor cuyo archivo no esta en `_ESPACIOS` NO se traduce a ojo:
    levanta `PinInvalido`. Inventar un espacio nuevo aqui convertiria en
    pineable un consumidor que nadie firmo.
    """
    consumidor = str(consumidor)
    archivo, _, resto = consumidor.partition(":")
    for patron, espacio in _ESPACIOS:
        m = patron.match(archivo)
        if not m:
            continue
        partes = [espacio]
        extra = m.groupdict().get("resto")
        if extra:
            partes.append(extra)
        partes.extend(p for p in resto.split(":") if p)
        return SEP.join(partes)
    raise PinInvalido(
        f"CONSUMIDOR-SIN-ESPACIO-LOGICO: {consumidor!r} -- su archivo no esta "
        f"en la tabla de espacios de tools/pines_mesa.py; un espacio nuevo se "
        f"declara ahi, no se infiere")


def indice_llaves(consumidores) -> dict[str, str]:
    """`llave_logica -> consumidor`, la vuelta del viaje.

    Se construye del universo REAL de consumidores que el registro deriva, no
    de una regla inversa escrita a mano: una inversa a mano y la directa se
    separan sin que nadie lo note. Una colision (dos consumidores con la misma
    llave) es un defecto de la llave y PARA aqui, no aguas abajo.
    """
    indice: dict[str, str] = {}
    for c in consumidores:
        try:
            llave = llave_logica(c)
        except PinInvalido:
            continue
        previo = indice.get(llave)
        if previo is not None and previo != c:
            raise PinInvalido(
                f"LLAVE-LOGICA-AMBIGUA: {llave!r} la producen {previo!r} y "
                f"{c!r}")
        indice[llave] = c
    return indice


def lee_pines(ruta: Path = RUTA_PINES) -> list[dict]:
    """Filas del canal, en orden de archivo. Ausente = canal vacio, que NO es
    un error: un arbol sin pines firmados es el estado normal."""
    if not Path(ruta).exists():
        return []
    with Path(ruta).open(encoding="utf-8") as fh:
        lineas = [l for l in fh if not l.startswith("#")]
    filas = list(csv.DictReader(lineas, delimiter="\t"))
    for i, f in enumerate(filas, start=1):
        faltan = [c for c in COLUMNAS if c not in f or f.get(c) is None]
        if faltan:
            raise PinInvalido(
                f"PIN-INCOMPLETO: fila {i} de {ruta} sin columnas "
                f"{', '.join(faltan)}")
        vistos = {f["llave_logica"] for f in filas[:i - 1]}
        if f["llave_logica"] in vistos:
            raise PinInvalido(
                f"PIN-DUPLICADO: {f['llave_logica']} aparece dos veces en "
                f"{ruta}; una lectura tiene un solo pin")
    return filas


# ── contexto: lo que las guardas necesitan saber del arbol ────────────────
# Se pasa como DATOS, no se lee aqui: este modulo no abre `data/corrida0/**`
# ni `milpa/**`. Quien llama (corrida0 / relevo_usos) ya tiene el registro
# derivado y lo presta; asi las guardas se prueban por mutacion sin tocar
# disco y sin que este modulo dependa de corrida0 (que lo importa a el).
#
#   corridas    calc_id -> {"estado", "cuenta_gen2", "resultado_replay",
#                           "resultados_ids": set[str]}
#   specs       calc_id -> spec.yaml ya cargada (dict)
#   conductas   RESULT id -> consumidor de `milpa/tramite.yaml` que lo declara
#               con `corrida0_generacion: GEN2` (y solo esos)

def _ingiere(spec: dict) -> str:
    """Razon por la que un CALC INGIERE en vez de medir, o cadena vacia.

    Ingerir es tomar como insumo un numero ya producido: un snapshot de
    valores, o los `resultados.json` de otra corrida. Por 4.1 eso no releva
    NUNCA, tenga hash o no -- y el hash es justo lo que lo hace parecer
    suficiente.
    """
    for entrada in (spec.get("inputs") or []):
        if not isinstance(entrada, dict):
            continue
        ruta = str(entrada.get("ruta") or "")
        nombre = ruta.rsplit("/", 1)[-1]
        if nombre.startswith("snapshot-") or "-snapshot" in nombre:
            return f"INGIERE-SNAPSHOT:{ruta}"
        if ruta.startswith("data/corrida0/") and nombre == "resultados.json":
            return f"INGIERE-RESULTADOS-DE-OTRA-CORRIDA:{ruta}"
    return ""


def _tiene_crudo(spec: dict) -> bool:
    """Un insumo CRUDO con hash: microdato del manifiesto, o un manifiesto de
    capturas selladas. `origen: repo` a secas no lo es."""
    for entrada in (spec.get("inputs") or []):
        if not isinstance(entrada, dict):
            continue
        if str(entrada.get("origen") or "") == "manifiesto":
            return True
        ruta = str(entrada.get("ruta") or "")
        if "manifiesto-capturas" in ruta.rsplit("/", 1)[-1]:
            return True
    return False


def valida_pin(fila: dict, corridas: dict, specs: dict,
               conductas_gen2: dict) -> tuple[str, str]:
    """Las cuatro guardas de 4.1. Devuelve `(ACEPTADO, "")` o
    `("RECHAZADO-<codigo>", "<por que>")`.

    El mensaje dice POR QUE, no solo que: un rechazo que no se puede leer se
    resuelve relajando la guarda, que es el defecto que la guarda existe para
    impedir.
    """
    llave = str(fila.get("llave_logica") or "")
    result = str(fila.get("result_gen2") or "")
    calc = str(fila.get("calc_gen2") or "")
    via = str(fila.get("via") or "")
    firma = str(fila.get("firma") or "")

    if via not in VIAS:
        return ("RECHAZADO-VIA-DESCONOCIDA",
                f"{llave}: via={via!r} no es una de {VIAS} (4.1 declara DOS "
                f"vias y ninguna tercera)")
    if not firma.strip():
        return ("RECHAZADO-SIN-FIRMA",
                f"{llave}: el canal es de FIRMA DE MESA; una fila sin "
                f"`firma` (archivo y fecha) no es un pin")

    c = corridas.get(calc)
    if c is None:
        return ("RECHAZADO-CALC-INEXISTENTE",
                f"{llave}: calc_gen2={calc!r} no esta en el registro")
    if not str(c.get("estado", "")).startswith(("SELLADA", "SUPERADO")):
        return ("RECHAZADO-CALC-NO-SELLADA",
                f"{llave}: {calc} esta {c.get('estado')!r}; guarda (a) exige "
                f"SELLADA")
    if str(c.get("cuenta_gen2", "")) != "SI":
        return ("RECHAZADO-CALC-NO-CUENTA-GEN2",
                f"{llave}: {calc} declara cuenta_gen2="
                f"{c.get('cuenta_gen2')!r}; guarda (a) exige SI")
    if not str(c.get("resultado_replay", "")).startswith("REPRODUCE"):
        return ("RECHAZADO-CALC-NO-REPRODUCE",
                f"{llave}: el replay de {calc} dice "
                f"{c.get('resultado_replay')!r}; guarda (a) exige REPRODUCE")
    if result not in set(c.get("resultados_ids") or ()):
        return ("RECHAZADO-RESULT-AJENO-AL-CALC",
                f"{llave}: {result} no es un resultado de {calc}")

    spec = specs.get(calc) or {}
    razon_ingestion = _ingiere(spec)
    if razon_ingestion:
        return ("RECHAZADO-RESULT-INGERIDO",
                f"{llave}: {calc} {razon_ingestion} -- 4.1: «Ingerir un "
                f"numero GEN1 como insumo, con hash o sin el, no cuenta "
                f"nunca»")

    if via == VIA_CRUDO:
        if not _tiene_crudo(spec):
            return ("RECHAZADO-SIN-INSUMO-CRUDO",
                    f"{llave}: {calc} no declara ningun input "
                    f"`origen: manifiesto` ni manifiesto de capturas "
                    f"selladas; la via (i) exige insumo crudo con hash")
        return (ACEPTADO, "")

    # via == VIA_CONDUCTA
    consumidor_conducta = conductas_gen2.get(result)
    if not consumidor_conducta:
        return ("RECHAZADO-CONDUCTA-NO-GEN2",
                f"{llave}: ninguna conducta de milpa/tramite.yaml declara HOY "
                f"{result} con `corrida0_generacion: GEN2`; la via (ii) lee "
                f"una conducta que YA tiene procedencia GEN2, no una que "
                f"podria tenerla")
    return (ACEPTADO, "")


def pines_validados(corridas: dict, specs: dict, conductas_gen2: dict,
                    ruta: Path = RUTA_PINES) -> tuple[dict, list[str]]:
    """`llave_logica -> fila` para los pines que pasan, y la lista de
    rechazos legibles. Un pin rechazado NO tumba a los demas: el contador se
    mueve por los que pasan y el rechazo se reporta."""
    aceptados: dict[str, dict] = {}
    rechazos: list[str] = []
    for fila in lee_pines(ruta):
        estado, motivo = valida_pin(fila, corridas, specs, conductas_gen2)
        if estado == ACEPTADO:
            aceptados[fila["llave_logica"]] = fila
        else:
            rechazos.append(f"{estado}: {motivo}")
    return aceptados, rechazos
