"""ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-2/-3 · reconstruye la fila completa
de `resultados.tsv` tras la normalizacion de COMMIT-A y COMMIT-B.

`tolerancia`, `funciones_dependencia` y `fuente_replay` salieron de
`resultados.tsv`: son identicas para todo RESULT de la misma corrida
(verificado por comando en #1109 -- 0/313 corridas con valor no
constante), asi que viven una vez por corrida en `corridas.tsv`. Un
consumidor que necesite esos tres campos por RESULT los recupera con
`join_resultado`, que hace exactamente el `join` por `corrida_id` que la
firma de mesa de `GEN2-TUBERIA-VISTA-NORMALIZADA-2` describe -- no
reinventa el dato, lo busca donde vive ahora.

`camino_linaje` (COMMIT-B, ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-3) tomo el
camino opuesto: cardinalidad medida 65 287/65 287 = 1.0 sobre
`resultados.tsv` en main (NC-260924-GEN2-TUBERIA-VISTA-NORMALIZADA-2-f1b2-01)
-- con la regla del encargo (>=0.5 -> bajo demanda, no dedup) no vive en
ninguna tabla. `join_resultado`/`leer_resultados_join` lo RE-DERIVAN
resultado -> corrida -> spec -> inputs llamando a la misma maquina que
`corrida0.py` usa para escribirlo hoy (`_lee_oferta` + `_propaga_envuelto`
sobre `decisiones.tsv`) -- no una segunda implementacion del mismo
calculo, la misma, para que el texto salga byte a byte igual (medido:
tests/test_vista.py::PruebaCaminoLinajeBajoDemanda, muestra de 500 filas
reales). Ese calculo es caro (recorre las ~310 carpetas `CALC-*/`, igual
que `corrida0.py registro --escribe`: ~70s medido 24/sep/2026) por eso se
cachea en el proceso (`_linajes_cache`, un solo calculo por invocacion) y
solo se dispara para una fila OFERTA que no trae ya el campo -- una fila
DEMANDA no lo necesita (patron mecanico `DEMANDA-PENDIENTE`) y un fixture
sintetico que ya declara `camino_linaje` nunca lo dispara.

No lee microdato, no mide, no adopta: es lectura pura sobre las vistas ya
derivadas (mas, para `camino_linaje`, sobre los `spec.yaml`/`ejecucion.json`
ya sellados de cada `CALC-*/` -- ningun archivo vivo, ningun microdato).
"""

from __future__ import annotations

import csv
import functools
import hashlib
import json
import sys
from pathlib import Path

# Mismo patron que tools/corrida0.py:102 -- corridas.tsv/resultados.tsv
# tienen campos (camino_linaje, funciones_dependencia) mas largos que el
# limite por defecto de 131072 bytes del modulo csv.
csv.field_size_limit(sys.maxsize)

RAIZ = Path(__file__).resolve().parent.parent
CORRIDAS = RAIZ / "data" / "corrida0"
VISTA_CORRIDAS = CORRIDAS / "corridas.tsv"
VISTA_RESULTADOS = CORRIDAS / "resultados.tsv"

# Campos que COMMIT-A movio de resultados.tsv a corridas.tsv (constantes
# por corrida_id). Un cambio a este conjunto es tambien un cambio a
# COLS_VISTA_RESULTADOS/COLS_VISTA_CORRIDAS en tools/corrida0.py -- ambos
# se editan juntos, nunca uno sin el otro.
CAMPOS_MOVIDOS_A_CORRIDA = ("tolerancia", "funciones_dependencia", "fuente_replay")

SIN_OFERTA_EN_VISTA = "SIN-OFERTA-EN-VISTA"


def _corrida0():
    """Import diferido de `tools/corrida0.py` (mismo patron que
    `tools/adq_investigacion.py`: este modulo se importa a veces como
    `vista` a secas -- sin la raiz del repo en `sys.path` -- y a veces
    como `tools.vista`; un `import corrida0` a secas funciona en los dos
    casos porque `corrida0.py` vive en el mismo directorio)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import corrida0
    return corrida0


def linajes_por_resultado(oferta: list[dict] | None = None,
                           decisiones: dict | None = None) -> dict[tuple[str, str], str]:
    """`{(corrida_id, resultado_id): camino_linaje}` para toda fila OFERTA,
    derivado bajo demanda resultado -> corrida -> spec -> inputs
    (COMMIT-B). Llama a `corrida0._lee_oferta(False)` (sin `--verifica`:
    esto es trazabilidad de procedencia, no replay de medicion) y
    `corrida0._propaga_envuelto` -- la misma maquina que escribia la
    columna hasta COMMIT-A, re-ejecutada en vez de reinventada para
    garantizar el mismo texto. `oferta`/`decisiones` explicitos (para
    tests con datos sinteticos) evitan la relectura de disco."""
    c0 = _corrida0()
    if oferta is None:
        oferta = c0._lee_oferta(False)
    if decisiones is None:
        decisiones = c0._lee_decisiones()
    c0._propaga_envuelto(oferta, decisiones)
    mapa: dict[tuple[str, str], str] = {}
    for o in oferta:
        corrida_id = (o.get("ejec") or {}).get("corrida_id") or o["calc_id"]
        for rid, linaje in o["linajes_resultados"].items():
            mapa[(corrida_id, rid)] = linaje["camino"]
    return mapa


@functools.lru_cache(maxsize=1)
def _linajes_cache() -> dict[tuple[str, str], str]:
    return linajes_por_resultado()


def _deriva_camino_linaje(fila: dict,
                           linajes: dict[tuple[str, str], str] | None) -> str | None:
    """`None` si `origen` no es `DEMANDA` ni `OFERTA` (fixture legacy que
    no lo declara, p.ej. los de `JoinResultado` en `tests/test_vista.py`
    escritos para COMMIT-A): NO dispara el cache -- `join_resultado`
    entonces deja el campo ausente, igual que antes de COMMIT-B. Una fila
    real de `resultados.tsv` siempre trae `origen` (`DEMANDA` u `OFERTA`,
    COLS_VISTA_RESULTADOS), asi que esta rama es solo para fixtures
    sinteticos incompletos -- nunca para una vista real."""
    origen = fila.get("origen")
    if origen not in ("DEMANDA", "OFERTA"):
        return None
    corrida_id = fila.get("corrida_id", "")
    resultado_id = fila.get("resultado_id", "")
    if origen == "DEMANDA":
        # Mismo patron mecanico que corrida0.py::_filas_registro escribe
        # para una fila DEMANDA (sin spec, nada que resolver todavia).
        return f"{corrida_id}/{resultado_id} -> DEMANDA-PENDIENTE"
    mapa = linajes if linajes is not None else _linajes_cache()
    return mapa.get((corrida_id, resultado_id), SIN_OFERTA_EN_VISTA)


def _leer_tsv_derivado(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8") as fh:
        lineas = [l for l in fh if not l.startswith("#")]
    return list(csv.DictReader(lineas, delimiter="\t"))


def corridas_por_id(ruta: Path = VISTA_CORRIDAS) -> dict[str, dict]:
    """`{corrida_id: fila}` de `corridas.tsv`, para pasar a `join_resultado`.
    `{}` si el archivo no existe (fixture sintetico de un solo TSV, o un
    consumidor que solo necesita camino_linaje): `join_resultado` cae al
    valor propio de la fila cuando lo tiene."""
    if not ruta.exists():
        return {}
    return {f["corrida_id"]: f for f in _leer_tsv_derivado(ruta)}


def join_resultado(fila_resultado: dict, corridas: dict[str, dict],
                    linajes: dict[tuple[str, str], str] | None = None) -> dict:
    """Devuelve una copia de `fila_resultado` con `tolerancia`,
    `funciones_dependencia`, `fuente_replay` y `camino_linaje` completos.
    No muta `fila_resultado`.

    Regla, igual para los cuatro campos: si la propia fila YA trae el
    campo (formato previo a COMMIT-A/B, o un fixture sintetico que lo
    declara a mano), ese valor manda -- no se pisa. Los tres primeros,
    ausentes, se buscan en `corridas` (join barato por `corrida_id`); si
    tampoco estan ahi (vista desincronizada, o `corridas` vino vacio por
    archivo ausente), quedan en `SIN-CORRIDA-EN-VISTA` en vez de lanzar
    `KeyError`.

    `camino_linaje`, ausente, se DERIVA (COMMIT-B) SOLO si la fila declara
    `origen` (`DEMANDA` u `OFERTA` -- toda fila real de `resultados.tsv` lo
    trae; un fixture legacy que no lo declara queda sin el campo, igual
    que antes de COMMIT-B, en vez de disparar un calculo que no pidio).
    `DEMANDA` es el patron mecanico `.../... -> DEMANDA-PENDIENTE`, gratis.
    `OFERTA` usa `linajes` (si el llamador ya lo calculo, p.ej. para no
    pagar el costo por fila) o, si no, el cache del proceso
    (`_linajes_cache`, un solo calculo de toda la oferta la primera vez
    que hace falta). Sin oferta que lo cubra (calc_id fuera del
    `_dirs_calc()` actual): `SIN-OFERTA-EN-VISTA`."""
    completa = dict(fila_resultado)
    corrida = corridas.get(fila_resultado.get("corrida_id"), {})
    for campo in CAMPOS_MOVIDOS_A_CORRIDA:
        if campo not in completa:
            completa[campo] = corrida.get(campo, "SIN-CORRIDA-EN-VISTA")
    if "camino_linaje" not in completa:
        derivado = _deriva_camino_linaje(completa, linajes)
        if derivado is not None:
            completa["camino_linaje"] = derivado
    return completa


def leer_resultados_join(
    ruta_resultados: Path = VISTA_RESULTADOS,
    ruta_corridas: Path = VISTA_CORRIDAS,
) -> list[dict]:
    """`resultados.tsv` con los campos de corrida y `camino_linaje` ya
    reconstruidos por fila -- el punto de entrada normal para un
    consumidor que no quiera hacer el join a mano. `camino_linaje` se
    deriva bajo demanda (via el cache del proceso) solo si alguna fila
    OFERTA lo necesita -- ver `join_resultado`."""
    corridas = corridas_por_id(ruta_corridas)
    return [join_resultado(resuelve_fila(f), corridas)
            for f in _leer_tsv_derivado(ruta_resultados)]


# ── ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-4 · COMMIT-B: `valor` por referencia ──
# Un RESULT es un número con unidad; una lista es una tabla. Todo `valor`
# cuya representación en la vista pase de UMBRAL_VALOR_BYTES (UTF-8) se
# escribe BYTE A BYTE a `data/corrida0/<spec_id>/valores-vista/<resultado_id>.<ext>`
# y la celda lleva `REF:<ruta relativa a la raíz>#sha256:<hex>`. La tabla es
# DERIVADA del `resultados.json` sellado (se regenera en cada `registro
# --escribe`), no un sello nuevo. `.json` si el texto parsea como JSON (es el
# caso medido: listas serializadas), `.txt` si no -- nunca se re-serializa:
# la equivalencia `valor_de(id)` antes/después es byte a byte.
UMBRAL_VALOR_BYTES = 1024
PREFIJO_REF = "REF:"
# `valores-vista/`, no `tablas/` (como decía el encargo): `tablas/` ya existe
# SELLADA dentro de CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-000{1,2} (8
# archivos, `git ls-files`), y es donde COMMIT-C pone las tablas que un
# medidor produce ANTES de sellar. Derivado y sellado no comparten carpeta.
DIR_VALORES = "valores-vista"


class ReferenciaRota(ValueError):
    """La celda `REF:` apunta a un archivo ausente o cuyo sha256 no casa.
    Falla en voz alta (D-23): nunca se devuelve la referencia como valor."""


def es_referencia(valor) -> bool:
    return isinstance(valor, str) and valor.startswith(PREFIJO_REF)


def resuelve_valor(valor, raiz: Path = RAIZ):
    """Texto original de una celda `valor`. Una celda que no es `REF:` se
    devuelve tal cual (idéntica a antes de COMMIT-B)."""
    if not es_referencia(valor):
        return valor
    ruta_rel, _, sha = valor[len(PREFIJO_REF):].partition("#sha256:")
    ruta = raiz / ruta_rel
    if not ruta.exists():
        raise ReferenciaRota(f"{valor}: {ruta_rel} no existe")
    datos = ruta.read_bytes()
    if hashlib.sha256(datos).hexdigest() != sha:
        raise ReferenciaRota(f"{valor}: sha256 de {ruta_rel} no casa")
    return datos.decode("utf-8")


def resuelve_fila(fila: dict, raiz: Path = RAIZ) -> dict:
    """Copia de la fila con `valor` resuelto; las demás columnas intactas."""
    if not es_referencia(fila.get("valor")):
        return fila
    return {**fila, "valor": resuelve_valor(fila["valor"], raiz)}


def ruta_tabla(spec_id: str, resultado_id: str, texto: str) -> str:
    try:
        json.loads(texto)
        ext = "json"
    except (ValueError, TypeError):
        ext = "txt"
    return f"data/corrida0/{spec_id}/{DIR_VALORES}/{resultado_id}.{ext}"


def referencia_valor(fila: dict, raiz: Path = RAIZ, escribe: bool = True) -> dict:
    """Lado escritor. Devuelve la fila con `valor` sustituido por `REF:` si
    su texto pasa del umbral; con `escribe`, deja la tabla en disco (se
    reescribe sólo si el contenido cambió). Idempotente: una celda que ya
    es `REF:` se resuelve y se vuelve a referenciar (misma ruta, mismo sha)."""
    texto = resuelve_valor(fila.get("valor"), raiz)
    texto = "" if texto is None else str(texto)
    datos = texto.encode("utf-8")
    if len(datos) <= UMBRAL_VALOR_BYTES:
        return {**fila, "valor": texto} if es_referencia(fila.get("valor")) else fila
    rel = ruta_tabla(fila["spec_id"], fila["resultado_id"], texto)
    if escribe:
        ruta = raiz / rel
        if not ruta.exists() or ruta.read_bytes() != datos:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.write_bytes(datos)
    return {**fila, "valor": f"{PREFIJO_REF}{rel}#sha256:{hashlib.sha256(datos).hexdigest()}"}


def valor_de(resultado_id: str, corrida_id: str | None = None,
             ruta_resultados: Path = VISTA_RESULTADOS, raiz: Path = RAIZ):
    """El `valor` de un RESULT tal como lo sella su `resultados.json`,
    resolviendo la referencia si la vista la trae. Con varias corridas para
    el mismo id (replays), `corrida_id` desambigua; sin él, varias filas con
    valores distintos es un error en voz alta. `KeyError` si no está."""
    filas = [f for f in _leer_tsv_derivado(ruta_resultados)
             if f.get("resultado_id") == resultado_id
             and (corrida_id is None or f.get("corrida_id") == corrida_id)]
    if not filas:
        raise KeyError(f"{resultado_id} no está en {ruta_resultados.name}")
    valores = {resuelve_valor(f.get("valor"), raiz) for f in filas}
    if len(valores) > 1:
        raise ValueError(f"{resultado_id}: {len(filas)} corridas con valores distintos; pasa corrida_id")
    return valores.pop()
