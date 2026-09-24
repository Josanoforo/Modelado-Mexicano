"""Guarda de P1 (ACTO GEN2-TUBERIA-RENDIMIENTO-1): `CLAUDE.md` trae las reglas
de lectura, y ninguna skill, comando ni encargo instruye `cat` de una vista
derivada. Defecto que atrapa: sesiones que abren `resultados.tsv` (65k filas)
o `manifiesto.yaml` (15k+ lineas) enteros para leer un dato."""
from __future__ import annotations

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VISTAS = r"(corridas|resultados|usos|marcador-segmento)\.(tsv|json)|manifiesto\.yaml"
_RE_CAT = re.compile(r"\bcat\s+[^\s|;&`]*(" + VISTAS + r")\b")


def _archivos():
    yield RAIZ / "CLAUDE.md"
    yield from (RAIZ / ".claude").rglob("*.md")
    yield from (RAIZ / "forense/encargos").rglob("*.md")
    yield from (RAIZ / "docs").rglob("*.md")


def test_claude_md_tiene_reglas_de_lectura():
    texto = (RAIZ / "CLAUDE.md").read_text(encoding="utf-8")
    for clave in ("## Reglas de lectura", "wc -l", "tools/consulta.py",
                  "git diff --stat", "se consultan, no se leen"):
        assert clave in texto, clave


def test_ningun_md_instruye_cat_de_una_vista():
    hallazgos = []
    for ruta in _archivos():
        if not ruta.is_file():
            continue
        for n, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
            if _RE_CAT.search(linea):
                hallazgos.append(f"{ruta.relative_to(RAIZ)}:{n}")
    assert not hallazgos, hallazgos


def test_regex_atrapa_el_caso_conocido():
    assert _RE_CAT.search("cat data/corrida0/resultados.tsv | head")
    assert _RE_CAT.search("cat data/manifiesto.yaml")
    assert not _RE_CAT.search("`cat` de `resultados.json`")
