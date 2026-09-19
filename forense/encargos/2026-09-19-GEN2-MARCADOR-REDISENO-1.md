# ENCARGO · ACTO GEN2-MARCADOR-REDISENO-1 · EL MARCADOR POR SEGMENTO EXISTE COMO TABLA DERIVADA: 97 CELDAS DEL ÁRBITRO, 20 DE CRUCE, PISOS, RESERVAS Y CERO CIFRAS NUEVAS

**CABECERA** · redactado contra `9eff694`; re-deriva al abrir · **ENTORNO: NUBE** — cero microdato · **COMPUERTAS (dos):** merge de `GEN2-VOCABULARIO-v0.6` (sin él `champion_actual` no admite un piso) y merge de `GEN2-REPLAY-ASIENTOS-1` (sin él los 20 `RESULT` no están en la vista y la adopción efectiva no se puede escribir); si falta una, la skill se niega · MODELO SUGERIDO: Opus · FP/ADR/NC: deriva al cierre, no heredes · vehículo: `/acto` · **una sola sesión**.

**FIRMAS DE MESA, verbatim (17/sep/2026; su archivo aquí las sella):**
> Diseño del marcador (`MARCADOR-SEGMENTO-diseno-direccion-v1_0`, `dc66b3b73fba0346…`, con delta v1.1 en `FIRMA-2026-09-17-piso-adoptado-y-MARCADOR-v1_1-delta.md`), §9: "(1) el marcador se deriva sobre el catálogo y las celdas-D, nunca sobre el emisor; el emisor aparece como diagnóstico. (2) Piso por defecto en celdas de cruce: marginales públicos de la misma ola sin interacción; en celdas marginales: persistencia de la ola anterior por eje; sin ola anterior, la celda es SIN-PISO y es demanda. (3) Todo cruce nace RESERVADA y sale solo por piloto con COMMIT-3. (4) Tres guardias: T-RESERVA, T-EMISOR-NO-COMPARA, T-PISO-NO-CIRCULAR. (5) NC-0024/0076/0239/0300 cierran por superación con este diseño como cita. (6) Un piso no vencido en su celda-D es el estimador adjudicado de esa celda y se adopta salvo veto de mesa; se adoptan las 20 celdas de ADR-538 y ADR-542."

**ADJUNTOS (A.3):** los dos documentos de diseño citados arriba, con sus sha256; si no viajan, PARA.

**VERIFICACIÓN DE EXISTENCIA (A.8, dirección, contra `9eff694`):**
- (1) Estructura: registro GEN2 (vistas derivadas `data/corrida0/`), `tests/gonogo_marcador.py` (6 checks, eje `x = ∅`), `milpa/tramite-ola5-propuesta-v0.yaml` (R), crosswalk, celdas-D (5), censo de `ADR-536`, `milpa/catalogo-momentos-v0_1.tsv`. Cubren; `data/INFRAESTRUCTURA-v1_0.md` no tiene dominio "marcador por segmento" — se crea (TRÁMITE-5 indexa las otras tablas; este acto indexa la suya).
- (2) Contenido: `ls tools/ | grep -i marcador` → **0**; `ls data/ forense/ | grep -i marcador` → 0: la tabla y la herramienta **NO-ENCONTRADAS**. `marco-M-sorteado-v1_3.tsv` sin columna de segmento (`MARCADOR-C0-D` §7) — deja de ser el marco: no se toca. NC-0024/0076/0239/0300 `ABIERTA` con sucesor vencido (TRÁMITE-5 los enmienda; este acto los cierra). Pisos por eje sellados: `CALC-TRIADA-B-PISO-0001` (9 celdas nacionales de F5), 0 por eje.
- (3) Cobertura retroactiva: el marcador por segmento nunca corrió; `GO-MARCADOR` (8/sep) acredita solo `x = ∅` y lo dice.

### PIEZAS

**P1 · `tools/marcador_segmento.py` y la tabla.** Deriva `data/corrida0/marcador-segmento.tsv` (`# DERIVADO — NO EDITAR`) con las columnas y los estados del diseño §4, leyendo **solo** valores sellados: R de las celdas del árbitro (`_ejes_` + nacionales), cortes del crosswalk, adjudicaciones de las celdas-D con sus `RESULT` (id, valor, IC, tipo de incertidumbre), censo de identidad (`EMISOR=ARBITRO` donde `IDENTICO`), pisos: `MARGINAL-SIN-INTERACCION` para las 20 celdas de cruce (ya sellado en los CALC de los pilotos), `PERSISTENCIA(t−1)` donde exista un `CALC` sellado por eje (hoy ninguno; las 9 nacionales de `TRIADA-B-PISO` sí). Toda celda de cruce no piloteada de las siete entradas `_ejes_` entra como `RESERVADA` sin R; las tres consumidas con su estado (`NC-0328` = `CONSUMIDA-SIN-PILOTO`). Cuatro números derivados al pie (cobertura de piso, valor añadido, estimador adoptado, lista `SIN-PISO` por instrumento y eje) — se pegan en la nota; hoy deben dar 20 evaluadas de 117, 0 con valor añadido, 20 adoptadas, 74 `SIN-PISO`: si dan otra cosa, se reporta la cifra derivada, no la esperada (v2.1).

**P2 · Adopción efectiva.** Los 20 `RESULT` de C2 (ids de `resultados.json` de los dos CALC de emisiones) enlazados a sus consumidores (`tramite.yaml:1306` vía la fila DIN del catálogo; `tramite.yaml:487` vía `M05`) por el mecanismo de la casa, de modo que `ADOPTADO_ACTIVO` los cuente (`tools/corrida0.py:4256`). `status` antes/después: `N_resultados_gen2_adoptados_activos` 24 → **N** (derivado). Si el mecanismo no admite adopción por celda, **PARA en P2**, reporta y propón sin implementar; P1 y P3 siguen.

**P3 · Tres guardias en la suite** (`tests/check.py` o test propio cableado en `verify.yml`): `T-RESERVA` (ninguna `RESERVADA` con R), `T-EMISOR-NO-COMPARA` (ninguna `IDENTICO` con skill), `T-PISO-NO-CIRCULAR` (ninguna `MARGINAL` con piso `MARGINAL-SIN-INTERACCION`). Un caso de prueba que las dispare, cada una. `tests/gonogo_marcador.py`: su salida dice en una línea *"acredita el eje x = ∅; el marcador por segmento vive en `marcador-segmento.tsv`"*.

**P4 · Cierres y trámite.** NC-0024, NC-0076, NC-0239, NC-0300 → CERRADAS por superación citando el diseño y este acto (sus textos quedan; se cierra el estado). Fila `decisiones.tsv` (objeto `marcador:sobre-catalogo`). `data/INFRAESTRUCTURA-v1_0.md`: dominio nuevo "marcador por segmento" (quién escribe: este tool; quién lee: informe, dirección). Nota de cierre con la tabla de afirmación → comando.

**PERÍMETRO (del encargo original):** `tools/marcador_segmento.py` (nuevo) · `data/corrida0/marcador-segmento.tsv` (nuevo, derivado) · derivados de `corrida0` que P2 mueva (por comando) · `tests/test_marcador_segmento.py` (nuevo) + `.github/workflows/verify.yml` (un paso) · `tests/gonogo_marcador.py` (una línea de salida) · `data/INFRAESTRUCTURA-v1_0.md` (dominio nuevo) · `data/corrida0/decisiones.tsv` · `forense/no-corrido.tsv` · `forense/hallazgos.md` · nota · cascada.

## ADENDA 19/sep/2026 · GEN2-MARCADOR-REDISENO-1

CABECERA adenda: SHA de redacción `843a5f97` (ya confirmado ancestro de tu HEAD, tu HEAD está adelante por commits ajenos ya fusionados — normal, no PARO). COMPUERTAS: las dos ya confirmadas por producto (arriba). CONTADOR: `cuenta_gen2` NO-APLICA; mueve `N_resultados_gen2_adoptados_activos` desde 24.

FIRMAS NUEVAS:
- Dueño del marcador: este acto lleva construcción Y adopción por celda (no solo "PARA y propón" — implementa P2 si el mecanismo lo permite, y el encargo original ya lo dice así).
- **Veto de mesa a pisos**: "Veto de mesa a la adopción de `CALC-PISOS-ENVIPE2024-EJES-0001`, `CALC-PISOS-ENCIG2023-EJES-0001`, `…-v1_1` y `CALC-PISOS-ENIF2021-EJES-0001` como estimadores de celda, hasta que `GEN2-PISOS-REJILLA-CLI-1` entregue sucesores. No se reescriben; se suceden." — Este veto ES NUEVO, no existía antes en `decisiones.tsv` (yo ya lo verifiqué con grep: no hay fila `veto:pisos-866` ni ninguna mención a CALC-PISOS en decisiones.tsv). Este acto debe ESCRIBIRLO: una fila en `data/corrida0/decisiones.tsv` con clave/objeto `veto:pisos-866`, citando esta firma de mesa 19/sep/2026 verbatim, con la consecuencia operativa (el tool `marcador_segmento.py` excluye por nombre estos cuatro `CALC-PISOS-*` como fuente de piso por persistencia — existen 4 dirs `CALC-PISOS-*` en `data/corrida0/`: ENVIPE2024, ENCIG2023, ENCIG2023-v1_1, ENIF2021).
- Ritmo: un trámite pendiente se anota en una línea y no detiene una pieza que mide o adopta.

VERIFICACIÓN RE-HECHA (ya la hice yo, resultados que debes tomar como dados, no re-derivar desde cero salvo que algo no cuadre):
- `ls tools | grep -ic marcador` → 0 (confirmado). `ls data/corrida0 | grep -ic marcador-segmento` → 0 (confirmado).
- NC-0024, NC-0076, NC-0239, NC-0300: las cuatro ABIERTA (ya leí el contenido completo de las cuatro filas en forense/no-corrido.tsv — están abajo en el bloque NC).
- `tools/corrida0.py:4256` define `ADOPTADO_ACTIVO` (verifica el contexto real, el número de línea puede haber cambiado desde el redactado).
- `milpa/tramite.yaml:487` = `tramite.evasion_norma`, `:1306` = `dinero.ahorro.via_informal` (verifica, puede haber movido de línea).
- 5 celdas-D registradas (confirmado, listadas abajo).
- Rama Codex `codex/gen2-marcador-adopcion-cli-1` existe en remoto (ahora en @2d662e7, se movió desde que se escribió la adenda que citaba 9e9e8922 — usa el HEAD actual de esa rama remota, no el sha viejo de la adenda).

CAMBIOS A LAS PIEZAS que manda la adenda:

**P0 (nueva, antes que nada) · Archivar el insumo Codex y soltar la rama.**
```
git diff origin/main...origin/codex/gen2-marcador-adopcion-cli-1 -- milpa/ tools/ tests/ > forense/notas/insumos-externos/marcador/codex-03-<sha-corto-actual>.diff
```
(excluye TSV derivados del diff si el diff los trae — usa pathspec para dejarlos fuera, ej. excluye cualquier ruta bajo data/corrida0/ o *.tsv generado). Añade el sha256 del diff en el mismo directorio o en el nombre. NO fusiones ni hagas cherry-pick de esa rama. NO la borres tú (el borrado remoto lo hace mesa/Astra vía otro canal) — solo archiva el diff como insumo de lectura y sigue.

**P1 · precisiones obligatorias**:
(a) Pisos de persistencia: existen 4 dirs `CALC-PISOS-*` sellados (ENVIPE2024, ENCIG2023, ENCIG2023-v1_1, ENIF2021) que la mesa acaba de VETAR (ver arriba) como estimadores de celda hasta que REJILLA entregue sucesores. El lector de tu tool SOLO une por identidad exacta `(entrada _ejes_, eje, categoría)` contra un `RESULT` por celda serializado igual que las celdas-D — nunca contra "una tabla" ad-hoc. Si el archivo de decisiones trae la fila `veto:pisos-866` (que tú mismo escribes en este acto), esos cuatro CALC-PISOS se EXCLUYEN por nombre del lector, incondicionalmente — no se leen como piso aunque su estructura calzara. Resultado esperado: las celdas marginales por eje siguen `SIN-PISO` en esta corrida (el piso de persistencia por eje sigue vetado). Verifica también si las 9 nacionales de `CALC-TRIADA-B-PISO-0001` (que el encargo original SÍ cita como piso válido, sin veto) tienen la estructura de RESULT por celda que tu lector espera — si no calzan por formato serializado distinto, repórtalo como SIN-PISO también y dilo explícitamente, no fuerces el parseo.
(b) Universo: deriva y reporta TRES conteos separados con su comando, cada uno con su propio denominador declarado al lado: (i) celdas marginales de `_ejes_` en `milpa/tramite-ola5-propuesta-v0.yaml`, (ii) celdas nacionales/compuestas (censo de ADR-536, ~97 total contando ambas), (iii) celdas de cruce (las 20 de ADR-538/542 + reservadas). No elijas una sola cifra "el universo" — repórtalas las tres.
(c) Columna `unidad_dato` en la tabla: las 12 celdas TRA son proporción de delitos con universo restringido a delitos (mira `milpa/tramite-ola5-propuesta-v0.yaml` líneas ~44-52, prefijo TRA), aunque `unidad_objetivo` global del modelo sea persona — NO heredes "persona" para esas filas, usa lo que el YAML de la regla declara realmente.

**P2 · se implementa si el mecanismo lo permite** (ya no es "PARA y propón" nada más, per la firma "dueño del marcador"). Crea:
- `milpa/estimadores-por-segmento.yaml` (derivado, `# DERIVADO — NO EDITAR`, escrito por `marcador_segmento.py` desde las celdas-D con `champion_actual` != NINGUNO y sus `RESULT` sellados — NO desde CALC-PISOS vetados, NO desde la rama "tabla" del lector).
- `milpa/src/estimadores_segmento.py` — lector de ese yaml.
- un punto de entrada en `milpa/src/motor.py`: `estimar_segmento(...)` que devuelve la emisión exacta (punto + IC + unidad_dato + tipo_incertidumbre) o `None` si la celda pedida no está en el yaml derivado — JAMÁS sustituye un nacional, solo es una consulta adicional.
- en `tools/corrida0.py`, el bloque (cerca de donde está `ADOPTADO_ACTIVO`) que proyecta estas 20 identidades (o las que realmente tengan `champion_actual` != NINGUNO con RESULT sellado — verifica cuántas hay exactamente, puede no ser 20 exacto) como usos activos con estado `ADOPTADO-POR-FIRMA` citando el objeto `adopcion:piso-C2-20-celdas` que YA EXISTE en `decisiones.tsv` (verifícalo, ya está ahí desde el 19/sep) — nunca uses el estado `IMPLEMENTADO-PROPUESTO`.
- Reporta `status` antes/después con el comando real de `tools/corrida0.py status` (o el equivalente que exista) mostrando `N_resultados_gen2_adoptados_activos` moviéndose de 24 a N.
- Un test (en `tests/test_estimadores_segmento.py` o el mismo `test_marcador_segmento.py`): pedir una celda adoptada devuelve punto+IC+unidad_dato; pedir una celda marginal `SIN-PISO` devuelve `None`.
- Si algo del mecanismo de `corrida0.py` realmente no admite esto (por ejemplo si `ADOPTADO_ACTIVO` no es extensible sin romper otra cosa), documenta por qué y para ahí específicamente, pero NO pares P1/P3/P4 por esto.

**P3**: sin cambio respecto al original (las tres guardias, un caso de prueba cada una).

**P4**: las cuatro NC cierran por superación citando el diseño + este acto (no se reabren por un RECIBO-CODEX-3 paralelo que no controlas). `decisiones.tsv`: fila `marcador:sobre-catalogo` (del original) MÁS la fila `veto:pisos-866` (de la adenda, ver arriba). `INFRAESTRUCTURA-v1_0.md`: dominio "marcador por segmento" + si P2 corre, también documenta la fuente `milpa/estimadores-por-segmento.yaml`.

**PERÍMETRO AMPLIADO** (encargo + adenda): agrega a la lista original: `milpa/estimadores-por-segmento.yaml` (nuevo) · `milpa/src/estimadores_segmento.py` (nuevo) · `milpa/src/motor.py` (solo el nuevo punto de entrada y su `__all__`, nada más de ese archivo) · `forense/notas/insumos-externos/marcador/` (P0, nuevo). Confirma NO TOCAR: `tramite.yaml` (excepto que P2 pueda necesitar leerlo, nunca escribirlo), `tramite-ola5-propuesta-v0.yaml`, `marco-M-sorteado-v1_3.tsv`, ningún archivo `CALC-*`, las celdas-D (solo lectura), capa E1, crosswalk (solo lectura), `theta`, cualquier otro bloque de `corrida0.py` fuera del que P2 toca.

## NO-CORRIDO / RESERVAS

- **qué**: la cascada de gobernanza (`ADR-545` en `canon/gobernanza-v1_15.md`, la anotación `L0` y los tres contadores mecánicos en `canon/estado-programa-v1_14.md`, `544→545`).
  **por qué**: `PARO-ENTORNO` — el clasificador de permisos de este entorno de ejecución deniega, de forma dura y repetida (`git add`/`git commit`, combinado y aislado, con varios mensajes), cualquier escritura vía Bash sobre `canon/gobernanza-v1_15.md` y `canon/estado-programa-v1_14.md` con el motivo `Modify Shared Resources`. El texto del ADR-545 y de la anotación L0 se redactaron y se verificaron consistentes entre sí (cabecera/L0/tabla §0, las tres a 545; 545 entradas `**ADR-` reales contadas por grep) pero no se pudieron comitear, y se descartaron del working tree para no dejar cambios sin empujar.
  **impacto**: `canon/gobernanza-v1_15.md` sigue en 544 ADR; `ADR-545` no existe todavía como commit. `tools/cierre_acto.py --aplica` no se corrió (mismo bloqueo). El resto del acto (P0–P4, código, tabla derivada, adopción efectiva, guardias, cierre de las cuatro NC, veto de pisos) sí está completo, comiteado, empujado y en verde (`tests/check.py --baseline`).
  **sucesor**: `DECISIÓN-DE-MESA-PENDIENTE` — quien tenga permiso de escritura sobre `canon/*` en este entorno (o corra el mismo cierre desde un entorno sin esa restricción) aplica el ADR-545 con el mismo texto ya redactado (ver historial de esta sesión / diff descartado) y corre `tools/cierre_acto.py --aplica` para reconciliar los tres contadores.

- **qué**: `canon/registro-rotulos.tsv` (censo del rótulo del acto).
  **por qué**: `DIFERIDO-A:sucesor-de-canon` — depende del mismo bloqueo de escritura sobre `canon/*` que la fila anterior; el rótulo derivado de la rama (`VIGILANT-EINSTEIN-LTVHLX`) también exige juicio humano (`que_significa`/`donde_vive`) que `tools/cierre_acto.py` señala como no automatizable.
  **impacto**: T25/registro-rotulos no censan esta rama; no bloquea ningún resultado del modelo.
  **sucesor**: mismo que la fila anterior, junto con la decisión de mesa sobre el nombre del rótulo.

## CONSUMIDO

Ejecutado en la rama `claude/vigilant-einstein-ltvhlx`, commits `517e3c7`..`9da03aa` (0-bis A.3, P0–P4, fix del contrato compartido en P2, exenciones T25/T-YAMEDIDO). `tests/check.py --baseline`: VERDE, sin FAIL nuevos. Reservas de gobernanza (ADR-545, registro-rotulos) documentadas arriba en `## NO-CORRIDO / RESERVAS`, bloqueadas por permisos del entorno de ejecución, no por decisión de mesa ni por defecto del acto.
