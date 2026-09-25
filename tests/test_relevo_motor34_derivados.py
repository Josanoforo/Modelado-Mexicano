#!/usr/bin/env python3
"""Pruebas sintéticas de los CALC derivados de complementos (ACTO GEN2-RELEVO-MOTOR-34-1).

Solo fixtures sintéticos: el medidor no se ejecuta contra el padre real antes
del COMMIT-1.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CALCS = (
    ROOT / "data/corrida0/CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001",
    ROOT / "data/corrida0/CALC-ENCUCI-0001-COMPLEMENTO-DERIVADO-0001",
)


def _modulo(calc: Path):
    spec = importlib.util.spec_from_file_location(
        "m34_" + calc.name.replace("-", "_"), calc / "medidor.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _contrato(calc: Path) -> dict:
    return yaml.safe_load((calc / "spec.yaml").read_text(encoding="utf-8"))


def _doc(contrato: dict, p=0.30, lo=0.20, hi=0.40, veredicto="TASA-REPORTADA",
         metodo="IC-SINTETICO") -> dict:
    valores = {}
    for par in contrato["parametros"]["complementos"]:
        valores.update({par["p_id"]: p, par["ic_lo_id"]: lo, par["ic_hi_id"]: hi,
                        par["veredicto_id"]: veredicto, par["metodo_ic_id"]: metodo})
    return {"spec_id": contrato["parametros"]["padre"]["calc_id"], "resultados": valores}


def _inputs(contrato: dict, doc: dict, rompe_sello: bool = False) -> dict:
    ids = contrato["parametros"]["padre"]["inputs"]
    resultados_b = (json.dumps(doc, sort_keys=True) + "\n").encode()
    spec_b = b"spec: sintetica\n"
    sello = {"resultados.json": "0" * 64 if rompe_sello else _sha(resultados_b),
             "spec.yaml": _sha(spec_b)}
    sello_b = (json.dumps(sello, sort_keys=True) + "\n").encode()
    return {
        ids["resultados"]: {"bytes": resultados_b},
        ids["spec"]: {"bytes": spec_b},
        ids["sello"]: {"bytes": sello_b},
        ids["sello_sha256"]: {"bytes": f"{_sha(sello_b)}  sello.json\n".encode()},
    }


@pytest.mark.parametrize("calc", CALCS, ids=lambda c: c.name)
def test_rama_estimable_emite_todos_los_ids_declarados(calc):
    m, c = _modulo(calc), _contrato(calc)
    out = m.medir(_inputs(c, _doc(c)), c)
    assert set(out) == {r["id"] for r in c["resultados"]}
    for par in c["parametros"]["complementos"]:
        pre = par["prefijo"]
        assert out[pre + "Q"] == pytest.approx(0.70, abs=1e-15)
        assert out[pre + "IC-LO-Q"] == pytest.approx(0.60, abs=1e-15)
        assert out[pre + "IC-HI-Q"] == pytest.approx(0.80, abs=1e-15)
        assert out[pre + "SUMA-P-Q"] == pytest.approx(1.0, abs=1e-15)
        assert out[pre + "COMPATIBILIDAD-LEGACY"] == "NO-COINCIDE-AL-GRANO"
    assert all(v is not None for v in out.values())


@pytest.mark.parametrize("calc", CALCS, ids=lambda c: c.name)
def test_coincide_al_grano_cuando_q_es_el_legacy(calc):
    m, c = _modulo(calc), _contrato(calc)
    c2 = copy.deepcopy(c)
    for par in c2["parametros"]["complementos"]:
        par["valor_legacy"] = 0.7
    out = m.medir(_inputs(c2, _doc(c2)), c2)
    for par in c2["parametros"]["complementos"]:
        assert out[par["prefijo"] + "COMPATIBILIDAD-LEGACY"] == "COINCIDE-AL-GRANO"


@pytest.mark.parametrize("calc", CALCS, ids=lambda c: c.name)
@pytest.mark.parametrize("kw,codigo", [
    ({"veredicto": "NO-ESTIMABLE-X"}, "PADRE-NO-ESTIMABLE-VEREDICTO"),
    ({"metodo": "NO-ESTIMABLE-DISENO"}, "PADRE-NO-ESTIMABLE-METODO-IC"),
    ({"lo": 0.5}, "PADRE-NO-ESTIMABLE-LIMITES"),
    ({"hi": 1.2}, "PADRE-NO-ESTIMABLE-LIMITES"),
    ({"p": None}, "PADRE-NO-ESTIMABLE-RESULTADO-NO-NUMERICO"),
    ({"p": float("nan")}, "PADRE-NO-ESTIMABLE-RESULTADO-NO-FINITO"),
    ({"p": True}, "PADRE-NO-ESTIMABLE-RESULTADO-NO-NUMERICO"),
])
def test_padre_no_estimable_se_rechaza_nunca_cero(calc, kw, codigo):
    m, c = _modulo(calc), _contrato(calc)
    with pytest.raises(RuntimeError, match=codigo):
        m.medir(_inputs(c, _doc(c, **kw)), c)


@pytest.mark.parametrize("calc", CALCS, ids=lambda c: c.name)
def test_sello_que_no_cubre_los_bytes_se_rechaza(calc):
    m, c = _modulo(calc), _contrato(calc)
    with pytest.raises(RuntimeError, match="SELLO-NO-CUBRE"):
        m.medir(_inputs(c, _doc(c), rompe_sello=True), c)


@pytest.mark.parametrize("calc", CALCS, ids=lambda c: c.name)
def test_spec_id_ajeno_se_rechaza(calc):
    m, c = _modulo(calc), _contrato(calc)
    doc = _doc(c)
    doc["spec_id"] = "CALC-OTRO"
    with pytest.raises(RuntimeError, match="SPEC-ID-INCORRECTO"):
        m.medir(_inputs(c, doc), c)


@pytest.mark.parametrize("calc", CALCS, ids=lambda c: c.name)
def test_clase_iii_padre_unico_y_sin_ingestion_ajena(calc):
    c = _contrato(calc)
    padre = c["parametros"]["padre"]["calc_id"]
    assert c["etiquetas"]["padre"] == padre
    for i in c["inputs"]:
        assert i["ruta"].startswith(f"data/corrida0/{padre}/")
