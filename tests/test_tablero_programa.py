#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_tablero_programa.py -- prueba mínima del bloque vivo committeado
de `tools/tablero_programa.py` (ACTO AUTOMATIZA-*, TABLERO-VIVO).

Usa un FIXTURE PEQUEÑO en `tempfile.TemporaryDirectory()` -- nunca el archivo
real de 90KB. Verifica, en aislamiento: idempotencia (dos pasadas de
--actualiza sobre el mismo archivo producen diff vacío en la segunda),
preservación byte a byte de todo lo que está fuera de los marcadores, y que
un ancla inválida (0 marcadores, o 2+ BEGIN) aborta sin escribir.

Corre sola:
    python3 tests/test_tablero_programa.py
"""
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import tablero_programa as TP  # noqa: E402

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def _indicadores_fixture():
    return {
        "sha": {"valor": "abc1234", "comando": "-", "nota": ""},
        "fecha_commit": {"valor": "2026-01-01", "comando": "-", "nota": ""},
        "es_origin_main": {"valor": True, "comando": "-", "nota": ""},
        "motor_reglas": {"valor": 1, "comando": "-", "nota": ""},
        "motor_reglas_con_dato": {"valor": 1, "comando": "-", "nota": ""},
        "motor_reglas_sin_dato": {"valor": [], "comando": "-", "nota": ""},
        "motor_conductas_medido": {"valor": 1, "comando": "-", "nota": ""},
        "motor_tiers": {"valor": {"FUERTE": 1}, "comando": "-", "nota": ""},
        "marco_v1_2_sorteado": {"valor": 1, "comando": "-", "nota": ""},
        "celdas_con_M": {"valor": 1, "comando": "-", "nota": ""},
        "celdas_con_R": {"valor": 1, "comando": "-", "nota": ""},
        "celdas_con_L": {"valor": 1, "comando": "-", "nota": ""},
        "celdas_puntuables_LMR": {"valor": 1, "comando": "-", "nota": ""},
        "celdas_sin_LMR": {"valor": [], "comando": "-", "nota": ""},
        "manifiesto_ids": {"valor": 1, "comando": "-", "nota": ""},
        "registro_curador_filas": {"valor": 1, "comando": "-", "nota": ""},
        "relaciones_filas": {"valor": 1, "comando": "-", "nota": ""},
        "inventario_reactivos_v1_2": {"valor": 1, "comando": "-", "nota": ""},
        "adr_max": {"valor": 1, "comando": "-", "nota": ""},
        "fp_max": {"valor": 1, "comando": "-", "nota": ""},
        "fp_abiertas": {"valor": [{"id": "FP-1", "creado": "2026-01-01", "dias": 1, "que": "x"}], "comando": "-", "nota": ""},
        "encargos_archivados": {"valor": 1, "comando": "-", "nota": ""},
        "encargos_consumidos": {"valor": 1, "comando": "-", "nota": ""},
        "cola_encargos": {"valor": {"a.md": "LISTO"}, "comando": "-", "nota": ""},
    }


NARRATIVA_ANTES = "**Nota humana previa.** Texto de prosa que NO debe tocarse.\n\n"
NARRATIVA_DESPUES = "\n\n## Sección histórica\nMás prosa humana que tampoco debe tocarse.\n"


def _escribe_fixture(dirpath, cuerpo_bloque="<!-- placeholder -->"):
    ruta = os.path.join(dirpath, "TABLERO-FIXTURE.md")
    contenido = (
        NARRATIVA_ANTES
        + TP.MARCA_INICIO + "\n" + cuerpo_bloque + "\n" + TP.MARCA_FIN
        + NARRATIVA_DESPUES
    )
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta


def prueba_idempotencia_y_preservacion():
    I = _indicadores_fixture()
    with tempfile.TemporaryDirectory() as d:
        ruta = _escribe_fixture(d)
        antes = open(ruta, encoding="utf-8").read()

        rc1 = TP._actualiza_tablero(ruta, I)
        afirma(rc1 == 0, f"primera pasada debió retornar 0, retornó {rc1}")
        despues1 = open(ruta, encoding="utf-8").read()

        afirma(despues1.startswith(NARRATIVA_ANTES), "el texto antes del BEGIN debe preservarse byte a byte")
        afirma(despues1.endswith(NARRATIVA_DESPUES), "el texto después del END debe preservarse byte a byte")
        afirma(TP.MARCA_INICIO in despues1 and TP.MARCA_FIN in despues1, "los marcadores deben seguir presentes")
        afirma("abc1234" in despues1, "el bloque nuevo debe contener el SHA derivado")
        afirma(despues1 != antes, "la primera pasada debe cambiar el contenido (placeholder -> bloque real)")

        rc2 = TP._actualiza_tablero(ruta, I)
        afirma(rc2 == 0, f"segunda pasada debió retornar 0, retornó {rc2}")
        despues2 = open(ruta, encoding="utf-8").read()
        afirma(despues2 == despues1, "segunda pasada sobre el mismo dict de indicadores debe ser un no-op (idempotencia)")


def prueba_ancla_invalida_sin_marcadores():
    I = _indicadores_fixture()
    with tempfile.TemporaryDirectory() as d:
        ruta = os.path.join(d, "TABLERO-SIN-MARCAS.md")
        contenido = "Solo prosa, sin marcadores.\n"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        rc = TP._actualiza_tablero(ruta, I)
        afirma(rc != 0, "0 marcadores debe abortar con código != 0")
        despues = open(ruta, encoding="utf-8").read()
        afirma(despues == contenido, "0 marcadores no debe escribir nada")


def prueba_ancla_invalida_doble_begin():
    I = _indicadores_fixture()
    with tempfile.TemporaryDirectory() as d:
        ruta = os.path.join(d, "TABLERO-DOBLE.md")
        contenido = (
            NARRATIVA_ANTES
            + TP.MARCA_INICIO + "\nbloque 1\n" + TP.MARCA_FIN
            + "\n" + TP.MARCA_INICIO + "\nbloque 2\n" + TP.MARCA_FIN
            + NARRATIVA_DESPUES
        )
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        rc = TP._actualiza_tablero(ruta, I)
        afirma(rc != 0, "2+ BEGIN debe abortar con código != 0")
        despues = open(ruta, encoding="utf-8").read()
        afirma(despues == contenido, "2+ BEGIN no debe escribir nada")


def prueba_ancla_invalida_end_antes_de_begin():
    I = _indicadores_fixture()
    with tempfile.TemporaryDirectory() as d:
        ruta = os.path.join(d, "TABLERO-INVERTIDO.md")
        contenido = TP.MARCA_FIN + "\n" + TP.MARCA_INICIO + "\n"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        rc = TP._actualiza_tablero(ruta, I)
        afirma(rc != 0, "END antes de BEGIN debe abortar con código != 0")
        despues = open(ruta, encoding="utf-8").read()
        afirma(despues == contenido, "END antes de BEGIN no debe escribir nada")


def prueba_estado_cola_lee_cabecera_no_substring():
    """NC-0252: `_estado_cola` debe leer `ESTADO:` real, no colarse por un
    substring que la BITACORA solo *menciona* (p.ej. "seguía LISTO-CAJA con
    el PR ya fusionado" dentro de un renglón `ESTADO: CONSUMIDO`)."""
    afirma(TP._estado_cola("ESTADO: CONSUMIDO — PR #602. Sincronizado: "
                            "seguía LISTO-CAJA con el PR ya fusionado.\n") == "CONSUMIDO",
           "ESTADO: CONSUMIDO no debe leerse LISTO por mencionar LISTO-CAJA en la glosa")
    afirma(TP._estado_cola("ESTADO: CONSUMIDO — PR #600. Sincronizado: "
                            "seguía GATEADO con el PR ya fusionado.\n") == "CONSUMIDO",
           "ESTADO: CONSUMIDO no debe leerse GATED por mencionar GATEADO en la glosa")
    afirma(TP._estado_cola("ESTADO: LISTO-NUBE\n") == "LISTO", "LISTO-<ENTORNO> -> LISTO")
    afirma(TP._estado_cola("ESTADO: GATEADO\nCOMPUERTA: X\n") == "GATED", "GATEADO -> GATED")
    afirma(TP._estado_cola("ESTADO: EN-CURSO\n") == "GATED", "EN-CURSO no es ni CONSUMIDO ni LISTO")
    afirma(TP._estado_cola("ESTADO: PARO-REPORTADO\n") == "GATED", "PARO-REPORTADO -> GATED")
    # formato viejo, sin cabecera ESTADO: -- cae al heurístico por substring.
    afirma(TP._estado_cola("texto libre\n## CONSUMIDO · PR #1\n") == "CONSUMIDO",
           "sin cabecera ESTADO:, el heurístico viejo sigue vigente")
    afirma(TP._estado_cola("texto libre, LISTO-NUBE mencionado\n") == "LISTO",
           "sin cabecera ESTADO:, el heurístico viejo sigue vigente (LISTO-)")
    afirma(TP._estado_cola("texto libre sin marcas\n") == "GATED",
           "sin cabecera ESTADO: ni substrings conocidos -> GATED")


def prueba_estado_cola_contra_arbol_real():
    """Cruza `_estado_cola` contra la cabecera `ESTADO:` real de
    `forense/encargos/cola/` -- el desfase que NC-0252 midió (GEN2-E1/E2/E4
    con `ESTADO: CONSUMIDO` reportados LISTO/GATED) no puede volver a pasar
    silencioso."""
    base = os.path.join(ROOT, "forense", "encargos", "cola")
    if not os.path.isdir(base):
        return
    revisados = 0
    for dirpath, _, nombres in os.walk(base):
        for nombre in nombres:
            if not nombre.endswith(".md"):
                continue
            ruta = os.path.join(dirpath, nombre)
            texto = TP.leer(ruta)
            m = TP._ESTADO_CABECERA.search(texto)
            if not m:
                continue
            revisados += 1
            estado = m.group(1).rstrip(".,;:")
            calculado = TP._estado_cola(texto)
            if estado.startswith("CONSUMIDO"):
                afirma(calculado == "CONSUMIDO", f"{ruta}: ESTADO: {estado} debe leerse CONSUMIDO, leyó {calculado}")
            elif estado.startswith("LISTO"):
                afirma(calculado == "LISTO", f"{ruta}: ESTADO: {estado} debe leerse LISTO, leyó {calculado}")
    afirma(revisados > 0, "debe haber al menos un archivo con cabecera ESTADO: en forense/encargos/cola/")


def main():
    prueba_idempotencia_y_preservacion()
    prueba_ancla_invalida_sin_marcadores()
    prueba_ancla_invalida_doble_begin()
    prueba_ancla_invalida_end_antes_de_begin()
    prueba_estado_cola_lee_cabecera_no_substring()
    prueba_estado_cola_contra_arbol_real()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_tablero_programa.py: 6 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
