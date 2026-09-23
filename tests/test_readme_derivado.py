"""Comprueba sólo los comandos de derivación conocidos de la portada."""
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
CLAVES = {
    "N_corridas_selladas",
    "N_resultados_gen2_sellados",
    "N_resultados_gen2_adoptados_activos",
    "celdas_validadas",
    "celdas_validadas_prospectiva",
    "celdas_validadas_retrospectiva",
    "N_resultados_gen2_pendientes_adopcion",
}


class ReadmeDerivado(unittest.TestCase):
    def test_status(self):
        salida = subprocess.check_output(
            ["python3", "tools/corrida0.py", "status"], cwd=ROOT, text=True
        )
        valores = dict(re.findall(r"(?m)^([A-Za-z0-9_]+)=(\d+)$", salida))
        filas = re.findall(
            r"(?m)^\|[^\n]+?\| ([\d ]+) \| <!-- deriva: "
            r"python3 tools/corrida0.py status \| rg '\^([A-Za-z0-9_]+)=' -->",
            README,
        )
        self.assertEqual({clave for _, clave in filas}, CLAVES)
        for impreso, clave in filas:
            self.assertEqual(int(impreso.replace(" ", "")), int(valores[clave]), clave)

    def test_reports(self):
        self.assertIn("<!-- deriva: rg --files corpus/reports -g '*.md' | wc -l -->", README)
        total = len(list((ROOT / "corpus/reports").glob("*.md")))
        self.assertIn(f"**{total} reports temáticos**", README)

    def test_celdas_de_evaluaciones(self):
        fuentes = {
            8: ("8/8 celdas", "forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md"),
            12: ("12/12 celdas", "forense/notas/2026-09-17-GEN2-CELDA-D-PILOTO-2-cierre.md"),
            15: ("3/15", "forense/notas/2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-cierre.md"),
            44: ("44 celdas puntuadas", "canon/informe-programa-v1_2.md"),
        }
        for cantidad, (frase, ruta) in fuentes.items():
            # Sólo estas fuentes conocidas: jamás evalúa comandos tomados del Markdown.
            salida = subprocess.check_output(["rg", "-F", frase, ruta], cwd=ROOT, text=True)
            self.assertIn(frase, salida)
            impreso = f"{cantidad} celdas puntuadas" if cantidad == 44 else f"{cantidad} celdas"
            self.assertIn(f"{impreso} <!-- deriva: rg -F '{frase}' {ruta} -->", README)
        frase = "12 celdas puntuadas por par"
        ruta = "forense/notas/2026-09-22-GEN2-DUELO-ENVIPE2026-EJECUCION-1-cierre.md"
        self.assertIn(frase, subprocess.check_output(["rg", "-F", frase, ruta], cwd=ROOT, text=True))
        self.assertIn(f"12 por cruce <!-- deriva: rg -F '{frase}' {ruta} -->", README)


if __name__ == "__main__":
    unittest.main()
