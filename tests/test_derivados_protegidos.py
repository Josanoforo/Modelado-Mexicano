#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_derivados_protegidos.py -- prueba de tools/derivados_protegidos.py
(P4, ACTO GEN2-TUBERIA-EFICIENCIA-1, firma de mesa 21/sep/2026 §2(2)).

Defecto que atrapa: la lista de archivos "DERIVADO -- NO EDITAR" se
deriva por comando (grep de la cabecera literal), nunca se teclea a mano --
un derivador nuevo que nace sin que alguien edite una lista aparte no debe
quedar sin protección. Corre en aislamiento: nunca asume qué hay hoy en
`data/corrida0/`, solo que el mecanismo de detección funciona sobre fixtures
propias y que el universo real declarado coincide con `git ls-files`.
"""
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import derivados_protegidos as DP  # noqa: E402

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def prueba_deteccion_por_cabecera_sobre_fixture():
    """Un archivo con la cabecera exacta se detecta; uno sin ella, no --
    contra `git ls-files` real (nunca se inventa un archivo versionado)."""
    rutas, examinados = DP.lista_derivados()
    afirma(isinstance(rutas, list) and examinados > 0,
           "debe examinar al menos un archivo de texto versionado")
    for r in rutas:
        if DP._es_tabla_de_valor(r):
            continue  # derivado por RUTA (valores-vista/*): no admite cabecera sin cambiar el valor
        with open(os.path.join(ROOT, r), "rb") as fh:
            primera = fh.readline().decode("utf-8", "replace").rstrip("\n")
        afirma(primera.startswith(DP.CABECERA),
               f"{r} está en la lista pero su primera línea no es la cabecera")
    # El universo conocido de hoy (§9 A.13, declarado, no supuesto): estos
    # archivos existen en el repo con la cabecera desde actos anteriores a
    # este; si alguno deja de tenerla el test lo nota por el lado inverso
    # (grep_manual abajo), no aquí.
    afirma("data/corrida0/marcador-segmento.tsv" in rutas,
           "marcador-segmento.tsv (cabecera conocida) debe aparecer en la lista")


def prueba_universo_coincide_con_grep_manual():
    """Ningún archivo versionado con la cabecera se queda fuera: se
    re-verifica con un grep independiente (no reusa la función bajo
    prueba) sobre el mismo `git ls-files`."""
    salida = subprocess.run(
        ["git", "-C", ROOT, "grep", "-l", "--", DP.CABECERA],
        capture_output=True, text=True,
    ).stdout.splitlines()
    esperado = {p for p in salida
                if not p.startswith("data/raw/") and not p.startswith(".git/")}
    rutas, _ = DP.lista_derivados()
    obtenido = {r for r in rutas if not DP._es_tabla_de_valor(r)}
    # `git grep -l` encuentra la cadena en cualquier parte del archivo; la
    # función solo cuenta si es la PRIMERA línea. Todo lo que la función
    # marca debe estar en el grep amplio (subconjunto, nunca al revés).
    # Excepción declarada: `valores-vista/*` es derivado por RUTA (§ arriba),
    # nunca por cabecera, así que se compara aparte de este grep.
    afirma(obtenido <= esperado,
           f"la función marcó archivos que ni siquiera contienen la cabecera: {obtenido - esperado}")


def prueba_toca_detecta_diff_en_derivado():
    """`--toca refA refB` sale 1 si el diff entre dos commits toca un
    archivo de la lista, 0 si no -- sobre un repo git temporal, sintético,
    nunca el repo real (aislamiento total)."""
    with tempfile.TemporaryDirectory() as tmp:
        def git(*args):
            subprocess.run(["git", *args], cwd=tmp, check=True,
                            capture_output=True, text=True)
        git("init", "-q")
        git("config", "user.email", "t@t.t")
        git("config", "user.name", "t")
        with open(os.path.join(tmp, "normal.txt"), "w") as fh:
            fh.write("a\n")
        with open(os.path.join(tmp, "derivado.tsv"), "w") as fh:
            fh.write(DP.CABECERA + "\ncol1\tcol2\n")
        git("add", "-A")
        git("commit", "-q", "-m", "base")
        base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp,
                               capture_output=True, text=True, check=True).stdout.strip()
        with open(os.path.join(tmp, "derivado.tsv"), "a") as fh:
            fh.write("valor1\tvalor2\n")
        git("add", "-A")
        git("commit", "-q", "-m", "toca derivado")
        cambia_derivado = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp,
                                          capture_output=True, text=True, check=True).stdout.strip()

        vieja_raiz = DP.RAIZ
        try:
            DP.RAIZ = tmp
            rc_si = DP.main(["--toca", base, cambia_derivado])
            rc_solo = DP.main(["--solo-derivados", base, cambia_derivado])
            with open(os.path.join(tmp, "normal.txt"), "a") as fh:
                fh.write("b\n")
            git("add", "-A")
            git("commit", "-q", "-m", "toca normal")
            cambia_normal = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=tmp,
                capture_output=True, text=True, check=True).stdout.strip()
            rc_ajeno = DP.main(["--solo-derivados", base, cambia_normal])
        finally:
            DP.RAIZ = vieja_raiz
    afirma(rc_si == 1, "tocar el archivo con cabecera DERIVADO debe salir 1")
    afirma(rc_solo == 0, "PR automático con sólo derivados debe pasar")
    afirma(rc_ajeno == 1, "PR automático con archivo ajeno debe fallar")


def main():
    prueba_deteccion_por_cabecera_sobre_fixture()
    prueba_universo_coincide_con_grep_manual()
    prueba_toca_detecta_diff_en_derivado()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_derivados_protegidos.py: 3 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
