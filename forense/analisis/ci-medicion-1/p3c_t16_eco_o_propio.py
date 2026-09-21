#!/usr/bin/env python3
"""P3 (corrección, ADENDA-1 A3) · ACTO GEN2-TUBERIA-CI-MEDICION-1.

TUBERÍA midió: en las 66 corridas donde T16 T-SUITE-SELF-CHECK falla,
¿falla ALGÚN OTRO test fuera de los dos heredados de baseline (T06/T08) en
esa MISMA ejecución de check.py (misma job_id)? Si sí en las 66, T16 no
atrapó nada por sí mismo -- falló por ECO (la cuenta de FAIL que T16
compara cambió porque otro test falló, no porque una afirmación vigente de
canon/ contradijera la corrida real).
"""
import csv
from collections import defaultdict

BASELINE_HEREDADOS = {"T06 consistencia numérica", "T08 mapa de evidencia por report"}

por_ejecucion = defaultdict(set)  # (run_id, job_id) -> {tests que fallaron}
with open("fallos-tests-runner.tsv") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        key = (row["run_id"], row["job_id"])
        por_ejecucion[key].add(row["test"])

ejecuciones_con_t16_fail = {k: v for k, v in por_ejecucion.items() if "T16 T-SUITE-SELF-CHECK" in v}

eco = 0       # T16 fallo Y algo mas (fuera de baseline) fallo tambien
propio = 0    # T16 fallo y NADA MAS (fuera de baseline) fallo
detalle_propio = []
for key, tests in ejecuciones_con_t16_fail.items():
    otros = tests - BASELINE_HEREDADOS - {"T16 T-SUITE-SELF-CHECK"}
    if otros:
        eco += 1
    else:
        propio += 1
        detalle_propio.append(key)

print(f"Corridas con T16 en FAIL: {len(ejecuciones_con_t16_fail)}")
print(f"  con >=1 fallo fuera de baseline en la MISMA ejecucion (ECO): {eco}")
print(f"  sin ningun otro fallo fuera de baseline (FALLO PROPIO): {propio}")
if detalle_propio:
    print("  detalle de las de fallo propio:", detalle_propio)

with open("t16-eco-o-propio.tsv", "w") as f:
    f.write("run_id\tjob_id\tclase\ttests_que_fallaron_junto_con_t16\n")
    for key, tests in sorted(ejecuciones_con_t16_fail.items()):
        otros = tests - BASELINE_HEREDADOS - {"T16 T-SUITE-SELF-CHECK"}
        clase = "ECO" if otros else "PROPIO"
        f.write(f"{key[0]}\t{key[1]}\t{clase}\t{'; '.join(sorted(tests))}\n")
print("Escrito t16-eco-o-propio.tsv")
