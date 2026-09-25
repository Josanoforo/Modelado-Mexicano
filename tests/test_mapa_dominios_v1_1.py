"""GEN2-MAPA-DOMINIOS-V1-1-1: el mapa v1.1 es derivado (D-23) y la compuerta A.15 muerde.

Defecto que atrapa: un dictamen MEDIBLE-EN-CORPUS escrito a mano o con un
texto de pregunta que no está en el inventario (A.15; transfers del 21/sep
dieron por ausente lo que estaba, y al revés cuesta lo mismo).
"""
import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DER = ROOT / "forense/analisis/dominios/redictamina_v1_1.py"


def test_verifica_byte_a_byte():
    r = subprocess.run([sys.executable, str(DER), "--verifica"], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stdout + r.stderr


def test_medible_en_corpus_nuevo_tiene_texto_verificado():
    with (ROOT / "canon/mapa-dominios-v1_1.tsv").open(encoding="utf-8", newline="") as fh:
        filas = list(csv.DictReader(fh, delimiter="\t"))
    assert all(f["dictamen"] for f in filas)
    for f in filas:
        if f["dictamen"] == "MEDIBLE-EN-CORPUS" and f["dictamen_v1_0"] != "MEDIBLE-EN-CORPUS":
            assert f["texto_pregunta_v1_1"] and f["variable_v1_1"]
            assert f["estado_corpus_v1_1"] == "TEXTO-VERIFICADO"


if __name__ == "__main__":
    test_verifica_byte_a_byte()
    test_medible_en_corpus_nuevo_tiene_texto_verificado()
    print("OK")
