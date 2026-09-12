#!/usr/bin/env python3
"""Comparacion explicita y reproducible entre dos valores identificados.

Este modulo no descubre parejas. Cada pareja declara dos referencias exactas,
un uso y un contrato cientifico. Tampoco adopta resultados ni escribe las
vistas de corrida0: solamente resuelve, compara y produce un informe.

Se importa desde ``tools/corrida0.py`` de forma perezosa. Las operaciones que
ya tienen una autoridad en corrida0 (carga de spec, sello y comparador de
adopcion) se reciben en ``canon`` para evitar duplicarlas y evitar un ciclo de
imports.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import os
from pathlib import Path
import sys
import tempfile
from typing import Any


VERSION_CONTRATO = "GEN2-DELTA-1"
DIMENSIONES = (
    "unidad", "escala", "direccion", "poblacion", "evento", "codigos",
    "periodo", "transformacion",
)
ESTADOS_COMPATIBLES = {
    "COINCIDE", "DISTINTO-INTENCIONAL", "DERIVA-DOCUMENTADA",
}
ESTADOS_INCOMPATIBLES = {"INCOMPATIBLE", "RUPTURA"}
ESTADOS_INDETERMINADOS = {"INFORMACION-INSUFICIENTE"}
TIPOS_NUMERICOS = {"entero", "flotante", "proporcion"}


class ErrorContrato(ValueError):
    """La peticion no expresa un contrato valido y no debe ejecutarse."""


class ReferenciaNoResuelta(RuntimeError):
    """Una identidad pedida no se pudo acreditar sin elegir por parecido."""


def _sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as fh:
        for bloque in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


def _ruta_repo(raiz: Path, crudo: str, *, debe_existir: bool = True) -> Path:
    if not crudo or Path(crudo).is_absolute():
        raise ReferenciaNoResuelta(f"ruta debe ser relativa al repo: {crudo!r}")
    candidata = (raiz / crudo).resolve()
    try:
        candidata.relative_to(raiz.resolve())
    except ValueError as exc:
        raise ReferenciaNoResuelta(f"ruta escapa del repo: {crudo!r}") from exc
    if debe_existir and not candidata.is_file():
        raise ReferenciaNoResuelta(f"fuente ausente: {crudo}")
    return candidata


def _verifica_archivo(raiz: Path, ref: dict, etiqueta: str) -> tuple[Path, str]:
    ruta_rel = ref.get("fuente") or ref.get("path")
    esperado = ref.get("sha256")
    if not isinstance(ruta_rel, str) or not isinstance(esperado, str):
        raise ReferenciaNoResuelta(
            f"{etiqueta}: fuente y sha256 explicitos son obligatorios")
    ruta = _ruta_repo(raiz, ruta_rel)
    obtenido = _sha256(ruta)
    if obtenido != esperado:
        raise ReferenciaNoResuelta(
            f"{etiqueta}: HASH-NO-COINCIDE {ruta_rel}: "
            f"esperado={esperado} obtenido={obtenido}")
    return ruta, obtenido


def _valor_por_ruta(objeto: Any, ruta: list[Any]) -> Any:
    actual = objeto
    for paso in ruta:
        if isinstance(actual, dict) and paso in actual:
            actual = actual[paso]
        elif isinstance(actual, list) and isinstance(paso, int) and 0 <= paso < len(actual):
            actual = actual[paso]
        else:
            raise ReferenciaNoResuelta(
                f"selector no encuentra el paso {paso!r} en {ruta!r}")
    return actual


def _convierte_valor(valor: Any, tipo: str) -> Any:
    if valor in (None, ""):
        return None
    if tipo == "entero":
        if isinstance(valor, bool):
            raise ReferenciaNoResuelta("un booleano no es un entero de resultado")
        try:
            numero = int(valor)
        except (TypeError, ValueError) as exc:
            raise ReferenciaNoResuelta(f"valor no entero: {valor!r}") from exc
        if isinstance(valor, float) and numero != valor:
            raise ReferenciaNoResuelta(f"valor no entero: {valor!r}")
        return numero
    if tipo in {"flotante", "proporcion"}:
        if isinstance(valor, bool):
            raise ReferenciaNoResuelta("un booleano no es un valor numerico")
        try:
            numero = float(valor)
        except (TypeError, ValueError) as exc:
            raise ReferenciaNoResuelta(f"valor no numerico: {valor!r}") from exc
        if not math.isfinite(numero):
            raise ReferenciaNoResuelta(f"valor no finito: {valor!r}")
        if tipo == "proporcion" and not 0.0 <= numero <= 1.0:
            raise ReferenciaNoResuelta(f"proporcion fuera de [0,1]: {numero!r}")
        return numero
    if tipo == "texto":
        return str(valor)
    raise ReferenciaNoResuelta(f"tipo de referencia desconocido: {tipo!r}")


def _resuelve_fuente(ref: dict, canon) -> dict:
    raiz = canon.RAIZ
    for campo in ("version", "tipo", "unidad", "selector"):
        if campo not in ref:
            raise ReferenciaNoResuelta(
                f"fuente: falta identidad obligatoria {campo!r}")
    ruta, sha = _verifica_archivo(raiz, ref, "fuente")
    selector = ref["selector"]
    if not isinstance(selector, dict):
        raise ReferenciaNoResuelta("fuente: selector debe ser un mapa")
    formato = selector.get("formato")

    if formato == "yaml":
        datos = canon._yaml_safe_load(ruta.read_text(encoding="utf-8"))
        recorrido = selector.get("ruta")
        if not isinstance(recorrido, list):
            raise ReferenciaNoResuelta("selector yaml requiere ruta como lista")
        valor = _valor_por_ruta(datos, recorrido)
        selector_resuelto = {"formato": formato, "ruta": recorrido}
    elif formato == "json":
        try:
            datos = json.loads(ruta.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ReferenciaNoResuelta(f"JSON ilegible: {exc}") from exc
        recorrido = selector.get("ruta")
        if not isinstance(recorrido, list):
            raise ReferenciaNoResuelta("selector json requiere ruta como lista")
        valor = _valor_por_ruta(datos, recorrido)
        selector_resuelto = {"formato": formato, "ruta": recorrido}
    elif formato == "tsv":
        clave = selector.get("clave")
        columna = selector.get("columna")
        if not isinstance(clave, dict) or not clave or not isinstance(columna, str):
            raise ReferenciaNoResuelta(
                "selector tsv requiere clave no vacia y columna")
        with ruta.open(encoding="utf-8", newline="") as fh:
            filas = list(csv.DictReader(fh, delimiter="\t"))
        coincidencias = [
            f for f in filas
            if all(str(f.get(k, "")) == str(v) for k, v in clave.items())
        ]
        if len(coincidencias) != 1:
            raise ReferenciaNoResuelta(
                f"selector tsv resolvio {len(coincidencias)} filas; se exige una: {clave}")
        if columna not in coincidencias[0]:
            raise ReferenciaNoResuelta(f"columna tsv ausente: {columna}")
        valor = coincidencias[0][columna]
        selector_resuelto = {"formato": formato, "clave": clave, "columna": columna}
    else:
        raise ReferenciaNoResuelta(f"formato de selector no soportado: {formato!r}")

    valor = _convierte_valor(valor, ref["tipo"])
    estado_valor = "NO-ESTIMABLE" if valor is None else "VALOR"
    return {
        "estado": "RESUELTA",
        "estado_valor": estado_valor,
        "clase_referencia": "FUENTE",
        "valor": valor,
        "tipo": ref["tipo"],
        "unidad": ref["unidad"],
        "fuente": ref["fuente"],
        "sha256": sha,
        "version": str(ref["version"]),
        "selector": selector_resuelto,
    }


def _resuelve_resultado(ref: dict, canon) -> dict:
    obligatorios = (
        "calc_id", "corrida_id", "resultado_id", "spec_sha256",
        "resultados_sha256", "sello_sha256",
    )
    faltan = [c for c in obligatorios if not ref.get(c)]
    if faltan:
        raise ReferenciaNoResuelta(
            f"resultado: faltan identidades/versiones {', '.join(faltan)}")

    calc_id = str(ref["calc_id"])
    try:
        directorio, spec = canon._carga_spec(calc_id)
    except Exception as exc:  # normaliza el bloqueo canónico como estado del par
        raise ReferenciaNoResuelta(f"{calc_id}: {exc}") from exc
    if spec.get("calc_id") != calc_id:
        raise ReferenciaNoResuelta(
            f"calc_id interno {spec.get('calc_id')!r} != {calc_id!r}")

    rutas = {
        "spec_sha256": directorio / "spec.yaml",
        "resultados_sha256": directorio / "resultados.json",
        "sello_sha256": directorio / "sello.json",
    }
    hashes = {}
    for campo, ruta in rutas.items():
        if not ruta.is_file():
            raise ReferenciaNoResuelta(f"{calc_id}: falta {ruta.name}")
        hashes[campo] = _sha256(ruta)
        if hashes[campo] != ref[campo]:
            raise ReferenciaNoResuelta(
                f"{calc_id}: {campo} no coincide: esperado={ref[campo]} "
                f"obtenido={hashes[campo]}")

    estado_sello, razon_sello = canon._verifica_sello(directorio)
    if estado_sello != "COINCIDE":
        raise ReferenciaNoResuelta(
            f"{calc_id}: sello {estado_sello}: {razon_sello}")

    try:
        ejecucion = json.loads((directorio / "ejecucion.json").read_text(encoding="utf-8"))
        resultados = json.loads(rutas["resultados_sha256"].read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ReferenciaNoResuelta(f"{calc_id}: artefacto JSON ilegible: {exc}") from exc
    if ejecucion.get("corrida_id") != ref["corrida_id"]:
        raise ReferenciaNoResuelta(
            f"corrida_id {ejecucion.get('corrida_id')!r} != {ref['corrida_id']!r}")

    rid = str(ref["resultado_id"])
    declaraciones = [r for r in (spec.get("resultados") or []) if r.get("id") == rid]
    if len(declaraciones) != 1:
        raise ReferenciaNoResuelta(
            f"{calc_id}/{rid}: aparece {len(declaraciones)} veces en spec; se exige una")
    valores = resultados.get("resultados") if isinstance(resultados, dict) else None
    if not isinstance(valores, dict) or rid not in valores:
        raise ReferenciaNoResuelta(f"{calc_id}/{rid}: RESULT ausente")
    if rid not in (ejecucion.get("resultado_ids") or []):
        raise ReferenciaNoResuelta(f"{calc_id}/{rid}: no consta en ejecucion.json")

    decl = declaraciones[0]
    valor = _convierte_valor(valores[rid], decl.get("tipo"))
    return {
        "estado": "RESUELTA",
        "estado_valor": "NO-ESTIMABLE" if valor is None else "VALOR",
        "clase_referencia": "RESULTADO-CORRIDA0",
        "valor": valor,
        "tipo": decl.get("tipo"),
        "unidad": decl.get("unidad", "NO-DECLARADA"),
        "calc_id": calc_id,
        "corrida_id": ref["corrida_id"],
        "resultado_id": rid,
        "spec_sha256": hashes["spec_sha256"],
        "resultados_sha256": hashes["resultados_sha256"],
        "sello_sha256": hashes["sello_sha256"],
        "sello": estado_sello,
        "git_commit_ejecucion": ejecucion.get("git_commit"),
        "declaracion": decl,
        "tolerancia": spec.get("tolerancia") or {},
        "tolerancia_adopcion": spec.get("tolerancia_adopcion"),
    }


def resuelve_referencia(ref: dict, canon) -> dict:
    if not isinstance(ref, dict):
        raise ReferenciaNoResuelta("referencia debe ser un mapa")
    clase = ref.get("clase")
    if clase == "fuente":
        return _resuelve_fuente(ref, canon)
    if clase == "resultado":
        return _resuelve_resultado(ref, canon)
    raise ReferenciaNoResuelta(f"clase de referencia desconocida: {clase!r}")


def _evidencias_acreditadas(evidencias: Any, canon, etiqueta: str) -> list[dict]:
    if not isinstance(evidencias, list) or not evidencias:
        raise ErrorContrato(f"{etiqueta}: se exige al menos una evidencia citada")
    salida = []
    for i, evidencia in enumerate(evidencias, 1):
        if not isinstance(evidencia, dict) or not evidencia.get("cita"):
            raise ErrorContrato(f"{etiqueta}[{i}]: falta cita")
        try:
            _, sha = _verifica_archivo(canon.RAIZ, evidencia, f"{etiqueta}[{i}]")
        except ReferenciaNoResuelta as exc:
            raise ErrorContrato(str(exc)) from exc
        salida.append({
            "fuente": evidencia.get("fuente") or evidencia.get("path"),
            "sha256": sha,
            "cita": str(evidencia["cita"]),
        })
    return salida


def evalua_comparabilidad(contrato: dict, canon) -> dict:
    if not isinstance(contrato, dict):
        raise ErrorContrato("comparabilidad debe ser un mapa")
    dimensiones = contrato.get("dimensiones")
    if not isinstance(dimensiones, dict):
        raise ErrorContrato("comparabilidad.dimensiones debe ser un mapa")
    faltan = [d for d in DIMENSIONES if d not in dimensiones]
    if faltan:
        raise ErrorContrato(
            f"comparabilidad: faltan dimensiones {', '.join(faltan)}")
    estados = {}
    for dimension in DIMENSIONES:
        dato = dimensiones[dimension]
        if not isinstance(dato, dict) or not dato.get("razon"):
            raise ErrorContrato(
                f"comparabilidad.{dimension}: estado y razon son obligatorios")
        estado = dato.get("estado")
        permitidos = ESTADOS_COMPATIBLES | ESTADOS_INCOMPATIBLES | ESTADOS_INDETERMINADOS
        if estado not in permitidos:
            raise ErrorContrato(
                f"comparabilidad.{dimension}: estado desconocido {estado!r}")
        estados[dimension] = {"estado": estado, "razon": str(dato["razon"])}

    evidencias = _evidencias_acreditadas(
        contrato.get("evidencias"), canon, "comparabilidad.evidencias")
    incompatibles = [d for d, v in estados.items() if v["estado"] in ESTADOS_INCOMPATIBLES]
    indeterminadas = [d for d, v in estados.items() if v["estado"] in ESTADOS_INDETERMINADOS]
    if incompatibles:
        estado = "INCOMPATIBILIDAD"
        causa = "ruptura/incompatibilidad en: " + ", ".join(incompatibles)
    elif indeterminadas:
        estado = "INFORMACION-INSUFICIENTE"
        causa = "informacion insuficiente en: " + ", ".join(indeterminadas)
    else:
        estado = "DEMOSTRADA"
        causa = "las ocho dimensiones tienen correspondencia acreditada"
    return {
        "estado": estado,
        "causa": causa,
        "dimensiones": estados,
        "evidencias": evidencias,
    }


def calcula_diferencia(valor_a: Any, valor_b: Any, *, escala: str,
                       relativo_permitido: bool, razon_relativo: str = "") -> dict:
    """Calcula siempre B-A; conserva faltantes y protege la base cero."""
    if valor_a is None or valor_b is None:
        return {
            "estado": "NO-CALCULABLE-VALOR-AUSENTE", "operacion": "B - A",
            "delta": None, "magnitud_absoluta": None,
            "puntos_porcentuales": None, "cambio_relativo": None,
            "estado_relativo": "NO-APLICA-VALOR-AUSENTE",
        }
    if isinstance(valor_a, bool) or isinstance(valor_b, bool) or not all(
            isinstance(v, (int, float)) for v in (valor_a, valor_b)):
        return {
            "estado": "NO-CALCULABLE-NO-NUMERICO", "operacion": "B - A",
            "delta": None, "magnitud_absoluta": None,
            "puntos_porcentuales": None, "cambio_relativo": None,
            "estado_relativo": "NO-APLICA-NO-NUMERICO",
        }
    a, b = float(valor_a), float(valor_b)
    if not math.isfinite(a) or not math.isfinite(b):
        return {
            "estado": "NO-CALCULABLE-NO-FINITO", "operacion": "B - A",
            "delta": None, "magnitud_absoluta": None,
            "puntos_porcentuales": None, "cambio_relativo": None,
            "estado_relativo": "NO-APLICA-NO-FINITO",
        }
    delta = b - a
    pp = delta * 100.0 if escala == "proporcion" else None
    relativo = None
    if not relativo_permitido:
        estado_rel = "NO-APLICA-POR-CONTRATO"
    elif a == 0.0:
        estado_rel = "NO-APLICA-BASE-CERO"
    else:
        relativo = delta / a
        estado_rel = "CALCULADO"
    return {
        "estado": "CALCULADO", "operacion": "B - A", "delta": delta,
        "magnitud_absoluta": abs(delta), "puntos_porcentuales": pp,
        "cambio_relativo": relativo, "estado_relativo": estado_rel,
        "razon_relativo": razon_relativo,
    }


def _evalua_representacion(config: Any, refs: dict, comparabilidad: dict, canon) -> dict:
    if not config or config.get("aplica") is False:
        razon = (config or {}).get("razon", "no se declaro comparacion de representacion")
        return {"estado": "NO-APLICA", "razon": razon, "delta_abs": None, "modo": None}
    if comparabilidad["estado"] != "DEMOSTRADA":
        return {
            "estado": "NO-APLICA-COMPARABILIDAD", "razon": comparabilidad["causa"],
            "delta_abs": None, "modo": None,
        }
    publicado = config.get("publicado")
    preciso = config.get("preciso")
    if {publicado, preciso} != {"a", "b"}:
        raise ErrorContrato("representacion requiere publicado/preciso = a/b en lados distintos")
    ref_publicada, ref_precisa = refs[publicado], refs[preciso]
    if ref_publicada.get("estado") != "RESUELTA" or ref_precisa.get("estado") != "RESUELTA":
        return {
            "estado": "NO-DETERMINABLE-REFERENCIA", "razon": "una referencia no se resolvio",
            "delta_abs": None, "modo": None,
        }
    if ref_precisa.get("clase_referencia") != "RESULTADO-CORRIDA0":
        raise ErrorContrato("representacion.preciso debe ser una referencia RESULT de corrida0")
    igual, delta, modo = canon._compara_adopcion(
        ref_precisa.get("valor"), ref_publicada.get("valor"),
        ref_precisa.get("declaracion") or {}, ref_precisa.get("tolerancia") or {},
        config.get("tolerancia_adopcion",
                   ref_precisa.get("tolerancia_adopcion")),
    )
    return {
        "estado": "IGUAL-AL-GRANO" if igual else "DISTINTO-AL-GRANO",
        "razon": "comparador canonico de adopcion; no es criterio de materialidad",
        "delta_abs": delta, "modo": modo,
    }


def _evalua_materialidad(config: Any, diferencia: dict, comparabilidad: dict,
                         canon) -> dict:
    if not config or config.get("criterio") in (None, ""):
        return {
            "estado": "NO-DETERMINABLE", "criterio": None,
            "razon": ((config or {}).get("razon") or
                      "no existe criterio sustantivo explicito y citado"),
        }
    if comparabilidad["estado"] != "DEMOSTRADA" or diferencia["estado"] != "CALCULADO":
        return {
            "estado": "NO-DETERMINABLE", "criterio": config.get("criterio"),
            "razon": "sin delta comparable no se evalua materialidad",
        }
    criterio = config["criterio"]
    if not isinstance(criterio, dict):
        raise ErrorContrato("materialidad.criterio debe ser mapa o null")
    _evidencias_acreditadas(
        criterio.get("evidencias"), canon, "materialidad.criterio.evidencias")
    metrica = criterio.get("metrica")
    mapa = {
        "magnitud_absoluta": diferencia.get("magnitud_absoluta"),
        "puntos_porcentuales_abs": (
            abs(diferencia["puntos_porcentuales"])
            if diferencia.get("puntos_porcentuales") is not None else None),
        "cambio_relativo_abs": (
            abs(diferencia["cambio_relativo"])
            if diferencia.get("cambio_relativo") is not None else None),
    }
    if metrica not in mapa:
        raise ErrorContrato(f"metrica de materialidad desconocida: {metrica!r}")
    try:
        umbral = float(criterio["umbral"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ErrorContrato("materialidad requiere umbral numerico") from exc
    valor = mapa[metrica]
    if valor is None:
        return {
            "estado": "NO-DETERMINABLE", "criterio": criterio,
            "razon": f"la metrica {metrica} no aplica a este par",
        }
    return {
        "estado": "MATERIAL" if valor >= umbral else "NO-MATERIAL",
        "criterio": criterio, "razon": f"{metrica}={valor} frente a umbral={umbral}",
    }


def _referencia_fallida(exc: Exception) -> dict:
    return {
        "estado": "NO-RESUELTA", "estado_valor": "NO-DETERMINABLE",
        "clase_referencia": "NO-DETERMINADA", "valor": None,
        "tipo": None, "unidad": None, "razon": str(exc),
    }


def compara_par(par: dict, canon) -> dict:
    for campo in ("id", "consumidor", "uso", "a", "b", "comparabilidad", "diferencia"):
        if campo not in par:
            raise ErrorContrato(f"par: falta campo obligatorio {campo!r}")
    if not isinstance(par["uso"], dict) or not par["uso"].get("descripcion"):
        raise ErrorContrato(f"{par['id']}: uso.descripcion es obligatorio")
    uso_evidencias = _evidencias_acreditadas(
        par["uso"].get("evidencias"), canon, f"{par['id']}.uso.evidencias")

    refs = {}
    for lado in ("a", "b"):
        try:
            refs[lado] = resuelve_referencia(par[lado], canon)
        except ReferenciaNoResuelta as exc:
            refs[lado] = _referencia_fallida(exc)

    comparabilidad = evalua_comparabilidad(par["comparabilidad"], canon)
    ref_fallida = any(r["estado"] != "RESUELTA" for r in refs.values())
    if ref_fallida:
        diferencia = {
            "estado": "NO-CALCULABLE-REFERENCIA", "operacion": "B - A",
            "delta": None, "magnitud_absoluta": None, "puntos_porcentuales": None,
            "cambio_relativo": None, "estado_relativo": "NO-APLICA-REFERENCIA",
            "unidad": par["diferencia"].get("unidad"),
        }
    elif comparabilidad["estado"] != "DEMOSTRADA":
        diferencia = {
            "estado": "NO-CALCULADO-COMPARABILIDAD", "operacion": "B - A",
            "delta": None, "magnitud_absoluta": None, "puntos_porcentuales": None,
            "cambio_relativo": None, "estado_relativo": "NO-APLICA-COMPARABILIDAD",
            "unidad": par["diferencia"].get("unidad"),
        }
    else:
        relativo = par["diferencia"].get("relativo") or {}
        diferencia = calcula_diferencia(
            refs["a"].get("valor"), refs["b"].get("valor"),
            escala=str(par["diferencia"].get("escala", "otra")),
            relativo_permitido=relativo.get("permitido") is True,
            razon_relativo=str(relativo.get("razon", "")),
        )
        diferencia["unidad"] = par["diferencia"].get("unidad")

    representacion = _evalua_representacion(
        par.get("representacion"), refs, comparabilidad, canon)
    materialidad = _evalua_materialidad(
        par.get("materialidad"), diferencia, comparabilidad, canon)

    if ref_fallida:
        resultado = "REFERENCIA-NO-RESUELTA"
    elif comparabilidad["estado"] != "DEMOSTRADA":
        resultado = f"DELTA-SUSTANTIVO-RECHAZADO-{comparabilidad['estado']}"
    else:
        resultado = (
            f"DELTA-{diferencia['estado']} · REPRESENTACION-{representacion['estado']} · "
            f"MATERIALIDAD-{materialidad['estado']}")
    return {
        "id": str(par["id"]),
        "consumidor": str(par["consumidor"]),
        "uso": {"descripcion": str(par["uso"]["descripcion"]),
                "evidencias": uso_evidencias},
        "referencias": refs,
        "reproducibilidad_referencias": (
            "ACREDITADA" if not ref_fallida else "NO-ACREDITADA"),
        "comparabilidad": comparabilidad,
        "diferencia": diferencia,
        "representacion": representacion,
        "materialidad": materialidad,
        "resultado": resultado,
    }


def _totales(pares: list[dict]) -> dict:
    return {
        "pares_examinados": len(pares),
        "comparables": sum(p["comparabilidad"]["estado"] == "DEMOSTRADA" for p in pares),
        "incompatibles": sum(p["comparabilidad"]["estado"] == "INCOMPATIBILIDAD" for p in pares),
        "comparabilidad_no_determinable": sum(
            p["comparabilidad"]["estado"] == "INFORMACION-INSUFICIENTE" for p in pares),
        "deltas_calculados": sum(p["diferencia"]["estado"] == "CALCULADO" for p in pares),
        "referencias_no_resueltas": sum(
            p["reproducibilidad_referencias"] != "ACREDITADA" for p in pares),
        "representacion_igual": sum(
            p["representacion"]["estado"] == "IGUAL-AL-GRANO" for p in pares),
        "materiales": sum(p["materialidad"]["estado"] == "MATERIAL" for p in pares),
        "no_materiales": sum(p["materialidad"]["estado"] == "NO-MATERIAL" for p in pares),
        "materialidad_no_determinable": sum(
            p["materialidad"]["estado"] == "NO-DETERMINABLE" for p in pares),
    }


def ejecuta(entrada: Path, canon) -> dict:
    entrada = entrada.resolve()
    try:
        entrada.relative_to(canon.RAIZ.resolve())
    except ValueError as exc:
        raise ErrorContrato("la entrada debe vivir dentro del repositorio") from exc
    if not entrada.is_file():
        raise ErrorContrato(f"entrada ausente: {entrada}")
    try:
        contrato = canon._yaml_safe_load(entrada.read_text(encoding="utf-8")) or {}
    except (OSError, ValueError) as exc:
        raise ErrorContrato(f"entrada ilegible: {exc}") from exc
    if contrato.get("version") != VERSION_CONTRATO:
        raise ErrorContrato(
            f"version debe ser {VERSION_CONTRATO!r}; llego {contrato.get('version')!r}")
    pares_crudos = contrato.get("pares")
    if not isinstance(pares_crudos, list) or not pares_crudos:
        raise ErrorContrato("pares debe ser una lista no vacia")
    ids = [p.get("id") for p in pares_crudos if isinstance(p, dict)]
    if len(ids) != len(pares_crudos) or len(ids) != len(set(ids)) or any(not i for i in ids):
        raise ErrorContrato("cada par requiere id no vacio y unico")
    pares = [compara_par(p, canon) for p in pares_crudos]
    totales = _totales(pares)
    return {
        "contrato": VERSION_CONTRATO,
        "entrada": str(entrada.relative_to(canon.RAIZ.resolve())),
        "entrada_sha256": _sha256(entrada),
        "descripcion": contrato.get("descripcion", ""),
        "totales": totales,
        "lectura_global": (
            "Los veredictos aplican solo a los pares explicitos examinados. "
            "Cero materiales no demuestra coincidencia general y la equivalencia "
            "de representacion no determina materialidad cientifica."),
        "pares": pares,
    }


def como_tsv(informe: dict) -> str:
    columnas = [
        "par_id", "consumidor", "uso", "a_estado", "a_clase", "a_valor",
        "a_fuente", "b_estado", "b_clase", "b_valor", "b_fuente",
        "referencias_reproducibles", "comparabilidad", "causa_comparabilidad",
        "delta_b_menos_a", "magnitud_absoluta", "unidad", "puntos_porcentuales",
        "cambio_relativo", "estado_relativo", "representacion", "modo_representacion",
        "materialidad", "criterio_materialidad", "resultado",
    ]
    salida = io.StringIO()
    escritor = csv.DictWriter(salida, fieldnames=columnas, delimiter="\t", lineterminator="\n")
    escritor.writeheader()
    for p in informe["pares"]:
        a, b, d = p["referencias"]["a"], p["referencias"]["b"], p["diferencia"]
        escritor.writerow({
            "par_id": p["id"], "consumidor": p["consumidor"],
            "uso": p["uso"]["descripcion"], "a_estado": a["estado"],
            "a_clase": a.get("clase_referencia"), "a_valor": a.get("valor"),
            "a_fuente": a.get("fuente") or a.get("resultado_id"),
            "b_estado": b["estado"], "b_clase": b.get("clase_referencia"),
            "b_valor": b.get("valor"), "b_fuente": b.get("fuente") or b.get("resultado_id"),
            "referencias_reproducibles": p["reproducibilidad_referencias"],
            "comparabilidad": p["comparabilidad"]["estado"],
            "causa_comparabilidad": p["comparabilidad"]["causa"],
            "delta_b_menos_a": d.get("delta"), "magnitud_absoluta": d.get("magnitud_absoluta"),
            "unidad": d.get("unidad"), "puntos_porcentuales": d.get("puntos_porcentuales"),
            "cambio_relativo": d.get("cambio_relativo"),
            "estado_relativo": d.get("estado_relativo"),
            "representacion": p["representacion"]["estado"],
            "modo_representacion": p["representacion"].get("modo"),
            "materialidad": p["materialidad"]["estado"],
            "criterio_materialidad": json.dumps(
                p["materialidad"].get("criterio"), ensure_ascii=False, sort_keys=True),
            "resultado": p["resultado"],
        })
    return salida.getvalue()


def _fmt(valor: Any) -> str:
    if valor is None:
        return "NO-APLICA"
    if isinstance(valor, float):
        return repr(valor)
    return str(valor)


def como_humano(informe: dict) -> str:
    t = informe["totales"]
    lineas = [
        "# Informe de delta explicito", "",
        f"Entrada: `{informe['entrada']}` (`{informe['entrada_sha256']}`).", "",
        (f"Pares examinados: **{t['pares_examinados']}** · comparables: "
         f"**{t['comparables']}** · incompatibles: **{t['incompatibles']}** · "
         f"comparabilidad no determinable: **{t['comparabilidad_no_determinable']}**."),
        (f"Deltas calculados: **{t['deltas_calculados']}** · materiales: "
         f"**{t['materiales']}** · materialidad no determinable: "
         f"**{t['materialidad_no_determinable']}**."), "",
        informe["lectura_global"], "",
    ]
    for p in informe["pares"]:
        a, b, d = p["referencias"]["a"], p["referencias"]["b"], p["diferencia"]
        lineas.extend([
            f"## {p['id']}", "",
            f"Consumidor/uso: `{p['consumidor']}` — {p['uso']['descripcion']}.", "",
            f"- A: `{_fmt(a.get('valor'))}` ({a.get('clase_referencia')}; {a.get('estado')}).",
            f"- B: `{_fmt(b.get('valor'))}` ({b.get('clase_referencia')}; {b.get('estado')}).",
            f"- Referencias: **{p['reproducibilidad_referencias']}**.",
            (f"- Comparabilidad: **{p['comparabilidad']['estado']}** — "
             f"{p['comparabilidad']['causa']}.") ,
            (f"- Diferencia B−A: **{_fmt(d.get('delta'))}** {d.get('unidad') or ''}; "
             f"magnitud `{_fmt(d.get('magnitud_absoluta'))}`; "
             f"pp `{_fmt(d.get('puntos_porcentuales'))}`; cambio relativo "
             f"`{_fmt(d.get('cambio_relativo'))}` ({d.get('estado_relativo')})."),
            (f"- Representacion: **{p['representacion']['estado']}**"
             f"{(' — ' + str(p['representacion'].get('modo'))) if p['representacion'].get('modo') else ''}."),
            (f"- Materialidad: **{p['materialidad']['estado']}** — "
             f"{p['materialidad']['razon']}.") ,
            f"- Resultado: **{p['resultado']}**.", "",
        ])
        if a.get("estado") != "RESUELTA":
            lineas.append(f"  Causa A: {a.get('razon')}")
        if b.get("estado") != "RESUELTA":
            lineas.append(f"  Causa B: {b.get('razon')}")
        if a.get("estado") != "RESUELTA" or b.get("estado") != "RESUELTA":
            lineas.append("")
    return "\n".join(lineas).rstrip() + "\n"


def _escribe_atomico(ruta: Path, contenido: str) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fd, temporal = tempfile.mkstemp(prefix=f".{ruta.name}.", dir=ruta.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(contenido)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(temporal, ruta)
    except Exception:
        try:
            os.unlink(temporal)
        except FileNotFoundError:
            pass
        raise


def escribe_salidas(informe: dict, salida_dir: Path, canon) -> list[str]:
    salida_dir = salida_dir.resolve()
    try:
        salida_dir.relative_to(canon.RAIZ.resolve())
    except ValueError as exc:
        raise ErrorContrato("salida-dir debe vivir dentro del repositorio") from exc
    artefactos = {
        "delta.json": json.dumps(informe, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        "delta.tsv": como_tsv(informe),
        "delta.md": como_humano(informe),
    }
    for nombre, contenido in artefactos.items():
        _escribe_atomico(salida_dir / nombre, contenido)
    return [str((salida_dir / n).relative_to(canon.RAIZ.resolve())) for n in artefactos]


def ejecuta_cli(args, canon) -> int:
    try:
        informe = ejecuta(Path(args.entrada), canon)
        if getattr(args, "salida_dir", None):
            artefactos = escribe_salidas(informe, Path(args.salida_dir), canon)
            print("ESCRITO: " + " · ".join(artefactos))
        formato = getattr(args, "formato", "humano")
        if formato == "json":
            print(json.dumps(informe, ensure_ascii=False, indent=2, sort_keys=True))
        elif formato == "tsv":
            print(como_tsv(informe), end="")
        else:
            print(como_humano(informe), end="")
    except ErrorContrato as exc:
        print(f"PETICION-INVALIDA · {exc}", file=sys.stderr)
        return 2
    return 1 if informe["totales"]["referencias_no_resueltas"] else 0
