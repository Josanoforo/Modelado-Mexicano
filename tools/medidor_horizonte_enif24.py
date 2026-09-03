#!/usr/bin/env python3
"""ACTO MAESTRA35-L7 · dinero.ahorro.volatilidad_horizonte_corto (R1.1) · ENIF 2024.

Ejecuta la spec CONGELADA en
`forense/notas/2026-09-02-MAESTRA35-L7-spec.md` (COMMIT-1).

R1.1 del modelo (canon/modelo-decision-v4_0.md:499): «SI el ingreso es
volátil/informal ENTONCES horizonte corto, ahorro informal ... — PORQUE G3
(volatilidad) + escasez». R1.1 tiene veredicto Hito D = D archivado
(`hitoD-R1.1-veredicto-v1_0.md`, 28/jul/2026), pero ESE `D` es específico al
dominio AGRÍCOLA (productores de temporal, Fondos de Aseguramiento / Seguro
Agrícola Catastrófico): "R1.1 no gana ni pierde información EN ESE DOMINIO.
Sale igual que entró" (§7 de esa ficha). No es un cierre general de R1.1, y
esta pieza NO reintenta ese falsador -- mide la TASA BASE nacional/urbana
(apparatus B-bis, "regla de señal" v2.3) vía ENIF 2024, población general.

Dos desenlaces (el SI-ENTONCES de la regla predice ambos):
  D1 · horizonte_corto  -- P4_10 == '1' ("menos de una semana / no tiene
       ahorros para cubrir gastos si dejara de recibir ingresos"). Lectura
       MÁS LITERAL de "corto": la categoría más extrema de la escala
       ordinal, que además incluye a quien no tiene ningún colchón. Los
       códigos {1,2} (<1 mes, convención de "fragilidad financiera" de
       reportes CNBV) quedan declarados como SENSIBILIDAD, no como
       principal -- ver spec §2.3.
  D2 · ahorra_solo_informal -- IDÉNTICO a `MAESTRA35-L1 · P2`
       (tools/medidor_ahorro_enif24.py::desenlaces), reusado tal cual, no
       redefinido: informal (P5_1_1..6) Y NO formal (P5_6_1..9).

Eje único: formalidad (P3_13), IDÉNTICO al de `MAESTRA35-L1 · P2`
(EJES_P2["formalidad"]) -- reusado por import, no transcrito, para que un
cambio futuro en la definición de L1 no pueda divergir en silencio de la
que esta pieza cita.

Unidad = PERSONA elegida 18+. Ponderador FAC_PER, diseño EST_DIS×UPM_DIS,
bootstrap conglomerado n_boot=10000 seed=42.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ejes_maestra35_l1 import Eje, imprime, mide_eje  # noqa: E402
from medidor_ahorro_enif24 import (  # noqa: E402
    EJES_P2, FORMAL, INFORMAL, ZIP, carga, sha256)

EJE_FORMALIDAD = next(e for e in EJES_P2 if e.nombre == "formalidad")
assert EJE_FORMALIDAD.orden == ["sin seguridad social", "con seguridad social"]
assert EJE_FORMALIDAD.signo == "desc"

CORTE_PRINCIPAL = {"1"}                 # horizonte_corto, lectura literal
CORTE_SENSIBILIDAD = {"1", "2"}         # <1 mes, convención CNBV


def guardias(df):
    print("GUARDIA · P4_10 value_counts (universo 18+, sin gate):")
    print(df["P4_10"].value_counts(dropna=False).sort_index().to_string())
    esperado = set("12345") | {"8", "9"}
    fuera_catalogo = ~df["P4_10"].isin(esperado)
    if fuera_catalogo.any():
        raise SystemExit(
            f"PARO · {int(fuera_catalogo.sum())} valores de P4_10 fuera del "
            f"catálogo esperado {sorted(esperado)}")


def desenlaces(df):
    horizonte_corto = df["P4_10"].isin(CORTE_PRINCIPAL)
    horizonte_corto_sens = df["P4_10"].isin(CORTE_SENSIBILIDAD)
    informal = df[INFORMAL].eq("1").any(axis=1)
    formal = df[FORMAL].eq("1").any(axis=1)
    ahorra_solo_informal = informal & ~formal   # idéntico a L1 P2
    return {
        "D1 · horizonte_corto (P4_10=1)": horizonte_corto,
        "D1-sens · horizonte_corto (P4_10 en {1,2})": horizonte_corto_sens,
        "D2 · ahorra_solo_informal (=L1 P2)": ahorra_solo_informal,
    }


def main():
    print("ACTO MAESTRA35-L7 · dinero.ahorro.horizonte_corto · ENIF 2024")
    print(f"payload  : {os.path.basename(ZIP)}")
    print(f"sha256   : {sha256(ZIP)}")
    df = carga()
    faltan = [c for c in ["P3_13", "P4_10"] if c not in df.columns]
    if faltan:
        raise SystemExit(f"PARO · faltan columnas en TMODULO.csv: {faltan}")
    df["P4_10"] = df["P4_10"].astype(str).str.strip().str.strip('"')
    df["P3_13"] = df["P3_13"].astype(str).str.strip().str.strip('"')
    print(f"tabla    : TMODULO.csv · {len(df):,} personas elegidas 18+")
    guardias(df)
    print()

    print("P3_13 -- cobertura reverificada")
    validos_p3_13 = df["P3_13"].isin(list("1234567"))
    print(f"  válidos 1-7: {int(validos_p3_13.sum()):,} de {len(df):,} "
          f"= {validos_p3_13.mean():.4%}")
    print()

    valido_p4_10 = df["P4_10"].isin(list("12345"))
    universo = df[validos_p3_13 & valido_p4_10].copy()
    print(f"universo triple (ahorro-elegible ∧ P3_13 válido ∧ P4_10 válido): "
          f"n = {len(universo):,} de {len(df):,}")
    print()

    w, est, upm = universo["_w"], universo["EST_DIS"], universo["UPM_DIS"]
    salida = {}
    for etiqueta, d in desenlaces(universo).items():
        print("=" * 78)
        print(f"DESENLACE {etiqueta}")
        print("=" * 78)
        r = mide_eje(universo, EJE_FORMALIDAD, d.astype(float), w, est, upm)
        imprime(r, "personas")
        salida[etiqueta] = r
    return salida


if __name__ == "__main__":
    main()
