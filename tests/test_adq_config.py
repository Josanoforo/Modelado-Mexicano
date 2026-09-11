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
import datetime
import sys
import tempfile
import os
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import adq_config as AC  # noqa: E402

FAILS = []

FIXTURE = """
calendario:
  hora: "07:30"
  dias_semana: [lunes, martes, miercoles, jueves, viernes]
  zona_iana: America/Mexico_City
  zona_windows: Central Standard Time (Mexico)
  ventana_observacion_minutos: 45
claude_timeout_segundos: 900
claude_kill_after_segundos: 60
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


def prueba_calendario_normaliza_consumidores_y_proxima_hora():
    cfg = yaml.safe_load(FIXTURE)
    cal = AC.calendario(cfg=cfg)
    afirma(cal["weekdays"] == [0, 1, 2, 3, 4],
           f"días Python deben derivarse del YAML, dio {cal['weekdays']!r}")
    afirma(cal["dias_windows"] == ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
           f"días Windows deben derivarse del mismo YAML, dio {cal['dias_windows']!r}")
    # Viernes 08:00 de México: la siguiente es lunes 07:30, aunque el
    # instante de entrada venga en UTC y la zona del host sea irrelevante.
    ahora = datetime.datetime(2026, 9, 11, 14, 0, tzinfo=datetime.timezone.utc)
    proxima = AC.proxima_ejecucion(ahora, cal)
    afirma(proxima.isoformat() == "2026-09-14T07:30:00-06:00",
           f"próxima hora debe respetar días/zona configurados, dio {proxima.isoformat()}")


def prueba_cambio_dia_y_zona_sale_de_la_misma_autoridad():
    cfg = yaml.safe_load(FIXTURE)
    cfg["calendario"].update({"hora": "10:15", "dias_semana": ["sabado"],
                               "zona_iana": "UTC", "zona_windows": "UTC"})
    cal = AC.calendario(cfg=cfg)
    proxima = AC.proxima_ejecucion(
        datetime.datetime(2026, 9, 11, 23, 0, tzinfo=datetime.timezone.utc), cal)
    afirma(proxima.isoformat() == "2026-09-12T10:15:00+00:00",
           f"cambio de día/zona debe propagarse, dio {proxima.isoformat()}")
    afirma(cal["dias_windows"] == ["Saturday"], "instalador debe recibir Saturday")


def prueba_invalida_y_overrides_declaran_valor_aplicado():
    cfg = yaml.safe_load(FIXTURE)
    cfg["calendario"]["hora"] = "25:90"
    res = AC.calendario_resuelto(cfg=cfg)
    afirma(res["degradada"] and res["hora"] == "07:30" and "25:90" in res["causa"],
           f"config inválida debe declarar causa y respaldo, dio {res!r}")
    bueno = AC.entero_resuelto("claude_kill_after_segundos",
                               "CLAUDE_KILL_AFTER_SEGUNDOS", 60,
                               entorno={"CLAUDE_KILL_AFTER_SEGUNDOS": "7"}, cfg=cfg)
    afirma(bueno["valor"] == 7 and bueno["fuente"].startswith("env:"),
           f"override válido debe ganar, dio {bueno!r}")
    malo = AC.entero_resuelto("claude_kill_after_segundos",
                              "CLAUDE_KILL_AFTER_SEGUNDOS", 60,
                              entorno={"CLAUDE_KILL_AFTER_SEGUNDOS": "cero"}, cfg=cfg)
    afirma(malo["valor"] == 60 and malo["degradada"] and "override inválido" in malo["causa"],
           f"override inválido debe usar YAML y declarar causa, dio {malo!r}")


def prueba_consumidores_no_reintroducen_calendario_propio():
    raiz = Path(__file__).resolve().parent.parent
    instalador = (raiz / "tools/windows/instala-tarea-adquisicion.ps1").read_text(encoding="utf-8")
    runner = (raiz / "tools/adquiere_cron.sh").read_text(encoding="utf-8")
    t31 = (raiz / "tests/check.py").read_text(encoding="utf-8")
    afirma("--calendario-json" in instalador and "$Calendario.hora" in instalador
           and "$Calendario.dias_windows" in instalador and "HoraLocal" not in instalador,
           "instalador debe derivar hora/días/zona del lector común")
    afirma("--calendario-json" in runner and 'export TZ="$ADQ_ZONA_HORARIA"' in runner,
           "runner debe fijar la zona del calendario común")
    afirma("t_cron_calendario_declarado" in t31 and "datetime.time(7, 30)" not in t31,
           "T31 no debe conservar 07:30 codificado aparte")


def main():
    prueba_obten_escalar_y_anidado()
    prueba_clave_ausente_lanza_keyerror()
    prueba_cli_imprime_valor()
    prueba_calendario_normaliza_consumidores_y_proxima_hora()
    prueba_cambio_dia_y_zona_sale_de_la_misma_autoridad()
    prueba_invalida_y_overrides_declaran_valor_aplicado()
    prueba_consumidores_no_reintroducen_calendario_propio()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_adq_config.py: 7 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
