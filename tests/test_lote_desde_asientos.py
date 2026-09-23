#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de `tools/lote_desde_asientos.py` -- ACTO
GEN2-TUBERIA-CANAL-PUBLICACION-1 (22/sep/2026), P1.

Corre standalone (`python3 tests/test_lote_desde_asientos.py`) y expone
`corre() -> list[str]` (lista de fallos, vacía si pasa) -- mismo patrón que
`tests/test_marcador_segmento.py`.

Casos:
  A · el parser del diff (`calc_ids_anadidos`): sólo líneas AÑADIDAS
      cuentan; una línea QUITADA no aporta calc_id; la cabecera repetida
      (archivo nuevo desde cero) se descarta; sin duplicados; orden de
      aparición.
  B · `lote_desde_diff` extremo a extremo, con git DE VERDAD en un repo
      temporal: dos asientos nuevos en el push, uno de un CALC con sello
      (entra al lote) y otro de un CALC sin sello.json (se descarta, no
      se calla -- va en `descartados`, con razón). Un tercer asiento que
      sólo EDITA una fila existente (no la añade) no entra al lote: sólo
      lo que el push realmente asentó de nuevo.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def _carga_modulo():
    spec = importlib.util.spec_from_file_location(
        "lote_desde_asientos", RAIZ / "tools" / "lote_desde_asientos.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _git(cwd, *args):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} falló: {r.stderr}")
    return r.stdout


def ok(nombre, condicion, detalle=""):
    estado = "OK" if condicion else "FALLA"
    print(f"  [{estado}] {nombre}" + (f" -- {detalle}" if detalle and not condicion else ""))
    return None if condicion else f"{nombre}: {detalle}"


def caso_A(m, fails):
    print("A · calc_ids_anadidos, sólo líneas añadidas")
    diff = (
        "diff --git a/forense/replay-evidencia.tsv b/forense/replay-evidencia.tsv\n"
        "--- a/forense/replay-evidencia.tsv\n"
        "+++ b/forense/replay-evidencia.tsv\n"
        "@@ -1,3 +1,4 @@\n"
        " calc_id\tcorrida_id\tresultado_replay\n"
        "-CALC-VIEJO-0001\tCALC-VIEJO-0001--aaa\tREPRODUCE\n"
        "+CALC-VIEJO-0001\tCALC-VIEJO-0001--bbb\tREPRODUCE\n"
        "+CALC-NUEVO-0001\tCALC-NUEVO-0001--ccc\tREPRODUCE\n"
        "+CALC-NUEVO-0001\tCALC-NUEVO-0001--ccc\tREPRODUCE\n"
    )
    ids = m.calc_ids_anadidos(diff)
    fails.append(ok("A1 sólo añadidas, sin la quitada, sin duplicar",
                     ids == ["CALC-VIEJO-0001", "CALC-NUEVO-0001"], str(ids)))

    diff_archivo_nuevo = (
        "diff --git a/forense/replay-evidencia.tsv b/forense/replay-evidencia.tsv\n"
        "new file mode 100644\n"
        "--- /dev/null\n"
        "+++ b/forense/replay-evidencia.tsv\n"
        "@@ -0,0 +1,2 @@\n"
        "+calc_id\tcorrida_id\n"
        "+CALC-A-0001\tCALC-A-0001--x\n"
    )
    ids2 = m.calc_ids_anadidos(diff_archivo_nuevo)
    fails.append(ok("A2 cabecera repetida como añadida se descarta",
                     ids2 == ["CALC-A-0001"], str(ids2)))


def caso_B(m, fails):
    print("B · lote_desde_diff extremo a extremo, git real")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _git(tmp, "init", "-q", "-b", "main")
        _git(tmp, "config", "user.email", "t@t")
        _git(tmp, "config", "user.name", "t")

        (tmp / "forense").mkdir()
        cab = "calc_id\tcorrida_id\tresultado_replay\tcontexto_replay\n"
        base_fila = "CALC-YA-PUBLICADO-0001\tCALC-YA-PUBLICADO-0001--aaa\tREPRODUCE\tIDENTICO\n"
        (tmp / "forense" / "replay-evidencia.tsv").write_text(cab + base_fila, encoding="utf-8")
        _git(tmp, "add", "-A")
        _git(tmp, "commit", "-qm", "base")
        antes = _git(tmp, "rev-parse", "HEAD").strip()

        # CALC-CON-SELLO: `sello.json` vacío (nada que cubrir, nada que
        # discordar) + su sidecar `sello.sha256` sellado DE VERDAD con la
        # CLI real -- `_verifica_sello()` exige el sidecar, no basta con que
        # `sello.json` exista. Califica para el lote.
        d_con_sello = tmp / "data" / "corrida0" / "CALC-CON-SELLO-0001"
        d_con_sello.mkdir(parents=True)
        (d_con_sello / "sello.json").write_text("{}", encoding="utf-8")
        _sella = subprocess.run(
            [sys.executable, str(RAIZ / "tools" / "sella_sha256.py"),
             str(d_con_sello / "sello.json")],
            capture_output=True, text=True)
        assert _sella.returncode == 0, _sella.stderr
        # CALC-SIN-SELLO: carpeta existe, sin sello.json -- se descarta.
        (tmp / "data" / "corrida0" / "CALC-SIN-SELLO-0001").mkdir(parents=True)

        nueva_edita = "CALC-YA-PUBLICADO-0001\tCALC-YA-PUBLICADO-0001--aaa\tREPRODUCE\tDISTINTO\n"
        nueva_con_sello = "CALC-CON-SELLO-0001\tCALC-CON-SELLO-0001--bbb\tREPRODUCE\tIDENTICO\n"
        nueva_sin_sello = "CALC-SIN-SELLO-0001\tCALC-SIN-SELLO-0001--ccc\tREPRODUCE\tIDENTICO\n"
        (tmp / "forense" / "replay-evidencia.tsv").write_text(
            cab + nueva_edita + nueva_con_sello + nueva_sin_sello, encoding="utf-8")
        _git(tmp, "add", "-A")
        _git(tmp, "commit", "-qm", "push con dos asientos nuevos y una edicion")
        despues = _git(tmp, "rev-parse", "HEAD").strip()

        salida = m.lote_desde_diff(antes, despues, cwd=tmp,
                                   corridas_dir=tmp / "data" / "corrida0")

    fails.append(ok("B1 sólo el CALC con sello entra al lote",
                     salida["calc_ids"] == ["CALC-CON-SELLO-0001"],
                     json.dumps(salida, ensure_ascii=False)))
    razones = {d["calc_id"]: d["razon"] for d in salida["descartados"]}
    fails.append(ok("B2 el sin sello se descarta con razón, no se calla",
                     "CALC-SIN-SELLO-0001" in razones
                     and "SIN-SELLO" in razones["CALC-SIN-SELLO-0001"],
                     json.dumps(razones, ensure_ascii=False)))
    fails.append(ok("B3 la edición en su sitio (no asiento nuevo) no entra",
                     "CALC-YA-PUBLICADO-0001" not in salida["calc_ids"],
                     str(salida["calc_ids"])))
    fails.append(ok("B4 examinados cuenta los tres candidatos del diff (A.13)",
                     salida["examinados"] == 3, str(salida)))


def caso_C(m, fails):
    print("C · recuperación de asientos sellados ausentes de la vista")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        (tmp / "forense").mkdir()
        corridas = tmp / "data" / "corrida0"
        corridas.mkdir(parents=True)
        (tmp / "forense" / "replay-evidencia.tsv").write_text(
            "calc_id\tcorrida_id\n"
            "CALC-PUBLICADO\tpub--x\n"
            "CALC-PENDIENTE\tpend--x\n"
            "CALC-PENDIENTE\tpend--x\n"
            "CALC-SIN-SELLO\tsin--x\n", encoding="utf-8")
        (corridas / "corridas.tsv").write_text(
            "# DERIVADO — NO EDITAR\ncorrida_id\tspec_id\n"
            "pub--x\tCALC-PUBLICADO\n", encoding="utf-8")
        sellado = corridas / "CALC-PENDIENTE"
        sellado.mkdir()
        (sellado / "sello.json").write_text("{}", encoding="utf-8")
        sella = subprocess.run(
            [sys.executable, str(RAIZ / "tools" / "sella_sha256.py"),
             str(sellado / "sello.json")], capture_output=True, text=True)
        assert sella.returncode == 0, sella.stderr
        salida = m.lote_pendiente(cwd=tmp, corridas_dir=corridas)
    fails.append(ok("C1 sólo el asiento ausente y sellado entra una vez",
                     salida["calc_ids"] == ["CALC-PENDIENTE"], str(salida)))
    fails.append(ok("C2 el ausente sin sello queda declarado",
                     salida["descartados"] == [{"calc_id": "CALC-SIN-SELLO",
                                                "razon": "SIN-SELLO: pendiente sin sello válido"}],
                     str(salida)))


def corre() -> list[str]:
    m = _carga_modulo()
    fails: list[str] = []
    caso_A(m, fails)
    caso_B(m, fails)
    caso_C(m, fails)
    return [f for f in fails if f]


if __name__ == "__main__":
    fallos = corre()
    if fallos:
        print(f"\n{len(fallos)} FALLO(S):")
        for f in fallos:
            print(f"  - {f}")
        sys.exit(1)
    print("\nOK -- todos los casos pasan")
