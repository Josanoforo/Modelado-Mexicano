# ENCARGO · ACTO RECENSO-DISEÑO-2 — «damos de alta TODO» (las 37 llaves)

- **SHA de redacción:** `754eb86` (`origin/main`, con `ADR-152`/`ACTO ADQ-DISENO-1` ya fusionado — verificado en `canon/gobernanza-v1_15.md` `ADR-155`, que cita este mismo SHA como el árbol vigente inmediatamente antes de que `RECENSO-DISEÑO-2` fusionara).
- **Entorno asignado:** UBUNTU (los descriptores viven con los payloads). NO NUBE.
- **Estado:** `CONSUMIDO` — ejecutado el 24/ago/2026 (`ADR-153`, fusionado como `PR #321`, `3bae09f`), nota `forense/notas/2026-08-24-recenso-diseno-2-cierre.md` (renombrada 25/ago/2026 para resolver una autocolisión `T02` con este mismo encargo — ver `## Cierre`). Archivado retroactivamente el 25/ago/2026 por `ACTO BANDAS-DOC-6` — el texto no se había commiteado al árbol pese a haberse ejecutado y fusionado (incumplimiento de `forense/encargos/convencion.md` detectado por ese acto; texto recuperado y archivado aquí, verbatim, sin editar).

## Bloque VERIFICACIÓN DE EXISTENCIA (dirección, tal como se lanzó)

Las 37 llaves sin fila las midió RECENSO-14 y viven en `FP-117` (5 programas INEGI: engasto·enestyc·enafin·mmsi·encoap; hosts externos encabezados por worldbank·banxico·ensanut.insp·cnbv·wvs·osf·gesis). El censo es del 4/ago; **re-deriva la lista hoy** cruzando manifiesto vs `diseno-muestral.yaml` — con `ADQ-1` fusionado puede haber llaves nuevas, y la lista manda sobre el 37 con la discrepancia declarada.

## Texto completo tal como se lanzó

> # ENCARGO · ACTO RECENSO-DISENO-2 — «damos de alta TODO» (las 37 llaves)
>
> | | |
> |---|---|
> | **Redactado por** | dirección, 24/ago/2026 · Firma que ejecuta: respuesta 6 de mesa, verbatim en ADR de SELLA-D |
> | **ENTORNO** | **UBUNTU** (los descriptores viven con los payloads). NO NUBE. · Modelo: Opus · 🚫 `--freeze` · `pgrep -af claude` · `iconv` en toda tubería |
> | **⛔ ORDEN** | **Tras fusionar `ADQ-DISENO-1`** (aprovecha lo recién bajado). · **CONTADOR:** cero — extiende la fuente de verdad del diseño a todo el conocido. Declarado (v2.3). |
>
> ════════ ARRANQUE ════════
> 1 · REPO: clon existente. 2 · SHA: base con ADQ-DISENO-1 fusionado — verifica que su nota existe; si no: PARA. 3 · data/raw: enlaza al corpus; este acto NO descarga (lo que falte quedó anotado por ADQ-1). 4 · ENTORNO tres partes (A.2): `sin_variable` · sonda INEGI · `ls data/raw/` (vacío = PARO). ⚠️ [v2.11] A.13 en todo negativo. 5 · ESPEJO: nada.
> ══════════════════════════
>
> ═══ VERIFICACIÓN DE EXISTENCIA (dirección) ═══
> Las 37 llaves sin fila las midió RECENSO-14 y viven en FP-117 (5 programas INEGI: engasto·enestyc·enafin·mmsi·encoap; hosts externos encabezados por worldbank·banxico·ensanut.insp·cnbv·wvs·osf·gesis). El censo es del 4/ago; **re-deriva la lista hoy** cruzando manifiesto vs `diseno-muestral.yaml` — con ADQ-1 fusionado puede haber llaves nuevas, y la lista manda sobre el 37 con la discrepancia declarada.
> ═══════════════════════════
>
> ## Método — el mismo de RECENSO-14, sin atajos nuevos
> Por llave: localiza el descriptor real en corpus (DDI/FD/nota metodológica) · extrae **ponderador · estrato · UPM · réplicas · universo del ponderador** con cita archivo:página del documento fuente · escribe la fila. **Nada se infiere de encuestas parecidas.** Sin descriptor → `EXISTE-NO-SATISFACE` con dónde buscaste y conteo (A.13), y receta A.5 si la fuente lo publica. Fuentes que no son muestra → `NO_APLICA_REGISTRO_ADMINISTRATIVO` (el valor que SELLA-D ya añadió). Verificación cruda mínima por fila: la columna de ponderador nombrada existe en el microdato y no es toda-vacía — confirmación, no cálculo.
>
> **Cierre:** FP-117 → `ejecutada_en` · tabla resumen (llave · estado A.4 · qué falta si falta) en `forense/notas/2026-08-24-recenso-diseno-2.md` · filas A.12 solo para lo que exija decisión nueva · ADR · recifrado estándar · suite **VERDE** con tail · encargo `CONSUMIDO` · párrafo a mesa: cuántas de las ~37 quedaron completas y cuáles son las 3 cojas que más duelen.
>
> ## PERÍMETRO
> `data/diseno-muestral.yaml` (solo filas nuevas + las que ADQ-1 destrabó) · `forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md` · nota · encargo · scratchpad. **Fuera de la lista: PARA.**
> Concurrencia: NUBE en paralelo permitido; renumera quien fusiona segundo.

## Cierre

**Resultado real, con la discrepancia declarada contra el encargo:** el encargo pedía dar de alta las **37** llaves de `FP-117` bajo la opción "alta-completa-37" de mesa (`FP-120`). La ejecución (`forense/notas/2026-08-24-recenso-diseno-2-cierre.md`) re-derivó la lista, tal como el propio bloque de VERIFICACIÓN DE EXISTENCIA exigía ("la lista manda sobre el 37 con la discrepancia declarada"), y encontró **13 llaves reales, no 37** — 24 de las 37 originales resultaron ser duplicados de filas ya existentes (`ensanut.insp`, `vanderbilt.edu`/LAPOP) o hosts administrativos/documentales sin identidad de fuente propia (Banxico, CNBV agregados, GDELT, UCDP, etc.), no encuestas nombrables. `data/diseno-muestral.yaml`: 43→56 filas (13 altas: 2 `MAPEADO`, 3 `SIN_DISEÑO_PUBLICADO`, 7 `PENDIENTE`, 1 `NO_APLICA_REGISTRO_ADMINISTRATIVO`). `FP-117` y `FP-120` → `ejecutada_en = 2026-08-24`. Abre `FP-123` (vocabulario del censo sin valor claro para un RCT — el paquete openicpsr "Compartamos AEJ"). `ADR-153` candidateado y luego renumerado por colisión de fusión (ver `ADR-155`, cascada). Fusionado como **`PR #321`** (SHA de fusión `3bae09f`, citado en `ADR-155`).

**Por qué este encargo se archiva hoy y no el 24/ago:** la propia nota de cierre del acto declara, verbatim: *"No se marca el encargo como CONSUMIDO ni se hizo commit/push — instrucción explícita del encargo; el worktree queda con los cambios sin commitear para revisión del supervisor."* El texto del encargo, sin embargo, nunca se commiteó a `forense/encargos/` en ningún acto posterior (incumpliendo `forense/encargos/convencion.md`, que exige commitearlo antes o junto con su lanzamiento) — hueco detectado por `ACTO BANDAS-DOC-6` (`ADR-160(c)`, 25/ago/2026), que no tenía el texto original y por eso no pudo archivarlo entonces. El texto llega ahora, aportado por dirección, y se archiva verbatim, sin editar, con este `## Cierre` añadido para no dejarlo como una ficha `VIVO` fantasma. La nota original se renombra en el mismo acto a `forense/notas/2026-08-24-recenso-diseno-2-cierre.md`: sin el sufijo, su nombre normalizado colisionaba con el de este mismo encargo (`T02`), mismo patrón ya usado por `ADR-135`/`ADR-158`.

**Perímetro de este archivado (25/ago/2026):** este archivo (nuevo) y el renombre de la nota (arriba) y, por transitividad, la deuda declarada en `ADR-160(c)`/`canon/estado-programa-v1_10.md` que este archivado salda — no se reabre ni edita `data/diseno-muestral.yaml` ni `forense/firmas-pendientes.tsv` (`FP-117`/`FP-120`/`FP-123` ya reflejan el resultado real desde el 24/ago; la cita a la nota en la fila `FP-123` queda sin actualizar, historia real de cuando se escribió, no colgante para las herramientas de este árbol).
