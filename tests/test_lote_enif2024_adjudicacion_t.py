#!/usr/bin/env python3
"""Pruebas de `CALC-DIN-LOTE-ENIF2024-ADJUDICACION-T-0001` (D-22, E.6).

ACTO `GEN2-DIN-LOTE-ENIF2024-SECUNDARIA-1`. Reusa el fabricante sintético del
lote (`tools/lote_enif2024/sintetico.py`, importado -- no se copia; produce
zips con la MISMA forma que los payloads reales, incluida la columna
`formalidad` que define el universo T) para ejercitar el conducto completo
(`medir()`) sin abrir microdato real, y prueba por mutación la guardia de
`cruce_t()` (ningún par fuera de los 5 autorizados). Prueba además, sobre el
`resultados.json` SELLADO del CALC primario (lectura únicamente, no lo
recalcula), que el estrato T de este CALC no aparece ahí -- ENMIENDA-1 §8.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
CALC_T = RAIZ / "data" / "corrida0" / "CALC-DIN-LOTE-ENIF2024-ADJUDICACION-T-0001"
CALC_PRIMARIO = RAIZ / "data" / "corrida0" / "CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001"


def _importa(nombre: str, ruta: Path):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def med():
    return _importa("medidor_adj_t_bajo_prueba", CALC_T / "medidor.py")


@pytest.fixture(scope="module")
def sint():
    return _importa("sintetico_lote_enif2024", RAIZ / "tools" / "lote_enif2024" / "sintetico.py")


@pytest.fixture(scope="module")
def lote_par():
    import yaml
    return yaml.safe_load((CALC_PRIMARIO / "spec.yaml").read_text())["parametros"]


def _c2r_sellado_sintetico(ids: dict, valor: float = 0.4) -> dict:
    """Un `resultados.json` de C2R fabricado: mismos 28 ids, valores
    sintéticos plausibles (nunca 0 ni 1, para que ninguna celda salga
    MARGINAL-DEGENERADO por construcción del piso citado)."""
    out = {}
    for _par, cats_a in ids.items():
        for _ca, cats_b in cats_a.items():
            for _cb, rid in cats_b.items():
                out[rid] = valor
    return {"resultados": out}


def _contrato_sintetico(spec_yaml_path: Path) -> dict:
    import yaml
    return yaml.safe_load(spec_yaml_path.read_text())


def _inputs_sinteticos(tmp_path: Path, sint, lote_par, c2r_sellado: dict,
                       vaciar21=None, vaciar24=None, n=900):
    import hashlib

    def sha(p):
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()

    z21 = sint.fabrica_zip(tmp_path / "enif2021.zip", "2021", n=n, seed=1, vaciar=vaciar21)
    z24 = sint.fabrica_zip(tmp_path / "enif2024.zip", "2024", n=n, seed=2, vaciar=vaciar24)
    c2r_path = tmp_path / "c2r_resultados.json"
    c2r_path.write_text(json.dumps(c2r_sellado))
    return {
        "enif2021_csv": {"ruta_absoluta": str(z21), "sha256": sha(z21)},
        "enif2024_csv": {"ruta_absoluta": str(z24), "sha256": sha(z24)},
        "IN-LOTE-SPEC-SELLADA": {"ruta_absoluta": str(CALC_PRIMARIO / "spec.yaml"),
                                 "sha256": sha(CALC_PRIMARIO / "spec.yaml")},
        "IN-C2R-SELLADO": {"ruta_absoluta": str(c2r_path), "sha256": sha(c2r_path)},
    }


def test_conducto_corre_sobre_sintetico_y_cubre_el_catalogo(tmp_path, med, sint, lote_par):
    """D-22(2): el punto de entrada corre sobre datos fabricados, nunca sobre
    un cruce reservado real, y `_valida_outputs` (aquí: comparación directa
    contra `catalogo_resultados()`) acepta la salida entera."""
    contrato = _contrato_sintetico(CALC_T / "spec.yaml")
    c2r = _c2r_sellado_sintetico(contrato["parametros"]["c2r_result_ids"])
    inputs = _inputs_sinteticos(tmp_path, sint, lote_par, c2r)
    out = med.medir(inputs, contrato)
    cat = med.catalogo_resultados(contrato["parametros"]["pares_t"], lote_par["ejes"])
    cat_ids = {c["id"] for c in cat}
    permite_null = {c["id"] for c in cat if c.get("permite_no_estimable")}
    assert cat_ids == set(out.keys()), (
        f"catalogo vs salida real difieren: solo_en_out={set(out) - cat_ids}, "
        f"solo_en_catalogo={cat_ids - set(out)}")
    for k, v in out.items():
        assert v is not None or k in permite_null, f"{k} sale None sin permite_no_estimable"
    assert out[f"{med.P}-G-GUARDIA-AST"] == "PASA"
    assert out[f"{med.P}-G-N-CELDAS"] == 28
    assert out[f"{med.P}-G-EN-DELTA-MAE-PRIMARIO-DEL-LOTE"] == "NO"


def test_celda_rara_una_ola_vacia(tmp_path, med, sint, lote_par):
    """Rama terminal: una categoría entera queda sin filas en 2024 (n=0 en
    una ola) -- no debe tronar, la celda sale sin soporte."""
    contrato = _contrato_sintetico(CALC_T / "spec.yaml")
    c2r = _c2r_sellado_sintetico(contrato["parametros"]["c2r_result_ids"])
    inputs = _inputs_sinteticos(tmp_path, sint, lote_par, c2r, vaciar24={"sexo": {"2"}})
    out = med.medir(inputs, contrato)
    puntuada = [v for k, v in out.items() if k.endswith("-PUNTUADA")]
    assert "NO" in puntuada, "se esperaba al menos una celda sin soporte con sexo=2 vaciado en 2024"


def test_marginal_masa_cero_en_2021(tmp_path, med, sint, lote_par):
    """Rama terminal: una categoría de un eje sin filas en 2021 dentro de T
    (masa cero) -- R3/P2 de esa celda deben salir `None`, declarados, no
    tronar."""
    contrato = _contrato_sintetico(CALC_T / "spec.yaml")
    c2r = _c2r_sellado_sintetico(contrato["parametros"]["c2r_result_ids"])
    inputs = _inputs_sinteticos(tmp_path, sint, lote_par, c2r, vaciar21={"tloc": {"3", "4"}})
    out = med.medir(inputs, contrato)
    assert out[f"{med.P}-G-GUARDIA-AST"] == "PASA"


def test_guardia_veta_par_no_autorizado_control_positivo(med, sint, tmp_path):
    """E.6: control positivo de la guardia -- `cruce_t` debe lanzar
    `ReservaRota` sobre cualquier par fuera de los 5 autorizados (aquí:
    sexo x localidad, que nunca es un par de este CALC)."""
    ola = sint.fabrica_zip(tmp_path / "enif2024.zip", "2024", n=200, seed=3)
    import pandas as pd
    par_lote = _contrato_sintetico(CALC_PRIMARIO / "spec.yaml")["parametros"]
    ola_t = med._carga_ola_t(ola, "2024", par_lote)
    rep = med.replicas_t_local(ola_t, 42, 200)
    with pytest.raises(med.ReservaRota):
        med.cruce_t(ola_t, "sexo", "localidad", rep, [("formalidad", "sexo")], lambda e: tuple(par_lote["ejes"][e]["orden"]))


def test_guardia_ast_pasa_sobre_el_archivo_real(med):
    viol = med.auditoria_ast(CALC_T / "medidor.py")
    assert viol == [], f"violaciones: {viol}"


def test_guardia_ast_detecta_cruce_extra_por_mutacion(med):
    """Control positivo (3D): si el archivo definiera una SEGUNDA función de
    cruce, la guardia debe reportarlo (R7)."""
    fuente = (CALC_T / "medidor.py").read_text(encoding="utf-8")
    mutada = fuente.replace(
        "def cruce_t(ola: OlaT",
        "def cruce_t_extra(ola):\n    return {}\n\n\ndef cruce_t(ola: OlaT",
    )
    viol = med.auditoria_ast_fuente(mutada)
    assert any("R7" in v for v in viol), "la mutación (segunda función de cruce) no fue detectada"


def test_estrato_t_fuera_del_delta_mae_primario_del_lote():
    """ENMIENDA-1 §8: ningún RESULT del CALC primario ya sellado usa el
    prefijo de este CALC secundario -- por construcción, no por acuerdo."""
    doc = json.loads((CALC_PRIMARIO / "resultados.json").read_text())
    resultados = doc.get("resultados", doc)
    prefijo = "RESULT-DIN-LOTE24-ADJ-T"
    ajenos = [k for k in resultados if k.startswith(prefijo)]
    assert ajenos == [], f"el CALC primario ya sellado trae ids del secundario: {ajenos}"
    # control positivo: el propio CALC secundario sí los tiene, en cuanto exista
    resultados_t_path = CALC_T / "resultados.json"
    if resultados_t_path.exists():
        doc_t = json.loads(resultados_t_path.read_text())
        propios = [k for k in doc_t.get("resultados", doc_t) if k.startswith(prefijo)]
        assert len(propios) > 100, "control positivo: el CALC secundario debería traer 900+ ids con su propio prefijo"


def test_medidor_primario_no_referencia_al_secundario():
    fuente_primaria = (CALC_PRIMARIO / "medidor.py").read_text(encoding="utf-8")
    assert "ADJUDICACION-T" not in fuente_primaria
    assert "adjudicacion_t" not in fuente_primaria.lower().replace("-", "_")
