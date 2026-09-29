#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_tablero_insumos.py -- ACTO GEN2-TUBERIA-TABLERO-INSUMOS-1 (29/sep/2026).

Guardia huérfana (D-21: entra por `ci_guardias --ejecuta-huerfanos`, sin editar verify.yml ni
check.py). D-14, por pieza: qué defecto real ya ocurrido atrapa y qué le costaba a un lector.

  (A) P1 · `corrida0._vista_publicada()`. Defecto: `status` publicaba contadores sin decir de
      cuándo eran; el último [deriva] fusionado era de las 10:20 del 28/sep, con otro en cola
      sin fusionar, y el puesto de tablero lo tuvo que inferir a mano. Casos sobre repos git
      sintéticos: commit y fecha del [deriva], una edición a mano de la vista NO cuenta, el
      merge de mesa lleva el [deriva] en el cuerpo, ramas derivados/auto-* (y no otras) en cola,
      y los tres NO-VERIFICABLE (sin refs de origin, sin [deriva], clon superficial).
  (B) P3 · `nc_por_clase`: un dueño EN-CURSO cuyo encargo ya está CONSUMIDO y cuya rama ya no
      vive es VENCIDA-CANDIDATA. Defecto: 42 NC decían «en curso» de cuatro actos ya fusionados
      (TUBERIA-3, CALC-ALTERNOS-LOTE-1, PISOS-DOMINIOS-Y-REGLAS-1, C1-SUCESORES-Y-LOTE-3) y el
      tablero las contaba como trabajo vivo. Sin ramas vivas (sin red) NO se adivina.
  (C) P4/P6 · dueños completos y DIRECCION. Defecto: de 27 filas ADQUISICION solo 6 nombraban
      una solicitud o una FP, y ninguna de las 18 APERTURA la FP que abriría su ola; un lector no
      sabía de qué objeto dependía cada una. Casos sobre datos sintéticos: lo citado debe existir
      y solo cuenta el dueño vigente (no lo que sigue a ` · antes:`).
  (D) El libro real: lista cada fila ABIERTA cuyo dueño no nombra su dato o está fuera de la lista
      cerrada. Las EXCEPCIONES (abajo) van con id y razón: cada una es «nadie ocupó la fila», no
      una derrota. Una fila nueva (fecha >= ACTIVACION) que incumpla FALLA; una anterior que no
      esté en la lista solo AVISA (D-16: los WARN se listan, no adjudican), para no romper a los
      actos que ya iban en vuelo cuando esta guardia nació.

Corre sola:  python3 tests/test_tablero_insumos.py
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
os.chdir(ROOT)

import corrida0 as C0  # noqa: E402
import nc_por_clase as NC  # noqa: E402

FALLAS = []


def afirma(cond, msg):
    if not cond:
        FALLAS.append(msg)


# ── (A) la fecha de la vista, sobre repos git sintéticos ────────────────────────────────────
USOS = "data/corrida0/usos.tsv"


def git(cwd, *args, fecha=None):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    if fecha:
        env["GIT_COMMITTER_DATE"] = env["GIT_AUTHOR_DATE"] = fecha
    r = subprocess.run(["git", *args], cwd=cwd, env=env, capture_output=True, text=True)
    assert r.returncode == 0, (args, r.stderr)
    return r.stdout.strip()


def escribe(dir_, ruta, texto):
    p = Path(dir_) / ruta
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")


def commit(dir_, asunto, ruta, texto, fecha="2026-09-28T09:00:00-0600"):
    escribe(dir_, ruta, texto)
    git(dir_, "add", "-A")
    git(dir_, "commit", "-q", "-m", asunto, fecha=fecha)
    return git(dir_, "rev-parse", "HEAD")


def repo_base(tmp):
    git(tmp, "init", "-q", "-b", "main")
    commit(tmp, "base", USOS, "v0\n", "2026-09-27T09:00:00-0600")


def con_origin(tmp):
    git(tmp, "remote", "add", "origin", "https://example.invalid/x.git")  # refspec de todas las ramas
    git(tmp, "update-ref", "refs/remotes/origin/main", "HEAD")
    for r in ("derivados/auto-111", "derivados/suite-9", "claude/x", "derivados/autonomo"):
        git(tmp, "update-ref", f"refs/remotes/origin/{r}", "HEAD")


def vista(dir_):
    viejo = C0.RAIZ
    C0.RAIZ = Path(dir_)
    try:
        return C0._vista_publicada()
    finally:
        C0.RAIZ = viejo


def caso_a():
    with tempfile.TemporaryDirectory() as t:
        repo_base(t)
        sha = commit(t, "[deriva] trozo 1 tras abc: 20 CALC, quedan 5 (#12)", USOS, "v1\n",
                     "2026-09-28T10:20:35-0600")
        commit(t, "otro cambio", "README.md", "x\n")
        con_origin(t)
        v = vista(t)
        afirma(v["vista_publicada_commit"] == sha, f"(A1) commit del [deriva]: {v}")
        afirma(v["vista_publicada_fecha"] == "2026-09-28T16:20:35Z", f"(A1) fecha en UTC: {v}")
        afirma(v["vista_publicada_commits_posteriores"] == "1", f"(A1) un PR fusionado después: {v}")
        # `derivados/suite-9`, `claude/x` y `derivados/autonomo` NO son un [deriva] en cola
        afirma(v["deriva_en_cola"] == 1, f"(A1) solo derivados/auto-* cuenta: {v}")
        afirma("sin red" in v["deriva_en_cola_fuente"], f"(A1) declara que no usó red: {v}")

        # (A2) una edición a mano de la vista NO es la vista publicada por el canal
        commit(t, "edita usos a mano", USOS, "v2 a mano\n")
        v2 = vista(t)
        afirma(v2["vista_publicada_commit"] == sha, f"(A2) un commit a mano no cuenta: {v2}")
        afirma(v2["vista_publicada_commits_posteriores"] == "2", f"(A2) dos después: {v2}")

        # (A6) clon superficial: el [deriva] queda más allá del borde -> NO-VERIFICABLE, no un cero
        with tempfile.TemporaryDirectory() as t2:
            git(t2, "clone", "-q", "--depth", "1", f"file://{t}", "clon")
            v6 = vista(os.path.join(t2, "clon"))
            afirma(v6["vista_publicada_commit"] == "NO-VERIFICABLE-CLON-SUPERFICIAL", f"(A6) superficial: {v6}")
            afirma(v6["deriva_en_cola"] == "NO-VERIFICABLE-CLON-DE-UNA-RAMA",
                   f"(A6) un clon de una rama no ve derivados/auto-*: no se dice 0: {v6}")


def caso_a3():
    """El merge de mesa (no squash) lleva el [deriva] en el cuerpo y es el commit publicado."""
    with tempfile.TemporaryDirectory() as t:
        repo_base(t)
        git(t, "checkout", "-q", "-b", "derivados/auto-9")
        commit(t, "[deriva] trozo 1 tras abc: 3 CALC, quedan 0", USOS, "v1\n", "2026-09-28T08:00:00-0600")
        git(t, "checkout", "-q", "main")
        git(t, "merge", "--no-ff", "-q", "derivados/auto-9", "-m",
            "Merge pull request #7 from x/derivados/auto-9\n\n[deriva] vistas generadas tras abc",
            fecha="2026-09-28T12:00:00-0600")
        head = git(t, "rev-parse", "HEAD")
        v = vista(t)
        afirma(v["vista_publicada_commit"] == head, f"(A3) el merge de mesa es la vista publicada: {v}")
        afirma(v["vista_publicada_fecha"] == "2026-09-28T18:00:00Z", f"(A3) fecha del merge, no del trozo: {v}")
        afirma(v["vista_publicada_commits_posteriores"] == "0", f"(A3) ninguno después: {v}")


def caso_a45():
    with tempfile.TemporaryDirectory() as t:
        repo_base(t)
        commit(t, "otro", "README.md", "x\n")
        v = vista(t)
        m = v["vista_publicada_commit"]
        afirma(m.startswith("NO-ENCONTRADO") and "2 commits" in m, f"(A5) sin [deriva]: se declara con conteo: {v}")
        afirma(v["deriva_en_cola"] == "NO-VERIFICABLE-SIN-REFS-DE-ORIGIN", f"(A4) sin refs de origin: {v}")
    with tempfile.TemporaryDirectory() as t:
        vs = vista(t)  # ni siquiera es un repo git
        afirma(vs["vista_publicada_commit"] == "NO-VERIFICABLE-SIN-GIT", f"(A7) sin git: {vs}")


# ── (B) VENCIDA-CANDIDATA ───────────────────────────────────────────────────────────────────
def caso_b():
    with tempfile.TemporaryDirectory() as t:
        cons, sin = Path(t, "consumido.md"), Path(t, "sin.md")
        cons.write_text("# encargo\n\n## CONSUMIDO\nPR #1\n", encoding="utf-8")
        sin.write_text("# encargo\n", encoding="utf-8")
        enc = {"GEN2-ACTO-X-1": str(cons), "GEN2-ACTO-Y-1": str(sin)}
        vivas = frozenset({"main", "acto/otra"})

        def clase(sucesor, v=vivas):
            r = {"sucesor": sucesor, "razon": "", "acto": "GEN2-OTRO-1"}
            return NC.clasifica(r, {}, enc, {}, v)

        c, _, _ = clase("EN-CURSO (GEN2-ACTO-X-1 · rama acto/x) · antes: nada")
        afirma(c == "VENCIDA-CANDIDATA", f"(B1) encargo CONSUMIDO y rama ausente: {c}")
        c, _, _ = clase("EN-CURSO (GEN2-ACTO-X-1 · rama acto/otra)")
        afirma(c == "EN-CURSO", f"(B2) rama viva: sigue en curso: {c}")
        c, _, _ = clase("EN-CURSO (GEN2-ACTO-Y-1 · rama acto/y)")
        afirma(c == "EN-CURSO", f"(B3) encargo sin CONSUMIDO: no está vencida: {c}")
        c, falta, ev = clase("EN-CURSO (GEN2-ACTO-X-1 · rama acto/x)", None)
        afirma(c == "EN-CURSO" and "NO-VERIFICABLE" in ev, f"(B4) sin ramas vivas no se adivina: {c} {ev}")
        c, _, _ = clase("EN-CURSO (GEN2-NO-EXISTE-9 · rama a/b)")
        afirma(c == "EN-CURSO", f"(B5) acto sin encargo archivado: no se adivina: {c}")
        c, _, _ = clase("DIRECCION (encargo por escribir: x) · antes: MESA (2026-10-05)")
        afirma(c == "ESPERA-DIRECCION", f"(B6) DIRECCION es un dueño de la lista cerrada: {c}")
    afirma(NC.ramas_vivas.__name__ == "ramas_vivas", "(B7) existe el lector de ramas vivas")


# ── (C) dueños completos ────────────────────────────────────────────────────────────────────
EXPEDIENTE = "forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21/04-INEGI-ENCIG-NC-0153.md"


def caso_c():
    cola = {"FUENTE_A": "SOLICITUD-PREPARADA"}
    obt = {("P1", "FUENTE-B"): "NO-OBTENIDO-POR-ESTE-AGENTE"}
    fps = {"FP-260928-X-abcd-01": "ABIERTA"}

    def d(s):
        return NC.dueno_incompleto(s, cola, obt, fps)

    afirma(os.path.isfile(EXPEDIENTE), f"(C0) el expediente real que usa el caso existe: {EXPEDIENTE}")
    for ok in ("ADQUISICION (x; solicitud: cola:FUENTE_A) · antes: y",
               "ADQUISICION (x; solicitud: obtencion:P1:FUENTE-B)",
               f"ADQUISICION (x; solicitud: {EXPEDIENTE})",
               "ADQUISICION (x; FP: FP-260928-X-abcd-01)",
               "APERTURA (ola; FP: FP-260928-X-abcd-01) · antes: y",
               "DIRECCION (encargo por escribir)", "MESA (2026-10-05) · z"):
        afirma(d(ok) is None, f"(C1) dueño completo debe pasar: {ok!r} -> {d(ok)}")
    afirma(d("ADQUISICION (x; solicitud: cola:NO_EXISTE)") == "ADQUISICION-SIN-SOLICITUD",
           "(C2) una cola: inexistente no cuenta")
    afirma(d("ADQUISICION (x; solicitud: obtencion:P9:NO-EXISTE)") == "ADQUISICION-SIN-SOLICITUD",
           "(C2) un par de obtencion inexistente no cuenta")
    afirma(d("ADQUISICION (x; solicitud: forense/expedientes-acceso/no-existe.md)") == "ADQUISICION-SIN-SOLICITUD",
           "(C2) una ruta inexistente no cuenta")
    afirma(d("ADQUISICION (x) · antes: cola:FUENTE_A") == "ADQUISICION-SIN-SOLICITUD",
           "(C3) lo citado en `antes:` no es el dueño vigente")
    afirma(d("APERTURA (ola)") == "APERTURA-SIN-FP", "(C4) APERTURA sin FP")
    afirma(d("APERTURA (ola; FP: FP-260928-X-abcd-99)") == "APERTURA-SIN-FP", "(C4) una FP inexistente no cuenta")
    afirma(d("primer [deriva] tras el merge de mesa") == "FUERA-DE-LA-LISTA-CERRADA", "(C5) prosa fuera de la lista")
    afirma(d("FP-260928-X-abcd-01") == "FUERA-DE-LA-LISTA-CERRADA", "(C5) una FP pelada no es un dueño")


# ── (D) el libro real ───────────────────────────────────────────────────────────────────────
ACTIVACION = "2026-09-29"  # filas nacidas desde este día deben cumplir; las anteriores solo avisan
EXCEPCIONES = {}  # id -> razón: «nadie ocupó la fila» (se listan en cada corrida)


def caso_d():
    fps, cola, obt = NC.estado_fps(), NC.cola_por_fuente(), NC.obtencion_por_par()
    abiertas = [r for r in NC.filas(NC.NC) if (r.get("estado") or "").strip() == "ABIERTA"]
    afirma(len(cola) > 900 and len(fps) > 600, f"(D0) leyó la cola ({len(cola)}) y las FP ({len(fps)})")
    incumplen = {}
    for r in abiertas:
        defecto = NC.dueno_incompleto(r["sucesor"], cola, obt, fps)
        if defecto:
            incumplen[r["id"]] = (defecto, r["fecha"])
    for fid, (defecto, fecha) in sorted(incumplen.items()):
        if fid in EXCEPCIONES:
            print(f"EXCEPCIÓN {fid} · {defecto} · {EXCEPCIONES[fid]}")
        elif fecha >= ACTIVACION:
            afirma(False, f"(D1) fila nueva sin dueño completo: {fid} ({defecto})")
        else:
            print(f"WARN {fid} · {defecto} (anterior a {ACTIVACION}: se lista, no adjudica)")
    for fid in sorted(set(EXCEPCIONES) - set(incumplen)):
        print(f"WARN excepción caducada (ya nombra su dato o ya no está ABIERTA): {fid}")
    n_adq = sum(1 for r in abiertas if r["sucesor"].startswith("ADQUISICION"))
    n_ape = sum(1 for r in abiertas if r["sucesor"].startswith("APERTURA"))
    ko = lambda tipo: sum(1 for i, (dfc, _) in incumplen.items() if dfc.startswith(tipo))  # noqa: E731
    print(f"ADQUISICION: {n_adq} ABIERTA · {ko('ADQUISICION')} sin solicitud ni FP | "
          f"APERTURA: {n_ape} ABIERTA · {ko('APERTURA')} sin FP | "
          f"fuera de la lista cerrada: {ko('FUERA')} | excepciones declaradas: {len(EXCEPCIONES)}")


def main():
    caso_a(); caso_a3(); caso_a45(); caso_b(); caso_c(); caso_d()
    if FALLAS:
        print(f"FALLA test_tablero_insumos: {len(FALLAS)}")
        for f in FALLAS:
            print("  ·", f)
        return 1
    print("OK test_tablero_insumos (A-D)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
