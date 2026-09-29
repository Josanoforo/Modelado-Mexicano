#!/usr/bin/env python3
"""«Dónde cambió el mexicano» v1.1 (ACTO GEN2-CIERRE-Y-PRODUCTO-3, P3).

v1.0 (`canon/donde-cambio-el-mexicano-v1_0.md`, GEN2-DONDE-CAMBIO-EL-MEXICANO-1) queda
intacto (E.1) y se hereda abajo sin editar. v1.1 añade la serie trimestral ENSU, cuyo
dictamen por serie vive sellado en `CALC-ENSU-SERIE-0001` (FIRMAS-20 A1, FIRMADA) y que
v1.0 no incluía (informe v1.5 §C: «la integración es del siguiente corte»). Se presenta
aparte: su spec, su τ² y su vocabulario son los de su CALC, no los de v1.0, y no se funde
con la tabla de v1.0. Cero cifras tecleadas: todo sale de `resultados.json` verificado.

Escribe canon/donde-cambio-el-mexicano-v1_1.md y
forense/analisis/donde-cambio/tabla-dictamen-ensu-v1_1.tsv.
Uso:  python3 forense/analisis/donde-cambio/genera_donde_cambio_v1_1.py [--verifica]
"""
from __future__ import annotations

import csv
import io
import pathlib
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "forense/analisis/catalogo"))
sys.path.insert(0, str(ROOT / "tools"))
from genera_catalogo import verified  # noqa: E402

CALC = "CALC-ENSU-SERIE-0001"
PREF = "RESULT-ENSU-DICTAMEN-"
V10 = ROOT / "canon/donde-cambio-el-mexicano-v1_0.md"
MD = ROOT / "canon/donde-cambio-el-mexicano-v1_1.md"
TSV = ROOT / "forense/analisis/donde-cambio/tabla-dictamen-ensu-v1_1.tsv"
CAMPOS = ["serie", "dictamen", "direccion", "delta_pp", "k", "ola_ini", "ola_fin", "n_fuera",
          "n_cambio_documentado", "result"]
ORDEN = ("ESTABLE", "CAMBIO-SOSTENIDO", "SALTO-DE-INSTRUMENTO", "SALTO-SIN-EXPLICAR", "SIN-SERIE")


def filas():
    d = verified(CALC)[0]
    bases = sorted(k[: -len("-DICTAMEN")] for k in d if k.startswith(PREF) and k.endswith("-DICTAMEN"))
    out = []
    for b in bases:
        g = lambda s: d.get(f"{b}-{s}", "")  # noqa: E731
        out.append({"serie": b.removeprefix(PREF), "dictamen": g("DICTAMEN"), "direccion": g("DIRECCION"),
                    "delta_pp": "" if g("DELTA-PP") in ("", None) else f"{float(g('DELTA-PP')):.2f}",
                    "k": g("K"), "ola_ini": g("OLA-INI"), "ola_fin": g("OLA-FIN"), "n_fuera": g("N-FUERA"),
                    "n_cambio_documentado": g("N-CAMBIO-DOCUMENTADO"), "result": f"{b}-DICTAMEN"})
    return out


def texto_md(rows) -> str:
    c = Counter(r["dictamen"] for r in rows)
    sube = [r for r in rows if r["dictamen"] == "CAMBIO-SOSTENIDO"]
    L = ["# Dónde sí cambió el mexicano · v1.1", "",
         "> | | |", "> |---|---|",
         "> | **ARCHIVO** | `donde-cambio-el-mexicano-v1_1.md` (sucesor de `v1_0`, que queda intacto — E.1, y se hereda abajo sin editar) |",
         "> | **ACTO** | `GEN2-CIERRE-Y-PRODUCTO-3` (P3) · cero mediciones · RETROSPECTIVA · sin adopción del dictamen |",
         "> | **NUEVO** | la serie trimestral ENSU (`CALC-ENSU-SERIE-0001`, FIRMAS-20 A1), con su propio dictamen sellado; **no se funde** con la tabla de v1.0 |",
         "> | **REGENERA** | `python3 forense/analisis/donde-cambio/genera_donde_cambio_v1_1.py` |", "",
         "«Cambió» es un hecho de la serie, no de la psicología: este documento no atribuye causa. Unidad: puntos "
         "porcentuales de la proporción de personas de `18+` en zonas urbanas que la serie mide (ENSU es urbana: "
         "ninguna fila se lee como «el mexicano»). Todo es RETROSPECTIVA.", "",
         "## Serie ENSU (percepción de inseguridad urbana, trimestral)", "",
         f"{len(rows)} series dictaminadas por el CALC. Vocabulario del propio CALC (mismas cinco palabras que v1.0; "
         "umbrales y τ² los de su spec):", "",
         "| dictamen | series |", "|---|---:|"]
    for k in ORDEN:
        L.append(f"| `{k}` | {c.get(k, 0)} |")
    L += ["", "### `CAMBIO-SOSTENIDO`", "",
          "La dirección es la de los pares COMPARABLE fuera del IC calibrado; el Δ es el que emite el CALC "
          "(`…-DELTA-PP`), y puede no coincidir en signo con la dirección (un tramo que sube de forma sostenida "
          "y cae al final, o al revés): se leen juntos, no se sustituye uno por otro.", "",
          "| serie | dirección | Δ pp (`-DELTA-PP`) | tramo | pares fuera | RESULT |", "|---|---|---:|---|---:|---|"]
    for r in sorted(sube, key=lambda r: (r["direccion"], r["serie"])):
        L.append(f"| `{r['serie']}` | {r['direccion']} | {r['delta_pp']} | {r['ola_ini']}–{r['ola_fin']} | "
                 f"{r['n_fuera']} | `{r['result']}` |")
    L += ["", "Lectura: los cambios sostenidos de ENSU son de percepción urbana. `SALTO-SIN-EXPLICAR` no es "
          "cambio: es un par fuera del IC calibrado sin la regla de cambio sostenido. `SALTO-DE-INSTRUMENTO` "
          "coincide con un cambio documentado de cuestionario o modo (columna `n_cambio_documentado`). Los cuatro "
          "hábitos con «No aplica» en el denominador (C09–C12) no se comparan con comunicados (reserva A1).", "",
          "Tabla por serie: `forense/analisis/donde-cambio/tabla-dictamen-ensu-v1_1.tsv`.", "",
          "## Módulo de auditoría, adenda v1.1", "",
          "- **¿Cuántos contadores movió este trabajo?** Cero: cita un dictamen sellado.",
          "- **[v2.16] ¿PROSPECTIVA o RETROSPECTIVA?** RETROSPECTIVA: todas las olas son anteriores a este documento.",
          "- **[v2.16] ¿Qué unidad y se promedia con otra?** Persona `18+` urbana, en pp; no se suma con series de v1.0.",
          "- **¿Violencia confundida con cultura?** La percepción de inseguridad sigue a la violencia ambiental; "
          "no es un rasgo.",
          "- **¿Sobregeneralización urbana?** ENSU es urbana por diseño.", "",
          "---", "", "# Heredado de v1.0 sin editar", "", V10.read_text(encoding="utf-8")]
    return "\n".join(L)


def main(argv) -> int:
    rows = filas()
    b = io.StringIO()
    w = csv.DictWriter(b, fieldnames=CAMPOS, delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    sal = {TSV: b.getvalue(), MD: texto_md(rows)}
    if "--verifica" in argv:
        malos = [str(p) for p, t in sal.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
        print("COINCIDE" if not malos else "DIFIERE " + " ".join(malos))
        return 1 if malos else 0
    for p, t in sal.items():
        p.write_text(t, encoding="utf-8")
    print(f"series_ensu={len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
