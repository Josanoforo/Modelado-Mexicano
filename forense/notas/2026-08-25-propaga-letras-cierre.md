# Nota de cierre — `ACTO PROPAGA-LETRAS`, 25/ago/2026

Ejecuta `forense/encargos/2026-08-25-PROPAGA-LETRAS-ENCARGO.md` (`FP-159`, `ADR-194`). Entorno **NUBE** (`cloud_default`). `SHA` de redacción `9c25f28`.

## §1 · Las tres firmas de mesa, verbatim

Chat de dirección, 25/ago/2026: **«R2.2: a - R8.2: a - R10.2: a»**, sobre las opciones (a) presentadas por `FP-159`/`ADR-191`:

- **R2.2 = a** → censo previo, molde `R2.1-v2`.
- **R8.2 = a** → «verificación puntual; si confirma apps-sin-tasa → archívese `B`».
- **R10.2 = a** → «D tras el cruce».

## §2 · Anexo — verificación puntual de `R8.2`, corrida por dirección (web, 25/ago/2026), aterrizado VERBATIM

Pregunta: ¿existe app/plataforma mexicana de tandas que publique tasa de incumplimiento? ¿Existe siquiera la tanda-entre-desconocidos como producto de plataforma en MX? Búsquedas (queries verbatim): (1) app tandas digitales México tasa de incumplimiento morosidad · (2) plataforma tandas entre desconocidos México app ahorro grupal Cundina. Hallazgos, con procedencia (b/c)=web, todo SIN-FETCH salvo snippets leídos: (i) Las apps de tanda mexicanas localizadas (TandaPlus, TandaMatic, Mi Cundina, Entre Cuentas, "Tandas de dinero" en Play) son organizadoras de tandas entre conocidos — llevan turnos, pagos y recordatorios; ninguna custodia dinero ni ejerce enforcement de plataforma, y ninguna publica tasa de incumplimiento (para varias el concepto ni aplica: no procesan pagos). (ii) Plataforma de tandas ENTRE DESCONOCIDOS operando en MX: NO-ENCONTRADO en estas búsquedas — el ecosistema documentado insiste en «personas de confianza», y "desconocidos/redes sociales" aparece solo como el vector de fraude, no como producto. (iii) Vía regulada adyacente EXISTE y se anota SIN usarse: Banxico (Reporte de Estabilidad 2026) publica IMOR de Sofipos (~9.8 % mar-2026, digitales vs tradicionales) — es crédito popular regulado, NO ROSCA entre desconocidos: es la re-spec de dominio distinto que la gemela ya advirtió (letra ≤C), queda como vía futura, no como evidencia de esta letra. (iv) Antecedentes que completan el universo: censo `R2.1` («candidata MINES resultó sitio de apuestas; ninguna directa abierta») y cruce `#363` (falsador `R8.2` NO-ENCONTRADO en corpus). Lectura: la fila `B` de la escala de `R8.2` —«apps con usuarios pero sin tasa de incumplimiento publicada»— describe exactamente el estado hallado, con reserva escrita: las apps existentes son organizadoras entre conocidos; la variante plataforma-entre-desconocidos que el falsador imaginó no se localizó operando en México — el falsador, tal como está redactado, hoy no tiene objeto medible con métrica pública.

## §3 · `R10.2` → archiva `D` (+1)

Entrada al Registro (parser `T18`, `hitoD-preregistro-v2_0.md` Nota 34 y bloque append-only): `R10.2` → `D`, con estampa de universo combinada `A.10`: pase `#361` (`forense/notas/2026-08-25-pase-falsadores.md`: ECCO íntegra, ELCOS `hallazgos.md:143`, mapa propietarias 6/ago) + gemelo `b06ad2f` (`forense/notas/2026-08-25-pase-falsadores-gemelo-b06ad2f.md`: `RE-ESPECIFICABLE`→`B`-máx **rechazada por mesa** — compra anécdota sin umbral) + cruce `#363` (fila exacta del TSV, `falsador_sin_fuente`/`R10.2`, citada) + la sinergia anotada: si `R2.2` termina en llave de clima, el mismo partnership reabre este `D` (vencible en alcance, reapertura por re-sello).

## §4 · `R8.2` → archiva `B` (RANURA ausente → queda PROPUESTA)

Aterrizado el anexo del §2 verbatim en esta nota; entrada al Registro **no se toca**: `R8.2` **no** gana línea en el bloque append-only. Habría archivado con la reserva escrita del anexo + universo (2 queries + censo `R2.1` + cruce `#363`) + la lectura ya pre-registrada en la propia ficha (si algún día sale `A`, «el enforcement de plataforma también sustituye» es matiz, no refutación) + vía-futura anotada (serie Sofipos/CNBV como re-spec ≤C, no ejercida) — **todo esto queda como PROPUESTA en esta nota**, sin tocar el Registro, porque la ranura de confirmación de 5 segundos llegó ausente al lanzarse el acto.

## §5 · `R2.2` → propaga la orden (sin archivar)

`ADR-194` registra la firma (a): censo previo molde-`R2.1`, lo corre mesa en sesión de proyecto con web (el bloque quotable lo entrega dirección aparte); la ficha `R2.2` recibe enmienda fechada de una línea («letra en espera del censo ordenado por mesa, 25/ago») — aplicada en `hitoD-preregistro-v2_0.md` §3.3. Nada más.

## §6 · Cierre

`FP-159` → `FIRMADA` con los tres verbatims + `ejecutada_en` = este acto (parcial: `R2.2`/`R10.2` ejecutados, `R8.2` PROPUESTO). `ADR-194` con todo. Set de sincronía: `README.md:36` re-derivado del Registro real (`21 de 27`); citas vivas de `canon/modelo-decision-v4_0.md` (`:65`, `:700`, `:885`); `canon/estado-programa-v1_10.md` (línea Hito D + «`R2.2` en censo»); esta nota-cierre; suite `--baseline` (🚫 nunca `--freeze`; `T22`/`T25` propios → censo declarado); encargo `CONSUMIDO`. **CONTADOR: +1 re-derivado** (no +2 — la RANURA de `R8.2` llegó ausente), declarado con `python3 tests/check.py --baseline`.

## Perímetro y NO-hace

Lista cerrada: Registro del preregistro + fichas `R8.2`/`R10.2`/`R2.2` (enmiendas fechadas) · `README.md:36` · citas `modelo-decision` · `gobernanza` · `estado` · tablero (`FP-159` + numeración libre) · notas · encargo. Fuera de esta lista, PARA. No toca `R2.1`/`R3.4`/`R10.1`/duelo/pool/milpa. No corre el censo de `R2.2` (es de mesa). No usa la serie Sofipos como evidencia. No colapsa «no localizado operando» con «no existe» — la reserva lo dice con las palabras del anexo.
