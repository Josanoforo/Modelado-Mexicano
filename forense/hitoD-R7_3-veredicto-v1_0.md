# HITO D · `R7.3` — constructibilidad del RDD medida, y propuesta de fila

### `hitoD-R7.3-veredicto` · **v1.0** · 20 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R7_3-veredicto-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R7.3-veredicto`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La corrida (COMMIT B) de `hitoD-R7.3-especificacion`: la tabla P1–P4 llena por lectura de cada instrumento en disco, con los `n` alrededor del corte de elegibilidad y la aritmética de precisión que se deriva de ellos. |
> | **QUÉ NO ES** | **No corrió ningún RDD y no corrió ningún sustituto** (spec §5.3). No adjudica: propone fila `C`. No mueve el contador `13 de 27`. |
> | **VERIFICAS ASÍ** | `python3 tests/hitod_r7_3_rdd_constructibilidad.py`; salida cruda en `forense/notas/2026-08-20-r7-3-rdd-constructibilidad-salida.txt`. |

**ESTAMPA DE UNIVERSO (`A.10`).** Sello tomado sobre `origin/main = 54da215`, 20/ago/2026, entorno **UBUNTU**. Universo examinado: **cinco** instrumentos, abiertos uno por uno — `r7_3_pub_beneficiarios_bienestar_csv` · `zenodo_electoral_precinct_level_mexico_municipal` · `mex_2021_lapop_americasbarometer_v1_2_w` · `mex_2023_lapop_americasbarometer_v1_0_w` · `latinobarometro2024_bd_stata`. **Denominador del universo de instrumentos posibles: no existe**, y se escribe en vez de omitirse — nadie ha censado cuántas fuentes mexicanas podrían sostener un RDD sobre la Pensión del Bienestar; los cinco de arriba son los que **este corpus** tiene y que a priori podían traer alguna de las cuatro piezas. Un instrumento nuevo puede vencer este sello en alcance sin refutarlo.

---

## 1 · La tabla P1–P4, llena por lectura y no por catálogo

| instrumento | unidad | **P1** asignación con corte | **P2** programa **nombrado** | **P3** desenlace electoral | **P4** aprobación presidencial |
|---|---|:---:|:---:|:---:|:---:|
| Padrón Único (CKAN), 748×14 | entidad × trimestre | **NO** | agregado — inutilizable | **NO** | **NO** |
| Base electoral por sección, 44 columnas | sección × año | **NO** | **NO** | **SÍ** | **NO** |
| LAPOP México 2021, 262 vars, n=2,998 | persona | **SÍ** (`q2`) | **NO** | **NO** | **SÍ** (`m1`) |
| LAPOP México 2023, 195 vars, n=1,622 | persona | **SÍ** (`q2`) | **NO** | **SÍ** (`vb2`/`vb3n`/`vb20`) | **SÍ** (`m1`) |
| Latinobarómetro 2024, 332 vars | persona, **18 países** | — | **NO** | — | — |

**Ningún instrumento reúne las cuatro a la misma unidad.** El más cercano es LAPOP México 2023, y lo que le falta es justamente **P2**: la búsqueda de *"bienestar"*, *"pensión para"* y *"adulto mayor"* sobre los 195 nombres **y** las 195 etiquetas devuelve **NINGUNA** variable. Lo más cercano es `mexwf1_19` — *"Recibir ayuda (dinero en efectivo, alimentos, productos básicos) del gobierno"* —, que es **ayuda genérica del gobierno**, no el programa que el falsador nombra.

**Dos hallazgos de instrumento que ningún acto previo había registrado.**

1. **LAPOP México 2021 no trae ninguna variable de voto.** `vb2`, `vb3n` y `vb20` están **ausentes** de sus 262 variables. Es la ola cuyo corte de elegibilidad sería **68** (el vigente 2019-2021, antes de la universalización a 65), es decir, la ola con el corte más nítido — y es precisamente la que no puede medir el desenlace. No es un detalle: es el cierre de la única ventana donde la discontinuidad de edad estuvo realmente activa como criterio de exclusión.
2. **`CONF-17` había clasificado la vía (b) de esta ficha como `EXISTE-SATISFACE`** para el dominio principal de INE. Medido aquí contra el instrumento: el desenlace electoral **sí** existe (la base por sección lo trae), pero **solo** P3 — y P3 sola no construye un RDD. La clasificación de puerta era correcta sobre lo que clasificaba (alcanzabilidad de la fuente) y **no** es una afirmación sobre constructibilidad del diseño. Se separan las dos cosas aquí, que es lo que faltaba.

---

## 2 · Los `n` alrededor del corte, y lo que se deriva de ellos

Aun aceptando la sustitución que la spec **prohíbe** (§5.3) —usar ayuda genérica en lugar del programa nombrado—, la vía tampoco alcanza. Se mide, no se afirma:

| ola | corte | ±10 | ±5 (izq/der) | ±3 (izq/der) | ±5 con desenlace y tratamiento |
|---|---|---|---|---|---|
| LAPOP 2021 | 68 | 511 | **256** (145/111) | **171** (87/84) | — (no hay desenlace electoral) |
| LAPOP 2023 | 65 | 310 | **160** (89/71) | **89** (49/40) | **143** |

**Aritmética de precisión sobre esos `n` — es un piso, no una estimación.** Con proporción 0.5 y sin penalización alguna por efecto de diseño, por ajuste polinómico local, ni por la inflación de un RDD difuso, el semiancho **mínimo** del IC95% de una diferencia entre los dos lados del corte sería:

| ola | ventana | EE mínimo | semiancho IC95% mínimo | ¿distingue 10 pp de cero? |
|---|---|---|---|---|
| 2021 | ±5 | 6.31 pp | **12.36 pp** | **NO** |
| 2021 | ±3 | 7.65 pp | **14.99 pp** | **NO** |
| 2023 | ±5 | 7.96 pp | **15.59 pp** | **NO** |
| 2023 | ±3 | 10.65 pp | **20.88 pp** | **NO** |

En las cuatro ventanas el semiancho mínimo **supera** el corte de 10 pp que la spec fijó en §5.1 tomando el borde conservador del rango de la ficha. **La vía de encuesta no puede hablar del umbral de esta ficha ni en el mejor de los casos imaginables**, mucho menos de *"efectos persistentes a escala nacional"*.

**Esto NO es un resultado sobre México.** Es un resultado sobre la precisión que las fuentes públicas permiten. No se estimó ningún efecto y no se reporta ninguno.

---

## 3 · Ponderador y diseño, declarados aunque no se estime

Se dejan escritos porque el próximo acto que intente esta vía los necesita y porque el encargo los exige explícitamente:

- **Padrón y base electoral:** registros administrativos, **sin ponderador**. No hay `FAC_*`, `EST_DIS` ni `UPM_DIS` que declarar.
- **LAPOP:** el análogo mexicano de `FAC_*`/`EST_DIS`/`UPM_DIS` está presente y verificado en la corrida — **`wt`** (peso de la muestra), **`strata`** (peso estandarizado), **`estratopri`** (región), **`estratosec`** (tamaño de municipalidad), **`upm`** (unidad primaria de muestreo). **`cluster`** (lugar de muestreo) está en 2023 y **no** en 2021. Ninguna estimación futura se reporta sin ellos.
- **Latinobarómetro 2024:** instrumento **regional de 18 países**; el submuestreo mexicano no lo convierte en una base con corte de elegibilidad, y **no nombra el programa** en ninguna de sus 332 variables.

---

## 4 · Propuesta de fila, contra el árbol congelado

**Ramas 1 y 2 del árbol, las dos satisfechas → fila `C`.** La rama 1 (ningún instrumento reúne P1+P2+P3+P4) se cumple por §1. La rama 2 (la precisión alcanzable no puede hablar de escala nacional) se cumple por §2, **de más**: no hace falta invocarla, pero se mide y se reporta porque cierra la vía por dos razones independientes en vez de una.

**Redacción propuesta para el archivo, si mesa adjudica:**

> *"`R7.3` → `C`: el RDD que su falsador exige no es construible con ninguna fuente pública en disco. Ninguno de los cinco instrumentos examinados reúne, a la misma unidad, variable de asignación con corte + el programa nombrado + desenlace electoral + aprobación presidencial; el más cercano (LAPOP México 2023) carece justamente del programa nombrado, y su ola hermana de 2021 —la del corte de 68, el más nítido— carece del desenlace electoral. Aun con la sustitución prohibida por ayuda genérica, el semiancho mínimo de IC95% alcanzable (12.4 a 20.9 pp según ventana y ola) supera el corte de 10 pp del Umbral."*

**Verificado, sin solape de filas.** `A` exige un RDD corrido; no lo hay. `B` **no se propone**, por la precedencia fijada al sellar: *"ya obtenido en la corrida previa"* describe un resultado anterior a la ficha, y archivarlo como veredicto del Hito D sería archivar como producto del Paso 2 algo que el Paso 2 no produjo. `D` está **excluida por la letra de la propia ficha** (*"no aplica: el diseño es concebible, solo no se ha hecho"*) y se respeta aunque el hueco haya resultado más ancho de lo que la ficha esperaba.

**No se adjudica, y aquí hay una pregunta de gobierno que este acto no puede resolver solo.** `ADR-55`/`ADR-56` fijaron que un `D` —una afirmación sobre nuestros instrumentos— lo archiva el acto que lo establece, mientras que `A`/`B`/`E` —afirmaciones sobre México— los propone el acto y los adjudica mesa. **Una fila `C` nunca se ha archivado en este programa** y su naturaleza es la del `D`: dice qué le falta a nuestro instrumental, no qué hace un mexicano. Este acto **propone `C` y no la archiva**, y abre fila de firma para que mesa decida la clase, en vez de decidirla el ejecutor (`ADR-76`/`ADR-79`: *"el ejecutor propaga una decisión dictada, no decide"*).

---

## 5 · Lo que este acto deja escrito para quien quiera desbloquear `R7.3`

La lista de la compra, nombrada y no genérica — es el aporte real de esta ficha:

1. **Un instrumento a nivel de persona con la Pensión del Bienestar nombrada como tal**, no "ayuda del gobierno". Candidato natural: el portal nominal `pub.bienestar.gob.mx`, que `CONF-17` intentó tres veces y **no resolvió por DNS**, y que sigue sin adquirirse.
2. **Desenlace electoral en esa misma unidad** — lo que ninguna fuente administrativa mexicana entrega, por secreto del voto. Vía realista: encuesta propia o convenio, no descarga.
3. **O bien un diseño geográfico**: una discontinuidad de cobertura del programa en el espacio, cruzable con la base por sección que este acto ya verificó íntegra. **No existe hoy** ninguna variable de asignación geográfica del programa en disco.
4. **Y la advertencia que se lleva la mitad del valor:** la universalización a 65 años en 2022 **destruyó la discontinuidad** que el diseño necesita. Un RDD sobre este programa tiene su ventana natural en 2019-2021 (corte 68) — y es justo la ola donde LAPOP no midió voto. **La oportunidad de identificación se está cerrando por reforma, no por falta de esfuerzo**, y eso no estaba escrito en ninguna parte del corpus.

---

## 6 · Módulo de auditoría de rigor extremo

**¿Qué afirmación describe el estado del corpus y no fue derivada?** Ninguna: los cinco instrumentos se abrieron en la corrida y cada conteo sale de la salida cruda. La única cifra no producida aquí —el corte de elegibilidad, 68 y luego 65— es normativa del programa social, no una medición, y va declarada como tal en el encabezado del script.

**¿Qué parece psicológico pero es un incentivo racional?** La regla entera. *"Conserva autonomía del voto"* describe una decisión bajo incentivos: si la transferencia es universal y nadie puede quitártela, condicionar el voto no es creíble. Que no podamos probarla no la vuelve más psicológica.

**¿Qué conclusiones serían peligrosas si alguien las usara de forma simplista?** Que `R7.3` "sobrevive". No sobrevive: **no ha sido probada**. Es la única regla del corpus rotulada *"con identificación causal"* y este acto establece que su identificación causal nunca se ha ejercido aquí. Leer `C` como respaldo sería exactamente el sesgo hacia abajo que el Bloque B-bis existe para impedir, pero al revés.

---

**el primer resultado que produjo este procedimiento es el que se reporta.**
