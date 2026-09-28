#!/usr/bin/env python3
"""Gate local de identidades y productos; no sustituye la revisión semántica."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ORIGINALS = {
    "Health__Body__Food_and_Substance_Use_in_Mexico__The_Behavioral_Layer_of_Decisions__Environment_and_Structure.md": "7f12dd6d7d3849d35ce948a1f76740f1200fed99",
    "Psicología_de_la_Juventud_Mexicana_Contemporánea__Gen_Z_y_Millennials_Jóvenes_como_Cohorte_Divergente.md": "c9c08ee6e2ae666f1142f1524f004b550f916366",
    "El_Mexicano_y_el_Tiempo__Estructura__no_Cultura__en_la_Planeación_y_el_Compromiso_Temporal.md": "aa12c3ad5be4cc0be61f19a03358fcdc0da1ac03",
}
for name, expected in ORIGINALS.items():
    source = ROOT / "corpus/reports" / name
    target = ROOT / "corpus/reports-v2" / name
    assert source.is_file() and target.is_file(), name
    observed = subprocess.check_output(["git", "hash-object", str(source)], cwd=ROOT, text=True).strip()
    assert observed == expected, (name, observed)

archive = ROOT / "forense/encargos/2026-09-27-ASTRA6-C3-SALUD-JUVENTUD-TIEMPO-1.md"
subprocess.run([sys.executable, "tools/sella_sha256.py", "--cuerpo", "--verifica", str(archive)],
               cwd=ROOT, check=True, capture_output=True)

for piece in ("salud", "juventud", "tiempo"):
    subprocess.run([sys.executable, str(HERE / piece / "verificar.py")], cwd=ROOT, check=True)
subprocess.run([sys.executable, str(HERE / "producir_lote.py"), "--check"], cwd=ROOT, check=True)
print("OK: tres identidades fuente, cuerpo archivado, controles por pieza e índice")
