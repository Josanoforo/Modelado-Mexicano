#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_digesto_ids_raiz.py -- `RE_FP_ID` de `tools/digesto_tramite.py`
lee las DOS épocas de id `FP` (`ACTO GEN2-TUBERIA-PARSER-FP-1`, 23/sep/2026).

DEFECTO REAL QUE ATRAPA, medido antes de escribir el parche:
`RE_FP_ID = re.compile(r"\\bFP-\\d+\\b")` sobre
`FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01` devolvía `['FP-260921']` — el
PREFIJO DE FECHA, que no es id de nadie. Su único consumidor,
`_nc_a_fila_mesa`, resuelve esa cita contra `fp_por_id`; una cita fantasma
no resuelve, y las 36 filas de `forense/no-corrido.tsv` cuyo `sucesor` cita
una FP de raíz de acto (universo 613, censado el 23/sep/2026 con lector de
CSV) perdían en silencio las dos lecturas del bloque: el plazo heredado
(`vence:`) y el residual «la sucesora ya cerró y la NC sigue abierta».
Coste para un lector de mesa: esas NC se presentaban como «Sucesor sin FP
visible … por aclarar» teniendo sucesora nombrada.

Casos (los cuatro que pide §5 P2 del encargo, más los del ancho):
  A1 id histórico (`FP-###`, espacio CERRADO por D-2).
  A2 id con raíz de acto (D-24).
  A3 id con guiones interiores en el rótulo, y con minúscula/`_` en él
     (`v1_2`) -- los dos existen en el tablero real.
  A4 NEGATIVO: `FP-260921` suelto NO es un id. Es la mutación exacta del
     defecto: si el parser lo acepta, vuelve la cita fantasma.
  A5 más negativos de «tercera época inventada», mismo criterio que
     `tests/test_tuberia_ids_union.py::caso_C`.
  B  el id nuevo no se PARTE en un `FP-###` fantasma dentro de una frase.
  C  control positivo sobre el árbol REAL: toda cita de `sucesor` que
     nombra una FP existente se resuelve, y ninguna cita resuelta es un
     prefijo de fecha. Cero filas examinadas no es un negativo (A.13).
"""
import csv
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import digesto_tramite as D  # noqa: E402

FALLAS = []


def ok(caso, cond, detalle=""):
    print(("  OK   " if cond else "  FALLA") + f" {caso}"
          + (f" -- {detalle}" if detalle else ""))
    if not cond:
        FALLAS.append(caso)


VIEJOS = ["FP-67", "FP-374", "FP-409"]
NUEVOS = [
    "FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01",
    "FP-260921-MOTOR-THETA-CONGELADA-1-e8fa-01",
    "FP-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_2-a6f5-01",
]
NO_SON_ID = [
    "FP-260921",    # EL DEFECTO: prefijo de fecha suelto
    "FP-260922",
    "FP-2609",      # fecha truncada
    "FP-26092",
    "FP-4099",      # el espacio viejo está CERRADO en ancho 3 (máx FP-409)
    "FP-260921-GEN2-TUBERIA-SUCESOR-1-6E60-01",   # hex en mayúscula
    "FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-1",    # secuencia de un dígito
    "FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60g-01",  # hex de cinco
    "FP-",
    "FP-abc",
]


def caso_A():
    print("A · gramática de `RE_FP_ID`, dos épocas")
    ok("A1 acepta la época vieja `FP-###`",
       all(D.RE_FP_ID.fullmatch(t) for t in VIEJOS),
       str([t for t in VIEJOS if not D.RE_FP_ID.fullmatch(t)]))
    ok("A2/A3 acepta la época nueva, con guion interior y con `v1_2`",
       all(D.RE_FP_ID.fullmatch(t) for t in NUEVOS),
       str([t for t in NUEVOS if not D.RE_FP_ID.fullmatch(t)]))
    ok("A4/A5 RECHAZA el prefijo suelto y la tercera época inventada",
       not any(D.RE_FP_ID.fullmatch(t) for t in NO_SON_ID),
       str([t for t in NO_SON_ID if D.RE_FP_ID.fullmatch(t)]))
    ok("A4-bis `FP-260921` suelto en una frase tampoco se lee como id",
       D.RE_FP_ID.findall("la sucesora FP-260921 no existe") == [],
       str(D.RE_FP_ID.findall("la sucesora FP-260921 no existe")))


def caso_B():
    print("B · el id nuevo no se parte en un `FP-###` fantasma")
    for t in NUEVOS:
        hallado = D.RE_FP_ID.findall(f"sucesor: `{t}` (ver nota)")
        ok(f"B `{t}` entero, una sola vez", hallado == [t], str(hallado))
    mixto = f"{NUEVOS[0]} y {VIEJOS[1]}"
    ok("B-bis una época de cada una en el MISMO texto",
       D.RE_FP_ID.findall(mixto) == [NUEVOS[0], VIEJOS[1]],
       str(D.RE_FP_ID.findall(mixto)))


def _lee(ruta):
    with open(os.path.join(RAIZ, ruta), newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def caso_C():
    print("C · control positivo sobre el árbol real")
    fp = _lee("forense/firmas-pendientes.tsv")
    nc = _lee("forense/no-corrido.tsv")
    # A.13: un negativo de un comando que no examinó archivos no es negativo.
    ok("C0 universo examinado declarado (A.13)",
       len(fp) > 0 and len(nc) > 0,
       f"FP={len(fp)} filas · NC={len(nc)} filas")
    if not fp or not nc:
        return
    ids = {f["id"].strip() for f in fp}
    # Toda FP de raíz de acto del tablero se reconoce como id completo.
    raiz = [i for i in ids if not re.fullmatch(r"FP-\d{1,3}", i) and i.startswith("FP-")]
    no_vistas = [i for i in raiz if not D.RE_FP_ID.fullmatch(i)]
    ok(f"C1 las {len(raiz)} FP de raíz de acto del tablero se reconocen",
       not no_vistas, str(no_vistas))
    # Ninguna cita extraída de `sucesor` es un prefijo de fecha.
    fantasmas, resueltas, con_raiz = set(), 0, 0
    for f in nc:
        suc = f.get("sucesor", "") or ""
        for cita in D.RE_FP_ID.findall(suc):
            if re.fullmatch(r"FP-\d{6}", cita):
                fantasmas.add(cita)
            if cita in ids:
                resueltas += 1
                if not re.fullmatch(r"FP-\d{1,3}", cita):
                    con_raiz += 1
    ok("C2 ninguna cita extraída es un prefijo de fecha",
       not fantasmas, str(sorted(fantasmas)))
    ok(f"C3 citas de `sucesor` que resuelven contra el tablero: {resueltas}"
       f" (de ellas {con_raiz} con raíz de acto)",
       con_raiz > 0, f"resueltas={resueltas} con_raiz={con_raiz}")


def main():
    print("═" * 72)
    print("  GEN2-TUBERIA-PARSER-FP-1 · `RE_FP_ID` lee las dos épocas")
    print("═" * 72)
    caso_A(); caso_B(); caso_C()
    print("─" * 72)
    if FALLAS:
        print(f"  {len(FALLAS)} FALLA(S): " + " · ".join(FALLAS))
        return 1
    print("  TODO VERDE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
