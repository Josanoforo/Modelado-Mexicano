ENCARGO · ACTO MAESTRA38-N10 · COBERTURA-COMPLETA-OLA6 — invoca /acto

SHA de redacción: 25383f35 · COMPUERTA: N9 fusionado (usa tools/ya_medido.py en su A.8;
verificar por producto: test -f tools/ya_medido.py). ENTORNO: NUBE. NO en CAJA. MODELO:
Fable (diseño de dominio completo; Opus mínimo). CARRILES: ninguno sobre notas de Ola 6.

FIRMA DE MESA — verbatim (4/sep/2026): «Entiendo que hay un mínimo y ese mínimo para
lanzar una ola es una cosa. Pero hoy no tenemos lo mínimo y no quiero hacerlo al mínimo
no después de haber invertido tanto en la infraestructura que creamos.» Traducción
operativa: el producto es el mapa completo de cada dominio —toda regla, no la más
cercana— y el plan para cubrirlo entero; el criterio 2 de §3.a se reporta como
consecuencia, nunca se optimiza.

A.8 contra 25383f35. Universo derivado del canon (§3.2 trabajo, §3.4 salud, §3.6 tiempo,
§3.8 cooperación, §3.9 información, §3.10 comunicación): ~30 reglas — el acto deriva la
lista exacta por comando en COMMIT-1 y la congela. Insumos en repo: reevaluación
2026-09-03 (criterio 2 y razón verbatim por dominio), mapeo-ola6-N5 (veredicto A.4 por
regla), N5 §1.3 (criterio a/b/c) y §2.6/§2.8 (método de reformulación), N6 (carga como
«tercera formulación complementaria»), inventario v1_1 (42 548 filas) + busca_reactivos,
ya_medido.py por cada id ANTES de escribir su fila. Cinco reglas ya clasificadas por
N5/N6 no se reclasifican: se citan.

SPEC — dos commits, sello «el primer resultado que produzca este procedimiento es el que
se reporta».

COMMIT-1 · UNIVERSO Y CRITERIO, antes de mirar el inventario.
  (a) Tabla dominio × regla: id, tier, texto SI…ENTONCES…PORQUE verbatim, antecedente(s)
      y desenlace separados, salida de ya_medido.py.
  (b) Criterio de clasificación por regla, cerrado: MEDIBLE-COMO-ESTÁ (antecedente y
      desenlace en la misma persona en algún instrumento del corpus) · REFORMULABLE
      (existe reactivo para una consecuencia observable del antecedente O para otro
      desenlace del mismo driver; conserva driver y signo; cambia una sola cosa) ·
      CON-CANDIDATA (instrumento identificado fuera del corpus, con ficha) ·
      HIPÓTESIS-SIN-INSTRUMENTO (ningún instrumento nacional lo mide; se escribe el
      instrumento mínimo: una pregunta, una población).
  (c) Regla de honestidad: si conservar el driver exige un reactivo que no existe, no
      es REFORMULABLE aunque haya algo parecido. Ruido de substring no cuenta (N5 §2.0).

COMMIT-2 · CLASIFICACIÓN CON EVIDENCIA, regla por regla, las ~30.
  Por regla: clasificación, reactivos (id, instrumento, texto copiado del inventario,
  n aproximado), y para REFORMULABLE el objeto reformulado + se_mueve_si + qué
  sostiene/refuta; para CON-CANDIDATA la ficha; para HIPÓTESIS el instrumento mínimo.
  Por dominio, el PLAN DE COBERTURA COMPLETA: (i) reglas medibles hoy → specs a sellar
  en nube (S6…, patrón N7), (ii) adquisiciones necesarias → filas de cola candidatas,
  (iii) hipótesis declaradas → salen del denominador, (iv) el criterio 2 como
  consecuencia: «con (i) el dominio queda en k de n; con (i)+(ii) en k' de n». Un
  dominio se declara COMPLETABLE (toda regla en i, ii o iii con ruta escrita) o
  INCOMPLETABLE (alguna regla sin ruta ni instrumento mínimo formulable — se dice cuál).

CIERRE. Nota forense/notas/2026-09-0X-MAESTRA38-N10-cobertura-ola6.md con las seis
tablas y una tabla resumen dominio → n reglas → medibles / reformulables / candidatas /
hipótesis → COMPLETABLE. FP-303 · «mesa firma el plan de cobertura por dominio» (vence
7 días), con el costo por dominio a la vista: specs (nube), mediciones (caja),
adquisiciones (mesa). Cero cambios en canon ni propuesta: N-siguiente propaga lo firmado
y sella specs por dominio. Hallazgos: una línea por regla que N5/reevaluación clasificó
distinto de lo que ya_medido.py devuelve.

PERÍMETRO. Toca: la nota · tablero (FP-303 + recibo) · A.3 · cascada. NO toca: canon/**
(salvo ADR) · milpa/** · forense/prereg-caja/ · data/** · cola. Si te encuentras
escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo
vale más que el atajo.

FP/ADR: ADR-341 (340 es N9) · FP-303 (decisión) · FP-304 recibo. CONTADOR: reglas de
Ola 6 con clasificación y ruta 2 → ~30 (declara el real) · dominios con plan de
cobertura completa 0 → 6 · medición de modelo: cero — diseño, declarado.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-N10 · COBERTURA-COMPLETA-OLA6` (5/sep/2026,
entorno **NUBE**, rama `claude/cobertura-ola6-maestra38-ef9l8m`), SHA de
redacción `25383f35` (= `origin/main` exacto al arrancar, sin desfase).
COMPUERTA `N9 fusionado` verificada por producto: `test -f tools/ya_medido.py`
contra `origin/main` → existe (`9e767a8`, `PR #538`). CUMPLE.

**Universo (COMMIT-1), congelado por comando.** `canon/modelo-decision-v4_0.md`
§3.2/§3.4/§3.6/§3.8/§3.9/§3.10 traen **25** reglas — el encargo estimaba
`~30`; **el real, derivado y verificado dos veces (conteo de bullets por
rango de línea + cruce contra el `REGISTRO` congelado de
`tests/validador_registro_ids.py`), es 25 — se declara.** `tools/ya_medido.py`
corrido en las 25 antes de clasificar (A.8): `NUNCA-MEDIDA` en las 25, sin
excepción — sin discrepancia contra `MAESTRA34-N5`/`MAESTRA36-N6` (preguntan
existencia de reactivo, no falsación real corrida; las dos lecturas
coinciden, declarado en `§5(a)` de la nota).

**Clasificación con evidencia (COMMIT-2), tres universos independientes por
regla.** `MAESTRA34-N5` (encuestas `v1_2`/`ext`, 241 591 filas) +
`MAESTRA36-N6` (administrativo, `data/manifiesto.yaml`, 1 104 entradas) +
**este acto** (`descargas_mx_v1_1`, 42 536 filas examinadas, 75 corridas —
tercer universo que ninguno de los dos primeros tenía asignado). Resultado:
**3 `MEDIBLE-COMO-ESTÁ`** (`salud.atencion.grave`, `salud.vacunacion.
disponible` — ya conocidas por N5 — y `comunicacion.inseguridad.ver_oir_
callar`, **hallazgo nuevo** vía módulo `AOJ` de LAPOP AmericasBarometer,
población general, no restringida a violencia de género), **3
`CON-CANDIDATA`** (`salud.adherencia.desabasto_vs_cuidadora` vía `N36`/Cero
Desabasto, ya registrada `CANDIDATA/PENDIENTE_EVIDENCIA`; `cooperacion.
comite.monitoreo_sancion_visible` y `cooperacion.faena.sancion_social_
pueblo_mestizo` vía CNGMD, pendientes de abrir bytes), **19
`HIPÓTESIS-SIN-INSTRUMENTO`** con instrumento mínimo escrito cada una.
`REFORMULABLE` queda en cero, honestamente: se intentó para las 17
`EXISTE-NO-SATISFACE` originales (10 de encuesta + 7 administrativas) y
ninguna sobrevivió la regla de honestidad (c) salvo la que resultó
`MEDIBLE-COMO-ESTÁ`. Detalle completo, seis tablas por dominio y tabla
resumen: `forense/notas/2026-09-05-MAESTRA38-N10-cobertura-ola6.md`.

**Criterio 2, como consecuencia — no se optimizó.** Con lo medible hoy: `0`
de `6` dominios (`≥3 EXISTE-SATISFACE`). Sumando las 3 adquisiciones con
ficha ya identificadas: **sigue en `0` de `6`** — ningún dominio llega a 3
agotando todo lo nombrable hoy; el techo teórico más alto es `salud` y
`cooperación` (2 de sus reglas cada uno, y dos de esas cuatro requieren
además un diseño multinivel persona↔municipio). **Pese a eso, los 6
dominios se declaran `COMPLETABLE`**: las 25 reglas, sin excepción, tienen
ruta escrita — medir hoy, adquirir con ficha, o instrumento mínimo de
hipótesis. Ningún dominio queda `INCOMPLETABLE`.

**Hallazgos.** Tres líneas en `forense/hallazgos.md` (5/sep/2026): (a) cero
discrepancia entre `MAESTRA34-N5`/`MAESTRA36-N6` y `tools/ya_medido.py`
sobre las 25 — declarada, no omitida, tal como el SPEC lo pedía; (b) la
subida de `comunicacion.inseguridad.ver_oir_callar` de `EXISTE-NO-SATISFACE`
a `MEDIBLE-COMO-ESTÁ` al cruzar `descargas_mx_v1_1` — alcance de inventario,
no error de N5/N6; (c) catálogo de homonimias de `busca_reactivos.py`
repetidas entre reglas ("jefe"=jefe de hogar, "cortes"=tribunales/apagones,
"favor"=guion de enumerador, "grave"=problema nacional en LAPOP), para que
un `/mapea` futuro no repita la formulación ya descartada.

**Cascada.** `ADR-341` (`canon/gobernanza-v1_15.md` §4, candidato derivado
contra el máximo real `340`, contiguo — coincide con el que el propio
encargo ya citaba, «340 es N9»; cabecera de conteo `340`→`341 ADR`).
`canon/estado-programa-v1_12.md`: `L0` gana la anotación de `ADR-341`
(insertada antes de la de `ADR-340`, sin reescribirla) y sube `340`→`341
ADR`; cabecera de conteo de `gobernanza` en la tabla de fuentes (línea 27)
recifrada igual. `canon/registro-rotulos.tsv`: fila `MAESTRA38-N10` censada,
junto a N2/N3/N4/N6/N8/N9. `forense/firmas-pendientes.tsv`: `FP-303`
(decisión de mesa, `ABIERTA — pendiente de firma`, vence 7 días,
12/sep/2026, informativo) y `FP-304` (recibo). `forense/tablero/
TABLERO-PROGRAMA.md` (nota inline) y `forense/tablero/TABLERO-PROGRAMA-
v1_1.md` (§8.9): recibo de este acto.

**Qué NO decide.** No cambia ningún dominio a `ACTIVO`. No relaja ni
reinterpreta el criterio 2 de `motor-nucleo-medible-v1_0.md` §3.a. No sella
ninguna de las 3 filas `MEDIBLE-COMO-ESTÁ` (propuesta — mesa/dirección
revisa, mismo estándar que las 2 originales de N5). No adquiere ningún
payload ni escribe fila de cola real (`data/**`/cola fuera de perímetro —
las fichas de la nota son recomendación textual, no inserción). No
reclasifica las 5 reglas de `FP-298` (`MAESTRA38-N5`/`N6`, otro dominio,
citadas solo como precedente de método en `§1.2` de la nota). No toca
`canon/modelo-decision-v4_0.md`, `milpa/**`, `forense/prereg-caja/` ni
`data/raw`.

**Verificación.** `python3 tests/check.py --baseline`: **LÍNEA BASE VERDE**,
3 FAIL / 170 WARN — sin cambio frente a la línea base de `MAESTRA38-N9`
(este acto no cierra `FP` alguna que `T22` cuente, no cambia conteos de
`T25`/`T-YAMEDIDO`: el propio encargo, tras esta sección `## CONSUMIDO`, ya
trae `NUNCA-MEDIDA` en su cuerpo, satisfaciendo `T-YAMEDIDO` sin necesitar
allowlist).

**Contador.** Reglas de Ola 6 con clasificación y ruta: **25** (no `~30`,
declarado). Dominios con plan de cobertura completa: **6** (`0`→`6`,
cumplido). Medición de modelo: **cero** — diseño, declarado, cumplido.

PR de este acto, contra `main`.
