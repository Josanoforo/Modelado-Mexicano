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
                 y su replay ACREDITA. Un CALC sin sellar, envuelto legacy, o
                 que no reproduce, no acredita nada. Desde TANDA-5 (P1, firma
                 F-R del 22/sep/2026) el replay se lee POR EJE en las TRES
                 vias por igual: exigen que el eje RESULTADO sea afirmativo --
                 `REPRODUCE` o `REPLICA-RESULTADO · CONTEXTO-DISTINTO` -- y el
                 CONTEXTO se declara en la `nota` del pin. `NO-REPRODUCE*` y
                 `NO-EJECUTABLE` quedan fuera por las tres vias; `NO-VERIFICABLE`
                 tampoco es afirmativo por si solo.
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
                 NUNCA, tenga hash o no. La UNICA excepcion es la clase
                 (iii) `iii-DERIVADO-DE-GEN2` (firma 7bf5-02, 21/sep/2026),
                 y solo bajo las cuatro condiciones de `_valida_derivado`:
                 un padre unico, sellado, que cuenta, con replay afirmativo,
                 y que no ingiere a su vez. Ingerir GEN1 sigue sin contar.

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
# ACTO GEN2-RELEVO-TANDA-4 · P3. Tercera clase, firma de direccion 7bf5-02
# bajo el mandato de mesa del 21/sep/2026: «Un derivado determinista de un
# RESULT GEN2 releva en clase propia, `iii-DERIVADO-DE-GEN2`, que el contador
# muestra sin fundir con (i) y (ii). La clase exige que TODO lo ingerido sea
# RESULT de un CALC sellado, que cuenta y cuyo replay es afirmativo en
# RESULTADO; un derivado de un derivado no entra. "Ingerir un numero GEN1 no
# cuenta nunca" queda intacto.»
VIA_DERIVADO = "iii-DERIVADO-DE-GEN2"
VIAS = (VIA_CRUDO, VIA_CONDUCTA, VIA_DERIVADO)

ACEPTADO = "ACEPTADO"

# Separador del eje RESULTADO dentro del veredicto compuesto de `verify`
# (`corrida0.verify`: `<RESULTADO> · CONTEXTO-DISTINTO`). El primer token es
# el eje RESULTADO; el resto habla del CONTEXTO.
_SEP_EJES = " · "

_PREFIJO_DE_ARBOL_CORRIDA0 = "data/corrida0/"

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
    # D-r3, firmada por mesa el 21/sep/2026 con el nombre `cortes-C1::<corte>`
    # (ACTO GEN2-TUBERIA-RES-LLAVE-1, P1). Se llama `cortes-C1` y no `celdas`
    # para que no se confunda con `celda-D::`. Declarar el espacio NO vuelve
    # pineable nada por si solo: un pin sigue exigiendo firma de mesa y las
    # cuatro guardas de 4.1.
    (re.compile(r"^milpa/src/celdas\.py$"), "cortes-C1"),
)

SEP = "::"

# Tokens del `resto` que el nombre del espacio YA dice, y que por eso no se
# repiten dentro de la llave. Mesa firmo `cortes-C1::<corte>`, no
# `cortes-C1::CORTES_C1::<corte>`: la tabla del archivo consumidor es
# precisamente lo que el espacio nombra. Se declara aqui, token por token, y
# solo se absorbe si va al PRINCIPIO del resto -- nunca a ojo.
_RESTO_REDUNDANTE = {
    "cortes-C1": ("CORTES_C1",),
}


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
        campos = [p for p in resto.split(":") if p]
        redundante = _RESTO_REDUNDANTE.get(espacio, ())
        if campos and campos[0] in redundante:
            campos = campos[1:]
        partes.extend(campos)
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


def vocabulario_replay() -> frozenset[str]:
    """Los veredictos de replay que CONCLUYEN sobre la reproducibilidad.

    Se IMPORTA de `corrida0` (tarde, para no cerrar el ciclo: `corrida0` ya
    importa este modulo). No se teclea aqui una segunda copia: una lista a
    mano y el vocabulario real se separan sin que nadie lo note, que es el
    defecto de procedencia que §2 prohibe.
    """
    import corrida0  # noqa: PLC0415  -- tardio a proposito (ciclo)
    return frozenset(corrida0.VEREDICTOS_CONCLUYENTES)


def veredictos_afirmativos_en_resultado(vocabulario=None) -> frozenset[str]:
    """Los veredictos cuyo EJE RESULTADO dice que el numero salio igual.

    Regla, no lista: el eje RESULTADO es el PRIMER token del veredicto
    compuesto, y `NO-` lo niega. Del vocabulario real
    (`REPRODUCE` · `NO-REPRODUCE` · `REPLICA-RESULTADO · CONTEXTO-DISTINTO` ·
    `NO-REPRODUCE · CONTEXTO-DISTINTO`) quedan los dos primeros afirmativos.
    `NO-EJECUTABLE` y `NO-VERIFICABLE` no estan en el vocabulario concluyente
    -- son limitacion de la sesion, no hallazgo sobre el numero (E.3) -- y por
    eso NO son afirmativos por la via corta: no entran al conjunto.
    """
    if vocabulario is None:
        vocabulario = vocabulario_replay()
    return frozenset(
        v for v in vocabulario
        if not str(v).split(_SEP_EJES)[0].strip().startswith("NO-"))


def _calcs_ingeridos(spec: dict) -> tuple[set[str], list[str]]:
    """`(CALCs cuyo arbol se ingiere, inputs que NO vienen de un CALC)`.

    Un input bajo `data/corrida0/<CALC>/…` es un numero que otra corrida ya
    produjo. Todo lo demas -- un TSV de GEN1, un snapshot, un microdato --
    cae en la segunda lista y la clase (iii) lo rechaza: la firma exige que
    TODO lo ingerido sea del padre.
    """
    calcs: set[str] = set()
    ajenos: list[str] = []
    for entrada in (spec.get("inputs") or []):
        if not isinstance(entrada, dict):
            continue
        ruta = str(entrada.get("ruta") or "")
        if ruta.startswith(_PREFIJO_DE_ARBOL_CORRIDA0):
            resto = ruta[len(_PREFIJO_DE_ARBOL_CORRIDA0):]
            calc, _, cola = resto.partition("/")
            if calc and cola:
                calcs.add(calc)
                continue
        ajenos.append(ruta or str(entrada.get("id") or "SIN-RUTA"))
    return calcs, ajenos


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


def _valida_derivado(llave: str, calc: str, spec: dict, corridas: dict,
                     specs: dict) -> tuple[str, str]:
    """Las CUATRO condiciones de la firma 7bf5-02 para la clase (iii).

    Es la unica puerta por la que un CALC que INGIERE releva algo, y por eso
    es la mas estrecha de las tres:

      1. TODO lo ingerido viene de UN solo CALC -- el padre. Cualquier input
         que no viva bajo `data/corrida0/<padre>/` (un TSV de GEN1, un
         snapshot, un microdato) tumba el pin: «Ingerir un numero GEN1 no
         cuenta nunca» (4.1) sigue intacto.
      2. Ese padre esta SELLADA/SUPERADO en el registro.
      3. Ese padre `cuenta_gen2 = SI`.
      4. El replay del padre es afirmativo en el eje RESULTADO.

    Y, ademas, el padre NO puede ingerir a su vez: un derivado de un derivado
    no entra (la firma lo dice literal). Sin esta ultima comprobacion la
    cadena se alarga sin limite y la distancia al crudo deja de ser auditable
    en un solo salto.
    """
    ingeridos, ajenos = _calcs_ingeridos(spec)
    if ajenos:
        return ("RECHAZADO-DERIVADO-INGIERE-AJENO",
                f"{llave}: {calc} ingiere insumos que no son del padre "
                f"({', '.join(sorted(ajenos))}); la clase (iii) exige que "
                f"TODO lo ingerido sea RESULT de un CALC GEN2 -- 4.1: "
                f"«Ingerir un numero GEN1 como insumo, con hash o sin el, no "
                f"cuenta nunca»")
    if len(ingeridos) != 1:
        return ("RECHAZADO-DERIVADO-SIN-PADRE-UNICO",
                f"{llave}: {calc} ingiere de {sorted(ingeridos) or 'nada'}; "
                f"la clase (iii) exige EXACTAMENTE un padre")
    padre = next(iter(ingeridos))

    p = corridas.get(padre)
    if p is None:
        return ("RECHAZADO-DERIVADO-PADRE-INEXISTENTE",
                f"{llave}: el padre {padre} de {calc} no esta en el registro")
    if not str(p.get("estado", "")).startswith(("SELLADA", "SUPERADO")):
        return ("RECHAZADO-DERIVADO-PADRE-NO-SELLADA",
                f"{llave}: el padre {padre} esta {p.get('estado')!r}; la "
                f"clase (iii) exige un padre SELLADA")
    if str(p.get("cuenta_gen2", "")) != "SI":
        return ("RECHAZADO-DERIVADO-PADRE-NO-CUENTA-GEN2",
                f"{llave}: el padre {padre} declara cuenta_gen2="
                f"{p.get('cuenta_gen2')!r}; la clase (iii) exige SI -- un "
                f"derivado no puede acreditar mas que su padre")
    replay_padre = str(p.get("resultado_replay", ""))
    if replay_padre not in veredictos_afirmativos_en_resultado():
        return ("RECHAZADO-DERIVADO-PADRE-NO-REPRODUCE",
                f"{llave}: el replay del padre {padre} dice {replay_padre!r},"
                f" que no es afirmativo en el eje RESULTADO")

    spec_padre = specs.get(padre) or {}
    abuelos, _ = _calcs_ingeridos(spec_padre)
    razon_padre = _ingiere(spec_padre)
    if abuelos or razon_padre:
        detalle = (f"ingiere a su vez de {sorted(abuelos)}" if abuelos
                   else razon_padre)
        return ("RECHAZADO-DERIVADO-DE-DERIVADO",
                f"{llave}: el padre {padre} {detalle}; la firma 7bf5-02 dice "
                f"literal que «un derivado de un derivado no entra»")
    return (ACEPTADO, "")


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
                f"{llave}: via={via!r} no es una de {VIAS} (las vias son "
                f"lista cerrada: las dos de 4.1 mas la clase (iii) que la "
                f"firma 7bf5-02 abrio; una cuarta se firma, no se infiere)")
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
    # Guarda (a), eje RESULTADO (ACTO GEN2-RELEVO-TANDA-4 · P1; extendida a
    # la via (i) por ACTO GEN2-RELEVO-TANDA-5 · P1, firma de mesa F-R del
    # 22/sep/2026: «La lectura del eje RESULTADO del replay vale igual para
    # la via (i); el CONTEXTO se declara en la nota de cada pin»). Las tres
    # vias leen el EJE RESULTADO del veredicto compuesto y declaran el
    # CONTEXTO en la `nota` del pin: un cambio de contexto ajeno a la
    # lectura -- otro commit en una herramienta del arbol -- no es un
    # hallazgo sobre el numero, y dejar fuera un sello cuyo resultado
    # replica era el defecto que TANDA-4 corrigio para (ii)/(iii); F-R lo
    # extiende a (i) porque el mismo razonamiento aplica igual. `NO-REPRODUCE*`
    # y `NO-EJECUTABLE` siguen fuera por las tres vias; `NO-VERIFICABLE` (el
    # eje RESULTADO cuando la sesion no pudo pronunciarse) tampoco esta en el
    # vocabulario CONCLUYENTE y por tanto tampoco es afirmativo -- no basta
    # por si solo.
    replay = str(c.get("resultado_replay", ""))
    if replay not in veredictos_afirmativos_en_resultado():
        return ("RECHAZADO-CALC-NO-REPRODUCE",
                f"{llave}: el replay de {calc} dice {replay!r}, que no es "
                f"afirmativo en el eje RESULTADO "
                f"({sorted(veredictos_afirmativos_en_resultado())}); guarda "
                f"(a) exige que el numero haya vuelto a salir igual")
    if result not in set(c.get("resultados_ids") or ()):
        return ("RECHAZADO-RESULT-AJENO-AL-CALC",
                f"{llave}: {result} no es un resultado de {calc}")

    spec = specs.get(calc) or {}

    if via == VIA_DERIVADO:
        return _valida_derivado(llave, calc, spec, corridas, specs)

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
