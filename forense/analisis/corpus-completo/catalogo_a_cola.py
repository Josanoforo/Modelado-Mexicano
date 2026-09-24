#!/usr/bin/env python3
"""ACTO GEN2-CORPUS-COMPLETO-1 · P2 · del catálogo al registro de la cola.

Mismo conducto que tools/dominios/hoja_a_cola.py (GEN2-ASTRA5-U5-ADQUISICION-1): filas
MICRODATO del registro `data/curacion-registro/cola-adquisicion-registro.tsv` por
(programa, ola), escritor canónico `tsv_crudo.upsert_fila`, y la vista se regenera con
`tools/vista_cola_adquisicion.py` (nunca a mano). hoja_a_cola.py parte de la hoja del mapa;
este puente parte del catálogo por comando (catalogo-v1_0.tsv), que ya trae programa y ola
normalizados, así que sus reglas de texto libre no aplican aquí y no se duplican.

Clave: `fila_origen = CORPUS-COMPLETO-1:<PROGRAMA>_<OLA>`; `fuente_canonica = <PROGRAMA>_<OLA>`.
A.8 por objeto: si el registro ya tiene una fila con esa `fuente_canonica` (de cualquier acto,
p. ej. ASTRA5-U5:ENSANUT_2018), el objeto no se duplica. A.8 por archivo lo resuelve el
catálogo (`en_manifiesto`) y, al registrar, la deduplicación por sha del manifiesto.

Uso: python3 catalogo_a_cola.py [--escribe] [--verifica]   (sin flags: reporta; D-23)
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "curador_registro"))
from tsv_crudo import leer_dicts, leer_lineas, upsert_fila  # noqa: E402

D = ROOT / "forense/analisis/corpus-completo"
CATALOGO = D / "catalogo-v1_0.tsv"
REGISTRO = ROOT / "data/curacion-registro/cola-adquisicion-registro.tsv"
PREFIJO = "CORPUS-COMPLETO-1:"
ACTO = "GEN2-CORPUS-COMPLETO-1"


def lee_catalogo() -> list[dict]:
    lineas = CATALOGO.read_text(encoding="utf-8").splitlines()
    cab = lineas[1].split("\t")
    return [dict(zip(cab, l.split("\t"))) for l in lineas[2:]]


def deriva() -> tuple[list[dict], list[str]]:
    campos = leer_lineas(REGISTRO)[0].rstrip("\n").split("\t")
    existentes = {r["fuente_canonica"].upper(): r["fila_origen"] for r in leer_dicts(REGISTRO)
                  if not r["fila_origen"].startswith(PREFIJO)}
    grupos: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in lee_catalogo():
        if r["clase"] == "ARCHIVO" and r["en_manifiesto"] == "NO":
            grupos[(r["programa"], r["ola"])].append(r)
    filas, omitidas = [], []
    for (prog, ola), rs in sorted(grupos.items()):
        fuente = f"{prog}_{ola}".replace(" ", "-")
        if fuente.upper() in existentes:
            omitidas.append(f"{fuente} (ya en cola: {existentes[fuente.upper()]})")
            continue
        r0 = rs[0]
        reserva = "RESERVADA" if any(x["reserva_al_entrar"] == "RESERVADA" for x in rs) else "ABIERTA"
        filas.append({
            "fila_origen": PREFIJO + fuente,
            "fuente_canonica": fuente,
            "fuente_canonica_normalizada": fuente,
            "discordancia_alias": "SIN_ALIAS",
            "estado_A4A5": "PENDIENTE",
            "prioridad": r0["prioridad"],
            "url_conocida": r0["url"],
            "ids_manifiesto": "",
            "origen": f"forense/analisis/corpus-completo/catalogo-v1_0.tsv ({r0['fuente']} {prog} ola {ola})",
            "nota": (f"{ACTO} P2 (catalogo_a_cola.py): {len(rs)} archivo(s) del catálogo por comando, "
                     f"ola {reserva}"
                     + (" (E.6: ola más reciente de programa con historia; bajar y hashear no es abrir)"
                        if reserva == "RESERVADA" else "")
                     + f"; licencia: {r0['licencia'][:120]}"),
        })
    return filas, omitidas


def main() -> int:
    filas, omitidas = deriva()
    campos = leer_lineas(REGISTRO)[0].rstrip("\n").split("\t")
    if "--verifica" in sys.argv:
        tiene = {r["fila_origen"] for r in leer_dicts(REGISTRO)}
        falta = [f["fila_origen"] for f in filas if f["fila_origen"] not in tiene]
        print(f"faltan {len(falta)} de {len(filas)}")
        return 1 if falta else 0
    print(f"filas derivadas={len(filas)} · reservadas={sum('RESERVADA' in f['nota'] for f in filas)}"
          f" · omitidas por A.8 de objeto={len(omitidas)}")
    for o in omitidas:
        print("  OMITE", o)
    if "--escribe" in sys.argv:
        tiene = {r["fila_origen"] for r in leer_dicts(REGISTRO)}
        n = 0
        for f in filas:
            if f["fila_origen"] in tiene:  # la fila es de /adquiere desde que nace
                continue
            upsert_fila(REGISTRO, f, campos)
            n += 1
        print(f"insertadas {n} filas en {REGISTRO.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
