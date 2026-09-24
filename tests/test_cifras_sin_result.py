#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_cifras_sin_result.py -- tools/recibo/cifras_sin_result.py.

ACTO GEN2-AUDITORIA-POST-HOC-ASTRA-1, pieza P1. Prueba dirigida contra un
repo git sintetico (no el repo real) para que el defecto que motivo la
segunda version del detector -- confundir "sin cita RESULT-* en la MISMA
LINEA" con "sin ninguna traza en el archivo" -- no vuelva sin que un test
lo note. Verificado a mano contra `CALC-ENDIREH-PISOS-2021-AYUDA-0001`
(real, en `forense/replay-evidencia.tsv`) antes de escribir este test;
aqui se reproduce el mismo patron en miniatura.

Corre solo:
    python3 tests/test_cifras_sin_result.py
"""
import os
import subprocess
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO_ROOT, "tools", "recibo", "cifras_sin_result.py")


def _git(cwd, *args):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)
    return r.stdout


def _correr_tool(cwd, merge, extra=()):
    env = dict(os.environ, CIFRAS_SIN_RESULT_RAIZ=cwd)
    r = subprocess.run(
        [sys.executable, TOOL, merge, "--json", *extra],
        cwd=cwd, capture_output=True, text=True, env=env,
    )
    return r.returncode, r.stdout, r.stderr


def _repo_sintetico(tmp):
    """Arma un repo git de un solo archivo bajo forense/analisis/ con dos
    commits: base sin cifras, merge que añade una tabla con una cifra
    citada por RESULT- en OTRA linea del mismo archivo (patron real)."""
    _git(tmp, "init", "-q")
    _git(tmp, "config", "user.email", "test@example.com")
    _git(tmp, "config", "user.name", "test")
    os.makedirs(os.path.join(tmp, "forense", "analisis"), exist_ok=True)
    ruta = os.path.join(tmp, "forense", "analisis", "demo.md")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("# Demo\n")
    _git(tmp, "add", ".")
    _git(tmp, "commit", "-q", "-m", "base")
    base = _git(tmp, "rev-parse", "HEAD").strip()

    with open(ruta, "w", encoding="utf-8") as f:
        f.write("# Demo\nResultado sellado RESULT-DEMO-0001.\n\n| fila | 42 |\n")
    _git(tmp, "add", ".")
    _git(tmp, "commit", "-q", "-m", "con cita en otra linea")
    con_cita = _git(tmp, "rev-parse", "HEAD").strip()

    return base, con_cita, ruta


def test_cifra_con_cita_en_otra_linea_no_marca_sin_traza():
    with tempfile.TemporaryDirectory() as tmp:
        _base, con_cita, _ruta = _repo_sintetico(tmp)
        codigo, salida, err = _correr_tool(tmp, con_cita)
        assert codigo == 0, f"tool fallo: {err}"
        import json
        r = json.loads(salida)
        assert r["archivos_con_cifras_nuevas"] == 1, r
        assert r["archivos_sin_result"] == 0, (
            "el detector confundio 'sin cita en la misma linea' con "
            f"'sin traza en el archivo': {r}"
        )


def test_cifra_sin_ninguna_traza_si_marca():
    with tempfile.TemporaryDirectory() as tmp:
        _git(tmp, "init", "-q")
        _git(tmp, "config", "user.email", "test@example.com")
        _git(tmp, "config", "user.name", "test")
        os.makedirs(os.path.join(tmp, "forense", "analisis"), exist_ok=True)
        ruta = os.path.join(tmp, "forense", "analisis", "demo.md")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("# Demo\n")
        _git(tmp, "add", ".")
        _git(tmp, "commit", "-q", "-m", "base")

        with open(ruta, "w", encoding="utf-8") as f:
            f.write("# Demo\n\n| fila | 42 |\n")
        _git(tmp, "add", ".")
        _git(tmp, "commit", "-q", "-m", "sin ninguna cita")
        sin_cita = _git(tmp, "rev-parse", "HEAD").strip()

        codigo, salida, err = _correr_tool(tmp, sin_cita)
        assert codigo == 0, f"tool fallo: {err}"
        import json
        r = json.loads(salida)
        assert r["archivos_sin_result"] == 1, r


def test_ci_guardias_excluido():
    with tempfile.TemporaryDirectory() as tmp:
        _git(tmp, "init", "-q")
        _git(tmp, "config", "user.email", "test@example.com")
        _git(tmp, "config", "user.name", "test")
        os.makedirs(os.path.join(tmp, "forense", "analisis", "ci-guardias"), exist_ok=True)
        ruta = os.path.join(tmp, "forense", "analisis", "ci-guardias", "censo.tsv")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("col\n")
        _git(tmp, "add", ".")
        _git(tmp, "commit", "-q", "-m", "base")

        with open(ruta, "w", encoding="utf-8") as f:
            f.write("col\n0.1\n")
        _git(tmp, "add", ".")
        _git(tmp, "commit", "-q", "-m", "runtime de test, no evidencia")
        merge = _git(tmp, "rev-parse", "HEAD").strip()

        codigo, salida, err = _correr_tool(tmp, merge)
        assert codigo == 0, f"tool fallo: {err}"
        import json
        r = json.loads(salida)
        assert r["archivos_con_cifras_nuevas"] == 0, (
            f"ci-guardias/ deberia excluirse: {r}"
        )


def test_autoprueba_interna_verde():
    r = subprocess.run(
        [sys.executable, TOOL, "--autoprueba"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "AUTOPRUEBA VERDE" in r.stdout


def main():
    casos = [
        test_cifra_con_cita_en_otra_linea_no_marca_sin_traza,
        test_cifra_sin_ninguna_traza_si_marca,
        test_ci_guardias_excluido,
        test_autoprueba_interna_verde,
    ]
    fallos = 0
    for caso in casos:
        try:
            caso()
            print("OK   {}".format(caso.__name__))
        except AssertionError as e:
            fallos += 1
            print("FAIL {}: {}".format(caso.__name__, e))
    print("---")
    if fallos:
        print("{} de {} casos FALLARON".format(fallos, len(casos)))
        return 1
    print("{} casos OK".format(len(casos)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
