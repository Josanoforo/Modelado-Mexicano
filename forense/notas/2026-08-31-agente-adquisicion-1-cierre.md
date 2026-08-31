# Nota de cierre · `ACTO MAESTRA33-A1 · AGENTE-ADQUISICION-1`

31/ago/2026 · worktree `/home/pc0/mm-agente-adquisicion-1` · rama `acto/maestra33-a1-agente-adquisicion-1` · SHA de arranque `ae1346d` (`origin/main` al crear el worktree — 6 commits después del `6a12244` que el encargo declara, los seis de `PR #412`/`ACTO MAESTRA33-C1`, fuera de este perímetro). Encargo: `forense/encargos/2026-08-31-MAESTRA33-A1-AGENTE-ADQUISICION-1.md`. `COMPUERTA: ninguna de merge` — sin línea `GATED a X`, sin gate que verificar.

## §1 · ARRANQUE

| # | Punto | Comando | Resultado |
|---|---|---|---|
| 1 | REPO | `pwd`; `git log -1`; `git status` | `/home/pc0/mm-agente-adquisicion-1`, worktree nuevo creado sobre `origin/main` (el clon base `/home/pc0/Modelado-Mexicano` estaba parado en `acto/maestra32-e18-reglas-ola5-fase1`, 593+ commits atrás — no se usó). `git status`: limpio al arrancar. |
| 2 | SHA | `git rev-list --count 6a12244..HEAD` | `6` — los seis commits de `PR #412`/`ACTO MAESTRA33-C1`, fuera del perímetro de este acto (no tocan `data/cola-adquisicion*`, `data/manifiesto.yaml` ni `forense/firmas-pendientes.tsv`). No es PARO. |
| 3 | `data/raw` | `ls -la data/raw` | Ausente al arrancar (esperado, gitignorado). Enlazado: `ln -s /home/pc0/mm-corpus/raw data/raw`. **Nota de infraestructura no bloqueante:** el propio corpus compartido trae un symlink `raw -> /home/pc0/mm-corpus/raw` **dentro de sí mismo** (`ls -la /home/pc0/mm-corpus/raw`, fechado 12/ago) — un bucle de filesystem real, preexistente, fuera del perímetro de este acto. `find -L` recursivo sin `-maxdepth` sobre `data/raw` lo detecta y lo reporta como bucle en vez de fallar en silencio; cualquier búsqueda futura ahí debe acotar profundidad o excluir el nombre `raw`. |
| 4 | ENTORNO | `echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-<sin_variable>}"`; `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/`; `ls data/raw \| head -1` | `<sin_variable>` (CAJA, confirma A.2) · `200` · corpus compartido montado y no vacío (231 archivos examinados a profundidad 1, `find -L`). Las tres partes A.2 confirmadas: CAJA, red real, corpus presente. |
| 5 | ESPEJO | — | Ninguna cifra de este acto sale del espejo del proyecto; todas del clon de (1). |

## §2 · A.8 — la premisa del encargo, verificada contra el árbol de hoy, no heredada

El encargo cita "`data/cola-adquisicion-2026-08-12.tsv` (15 filas `EXISTE-NO-VERIFICADO`, `FP-17`)". Verificado directamente:

```
$ grep -c "EXISTE-NO-VERIFICADO" data/cola-adquisicion-2026-08-12.tsv
42
```

Ese `42` **no** son las 15 de `FP-17` — son coincidencias léxicas dentro de texto narrativo de otras columnas. Releyendo `FP-17` completa y su nota de ejecución (`forense/notas/2026-08-18-adquisicion-material-15-fuentes.md`):

> "**Cero `EXISTE-NO-VERIFICADO`.** De las 15: 6 `EXISTE-SATISFACE`, 7 `EXISTE-NO-SATISFACE`, 1 `NO OBTENIDO … EN 7 INTENTOS`, 1 `NO-ENCONTRADO`." (§4 de esa nota, `ACTO ADQ-15`, 18/ago/2026)

**Las 15 de `FP-17` ya fueron caminadas — dos veces.** `ACTO ADQ-15` (18/ago) las trabajó todas; su complemento `ACTO LOTE UBUNTU-ADQ-1` (19/ago, T3) retomó los 4 residuos que ADQ-15 no cerró (WB 6667, WB 870, LAOMS, ENAFIN) y además completó `SERIES_SPEI_CODI_BANXICO`, las olas 2019/2021 de `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS`, y **el `basededatossfd.zip` de IFT SFD que ADQ-15 no había conseguido en 11 intentos**. Ninguno de estos resultados del complemento se escribió de vuelta a las columnas `estado_adquisicion_ADQ15`/`estado_adquisicion_R74R75` de `data/cola-adquisicion-2026-08-12.tsv` — viven solo en la fila `FP-17` de `forense/firmas-pendientes.tsv`. Esa es la causa real del desfase que el encargo reporta: la tabla de 08-12 **nunca se actualizó** con el trabajo de LOTE-UBUNTU-ADQ-1, así que leerla directamente (en vez de `FP-17`) sugiere 15 filas pendientes que ya no lo están.

**Dos de las 15 nunca tuvieron fila propia** en ninguna de las 5 colas de agosto (`EXPERIMENTO_INFORMACION_ELECTORAL_2009` y `FINANZAS` — ADQ-15 §1 ya lo declaró: "3 no cruzan por `fuente_canonica`... trabajadas al final"). `data/cola-adquisicion-v1_0.tsv` las añade como filas nuevas (`EXPERIMENTO_INFORMACION_ELECTORAL_2009` → `OBTENIDO`, paquete JPAL ya en manifiesto; `FINANZAS` → `PENDIENTE`, identidad sin resolver, sin reintento en este acto por no haber información nueva que aportar al mismo sondeo agotado).

**Radio_confianza (E20-P1).** Localizado en `forense/notas/2026-08-31-cura-radio-cierre.md` §(d3) (re-emisión por `ACTO MAESTRA32-E20 · LOTE-NUBE-1 · P1`) y confirmado también como ítem (6), `ABIERTA`, en `FP-179`: el instrumento requerido es **WVS ola 7 México (2018)** — único con batería de confianza por círculos (`V102`-`V107`) y módulo de hogar en la misma muestra. Verificado 31/ago: 0 de 489 `payload_id` del inventario coinciden con `wvs`/`world`/`values`; ausente de `data/manifiesto.yaml`. Plegado en la fila `WVS` ya existente de `cola-adquisicion-2026-08-12.tsv` (palanca 3) con prioridad elevada, en vez de duplicarla.

## §3 · P1 — consolidación

`data/cola-adquisicion-v1_0.tsv`, 72 filas: 56 heredadas de `cola-adquisicion-2026-08-12.tsv` (las 54 originales + `EXPERIMENTO_INFORMACION_ELECTORAL_2009` + `FINANZAS`, corrigiendo el hueco de §2) + 16 candidatos nuevos absorbidos de los cuatro `cola-ext-*-2026-08-06.tsv` sin fila propia en la tabla de 08-12. Las 5 tablas de agosto **no se borran** — quedan citadas como puntero (columna `origen`) en cada fila que absorben.

`estado_A4A5` se re-derivó fila por fila contra el árbol de hoy (`data/manifiesto.yaml`, `forense/firmas-pendientes.tsv`, notas de cierre citadas), no copiado de las columnas `ADQ15`/`R74R75` sin verificar — esas columnas, como muestra §2, estaban incompletas. Regla de mapeo declarada (no una quinta categoría): un payload adquirido pero analíticamente insuficiente para la pregunta original (`EXISTE-NO-SATISFACE`) cuenta `OBTENIDO` en esta tabla — la suficiencia analítica es pregunta fuera del alcance de una tabla de *adquisición*.

**Conteo al cerrar P1** (antes de la caminata de P3): 21 `OBTENIDO` · 44 `PENDIENTE` · 6 `NO-ACCESIBLE` · 1 `NO-OBTENIDO-POR-ESTE-AGENTE`.

Varias filas quedan `PENDIENTE` con nota de **posible duplicado no forzado** (mismo patrón que `TRIAGE-63` ya estableció para este corpus: declarar el parecido, no fusionar sin URL/evidencia propia) — once casos, todos citados por línea exacta en la tabla.

## §4 · P2 — la skill

`.claude/commands/adquiere.md`. Mecanismo, no resumen: A.8 por fila (`grep` contra `manifiesto.yaml`, criterio host+patrón heredado de `ACTO ADQ-15`) antes de cualquier petición de red; UA de navegador, sin scraping agresivo, sin credenciales ni clickwrap (eso convierte la fila en `NO-ACCESIBLE`, no en un reintento); A.7 doble descarga con verificación de **estructura** (no solo tamaño/hash — el caso del PDF truncado de IFT que `ACTO ADQ-15` documentó es la razón concreta); anti-PR#77 verificado con `ls -la data/raw`; recetas de navegador ≤1 minuto en cada fallo, nunca una conclusión de "no existe".

## §5 · P3 — primera caminata

Elegibles hoy entre "las 15 de `FP-17` + radio_confianza" según `data/cola-adquisicion-v1_0.tsv`: de las 17 filas totales (15 + `radio_confianza`/WVS + verificación), **solo `WVS` estaba `PENDIENTE`** — las 16 restantes ya estaban `OBTENIDO` (11), `NO-ACCESIBLE` (3: WB 6667, WB 870, ENAFIN) o `NO-OBTENIDO-POR-ESTE-AGENTE` (1: LAOMS, 15 intentos acumulados) o `PENDIENTE` sin nueva información que aportar (`FINANZAS`, identidad agotada por ADQ-15).

### Intento — WVS ola 7 México (2018)

Siete peticiones deliberadas, sin fuerza bruta, UA de navegador (`curl -A "Mozilla/5.0..."`, `--max-time` explícito):

```
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 -A "<UA>" \
    https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp        → 200
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 -A "<UA>" \
    https://www.worldvaluessurvey.org/WVSContents.jsp?CMSID=Findings → 200
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 -A "<UA>" \
    https://www.worldvaluessurvey.org/WVSDocumentationWVL.jsp        → 200
```

Sitio alcanzable, sin bloqueo de red ni de sandbox. La página de documentación WV7 es un *shell* JS (`SetContent('#DocumentationWV7')` → formulario oculto `Datos`, `action=WVS...jsp`) sin el listado de archivos. Replicado el `POST` que dispara el tab `wvswave7` (`CMSID=wvswave7` sobre `WVSContents.jsp`) — responde `200`, 1.9 MB, pero el contenedor de archivos descargables está **vacío** en ese HTML: el listado real lo puebla un grid JS (`dhtmlxgrid`, cargado por `js/grid/dhtmlxtabbar.js`) contra un endpoint de datos que no se localizó en las peticiones de esta caminata — no es un muro de credencial confirmado (a diferencia de WB 6667/WB 870), es un límite de renderizado que `curl` no ejecuta.

**Precedente ya establecido en este mismo programa:** `data/INFRAESTRUCTURA-v1_0.md:26` cita `84f8e30` ("`ACTO P·LOTE-1`: WVS obtenido por el usuario, 11 archivos") — WVS ya había requerido la vía "usuario, vía navegador" antes de hoy, para otra ola. Consistente con lo encontrado ahora.

**Veredicto: `NO-OBTENIDO-POR-ESTE-AGENTE (1 intento)`.** No se deriva "no existe" ni "no está disponible" de este fallo — el sitio funciona, la ola 7 México es pública en la práctica del propio archivo WVS; lo que falla es el acceso programático de este agente en esta caminata.

### Paquete de recetas — un solo bloque

| # | Fila | Estado | Receta (≤1 min, verbatim) |
|---|---|---|---|
| 1 | `WVS` (ola 7 México 2018) | `NO-OBTENIDO-POR-ESTE-AGENTE(1)` — **nueva de hoy** | Abrir `https://www.worldvaluessurvey.org/` → menú **Data & Documentation** → **Wave 7 (2017-2022)** → seleccionar México / archivo completo de la ola 7 (formato SPSS/Stata/CSV) → aceptar el acuerdo de uso si aparece → descargar. Nombre de archivo exacto **no confirmado** (no se alcanzó el listado real) — declarado, no inventado. |
| 2 | `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` (LAOMS) | `NO-OBTENIDO-POR-ESTE-AGENTE(15)` — carried forward | Abrir `https://laoms.org/` en navegador; si tampoco carga, copia de archivo en `web.archive.org/web/2024/https://laoms.org/` (200, 115 907 B, verificado 2026-08-18 — es copia de archivo, **no** la base). |
| 3 | `IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016` (WB 6667) | `NO-ACCESIBLE` — no es receta de clic, es **decisión de mesa** | Exige cuenta gratuita en el catálogo de microdatos del Banco Mundial (registro institucional, no pago). `ACTO ADQ-15` y `LOTE-UBUNTU-ADQ-1` deliberadamente no crearon la cuenta. Si mesa autoriza registrar una cuenta institucional, esa autorización — no un clic — es lo que falta. |
| 4 | `MEXICO_ENTERPRISE_SURVEYS_COMPONENTE_PANEL_CANDIDATO_2006_2010` (WB 870) | `NO-ACCESIBLE` — misma decisión de mesa que la fila 3 | Mismo portal, mismo criterio: `login.enterprisesurveys.org/en/signin`. |

`ENAFIN` (Laboratorio de Microdatos, presencial) y las tres comerciales (`Kantar`, `NielsenIQ`, `Mercer/GPTW`) quedan **fuera** de este paquete a propósito: ninguna cabe en "receta de navegador ≤1 minuto" — la primera exige presencia física, las otras cotización/contrato. Siguen `NO-ACCESIBLE`, sin receta, declarado.

### Filas del tablero que `FP-17` pedía como PROPUESTA

`FP-17` declaró explícitamente que "la palanca (prioridad) y la firma de lote son decisión de mesa" — nunca sellada. `data/cola-adquisicion-v1_0.tsv` hereda los 54 valores `palanca` de `FP-17`/`cola-adquisicion-2026-08-12.tsv` como columna `prioridad` sin alterarlos, y propone la escala mixta (`academico-N`/`civil-N`/`general-N`/`oficial-N`) para los 16 candidatos nuevos absorbidos de las tablas de agosto. Esto se registra como **`FP-209`, `PROPUESTA`, `ABIERTA`** (§6) — no autosellada por este acto.

## §6 · Tablero

- **`FP-17`** (`forense/firmas-pendientes.tsv:18`): columna `ejecutada_en` recibe `|| COMPLEMENTO por ACTO MAESTRA33-A1 · AGENTE-ADQUISICION-1`, documentando que las dos filas sin `palanca` (`EXPERIMENTO_INFORMACION_ELECTORAL_2009`, `FINANZAS`) ya tienen hogar en `data/cola-adquisicion-v1_0.tsv`, y que los resultados de `LOTE-UBUNTU-ADQ-1` (nunca escritos a la tabla de 08-12) ya están reflejados en la tabla `v1_0`. `FP-17` sigue `FIRMADA`/`EJECUTADA`, sin reabrir.
- **`FP-179`** (`forense/firmas-pendientes.tsv:177`): ítem `(6)` recibe `ENMIENDA FECHADA (31/ago/2026, ACTO MAESTRA33-A1 · AGENTE-ADQUISICION-1)`: registrado en la fila `WVS` de la tabla nueva, primer intento programático sin éxito (§5), receta de navegador entregada. Sigue `ABIERTA` — no se resuelve hoy.
- **`FP-209` nueva, `ABIERTA`**: recibo de este acto (P1/P2/P3, contador, hallazgos de §2) + propuesta de la escala de prioridad para que mesa la ratifique o la corrija (§5, filas del tablero).

## §7 · CONTADOR

Payloads `OBTENIDO` en `data/cola-adquisicion-v1_0.tsv`: **21 → 21** (adquisición, no medición — declarado, como fija el propio encargo). La caminata de hoy no sumó un `OBTENIDO` nuevo: el único candidato elegible y accesible (`WVS`) cerró en `NO-OBTENIDO-POR-ESTE-AGENTE`. El valor real de P3 es haber **corregido el estado de las 15 de `FP-17`** (que la tabla de 08-12, sin actualizar, seguía mostrando parcialmente pendientes) y haber dejado el mecanismo recurrente (`/adquiere`) instalado para las próximas caminatas.

## §8 · Perímetro — qué se escribió y qué no

**Escrito:** `data/cola-adquisicion-v1_0.tsv` (nueva) · `.claude/commands/adquiere.md` (nueva) · `forense/firmas-pendientes.tsv` (`FP-17` complementada, `FP-179` enmendada, `FP-209` nueva) · esta nota · el encargo a `CONSUMIDO` · cascada (`ADR-242` candidato, `canon/gobernanza-v1_15.md`/`canon/estado-programa-v1_10.md` recifrados, `canon/registro-rotulos.tsv` censado).

**No escrito:** `data/cola-adquisicion-2026-08-12.tsv` ni las cuatro `cola-ext-*` (quedan intactas, como puntero histórico — el encargo lo exige explícitamente). `data/manifiesto.yaml` (ningún payload nuevo entró al corpus en esta caminata — `WVS` no se obtuvo). `milpa/**`. Ningún microdato se abrió ni se analizó.

**Anti-PR#77:** no aplica esta vez — no hubo payload que mover a `data/raw`, porque el único intento de descarga (`WVS`) no llegó a un archivo.
