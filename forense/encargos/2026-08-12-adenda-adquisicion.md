# ENCARGOS · ADQUISICIÓN — O (cola por demanda) · P (lotes de descarga) · Q (EMOVI/LAPOP como insumos T0) · R (descubrimiento acotado)

- **SHA de redacción**: `cfed849` (base declarada por el propio encargo: "base origin/main = cfed849 o posterior").
- **Entorno asignado**: por acto. **O**: cualquiera de los dos (caja local o nube), declarado — no necesita red; este acto corrió en caja local (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir, firma Ubuntu-con-red), sin usar la red. **P/Q/R**: caja local obligatoria (`sin_variable` + sonda 200) — no se lanzan en nube; no ejecutados en este acto.
- **Estado**: `CONSUMIDO (parcial)` — **ACTO O** ejecutado por el PR de esta rama (`acto-o/cola-adquisicion`), detalle en `forense/notas/2026-08-12-acto-o-cola-adquisicion.md`. **ACTOS P, Q y R no se ejecutaron** — el propio encargo, en su sección "ORDEN Y PRESUPUESTO", instruye secuencia estricta: "O primero (una sesión, firma tu corte al fusionar) → P por lotes (cada lote su sesión) → Q cuando quepa → R al final, un dominio a la vez." Esta sesión ejecuta únicamente el primer eslabón; P/Q/R quedan para actos separados, gateados en la cola que O propone (mesa firma el corte al fusionar este PR).

Archivado per convención de este directorio (`forense/encargos/convencion.md`), como primer commit de este acto, antes de ejecutar el resto del bloque de ARRANQUE — Regla A.3 (`instrucciones-proyecto-v2_5.md`, Bloque D-bis).

---

## Texto completo del encargo, tal como se recibió

════════════════════════════════════════════════════════════════════════
ENCARGOS · ADQUISICIÓN — O (cola por demanda) · P (lotes de descarga) · Q (EMOVI/LAPOP como insumos T0) · R (descubrimiento acotado)
12/ago/2026 · ejecutan la ADENDA-ADQUISICIÓN del plan v1.0 · base origin/main = cfed849 o posterior · construcción R1/R2/R3 · el CARRIL B ya está emitido como ACTO N (DESC-1) y no se duplica aquí

════════ ARRANQUE — cada acto reporta sus cinco líneas antes de nada ════════ 1·REPO (clon existente; ruta · git log -1 · status). 2·SHA (compara; si main avanzó, re-deriva la cola/premisas). 3·data/raw (enlaza al corpus compartido; P/Q/R descargan → verificación PR#77 al cierre obligatoria). 4·ENTORNO (P/Q/R: caja local — sin_variable + sonda 200; O: cualquiera de los dos, declara cuál — no necesita red). 5·ESPEJO (nada). R3: abren en paralelo entre sí y con K/L/M/N/U (perímetros disjuntos salvo hallazgos: union + rebase local; botón solo limpios). ═══════════════════════════════════════════════════════════════════════════

ACTO O · LA COLA DE ADQUISICIÓN, DERIVADA Y CONGELADA — nada se baja aquí (un commit)

Premisas (script):

```bash
set -u; cd "$(git rev-parse --show-toplevel)"
awk -F'\t' 'NR==1{for(i=1;i<=NF;i++){if($i~/capa2/)a=i}} NR>1 && $a=="NO_REFERENCIADO"' data/curacion-registro/relaciones.tsv | wc -l   # esperado ~105; repórtalo
ls forense/censo-estimabilidad-coeficientes-v1_0.md data/catalogo-fuentes-v2_0.md >/dev/null && echo "PASA insumos" || echo "PARA insumos"
```

Qué hace: deriva —con cada comando a la vista— data/cola-adquisicion-YYYY-MM-DD.tsv (fecha tuya; entra al puntero por la regla de conducto) con una fila por fuente NO_REFERENCIADO y columnas: fuente_canonica · n_necesidades_servidas (N1-N15) · destraba_sin_ruta (fila del censo o NO) · destraba_condicional_faltante · celda_piloto_FIN (sí/no) · url_conocida (de cola-ext/índices, o VACIO) · clasificacion_a4_previa · palanca (= orden lexicográfico: sin_ruta > condicional > n_necesidades > piloto). Propone el corte (los lotes 1-3, ≤5 fuentes por lote) en el cuerpo del PR — mesa firma el corte al fusionar; nada de la cola obliga hasta entonces. Perímetro: el TSV nuevo + forense/notas/ (1) + hallazgos. Contadores: 0 — este acto ordena; P baja.

ACTO P · LOTE DE DESCARGA k — repetible, un lote por sesión (dos commits por lote)

Gate: la cola de O fusionada (ls data/cola-adquisicion-*.tsv | sort | tail -1 = el puntero) y el corte firmado en su PR. Premisas (script): puntero presente · las ≤5 fuentes del lote k con su fila · corpus montado. Commit 1 — el lote congelado: las fuentes del lote k copiadas verbatim de la cola (fila y palanca), la URL a sondar por fuente, y el criterio de cierre por clase A.4/A.5. Frase de siempre. Commit 2 — la ejecución: por fuente: sonda A.5 en sesión (falla ⇒ NO OBTENIDO POR ESTE AGENTE EN N INTENTOS + salida cruda + receta manual <1 min — el usuario ya ha bajado a mano lo declarado imposible) · descarga a data/raw del corpus compartido · sha256 vía tests/manifiesto.py --registra · decisión de adquisición por la vía del motor (decisiones-adquisicion/capa2 — jamás editar TSV a mano; si el motor no tiene vía para algo, hallazgo y EN-ESPERA-DE-VIA) · ficha RNM localizada ⇒ fila de puerta + activo documental (conducto) · pago/afiliación institucional ⇒ NO-ACCESIBLE declarado, no se fuerza (registro gratuito NO cuenta como no-accesible: se declara y se hace). Conteos PRISMA al cierre: intentadas / sondeadas-200 / bajadas / íntegras / con-ficha / no-accesibles / no-obtenidas. Nada se abre a nivel variable — la apertura es acto posterior por demanda. Contador: capa2 movida en las filas del lote.

ACTO Q · EMOVI (CEEY) + LAPOP — de cita huérfana a insumo T0 con parser (dos commits)

Premisas (script): ambas ausentes del rastreador (grep -ci "emovi\|lapop" data/curacion-universo/fuentes-t0.tsv → esperado 0 cada una; si ≥1, re-deriva el alcance) · corpus montado. Commit 1 — pre-registro: qué edición se busca (EMOVI: la vigente del CEEY; LAPOP: olas México), términos, portales candidatos (SIN-FETCH hasta abrir — A.6), criterio por clase A.4, y la pregunta de vía declarada: ¿los insumos T0 son config/dato (lista que se extiende) o código (parser nuevo = modificación de motor)? — se responde LEYENDO tools/curador_registro/ antes de tocar nada. Commit 2 — ejecución: sonda + descarga + sha256 + manifiesto + ficha/puerta, como en P. La vía del insumo: si es config/dato ⇒ se extiende y se corre el snapshot por el motor; si exige código ⇒ NO se modifica el motor aquí — se entrega el parser como propuesta (archivo en forense/notas/ con el diff exacto) y el insumo queda EN-ESPERA-DE-VIA, citando la ventana pre-piloto de ADR-70(d) para que mesa decida el acto de motor. LAPOP con registro/licencia: se declara lo que exige; si es afiliación ⇒ NO-ACCESIBLE con receta manual. Contador: 2 fuentes de cita-huérfana a estado registrado (adquiridas, en-espera, o no-accesibles con razón).

ACTO R · DESCUBRIMIENTO ACOTADO — una sesión por dominio de demanda insatisfecha (dos commits por dominio)

Población cerrada de dominios (derívala, no la copies): los huecos ESTRUCTURALES del censo (filas 10 y 14: co-observación sin muestra común) + condicionales faltantes sin candidato en el registro. Un dominio por sesión. Commit 1 — pre-registro del dominio: la necesidad exacta (reactivo+desenlace que deben co-observarse, o el puente), los términos de búsqueda, los tipos de puerta admisibles (encuestas nacionales, registros administrativos, paneles académicos), y el criterio de suficiencia: la sesión termina cuando una pasada completa de términos no produce candidatas nuevas — escrito antes de buscar. Commit 2 — el barrido: candidatas por buscador ⇒ SIN-FETCH (A.6, jamás promovidas sin abrir) ⇒ sonda/apertura de portada ⇒ clasificación A.4 con universo+mecanismo+fecha ⇒ fila en el puntero de puertas por cada candidata clasificada (conducto). Ninguna palabra prohibida; "no apareció con estos términos en estos portales" es el techo de cualquier negativa. Qué NO hace: no baja microdato (eso vuelve por O/P si la candidata prospera), no promete resolver lo estructural — su entregable honesto puede ser "el hueco sigue, y ahora con universo de búsqueda declarado". Contador: filas nuevas de puertas/candidatas, con el embudo contado.

ORDEN Y PRESUPUESTO. O primero (una sesión, firma tu corte al fusionar) → P por lotes (cada lote su sesión; párate entre lotes si K/M están pidiendo la caja — los actos que mueven valores van antes que los que llenan disco) → Q cuando quepa → R al final, un dominio a la vez. La regla madre de la adenda gobierna: se baja por demanda nombrada, nunca por completismo; el contador del programa son los valores, no los gigabytes — y si a mitad de cualquier lote aparece algo que desbloquea un cálculo, eso vale más que terminar el lote: repórtalo y para.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `git grep -Fl -- "2026-08-12-adenda-adquisicion.md"` (excluyendo forense/digesto/) cita nota(s) de cierre: forense/notas/2026-08-12-acto-o-cola-adquisicion.md. Encargo pre-ADR-por-archivo (anterior al 18/ago/2026): la evidencia de ejecución vive en la nota de cierre, no en canon/gobernanza-v1_15.md. Marca ausente era defecto de trámite retroactivo, resuelto por esta auditoría.
