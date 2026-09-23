#!/usr/bin/env python3
"""Guardia de MONOTONÍA de `celdas_validadas` (ACTO
GEN2-TUBERIA-METRICA-RECTORA-1 · P4). QUÉ DEFECTO ATRAPA: un merge que borra
o descongela sin querer un veredicto sellado bajaría la métrica rectora sin
que nadie lo note -- E.3 dice que un veredicto sellado no se borra, y la
única bajada legítima es una fila `VENCIDO-EN-ALCANCE` de mesa (A.10). Sin
este guardia, esa bajada pasaría en silencio hasta que alguien comparara dos
digestos a mano.

N (últimos N merges de primer padre de `main` que se inspeccionan) lo decide
el ejecutor (D-19, latitud del encargo): se fija en `_N_MERGES` de abajo, con
su razón declarada. La derivación cuesta ~0.1 s por commit sobre archivos ya
en el árbol, pero medir un commit HISTÓRICO exige verlo con el código de ESE
commit (el módulo `celdas_validadas.py` no existía antes de este acto), así
que este test usa `git worktree` para revisar cada commit con su propio
árbol -- más caro que 0.1 s, y por eso N se mantiene moderado.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: Últimos N merges de primer padre de main que este guardia inspecciona.
#: 8: suficiente para cubrir varios días de actos sin volver la suite lenta
#: (cada commit revisado es un worktree + una corrida de script, no 0.1 s).
_N_MERGES = 8


def _sh(cmd, cwd=RAIZ, timeout=120):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True,
                        text=True, timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def _merges_recientes(n):
    rc, out, _ = _sh(f"git log --first-parent --merges -n {n} --format=%H origin/main")
    if rc != 0 or not out:
        rc, out, _ = _sh(f"git log --first-parent --merges -n {n} --format=%H HEAD")
    return [l for l in out.splitlines() if l.strip()]


def _total_en_commit(sha, tmproot):
    """Deriva `total_celdas_validadas` en el árbol de `sha`, usando un
    worktree desechable -- el módulo/función que exista EN ESE commit, no el
    de hoy. Devuelve None (NO-VERIFICABLE-AQUÍ) si ni el módulo nuevo ni la
    función vieja del tablero existen ahí."""
    wt = os.path.join(tmproot, sha[:12])
    rc, _, err = _sh(f"git worktree add --detach --force {wt} {sha}")
    if rc != 0:
        return None
    try:
        rc, out, _ = _sh(
            "python3 tools/celdas_validadas.py --json 2>/dev/null || true", cwd=wt)
        import json as _json
        if out.strip():
            try:
                d = _json.loads(out)
                if "total_celdas_validadas" in d:
                    return d["total_celdas_validadas"]
            except ValueError:
                pass
        # Commits anteriores a este acto: la función vivía en tablero_programa.py.
        rc, out, _ = _sh(
            "python3 -c \"import sys; sys.path.insert(0,'tools'); "
            "import json, tablero_programa as T; "
            "print(json.dumps(T._celdas_validadas()))\" 2>/dev/null || true", cwd=wt)
        if out.strip():
            try:
                d = _json.loads(out)
                return d.get("total_celdas_validadas")
            except ValueError:
                return None
        return None
    finally:
        _sh(f"git worktree remove --force {wt}")


def _vencido_en_alcance_entre(sha_antes, sha_despues):
    """Busca por OBJETO (A.10/A.17), no por defecto: ¿hay alguna fila
    VENCIDO-EN-ALCANCE nueva entre los dos commits en los registros de mesa?"""
    rc, out, _ = _sh(
        f"git diff {sha_antes}..{sha_despues} -- data/corrida0/decisiones.tsv "
        f"'forense/*.tsv' | grep -c 'VENCIDO-EN-ALCANCE' || true")
    try:
        return int(out.strip() or "0") > 0
    except ValueError:
        return False


@unittest.skipUnless(shutil.which("git"), "git no disponible")
class TestMonotoniaCeldasValidadas(unittest.TestCase):

    def test_no_baja_sin_vencido_en_alcance(self):
        shas = _merges_recientes(_N_MERGES)
        if len(shas) < 2:
            self.skipTest("menos de dos merges de primer padre disponibles -- "
                           "nada que comparar (NO-VERIFICABLE-AQUÍ)")
        # git log entrega del más nuevo al más viejo: se invierte para leer
        # la historia en orden cronológico.
        shas = list(reversed(shas))
        with tempfile.TemporaryDirectory(prefix="celdas-validadas-monotonia-") as tmp:
            totales = [(sha, _total_en_commit(sha, tmp)) for sha in shas]

        pares_verificables = [(a, b) for a, b in zip(totales, totales[1:])
                               if a[1] is not None and b[1] is not None]
        if not pares_verificables:
            self.skipTest("ningún par de commits consecutivos fue medible "
                           "(NO-VERIFICABLE-AQUÍ)")

        bajadas_sin_explicar = []
        for (sha_a, total_a), (sha_b, total_b) in pares_verificables:
            if total_b < total_a and not _vencido_en_alcance_entre(sha_a, sha_b):
                bajadas_sin_explicar.append(
                    f"{sha_a[:8]} ({total_a}) -> {sha_b[:8]} ({total_b}): "
                    "sin fila VENCIDO-EN-ALCANCE en decisiones.tsv/forense/*.tsv")

        self.assertFalse(
            bajadas_sin_explicar,
            "celdas_validadas bajó sin VENCIDO-EN-ALCANCE (E.3/A.10):\n" +
            "\n".join(bajadas_sin_explicar))


if __name__ == "__main__":
    unittest.main()
