#!/usr/bin/env python3
"""P5 · ACTO GEN2-TUBERIA-CI-MEDICION-1. Ensambla el barrido de pasos de
verify.yml: junta nacimiento (comentario del propio workflow), costo en el
runner (ERA3 -- la arquitectura vigente hoy, ver p2b) y evidencia de fallo
(P2, jobs-pasos.tsv), y aplica recomendación (juicio del ejecutor).
"""
import csv

nacimiento = {(r["job"], r["paso"]): r for r in csv.DictReader(open("nacimiento-verify-steps.tsv"), delimiter="\t")}
evidencia = {(r["job"], r["paso"]): r for r in csv.DictReader(open("evidencia-pasos-verify.tsv"), delimiter="\t")}
costo_era3 = {}
for r in csv.DictReader(open("duracion-por-paso-por-era.tsv"), delimiter="\t"):
    if r["era"].startswith("ERA3") or r["era"].startswith("ERA4"):
        key = (r["job"], r["paso"])
        # ERA4 tiene sólo 5 muestras; preferimos ERA3 (97) si existe para ambos
        if key not in costo_era3 or r["era"].startswith("ERA3"):
            costo_era3[key] = r

INFRA = {"Checkout sin marketplace (repo público — cero descargas de action)",
         "Checkout con la base (clon propio — D-23, no se toca el de otro job)",
         "Intérprete del runner (crudo, para que quede en el log)",
         "Instala dependencias (requirements.txt — explícito, nunca lo que traiga el runner)",
         "Set up job", "Complete job"}

REC = {}  # (job,paso) -> (rec, justificacion)

REC[("adicionales", "marcador por segmento — tabla derivada y guardias (bloqueante)")] = (
    "ABARATAR",
    "Paso más caro de todo verify.yml hoy (mediana 136s, p90 149s -- consistente con los 134s que "
    "midió PR #901 en el primer runner: no se ha movido). Corre dos archivos en serie dentro del "
    "job `adicionales` (que ya suma otros ~20 pasos); `adicionales` es hoy el job que fija la ruta "
    "crítica (mediana 159-220s, por encima de `suite`). Aislarlo en un job propio, en paralelo a "
    "`suite` y al resto de `adicionales`, no reduce su propio costo pero sí la ruta crítica de la "
    "corrida: hoy max(suite~120s, adicionales~159-220s) domina; con el marcador aislado sería "
    "max(suite~120s, marcador~136-149s, resto-adicionales~20-30s) -- ahorro estimado 20-70s por "
    "corrida (más en p90) sin tocar ninguna aserción. Mismo patrón que PR #901 ya aplicó una vez "
    "para separar `suite` de `adicionales`.",
)
REC[("suite", "Suite de verificación (modo línea base — verde = no empeoraste)")] = (
    "MANTENER",
    "Es tests/check.py -- ver el desglose test por test en barrido-check-tests.tsv (53 filas). "
    "A nivel de paso: mediana 109-121s, dominado por T16 (61s mediana runner) y T32 (39s).",
)
REC[("check", "Suite de verificación (modo línea base — verde = no empeoraste)")] = (
    "HISTORICO",
    "Mismo paso que arriba, pero de la arquitectura ERA1 (un solo job `check` monolítico, hasta el "
    "20/sep ~02:00, sustituida por PR #901). Ya no existe en el verify.yml vigente.",
)
REC[("guardias", "Guardias huérfanas — censo + invocador correcto por archivo (bloqueante)")] = (
    "MANTENER",
    "13 fallos en CI (12 en rama de PR): atrapa activamente tests/test_*.py que nacen huérfanos "
    "(ni en verify.yml ni en el censo). Nacido 20/sep (ACTO GEN2-CI-GUARDIAS-VIVAS-1) por el mismo "
    "defecto que motiva este acto: 97 de 122 test_*.py no corrían en CI y nadie lo notaba.",
)
REC[("adicionales", "Checkout sin marketplace (repo público — cero descargas de action)")] = (
    "MANTENER",
    "1 fallo en CI (sin evidencia de en qué rama). Infraestructura común a los 4 jobs con checkout "
    "propio; el diseño de checkout independiente por job es deliberado (D-23, evita que un job "
    "mute el clon de otro) y cada checkout es barato (mediana 5-6s).",
)
REC[("adicionales", "métrica rectora — celdas_validadas en la primera línea del tablero (bloqueante)")] = (
    "MANTENER",
    "1 fallo en CI. Recién nacido (ACTO GEN2-SENAL-1, 21/sep) -- sólo 53-64 corridas con dato, "
    "demasiado joven para juzgar caducidad.",
)
REC[("adicionales", "Inyección temporal exclusiva de la prueba de compuerta")] = (
    "HISTORICO",
    "3 corridas, 1 fallo, todas el 20/sep ~02:00: paso transitorio (probablemente la propia "
    "validación del cambio de compuerta de PR #901 in vivo). No existe en el verify.yml vigente; "
    "no requiere recomendación.",
)
REC[("suite", "Inyección temporal exclusiva de la prueba de compuerta")] = REC[
    ("adicionales", "Inyección temporal exclusiva de la prueba de compuerta")
]
REC[("check", "Todos los grupos requeridos terminaron correctamente")] = (
    "MANTENER",
    "Compuerta final (`always()`), 1 paso, <1s de costo propio. 51 fallos son el reflejo mecánico "
    "de que ALGÚN job requerido falló (no un defecto propio del paso).",
)
for j in ("suite", "adicionales", "guardias", "preflight-calc"):
    for p in ("Set up job", "Complete job", "Checkout con la base (clon propio — D-23, no se toca el de otro job)",
              "Intérprete del runner (crudo, para que quede en el log)",
              "Instala dependencias (requirements.txt — explícito, nunca lo que traiga el runner)"):
        REC.setdefault((j, p), (
            "MANTENER",
            "Infraestructura del job (checkout/intérprete/dependencias), barata (mediana ≤6s) y "
            "sin evidencia de fallo propio en la ventana medida.",
        ))

filas = []
for key, nac in nacimiento.items():
    if nac["paso"] == "Todos los grupos requeridos terminaron correctamente" and nac["job"] != "check":
        continue
    ev = evidencia.get(key, {})
    costo = costo_era3.get(key, {})
    rec, just = REC.get(key, (
        "MANTENER",
        f"Cita de nacimiento: {nac['citas'] or 's/cita explícita'}. "
        f"{ev.get('n_fail','0')} fallos en CI en la ventana medida"
        + (f" ({ev.get('fail_en_pr','0')} en rama de PR)." if ev.get("n_fail", "0") != "0" else ". Sin evidencia de fallo, costo bajo."),
    ))
    filas.append({
        "job": key[0], "paso": key[1], "linea_verify_yml": nac["linea"],
        "nacimiento_citas": nac["citas"],
        "costo_mediana_s": costo.get("mediana_s", ""), "costo_p90_s": costo.get("p90_s", ""),
        "n_corridas_costo": costo.get("n", ""),
        "n_fallos_ci": ev.get("n_fail", "0"), "ultimo_fallo": ev.get("ultimo_fail", ""),
        "fallos_en_pr": ev.get("fail_en_pr", "0"),
        "recomendacion": rec, "justificacion": just,
    })

with open("barrido-verify-steps.tsv", "w", encoding="utf-8") as f:
    cols = ["job", "paso", "linea_verify_yml", "nacimiento_citas", "costo_mediana_s", "costo_p90_s",
            "n_corridas_costo", "n_fallos_ci", "ultimo_fallo", "fallos_en_pr", "recomendacion", "justificacion"]
    f.write("\t".join(cols) + "\n")
    for r in filas:
        f.write("\t".join(str(r[c]) for c in cols) + "\n")

print(f"Escrito barrido-verify-steps.tsv ({len(filas)} filas)")
