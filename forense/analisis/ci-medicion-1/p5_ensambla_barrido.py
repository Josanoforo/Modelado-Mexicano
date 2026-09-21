#!/usr/bin/env python3
"""P5 · ACTO GEN2-TUBERIA-CI-MEDICION-1. Ensambla la lista del barrido:
una fila por test de tests/check.py, por paso de verify.yml, por paso de
la cascada de /acto, y por archivo de test no cableado. Junta los insumos
mecánicos (P1-P4 de este acto) y aplica REC (recomendación + justificación),
que es juicio del ejecutor, no derivación automática -- declarado así.
"""
import csv

def leer_tsv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))

nacimiento_check = {r["label"]: r for r in leer_tsv("nacimiento-check-tests.tsv")}
tiempos_local = {r[0]: r[1] for r in csv.reader(open("tiempos-locales-run1.tsv"), delimiter="\t")}
tiempos_runner = {r["test"]: r for r in leer_tsv("tiempos-tests-runner-agg.tsv")}
fallos_runner = {r["test"]: r for r in leer_tsv("fallos-tests-runner-agg.tsv")}

# ---------------------------------------------------------------------
# Recomendaciones para los 53 tests de check.py -- juicio del ejecutor.
# Categoría CONTENIDO (§3 instrucciones): fuera de alcance por mandato
# explícito del encargo ("Las reglas de contenido quedan fuera").
CONTENIDO_S3 = {
    "T06 consistencia numérica", "T07 vocabulario de tiers",
    "T08 mapa de evidencia por report", "T09 marco (c) usado como causa",
    "T10 diáspora (b) sin marcar", "T11 afirmaciones de estado absolutas",
}

REC_CHECK = {}  # label -> (rec, justificacion, costo_lector_si_elimina)

for label in nacimiento_check:
    if label in CONTENIDO_S3:
        REC_CHECK[label] = (
            "FUERA-DE-ALCANCE",
            "Regla de contenido (§3 instrucciones-proyecto): protege la calidad de los reports "
            "(marcos importados como causa, diáspora sin marcar, vocabulario de tiers, mapa de "
            "evidencia, consistencia numérica de Gini/confianza). El encargo excluye §3 de esta "
            "lista explícitamente.",
            "",
        )

REC_CHECK["T16 T-SUITE-SELF-CHECK"] = (
    "ELIMINAR",
    "Decisión ya tomada por dirección en el mandato de este acto (\"T16 se elimina -- este acto "
    "aporta la evidencia, no lo elimina\"). Evidencia medida aquí: relanza el núcleo completo en "
    "un subproceso (mediana local 46-61s, p90 runner 87.7s; es el paso más caro de toda la "
    "cascada); hoy pasa limpio (0 afirmaciones FAIL/WARN vigentes contradictorias en los 11 "
    "archivos de canon/, confirmado por la corrida local VERDE de este acto). SÍ atrapó algo real "
    "66 veces en el runner entre el 18 y el 20/sep (55 en rama de PR) -- no es un test que nunca "
    "sirvió, es uno cuyo costo (relanzar TODO el núcleo por cada corrida, multiplicado por las 2-3 "
    "invocaciones de check.py de la cascada de /acto) superó lo que protege una vez que las "
    "afirmaciones vigentes de FAIL/WARN en canon/ se volvieron raras. Costo a un lector si se "
    "elimina: pierde la única guardia mecánica de que una nota o un ADR no mienta sobre el estado "
    "de la suite; sustituir por una verificación más barata (comparar sólo las líneas con "
    "`_CAMBIO_FECHADO`/`MARCA_HISTORICA` contra el `baseline.json` ya escrito, sin relanzar nada) "
    "es la vía de abaratamiento si dirección prefiere abaratar en vez de eliminar del todo.",
    "pierde la única guardia mecánica de notas/ADR que mienten sobre el estado de la suite",
)

REC_CHECK["T32 T-CORRIDA0"] = (
    "MANTENER",
    "Segundo test más caro del núcleo (mediana runner 39.4s, p90 65.7s; local ~20-41s). Protege "
    "la tubería corrida0/reproducibilidad GEN2 (ACTO GEN2-E3 · AUTOMATIZA-GEN2-1) -- no tiene "
    "evidencia de fallo en CI en la ventana medida, pero es el ejecutor de `tools/corrida0.py`, "
    "que resuelve toda la cadena SPEC->CALC->RESULT->USO de la que depende E.2/E.3. Candidato a "
    "ABREVIAR la investigación de por qué tarda tanto (¿corre subprocesos reales, IO de disco "
    "repetida?) en un acto de velocidad sucesor, pero no a eliminar ni abaratar a ciegas aquí.",
    "",
)

REC_CHECK["T32-quater T-PINES-MESA"] = (
    "MANTENER",
    "Tercer más caro (mediana runner 28.4s), pero recién nacido (ACTO GEN2-RELEVO-TANDA-3, "
    "20/sep) -- sólo 21 corridas con dato, cero fallos capturados todavía. Demasiado joven para "
    "juzgar caducidad; se revisa en el próximo barrido (regla de caducidad a 3 meses, §9).",
    "",
)

REC_CHECK["T35 T-REPRO"] = (
    "MANTENER",
    "Regla explícita del encargo: T-REPRO se puede abaratar, nunca eliminar. Ya corre en un "
    "worker `spawn` separado desde PR #901 (paralelo al resto del núcleo) -- el abaratamiento ya "
    "se hizo una vez. Mediana runner baja (7.8s) pero p90 alto (25.2s, variable entre corridas): "
    "sin evidencia de qué corridas son las lentas no hay una acción concreta que recomendar más "
    "allá de mantener.",
    "",
)

# El resto de los tests estructurales (T01-T47 salvo los de arriba): MANTENER
# por defecto -- baratos (mediana local <2s casi todos) y sin evidencia de que
# lo que protegen dejó de existir. Se anota individualmente sólo cuando el
# historial de fallos aporta algo que decir.
DEFECTOS_NOTABLES = {
    "T02 duplicados nombre/contenido": "51 fallos en CI en la ventana medida (40 en rama de PR): "
        "atrapa activamente duplicados de nombre/contenido antes de fusionar. Mantener sin duda.",
    "T22 T-FIRMAS": "10 fallos en CI (8 en PR): protege el tablero de firmas pendientes (A.12), "
        "atrapa activamente.",
    "T27 T-INFRA": "6 fallos en CI, los 6 en rama de PR: protege data/INFRAESTRUCTURA-v1_0.md.",
    "T30 T-YAMEDIDO": "4 fallos en CI, los 4 en PR: protege contra reclasificar una regla ya medida "
        "(ADR-340, defecto real repetido dos veces la misma semana).",
    "T25 T-ROTULOS": "4 fallos en CI, los 4 en PR (uno de ellos, medido por T-YAMEDIDO, obligó a la "
        "corrección de este propio encargo -- ver §hallazgos).",
    "T26-bis T-TSV-CRUDO-ROUND-TRIP": "4 fallos en CI, los 4 en PR: protege el round-trip TSV crudo "
        "de la cola de adquisición.",
    "T19a cabecera cruzada estado→modelo": "3 fallos en CI, los 3 en PR.",
    "T34 T-NO-CORRIDO": "1 fallo en CI (A.14 -- protege que NO-CORRIDO no se pierda).",
    "T15 T-ADR-COUNT": "1 fallo en CI: protege el contador de ADR contra desincronía.",
    "T32-bis T-PISOS-REJILLA": "1 fallo en CI.",
}

with open("barrido-check-tests.tsv", "w", encoding="utf-8") as f:
    f.write(
        "label\tlinea\tnacimiento_citas\tcosto_local_s\tcosto_runner_mediana_s\tcosto_runner_p90_s\t"
        "n_fallos_ci\tultimo_fallo_run_id\tfallos_en_pr\trecomendacion\tjustificacion\n"
    )
    for label, row in nacimiento_check.items():
        costo_local = tiempos_local.get(label, "")
        tr = tiempos_runner.get(label, {})
        fr = fallos_runner.get(label, {})
        rec, just, _ = REC_CHECK.get(label, ("MANTENER", "Barato y sin evidencia de que lo que protege dejó de existir.", ""))
        if label in DEFECTOS_NOTABLES:
            just = DEFECTOS_NOTABLES[label] + (" " + just if just and "Barato" not in just else "")
        f.write(
            f"{label}\t{row['linea']}\t{row['citas']}\t{costo_local}\t"
            f"{tr.get('mediana_s','')}\t{tr.get('p90_s','')}\t"
            f"{fr.get('n_fallos','0')}\t{fr.get('ultimo_run_id','')}\t{fr.get('fallos_en_pr','0')}\t"
            f"{rec}\t{just}\n"
        )

print(f"Escrito barrido-check-tests.tsv ({len(nacimiento_check)} filas)")
