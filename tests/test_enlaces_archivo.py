"""Enlaces locales de los documentos públicos nuevos.

El histórico sellado conserva citas a rutas antiguas; no se reescribe para
forzar una prueba global de enlaces.
"""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PUBLICOS = [
    "README.md", "AVISO-DE-ALCANCE.md", "USO-ACEPTABLE.md",
    "docs/index.md", "docs/verificar.md", "docs/guia-lectura-publica.md",
    "docs/catalogo.md", "docs/contacto.md",
]


class EnlacesArchivo(unittest.TestCase):
    def test_enlaces_relativos(self):
        rotos = []
        for nombre in PUBLICOS:
            path = ROOT / nombre
            for destino in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if destino.startswith(("http:", "https:", "#", "{{")):
                    continue
                destino = destino.split("#", 1)[0]
                if destino and not (path.parent / destino).exists():
                    rotos.append(f"{nombre}: {destino}")
        self.assertEqual(rotos, [])


if __name__ == "__main__":
    unittest.main()
