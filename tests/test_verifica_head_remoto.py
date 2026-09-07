#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_verifica_head_remoto.py -- tools/verifica_head_remoto.py.
ACTO AUTOMATIZA-2-A · BLINDA-HEAD-PR.

Sin red real: el "remoto" es un repo `--bare` en una ruta de archivo local
(`git ls-remote` sobre una ruta local no toca la red). Demuestra los cinco
estados del guard, cada uno mapeado directamente a su exit code:

  test_sincronizado_tras_push
      local == remoto tras push -> 0 PR_HEAD_SINCRONIZADO. Éste es el
      estado que un PR debe alcanzar antes de declararse listo para mesa.

  test_commit_local_sin_push_desactualizado
      un commit local que nunca se empujó dejaría a mesa fusionando un
      HEAD viejo -- exactamente el defecto real de PR #572 -- ->
      2 PR_HEAD_DESACTUALIZADO.

  test_push_vuelve_a_sincronizar
      tras el push del commit del caso anterior, el guard vuelve a
      0 PR_HEAD_SINCRONIZADO -- no es un estado permanente, es del
      momento en que se corre.

  test_rama_ausente
      se pide una rama que el remoto (real, respondiendo) no tiene ->
      3 RAMA_AUSENTE_EN_ORIGIN. No es lo mismo que "remoto no
      verificable": aquí `ls-remote` sí funcionó.

  test_remoto_no_verificable
      `--remote` apunta a una ruta que no resuelve a ningún repo ->
      4 HEAD_REMOTO_NO_VERIFICABLE. `ls-remote` en sí falla.

Corre solo:
    python3 tests/test_verifica_head_remoto.py
"""
import os
import subprocess
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO_ROOT, "tools", "verifica_head_remoto.py")


def _run_git(args, cwd):
    r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    assert r.returncode == 0, "git {} fallo: {}".format(args, r.stderr)
    return r.stdout.strip()


def _init_local_con_remoto(tmp, branch="rama-prueba"):
    """Bare remoto en tmp/remoto.git + working repo en tmp/local con
    `origin` apuntando a esa ruta de archivo (sin red)."""
    remoto = os.path.join(tmp, "remoto.git")
    local = os.path.join(tmp, "local")
    os.makedirs(local, exist_ok=True)
    subprocess.run(["git", "init", "--bare", "-q", remoto], check=True)
    _run_git(["init", "-q", "-b", branch], cwd=local)
    _run_git(["config", "user.email", "t@example.com"], cwd=local)
    _run_git(["config", "user.name", "t"], cwd=local)
    _run_git(["remote", "add", "origin", remoto], cwd=local)
    with open(os.path.join(local, "a.txt"), "w") as f:
        f.write("uno\n")
    _run_git(["add", "a.txt"], cwd=local)
    _run_git(["commit", "-q", "-m", "commit inicial"], cwd=local)
    _run_git(["push", "-u", "-q", "origin", branch], cwd=local)
    return local, remoto, branch


def _correr_tool(local, extra_args):
    r = subprocess.run(
        [sys.executable, TOOL] + extra_args,
        cwd=local, capture_output=True, text=True,
    )
    return r.returncode, r.stdout


def test_sincronizado_tras_push():
    with tempfile.TemporaryDirectory() as tmp:
        local, _remoto, branch = _init_local_con_remoto(tmp)
        codigo, salida = _correr_tool(local, ["--branch", branch])
        assert codigo == 0, salida
        assert "PR_HEAD_SINCRONIZADO" in salida
        assert "refs_examinadas=1" in salida


def test_commit_local_sin_push_desactualizado():
    with tempfile.TemporaryDirectory() as tmp:
        local, _remoto, branch = _init_local_con_remoto(tmp)
        with open(os.path.join(local, "b.txt"), "w") as f:
            f.write("dos\n")
        _run_git(["add", "b.txt"], cwd=local)
        _run_git(["commit", "-q", "-m", "segundo commit, sin empujar"], cwd=local)
        codigo, salida = _correr_tool(local, ["--branch", branch])
        assert codigo == 2, salida
        assert "PR_HEAD_DESACTUALIZADO" in salida
        assert "NO FUSIONAR" in salida


def test_push_vuelve_a_sincronizar():
    with tempfile.TemporaryDirectory() as tmp:
        local, _remoto, branch = _init_local_con_remoto(tmp)
        with open(os.path.join(local, "b.txt"), "w") as f:
            f.write("dos\n")
        _run_git(["add", "b.txt"], cwd=local)
        _run_git(["commit", "-q", "-m", "segundo commit"], cwd=local)
        codigo, _ = _correr_tool(local, ["--branch", branch])
        assert codigo == 2
        _run_git(["push", "-q", "origin", branch], cwd=local)
        codigo, salida = _correr_tool(local, ["--branch", branch])
        assert codigo == 0, salida
        assert "PR_HEAD_SINCRONIZADO" in salida


def test_rama_ausente():
    with tempfile.TemporaryDirectory() as tmp:
        local, _remoto, _branch = _init_local_con_remoto(tmp)
        codigo, salida = _correr_tool(local, ["--branch", "rama-que-no-existe"])
        assert codigo == 3, salida
        assert "RAMA_AUSENTE_EN_ORIGIN" in salida
        assert "refs_examinadas=0" in salida
        assert "NO FUSIONAR" in salida


def test_remoto_no_verificable():
    with tempfile.TemporaryDirectory() as tmp:
        local, _remoto, branch = _init_local_con_remoto(tmp)
        ruta_inexistente = os.path.join(tmp, "no-existe.git")
        codigo, salida = _correr_tool(
            local, ["--remote", ruta_inexistente, "--branch", branch]
        )
        assert codigo == 4, salida
        assert "HEAD_REMOTO_NO_VERIFICABLE" in salida
        assert "NO FUSIONAR" in salida


def main():
    casos = [
        test_sincronizado_tras_push,
        test_commit_local_sin_push_desactualizado,
        test_push_vuelve_a_sincronizar,
        test_rama_ausente,
        test_remoto_no_verificable,
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
