ENCARGO · ACTO GEN2-FAM-UNION-ESTIMANDO-1 · LA REGLA `familia.union.libre` DICE "PRIMERA UNIÓN" Y CARGA UNA CIFRA DE SITUACIÓN CONYUGAL ACTUAL: UN ESTIMANDO, UN NOMBRE, UNA CIFRA SELLADA

CABECERA (D-12) · SHA de redacción `8e455bd6`; re-deriva al abrir · ENTORNO: NUBE — cero microdato; las dos mediciones ya están selladas; NO caja · una sola sesión, rama propia; `/acto` PARA si ya está archivado en otra rama viva · COMPUERTA: `CALC-ENADID-0001` (#869) y `CALC-EDER-0003` en main (cumplida) · MODELO: Opus (toca una regla del motor con tier FUERTE) · FP/ADR/NC: deriva al cierre; renumera quien fusione segundo · CONTADOR: `cuenta_gen2` NO-APLICA (no sella corrida); mueve el relevo de RES-0043/0044 y `adoptados_activos` si el enlace queda activo — reporta lo derivado.

EL PROBLEMA, EN TRES HECHOS LEÍDOS (contra `8e455bd6`)

1. `milpa/tramite.yaml:1034-1037` — regla `familia.union.libre`, `situacion: primera_union`, tier `FUERTE`: `union_libre p = 0.1905`, `matrimonio_directo p = 0.8095`, clase "prevalencia bruta ponderada 15+, ENADID 2023, `p3_27_ag`".
2. `CALC-ENADID-0001` (#869, `REPRODUCE/IDENTICO`) re-midió esa fuente y su nota dictamina: 0.1905 es situación conyugal actual de toda la población 15+; 0.8095 es su complemento aritmético — incluye solteras, separadas, divorciadas y viudas — y "no significa matrimonio". Actualmente casada: 0.359 bruta.
3. `CALC-EDER-0003` (sellada, `cuenta_gen2 = SI`, `REPRODUCE`) mide lo que el nombre de la regla promete — tipo de primera unión, EDER 2017, n = 18 689 alguna vez unidos: `P-LIBRE = 0.481`, `P-DIRECTO = 0.519`, con IC de diseño y gradiente por cohorte. Su propio resultado dice `DELTA-VS-GEN1 = NO-APLICA-ESTIMANDO-DISTINTO`. Costo para un lector: el motor afirma hoy que 81% de las primeras uniones en México son matrimonio directo; la medición sellada de ese estimando dice 52%. Son 29 puntos en una regla FUERTE, y la causa no es un error de cálculo: es un nombre puesto sobre otra cantidad.

FIRMA DE MESA — FIRMADA, primera opción. Mesa, 19/sep/2026, a las tres propuestas de dirección: «si si y de acuerdo contigo.» («de acuerdo contigo» = la recomendación de dirección: tipo de primera unión con EDER). Texto operativo:
"La regla `familia.union.libre` mide tipo de primera unión. Sus `p` pasan a ser los de `CALC-EDER-0003` (`P-LIBRE`, `P-DIRECTO`, con IC y universo: personas alguna vez unidas, EDER 2017). La prevalencia ENADID 2023 de situación conyugal actual se conserva como dato descriptivo aparte, con nombre propio (`union_libre_actual`, `actualmente_casada`), nunca como `matrimonio_directo`. RES-0043 y RES-0044 se relevan según esto." Alternativa que mesa NO eligió (queda como historia): la regla pasa a `situacion: situacion_conyugal_actual` con los RESULT de ENADID y el nombre `matrimonio_directo` desaparece. Dirección recomienda la primera: el `porque` de la regla (unión libre como opción racional ante baja garantía institucional del matrimonio) habla de cómo se entra a la unión, no de cuánta gente está hoy en cada estado.

VERIFICACIÓN DE EXISTENCIA (A.8)

* (1) Gobiernan `milpa/tramite.yaml`, `data/corrida0/relevo-usos-v1_0.tsv` (fila 46: RES-0044 → `…:matrimonio_directo`, `LEGACY-GEN1`, `LISTADO-PARA-MESA`, candidato `CALC-EDER-0003`), `tools/relevo_usos.py`, `tools/medidor_union_libre.py`, `tests/check.py`. Cubren.
* (2) `git grep -n "matrimonio_directo" -- milpa/` → `tramite.yaml:1037` sigue con 0.8095: no está hecho. NC-0254 cerró (#872) con sucesor "corrida ENADID 2023": la corrida existe; el relevo no.
* (3) Decisión previa a re-verificar (A.17), no a heredar: la spec de `CALC-EDER-0003` (línea 22) dice que la regla "conserva su p y su veredicto CORROBORADA". Localiza el ADR/FP que lo decidió y cítalo: esta firma lo sucede, no lo ignora.

PIEZAS

P1 · Los dos estimandos, por texto de pregunta (A.15). Cita del cuestionario ENADID 2023 (3.27, situación conyugal) y del FD de EDER 2017 (`edo_civil1`, primera unión): evento, unidad, universo, denominador, periodo. Tabla de dos filas. Si la lectura contradice alguno de los tres hechos de arriba, PARA y reporta. P2 · La regla. Edita solo la entrada `familia.union.libre`: conductas, `p`, IC, `clase` con instrumento-ola-universo, `RESULT` citados por id. El gradiente por cohorte de EDER ya sellado se conserva si ya está en la regla; no se añade nada que no tenga `RESULT`. Bloque descriptivo aparte para situación actual con los ids de `CALC-ENADID-0001`. Tier: se re-evalúa por separado la cifra (medida, dos olas de fuente distinta) y el mecanismo del `porque` (hipótesis razonable: ningún instrumento mide "garantía institucional"; el propio yaml lo marca `NO-MEDIDO`). Si el esquema no admite tier partido, se declara en `nota` y va a mesa como FP. P3 · Relevo. RES-0043/0044 por `tools/relevo_usos.py`, por comando; si el comando no cubre el renombre, PARA esta pieza y propón. `status` antes/después con worktree. P4 · Un test que falle si `matrimonio_directo` vuelve a aparecer con una `clase` que cite `p3_27` o "situación conyugal". Es el defecto ocurrido; ninguno más.

PERÍMETRO Y CONCURRENCIA

`milpa/tramite.yaml` (una entrada) · `milpa/procedencia.yaml` solo si la entrada lo exige · `relevo-usos` y derivados por comando · `tests/test_union_estimando.py` (nuevo) · `decisiones.tsv`, `no-corrido.tsv`, `hallazgos.md`, ADR, recifrado L0, tablero (cascada). No toca: ningún CALC · `tramite-ola5-propuesta-v0.yaml` · marcador · `tools/corrida0.py` · ninguna otra regla. En paralelo: MARCADOR-PISOS-ENLACE-1 y RECIBO-CODEX-4 (comparten solo TSV de gobierno). «Si te encuentras escribiendo fuera de esta lista, PARA.»

LO QUE NO HACE

No mide · no re-ejecuta ENADID ni EDER · no toca otras reglas de `familia.*` aunque encuentre el mismo patrón — las lista (ver sucesor).

SUCESOR

Barrido de una pasada: ¿qué otras conductas de `tramite.yaml` son "complemento aritmético con nombre sustantivo"? Lista con archivo y línea en la nota; de ahí sale, si hay demanda, el siguiente acto.

MÓDULO DE AUDITORÍA (afirma sobre México: aplica completo)

¿Estructura confundida con cultura? La unión libre en México tiene gradiente fuerte por cohorte, escolaridad y región, y costos reales de formalización; leerla como "preferencia cultural" o como "unión fallida" es el riesgo de mala lectura — la regla dice "opción racional" y eso es una hipótesis, no un hallazgo. ¿Sobregeneralización? EDER 2017 cubre personas alguna vez unidas; no habla de quienes nunca se unieron ni de uniones posteriores; ninguna de las dos fuentes segmenta aquí por condición indígena, donde la unión consuetudinaria es otro orden institucional: fuera por diseño, y se dice. Clase de evidencia: (a) en ambas fuentes. Escalas: proporción sobre universos distintos (alguna vez unidos vs. población 15+): por eso no se restan ni se promedian. Falsabilidad: la cifra cambia si una EDER posterior mueve `P-LIBRE` fuera de su IC por cohorte; el mecanismo cambia si aparece un instrumento que mida garantía institucional percibida y no correlaciona. Peligroso leído simplista: "48% entra por unión libre" como juicio sobre estabilidad familiar.
