ENCARGO · ACTO GEN2-R-SERIE-DBF · LA SERIE SE CERTIFICA DE CERO, TRÍO VIEJO — las tres olas en formato de otra década, donde el codebook manda y el inventario no llega

CABECERA · CAJA (UBUNTU), Opus · NO se lanza en NUBE — sin bytes no hay acto (A.2) · COMPUERTA: GATED a PR del ACTO GEN2-R-SERIE-CSV fusionado — hereda su spec familia y evita dos actos simultáneos en la misma caja (la skill /acto verifica contra origin/main y se niega con A.13 si no está; no arranques a mano para saltártelo) · redactado contra 05f5fc56 (PR #653) · candidatos CALC/FP/NC/ADR: deriva al cierre, no heredes.

FIRMA DE MESA, 9/sep/2026, verbatim (misma pluma que el trío CSV, adentro por dictado de mesa): «Decisión 1 - Más que barata es la mejor? Si es la mejor lo hacemos si no estamos seguro corremos de 0. Decisión 2 - firmemos. la correspondencia puede esperar un día más. La decisión va en el encargo no fuera y mi firma es el merge. Dame los encargos.» — mismo diseño respondido por dirección: correr de 0 con los bytes de la bodega y el GEN1 solo como control posterior. ⚠️ FIRMA DE CONTADOR con OBJETO: cuenta_gen2 = SI para los tres CALC que este acto selle; el acto la escribe con esta cita, el merge la perfecciona.

VERIFICACIÓN DE EXISTENCIA (A.8, contestada por dirección, 9/sep/2026, contra 05f5fc56): (1) ESTRUCTURA — las tres plazas: CORR-0024 ENVIPE 2012 (envipe_2012_base_de_datos_envipe_2012_dbf) · CORR-0028 ENVIPE 2013 (envipe_2013_bd_envipe13_dbf) · CORR-0032 ENVIPE 2015 (envipe_2015_bd_envipe2015_dbf), script tools/arbitra.py, CAJA, RES-0093/0098/0103. Gobiernan además espec-R-ciega-v1_2.tsv (el estimando R) y ENVIPE-DENUNCIA-spec-v1_0 (el secundario homologado), heredados de la familia que el trío CSV selló. (2) CONTENIDO — los tres payloads EXISTEN en el manifiesto con url_origen INEGI (…/2012/microdatos/base_de_datos_envipe_2012_dbf.zip, etc.) y fecha_descarga 2026-08-05: nada que adquirir. corridas-R/CIV-M-01/-02/-04.json → EXISTEN, COMPUTADO (R=0.2590/0.2434/0.2437 — contaminación declarada abajo). ls data/corrida0/ | grep CALC-R al redactar → solo lo que el trío CSV haya creado: las tres celdas de ESTE trío NO-ENCONTRADO — re-verifícalo al abrir contra tu main (A.8 es del que escribe Y del que ejecuta). (3) COBERTURA RETROACTIVA — ⚠️ la que muerde aquí: data/inventario-reactivos-v1_2.tsv trae 0 filas BP1_2x para envipe_2013 y envipe_2015 — y sin embargo las corridas GEN1 computaron sobre esas olas. El inventario NO cubre los payloads DBF (nació del pipeline CSV): un negativo derivado del inventario sería falso para este trío (A.15/A.13 — un comando que no examinó archivos no produce negativos). Toda existencia de reactivo aquí se resuelve abriendo el codebook/descriptor DE LA OLA, nunca el inventario.

CONTAMINACIÓN, DECLARADA (ADR-46). Los tres valores GEN1 están en el repo y dirección los leyó. La spec no elige nada para acercarse a ellos: tabla ciega + codebook por ola, y el COMMIT-1 cierra con «el primer resultado que produzca este procedimiento es el que se reporta».

PIEZAS: P1 · SPEC POR OLA (COMMIT-1, solo codebook/metadato). Extiende la familia R-ENVIPE-SERIE con un spec.yaml por CALC. Aquí el trabajo real es de archivista: (a) el nombre y los códigos del reactivo de razones de no denuncia pueden diferir en 2012/2013/2015 — se mapean POR ARCHIVO desde el descriptor de cada ola (A.15c: hs02g ya enseñó que el mismo nombre significa cosas distintas en libros distintos; aquí aplica al revés, mismo reactivo puede llevar otro nombre); (b) los DBF se abren con lector declarado en dependencias (encoding y anchos verificados contra el descriptor — el patrón del hallazgo 3.4 de ayer: llaves de texto opacas, jamás normalizar a entero); (c) si una categoría del catálogo viejo no mapea limpio a C1/C2 (p.ej. menos códigos en 2012), la spec declara el mapeo y su residuo ANTES de abrir microdato — y si no hay mapeo defendible, esa ola sale NO-CONSTRUIBLE en el estimando secundario con el codebook citado, conservando el primario R si la tabla ciega sí es construible. Los dos desenlaces son entregables. P2 · MEDICIÓN (COMMIT-2). Tres CALC (sugerido CALC-R-CIV-M-01/-02/-04), preflight → run → verify, embudo por ola, diseño con su regla pre-declarada. Control positivo posterior, por script, sobre el punto contra el JSON GEN1 — coincidencia se reporta, discrepancia se reporta con embudo; ninguna de las dos edita la spec hacia atrás (un tercer commit lo diría, E.5). P3 · NOTA DEL LOTE Y LA SERIE COMPLETA. Primer párrafo: los tres R con cadena y sus controles. Después, por primera vez con cadena GEN2 de punta a punta: la serie 2012→2025 en el estimando secundario homologado, con sus IC, sus universos declarados por punto, y la frase que la acota: descriptiva, no adjudicada — la transferencia se contrata en F5. Si el mapeo de códigos obligó a residuos en alguna ola, la serie lo marca en ese punto en vez de esconderlo.

PERÍMETRO Y CONCURRENCIA. Toca: forense/prereg-caja/R-ENVIPE-SERIE* (extensión, sin editar lo sellado por el CSV — sucesión, no reescritura) · data/corrida0/CALC-R-*/ (tres nuevos) · TSV re-derivados · forense/notas/ · forense/no-corrido.tsv (append) · 0-bis · cascada. EN PARALELO puede vivir FIRMAS-ADOPCION-1 (NUBE) y REVISA-CALC — intersección solo en TSV derivados y no-corrido: append/re-deriva y reporta pisadas. «Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.»

CONTADOR: sí — tres CALC con cadena E.2; la firma viaja arriba, con OBJETO.

LO QUE NO HACE: no reescribe los JSON GEN1 ni la familia sellada por el CSV · no adjudica estabilidad ni transferencia · no toca capturas L, marcador, ni milpa/ · no repara el inventario de reactivos para DBF (si su hueco molesta a futuro, es fila NC con sucesor, no arreglo de paso).

SUCESORES: adopción por lote de los seis R en el duelo (F3) · contrato del duelo temporal (F5, con la serie completa a la vista) · si mesa quiere la comparación formal GEN1↔GEN2 de la serie, el activador de delta con este par concreto.

CIERRE · Cascada completa + ## NO-CORRIDO / RESERVAS + ## CONSUMIDO con el PR.

---

## NO-CORRIDO / RESERVAS

Seis filas. Ninguna vacía.

| # | qué (verbatim del encargo) | por qué | impacto | sucesor |
|---|---|---|---|---|
| `NC-0098` | «diseño con su regla pre-declarada» — la variante `U4` (unidad **persona**, `ID_PER`, `FAC_ELE`, `tper_vic2`) que `prereg-caja-ENVIPE-DENUNCIA` define | `FUERA-DE-PERÍMETRO` | Ninguno sobre este acto: la familia `R-ENVIPE-SERIE` mide `U_R` y `U1`, **ambos de unidad delito** sobre `tmod_vic` con `FAC_DEL`, y ningún `RESULT` del trío CSV toca `tper_vic2`. La guardia de `tper_vic2` sale **`NO-APLICA`** por ola — valor declarado, no omisión (`D-15`). Los tres dictámenes GEN1 del trío viejo también son de unidad delito, así que el control positivo tampoco la necesitaba. | acto que necesite `U4` en olas anteriores a 2021; para 2012 ver `NC-0099` |
| `NC-0099` | «se mapean POR ARCHIVO desde el descriptor de cada ola» — declarar la ruta que permitiría construir `U4` en **ENVIPE 2012** | `DIFERIDO-A:SIN-ASIGNAR` | Medido contra el descriptor: `tper_vic.dbf` de 2012 tiene **311 436 filas, las mismas que `tsdem.DBF`** —censo del hogar, no persona seleccionada— y **no trae `N_REN`**. Aislar a la persona seleccionada exigiría un join a `tsdem` por `N_REN == R_SEL` que ninguna spec de esta familia declara. **No se improvisó**: un join nuevo devuelve vacío en vez de error y el denominador se equivocaría en silencio. 2013 y 2015 no tienen el problema. | acto que abra `U4` en olas DBF: debe **declarar** el join a `tsdem` en su spec y verificar su cardinalidad antes de medir |
| `NC-0100` | «no repara el inventario de reactivos para DBF (si su hueco molesta a futuro, es fila `NC` con sucesor)» | `FUERA-DE-PERÍMETRO` | **Corrige de paso la premisa (3) de este encargo**: el inventario **sí** cubre `envipe2012`/`2013`/`2015` a nivel de presencia de columna —400 / 419 / 485 filas, con 12 / 11 / 11 filas `BP1_2*`— y por eso `corrida0 spec-check` da **6 OK · 0 FAIL** en los tres. Lo que falta es `texto_reactivo`, **vacío en las 1 304 filas**. Ningún negativo de este acto se derivó del inventario. | acto con `data/inventario-reactivos-v1_2.tsv` y `tools/inventario_reactivos.py` en su perímetro |
| `NC-0101` | «la serie 2012→2025 en el estimando secundario homologado» — las **ocho** olas que siguen sin medir (2011, 2014, 2016, 2017, 2018, 2019, 2020, 2022) | `DIFERIDO-A:SIN-ASIGNAR` | La serie pasa de cuatro a **siete** puntos sobre trece. El hueco que muerde está entre los años de delito **2014 y 2020**: seis años sin medir, justo donde la serie cambia de nivel. Por eso se publica **descriptiva**. Los ocho payloads **existen** en el manifiesto: no hay nada que adquirir, falta medir. | acto hermano por lote de olas, mismo patrón `GEN2-R-SERIE-<formato>` |
| `NC-0102` | «SUCESORES: adopción por lote de los seis `R` en el duelo (F3)» | `DIFERIDO-A:F3` | Cero adopciones por diseño: ningún `RESULT` de las dos familias se cita en `milpa/`. Los seis quedan como `OFERTA`. `N_resultados_gen2_adoptados_activos` sigue en **2**. | `F3`, por lote y con firma de mesa por merge |
| `NC-0103` | «CONTADOR: sí — tres `CALC` con cadena `E.2`» — la fila en `data/corrida0/decisiones.tsv` | `FUERA-DE-PERÍMETRO` | Mismo caso y mismo desenlace que `NC-0097`: **ningún contador se queda quieto**. El registro ya cuenta los tres porque la firma con OBJETO viaja verbatim en `etiquetas.cuenta_gen2_firma`. `N_corridas_selladas` 11→**14**, `N_resultados_sellados` 901→**1021**, `N_resultados_gen2_sellados` 631→**751**. | el mismo acto que resuelva `NC-0097` |

**Reserva sobre `NC-0094` (adenda de dirección a este acto).** Antes del
`corrida0 registro --escribe` se corrió el diff en seco **con `--verifica`** y se
midió el efecto sobre las columnas `resultado_replay`/`contexto_replay` de las
corridas **ajenas** a este acto: **cero filas ajenas tocadas** —el diff es
`3 + / 0 −` en `corridas.tsv` y `120 + / 0 −` en `resultados.tsv`, y `usos.tsv`
sin diferencia—. Por eso se escribió. Si alguna hubiera cambiado, no se
escribía. La contención de `NC-0094` se respetó y la reparación sigue siendo de
otro acto.

**Reserva sobre `FP-370`.** Sigue **ABIERTA**, y ahora gatea también el estatus
del insumo de estas tres celdas: `forense/prereg-duelo-v2/codificacion-R-v1_0.tsv`
—de donde salen codificación, universo, ponderador y diseño de las **seis**—
continúa en estado `PROPUESTA`. Ninguna cifra de los seis `CALC` cambia por eso.

**Perímetro: una escritura fuera de la lista enumerada, declarada.** El encargo
enumera el perímetro y `tests/` no aparece por nombre. Se tocó
`tests/test_corrida0.py` para mover los tres contadores de `T-STATUS-SMOKES` que
este acto hace avanzar por construcción — misma escritura y misma razón que
declaró `ADR-433`: un contador que el acto mueve y no actualiza deja la suite
roja para el siguiente.

---

## CONSUMIDO

Ejecutado por **`PR #661`** (`ACTO GEN2-R-SERIE-DBF · LA SERIE SE CERTIFICA DE
CERO, TRÍO VIEJO`), rama `acto/gen2-r-serie-dbf`, 9/sep/2026, **CAJA (Ubuntu)
con corpus montado**, Opus.

Ocho commits: 0-bis `658ce39` (encargo recuperado verbatim del transcript de la
sesión que murió a los 74 segundos por reinicio de la máquina) · corrección del
0-bis `c0d0299` (texto canónico de mesa; diff de **una línea** sobre veinte
párrafos idénticos byte a byte) · `COMMIT-1` `894707a` (spec por ola
`R-ENVIPE-SERIE-DBF`, los tres `CALC-R`, el `medidor.py` byte-idéntico y el
script de control, congelados **sin abrir un solo registro de microdato**) ·
`COMMIT-2a` `2951696` / `COMMIT-2b` `dd95bca` / `COMMIT-2c` `7861db2` (las tres
olas selladas, una por commit, cada una con el árbol limpio que el `preflight`
exige) · `COMMIT-3` `a9580ef` (P3, nota del lote, serie de siete puntos,
`NC-0098`…`NC-0103` y cascada `ADR-434`) · merge de `origin/main` y declaración
de la colisión de numeración `2c5cb0d`.

**Lo que este acto entregó:** tres árbitros `R` con cadena `E.2` completa y
control positivo externo con **delta `+0` exacto** contra los tres dictámenes
GEN1; el hallazgo del **corrimiento de `BPCOD` en 2012**, con sus once parejas
verbatim, su residuo nulo declarado y un falsador **estructural** que no usa
resultados; el **vínculo de diseño por ola** que evitó declarar `NO-ESTIMABLE`
dos de tres olas por un falso negativo de nombre; la **corrección contra el
árbol de la premisa (3)** del propio encargo; y la serie homologada llevada de
cuatro a **siete** puntos, descriptiva y con su costura visible.

**Lo que NO entregó** está en `## NO-CORRIDO / RESERVAS`, arriba: seis filas,
ninguna vacía, ninguna huérfana.

⚠️ **`ADR-434` puede pasar a `435` antes del merge.** `PR #660` está abierto con
el mismo número redactado; regla de la casa, **renumera quien fusiona segundo**.
