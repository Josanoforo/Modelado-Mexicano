# ENCARGO · ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-2-3

**Archivado verbatim por 0-bis A.3 el 20/sep/2026 (21:07 CST).** Texto recibido de dirección, sin editar. Base del acto: `origin/main` = `04a2edeb` (SHA de redacción del encargo; 0 commits de diferencia al abrir). Rama: `acto/gen2-celda-d-piloto-3-commit-2-3`, worktree `/home/pc0/mm-piloto-3-c23`.

---

ENCARGO · ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-2-3 · SE ABRE ENCIG 2025 POR PRIMERA VEZ: EMISIONES SELLADAS, DESPUÉS LA REALIDAD, DESPUÉS EL VEREDICTO — CON EL CÓDIGO QUE YA ESTÁ CONGELADO Y NI UNA LÍNEA MÁS

ENTORNO: CAJA (máquina local, corpus montado). El hook de arranque imprime ENTORNO-DERIVADO; si no dice CAJA, PARA en una línea. Worktree nuevo: nace sin data/raw ni data/raices.local.yaml — se enlazan; no es PARO.

CABECERA · SHA de redacción 04a2edeb; re-deriva al abrir · una sola sesión, rama propia · MODELO: Opus · MODO: RÍGIDO — reserva de evaluación y spec congelada: la latitud es sobre logística, nunca sobre el procedimiento · F3 (FP-400, firmada): quien congeló el COMMIT-1 v1.1 no ejecuta. Lo congeló la sesión de caja pc0-77 (rama acto/gen2-celda-d-piloto-3-commit-1-v1_1, #926). Si tú eres esa sesión, o tienes en contexto los diseños A/B o el careo del piloto 3, PARA y dilo · CONTADOR: sella dos corridas; cuenta_gen2 = SI propuesto para ambas, nacen PENDIENTE-DE-MESA salvo firma; no adopta; adoptados_activos no debe moverse · FP/ADR/NC: deriva al cierre.

1 · OBJETIVO

Ejecutar, tal como está congelado, el tercer piloto pre-registrado del programa: ¿se transporta a 2025 una interacción edad × escolaridad que fue estable en 2021 y 2023, cuando el nivel de la cantidad se movió once puntos? Es la primera vez que alguien del programa abre ENCIG 2025 por dos variables. Se hace una sola vez. «Hecho» significa: CALC-GOB-DIGITAL-EXE-EMISIONES-0002 sellado y empujado; después CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001 sellado; veredicto y B-bis resueltos con las palabras de la spec; las dos corridas en la vista con su asiento de replay (E.7); celda-D llena; marcador re-derivado.

2 · FIRMAS DE MESA

Ya dadas, verbatim — no se piden otra vez:

FP-389 · F1-bis (20/sep): rejilla de edad y coherencia sobre el universo sin residuo; elegibilidad con tolerancia de ⅓; 18–29 × hasta primaria FUERA-DE-SOPORTE ex ante. FP-399 · S2 (20/sep): «El código 97 es edad real censurada y se reconoce como tal. […] Para 2025, el COMMIT-2 cuenta los trámites con código 97 con una sola variable de agrupación y lo reporta. Siguen fuera del universo del cruce […]. Si superan el 1 % de los trámites de la banda 60+, el veredicto lleva la marca RESERVA-S2; no detiene el piloto.» FP-400 · F3 (20/sep): «El COMMIT-1 v1.1 lo congela esta sesión, en caja. […] Los COMMIT-2 y 3 los ejecuta OTRA sesión.» Cuaderno del 21/sep, renglón 4.2: «unidad «evento» — a». (FP-393 sigue ABIERTA en main al redactar: la propaga GEN2-TRAMITE-FIRMAS-3, en vuelo. Si al llegar al registro de la celda-D ya fusionó, usa evento; si no, registra lo que el contrato admita hoy, di cuál, y deja NC con ese sucesor. No es PARO.)

Propuesta — tu lanzamiento con este archivo es el sello; sin ella las dos corridas nacen PENDIENTE-DE-MESA:

«Cuentan (cuenta_gen2 = SI) CALC-GOB-DIGITAL-EXE-EMISIONES-0002 y CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001, sea cual sea el veredicto: una prueba pre-registrada que sale "nadie vence" o "falsador débil" cuenta igual que una que sale "vence".»

3 · LO QUE DIRECCIÓN SABE (contra 04a2edeb, 21/sep)
[EJECUTADO] cd forense/prereg-caja && sha256sum -c GOB-gobierno-digital-exe15-spec-v1_1.sha256 → OK.
[EJECUTADO] python3 -m pytest tests/test_piloto3_v11.py -q en el contenedor de dirección, sin corpus: 6 passed, 1 skipped, 6.6 s. Pasan: medir() de punta a punta sobre sintético, adjudicacion.medir() sobre un R sintético, las negativas de la adjudicación sin sello, y las guardias. El skipped es la prueba de oro, que necesita ENCIG 2023.
[LEÍDO] Nota del COMMIT-1 v1.1 (forense/notas/nota-2026-09-20-gen2-celda-d-piloto-3-commit-1-v1_1.md:41): en caja, test_b_oro_2023_reproduce_los_sellados PASSED — 16 n exactos, |Δp| = 0.0, |Δδ| = 1.7e-16, |ΔIC| < 1e-9, residuo de edad 107 = 107 × código 98. Yo no lo ejecuté; tú sí debes, antes de abrir 2025.
[EJECUTADO] Compuertas en firmas-pendientes.tsv y no-corrido.tsv: FP-389, FP-399, FP-400 → FIRMADA · NC-0355 → CERRADA, veredicto CAMBIO-MENOR por texto (reactivo 7.3, nueve opciones, N_TRA = 01 y flujo idénticos en 2021/2023/2025; 2025 inserta el trámite 15 y recorre 15–22 → 16–23; nada toca el 01 ni {4,5} sobre {1,2,4,5,6}).
[LEÍDO] Spec v1.1: estimando = proporción de pagos ordinarios del servicio de luz (N_TRA == 01) por canal digital {4,5} entre canal válido, unidad TRÁMITE; 16 celdas, 15 PUNTUADA; candidatos C2, C1a, C1b, S½, Sλ con λ = 0.8937949410086089; PCG64(20260919), 10 000 réplicas en bloques de 50; unión sec_7 ← residentes por ID_PER, m:1, validada. Orden de ejecución (:57): corrida0 run CALC-GOB-DIGITAL-EXE-EMISIONES-0002 → commit y push → corrida0 run CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001.
[LEÍDO] Spec :43: el tercer requisito de soporte (n ≥ 200 en 2025) exige agrupar por dos variables, así que solo lo lee el código del COMMIT-3; el COMMIT-2 lo deja como hipótesis declarada. :62: la adjudicación se niega si falta el sello de emisiones, si su sha256 no coincide, o si el C2 recalculado no reproduce el sellado a 1e-9.
[EXISTE] data/curacion-registro/celdas-d/GOB.gobierno_digital.encig2025.edad_x_escolaridad.yaml (la trajo #926); no leí con qué unidad nació.
[SUPUESTO] que ninguno de los dos CALC lee el yaml legacy del árbitro como insumo. Si lo leen, el registro puede bajar cuenta_gen2 a NO al regenerar (caso FP-395/397): no fuerces nada, reporta el campo que decide.
[SUPUESTO] que nadie ha abierto ENCIG 2025 por dos variables desde el 20/sep. Busca en el repo y en tu disco restos que por nombre lo sugieran; si hay alguno, ruta, fecha y tamaño — no lo abras — y PARA antes del COMMIT-2.
4 · YA HECHO / YA DECIDIDO

#894 y #903 (P0 en nube, PARO y selección del cruce) · #924 (S1 y S2 por texto en caja; PARO por medidor vacío) · #926 (COMMIT-1 v1.1 con cuerpo y prueba de oro). Nada de COMMIT-2 ni 3 existe: los dos directorios CALC traen solo spec.yaml y su código; CALC-GOB-DIGITAL-EXE-EMISIONES-0001 es la v1.0, superada sin correr.

5 · PIEZAS — orden estricto; cada una gatea a la siguiente

P0 · Antes de tocar 2025. Sidecar de la spec OK · pytest tests/test_piloto3_v11.py: los 7 deben pasar aquí, incluida la de oro sobre ENCIG 2023. Si la de oro falla en tu entorno: PARO — el código congelado ya no reproduce lo sellado y no se abre la ola. P1 · COMMIT-2 · emisiones. python3 tools/corrida0.py run CALC-GOB-DIGITAL-EXE-EMISIONES-0002, sin argumentos que la spec no declare. Sella. Reporta el conteo de código 97 en 2025 y si dispara RESERVA-S2 (FP-399). Registro en la vista y asiento de replay en este mismo paso (E.7). Commit y push. Confirma con git ls-remote que el commit está en origin antes de seguir: el orden del diff es el sello. P2 · COMMIT-3 · la realidad y el veredicto. python3 tools/corrida0.py run CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001. El código deriva R(a,b), verifica el soporte de 2025, adjudica por celda con las dos condiciones INDECIDIBLE, aplica la regla de ¾ y calcula ΔMAE con su IC. Si fallan ≥ 5 de 15 por soporte: FUERA-DE-SOPORTE global, y ése es el veredicto. Sella, vista, replay. P3 · El veredicto, con las palabras de la spec. B-bis tal como está escrito: corroborada, acotada · falsador débil (manda si ambas lecturas caben) · un retador vence — y si vence Sλ y no S½, o al revés, el hallazgo es sobre cuánto encoger. Nada que no esté pre-registrado entra al veredicto. Si ves algo interesante, va en una sección rotulada EXPLORATORIO — NO ADJUDICA, después del veredicto, nunca antes. P4 · Registro. Celda-D GOB… con veredicto, margen_material, champion_actual (el que la regla dé; NINGUNO si nadie vence — y entonces, por la firma del 17/sep, el piso C2 no vencido es el estimador de la celda: dilo, no lo adoptes tú), y la unidad según §2. Marcador re-derivado por comando: el par edad × escolaridad de ENCIG 2025 deja de estar RESERVADA. Reporta celdas_validadas antes/después, derivado. P5 · Para mesa, al frente de la nota, en lenguaje llano: qué se probó, qué salió, con qué certeza, y qué no significa. Una página.

6 · LATITUD — solo logística

Enlazar data/raw; instalar dependencias que requirements.txt no traiga (pytest, numpy, pandas); resolver rutas; reintentar un paso que falló por entorno sin haber producido salida. Un paso que produjo salida no se repite: «el primer resultado que produzca este procedimiento es el que se reporta».

7 · PAROS (lista cerrada)

a) Editar spec, sidecar, medidor.py, adjudicacion.py, λ, umbrales, lista de PUNTUADA o B-bis · b) el código congelado no corre → no se parcha; el sucesor es un COMMIT-1 v1.2 de otra sesión · c) agrupar encig25* por dos variables fuera de adjudicacion.py, o antes de que las emisiones estén selladas y empujadas · d) cualquier salida en scratch · e) repetir una corrida que ya produjo resultado · f) la prueba de oro no pasa · g) entorno equivocado, o F3 violada · h) rastro de que 2025 ya se abrió por dos variables. No es paro: main movido; cuenta_gen2 rebajada por el registro; FP-393 aún abierta; un veredicto que no te guste.

8 · COMPUERTAS

«Prueba de oro en verde» protege: abrir dato. «Emisiones selladas y en origin» protege: abrir dato (el cruce de 2025). Ninguna más.

9 · PERÍMETRO

Propio: los dos directorios CALC — solo ejecucion.json, resultados.json, sello.* · la celda-D GOB… · filas propias en corridas.tsv, resultados.tsv, replay-evidencia.tsv · derivados y marcador por comando · nota · cascada. Ajeno: la spec y su sidecar · todo .py de los dos CALC · tools/ · tests/test_piloto3_v11.py · cualquier payload que no sea ENCIG 2021/2023/2025 · los otros dos cruces de ENCIG 2025 (sexo × edad, sexo × escolaridad), que siguen RESERVADA.

10 · NO HACE · SUCESORES · AUDITORÍA · CIERRE

No adopta · no mide nada fuera de la spec · no toca los otros cruces · no re-dictamina S1 ni S2. Sucesores: firma de mesa sobre el estimador de la celda · la mesa MOTOR recibe el resultado: es el primer dato sobre si una interacción histórica encogida sirve de algo, y alimenta su lista de retadores · informe v1.2. Auditoría (afirma sobre México: aplica completo). El universo es pagar la luz: una clase de trámite, entre quienes lo hicieron. No es «gobierno digital» ni confianza en el Estado. edad × escolaridad aquí es, antes que actitud, acceso, conectividad, bancarización y alfabetización digital por cohorte; la celda con interacción en 2021 y 2023 es 60+ × hasta primaria — donde el piso, que supone no-interacción, más se equivocaría, y donde un lector aplicado más daño haría con una cifra centrada. La celda excluida (jóvenes con primaria o menos) es escasa porque la cobertura escolar subió: estructura, no dato faltante. Si un retador vence, dice que una regularidad se transporta entre olas; no dice por qué existe. Si nadie vence con IC ancho, es falsador débil, no «tercera corroboración». Unidad trámite: quien pagó doce veces cuenta doce. Sin región ni condición indígena en la rejilla. Clase (a). Ninguna cifra esperada en este encargo. Peligroso leído simplista: «C2 gana tres veces» como «no hay interacciones entre segmentos en México»; «+11 pp» como confianza digital. Cascada de /acto · ## NO-CORRIDO / RESERVAS · ## CONSUMIDO · cero ramas.
