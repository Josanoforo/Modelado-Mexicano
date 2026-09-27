# -*- coding: utf-8 -*-
"""Test de `tools/recibo/comparaciones.py` (ACTO GEN2-RECIBO-ASTRA6-1).

Defecto que atrapa: un recibo que reporta «685 distintas» sin repartirlas por
componente, o que da estado a una llave sin tolerancia preexistente citada
(compuerta «adoptar» del encargo). Costo para un lector: leer 2 569 DISCREPA
como 2 569 cifras erroneas del catalogo.
"""
import base64
import hashlib
import sys
from collections import Counter
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools" / "recibo"))
import comparaciones as C  # noqa: E402

LOTE = RAIZ / "forense/validacion-independiente/catalogo-1-ejecucion-lote1"


@pytest.fixture(scope="module")
def recibo():
    if not (LOTE / "entregas.json").exists():
        pytest.skip("lote 1 ausente")
    return C.recibe(LOTE)


def test_toda_llave_tiene_estado_con_tolerancia_citada(recibo):
    filas, _, resumen = recibo
    assert resumen["llaves"] == len(filas) == 3371
    assert resumen["sin_estado"] == 0
    assert all("spec.yaml" in f["tolerancia_citada"] for f in filas)


def test_reparto_casa_con_el_informe_del_lote(recibo):
    _, _, resumen = recibo
    assert resumen["por_estado_componente"] == {
        "COINCIDE|PUNTO+IC": 3, "DISCREPA|IC": 1873, "DISCREPA|PUNTO": 685,
        "DISCREPA|PUBLICABILIDAD": 11, "NO-RECALCULABLE-DESDE-SPEC|SPEC": 799}
    assert resumen["artefacto_comparador_dentro_recomputado_distinto"] == 0
    assert all(resumen["comparacion_sha_casa"].values())


def test_spec_insuficiente_separa_empaquetado_de_d15(recibo):
    _, _, resumen = recibo
    total = Counter()
    for k, v in resumen["spec_por_causa"].items():
        total[k.split("|")[1]] += v
    assert sum(total.values()) == 799
    assert total["PAQUETE-SIN-IDENTIDAD-DE-VENTANA"] == 767
    assert "D15-OTRA" not in total


def test_ceguera_un_rotulo_por_paquete(recibo):
    _, ceg, _ = recibo
    assert len(ceg) == 9
    assert {c["rotulo_recibo"] for c in ceg} <= {
        "CIEGA-POR-SEPARACION", "REIMPLEMENTACION-INDEPENDIENTE-NO-CIEGA"}


def test_commit_mutado_no_verifica():
    raw = (b"tree 0\nauthor a <a> 1790469381 +0000\n"
           b"committer a <a> 1790469381 +0000\n\nx\n")
    oid = hashlib.sha1(b"commit %d\0" % len(raw) + raw).hexdigest()
    prueba = {"commit_oid": oid,
              "commit_content_base64": base64.b64encode(raw).decode()}
    assert C._commit(prueba)[0] is True
    prueba["commit_content_base64"] = base64.b64encode(raw + b"y").decode()
    assert C._commit(prueba)[0] is False


def test_cubos():
    assert C._cubo(0.00005, [1e-4, 1e-3]) == "<=0.0001"
    assert C._cubo(0.5, [1e-4, 1e-3]) == ">0.001"
