#!/usr/bin/env python3
"""Deriva la evidencia física de las 17 aperturas de M-APERTURA sobre la generación v7.

Produce `b2-v7-mapertura-17-observacion.tsv`. NO corrige capa 4 y no emite propuestas
semánticas: corregir capa 4 exige la vía fail-closed del §19 (C5), que el encargo de
ACTO B2-V7 declara PARO. Esto es el insumo medido que esa corrección necesitaría.

Reglas duras aplicadas, ambas por defectos ya pagados en este proyecto:
  · el join va por igualdad EXACTA de id, jamás por subcadena. Medido: 7 de los 20 ids
    son prefijo de otros ids que también están en el ledger (`mex_2011_lfepie_v01_m`
    está contenido en tres más), así que un match por `in` produce falsos positivos.
  · el veredicto físico NO se lee de `estado_terminal` del ledger. En la generación v7
    ese campo —y con él `estado`, `parser`, `build_sha256` y `reporte_sha256`— quedó
    no fiable para 376 filas por un defecto del validador de privacidad, ya diagnosticado
    (ADR-98(f)). La verdad está en el expediente de `staging-v7`, y de ahí se lee.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

REPO = Path("/home/pc0/Modelado-Mexicano-barrido2")
LISTA = REPO / "data/lista-apertura-enlace2-2026-08-14.tsv"
LEDGER = REPO / ".barrido2/private/t0/ledger-v7.tsv"
STAGING = REPO / ".barrido2/staging-v7"
RELACIONES = REPO / "data/curacion-registro/relaciones.tsv"
SALIDA = REPO / "data/curacion-registro/b2-v7-mapertura-17-observacion.tsv"

CAMPOS = [
    "relacion_id", "necesidad_id", "fuente_canonica_normalizada", "grupo_payload",
    "capa2_actual", "capa4_actual", "id_manifiesto_anclado_en_relaciones",
    "id_manifiesto_que_provee", "representacion_id", "sha256_12", "wave_initial",
    "veredicto_fisico", "registros_indice", "registros_excepcion", "prohibicion_18_8",
]


def leer_tsv(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main() -> int:
    lista = [f for f in leer_tsv(LISTA) if f["en_manifiesto"].strip() == "SI"]
    rel = {r["relacion_id"]: r for r in leer_tsv(RELACIONES)}

    # índice del ledger por payload, igualdad exacta, mirando también payload_ids_json
    por_payload: dict[str, dict[str, str]] = {}
    for fila in leer_tsv(LEDGER):
        for pid in {fila["payload_id"], *json.loads(fila["payload_ids_json"])}:
            por_payload.setdefault(pid, fila)

    # el grupo de payload es la cadena exacta de la columna, no el nombre de la fuente
    grupos: dict[str, str] = {}
    for f in lista:
        clave = f["ids_manifiesto_que_lo_proveen"].strip()
        if clave not in grupos:
            grupos[clave] = f"G{len(grupos) + 1}"

    filas: list[list[str]] = []
    for f in lista:
        rid = f["relacion_id"].strip()
        r = rel.get(rid, {})
        anclado = (r.get("id_manifiesto") or "NO_DETERMINADO").strip() or "NO_DETERMINADO"
        capa4 = (r.get("capa4_apertura_mapeo") or "NO-DETERMINABLE").strip()
        grupo = grupos[f["ids_manifiesto_que_lo_proveen"].strip()]
        for pid in [i.strip() for i in f["ids_manifiesto_que_lo_proveen"].split(";") if i.strip()]:
            led = por_payload.get(pid)
            if led is None:
                filas.append([rid, f["necesidad_id"], f["fuente_canonica_normalizada"], grupo,
                              f["capa2_actual"], capa4, anclado, pid, "NO-APLICA", "NO-APLICA",
                              "NO-APLICA", "NO-LLEGO-AL-BARRIDO", "0", "0", "NO-APLICA"])
                continue
            exp = STAGING / led["tarea_id"]
            indice = exp / "e2-neutral-index.jsonl"
            total = excep = 0
            with indice.open(encoding="utf-8") as fh:
                for linea in fh:
                    if not linea.strip():
                        continue
                    total += 1
                    if json.loads(linea).get("estado") == "EXCEPCION-ESPECIFICA":
                        excep += 1
            veredicto = "OBSERVADO-CON-EXCEPCION" if excep else "OBSERVADO-E2"
            # §18.8: una celda no puede cerrar en INDEXADO-NO-DESCARGADO si el payload se observó
            infringe = "INFRINGE-18.8" if capa4 == "INDEXADO-NO-DESCARGADO" else "NO-APLICA"
            filas.append([rid, f["necesidad_id"], f["fuente_canonica_normalizada"], grupo,
                          f["capa2_actual"], capa4, anclado, pid, led["representacion_id"],
                          led["sha256"][:12], led["wave_initial"], veredicto,
                          str(total), str(excep), infringe])

    for fila in filas:
        assert len(fila) == len(CAMPOS)
        for celda in fila:
            assert celda != "" and "\t" not in celda and "\n" not in celda
    SALIDA.write_text(
        "\n".join("\t".join(x) for x in [CAMPOS, *filas]) + "\n", encoding="utf-8")

    relaciones = {x[0] for x in filas}
    print(json.dumps({
        "relaciones": len(relaciones),
        "pares_relacion_payload": len(filas),
        "payloads_distintos": len({x[7] for x in filas}),
        "grupos_de_payload": len(grupos),
        "veredictos": {v: sum(1 for x in filas if x[11] == v)
                       for v in sorted({x[11] for x in filas})},
        "relaciones_que_infringen_18_8": len({x[0] for x in filas if x[14] == "INFRINGE-18.8"}),
        "anclaje_util": sum(1 for x in filas if x[6] == x[7]),
        "registros_indice_totales": sum(int(x[12]) for x in
                                        {x[7]: x for x in filas}.values()),
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
