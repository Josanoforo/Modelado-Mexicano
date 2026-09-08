ENCARGO · GEN2-TRAMITE-TABLERO-2
Refrescar §9 del tablero y asentar la serie de negativos falsos
Redactado el 8/sep/2026 contra origin/main = d1a97cd6. Validado por dirección (Tablero 004): acto propio, con compuerta.

Cabecera
campo	valor
SHA de redacción	d1a97cd6 (8/sep 15:01 −06:00, tras fusionar el PR #634)
ENTORNO ASIGNADO	NUBE. No lanzar en caja: no toca microdato, data/raw ni red a fuentes
COMPUERTA	GATED a GEN2-FIRMA-CONTADOR. Ver el bloque de abajo — es verificable y la skill debe negarse si no se cumple
MODELO SUGERIDO	Sonnet. Dos ediciones de archivo, sin juicio
Candidatos	Máximos al redactar: ADR-412 · FP-359 · NC-0052 → candidatos ADR-413 · FP-360 · NC-0053. Derívalos con tools/cierre_acto.py; no los heredes — al redactar el anterior ya quedaron cortos en una tarde
Ramas vivas	origin/acto/gen2-e5-calc-0001-0003 y origin/acto/gen2-e5-1-verificador-calc0003v2, ambas de caja. Perímetro disjunto
ADJUNTO OBLIGATORIO	Uno: TABLERO-PROGRAMA.md, cuerpo v2.3 regenerado después de la firma

⚠️ COMPUERTA — verifícala antes de tocar nada
Este acto no se ejecuta hasta que GEN2-FIRMA-CONTADOR haya fusionado a main. La razón es la que dirección nombró y es exacta: si el cuerpo v2.3 aterriza antes de la firma, nace mintiendo en §2 el mismo día que corregimos §9 por mentir. Sería el defecto que este acto existe para reparar, cometido por el acto que lo repara.

Verificación mecánica, no de juicio:
git fetch origin && git rev-parse --short origin/main
python3 tools/corrida0.py status | head -5
Si N_corridas_selladas sigue en 0 y N_resultados_sellados en 0: la firma no ha fusionado. La skill se niega, reporta con A.13 y termina con cero commits.
Si ya se movieron: la compuerta está abierta. Sigue.

Segunda verificación, sobre el adjunto: la tabla de §2 del cuerpo v2.3 debe coincidir con la salida de status en el momento de ejecutar. Si no coincide, PARO sobre B1 con razón PARO-PREMISA — el adjunto se regenera del lado del tablero y el acto se relanza. No edites las cifras del adjunto para hacerlas cuadrar: eso es inventar el adjunto por otra vía, y el blindaje existe precisamente contra eso.

Arranque
Ejecuta /acto. Si el terreno no coincide con lo declarado, PARA y repórtalo.
Si el adjunto no llega: PARO sobre B1, razón PARO-PREMISA, y B2 corre igual. Dirección confirma que el lanzamiento lleva el .md pegado junto al encargo; el blindaje queda por si acaso, que es la tercera vez que hace falta.

Verificación de existencia (A.8)
(1) Estructura. El índice ya gobierna el dominio: grep -c "forense/tablero" data/INFRAESTRUCTURA-v1_0.md → 5 (lo cerró A7 del PR #633). Sin hueco que declarar.
(2) Contenido. Reproducidas por dirección contra su árbol, las cuatro:
$ grep -c '9 · Ajustes pendientes en el repo' forense/tablero/TABLERO-PROGRAMA.md   → 1   la sección obsoleta SIGUE ahí
$ grep -cE '^\| \*\*A[1-7]\*\*'                forense/tablero/TABLERO-PROGRAMA.md   → 6   las filas de pendientes
$ grep -c '#633'                               forense/tablero/TABLERO-PROGRAMA.md   → 0   el acta de verificación NO está
$ grep -c 'forense/tablero' data/INFRAESTRUCTURA-v1_0.md                            → 5   confirmado
Vocabulario A.4: NO-ENCONTRADO. La §9 sigue listando como pendientes los siete ajustes que el PR #633 ya ejecutó.
(3) Cobertura retroactiva. No aplica: la §9 nació en el cuerpo que aterrizó el 8/sep.

Piezas
B1 · Reemplazar el cuerpo curado por la versión v2.3
Sustituye el contenido de forense/tablero/TABLERO-PROGRAMA.md por el adjunto, íntegro.
Qué cambia: el bloque derivado se refresca al SHA de ejecución; §9 deja de ser lista de pendientes y pasa a acta de verificación de las siete piezas del PR #633, con comando y resultado por fila; entra §10 con lo que queda abierto; se asientan las dos retractaciones; la bitácora gana la fila v2.3; y §2 lleva la señal post-firma, no la de antes.
Por qué no es cosmética: un tablero que declara pendiente lo que ya se hizo miente sobre el estado del programa, que es lo que el tablero existe para no hacer. El defecto lo introdujo la conversación del tablero al mandar un cuerpo con una sección que caducaba al fusionarse.
Verificación de cierre:
grep -cx '<!-- TABLERO-DERIVADO:BEGIN -->' forense/tablero/TABLERO-PROGRAMA.md   # esperado 1
grep -cx '<!-- TABLERO-DERIVADO:END -->'   forense/tablero/TABLERO-PROGRAMA.md   # esperado 1
grep -c '9 · Ajustes pendientes en el repo' forense/tablero/TABLERO-PROGRAMA.md  # esperado 0
grep -c '#633'                              forense/tablero/TABLERO-PROGRAMA.md  # esperado >=1
python3 tools/tablero_programa.py --actualiza                                    # sin error
python3 tools/corrida0.py status                                                 # debe coincidir con §2

B2 · Asentar en forense/hallazgos.md la serie de tres negativos falsos
Una entrada, fechada, con las tres instancias juntas — el valor está en verlas como serie, no como incidentes sueltos. Las tres son de la conversación del tablero, del 8/sep, y las tres son A.13. Dirección avaló esta forma.
grep -rlE "Gen 2|v2_1|Snapshot v1\.7" dio positivo en los tres archivos de forense/tablero/: v2_1 casa como subcadena con v2_13. Casi da por aterrizados snapshots que no lo estaban. La prueba correcta es por SHA.
Un grep de encabezados con patrón ^- \*\*[A-Za-zá ]+\.\*\* excluía paréntesis, y por eso se concluyó que el bloque vivo no conocía Gen 2. Sí lo conocía: la línea es - **GEN2 (derivado de corrida0 status).**.
Una lectura de 3 000 de 80 323 caracteres del ADR-411 llevó a afirmar que no declaraba el perímetro. Lo declara, y nombra tests/check.py con la constante _T_YAMEDIDO_ARCHIVOS_CONOCIDOS.
La lección, en una línea: en las tres el comando corrió, devolvió algo, y ese algo no era lo que se creía haber preguntado. A.13 exige declarar cuántos archivos examinó un negativo; estas tres piden declarar además qué examinó de cada uno — subcadena contra línea, patrón contra campo, fragmento contra documento.
No añade regla ni test. Es una entrada de hallazgos, y por eso no paga el impuesto de v2.3 §aparato.

Perímetro y concurrencia
Toca: forense/tablero/TABLERO-PROGRAMA.md · forense/hallazgos.md · más la cascada de cierre, que en este repo incluye siempre canon/gobernanza-v1_15.md, canon/registro-rotulos.tsv, canon/estado-programa-v1_12.md (§L0), forense/no-corrido.tsv y el propio encargo archivado en forense/encargos/.
Condicional de la cascada, aportada por dirección y ahora en la plantilla: forense/firmas-pendientes.tsv entra a la cascada siempre que el acto cree o ejecute una ranura de firma (A.12). B2 no crea ninguna, así que para este acto la lista de arriba está completa tal cual. Y tests/check.py es lectura en el cierre —--baseline en VERDE o PARO— no escritura: no es cascada salvo que el acto añada un test, que aquí no.
Actos en paralelo: dos ramas de caja con perímetro data/corrida0/CALC-* y los tres TSV del registro. Disjunto.
Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

Contador
Este acto no mueve ningún contador de la señal de Gen 2, y se declara. La señal la mueve GEN2-FIRMA-CONTADOR, que corre antes; este acto solo hace que el tablero la refleje. Es corrección de un artefacto de registro.

Lo que este encargo NO hace
No traza el origen de ningún dato de Gen 1.
No toca milpa/**, data/corrida0/**, ni ninguna corrida sellada. En particular no toca milpa/tramite.yaml: el defecto que un sucesor le atribuía no existe — las tres líneas tier: de más están anidadas a indentación 6 y motor_tiers parsea por regla. Dirección reprodujo la retractación con histograma de indentación.
No atribuye el salto de WARN 203 → 211. Costaría tres corridas de suite y ninguno de los actos declaró añadir avisos. Queda como T1 en §10, sin dueño.
No cierra G1 (el GO de E.5 no derivable) ni G2 (vigencia y delta sin implementar): son de dirección.

Cierre
Cascada por tools/cierre_acto.py. ## NO-CORRIDO / RESERVAS obligatoria antes de ## CONSUMIDO, con Ninguno. si no hay. Filas esperables: B1 por adjunto faltante o por señal discordante (PARO-PREMISA). Política de cero ramas: la rama se fusiona o se borra.

Orden de la tarde, para que nadie lance a ciegas
Fijado por dirección:
#634 — ya fusionó, 8/sep 15:01. main en d1a97cd6, máximos ADR-412 · FP-359 · NC-0052.
GEN2-FIRMA-CONTADOR (NUBE) — mueve la señal. Es la compuerta de este acto.
UNIVERSO-C (caja) — le llegó su turno.
GEN2-TRAMITE-TABLERO-2 (NUBE, este) — con el v2.3 ya regenerado contra la señal post-firma.
Pendiente del lado del tablero antes de lanzar: regenerar el adjunto v2.3 con la señal post-firma. La receta es python3 tools/corrida0.py status sobre main una vez la firma fusione, y reescribir la tabla de §2 con esa salida. Hasta que eso ocurra, el adjunto que existe hoy lleva la señal pre-firma y no debe lanzarse.

## NO-CORRIDO / RESERVAS

- **qué:** B1 · Reemplazar el cuerpo curado por la versión v2.3 (`forense/tablero/TABLERO-PROGRAMA.md`).
  **por qué:** `PARO-PREMISA`.
  **impacto:** §9 del tablero sigue listando como pendientes las siete piezas que el PR #633 ya ejecutó; §2 sigue con la señal pre-firma (`0/86` corridas selladas, `0/205` resultados sellados) en vez de la real (`3/86`, `211/205`).
  **sucesor:** `GEN2-TRAMITE-TABLERO-2` (relanzamiento), con el adjunto v2.3 regenerado del lado del tablero contra la señal post-firma. Asentado como `NC-0054` en `forense/no-corrido.tsv`, `estado = ABIERTA`.

  El adjunto sí llegó a la sesión, así que el bloqueo no es por ausencia: es por **señal discordante**, el caso que este mismo encargo nombra en su bloque de COMPUERTA y para el que prohíbe explícitamente el remedio de editar las cifras del adjunto. Su bloque derivado trae `SHA d1a97cd6`, `ADR máximo 412`, `FP máximo 359` y `corridas selladas 0/86 · resultados sellados 0/205` — la señal de **antes** de que `GEN2-FIRMA-CONTADOR` fusionara. Contra el árbol de ejecución (`origin/main` tras el `PR #636`, `ADR` real `413`, `FP` máximo `360`, `python3 tools/corrida0.py status` → `N_corridas_selladas=3`, `N_resultados_sellados=211`), ninguna de las cuatro cifras coincide.
