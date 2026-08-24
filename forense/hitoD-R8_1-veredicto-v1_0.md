# HITO D · `R8.1` — el falsador corrido contra los cuatro instrumentos, y propuesta de fila

### `hitoD-R8.1-veredicto` · **v1.0** · 20 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R8_1-veredicto-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R8.1-veredicto`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La corrida (COMMIT B) de `hitoD-R8.1-especificacion`: la tabla Q1–Q4 llena por lectura de los cuatro instrumentos en disco. |
> | **QUÉ NO ES** | No adjudica: propone fila `D`. No numera `D-07`: lo propone a mesa. No mueve el contador por sí mismo. |
> | **VERIFICAS ASÍ** | `python3 tests/hitod_r8_1_contribucion.py`; salida cruda en `forense/notas/2026-08-20-r8-1-contribucion-salida.txt`. |

**ESTAMPA DE UNIVERSO (`A.10`).** Sello tomado sobre `origin/main = 54da215`, 20/ago/2026, entorno **UBUNTU**. Universo examinado: **cuatro** instrumentos abiertos uno por uno — `r8_1_contraloria_social_2019_2025_csv` (7 filas de dato, 2019-2025) · `ADQ15_OMCA_conflictos_agua` (375 conflictos) · LAPOP México 2021 (262 vars) y 2023 (195 vars) · `encup_2012_base_datos_xlsx` (282 columnas). **Denominador del universo de instrumentos posibles: no existe** y se escribe en vez de omitirse. Este sello no rige ningún instrumento de encuesta a hogares con módulo de bien público que se adquiera después — ver §5.

---

## 1 · La tabla Q1–Q4, llena por lectura

| instrumento | unidad | **Q1** tasa con denominador | **Q2** ≥2 años, misma unidad-bien | **Q3** ausencia de sanción | **Q4** fuera del comunal |
|---|---|:---:|:---:|:---:|:---:|
| Contraloría Social, 7 filas × 9 col. | **año fiscal nacional** | **NO** | **NO** | **NO** | **NO** |
| OMCA conflictos por el agua, 375 reg. | **conflicto** | **NO** | parcial | **NO** | SÍ |
| LAPOP México 2021 | persona | parcial (ver §2) | **NO** | **NO** | SÍ |
| LAPOP México 2023 | persona | **NO** | **NO** | **NO** | SÍ |
| ENCUP 2012, 282 columnas | persona | **NO** | **NO** | **NO** | SÍ |

**`Q3` tiene cobertura CERO en los cinco.** Ningún instrumento en disco registra, para un bien público concreto, si existe o no un mecanismo de sanción o un liderazgo con capacidad de excluir. **Sin `Q3` no hay falsador: hay descripción.**

**Un falso positivo del propio patrón de búsqueda, declarado en vez de ocultado.** La única columna que el patrón de `Q3` marcó en Contraloría Social es `beneficios_vigilados` — y **no** es una variable de sanción: es un **conteo** de beneficios vigilados. Se registra el falso positivo porque un lector que corriera el mismo `grep` sin abrir el archivo concluiría lo contrario.

---

## 2 · Lo más cerca que estuvo cualquier instrumento, y por qué falló

**LAPOP México 2021 trae un módulo de agua con 22 variables `psc2r2_*` — *"Persona que paga el servicio de agua"* —, incluida `psc2r2_99`: *"No pagan por el agua que consumen"*.** Es lo más cercano a una tasa de aportación a un bien público que existe en este corpus, y ningún acto previo lo había señalado. **Falla por dos piezas, no por una:**

- **Falla `Q2`:** la batería **no existe en la ola 2023**. Es una sola ola. El Umbral pide *"durante ≥2 años"* sobre la misma unidad-bien, y una sola ola no lo da.
- **Falla `Q3`:** cero variables de corte de servicio, multa o exclusión. En agua urbana la sanción canónica es el **corte**, y no está medida.

**No se calculó ninguna tasa de pago de agua**, y no por descuido: hacerlo sería exactamente el diseño sustituto que la spec prohíbe en §5.3 de su hermana `R7.3` y que el árbol de esta ficha no autoriza. Se deja nombrado para el sucesor, que es donde vale.

**Las baterías de ENCUP 2012 y LAPOP 2023 miden otra cosa, y la distinción no es sutil.** ENCUP trae **30 columnas** de participación: `P57_1`…`P57_9` (asistió a reunión de juntas de vecinos, junta de colonos, condóminos, asambleas de la comunidad, cooperativas o asamblea ejidal…), `P69_1`…`P69_16` (es o ha sido **miembro** de…), `P59_11` (ha hecho **donativos** a alguna organización social). LAPOP 2023 trae `cp8` (*"asiste a reuniones de un comité o junta de mejoras para la comunidad"*). **Todas miden asistencia, membresía o donativo a una organización; ninguna mide aportación a un bien público identificado con denominador conocido.** Asistir a la junta de vecinos no es contribuir al bien que la junta administra, y la ficha pide lo segundo.

**ENCUP 2012, además, no permite varianza de diseño:** trae ponderador (`factor`, `POND`) pero **ningún estrato ni UPM** entre sus 282 columnas. Cualquier tasa que alguien estime con ella lleva un error estándar mal especificado, y queda escrito aquí.

---

## 3 · Dos defectos del payload de OMCA, encontrados de paso y registrados

No tocan el veredicto y por eso van aquí y no en el argumento:

1. **El campo `anio` contiene `20´18`** — con acento agudo en lugar de dígito. Por eso el rango se lee `1926..20´18` y arroja **45 valores distintos** donde debería haber menos. Es corrupción de captura en el payload publicado, no de la descarga: el `sha256` verificó `COINCIDE`.
2. **`presencia_indigena` mezcla idiomas**: entre sus valores conviven nombres de pueblos (`Chatinos`, `Chinantecos`, `Huaves`, `Lacandones`) y la cadena en inglés **`IT doesn't have`** como codificación de "no tiene".

Se registran en `forense/hallazgos.md` para quien vaya a usar OMCA con otro fin.

---

## 4 · Propuesta de fila, contra el árbol congelado

**Rama 4 → fila `D`.** Ningún instrumento construye `Q1+Q2+Q3+Q4`; y la razón por la que falla `Q3` **en los cinco a la vez** es la estructural que la spec declaró **antes** de correr: el brazo sin sanción no produce registro.

**La predicción pre-declarada se confirma, y esa es la mitad del valor.** `hitoD-R8.1-especificacion §3` escribió, antes de abrir un solo archivo, que el falsador *"pide evidencia de una ausencia, y las ausencias no generan registro"*, y dejó su propia salida abierta: *"una encuesta a hogares sí puede medir contribución a un bien público sin pasar por ningún registro de comités… si algún instrumento de encuesta en disco construye Q1+Q3 a la vez, el defecto es menos grave"*. **Se corrieron las tres encuestas del corpus con módulo comunitario —LAPOP 2021, LAPOP 2023, ENCUP 2012— y ninguna construye `Q3`.** La salida quedó abierta y no se tomó; el defecto queda como se declaró.

**Por eso se propone `D-07` a mesa**, con este texto y sin numerarlo aquí:

> **`D-07` · `R8.1` — el falsador pide evidencia de una ausencia.** *"Bien público con contribución alta y sostenida **sin monitoreo ni sanción"*: el brazo sin mecanismo no produce comité, ni acta, ni padrón, ni fila administrativa, y ninguna de las tres encuestas mexicanas con módulo comunitario mide si el bien tiene sanción. Reescribirlo exige medir el mecanismo, no buscarlo en un inventario.*

**Verificado, sin solape de filas que quede sin resolver.** `A` y `B` exigen una tasa; no se construye ninguna. `C` (*"exigiría inventario de comités con y sin mecanismo"*) **también se lee cierta**, y por la precedencia fijada al sellar **manda `D`**: precedente directo de `ADR-56`, donde `R4.1`, `R4.3` (ambas mitades), `R9.1` y `R9.2` se archivaron `D` teniendo su propia fila `C` describiendo un diseño más fino inexistente. La frontera de `ADR-10` **no se cruzó**: ningún caso de faena o tequio se usó, y OMCA —el único instrumento con `Q4` explícito vía `presencia_indigena`— no aportó al veredicto.

**Sobre archivar.** Un `D` es una afirmación sobre **nuestro instrumental**, no sobre México, y `ADR-55`/`ADR-56` fijaron que el acto que lo establece lo archiva. Este acto **sí archiva `R8.1` → `D`** en el bloque append-only, y el contador se mueve por esta ficha. Lo que **no** archiva es `D-07`: eso es enmienda a la tabla de defectos del Paso 1 y va a firma de mesa.

---

## 5 · Lo que desbloquearía `R8.1`, nombrado y no genérico

1. **Un módulo de encuesta que pregunte, sobre un bien público concreto, las dos cosas a la vez**: *"¿usted aporta?"* y *"¿qué pasa si no aporta?"*. La segunda es `Q3` y no la hace ninguna encuesta mexicana pública hoy. Es una pregunta, no una base de datos.
2. **Repetir el módulo de agua de LAPOP 2021 en una segunda ola** cerraría `Q2` — y con un ítem de corte de servicio, cerraría `Q3` también. **Es el camino más corto que existe** y cuesta dos ítems, no un instrumento nuevo.
3. **Lo que NO desbloquea:** más inventarios de comités. `C` pide el inventario, y el inventario es exactamente lo que no puede existir para el brazo de control. **Adquirir por esa vía sería gastar sin poder cerrar la ficha**, y decirlo es el aporte operativo de este acto.

---

## 6 · Módulo de auditoría de rigor extremo

**¿Qué confunde estructura con cultura?** El riesgo mayor de esta regla, si alguien la usara sin falsador: *"free-riding racional"* suena a diagnóstico de carácter y es una predicción de teoría de juegos. Que no podamos probarla la deja como teoría importada, no como hallazgo mexicano — y `R8.1` es `[FUERTE]` en el motor.

**¿Qué cambiaría con foco rural, indígena o popular?** Todo, y la frontera de `ADR-10` lo impide por diseño. El caso donde la contribución sin sanción formal está mejor documentada en México es exactamente el que la ficha declara error categorial. La regla se juzga en el terreno donde peor se mide, y eso es una decisión de modelo, no un accidente de este acto.

**¿Qué afirmación describe el estado del corpus y no fue derivada?** Ninguna: los cuatro instrumentos se abrieron en la corrida. Un desajuste menor de metadato: el campo `formato` del manifiesto dice *"CSV, 8 filas"* para Contraloría Social y `CONF-17` dijo *"7 filas"*; el archivo tiene **8 líneas** (1 encabezado + **7 filas de dato**, 2019-2025). Ambas cifras son correctas bajo su propio criterio de conteo; se desambigua aquí y no se corrige el manifiesto (fuera de perímetro).

---

**el primer resultado que produjo este procedimiento es el que se reporta.**
