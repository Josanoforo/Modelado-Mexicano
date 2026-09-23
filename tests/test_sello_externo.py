#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test de `tools/sello_externo.py` (GEN2-TUBERIA-SELLO-EXTERNO-1). Fixture
propia con un repo git sintético en un directorio temporal -- nunca depende
del contenido real de data/corrida0/ ni forense/prereg-caja/, para que el
crecimiento del corpus real no pueda romper esta prueba.

Corre sola:

    python3 tests/test_sello_externo.py
"""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def _sh(cwd, *args):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} -> {r.stderr}")
    return r.stdout.strip()


def _repo_sintetico(td):
    repo = Path(td) / "repo"
    repo.mkdir()
    _sh(repo, "init", "-q", "-b", "main")
    _sh(repo, "config", "user.email", "fixture@example.org")
    _sh(repo, "config", "user.name", "fixture")
    (repo / "README.md").write_text("fixture\n")
    _sh(repo, "add", "-A")
    _sh(repo, "commit", "-q", "-m", "raíz del repo fixture")

    (repo / "data" / "corrida0" / "CALC-FIX-0001").mkdir(parents=True)
    (repo / "data" / "corrida0" / "CALC-FIX-0001" / "sello.json").write_text('{"x": "1"}\n')
    _sh(repo, "checkout", "-q", "-b", "rama-a")
    _sh(repo, "add", "-A")
    _sh(repo, "commit", "-q", "-m", "añade sello fixture CALC-FIX-0001")
    _sh(repo, "checkout", "-q", "main")
    _sh(repo, "merge", "--no-ff", "-q", "-m", "Merge pull request #7 from x/rama-a", "rama-a")

    (repo / "forense" / "prereg-caja").mkdir(parents=True)
    (repo / "forense" / "prereg-caja" / "FIX-spec-v1_0.sha256").write_text("deadbeef  algo\n")
    _sh(repo, "checkout", "-q", "-b", "rama-b")
    _sh(repo, "add", "-A")
    _sh(repo, "commit", "-q", "-m", "añade sidecar fixture FIX-spec-v1_0")
    _sh(repo, "checkout", "-q", "main")
    _sh(repo, "merge", "--no-ff", "-q", "-m", "Merge pull request #8 from x/rama-b", "rama-b")
    return repo


def prueba_censa_filas_y_pr():
    import sello_externo as SE

    with tempfile.TemporaryDirectory() as td:
        repo = _repo_sintetico(td)
        orig_root = SE.REPO_ROOT
        SE.REPO_ROOT = repo
        try:
            filas = SE.censa_filas(base_ref="main")
        finally:
            SE.REPO_ROOT = orig_root

        afirma(len(filas) == 2, f"debe censar los dos sellos fixture, dio {len(filas)}")
        por_id = {f["id"]: f for f in filas}
        afirma(por_id["CALC-FIX-0001"]["tipo"] == "CALC", "CALC-FIX-0001 debe tipar CALC")
        afirma(por_id["CALC-FIX-0001"]["pr"] == "7", f"PR del primer sello debe ser 7, dio {por_id['CALC-FIX-0001']['pr']}")
        afirma(por_id["FIX-spec-v1_0"]["tipo"] == "SPEC", "FIX-spec-v1_0 debe tipar SPEC")
        afirma(por_id["FIX-spec-v1_0"]["pr"] == "8", f"PR del segundo sello debe ser 8, dio {por_id['FIX-spec-v1_0']['pr']}")
        sha_esperado = hashlib.sha256((repo / "data/corrida0/CALC-FIX-0001/sello.json").read_bytes()).hexdigest()
        afirma(por_id["CALC-FIX-0001"]["sha256"] == sha_esperado,
               "sha256 del sello debe calcularse sobre el archivo, no inventarse")
        afirma(por_id["CALC-FIX-0001"]["firma_gpg_estado"] == "N"
               and por_id["CALC-FIX-0001"]["firma_gpg_keyid"] == "SIN-LLAVE",
               f"merge sin firmar debe declararlo, no inventar una llave, dio {por_id['CALC-FIX-0001']}")


def prueba_manifiesto_determinista():
    import sello_externo as SE

    with tempfile.TemporaryDirectory() as td:
        repo = _repo_sintetico(td)
        orig_root = SE.REPO_ROOT
        SE.REPO_ROOT = repo
        try:
            filas1 = SE.censa_filas(base_ref="main")
            filas2 = SE.censa_filas(base_ref="main")
            destino = repo / "m.tsv"
            sha1 = SE.escribe_manifiesto(filas1, destino)
            sha2 = SE.escribe_manifiesto(filas2, destino)
        finally:
            SE.REPO_ROOT = orig_root
        afirma(sha1 == sha2, f"dos corridas sobre el mismo árbol deben dar el mismo sha256, dio {sha1} != {sha2}")
        afirma("sha256-manifiesto" in destino.read_text(), "el manifiesto debe traer su propio sha256 al final")


def prueba_stamp_solo_delta():
    import sello_externo as SE

    with tempfile.TemporaryDirectory() as td:
        repo = _repo_sintetico(td)
        anterior = repo / "anterior.tsv"
        anterior.write_text("tipo\tid\truta\tsha256\ncommit\nfecha_commit\npr\nmerged_at\n")
        anterior.write_text(
            "tipo\tid\truta\tsha256\tcommit\tfecha_commit\tpr\tmerged_at\n"
            "CALC\tCALC-FIX-0001\tdata/corrida0/CALC-FIX-0001/sello.json\tabc\tdead\tX\t7\tX\n"
        )
        orig_root = SE.REPO_ROOT
        SE.REPO_ROOT = repo
        try:
            filas = SE.censa_filas(base_ref="main")
            anteriores_ids = {(f["tipo"], f["id"]) for f in SE.lee_manifiesto(anterior)}
            delta = [f for f in filas if (f["tipo"], f["id"]) not in anteriores_ids]
        finally:
            SE.REPO_ROOT = orig_root
        afirma(len(delta) == 1 and delta[0]["id"] == "FIX-spec-v1_0",
               f"el delta debe traer solo el sello nuevo, dio {[f['id'] for f in delta]}")


def main():
    prueba_censa_filas_y_pr()
    prueba_manifiesto_determinista()
    prueba_stamp_solo_delta()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_sello_externo.py: 3 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
