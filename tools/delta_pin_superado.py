#!/usr/bin/env python3
"""Delta del pin de un `resultado_id` íntegramente superado — por comando.

ACTO MOTOR-LINAJE-1 · 21/sep/2026 · §5-P2 de
`forense/encargos/2026-09-21-motor-linaje-1-nc0401.md`.

Firma de mesa (21/sep/2026): «el pin del consumidor se actualiza en el mismo
acto CON delta calculado por script». Este es ese script. No escribe ningún
pin: deriva el universo, lo cuenta y reporta. Decidir es de mesa.

Lee SOLO las vistas derivadas de 17 (`data/corrida0/resultados.tsv` y
`usos.tsv`). No abre microdato, no toca `milpa/tramite.yaml`, no escribe nada.

Vocabulario A.4 en la columna `veredicto`:
  SIN-PIN            — ningún uso activo pin-ea este id; no hay delta que
                       calcular y no hay nada que actualizar.
  SUCESOR-NO-ENCONTRADO-EN-LA-VISTA — el `estado` nombra un sucesor que no
                       es un `resultado_id` con fila vigente (suele ser un
                       id de corrida/spec, no de resultado). No se resuelve
                       ni se adivina.
  DENTRO-DE-TOLERANCIA / FUERA-DE-TOLERANCIA — hay pin y hay sucesor
                       resoluble: el delta se compara contra la tolerancia
                       declarada del tipo. FUERA-DE-TOLERANCIA no se
                       escribe: va a mesa por los bins de la ADENDA 15/sep.
  NO-COMPARABLE      — alguno de los dos valores no es numérico.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import math
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RUTA_RESULTADOS = RAIZ / "data" / "corrida0" / "resultados.tsv"
RUTA_USOS = RAIZ / "data" / "corrida0" / "usos.tsv"


def _leer(ruta: Path) -> list[dict[str, str]]:
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    if lineas and lineas[0].startswith("# DERIVADO"):
        lineas = lineas[1:]
    return list(csv.DictReader(lineas, delimiter="\t"))


def _numero(valor: str):
    try:
        n = float(str(valor).strip())
    except (TypeError, ValueError):
        return None
    return n if math.isfinite(n) else None


def _sucesor(estado: str) -> str:
    texto = str(estado).strip()
    for flecha in ("→", "->"):
        if flecha in texto:
            resto = texto.split(flecha, 1)[1].strip()
            if resto:
                return resto
    return "NO-DECLARADO-EN-EL-CAMPO-ESTADO"


def _tolerancia_abs(crudo: str):
    try:
        return float(json.loads(crudo).get("abs"))
    except Exception:
        return None


def analiza(ruta_resultados=RUTA_RESULTADOS, ruta_usos=RUTA_USOS):
    filas = _leer(ruta_resultados)
    por_id = collections.defaultdict(list)
    for f in filas:
        por_id[f["resultado_id"]].append(f)

    vigentes = {
        rid: [f for f in fs
              if not str(f.get("estado", "")).startswith("SUPERADO")]
        for rid, fs in por_id.items()
    }
    superados = {rid: fs for rid, fs in por_id.items() if not vigentes[rid]}

    pines = collections.defaultdict(list)
    for u in _leer(ruta_usos):
        if u.get("activo") != "SI":
            continue
        for col in ("resultado_id", "corrida0_resultado_id"):
            if u.get(col):
                pines[u[col]].append(u["consumidor"])

    reporte = []
    for rid in sorted(superados):
        fila = superados[rid][0]
        suc = _sucesor(fila.get("estado", ""))
        consumidores = sorted(set(pines.get(rid, [])))
        viejo = _numero(fila.get("valor", ""))
        tol = _tolerancia_abs(fila.get("tolerancia", ""))

        fila_suc = (vigentes.get(suc) or [None])[0]
        nuevo = _numero(fila_suc.get("valor", "")) if fila_suc else None

        if not consumidores:
            veredicto, delta = "SIN-PIN", None
        elif fila_suc is None:
            veredicto, delta = "SUCESOR-NO-ENCONTRADO-EN-LA-VISTA", None
        elif viejo is None or nuevo is None:
            veredicto, delta = "NO-COMPARABLE", None
        else:
            delta = nuevo - viejo
            veredicto = ("DENTRO-DE-TOLERANCIA"
                         if tol is not None and abs(delta) <= tol
                         else "FUERA-DE-TOLERANCIA")
        reporte.append({
            "resultado_id": rid, "sucesor_declarado": suc,
            "consumidores_activos": consumidores,
            "valor_superado": viejo, "valor_sucesor": nuevo,
            "delta": delta, "tolerancia_abs": tol, "veredicto": veredicto,
        })
    return {
        "universo_ids_en_la_vista": len(por_id),
        "ids_integramente_superados": len(superados),
        "archivos_examinados": 2,
        "filas": reporte,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--id", action="append", default=None,
                    help="limita el reporte a estos resultado_id")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    r = analiza()
    if a.id:
        r["filas"] = [f for f in r["filas"] if f["resultado_id"] in set(a.id)]

    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    print(f"DELTA-PIN-SUPERADO · universo={r['universo_ids_en_la_vista']} ids "
          f"· integramente_superados={r['ids_integramente_superados']} "
          f"· archivos_examinados={r['archivos_examinados']} (A.13)")
    cuenta = collections.Counter(f["veredicto"] for f in r["filas"])
    for v, n in sorted(cuenta.items()):
        print(f"  {v}: {n}")
    for f in r["filas"]:
        if f["veredicto"] != "SIN-PIN" or a.id:
            print(f"  · {f['resultado_id']} → sucesor={f['sucesor_declarado']}"
                  f" · pines={f['consumidores_activos'] or 'NINGUNO'}"
                  f" · delta={f['delta']} · {f['veredicto']}")
    hay_pin = [f for f in r["filas"] if f["consumidores_activos"]]
    if not hay_pin:
        print("  VEREDICTO: ningun uso ACTIVO pin-ea un id integramente "
              "superado. No hay pin que actualizar ni delta que firmar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
