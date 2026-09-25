#!/usr/bin/env python3
"""Inventario de las 34 lecturas legacy del consumidor `motor` (ACTO GEN2-RELEVO-MOTOR-34-1, P1/P4).

Universo: filas de `tools/relevo_usos.py --json` cuyo consumidor cae en el
bucket `motor` de `corrida0._legacy_por_consumidor` (milpa/tramite.yaml o
milpa/src/) y que en la vista de ORIGIN/MAIN (`git show origin/main:data/corrida0/usos.tsv`)
leían LEGACY-GEN1. Escribe `inventario-34-v1_0.tsv` junto a este archivo.
Uso: python3 forense/analisis/relevo-motor/inventario_motor34.py
"""
from __future__ import annotations

import csv
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import escribe_relevo_consumo as E  # noqa: E402

SALIDA = Path(__file__).with_name("inventario-34-v1_0.tsv")

# Destino de las lecturas que NO releva el escritor: razón A.14 + motivo.
RESIDUO = {
    **{r: ("DECISIÓN-DE-MESA-PENDIENTE", "ASIGNADO sin estimando declarado; la regla ya trae conductas GEN2 medidas, pero emitir_binaria devuelve este par (tramite.yaml:65-67); cambiar qué devuelve es semántica del motor, no relevo")
       for r in ("RES-0001", "RES-0002", "RES-0007", "RES-0008", "RES-0019", "RES-0020", "RES-0023", "RES-0024")},
    **{r: ("DIFERIDO-A:GEN2-RELEVO-MOTOR-34-2-CAJA", "ASIGNADO sin ninguna medición GEN2 en la regla (fuente validación CoDi); exige CALC nuevo desde microdato en CAJA")
       for r in ("RES-0017", "RES-0018")},
    **{r: ("DECISIÓN-DE-MESA-PENDIENTE", "uso_motor NO-ADOPTAR-NC-0107 (variante deduplicada discrepante, «conservar sólo como historia») pero activa en el motor; el veredicto sellado es NO-ADOPTABLE")
       for r in ("RES-0009", "RES-0010", "RES-0011", "RES-0012")},
    **{r: ("DIFERIDO-A:GEN2-RELEVO-MOTOR-34-2-CAJA", "GEN1 de ENNViH/MxFLS olas 2-3 sin CALC (E.1: re-medir desde crudo); payloads ennvih2_2005_*/ennvih3_2009_* en el manifiesto")
       for r in ("RES-0029", "RES-0030")},
    **{r: ("DIFERIDO-A:GEN2-RELEVO-MOTOR-34-2-CAJA", "CALC-L8-CONVERSION-0001 reproduce pero ingiere data/l8-resultados-tipo-boleta-v1_0.json (origen repo, número GEN1): por 4.1 no releva; re-medir desde cómputos crudos")
       for r in ("RES-0050", "RES-0051", "RES-0052")},
    **{r: ("DECISIÓN-DE-MESA-PENDIENTE", "partición categórica sellada (milpa/src/celdas.py:CORTES_C1, ADR-537 / ADR-100(2)); no hay RESULT numérico que la releve y reclasificarla fuera del contador es tocar el contador")
       for r in ("RES-0165", "RES-0166", "RES-0167", "RES-0168", "RES-0169", "RES-0170")},
}


def _legacy_en_origin_main() -> set[str]:
    crudo = subprocess.run(["git", "show", "origin/main:data/corrida0/usos.tsv"],
                           cwd=ROOT, capture_output=True, text=True, check=True).stdout
    lineas = [l for l in crudo.splitlines() if not l.startswith("#")]
    return {f["resultado_id"] for f in csv.DictReader(lineas, delimiter="\t")
            if f["activo"] == "SI" and f["generacion_leida"] == "LEGACY-GEN1"
            and (f["consumidor"].startswith("milpa/tramite.yaml")
                 or f["consumidor"].startswith("milpa/src/"))}


def main() -> None:
    oferta = {r["resultado_id"]: r for r in json.loads(subprocess.run(
        [sys.executable, str(ROOT / "tools/relevo_usos.py"), "--json"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout)}
    relevos = {f"milpa/tramite.yaml:{r[0]}:{r[1]}": r for r in E.RELEVOS_V3}
    universo = sorted(_legacy_en_origin_main())
    filas = []
    for res in universo:
        o = oferta[res]
        rel = relevos.get(o["consumidor"])
        if rel:
            fila = {"via": rel[4], "calc_gen2": rel[2], "result_gen2": rel[3],
                    "estado": "RELEVADO-POR-ESCRITOR", "razon": "cuatro guardas 4.1 (+D6) en tools/escribe_relevo_consumo.py::guardas_v3"}
        else:
            razon, motivo = RESIDUO[res]
            fila = {"via": "RESIDUO", "calc_gen2": o.get("calc_candidato", ""),
                    "result_gen2": o.get("result_gen2_candidato", ""),
                    "estado": razon, "razon": motivo}
        filas.append({"resultado_id": res, "consumidor": o["consumidor"],
                      "tipo_uso": o["tipo_uso"], "valor_legacy": o["valor_legacy"],
                      "veredicto_relevo_usos_al_derivar": o["veredicto"], **fila})
    if len(filas) != 34 or set(RESIDUO) | {r for r in universo if oferta[r]["consumidor"] in relevos} != set(universo):
        raise SystemExit(f"UNIVERSO-DISCORDANTE: {len(filas)} filas")
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(filas[0]), delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(filas)
    SALIDA.write_text(buf.getvalue(), encoding="utf-8")
    print(f"{len(filas)} lecturas · relevadas {sum(f['via'] != 'RESIDUO' for f in filas)} · "
          f"residuo {sum(f['via'] == 'RESIDUO' for f in filas)} -> {SALIDA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
