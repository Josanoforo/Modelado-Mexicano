import json
from pathlib import Path

import tools.verifica_aislada as aislada


def _fixture(root: Path, calc_id: str, texto: str) -> None:
    calc = root / "data" / "corrida0" / calc_id
    calc.mkdir(parents=True)
    (calc / "spec.yaml").write_text("calc_id: " + calc_id + "\n")
    (calc / "ejecucion.json").write_text('{"spec_yaml_sha256":"s","script_blob_sha256":"' + texto.strip() + '","input_sha256":{"x":"i"}}')
    (calc / "medidor.py").write_text(texto)
    (root / "tools").mkdir(exist_ok=True)
    (root / "tools" / "corrida0.py").write_text(
        "def verify(calc_id, imprime=False): return {'veredicto':'REPRODUCE','contexto':'IDENTICO'}\n"
        "def _identidad_replay(e): return (e['spec_yaml_sha256'],e['script_blob_sha256'],'x=i')\n")


def test_verifica_aislada_separa_proceso_resultado_contexto_e_identidad(tmp_path):
    _fixture(tmp_path, "CALC-A", "A\n")
    _fixture(tmp_path, "CALC-B", "B\n")
    a = aislada.verificar("CALC-A", root=tmp_path)
    b = aislada.verificar("CALC-B", root=tmp_path)
    assert a["proceso_aislado"] and b["proceso_aislado"]
    assert a["resultado_replay"] == b["resultado_replay"] == "REPRODUCE"
    assert a["contexto_replay"] == b["contexto_replay"] == "IDENTICO"
    assert a["identidad"]["script_blob_sha256"] != b["identidad"]["script_blob_sha256"]
    assert "CALC-A" not in b["salida_cruda"]
