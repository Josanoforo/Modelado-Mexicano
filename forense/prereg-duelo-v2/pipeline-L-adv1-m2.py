#!/usr/bin/env python3
"""
`ADV1-M2` · tubería L — elicitación mecánica y ciega del corredor L.

ACTO: DUELO-PREREG-V2 (nube, Opus). Escrito 20/ago/2026. Gate: T-SELLO + ACT-PIL-2 fusionados.

*** ESTE SCRIPT NO SE EJECUTA EN ESTE ACTO. *** Es pre-registro ejecutable: la
especificación se congela AQUÍ, en repo, antes de correr una sola celda contra
un modelo real -- exactamente lo que ADV1-M2 exige ("sin humano en el bucle",
"hashes de los cuatro corredores comprometidos antes de que R exista"). Quien
lo corra lo hace en una sesión limpia fuera de este proyecto (D-iii, TRANSFER
§4: "sesiones limpias fuera del proyecto, mismo patrón que estas
adversariales"), nunca dentro de esta caja NUBE repo-only, y nunca antes de
que el marco de candidatas (`forense/marco-candidatas-piloto-v1_0.tsv`,
ya construido por ACT-PIL-2, NO reconstruido aquí) y el sorteo con semilla
pública (D-iii, pendiente de ACT-PIL-3) existan.

Fuente normativa, verbatim (CAREO-ADV-DUELO-diseno-v2-2026-08-19.md §B, M2):

    "M2 · Elicitación mecánica y ciega. Un script toma la spec y produce las
    respuestas sin humano en el bucle: L con modelo+versión+fecha+temperatura
    fijados, k=5-10 corridas, agregado pre-registrado (mediana+cuantiles;
    self-consistency en categóricas), TODAS las corridas registradas sin
    descarte, dispersión reportada; las sesiones L las corre alguien/algo
    ajeno a las celdas de M (sesiones limpias, como estas adversariales);
    dos variantes L-solo / L+corpus. M emite punto e intervalo de su
    incertidumbre de parámetros. Hashes de los cuatro corredores
    comprometidos antes de que R exista."

Los "cuatro corredores" son L, M, B, E (CAREO §B, primera línea del diseño
v2: "Corredores: cuatro. L ... M ... B ... E ..."). Este script produce y
compromete (hashea) las salidas de L; los análogos de M, B, E tienen sus
propias specs (M ya vive en el motor de decisión; B y E en
`corredor-B-tasa-base.py` y `corredor-E-combinacion-LM.py` de este mismo
directorio) -- el compromiso conjunto de los cuatro (T2 de este acto) se
hace vía `commit_hash_registry()` al final de este archivo, que cualquier
corredor puede invocar antes de que R exista.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

# --------------------------------------------------------------------------
# 1 · Parámetros del corredor, explícitos (M2: "modelo+versión+fecha+
#     temperatura fijados", "es parte del experimento, no una preferencia"
#     -- TRANSFER §5).
# --------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class ParametrosCorredorL:
    """Fijados ANTES de correr una sola celda. Nunca se eligen post-hoc."""

    modelo_id: str          # p.ej. "claude-opus-4-...-20260815" -- mesa lo fija
    version_declarada: str  # cadena de versión textual del proveedor, verbatim
    fecha_congelacion: str  # ISO 8601, fecha en que estos parámetros se sellan
    temperatura: float      # 0.0-2.0 según el proveedor; mesa lo fija
    k_corridas: int         # 5 <= k <= 10, ADV1-M2 exige el rango
    variante: Literal["L-solo", "L+corpus"]
    corpus_id_si_aplica: str | None = None  # hash/ruta del corpus tierizado
    ejecutor: str = "sesión limpia fuera del proyecto (D-iii)"

    def __post_init__(self) -> None:
        if not (5 <= self.k_corridas <= 10):
            raise ValueError("ADV1-M2 exige k=5-10 corridas, sin excepción.")
        if self.variante == "L+corpus" and not self.corpus_id_si_aplica:
            raise ValueError("L+corpus exige declarar el corpus_id_si_aplica.")
        if self.variante == "L-solo" and self.corpus_id_si_aplica:
            raise ValueError("L-solo no debe traer corpus adjunto -- rompería el ciego.")


# --------------------------------------------------------------------------
# 2 · La spec de una celda -- se lee de marco-candidatas-piloto-v1_0.tsv
#     (ACT-PIL-2, no se reconstruye aquí). El pipeline NO enumera candidatas.
# --------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class SpecCelda:
    id: str
    encuesta: str
    ola: str
    universo: str
    variable: str
    estimador: str
    escala: str  # binaria | ordinal k=N | continua (unidad)
    frase_discriminacion: str


def cargar_specs_desde_marco(ruta_tsv: Path) -> list[SpecCelda]:
    """Lee `forense/marco-candidatas-piloto-v1_0.tsv` -- NUNCA se edita ese
    archivo desde este script; solo se lee. El sorteo con semilla pública
    (D-iii, ACT-PIL-3) decide qué subconjunto de filas corre el piloto;
    este pipeline recibe la lista ya sorteada como parámetro externo, no la
    deriva por su cuenta."""
    import csv

    with ruta_tsv.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        return [
            SpecCelda(
                id=row["id"],
                encuesta=row["encuesta"],
                ola=row["ola"],
                universo=row["universo"],
                variable=row["variable"],
                estimador=row["estimador"],
                escala=row["escala"],
                frase_discriminacion=row["frase_discriminacion"],
            )
            for row in reader
        ]


# --------------------------------------------------------------------------
# 3 · El prompt -- construido mecánicamente desde la spec, nunca a mano por
#     celda (eso reintroduciría el "redactor de L conoce el motor",
#     CAREO §A, 5/5 corridas). Plantilla única, parametrizada.
# --------------------------------------------------------------------------


PLANTILLA_L_SOLO = """\
Estás respondiendo como estimador de una cantidad encuestable en México.
No tienes acceso a ningún documento adjunto de este proyecto de investigación.
Encuesta: {encuesta} (ola {ola}).
Universo: {universo}.
Variable/reactivo: {variable} ({estimador}).
Escala de respuesta: {escala}.
Da tu mejor estimación puntual y, si la escala es continua, un intervalo de
confianza subjetivo. Si no conoces el dato, dilo explícitamente -- no
inventes una cifra plausible. Cita la fuente de tu estimación si la tienes
(sonda canario: fuente textual declarada, ver M1)."""

PLANTILLA_L_CORPUS = PLANTILLA_L_SOLO + """

Contexto adicional (corpus tierizado, {corpus_id}): {contexto_corpus}"""


def construir_prompt(spec: SpecCelda, params: ParametrosCorredorL, contexto_corpus: str = "") -> str:
    if params.variante == "L-solo":
        return PLANTILLA_L_SOLO.format(
            encuesta=spec.encuesta, ola=spec.ola, universo=spec.universo,
            variable=spec.variable, estimador=spec.estimador, escala=spec.escala,
        )
    return PLANTILLA_L_CORPUS.format(
        encuesta=spec.encuesta, ola=spec.ola, universo=spec.universo,
        variable=spec.variable, estimador=spec.estimador, escala=spec.escala,
        corpus_id=params.corpus_id_si_aplica, contexto_corpus=contexto_corpus,
    )


# --------------------------------------------------------------------------
# 4 · Ejecución de las k corridas -- interfaz abstracta. La implementación
#     concreta (llamada real al proveedor del modelo) NO vive aquí: este
#     acto es NUBE repo-only y prohíbe correr el script. `llamar_modelo` es
#     el único punto que una sesión ejecutora real debe rellenar.
# --------------------------------------------------------------------------


@dataclasses.dataclass
class RespuestaCorrida:
    indice: int              # 1..k, orden de ejecución real
    texto_crudo: str         # salida completa del modelo, sin editar
    valor_extraido: float | str | None  # parseo del punto/categoría
    fuente_citada: str | None           # sonda canario
    timestamp: str


def llamar_modelo(prompt: str, params: ParametrosCorredorL) -> str:
    """PENDIENTE DE IMPLEMENTACIÓN REAL por la sesión ejecutora (fuera de
    este acto, fuera de esta caja). Debe: (1) fijar modelo_id/version/
    temperatura exactamente como en `params`, (2) no reintentar en caso de
    rechazo salvo error de transporte (un rechazo de contenido es una
    corrida válida, se registra, no se descarta -- M2: "TODAS las corridas
    registradas sin descarte"), (3) devolver el texto crudo sin post-proceso."""
    raise NotImplementedError(
        "Este script es spec de pre-registro. No se ejecuta en el acto "
        "DUELO-PREREG-V2 (NUBE, repo-only). La sesión ejecutora real "
        "implementa esta función."
    )


def correr_celda(spec: SpecCelda, params: ParametrosCorredorL, contexto_corpus: str = "") -> list[RespuestaCorrida]:
    """k=5-10 corridas, TODAS registradas, CERO descarte -- incluidas
    negativas, ambiguas, o de rechazo. La dispersión entre corridas es un
    resultado, no un problema a limpiar."""
    prompt = construir_prompt(spec, params, contexto_corpus)
    corridas: list[RespuestaCorrida] = []
    for i in range(1, params.k_corridas + 1):
        texto = llamar_modelo(prompt, params)  # nunca se llama en este acto
        corridas.append(
            RespuestaCorrida(
                indice=i,
                texto_crudo=texto,
                valor_extraido=None,  # el parseo real lo hace la sesión ejecutora
                fuente_citada=None,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
        )
    return corridas


# --------------------------------------------------------------------------
# 5 · Agregado pre-registrado -- mediana+cuantiles para continuas,
#     self-consistency (moda) para categóricas. Dispersión SIEMPRE reportada.
# --------------------------------------------------------------------------


def agregar_continua(valores: list[float]) -> dict:
    if not valores:
        return {"mediana": None, "q10": None, "q90": None, "dispersion_iqr": None, "n": 0}
    ordenados = sorted(valores)
    n = len(ordenados)
    mediana = statistics.median(ordenados)
    q10 = ordenados[max(0, int(0.10 * (n - 1)))]
    q90 = ordenados[min(n - 1, int(0.90 * (n - 1)))]
    q25 = ordenados[max(0, int(0.25 * (n - 1)))]
    q75 = ordenados[min(n - 1, int(0.75 * (n - 1)))]
    return {
        "mediana": mediana, "q10": q10, "q90": q90,
        "dispersion_iqr": q75 - q25, "n": n,
    }


def agregar_categorica(valores: list[str]) -> dict:
    if not valores:
        return {"moda": None, "self_consistency": None, "distribucion": {}, "n": 0}
    conteo: dict[str, int] = {}
    for v in valores:
        conteo[v] = conteo.get(v, 0) + 1
    moda = max(conteo, key=conteo.get)
    return {
        "moda": moda,
        "self_consistency": conteo[moda] / len(valores),  # fracción de corridas que coincide
        "distribucion": conteo,
        "n": len(valores),
    }


# --------------------------------------------------------------------------
# 6 · Compromiso por hash de los cuatro corredores ANTES de que R exista.
#     ADV1-M2, última frase: "Hashes de los cuatro corredores comprometidos
#     antes de que R exista." L/M/B/E, ver corredor-B-tasa-base.py y
#     corredor-E-combinacion-LM.py.
# --------------------------------------------------------------------------


def hash_salida(payload: dict) -> str:
    """sha256 determinista de la salida serializada -- json con claves
    ordenadas, sin espacios extra, para que el hash sea reproducible."""
    serial = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(serial.encode("utf-8")).hexdigest()


def commit_hash_registry(
    salidas_L: dict, salidas_M: dict, salidas_B: dict, salidas_E: dict,
    ruta_salida: Path,
) -> dict:
    """Escribe el registro de compromiso de los cuatro corredores, con
    timestamp y hash individual + hash conjunto. Este registro debe existir
    y estar comiteado ANTES de que el árbitro R corra sobre microdato --
    es la garantía de que ningún corredor se ajustó después de ver R."""
    registro = {
        "timestamp_compromiso": datetime.now(timezone.utc).isoformat(),
        "corredores": {
            "L": {"hash": hash_salida(salidas_L)},
            "M": {"hash": hash_salida(salidas_M)},
            "B": {"hash": hash_salida(salidas_B)},
            "E": {"hash": hash_salida(salidas_E)},
        },
    }
    registro["hash_conjunto"] = hash_salida(registro["corredores"])
    ruta_salida.write_text(json.dumps(registro, indent=2, ensure_ascii=False), encoding="utf-8")
    return registro


# --------------------------------------------------------------------------
# NOTA DE CIERRE: este archivo es spec + andamiaje, no un binario ejecutable
# en este acto. `llamar_modelo` deliberadamente lanza NotImplementedError.
# Quien lo active debe hacerlo en una sesión limpia fuera de este proyecto
# (D-iii) y solo después del sorteo con semilla pública (ACT-PIL-3, aún no
# lanzado al momento de escribir esto).
# --------------------------------------------------------------------------

if __name__ == "__main__":
    raise SystemExit(
        "pipeline-L-adv1-m2.py es pre-registro ejecutable, no un script para "
        "correr aquí. Ver docstring del módulo -- DUELO-PREREG-V2 prohíbe "
        "ejecutarlo en este acto."
    )
