#!/usr/bin/env python3
"""Consulta operativa del emisor GEN2 con contrato explícito.

La ruta normal sólo consume ``emitir_binaria_contrato``: no genera snapshots,
no reimplementa el motor y no usa el valor histórico como fallback. Una
transferencia debe transportar el objeto ``seleccion`` completo producido por
``SELECCION-TEMPORAL-v1``; el emisor lo reproduce contra evidencia sellada.

Ejemplos:

  python3 tools/consulta_gen2.py --lista-consumidores
  python3 tools/consulta_gen2.py \
    --consumidor 'milpa/tramite.yaml:familia.seguro.volatilidad_ausencia_estado:recibe_remesas' \
    --proposito consulta --contexto-json '{}' --uso MEDICION-GEN2 --json
  python3 tools/consulta_gen2.py --peticion peticion.json --json
  python3 tools/consulta_gen2.py --lote peticiones.json --json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path
from typing import Any

import yaml

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from milpa.src.emisor import (  # noqa: E402
    MODO_GEN2,
    PrediccionM,
    cargar_indice_linaje_emision,
    cargar_reglas,
    emitir_binaria_contrato,
)
from tools.snapshot_motor_gen2 import (  # noqa: E402
    _familia,
    _ola,
    _salida_cruda,
    _universo_conducta,
)
from tools import adq_suficiencia  # noqa: E402


VERSION_CONTRATO = "CONSULTA-GEN2-v1"
RUTA_TRAMITE = RAIZ / "milpa" / "tramite.yaml"
RUTAS_CONTRATO = (
    Path("tools/consulta_gen2.py"),
    Path("tools/adq_suficiencia.py"),
    Path("tools/adq_investigacion.py"),
    Path("tools/snapshot_motor_gen2.py"),
    Path("tools/emite_m.py"),
    Path("tools/baseline_temporal.py"),
    Path("milpa/src/emisor.py"),
    Path("milpa/src/linaje.py"),
    Path("milpa/tramite.yaml"),
    Path("data/corrida0/usos.tsv"),
    Path("data/corrida0/resultados.tsv"),
    Path("data/adq-investigacion.yaml"),
)
CLAVES_PETICION = {
    "id", "consumidor", "proposito", "contexto", "uso", "seleccion",
}


def _hash_contrato() -> dict[str, Any]:
    archivos = {
        str(ruta): hashlib.sha256((RAIZ / ruta).read_bytes()).hexdigest()
        for ruta in RUTAS_CONTRATO
    }
    canon = "".join(f"{ruta}\t{sha}\n" for ruta, sha in sorted(archivos.items()))
    return {
        "version": VERSION_CONTRATO,
        "sha256": hashlib.sha256(canon.encode("utf-8")).hexdigest(),
        "archivos": archivos,
    }


def _partes_consumidor(consumidor: object) -> tuple[str, str]:
    if not isinstance(consumidor, str):
        raise ValueError("consumidor debe ser una identidad textual exacta")
    partes = consumidor.split(":", 2)
    if len(partes) != 3 or partes[0] != "milpa/tramite.yaml":
        raise ValueError(
            "identidad de consumidor inválida; se espera "
            "milpa/tramite.yaml:<regla>:<conducta>")
    if not partes[1] or not partes[2]:
        raise ValueError("identidad de consumidor incompleta")
    return partes[1], partes[2]


def _documento_tramite() -> tuple[dict[str, dict], list[str]]:
    texto = RUTA_TRAMITE.read_text(encoding="utf-8")
    doc = yaml.safe_load(texto)
    return {r["id"]: r for r in doc["reglas"]}, texto.splitlines()


def _salida_regla(regla, conducta: str):
    candidatas = [s for s in regla.entonces if s.conducta == conducta]
    if len(candidatas) != 1:
        raise ValueError(
            f"el consumidor no identifica una salida única: "
            f"{regla.id}:{conducta}")
    return candidatas[0]


def _resumen_peticion(peticion: object) -> object:
    """Conserva identidad y corte sin reimprimir números no autenticados."""
    if not isinstance(peticion, Mapping):
        return {"tipo_recibido": type(peticion).__name__}
    resumen = {
        k: peticion[k]
        for k in ("id", "consumidor", "proposito", "contexto", "uso")
        if k in peticion
    }
    extras = sorted(set(peticion) - CLAVES_PETICION)
    if extras:
        resumen["campos_adicionales"] = extras
    seleccion = peticion.get("seleccion")
    if isinstance(seleccion, Mapping):
        objetivo = seleccion.get("objetivo")
        elegida = seleccion.get("seleccion")
        evidencia = (
            elegida.get("evidencia_procedencia")
            if isinstance(elegida, Mapping) else None)
        resumen["seleccion"] = {
            "contrato_version": seleccion.get("contrato_version"),
            "estado": seleccion.get("estado"),
            "metodo": seleccion.get("metodo"),
            "objetivo": {
                "serie": objetivo.get("serie"),
                "periodo": objetivo.get("periodo"),
                "corte_temporal": objetivo.get("corte_temporal"),
            } if isinstance(objetivo, Mapping) else None,
            "observacion": {
                "serie": elegida.get("serie"),
                "periodo": elegida.get("periodo"),
                "disponibilidad": elegida.get("disponibilidad"),
                "resultado_id": (
                    evidencia.get("resultado_id")
                    if isinstance(evidencia, Mapping) else None),
                "fuente": (
                    evidencia.get("fuente")
                    if isinstance(evidencia, Mapping) else None),
            } if isinstance(elegida, Mapping) else None,
        }
    elif "seleccion" in peticion:
        resumen["seleccion"] = {"tipo_recibido": type(seleccion).__name__}
    return resumen


def _no_coverage(peticion: object, motivo: str) -> dict[str, Any]:
    return {
        "contrato": _hash_contrato(),
        "peticion": _resumen_peticion(peticion),
        "estado": "NO_COVERAGE",
        "motivo_no_cobertura": motivo,
        "resultado": {"id": None, "fuente": None},
        "referencias": [str(r) for r in RUTAS_CONTRATO],
    }


def _metadatos_resultado(indice, prediccion: PrediccionM) -> tuple[dict, list[str]]:
    evidencia = indice.resultados.get(prediccion.resultado_id or "")
    if evidencia is None:
        return {"id": prediccion.resultado_id, "fuente": None}, []
    referencias = [
        "data/corrida0/resultados.tsv",
        "data/corrida0/usos.tsv",
    ]
    if evidencia.spec_id:
        base = Path("data/corrida0") / evidencia.spec_id
        for nombre in ("spec.yaml", "ejecucion.json", "resultados.json"):
            if (RAIZ / base / nombre).is_file():
                referencias.append(str(base / nombre))
    return {
        "id": evidencia.resultado_id,
        "fuente": evidencia.fuente_replay or None,
        "corrida_id": evidencia.corrida_id or None,
        "spec_id": evidencia.spec_id or None,
        "tipo": evidencia.tipo or None,
        "unidad": evidencia.unidad or None,
        "generacion": evidencia.generacion or None,
        "origen_numerico": evidencia.origen_numerico or None,
    }, referencias


def _periodo(prediccion: PrediccionM, seleccion: object,
             regla_id: str, conducta: str, lineas: list[str]) -> object:
    if prediccion.proposito == "transferencia" and isinstance(seleccion, Mapping):
        elegida = seleccion.get("seleccion")
        objetivo = seleccion.get("objetivo")
        return {
            "seleccion": elegida.get("periodo") if isinstance(elegida, Mapping) else None,
            "objetivo": objetivo.get("periodo") if isinstance(objetivo, Mapping) else None,
            "corte_temporal": (
                objetivo.get("corte_temporal")
                if isinstance(objetivo, Mapping) else None),
        }
    try:
        return _ola(regla_id, conducta, lineas)
    except (KeyError, LookupError, ValueError):
        return {"valor": None, "cita": None}


def _advertencia(tipo: object, unidad: object) -> str:
    texto = f"{tipo or ''} {unidad or ''}".lower()
    if "proporcion" in texto or "[0,1]" in texto:
        return (
            "Proporción poblacional del universo declarado; no es diagnóstico "
            "ni probabilidad personalizada validada.")
    return "Interpretar sólo dentro del universo, evento, periodo y uso declarados."


def consultar(peticion: object) -> dict[str, Any]:
    """Resuelve una petición y conserva ``NO_COVERAGE`` como salida normal."""
    if not isinstance(peticion, Mapping):
        return _no_coverage(peticion, "la petición debe ser un objeto JSON")
    peticion = dict(peticion)
    extras = sorted(set(peticion) - CLAVES_PETICION)
    if extras:
        return _no_coverage(
            peticion,
            "campos no permitidos en la petición: " + ", ".join(extras))
    faltan = [k for k in ("consumidor", "proposito", "contexto", "uso")
              if k not in peticion]
    if faltan:
        return _no_coverage(
            peticion, "faltan campos explícitos: " + ", ".join(faltan))
    if not isinstance(peticion["contexto"], Mapping):
        return _no_coverage(peticion, "contexto debe ser un objeto JSON explícito")

    proposito = str(peticion["proposito"] or "").strip().lower()
    if proposito not in {"consulta", "transferencia"}:
        return _no_coverage(
            peticion, "propósito debe ser 'consulta' o 'transferencia'")
    uso = str(peticion["uso"] or "").strip()
    if not uso:
        return _no_coverage(peticion, "uso debe declararse explícitamente")
    seleccion = peticion.get("seleccion")
    if proposito == "transferencia" and not isinstance(seleccion, Mapping):
        return _no_coverage(
            peticion,
            "transferencia exige seleccion estructurada con objetivo, corte y evidencia")

    try:
        regla_id, conducta = _partes_consumidor(peticion["consumidor"])
    except ValueError as exc:
        return _no_coverage(peticion, str(exc))

    reglas = {r.id: r for r in cargar_reglas()}
    regla = reglas.get(regla_id)
    if regla is None:
        return _no_coverage(peticion, f"regla desconocida: {regla_id}")
    try:
        salida = _salida_regla(regla, conducta)
    except ValueError as exc:
        return _no_coverage(peticion, str(exc))

    indice = cargar_indice_linaje_emision()
    prediccion = emitir_binaria_contrato(
        regla,
        conducta,
        dict(peticion["contexto"]),
        modo=MODO_GEN2,
        proposito=proposito,
        uso_solicitado=uso,
        indice=indice,
        seleccion_transferencia=seleccion,
    )

    # La aptitud de linaje acredita procedencia y replay, no que el reactivo
    # responda la necesidad científica. La proyección enlaza sólo
    # incompatibilidades concretas ya asentadas y falla cerrado antes de
    # exponer el valor.
    try:
        suficiencia_uso = adq_suficiencia.proyecta_consumidor(
            str(peticion["consumidor"]))
    except (KeyError, ValueError) as exc:
        return _no_coverage(
            peticion, f"guardia de suficiencia no resoluble: {exc}")
    if (suficiencia_uso and
            suficiencia_uso["accion_consumidor"] ==
            "NO_EMITIR_RESULTADO_SOLICITADO"):
        prediccion = replace(
            prediccion,
            estado="NO_COVERAGE",
            valor_punto=None,
            detalle=(
                f"{suficiencia_uso['necesidad_id']}: evidencia incompatible "
                f"con el uso solicitado; {suficiencia_uso['brecha']}"),
        )

    campos_desconocidos = sorted(
        set(peticion["contexto"]) - set(dict(salida.dominio_elegible)))
    if campos_desconocidos:
        prediccion = replace(
            prediccion,
            estado="NO_COVERAGE",
            valor_punto=None,
            detalle=(
                "campos de dominio desconocidos para el consumidor: "
                + ", ".join(campos_desconocidos)),
        )

    reglas_crudas, lineas = _documento_tramite()
    regla_cruda = reglas_crudas[regla_id]
    salida_cruda = _salida_cruda(regla_cruda, conducta)
    dominio = dict(salida.dominio_elegible)
    resultado, referencias_resultado = _metadatos_resultado(indice, prediccion)
    transformacion = (
        f"1-p({salida.complemento_de})"
        if salida.complemento_de else
        (salida_cruda.get("evento") or conducta))
    respuesta: dict[str, Any] = {
        "contrato": _hash_contrato(),
        "peticion": _resumen_peticion(peticion),
        "estado": prediccion.estado,
        "resultado": resultado,
        "estimando": {
            "poblacion": _universo_conducta(regla_cruda, conducta, dominio),
            "unidad": resultado.get("unidad"),
            "evento": salida_cruda.get("evento") or f"conducta={conducta}",
            "periodo": _periodo(
                prediccion, seleccion, regla_id, conducta, lineas),
            "transformacion": transformacion,
        },
        "dependencia": {
            "padre": salida.complemento_de,
            "estructurales": list(prediccion.dependencias_estructurales),
            "camino_linaje": prediccion.camino_linaje,
            "rol_seleccion": prediccion.rol_seleccion,
        },
        "aptitud": {
            "estado": prediccion.aptitud_uso,
            "validacion_independiente": (
                indice.resultados.get(prediccion.resultado_id or "").validacion_independiente
                if prediccion.resultado_id in indice.resultados else None),
            "rol_uso": salida.rol_uso,
            "uso_solicitado": prediccion.uso_solicitado,
            "alcance": salida.uso_motor or "uso declarado por RESULT",
        },
        "dominio": {
            "requerido": dominio,
            "recibido": dict(peticion["contexto"]),
        },
        "advertencia_interpretacion": _advertencia(
            resultado.get("tipo"), resultado.get("unidad")),
        "referencias": sorted(set(
            [str(r) for r in RUTAS_CONTRATO] + referencias_resultado)),
    }
    if suficiencia_uso:
        respuesta["suficiencia_uso"] = suficiencia_uso
    if prediccion.estado == "EMITE":
        respuesta["valor"] = {
            "punto": prediccion.valor_punto,
            "tipo_escala": prediccion.tipo_escala,
            "categoria": prediccion.valor_categoria,
        }
    else:
        respuesta["motivo_no_cobertura"] = prediccion.detalle
    return respuesta


def listar_consumidores() -> list[dict[str, Any]]:
    indice = cargar_indice_linaje_emision()
    reglas = {r.id: r for r in cargar_reglas()}
    filas = []
    for consumidor, uso in sorted(indice.usos.items()):
        if not consumidor.startswith("milpa/tramite.yaml:"):
            continue
        try:
            regla_id, conducta = _partes_consumidor(consumidor)
            salida = _salida_regla(reglas[regla_id], conducta)
        except (KeyError, ValueError):
            continue
        filas.append({
            "consumidor": consumidor,
            "familia": _familia(regla_id),
            "generacion": uso.corrida0_generacion,
            "resultado_id": uso.corrida0_resultado_id or None,
            "campos_dominio": dict(salida.dominio_elegible),
            "rol_uso": salida.rol_uso,
            "uso_registrado": uso.uso_solicitado or None,
        })
    return filas


def _leer_json(ruta: Path) -> object:
    return json.loads(ruta.read_text(encoding="utf-8"))


def _imprimir_humano(respuesta: dict[str, Any]) -> None:
    print(f"estado: {respuesta['estado']}")
    print(f"consumidor: {respuesta.get('peticion', {}).get('consumidor', '-')}")
    resultado = respuesta.get("resultado", {})
    print(f"RESULT: {resultado.get('id') or '-'}")
    print(f"fuente: {resultado.get('fuente') or '-'}")
    if "valor" in respuesta:
        print(f"valor: {respuesta['valor']['punto']}")
    else:
        print(f"motivo: {respuesta.get('motivo_no_cobertura', '-')}")
    if "estimando" in respuesta:
        print(f"población: {respuesta['estimando']['poblacion']}")
        print(f"unidad: {respuesta['estimando']['unidad']}")
        print(f"evento: {respuesta['estimando']['evento']}")
        print(f"periodo: {json.dumps(respuesta['estimando']['periodo'], ensure_ascii=False)}")
        print(f"transformación: {respuesta['estimando']['transformacion']}")
        print(f"aptitud: {respuesta['aptitud']['estado']}")
        print(f"validación independiente: {respuesta['aptitud']['validacion_independiente']}")
        print(f"alcance: {respuesta['aptitud']['alcance']}")
        print(f"límite: {respuesta['advertencia_interpretacion']}")
    print(
        f"contrato: {respuesta['contrato']['version']} "
        f"sha256={respuesta['contrato']['sha256']}")


def _json_cli(valor: str, etiqueta: str) -> object:
    try:
        if valor.startswith("@"):
            return _leer_json(Path(valor[1:]))
        return json.loads(valor)
    except (json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"{etiqueta} no es JSON válido: {exc}") from exc


def _peticion_banderas(args: argparse.Namespace) -> dict[str, Any] | None:
    valores = (args.consumidor, args.proposito, args.contexto_json, args.uso,
               args.seleccion_json)
    if not any(v is not None for v in valores):
        return None
    faltan = [nombre for nombre, valor in {
        "--consumidor": args.consumidor,
        "--proposito": args.proposito,
        "--contexto-json": args.contexto_json,
        "--uso": args.uso,
    }.items() if valor is None]
    if faltan:
        raise ValueError("faltan banderas: " + ", ".join(faltan))
    peticion = {
        "consumidor": args.consumidor,
        "proposito": args.proposito,
        "contexto": _json_cli(args.contexto_json, "--contexto-json"),
        "uso": args.uso,
    }
    if args.seleccion_json is not None:
        peticion["seleccion"] = _json_cli(
            args.seleccion_json, "--seleccion-json")
    return peticion


def _escribir_sin_sobrescribir(ruta: Path, contenido: str,
                               sobrescribir: bool) -> None:
    if ruta.exists() and not sobrescribir:
        raise FileExistsError(
            f"el destino ya existe: {ruta}; usa --sobrescribir explícitamente")
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Consulta GEN2 por identidad exacta con dominio, uso y propósito explícitos.",
        epilog=(
            "Transferencia: --seleccion-json debe contener SELECCION-TEMPORAL-v1 "
            "con objetivo, corte, observación y evidencia; el motor la reautentica."))
    entrada = parser.add_mutually_exclusive_group()
    entrada.add_argument("--peticion", type=Path, help="objeto JSON de petición")
    entrada.add_argument("--lote", type=Path, help="arreglo JSON de peticiones")
    entrada.add_argument(
        "--lista-consumidores", action="store_true",
        help="lista identidades exactas y valores requeridos del dominio")
    parser.add_argument("--consumidor")
    parser.add_argument("--proposito", choices=("consulta", "transferencia"))
    parser.add_argument(
        "--contexto-json",
        help="objeto JSON explícito o @archivo; usa '{}' si el dominio es vacío")
    parser.add_argument("--uso", help="p. ej. MEDICION-GEN2 o DESCRIPTIVO")
    parser.add_argument(
        "--seleccion-json",
        help="SELECCION-TEMPORAL-v1 como JSON o @archivo")
    parser.add_argument("--json", action="store_true", help="salida JSON")
    parser.add_argument("--salida", type=Path, help="destino propio para un lote")
    parser.add_argument(
        "--sobrescribir", action="store_true",
        help="autoriza reemplazar --salida; nunca modifica snapshots")
    parser.add_argument(
        "--verifica", type=Path,
        help="con --lote, compara respuestas reproducidas contra este JSON")
    args = parser.parse_args()

    try:
        directa = _peticion_banderas(args)
        if args.lista_consumidores:
            if directa is not None:
                parser.error("--lista-consumidores no admite banderas de petición")
            filas = listar_consumidores()
            if args.json:
                print(json.dumps(filas, ensure_ascii=False, indent=2, allow_nan=False))
            else:
                for fila in filas:
                    print(
                        f"{fila['consumidor']}\n"
                        f"  generación={fila['generacion']} "
                        f"uso={fila['uso_registrado'] or '-'} "
                        f"dominio={json.dumps(fila['campos_dominio'], ensure_ascii=False)}")
            return 0

        if args.lote:
            if directa is not None:
                parser.error("--lote no admite banderas de petición")
            peticiones = _leer_json(args.lote)
            if not isinstance(peticiones, list):
                raise ValueError("--lote debe contener un arreglo JSON")
            respuestas = [consultar(p) for p in peticiones]
            texto = json.dumps(
                respuestas, ensure_ascii=False, indent=2, sort_keys=True,
                allow_nan=False) + "\n"
            if args.verifica:
                esperadas = _leer_json(args.verifica)
                if respuestas != esperadas:
                    print(f"FALLA respuestas distintas: {args.verifica}", file=sys.stderr)
                    return 1
                print(f"OK respuestas reproducibles: {args.verifica}")
                return 0
            if args.salida:
                _escribir_sin_sobrescribir(
                    args.salida, texto, args.sobrescribir)
                print(f"OK respuestas: {args.salida}")
            else:
                print(texto, end="")
            return 0

        if args.peticion:
            if directa is not None:
                parser.error("--peticion no admite banderas de petición")
            peticion = _leer_json(args.peticion)
        elif directa is not None:
            peticion = directa
        else:
            parser.error(
                "indica --peticion, --lote, --lista-consumidores o las banderas de petición")

        respuesta = consultar(peticion)
        if args.salida or args.verifica or args.sobrescribir:
            parser.error("--salida/--verifica/--sobrescribir sólo aplican a --lote")
        if args.json:
            print(json.dumps(
                respuesta, ensure_ascii=False, indent=2, sort_keys=True,
                allow_nan=False))
        else:
            _imprimir_humano(respuesta)
        return 0
    except (FileExistsError, OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"entrada inválida: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
