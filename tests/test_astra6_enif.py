"""Entrada del censo CI a las pruebas del paquete ENIF congelado."""
import subprocess
import sys
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
def test_paquete_enif_guardias_y_terminales():
    r=subprocess.run([sys.executable,"-m","pytest","-q",str(ROOT/"tools/familias-2027/enif/tests")],cwd=ROOT,text=True,capture_output=True)
    assert r.returncode == 0, r.stdout + r.stderr
