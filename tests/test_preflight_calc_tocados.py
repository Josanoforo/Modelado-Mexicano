#!/usr/bin/env python3
"""Prueba por MUTACIÓN de `tools/preflight_calc_tocados.py`.

ACTO GEN2-TUBERIA-PREFLIGHT-CI-1 (21/sep/2026).

Un chequeo que sólo se prueba contra el árbol real prueba el árbol, no el
chequeo: hoy pasa porque hoy no hay defecto. Aquí se FABRICA cada uno de los
tres defectos ya observados (#781, #903, #926) y cada uno de los estados
legítimos, sobre CALC SINTÉTICOS en un repo git temporal — nunca sobre los
CALC reales, que este acto no toca.

El repo temporal se arma con `git archive HEAD tools milpa tests
requirements.txt`: `tools/corrida0.py` importa `milpa.src.emisor` y
`tests/payload_resolver` en su cabecera, así que copiar sólo `tools/` no
arranca. No se copia `data/corrida0`: el universo del repo temporal son
exclusivamente los CALC que esta prueba fabrica.

Se corre solo: `python3 tests/test_preflight_calc_tocados.py`
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))

import preflight_calc_tocados as P  # noqa: E402

FALLOS: list[str] = []


def afirma(ok: bool, etiqueta: str, detalle: str = "") -> None:
    print(f"  [{'OK  ' if ok else 'FALL'}] {etiqueta}"
          + (f"   {detalle}" if detalle and not ok else ""))
    if not ok:
        FALLOS.append(etiqueta)


# ---------------------------------------------------------------- utilidades

def git(cwd: Path, *args: str) -> str:
    r = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                       text=True, check=True)
    return r.stdout


def sha256(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


SPEC_MD = "# spec sintética de prueba\n\nNo mide nada. Existe para que `preflight` tenga qué hashear.\n"

# El molde LIMPIO: pasa `preflight` sin un solo bloqueo. Cada mutación de
# abajo le quita o le tuerce exactamente una cosa.
MOLDE = """calc_id: {calc}
spec_md: spec.md
spec_md_sha256: {sha_md}
script: data/corrida0/{calc}/medidor.py

inputs:
  - {{id: insumo_sintetico, origen: repo, ruta: data/corrida0/{calc}/insumo.txt, sha256: {sha_in}}}

variables: []
universo: "Universo sintético: ninguna persona real."
filtros: "Ninguno."
ponderador: NO-APLICA
transformacion: "Ninguna."
estimando: "Ninguno: este CALC no mide."
dependencias_materiales: []

parametros: {{proposito: prueba-por-mutacion}}
seed: {{aplica: false}}
tolerancia: {{tipo: determinista, abs: 0.0}}

resultados:
  - {{id: RESULT-SINTETICO-1, tipo: entero, unidad: conteo}}
"""


def escribe_calc(repo: Path, calc: str, *, quita_spec_md=False,
                 spec_md_como_ruta_raiz=False, quita_seed=False,
                 quita_medidor=False, input_ausente=False,
                 sellado=False) -> None:
    """Fabrica un CALC sintético. Cada bandera es UNA mutación."""
    d = repo / "data" / "corrida0" / calc
    d.mkdir(parents=True, exist_ok=True)
    (d / "insumo.txt").write_text("insumo sintético\n", encoding="utf-8")
    if not quita_medidor:
        (d / "medidor.py").write_text("# medidor sintético\n", encoding="utf-8")
    if not quita_spec_md:
        (d / "spec.md").write_text(SPEC_MD, encoding="utf-8")

    spec = MOLDE.format(calc=calc, sha_md=sha256(SPEC_MD),
                        sha_in=sha256("insumo sintético\n"))
    if spec_md_como_ruta_raiz:
        # El defecto de #926, exacto: la ruta se escribe desde la raíz del
        # repo, y `preflight` la resuelve relativa al directorio del CALC.
        spec = spec.replace(
            "spec_md: spec.md",
            f"spec_md: forense/prereg-caja/{calc}-spec-v1_1.md")
    if quita_seed:
        # El defecto de #903: campo obligatorio ausente.
        spec = spec.replace("seed: {aplica: false}\n", "")
    if input_ausente:
        (d / "insumo.txt").unlink()
    (d / "spec.yaml").write_text(spec, encoding="utf-8")
    if sellado:
        (d / "sello.json").write_text("{}\n", encoding="utf-8")
        (d / "sello.sha256").write_text("0\n", encoding="utf-8")


def arma_repo(tmp: Path) -> Path:
    repo = tmp / "repo"
    repo.mkdir()
    tar = subprocess.Popen(
        ["git", "archive", "HEAD", "tools", "milpa", "tests", "requirements.txt"],
        cwd=str(RAIZ), stdout=subprocess.PIPE)
    subprocess.run(["tar", "-x", "-C", str(repo)], stdin=tar.stdout, check=True)
    tar.wait()
    # El archivo bajo prueba se copia del ÁRBOL, no de `HEAD`: la prueba tiene
    # que ejercitar la versión que esta sesión está escribiendo, no la última
    # commiteada (que en el primer commit del acto todavía no existe).
    shutil.copy2(RAIZ / "tools" / "preflight_calc_tocados.py",
                 repo / "tools" / "preflight_calc_tocados.py")
    (repo / ".gitignore").write_text("__pycache__/\n*.pyc\n", encoding="utf-8")
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "prueba@sintetica.local")
    git(repo, "config", "user.name", "prueba sintetica")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "base sintética")
    return repo


def corre(repo: Path, base: str, cabeza: str = "HEAD") -> tuple[int, str]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run(
        [sys.executable, "tools/preflight_calc_tocados.py",
         "--base", base, "--cabeza", cabeza],
        cwd=str(repo), capture_output=True, text=True, env=env)
    return r.returncode, r.stdout + r.stderr


# ------------------------------------------------- 1 · clasificación pura

def prueba_clasificacion() -> None:
    print("\n1 · CLASIFICACIÓN de bloqueos (lista cerrada de legítimos)")
    casos_warn = [
        "script_ausente=tools/x.py",
        "input_repo_ausente=r1:data/x.json",
        "input_repo_no_commiteado=r1",
        "input_manifiesto_AUSENTE=enigh2022_nc_csv",
        "input_manifiesto_RAIZ-NO-CONFIGURADA=x",
        "spec_md_sha256_discorda_origin_main",
    ]
    for b in casos_warn:
        clase, _ = P.clasifica(b)
        afirma(clase == P.WARN, f"WARN · {b}", f"dio {clase}")

    casos_fail = [
        "ausente=data/corrida0/CALC-X/spec.md",          # #781 y #926
        "spec_sin_seed",                                  # #903
        "spec_sin_tolerancia",
        "spec_md_sha256_discorda_arbol",
        "input_repo_sin_sha_declarado=r1",
        "input_repo_sha_discorda=r1",
        "campo_sustantivo_ausente=estimando",
        "calc_id_discorda(spec=CALC-A, dir=CALC-B)",
        "no_commiteado=data/corrida0/CALC-X/spec.yaml",
        "seed_dict_sin_aplica",
        "resultado_sin_unidad=#1",
        "ids_resultados_duplicados=['r1']",
        "tolerancia_sin_tipo",
        # Un bloqueo que hoy no existe: si dirección añade uno, este chequeo
        # lo trata como `preflight` lo trata, sin que nadie lo edite.
        "bloqueo_inventado_que_no_esta_en_ninguna_lista=x",
    ]
    for b in casos_fail:
        clase, _ = P.clasifica(b)
        afirma(clase == P.FAIL, f"FAIL · {b}", f"dio {clase}")

    for b in ("calc_ya_sellado=CALC-INMUTABLE-YA-SELLADO",
              "sello_previo_incompatible=SELLO_NO_COINCIDE",
              "working_tree_dirty=SI"):
        clase, _ = P.clasifica(b)
        afirma(clase == P.FUERA, f"FUERA-DE-ALCANCE · {b}", f"dio {clase}")

    # Cada estado legítimo trae su razón escrita, no una cadena vacía.
    for tabla in (P.ESTADOS_LEGITIMOS, P.PREFIJOS_LEGITIMOS, P.FUERA_DE_ALCANCE):
        for tok, razon in tabla.items():
            afirma(len(razon) > 30, f"razón declarada para `{tok}`")


# --------------------------------------------- 2 · mutación de punta a punta

def prueba_mutacion(repo: Path) -> None:
    base = git(repo, "rev-parse", "HEAD").strip()

    def rama(nombre: str, fabrica) -> tuple[int, str]:
        git(repo, "checkout", "-q", "-B", nombre, base)
        fabrica()
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", nombre)
        return corre(repo, base)

    print("\n2 · UNIVERSO VACÍO")
    cod, sal = rama("vacio", lambda: (repo / "tools" / "nota.txt")
                    .write_text("un cambio que no toca ningún CALC\n", encoding="utf-8"))
    afirma(cod == 0, "universo vacío: pasa", sal)
    afirma("0 CALC sin sello tocados" in sal, "universo vacío: lo dice", sal)

    print("\n3 · CALC LIMPIO")
    cod, sal = rama("limpio", lambda: escribe_calc(repo, "CALC-SINT-LIMPIO-0001"))
    afirma(cod == 0, "CALC limpio: pasa", sal)
    afirma("VERDE" in sal, "CALC limpio: preflight VERDE", sal)

    print("\n4 · LOS TRES DEFECTOS YA OBSERVADOS → FAIL")
    cod, sal = rama("d926", lambda: escribe_calc(
        repo, "CALC-SINT-D926-0001", spec_md_como_ruta_raiz=True))
    afirma(cod == 1, "#926 · spec_md que no resuelve: rojo", sal)
    afirma("FAIL" in sal and "ausente=" in sal, "#926 · el rojo dice qué lo puso rojo", sal)

    cod, sal = rama("d903", lambda: escribe_calc(
        repo, "CALC-SINT-D903-0001", quita_seed=True))
    afirma(cod == 1, "#903 · campo obligatorio ausente: rojo", sal)
    afirma("spec_sin_seed" in sal, "#903 · nombra `spec_sin_seed`", sal)

    cod, sal = rama("d781", lambda: escribe_calc(
        repo, "CALC-SINT-D781-0001", quita_spec_md=True))
    afirma(cod == 1, "#781 · sin spec.md: rojo", sal)
    afirma("spec.md" in sal, "#781 · nombra el archivo ausente", sal)

    print("\n5 · ESTADOS LEGÍTIMOS → WARN, nunca rojo")
    cod, sal = rama("warn_script", lambda: escribe_calc(
        repo, "CALC-SINT-SINMEDIDOR-0001", quita_medidor=True))
    afirma(cod == 0, "sólo script_ausente: pasa", sal)
    afirma("WARN" in sal and "script_ausente" in sal, "sólo script_ausente: WARN", sal)

    cod, sal = rama("warn_input", lambda: escribe_calc(
        repo, "CALC-SINT-CADENA-0001", input_ausente=True))
    afirma(cod == 0, "sólo input_repo_ausente: pasa", sal)
    afirma("WARN" in sal and "input_repo_ausente" in sal,
           "sólo input_repo_ausente: WARN", sal)

    print("\n6 · UN CALC SELLADO NO ENTRA AL UNIVERSO")
    cod, sal = rama("sellado", lambda: escribe_calc(
        repo, "CALC-SINT-SELLADO-0001", quita_seed=True, sellado=True))
    afirma(cod == 0, "CALC sellado con defecto: no entra, pasa", sal)
    afirma("0 CALC sin sello tocados" in sal, "CALC sellado: universo vacío", sal)

    print("\n7 · EL CHEQUEO NO ESCRIBE EN EL ÁRBOL QUE VERIFICA (D-23)")
    git(repo, "checkout", "-q", "-B", "nosucio", base)
    escribe_calc(repo, "CALC-SINT-NOSUCIO-0001")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "nosucio")
    cod, sal = corre(repo, base)
    sucio = git(repo, "status", "--porcelain").strip()
    afirma(sucio == "", "árbol limpio después de correr el chequeo", repr(sucio))
    afirma("working_tree_dirty" not in sal,
           "no aparece working_tree_dirty fabricado por el chequeo", sal)


def main() -> int:
    print("T-PREFLIGHT-CALC-TOCADOS · prueba por mutación "
          "(ACTO GEN2-TUBERIA-PREFLIGHT-CI-1)")
    prueba_clasificacion()
    tmp = Path(tempfile.mkdtemp(prefix="preflight-calc-tocados-"))
    try:
        repo = arma_repo(tmp)
        prueba_mutacion(repo)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"\nRESULTADO: {'FALLOS=' + str(len(FALLOS)) if FALLOS else 'VERDE'}")
    for f in FALLOS:
        print(f"  · {f}")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
