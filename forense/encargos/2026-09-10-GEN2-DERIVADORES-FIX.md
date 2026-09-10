ENCARGO · ACTO GEN2-DERIVADORES-FIX · EL BUSCADOR LEE TODO EL DOCUMENTO Y EL VACÍO DEJA DE SER COMODÍN — H4/H6 de la revisión adversarial, más la ceguera declarada del inventario (NC-0123)

CABECERA · NUBE, Opus · NO se lanza en CAJA · COMPUERTA: GATED a PR del ACTO GEN2-ADQ-CONTRATO-FIX fusionado (fila NUBE; orden recomendado por la revisión) · redactado contra origin/main = cc1cfe2c · candidatos: deriva al cierre, no heredes.

FIRMA DE MESA, 9/sep/2026, verbatim (adentro; su merge sella): «Encargo f5 corriendo, revisa este de chatpgt y dame este encargo y los que siguen de Gen2, necesito que medes al menos 5 encargos a correr en claude code, no me separas los que te estoy pidiendo, dame 5 completos.» — despacho 2/5. Verificación de dirección: H6 confirmado en patrón en clon propio (tools/corrida0.py ~2921–2938: if asentado and asentado != hoy — el hash vacío jamás se compara, comodín exacto donde la vigencia exige identidad); H4 con fixture ejecutado por la revisión, se re-ejecuta aquí primero.

VERIFICACIÓN DE EXISTENCIA (A.8, dirección, contra cc1cfe2c): gobiernan tools/digesto_tramite.py (_busca_candidatas_fila_k, texto.find(rid) una sola vez) y tools/corrida0.py (comparación de identidad en vigencia). La revisión constató que las 26 filas reales del registro SÍ traen los tres campos de identidad — el defecto es laguna ante evidencia incompleta futura, no corrupción presente: se repara la compuerta, no se reabre historia. NC-0123 EXISTE ABIERTA (índice de reactivos ciego a ENIF; misma clase que su ceguera a DBF que el trío viejo ya padeció).

PIEZAS: P0 · CASOS ROJOS PRIMERO. Re-ejecuta los dos contraejemplos (H4: primera mención con obligación + segunda con sucesora firmada → cero candidatas; H6: recibo REPRODUCE/IDENTICO sin hashes → (True,'') ante identidad nueva) y congélalos como tests que fallan antes de tocar código. P1 · H4, TODAS LAS APARICIONES. _busca_candidatas_fila_k examina TODAS las apariciones del id con identidad completa (id como token, no como prefijo de otro id), aplica exclusiones POR APARICIÓN y deduplica después; archivo ilegible → universo declarado incompleto (A.13), nunca silencio. La coincidencia sigue siendo candidata — el cierre humano conserva cita y estampa. Para sucesoras que no repiten el id literal: implementa solo el seguimiento de referencias realmente derivable (enlace explícito a la fila) y declara el residual de lectura humana — sin motor semántico. El tope de presentación pagina: la rutina puede recorrer todas las candidatas en ciclos sucesivos sin ocultar filas indefinidamente. Aceptación: primera mención excluida y segunda válida · varias candidatas en un archivo · id prefijo de otro · fuente ilegible · sucesora enlazada sin repetir id · paginación que agota el conjunto. P2 · H6, IDENTIDAD SUFICIENTE O NADA. La proyección de vigencia exige los campos de identidad completos para acreditar REPRODUCE vigente; un recibo con hash vacío se proyecta como historia con limitación expresa (IDENTIDAD-INCOMPLETA), jamás como verificación equivalente. Cálculo legítimamente sin insumos ≠ información ausente: tratamiento explícito propio (SIN-INSUMOS-DECLARADO), no comodín. Aceptación: vaciar cada hash por separado · cambiar cada hash por separado · el caso sin-insumos declarado pasa · la ausencia de identidad nunca certifica identidad. P3 · NC-0123, LA CEGUERA SE DECLARA (reparación bajo D-14, no por reflejo). La cabecera de data/inventario-reactivos-v1_2.tsv (o su sucesor versionado) gana la declaración de cobertura: qué payloads/formatos indexa y cuáles NO (DBF completo, ENIF — con la lista derivada por comando, no de memoria), de modo que ningún negativo pueda derivarse de él fuera de su universo (A.15 ya lo prohíbe; ahora el archivo mismo lo grita). La REPARACIÓN (indexar DBF/ENIF) solo se ejecuta si contestas por escrito el gate D-14 en la nota — defecto real citado (dos falsos negativos ya pagados: trío viejo y S-specs), daño material, costo menor que seguir resolviendo por codebook — y si la respuesta es no, NC-0123 se cierra POR DECLARACIÓN con sucesor condicional al próximo falso negativo. Ambos desenlaces son entregables.

PERÍMETRO Y CONCURRENCIA. Toca: tools/digesto_tramite.py · tools/corrida0.py (solo la comparación de identidad) · data/inventario-reactivos-* (cabecera/sucesor) · tests propios (test_digesto_candidatas, test_corrida0 casos nuevos) · forense/notas/ · forense/no-corrido.tsv · 0-bis · cascada. EN PARALELO: MOTOR-SEMANTICA (milpa — cero intersección), F5-RECAPTURA (caja) y, si ya fusionó, DUELO-CALC espera a nadie — pero si DUELO-CALC corre a la vez, NO toques rutas de run/verify más allá de la comparación listada. «Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.»

CONTADOR: no, y se dice. LO QUE NO HACE: no toca adq_doctor/adquiere_cron (hermano 1/5) · no reabre las 26 filas sanas · no construye seguimiento semántico de sucesoras · no indexa nada sin el D-14 contestado. SUCESORES: el primer ciclo de trámite post-H4 (debe encontrar la candidata que hoy se pierde) · la decisión de mesa sobre la fecha indeterminada (viaja de 1/5). CIERRE · Cascada + ## NO-CORRIDO / RESERVAS + ## CONSUMIDO con el PR.

## NO-CORRIDO / RESERVAS

- **qué**: SUCESORES declarados por el encargo, «el primer ciclo de trámite
  post-H4 (debe encontrar la candidata que hoy se pierde)».
  **por qué**: `NO-VERIFICABLE-AQUÍ` — la reparación de H4 está probada
  contra fixtures (seis casos nuevos en `tests/test_digesto_candidatas.py`,
  dos de ellos reproduciendo el defecto exacto en rojo antes de reparar:
  `t_h4_primera_mencion_excluida_segunda_valida` y
  `t_h4_id_prefijo_de_otro_no_colisiona`), pero una demostración en
  PRODUCCIÓN de que un ciclo real de `/tramite` encuentra hoy una candidata
  que antes se perdía exige que ese ciclo corra sobre el árbol real
  después de este merge — no algo que esta sesión pueda observar antes de
  fusionar.
  **impacto**: la reparación de H4 no tiene todavía un caso de producción
  confirmado; queda probada sólo por fixture.
  **sucesor**: el primer ciclo de `/tramite` que corra después de este PR
  — mesa/trámite observa si el digesto trae una candidata nueva que el
  código viejo hubiera perdido.

- **qué**: P3, «la REPARACIÓN (indexar DBF/ENIF)».
  **por qué**: `PARO-ENTORNO` — gate D-14 respondido NO en
  `forense/notas/2026-09-10-nc-0123-d14.md`: la reparación real exige leer
  FD/microdato reales (`pyreadstat`/`dbfread`/`openpyxl`) contra
  `data/raw` montado, ausente en NUBE (`python3 tools/entorno.py`:
  `data/raw` NO montado, `numpy`/`pandas`/`pyreadstat` `AUSENTE`). Además,
  la medición ampliada (102/116 instrumentos, no sólo ENIF) hace que
  "indexar DBF/ENIF" sea sólo una fracción del hallazgo real, medido por
  comando en la misma nota.
  **impacto**: 102 de 116 instrumentos del índice de reactivos (241591
  filas de universo) siguen sin texto buscable; sólo `variable_id` los
  alcanza. Declarado en la cabecera de ambos TSV
  (`data/inventario-reactivos-v1_2.tsv`/`-ext-v1_0.tsv`), así que ningún
  negativo futuro puede derivarse fuera de esa cobertura (A.15).
  **sucesor**: `NC-0136` (`ABIERTA`) — acto de CAJA con `tools/` en su
  perímetro, corpus montado y `pyreadstat`/`dbfread` instalados.

- **qué**: SUCESORES declarados por el encargo, «la decisión de mesa sobre
  la fecha indeterminada (viaja de 1/5)».
  **por qué**: `FUERA-DE-PERÍMETRO` — pertenece a `tools/adq_doctor.py`
  (H2 de `ACTO GEN2-ADQ-CONTRATO-FIX`), fuera del perímetro de este acto
  (que sólo toca `tools/digesto_tramite.py` y la comparación de identidad
  de `tools/corrida0.py`).
  **impacto**: ninguno nuevo — ya viajaba como `DECISIÓN-DE-MESA-PENDIENTE`
  desde `ACTO GEN2-ADQ-CONTRATO-FIX`.
  **sucesor**: mesa — carga hacia el siguiente despacho de la secuencia de
  5 (3/5).

## CONSUMIDO

Ejecutado por [PR #672](https://github.com/Josanoforo/Modelado-Mexicano/pull/672), 10/sep/2026, NUBE, Opus declarado/Sonnet 5 real.

P0 ejecutada (dos contraejemplos congelados en rojo, confirmados fallando
contra el código viejo, antes de reparar). P1 ejecutada (H4:
`_busca_candidatas_fila_k` recorre todas las apariciones como token
completo, exclusiones por aparición, dedup, archivo ilegible declarado,
enlace explícito por línea; seis casos nuevos en
`tests/test_digesto_candidatas.py`). P2 ejecutada (H6:
`_evidencia_vigente` ya no trata el vacío como comodín — `IDENTIDAD-INCOMPLETA`
explícita, `SIN-INSUMOS-DECLARADO` sigue comparando normal; caso nuevo en
`tests/test_corrida0.py`). P3 ejecutada por declaración (gate D-14
contestado NO por ENTORNO en `forense/notas/2026-09-10-nc-0123-d14.md`;
`NC-0123` → `CERRADA`; `NC-0136` nueva con el hallazgo ampliado, 102/116
instrumentos). `ADR-445`. `tests/check.py --baseline` VERDE, sin FAIL
nuevo.
