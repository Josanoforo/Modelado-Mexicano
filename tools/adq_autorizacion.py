#!/usr/bin/env python3
"""Contrato común de autorización para objetos de adquisición.

La autorización vigente puede vivir en la metadata JSON de un residual o en
la historia legacy. La metadata estructurada gana sobre prosa histórica: una
marca vieja ``SONDA-LATERAL-RECOMENDADA`` no revoca un mandato posterior.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from dataclasses import dataclass

MARCADOR = "RESIDUAL-ADQ-V1="
_TOKEN_INDIVIDUAL = re.compile(
    r"AUTORIZADA:(?P<quien>[^/\s]+)/(?P<fecha>\d{4}-\d{2}-\d{2})/(?P<objeto>[^/\s]+)"
)
_TOKEN_ALCANCE = re.compile(
    r"AUTORIZADA-POR-ALCANCE:(?P<quien>[^/\s]+)/(?P<fecha>\d{4}-\d{2}-\d{2})/"
    r"(?P<acto>[A-Z0-9_.-]+)/(?P<objeto>[^/\s]+)"
)
_NEGACION = re.compile(r"\bNO[-\s]+AUTORIZAD[AO]S?\b", re.IGNORECASE)


@dataclass(frozen=True)
class Autorizacion:
    autorizada: bool
    razon: str
    token: str | None = None
    modalidad: str | None = None


def _bloques(nota: str) -> tuple[dict, str]:
    """Separa la metadata residual de la historia; nunca mezcla sus reglas."""
    meta: dict = {}
    historia: list[str] = []
    for parte in (nota or "").split(" || "):
        if parte.startswith(MARCADOR):
            try:
                valor = json.loads(parte[len(MARCADOR):])
            except json.JSONDecodeError:
                historia.append(parte)
            else:
                if isinstance(valor, dict):
                    meta = valor
                else:
                    historia.append(parte)
        else:
            historia.append(parte)
    return meta, " || ".join(historia)


def _evalua_texto(texto: str, objeto: str, corte: dt.date) -> Autorizacion:
    if not texto:
        return Autorizacion(False, "autorización ausente")
    if _NEGACION.search(texto):
        return Autorizacion(False, "negación explícita de autorización")

    hallazgos: list[tuple[str, re.Match[str]]] = []
    hallazgos.extend(("individual", m) for m in _TOKEN_INDIVIDUAL.finditer(texto))
    hallazgos.extend(("alcance", m) for m in _TOKEN_ALCANCE.finditer(texto))
    if not hallazgos:
        if "AUTORIZADA:" in texto or "AUTORIZADA-POR-ALCANCE:" in texto:
            return Autorizacion(False, "token de autorización mal formado")
        return Autorizacion(False, "autorización afirmativa ausente")

    validos: list[tuple[str, re.Match[str], dt.date]] = []
    errores: list[str] = []
    for modalidad, match in hallazgos:
        try:
            fecha = dt.date.fromisoformat(match.group("fecha"))
        except ValueError:
            errores.append("fecha inválida")
            continue
        if match.group("objeto") != objeto:
            errores.append("objeto distinto")
            continue
        validos.append((modalidad, match, fecha))
    if not validos:
        return Autorizacion(False, "; ".join(sorted(set(errores))) or "token no aplicable")

    identidades = {
        (m.group("quien"), m.group("fecha"), modalidad,
         m.groupdict().get("acto", ""), m.group("objeto"))
        for modalidad, m, _fecha in validos
    }
    if len(identidades) != 1:
        return Autorizacion(False, "autorización ambigua: múltiples tokens vigentes")
    modalidad, match, _fecha = validos[0]
    return Autorizacion(True, f"autorización {modalidad} válida para {objeto}",
                        match.group(0), modalidad)


def evalua_autorizacion(nota: str, objeto: str,
                        corte: dt.date | None = None) -> Autorizacion:
    """Evalúa metadata primero y usa historia sólo como compatibilidad legacy."""
    corte = corte or dt.date.today()
    meta, historia = _bloques(nota)
    autoridad = str(meta.get("autoridad", "")).strip()
    if autoridad:
        return _evalua_texto(autoridad, objeto, corte)
    return _evalua_texto(historia, objeto, corte)


def esta_autorizada(nota: str, objeto: str, corte: dt.date | None = None) -> bool:
    return evalua_autorizacion(nota, objeto, corte).autorizada
