"""Adjudicación (COMMIT-3) del duelo prospectivo ENIGH 2024 -- nivel nacional
único, sin ejes ni cruces (`DISENO-duelo-prospectivo-ENIGH2024-v1_0.md §3`).

ACTO `GEN2-ENIGH2024-DUELO-COMMIT-2-3`. `#988` (ACTO GEN2-ENIGH2024-SERIE-Y-
COMMIT-1) dejó EMISIONES y ORIGEN-MOVIL sellados pero no construyó esta pieza
(el `[SUPUESTO]` del encargo aplicó). Congelada aquí, ANTES de que
`corrida0 run CALC-ENIGH-DUELO-EMISIONES-0001` abra el zip de 2024 (COMMIT-2
corre después, en este mismo acto, en un commit posterior) -- este medidor no
ha visto ningún dato de 2024 al escribirse.

Regla de adjudicación (DISEÑO §5, verbatim): un retador VENCE AL PISO si
(a) su |error| sobre 2024 es menor que el de C-PISO, Y (b) su MAE de la
validación de origen móvil (RETROSPECTIVA-MECÁNICA, ya sellada en
`CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001`) también lo es. Vence sólo en (a):
`PROPUESTA-CON-RESERVA`. Ninguno vence las dos: `C-PISO` se adopta.

Operacionalización propia de este CALC, no escrita letra por letra en el
DISEÑO y declarada aquí porque D-24/E.6 exigen congelarla antes de abrir
dato (B-bis-2, «¿tiene tendencia legible?»): se aplica la MISMA regla de dos
condiciones de §5, sustituyendo C-PISO por C-MEDIA como referencia --
¿algún C-T2/C-T3/C-TS vence a C-MEDIA en (a) el punto de 2024 y (b) el MAE
retrospectivo? Si sí, la tendencia lineal supera al nulo "sin tendencia" y
B-bis-2 se lee REFUTADA (tendencia legible); si no, ACOTADA (no se
distingue tendencia de ruido con cuatro puntos). Es la lectura natural de
"C-MEDIA no es vencida por C-T2/C-T3/C-TS" del DISEÑO, con el mismo par de
condiciones que ya rige la comparación con el piso -- no se inventa un
umbral nuevo.

Nivel cruce y marginal: `NO-CONSTRUIBLE` fijo (DISEÑO §3/§4.3) -- nadie
corrió el mecanismo contra esta fuente, no hay veredicto que calcular.

Interfaz estable: medir(inputs, contrato) -> {"RESULT-...": valor}.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys

CONTENDIENTES = ("C-PISO", "C-T2", "C-T3", "C-TS", "C-MEDIA")
RETADORES = ("C-T2", "C-T3", "C-TS", "C-MEDIA")
RETADORES_DE_TENDENCIA = ("C-T2", "C-T3", "C-TS")


def _carga_modulo(nombre, ruta_absoluta):
    spec = importlib.util.spec_from_file_location(nombre, ruta_absoluta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _clave(cid: str) -> str:
    return cid.replace("-", "")


def _texto_bool(v) -> str:
    if v is None:
        return "NO-ESTIMABLE"
    return "SI" if v else "NO"


def medir(inputs, contrato):
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    # se carga sólo por el catálogo CONTENDIENTES/orden -- ya validado y
    # ejecutado en EMISIONES y ORIGEN-MOVIL; este medidor no vuelve a
    # predecir nada, sólo compone lo ya sellado.
    nacional_mod = _carga_modulo("enigh_duelo_nacional", os.path.join(raiz, "tools", "enigh_duelo_nacional.py"))
    assert tuple(nacional_mod.CONTENDIENTES) == CONTENDIENTES

    emisiones = json.loads(inputs["emisiones_selladas"]["bytes"].decode("utf-8"))["resultados"]
    origen_movil = json.loads(inputs["origen_movil_sellado"]["bytes"].decode("utf-8"))["resultados"]

    r_p = emisiones["RESULT-ENIGHEM-R-P"]
    r_estado = emisiones["RESULT-ENIGHEM-R-ESTADO"]
    r_ic_json = emisiones["RESULT-ENIGHEM-R-IC95-JSON"]
    r_ic = json.loads(r_ic_json) if r_ic_json else None
    predicciones = json.loads(emisiones["RESULT-ENIGHEM-PREDICCIONES-JSON"])
    r_valido = (r_estado == "REPORTADO") and (r_p is not None)

    salida: dict = {}
    abs_error: dict[str, float | None] = {}
    mae_retro: dict[str, float | None] = {}

    for cid in CONTENDIENTES:
        clave = _clave(cid)
        pr = predicciones[cid]
        p = pr["p"]
        ic = pr["ic95"]

        if p is None or not r_valido:
            err = abserr = None
            r_en_ic = cand_en_ic = None
        else:
            err = 100.0 * (p - r_p)
            abserr = abs(err)
            r_en_ic = None if ic is None else bool(ic[0] <= r_p <= ic[1])
            cand_en_ic = None if r_ic is None else bool(r_ic[0] <= p <= r_ic[1])
        abs_error[cid] = abserr

        mae = origen_movil.get(f"RESULT-ENIGHDM-{clave}-MAE-PP")
        cob = origen_movil.get(f"RESULT-ENIGHDM-{clave}-COBERTURA-R-EN-IC-CAND")
        mae_retro[cid] = mae

        salida[f"RESULT-ENIGHADJ-{clave}-P"] = p
        salida[f"RESULT-ENIGHADJ-{clave}-ERROR-PP"] = err
        salida[f"RESULT-ENIGHADJ-{clave}-ABS-ERROR-PP"] = abserr
        salida[f"RESULT-ENIGHADJ-{clave}-R-DENTRO-IC-CAND"] = _texto_bool(r_en_ic)
        salida[f"RESULT-ENIGHADJ-{clave}-CAND-DENTRO-IC-R"] = _texto_bool(cand_en_ic)
        salida[f"RESULT-ENIGHADJ-{clave}-MAE-RETROSPECTIVO-PP"] = mae
        salida[f"RESULT-ENIGHADJ-{clave}-COBERTURA-RETROSPECTIVA-FRAC"] = cob

    # -- veredicto por retador vs C-PISO (DISEÑO §5) --------------------
    piso_abs, piso_mae = abs_error["C-PISO"], mae_retro["C-PISO"]
    ganadores_vence = []
    for cid in RETADORES:
        clave = _clave(cid)
        completo = None not in (abs_error[cid], piso_abs, mae_retro[cid], piso_mae)
        if not completo:
            cond_a = cond_b = None
            veredicto = "NO-ESTIMABLE"
        else:
            cond_a = abs_error[cid] < piso_abs
            cond_b = mae_retro[cid] < piso_mae
            if cond_a and cond_b:
                veredicto = "VENCE-AL-PISO"
                ganadores_vence.append(cid)
            elif cond_a and not cond_b:
                veredicto = "PROPUESTA-CON-RESERVA"
            else:
                veredicto = "NO-VENCE"
        salida[f"RESULT-ENIGHADJ-{clave}-CONDICION-A-2024"] = _texto_bool(cond_a)
        salida[f"RESULT-ENIGHADJ-{clave}-CONDICION-B-RETROSPECTIVA"] = _texto_bool(cond_b)
        salida[f"RESULT-ENIGHADJ-{clave}-VEREDICTO"] = veredicto

    veredicto_general = ("VENCE-AL-PISO:" + ",".join(sorted(ganadores_vence))
                         if ganadores_vence else "C-PISO-ADOPTADO")
    salida["RESULT-ENIGHADJ-VEREDICTO-GENERAL-NACIONAL"] = veredicto_general

    # -- ganador retrospectivo / ganador 2024, entre los cinco ----------
    validos_retro = {c: v for c, v in mae_retro.items() if v is not None}
    validos_2024 = {c: v for c, v in abs_error.items() if v is not None}
    ganador_retro = min(validos_retro, key=validos_retro.get) if validos_retro else None
    ganador_2024 = min(validos_2024, key=validos_2024.get) if validos_2024 else None
    salida["RESULT-ENIGHADJ-GANADOR-RETROSPECTIVO"] = ganador_retro or "NO-ESTIMABLE"
    salida["RESULT-ENIGHADJ-GANADOR-2024"] = ganador_2024 or "NO-ESTIMABLE"

    # -- B-bis-1: el piso es difícil de vencer ---------------------------
    salida["RESULT-ENIGHADJ-BBIS1-DICTAMEN"] = "CORROBORADA" if not ganadores_vence else "REFUTADA"

    # -- B-bis-2: tendencia legible? (T2/T3/TS vencen a C-MEDIA, misma
    #    regla de dos condiciones -- ver docstring) --------------------
    media_abs, media_mae = abs_error["C-MEDIA"], mae_retro["C-MEDIA"]
    vence_a_media = []
    for cid in RETADORES_DE_TENDENCIA:
        if None in (abs_error[cid], media_abs, mae_retro[cid], media_mae):
            continue
        if abs_error[cid] < media_abs and mae_retro[cid] < media_mae:
            vence_a_media.append(cid)
    salida["RESULT-ENIGHADJ-BBIS2-DICTAMEN"] = (
        "REFUTADA-TENDENCIA-LEGIBLE:" + ",".join(sorted(vence_a_media))
        if vence_a_media else "ACOTADA")

    # -- B-bis-3/4: ¿el ganador retrospectivo es también el de 2024? ----
    if ganador_retro is not None and ganador_2024 is not None:
        bbis34 = "CORROBORADA" if ganador_retro == ganador_2024 else "FALSADOR-DEBIL"
    else:
        bbis34 = "NO-ESTIMABLE"
    salida["RESULT-ENIGHADJ-BBIS3-4-DICTAMEN"] = bbis34

    salida["RESULT-ENIGHADJ-PRIORIDAD-BBIS-NOTA"] = (
        "BBIS1-MANDA-SOBRE-BBIS3-SI-AMBAS-SE-SATISFACEN-A-LA-VEZ (DISENO Sec6, verbatim)")
    salida["RESULT-ENIGHADJ-NIVEL-CRUCE-MARGINAL"] = "NO-CONSTRUIBLE"
    return salida
