#!/usr/bin/env python3
"""P3 · ACTO GEN2-TUBERIA-CI-MEDICION-1. Descarga el log del job que corrió
"Suite de verificación (modo línea base...)" (tests/check.py) en cada
corrida completa (success/failure), y extrae:
  - duración de cada test T-nn en el runner (líneas `[tiempo]`, sólo el
    nivel externo -- se descartan las `[T16/hijo]`, que son el rerun
    interno de T16 sobre sí mismo).
  - fallos por test (líneas `[FAIL]` con su etiqueta).
No se guarda el log completo (volumen); se guarda sólo lo extraído, más
un recorte de contexto alrededor de cada FAIL para evidencia.

Universo: TODOS los jobs con ese paso y conclusion en (success, failure)
-- no es muestra, es el universo completo de corridas completas
(justificación: volumen manejable, ~320 descargas, dentro del rate limit
de 5000/h de un token autenticado). Declarado en P3 del informe.
"""
import json
import re
import subprocess
import sys
import time

REPO = "Josanoforo/Modelado-Mexicano"
PASO_OBJETIVO = "Suite de verificación (modo línea base — verde = no empeoraste)"


def gh_api_logs(job_id):
    for intento in range(3):
        out = subprocess.run(
            ["gh", "api", f"repos/{REPO}/actions/jobs/{job_id}/logs"],
            capture_output=True, text=True,
        )
        if out.returncode == 0:
            return out.stdout
        sys.stderr.write(f"reintento {intento+1} job {job_id}: {out.stderr[:200]}\n")
        time.sleep(2)
    return None


def main():
    with open("jobs.json") as f:
        jobs_por_run = json.load(f)
    with open("runs.json") as f:
        runs = {str(r["id"]): r for r in json.load(f)}

    objetivo = []
    for rid, jobs in jobs_por_run.items():
        for j in jobs:
            pasos = [s["name"] for s in (j.get("steps") or [])]
            if PASO_OBJETIVO in pasos and j.get("conclusion") in ("success", "failure"):
                objetivo.append((rid, j["id"], j["name"], j["conclusion"]))

    sys.stderr.write(f"UNIVERSO: {len(objetivo)} jobs con el paso de la suite, conclusion completa\n")

    tiempos_rows = []  # run_id, job_id, job_name, evento, rama, conclusion_run, test, dur_s
    fallos_rows = []   # run_id, job_id, job_name, evento, rama, conclusion_run, test, contexto
    no_leidos = []

    for i, (rid, job_id, job_name, job_concl) in enumerate(objetivo):
        r = runs.get(rid, {})
        evento = r.get("event", "")
        rama = r.get("head_branch", "")
        run_concl = r.get("conclusion", "")
        log = gh_api_logs(job_id)
        if log is None:
            no_leidos.append((rid, job_id))
            continue
        lines = log.splitlines()
        for k, line in enumerate(lines):
            # las lineas de log de Actions traen un timestamp ISO al inicio; lo
            # despojamos para matchear el patron fijo de check.py
            contenido = re.sub(r"^\S+Z\s*", "", line)
            if "[T16/hijo]" in contenido:
                continue
            m = re.search(r"\[tiempo\]\s*(.+?):\s*([0-9.]+)\s*s\s*$", contenido)
            if m:
                tiempos_rows.append(
                    (rid, job_id, job_name, evento, rama, run_concl, m.group(1), m.group(2))
                )
                continue
            m2 = re.search(r"\[FAIL\]\s*(\S.*?)(?:\s*\(\d+ fail.*\))?\s*$", contenido)
            if m2:
                contexto = " | ".join(
                    re.sub(r"^\S+Z\s*", "", x).strip() for x in lines[k : k + 2]
                )
                fallos_rows.append(
                    (rid, job_id, job_name, evento, rama, run_concl, m2.group(1).strip(), contexto[:300])
                )
        if (i + 1) % 25 == 0:
            sys.stderr.write(f"{i+1}/{len(objetivo)} logs procesados\n")

    with open("tiempos-tests-runner.tsv", "w") as f:
        f.write("run_id\tjob_id\tjob_name\tevento\trama\tconclusion_run\ttest\tduracion_s\n")
        for row in tiempos_rows:
            f.write("\t".join(str(x) for x in row) + "\n")

    with open("fallos-tests-runner.tsv", "w") as f:
        f.write("run_id\tjob_id\tjob_name\tevento\trama\tconclusion_run\ttest\tcontexto\n")
        for row in fallos_rows:
            f.write("\t".join(str(x) for x in row) + "\n")

    with open("p3-no-leidos.tsv", "w") as f:
        f.write("run_id\tjob_id\n")
        for rid, jid in no_leidos:
            f.write(f"{rid}\t{jid}\n")

    sys.stderr.write(
        f"TOTAL: {len(objetivo)} examinados, {len(objetivo)-len(no_leidos)} leidos, "
        f"{len(no_leidos)} NO-ACCESIBLE; {len(tiempos_rows)} filas de tiempo, "
        f"{len(fallos_rows)} filas de fallo\n"
    )


if __name__ == "__main__":
    main()
