#!/usr/bin/env python3
"""Guardia de uso: expone cobertura por dimensión sin fabricar un puntaje."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from tools import adq_investigacion
except ImportError:  # ejecución directa: python3 tools/adq_suficiencia.py
    import adq_investigacion

RAIZ = Path(__file__).resolve().parent.parent


def _sha256(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def _path_evidencia(raiz: Path, referencia: str) -> Path:
    return raiz / referencia.split("#", 1)[0]


def _integridad_evidencias(raiz: Path, evidencias: list[str]) -> dict[str, str | None]:
    return {ref: _sha256(_path_evidencia(raiz, ref)) for ref in evidencias}


def _accion_reportada(suficiencia: dict) -> str:
    try:
        return {
            "APTA_USO_DECLARADO": "PUEDE_EMITIR_USO_DECLARADO",
            "APTA_ALCANCE_MENOR": "SOLO_EMITIR_ALCANCE_MENOR_ROTULADO",
            "INCOMPATIBLE": "NO_EMITIR_RESULTADO_SOLICITADO",
        }[suficiencia["uso_habilitado"]]
    except KeyError as exc:
        raise ValueError("suficiencia sin uso_habilitado reconocido") from exc


def _evalua_decision(estado: dict, contrato: dict, vinculo: dict,
                     consumidor: str, resultado_id: str | None,
                     uso_solicitado: str | None, raiz: Path, *,
                     alcance_menor: bool = False
                     ) -> tuple[bool, str, dict | None]:
    """Una suficiencia de investigación nunca equivale a adopción de emisión."""
    decision = estado.get("decision_emision")
    if not isinstance(decision, dict):
        return False, "sin decisión explícita de emisión aplicable", None

    esperados = {
        "necesidad_id": contrato["id"],
        "version_pregunta": contrato["version_pregunta"],
        "consumidor": consumidor,
        "resultado_id": resultado_id,
        "uso_aprobado": uso_solicitado,
    }
    if alcance_menor:
        esperados.update({
            "uso_menor": vinculo.get("uso_menor"),
            "uso_original": vinculo.get("uso_original"),
        })
    discrepantes = [
        clave for clave, esperado in esperados.items()
        if not esperado or decision.get(clave) != esperado
    ]
    if discrepantes:
        return (False,
                "decisión de emisión no aplicable a " + ", ".join(discrepantes),
                decision)

    evidencias = decision.get("evidencias")
    evidencias_estado = estado.get("evidencias") or []
    if (not isinstance(evidencias, list) or not evidencias or
            any(not isinstance(x, str) or not x.strip() for x in evidencias) or
            any(x not in evidencias_estado for x in evidencias)):
        return False, "decisión sin evidencia enlazada al estado", decision
    if any(_sha256(_path_evidencia(raiz, x)) is None for x in evidencias):
        return False, "decisión con evidencia no reproducible en el árbol", decision

    clase = decision.get("clase")
    bloqueado = vinculo["resultado_bloqueado_id"]
    if alcance_menor:
        if clase != "AUTORIZA_ALCANCE_MENOR_RESULTADO_EXISTENTE":
            return False, "decisión no autoriza el alcance menor exacto", decision
        if resultado_id != bloqueado:
            return False, "decisión de alcance menor no corresponde al RESULT", decision
    elif clase == "AUTORIZA_RESULTADO_EXISTENTE":
        if resultado_id != bloqueado:
            return False, "decisión para resultado existente no corresponde al RESULT", decision
    elif clase == "ADOPTA_SUCESOR_CALCULADO":
        if (resultado_id == bloqueado or decision.get("calculada") is not True or
                decision.get("adoptada") is not True):
            return False, "sucesor no está calculado y adoptado", decision
    else:
        return False, "clase de decisión de emisión no reconocida", decision
    return True, "decisión explícita y evidencia aplicables", decision


def proyecta(necesidad_id: str, cfg: dict | None = None,
             raiz: Path | None = None, *, consumidor: str | None = None,
             resultado_id: str | None = None,
             uso_solicitado: str | None = None) -> dict:
    raiz = raiz or RAIZ
    cfg = cfg or adq_investigacion.cargar_config()
    contratos = {x["id"]: x for x in cfg.get("necesidades", [])}
    if necesidad_id not in contratos:
        raise KeyError(f"{necesidad_id}: sin contrato operativo de suficiencia")
    contrato = contratos[necesidad_id]
    ruta_estado = Path(cfg["estado_dir"]) / f"{necesidad_id}.json"
    path_estado = raiz / ruta_estado
    estado_leido = adq_investigacion._lee_json(path_estado)
    estado_valido = bool(estado_leido) and all((
        estado_leido.get("necesidad_id") == necesidad_id,
        estado_leido.get("version_pregunta") == contrato["version_pregunta"],
    ))
    descarte = None
    if estado_leido and not estado_valido:
        descarte = "estado descartado: necesidad_id o version_pregunta no vigentes"
    estado = estado_leido if estado_valido else {}
    suficiencia = estado.get("suficiencia") or contrato.get("suficiencia_actual")
    if not suficiencia:
        suficiencia = {
            **{x: "NO_ACREDITADA" for x in ("identidad", "conceptual", "poblacional",
                                               "seleccion_no_respuesta", "unidad",
                                               "temporalidad", "diseno", "identificacion")},
            "uso_habilitado": "INCOMPATIBLE", "pregunta_original": "ABIERTA",
        }
    accion_reportada = _accion_reportada(suficiencia)
    accion = accion_reportada
    estado_efectivo = {
        "PUEDE_EMITIR_USO_DECLARADO": "PENDIENTE_VINCULO_Y_DECISION",
        "SOLO_EMITIR_ALCANCE_MENOR_ROTULADO": "LIMITADA_A_ALCANCE_MENOR",
        "NO_EMITIR_RESULTADO_SOLICITADO": "BLOQUEADA_POR_INCOMPATIBILIDAD",
    }[accion_reportada]
    motivo_bloqueo = contrato["brecha"]
    decision = None
    evidencias = sorted(set(
        contrato.get("evidencias_guardia", []) + estado.get("evidencias", [])))
    vinculos = contrato.get("vinculos_consulta", [])
    vinculo = next((x for x in vinculos if x.get("consumidor") == consumidor), None)
    vinculo_menor = None
    if consumidor is not None:
        if vinculo is None:
            accion = "NO_EMITIR_RESULTADO_SOLICITADO"
            estado_efectivo = "BLOQUEADA_SIN_VINCULO_RESULTADO_USO"
            motivo_bloqueo = "consumidor sin vínculo explícito a RESULT y uso"
        elif (accion_reportada != "SOLO_EMITIR_ALCANCE_MENOR_ROTULADO" and
              uso_solicitado != vinculo.get("uso_requerido")):
            accion = "NO_EMITIR_RESULTADO_SOLICITADO"
            estado_efectivo = "BLOQUEADA_USO_NO_APROBADO"
            motivo_bloqueo = "el uso solicitado no coincide con el vínculo aprobado"
        elif accion_reportada == "PUEDE_EMITIR_USO_DECLARADO":
            habilita, motivo, decision = _evalua_decision(
                estado, contrato, vinculo, consumidor, resultado_id,
                uso_solicitado, raiz)
            accion = ("PUEDE_EMITIR_USO_DECLARADO" if habilita else
                      "NO_EMITIR_RESULTADO_SOLICITADO")
            estado_efectivo = ("HABILITADA_POR_DECISION_APLICABLE" if habilita else
                               "BLOQUEADA_SIN_DECISION_APLICABLE")
            motivo_bloqueo = motivo
        elif accion_reportada == "NO_EMITIR_RESULTADO_SOLICITADO":
            estado_efectivo = "BLOQUEADA_POR_INCOMPATIBILIDAD"
        else:
            menores = contrato.get("vinculos_alcance_menor", [])
            vinculo_menor = next((x for x in menores if all((
                x.get("consumidor") == consumidor,
                x.get("resultado_bloqueado_id") == resultado_id,
                x.get("uso_menor") == uso_solicitado,
                x.get("uso_original") == vinculo.get("uso_requerido"),
            ))), None)
            if vinculo_menor is None:
                accion = "NO_EMITIR_RESULTADO_SOLICITADO"
                estado_efectivo = "BLOQUEADA_SIN_VINCULO_ALCANCE_MENOR"
                motivo_bloqueo = (
                    "la aptitud de alcance menor no enlaza explícitamente "
                    "RESULT, uso menor y uso original")
            else:
                habilita, motivo, decision = _evalua_decision(
                    estado, contrato, vinculo_menor, consumidor, resultado_id,
                    uso_solicitado, raiz, alcance_menor=True)
                accion = ("SOLO_EMITIR_ALCANCE_MENOR_ROTULADO" if habilita else
                          "NO_EMITIR_RESULTADO_SOLICITADO")
                estado_efectivo = (
                    "HABILITADA_POR_DECISION_DE_ALCANCE_MENOR_APLICABLE"
                    if habilita else "BLOQUEADA_SIN_DECISION_APLICABLE")
                motivo_bloqueo = motivo
    return {
        "necesidad_id": necesidad_id, "version_pregunta": contrato["version_pregunta"],
        "consumidor": contrato["consumidor"], "uso_solicitado": contrato["uso"],
        "accion_consumidor": accion, "suficiencia": suficiencia,
        "accion_reportada_investigacion": accion_reportada,
        "estado_efectivo": estado_efectivo,
        "motivo_bloqueo": motivo_bloqueo,
        "brecha": contrato["brecha"],
        "evidencias": evidencias,
        "integridad_evidencias": _integridad_evidencias(raiz, evidencias),
        "decision_emision": decision,
        "vinculo_evaluado": {
            "consumidor": consumidor,
            "resultado_id": resultado_id,
            "uso_solicitado": uso_solicitado,
            "resultado_bloqueado_id": (
                vinculo.get("resultado_bloqueado_id") if vinculo else None),
            "uso_requerido": vinculo.get("uso_requerido") if vinculo else None,
            "vinculo_alcance_menor": (
                vinculo_menor if accion_reportada ==
                "SOLO_EMITIR_ALCANCE_MENOR_ROTULADO" else None),
        } if consumidor is not None else None,
        "fuente_estado": (str(ruta_estado) if estado.get("suficiencia")
                          else "data/adq-investigacion.yaml"),
        "integridad_estado": {
            "ruta_observada": str(ruta_estado),
            "sha256_observado": _sha256(path_estado),
            "identidad_valida": estado_valido,
            "descarte": descarte,
        },
    }


def proyecta_consumidor(consumidor: str, cfg: dict | None = None,
                        raiz: Path | None = None, *,
                        resultado_id: str | None = None,
                        uso_solicitado: str | None = None) -> dict | None:
    """Devuelve la guardia declarada para una identidad exacta de consulta.

    La relación vive en la proyección operativa de necesidades, no en una
    heurística por nombre. Dos necesidades activas no pueden gobernar la misma
    emisión sin una decisión explícita: en ese caso se falla cerrado.
    """
    cfg = cfg or adq_investigacion.cargar_config()
    coincidencias = [
        x["id"] for x in cfg.get("necesidades", [])
        if consumidor in x.get("consumidores_consulta", [])
    ]
    if not coincidencias:
        return None
    if len(coincidencias) != 1:
        raise ValueError(
            f"{consumidor}: guardia de suficiencia ambigua: "
            + ", ".join(coincidencias))
    return proyecta(
        coincidencias[0], cfg, raiz, consumidor=consumidor,
        resultado_id=resultado_id, uso_solicitado=uso_solicitado)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--prepara-uso", metavar="NC_ID")
    ap.add_argument("--todas", action="store_true")
    args = ap.parse_args()
    cfg = adq_investigacion.cargar_config()
    if args.prepara_uso:
        print(json.dumps(proyecta(args.prepara_uso, cfg), ensure_ascii=False, indent=2))
        return 0
    if args.todas:
        print(json.dumps([proyecta(x["id"], cfg) for x in cfg["necesidades"]],
                         ensure_ascii=False, indent=2))
        return 0
    ap.error("elige --prepara-uso NC_ID o --todas")


if __name__ == "__main__":
    raise SystemExit(main())
