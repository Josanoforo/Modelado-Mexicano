#!/usr/bin/env python3
"""Preflight documental de F6 y transformaciones sintéticas mínimas.

Este módulo no resuelve rutas de payload, no abre microdatos, no llama modelos
y no escribe resultados. Las tarjetas son la única entrada del preflight.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import yaml

try:  # ejecución como script desde tools/
    from calcula_f5_sin_fugas import ContratoInvalido, _numero
except ModuleNotFoundError:  # importación desde tests/ como módulo del repo
    from tools.calcula_f5_sin_fugas import ContratoInvalido, _numero


ESTADO_SPEC = "PREPARADA-PARA-MESA · NO AUTORIZA EMISIONES NI R"
ESTADOS_DEFINICION_APTOS = {"ACREDITADA"}
ESTADOS_M_APTOS = {"ELEGIBLE"}
ESTADOS_RESERVA_APTOS = {"LIMPIA"}
ESTADOS_FIRMA_APTOS = {"FIRMADA"}


def _exige(condicion: bool, mensaje: str) -> None:
    if not condicion:
        raise ContratoInvalido(mensaje)


def proporcion_ponderada(
    filas: Iterable[dict], *, evento: set, elegible: str = "elegible",
    respuesta: str = "respuesta", peso: str = "peso", missing: set | None = None,
) -> float:
    """Proporción entre respuestas válidas elegibles; salto/missing salen.

    La función es sólo para fixtures sintéticos. Un blanco o missing nunca se
    convierte en respuesta negativa y un peso inválido se rechaza.
    """
    missing = set() if missing is None else set(missing)
    numerador = 0.0
    denominador = 0.0
    for i, fila in enumerate(filas, start=1):
        if fila.get(elegible) is not True:
            continue
        valor = fila.get(respuesta)
        if valor is None or valor in missing:
            continue
        w = _numero(fila.get(peso), f"peso_fila_{i}", 0.0)
        _exige(w > 0.0, f"peso_no_positivo_fila_{i}")
        denominador += w
        if valor in evento:
            numerador += w
    _exige(denominador > 0.0, "denominador_vacio")
    return numerador / denominador


def evento_issp_compuesto(valor, *, codigo_compuesto=1,
                          missing=frozenset({8, 9, None})) -> bool | None:
    """Codifica la categoría conjunta sin inventar familia frente a amistad."""
    if valor in missing:
        return None
    _exige(valor in {1, 2, 3, 4, 5, 6, 7},
           f"codigo_issp_fuera_contrato={valor!r}")
    return valor == codigo_compuesto


def a_puntos_porcentuales(valor: float, escala: str) -> float:
    numero = _numero(valor, "valor")
    if escala == "proporcion_0_1":
        _exige(numero <= 1.0, "proporcion_fuera_de_0_1")
        return numero * 100.0
    if escala == "porcentaje_0_100":
        _exige(numero <= 100.0, "porcentaje_fuera_de_0_100")
        return numero
    raise ContratoInvalido(f"escala_incompatible={escala}")


def error_absoluto_pp(prediccion: float | None, realidad: float,
                      *, escala_prediccion: str,
                      escala_realidad: str) -> float | None:
    """Una abstención conserva falta de cobertura; jamás se puntúa como cero."""
    if prediccion is None:
        return None
    return abs(
        a_puntos_porcentuales(prediccion, escala_prediccion)
        - a_puntos_porcentuales(realidad, escala_realidad)
    )


def agregar_errores_por_familia(filas: Iterable[dict]) -> dict[str, dict]:
    """Agrega celdas dentro de familia sin inflar la unidad inferencial."""
    por_familia: dict[str, list[float]] = defaultdict(list)
    celdas: dict[str, int] = defaultdict(int)
    abstenciones: dict[str, int] = defaultdict(int)
    for i, fila in enumerate(filas, start=1):
        familia = str(fila.get("familia_id") or "").strip()
        _exige(bool(familia), f"familia_vacia_fila_{i}")
        celdas[familia] += 1
        error = fila.get("error_pp")
        if error is None:
            abstenciones[familia] += 1
            continue
        por_familia[familia].append(_numero(error, f"error_fila_{i}", 0.0))
    salida = {}
    for familia in sorted(celdas):
        valores = por_familia.get(familia, [])
        salida[familia] = {
            "n_celdas": celdas[familia],
            "n_con_error": len(valores),
            "abstenciones": abstenciones[familia],
            "error_medio_pp": (sum(valores) / len(valores)) if valores else None,
        }
    return salida


def cargar_tarjetas(ruta: Path) -> dict:
    _exige(ruta.is_file(), f"tarjetas_ausentes={ruta}")
    datos = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    _exige(isinstance(datos, dict), "tarjetas_raiz_no_mapa")
    return datos


def _texto_no_vacio(mapa: dict, campo: str, contexto: str) -> str:
    valor = mapa.get(campo)
    _exige(isinstance(valor, str) and bool(valor.strip()),
           f"{contexto}_{campo}_ausente")
    return valor.strip()


def _preflight_celda(celda: dict, firma_estado: str) -> dict:
    cid = _texto_no_vacio(celda, "id_celda", "celda")
    for campo in (
        "familia_id", "candidata_id", "estimando", "poblacion", "unidad",
        "evento", "filtro", "denominador", "missing", "ponderador",
        "diseno", "periodo", "regla_consumidora",
    ):
        _texto_no_vacio(celda, campo, cid)
    escala = celda.get("escala")
    _exige(isinstance(escala, dict), f"{cid}_escala_ausente")
    _exige(escala.get("valor") == "proporcion_0_1",
           f"{cid}_escala_valor_no_comun")
    _exige(escala.get("error") == "puntos_porcentuales",
           f"{cid}_escala_error_no_pp")
    refs = celda.get("referencias_documentales")
    _exige(isinstance(refs, list) and refs
           and all(isinstance(x, str) and x.strip() for x in refs),
           f"{cid}_referencias_documentales_ausentes")
    payload = celda.get("payload_ref")
    _exige(isinstance(payload, str) and payload,
           f"{cid}_payload_ref_declarativo_ausente")

    definicion = celda.get("definicion", {})
    m = celda.get("enlace_M", {})
    reserva = celda.get("reserva", {})
    bloqueos = []
    if definicion.get("estado") not in ESTADOS_DEFINICION_APTOS:
        bloqueos.append(f"DEFINICION:{definicion.get('estado', 'AUSENTE')}")
    if m.get("estado") not in ESTADOS_M_APTOS:
        bloqueos.append(f"M:{m.get('estado', 'AUSENTE')}")
    if reserva.get("estado") not in ESTADOS_RESERVA_APTOS:
        bloqueos.append(f"RESERVA:{reserva.get('estado', 'AUSENTE')}")
    dependencias = celda.get("dependencias_pendientes", [])
    _exige(isinstance(dependencias, list)
           and all(isinstance(x, str) and x.strip() for x in dependencias),
           f"{cid}_dependencias_malformadas")
    if bloqueos:
        estado = "DEFINICION_O_CANDIDATO_INSUFICIENTE"
    elif firma_estado not in ESTADOS_FIRMA_APTOS:
        estado = "AUTORIZACION_PENDIENTE"
        bloqueos.append(f"FIRMA:{firma_estado}")
    else:
        estado = "PREPARACION_COMPLETA"
    return {
        "id_celda": cid,
        "familia_id": celda["familia_id"],
        "estado": estado,
        "bloqueos": bloqueos,
        "dependencias_pendientes": dependencias,
        "payload_abierto": False,
    }


def preflight(datos: dict) -> dict:
    _exige(datos.get("estado") == ESTADO_SPEC, "estado_spec_no_protege")
    _exige(datos.get("llamadas_autorizadas") is False,
           "llamadas_no_deben_estar_autorizadas")
    firma = datos.get("firma", {})
    _exige(isinstance(firma, dict), "firma_ausente")
    firma_estado = str(firma.get("estado") or "AUSENTE")
    celdas = datos.get("celdas")
    _exige(isinstance(celdas, list) and celdas, "celdas_vacias")
    _exige(len(celdas) <= 4, "mas_de_cuatro_celdas")
    detalle = [_preflight_celda(celda, firma_estado) for celda in celdas]
    ids = [x["id_celda"] for x in detalle]
    _exige(len(ids) == len(set(ids)), "ids_celda_duplicados")
    familias = {x["familia_id"] for x in detalle}
    _exige(len(familias) <= 2, "mas_de_dos_familias")
    estados = defaultdict(int)
    for fila in detalle:
        estados[fila["estado"]] += 1
    autorizada = (
        firma_estado in ESTADOS_FIRMA_APTOS
        and estados["PREPARACION_COMPLETA"] == len(detalle)
        and datos.get("llamadas_autorizadas") is True
    )
    # El contrato actual fija llamadas_autorizadas=false; se conserva la
    # expresión explícita para impedir que un YAML parseable suplante firma.
    _exige(not autorizada, "spec_de_preparacion_no_puede_autorizar")
    return {
        "schema_version": datos.get("schema_version"),
        "estado_spec": datos["estado"],
        "firma_estado": firma_estado,
        "familias": len(familias),
        "celdas": len(detalle),
        "conteos": dict(sorted(estados.items())),
        "autorizado_para_llamadas": False,
        "microdatos_abiertos": False,
        "modelos_llamados": False,
        "resultados_canonicos_escritos": False,
        "detalle": detalle,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Preflight documental F6; nunca abre payloads ni llama modelos."
    )
    parser.add_argument("--cards", type=Path, required=True,
                        help="YAML de tarjetas F6")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        resultado = preflight(cargar_tarjetas(args.cards))
    except (ContratoInvalido, OSError, yaml.YAMLError) as exc:
        print(json.dumps({"estado": "PRECHECK-INVALIDO", "error": str(exc)},
                         ensure_ascii=False, sort_keys=True))
        return 2
    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, sort_keys=True,
                         indent=2))
    else:
        print("F6-PREFLIGHT")
        print(f"familias={resultado['familias']} celdas={resultado['celdas']}")
        for fila in resultado["detalle"]:
            bloqueos = ",".join(fila["bloqueos"]) or "NINGUNO"
            print(f"{fila['id_celda']}\t{fila['estado']}\t{bloqueos}")
        print("AUTORIZADO_PARA_LLAMADAS=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
