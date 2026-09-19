#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_union_estimando.py -- ACTO GEN2-FAM-UNION-ESTIMANDO-1
(`forense/encargos/2026-09-19-GEN2-FAM-UNION-ESTIMANDO-1.md`, 19/sep/2026).

P4 del encargo, verbatim: «Un test que falle si `matrimonio_directo` vuelve
a aparecer con una `clase` que cite `p3_27` o "situación conyugal". Es el
defecto ocurrido; ninguno más.»

EL DEFECTO QUE CONGELA. Hasta el 19/sep/2026 `milpa/tramite.yaml` traía, en
la regla `familia.union.libre` (`situacion: primera_union`):

    - {conducta: matrimonio_directo, p: 0.809500,
       clase: "MEDIDO·p(prevalencia bruta ponderada 15+, tasa base;
                        ENADID 2023, p3_27_ag)"}

0.8095 es 1 − 0.190541, el COMPLEMENTO ARITMÉTICO de la unión libre en la
situación conyugal ACTUAL de la población de 15+ (ENADID 2023, P3_27). Ese
complemento incluye solteras, separadas, divorciadas y viudas: no significa
matrimonio, y menos «matrimonio directo», que es un tipo de PRIMERA UNIÓN.
No fue un error de cálculo -- `CALC-ENADID-0001` reprodujo 0.1905406 sobre
la misma fuente -- sino un NOMBRE puesto sobre otra cantidad.

Este test no juzga la cifra: juzga el PAR (nombre, procedencia declarada).
Si una conducta llamada `matrimonio_directo` vuelve a declarar una `clase`
que cita el reactivo de situación conyugal actual (`p3_27`, `p3_27_ag`) o la
frase «situación conyugal», el defecto volvió y la prueba falla.

Corre sola:

    python3 tests/test_union_estimando.py
"""
import pathlib
import re
import sys

import yaml

RAIZ = pathlib.Path(__file__).resolve().parents[1]
TRAMITE = RAIZ / "milpa" / "tramite.yaml"

CONDUCTA = "matrimonio_directo"

# El reactivo de SITUACIÓN CONYUGAL ACTUAL de ENADID, en las formas en que el
# árbol lo escribe de verdad, y la frase castellana con y sin acento.
PROHIBIDO = re.compile(
    r"p3[_\s-]?27"          # p3_27, p3_27_ag, P3-27, "p3 27"
    r"|situaci[oó]n\s+conyugal",
    re.IGNORECASE,
)


def _salidas(regla):
    for clave in ("entonces", "transiciones"):
        for salida in regla.get(clave) or []:
            if isinstance(salida, dict):
                yield clave, salida


def hallazgos():
    """Pares (regla, clase) donde `matrimonio_directo` cita el otro estimando."""
    crudo = yaml.safe_load(TRAMITE.read_text(encoding="utf-8"))
    malos = []
    vistas = 0
    for regla in crudo.get("reglas") or []:
        for clave, salida in _salidas(regla):
            if str(salida.get("conducta", "")) != CONDUCTA:
                continue
            vistas += 1
            clase = str(salida.get("clase") or "")
            if PROHIBIDO.search(clase):
                malos.append((regla.get("id"), clave, clase))
    return vistas, malos


def test_matrimonio_directo_no_cita_situacion_conyugal_actual():
    vistas, malos = hallazgos()
    # A.13: un negativo de un comando que no examinó nada no es un negativo.
    assert vistas > 0, (
        "ninguna conducta `matrimonio_directo` en milpa/tramite.yaml: el test "
        "no examinó nada y su verde no significa nada. Si la conducta se "
        "renombró por firma de mesa, este test se actualiza con esa firma."
    )
    assert not malos, (
        "`matrimonio_directo` es un tipo de PRIMERA UNIÓN (EDER 2017, "
        "edo_civil1). Estas conductas lo declaran contra el reactivo de "
        "SITUACIÓN CONYUGAL ACTUAL (ENADID 2023, P3_27), cuyo complemento "
        "incluye solteras, separadas, divorciadas y viudas:\n"
        + "\n".join(f"  {rid} · {clave} · clase={clase}" for rid, clave, clase in malos)
    )


def test_el_detector_reconoce_el_defecto_historico():
    """Control positivo: el regex atrapa la `clase` exacta que hubo hasta hoy."""
    historica = ("MEDIDO·p(prevalencia bruta ponderada 15+, tasa base; "
                 "ENADID 2023, p3_27_ag)")
    assert PROHIBIDO.search(historica)
    assert PROHIBIDO.search("situacion conyugal actual, 15+")
    assert PROHIBIDO.search("situación conyugal")
    # Y NO atrapa la clase vigente, que es del estimando correcto.
    vigente = ("MEDIDO·p(proporción ponderada del TIPO DE PRIMERA UNIÓN; "
               "EDER 2017, historiavida.csv/edo_civil1, primer código no-cero "
               "por persona; universo: personas alguna vez unidas, n = 18 689; "
               "ponderador factor_per)")
    assert not PROHIBIDO.search(vigente)


if __name__ == "__main__":
    fallos = 0
    for nombre, prueba in sorted(globals().items()):
        if not nombre.startswith("test_") or not callable(prueba):
            continue
        try:
            prueba()
        except AssertionError as exc:
            fallos += 1
            print(f"FAIL {nombre}\n{exc}")
        else:
            print(f"OK   {nombre}")
    vistas, _ = hallazgos()
    print(f"# conductas `{CONDUCTA}` examinadas en {TRAMITE}: {vistas}")
    sys.exit(1 if fallos else 0)
