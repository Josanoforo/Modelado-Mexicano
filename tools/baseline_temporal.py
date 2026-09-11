#!/usr/bin/env python3
"""Selector B para proporciones: última ola disponible antes del objetivo.

Sucesor optativo de corredor-B-tasa-base.py; no modifica el script sellado.
La función es cálculo puro: el consumidor debe suministrar valores y metadatos
verificados. No autentica RESULT, no sella CALC, no adopta parámetros y no lee
las series GEN1. En GEN2 se llama desde un medidor sobre su snapshot declarado.

Uso exploratorio: python3 tools/baseline_temporal.py entrada.json
El JSON contiene `objetivo` e `historial`, con los campos de las dataclasses.
Fechas ISO YYYY-MM-DD; `disponible_desde` corresponde a la versión del insumo
utilizada, no necesariamente a su primera publicación ni a la ejecución CALC.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Serie:
    encuesta: str
    reactivo: str
    universo: str
    codificacion: str
    segmento: str
    unidad: str  # esta versión admite exclusivamente "proporcion"

    def __post_init__(self):
        for nombre, valor in vars(self).items():
            if (not isinstance(valor, str) or not valor.strip()
                    or valor.strip().upper() in {"PENDIENTE", "NO-DEFINIDO"}):
                raise ValueError(f"serie.{nombre} debe estar definido")
        if self.unidad != "proporcion":
            raise ValueError("B requiere proporciones [0,1], no porcentajes")


def _intervalo(inicio: date, fin: date) -> None:
    if type(inicio) is not date or type(fin) is not date or inicio > fin:
        raise ValueError("periodo inválido: requiere fechas ordenadas")


@dataclass(frozen=True)
class Objetivo:
    serie: Serie
    periodo_inicio: date
    periodo_fin: date
    fecha_corte: date

    def __post_init__(self):
        _intervalo(self.periodo_inicio, self.periodo_fin)
        if type(self.serie) is not Serie:
            raise ValueError("objetivo.serie debe ser Serie")
        if type(self.fecha_corte) is not date or self.fecha_corte > self.periodo_inicio:
            raise ValueError("el corte debe ser anterior o igual al inicio del objetivo")


@dataclass(frozen=True)
class Observacion:
    serie: Serie
    periodo_inicio: date
    periodo_fin: date
    disponible_desde: date | None
    publicada: bool
    p: float | None
    resultado_id: str
    fuente: str

    def __post_init__(self):
        _intervalo(self.periodo_inicio, self.periodo_fin)
        if type(self.serie) is not Serie:
            raise ValueError("observacion.serie debe ser Serie")
        if self.disponible_desde is not None:
            if (type(self.disponible_desde) is not date
                    or self.disponible_desde < self.periodo_fin):
                raise ValueError("disponible_desde debe identificar una versión posterior al cierre de la ola")
        if type(self.publicada) is not bool:
            raise ValueError("publicada debe declararse como booleano")
        if self.p is not None and (type(self.p) not in (int, float)
                or not math.isfinite(self.p) or not 0 <= self.p <= 1):
            raise ValueError("p debe ser finita en [0,1] o null")
        if any(not isinstance(v, str) or not v.strip()
               for v in (self.resultado_id, self.fuente)):
            raise ValueError("cada observación requiere resultado_id y fuente")


def seleccionar_baseline(objetivo: Objetivo, historial: list[Observacion]) -> dict:
    """No usa R objetivo ni ajusta tendencia. No infiere equivalencias.

    Conserva la precedencia del B sellado: pública previa; en su ausencia,
    persistencia de una medición previa disponible; en su ausencia, abstención.
    Igualar `Serie` exige igual población, reactivo, codificación, segmento y
    escala. Un crosswalk entre instrumentos tiene que resolverse antes y estar
    documentado por el consumidor: este selector no lo decide por semejanza.
    """
    elegibles, excluidas = [], []
    for obs in historial:
        motivo = None
        if obs.serie != objetivo.serie:
            motivo = "OTRA_SERIE"
        elif obs.periodo_fin >= objetivo.periodo_inicio:
            motivo = "OLA_NO_ANTERIOR"
        elif obs.disponible_desde is None:
            motivo = "DISPONIBILIDAD_NO_DOCUMENTADA"
        elif obs.disponible_desde > objetivo.fecha_corte:
            motivo = "NO_DISPONIBLE_AL_CORTE"
        elif obs.p is None:
            motivo = "VALOR_NO_ESTIMABLE"
        if motivo:
            excluidas.append({"resultado_id": obs.resultado_id, "motivo": motivo})
        else:
            elegibles.append(obs)

    publicas = [obs for obs in elegibles if obs.publicada]
    candidatas = publicas or elegibles
    if not candidatas:
        return {"estado": "SIN_BASELINE", "metodo": "SIN_BASELINE", "p": None,
                "resultado_id": None, "fuente": None, "excluidas": excluidas}

    ultimo_fin = max(obs.periodo_fin for obs in candidatas)
    ultimas = [obs for obs in candidatas if obs.periodo_fin == ultimo_fin]
    if len(ultimas) != 1:
        raise ValueError("baseline ambiguo: más de una observación en la última ola elegible")
    seleccionada = ultimas[0]
    return {
        "estado": "EMITE",
        "metodo": "ultima_ola_publica" if publicas else "persistencia",
        "p": seleccionada.p,
        "resultado_id": seleccionada.resultado_id,
        "fuente": seleccionada.fuente,
        "periodo_inicio": seleccionada.periodo_inicio.isoformat(),
        "periodo_fin": seleccionada.periodo_fin.isoformat(),
        "disponible_desde": seleccionada.disponible_desde.isoformat(),
        "excluidas": excluidas,
    }


def seleccionar_transferencia(
        objetivo: Objetivo,
        historial: list[Observacion],
        *,
        estimando: str,
        transformacion: str,
) -> dict:
    """Envuelve la selección temporal en un contrato transportable.

    El selector comprueba identidad exacta de serie, precedencia, disponibilidad
    y unicidad, igual que :func:`seleccionar_baseline`. Además conserva en una
    sola estructura los metadatos que el emisor necesita volver a contrastar
    contra evidencia sellada. No adjudica compatibilidad científica ni rol
    experimental: esas dos decisiones se derivan en el emisor desde la spec y
    el registro, no desde una etiqueta aportada por el llamador.
    """
    for nombre, valor in {
        "estimando": estimando,
        "transformacion": transformacion,
    }.items():
        if (not isinstance(valor, str) or not valor.strip()
                or valor.strip().upper() in {"PENDIENTE", "NO-DEFINIDO"}):
            raise ValueError(f"{nombre} debe estar definido")

    base = seleccionar_baseline(objetivo, historial)
    por_id = {obs.resultado_id: obs for obs in historial}
    if len(por_id) != len(historial):
        raise ValueError("resultado_id duplicado en historial de transferencia")
    elegida = (por_id.get(base["resultado_id"])
               if base["resultado_id"] is not None else None)

    return {
        **base,
        "contrato_version": "SELECCION-TEMPORAL-v1",
        "objetivo": {
            "serie": asdict(objetivo.serie),
            "estimando": estimando,
            "transformacion": transformacion,
            "periodo": {
                "inicio": objetivo.periodo_inicio.isoformat(),
                "fin": objetivo.periodo_fin.isoformat(),
            },
            "corte_temporal": objetivo.fecha_corte.isoformat(),
        },
        "seleccion": None if elegida is None else {
            "serie": asdict(elegida.serie),
            "periodo": {
                "inicio": elegida.periodo_inicio.isoformat(),
                "fin": elegida.periodo_fin.isoformat(),
            },
            "disponibilidad": elegida.disponible_desde.isoformat(),
            "evidencia_procedencia": {
                "resultado_id": elegida.resultado_id,
                "fuente": elegida.fuente,
                "valor": elegida.p,
            },
        },
    }


def desde_documento(doc: dict) -> dict:
    """Adaptador JSON para CLI o bytes del snapshot recibido por un medidor."""
    def campos(registro):
        r = dict(registro)
        r["serie"] = Serie(**r["serie"])
        for campo in ("periodo_inicio", "periodo_fin", "fecha_corte", "disponible_desde"):
            if campo in r and r[campo] is not None:
                r[campo] = date.fromisoformat(r[campo])
        return r
    objetivo = Objetivo(**campos(doc["objetivo"]))
    historial = [Observacion(**campos(r)) for r in doc["historial"]]
    return seleccionar_baseline(objetivo, historial)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path)
    args = parser.parse_args()
    try:
        salida = desde_documento(json.loads(args.entrada.read_text(encoding="utf-8")))
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.exit(2, f"entrada inválida: {exc}\n")
    print(json.dumps(salida, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
