"""Contrato mínimo de aptitud numérica para consumidores GEN2.

Este módulo no resuelve rutas ni decide semántica científica. Recibe el origen
numérico ya trazado por ``tools/corrida0.py`` y responde si ese origen puede
usarse bajo el rol declarado. Es deliberadamente pequeño para que el registro,
T35 y el emisor puedan compartir la misma decisión sin importar entre sí.
"""
from __future__ import annotations


ORIGEN_NUEVO = "NUEVO"
ORIGEN_HEREDADO = "HEREDADO"
ORIGEN_MIXTO = "MIXTO"
ORIGEN_INDETERMINADO = "INDETERMINADO"
ORIGENES = {
    ORIGEN_NUEVO, ORIGEN_HEREDADO, ORIGEN_MIXTO, ORIGEN_INDETERMINADO,
}

USO_MEDICION_GEN2 = "MEDICION-GEN2"
USO_CONFIRMACION_INDEPENDIENTE = "CONFIRMACION-INDEPENDIENTE"
USOS_CON_HERENCIA = {"HISTORICO", "BASELINE", "DESCRIPTIVO", "CALIBRACION"}

APTA_LINAJE = "APTA-POR-LINAJE"
APTA_CON_HERENCIA = "APTA-CON-HERENCIA-DECLARADA"
NO_APTA = "NO-APTA"
NO_EVALUADA = "NO-EVALUADA"


def combina_origenes(origenes: list[str]) -> str:
    """Combina sólo procedencia numérica; código/metadato no llegan aquí."""
    valores = {o for o in origenes if o in ORIGENES}
    if not valores:
        return ORIGEN_NUEVO
    if ORIGEN_INDETERMINADO in valores:
        return ORIGEN_INDETERMINADO
    if ORIGEN_MIXTO in valores or valores == {ORIGEN_NUEVO, ORIGEN_HEREDADO}:
        return ORIGEN_MIXTO
    return next(iter(valores))


def aptitud_para_uso(origen_numerico: str, uso_solicitado: str,
                     validacion_independiente: str = "NO-HECHA",
                     rol_evaluacion: str = "") -> tuple[str, str]:
    """Devuelve ``(aptitud, motivo)`` sin usar generación ni contador.

    ``APTA-POR-LINAJE`` significa exactamente eso: no certifica que variable,
    unidad, población o transformación sean adecuadas para el parámetro. Esa
    compatibilidad científica sigue siendo humana.
    """
    origen = str(origen_numerico or ORIGEN_INDETERMINADO).upper()
    uso = str(uso_solicitado or "").upper()
    validacion = str(validacion_independiente or "NO-HECHA").upper()
    rol = str(rol_evaluacion or "").upper()

    if uso in ("", "LEGACY-NO-DECLARADO"):
        return NO_EVALUADA, "el consumidor legacy no declara un uso GEN2"
    if origen not in ORIGENES:
        return NO_APTA, f"origen numérico desconocido: {origen or '<vacío>'}"
    if origen == ORIGEN_INDETERMINADO:
        return NO_APTA, "el origen numérico no está acreditado"

    if uso == USO_MEDICION_GEN2:
        if origen == ORIGEN_NUEVO:
            return APTA_LINAJE, ("origen NUEVO; no certifica compatibilidad "
                                 "semántica del estimando con el parámetro")
        return NO_APTA, (f"una medición GEN2 no adopta origen {origen}; "
                         "cuenta_gen2 y el sello no cambian la procedencia")

    if uso in USOS_CON_HERENCIA:
        if origen == ORIGEN_NUEVO:
            return APTA_LINAJE, "origen NUEVO para uso explícitamente declarado"
        return APTA_CON_HERENCIA, (f"uso {uso} permite origen {origen} sin "
                                   "borrar su herencia")

    if uso == USO_CONFIRMACION_INDEPENDIENTE:
        if origen != ORIGEN_NUEVO:
            return NO_APTA, f"confirmación independiente exige origen NUEVO; recibió {origen}"
        if validacion != "PASA" or rol not in {"HOLDOUT", "EVALUACION-RETENIDA"}:
            return NO_APTA, ("confirmación independiente requiere validación PASA "
                             "y rol HOLDOUT/EVALUACION-RETENIDA; contrato pendiente de 19")
        return APTA_LINAJE, "origen NUEVO y rol de evaluación retenida acreditado"

    return NO_APTA, f"uso solicitado no reconocido: {uso}"
