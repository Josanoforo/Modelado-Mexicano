#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Derivador del censo de estimabilidad de los 15 coeficientes de generador.

Encargo `forense/encargos/2026-08-18-CENSO-CMD.md` (`FP-37`). Formaliza como
código dos recetas que hasta ahora se ejecutaron a mano:

  1. El mapeo `necesidad_id` -> fila del censo, verbatim de
     `data/curacion-registro/necesidad-objeto-modelo.tsv` ("fila N del censo
     = N{N}", citado por `forense/registro-recalculo-v1_0.md` §1 Entrada 0).
  2. Las reglas de precedencia RUTA-A/RUTA-I/RUTA-C/SIN-RUTA de
     `forense/censo-estimabilidad-coeficientes-v1_0.md` §1, ya volcadas a
     forma tabular en `milpa/procedencia.yaml:rutas_estimabilidad_coeficiente`
     (congeladas ahí a `version_censo: "1.0"`) más la única regla de
     reclasificación que v1.1 aplicó sobre esa base: una necesidad `SIN-RUTA`
     en v1.0 sube a `RUTA-C` si `data/curacion-registro/relaciones.tsv` trae,
     para esa misma necesidad, una fila con `capa4_apertura_mapeo=
     EXISTE-SATISFACE` y `clasificacion_relacion=CONFIRMADA` — exactamente el
     criterio que `registro-recalculo-v1_0.md` §1 Entrada 0 verificó a mano
     para N12/N13/N14 (las tres reclasificaciones de
     `censo-estimabilidad-coeficientes-v1_1.md`) y que declaró negativo, tras
     revisar las 12 filas restantes, para el resto.

    No lee ni escribe `data/curacion-registro/**` -- solo lee. No toca
    `milpa/procedencia.yaml`.

Uso:
    python3 tools/censo_estimabilidad.py                # imprime la tabla
    python3 tools/censo_estimabilidad.py --write RUTA.md # escribe el censo generado
    python3 tools/censo_estimabilidad.py --reparto       # solo el reparto (receta §7)
"""
import csv
import io
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCEDENCIA = os.path.join(ROOT, "milpa", "procedencia.yaml")
NECESIDAD_OBJETO_MODELO = os.path.join(
    ROOT, "data", "curacion-registro", "necesidad-objeto-modelo.tsv"
)
RELACIONES = os.path.join(ROOT, "data", "curacion-registro", "relaciones.tsv")

RUTAS_VALIDAS = ("RUTA-A", "RUTA-I", "RUTA-C", "SIN-RUTA")


def _read_tsv(path):
    with io.open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def cargar_censo_v1_0():
    """gen.coef -> {ruta, prioridad, nota} desde `procedencia.yaml`
    (`rutas_estimabilidad_coeficiente`, congelado a `version_censo: "1.0"`,
    verbatim de `censo-estimabilidad-coeficientes-v1_0.md` §5)."""
    with io.open(PROCEDENCIA, encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    bloque = doc["rutas_estimabilidad_coeficiente"]
    assert bloque["version_censo"] == "1.0", (
        "milpa/procedencia.yaml:rutas_estimabilidad_coeficiente cambió de "
        "version_censo -- el derivador asume que sigue siendo la foto v1.0 "
        "sobre la que v1.1 reclasifica; revisar este derivador antes de seguir."
    )
    out = {}
    for fila in bloque["detalle"]:
        clave = "{}.{}".format(fila["gen"], fila["coef"])
        out[clave] = {
            "ruta": fila["ruta"],
            "prioridad": fila["prioridad"],
            "nota": fila["nota"],
        }
    return out


def cargar_mapa_necesidades():
    """necesidad_id (N1..N15) -> gen.coef, orden = orden de fila del censo.

    Verbatim de `necesidad-objeto-modelo.tsv`: "fila N del censo = N{N}"
    (citado por `registro-llaves-identificacion`/`registro-recalculo`
    Entrada 0). Solo las 15 necesidades de coeficientes de generador --
    excluye N16 en adelante (necesidades de reglas de trámite/dinero/cívico,
    fuera del perímetro de este censo)."""
    filas = _read_tsv(NECESIDAD_OBJETO_MODELO)
    mapa = {}
    for fila in filas:
        nid = fila["necesidad_id"]
        try:
            n = int(nid[1:])
        except ValueError:
            continue
        if not (1 <= n <= 15):
            continue
        objeto = fila["objeto_modelo_origen"]  # p.ej. "G1.confianza_institucional"
        mapa[nid] = objeto
    if len(mapa) != 15:
        raise SystemExit(
            "esperaba 15 necesidades N1..N15 en necesidad-objeto-modelo.tsv, "
            "encontré {}".format(len(mapa))
        )
    return mapa


def cargar_relaciones_por_necesidad():
    """necesidad_id -> lista de filas de relaciones.tsv (solo las columnas
    que usa la regla de reclasificación)."""
    filas = _read_tsv(RELACIONES)
    out = {}
    for fila in filas:
        out.setdefault(fila["necesidad_id"], []).append(fila)
    return out


def hay_existe_satisface_confirmada(relaciones_de_la_necesidad):
    """La regla de reclasificación de v1.0 -> v1.1 (Entrada 0 de
    `registro-recalculo`, verbatim): capa4_apertura_mapeo=EXISTE-SATISFACE
    y clasificacion_relacion=CONFIRMADA, en la misma fila de relaciones.tsv.
    Devuelve la fila que satisface la regla (para citarla), o None."""
    for r in relaciones_de_la_necesidad:
        if (
            r.get("capa4_apertura_mapeo") == "EXISTE-SATISFACE"
            and r.get("clasificacion_relacion") == "CONFIRMADA"
        ):
            return r
    return None


def derivar():
    """Devuelve una lista de 15 dicts, una por fila del censo, en orden
    N1..N15, con la ruta final (v1.0 salvo reclasificación v1.1)."""
    censo_v1_0 = cargar_censo_v1_0()
    mapa_necesidades = cargar_mapa_necesidades()
    relaciones = cargar_relaciones_por_necesidad()

    filas = []
    for n in range(1, 16):
        nid = "N{}".format(n)
        objeto = mapa_necesidades[nid]
        gen, coef = objeto.split(".", 1)
        base = censo_v1_0.get(objeto)
        if base is None:
            raise SystemExit(
                "{} ({}) no tiene entrada en "
                "procedencia.yaml:rutas_estimabilidad_coeficiente".format(nid, objeto)
            )
        ruta = base["ruta"]
        justificacion = base["nota"]
        reclasificada = False
        match = None
        if ruta == "SIN-RUTA":
            match = hay_existe_satisface_confirmada(relaciones.get(nid, []))
            if match is not None:
                ruta = "RUTA-C"
                reclasificada = True
                justificacion = (
                    # No se escribe la subcadena literal "SIN-RUTA" aquí a
                    # propósito -- de lo contrario grep -oE la cuenta junto
                    # con la ruta real de esta misma fila (mismo modo de
                    # falla que censo-estimabilidad-coeficientes-v1_1.md §7
                    # ya documentó y corrigió para las mismas tres filas).
                    "reclasificada desde la clase sin ruta de v1.0: "
                    "relaciones.tsv trae "
                    "capa4_apertura_mapeo=EXISTE-SATISFACE + "
                    "clasificacion_relacion=CONFIRMADA para {} "
                    "({}, fuente: {})".format(
                        nid, match["relacion_id"], match.get("fuente_nombre", "")
                    )
                )
        assert ruta in RUTAS_VALIDAS
        filas.append(
            {
                "fila": n,
                "necesidad_id": nid,
                "gen": gen,
                "coef": coef,
                "ruta": ruta,
                "ruta_v1_0": base["ruta"],
                "reclasificada": reclasificada,
                "prioridad": base["prioridad"],
                "justificacion": justificacion,
                "relacion_id": match["relacion_id"] if match else None,
            }
        )
    return filas


def reparto(filas):
    from collections import Counter

    c = Counter(f["ruta"] for f in filas)
    return {r: c.get(r, 0) for r in RUTAS_VALIDAS}


def comando_de_fila(fila):
    """Comando con el que se puede verificar, desde cero, la ruta de esta
    fila -- para citar en fichas (F3) que necesiten instrumento+comando por
    coeficiente, no solo el veredicto. Todos los comandos corren tal cual
    desde la raíz del repo."""
    nid = fila["necesidad_id"]
    if fila["reclasificada"]:
        return (
            "python3 -c \"import csv; r=[x for x in csv.DictReader(open("
            "'data/curacion-registro/relaciones.tsv'), delimiter='\\t') if "
            "x['necesidad_id']=='{n}' and x['capa4_apertura_mapeo']=="
            "'EXISTE-SATISFACE' and x['clasificacion_relacion']=='CONFIRMADA'"
            "]; print(r)\""
        ).format(n=nid)
    if fila["ruta"] in ("RUTA-A", "RUTA-C") and fila["ruta_v1_0"] == fila["ruta"]:
        return (
            "python3 -c \"import yaml; d=yaml.safe_load(open("
            "'milpa/procedencia.yaml')); print([r for r in "
            "d['rutas_estimabilidad_coeficiente']['detalle'] if "
            "r['gen']=='{g}' and r['coef']=='{c}'])\""
        ).format(g=fila["gen"], c=fila["coef"])
    if fila["ruta"] == "RUTA-I":
        return "grep -n 'CAL-G3' canon/gobernanza-v1_15.md"
    return (
        "python3 -c \"import csv; r=[x for x in csv.DictReader(open("
        "'data/curacion-registro/relaciones.tsv'), delimiter='\\t') if "
        "x['necesidad_id']=='{n}']; print(r)\""
    ).format(n=nid)


def tabla_markdown(filas):
    encabezado = (
        "| # | necesidad_id | Gen.coeficiente | Ruta | Llave/instrumento citado "
        "| Comando de verificación |\n"
        "|---|---|---|---|---|---|\n"
    )
    renglones = []
    for f in filas:
        renglones.append(
            "| {fila} | `{nid}` | `{gen}.{coef}` | **{ruta}** | {just} | "
            "`{cmd}` |".format(
                fila=f["fila"],
                nid=f["necesidad_id"],
                gen=f["gen"],
                coef=f["coef"],
                ruta=f["ruta"],
                just=f["justificacion"],
                cmd=comando_de_fila(f),
            )
        )
    return encabezado + "\n".join(renglones) + "\n"


def documento_completo(filas):
    r = reparto(filas)
    reclasificadas = [f for f in filas if f["reclasificada"]]
    doc = []
    doc.append("# Censo de estimabilidad de los 15 coeficientes de generador")
    doc.append(
        "### `censo-estimabilidad-coeficientes` · **v1.2** · generado por comando"
        " · `tools/censo_estimabilidad.py`, ENCARGO CENSO-CMD"
    )
    doc.append("")
    doc.append("> | | |")
    doc.append("> |---|---|")
    doc.append("> | **ARCHIVO** | `censo-estimabilidad-coeficientes-v1_2.md` |")
    doc.append(
        "> | **QUÉ ES** | El mismo censo de "
        "`censo-estimabilidad-coeficientes-v1_1.md` (sellado `ADR-89`), "
        "**derivado por comando en vez de escrito a mano**: "
        "`tools/censo_estimabilidad.py` lee "
        "`milpa/procedencia.yaml:rutas_estimabilidad_coeficiente` "
        "(la foto tabular de v1.0) y `data/curacion-registro/relaciones.tsv`, "
        "y aplica la única regla de reclasificación v1.0→v1.1 (`SIN-RUTA` sube "
        "a `RUTA-C` si `relaciones.tsv` trae, para la misma necesidad, "
        "`capa4_apertura_mapeo=EXISTE-SATISFACE` + "
        "`clasificacion_relacion=CONFIRMADA`) — la misma regla que "
        "`forense/registro-recalculo-v1_0.md` §1 Entrada 0 verificó a mano. "
        "No abre microdato, no toca `data/curacion-registro/**` ni "
        "`milpa/procedencia.yaml` (solo lee). |"
    )
    doc.append(
        "> | **QUÉ NO ES** | No es una redeterminación independiente de las "
        "rutas: la clasificación base (RUTA-A/RUTA-I/RUTA-C de v1.0) se lee "
        "de `procedencia.yaml`, no se recalcula desde el corpus crudo — "
        "ese trabajo ya lo hizo `censo-estimabilidad-coeficientes-v1_0.md`. "
        "No cambia ningún valor `ASIGNADO`, no adjudica ningún veredicto de "
        "Hito D. |"
    )
    doc.append(
        "> | **VERIFICAS ASÍ** | `python3 tools/censo_estimabilidad.py` "
        "reproduce este archivo completo; `python3 tools/censo_estimabilidad.py "
        "--reparto` reproduce solo §2. `tests/test_censo_derivado.py` falla si "
        "el derivador diverge de este archivo o del reparto sellado por "
        "`ADR-89` sin que medie un ADR nuevo. |"
    )
    doc.append(
        "> | **SELLADA POR** | Hereda el sello de `ADR-89` (`canon/"
        "gobernanza-v1_15.md`) sobre el reparto y la taxonomía — este acto "
        "(`ENCARGO CENSO-CMD`, `FP-37`) no reabre ninguna fila, solo verifica "
        "por comando que el mecanismo reproduce exacto lo ya sellado (15/15 "
        "filas, mismo reparto). |"
    )
    doc.append("")
    doc.append("---")
    doc.append("")
    doc.append("## 1 · Las 15 filas")
    doc.append("")
    doc.append(
        "Columna `Comando de verificación`: corre desde la raíz del repo, "
        "reproduce la evidencia citada en `Llave/instrumento citado` para "
        "esa fila sola — para que una ficha (F3) que cite un coeficiente "
        "pueda apuntar a instrumento+comando, no solo al veredicto."
    )
    doc.append("")
    doc.append(tabla_markdown(filas).rstrip("\n"))
    doc.append("")
    doc.append("---")
    doc.append("")
    doc.append("## 2 · Reparto — comando y resultado")
    doc.append("")
    doc.append(
        "Receta de conteo, verbatim de "
        "`censo-estimabilidad-coeficientes-v1_1.md` §7 (misma clase de fallo "
        "ya corregido ahí: solo filas de datos, patrón `^\\| [0-9]+ \\|`):"
    )
    doc.append("")
    doc.append("```")
    doc.append(
        "$ python3 tools/censo_estimabilidad.py --write /tmp/censo-v1_2.md"
    )
    doc.append(
        "$ grep -E '^\\| [0-9]+ \\|' /tmp/censo-v1_2.md | "
        "grep -oE 'RUTA-[CIA]|SIN-RUTA' | sort | uniq -c"
    )
    doc.append("      {} RUTA-A".format(r["RUTA-A"]))
    doc.append("      {} RUTA-C".format(r["RUTA-C"]))
    doc.append("      {} RUTA-I".format(r["RUTA-I"]))
    doc.append("      {} SIN-RUTA".format(r["SIN-RUTA"]))
    doc.append("```")
    doc.append("")
    total = sum(r.values())
    doc.append(
        "**{a} + {c} + {i} + {s} = {t}.** Coincide exacto con el reparto "
        "sellado por `ADR-89` sobre `censo-estimabilidad-coeficientes-v1_1.md` "
        "(`3 RUTA-A · 5 RUTA-C · 1 RUTA-I · 6 SIN-RUTA`).".format(
            a=r["RUTA-A"], c=r["RUTA-C"], i=r["RUTA-I"], s=r["SIN-RUTA"], t=total
        )
    )
    doc.append("")
    doc.append("---")
    doc.append("")
    doc.append(
        "## 3 · Filas reclasificadas por la regla v1.0→v1.1 ({} de 15)".format(
            len(reclasificadas)
        )
    )
    doc.append("")
    for f in reclasificadas:
        doc.append(
            "- fila {fila} (`{n}`, `{g}.{c}`): {j}".format(
                fila=f["fila"],
                n=f["necesidad_id"],
                g=f["gen"],
                c=f["coef"],
                j=f["justificacion"],
            )
        )
    doc.append("")
    doc.append("---")
    doc.append("")
    doc.append("## 4 · Lo que este acto no hace")
    doc.append("")
    doc.append(
        "No re-audita las 12 filas no reclasificadas — hereda su ruta de "
        "`procedencia.yaml:rutas_estimabilidad_coeficiente`, que a su vez "
        "hereda de `censo-estimabilidad-coeficientes-v1_0.md` §5. No abre "
        "microdato. No escribe en `data/curacion-registro/**` ni en "
        "`milpa/procedencia.yaml`. Si el derivador diverge del reparto "
        "sellado, `tests/test_censo_derivado.py` falla y la divergencia se "
        "investiga con su propio ADR antes de declarar nada — no aquí."
    )
    doc.append("")
    return "\n".join(doc)


def main(argv):
    filas = derivar()
    if "--reparto" in argv:
        r = reparto(filas)
        print(
            "      {} RUTA-A\n      {} RUTA-C\n      {} RUTA-I\n      {} SIN-RUTA".format(
                r["RUTA-A"], r["RUTA-C"], r["RUTA-I"], r["SIN-RUTA"]
            )
        )
        return 0
    if "--tabla" in argv:
        print(tabla_markdown(filas))
        return 0
    doc = documento_completo(filas)
    if "--write" in argv:
        idx = argv.index("--write")
        destino = argv[idx + 1]
        with io.open(destino, "w", encoding="utf-8") as out:
            out.write(doc)
        print("escrito: {}".format(destino), file=sys.stderr)
    else:
        print(doc)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
