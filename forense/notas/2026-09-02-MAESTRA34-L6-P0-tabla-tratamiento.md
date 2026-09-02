# `ACTO MAESTRA34-L6 · CIVICA-HOMOLOGACION-ESCALONADA` — `P0`, tabla de tratamiento

2/sep/2026 · entorno **UBUNTU** · `COMPUERTA: GATED a MAESTRA34-L5` (verificada) ·
Encargo: `forense/encargos/2026-09-02-MAESTRA34-L6-CIVICA-HOMOLOGACION-ESCALONADA.md`
(`SHA de redacción 29ab80a`, archivado verbatim por A.3 en el primer commit).
Ejecutado con `/acto` (`ADR-237`).

**Este commit no contiene ningún resultado electoral.** Sólo calendario y cargos.
Ningún archivo de resultados fue abierto ni descargado antes de él.

---

## 0 · Compuerta, verificada por producto

```
$ git log -5 --oneline origin/main
11af678 Merge pull request #467 from .../acto/maestra34-l5-gobierno-digital-evasion-ahorro
$ git show origin/main:milpa/tramite-ola5-propuesta-v0.yaml | grep -n "util_sin_coercion_encig2025\|evasion_norma_envipe2025\|tiene_ahorros_enif2024"
684:  - id: tramite.gobierno_digital.util_sin_coercion_encig2025
742:  - id: tramite.evasion_norma_envipe2025
803:  - id: dinero.ahorro.tiene_ahorros_enif2024
```

Las tres entradas que `MAESTRA34-L5` debía producir están en `origin/main`. Compuerta
**CUMPLIDA**. Base del acto: `origin/main = 11af678`, 18 commits por delante del
`29ab80a` que el encargo declara (main se movió; no es PARO — se re-derivó el perímetro
contra el árbol nuevo).

## 1 · A.8, contra el árbol de este acto

Las cinco premisas del encargo se re-corrieron y las cinco son **ciertas**:

| premisa del encargo | comando | salida |
|---|---|---|
| TEPJF `NO-ENCONTRADO` | conteo de `tepjf` en `data/manifiesto.yaml` | **0** (control positivo: 18 884 líneas leídas, `concurren`=sí, `sicee`=5) |
| SICEE 5 menciones | conteo de `sicee` en `data/manifiesto.yaml` | **5** |
| calendario de homologación `NO-ENCONTRADO` | `grep -ril "homologaci" data/ forense/` | `forense/encargos/2026-09-02-MAESTRA34-N9-…md`, `forense/notas/2026-08-20-act-pil-2-marco.md` — **ninguna tabla** |
| 16 payloads OPLE de `L4` existen | ids `iec_coahuila_*`, `ieem_edomex_*` en manifiesto | presentes |
| crosswalk sección→municipio 2016 existe | `ine_mge_2016_*` | presente |

**A.13 del negativo:** el barrido que produjo esos conteos leyó, byte a byte y sin
depender de `ugrep`, **2 810 archivos / 206 681 585 bytes** del árbol (excluyendo
`.git` y `data/raw`). Un negativo de este barrido sí es un negativo.

## 2 · Lo que se encontró antes de buscar nada: SICEE no está caído, esta caja está bloqueada

`siceef.ine.mx` devuelve **403 con 163 097 B**, y el cuerpo es una página del Centro de
Atención a Usuarios del INE cuyo texto visible dice, verbatim:

> AVISO · No tiene acceso permitido a la URL que intentas consultar. […] **Bloqueo IP:
> 187.13.205.53** · ID: a34e53c2eda946e8

**La misma página, con la misma IP, sale en los cinco hosts probados**:
`siceef.ine.mx`, `siceen21.ine.mx`, `computos2024.ine.mx`, `portalanterior.ine.mx` y
`prep2021.ine.mx`. `www.ine.mx` (**200**, 203 456 B) y `repositoriodocumental.ine.mx`
(**200**, 755 791 B) **no** lo sufren.

Esto **corrige el registro** de tres actos previos, que atribuyeron el mismo síntoma a
otras causas: `MAESTRA34-A1` (`ADR-278`) y `MAESTRA34-L3` (`ADR-280`) anotaron
«SICEE = Tableau» y `MAESTRA34-L4` (`ADR-284`) anotó «`computos2024` con 403 de
Cloudflare». No es Tableau ni Cloudflare: es **un bloqueo de IP del propio INE contra la
IP de salida de esta caja**, declarado en el cuerpo de la respuesta. Consecuencia
operativa, que vale para todo acto futuro: **ninguna ruta programática del INE distinta
de `www.ine.mx` y del repositorio documental sirve desde esta caja**, y el remedio no es
otro `curl` — es navegador (receta) u otra IP.

## 3 · La fuente que sí sirve, y por qué es primaria

El encargo manda derivar el calendario «de fuente primaria (SICEE/OPLE/DOF), no de
memoria». SICEE está bloqueado; el DOF (`dof.gob.mx`, **200** — ojo, `www.dof.gob.mx`
falla en TLS) publica el decreto federal de 2014 pero **no** las fechas locales, que son
de derecho estatal; y los 32 OPLE son 32 portales. La fuente primaria que cubre las 32
entidades de una sola vez es la **tercera pata legal del mismo hecho**: el INE, que
co-organiza cada Proceso Electoral Local, aprueba por acuerdo del Consejo General el
**Plan Integral y los Calendarios de Coordinación** de cada ciclo, y ese acuerdo declara,
entidad por entidad, los **cargos a elegir** y el calendario completo de actividades.

Se localizaron por la **API REST de DSpace 6.4** del Repositorio Documental del INE
(`/rest/handle/123456789/<id>?expand=bitstreams`), que sí responde. **30 payloads**
`OBTENIDO`, uno por anexo, cubriendo **todos los ciclos de 2015 a 2025**:

| jornada | acuerdo del CG del INE | handle | anexo usado |
|---|---|---|---|
| 2015 | ordinaria 18/dic/2014 | `87134` | acuerdo (PDF + txt) |
| 2015 (extraordinarias) | extraordinaria 14/oct/2015 | `79710` | acuerdo (txt) |
| 2016 | extraordinaria 16/dic/2015 | `87457` | acuerdo, **considerando 20** |
| 2017 | extraordinaria 7/sep/2016 | `85998` | anexo 1 (calendarios por entidad) |
| 2017 (extraord.) | extraordinaria 14/oct/2016 | `86038` | anexos 1 y 2 |
| 2018 | extraordinaria 8/sep/2017 | `93570` | anexo 2 (**30 hojas, una por entidad**) |
| 2019 | extraordinaria 6/ago/2018 | `97991` | anexos 1-5 (Ags, BC, Dgo, QRoo, Tamps) |
| 2019 (Puebla extr.) | 2ª extraordinaria 6/feb/2019 | `101943` | anexo 2 |
| 2020 | extraordinaria 30/sep/2019 | `112696` | anexos 1-3 (Coahuila, Hidalgo) |
| 2021 | extraordinaria 7/ago/2020 | `114312` | anexo 1 (**32 hojas**) + anexo 2 |
| 2022 | ordinaria 28/jul/2021 | `122210` | anexo 1 (Concentrado) |
| 2023 | extraordinaria 26/sep/2022 | `143140` | anexo C (Concentrado) |
| 2024 | extraordinaria 20/jul/2023 | `152565` | anexo 2 (**32 hojas, con «Cargos a elegir»**) |
| 2025 | ordinaria 26/sep/2024 | `176887` | anexo 2 (Calendario) |

**A.7 cumplida en las 30**: doble descarga, `sha256` **idéntico en las dos** (23 por la
ruta REST + 7 por la ruta `xmlui/bitstream`, 0 diferencias). Estructura de contenedor
verificada: `zipfile.testzip()=None` en los 23 XLSX/XLSM, `%PDF`+`%%EOF` en los PDF,
decodificación UTF-8 estricta en los `.txt`. **Una anomalía declarada**: el bitstream
`CGex202110-20-ap-4-Calendario.xlsx` (handle `125406`) **es un PDF servido con extensión
`.xlsx`** — `%PDF` en el byte 0, `%%EOF` al final, 187 717 B. No está roto; está mal
nombrado en origen. Registrado como `formato: pdf`.

**Anti-PR#77**: los 30 viven en `/home/pc0/mm-corpus/raw/electoral_calendario_pel_ine/`,
no en el worktree. `data/manifiesto.yaml` **953 → 983** (+30).
`tests/manifiesto.py --verifica`: `data_raw: coincide=872 · no_coincide=0 · ausente=0`.

## 4 · Cómo se lee «hubo elección de ayuntamientos», y la trampa que trae la fuente

`tools/p0_calendario_pel.py` no cree el rótulo: exige que la **actividad** nombre a la vez
el cargo municipal (`ayuntamiento|alcaldía|presidencia municipal|junta municipal|concejal|
regiduría|sindicatura`) y un acto electoral (`campaña|precampaña|registro|candidatura|
topes de gastos|coalición|cómputo|boleta|apoyo ciudadano|plataforma`). «Órganos
Municipales» queda **fuera a propósito**: nombra la estructura desconcentrada del OPL, no
la elección.

Esa exigencia atrapó un defecto documental real. La hoja **`Veracruz`** del anexo del PEL
2023-2024 declara en su fila 2, verbatim, **«Cargos a elegir: Gubernatura, y
ayuntamientos»** — y su calendario de actividades tiene **cero** actividades municipales,
mientras las 31 hojas restantes con ayuntamientos traen todas «Campaña para
Ayuntamientos». La contradicción se resolvió **con una tercera fuente, no a ojo**: el
anexo del PEL **2024-2025** (handle `176887`) contiene exactamente dos entidades, Durango
y **Veracruz**, y Veracruz trae ahí **17 actividades municipales**. Luego los
ayuntamientos de Veracruz se eligieron en la jornada de **2025**, no en la de 2024, y el
rótulo del anexo 2023-2024 es un error de la hoja del INE. **Si se hubiera leído el
rótulo en vez de la actividad, Veracruz habría entrado al universo con una elección
municipal que no existió.**

## 5 · La concurrencia se lee de la fecha de jornada, no del año

Chiapas obliga a esa distinción. El acuerdo del CG de 14/oct/2015 (handle `79710`) dice,
verbatim: **«el 19 de julio de 2015 se celebró la elección de diputados y ayuntamientos
del estado de Chiapas»** — año federal, jornada **distinta** de la federal del 7 de junio.
La tabla lo registra como excepción documentada, con su cita, y no como un `SI` derivado
del año.

**Verificación A.13 de que no hay más excepciones en la ventana.** Para cada ciclo se
extrajo la fecha de **fin de la última campaña** de cada entidad (la actividad está en
todos los anexos). Si una entidad hubiera votado otro día, su campaña habría terminado
otro día:

| ciclo | entidades leídas | fechas distintas de fin de campaña |
|---|---|---|
| 2018 | **30** | `['2018-06-27']` |
| 2019 | 5 | `['2019-05-29']` |
| 2020 | 2 | `['2020-06-03']` |
| **2021** | **32** | `['2021-06-02']` |
| 2022 | 6 | `['2022-06-01']` |
| 2023 | 2 | `['2023-05-31']` |
| **2024** | **32** | `['2024-05-29']` |
| 2025 | 2 | `['2025-05-28']` |

**Una sola fecha por ciclo, en los tres años federales con anexo por entidad.** No hay
ninguna entidad desfasada en 2018, 2021 ni 2024. La única excepción de la ventana es
Chiapas 2015. (Nota: el `2020-06-03` del ciclo 2019-2020 es el calendario **aprobado en
septiembre de 2019**, anterior al aplazamiento por COVID que llevó la jornada de Coahuila
e Hidalgo al 18/oct/2020; 2020 no es año federal, así que el aplazamiento no cambia la
clasificación de concurrencia.)

## 6 · La tabla

`data/p0-calendario-ayuntamientos-v1_0.tsv` — **146 filas** (entidad × jornada), con
fuente, hoja, acuerdo y handle por fila.
`data/p0-tratamiento-homologacion-v1_0.tsv` — **32 filas**, una por entidad.

| estatus | entidades |
|---|---|
| **TRATADO** (tiene elección municipal no concurrente **y** concurrente en la ventana) | **14** |
| SIEMPRE-CONCURRENTE-EN-VENTANA | 17 (16 con 2015 indeterminado + Puebla) |
| **NUNCA-TRATADO** | **1** (Durango) |

**Cohortes de tratamiento** (`g` = primer año en que la elección municipal de la entidad
fue concurrente, habiendo sido no concurrente antes):

| cohorte | n | entidades | «antes» observado |
|---|---|---|---|
| **`g2018`** | **8** | Chiapas, Chihuahua, Coahuila, Oaxaca, Quintana Roo, Sinaloa, Tamaulipas, Zacatecas | 2015 (Chiapas), 2016 (seis), 2017 (Coahuila) |
| **`g2021`** | **5** | Aguascalientes, Baja California, Nayarit, Tlaxcala, Veracruz | 2016, 2017, 2019 |
| **`g2024`** | **1** | Hidalgo | 2016, 2020 |
| nunca tratado | 1 | Durango | 2016, 2019, 2022, 2025 (las cuatro no concurrentes) |

**14 estados tratados con antes y después dentro de la ventana** — por encima del mínimo
de **≥8** que el encargo declara para que `P3` no corra acotado.

## 7 · Lo que la tabla obliga a decir sobre la identificación, antes de medir

Esto no es un resultado; es una consecuencia aritmética de la tabla de P0, y se escribe
**aquí**, antes de tocar un solo dato de participación, porque cambia el estimando.

**En los años federales 2018, 2021 y 2024 no existe ni un municipio no tratado.** El §5
lo mide: una sola fecha de jornada por ciclo, en las 30 / 32 / 32 entidades. Como todas
las elecciones locales se celebran el primer domingo de junio, «concurrente» equivale a
«el año de la elección municipal es año federal», salvo Chiapas 2015. Por lo tanto el
tratamiento es **colineal con el año** dentro de la ventana, y el control que la firma de
mesa propone —«control de "año presidencial" dado por los estados no tratados en el mismo
año»— **no existe para 2018, 2021 ni 2024**; sólo existe para 2015, y sólo lo aporta
Chiapas.

Una especificación con efectos fijos de **año electoral** absorbería el tratamiento
entero. El diseño escalonado sigue identificando, pero por otras tres palancas, todas
verificadas en la tabla de arriba y ninguna disponible para `MAESTRA34-L4`:

1. **Escalonamiento real**: tres cohortes (`g2018`, `g2021`, `g2024`) cuyos «antes» caen
   en años distintos (2015, 2016, 2017, 2019, 2020), de modo que el contrafactual de cada
   cohorte se toma de las entidades **aún no tratadas**, no de un año calendario común.
2. **Concurrencia de intermedia contra concurrencia de presidencial**: `g2021` se trata en
   una elección **intermedia** (sin presidencia en la boleta) y `g2018`/`g2024` en una
   **presidencial**. Si el efecto fuera «atención de año presidencial» y no «misma
   boleta», `g2021` tendría que dar mucho menos. Es el contraste que separa las dos
   lecturas que `L4` dejó confundidas, y existe porque el escalonamiento lo creó.
3. **Un control nunca tratado con serie propia**: Durango, con cuatro elecciones
   municipales consecutivas (2016, 2019, 2022, 2025) **todas** no concurrentes, más
   Chiapas 2015 como única elección municipal no concurrente celebrada en un año federal.

La spec congelada de `P2` declarará el estimador sobre esta base y **no** incluirá efectos
fijos de año electoral saturados, porque la tabla de P0 demuestra que no son estimables
junto al tratamiento.

## 8 · Lo que P0 no determinó, dicho como falta y no como cero

Para la jornada de **2015** los acuerdos del CG enumeran las entidades con jornada local
coincidente con la federal (BCS, Campeche, Colima, Chiapas, Distrito Federal, Guanajuato,
Guerrero, Jalisco, México, Michoacán, Morelos, Nuevo León, Querétaro, San Luis Potosí,
Sonora, Tabasco y Yucatán) y los cargos **en conjunto** («gobernador, diputados locales
y/o ayuntamientos»), pero **no** entidad por entidad: el ciclo 2014-2015 es el único cuyos
anexos por entidad no están publicados como hoja de cálculo en el repositorio. Esas 16
entidades quedan `INDETERMINADO` en 2015 y su estatus se declara
`SIEMPRE-CONCURRENTE-EN-VENTANA-CON-2015-INDETERMINADO`, **no** «sin elección». No afecta
a ninguna de las 14 tratadas: sus «antes» están todos documentados a nivel de cargo.

Sí quedaron documentadas a nivel de cargo, por el texto del acuerdo, cuatro elecciones
municipales de 2015: Chiapas (19/jul, diputados y ayuntamientos), Michoacán (112
ayuntamientos), Guerrero (Tixtla) y Querétaro (Huimilpan) — las tres últimas por vía de
las extraordinarias que el acuerdo relata.
