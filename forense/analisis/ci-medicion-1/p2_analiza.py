#!/usr/bin/env python3
"""P2 (análisis) · ACTO GEN2-TUBERIA-CI-MEDICION-1. A partir de runs.json y
jobs.json (P1/P2 recolección): duración total por corrida, espera inicial
(creación -> primer job en marcha) y job de ruta crítica. Script de un
solo uso.

Nota (A.13): la primera versión de este script también agregaba duración
por (job, paso) agrupando SOLO por nombre de job -- mezclaba el job
monolítico `check` de ERA1 (hacía todo, hasta el 20/sep ~02:00) con el job
`check` de compuerta rápida de hoy, mismo nombre, funciones opuestas. Esa
parte se retiró de aquí y se rehizo correctamente, segmentada por firma de
job, en `p2b_analiza_por_era.py` -- lo que sigue abajo (duración por
corrida) no tenía ese defecto, así que se conserva.
"""
import json
import statistics as st
from datetime import datetime, timezone


def parse_ts(s):
    if not s:
        return None
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def mediana_p90(vals):
    if not vals:
        return None, None
    vals = sorted(vals)
    med = st.median(vals)
    idx = min(len(vals) - 1, int(round(0.9 * (len(vals) - 1))))
    return round(med, 2), round(vals[idx], 2)


def main():
    with open("runs.json") as f:
        runs = {str(r["id"]): r for r in json.load(f)}
    with open("jobs.json") as f:
        jobs_por_run = json.load(f)

    filas = []
    corrida_total = []
    espera_inicial_vals = []
    for rid, r in runs.items():
        jobs = jobs_por_run.get(rid, [])
        creado = parse_ts(r.get("created_at"))
        inicios = [parse_ts(j.get("started_at")) for j in jobs if j.get("started_at")]
        fines = [parse_ts(j.get("completed_at")) for j in jobs if j.get("completed_at")]
        primer_job = min(inicios) if inicios else None
        ultimo_fin = max(fines) if fines else None
        espera_inicial = (primer_job - creado).total_seconds() if (creado and primer_job) else None
        duracion_total = (ultimo_fin - creado).total_seconds() if (creado and ultimo_fin) else None
        ruta_critica, ruta_dur = "", 0.0
        for j in jobs:
            ji, jf = parse_ts(j.get("started_at")), parse_ts(j.get("completed_at"))
            if ji and jf:
                d = (jf - ji).total_seconds()
                if d > ruta_dur:
                    ruta_dur, ruta_critica = d, j["name"]
        filas.append(
            {
                "run_id": rid,
                "evento": r.get("event", ""),
                "conclusion": r.get("conclusion") or "",
                "creado": r.get("created_at", ""),
                "espera_inicial_s": round(espera_inicial, 1) if espera_inicial is not None else "",
                "duracion_total_s": round(duracion_total, 1) if duracion_total is not None else "",
                "ruta_critica_job": ruta_critica,
                "ruta_critica_s": round(ruta_dur, 1) if ruta_dur else "",
            }
        )
        if duracion_total is not None and r.get("conclusion") in ("success", "failure"):
            corrida_total.append(duracion_total)
        if espera_inicial is not None:
            espera_inicial_vals.append(espera_inicial)

    with open("duracion-por-corrida.tsv", "w") as f:
        f.write("run_id\tevento\tconclusion\tcreado\tespera_inicial_s\tduracion_total_s\truta_critica_job\truta_critica_s\n")
        for r in filas:
            f.write(
                f"{r['run_id']}\t{r['evento']}\t{r['conclusion']}\t{r['creado']}\t"
                f"{r['espera_inicial_s']}\t{r['duracion_total_s']}\t{r['ruta_critica_job']}\t{r['ruta_critica_s']}\n"
            )

    med_tot, p90_tot = mediana_p90(corrida_total)
    med_esp, p90_esp = mediana_p90(espera_inicial_vals)
    print(f"corridas completas (success/failure) con duracion: {len(corrida_total)}")
    print(f"duracion total de corrida: mediana={med_tot}s p90={p90_tot}s")
    print(f"espera inicial (creacion->primer job): mediana={med_esp}s p90={p90_esp}s (n={len(espera_inicial_vals)})")


if __name__ == "__main__":
    main()
