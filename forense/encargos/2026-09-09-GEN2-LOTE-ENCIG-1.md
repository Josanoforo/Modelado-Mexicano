ENCARGO · ACTO GEN2-LOTE-ENCIG-1 · SEGUNDO LOTE DE LA CARTERA — la mordida por canal con denominadores a la vista, y esta vez el ciclo entero: medir, citar en el motor, probar el consumo

CABECERA · CAJA (UBUNTU), Opus (medidor de dos commits, D-13) · NO se lanza en NUBE — sin bytes no hay acto (A.2) · COMPUERTA: GATED a PR del ACTO GEN2-R-SERIE-DBF fusionado — un solo empleado de caja a la vez; la skill /acto verifica contra origin/main y se niega con A.13 si no está · redactado contra origin/main = 4497029a (PR #657) · candidatos CALC/FP/NC/ADR: deriva al cierre, no heredes.

FIRMA DE MESA, 9/sep/2026, verbatim (adentro, por dictado de mesa; su merge sella): «Encargo ACTO GEN2-R-SERIE-DBF corriendo PR's mergeados, dame los siguientes encargos.» — la cartera ENVIPE→ENCIG→ENIF viene firmada por el plan de obra v1.1 (F4, sellado por merge del PR #652); este encargo es el segundo tramo. ⚠️ FIRMA DE CONTADOR con OBJETO, incluida aquí (estándar FP-367/368, patrón de los lotes R): cuenta_gen2 = SI para el CALC que este acto selle — el acto escribe la decisión citando este párrafo; el merge de mesa la perfecciona.

VERIFICACIÓN DE EXISTENCIA (A.8, contestada por dirección, 9/sep/2026, contra 4497029a): (1) ESTRUCTURA — la plaza: CORR-0002, 10 RESULT (RES-0003/0004/0009–0016), payload encig25_base_datos_csv, vía CAJA. Gobiernan: data/manifiesto.yaml (payload EXISTE, verificado en sesión previa) · forense/notas/2026-09-09-identidad-encig-corr-0002-0003.md (la identidad ya resuelta: es ENCIG 2025; la columna instrumento de la demanda dice ENCIG2023 porque su DERIVACIÓN está mal, no la fila — el sucesor lee payload, nunca instrumento) · milpa/tramite.yaml (los consumidores, con sus valores GEN1 a la vista). (2) CONTENIDO — ls forense/prereg-caja/ | grep -icE "encig" → 0 sobre el listado completo (A.13): NO-ENCONTRADO — la spec no existe; producirla no duplica nada. Los 10 consumidores EXISTEN en la demanda con valores GEN1 sellados: tramite.mordida.discrecional (par 0.085118/0.914882) y tramite.mordida.con_registro en dos rondas por canal (presencial 0.116/0.884 y _r2 0.141041/0.858959 · digital 0.027358/0.972642 y _r2 0.029868/0.970132) — la cadena es lo que falta, no los números; mismo patrón que el lote ENVIPE. (3) COBERTURA RETROACTIVA — los valores GEN1 nacieron de actos MAESTRA35 (agosto), anteriores al registro: son control positivo, jamás insumo (E.1).

CONTAMINACIÓN, DECLARADA (ADR-46). Los diez valores GEN1 están en el repo y dirección los leyó (arriba). La spec no elige nada para acercarse a ellos: codificación, universo y denominadores salen del codebook, y el COMMIT-1 cierra con «el primer resultado que produzca este procedimiento es el que se reporta».

PIEZAS (D-11; un lote = una corrida coherente = un PR): P0 · LA DERIVACIÓN QUE ETIQUETÓ MAL. Localiza el derivador de demanda-corridas.tsv y corrige la fuente de la columna instrumento para que derive del payload/manifiesto (la nota de identidad lo prescribe: hoy agrupa ENCUCI 2020 bajo "ENCIG2023"). Re-deriva la demanda y pega el diff de las filas corregidas. Si el derivador no es localizable en una búsqueda razonable (di cuántos archivos examinaste, A.13), la pieza sale como fila NC con sucesor — no se parcha el TSV derivado a mano jamás. P1 · IDENTIDAD Y SPEC (COMMIT-1, solo codebook/metadato — E.5). Resuelve del codebook ENCIG 2025, ANTES de abrir microdato: unidad de observación (persona / experiencia / trámite — cambia el denominador y el codebook manda, no el nombre de la conducta), población elegible y selección de trámites, el reactivo de pago informal con sus códigos y dirección, qué distingue la ronda base de la _r2 (dos rondas del cuestionario: la spec declara qué pregunta alimenta cada consumidor o marca _r2 NO-CONSTRUIBLE con cita), el canal (presencial/digital: cómo se define y quién es elegible en cada uno), y diseño (ponderador/EST/UPM — la lección de FP-201: verifica si la varianza de diseño es identificable antes de renunciar a ella). Spec de dos capas; NO-APLICA es un valor. P2 · MEDICIÓN (COMMIT-2, no edita el 1). Un CALC, los 10 RESULT con embudo contado por denominador (elegibles, no-aplica, NS/NR, faltantes — cero no sustituye falta de dato), escala declarada por RESULT (A-bis.3). ⚠️ Los pares que "suman 1" son hipótesis del codebook, no herencia: si el reactivo tiene categorías fuera del par (el hallazgo 3.2 del lote ENVIPE), el complemento se emite con su denominador escrito y NO como cantidad medida independiente — y su cita de adopción se prohíbe en P3, patrón NC-0085. La diferencia presencial−digital se rotula asociación (elección de canal y elegibilidad la confunden); ningún RESULT causal. Control positivo posterior, por script, contra los diez valores GEN1 — coincidencia se reporta, discrepancia se reporta con embudo, nada se ajusta hacia atrás. P3 · ADOPCIÓN Y CONSUMO (F3, esta vez adentro — la lección del lote ENVIPE). Escribe las citas corrida0_resultado_id + corrida0_generacion: GEN2 en milpa/tramite.yaml SOLO para los RESULT que sean cantidades genuinamente medidas (el patrón de la línea 583: el p NO se mueve, se declara de dónde viene); los complementos no medidos quedan sin cita y con su fila NC de advertencia. Re-deriva usos.tsv, corre la sonda de consumo del emisor en solo-lectura (patrón §4.1 del cierre ENVIPE) y pega su salida. Reporta adoptados_activos y dependencias_legacy antes/después, salida cruda, sin cifras esperadas (E.4).

PERÍMETRO Y CONCURRENCIA. Toca: derivador de demanda + demanda-*.tsv re-derivados (P0) · forense/prereg-caja/ENCIG-MORDIDA* · data/corrida0/CALC-*/ (uno nuevo) · TSV re-derivados por el comando de la casa · milpa/tramite.yaml (SOLO las líneas de cita de sus 10 consumidores) · forense/notas/ · forense/no-corrido.tsv (append) · 0-bis · cascada. EN PARALELO puede vivir REVISA-CALC post-hoc y trámites NUBE — intersección solo en TSV derivados y no-corrido: append/re-deriva y reporta pisadas. «Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.»

CONTADOR: sí — un CALC con cadena E.2 completa; la firma viaja arriba, con OBJETO.

LO QUE NO HACE: no mide ENIF ni ENCUCI (encargos hermanos) · no toca las reglas _ejes_* de la propuesta OLA5 (FP-241/252 siguen de mesa) · no adjudica causalidad del canal · no toca marcador, capturas, ni los CALC-R · no repara nada del inventario de reactivos.

SUCESORES: GEN2-LOTE-ENIF-1 (gateado a este merge) · GEN2-LOTE-ENCUCI-1 (CORR-0003, 2 RESULT — dirección lo redacta al cerrar ENIF) · si algún _r2 sale NO-CONSTRUIBLE, la decisión de su consumidor sube a mesa por la vista --mesa.

CIERRE · Cascada completa + ## NO-CORRIDO / RESERVAS + ## CONSUMIDO con el PR.

---

## ADENDA DE PROPAGACIÓN (dirección, 9/sep/2026) — verbatim

ADENDA DE PROPAGACIÓN al ACTO GEN2-LOTE-ENCIG-1, dirección, 9/sep/2026 — cinco actualizaciones que superan líneas del encargo; ante conflicto, manda esta adenda:
(1) COMPUERTA CUMPLIDA Y REESCRITA. Los gates son ahora «#661 (R-SERIE-DBF) y #662 (PREP-LOTE) fusionados» — ambos están en origin/main. Re-deriva contra el main vigente al abrir; el SHA 4497029a de redacción quedó atrás.
(2) P0 ELIMINADO. La corrección del derivador ya la hizo el ACTO GEN2-PREP-LOTE (PR #662): no toques _instrumento() ni re-derives identidad. Tu fuente de agrupación es la demanda vigente + forense/notas/2026-09-09-GEN2-PREP-LOTE-identidad-migracion.md.
(3) SON 12 RESULT, NO 10. CORR-0002 (ENCIG2025, mismo id) agrupa ahora RES-0003/0004/0009–0016/0021/0022 — enumera desde la demanda en tu arranque y pega la lista; la cifra «10» del A.8 de dirección quedó superada por la migración. CORR-0001 (ENCIG2023, sin payload, 4 RESULT) NO es de este lote: ni lo midas ni lo declares — es identidad pendiente con decisión propia.
(4) NC-0094 YA ES MECÁNICA. registro --escribe trae la protección de evidencia (PR #660, verificada en producción): cierra con el flujo estándar, sin diff manual — si la protección se niega, eso es hallazgo, repórtalo.
(5) ABSORBE EL ASIENTO NC-0097. En tu escritura de decisiones.tsv (donde va tu propia firma de contador), asienta también las tres filas de los CALC-R del CSV con cita a la firma embebida en su encargo y al merge #657 — asiento, no re-firma — y cierra NC-0097 con este PR. Es el sucesor que E1 nombró; te cuesta tres filas y la re-derivación que ya ibas a hacer.

---

## Bloque de archivo (A.3) — añadido por el ejecutor, NO edita el texto verbatim de arriba

## A.8 · `tools/ya_medido.py` — salida corrida en la caja del acto

Este encargo cita tres ids de regla del motor en su cuerpo
(`tramite.mordida.discrecional`, `tramite.mordida.con_registro`,
`tramite.gobierno_digital.util_sin_coercion`), así que A.8 y `T-YAMEDIDO`
exigen la salida del comando. Corrida con `TZ=UTC` (`T-YAMEDIDO-HUSO`),
sobre el árbol de este acto, **cruda**:

```
### tramite.mordida.discrecional
=== ya_medido: tramite.mordida.discrecional ===
  resuelto por canon: tramite.mordida.discrecional -> R3.1 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
  términos de búsqueda (match exacto): tramite.mordida.discrecional, R3.1

-- milpa/tramite.yaml --
  milpa/tramite.yaml:40  situacion=realiza_tramite_gobierno tier=FUERTE p=0.62
      id: tramite.mordida.discrecional
  milpa/tramite.yaml:434  situacion=enfrenta_norma_percibida_inutil_o_extractiva tier=FUERTE p=0.66
      id: tramite.evasion_norma

-- milpa/tramite-ola5-propuesta-v0.yaml --
  milpa/tramite-ola5-propuesta-v0.yaml:131  situacion=realiza_tramite_gobierno tier=SELLADA p=0.62
      id: tramite.mordida.discrecional
  milpa/tramite-ola5-propuesta-v0.yaml:317  situacion=PENDIENTE-DE-MESA tier=SELLADA p=0.538502
      id: dinero.planeacion.formal_estable
  milpa/tramite-ola5-propuesta-v0.yaml:462  situacion=realiza_tramite_gobierno tier=PENDIENTE-DE-MESA). p=0.085118
      id: tramite.mordida.discrecional_encig_serie
  milpa/tramite-ola5-propuesta-v0.yaml:903  situacion=PENDIENTE-DE-MESA tier=SELLADA p=0.642080
      id: dinero.ahorro.tiene_ahorros_enif2024

-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:704  tier=[MEDIA]
      - **49 reglas** *(42 en v2 · 43 en v2.1 por conf.07 · 44 en v2.3 al partir la diagonal)*. **Hito D (perímetro de 27 reglas, subconjunto de las 49): 26 de 27 corridas archivadas**<!-- T20:HITO-D pob=re
  canon/modelo-decision-v4_0.md:742  tier=[FUERTE]
      | `R3.1` | L232 | Trámite presencial discrecional sin registro → mordida | `[FUERTE]` | Sí *(Nota 14, 4/ago/2026)* |

-- forense/notas/*-L*-*.md --
  forense/notas/2026-09-01-MAESTRA34-L2-ARBITRA-v1_2-cierre.md:17  p=0.62
      y `p: 0.62, clase: ASIGNADO` de `tramite.mordida.discrecional`. `TRA-M-02` es
  forense/notas/2026-09-01-MAESTRA34-L2-ARBITRA-v1_2-cierre.md:18  
      **ENCUCI 2020, `AP5_17|AP5_18`, regla `tramite.mordida.discrecional`**: la tasa
  forense/notas/2026-09-09-GEN2-PREP-LOTE-identidad-migracion.md:17  
      como `ENCIG2023` — el rastro de cuando `tramite.mordida.discrecional` era
  forense/notas/2026-09-09-GEN2-PREP-LOTE-identidad-migracion.md:179  
      No corrigió `milpa/tramite.yaml:tramite.mordida.discrecional`'s `fuente:`

-- forense/prereg-caja/S*-spec-*.md --
  forense/prereg-caja/S18-MODULACION-OLA-R3-1-spec-v1_0.md:1  
      # S18 · Pre-registro de la MODULACIÓN POR OLA de `R3.1` — `tramite.mordida.discrecional` / `enmienda_encig2025` sobre la serie ENCIG de ocho olas
  forense/prereg-caja/S18-MODULACION-OLA-R3-1-spec-v1_0.md:9  
      > | **QUÉ ES** | Spec propia de la **modulación por ola** para la segunda de las dos reglas que el marco vigente trae con `serie_olas`: `tramite.mordida.discrecional`, enmienda `enmienda_encig2025` (`
  forense/prereg-caja/S18-MODULACION-OLA-R3-1-spec-v1_0.md:10  
      > | **QUÉ NO ES** | **No corre ningún CALC y no produce ninguna cifra nueva.** No re-mide ninguna ola de ENCIG. No promedia, no ajusta tendencia, no interpola. No mueve `R3.1` ni toca el `0.62` ASIGNA
  forense/prereg-caja/S18-MODULACION-OLA-R3-1-spec-v1_0.md:19  
      La regla `tramite.mordida.discrecional` conserva su `0.62`/`0.38` ASIGNADO como historia **`REFUTADA-POR-R`**; la enmienda `enmienda_encig2025` (firma DM, 1/sep/2026, `ACTO MAESTRA34-N4`) lo sustituye
  forense/prereg-caja/S18-MODULACION-OLA-R3-1-spec-v1_0.md:23  
      `milpa/tramite.yaml:tramite.mordida.discrecional.enmienda_encig2025.serie_olas`, ocho entradas:
  forense/prereg-caja/S18-MODULACION-OLA-R3-1-spec-v1_0.md:76  
      Inventario citado: las ocho olas están en corpus con `payload_manifiesto_id` y `sha256_payload` publicados en `serie_olas` (`encig_2011_base_datos_encig2011_dbf` … `encig25_base_datos_csv`). Esta spec
  forense/prereg-caja/S18-MODULACION-OLA-R3-1-spec-v1_0.md:80  
      1. **No mueve `R3.1`.** Ni el `0.62` ASIGNADO (que sigue `REFUTADA-POR-R`, se conserva como historia y no se borra) ni el `0.085118` de la enmienda. Ninguna cifra de la modulación entra a un veredicto
  forense/prereg-caja/S18-MODULACION-OLA-R3-1-spec-v1_0.md:87  
      Congelada en el `COMMIT-1` del `ACTO GEN2-C0-B`. Esta spec **no produce cifras**. Si un acto sucesor corre un CALC de modulación sobre `R3.1`, **el primer resultado que produzca ese procedimiento es e

-- canon/registro-rotulos.tsv (alias) --
  canon/registro-rotulos.tsv:61  
      E	MAESTRA32-E15
  canon/registro-rotulos.tsv:66  
      E	MAESTRA32-E18
  canon/registro-rotulos.tsv:110  
      N	MAESTRA34-N4
  canon/registro-rotulos.tsv:202  
      M	MAESTRA38-M13
  canon/registro-rotulos.tsv:206  
      S	MAESTRA38-SELLO-3
  canon/registro-rotulos.tsv:251  
      GEN2	GEN2-C0-B

========================================
NUNCA-MEDIDA

### tramite.mordida.con_registro
=== ya_medido: tramite.mordida.con_registro ===
  resuelto por canon: tramite.mordida.con_registro -> R3.2 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
  términos de búsqueda (match exacto): tramite.mordida.con_registro, R3.2

-- milpa/tramite.yaml --
  milpa/tramite.yaml:40  situacion=realiza_tramite_gobierno tier=FUERTE p=0.62
      id: tramite.mordida.discrecional
  milpa/tramite.yaml:122  situacion=realiza_tramite_gobierno tier=FUERTE p=0.88
      id: tramite.mordida.con_registro

-- milpa/tramite-ola5-propuesta-v0.yaml --
  milpa/tramite-ola5-propuesta-v0.yaml:131  situacion=realiza_tramite_gobierno tier=SELLADA p=0.62
      id: tramite.mordida.discrecional
  milpa/tramite-ola5-propuesta-v0.yaml:462  situacion=realiza_tramite_gobierno tier=PENDIENTE-DE-MESA). p=0.085118
      id: tramite.mordida.discrecional_encig_serie
  milpa/tramite-ola5-propuesta-v0.yaml:543  situacion=realiza_tramite_gobierno tier=SELLADA veredicto=veredicto=digital: p=0.027358
      id: tramite.mordida.con_registro_encig2025
  milpa/tramite-ola5-propuesta-v0.yaml:903  situacion=PENDIENTE-DE-MESA tier=SELLADA p=0.642080
      id: dinero.ahorro.tiene_ahorros_enif2024

-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:704  tier=[MEDIA]
      - **49 reglas** *(42 en v2 · 43 en v2.1 por conf.07 · 44 en v2.3 al partir la diagonal)*. **Hito D (perímetro de 27 reglas, subconjunto de las 49): 26 de 27 corridas archivadas**<!-- T20:HITO-D pob=re
  canon/modelo-decision-v4_0.md:743  tier=[FUERTE]
      | `R3.2` | L233 | Digitalización/testigos/registrable → baja la mordida | `[FUERTE]` | Sí |

-- forense/notas/*-L*-*.md --
  forense/notas/2026-09-01-MAESTRA34-L1-MORDIDA-SERIE-cierre.md:94  
      ## P3 · Censo `tramite.mordida.con_registro`
  forense/notas/2026-09-02-MAESTRA35-L1-resultados.md:9  
      # `P1` · `tramite.mordida.con_registro` recorrida sin deduplicar
  forense/notas/2026-09-02-MAESTRA35-L1-resultados.md:101  
      - **Enmienda in situ** bajo `tramite.mordida.con_registro_encig2025` en
  forense/notas/2026-09-02-MAESTRA35-L1-spec.md:87  
      ## §2 · `P1` · `tramite.mordida.con_registro` recorrida sin deduplicar
  forense/notas/2026-09-02-MAESTRA35-L1-spec.md:120  
      `tramite.mordida.con_registro_encig2025` en
  forense/notas/2026-09-02-MAESTRA35-L1-spec.md:294  
      - `tramite.mordida.con_registro_encig2025` — enmienda in situ (`P1`)

-- forense/prereg-caja/S*-spec-*.md --
  (sin apariciones)

-- canon/registro-rotulos.tsv (alias) --
  canon/registro-rotulos.tsv:66  
      E	MAESTRA32-E18
  canon/registro-rotulos.tsv:104  
      L	MAESTRA34-L1
  canon/registro-rotulos.tsv:110  
      N	MAESTRA34-N4
  canon/registro-rotulos.tsv:123  
      L	MAESTRA35-L1
  canon/registro-rotulos.tsv:128  
      N	MAESTRA35-N4

========================================
NUNCA-MEDIDA

### tramite.gobierno_digital.util_sin_coercion
=== ya_medido: tramite.gobierno_digital.util_sin_coercion ===
  resuelto por canon: tramite.gobierno_digital.util_sin_coercion -> R3.4 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
  términos de búsqueda (match exacto): tramite.gobierno_digital.util_sin_coercion, R3.4

-- milpa/tramite.yaml --
  milpa/tramite.yaml:339  situacion=le_ofrecen_servicio_gobierno_digital tier=FUERTE p=0.71
      id: tramite.gobierno_digital.util_sin_coercion

-- milpa/tramite-ola5-propuesta-v0.yaml --
  milpa/tramite-ola5-propuesta-v0.yaml:784  situacion=le_ofrecen_servicio_gobierno_digital tier=SELLADA p=0.673393
      id: tramite.gobierno_digital.util_sin_coercion_encig2025
  milpa/tramite-ola5-propuesta-v0.yaml:1598  situacion=SELLADA tier=SELLADA p=0.681276
      id: tramite.gobierno_digital.util_sin_coercion_ejes_encig2025
  milpa/tramite-ola5-propuesta-v0.yaml:1772  situacion=SELLADA-PENDIENTE-CARGA tier=FUERTE p=0.207026
      id: tramite.gobierno_digital.uso_general_endutih2025

-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:704  tier=[MEDIA]
      - **49 reglas** *(42 en v2 · 43 en v2.1 por conf.07 · 44 en v2.3 al partir la diagonal)*. **Hito D (perímetro de 27 reglas, subconjunto de las 49): 26 de 27 corridas archivadas**<!-- T20:HITO-D pob=re
  canon/modelo-decision-v4_0.md:727  
      **Decisión: los IDs son un registro CONGELADO, no una fórmula.** (a) Los **24 IDs ya usados en fichas** (`R1.1`–`R10.3`, ver `hitoD-preregistro`) quedan exactamente como están; nunca se recomputan. (b
  canon/modelo-decision-v4_0.md:745  tier=[MEDIA-FUERTE]
      | `R3.4` | L235 | Gobierno digital coercitivo (CoDi) rechazado vs. útil (SPEI) adoptado — **el gate** | `[MEDIA-FUERTE]` | Sí *(Nota 15, 4/ago/2026)* |

-- forense/notas/*-L*-*.md --
  forense/notas/2026-09-02-MAESTRA34-L5-P0-censo.md:28  
      | `tramite.gobierno_digital.util_sin_coercion` ASIGNADO, `adopta` 0.71 | `sed -n '177,201p' milpa/tramite.yaml` | **VERDADERA**; la regla **no tiene bloque `disparadores`**, solo `contexto_producto: {
  forense/notas/2026-09-02-MAESTRA34-L5-P0-censo.md:78  
      ## §2 · P1 · `tramite.gobierno_digital.util_sin_coercion` — ENCIG 2025
  forense/notas/2026-09-02-MAESTRA34-L5-P0-censo.md:288  
      | P1 | `tramite.gobierno_digital.util_sin_coercion` | ENCIG 2025 | **EXISTE-SATISFACE con mapeo declarado** | **sí** |
  forense/notas/2026-09-02-MAESTRA34-L5-P1-spec.md:1  
      # ACTO MAESTRA34-L5 · P1 · `tramite.gobierno_digital.util_sin_coercion` — SPEC CONGELADA
  forense/notas/2026-09-02-MAESTRA34-L6-P0-tabla-tratamiento.md:19  
      684:  - id: tramite.gobierno_digital.util_sin_coercion_encig2025
  forense/notas/2026-09-02-MAESTRA34-L6-cierre.md:48  
      684:  - id: tramite.gobierno_digital.util_sin_coercion_encig2025
  forense/notas/2026-09-02-MAESTRA35-L1-resultados.md:207  
      # `P3` · `tramite.gobierno_digital.util_sin_coercion` por ejes, ENCIG 2025
  forense/notas/2026-09-02-MAESTRA35-L1-spec.md:203  
      ## §4 · `P3` · `tramite.gobierno_digital.util_sin_coercion` por ejes, ENCIG 2025
  forense/notas/2026-09-02-MAESTRA35-L1-spec.md:296  
      - `tramite.gobierno_digital.util_sin_coercion_ejes_encig2025` (`P3`)
  forense/notas/2026-09-02-MAESTRA35-L6-P0-censo.md:81  
      Esto **no vacía el acto**: aquel censo juzgaba las condiciones `B`/`C` de `R3.4`
  forense/notas/2026-09-02-MAESTRA35-L6-P0-censo.md:480  
      `estampa A.10` de la regla espejo `tramite.gobierno_digital.util_sin_coercion`
  forense/notas/2026-09-02-MAESTRA35-L6-spec.md:25  
      `tramite.gobierno_digital.util_sin_coercion` declara expresamente no haber

-- forense/prereg-caja/S*-spec-*.md --
  (sin apariciones)

-- canon/registro-rotulos.tsv (alias) --
  canon/registro-rotulos.tsv:29  
      E	E1
  canon/registro-rotulos.tsv:48  
      E	MAESTRA32-E1
  canon/registro-rotulos.tsv:90  
      C	MAESTRA33-C7
  canon/registro-rotulos.tsv:120  
      L	MAESTRA34-L5
  canon/registro-rotulos.tsv:122  
      N	MAESTRA35-N1

========================================
NUNCA-MEDIDA
```

### Lectura del veredicto — **`NUNCA-MEDIDA` es un FALSO NEGATIVO aquí, y se declara en vez de repetirlo**

Las tres reglas **SÍ están medidas y selladas** en `milpa/tramite.yaml`, que es
la primera de las cinco fuentes que el propio script cruza:
`paga_mordida_encig2025 p: 0.085118`, `paga_mordida_encig2025_presencial_r2
p: 0.141041`, `paga_mordida_encig2025_digital_r2 p: 0.029868` y
`adopta_encig2025_luz p: 0.673393`, las cuatro con
`clase: "MEDIDO·p(tasa base ponderada…)"`. El propio cuerpo de la salida de
arriba las imprime. **Este acto NO trata territorio virgen y no lo presenta
como tal** — su §0.2 de la spec sellada lo dice con el conteo a la vista.

Dos causas mecánicas, verificadas contra el código, no supuestas:

1. **`_tiene_veredicto_real()` no reconoce `MEDIDO`.** Solo acepta los diez
   veredictos de falsación `R` (`VEREDICTOS_REALES` =
   `CORROBORADA`, `NO-DISCRIMINA`, `REFUTADA-COMO-CAUSAL`, …) o un campo
   `veredicto:` con valor. Una regla medida como **tasa base** —el patrón de
   todo el lote F4→F3— no deja ninguna de esas marcas, así que es invisible
   para el veredicto final aunque su `p` MEDIDO esté sellado.
2. **La ventana de ±260 caracteres pierde el veredicto que sí existe.** En
   `tramite.gobierno_digital.util_sin_coercion` el bloque mide 8 946
   caracteres y trae `NO-DISCRIMINA` en el desplazamiento 5 472;
   `_ventana_de_terminos()` recorta a `[0, 268)` alrededor del `id:` y no lo
   ve. Aquí el falso negativo se produce **incluso bajo la semántica estrecha
   del propio script**.

Consecuencia para el guardián, dicha sin adorno: `T-YAMEDIDO` existe para que
ningún acto llame «territorio virgen» a una regla ya medida, y para estas tres
reglas **el guardián habría dejado pasar exactamente ese error**. Queda como
fila `NC` de este acto con sucesor nombrado; este acto **no repara
`ya_medido.py`** — está fuera de su perímetro.

---

## NO-CORRIDO / RESERVAS

| id | qué | por qué | impacto | sucesor |
|---|---|---|---|---|
| `NC-0107` | `RES-0009`/`RES-0011` (`paga_mordida_encig2025_presencial`/`_digital`, rama base `CD`) quedan **sin cita** de adopción | `NO-VERIFICABLE-AQUÍ` | `B-P-PRE-CD` y `B-P-DIG-CD` no reproducen al grano de seis decimales (`−3.227e-05`, `−2.362e-06`; `n` 9 942/6 339 contra 9 937/6 337 declaradas). La regla de desempate de `MAESTRA34-L1` para los 501 `ID_TRA` cuyas filas difieren en `P7_3` no está escrita en ningún artefacto reproducible. `adoptados_activos` sube 4, no 6 | `SIN-ASIGNAR` — acto que documente esa regla de desempate, o que declare la rama `CD` retirada en favor de `SD` |
| `NC-0108` | Los seis complementos (`RES-0004/0010/0012/0014/0016/0022`) quedan **sin cita** | `DECISIÓN-DE-MESA-PENDIENTE` | Son `1 −` el primario sobre denominadores que excluyen categorías reales del reactivo (residuos `0.002258`/`0.219818`/`0.011176`). Seis consumidores siguen `LEGACY-GEN1`; `dependencias_legacy` baja 4, no 10. Patrón `NC-0085` | `SIN-ASIGNAR` — mesa decide si un complemento aritmético puede llevar cita, o si se re-especifica con su denominador en el rótulo |
| `NC-0109` | **`tools/ya_medido.py` da `NUNCA-MEDIDA` para tres reglas medidas y selladas** | `FUERA-DE-PERÍMETRO` | `T-YAMEDIDO` existe para impedir que un acto llame «territorio virgen» a una regla ya medida, y para estas tres **habría dejado pasar exactamente ese error**. Dos causas verificadas contra el código: `_tiene_veredicto_real()` no reconoce `MEDIDO` (solo los diez veredictos `R`), y la ventana de ±260 caracteres pierde el `NO-DISCRIMINA` del desplazamiento 5 472 | `SIN-ASIGNAR` — acto con `tools/ya_medido.py` en su perímetro |
| `NC-0110` | El mapeo canal↔disparador de `tramite.mordida.con_registro` **no cubre el 21.98% del peso** | `DECISIÓN-DE-MESA-PENDIENTE` | `P7_3` tiene ocho categorías; el par presencial `{1}`/digital `{3,4,5}` deja fuera `2` (banco, supermercado, tienda, farmacia) y `6` (módulos móviles): 6 588 eventos. La regla mapea «digital ≈ registro_o_testigos» y «presencial ≈ nadie observa», y ese mapeo no dice nada de quien paga en el banco | `SIN-ASIGNAR` — mesa decide si el par se re-especifica o si se declara su alcance recortado |
| `NC-0111` | El denominador de la familia B **no es el universo de trámites** | `NO-VERIFICABLE-AQUÍ` | `B-COBERTURA = 0.200895`: `P8_4` solo se pregunta a quien declaró algo en 8.3, así que el estimando es `p(este trámite fue el señalado | trámite de alguien que ya declaró corrupción)`. Reserva heredada de GEN1, aquí **contada** por primera vez. Corregirla exigiría un universo que el instrumento no da | `SIN-ASIGNAR` — no reparable con ENCIG; requiere otro instrumento o una re-especificación del consumidor |
| `NC-0112` | Método de IC **sobre ranura vacía**, e IC como límite inferior en B y C | `DECISIÓN-DE-MESA-PENDIENTE` | Nadie pre-registró el método de IC para estas series; lo eligió el ejecutor y se declara (§3.7 de la sellada). 71 (presencial) y 78 (digital) estratos de UPM única en B, 8 en C → `IC-CON-ESTRATOS-DE-UPM-UNICA`: esos IC se leen como **límite inferior de la anchura verdadera**, nunca como IC exactos. La familia A no tiene ninguno | `SIN-ASIGNAR` — mesa fija el método de IC de la serie |
| `NC-0113` | El reactivo 8.3 completo (`A-P-SOLANY = 0.115702`) **no lo cita ningún consumidor**, y el rótulo `paga_mordida` mide solicitud, no pago | `DECISIÓN-DE-MESA-PENDIENTE` | Restringir 8.3 a su primer inciso cuesta `+0.030584`; y de quienes llegan a `P8_6` (`n = 4 883`) solo el **66.29%** entregó algo. El motor ejecuta `0.085118` bajo un nombre que promete pago. Este acto **no renombra nada** ni mueve el `p` | `SIN-ASIGNAR` — mesa decide si el consumidor se re-ancla a `SOLANY`, se renombra, o se deja con la reserva escrita en la cita |

**Cierra este PR:** `NC-0097` (asiento de las tres filas de `cuenta_gen2=SI` de los `CALC-R` del CSV en `decisiones.tsv`, ADENDA 5). `NC-0103` (trío DBF) **no** es de este acto y sigue abierta.

**Piezas del encargo NO ejecutadas:** `P0` — `SUSTITUIDO-POR: ACTO GEN2-PREP-LOTE` (`PR #662`), por ADENDA (2). Absorbe la corrección de `_instrumento()` y la re-derivación de identidad **completas**; **nada queda huérfano** de esa pieza. `CORR-0001` (ENCIG2023, 4 `RESULT`) queda fuera por instrucción explícita de la ADENDA (3): ni se mide ni se declara.

---

## CONSUMIDO

`ACTO GEN2-LOTE-ENCIG-1` cierra con **`PR #664`**
(`https://github.com/Josanoforo/Modelado-Mexicano/pull/664`), rama
`acto/gen2-lote-encig-1`, contra `origin/main = b984531` (`PR #663`).

**Lo que entregó:** la spec sellada `prereg-caja-ENCIG-MORDIDA` v1.0
(`forense/prereg-caja/ENCIG-MORDIDA-spec-v1_0.md`, `sha 00c7c4a6…`), congelada
antes de abrir un byte de microdato; la corrida `data/corrida0/CALC-ENCIG-0001/`
(108 `RESULT`, `PRE-FLIGHT VERDE` → `verify: REPRODUCE` 108/108,
`CONTEXTO=IDENTICO`, `cuenta_gen2 = SI`); control positivo contra GEN1
**`REPRODUCE-4/6`**; y —por primera vez en la cartera F4→F3— el **ciclo entero**:
cuatro citas `corrida0_resultado_id` + `corrida0_generacion: GEN2` escritas en
`milpa/tramite.yaml` con los doce `p` **intactos**, sonda de consumo del emisor
**4/4** en solo lectura, `adoptados_activos` **2 → 6** y `dependencias_legacy`
**203 → 199**.

**Cascada:** `ADR-438` · `L0` recifrado · tres contadores reconciliados con
`tools/cierre_acto.py --aplica` · rótulo `LOTE / GEN2-LOTE-ENCIG-1` censado en
`canon/registro-rotulos.tsv` · `tests/check.py --baseline` **VERDE** ·
`NC-0097` **CERRADA** · `NC-0107`…`NC-0113` abiertas con sucesor ·
nota de cierre en `forense/notas/2026-09-09-GEN2-LOTE-ENCIG-1-cierre.md`.

**Sucesor:** `GEN2-LOTE-ENIF-1`, gateado al merge de este PR.

**El merge de mesa es la firma** — de la adopción (E.2) y del contador
(`cuenta_gen2 = SI`, con OBJETO explícito en el propio encargo).
