"""R sintética exclusivamente; ningún registro reservado se lee."""
import importlib.util
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("lector_futuro", ROOT/"tools/familias-2027/enif/lector.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
spec = importlib.util.spec_from_file_location("corrida_futuro", ROOT/"tools/corrida0.py")
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
SCHEMA = yaml.safe_load((ROOT/"tools/familias-2027/enif/contrato-futuro.yaml").read_text())


def entradas():
    ins = {k: {"bytes": (ROOT/"data/corrida0"/k/"resultados.json").read_bytes()} for k in m.PISOS_HASH}
    ins["enif_2027"] = {"ruta_absoluta": "SINTETICO-NO-ARCHIVO"}
    meta = {"unidad":"persona18+","peso":"FAC_PER","formal":list(m.FORMAL),"informal":list(m.INFORMAL),"periodo":"ultimos12meses"}
    return ins, {"estado":"RESERVADA","autoridad_ola":"AUTORIZACION-SINTETICA","metadatos":meta,"comparabilidad_cotejada":True}


def filas(completo=False, singleton=False, vacio=False):
    rows = []
    for j in range(10080 if completo else 12):
        r = dict.fromkeys(m.COLS, "2")
        r.update(LLAVEMOD=str(j), FAC_PER="1", EDAD_V="98", EST_DIS=str(j%180), UPM_DIS=str((j//180)%6))
        if singleton:r["UPM_DIS"] = "única"
        if vacio:r["EST_DIS"] = ""
        r["P5_6_1"] = "1" if j%2 else "b"
        r["P5_1_1"] = "1" if j%3 else "2"
        rows.append(r)
    return rows


@pytest.mark.parametrize("caso", ["completo", "parcial", "singleton", "diseno-vacio"])
def test_terminales_real_yaml(caso, monkeypatch):
    rows = filas(caso=="completo", caso=="singleton", caso=="diseno-vacio")
    monkeypatch.setattr(m, "lee_zip", lambda _: rows)
    ins, contrato = entradas()
    out = m.medir_futuro(ins, contrato)
    assert c._valida_outputs(SCHEMA, out) == []
    assert set(out) == {x["id"] for x in SCHEMA["resultados"]}
    if caso != "completo":
        assert out["RESULT-FAMILIA-ENIF-FUTURO-AHORRO-FORMAL-ESTADO"] == "NO-ESTIMABLE"
    if caso == "diseno-vacio":
        assert out["RESULT-FAMILIA-ENIF-FUTURO-AHORRO-FORMAL-LO"] is None


def test_guardia_piso_antes_lectura(monkeypatch):
    ins, contrato = entradas()
    parent = next(iter(m.PISOS_HASH)); ins[parent]["bytes"] = b"{}"
    monkeypatch.setattr(m,"lee_zip", lambda _: pytest.fail("no debe abrir antes de hash"))
    with pytest.raises(PermissionError):m.medir_futuro(ins, contrato)
    ins, contrato = entradas(); contrato["autoridad_ola"] = None
    with pytest.raises(PermissionError):m.medir_futuro(ins, contrato)
