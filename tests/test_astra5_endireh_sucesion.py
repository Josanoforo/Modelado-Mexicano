import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

path = Path(__file__).resolve().parents[1] / "tools/corrida0.py"
spec = importlib.util.spec_from_file_location("corrida0", path)
corrida0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(corrida0)


def test_sucesion_externa_ata_spec_y_sello(tmp_path):
    carpeta = tmp_path / "CALC-ENDIREH-TEST-v2"
    carpeta.mkdir()
    (carpeta / "spec.yaml").write_text("calc_id: CALC-ENDIREH-TEST-v2\n")
    (carpeta / "sello.json").write_text('{"firma":"sellada"}\n')
    sha = lambda nombre: hashlib.sha256((carpeta / nombre).read_bytes()).hexdigest()
    meta = {"calc_id": carpeta.name, "repite_de": "CALC-ENDIREH-TEST-v1",
            "spec_yaml_sha256": sha("spec.yaml"), "sello_sha256": sha("sello.json")}
    (carpeta / "sucesion.json").write_text(json.dumps(meta))
    ejec = {"spec_yaml_sha256": meta["spec_yaml_sha256"]}
    assert corrida0._sucesion_externa(carpeta, {}, ejec) == meta["repite_de"]
    (carpeta / "sello.json").write_text('{"firma":"distinta"}\n')
    with pytest.raises(corrida0.ParoRegistro, match="SUCESION-IDENTIDAD"):
        corrida0._sucesion_externa(carpeta, {}, ejec)


def test_sucesion_no_contradice_spec(tmp_path):
    carpeta = tmp_path / "CALC-ENDIREH-TEST-v2"
    carpeta.mkdir()
    (carpeta / "spec.yaml").write_text("calc_id: CALC-ENDIREH-TEST-v2\n")
    (carpeta / "sello.json").write_text("{}\n")
    sha = lambda nombre: hashlib.sha256((carpeta / nombre).read_bytes()).hexdigest()
    meta = {"calc_id": carpeta.name, "repite_de": "CALC-ENDIREH-TEST-v1",
            "spec_yaml_sha256": sha("spec.yaml"), "sello_sha256": sha("sello.json")}
    (carpeta / "sucesion.json").write_text(json.dumps(meta))
    with pytest.raises(corrida0.ParoRegistro, match="SUCESION-CONFLICTO"):
        corrida0._sucesion_externa(carpeta, {"repite_de": "otro"},
                                  {"spec_yaml_sha256": meta["spec_yaml_sha256"]})
