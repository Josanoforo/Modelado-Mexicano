#!/usr/bin/env python3
"""Regresión de `tools/digesto_tramite.py::seccion_i` -- fecha como
`datetime.date`, ACTO GEN2-T11 · RUTINAS-FIX (8/sep/2026,
`forense/encargos/2026-09-08-GEN2-T11-RUTINAS-FIX.md`).

Dos defectos, medidos contra `fbd847de` con el comando exacto que el encargo
cita, el primero desnudando al segundo:

  1. `main()` construye `fecha` como `datetime.date` (`argparse` con
     `type=datetime.date.fromisoformat` o default `datetime.date.today()`) y
     `seccion_i`/`seccion_j` (nuevas de `ACTO GEN2-E7` pieza D) llamaban
     `datetime.date.fromisoformat(fecha)`, que exige `str` y solo atrapaba
     `ValueError` -- un `TypeError` real (`fromisoformat: argument must be
     str`) tumbaba el primer digesto post-E7-D antes de escribir nada. La
     huella de ese PARO vive en `forense/rutinas.tsv` (rutina `tramite`,
     8/sep/2026).
  2. Arreglado (1), el auto-check T25 (`tests/check.py::_T25_ROTULO_BARE`)
     paraba con «rótulo pelado» -- la sección I (`forense/rutinas.tsv`)
     copiaba texto del árbol tal cual, sin pasar por `neutraliza()` como las
     firmas sí hacen (`seccion_a`/`seccion_c`). Las filas retrofit de
     ADR-393 traen rótulos `M`/`E` pelados (`E7`, `E3`…) que `neutraliza()`
     existe exactamente para blindar.

`seccion_h` (`forense/no-corrido.tsv`) recibió el mismo arreglo, pero
`ACTO AUTO-DIGESTO-1 · CAMBIOS-DESDE-EL-ULTIMO-CORTE` (8/sep/2026, en vuelo
al mismo tiempo) reescribió esa sección entera al formato incremental --
al fusionar main aquí, el arreglo de neutralización se reintegró sobre esa
nueva forma directamente en `tools/digesto_tramite.py::seccion_h` (el
helper `_n`), y su cobertura de regresión vive donde ya vive el resto de la
sección H: `tests/test_digesto_nc.py` (caso
`t_neutralizacion_preservada_en_diff`), no aquí.

Qué prueba el caso de este archivo:
  test_seccion_i_acepta_date_y_neutraliza -- `seccion_i(raiz, fecha, cuenta)`
  con `fecha` un `datetime.date` (no un `str`) no lanza, y una fila de
  `rutinas.tsv` cuyo `resultado` trae un rótulo pelado (`E7 (x)`) sale
  `_E7 (x)` en la tabla, sumando en `cuenta`.

Corre solo:
    python3 tests/test_digesto_fecha.py
"""
import datetime
import os
import sys
import tempfile

sys.path.insert(0, "tools")
import digesto_tramite  # noqa: E402


def _escribe(ruta, texto):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as fh:
        fh.write(texto)


def test_seccion_i_acepta_date_y_neutraliza():
    with tempfile.TemporaryDirectory() as raiz:
        hoy = datetime.date.today()
        _escribe(
            os.path.join(raiz, "forense", "rutinas.tsv"),
            "fecha\trutina\tresultado\tdetalle\n"
            f"{hoy.isoformat()}\ttramite\tE7 (x)\tfixture de prueba\n",
        )
        cuenta = digesto_tramite.Cuenta()

        # Defecto 1: `fecha` llega como datetime.date (la misma firma que
        # main() usa), no como str -- antes de este parche, esto lanzaba
        # TypeError dentro de datetime.date.fromisoformat(fecha).
        out, por_rutina = digesto_tramite.seccion_i(raiz, hoy, cuenta)

        assert por_rutina.get("tramite"), "la fila fixture debe caer en la ventana de 7 días"
        texto = "\n".join(out)

        # Defecto 2: el rótulo pelado 'E7' copiado del tsv debe salir
        # neutralizado ('_E7'), nunca desnudo -- T25 lo atraparía si no.
        assert "`_E7 (x)`" in texto, texto
        assert "| E7 (x) |" not in texto and "`E7 (x)`" not in texto, texto
        assert cuenta.rotulos >= 1, "neutraliza() debe sumar en el contador del pie"
        print("  OK -- seccion_i acepta datetime.date sin lanzar y neutraliza "
              "el rótulo pelado copiado de rutinas.tsv.")


if __name__ == "__main__":
    test_seccion_i_acepta_date_y_neutraliza()
    print()
    print("El caso de este archivo coincide. Detalle del hallazgo y de la")
    print("corrección: encabezado de este archivo y tools/digesto_tramite.py")
    print("(seccion_i, neutraliza).")
