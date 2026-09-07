# `ACTO MAESTRA38-LOTE-CRUCE` · COMMIT-2 · Resultados

`A3-cruce + N16 + C + ENVIPE + COERCITIVO + LAPOP-21/23`. Corrida 6/sep/2026,
**CAJA (Ubuntu, corpus montado, red disponible pero no usada)**, contra
`origin/main` `b1be1438634e87cfc68b5ee1e27db0bd92617ac1`. Encargo verbatim en
`forense/encargos/2026-09-06-MAESTRA38-LOTE-CRUCE.md`; universo por pieza
congelado en `forense/prereg-caja/S11-CRUCE-spec-v1_0.md` (`.sha256`
`c78a894d…`), COMMIT-1 anterior a abrir un solo archivo de datos.

**Las seis piezas cerraron. Ninguna PARÓ.** Medición: cero — este acto no
emite `p`, no mueve ningún tier, no toca `milpa/tramite*.yaml`, ni el
manifiesto, ni la cola, ni `relaciones.tsv`.

---

## §0 · Lo que hay que leer antes que los resultados: cuatro premisas del encargo que no se reprodujeron

Están todas en `S11-CRUCE-spec-v1_0.md §0`, con el comando y la salida. Aquí
sólo lo que cambia una decisión:

1. **`data/inventario-reactivos-descargas-mx-v1_2.tsv` ya existía en `main`**,
   como copia byte-idéntica de `v1_0` (28 949 líneas contra las 42 548 de
   `v1_1`). `S11 §0.1`, escrita en COMMIT-1, lo leyó como «`v1_2` está por
   debajo de `v1_1`» y anunció reconstruirlo como superconjunto de `v1_1`.
   **Eso era falso, y la corrección es de este COMMIT-2** — ver §0-bis. La
   spec está congelada con su `.sha256` y **no se edita**; se corrige aquí,
   que es donde el registro de la casa manda corregirla.
2. **Las tres fuentes de A4 y la base de protesta no están bajo
   `descargas_mx`, sino bajo `data_raw`** (campo `raiz:` del manifiesto, y el
   disco). La pieza (a) corrió donde están.
3. **La lista C de 29 relaciones está en A6 `§4.3`, no en `§3`, y es un
   desglose por fuente, no una lista de filas.** Se derivó de
   `relaciones.tsv` y el desglose resultante cuadra celda por celda con el de
   A6, incluidas sus dos anotaciones («MMAD bajo dos nombres», «MICROCREDIT
   ×2»).
4. **LAPOP 2021/2023 no tenían «0 filas en el inventario».** Tenían 262 y 585,
   **con texto**, desde `v1_1` (3/sep). Ver §6: la pieza (f) no se cancela,
   se reorienta a lo que sí estaba sin verificar, y ahí encuentra algo peor.

---

## §0-bis · Corrección de este COMMIT-2 a su propio COMMIT-1: `v1_1` **no** contiene a `v1_2`

`S11 §0.1` supuso que reconstruir `v1_2` desde `v1_1` no perdía nada, porque
`v1_2` era copia de `v1_0` y la ficha de `v1_1` en `data/INFRAESTRUCTURA-v1_0.md`
dice que `v1_1` trae «los **116** `payload_id` de `v1_0` … idénticos byte a
byte». **La diferencia de conjuntos dice otra cosa**, y se midió antes de
escribir el archivo final:

```
v1_1 (filas únicas)                    42 515
v1_2 anterior (filas únicas)           28 923
v1_2 anterior \ v1_1                    9 443      <-- se habrían PERDIDO
v1_1 \ v1_2 anterior                   23 035
intersección                           19 480
```

Las **9 443** filas son las de `UNIVERSO-2026-09/` que `ACTO MAESTRA38-A1`
depositó (ENADIS, MOTRAL, ENCO, ENCRIGE, CONEVAL, ENJUVE, ENVE, ENH,
Intercensal 2015) y que `v1_1` —anterior a ese acto— no podía tener.
**Ninguna de las dos versiones contiene a la otra**: `v1_2` no era «`v1_1`
menos filas», era **otro linaje**. El número de versión más alto no señalaba
ni más ni menos contenido, señalaba **otro corte**.

`v1_2` queda entonces como **unión verificada de tres conjuntos**, no como
superconjunto de uno: `v1_1` (42 515) ∪ `v1_2` anterior (28 923) ∪ filas
nuevas de este acto (24 169) = **76 127 filas únicas**. `v1_1` intacto
(`git diff --stat` sobre él: vacío) y el contenido del `v1_2` anterior
íntegro dentro del nuevo.

**Esto es exactamente el defecto que `S11 §2` describe para los reactivos,
aplicado a los archivos:** dos objetos con el mismo rótulo de familia y
números de versión consecutivos no son comparables por el rótulo. Si este
acto hubiera confiado en su propio COMMIT-1 en vez de medir la diferencia,
habría borrado 9 443 filas en silencio y ningún test lo habría visto.

---

## §1 · Contador del acto

| contador pedido | resultado |
|---|---|
| instrumentos mínimos de Ola 6 con cobertura conocida | **8 de 19** — y las ocho son `PARCIAL`. **`CUBIERTO-POR`: 0.** 11 `SIN-COBERTURA-EN-ESTAS-FUENTES` |
| constructos R7 con instrumento fuera de MPS | **3 de 3** — los tres `CUBIERTO`, y ninguno por LAPOP |
| antecedentes de `C_agravio` en ENVIPE | **2 de 3** (`AGRAVIO` ✓, `FALLA_ESTATAL` ✓, `RED_PREVIA` ✗). Veredicto de pieza: **`NO-CUBRE`** — porque falta el desenlace, no sólo un antecedente |
| relaciones `NO-ENCONTRADO` con paralela | **24 de 29** (14 `PARALELA-CUBRE` + 10 `PARALELA-PARCIAL`); 5 `NINGUNA-EN-CORPUS`. Por constructo: 6 de 10 con paralela completa |
| coercitivo con instrumento | **0** — `SIN-COBERTURA`, con control positivo |
| reactivos inventariados de LAPOP 2021/2023 | **262 + 585 = 847**, ya presentes desde `v1_1`; **0 nuevos**. Controles verificados contra el `.dta`: **4 de 10 presentes** |
| medición | **cero** (cruce) |

**Inventario:** `data/inventario-reactivos-descargas-mx-v1_2.tsv` = unión de
`v1_1` (42 515 únicas) ∪ `v1_2` anterior (28 923) ∪ **24 169 filas nuevas** =
**76 127 filas únicas** (§0-bis); 15 598 de las nuevas traen texto. `v1_1` no
se tocó (`git diff --stat` sobre él: vacío).

---

## §2 · Pieza (a) — A3-cruce: 0 de 19 cubiertos, y por qué eso es el resultado, no la falta de uno

`data/cruce-ola6-v1_0.tsv`. Universo: 122 archivos de las cuatro fuentes,
22 969 filas inventariadas, **15 141 con texto**.

**Dos de las cuatro fuentes no pueden producir `CUBIERTO-POR` por
construcción, y se declara antes de leer los veredictos:** `ecopred2014`
(1 110 filas) y `A6_MMAD_PROTESTA_MEXICO` (31 filas) tienen **0 filas con
texto** — el `.dbf` de ECOPRED no lleva etiquetas y el `.csv` de MMAD tampoco.
Por `S11 §2`, un nombre de variable sin texto nunca produce `CUBIERTO-POR`.
De las cuatro fuentes que el encargo nombra, sólo dos (`losmexicanos_unam_iij`,
13 544 filas con texto; `cultura_constitucional_unam_iij`, 572) podían
aportar juicio.

**Las ocho `PARCIAL`** están en el append de
`forense/notas/2026-09-05-MAESTRA38-N12-modulo-propio-v0.md`, con qué existe y
qué falta en cada una. Las tres que más mueven el costo del plan:

- **`salud.atencion.leve_sin_imss` (`R4.1`)** — la Encuesta Nacional de Salud
  (UNAM-IIJ) trae `p13 ¿Para resolver este problema de salud qué acción
  realizó?` con las **tres opciones exactas** que el instrumento mínimo
  nombra (`5 Se atendió en una farmacia`, `10 Se automedicó`, `1/2/3` consulta
  formal), `p14` con la opción `8 Consultorio adyacente a la farmacia`, y `p9
  ¿Cuenta con afiliación a alguna institución de salud?` para la población
  «sin seguridad social». **Falta un solo ítem: la severidad percibida.** Es
  la fila más barata de las 19 y no lo era antes de este cruce.
- **`trabajo.prestaciones.formalidad_pesa_mas_que_salario` (`R2.3`)** — la
  fila que `N10`/`N12 §1.5` dejaron **sin frase-pregunta verbatim**. Economía
  y Empleo sí trae el desenlace de preferencia declarada que faltaba
  (`p18_1` «Que sea estable y seguro» contra `p18_2` «Que proporcione ingresos
  altos», más elección forzada en `p19`/`p20`). **No se promueve a
  `CUBIERTO-POR`**: el eje medido es *estabilidad vs. ingreso*, no
  *prestaciones formales vs. salario nominal*, y un empleo informal puede ser
  estable. Es justo el parecido nominal que el criterio prohíbe.
- **`informacion.escuela.miedo_a_caer_clase_media` (`R9.4`)** — `p4 Dada la
  situación económica actual, ¿usted cree que sus hijos podrán vivir ______
  que usted?` es, palabra por palabra, la percepción de movilidad descendente
  del instrumento mínimo. Falta la liga a la elección de escuela.

**Dominio entero sin una sola cobertura parcial: `tiempo` (4/4).** Es el único
de los seis.

---

## §3 · Pieza (b) — los tres constructos de `R7.3`/`R7.6`: cubiertos los tres, y por una fuente que estaba en el corpus sin inventariar

`data/cruce-r7-v1_0.tsv`, filas (b). El instrumento no es LAPOP: es
**CIDE-CSES 2015**, tres `.sav` bajo `descargas_mx/UNIVERSO-2026-09/CSES/`
que tenían **0 filas en los cuatro inventarios** y que este acto inventarió
(1 200 filas, 1 025 con texto).

| constructo | veredicto | qué lo cubre |
|---|---|---|
| beneficiario de programa social | `CUBIERTO` | `pcyc12`/`pcyc12a`/`pcyc12b` (LICONSA, PROCAMPO, PROSPERA por nombre), `pcyc16` beca escolar, `pcyc17` pensión de adultos mayores, `pcyc18` apoyo alimentario — **y el nivel de gobierno que lo otorga** (`pcyc16a-c`, federal/estatal/municipal) |
| «le condicionaron / le pidieron el voto a cambio» | `CUBIERTO` | `pcyc13` **y** `pcyc14` |
| secreto del voto percibido | `CUBIERTO` | `p14`, y `pvoto1`/`pvoto2`/`pvoto3` |

Lo que hace a esta fuente distinta de lo ya medido, en dos puntos:

1. **Separa la zanahoria del garrote.** `pcyc13`: «¿algún candidato … le
   ofreció incluirlo en alguno de los programas … **a cambio de que Usted
   votara** por ese partido?». `pcyc14`: «…¿lo **amenazó con quitarle** alguno
   de los programas mencionados **si Usted no votaba** por ese partido?» —
   ofrecimiento condicionado y amenaza de retiro del beneficio ya recibido,
   atados al programa nombrado en la pregunta anterior, en la misma persona.
   Trae además el brazo observacional de vecindario (`pcyc7`/`pcyc8`, «¿vio a
   gente del (PARTIDO) repartiendo regalos … en su colonia?») y una viñeta
   normativa (`pcyc9a`, los 200 pesos).
2. **`pvoto1`/`pvoto2`/`pvoto3` no son tres preguntas: son un experimento de
   encuadre** sobre la misma. `pvoto1` antepone que observadores
   internacionales certificaron garantías; `pvoto2` antepone que hubo reportes
   de funcionarios de casilla marcando boletas; `pvoto3` va sin preámbulo. Es
   variación exógena en la percepción de secreto, que es exactamente lo que
   `R7.3` necesita y que ninguna medición previa de la regla tuvo.

`ENCUP 2012` y `CSES5` **no pudieron aportar**: 0 filas con texto las dos
(`.xlsx` y `.csv` sin etiquetas). Latinobarómetro 2024 aporta sólo el primer
constructo (`S6`); LAPOP 2019 sólo el primero (`cct1b`).

**Este acto no escribe ninguna spec.** Que CIDE-CSES 2015 abra o no una para
`R7.3`/`R7.6` es decisión de mesa.

---

## §4 · Pieza (c) — ENVIPE: `NO-CUBRE`, y no por el antecedente que faltaba

`data/cruce-envipe-agravio-v1_0.tsv`. Los tres antecedentes se leyeron de
`forense/prereg-caja/S5-L5-spec-v1_0.md §3.1`, no de memoria.

**El inventario no servía para esta pieza y se dice:** las 44 payloads de
ENVIPE inventariadas (7 673 filas en `-ext-v1_0`, 23 467 en `-v1_2`) tienen
`texto_reactivo` **vacío** — ni el `.dbf` ni los `.sav` de INEGI llevan
etiquetas. El texto salió del descriptor, `data/raw/fd_envipe2025.pdf`,
98 páginas, **5 392 líneas** extraídas con `pypdf`.

| | veredicto | evidencia |
|---|---|---|
| `AGRAVIO` | `CUBRE` | 41 líneas del FD con «víctima»; el módulo de victimización es el objeto de la encuesta |
| `FALLA_ESTATAL` | `CUBRE` | `5.4 ¿Cuánta confianza le inspira la (el) (AUTORIDAD)?`, escala de 4 puntos (`AP5_4_*`); 59 líneas con «confianza» |
| `RED_PREVIA` | **`NO-CUBRE`** | 0 líneas con «asociaci», «vecinal» o «comit[eé]»; **1** con «organizaci», y es prosa de la introducción |
| `URBANO` | `CUBRE` | `DOMINIO`: `U Urbano` · `C Complemento urbano` · `R Rural` — **tres** estratos, no dos |
| **desenlace (protesta)** | **`NO-CUBRE`** | **0 líneas** con «protest», «manifestaci», «march», «bloqueo» o «plantón», sobre las 5 392 del FD 2025 (508 variables, la ola más ancha) |

**El hallazgo es el desenlace, no el antecedente.** ENVIPE mide **denuncia
ante el Ministerio Público** (14 líneas con «denunci»), que es acción
individual y legal ante la autoridad, no acción colectiva contenciosa.
Tomar una por la otra sería el parecido nominal que `S11 §2` prohíbe.

**Consecuencia para `FP-316 (b)` / `ADR-363`.** La `se_mueve_si` que ese
sello escribió para `R7.4` dice, verbatim: «una fuente con sobremuestra rural
que estime `C_completo` (**ENVIPE: pieza del LOTE-CRUCE**) — si CUBRE, se
escribe S5 v1.1 …». **ENVIPE no la puede disparar**: tiene la sobremuestra
rural (`n = 3 770` en `DOMINIO=R`, 2025, `TMod_Vic`, contra 40 280 totales —
unas **2.4 veces la `n` total** de una ola LAPOP mexicana), pero no tiene la
variable dependiente. La cláusula está escrita contra una fuente que no puede
cumplirla. **No se escribe S5 v1.1, no se declara candidata**, y se deja a
mesa la re-especificación. Nada de `milpa/` se toca aquí.

---

## §5 · Pieza (d) — las 29 relaciones `NO-ENCONTRADO`: 24 tienen paralela

`data/cruce-relaciones-noencontrado-v1_0.tsv`, una fila por relación.
`data/curacion-registro/relaciones.tsv` **no se edita**. El veredicto es del
**constructo** (la `necesidad_id`), no de la fuente: las relaciones que piden
lo mismo comparten paralela.

| necesidad | constructo | filas | veredicto | paralela |
|---|---|---|---|---|
| `N13` | `G5.familismo_obligacion` | 6 | `PARALELA-CUBRE` | Encuesta Nacional de Familia `p28`/`p29` (la obligación en **las dos direcciones**, misma persona) |
| `N3` | `G2.sens_estatus` | 9 | `PARALELA-PARCIAL` | Cultura Constitucional `P91_*` (discriminación percibida por educación, acento, vestido, trabajo en el campo) — brazo receptor, falta la sensibilidad |
| `N4` | `G2.aversion_riesgo` | 2 | `PARALELA-CUBRE` | CAFR 2005 §5: dos series de elección entre loterías (`p5_1_*`, `p5_4_*`) y punto de indiferencia (`p5_2`) |
| `N12` | `G5.familismo_apoyo` | 2 | `PARALELA-CUBRE` | Encuesta Nacional de Salud `p43_1`/`p43_2` (familia **vs.** amigos, misma escala) |
| `N14` | `G5.radio_confianza` | 2 | `PARALELA-CUBRE` | LAPOP 2006 `MEX23` + Cultura Constitucional `P13_1..P13_19` |
| `N20` | `civico.denuncia.con_seguro` | 1 | `PARALELA-CUBRE` | Movilidad y Transporte `p25_7_*` (¿denunció? por delito) + `p8h` (¿su automóvil está asegurado?) — **reserva:** dos archivos del mismo estudio, no se verificó llave de unión |
| `N26` | `R7.3` | 1 | `PARALELA-CUBRE` | CIDE-CSES 2015 `p14`/`pvoto*` (§3) |
| `N19` | `dinero.ahorro.con_puente_y_respaldo` | 1 | `PARALELA-PARCIAL` | LFEPIE 2011 `q16`/`q17` (caja de ahorro) — cubre el puente, no el respaldo |
| `N10` | `G4.horizonte_temporal` | 2 | **`NINGUNA-EN-CORPUS`** | ninguna elección intertemporal en 350 832 filas; la CAFR trae la gemela de riesgo pero no la temporal |
| `N17` | `tramite.gobierno_digital.coercitivo` | 3 | **`NINGUNA-EN-CORPUS`** | el corpus entero no tiene el reactivo (§6) |

**14 `PARALELA-CUBRE` · 10 `PARALELA-PARCIAL` · 5 `NINGUNA-EN-CORPUS`.**
Lo que esto dice del programa: de las 29 relaciones marcadas
`NO-ENCONTRADO`, **la mayoría no era un hueco del corpus sino un hueco de la
fuente concreta** que se abrió — `G5.familismo_obligacion` llevaba seis
relaciones abiertas contra ENFIH/ENSAFI/ENBIARE mientras la Encuesta Nacional
de Familia ya lo preguntaba textualmente.

---

## §6 · Pieza (e) — `coercitivo`: `SIN-COBERTURA`, con control positivo

`data/cruce-r7-v1_0.tsv`, última fila.

Instrumento mínimo, verbatim del `se_mueve_si` de las dos entradas
`coercitivo_*` de `milpa/tramite-ola5-propuesta-v0.yaml` (líneas 2691 y 3179,
leídas, no editadas): «instrumento de encuesta con **tenencia vigente de
e.firma por persona** (ENCIG/ENDUTIH/ENIF, ítem nuevo)».

```
regex  'firma electr|e\.?firma|fiel|certificado digital|firma digital'
sobre  data/inventario-reactivos-descargas-mx-v1_1.tsv + -v1_2.tsv
       + data/inventario-reactivos-ext-v1_0.tsv + data/inventario-reactivos-v1_2.tsv
       = 350 832 filas examinadas, 4 archivos
aciertos con texto de reactivo: 5, y los 5 son falsos positivos declarados
  · Encuesta Nacional de Género p15 «¿Alguna vez, usted le ha sido INFIEL...?»  (×2)
  · WVS-7 FW_START / FW_END
  · Encuesta Nacional de Género p63_3 (frase de batería)
CONTROL POSITIVO, mismo comando, mismo universo: 'trámite' -> 26 aciertos con texto
  (LAPOP 2004 aoj19, LAPOP 2006 SGL2, Corrupción y Cultura de la Legalidad p12/p14)
```

El negativo lo produjo un comando que sí examinó archivos y que sí encuentra
lo que hay (A.13). **`tramite.gobierno_digital.coercitivo` sigue siendo la
única regla del motor sin dato**, `ya_medido.py` la devuelve `NUNCA-MEDIDA`,
y su cláusula de movimiento **tampoco se puede disparar con el corpus de
hoy**. No se escribe spec `N7`; corresponde a dirección re-especificar.

---

## §7 · Pieza (f) — LAPOP 2021/2023: la premisa era falsa, y lo que hay debajo es peor

`data/cruce-lapop2123-v1_0.tsv`. Leído **directo del `.dta`** con
`pyreadstat`, no del inventario.

| control | 2021 (262 col) | 2023 (195 col) |
|---|---|---|
| `clien1n` | **AUSENTE** | **AUSENTE** |
| `clien1na` | **AUSENTE** | **AUSENTE** |
| `vb2` | AUSENTE | PRESENTE — «Registro de votaciones: última elección presidencial/general de 2021» |
| `AOJ11` | PRESENTE — «Percepción de inseguridad en el barrio» | PRESENTE — «Percepción de seguridad en el vecindario» |
| `AOJ12` | AUSENTE | PRESENTE — «Si es víctima de un crimen, la fe en el sistema de justicia» |

**4 de 10 presentes.** Y el censo de la familia entera de variables lo cierra:
2021 trae `aoj11`, `aojg2n`, `aojg3n1` y **ninguna** `clien*` ni `vb2*`;
2023 trae `aoj11`, `aoj12`, `vb2`, `vb20`, `vb21n` y **ninguna** `clien*`.

`SELLO-2 §B` escribió tres `se_mueve_si` (`R7.7`, `R7.6` brazo proximidad,
`R10.3`) cuya condición era «LAPOP 2021 o 2023 con `clien1n`/`clien1na` ×
turnout verificado». **Las tres son inejecutables con estos dos archivos**, y
no porque falte inventariarlos —ya estaban inventariados— sino porque el
reactivo no está en el instrumento de esas olas. `R10.3`, en cambio, **sí**
puede moverse: su cláusula pide la batería `AOJ1/AOJ11/AOJ12/vic1` en una ola
≥ 2019, y 2023 trae `AOJ11` y `AOJ12`.

---

## §8 · Qué queda para mesa

Tres cosas, ninguna decidida aquí:

1. **Dos cláusulas de movimiento escritas contra fuentes que no pueden
   cumplirlas** — `R7.4` contra ENVIPE (§4) y
   `tramite.gobierno_digital.coercitivo` contra el corpus (§6) —, más las
   tres de `SELLO-2` que dependen de `clien1n`/`clien1na` (§7). Un
   `se_mueve_si` que nadie puede disparar no es una cláusula, es un cierre
   con otra cara.
2. **CIDE-CSES 2015 cubre los tres constructos de `R7.3`/`R7.6`** (§3), con
   un experimento de encuadre encima. Si mesa lo autoriza, es spec, no
   adquisición.
3. **El módulo propio baja de 19 filas enteras a 11 enteras + 8 recortadas**
   (§2), y la más barata (`R4.1`) queda a un ítem.

**El primer resultado que produjo este procedimiento es el que se reporta.**
