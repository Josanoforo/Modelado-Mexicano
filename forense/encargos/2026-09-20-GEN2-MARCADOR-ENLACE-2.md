# ENCARGO · ACTO GEN2-MARCADOR-ENLACE-2 · EL MARCADOR NO SE HA ENTERADO DE TRES MEDICIONES YA SELLADAS: PISOS DE FORMALIDAD, IC DE ENIF 2024 E IC DE ENVIPE 2025

> Archivado verbatim por A.3 / 0-bis. Texto tal como mesa lo entregó a la sesión.
> CONSUMIDO al pie.

ENTORNO: NUBE — NO caja. Todo insumo es un RESULT sellado.

CABECERA (D-12) · SHA de redacción 8b7b0562; re-deriva al abrir · una sola sesión, rama propia · COMPUERTA: #911, #915 y #916 en main (cumplida) · MODELO: Opus · CONTADOR: cuenta_gen2 NO-APLICA; mueve sin_piso del marcador y el tipo_incertidumbre de las emisiones; adoptados_activos no debe moverse — si se mueve, PARA · FP/ADR/NC: deriva al cierre · corre en paralelo con #922 (tools/corrida0.py): no lo toques.

VERIFICACIÓN DE EXISTENCIA (dirección contra 8b7b0562)

python3 tools/marcador_segmento.py --json → sin_piso: 21, cobertura_de_piso: 73 — idéntico a antes de #915, que selló CALC-PISOS-ENIF2021-FORMALIDAD-0001 (6 celdas + 3 de universo, REPRODUCE/IDENTICO) y cuya nota dice «el enlace al marcador PARA por perímetro»: una línea no bastaba. Las emisiones C2 compuestas siguen NO-PROPAGADA-COVARIANZA-NO-SELLADA, aunque CALC-C2-COMPUESTO-IC-ENIF2024-0001 (#911) y CALC-C2-COMPUESTO-IC-ENVIPE2025-0001 (#916) ya traen IC réplica por réplica. Ambos actos dejaron «no actualiza el marcador» como sucesor. NO-ENCONTRADO: el enlace no existe.

PIEZAS

P1 · Lee por qué paró #915 (su nota, sección del PARO) y resuelve eso, no otra cosa: registrar una segunda tabla de identidad (PISOS-ENIF2021-formalidad-metadatos-*) junto a la de rejilla. Generaliza lo mínimo: el marcador lee una lista de tablas de identidad declarada en un solo sitio, con el mismo contrato de columnas; el test de enlace (toda fila CONSTRUIBLE enlaza con exactamente una MARGINAL) corre sobre todas. Las 4 filas NO-CONSTRUIBLE de formalidad en la tabla de rejilla quedan sucedidas, no editadas: si dos tablas hablan de la misma celda, manda la más reciente y el marcador lo dice en piso_fuente. P2 · ENUT y EDER. #908 dictaminó 11 celdas ENUT NO-CONSTRUIBLE por texto y 4 de EDER SIN-PISO-POR-DISEÑO. Verifica que el marcador muestre esas causas y no SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD; si #908 ya lo hizo, una línea y sigue. P3 · IC de las emisiones. El lector de emisiones toma IC-LO/IC-HI de los dos CALC de IC donde existan, por identidad exacta de celda; tipo_incertidumbre pasa a IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS solo en esas; las de ENCIG 2025 y cualquier IC-NO-CONSTRUIBLE conservan NO-PROPAGADA. El estado sigue EMITIDA-SIN-EVALUAR y el cruce sigue RESERVADA. La guardia existente (una emitida no sale por la vía por defecto ni cuenta en ADOPTADO_ACTIVO) debe seguir verde sin editarla. P4 · Re-deriva y reporta los números del marcador antes/después, cada uno con su denominador. No te doy la cifra esperada. Una frase en la nota, obligatoria: un IC estrecho sobre un C2 compuesto mide ruido muestral de un estimador que supone no-interacción; no mide el error de ese supuesto.

PERÍMETRO

tools/marcador_segmento.py · milpa/src/estimadores_segmento.py y milpa/estimadores-por-segmento.yaml (derivado) solo para P3 · tests/test_marcador_segmento.py, tests/test_estimadores_segmento.py (casos nuevos) · marcador-segmento.tsv re-derivado · data/INFRAESTRUCTURA-v1_0.md (lista de tablas de identidad) · cascada. No toca ningún CALC · ninguna tabla de identidad · tools/corrida0.py · el yaml del árbitro · celdas-D. «Si te encuentras escribiendo fuera de esta lista, PARA.»

LO QUE NO HACE

No mide el error de persistencia de las 6 celdas nuevas (sucesor: CALC nuevo, nube) · no adopta · no toca el par del piloto 3.

## CONSUMIDO

`ACTO GEN2-MARCADOR-ENLACE-2` ejecutado en la rama `claude/pensive-keller-7wxjod`; PR y ADR citados en `forense/notas/2026-09-20-GEN2-MARCADOR-ENLACE-2-cierre.md`.
