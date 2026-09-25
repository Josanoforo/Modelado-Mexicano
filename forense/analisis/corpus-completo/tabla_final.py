#!/usr/bin/env python3
"""ACTO GEN2-CORPUS-COMPLETO-1 · P4 · tabla final programa × olas, derivada (nada tecleado).

Fuentes: catalogo-v1_0.tsv (programa, ola, archivos), el registro de la cola (estado de cada
(programa, ola), de este acto y de otros), crudo/externos-inventario.tsv (barreras y recetas de
las fuentes no INEGI sin archivo directo) y la bitácora (intentos).

Columnas: fuente · programa · olas_adquiridas_por_este_acto · olas_ya_en_corpus (de antes o de
otro acto) · olas_reservadas_al_entrar · no_obtenido (con «NO OBTENIDO POR ESTE AGENTE EN N
INTENTOS» + receta) · licencia_o_barrera.
Uso: python3 tabla_final.py [--verifica]
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D = ROOT / "forense/analisis/corpus-completo"
sys.path.insert(0, str(ROOT / "tools" / "curador_registro"))
from tsv_crudo import leer_dicts  # noqa: E402

SALIDA = D / "tabla-final-v1_0.tsv"


def lee(path: Path) -> list[dict]:
    lineas = path.read_text(encoding="utf-8").splitlines()
    i = 1 if lineas[0].startswith("#") else 0
    cab = lineas[i].split("\t")
    return [dict(zip(cab, l.split("\t"))) for l in lineas[i + 1:]]


def deriva() -> str:
    cat = lee(D / "catalogo-v1_0.tsv")
    reg = {r["fuente_canonica"]: r for r in leer_dicts(ROOT / "data/curacion-registro/cola-adquisicion-registro.tsv")}
    intentos = defaultdict(int)
    for b in lee(D / "bitacora-descargas.tsv"):
        intentos[f"{b['programa']}_{b['ola']}".replace(" ", "-")] += 1
    prog = defaultdict(lambda: {"fuente": "", "este": set(), "antes": set(), "res": set(), "no": [], "lic": set()})
    for c in cat:
        if c["clase"] != "ARCHIVO":
            continue
        p = prog[c["programa"]]
        p["fuente"] = c["fuente"]
        p["lic"].add(c["licencia"].split(" (")[0][:80])
        k = f"{c['programa']}_{c['ola']}".replace(" ", "-")
        fila = reg.get(k)
        if c["en_manifiesto"] == "SI":
            p["antes"].add(c["ola"])
        elif fila and fila["fila_origen"].startswith("CORPUS-COMPLETO-1:"):
            estado = fila["estado_A4A5"]
            if estado.startswith("OBTENIDO"):
                p["este"].add(c["ola"])
                if c["reserva_al_entrar"] == "RESERVADA":
                    p["res"].add(c["ola"])
            else:
                p["no"].append(f"{c['ola']}: NO OBTENIDO POR ESTE AGENTE EN {intentos[k]} INTENTOS")
        elif fila:  # objeto de otro acto (A.8 de objeto)
            p["antes"].add(f"{c['ola']} [{fila['fila_origen'].split(':')[0]} {fila['estado_A4A5']}]")
    for e in lee(D / "crudo/externos-inventario.tsv"):
        if e["url"].lower().endswith((".zip", ".dta", ".sav", ".csv", ".rar", ".7z", ".xlsx", ".xls")):
            continue  # archivo directo: ya está en el catálogo y en la cola
        p = prog[e["programa"].upper()]
        p["fuente"] = "EXTERNO"
        acceso = e["licencia_acceso"]
        if acceso.startswith(("REGISTRO", "NO-APLICA")) or "sin descarga" in acceso or "agregado" in e["ola"]:
            p["lic"].add(acceso[:120])
            if acceso.startswith("REGISTRO"):
                p["no"].append(f"{e['ola']}: NO OBTENIDO POR ESTE AGENTE EN 1 INTENTOS (barrera: {acceso[:60]}); "
                               f"RECETA: {e['nota'][:300]}")
            else:
                p["no"].append(f"{e['ola']}: NO-APLICA (sin microdato individual publicado): {e['nota'][:160]}")
        else:
            p["lic"].add(acceso[:80])
    # externos: lo que otro acto ya trajo, por fila OBTENIDO del registro con el mismo prefijo
    alias = {"CEEY_EMOVI": "EMOVI", "WVS": "WVS", "EVS": "EVS"}
    for nombre, p in prog.items():
        if p["fuente"] != "EXTERNO":
            continue
        pref = alias.get(nombre, nombre)
        for k, fila in reg.items():
            if (k.upper() == pref or k.upper().startswith(pref + "_")) and fila["estado_A4A5"].startswith("OBTENIDO") \
                    and not fila["fila_origen"].startswith("CORPUS-COMPLETO-1:"):
                p["antes"].add(f"{(k.split('_', 1) + [k])[1]} [{fila['fila_origen'].split(':')[0]}]")
    out = ["fuente\tprograma\tn_olas_este_acto\tolas_adquiridas_por_este_acto\tolas_ya_en_corpus\t"
           "olas_reservadas_al_entrar\tno_obtenido\tlicencia_o_barrera"]
    for nombre in sorted(prog, key=lambda n: (prog[n]["fuente"], n)):
        p = prog[nombre]
        out.append("\t".join([p["fuente"], nombre, str(len(p["este"])), ";".join(sorted(p["este"])),
                              ";".join(sorted(p["antes"])), ";".join(sorted(p["res"])),
                              " | ".join(p["no"]).replace("\t", " "), ";".join(sorted(p["lic"]))]))
    return "\n".join(out) + "\n"


def main() -> int:
    texto = deriva()
    if "--verifica" in sys.argv:
        ok = SALIDA.exists() and SALIDA.read_text(encoding="utf-8") == texto
        print("COINCIDE" if ok else "DIFIERE")
        return 0 if ok else 1
    SALIDA.write_text(texto, encoding="utf-8")
    print(f"{texto.count(chr(10)) - 1} programas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
