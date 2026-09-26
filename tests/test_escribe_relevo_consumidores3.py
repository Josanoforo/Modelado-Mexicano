#!/usr/bin/env python3
"""Escritor V6 (ACTO GEN2-RELEVO-CONSUMIDORES-3, FIRMAS-18 H1/H2/H3): una
prueba por llave -- 8 coeficientes HISTÓRICO-SIN-RELEVO, 1 probabilidad
citada, 11 conservadas con rótulo, 4 momentos HISTÓRICO, M04 acotado -- más
la salida del contador por firma (H3 por tipo_uso), idempotencia y rechazos
atómicos."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import corrida0 as C  # noqa: E402
import escribe_relevo_consumo as E  # noqa: E402


@pytest.fixture(scope="module")
def ctx():
    return E._ctx_corridas()


@pytest.fixture(scope="module")
def marcados():
    return C._consumidores_historico_sin_relevo()


@pytest.fixture(scope="module")
def proc():
    return E._yaml_load(E.PROCEDENCIA)


@pytest.mark.parametrize("par", E.H1_COEFICIENTES, ids=lambda p: f"{p[0]}.{p[1]}")
def test_h1_coeficiente_historico(par, proc, marcados):
    gen, coef = par
    d = next(d for d in proc["asignados_coeficiente"]["detalle"] if d["gen"] == gen)
    assert d["historico_sin_relevo"][coef].startswith(E.HISTORICO)
    assert "H1 (FIRMAS-18" in d["historico_sin_relevo"][coef]
    assert coef in d["coefs"]  # el valor no cambia: sigue en `coefs`
    assert f"milpa/procedencia.yaml:asignados_coeficiente:{gen}.{coef}" in marcados


def test_h1_solo_los_ocho(proc):
    marcados_yaml = {(d["gen"], c) for d in proc["asignados_coeficiente"]["detalle"]
                     for c in (d.get("historico_sin_relevo") or {})}
    assert marcados_yaml == set(E.H1_COEFICIENTES)
    # los sellados (G1, G3.horizonte_temporal, ...) no se marcan
    sellados = {(e["gen"], e["coef"]) for e in proc["coeficientes_generador_sellados"]}
    assert not marcados_yaml & sellados


@pytest.mark.parametrize("cita", E.H1_CITA, ids=lambda c: c[0])
def test_h1_probabilidad_citada(cita, proc, ctx):
    regla, r_p, r_q = cita
    e = {x["regla"]: x for x in proc["asignados_probabilidad"]}[regla]
    consumidor = f"milpa/procedencia.yaml:asignados_probabilidad:{regla}"
    p = E.guardas_v4(consumidor, E._calc_de_result(r_p), r_p, ctx)
    q = E.guarda_complemento_v6(consumidor, r_q, ctx)
    assert [f"{v:.6f}" for v in e["valores"]] == [f"{p:.6f}", f"{q:.6f}"]
    assert e["corrida0_resultado_id"] == r_p and e["corrida0_generacion"] == "GEN2"
    marca = C._ids_corrida0_declarados()[consumidor]
    assert marca["generacion"] == "GEN2" and marca["resultado_id"] == r_p


@pytest.mark.parametrize("cons", E.H1_CONSERVA, ids=lambda c: c[0])
def test_h1_probabilidad_conservada_sigue_legacy(cons, proc, marcados):
    regla, _razon = cons
    e = {x["regla"]: x for x in proc["asignados_probabilidad"]}[regla]
    assert e["rotulo_relevo"].startswith(E.ROTULO_H1)
    assert "corrida0_resultado_id" not in e
    assert f"milpa/procedencia.yaml:asignados_probabilidad:{regla}" not in marcados


def test_h1_doce_probabilidades_cubiertas():
    assert len(E.H1_CITA) + len(E.H1_CONSERVA) == 12


@pytest.mark.parametrize("m", [m for m, _ in E.H2_HISTORICO])
def test_h2_momento_historico(m, marcados):
    assert f"milpa/catalogo-momentos-v0_1.tsv:{m}" in marcados
    marca = C._marcas_catalogo(E.CATALOGO).get(f"milpa/catalogo-momentos-v0_1.tsv:{m}")
    assert marca is None  # sin valor ni cita: no es relevo


@pytest.mark.parametrize("acota", E.H2_ACOTA, ids=lambda a: a[0])
def test_h2_momento_acotado(acota, ctx, marcados):
    m, result, disc = acota
    valor = E.guardas_v4(f"x:{m}", E._calc_de_result(result), result, ctx)
    marca = C._marcas_catalogo(E.CATALOGO)[f"milpa/catalogo-momentos-v0_1.tsv:{m}"]
    assert marca["resultado_id"] == result and marca["generacion"] == "GEN2"
    assert marca["valor"] == valor and marca["discrepancia_gen1"] == disc
    assert f"milpa/catalogo-momentos-v0_1.tsv:{m}" not in marcados


def test_h2_residuo_sin_tocar(marcados):
    for m in ("M03", "M05", "M23"):
        assert f"milpa/catalogo-momentos-v0_1.tsv:{m}" not in marcados


def test_h3_por_tipo_uso():
    base = C.PREFIJO_MARCO_H3
    assert C._es_historico_sin_relevo({"consumidor": base + "X:L:L-solo", "tipo_uso": "celda_L"}, set())
    assert C._es_historico_sin_relevo({"consumidor": base + "X:AGREGADO", "tipo_uso": "celda_AGREGADO"}, set())
    assert not C._es_historico_sin_relevo({"consumidor": base + "X:M", "tipo_uso": "celda_M"}, set())
    assert not C._es_historico_sin_relevo({"consumidor": base + "X:R", "tipo_uso": "celda_R"}, set())


def test_status_suma_y_desglose():
    s = C.status(imprime=False)
    assert s["legacy_fuera_del_contador_por_firma__historico_sin_relevo"] == (
        len(E.H1_COEFICIENTES) + len(E.H2_HISTORICO) + 42)
    assert s["legacy_activas_por_consumidor__marco_del_duelo"] == 1
    assert s["dependencias_numericas_legacy_activas"] == sum(
        v for k, v in s.items() if k.startswith("legacy_activas_por_consumidor__"))


def test_v6_idempotente(ctx):
    for ruta, fn in ((E.PROCEDENCIA, E.transform_procedencia_v6),
                     (E.CATALOGO, E.transform_catalogo_v6)):
        fuente = ruta.read_text(encoding="utf-8")
        assert fn(fuente, ctx) == fuente


def test_v6_rechaza_marca_distinta(ctx):
    fuente = E.PROCEDENCIA.read_text(encoding="utf-8").replace(
        "valor conservado, no cuenta como deuda", "otra cosa", 1)
    with pytest.raises(ValueError, match="rechazo atómico"):
        E.transform_procedencia_v6(fuente, ctx)


def test_v6_rechaza_momento_con_relevo_distinto(ctx):
    fuente = E.CATALOGO.read_text(encoding="utf-8").replace(
        "NO-EQUIVALENTE-PAGO (ENCIG P8_3", "OTRO (ENCIG P8_3", 1)
    with pytest.raises(ValueError, match="rechazo atómico"):
        E.transform_catalogo_v6(fuente, ctx)
