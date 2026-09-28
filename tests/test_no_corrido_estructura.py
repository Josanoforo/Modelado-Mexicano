"""Guardia de estructura de forense/no-corrido.tsv (ACTO GEN2-TRAMITE-PENDIENTES-2 · P2).

Defecto real que atrapa: 10 filas con `estado` vacío (el valor cayó en otra
columna) y 2 con 10 campos — deuda que ni `status`, ni el tablero, ni
`nc_por_clase.py` contaban durante siete cortes del tablero.

FAIL: número de campos ≠ cabecera, o `estado` fuera de
{ABIERTA*, CERRADA*, NO-APLICA-MIENTRAS-ABIERTA}.
WARN (D-16, no adjudica): filas ABIERTA cuya razón no empieza por un token A.14.
"""
import csv
import os
import warnings

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NC = os.path.join(RAIZ, "forense", "no-corrido.tsv")
TOKENS = ("PARO-ENTORNO", "PARO-PREMISA", "FUERA-DE-PERÍMETRO", "SUSTITUIDO-POR",
          "DIFERIDO-A", "NO-VERIFICABLE-AQUÍ", "DECISIÓN-DE-MESA-PENDIENTE")


def _filas():
    with open(NC, encoding="utf-8", newline="") as f:
        return list(csv.reader(f, delimiter="\t"))


def estado_valido(e):
    return e.startswith("ABIERTA") or e.startswith("CERRADA") or e == "NO-APLICA-MIENTRAS-ABIERTA"


def test_campos_igual_a_cabecera():
    r = _filas()
    malas = [(x[0] if x else "", len(x)) for x in r[1:] if len(x) != len(r[0])]
    assert not malas, f"filas con campos != {len(r[0])}: {malas}"


def test_estado_en_vocabulario():
    r = _filas()
    i = r[0].index("estado")
    malas = [x[0] for x in r[1:] if len(x) > i and not estado_valido(x[i])]
    assert not malas, f"estado fuera de vocabulario: {malas}"


def test_token_razon_warn():
    r = _filas()
    i, j = r[0].index("estado"), r[0].index("razon")
    sin = [x[0] for x in r[1:] if len(x) > i and x[i].startswith("ABIERTA")
           and not x[j].startswith(TOKENS)]
    if sin:
        warnings.warn(f"WARN razón sin token A.14 en {len(sin)} filas ABIERTA")


def test_guardia_atrapa_mutacion():
    assert not estado_valido("")
    assert not estado_valido("GEN2-RECIBO-ASTRA-2")
    assert estado_valido("CERRADA-POR-DISEÑO")
