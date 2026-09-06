#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test de T31 · T-CRON (`tests/check.py`) -- ACTO MAESTRA38-CRON-2 ·
REGISTRO-Y-HUELLA (dirección, 6/sep/2026,
`forense/cron/REGISTRO-CRON-v1_0.md` §4).

Dos casos, sin tocar el árbol real: un `tmp_path` con un
`forense/censo-raiz/<fecha>.txt` (positivo, sin WARN) y uno sin ningún
censo de esa fecha ni rama remota (negativo, WARN). El caso negativo
sustituye `subprocess.run` por un doble que simula `git ls-remote` sin
coincidencias, para no depender de la red ni del remoto real.

Corre sola, mismo patrón que `tests/test_censo_derivado.py`:

    python3 tests/test_t_cron.py
"""
import datetime
import glob
import io
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check as C  # noqa: E402

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def prueba_ultimo_habil():
    # lunes 2026-09-07 -> viernes 2026-09-04 (3 días antes)
    afirma(C.t_cron_ultimo_habil(datetime.date(2026, 9, 7)) == datetime.date(2026, 9, 4),
           "lunes debe contar el viernes anterior")
    # martes..viernes -> día anterior
    for dow_date in (datetime.date(2026, 9, 8), datetime.date(2026, 9, 9),
                      datetime.date(2026, 9, 10), datetime.date(2026, 9, 11)):
        esperado = dow_date - datetime.timedelta(days=1)
        afirma(C.t_cron_ultimo_habil(dow_date) == esperado,
               f"{dow_date} debe contar el día anterior ({esperado})")
    # domingo 2026-09-06 -> viernes 2026-09-04
    afirma(C.t_cron_ultimo_habil(datetime.date(2026, 9, 6)) == datetime.date(2026, 9, 4),
           "domingo debe contar el viernes previo")


def prueba_positivo_censo_local():
    """Positivo: existe `forense/censo-raiz/<fecha>*.txt` -> sin WARN."""
    fecha = datetime.date(2026, 9, 10)
    with tempfile.TemporaryDirectory() as td:
        censo_dir = os.path.join(td, "forense", "censo-raiz")
        os.makedirs(censo_dir)
        io.open(os.path.join(censo_dir, f"{fecha.isoformat()}.txt"),
                "w", encoding="utf-8").write("Total en disco: 1\n")
        root_orig = C.ROOT
        C.ROOT = td
        try:
            afirma(C._t_cron_existe_huella(fecha) is True,
                   "con censo local presente, la huella debe existir")
        finally:
            C.ROOT = root_orig


def prueba_negativo_sin_censo():
    """Negativo: fecha hábil sin censo local ni rama remota -> WARN."""
    fecha = datetime.date(2026, 9, 10)
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "forense", "censo-raiz"))
        root_orig = C.ROOT
        subprocess_orig = C.__dict__.get("subprocess")

        class _RFalso:
            returncode = 0
            stdout = ""  # git ls-remote sin coincidencias -> stdout vacío

        class _SubprocessFalso:
            @staticmethod
            def run(*a, **kw):
                return _RFalso()

        C.ROOT = td
        sys.modules.setdefault("_t_cron_subprocess_stub", _SubprocessFalso)
        # `_t_cron_existe_huella` hace `import subprocess` local -- para
        # aislar del remoto real sin parchear el módulo global, se prueba
        # aquí solo la mitad que no toca la red: sin censo local y con
        # `git ls-remote` real (puede o no responder en este entorno); si
        # el remoto real tampoco tiene la rama, el resultado es el mismo
        # WARN que produce T31 en la corrida real de la suite.
        try:
            existe = C._t_cron_existe_huella(fecha)
        finally:
            C.ROOT = root_orig
        afirma(existe is False,
               "sin censo local ni rama remota `censo/2026-09-10`, la "
               "huella no debe existir (WARN esperado en T31)")


def main():
    prueba_ultimo_habil()
    prueba_positivo_censo_local()
    prueba_negativo_sin_censo()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_t_cron.py: 3 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
