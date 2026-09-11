#!/usr/bin/env python3
"""Cara corrida0 del reanálisis F5: consume sólo el snapshot resuelto."""
from __future__ import annotations

import json
import sys
import types


def _modulo_desde_input(nombre: str, entrada: dict) -> types.ModuleType:
    crudo = entrada.get("bytes")
    if not isinstance(crudo, bytes):
        raise RuntimeError(f"{entrada.get('id')}: bytes no resueltos")
    ruta = str(entrada.get("ruta") or entrada.get("id"))
    modulo = types.ModuleType(nombre)
    modulo.__file__ = ruta
    sys.modules[nombre] = modulo
    exec(compile(crudo.decode("utf-8"), ruta, "exec"), modulo.__dict__)
    return modulo


def _linaje_comun(modulo):
    """Adapta la única decisión común; no vuelve a resolver procedencia.

    El snapshot sucesor de 18 debe traer el origen/camino que 17 trazó. Este
    medidor sólo pregunta a ``aptitud_para_uso`` si ese origen sirve para una
    evaluación retenida. El snapshot histórico no trae esos campos y por eso
    cae, correctamente, en INDETERMINADO.
    """
    aptitud_para_uso = getattr(modulo, "aptitud_para_uso", None)
    if not callable(aptitud_para_uso):
        raise RuntimeError(
            "el módulo común de 17 no expone aptitud_para_uso")
    requerida = {
        "APTA_LINAJE", "ORIGEN_INDETERMINADO",
        "USO_CONFIRMACION_INDEPENDIENTE",
    }
    faltan = sorted(nombre for nombre in requerida if not hasattr(modulo, nombre))
    if faltan:
        raise RuntimeError(f"interfaz común de 17 incompleta: {faltan}")

    def clasificar(**contexto):
        celda = contexto["celda_m"]
        origen = celda.get("origen_numerico", modulo.ORIGEN_INDETERMINADO)
        dependencia = celda.get("dependencia_objetivo", "INDETERMINADA")
        camino = celda.get("camino_linaje") or []
        if isinstance(camino, str):
            camino = [camino]
        aptitud, motivo = aptitud_para_uso(
            origen, modulo.USO_CONFIRMACION_INDEPENDIENTE,
            validacion_independiente=celda.get(
                "validacion_independiente", "NO-HECHA"),
            rol_evaluacion=celda.get("rol_evaluacion", ""),
        )
        if origen == modulo.ORIGEN_INDETERMINADO or dependencia == "INDETERMINADA":
            estado = "INDETERMINADO"
        elif aptitud == modulo.APTA_LINAJE and dependencia == "NO":
            estado = "APTO"
        else:
            estado = "NO-APTO"
        return {
            "estado": estado, "origen_numerico": origen,
            "dependencia_objetivo": dependencia, "camino": camino,
            "razon": motivo,
        }

    return clasificar


def _comp(resultado: dict, clave: str) -> dict:
    return resultado["comparaciones_diagnosticas"].get(clave, {})


def medir(inputs: dict, contrato: dict) -> dict:
    calculador = _modulo_desde_input(
        "calcula_f5_sin_fugas_resuelto",
        next(e for e in inputs.values() if e.get("rol") == "calculador"),
    )
    linaje = _modulo_desde_input(
        "linaje_gen2_resuelto_f5",
        next(e for e in inputs.values() if e.get("rol") == "linaje"),
    )
    resultado, filas = calculador.calcular(
        inputs, contrato, _linaje_comun(linaje))
    estados = resultado["estados_captura"]
    cobertura = resultado["cobertura"]
    mae = resultado["mae_pp_diagnostico"]

    salida = {
        "RESULT-F5SF-POSICIONES": len(filas),
        "RESULT-F5SF-VALIDAS": estados.get("VALIDA", 0),
        "RESULT-F5SF-ABSTENCIONES": estados.get("ABSTENCION", 0),
        "RESULT-F5SF-MALFORMADAS": estados.get("MALFORMADA", 0),
        "RESULT-F5SF-ERRORES-TECNICOS": estados.get("ERROR_TECNICO", 0),
        "RESULT-F5SF-ERRORES-IDENTIDAD": estados.get("ERROR_IDENTIDAD", 0),
        "RESULT-F5SF-MARCO-N": resultado["marco_n"],
        "RESULT-F5SF-U3-N": resultado["u3_n"],
        "RESULT-F5SF-U3-IDS": ",".join(resultado["u3_puntuable"]),
        "RESULT-F5SF-COMPARACION-COMPROMETIDA": (
            "SI" if resultado["comparacion_congelada_comprometida"] else "NO"),
        "RESULT-F5SF-COBERTURA-L-SOLO": cobertura["L_SOLO_con_punto"],
        "RESULT-F5SF-COBERTURA-L-CORPUS": cobertura["L_CORPUS_con_punto"],
        "RESULT-F5SF-COBERTURA-M-PUNTO": cobertura["M_con_punto"],
        "RESULT-F5SF-COBERTURA-M-ELEGIBLE": cobertura["M_elegible"],
        "RESULT-F5SF-COBERTURA-R": cobertura["R_con_punto"],
        "RESULT-F5SF-MAE-L-SOLO-PP": mae["L_SOLO"],
        "RESULT-F5SF-MAE-L-CORPUS-PP": mae["L_CORPUS"],
        "RESULT-F5SF-MAE-M-PP": mae["M"],
        "RESULT-F5SF-VEREDICTO-GLOBAL": resultado["veredicto_global"],
        "RESULT-F5SF-DETALLE-CELDAS-JSON": json.dumps(
            resultado["celdas"], ensure_ascii=False, sort_keys=True,
            separators=(",", ":")),
    }
    nombres = {
        "L_CORPUS_vs_L_SOLO": "LCORPUS-LSOLO",
        "M_vs_L_SOLO": "M-LSOLO",
        "M_vs_L_CORPUS": "M-LCORPUS",
    }
    for clave, corto in nombres.items():
        comparacion = _comp(resultado, clave)
        prefijo = f"RESULT-F5SF-DELTA-{corto}"
        salida[f"{prefijo}-PUNTO-PP"] = comparacion.get("delta_mae_pp")
        salida[f"{prefijo}-IC95-LO-PP"] = comparacion.get("ic_lo")
        salida[f"{prefijo}-IC95-HI-PP"] = comparacion.get("ic_hi")
        salida[f"{prefijo}-VEREDICTO"] = comparacion.get(
            "veredicto", "NO-ESTIMABLE")
    return salida
