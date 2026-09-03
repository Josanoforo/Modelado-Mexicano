# ENCARGO ENLACE-2 · adjudicación de las 68 SI_O_REFERENCIADO y destino de las 19 INDEXADO-NO-DESCARGADO

- **SHA de redacción:** `84b2acf` (`origin/main`, post-#228) — el propio documento lo declara en su encabezado y se verificó por comando contra el clon de esta sesión antes de arrancar.
- **Entorno asignado:** «caja o nube con corpus» (§4, fila 6 de la tabla de lanzamiento) · **SIN red** — declarado por el propio encargo, sonda saltada. Ejecutado en esta ocasión en la CAJA (Ubuntu/WSL local) con el corpus montado por symlink, que es lo que ENLACE-1 Commit 1 no tuvo.
- **Estado:** CONSUMIDO por PR de ACTO ENLACE-2 — ejecutado en `forense/notas/2026-08-14-enlace2-clase-limbo.md` (Commit 1: política congelada) y `forense/notas/2026-08-14-enlace2-68-mas-19.md` (Commits 2-3: adjudicación de las 68, corrida de la vía, destino de las 19). Contador movido: capa2 `SI` 43 → 51.
- **Concurrencia declarada por el propio encargo:** «serializa con nadie: `relaciones.tsv` es solo suyo esta ola». SANEA-MAPEO, el otro encargo de F-B, declara explícitamente que **NO** toca `relaciones.tsv`.

## Bloque VERIFICACIÓN DE EXISTENCIA (A.8, Parte 2 — contestado por quien ejecuta)

- **Estructura — qué tablas gobiernan este dominio, derivado de `data/INFRAESTRUCTURA-v1_0.md` y del árbol, no de memoria:** `data/curacion-registro/relaciones.tsv` (el registro de demanda: 197 filas × 19 columnas, capa1-capa4) es la tabla gobernante del enlace; `data/curacion-registro/evidencias.tsv` es su tabla hermana a nivel de evidencia (misma llave `relacion_id`); `data/manifiesto.yaml` (631 entradas) es el registro de payloads; `data/abrir4-variables-2026-08-08.tsv` es el puente variable↔`id_manifiesto` del barrido ABRIR-4; `data/inventarios/alias-fuentes.yaml` (128 canónicos) resuelve nombres de fuente. **Ninguna tabla nueva se crea por este acto.**
- **Contenido — qué hay ya escrito sobre lo que el encargo pide:** la clase-limbo la definió y la midió ACTO V2 (`forense/notas/2026-08-13-v2-via-capa2.md` §1-§2); el mecanismo de asignación lo probó ENLACE-1 sobre 21 filas (`forense/notas/2026-08-13-enlace1-commit1-reglas-mapeo.md`); la vía existe y está parchada (ADR-73). **Este encargo no reabre nada de eso: lo consume.**
- **Cobertura retroactiva:** las 68 filas nunca han sido adjudicadas una a una — es el hueco H4 que el propio documento mide. Las 19 `INDEXADO-NO-DESCARGADO` (hueco H3) tampoco tienen dueño. Verificado que **no existe** ninguna nota previa de ENLACE-2 en `forense/notas/` antes de este acto.

## Nota de archivo

El documento de dirección vive fuera del repo (lo subió el usuario a su carpeta de descargas). Per la convención de este directorio —*«Si el encargo necesita un texto que vive fuera del repo, ese texto va pegado inline dentro del propio encargo»*— se pega **íntegro y verbatim** abajo: no solo §4.B, sino el documento completo, porque §1 (la tubería), §2 (la matriz de huecos H3/H4) y §3 (el plan multifase) son el contexto que fija el alcance del encargo y sin ellos la auditoría posterior no puede reconstruir por qué el acto hizo lo que hizo.

**sha256 del documento pegado:** `46b1823e1357d8ddf647705a328b66c66904e41bf885edd1e87aada1cb82e7ab` (15 974 bytes, 97 líneas) — para que quien audite después pueda confirmar que esto es lo que se lanzó y no una reescritura.

---

# Texto completo del documento de dirección, verbatim

---

# AUDITORÍA A-Z DEL PROGRAMA + INFRAESTRUCTURA DEL SIMULADOR + PLAN MULTIFASE
### 14/ago/2026 · verificado por dirección contra clon propio: `origin/main = 84b2acf` (post-#228) · **cero cifras heredadas: cada número de este documento salió de un comando corrido en esta sesión sobre ese árbol** · ADR máx: 80 · suite base `3d0d1e5`

---

## §1 · LA TUBERÍA COMPLETA, ETAPA POR ETAPA — números de hoy y hueco de cada etapa

**E1 · DEMANDA.** 33 necesidades (`necesidad-objeto-modelo.tsv`, N1-N33) → **197 relaciones** → **75 fuentes canónicas**. Íntegra y estable. Sin hueco.

**E2 · FUENTES Y PUERTAS.** Cola de adquisición: 54 fuentes con palanca. Puntero de puertas: ~104 filas + regla de precedencia real-vs-gap (#208). Acceso medido por sondeo (#205, `acceso-puertas`). El sondeo de las 27 `CANDIDATA-A-SONDEO` **ya corrió** (#228, SONDEO-COMPLETO per ADR-80, las 17 Hito-D primero). **Huecos: H1** (el crosswalk 7/1/67 es snapshot pre-adquisiciones — CSES/GPS/ISSP/ENSAFI/ENFIH ya tienen puerta y el crosswalk no lo sabe) y **H10** (los veredictos del sondeo-27 viven en su TSV y nadie los ha consumido hacia puertas/cola).

**E3 · PAYLOADS.** Manifiesto: **631** entradas (554 → 631: Lote-2 aterrizó, ISSP 16, Lote-3 sumó **53 archivos de descargas manuales**, splits). Corpus compartido verificado por los actos (patrón PR#77 aplicado). **Consumo trazable medido por primera vez: 22/550 = 4.0%** (ACTO CEP, entrada 6 — hash exacto 2 + ruta exacta 20). `SIN-DEMANDA` real: **538/550 = 97.8%** (medido, no el 58% estimado). **Hueco H2:** la entrada 6 tiene su medición COMPLETA y está `ABIERTA` esperando únicamente el cierre formal de mesa — y su §advertencia es seria: podar por `SIN-DEMANDA` borraría insumos de veredictos sellados.

**E4 · APERTURAS.** Base del censo de explotación: 8/550 = 1.45% con apertura registrada; encima: **+94 diccionarios** (reapertura 52A/54, 208/208 `NO-ENCONTRADO`), 14 celdas ISSP, 28 ENASEM. La capa4 de relaciones, poblada hoy: 3 `EXISTE-SATISFACE` · 8 `SATISFACE-UMBRAL-DOCUMENTAL` · **19 `INDEXADO-NO-DESCARGADO`** · 14+1 `NO-ENCONTRADO` · 9 `EXISTE-NO-SATISFACE` · 6 `MAPEADO-NO-SATISFACE` · 5 `CANDIDATA` · 2 `ABIERTO-SIN-MAPEO` · 68 `SIN_APERTURA_EXPLICITA` · 54 vacías (las NO_REF). **Hueco H3:** las 19 `INDEXADO-NO-DESCARGADO` son celdas donde el codebook indexa la variable pero el dato no está bajado/abierto — nadie las tiene asignadas.

**E5 · ENLACE (capa2/3).** `SI` **43/197** con capa3 `EXISTE;COINCIDE;INTEGRO` 43/43 (reconciliado). `NO_REFERENCIADO` 86. **Hueco H4 — el mayor de la tubería de datos:** los **68 `SI_O_REFERENCIADO`/`SI_O_PARCIAL`** son la clase-limbo que V2 definió ("referenciada en trabajo analítico real, no confirmada") y **ningún acto los ha adjudicado uno a uno** a SI o NO. Es más de un tercio de las relaciones. La vía parchada (ADR-73) + el diagnóstico existen; falta el acto (ENLACE-2, nunca lanzado).

**E6 · PRODUCCIÓN.** 11 filas, **11/11 `CALCULO_REPRODUCIBLE`**, 3 expedientes sellados, pipeline (`prepare→produce→integrate`) probado dos veces con reproducción byte a byte. **Hueco H6:** PROD-P638 sin correr — la fila 12, el `LISTO` de la celda de obligación y la oncena condicional cuelgan de él.

**E7 · PROCEDENCIA / CONDICIONALES.** 17 entradas con clase: 9 `MEDIDO·PARCIAL(x)` + 5 `MEDIDO·*` + **1 `MEDIDO·NACIONAL`** (la décima, PROC-10-bis) + 1 `GATE·ID-X` (G3, compuerta inalcanzable verificada — no es hueco, es veredicto) + 1 `PENDIENTE` (confianza_institucional genérica, medición condicional no corrida — pendiente legítimo con dueño futuro). **Contador: `10 de 15`** ✓ en README+modelo, T19b/T19c verdes.

**E8 · COEFICIENTES / LLAVES / RECÁLCULO.** Censo v1.1: **3 RUTA-A · 5 RUTA-C · 1 RUTA-I · 6 SIN-RUTA** (universo de llaves 9/9 declarado). Coeficientes medidos: **0/15** — y `modelo:396` sella que **los 15 β son `ASIGNADO` por razón estructural**, no por descuido: medirlos es exactamente lo que las RUTA-C/llaves/celdas-D existen para cambiar. Llaves: **1/2**. Recálculo: **0/1/2/4 CERRADAS · 3/5/6 ABIERTAS** — la 3 (7 veredictos D) con gate cumplido y acto nombrado (E3-TRIAGE, ADR-79(d)); la 5 gateada por el sello del motor (E5, ADR-79(c), ajena); la 6 con medición completa esperando cierre (H2).

**E9 · MODELO.** `4 de 144` congelado desde 31/jul (la tabla de `modelo:625-632` lo re-expresa: 144 → **54 enumerables** (15 β + 39 reglas), 4 `MEDIDO`); 22 g.l. del ajuste = **7+15** (`modelo:260,628`); condicionales `10 de 15`. La invarianza ENCUCI↔ENBIARE **corrió** (#226, diseño sellado ADR-76(d), 2 ítems, bootstrap, dicotomización cero). **Hueco H5:** su salida NO se ha adjudicado — la celda de radio sigue con clase `PROXY_PARCIAL` de ADR-67(a); la firma que la resuelve es de mesa con el resultado enfrente, y no está dada.

**E10 · EL SIMULADOR.** El dictamen honesto que pediste, sin maquillaje:
- **Lo que EXISTE y corre (A→Y de registro):** el contrato celda-D v0.4 sellado (ADR-68/71d) · 3 celdas-D (las 3 semillas de ADR-68: radio, familismo.actitud, obligación) · el pipeline de producción completo y probado · `via_capa2` parchada · svystat · la suite (T15/T19b-c/…) · `procedencia.yaml` como contrato de insumos (con π(x) anclada: `tasa_informalidad {v:0.31, src:ENOE, sae:true}` y tick trimestral ENOE, `milpa-spec:269`) · los **7 umbrales go/no-go sellados** (ADR-68, `gobernanza:906-916`) · el plan de fases escrito (`milpa-plan` Fase 0 fundación → Fase 1 rebanada vertical "la que decide todo" → Fases 2-3) · el pre-registro de falsación de la matriz completo (§6, 4 filas + precedencia).
- **Lo que NO existe, y por diseño sellado, no por hueco de descuido:** **cero código ejecutable** (`milpa/` = 6 documentos, `find` de .py = vacío, cero `simula/campo_medio` en tools) · **catálogo de momentos inexistente** (M4 lo CONSTITUYE) · **M1 sin sellar** — y ADR-68(g) es explícito: la interfaz queda declarada SIN decidir M1. La secuencia es correcta; **el hueco real (H7) es que sus dos precondiciones — MOTOR-1 y RONDA-M — SIGUEN SIN LANZARSE** (cero notas, verificado). El simulador no está atorado en ingeniería: está atorado en dos sesiones que nadie ha abierto.
- **Veredicto de infraestructura A-Z:** la mitad de REGISTRO (demanda→procedencia) está diseñada, instrumentada, testeada y CORRIENDO de la A a la Z — con los cuatro huecos de datos H1/H3/H4/H6, todos con encargo abajo. La mitad de EJECUCIÓN (motor→momentos→calibración→go/no-go) está **diseñada de la A a la Z en papel sellado** (spec, plan, umbrales, falsación, contrato de insumos) y **sin una línea de código** — gateada en M1 a propósito. El plan de abajo hace ambas cosas a la vez: cierra los huecos de datos EN PARALELO con destrabar M1, y deja el primer encargo de implementación (MOTOR-3/E0) escrito con sus ranuras.

---

## §2 · MATRIZ DE HUECOS — cada uno con evidencia y su encargo

| ID | Hueco | Evidencia (comando de hoy) | Lo cierra |
|---|---|---|---|
| H1 | Crosswalk demanda↔puertas desactualizado | 7/1/67 vs puertas ~104 con CSES/GPS/ISSP/ENSAFI/ENFIH ya reales | **SANEA-MAPEO** (§4.B) |
| H2 | Entrada 6 medida y sin cerrar | registro fila 6 `ABIERTA` + 22/550 | **CIERRE-E6** (§4.A, mesa) |
| H3 | 19 celdas `INDEXADO-NO-DESCARGADO` sin dueño | capa4 count | **ENLACE-2** las clasifica; las descargables van a cola |
| H4 | 68 relaciones en clase-limbo `SI_O_REFERENCIADO` | capa2 count | **ENLACE-2** (§4.B) |
| H5 | Invarianza corrida sin adjudicación (celda radio `PROXY_PARCIAL`) | celda yaml + ADR-67(a) vigente | **ADJUDICA-RADIO** (§4.A, mesa) |
| H6 | PROD-P638 sin correr (oncena + fila 12) | cero nota; celda `PENDIENTE` | **PROD-P638** (vigente, gate ya satisfecho) |
| H7 | MOTOR-1 y RONDA-M sin lanzar → M1 sin cascada ni juicio | cero notas | **lanzarlos HOY** (§4.C) |
| H8 | Cero código del simulador + catálogo de momentos | `find` vacío | **MOTOR-3/E0** (§4.C, molde completo con ranuras-M1) |
| H9 | Entradas 3 y 5 del recálculo abiertas | registro | E3-TRIAGE (nombrado ADR-79(d)) · E5 (post-sello, ajeno) |
| H10 | Sondeo-27 sin consumir hacia puertas/cola | TSV del sondeo intacto río abajo | **SANEA-MAPEO** (§4.B) |
| H11 | A.9: instrucciones v2.8 en repo, proyecto atrás | `ls` repo + listado del proyecto | tú, un minuto |

---

## §3 · PLAN MULTIFASE — cuatro fases, todo lo paralelo declarado

```
F-A · MESA HOY (repo-only, dos micro-actos + dos botones ya dados)
F-B · SANEAR LA TUBERÍA (∥ entre sí y con F-C; cierran H1/H3/H4/H10)
F-C · DESTRABAR Y CONSTRUIR EL MOTOR (H7 hoy; H8 al sellar M1)
F-D · RECÁLCULO Y CENSO (H9; carriles ya nombrados por ADR-79)
```

### F-A · Dos micro-encargos de mesa (un amanuense, una sesión, hoy)

**ENCARGO ADJUDICA-RADIO (H5).** Nube, repo-only. ARRANQUE íntegro (v2.8). **Premisa 1 y única sustantiva: leer COMPLETA la salida del acto de invarianza** (`forense/notas/2026-08-13-invarianza-encuci-enbiare.md` — el veredicto CONFIGURAL/MÉTRICA impreso por su script, con IC y réplicas; este encargo NO lo transcribe a propósito: quien firma lo lee del original, no de un resumen). Ranura de firma: `[MESA: con veredicto X, la clase PROXY_PARCIAL de ADR-67(a) se resuelve como ___ / se mantiene con razón ___]`. Ejecución: enmienda in-situ sobre ADR-67(a) (patrón ADR-75), campos de la celda radio actualizados según la firma, cascada de estado, suite. Perímetro: `gobernanza` (enmienda in situ) · la celda · `estado-programa` · nota · A.3 · hallazgos. **Contador:** la primera celda-D con su comparación de estimadores ADJUDICADA — el insumo que el contrato celda-D existe para producir.

**ENCARGO CIERRE-E6 (H2).** Mismo molde. Premisa: la medición de ACTO CEP (22/550, dos vías) leída del registro fila 6 + su nota. Ranura: `[MESA: la entrada 6 cierra como RECALCULADO — ___ ; y la advertencia sobre poda por SIN-DEMANDA se sella como regla / se registra sin sellar]`. Ejecución: la fila del registro + propagación mínima. **Contador:** recálculo 4/6 → 5/6 cerradas.

### F-B · Dos encargos de saneamiento (∥, sin red, worktrees propios)

**ENCARGO SANEA-MAPEO (H1+H10).** Repo-only. Premisas-script: re-derivar el estado del puntero de puertas y del TSV del sondeo-27 (filas y clasificaciones — no heredar "27/17"). Commit 1: método congelado — (a) re-derivación del crosswalk contra el puntero VIGENTE (mismas reglas de evidencia de MAP-B, citadas; cada fila que cambia lleva su evidencia nueva); (b) consumo del sondeo: cada veredicto del TSV de #228 aplicado a su fila de puerta (clasificación A.4 con universo) y, donde el veredicto habilite adquisición, la fila propuesta para la cola (PROPUESTA — la palanca/firma de lote es de mesa). Commit 2: los dos TSV nuevos con fecha propia (regla del puntero: snapshot superset) + embudo contado. **NO toca** `relaciones.tsv` (Carril ENLACE-2) ni baja nada. **Contador:** crosswalk al día + N veredictos del sondeo convertidos en filas consultables.

**ENCARGO ENLACE-2 (H4+H3) — el grande de la tubería.** Sin red, corpus montado. Premisas: `via_capa2.py` corrida en lectura (el diagnóstico VIGENTE — no heredar 97), el conteo 68 re-derivado, la nota de ENLACE-1 y el parche ADR-73 leídos. Commit 1 congelado: (a) la política de adjudicación de los 68, derivada del precedente de V2 §1 (la clase existe porque "referenciada en trabajo analítico ≠ confirmada"): por fila, la referencia analítica se abre y se verifica — si el objeto citado existe en el payload/expediente citado ⇒ `SI` con `id_manifiesto`; si no ⇒ `NO_REFERENCIADO` con la razón; **indecidible queda indecidible con nota** — cero adivinanza; (b) el tratamiento de las 19 `INDEXADO-NO-DESCARGADO`: por celda, qué payload falta, si está en el manifiesto (⇒ es apertura pendiente, va a lista-de-apertura) o no (⇒ va como PROPUESTA a la cola); (c) la política de pares [RANURA — mesa la firmó PROPUESTA en el diseño previo; si sigue sin firma, este acto solo enlaza los sin-par y lo declara]. Commit 2: asignaciones → vía en lectura (diffs = exactamente lo asignado) → `--escribe` → suite. **Contador esperado: capa2 `SI` 43 → N** (el N lo produce la vía) — el segundo gran movimiento de adquisición del programa.

### F-C · El motor: hoy y después del sello

**HOY (H7):** lanzar **MOTOR-1** (cuerpo autocontenido §3 del doc del 14/ago, YA archivado en el repo vía #224 — el lanzador solo sube los 5 archivos con hash) y **RONDA-M** (Opus, sesión nueva; encargo archivado ídem). **PROD-P638** (H6) a la caja — su gate quedó satisfecho al fusionar #227 (la clase `MEDIDO·NACIONAL` existe). Tres sesiones, cero dependencias entre sí.

**AL SELLAR M1 (MOTOR-2, mesa — con cascada + veredicto de ronda):** el aviso a E5 con su A.3, el banner ADR-62 resuelto — y se lanza:

**ENCARGO MOTOR-3 · E0 — la primera implementación (molde completo; las ranuras se llenan del ADR de M1, señaladas una a una).** Caja o nube según `milpa-plan` Fase 0; worktree propio; **la ventana ADR-70(d) queda CERRADA al arrancar E0 — este acto NO toca `tools/curador_registro/`, consume**. Perímetro: `milpa/src/` (nuevo) · `milpa/catalogo-momentos-v0_1.md` + su tabla · `tests/` solo tests NUEVOS del motor · nota/A.3/hallazgos. Commit 1 — pre-registro: (a) **el catálogo de momentos, constituido** (M4): momentos del piloto finanzas-del-hogar enumerados desde el libro de demanda `[RANURA M5: derivado del libro como fuente única / listas con cruce declarado — según firma]`, **con roles AJUSTE/HOLDOUT sellados AQUÍ, antes de escanear nada** — la circularidad que M4 existe para impedir; (b) el contrato de entrada: `procedencia.yaml` es LA fuente de θ/valores — el código lee clases y respeta `MEDIDO·NACIONAL` sin segmentar, `ASIGNADO` con su banda, `GATE·ID` como exclusión; (c) π(x): cortes iniciales `[RANURA M2: los cortes que mesa selle]` materializados desde ENOE (la fuente que la spec ancla), con el acto de datos que los produce nombrado si el payload falta; (d) `G1b` `[RANURA M3: campo medio declarado HIPÓTESIS / alternativa firmada]`; (e) la escala de falsación de matriz §6 copiada verbatim como la del acto, con su precedencia; (f) los **7 umbrales de ADR-68 transcritos como asserts ejecutables** — el go/no-go de Fase 1 se decide por comando, no por prosa. Commit 2: la rebanada mínima que compila y corre las 3 celdas-semilla contra momentos AJUSTE, holdout intocado, salida reproducible con hash. **Gate de semana 1 de ADR-68 vigente. Contador: el primero de la mitad de ejecución — "momentos HOLDOUT reproducidos: 0 de M" nace y empieza a contar.**

### F-D · Recálculo y censo (carriles ya nombrados — punteros, no re-emisión)
E3-TRIAGE (entrada 3; ADR-79(d), gate cumplido) · E5 (entrada 5; espera el número del ADR de M1, con su A.3) · RUTA-SELLO · FUSION-PUERTAS · A10-ESTAMPA — los cinco con rótulo propio en ADR-79; se lanzan cuando la caja/nube respire, ninguno gatea al motor.

---

## §4 · TABLA DE LANZAMIENTO — lo que sale HOY, en paralelo

| Sesión | Acto | Entorno |
|---|---|---|
| 1 | MOTOR-1 (5 archivos con hash) | nube |
| 2 | RONDA-M | **Opus**, nueva |
| 3 | PROD-P638 | caja + corpus |
| 4 | ADJUDICA-RADIO + CIERRE-E6 (mismo amanuense, secuencial) | nube |
| 5 | SANEA-MAPEO | nube |
| 6 | ENLACE-2 | caja o nube con corpus (serializa con nadie: `relaciones.tsv` es solo suyo esta ola) |
| tú | H11 (v2.8 al proyecto) + firmas de las ranuras A cuando lleguen | — |

**Contadores que esta ola mueve, en orden esperado:** condicionales `10→11 de 15` (PROD-P638) · producciones `11→12` · capa2 `43→N` (ENLACE-2) · recálculo `4→5/6 cerradas` (CIERRE-E6) · la primera celda-D ADJUDICADA (radio) · y, al sellar M1, nace el contador de la mitad que hoy no existe. **Contadores movidos por esta auditoría: 0 — es dirección, y lo dice.**

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `git grep -Fl -- "2026-08-14-ENLACE-2-adjudicacion-68-y-19.md"` (excluyendo forense/digesto/) cita nota(s) de cierre: forense/notas/2026-08-14-enlace2-clase-limbo.md, forense/notas/2026-08-14-tablero-firmas-commit3.md, forense/notas/2026-08-26-e10-r21-adjudica-cierre.md. Encargo pre-ADR-por-archivo (anterior al 18/ago/2026): la evidencia de ejecución vive en la nota de cierre, no en canon/gobernanza-v1_15.md. Marca ausente era defecto de trámite retroactivo, resuelto por esta auditoría.
