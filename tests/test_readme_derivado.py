"""Cifras de la portada: toda cifra visible sale de un comando conocido.

ACTO GEN2-FRONT-3-PORTADA-1 (P2) sucede a la versión de FRONT-1: la tabla de
`status` vive ahora en docs/estado.md (claves y comandos, sin valores), y la
portada escribe cada cifra como `**valor** <!-- deriva[clave]: comando -->`.
Nunca se evalúa un comando tomado del Markdown: el comando visible debe ser,
verbatim, el que `tools/readme_derivado.py` declara para esa clave.
"""
from pathlib import Path
import json
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import readme_derivado as RD  # noqa: E402

README = (ROOT / "README.md").read_text(encoding="utf-8")
INDEX = (ROOT / "docs/index.md").read_text(encoding="utf-8")
ESTADO = (ROOT / "docs/estado.md").read_text(encoding="utf-8")


def _visible(texto: str) -> str:
    texto = RD.MARCA.sub("", texto)
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    texto = re.sub(r"\]\([^)]*\)", "]", texto)
    texto = re.sub(r"`[^`\n]*`", "", texto)  # nombres de comando/archivo, no cifras
    return re.sub(r"^---\n.*?\n---\n", "", texto, flags=re.S)


class PortadaDerivada(unittest.TestCase):
    def test_marcas_con_valor_y_comando_de_fuentes(self):
        for nombre, texto in (("README.md", README), ("docs/index.md", INDEX)):
            marcas = RD.MARCA.findall(texto)
            self.assertGreaterEqual(len(marcas), 3, nombre)
            for impreso, clave, comando in marcas:
                self.assertIn(clave, RD.FUENTES, f"{nombre}: deriva[{clave}]")
                self.assertEqual(comando, RD.FUENTES[clave][0], f"{nombre}: comando de {clave}")
                self.assertEqual(impreso, RD.valor(clave), f"{nombre}: {clave}")

    def test_ninguna_cifra_sin_comando(self):
        for nombre, texto in (("README.md", README), ("docs/index.md", INDEX)):
            sueltas = re.findall(r"\d+", _visible(texto))
            self.assertEqual(sueltas, [], f"{nombre}: cifras visibles sin marca deriva")

    def test_status_dentro_del_bloque_derivado(self):
        # derivados_protegidos.py --solo-derivados solo acepta cambios dentro
        # del bloque: toda cifra de `status` debe vivir ahí.
        a = README.index("<!-- TABLERO-DERIVADO:BEGIN -->")
        b = README.index("<!-- TABLERO-DERIVADO:END -->")
        for mo in RD.MARCA.finditer(README):
            if RD.FUENTES[mo.group(2)][0].startswith("python3 tools/corrida0.py status"):
                self.assertTrue(a < mo.start() < b, mo.group(2))
        for mo in RD.MARCA.finditer(INDEX):
            self.assertFalse(RD.FUENTES[mo.group(2)][0].startswith("python3 tools/corrida0.py status"),
                             "docs/index.md no puede llevar cifras de status: el job guardias no la reescribe")

    def test_badges(self):
        for nombre, cuerpo in RD.badges().items():
            ruta = ROOT / "docs/data/badges" / f"{nombre}.json"
            self.assertEqual(json.loads(ruta.read_text(encoding="utf-8")), cuerpo, nombre)

    def test_reports(self):
        self.assertIn("<!-- deriva: rg --files corpus/reports -g '*.md' | wc -l -->", ESTADO)
        total = len(list((ROOT / "corpus/reports").glob("*.md")))
        self.assertIn(f"**{total} reports temáticos**", ESTADO)

    def test_celdas_de_evaluaciones(self):
        fuentes = {
            8: ("8/8 celdas", "forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md"),
            12: ("12/12 celdas", "forense/notas/2026-09-17-GEN2-CELDA-D-PILOTO-2-cierre.md"),
            15: ("3/15", "forense/notas/2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-cierre.md"),
            44: ("44 celdas puntuadas", "canon/informe-programa-v1_2.md"),
        }
        for cantidad, (frase, ruta) in fuentes.items():
            # Sólo estas fuentes conocidas: jamás evalúa comandos tomados del Markdown.
            fuente = (ROOT / ruta).read_text(encoding="utf-8")
            self.assertIn(frase, fuente)
            impreso = f"{cantidad} celdas puntuadas" if cantidad == 44 else f"{cantidad} celdas"
            self.assertIn(f"{impreso} <!-- deriva: rg -F '{frase}' {ruta} -->", ESTADO)
        frase = "12 celdas puntuadas por par"
        ruta = "forense/notas/2026-09-22-GEN2-DUELO-ENVIPE2026-EJECUCION-1-cierre.md"
        self.assertIn(frase, (ROOT / ruta).read_text(encoding="utf-8"))
        self.assertIn(f"12 por cruce <!-- deriva: rg -F '{frase}' {ruta} -->", ESTADO)


if __name__ == "__main__":
    unittest.main()
