"""Prueba en seco (huerfana, D-21): que se rompe si marco-M-sorteado-v1_3.tsv
falta, sin retirar ni tocar el archivo real.

Copia el arbol con `cp -al` (hardlinks: cambiar el nombre de un dirent en la
copia no toca el inode que sigue enlazado desde el repo real), renombra el
marco en la copia y corre los tres comandos que
forense/notas/2026-09-22-GEN2-MARCO-M-CONSUMIDOR-1-mapa.tsv predice.

Defecto que atrapa: que alguien retire o rotule HISTORICO el marco sin haber
medido el costo -- este test es la evidencia mecanica de ACTO
GEN2-MARCO-M-CONSUMIDOR-1 y falla si el costo real diverge del mapa.
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MARCO_REL = "forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv"


class TestMarcoMEnSeco(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if shutil.which("cp") is None:
            raise unittest.SkipTest("cp no disponible")
        cls._tmp = tempfile.mkdtemp(prefix="marco-m-en-seco-")
        cls.arbol = Path(cls._tmp) / "arbol"
        subprocess.run(["cp", "-al", str(REPO), str(cls.arbol)], check=True)
        marco = cls.arbol / MARCO_REL
        if not marco.exists():
            raise unittest.SkipTest(f"{MARCO_REL} no existe en el arbol -- nada que probar en seco")
        marco.rename(marco.with_suffix(marco.suffix + ".HISTORICO"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls._tmp, ignore_errors=True)

    def _corre(self, *args):
        return subprocess.run(
            args, cwd=self.arbol, capture_output=True, text=True, timeout=120
        )

    def test_gonogo_marcador_falla_en_legacy_no_leido(self):
        r = self._corre("python3", "tests/gonogo_marcador.py")
        self.assertIn("LEGACY-NO-LEIDO", r.stdout + r.stderr)
        self.assertIn("NO-GO", r.stdout + r.stderr)

    def test_corrida0_status_no_crashea(self):
        r = self._corre("python3", "tools/corrida0.py", "status")
        self.assertEqual(r.returncode, 0, msg=r.stdout + r.stderr)
        self.assertNotIn("FileNotFoundError", r.stderr)

    def test_corrida0_demanda_crashea_por_marco_vigente(self):
        r = self._corre("python3", "tools/corrida0.py", "demanda")
        combinado = r.stdout + r.stderr
        self.assertIn("FileNotFoundError", combinado)
        self.assertIn(MARCO_REL, combinado)


if __name__ == "__main__":
    unittest.main()
