#!/usr/bin/env python3
"""GEN2-L-DESDE-CAPTURAS-1 · CALC que produce L por celda y por variante desde
las 224 capturas selladas de `corridas-L-completa-v1_0/`, con el agregador
`tools/agrega_l_v1_0.py` (mediana, dispersión MAD, IC bootstrap).

No re-decide la regla de inválidas (sellada en F5-completa-spec-v1_0.md §4,
10/sep/2026, anterior a este acto) ni el agregador (mediana, misma spec §4).
No re-extrae con un extractor nuevo: reutiliza `tools/calcula_f5_completa.py
::extraer` vía `tools/agrega_l_v1_0.py`.

También produce P4: la tabla de diferencias contra GEN1, descompuesta en
(1) efecto del agregador (media GEN1 vs mediana sobre el MISMO conjunto
v1.2, cuando reconstruible) y (2) efecto del conjunto de extracción
(mediana v1.2 vs mediana sobre las 224 capturas completas).
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from agrega_l_v1_0 import agregar_celda, extraer  # noqa: E402

DIR = ROOT / "forense/prereg-duelo-v2"
PLAN = DIR / "F5-completa-plan-v1_0.json"
LEGACY_AGREGADO = DIR / "agregado-v1_3-resultado.json"
LEGACY_EXTRAIDO_V12 = DIR / "L-extraido-v1_2.tsv"

VARIANTE_NOMBRE = {"L-solo": "L_solo", "L+corpus": "L_corpus"}


def _mediana_v12_por_celda_variante() -> dict:
    """Reconstruye la mediana sobre el conjunto EXTRAIBLE de v1.2, por
    (celda, variante). `NO-RECONSTRUIBLE` si no hay ninguna fila EXTRAIBLE."""
    import statistics
    filas = defaultdict(list)
    with LEGACY_EXTRAIDO_V12.open(encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f, delimiter="\t"):
            if fila["estado"] != "EXTRAIBLE":
                continue
            clave = (fila["id_celda"], fila["variante"])
            filas[clave].append(float(fila["valor"]))
    out = {}
    for clave, valores in filas.items():
        out[clave] = {"mediana_v12": statistics.median(valores), "n_v12": len(valores)}
    return out


def calcular() -> dict:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    posiciones = plan["posiciones"]
    if len(posiciones) != 224:
        raise RuntimeError(f"plan distinto de 224: {len(posiciones)}")

    por_grupo = defaultdict(list)
    for pos in posiciones:
        por_grupo[(pos["id_celda"], pos["variante"])].append(pos)

    errores_identidad = []
    tabla = {}
    for (celda, variante), posgrupo in sorted(por_grupo.items()):
        ev = []
        for pos in sorted(posgrupo, key=lambda p: p["replica"]):
            ruta = ROOT / pos["ruta"]
            if not ruta.exists():
                ev.append(("PENDIENTE", None))
                continue
            captura = json.loads(ruta.read_text(encoding="utf-8"))
            if captura.get("identidad") != pos["identidad"]:
                errores_identidad.append(str(ruta.relative_to(ROOT)))
                ev.append(("ERROR_IDENTIDAD", None))
                continue
            estado, valor, _ = extraer(captura.get("texto_crudo"), captura.get("estado_captura", "OK"))
            ev.append((estado, valor))
        r = agregar_celda(ev, n_programadas=len(posgrupo))
        tabla[f"{celda}:{variante}"] = {
            "id_celda": celda, "variante": variante,
            "n_programadas": r.n_programadas, "n_ejecutadas": r.n_ejecutadas,
            "n_validas": r.n_validas, "n_abstenciones": r.n_abstenciones,
            "n_malformadas": r.n_malformadas, "n_errores_tecnicos": r.n_errores_tecnicos,
            "mediana": r.mediana, "dispersion_mad": r.dispersion_mad,
            "ic_lo": r.ic_lo, "ic_hi": r.ic_hi,
        }

    n_celdas_con_mediana = sum(1 for v in tabla.values() if v["mediana"] is not None)
    n_celdas_sin_mediana = sum(1 for v in tabla.values() if v["mediana"] is None)

    # P4: diferencias contra GEN1, descompuestas.
    legacy = json.loads(LEGACY_AGREGADO.read_text(encoding="utf-8"))["celdas"]
    v12 = _mediana_v12_por_celda_variante()
    diferencias = {}
    for (celda, variante), grp in sorted(por_grupo.items()):
        nombre_legacy = VARIANTE_NOMBRE[variante]
        gen1_media = legacy.get(celda, {}).get(nombre_legacy)
        clave_v12 = (celda, variante)
        rec = v12.get(clave_v12)
        gen2_mediana_224 = tabla[f"{celda}:{variante}"]["mediana"]
        fila = {
            "id_celda": celda, "variante": variante,
            "gen1_media": gen1_media,
            "reconstruible_v12": rec is not None,
        }
        if rec is not None:
            fila["mediana_v12"] = rec["mediana_v12"]
            fila["n_replicas_v12"] = rec["n_v12"]
            if gen1_media is not None:
                fila["delta_agregador_pp"] = (rec["mediana_v12"] - gen1_media) * 100
        else:
            fila["mediana_v12"] = None
            fila["delta_agregador_pp"] = "NO-RECONSTRUIBLE"
        fila["mediana_gen2_224"] = gen2_mediana_224
        if rec is not None and gen2_mediana_224 is not None:
            fila["delta_conjunto_pp"] = (gen2_mediana_224 - rec["mediana_v12"]) * 100
        else:
            fila["delta_conjunto_pp"] = "NO-RECONSTRUIBLE"
        if gen1_media is not None and gen2_mediana_224 is not None:
            fila["delta_total_gen1_vs_gen2_pp"] = (gen2_mediana_224 - gen1_media) * 100
        else:
            fila["delta_total_gen1_vs_gen2_pp"] = None
        diferencias[f"{celda}:{variante}"] = fila

    return {
        "acto": "GEN2-L-DESDE-CAPTURAS-1",
        "n_posiciones": len(posiciones),
        "n_slots": len(tabla),
        "n_celdas_con_mediana": n_celdas_con_mediana,
        "n_celdas_sin_mediana": n_celdas_sin_mediana,
        "errores_identidad": errores_identidad,
        "tabla_l_por_celda_variante": tabla,
        "diferencias_vs_gen1": diferencias,
    }


def main() -> int:
    resultado = calcular()
    salida = DIR / "L-desde-capturas-resultado-v1_0.json"
    salida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    resumen = {k: resultado[k] for k in
               ("n_posiciones", "n_slots", "n_celdas_con_mediana", "n_celdas_sin_mediana", "errores_identidad")}
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
