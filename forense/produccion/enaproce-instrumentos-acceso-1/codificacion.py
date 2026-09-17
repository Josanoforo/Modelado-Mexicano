#!/usr/bin/env python3
"""Codificación sintética del contrato ENAPROCE; no lee microdatos.

La entrada es deliberadamente normalizada. En particular, ``problem_codes``
representa los códigos seleccionados en la pregunta de problemas: uno en 2015
y hasta tres en 2018. El futuro lector del archivo real deberá resolver la
forma física de P81_6 y los faltantes usando el FD oficial antes de invocar
esta función.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite
from typing import Iterable


PROCEDURE_CODES_2015 = frozenset({1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13})
PROCEDURE_CODES_2018 = PROCEDURE_CODES_2015 | {19}
PROBLEM_CODES_2015_MICRO = frozenset({1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15})
PROBLEM_CODES_2015_PYME = frozenset({1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16})
PROBLEM_CODES_2018 = frozenset({1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16, 19})


@dataclass(frozen=True)
class Classification:
    wave: int
    instrument: str
    exceso_tramites_problem: bool | None
    named_procedure_obstacle: bool | None
    fiscal_compliance_cost: float | None
    monthly_procedure_hours: float | None
    burden_observed: bool
    corruption_outcome_observed: bool
    eligible_for_current_r03: bool


def _nonnegative_or_none(value: object, field: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field}: se requiere número o null")
    number = float(value)
    if not isfinite(number) or number < 0:
        raise ValueError(f"{field}: se requiere número finito no negativo")
    return number


def classify_record(
    *,
    wave: int,
    instrument: str,
    problem_codes: Iterable[int] | None,
    procedure_code: int | None,
    fiscal_compliance_cost: object,
    monthly_procedure_hours: object,
) -> dict[str, object]:
    """Clasifica un registro sintético bajo reglas documentadas.

    ``instrument`` es ``micro`` o ``pyme``. ``None`` significa faltante: nunca
    se transforma en cero ni en una respuesta negativa.
    """

    if wave not in {2015, 2018}:
        raise ValueError("wave: sólo 2015 o 2018")
    if instrument not in {"micro", "pyme"}:
        raise ValueError("instrument: sólo micro o pyme")

    codes = None if problem_codes is None else tuple(problem_codes)
    if codes is not None:
        allowed = (
            PROBLEM_CODES_2018
            if wave == 2018
            else PROBLEM_CODES_2015_MICRO
            if instrument == "micro"
            else PROBLEM_CODES_2015_PYME
        )
        max_codes = 3 if wave == 2018 else 1
        if not codes or len(codes) > max_codes or len(set(codes)) != len(codes):
            raise ValueError("problem_codes: longitud/repetición incompatible con la ola")
        invalid = set(codes) - allowed
        if invalid:
            raise ValueError(f"problem_codes no documentados: {sorted(invalid)}")
        if wave == 2018 and 16 in codes and len(codes) != 1:
            raise ValueError("problem_codes: 'sin problemas' no admite otra selección")

    allowed_procedures = PROCEDURE_CODES_2018 if wave == 2018 else PROCEDURE_CODES_2015
    if procedure_code is not None and procedure_code not in allowed_procedures:
        raise ValueError(f"procedure_code no documentado: {procedure_code}")

    cost = _nonnegative_or_none(fiscal_compliance_cost, "fiscal_compliance_cost")
    hours = _nonnegative_or_none(monthly_procedure_hours, "monthly_procedure_hours")
    problem = None if codes is None else 6 in codes
    named_obstacle = None if procedure_code is None else procedure_code != 13

    result = Classification(
        wave=wave,
        instrument=instrument,
        exceso_tramites_problem=problem,
        named_procedure_obstacle=named_obstacle,
        fiscal_compliance_cost=cost,
        monthly_procedure_hours=hours,
        burden_observed=cost is not None or hours is not None,
        # El instrumento revisado no contiene este desenlace.
        corruption_outcome_observed=False,
        eligible_for_current_r03=False,
    )
    return asdict(result)
