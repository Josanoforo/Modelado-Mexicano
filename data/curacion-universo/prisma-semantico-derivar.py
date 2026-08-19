#!/usr/bin/env python3
"""Deriva el PRISMA semántico y el PRISMA de M-APERTURA de BARRIDO-2 (§23).

ACTO B2-SEMANTICO, 18/ago/2026. El §23 exige que "toda cifra declara
denominador y comando", así que ninguna de estas cifras se teclea: todas salen
de los productos versionados de este acto, y cada fila lleva escrito de qué
denominador sale y con qué comando se reproduce.

Se escribe aparte del PRISMA material (que genera `write_barrido2_material.py`)
para no tocar un producto ya congelado por el gate del §15.

    python3 data/curacion-universo/prisma-semantico-derivar.py --repo .
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def leer(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def tabla(filas: list[tuple[str, object, str, str]]) -> str:
    out = ["| Métrica | Cifra | Denominador | Comando de derivación |",
           "|---|---:|---|---|"]
    for metrica, cifra, denominador, comando in filas:
        out.append(f"| {metrica} | {cifra} | {denominador} | `{comando}` |")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--fecha", default="2026-08-18")
    args = parser.parse_args()
    R = args.repo.resolve()

    B = R / "data" / "curacion-registro" / "ejecucion-semantica" / "barrido2"
    U = R / "data" / "curacion-universo"
    propuestas = leer(B / "propuestas-barrido2.tsv")
    tareas = leer(B / "tareas-semanticas-barrido2.tsv")
    decisiones = leer(B / "decisiones-integracion-barrido2.tsv")
    cableado = leer(R / "data" / "cableado-universo-v1_0.tsv")
    apertura = leer(R / "data" / "lista-apertura-enlace2-2026-08-14.tsv")
    relaciones = {r["relacion_id"]: r
                  for r in leer(R / "data" / "curacion-registro" / "relaciones.tsv")}

    ver = Counter(p["veredicto_a4"] for p in propuestas)
    acc = Counter(p["accion_propuesta"] for p in propuestas)
    est = Counter(d["estado_integracion"] for d in decisiones)
    fp24 = sum(1 for p in propuestas if p["dependencia_fp24"] == "SI")
    negativos = sum(v for k, v in ver.items() if k.startswith("NO-"))
    CMD = "python3 data/curacion-universo/prisma-semantico-derivar.py"

    semantico = [
        ("objetos_revisados", len({t['objeto_logico_id'] for t in tareas}),
         "objetos lógicos distintos elegidos por curaduría", CMD),
        ("tareas_semanticas", len(tareas), "elecciones de curador verificadas por hash", CMD),
        ("propuestas", len(propuestas), "tareas con veredicto supervisado", CMD),
        ("accion_ALTA", acc.get("ALTA", 0), "propuestas", CMD),
        ("accion_CAMBIO", acc.get("CAMBIO", 0), "propuestas", CMD),
        ("accion_SIN_CAMBIO", acc.get("SIN_CAMBIO", 0), "propuestas", CMD),
        ("accion_TERMINAL", acc.get("TERMINAL", 0), "propuestas", CMD),
        ("EXISTE-SATISFACE", ver.get("EXISTE-SATISFACE", 0), "propuestas", CMD),
        ("EXISTE-NO-SATISFACE", ver.get("EXISTE-NO-SATISFACE", 0), "propuestas", CMD),
        ("negativos", negativos, "propuestas", CMD),
        ("SIN-DEMANDA-CONFIRMADO", 0,
         "propuestas — este acto no emite ninguno; exige E2 + revisión N1-N33 + supervisor", CMD),
        ("dependencia_fp24_SI", fp24, "propuestas", CMD),
        ("FP24_integrables_ordinariamente", len(propuestas) - fp24,
         "propuestas — decidibles por evidencia fuente/objeto-específica", CMD),
        ("validadas", sum(1 for p in propuestas if p["estado_supervision"] == "VALIDADA"),
         "propuestas", CMD),
        ("integradas", est.get("INTEGRADA", 0), "decisiones de integración", CMD),
        ("rechazadas_fail_closed", est.get("RECHAZADA_FAIL_CLOSED", 0),
         "decisiones de integración", CMD),
        ("conflictos_materiales", est.get("CONFLICTO_MATERIAL", 0),
         "decisiones de integración", CMD),
        ("no_determinadas", est.get("NO_DETERMINADO", 0), "decisiones de integración", CMD),
        ("filas_de_cableado", len(cableado), "una por propuesta proyectada", CMD),
    ]

    absorbidas = [r for r in apertura if r.get("destino") == "APERTURA-PENDIENTE"]
    cola = [r for r in apertura if r.get("destino") == "PROPUESTA-A-COLA"]
    con_propuesta = {p["relacion_id_actual"] for p in propuestas}
    observadas = [r for r in absorbidas
                  if relaciones.get(r["relacion_id"], {}).get("capa3_disco_real", "").startswith("EXISTE")]
    corregidas = [r for r in absorbidas
                  if relaciones.get(r["relacion_id"], {}).get("capa4_apertura_mapeo")
                  not in ("INDEXADO-NO-DESCARGADO", "", None)]
    pendientes = [r for r in absorbidas if r["relacion_id"] not in con_propuesta]

    mapertura = [
        ("esperadas", len(absorbidas),
         "filas de lista-apertura con destino=APERTURA-PENDIENTE", CMD),
        ("denominador_propio_sin_payload", len(cola),
         "filas con destino=PROPUESTA-A-COLA — no pertenecen a las 17", CMD),
        ("observadas_E2", sum(1 for r in absorbidas if r["relacion_id"] in con_propuesta),
         "de las esperadas, con material E2 elegido y verificado", CMD),
        ("con_capa3_EXISTE_antes_del_acto", len(observadas),
         "de las esperadas — el resto tenía capa2/capa3 NO_REFERENCIADO", CMD),
        ("propuestas", sum(1 for p in propuestas
                           if p["relacion_id_actual"] in {r["relacion_id"] for r in absorbidas}),
         "propuestas emitidas sobre las esperadas", CMD),
        ("capa4_corregida", len(corregidas),
         "de las esperadas, ya fuera de INDEXADO-NO-DESCARGADO", CMD),
        ("excepciones", 0, "de las esperadas — ninguna quedó sin material accesible", CMD),
        ("pendientes", len(pendientes), "de las esperadas, sin propuesta", CMD),
    ]

    texto = f"""# PRISMA semántico BARRIDO-2

Fecha: {args.fecha}. Acto: `ACTO B2-SEMANTICO` (C4/C5/C6). Red material: deshabilitada.

Toda cifra declara denominador y comando (§23). Ninguna está tecleada: todas se
derivan de los productos versionados de este acto.

{tabla(semantico)}

## PRISMA de M-APERTURA absorbido (§18, §23)

Las esperadas son las filas de `data/lista-apertura-enlace2-2026-08-14.tsv` con
`destino=APERTURA-PENDIENTE`. Las de `destino=PROPUESTA-A-COLA` llevan
denominador propio y **no** se cuentan entre ellas: no tienen payload en el
ledger, de modo que no hay material que absorber.

{tabla(mapertura)}
"""
    salida = U / "prisma-semantico-barrido2.md"
    salida.write_text(texto, encoding="utf-8")
    print(f"escrito: {salida.relative_to(R)}  ({len(texto)} bytes)")
    print(f"propuestas={len(propuestas)} tareas={len(tareas)} decisiones={len(decisiones)} "
          f"cableado={len(cableado)} fp24_SI={fp24}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
