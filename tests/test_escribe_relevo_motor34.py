#!/usr/bin/env python3
"""Escritor V3 (ACTO GEN2-RELEVO-MOTOR-34-1): una prueba por llave y las guardas de 4.1."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import escribe_relevo_consumo as E  # noqa: E402
from milpa.src.emisor import cargar_reglas  # noqa: E402


@pytest.fixture(scope="module")
def ctx():
    return E._ctx_corridas()


@pytest.fixture(scope="module")
def reglas():
    return {r["id"]: r for r in E._yaml_load(E.TARGET)["reglas"]}


@pytest.mark.parametrize("relevo", E.RELEVOS_V3, ids=lambda r: f"{r[0]}:{r[1]}")
def test_llave_pasa_guardas_y_el_motor_materializa_el_result(relevo, ctx, reglas):
    valor = E.guardas_v3(relevo, ctx, reglas)
    regla_id, conducta, _calc, result, _via = relevo
    salida = next(s for s in {r.id: r for r in cargar_reglas(E.TARGET)}[regla_id].entonces
                  if s.conducta == conducta)
    assert salida.resultado_id == result
    assert f"{salida.p:.6f}" == f"{valor:.6f}"


def test_transform_es_idempotente():
    fuente = E.TARGET.read_text(encoding="utf-8")
    for relevo in E.RELEVOS_V3:
        valor = next(s.p for s in {r.id: r for r in cargar_reglas(E.TARGET)}[relevo[0]].entonces
                     if s.conducta == relevo[1])
        assert E.transform_v3(fuente, relevo, valor) == fuente


def _texto_sin_cita(relevo) -> tuple[str, str]:
    """Texto sintético mínimo con la conducta sin cita, en forma flujo."""
    regla_id, conducta, *_ = relevo
    return (f"reglas:\n  - id: {regla_id}\n    entonces:\n"
            f"      - {{conducta: {conducta}, p: 0.500000, clase: \"X\"}}\n"), regla_id


def test_via_iii_no_cambia_p():
    relevo = next(r for r in E.RELEVOS_V3 if r[4] == E.VIA_III)
    texto, _ = _texto_sin_cita(relevo)
    with pytest.raises(ValueError, match="no cambia p"):
        E.transform_v3(texto, relevo, 0.25)


def test_via_i_escribe_p_igual_al_result():
    relevo = next(r for r in E.RELEVOS_V3 if r[4] == E.VIA_I)
    texto, _ = _texto_sin_cita(relevo)
    nuevo = E.transform_v3(texto, relevo, 0.1234567)
    assert f"p: 0.123457, corrida0_resultado_id: {relevo[3]}, corrida0_generacion: GEN2," in nuevo


def test_cita_previa_distinta_rechazo_atomico():
    relevo = E.RELEVOS_V3[0]
    texto, _ = _texto_sin_cita(relevo)
    texto = texto.replace("clase:", "corrida0_resultado_id: RESULT-OTRO, clase:")
    with pytest.raises(ValueError, match="rechazo atómico"):
        E.transform_v3(texto, relevo, 0.5)


def test_replay_no_afirmativo_se_rechaza(ctx, reglas):
    relevo = E.RELEVOS_V3[0]
    malo = copy.deepcopy(ctx)
    malo[relevo[2]]["resultado_replay"] = "NO-REPRODUCE"
    with pytest.raises(ValueError, match="no afirmativo"):
        E.guardas_v3(relevo, malo, reglas)


def test_cuenta_gen2_distinta_de_si_se_rechaza(ctx, reglas):
    relevo = E.RELEVOS_V3[-1]
    malo = copy.deepcopy(ctx)
    malo[relevo[2]]["cuenta_gen2"] = "PENDIENTE-DE-MESA"
    with pytest.raises(ValueError, match="cuenta_gen2"):
        E.guardas_v3(relevo, malo, reglas)


def test_via_i_payload_distinto_se_rechaza(ctx, reglas):
    relevo = next(r for r in E.RELEVOS_V3 if r[4] == E.VIA_I)
    malas = copy.deepcopy(reglas)
    malas[relevo[0]]["payload_manifiesto_id"] = "otro_payload"
    with pytest.raises(ValueError, match="mismo payload"):
        E.guardas_v3(relevo, ctx, malas)


def test_via_iii_consumidor_no_declarado_por_la_spec_se_rechaza(ctx, reglas):
    regla_id, conducta, calc, result, via = next(r for r in E.RELEVOS_V3 if r[4] == E.VIA_III)
    with pytest.raises(ValueError, match="no declara"):
        E.guardas_v3((regla_id, "otra_conducta", calc, result, via), ctx, reglas)
