#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test de `tools/adq_config.py` (P6, ACTO ADQ-CRON-V2). Fixture propia en
un archivo temporal -- nunca lee ni depende del contenido real de
`data/adq-config.yaml`, para que un cambio de mesa a los ids de la PDN no
pueda romper esta prueba.

Corre sola:

    python3 tests/test_adq_config.py
"""
import io
import sys
import tempfile
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import adq_config as AC  # noqa: E402

FAILS = []

FIXTURE = """
zona_horaria: America/Mexico_City
claude_timeout_segundos: 900
pdn:
  ventana_dia_inicio: 1
  ventana_dia_fin: 3
  sistemas:
    s1:
      url: "https://example.org/s1"
      sis_descarga: s1
      id_manifiesto: fixture_s1
"""


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def prueba_obten_escalar_y_anidado():
    with tempfile.TemporaryDirectory() as td:
        ruta = os.path.join(td, "adq-config.yaml")
        io.open(ruta, "w", encoding="utf-8").write(FIXTURE)
        cfg = AC.cargar(ruta)
        afirma(AC.obten("claude_timeout_segundos", cfg) == 900,
               "escalar de primer nivel debe resolver")
        afirma(AC.obten("pdn.sistemas.s1.url", cfg) == "https://example.org/s1",
               "ruta punteada anidada debe resolver")
        afirma(AC.obten("pdn.sistemas.s1.id_manifiesto", cfg) == "fixture_s1",
               "última hoja de la ruta debe resolver")


def prueba_clave_ausente_lanza_keyerror():
    with tempfile.TemporaryDirectory() as td:
        ruta = os.path.join(td, "adq-config.yaml")
        io.open(ruta, "w", encoding="utf-8").write(FIXTURE)
        cfg = AC.cargar(ruta)
        try:
            AC.obten("pdn.sistemas.s99.url", cfg)
            afirma(False, "una clave ausente debe lanzar KeyError, no devolver None")
        except KeyError as e:
            afirma("s99" in str(e), f"el KeyError debe nombrar el tramo que faltó, dio: {e}")


def prueba_cli_imprime_valor():
    with tempfile.TemporaryDirectory() as td:
        ruta = os.path.join(td, "adq-config.yaml")
        io.open(ruta, "w", encoding="utf-8").write(FIXTURE)
        ruta_orig = AC.RUTA_CONFIG
        AC.RUTA_CONFIG = ruta
        salida = io.StringIO()
        stdout_bak = sys.stdout
        sys.stdout = salida
        try:
            codigo = AC.main(["claude_timeout_segundos"])
        finally:
            sys.stdout = stdout_bak
            AC.RUTA_CONFIG = ruta_orig
        afirma(codigo == 0, f"CLI debe salir 0 para una clave válida, dio {codigo}")
        afirma(salida.getvalue().strip() == "900",
               f"CLI debe imprimir el valor crudo, dio {salida.getvalue()!r}")


def main():
    prueba_obten_escalar_y_anidado()
    prueba_clave_ausente_lanza_keyerror()
    prueba_cli_imprime_valor()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_adq_config.py: 3 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
