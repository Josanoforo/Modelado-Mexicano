#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test del derivador `tools/censo_estimabilidad.py` -- ENCARGO CENSO-CMD
(`forense/encargos/2026-08-18-CENSO-CMD.md`, `FP-37`).

Falla si el censo derivado por comando (`censo-estimabilidad-coeficientes-
v1_2.md`, generado por `tools/censo_estimabilidad.py`) diverge, fila por
fila o en el reparto agregado, del censo vigente sellado por `ADR-89`
(`censo-estimabilidad-coeficientes-v1_1.md`, 15/15 filas, `3 RUTA-A ·
5 RUTA-C · 1 RUTA-I · 6 SIN-RUTA`) -- sin que medie un ADR que declare la
divergencia. El punto 4 del encargo es explícito: "si diverge: investigar
la divergencia antes de declarar nada", nunca silenciarla.

Corre sola, mismo patrón que `tests/test_join_folioviv.py` (no depende de
`check.py`, no está wireada a CI en este acto):

    python3 tests/test_censo_derivado.py
"""
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import censo_estimabilidad as D  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CENSO_V1_1 = ROOT / "forense" / "censo-estimabilidad-coeficientes-v1_1.md"
CENSO_V1_2 = ROOT / "forense" / "censo-estimabilidad-coeficientes-v1_2.md"

RUTA_SELLADA_POR_FILA = {
    1: "RUTA-A", 2: "RUTA-A", 3: "SIN-RUTA", 4: "SIN-RUTA", 5: "RUTA-I",
    6: "SIN-RUTA", 7: "RUTA-A", 8: "RUTA-C", 9: "RUTA-C", 10: "SIN-RUTA",
    11: "SIN-RUTA", 12: "RUTA-C", 13: "RUTA-C", 14: "RUTA-C", 15: "SIN-RUTA",
}
REPARTO_SELLADO = {"RUTA-A": 3, "RUTA-C": 5, "RUTA-I": 1, "SIN-RUTA": 6}

FAILS = []


def check(cond, msg):
    if not cond:
        FAILS.append(msg)


def extraer_rutas_de_tabla(texto):
    """Misma receta que censo-estimabilidad-coeficientes-v1_1.md §7: solo
    filas de datos (patrón `^\\| N \\|`), no todo el archivo."""
    rutas = {}
    for linea in texto.splitlines():
        m = re.match(r"^\| (\d+) \|.*\*\*`?(RUTA-[AIC]|SIN-RUTA)`?\*\*", linea)
        if m:
            rutas[int(m.group(1))] = m.group(2)
    return rutas


def t01_derivador_reproduce_reparto_sellado():
    filas = D.derivar()
    r = D.reparto(filas)
    check(
        r == REPARTO_SELLADO,
        "reparto del derivador {} != reparto sellado por ADR-89 {} -- "
        "investigar la divergencia (encargo CENSO-CMD, punto 4) antes de "
        "declarar nada".format(r, REPARTO_SELLADO),
    )


def t02_derivador_reproduce_ruta_por_fila():
    filas = D.derivar()
    for f in filas:
        esperado = RUTA_SELLADA_POR_FILA[f["fila"]]
        check(
            f["ruta"] == esperado,
            "fila {} ({}, {}.{}): derivador da {}, censo v1.1 sellado dice "
            "{}".format(
                f["fila"], f["necesidad_id"], f["gen"], f["coef"], f["ruta"],
                esperado,
            ),
        )


def t03_censo_v1_1_no_se_toco():
    """Este encargo no reabre v1.1 -- verificación de que sigue trayendo su
    propio reparto sellado, no que este test lo repita a ciegas."""
    check(CENSO_V1_1.exists(), "falta forense/censo-estimabilidad-coeficientes-v1_1.md")
    if not CENSO_V1_1.exists():
        return
    texto = io.open(CENSO_V1_1, encoding="utf-8").read()
    rutas = extraer_rutas_de_tabla(texto)
    check(len(rutas) == 15, "v1.1 no trae 15 filas de datos reconocibles ({})".format(len(rutas)))
    from collections import Counter
    c = Counter(rutas.values())
    reparto_v1_1 = {r: c.get(r, 0) for r in D.RUTAS_VALIDAS}
    check(
        reparto_v1_1 == REPARTO_SELLADO,
        "el reparto leído de v1.1 ({}) ya no coincide con el sellado por "
        "ADR-89 ({}) -- alguien editó v1.1 fuera de protocolo".format(
            reparto_v1_1, REPARTO_SELLADO
        ),
    )
    check(
        rutas == RUTA_SELLADA_POR_FILA,
        "v1.1 cambió de ruta en al menos una fila frente a lo sellado por "
        "ADR-89",
    )


def t04_censo_v1_2_generado_esta_presente_y_al_dia():
    """`censo-estimabilidad-coeficientes-v1_2.md` (perímetro del encargo:
    generado por el derivador, no editado a mano) debe existir y coincidir
    byte a byte con lo que el derivador produce hoy."""
    check(
        CENSO_V1_2.exists(),
        "falta forense/censo-estimabilidad-coeficientes-v1_2.md -- correr "
        "`python3 tools/censo_estimabilidad.py --write "
        "forense/censo-estimabilidad-coeficientes-v1_2.md`",
    )
    if not CENSO_V1_2.exists():
        return
    en_disco = io.open(CENSO_V1_2, encoding="utf-8").read()
    regenerado = D.documento_completo(D.derivar())
    check(
        en_disco == regenerado,
        "censo-estimabilidad-coeficientes-v1_2.md en disco no coincide con "
        "lo que el derivador produce ahora mismo -- fue editado a mano o "
        "quedó desactualizado; regenerar con `tools/censo_estimabilidad.py "
        "--write`",
    )
    rutas = extraer_rutas_de_tabla(en_disco)
    check(
        rutas == RUTA_SELLADA_POR_FILA,
        "censo-estimabilidad-coeficientes-v1_2.md en disco diverge del "
        "reparto sellado por fila",
    )


def main():
    for name, fn in [
        ("T-CENSO-01 reparto agregado", t01_derivador_reproduce_reparto_sellado),
        ("T-CENSO-02 ruta por fila", t02_derivador_reproduce_ruta_por_fila),
        ("T-CENSO-03 v1.1 intacto", t03_censo_v1_1_no_se_toco),
        ("T-CENSO-04 v1.2 generado y al día", t04_censo_v1_2_generado_esta_presente_y_al_dia),
    ]:
        before = len(FAILS)
        fn()
        mark = "FAIL" if len(FAILS) > before else " ok "
        print("  [{}]  {}".format(mark, name))

    if FAILS:
        print("\n{} FAIL:".format(len(FAILS)))
        for m in FAILS:
            print("  · {}".format(m))
        return 1
    print("\nOK -- derivador reproduce el censo vigente, 15/15 filas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
