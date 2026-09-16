#!/usr/bin/env python3
"""Regresiones dirigidas del correctivo de la rutina de derivados."""

from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "deriva_cron.sh"
RESUMEN = ROOT / "tools" / "deriva_resumen.py"
LAUNCHER = ROOT / "tools" / "adquiere_launcher.sh"
SHA_A = "a" * 64
SHA_B = "b" * 64


def run(*args: str, cwd: Path | None = None, env: dict | None = None) -> subprocess.CompletedProcess:
    effective = dict(os.environ)
    effective.update(env or {})
    return subprocess.run(args, cwd=cwd, env=effective, text=True,
                          capture_output=True, timeout=30)


def write_tsv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, delimiter="\t", fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


class ResumenTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.nuevo = self.root / "nuevo.json"
        self.t0 = self.root / "t0.json"
        self.fechado = self.root / "fechado.json"
        self.universo = self.root / "universo.tsv"
        self.ledger = self.root / "ledger.tsv"
        conteos = {
            "cota_superior_activos_declarados": 10,
            "identidades_locales_verificadas": 2,
            "numerador_adquirido_identidades_locales_verificadas": 2,
        }
        self.nuevo.write_text(json.dumps({"snapshot_t0_sha256": SHA_B, "conteos": conteos}), encoding="utf-8")
        self.t0.write_text(json.dumps({"snapshot_t0_sha256": SHA_A, "conteos": dict(conteos, identidades_locales_verificadas=1, numerador_adquirido_identidades_locales_verificadas=1)}), encoding="utf-8")
        write_tsv(self.universo, ["hash_local"], [{"hash_local": SHA_A}, {"hash_local": SHA_B}])
        write_tsv(self.ledger, ["sha256", "estado_terminal"], [
            {"sha256": SHA_A, "estado_terminal": "SI"},
            {"sha256": SHA_B, "estado_terminal": "NO"},
        ])

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def command(self, anterior: Path, salida: Path) -> subprocess.CompletedProcess:
        return run("python3", str(RESUMEN), "--nuevo", str(self.nuevo),
                   "--anterior", str(anterior), "--universo-tsv", str(self.universo),
                   "--ledger", str(self.ledger), "--fecha", "2026-09-16",
                   "--salida", str(salida), cwd=ROOT)

    def test_t0_y_fechado_se_comparan_y_repeticion_es_idempotente(self) -> None:
        first = self.command(self.t0, self.fechado)
        self.assertEqual(first.returncode, 0, first.stderr)
        doc = json.loads(self.fechado.read_text(encoding="utf-8"))
        self.assertEqual(doc["snapshot_sha256_del_dia"], SHA_B)
        self.assertEqual(doc["conteos_operativos"]["adquiridos_identidades_sha256"], 2)
        self.assertEqual(doc["conteos_operativos"]["inspeccionados_identidades_sha256"], 1)
        self.assertNotIn("porcentaje_inspeccion", doc["conteos_operativos"])
        self.assertIn("no se publica porcentaje", doc["conteos_operativos"]["reserva_denominador"])
        siguiente = self.root / "universo-2026-09-16-r02.json"
        second = self.command(self.fechado, siguiente)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertFalse(siguiente.exists(), second.stdout)

    def test_huella_ausente_o_invalida_es_fallo_explicito(self) -> None:
        for bad in ({"conteos": {}}, {"snapshot_sha256_del_dia": "no-es-sha", "conteos": {}}):
            self.t0.write_text(json.dumps(bad), encoding="utf-8")
            result = self.command(self.t0, self.fechado)
            self.assertNotEqual(result.returncode, 0)
            self.assertRegex(result.stderr, "HUELLA_(AUSENTE|INVALIDA)")


class RamaYFallosTest(unittest.TestCase):
    def test_resumen_revisionado_es_la_referencia_mas_reciente(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            derivados = Path(td)
            (derivados / "universo-2026-09-16.json").touch()
            revision = derivados / "universo-2026-09-16-r02.json"
            revision.touch()
            script = textwrap.dedent(f"""\
                export DERIVA_CRON_SOLO_DEFINE=1 DERIVA_LOG_ROOT=$(mktemp -d)
                source '{RUNNER}'
                DERIVADOS_DIR='{derivados}'
                ultimo_resumen_universo
            """)
            result = run("bash", "-c", script, cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(Path(result.stdout.strip()), revision)

    def test_rama_diaria_antigua_absorbe_main_y_repeticion_conserva_commit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); bare = root / "origin.git"; work = root / "work"
            self.assertEqual(run("git", "init", "--bare", str(bare)).returncode, 0)
            self.assertEqual(run("git", "clone", str(bare), str(work)).returncode, 0)
            run("git", "config", "user.email", "fixture@example.invalid", cwd=work)
            run("git", "config", "user.name", "Fixture", cwd=work)
            (work / "base").write_text("base\n"); run("git", "add", "base", cwd=work); run("git", "commit", "-m", "base", cwd=work)
            run("git", "branch", "-M", "main", cwd=work); run("git", "push", "-u", "origin", "main", cwd=work)
            run("git", "switch", "-c", "derivados/2026-09-16", cwd=work)
            (work / "diario").write_text("pendiente\n"); run("git", "add", "diario", cwd=work); run("git", "commit", "-m", "diario", cwd=work)
            daily = run("git", "rev-parse", "HEAD", cwd=work).stdout.strip(); run("git", "push", "origin", "HEAD", cwd=work)
            run("git", "switch", "main", cwd=work); (work / "nuevo-main").write_text("nuevo\n"); run("git", "add", "nuevo-main", cwd=work); run("git", "commit", "-m", "main nuevo", cwd=work); run("git", "push", "origin", "main", cwd=work)
            main = run("git", "rev-parse", "HEAD", cwd=work).stdout.strip()
            script = textwrap.dedent(f"""\
                export DERIVA_CRON_SOLO_DEFINE=1 DERIVA_FECHA=2026-09-16
                source '{RUNNER}'
                cd '{work}'
                RAMA='derivados/2026-09-16'; LOGFILE='{root / 'sync.log'}'
                sincroniza_rama_diaria '{main}' origin/main
                git merge-base --is-ancestor '{daily}' HEAD
                git merge-base --is-ancestor '{main}' HEAD
                git push origin HEAD:refs/heads/derivados/2026-09-16
                first=$(git rev-parse HEAD)
                sincroniza_rama_diaria '{main}' origin/main
                test "$first" = "$(git rev-parse HEAD)"
            """)
            result = run("bash", "-c", script, cwd=ROOT)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_cada_paso_obligatorio_propaga_fallo(self) -> None:
        for phase in ("SUITE", "UNIVERSO", "TABLERO", "REGISTRO", "PUBLICACION"):
            script = textwrap.dedent(f"""\
                export DERIVA_CRON_SOLO_DEFINE=1 DERIVA_LOG_ROOT=$(mktemp -d)
                source '{RUNNER}'
                falla() {{ return 7; }}
                paso_obligatorio '{phase}' falla
            """)
            result = run("bash", "-c", script, cwd=ROOT)
            self.assertEqual(result.returncode, 7, f"{phase}: {result.stdout}{result.stderr}")
            self.assertIn(f"PARO-{phase}", result.stdout + result.stderr)


class LauncherTest(unittest.TestCase):
    def test_revision_publicada_ausente_se_obtiene_antes_del_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); bare = root / "origin.git"; seed = root / "seed"; clone = root / "clone"
            marker = root / "deriva-ejecutada"
            self.assertEqual(run("git", "init", "--bare", str(bare)).returncode, 0)
            self.assertEqual(run("git", "clone", str(bare), str(seed)).returncode, 0)
            run("git", "config", "user.email", "fixture@example.invalid", cwd=seed)
            run("git", "config", "user.name", "Fixture", cwd=seed)
            (seed / "tools").mkdir(); (seed / "forense/adq-log/estado").mkdir(parents=True)
            shutil.copy2(LAUNCHER, seed / "tools/adquiere_launcher.sh")
            (seed / "tools/deriva_cron.sh").write_text(
                f"#!/bin/sh\ntouch '{marker}'\nexit 0\n", encoding="utf-8")
            (seed / "tools/deriva_cron.sh").chmod(0o755)
            run("git", "add", ".", cwd=seed); run("git", "commit", "-m", "main", cwd=seed)
            run("git", "branch", "-M", "main", cwd=seed); run("git", "push", "-u", "origin", "main", cwd=seed)
            run("git", "switch", "-c", "despliegue", cwd=seed)
            (seed / "revision").write_text("publicada\n", encoding="utf-8")
            run("git", "add", "revision", cwd=seed); run("git", "commit", "-m", "revision", cwd=seed)
            revision = run("git", "rev-parse", "HEAD", cwd=seed).stdout.strip()
            run("git", "push", "origin", "despliegue", cwd=seed)
            self.assertEqual(run("git", "clone", "--no-local", "--single-branch", "--branch", "main",
                                 str(bare), str(clone)).returncode, 0)
            self.assertNotEqual(run("git", "cat-file", "-e", f"{revision}^{{commit}}", cwd=clone).returncode, 0)
            result = run("bash", "tools/adquiere_launcher.sh", cwd=clone, env={
                "ADQ_DEPLOY_REVISION": revision, "MM_TRAMO": "derivacion",
                "ADQ_DISPARADOR": "prueba",
            })
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(run("git", "rev-parse", "HEAD", cwd=clone).stdout.strip(), revision)
            self.assertTrue(marker.exists())

    def test_derivacion_corre_aunque_adquisicion_no_tenga_despacho(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); (root / "tools").mkdir(); (root / "forense/adq-log/estado").mkdir(parents=True)
            shutil.copy2(LAUNCHER, root / "tools/adquiere_launcher.sh")
            marker = root / "deriva-ejecutada"
            (root / "tools/deriva_cron.sh").write_text(f"#!/bin/sh\ntouch '{marker}'\nexit 0\n", encoding="utf-8")
            (root / "tools/deriva_cron.sh").chmod(0o755)
            (root / "tools/adquiere_cron.sh").write_text("#!/bin/sh\nexit 99\n", encoding="utf-8")
            (root / "tools/adq_investigacion.py").write_text(textwrap.dedent("""\
                import json, sys
                if '--recupera-presupuesto' in sys.argv:
                    print(json.dumps({'recuperacion_pendiente': []})); raise SystemExit(0)
                print(json.dumps({'razones': []})); raise SystemExit(10)
            """), encoding="utf-8")
            bindir = root / "bin"; bindir.mkdir()
            (bindir / "git").write_text(textwrap.dedent("""\
                #!/bin/sh
                case "$1" in
                  rev-parse) printf '%064d\n' 0;;
                  fetch|merge-base|checkout) exit 0;;
                  *) exit 0;;
                esac
            """), encoding="utf-8"); (bindir / "git").chmod(0o755)
            result = run("bash", str(root / "tools/adquiere_launcher.sh"), cwd=root, env={
                "PATH": f"{bindir}:{os.environ['PATH']}",
                "ADQ_COMPROBACION_LIGERA": "1", "MM_TRAMO": "ambos",
            })
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(marker.exists(), "el tramo determinista quedó condicionado al despacho")
            self.assertNotIn("99", (root / "forense/adq-log/launcher.log").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
