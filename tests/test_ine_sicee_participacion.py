"""Contrato sintético de CALC-INE-PISOS-SICEE-0001."""
import importlib.util
import json
from pathlib import Path

import pytest

MODULE = Path(__file__).resolve().parents[1] / "data/corrida0/CALC-INE-PISOS-SICEE-0001/medidor.py"
spec = importlib.util.spec_from_file_location("ine_sicee", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
CARGOS = {"PRE", "DIP_MR"}


def _r(cargo, anio, dist, tv, ln, pct):
    return {"cargo": cargo, "anio": anio, "distribucion": dist, "total_votos": tv,
            "lista_nominal": ln, "porcentaje_participacion": pct,
            "num_votos_nulos": "0", "num_votos_can_nreg": "0"}


def test_tasa_diferencia_y_distribucion_opaca():
    filas, diag = mod.filas_medidas(
        [_r("PRE", 2024, 2, "600", 1000, "60.00"), _r("PRE", 2024, 1, "6,000", 10000, "60%"),
         _r("DIP_MR", 2021, 1, "5", 0, "0")], CARGOS)
    assert [(f["cargo"], f["distribucion"]) for f in filas] == [("DIP_MR", 1), ("PRE", 1), ("PRE", 2)]
    assert filas[0]["estado"] == "NO-ESTIMABLE"
    assert filas[1]["tasa"] == 0.6 and filas[1]["dif_pp"] == 0.0
    pre = [d for d in diag if d["cargo"] == "PRE"][0]
    assert pre["n_distribuciones"] == 2 and pre["total_votos_igual"] is False


def test_cargo_fuera_y_valor_no_numerico_detienen():
    with pytest.raises(ValueError):
        mod.filas_medidas([_r("GOB", 2024, 1, "1", 2, "50")], CARGOS)
    with pytest.raises(ValueError):
        mod.filas_medidas([_r("PRE", 2024, 1, "", 2, "50")], CARGOS)


def test_medir_emite_json_canonico(tmp_path):
    p = tmp_path / "s.json"
    p.write_text(json.dumps([_r("PRE", 2018, 1, "63", 100, "63")]), encoding="utf-8")
    out = mod.medir({mod.PID: {"ruta_absoluta": str(p)}}, {"parametros": {"cargos": ["PRE"]}})
    assert out["RESULT-INE-PISOS-SICEE-FILAS"] == 1
    assert json.loads(out["RESULT-INE-PISOS-SICEE-TABLA"])["filas"][0]["tasa"] == 0.63


def test_conducto_acepta_salida_con_no_estimable(tmp_path):
    import yaml
    root = Path(__file__).resolve().parents[1]
    s0 = importlib.util.spec_from_file_location("c0", root / "tools/corrida0.py")
    c0 = importlib.util.module_from_spec(s0)
    s0.loader.exec_module(c0)
    s = yaml.safe_load((MODULE.parent / "spec.yaml").read_text(encoding="utf-8"))
    p = tmp_path / "s.json"
    p.write_text(json.dumps([_r("PRE", 2018, 1, "63", 100, "63"), _r("CONS_POP", 2021, 2, "1", 0, "0")]), encoding="utf-8")
    out = mod.medir({mod.PID: {"ruta_absoluta": str(p)}}, c0.contrato_ejecutable(s))
    assert c0._valida_outputs(s, out) == []
