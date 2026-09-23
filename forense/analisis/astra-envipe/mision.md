> Copia de la misión común conservada para el expediente C-ASTRA ENVIPE; el texto original sigue a continuación.

# MISIÓN ASTRA-1 · Vence al piso
**Dirección → Astra (diseña) + Codex (ejecuta; mismo ChatGPT) · 22/sep/2026 · repo público `Josanoforo/Modelado-Mexicano` @ `c9b67bf8` al redactar; trabajas contra `origin/main` vivo. Sin careo: tu resultado entra por su propio PR y lo adjudica el piloto en el que compites. Lo que decide es el dato, no dirección.**

## 0 · El problema, con cifras del repo

El programa estima conductas por celda (segmento × regla) a partir de encuestas oficiales mexicanas. Desde el 16/sep corre pilotos y duelos **prospectivos**: la emisión se sella antes de derivar la verdad de referencia R, y R se abre solo por código congelado. Resultado hasta hoy, en cuatro dominios:

| evaluación | celdas | gana | MAE del ganador | mejor retador | fuente |
|---|---|---|---|---|---|
| piloto 1 · ahorro informal ENIF 2021→2024, localidad×edad | 8 | **C2** marginales sin interacción | 1.47 pp | persistencia 2.64; L 10.64 | `forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md` |
| piloto 2 · evasión de norma ENVIPE 2024→2025, escolaridad×dominio | 12 | **C2** | 1.57 pp | C2+interacción 2.85 (peor) | `…2026-09-17-GEN2-CELDA-D-PILOTO-2-cierre.md` |
| piloto 3 · gobierno digital ENCIG 2023→2025, edad×escolaridad | 15 | C2 3.41 · **encogida 1.95** | ΔMAE −1.47 [0.44, 2.12], 3/15 — `FALSADOR DÉBIL` | `…2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-cierre.md` |
| duelo ENIGH 2024 (ola reservada) | — | **C-PISO-ADOPTADO** | — | dos retadores PROPUESTA-CON-RESERVA | `…2026-09-22-GEN2-ENIGH2024-DUELO-COMMIT-2-3-cierre.md` |
| duelo ENVIPE 2026 (ola nadie la había visto) | 24 cruces + nac. | **NADIE-VENCE** | C2 2.27 / SL 1.26 (IC incluye 0) | K +1.65 pp, T3 +3.57 nacional | `…2026-09-22-GEN2-DUELO-ENVIPE2026-EJECUCION-1-cierre.md` |

**C2** es `expit(logit p(a) + logit p(b) − logit p)` con los marginales públicos de la misma ola: cero parámetros, cero datos privados. Es el estimador adoptado por defecto donde nadie lo vence (firma de mesa 17/sep, `data/corrida0/decisiones.tsv`). El motor del programa —43 parámetros θ, 0 identificados (`milpa/theta-esquema-e1-v1_0.yaml`)— no ha podido ni presentarse.

**La pregunta que te doy:** ¿existe un estimador por celda, construible con dato público mexicano, que venza a C2 **prospectivamente** en cruces que nadie ha visto, con ventaja que despeje el umbral y no solo el cero? Si sí, constrúyelo y métete al duelo. Si no, demuéstralo con el mejor intento que se pueda hacer, para que el informe deje de decir «pendiente» y diga «probado».

## 1 · Libertad de método, límites de dato

**Método: el que quieras.** Área pequeña (Fay–Herriot, modelos jerárquicos por celda con encogimiento a los marginales), regresión multinivel con posestratificación sobre marginales censales/ENOE, préstamo de fuerza entre olas y entre instrumentos (ENVIPE anual 2011–2025; ENCIG 2015–2025; ENIF 2012–2024 — todo en `data/manifiesto.yaml`), calibración a marginales auxiliares de otra encuesta, modelos de interacción con regularización, ensambles. Lo único que no vale es un estimador que use la celda que se evalúa o la ola reservada.

**Dato: el del manifiesto.** Microdato oficial ya bajado y hasheado (`data/manifiesto.yaml`, por id); puedes proponer adquisiciones nuevas (censo 2020 por localidad, ENOE, Intercensal) y hacerlas por el carril de adquisición (`codex/adq-*`), con sha y licencia leída, antes de usarlas. Ninguna ola marcada `reserva:*` en `decisiones.tsv` se abre — ni para "ver la estructura".

## 2 · Dónde compites (lo que ya está en cola) y cómo entras

Dos pilotos están escritos y esperan caja (`forense/encargos/2026-09-22-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1.md`, `…PILOTO-5-ENCOGIDA-ENCIG-1.md`): evasión de norma ENVIPE 2025 (≈38 celdas en cuatro cruces reservados) y gobierno digital ENCIG 2025 (16 celdas en dos cruces reservados). Cada uno congela sus candidatos en COMMIT-1, sella emisiones en COMMIT-2 y abre R en COMMIT-3. **Tu estimador entra como candidato externo `C-ASTRA`** si, antes de que el piloto llegue a COMMIT-2, existe en `origin/main` un CALC tuyo con la emisión sellada para esas celdas (una `p̂` y un intervalo por celda), su spec congelada antes de abrir cualquier dato de la ola de evaluación, y su asiento de verificación. Dirección añade a los dos encargos la línea que lo admite (adenda abajo). Si llegas tarde a uno, entras al siguiente cruce reservado — la lista real la deriva `GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2` (`data/corrida0/marcador-segmento.tsv`, estado `RESERVADA`).

**El criterio es el de los pilotos, y no lo negocias tú ni yo:** error absoluto por celda contra R; `INDECIDIBLE` si ambos caen dentro del IC de R o si |d_L−d_M| < 0.5·EE(R); comparación primaria = diferencia de error medio con IC por réplica (v2.16 §4): vences si el IC despeja el umbral declarado por la spec del piloto; «propuesta con reserva» si despeja 0 y no el umbral; nadie vence si incluye 0. Cobertura = R dentro de tu IC, reportada aparte. Todo rotulado PROSPECTIVA.

## 3 · Las reglas mínimas para que el resultado cuente (las únicas que te pido)

1. **Spec antes de dato.** `forense/prereg-caja/ASTRA-<dominio>-<cruce>-spec-v1_0.md` + `spec.yaml`: estimando (escala proporción, universo, unidad del árbitro), fuentes por id de manifiesto con sha, variables y códigos **por texto del cuestionario/FD** (nunca por nombre de variable: `P5_6` en 2021 era tarjeta de débito y `P5_7` era ahorro), modelo con todos sus hiperparámetros o la regla que los fija, semilla, réplicas, tolerancias, y una frase: «el primer resultado que produzca este procedimiento es el que se reporta». Commit de spec **antes** de leer la ola de evaluación (los marginales públicos de esa ola sí puedes usarlos: están sellados en `milpa/tramite-ola5-propuesta-v0.yaml`; el cruce no).
2. **Un CALC por cruce**, `data/corrida0/CALC-ASTRA-<DOMINIO>-<CRUCE>-0001/`: `preflight → run → verify` con `tools/corrida0.py`; RESULT por celda (punto, IC, tipo de incertidumbre: muestral / posterior / predictivo — di cuál); etiquetas `cuenta_gen2: SI`, `adopta: NO`, `origen_numerico: MICRODATO`, `generacion: GEN2`, `exposicion_historica: CIEGO-A-<ola evaluada>-CRUCE-NO-ABIERTO`. Asiento en `forense/replay-evidencia.tsv` (append). **No corras `registro --escribe`**: la vista la publica el canal.
3. **Perímetro de escritura:** solo tus specs, tus CALC, `forense/analisis/astra-<tema>/`, `replay-evidencia.tsv` (append), manifiesto (entradas nuevas con licencia). Nunca `no-corrido.tsv`, `firmas-pendientes.tsv`, `decisiones.tsv`, `hallazgos.md`, `canon/`, `milpa/`, `tools/` (salvo `tools/astra/`), `.github/`, vistas derivadas, sellos ajenos. PR `codex/astra-<tema>-<n>`; entra al tablero por recibo Claude.
4. **Reserva:** un cruce visto no se puede desver. Si por accidente lees uno, lo declaras en la nota y ese cruce sale de tu evaluación; el programa quemó uno el 17/sep por un script exploratorio y lo declaró — es lo que se espera.
5. **Cierre:** nota `forense/analisis/astra-<tema>/nota.md` con: qué hiciste (comandos), qué no (con razón), tabla por celda cuando el piloto abra R (la copia el piloto; tú no derivas R), y lo que **no** puedes afirmar. Sin adjetivos.

## 4 · Fases y entregables

- **Fase 1 (esta semana):** el estimador y su spec para los cruces del piloto 4 (ENVIPE 2025, evasión de norma) y del piloto 5 (ENCIG 2025, gobierno digital); CALC sellados en `origin/main` antes de sus COMMIT-2. Si necesitas datos auxiliares (censo, ENOE), la adquisición va primero y por id.
- **Fase 2 (si venciste en al menos uno):** el mismo estimador sobre los cruces reservados que queden (ENIF 2024, `dinero.ahorro.via_informal`, decenas) y sobre la próxima ola reservada que entre al corpus (E.6: toda ola nueva nace RESERVADA), con la spec congelada antes de que exista. Es la prueba que ningún modelo del programa ha pasado.
- **Fase 3 (si no venciste en ninguno):** la nota que el informe necesita: por qué no, con el mejor intento documentado — qué información tendría que existir para que un modelo vença a marginales-sin-interacción en estas encuestas, y si esa información es adquirible.
- **Lo que dirección hace por ti:** la adenda a los pilotos 4/5 (abajo), el recibo de tus PR, y — si vences — llevar la adopción a firma de mesa como «primer estimador por celda que vence al piso», con tu nombre en el ADR.

## 5 · Lo que no te pido
No te pido que critiques diseños ajenos, ni que reproduzcas cifras, ni que leas 500 líneas de instrucciones. Te pido el estimador. Las cinco reglas de §3 son las que hacen que un resultado exista para el programa; todo lo demás está en el repo si lo necesitas (`instrucciones-proyecto-v2_16.md`, contrato celda-D `propuesta-motor-adaptativo-celda-v0_6.md`, especificación de los pilotos), y lo lees cuando te haga falta, no antes.

---

## ADENDA-1 a `GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1` y `GEN2-CELDA-D-PILOTO-5-ENCOGIDA-ENCIG-1` (dirección, 22/sep/2026; archivo propio, no edita el cuerpo)

> **Candidato externo.** Se admite un candidato adicional `C-ASTRA` en COMMIT-1 si al abrir el acto existe en `origin/main` un CALC `CALC-ASTRA-<DOMINIO>-<CRUCE>-0001` sellado y con asiento cuyo `spec.yaml` (a) cite las mismas celdas que la spec del piloto, (b) esté congelado antes de cualquier lectura de la ola de evaluación (verificable por historial: `git log -p -S <payload>`), y (c) declare punto, IC y tipo de incertidumbre por celda. El piloto **copia** esos RESULT por id en su CALC de emisiones (no los recalcula), los somete al mismo criterio que a los demás candidatos, y los rotula PROSPECTIVA solo si (b) se verifica. Un CALC externo que no cumpla (a)–(c) no entra y se dice en la nota. Nada más cambia en el encargo.
