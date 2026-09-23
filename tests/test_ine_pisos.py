"""Protege denominador, suma ponderada y cobertura del conteo INE."""
import importlib.util
import json
import zipfile
from pathlib import Path


MODULE = Path(__file__).resolve().parents[1] / "data/corrida0/CALC-INE-PISOS-2024-0001/medidor.py"
spec = importlib.util.spec_from_file_location("ine_pisos", MODULE)
medidor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(medidor)


def test_tasa_es_razon_de_sumas_y_ns_no_es_voto(tmp_path):
    path = tmp_path / "ine.zip"
    header = "AELEC,EDOCVE,SEXO,LN,SV,NV,NS\n"
    with zipfile.ZipFile(path, "w") as archive:
        for state in range(1, 33):
            records = "2024,%02d,0,100,40,50,10\n2024,%02d,0,900,720,180,0\n" % (state, state)
            archive.writestr(f"s{state:02d}.csv", header + records)
    out = medidor.medir({medidor.PID: {"ruta_absoluta": str(path)}}, {})
    rows = json.loads(out["RESULT-INE-PISOS-2024-TABLA"])
    national = next(x for x in rows if x["geo"] == "nacional" and x["sexo"] == "total")
    assert out["RESULT-INE-PISOS-2024-FILAS"] == 64
    assert out["RESULT-INE-PISOS-2024-DESCUADRES"] == 0
    assert national["tasa_ln"] == 0.76
    assert national["ns"] == 320
    assert national["tasa_marca_conocida"] > national["tasa_ln"]
