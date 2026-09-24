"""Cifras derivadas de los cuatro artefactos del ACTO GEN2-FRONT-2.

Mismo patrón que test_readme_derivado.py: cada `<!-- deriva: CMD -->` se
corre de verdad y se compara contra el número impreso a su izquierda. No
evalúa comandos arbitrarios pegados por otra mano: sólo los que ya viven en
estos cuatro archivos.
"""
from __future__ import annotations

import csv
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARCHIVOS_CON_DERIVA = [
    "docs/one-pager.md",
    "docs/reto.md",
    "docs/deck/02-seis-evaluaciones.md",
]

PATRON_DERIVA = re.compile(r"(\d[\d ]*)\s*<!--\s*deriva:\s*(.+?)\s*-->")


class CifrasDerivadas(unittest.TestCase):
    def _corre(self, comando: str) -> str:
        resultado = subprocess.run(
            ["bash", "-c", comando], cwd=ROOT, capture_output=True, text=True, timeout=200,
        )
        self.assertEqual(resultado.returncode, 0, f"comando falló: {comando}\n{resultado.stderr}")
        return resultado.stdout

    def test_deriva_en_los_cuatro_artefactos(self):
        total_verificado = 0
        for nombre in ARCHIVOS_CON_DERIVA:
            texto = (ROOT / nombre).read_text(encoding="utf-8")
            hallazgos = PATRON_DERIVA.findall(texto)
            self.assertTrue(hallazgos, f"{nombre} no trae ningún <!-- deriva: ... --> citado")
            for impreso, comando in hallazgos:
                salida = self._corre(comando)
                m = re.search(r"(\d+)\s*\Z", salida.strip())
                self.assertIsNotNone(m, f"{nombre}: comando sin número al final: {comando!r} -> {salida!r}")
                esperado = int(impreso.replace(" ", ""))
                self.assertEqual(
                    esperado, int(m.group(1)),
                    f"{nombre}: '{impreso.strip()}' <!-- deriva: {comando} --> dio {m.group(1)}",
                )
                total_verificado += 1
        self.assertGreaterEqual(total_verificado, 10)

    def test_tabla_de_piso_solo_adoptado(self):
        salida = self._corre("python3 tools/genera_tabla_piso.py")
        m = re.search(r"^filas_adoptadas=(\d+)$", salida, re.MULTILINE)
        self.assertIsNotNone(m)
        n_generado = int(m.group(1))

        with (ROOT / "canon/tabla-de-piso-v1_0.tsv").open(newline="", encoding="utf-8") as f:
            filas = list(csv.DictReader(f, delimiter="\t"))
        self.assertEqual(len(filas), n_generado)
        estados = {fila["estado_adopcion"] for fila in filas}
        self.assertEqual(estados, {"ADOPTADO-POR-FIRMA", "CONSUMO-GEN2-ACTIVO"})

        status = self._corre("python3 tools/corrida0.py status")
        m2 = re.search(r"^N_resultados_gen2_adoptados_activos=(\d+)$", status, re.MULTILINE)
        self.assertIsNotNone(m2)
        self.assertEqual(len(filas), int(m2.group(1)))

    def test_delta_mae_piloto3_citado_verbatim(self):
        fuente = (ROOT / "forense/notas/2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-cierre.md").read_text(encoding="utf-8")
        frase = "Sλ 1.465 pp, IC95 [0.439, 2.115]"
        self.assertIn(frase, fuente)
        deck = (ROOT / "docs/deck/02-seis-evaluaciones.md").read_text(encoding="utf-8")
        self.assertIn("1.465 pp IC95 [0.439, 2.115]", deck)


if __name__ == "__main__":
    unittest.main()
