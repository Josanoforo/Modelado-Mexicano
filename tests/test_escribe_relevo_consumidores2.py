#!/usr/bin/env python3
"""Escritor V4 (ACTO GEN2-RELEVO-CONSUMIDORES-2): una prueba por llave
(procedencia `civico.denuncia.con_seguro`, catálogo `M08`), idempotencia,
rechazos atómicos y la lectura del registro bajo la llave de la demanda."""
from __future__ import annotations

import csv
import io
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


@pytest.mark.parametrize("relevo", E.RELEVOS_PROCEDENCIA_V4, ids=lambda r: r[0])
def test_procedencia_llave_materializa_result(relevo, ctx):
    regla, results = relevo
    consumidor = f"milpa/procedencia.yaml:asignados_probabilidad:{regla}"
    valores = [E.guardas_v4(consumidor, E.CALC_SEGURO, r, ctx) for r in results]
    entrada = {e["regla"]: e for e in
               E._yaml_load(E.PROCEDENCIA)["asignados_probabilidad"]}[regla]
    assert entrada["corrida0_resultado_id"] == results[0]
    assert entrada["corrida0_generacion"] == "GEN2"
    assert [f"{v:.6f}" for v in entrada["valores"]] == [f"{v:.6f}" for v in valores]
    # el registro la ve bajo la MISMA llave que escribe la demanda
    marca = C._ids_corrida0_declarados()[consumidor]
    assert marca["generacion"] == "GEN2" and marca["resultado_id"] == results[0]


@pytest.mark.parametrize("relevo", E.RELEVOS_CATALOGO_V4, ids=lambda r: r[0])
def test_catalogo_llave_materializa_result(relevo, ctx):
    momento, result, _disc = relevo
    valor = E.guardas_v4(f"milpa/catalogo-momentos-v0_1.tsv:{momento}",
                         E.CALC_SEGURO, result, ctx)
    marca = C._marcas_catalogo(E.CATALOGO)[f"milpa/catalogo-momentos-v0_1.tsv:{momento}"]
    assert marca["resultado_id"] == result and marca["generacion"] == "GEN2"
    assert marca["valor"] == valor


def test_catalogo_columnas_selladas_intactas():
    import subprocess  # noqa: PLC0415
    viejo = subprocess.run(
        ["git", "show", "e760e5bd:milpa/catalogo-momentos-v0_1.tsv"],
        cwd=ROOT, capture_output=True, text=True)
    if viejo.returncode != 0:
        pytest.skip("commit de 0-bis no disponible en este clon")
    nuevo = E.CATALOGO.read_text(encoding="utf-8").splitlines()
    for a, b in zip(viejo.stdout.splitlines(), nuevo, strict=True):
        assert b.startswith(a + "\t")


def test_v4_idempotente():
    for regla, results in E.RELEVOS_PROCEDENCIA_V4:
        fuente = E.PROCEDENCIA.read_text(encoding="utf-8")
        assert E.transform_procedencia_v4(fuente, regla, [0.5, 0.5], results[0]) == fuente
    fuente = E.CATALOGO.read_text(encoding="utf-8")
    fila = {c: v for c, v in next(
        f for f in csv.DictReader(io.StringIO(fuente), delimiter="\t")
        if f["id_momento"] == "M08").items() if c in E.COLUMNAS_CATALOGO_V4}
    assert E.transform_catalogo_v4(fuente, "M08", fila) == fuente


def test_procedencia_cita_distinta_rechazo_atomico():
    texto = ("asignados_probabilidad:\n  - regla: x.y\n    valores: [0.5, 0.5]\n"
             "    corrida0_resultado_id: RESULT-OTRO\n")
    with pytest.raises(ValueError, match="cita previa distinta"):
        E.transform_procedencia_v4(texto, "x.y", [0.4, 0.6], "RESULT-A")


def test_procedencia_cardinalidad_distinta_rechaza():
    texto = "asignados_probabilidad:\n  - regla: x.y\n    valores: [0.2, 0.3, 0.5]\n"
    with pytest.raises(ValueError, match="cardinalidad"):
        E.transform_procedencia_v4(texto, "x.y", [0.4, 0.6], "RESULT-A")


def test_catalogo_cita_distinta_rechazo_atomico():
    fuente = E.CATALOGO.read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="cita previa distinta"):
        E.transform_catalogo_v4(fuente, "M08", {"valor_gen2": "0.5"})


def test_guarda_rechaza_calc_que_ingiere(ctx):
    # la adjudicación GOB ingiere RESULT de otra corrida: vía (i) no pasa
    with pytest.raises(ValueError):
        E.guardas_v4("x", "CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001",
                     "RESULT-GOB-EXE15-ADJ-2025-B-BIS", ctx)


# ── V5 · FIRMAS-16 B1/B2 sobre milpa/tramite.yaml (ADENDA-1, P5) ───────────
from milpa.src import emisor  # noqa: E402

_REGLAS = {r.id: r for r in emisor.cargar_reglas(E.TARGET)}


@pytest.mark.parametrize("llave", E.B1_RETIRA, ids=lambda k: f"{k[0]}:{k[1]}")
def test_b1_retira_devuelve_par_gen2_del_hermano(llave):
    regla_id, asignado, hermano = llave
    a = emisor.emitir_binaria(_REGLAS[regla_id], asignado)
    h = emisor.emitir_binaria(_REGLAS[regla_id], hermano)
    assert a.valor_punto == h.valor_punto and a.resultado_id == h.resultado_id
    assert a.resultado_generacion == "GEN2" and a.clase != "ASIGNADO"


@pytest.mark.parametrize("llave", E.B1_CONSERVA, ids=lambda k: f"{k[0]}:{k[1]}")
def test_b1_conserva_asignado_con_rotulo(llave):
    regla_id, asignado, _razon = llave
    s = next(x for x in _REGLAS[regla_id].entonces if x.conducta == asignado)
    assert s.clase == "ASIGNADO" and s.resultado_id is None
    lineas = E.TARGET.read_text(encoding="utf-8").splitlines()
    i = E._ubica_conducta([l + "\n" for l in lineas], regla_id, asignado)
    if (regla_id, asignado) in E.CITADAS_POR_M_SELLADA:
        assert E.ROTULO_B1 in lineas[i - 1] and E.ROTULO_B1 not in lineas[i]
    else:
        assert E.ROTULO_B1 in (s.uso_motor or "")


@pytest.mark.parametrize("llave", E.B2_HISTORICO, ids=lambda k: k[1])
def test_b2_rol_historico_no_emite(llave):
    regla_id, conducta = llave
    s = next(x for x in _REGLAS[regla_id].entonces if x.conducta == conducta)
    assert s.rol_uso == "historico" and "NO-ADOPTAR-NC-0107" in s.uso_motor
    assert emisor.emitir_binaria(_REGLAS[regla_id], conducta).estado == "NO-EMITE"


def test_v5_idempotente(ctx):
    fuente = E.TARGET.read_text(encoding="utf-8")
    assert E.transform_motor_v5(fuente, ctx) == fuente


def test_b1_rechaza_hermano_sin_cita(ctx):
    regla = {"id": "x", "entonces": [{"conducta": "h", "p": 0.5, "clase": "MEDIDO"}]}
    with pytest.raises(ValueError, match="no cita GEN2"):
        E.guardas_b1(regla, "h", ctx)


def test_b3_cortes_fuera_del_contador_y_b2_no_activo():
    assert "corte_pi" in C.TIPOS_FUERA_DEL_CONTADOR
    v = C._filas_registro(verifica=False)
    esperados = {f"milpa/tramite.yaml:{r}:{c}" for r, c in E.B2_HISTORICO}
    assert C._consumidores_rol_historico() == esperados
    hist = [u for u in v["usos"] if u["consumidor"] in esperados]
    assert len(hist) == len(esperados) and all(u["activo"] == "NO" for u in hist)
