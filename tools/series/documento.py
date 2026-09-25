"""Tabla de dictamen y documento «Dónde sí cambió el mexicano» (DONDE-CAMBIO P4).

Deriva TODO de los RESULT sellados de `CALC-*-SERIE-DICTAMEN-0001` y del mapa
congelado (metadatos de texto). Ninguna cifra se teclea: cada línea con cifras
cita el RESULT del que sale. `tests/test_donde_cambio_documento.py` regenera
ambos archivos y exige igualdad byte a byte.

Uso: PYTHONPATH=. python3 tools/series/documento.py [--escribe]
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

from tools.series import dictamen as D

RAIZ = Path(__file__).resolve().parents[2]
CALC0 = RAIZ / "data/corrida0"
MAPA = RAIZ / "forense/analisis/donde-cambio/mapa"
TABLA = RAIZ / "forense/analisis/donde-cambio/tabla-dictamen-v1_0.tsv"
DOC = RAIZ / "canon/donde-cambio-el-mexicano-v1_0.md"
INSTS = ["ENVIPE", "ENCIG", "ENIF", "ENUT", "ENIGH", "ENOE", "ENDIREH", "MOCIBA", "OTROS"]
COLS = ["serie_id", "instrumento", "dominio", "conducta_texto", "eje", "segmento", "unidad",
        "dictamen", "direccion", "k", "olas", "delta_pp", "pares_fuera", "causa_sin_serie",
        "calc", "result"]


def _pp(x):
    return f"{x:+.1f} pp"


def carga():
    filas = []
    for p in sorted(MAPA.glob("*.tsv")):
        filas += D.lee_mapa(p.read_text(encoding="utf-8"))
    ser = D.series_de(filas)
    ev = D.evaluables(filas)
    res = {}
    for inst in INSTS:
        c = f"CALC-{inst}-SERIE-DICTAMEN-0001"
        res[inst] = (c, json.loads((CALC0 / c / "resultados.json").read_text(encoding="utf-8"))["resultados"])
    return ser, ev, res


def causa(sid, olas, ev, t):
    if t["dictamen"] != "SIN-SERIE":
        return ""
    if len(olas) < 3:
        return "MENOS-DE-3-OLAS-EN-EL-CORPUS"
    if sid not in ev:
        return "COMPARABILIDAD-NO-DOCUMENTADA-O-NO-COMPARABLE"
    if any("FUERA-DE-ESCALA" in o.get("nota", "") for o in olas):
        return "FUERA-DE-ESCALA-(0,1)"
    return "SIN-IC-O-VALOR-EN-FRONTERA"


def tabla(ser, ev, res):
    lineas, filas = ["\t".join(COLS)], []
    for inst in INSTS:
        calc, r = res[inst]
        pref = f"RESULT-DC-{inst}"
        for t in json.loads(r[pref + "-TABLA"]):
            olas = ser[t["serie_id"]]
            o0 = olas[0]
            f = {
                "serie_id": t["serie_id"], "instrumento": o0["instrumento"], "dominio": o0["dominio"],
                "conducta_texto": o0["conducta_texto"].replace("\t", " "), "eje": o0["eje"],
                "segmento": o0["segmento"], "unidad": o0["unidad"].replace("\t", " "),
                "dictamen": t["dictamen"], "direccion": t["direccion"], "k": str(t["k"]),
                "olas": t["olas"], "delta_pp": "" if t["delta_pp"] is None else repr(t["delta_pp"]),
                "pares_fuera": t["pares_fuera"], "causa_sin_serie": causa(t["serie_id"], olas, ev, t),
                "calc": calc, "result": f"{pref}-TABLA#serie_id={quote(t['serie_id'], safe='')}",
            }
            filas.append(f)
            lineas.append("\t".join(f[c] for c in COLS))
    return "\n".join(lineas) + "\n", filas


def documento(filas, res):
    V = D.VOCAB
    tot = Counter(f["dictamen"] for f in filas)
    n = len(filas)
    cita_n = "RESULT-DC-<INST>-N-<DICTAMEN> y RESULT-DC-<INST>-N-SERIES de los nueve CALC-<INST>-SERIE-DICTAMEN-0001"
    # comprobación: el total por dictamen es la suma de los RESULT N-*
    for v in V:
        assert tot[v] == sum(res[i][1][f"RESULT-DC-{i}-N-{v}"] for i in INSTS)
    assert n == sum(res[i][1][f"RESULT-DC-{i}-N-SERIES"] for i in INSTS)
    L = []
    L.append(f"**Resumen.** {n} series (conducta × segmento) dictaminadas: "
             f"{tot['ESTABLE']} ESTABLE · {tot['CAMBIO-SOSTENIDO']} CAMBIO-SOSTENIDO · "
             f"{tot['SALTO-DE-INSTRUMENTO']} SALTO-DE-INSTRUMENTO · {tot['SALTO-SIN-EXPLICAR']} SALTO-SIN-EXPLICAR · "
             f"{tot['SIN-SERIE']} SIN-SERIE — suma de {cita_n}.")
    L.append("")
    L.append("# Dónde sí cambió el mexicano")
    L.append("")
    L.append("ACTO GEN2-DONDE-CAMBIO-EL-MEXICANO-1 · GEN2 · `cuenta_gen2: SI` · `adopta: NO` · "
             "todo lo que sigue es **RETROSPECTIVA** (v2.16 §4): ninguna ola evaluada es posterior al sello "
             "de ninguna emisión. Vocabulario, umbrales y desempate sellados antes del primer dato en "
             "`forense/prereg-caja/DONDE-CAMBIO-spec-v1_0.md` (commit `9aea5a09`); mapa de series congelado sin "
             "valores en `forense/analisis/donde-cambio/mapa/CONGELADO.md`; tabla completa, una fila por serie, "
             "en `forense/analisis/donde-cambio/tabla-dictamen-v1_0.tsv`.")
    L.append("")
    L.append("«Cambió» es un hecho de la serie, no de la psicología (v2.16 §3): este documento no atribuye causa. "
             "Unidad de cada cifra: puntos porcentuales (pp) de la proporción que la serie mide, en la unidad "
             "que declara (persona, hogar, delito o trámite); ninguna cifra de una unidad se suma con otra.")
    L.append("")
    L.append("## Vocabulario (spec §4, primera regla que se cumple)")
    L.append("")
    L.append("- `SIN-SERIE` — menos de tres olas comparables por texto con punto e IC en (0,1).")
    L.append("- `CAMBIO-SOSTENIDO` — dos o más pares COMPARABLE fuera del IC calibrado en la misma dirección, y más que en la contraria.")
    L.append("- `SALTO-DE-INSTRUMENTO` — un par fuera coincidente con un cambio de cuestionario, modo o diseño citado por texto.")
    L.append("- `SALTO-SIN-EXPLICAR` — algún par COMPARABLE fuera sin cumplir la regla de cambio sostenido (término de #972).")
    L.append("- `ESTABLE` — el piso t−1 cubre a t en todos los pares del tramo.")
    L.append("")
    L.append("## Por instrumento")
    L.append("")
    L.append("| instrumento | series | ESTABLE | CAMBIO-SOSTENIDO | SALTO-DE-INSTRUMENTO | SALTO-SIN-EXPLICAR | SIN-SERIE | τ² | RESULT |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for i in INSTS:
        c, r = res[i]
        p = f"RESULT-DC-{i}"
        L.append(f"| {i} | {r[p + '-N-SERIES']} | " + " | ".join(str(r[f'{p}-N-{v}']) for v in
                 ("ESTABLE", "CAMBIO-SOSTENIDO", "SALTO-DE-INSTRUMENTO", "SALTO-SIN-EXPLICAR", "SIN-SERIE"))
                 + f" | {r[p + '-TAU2-FUENTE']} | `{p}-N-*`, `{p}-TAU2-*` |")
    L.append("")
    L.append("τ²: `SELLADO` = parámetro de persistencia ya sellado (ENIF #1009, ENCIG #1041); `CALCULADO-AQUI` = "
             "mismo método, calculado en este acto y emitido como `RESULT-DC-<INST>-TAU2-<EJE>` reutilizable. "
             "OTROS = BANXICO, EDER, ENCUCI, ENFIH, ENNViH, ENSANUT, LAPOP, MOTRAL.")
    L.append("")
    por_dom = defaultdict(list)
    for f in filas:
        por_dom[f["dominio"]].append(f)
    L.append("## Por dominio: qué cambió, qué saltó, qué es estable")
    L.append("")
    for dom in sorted(por_dom):
        fs = por_dom[dom]
        cnt = Counter(f["dictamen"] for f in fs)
        L.append(f"### {dom}")
        L.append("")
        L.append(f"{len(fs)} series: " + " · ".join(f"{cnt[v]} {v}" for v in V if cnt[v])
                 + f" (conteo de filas de `tabla-dictamen-v1_0.tsv`, columna `result` → `RESULT-DC-<INST>-TABLA`).")
        L.append("")
        for v in ("CAMBIO-SOSTENIDO", "SALTO-DE-INSTRUMENTO", "SALTO-SIN-EXPLICAR"):
            sel = [f for f in fs if f["dictamen"] == v]
            if not sel:
                continue
            L.append(f"**{v}**")
            L.append("")
            for f in sel:
                pares = []
                for q in f["pares_fuera"].split(";"):
                    ab, est, dr, mag, m20 = q.split(":")
                    pares.append(f"{ab.replace('>', '→')} {_pp(float(mag[:-2]))} ({est}{', toca 2020' if m20.endswith('SI') else ''})")
                dirx = f" {f['direccion']}" if f["direccion"] != "NINGUNA" else ""
                L.append(f"- `{f['serie_id']}`{dirx} — {f['conducta_texto'][:90]}; unidad {f['unidad'][:40]}; "
                         f"olas {f['olas'].split(',')[0]}–{f['olas'].split(',')[-1]} (k={f['k']}); acumulado "
                         f"{_pp(float(f['delta_pp']))}; pares fuera: {'; '.join(pares)} · `{f['result']}`")
            L.append("")
    # auditoría
    fuera = [f for f in filas if f["dictamen"] in ("CAMBIO-SOSTENIDO", "SALTO-SIN-EXPLICAR", "SALTO-DE-INSTRUMENTO")]
    solo2020 = [f for f in fuera if all(q.endswith("2020=SI") for q in f["pares_fuera"].split(";"))]
    enoe_cs = [f for f in filas if f["instrumento"] == "ENOE" and f["dictamen"] == "CAMBIO-SOSTENIDO"]
    causas = Counter(f["causa_sin_serie"] for f in filas if f["dictamen"] == "SIN-SERIE")
    L.append("## Por qué tantas series son SIN-SERIE")
    L.append("")
    for k2, v2 in causas.most_common():
        L.append(f"- {k2}: {v2} series (columna `causa_sin_serie` de la tabla; dictamen `RESULT-DC-<INST>-TABLA`).")
    L.append("")
    por_inst = Counter((f["instrumento"], f["causa_sin_serie"]) for f in filas if f["dictamen"] == "SIN-SERIE")
    L.append("Por instrumento y causa: " + " · ".join(f"{i} {c} {v}" for (i, c), v in sorted(por_inst.items()))
             + " (misma columna, `RESULT-DC-<INST>-TABLA`).")
    L.append("")
    L.append("La causa dominante es de corpus, no de dato: la mayoría de las celdas del catálogo (ENIF) y de los "
             "pisos (ENDIREH, MOCIBA) existen en una o dos olas. ENDIREH une series entre olas sólo por cadena "
             "idéntica de resultado, eje, categoría y ventana (sin mapeo semántico entre módulos que cambian de "
             "nombre), y no tiene tabla ni spec de comparabilidad por texto: donde sí hay tres olas, el par no se "
             "presume comparable (spec §2, A.15) y la serie se corta. MOCIBA 2016→2017 es NO-COMPARABLE por su propia "
             "spec (`RESULT-DC-MOCIBA-TABLA`). Ese hueco es el entregable: sin crosswalk de módulos y tabla de comparabilidad no hay serie que "
             "dictaminar.")
    L.append("")
    L.append("## Módulo de auditoría de rigor extremo")
    L.append("")
    L.append(f"- **¿Estructura o crisis —2020— y no cultura?** {len(solo2020)} de {len(fuera)} series con par fuera "
             "lo tienen sólo en un par que toca 2020: " + ", ".join(f"`{f['serie_id']}`" for f in solo2020)
             + " (`RESULT-DC-<INST>-TABLA`, campo `pares_fuera`, marca `2020=SI`). Son candidatas a estructura o crisis, no a cultura.")
    L.append(f"- **Los {len(enoe_cs)} CAMBIO-SOSTENIDO son todos ENOE y no se leen como cambio de conducta.** "
             "Acumulados entre " + f"{_pp(min(float(f['delta_pp']) for f in enoe_cs))} y {_pp(max(float(f['delta_pp']) for f in enoe_cs))}"
             " (`RESULT-DC-ENOE-<SERIE>-DELTA-PP`), con pares fuera en ambas direcciones: la regla sellada los cuenta "
             "porque el IC muestral de ENOE es estrecho y su τ² calculado aquí es pequeño "
             "(`RESULT-DC-ENOE-TAU2-*`); la spec de ENOE declara que no hay covarianza longitudinal estimable "
             "(`SIN-COVARIANZA-LONGITUDINAL`). No se reinterpreta la regla (PARO d); se declara aquí.")
    L.append("- **¿Pobreza, violencia o informalidad confundidas con cultura?** El dictamen no atribuye causa. Una "
             "caída de la no denuncia (ENVIPE) o del desaliento laboral (ENOE) es compatible con cambios de "
             "incidencia, de mercado laboral o de oferta institucional antes que de disposición.")
    L.append("- **¿Sobregeneralización desde clase media urbana?** ENCIG cubre ciudades de 100 mil o más "
             "(universo de los CALC-ENCIG-SERIE-CANAL-* que consume `RESULT-DC-ENCIG-TABLA`); sus dictámenes no hablan de lo rural.")
    L.append("- **¿Qué afirmación sobre el corpus fue escrita a mano?** Ninguna cifra de este documento: se regenera "
             "desde los RESULT sellados (`tests/test_donde_cambio_documento.py`).")
    L.append("- **¿Cuántos contadores movió este trabajo?** Nueve CALC sellados con `cuenta_gen2: SI`, `adopta: NO` "
             "(`CALC-<INST>-SERIE-DICTAMEN-0001`); ninguna adopción, ningún movimiento de `celdas_validadas`.")
    L.append("- **PROSPECTIVA/RETROSPECTIVA:** todo RETROSPECTIVA; ninguna frase mezcla columnas.")
    L.append("- **Unidad:** cada serie conserva la suya (columna `unidad`); ninguna suma cruza persona, hogar, delito o trámite.")
    L.append("- **Lo que sería peligroso leído simplista:** «ESTABLE» no es «no cambió nada»: es que el piso de la ola "
             "anterior cubre a la siguiente con el IC calibrado; un IC ancho vuelve ESTABLE casi cualquier serie.")
    L.append("")
    L.append("## Sucesores")
    L.append("")
    L.append("Informe v1.3 §«dónde cambió»; U4 (familias 2027) toma los CAMBIO-SOSTENIDO como candidatos a estimando "
             "prospectivo, con la reserva ENOE de arriba. Tablas de comparabilidad por texto para ENDIREH y las "
             "conductas ENIF sin tabla convertirían SIN-SERIE en series dictaminables.")
    L.append("")
    return "\n".join(L)


def main():
    ser, ev, res = carga()
    t, filas = tabla(ser, ev, res)
    d = documento(filas, res)
    if "--escribe" in sys.argv:
        TABLA.write_text(t, encoding="utf-8")
        DOC.write_text(d, encoding="utf-8")
    print(d.splitlines()[0])
    return t, d


if __name__ == "__main__":
    main()
