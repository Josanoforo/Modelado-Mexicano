#!/usr/bin/env python3
"""Construye el snapshot reproducible del emisor GEN2 explícito.

No resuelve linaje: consume las vistas derivadas por ``tools/corrida0.py`` y
el contrato compartido de ``milpa.src.linaje``. El snapshot no es un sello ni
una adopción científica; registra qué salidas ya adoptadas pueden emitir y por
qué las restantes fallan cerradas.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from dataclasses import asdict
from datetime import date
from pathlib import Path

import yaml

from milpa.src.emisor import (
    MODO_GEN2,
    MODO_HISTORICO,
    RAIZ,
    cargar_indice_linaje_emision,
    cargar_reglas,
    emitir_binaria_contrato,
)
from tools.baseline_temporal import (
    Objetivo,
    Observacion,
    Serie,
    seleccionar_transferencia,
)
from tools.emite_m import cita_ola_calibracion


VERSION = "GEN2-MOTOR-EXPLICITO-v1.2"
RUTA_SNAPSHOT = (
    RAIZ / "forense" / "prereg-duelo-v2" /
    "snapshot-M-gen2-explicito-v1_2.json"
)
RUTA_SPEC_B = RAIZ / "data" / "corrida0" / "CALC-B-0001" / "spec.yaml"
RUTA_RESULTADOS_B = (
    RAIZ / "data" / "corrida0" / "CALC-B-0001" / "resultados.json"
)


def _sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def _hash_conjunto(rutas: list[Path]) -> dict:
    archivos = {str(r.relative_to(RAIZ)): _sha256(r) for r in rutas}
    canon = "".join(f"{k}\t{v}\n" for k, v in sorted(archivos.items()))
    return {
        "sha256": hashlib.sha256(canon.encode("utf-8")).hexdigest(),
        "archivos": archivos,
    }


def _familia(regla_id: str) -> str:
    raiz = regla_id.split(".", 1)[0]
    return {
        "civico": "CIV",
        "tramite": "TRA",
        "familia": "FAM",
        "dinero": "DIN",
    }.get(raiz, raiz.upper())


def _partes_consumidor(consumidor: str) -> tuple[str, str]:
    partes = consumidor.split(":", 2)
    if len(partes) != 3 or partes[0] != "milpa/tramite.yaml":
        raise ValueError(f"consumidor de trámite no reconocido: {consumidor}")
    return partes[1], partes[2]


def _universo_conducta(regla: dict, conducta: str, dominio: dict) -> str:
    candidatos = []
    for valor in regla.values():
        if not isinstance(valor, dict):
            continue
        if conducta in (valor.get("aplica_a") or []) and valor.get("universo"):
            candidatos.append(str(valor["universo"]))
    if len(set(candidatos)) > 1:
        raise ValueError(
            f"{regla['id']}/{conducta}: universos ambiguos en enmiendas")
    if candidatos:
        return candidatos[0]
    if regla.get("universo"):
        return str(regla["universo"])
    if dominio:
        return "dominio elegible explícito: " + json.dumps(
            dominio, ensure_ascii=False, sort_keys=True)
    return "NO-DECLARADO-EN-REGLA; consultar unidad del RESULT"


def _salida_cruda(regla: dict, conducta: str) -> dict:
    salidas = [e for e in regla.get("entonces", [])
               if e.get("conducta") == conducta]
    if len(salidas) != 1:
        raise ValueError(
            f"{regla['id']}/{conducta}: se esperaba una salida exacta")
    return salidas[0]


def _ola(regla_id: str, conducta: str, lineas: list[str]) -> dict:
    valor, cita = cita_ola_calibracion(regla_id, conducta, lineas)
    return {"valor": valor, "cita": cita}


def _seleccion_enigh_operativa(indice, regla) -> dict:
    spec = yaml.safe_load(RUTA_SPEC_B.read_text(encoding="utf-8"))
    resultados_doc = json.loads(RUTA_RESULTADOS_B.read_text(encoding="utf-8"))
    resultados = resultados_doc["resultados"]
    parametros = spec["parametros"]
    serie = Serie(**parametros["serie"])
    objetivo_anio = 2022
    objetivo = Objetivo(
        serie=serie,
        periodo_inicio=date(objetivo_anio, 1, 1),
        periodo_fin=date(objetivo_anio, 12, 31),
        fecha_corte=date(objetivo_anio - 1, 12, 31),
    )
    historial = []
    for ficha in parametros["olas"]:
        anio = int(ficha["ola"])
        if anio == objetivo_anio:
            continue
        resultado_id = f"RESULT-B-ENIGH-{anio}-P"
        historial.append(Observacion(
            serie=serie,
            periodo_inicio=date(anio, 1, 1),
            periodo_fin=date(anio, 12, 31),
            disponible_desde=date.fromisoformat(str(ficha["modified"])),
            publicada=True,
            p=resultados[resultado_id],
            resultado_id=resultado_id,
            fuente=ficha["payload_id"],
        ))
    seleccion = seleccionar_transferencia(
        objetivo,
        historial,
        estimando=str(spec["estimando"]),
        transformacion=str(spec["transformacion"]),
    )
    if seleccion["estado"] != "EMITE":
        raise AssertionError(f"transferencia ENIGH dejó de emitir: {seleccion}")
    salida = emitir_binaria_contrato(
        regla,
        "recibe_remesas",
        {},
        modo=MODO_GEN2,
        proposito="transferencia",
        uso_solicitado="MEDICION-GEN2",
        indice=indice,
        seleccion_transferencia=seleccion,
    )
    return {
        "familia": "FAM",
        "consumidor": (
            "milpa/tramite.yaml:familia.seguro."
            "volatilidad_ausencia_estado:recibe_remesas"
        ),
        "objetivo": "ENIGH-NS 2022",
        "fecha_corte": "2021-12-31",
        "serie_exacta": asdict(serie),
        "selector": seleccion,
        "rol_seleccionado": salida.rol_seleccion,
        "evaluacion": "NO-EVALUACION-INDEPENDIENTE",
        "emision": asdict(salida),
    }


def construir_snapshot() -> dict:
    indice = cargar_indice_linaje_emision()
    reglas = {r.id: r for r in cargar_reglas()}
    tramite = yaml.safe_load(
        (RAIZ / "milpa" / "tramite.yaml").read_text(encoding="utf-8"))
    reglas_crudas = {r["id"]: r for r in tramite["reglas"]}
    lineas_tramite = (
        RAIZ / "milpa" / "tramite.yaml").read_text(encoding="utf-8").splitlines()

    antes_familia = Counter()
    antes_generacion_global = Counter(
        "GEN2-DIRECTO" if uso.corrida0_generacion == "GEN2" else "LEGACY"
        for uso in indice.usos.values())
    antes_generacion_motor = Counter()
    for consumidor, uso in indice.usos.items():
        if not consumidor.startswith("milpa/tramite.yaml:"):
            continue
        regla_id, _ = _partes_consumidor(consumidor)
        antes_familia[_familia(regla_id)] += 1
        antes_generacion_motor[
            "GEN2-DIRECTO" if uso.corrida0_generacion == "GEN2" else "LEGACY"
        ] += 1

    salidas = []
    despues_familia = Counter()
    estados = Counter()
    for consumidor, uso in sorted(indice.usos.items()):
        if (not consumidor.startswith("milpa/tramite.yaml:")
                or uso.corrida0_generacion != "GEN2"):
            continue
        regla_id, conducta = _partes_consumidor(consumidor)
        regla = reglas[regla_id]
        regla_cruda = reglas_crudas[regla_id]
        salida_cruda = _salida_cruda(regla_cruda, conducta)
        dominio = dict(salida_cruda.get("dominio_elegible") or {})
        rol = str(salida_cruda.get("rol_uso") or "medicion_directa")
        uso_solicitado = (
            "DESCRIPTIVO" if rol == "proxy_descriptivo" else "MEDICION-GEN2")
        emision = emitir_binaria_contrato(
            regla, conducta, dominio, modo=MODO_GEN2, proposito="consulta",
            uso_solicitado=uso_solicitado, indice=indice)
        evidencia = indice.resultados[uso.corrida0_resultado_id]
        familia = _familia(regla_id)
        estados[emision.estado] += 1
        if emision.estado == "EMITE":
            despues_familia[familia] += 1
        salidas.append({
            "consumidor": consumidor,
            "familia": familia,
            "parametro_regla": f"{regla_id}:{conducta}",
            "resultado_id": evidencia.resultado_id,
            "valor_resultado_completo": evidencia.valor,
            "tipo": evidencia.tipo,
            "unidad": evidencia.unidad,
            "evento": salida_cruda.get("evento") or f"conducta={conducta}",
            "universo": _universo_conducta(regla_cruda, conducta, dominio),
            "ola": _ola(regla_id, conducta, lineas_tramite),
            "transformacion": salida_cruda.get("evento") or conducta,
            "uso_permitido": uso_solicitado,
            "rol_uso": rol,
            "condicion_activacion": {
                "regla": dict(regla.condiciones()),
                "dominio_resultado": dominio,
            },
            "estado": emision.estado,
            "origen_numerico": emision.origen_numerico,
            "aptitud_uso": emision.aptitud_uso,
            "camino_linaje": emision.camino_linaje,
            "fuente_replay": evidencia.fuente_replay,
            "validacion_independiente": evidencia.validacion_independiente,
            "dependencias_estructurales": list(
                emision.dependencias_estructurales),
            "alcance": salida_cruda.get("uso_motor") or "uso declarado por RESULT",
        })

    # Complemento adoptado previamente: deriva del padre y no aumenta el
    # contador de mediciones GEN2 directas.
    regla_encuci = reglas["tramite.mordida.discrecional"]
    complemento_encuci = next(
        s for s in regla_encuci.entonces
        if s.conducta == "sin_solicitud_y_sin_entrega_encuci2020")
    emision_complemento = emitir_binaria_contrato(
        regla_encuci, complemento_encuci.conducta,
        dict(complemento_encuci.dominio_elegible), modo=MODO_GEN2,
        proposito="consulta", uso_solicitado="MEDICION-GEN2", indice=indice)

    # La propuesta ENVIPE se documenta pero permanece fuera hasta firma.
    regla_envipe = reglas["civico.denuncia.miedo_desconfianza"]
    complemento_envipe = next(
        s for s in regla_envipe.entonces
        if s.conducta == "denuncia_por_otra_razon")
    emision_envipe = emitir_binaria_contrato(
        regla_envipe, complemento_envipe.conducta,
        dict(complemento_envipe.dominio_elegible), modo=MODO_GEN2,
        proposito="consulta", uso_solicitado="MEDICION-GEN2", indice=indice)

    regla_historica = reglas["tramite.mordida.discrecional"]
    historica = emitir_binaria_contrato(
        regla_historica, "paga_mordida", {}, modo=MODO_HISTORICO,
        proposito="baseline", uso_solicitado="BASELINE", indice=indice)

    rutas_motor = [
        RAIZ / "milpa" / "src" / "emisor.py",
        RAIZ / "milpa" / "src" / "linaje.py",
        RAIZ / "tools" / "baseline_temporal.py",
    ]
    rutas_contrato = [
        RAIZ / "milpa" / "tramite.yaml",
        RAIZ / "data" / "corrida0" / "usos.tsv",
        RAIZ / "data" / "corrida0" / "resultados.tsv",
        RUTA_SPEC_B,
        RAIZ / "data" / "corrida0" / "CALC-B-0001" / "ejecucion.json",
        RUTA_RESULTADOS_B,
    ]
    return {
        "schema_version": "1.2",
        "sucesion": {
            "reemplaza": (
                "forense/prereg-duelo-v2/"
                "snapshot-M-gen2-explicito-v1_1.json"),
            "motivo": (
                "incorpora el overlay independiente de los 16 parámetros "
                "activos sin reescribir el snapshot v1.1"),
            "consumidores": [
                "tools/snapshot_motor_gen2.py",
                "tests/test_motor_gen2_explicito.py",
            ],
        },
        "fecha_corte": "2026-09-11",
        "modo": MODO_GEN2,
        "naturaleza": (
            "snapshot reproducible de consumo; no sello CALC ni firma científica"),
        "motor": {"version": VERSION, **_hash_conjunto(rutas_motor)},
        "contrato_consumido": _hash_conjunto(rutas_contrato),
        "cobertura": {
            "antes": {
                "registro_activo_total": len(indice.usos),
                "registro_por_generacion": dict(
                    sorted(antes_generacion_global.items())),
                "alcance_emisor_tramite": {
                    "consumidores_activos": sum(antes_generacion_motor.values()),
                    "por_generacion": dict(
                        sorted(antes_generacion_motor.items())),
                    "por_familia": dict(sorted(antes_familia.items())),
                },
            },
            "despues_modo_gen2_explicito": {
                "consumidores_directos_evaluados": len(salidas),
                "por_estado": dict(sorted(estados.items())),
                "emiten_por_familia": dict(sorted(despues_familia.items())),
                "criterio": (
                    "enlace directo GEN2 + origen apto + RESULT sellado + "
                    "dominio/uso compatibles; conteos re-derivados, no congelados"),
            },
        },
        "salidas_gen2_directas": salidas,
        "complemento_dependiente_adoptado": {
            "consumidor": (
                "milpa/tramite.yaml:tramite.mordida.discrecional:"
                "sin_solicitud_y_sin_entrega_encuci2020"),
            "cuenta_como_medicion_independiente": False,
            "emision": asdict(emision_complemento),
        },
        "complemento_envipe_pendiente_de_firma": {
            "consumidor": (
                "milpa/tramite.yaml:civico.denuncia.miedo_desconfianza:"
                "denuncia_por_otra_razon"),
            "contrato": (
                "complemento del padre a nivel persona bajo U1/U4; no es "
                "categoría 09 ni 'alguna otra razón'"),
            "cuenta_como_medicion_independiente": False,
            "emision": asdict(emision_envipe),
        },
        "transferencia_temporal_operativa": _seleccion_enigh_operativa(
            indice, reglas["familia.seguro.volatilidad_ausencia_estado"]),
        "baseline_historico_identificado": {
            "consumidor": (
                "milpa/tramite.yaml:tramite.mordida.discrecional:paga_mordida"),
            "emision": asdict(historica),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verifica", type=Path,
        help="compara el snapshot re-derivado contra este archivo")
    parser.add_argument(
        "--actualiza", action="store_true",
        help=f"regenera el artefacto versionado {RUTA_SNAPSHOT.relative_to(RAIZ)}")
    args = parser.parse_args()
    # Normaliza tuplas de dataclasses a la representación JSON que se vuelve
    # a leer del archivo; así ``--verifica`` compara estructura, no tipos de
    # contenedor propios de Python.
    actual = json.loads(json.dumps(construir_snapshot(), ensure_ascii=False))
    if args.actualiza:
        RUTA_SNAPSHOT.write_text(
            json.dumps(actual, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n", encoding="utf-8")
        print(f"OK snapshot actualizado: {RUTA_SNAPSHOT}")
        return 0
    if args.verifica:
        esperado = json.loads(args.verifica.read_text(encoding="utf-8"))
        if actual != esperado:
            raise SystemExit(f"snapshot desactualizado: {args.verifica}")
        print(f"OK snapshot reproducible: {args.verifica}")
        return 0
    print(json.dumps(actual, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
