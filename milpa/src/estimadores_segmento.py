# -*- coding: utf-8 -*-
"""Lector de `milpa/estimadores-por-segmento.yaml` (DERIVADO por
`tools/marcador_segmento.py`).

ACTO GEN2-MARCADOR-REDISENO-1 (adenda de dirección, 19/sep/2026), P2.

Este módulo NO calibra, NO adopta y NO escribe nada: consulta un YAML ya
derivado y devuelve la emisión exacta que trae, o `None` si la celda pedida
no está ahí. La adopción por celda ocurre en `tools/marcador_segmento.py`
(qué entra al YAML) y en `decisiones.tsv` (objeto
`adopcion:piso-C2-20-celdas`, firma de mesa) -- este módulo es solo la
ranura de consulta que `milpa/src/motor.py::estimar_segmento` expone.
"""
from __future__ import annotations

from pathlib import Path

import yaml

RUTA_ESTIMADORES = (Path(__file__).resolve().parents[2]
                     / "milpa" / "estimadores-por-segmento.yaml")


ADOPTADO_ACTIVO = "ADOPTADO-POR-FIRMA"
EMITIDA_SIN_EVALUAR = "EMITIDA-SIN-EVALUAR"


# Caché por (ruta, mtime_ns, tamaño). El YAML pasó de 20 a 226 entradas al
# incorporar las emisiones, y `estimador_de_celda` se llama una vez por
# celda: sin caché, consultar la rejilla entera reparsea el archivo cientos
# de veces. La llave incluye mtime y tamaño, no sólo la ruta, para que una
# re-derivación del YAML invalide la entrada -- un caché que devuelve el
# archivo de antes sería peor que no tenerlo.
_CACHE: dict[tuple, dict] = {}


def _crudo(ruta: Path | None = None) -> dict:
    ruta = ruta or RUTA_ESTIMADORES
    try:
        st = ruta.stat()
    except OSError:
        return {}
    llave = (str(ruta), st.st_mtime_ns, st.st_size)
    if llave not in _CACHE:
        _CACHE.clear()          # una sola versión viva; no crece sin límite
        _CACHE[llave] = yaml.safe_load(ruta.read_text(encoding="utf-8")) or {}
    return _CACHE[llave]


def _carga(ruta: Path | None = None) -> dict:
    """SOLO las adoptadas. Es la vía por defecto y no cambia."""
    return _crudo(ruta).get("celdas") or {}


def _carga_emitidas(ruta: Path | None = None) -> dict:
    """Las `EMITIDA-SIN-EVALUAR`, que viven en clave SEPARADA del YAML
    (`emitidas_sin_evaluar`) y con espacio de nombres de id propio
    (`CRUCE-EMITIDA::…`). Nunca se mezclan con `celdas`."""
    return _crudo(ruta).get("emitidas_sin_evaluar") or {}


def estimador_de_celda(celda_id: str, *, ruta: Path | None = None,
                        incluir_no_evaluadas: bool = False) -> dict | None:
    """Devuelve `{punto, ic95_inf, ic95_sup, unidad_dato, tipo_incertidumbre,
    resultado_id, regla_origen, estado}` para `celda_id`, o `None`.

    **Por defecto devuelve SOLO celdas adoptadas.** `celda_id` es el mismo id
    que trae `marcador-segmento.tsv` en su columna `celda_id` (p. ej.
    `CRUCE::DIN...::L1xE1`).

    `incluir_no_evaluadas=True` es la ÚNICA vía por la que sale una celda
    `EMITIDA-SIN-EVALUAR` (`ACTO GEN2-C2-COMPUESTO-RESERVADAS-1`, firma de
    mesa 19/sep/2026). El argumento es explícito y sin valor por defecto
    permisivo a propósito: la firma dice que esas emisiones están
    «excluidas de la estimación adoptada del motor y de toda decisión
    automática», y una decisión automática es exactamente la que toma un
    llamador que no sabe que las está pidiendo.

    La respuesta **siempre** trae `estado`, en los dos casos, para que
    ningún consumidor pueda usar una emisión creyéndola adoptada: las
    adoptadas salen con `ADOPTADO-POR-FIRMA` y las emitidas con
    `EMITIDA-SIN-EVALUAR`. Una emisión **no pasa a adoptada por uso**.
    """
    entrada = _carga(ruta).get(celda_id)
    if entrada is not None:
        salida = dict(entrada)
        salida.setdefault("estado", ADOPTADO_ACTIVO)
        return salida
    if not incluir_no_evaluadas:
        return None
    entrada = _carga_emitidas(ruta).get(celda_id)
    if entrada is None:
        return None
    salida = dict(entrada)
    # No se hereda del YAML: se fija aquí, para que un YAML mal derivado no
    # pueda hacer pasar una emisión por adoptada.
    salida["estado"] = EMITIDA_SIN_EVALUAR
    return salida


def celdas_emitidas_sin_evaluar(*, ruta: Path | None = None) -> dict:
    """Listado explícito de las emisiones, para exploración. No es una vía
    de consumo del motor: cada entrada trae `estado = EMITIDA-SIN-EVALUAR`.

    `ACTO GEN2-MARCADOR-ENLACE-2` (20/sep/2026, P3): desde `#911`/`#916`,
    una emisión PUEDE traer `ic95_inf`/`ic95_sup` -- los que el CALC de IC
    de su ola selló réplica por réplica, con `tipo_incertidumbre =
    IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS` y
    `ic95_fuente` con el nombre del CALC. Las que ningún CALC cubre siguen
    con los dos campos vacíos y `NO-PROPAGADA-COVARIANZA-NO-SELLADA`.

    **Traer IC no las vuelve adoptadas.** Ese IC mide el ruido muestral de
    un estimador que SUPONE no-interacción; no mide el error de ese
    supuesto, que es justamente lo que falta evaluar. El estado sigue
    `EMITIDA-SIN-EVALUAR` y la vía por defecto del lector sigue sin
    devolverlas."""
    return {k: dict(v, estado=EMITIDA_SIN_EVALUAR)
            for k, v in _carga_emitidas(ruta).items()}


__all__ = ["estimador_de_celda", "celdas_emitidas_sin_evaluar",
           "RUTA_ESTIMADORES", "ADOPTADO_ACTIVO", "EMITIDA_SIN_EVALUAR"]
