"""Guardas de ACTO GEN2-TUBERIA-CABLEADO-SESIONES-1.

Defectos que atrapan: (P1) sesiones que abren enteros derivados de 65k filas
o archivos de cientos de líneas pese a la regla escrita (RENDIMIENTO-1 la
dejó como consejo); (P2) reglas de Codex y de Claude que divergen en silencio;
(P3) una memoria operativa editada por máquina fuera de su bloque marcado, o
que crece hasta dejar de caber en el arranque.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest  # noqa: F401  -- invocador pytest en ci_guardias

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))
import hook_lectura  # noqa: E402
import memoria_operativa  # noqa: E402


def _decide(evento, tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    return hook_lectura.decide(evento)


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "data/corrida0").mkdir(parents=True)
    (tmp_path / "data/corrida0/resultados.tsv").write_text("a\n")
    (tmp_path / "grande.md").write_text("x\n" * 201)
    (tmp_path / "chico.md").write_text("x\n" * 200)
    (tmp_path / "forense/analisis/cableado").mkdir(parents=True)
    return tmp_path


@pytest.mark.parametrize("cmd,bloquea", [
    ("cat data/corrida0/resultados.tsv", True),
    ("cat grande.md | head", True),
    ("less grande.md", True),
    ("cat chico.md", False),
    ("head -n 5 grande.md", False),
    ("git log -p -n 2", True),
    ("git log -p -n 2 -- tools/x.py", False),
    ("git log --oneline -n 5", False),
    ("python3 -m pytest tests/t.py", True),
    ("pytest -q tests/t.py | tail -n 20", False),
    ("cat > nuevo.txt <<'EOF'\ncat grande.md\nEOF", False),
    ("cat grande.md # --permitir-lectura-completa", False),
])
def test_hook_bash(repo, monkeypatch, cmd, bloquea):
    ev = {"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": str(repo)}
    codigo, _ = _decide(ev, repo, monkeypatch)
    assert codigo == (2 if bloquea else 0)


def test_hook_read_y_registro(repo, monkeypatch):
    ev = {"tool_name": "Read", "session_id": "s1", "cwd": str(repo),
          "tool_input": {"file_path": str(repo / "grande.md")}}
    assert _decide(ev, repo, monkeypatch)[0] == 2
    ev["tool_input"]["limit"] = 50
    assert _decide(ev, repo, monkeypatch)[0] == 0
    _decide({"tool_name": "Bash", "cwd": str(repo), "tool_input":
             {"command": "cat grande.md # --permitir-lectura-completa"}}, repo, monkeypatch)
    filas = (repo / hook_lectura.REGISTRO).read_text().splitlines()
    assert filas[0].startswith("fecha\tsesion")
    assert [f.split("\t")[3] for f in filas[1:]] == ["BLOQUEO", "ESCAPE"]


def test_hook_proceso_sale_2():
    ev = json.dumps({"tool_name": "Bash", "tool_input": {"command": "git log -p"}})
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(RAIZ / "tests"))  # registro fuera del árbol real
    p = subprocess.run([sys.executable, str(RAIZ / "tools/hook_lectura.py")], input=ev,
                       capture_output=True, text=True, env=env)
    assert p.returncode == 2 and "consulta.py" in p.stderr


def test_settings_cablea_hook_y_arranque():
    s = json.loads((RAIZ / ".claude/settings.json").read_text())
    pre = s["hooks"]["PreToolUse"][0]
    assert pre["matcher"] == "Bash|Read"
    assert "hook_lectura.py" in pre["hooks"][0]["command"]
    cmds = [h["command"] for h in s["hooks"]["SessionStart"][0]["hooks"]]
    assert any("entorno.py\" --arranque" in c for c in cmds)
    assert any("arranque_memoria.py" in c for c in cmds)


def test_agents_espejo_de_reglas():
    agents = (RAIZ / "AGENTS.md").read_text(encoding="utf-8")
    m = re.search(r"<!-- REGLAS-DE-LECTURA:INICIO[^\n]*-->\n(.*?)<!-- REGLAS-DE-LECTURA:FIN -->",
                  agents, re.S)
    assert m, "AGENTS.md sin bloque espejo"
    assert m.group(1) == (RAIZ / "canon/REGLAS-DE-LECTURA.md").read_text(encoding="utf-8")
    claude = (RAIZ / "CLAUDE.md").read_text(encoding="utf-8")
    assert "@canon/REGLAS-DE-LECTURA.md" in claude
    assert "@canon/MEMORIA-OPERATIVA.md" in claude
    assert "canon/MEMORIA-OPERATIVA.md" in agents


def test_memoria_cabe_y_bloque_coincide():
    texto = memoria_operativa.MEM and open(memoria_operativa.MEM, encoding="utf-8").read()
    assert texto.count("\n") <= memoria_operativa.MAX_LINEAS
    assert texto == memoria_operativa.memoria_con(memoria_operativa.bloque())


def test_fecha_firma():
    assert str(memoria_operativa.fecha_firma("24/sep/2026, verbatim")) == "2026-09-24"
    assert memoria_operativa.fecha_firma("sin fecha") is None


def test_pyproject_igual_a_requirements():
    """Una lista de dependencias, dos formatos: si divergen, uv.lock miente."""
    req = [l.split("#")[0].strip() for l in
           (RAIZ / "requirements.txt").read_text(encoding="utf-8").splitlines()]
    req = sorted(r for r in req if r)
    py = (RAIZ / "pyproject.toml").read_text(encoding="utf-8")
    bloque = py[py.index("dependencies = ["):py.index("]", py.index("dependencies = ["))]
    assert sorted(re.findall(r'"([^"]+)"', bloque)) == req
    assert (RAIZ / "uv.lock").is_file()
