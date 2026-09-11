#!/usr/bin/env python3
"""Calculador sucesor de F5 con inputs cerrados y elegibilidad por celda.

El núcleo no abre archivos. Recibe exactamente el snapshot de inputs que
``tools/corrida0.py`` resolvió una vez, más el contrato ejecutable de la spec.
La procedencia numérica se obtiene mediante el callable del resolver común de
``ACTO GEN2-LINAJE-Y-ADOPCION``; este módulo no mantiene otra clasificación.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import random
import re
import statistics
from collections import Counter
from typing import Callable


class ContratoInvalido(RuntimeError):
    """La estructura no permite identificar una comparación inequívoca."""


ClasificadorLinaje = Callable[..., dict]


def _exige(condicion: bool, mensaje: str) -> None:
    if not condicion:
        raise ContratoInvalido(mensaje)


def _texto(entrada: dict) -> str:
    crudo = entrada.get("bytes")
    _exige(isinstance(crudo, bytes), f"input_sin_bytes={entrada.get('id')}")
    return crudo.decode("utf-8")


def _verifica_inputs(inputs: dict[str, dict]) -> None:
    _exige(isinstance(inputs, dict) and inputs, "inputs_vacios_o_no_mapa")
    for iid, entrada in inputs.items():
        _exige(iid == entrada.get("id"), f"input_id_discorda={iid}")
        _exige(entrada.get("estado") == "COINCIDE", f"input_no_coincide={iid}")
        crudo = entrada.get("bytes")
        _exige(isinstance(crudo, bytes), f"input_repo_sin_bytes={iid}")
        real = hashlib.sha256(crudo).hexdigest()
        _exige(real == entrada.get("sha256"), f"input_sha_discorda={iid}")
        _exige(entrada.get("rol") in {
            "contrato_estudio", "plan", "snapshot_m", "universo_r",
            "tarjetas_mr", "calculador", "linaje", "captura_l",
            "resultado_r",
        }, f"input_rol_desconocido={iid}:{entrada.get('rol')}")


def _por_rol(inputs: dict[str, dict], rol: str) -> list[dict]:
    return [entrada for entrada in inputs.values() if entrada.get("rol") == rol]


def _unico(inputs: dict[str, dict], rol: str) -> dict:
    encontrados = _por_rol(inputs, rol)
    _exige(len(encontrados) == 1,
           f"input_rol_no_unico={rol}:n={len(encontrados)}")
    return encontrados[0]


def _filas_tsv(entrada: dict) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(_texto(entrada)), delimiter="\t"))


def _mapa_unico(filas: list[dict], campo: str, nombre: str) -> dict[str, dict]:
    salida: dict[str, dict] = {}
    for i, fila in enumerate(filas, start=1):
        clave = str(fila.get(campo, "")).strip()
        _exige(bool(clave), f"{nombre}_id_vacio=fila_{i}")
        _exige(clave not in salida, f"{nombre}_id_duplicado={clave}")
        salida[clave] = fila
    return salida


def _numero(valor, nombre: str, minimo: float | None = None,
            maximo: float | None = None) -> float:
    _exige(isinstance(valor, (int, float)) and not isinstance(valor, bool),
           f"{nombre}_no_numerico={valor!r}")
    numero = float(valor)
    _exige(math.isfinite(numero), f"{nombre}_no_finito={valor!r}")
    if minimo is not None:
        _exige(numero >= minimo, f"{nombre}_menor_que_{minimo}={numero}")
    if maximo is not None:
        _exige(numero <= maximo, f"{nombre}_mayor_que_{maximo}={numero}")
    return numero


def _parametros(contrato: dict) -> dict:
    p = contrato.get("parametros")
    _exige(isinstance(p, dict), "parametros_ausentes")
    requeridos = {
        "plan_version", "n_posiciones", "k_replicas", "variantes",
        "seleccion", "bootstrap_replicas", "nivel_ic", "delta_banda_pp",
        "tolerancia_numerica_pp", "contendientes", "comparaciones",
        "u3_congelado", "proposito", "estado_firewall_apto",
        "estado_m_apto", "comparabilidad_apta", "cumple_corte_apto",
        "r_punto_apto", "regex_punto_l", "estados_r_aptos",
    }
    faltan = sorted(requeridos - set(p))
    _exige(not faltan, f"parametros_faltantes={faltan}")
    _exige(p["seleccion"] == "MEDIANA-DE-REPLICAS-VALIDAS",
           f"seleccion_no_soportada={p['seleccion']}")
    _exige(isinstance(p["variantes"], dict) and len(p["variantes"]) == 2,
           "variantes_deben_mapear_dos_brazos")
    _exige(set(p["variantes"].values()) == {"L_SOLO", "L_CORPUS"},
           "variantes_no_corresponden_a_brazos_f5")
    _exige(isinstance(p["contendientes"], list)
           and set(p["contendientes"]) == {"L_SOLO", "L_CORPUS", "M"},
           "contendientes_no_son_triada_f5")
    for nombre in ("n_posiciones", "k_replicas", "bootstrap_replicas"):
        _exige(isinstance(p[nombre], int) and not isinstance(p[nombre], bool)
               and p[nombre] >= 1, f"{nombre}_no_entero_positivo")
    _numero(p["nivel_ic"], "nivel_ic", 0.0, 1.0)
    _exige(0.0 < float(p["nivel_ic"]) < 1.0, "nivel_ic_debe_ser_abierto_0_1")
    _numero(p["delta_banda_pp"], "delta_banda_pp", 0.0)
    _numero(p["tolerancia_numerica_pp"], "tolerancia_numerica_pp", 0.0)
    comparaciones = p["comparaciones"]
    _exige(isinstance(comparaciones, list)
           and all(isinstance(par, list) and len(par) == 2
                   and par[0] != par[1] for par in comparaciones),
           "comparaciones_malformadas")
    pares = {frozenset(par) for par in comparaciones}
    _exige(len(comparaciones) == 3 and pares == {
        frozenset(("L_SOLO", "L_CORPUS")),
        frozenset(("L_SOLO", "M")),
        frozenset(("L_CORPUS", "M")),
    }, "comparaciones_no_cubren_triada_exacta")
    _exige(isinstance(p["u3_congelado"], list)
           and all(isinstance(cid, str) and cid for cid in p["u3_congelado"]),
           "u3_congelado_malformado")
    _exige(isinstance(p["regex_punto_l"], str), "regex_punto_l_no_texto")
    try:
        re.compile(p["regex_punto_l"])
    except re.error as exc:
        raise ContratoInvalido(f"regex_punto_l_invalido={exc}") from exc
    _exige(isinstance(p["estados_r_aptos"], list)
           and all(isinstance(estado, str) and estado
                   for estado in p["estados_r_aptos"]),
           "estados_r_aptos_malformados")
    semilla = contrato.get("seed")
    _exige(isinstance(semilla, dict) and semilla.get("aplica") is True,
           "seed_no_aplica")
    _exige("valor" in semilla and semilla.get("rng") == "random.Random",
           "seed_sin_valor_o_rng_incorrecto")
    _exige(isinstance(semilla["valor"], int)
           and not isinstance(semilla["valor"], bool), "seed_no_entera")
    return p


def _extraer(texto: str | None, estado_captura: str, patron: re.Pattern) \
        -> tuple[str, float | None, str]:
    if estado_captura != "OK" or texto is None:
        return "ERROR_TECNICO", None, "captura sin respuesta CLI válida"
    lineas = [linea.strip() for linea in texto.splitlines() if linea.strip()]
    if not lineas:
        return "MALFORMADA", None, "respuesta vacía"
    ultima = lineas[-1]
    if ultima == "ABSTENCION":
        return "ABSTENCION", None, ultima
    coincidencia = patron.fullmatch(ultima)
    if not coincidencia:
        return "MALFORMADA", None, ultima[:240]
    valor = float(coincidencia.group(1).replace(",", "."))
    if not 0.0 <= valor <= 100.0:
        return "MALFORMADA", None, ultima[:240]
    return "VALIDA", valor / 100.0, ultima


def _percentil(valores: list[float], q: float) -> float:
    _exige(bool(valores), "percentil_lista_vacia")
    ordenados = sorted(valores)
    posicion = (len(ordenados) - 1) * q
    inferior = int(posicion)
    superior = min(inferior + 1, len(ordenados) - 1)
    fraccion = posicion - inferior
    return (ordenados[inferior] * (1 - fraccion)
            + ordenados[superior] * fraccion)


def adjudicar_ic(inferior: float, superior: float, delta: float,
                 tolerancia: float, a: str, b: str) -> str:
    _exige(inferior <= superior, "ic_invertido")
    if superior < -delta - tolerancia:
        return f"{a}-GANA"
    if inferior > delta + tolerancia:
        return f"{b}-GANA"
    if inferior >= -delta - tolerancia and superior <= delta + tolerancia:
        return "EMPATE-PRACTICO"
    return "INCONCLUSO"


def _valida_plan(plan: dict, p: dict) -> list[dict]:
    _exige(plan.get("version") == p["plan_version"],
           f"plan_version_discorda={plan.get('version')!r}")
    _exige(plan.get("n_posiciones") == p["n_posiciones"],
           "plan_n_posiciones_discorda_contrato")
    _exige(plan.get("k") == p["k_replicas"], "plan_k_discorda_contrato")
    _exige(plan.get("variantes") == list(p["variantes"]),
           "plan_variantes_discordan_contrato")
    posiciones = plan.get("posiciones")
    _exige(isinstance(posiciones, list)
           and len(posiciones) == p["n_posiciones"],
           "plan_longitud_posiciones_discorda")
    vistos_tupla, vistos_ruta, vistos_identidad = set(), set(), set()
    for posicion in posiciones:
        clave = (posicion.get("id_celda"), posicion.get("variante"),
                 posicion.get("replica"))
        _exige(all(x not in (None, "") for x in clave),
               f"plan_posicion_malformada={clave!r}")
        _exige(clave not in vistos_tupla, f"plan_posicion_duplicada={clave!r}")
        vistos_tupla.add(clave)
        ruta = posicion.get("ruta")
        identidad = posicion.get("identidad")
        _exige(isinstance(ruta, str) and ruta and ruta not in vistos_ruta,
               f"plan_ruta_vacia_o_duplicada={ruta!r}")
        _exige(isinstance(identidad, str)
               and re.fullmatch(r"[0-9a-f]{64}", identidad) is not None
               and identidad not in vistos_identidad,
               f"plan_identidad_invalida_o_duplicada={identidad!r}")
        vistos_ruta.add(ruta)
        vistos_identidad.add(identidad)
    return posiciones


def _capturas(plan: list[dict], entradas: list[dict], p: dict) \
        -> tuple[dict, list[dict], list[str]]:
    por_ruta = _mapa_unico(entradas, "ruta", "input_captura_ruta")
    rutas_plan = {pos["ruta"] for pos in plan}
    _exige(set(por_ruta) == rutas_plan,
           "capturas_inputs_no_corresponden_exactamente_al_plan")
    patron = re.compile(p["regex_punto_l"])
    agregados: dict[tuple[str, str], list[tuple[str, float | None]]] = {}
    filas, violaciones = [], []
    for posicion in plan:
        entrada = por_ruta[posicion["ruta"]]
        try:
            captura = json.loads(_texto(entrada))
        except (ValueError, UnicodeError) as exc:
            raise ContratoInvalido(
                f"captura_json_invalido={entrada['id']}:{type(exc).__name__}")
        identidad = captura.get("identidad")
        identidad_ok = (isinstance(identidad, str)
                        and identidad == posicion["identidad"])
        metadatos_ok = (
            captura.get("id_celda") == posicion["id_celda"]
            and captura.get("variante") == posicion["variante"]
            and captura.get("replica") == posicion["replica"]
        )
        if not identidad_ok or not metadatos_ok:
            estado, valor, evidencia = (
                "ERROR_IDENTIDAD", None,
                "identidad o coordenadas distintas del plan",
            )
            violaciones.append(
                f"captura_identidad={posicion['id_celda']}:{posicion['variante']}:"
                f"{posicion['replica']}"
            )
        else:
            estado, valor, evidencia = _extraer(
                captura.get("texto_crudo"),
                captura.get("estado_captura", "DESCONOCIDO"), patron,
            )
        clave = (posicion["id_celda"], posicion["variante"])
        agregados.setdefault(clave, []).append((estado, valor))
        filas.append({
            "id_celda": posicion["id_celda"],
            "variante": posicion["variante"],
            "replica": posicion["replica"],
            "estado": estado,
            "valor": valor,
            "evidencia": evidencia,
            "input_id": entrada["id"],
        })
    return agregados, filas, violaciones


def _resultado_r(entrada: dict, id_celda: str, p: dict) -> tuple[float, dict]:
    try:
        datos = json.loads(_texto(entrada))
    except (ValueError, UnicodeError) as exc:
        raise ContratoInvalido(
            f"resultado_r_json_invalido={id_celda}:{type(exc).__name__}")
    esperado_calc = entrada.get("calc_id_esperado")
    _exige(datos.get("spec_id") == esperado_calc,
           f"resultado_r_spec_id_discorda={id_celda}")
    resultados = datos.get("resultados")
    _exige(isinstance(resultados, dict), f"resultado_r_sin_mapa={id_celda}")
    clave = entrada.get("result_id_punto")
    _exige(isinstance(clave, str) and clave in resultados,
           f"resultado_r_sin_punto={id_celda}")
    punto = _numero(resultados[clave], f"punto_r_{id_celda}", 0.0, 1.0)
    clave_estado = entrada.get("result_id_estado")
    if clave_estado:
        _exige(resultados.get(clave_estado) in p.get("estados_r_aptos", []),
               f"resultado_r_estado_no_apto={id_celda}:"
               f"{resultados.get(clave_estado)!r}")
    return punto, datos


def _normaliza_linaje(resuelto: dict, id_celda: str) -> dict:
    _exige(isinstance(resuelto, dict), f"linaje_no_mapa={id_celda}")
    estado = resuelto.get("estado")
    _exige(estado in {"APTO", "NO-APTO", "INDETERMINADO"},
           f"linaje_estado_invalido={id_celda}:{estado!r}")
    dependencia = resuelto.get("dependencia_objetivo")
    _exige(dependencia in {"SI", "NO", "INDETERMINADA"},
           f"linaje_dependencia_invalida={id_celda}:{dependencia!r}")
    camino = resuelto.get("camino") or []
    _exige(isinstance(camino, list)
           and all(isinstance(paso, str) and paso for paso in camino),
           f"linaje_camino_invalido={id_celda}")
    _exige(estado != "APTO" or bool(camino),
           f"linaje_apto_sin_camino={id_celda}")
    return {
        "estado": estado,
        "origen_numerico": resuelto.get("origen_numerico", "INDETERMINADO"),
        "dependencia_objetivo": dependencia,
        "camino": camino,
        "razon": str(resuelto.get("razon") or ""),
    }


def calcular(inputs: dict[str, dict], contrato: dict,
             clasificar_linaje: ClasificadorLinaje) -> tuple[dict, list[dict]]:
    """Valida, calcula y conserva exclusiones sin volver a tocar el disco."""
    _verifica_inputs(inputs)
    for rol in ("contrato_estudio", "plan", "snapshot_m", "universo_r",
                "tarjetas_mr", "calculador", "linaje"):
        _unico(inputs, rol)
    p = _parametros(contrato)
    plan = json.loads(_texto(_unico(inputs, "plan")))
    posiciones = _valida_plan(plan, p)

    universo = _mapa_unico(_filas_tsv(_unico(inputs, "universo_r")),
                           "id_celda", "universo")
    tarjetas = _mapa_unico(_filas_tsv(_unico(inputs, "tarjetas_mr")),
                           "id_celda", "tarjetas")
    snapshot_datos = json.loads(_texto(_unico(inputs, "snapshot_m")))
    celdas_snapshot = snapshot_datos.get("celdas")
    _exige(isinstance(celdas_snapshot, list), "snapshot_m_sin_celdas")
    snapshot = _mapa_unico(celdas_snapshot, "id_celda", "snapshot_m")
    ids_plan = {pos["id_celda"] for pos in posiciones}
    _exige(ids_plan == set(universo) == set(snapshot) == set(tarjetas),
           "ids_plan_universo_snapshot_tarjetas_no_corresponden")

    entradas_r = _mapa_unico(_por_rol(inputs, "resultado_r"),
                             "id_celda", "input_r")
    _exige(set(entradas_r) == set(universo),
           "ids_resultados_r_no_corresponden_al_universo")
    for cid, fila in universo.items():
        ruta_esperada = f"{fila['fuente_R'].rstrip('/')}/resultados.json"
        _exige(entradas_r[cid].get("ruta") == ruta_esperada,
               f"ruta_resultado_r_discorda_universo={cid}")

    agregados, filas_captura, violaciones = _capturas(
        posiciones, _por_rol(inputs, "captura_l"), p,
    )
    estados_captura = Counter(fila["estado"] for fila in filas_captura)

    puntos_l = {"L_SOLO": {}, "L_CORPUS": {}}
    detalle: dict[str, dict] = {}
    r_datos: dict[str, dict] = {}
    puntos_r: dict[str, float] = {}
    puntos_m: dict[str, float | None] = {}
    m_elegible: dict[str, bool] = {}
    ids_ordenados = sorted(universo)

    for cid in ids_ordenados:
        tarjeta, celda_m = tarjetas[cid], snapshot[cid]
        punto_r, datos_r = _resultado_r(entradas_r[cid], cid, p)
        puntos_r[cid], r_datos[cid] = punto_r, datos_r
        razones: list[str] = []

        punto_m_crudo = celda_m.get("punto_M")
        try:
            punto_m = _numero(punto_m_crudo, f"punto_m_{cid}", 0.0, 1.0)
        except ContratoInvalido:
            punto_m = None
            razones.append("PUNTO-M-AUSENTE-O-MALFORMADO")
        puntos_m[cid] = punto_m
        if celda_m.get("identidad_confirmada") is not True:
            razones.append("IDENTIDAD-M-NO-CONFIRMADA")
        if celda_m.get("estado_M") != p["estado_m_apto"]:
            razones.append(f"ESTADO-M-{celda_m.get('estado_M', 'DESCONOCIDO')}")
        if celda_m.get("estado_firewall") != p["estado_firewall_apto"]:
            razones.append(
                f"FIREWALL-{celda_m.get('estado_firewall', 'DESCONOCIDO')}"
            )
        if tarjeta.get("proposito") != p["proposito"]:
            razones.append("TARJETA-PROPOSITO-DISCORDANTE")
        if tarjeta.get("comparabilidad") != p["comparabilidad_apta"]:
            razones.append(
                f"COMPARABILIDAD-{tarjeta.get('comparabilidad', 'DESCONOCIDA')}"
            )
        if tarjeta.get("estimando_alineado") != "SI":
            razones.append("ESTIMANDO-NO-ALINEADO")
        if tarjeta.get("cumple_corte") != p["cumple_corte_apto"]:
            razones.append(f"CORTE-{tarjeta.get('cumple_corte', 'DESCONOCIDO')}")
        if tarjeta.get("R_punto_apto") != p["r_punto_apto"]:
            razones.append(f"R-PUNTO-{tarjeta.get('R_punto_apto', 'DESCONOCIDO')}")

        linaje = _normaliza_linaje(clasificar_linaje(
            id_celda=cid,
            celda_m=dict(celda_m),
            resultado_r=dict(datos_r),
            tarjeta=dict(tarjeta),
            proposito=p["proposito"],
        ), cid)
        if linaje["estado"] != "APTO":
            razones.append(f"LINAJE-{linaje['estado']}")
        if linaje["dependencia_objetivo"] != "NO":
            razones.append(
                f"DEPENDENCIA-OBJETIVO-{linaje['dependencia_objetivo']}"
            )

        brazos = {}
        for variante, contendiente in p["variantes"].items():
            observaciones = agregados.get((cid, variante), [])
            _exige(len(observaciones) == p["k_replicas"],
                   f"replicas_discordan={cid}:{variante}:{len(observaciones)}")
            conteos = Counter(estado for estado, _valor in observaciones)
            valores = [valor for estado, valor in observaciones
                       if estado == "VALIDA" and valor is not None]
            punto = statistics.median(valores) if valores else None
            puntos_l[contendiente][cid] = punto
            brazos[contendiente] = {
                "programadas": p["k_replicas"],
                "validas": conteos["VALIDA"],
                "abstenciones": conteos["ABSTENCION"],
                "malformadas": conteos["MALFORMADA"],
                "errores_tecnicos": conteos["ERROR_TECNICO"],
                "errores_identidad": conteos["ERROR_IDENTIDAD"],
                "punto_mediana": punto,
            }
            if conteos["ERROR_IDENTIDAD"]:
                razones.append(f"IDENTIDAD-L-{contendiente}")

        es_elegible = not razones
        m_elegible[cid] = es_elegible
        detalle[cid] = {
            "fuente_criterio": tarjeta.get("fuente_criterio", ""),
            "criterio": tarjeta.get("causa", ""),
            "R": punto_r,
            "R_incertidumbre": tarjeta.get("R_incertidumbre", "DESCONOCIDA"),
            "M": punto_m,
            "linaje": linaje,
            "brazos": brazos,
            "elegible": es_elegible,
            "razones_exclusion": razones,
        }

    puntos = {**puntos_l, "M": puntos_m}
    u3 = [cid for cid in ids_ordenados
          if m_elegible[cid]
          and all(puntos[nombre].get(cid) is not None
                  for nombre in p["contendientes"])]
    u3_congelado = list(p["u3_congelado"])
    _exige(len(u3_congelado) == len(set(u3_congelado)),
           "u3_congelado_tiene_duplicados")
    _exige(set(u3_congelado) <= set(universo),
           "u3_congelado_contiene_id_extrano")
    comparacion_comprometida = u3 != sorted(u3_congelado)
    if violaciones:
        comparacion_comprometida = True

    errores = {
        nombre: [abs(puntos[nombre][cid] - puntos_r[cid]) * 100 for cid in u3]
        for nombre in p["contendientes"]
    }
    mae = {
        nombre: (statistics.mean(valores) if valores else None)
        for nombre, valores in errores.items()
    }
    comparaciones = {}
    if u3:
        n_boot = int(p["bootstrap_replicas"])
        semilla = contrato["seed"]["valor"]
        rng = random.Random(semilla)
        indices = [[rng.randrange(len(u3)) for _ in u3] for _ in range(n_boot)]
        alpha = (1.0 - float(p["nivel_ic"])) / 2.0
        for a, b in p["comparaciones"]:
            _exige(a in errores and b in errores,
                   f"comparacion_contendiente_desconocido={a}:{b}")
            deltas = [statistics.mean(errores[a][i] - errores[b][i]
                                      for i in muestra)
                      for muestra in indices]
            inferior = _percentil(deltas, alpha)
            superior = _percentil(deltas, 1.0 - alpha)
            comparaciones[f"{a}_vs_{b}"] = {
                "delta_mae_pp": mae[a] - mae[b],
                "ic_lo": inferior,
                "ic_hi": superior,
                "veredicto": adjudicar_ic(
                    inferior, superior,
                    float(p["delta_banda_pp"]),
                    float(p["tolerancia_numerica_pp"]), a, b,
                ),
            }

    cobertura = {
        "L_SOLO_con_punto": sum(v is not None for v in puntos_l["L_SOLO"].values()),
        "L_CORPUS_con_punto": sum(v is not None for v in puntos_l["L_CORPUS"].values()),
        "M_con_punto": sum(v is not None for v in puntos_m.values()),
        "M_elegible": sum(m_elegible.values()),
        "R_con_punto": len(puntos_r),
        "U3_puntuable": len(u3),
    }
    cobertura_contendiente = {
        "L_SOLO": cobertura["L_SOLO_con_punto"],
        "L_CORPUS": cobertura["L_CORPUS_con_punto"],
        "M": cobertura["M_con_punto"],
    }
    ganadores = []
    if u3 and not comparacion_comprometida:
        for x in p["contendientes"]:
            otros = [y for y in p["contendientes"] if y != x]
            # La escala global heredada exige ambas dominancias Y cobertura
            # no inferior sobre el marco, no solamente sobre U3.
            gana = all(cobertura_contendiente[x]
                       >= cobertura_contendiente[y] for y in otros)
            for y in otros:
                directa = comparaciones.get(f"{x}_vs_{y}")
                inversa = comparaciones.get(f"{y}_vs_{x}")
                veredicto = (directa or inversa or {}).get("veredicto")
                gana &= veredicto == f"{x}-GANA"
            if gana:
                ganadores.append(x)

    if comparacion_comprometida or not u3:
        veredicto = "NO-ADJUDICABLE-POR-CONTROL"
    elif len(ganadores) == 1:
        veredicto = f"GANADOR-TRIADA-{ganadores[0]}"
    else:
        veredicto = "SIN-GANADOR-UNICO"

    resultado = {
        "naturaleza": "REANALISIS-DIAGNOSTICO-PANEL-CONOCIDO",
        "proposito": p["proposito"],
        "marco_n": len(universo),
        "u3_congelado": u3_congelado,
        "u3_puntuable": u3,
        "u3_n": len(u3),
        "comparacion_congelada_comprometida": comparacion_comprometida,
        "cobertura": cobertura,
        "cobertura_contendiente_para_adjudicacion": cobertura_contendiente,
        "estados_captura": dict(sorted(estados_captura.items())),
        "mae_pp_diagnostico": mae,
        "comparaciones_diagnosticas": comparaciones,
        "veredicto_global": veredicto,
        "violaciones_identidad": violaciones,
        "parametros_consumidos": {
            "n_posiciones": p["n_posiciones"],
            "k_replicas": p["k_replicas"],
            "seleccion": p["seleccion"],
            "bootstrap_replicas": p["bootstrap_replicas"],
            "seed": contrato["seed"]["valor"],
            "rng": contrato["seed"]["rng"],
            "nivel_ic": p["nivel_ic"],
            "delta_banda_pp": p["delta_banda_pp"],
            "tolerancia_numerica_pp": p["tolerancia_numerica_pp"],
        },
        "celdas": detalle,
    }
    return resultado, filas_captura
