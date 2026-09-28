#!/usr/bin/env python3
"""Inventario de olas reservadas y vista de aperturas — ACTO GEN2-APERTURAS-PREREGISTRADAS-1.

Uso:
    python3 forense/prereg-aperturas/inventario_aperturas.py            # imprime (no escribe; D-23)
    python3 forense/prereg-aperturas/inventario_aperturas.py --escribe  # escribe la vista y los expedientes mínimos
    python3 forense/prereg-aperturas/inventario_aperturas.py --verifica # 0 si la vista casa con la derivación

Universo (A.15, por id): `data/manifiesto.yaml`, entradas cuyo campo `estado_reserva`
empieza por `RESERVADA` (vocabulario observado el 28/sep: `RESERVADA-NO-ABIERTA-NO-INDEXAR-L`,
`RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO-ABRIR`; `DOCUMENTACION-ESTRUCTURAL-NO-RESPUESTAS`
no es reserva de respuestas y queda fuera). Se agrupan por programa × ola por prefijo de id.
Se añaden las olas que la reserva nombra por firma sin campo en el manifiesto (FIRMA_SIN_CAMPO).

`cruces_vistos` se DERIVA: todo `data/corrida0/CALC-*/spec.yaml` que nombra un id reservado.
`contendientes` y `familia` son la tabla CONTENDIENTES (LEÍDO, con cita) — regla 6: sólo sellados.
"""
from __future__ import annotations

import functools
import glob
import os
import re
import sys
from collections import defaultdict

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VISTA = "data/corrida0/aperturas-pendientes-v1_0.tsv"
EXP = "forense/prereg-aperturas"
COLUMNAS = ("programa", "ola", "n_ids", "ids", "estado_reserva", "contendientes", "familia",
            "cruces_vistos", "expediente", "que_la_abre", "firma_que_faltaria", "nota")

# (programa, ola) -> (contendientes, familia 2027 que la usa como R, cita LEÍDO)
CONTENDIENTES = {
    ("ENSANUT", "2025"): ("CALC-ENSANUT-PISOS-SALUD-0001", "NINGUNA",
                          "spec.yaml:22 ola_reservada: ENSANUT 2025; SALUD-ENSANUT-PISOS-spec §4 ICC sobre piso 2024"),
    ("ENCODAT", "2025"): ("CALC-ENCODAT-PISOS-SUSTANCIAS-0001", "NINGUNA",
                          "spec.yaml:22 ola_reservada: ENCODAT 2025; una ola abierta, IC de diseño"),
}
# olas reservadas por firma o encargo sin campo `estado_reserva` en el manifiesto
# (programa, ola) -> (patrón de ids de microdato, estado, nota)
FIRMA_SIN_CAMPO = {
    ("ENVIPE", "2026"): (r"^envipe2026_csv$", "PREMISA-CAIDA-YA-ABIERTA",
                         "memoria §1 y encargo la dan por reservada; el código congelado CALC-DUELO-ENVIPE2026-ADJUDICACION-0001 "
                         "(ejecucion.json 2026-09-22T20:19Z) y CALC-DUELO-ENVIPE2026-MARGINALES-ADJUDICACION-0001 (2026-09-23T01:01Z) "
                         "ya la abrieron por E.6 (prueba pre-registrada); envipe2026_csv sin estado_reserva"),
    ("ENIGH", "2024"): (r"^(enigh2024_nc_csv|cc1_inegi_enigh_2024__enigh2024_ns_.*)$", "FIRMA-SIN-CAMPO",
                        "memoria §1: ENIGH 2024 reservada salvo seis columnas AMAI (C7); ningún id enigh 2024 lleva estado_reserva. "
                        "Apertura parcial ya hecha por código congelado: CALC-AMAI-NSE-ENIGH-2024-0001 (C7) y el duelo nacional de remesas "
                        "(CALC-ENIGH-DUELO-ADJUDICACION-0001, guardián tools/enigh_duelo_guardian.py: solo la columna remesas); el resto sigue reservado"),
    ("ENIF", "2024"): (r"^(enif2024_csv|enif_2024_enif_2024_bd_csv)$", "PREMISA-CAIDA-YA-ABIERTA",
                       "encargo §5 la nombra; CALC-C2-COMPUESTO-IC-ENIF2024-0001 ya la abrió (tests/test_c2_ic_enif2024_guardia.py); sin estado_reserva"),
}


@functools.lru_cache(maxsize=1)
def _manifiesto():
    with open(os.path.join(RAIZ, "data", "manifiesto.yaml"), encoding="utf-8") as f:
        return yaml.load(f, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))


def _reservadas(m):
    return [e for e in m if str(e.get("estado_reserva", "")).startswith("RESERVADA")]


def reservados_del_manifiesto():
    return [e["id"] for e in _reservadas(_manifiesto())]


def archivos_reservados_del_manifiesto():
    return [str(e["archivo"]) for e in _reservadas(_manifiesto()) if e.get("archivo")]


def programa_ola(i: str):
    m = re.match(r"cc1_inegi_([a-z]+)_(\d{4})(t\d)?__", i)
    if m:
        return m.group(1).upper(), m.group(2) + (m.group(3).upper() if m.group(3) else "")
    m = re.match(r"oe1_([a-z]+)_(\d{4})_", i)
    if m:
        return m.group(1).upper(), m.group(2)
    if i.startswith("cses5_"):
        return "CSES", "MODULO5-2016-2021"
    m = re.match(r"enoe_(\d{4})_(\d)t_", i)
    if m:
        return "ENOE", f"{m.group(1)}T{m.group(2)}"
    m = re.match(r"([a-z]+)_(\d{4})_", i)
    if m:
        return m.group(1).upper(), m.group(2)
    return i.upper(), "?"


def _specs():
    out = {}
    for p in sorted(glob.glob(os.path.join(RAIZ, "data", "corrida0", "CALC-*", "spec.yaml"))):
        with open(p, encoding="utf-8") as f:
            out[os.path.basename(os.path.dirname(p))] = f.read()
    return out


def _dir(prog, ola):
    return f"{EXP}/{prog}-{ola}"


def filas():
    todo = _manifiesto()
    m = _reservadas(todo)
    g = defaultdict(list)
    for e in m:
        g[programa_ola(e["id"])].append(e)
    extra = {k: sorted(e["id"] for e in todo if re.match(v[0], e["id"])) for k, v in FIRMA_SIN_CAMPO.items()}
    specs = _specs()
    out = []
    for k in sorted(set(g) | set(FIRMA_SIN_CAMPO)):
        prog, ola = k
        es = g.get(k, [])
        ids = sorted(e["id"] for e in es) or extra.get(k, [])
        pat = re.compile(r"\b(?:" + "|".join(map(re.escape, ids)) + r")\b") if ids else None
        vistos = sorted(c for c, t in specs.items() if pat and pat.search(t))
        cont, fam, cita = CONTENDIENTES.get(k, ("NINGUNO", "NINGUNA", ""))
        estado = ";".join(sorted({str(e["estado_reserva"]) for e in es})) or FIRMA_SIN_CAMPO[k][1]
        nota = [cita] if cita else []
        if k in FIRMA_SIN_CAMPO:
            nota.append(FIRMA_SIN_CAMPO[k][2])
        if vistos and not estado.startswith("PREMISA-CAIDA"):
            nota.append("CRUCE-VISTO: id reservado consumido por CALC sellado; el campo estado_reserva no lo refleja (hallazgo; solo mesa re-rotula)")
        if cont != "NINGUNO":
            abre = "CODIGO-CONGELADO(expediente) en caja, previa firma de mesa que congele el expediente como COMMIT-1 de apertura"
            falta = f"FIRMA-DE-MESA: congelar {_dir(prog, ola)} y autorizar su apertura"
        elif estado == "PREMISA-CAIDA-YA-ABIERTA":
            abre, falta = "YA-ABIERTA", "NINGUNA"
        else:
            abre = "SOLO-MESA-POR-ESCRITO (sin prueba pre-registrada)"
            falta = "FIRMA-DE-MESA por escrito, o un contendiente sellado antes de abrir (regla 6: ninguno nuevo en esta etapa)"
        out.append({"programa": prog, "ola": ola, "n_ids": str(len(ids)), "ids": ";".join(ids),
                    "estado_reserva": estado, "contendientes": cont, "familia": fam,
                    "cruces_vistos": ";".join(vistos) or "NINGUNO", "expediente": _dir(prog, ola),
                    "que_la_abre": abre, "firma_que_faltaria": falta, "nota": " · ".join(nota)})
    return out


def _tsv(rows):
    # Cabecera de procedencia, no `# DERIVADO — NO EDITAR`: esa marca reserva el archivo al canal
    # [deriva] (tools/derivados_protegidos.py); esta vista viaja versionada, como el crosswalk de carriles.
    lin = [f"# {VISTA} · ACTO GEN2-APERTURAS-PREREGISTRADAS-1 · derivado por `python3 forense/prereg-aperturas/inventario_aperturas.py --escribe` (--verifica compara byte a byte). Nunca a mano.",
           "\t".join(COLUMNAS)]
    lin += ["\t".join(r[c].replace("\t", " ") for c in COLUMNAS) for r in rows]
    return "\n".join(lin) + "\n"


def _minimo(r):
    return (f"# Expediente mínimo de apertura · {r['programa']} {r['ola']}\n\n"
            f"Derivado por `forense/prereg-aperturas/inventario_aperturas.py --escribe` (ACTO GEN2-APERTURAS-PREREGISTRADAS-1).\n\n"
            f"- Estado de reserva: `{r['estado_reserva']}` · ids ({r['n_ids']}): fila de `{VISTA}`.\n"
            f"- Contendientes sellados que la nombran como R: **{r['contendientes']}** · familia 2027: **{r['familia']}**.\n"
            f"- Cruces vistos (CALC sellados que consumen un id): {r['cruces_vistos']}.\n"
            + (f"- **Ya abierta por código congelado** (premisa del encargo caída): {r['que_la_abre']}.\n"
               if r["que_la_abre"] == "YA-ABIERTA" else
               f"- **Sin prueba pre-registrada: solo mesa por escrito.** Qué la abre: {r['que_la_abre']}.\n")
            + f"- Nota: {r['nota'] or '—'}\n")


def main(argv):
    rows = filas()
    if "--verifica" in argv:
        with open(os.path.join(RAIZ, VISTA), encoding="utf-8") as f:
            casa = f.read() == _tsv(rows)
        print(f"{VISTA}: {'CASA' if casa else 'NO-CASA'}")
        return 0 if casa else 1
    if "--escribe" not in argv:
        sys.stdout.write(_tsv(rows))
        return 0
    with open(os.path.join(RAIZ, VISTA), "w", encoding="utf-8") as f:
        f.write(_tsv(rows))
    for r in rows:
        if r["contendientes"] == "NINGUNO":
            d = os.path.join(RAIZ, r["expediente"])
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, f"EXPEDIENTE-{os.path.basename(d)}.md"), "w", encoding="utf-8") as f:
                f.write(_minimo(r))
    print(f"filas={len(rows)} ids={sum(int(r['n_ids']) for r in rows)} vista={VISTA}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
