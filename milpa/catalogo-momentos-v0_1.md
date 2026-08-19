# Catálogo de momentos · piloto `finanzas-del-hogar`

### `catalogo-momentos` · **v0.1** · 18 de agosto de 2026 · `ACTO LANE-A-E0-E5`, COMMIT C1 · fase **CON SELLO** de `forense/encargos/2026-08-14-MOTOR-3-E0-autocontenido.md`

> | | |
> |---|---|
> | **ARCHIVO** | `milpa/catalogo-momentos-v0_1.md` + su tabla `milpa/catalogo-momentos-v0_1.tsv` |
> | **NOMBRE ESTABLE** | **`catalogo-momentos`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | El **pre-registro** que `canon/gobernanza-v1_15.md:461` exige: los momentos que el motor pretende reproducir, enumerados **antes** de que exista una sola corrida, con su `rol_calibracion` (`AJUSTE`/`HOLDOUT`) **sellado en este commit**. Firma de mesa que lo constituye: `ADR-100(4)` (M4). |
> | **QUÉ NO ES** | No es una medición. No trae una sola cifra nueva sobre México. No adjudica ningún momento como computable — eso es veredicto del COMMIT C2, con vocabulario A.4 (fix **M10** de `RONDA-M`). No es el registro celda-D de `ADR-68(a)`: son artefactos hermanos y su relación sigue abierta (S1 ≈ M5, §5). |
> | **VERIFICAS ASÍ** | Cada fila sale por comando del libro de demanda (`data/curacion-registro/necesidad-objeto-modelo.tsv`), fuente única por `ADR-100(5)` (M5). El comando de re-derivación está en §2 y su salida debe ser idéntica a la tabla, fila por fila. |

---

## 0 · El muro, dicho antes que nada

**Tocar un momento `HOLDOUT` después de este commit es violación de pre-registro**, y `tests/test_motor_holdout.py` lo vigila con tres pruebas, no una: (a) el conjunto `HOLDOUT` no cambia entre commits; (b) ninguna ruta de código que evalúe celdas-semilla lee el valor de un momento `HOLDOUT`; (c) los roles quedaron sellados en un commit **anterior en historia de git** a todo resultado — que es literalmente el umbral (1) de `ADR-68` (Ronda 1 §7).

**Contador nuevo del programa, que nace aquí y desde hoy se cuenta:**

> **momentos HOLDOUT reproducidos: `0` de `14`.**

`0` no es una promesa de que subirá. E0 no calibra: compila y reproduce lo ya adjudicado. Ver §6 (B-bis).

---

## 1 · Las firmas bajo las que este catálogo existe — `ADR-100`, verbatim

Mesa no dio seis firmas separadas: dio **una firma por lote** con una cláusula propia por M dentro de la misma frase (`ADR-91`, `PR #246`, 17/ago/2026, *"Adelante con la propuesta."*, sellada como `ADR-100`). Las cláusulas que gobiernan este archivo, verbatim:

- **M4** — *"catálogo de momentos como pre-registro de gobernanza:461, roles AJUSTE/HOLDOUT sellados en su commit 1"*. **CONDICIONADA** por el inciso (9) de `ADR-100`.
- **M5** — *"libro de demanda como fuente única del curador"*. **CONDICIONADA**. De aquí sale la enumeración de §2, y de ninguna otra parte.
- **M2** — *"cortes iniciales por eje conforme a la cascada, respetando los tres ejes de hogar"*. Dueño del sello por eje: **este catálogo, en este commit** (`ADR-100(2)`). Ver §3.
- **M3** — *"campo medio para G1b con estatus HIPÓTESIS"*. Ver §4.

**La condición, no retirada:** `ADR-100(9)` deja `M2`/`M4`/`M5` sujetas a re-verificación contra el universo nuevo de `BARRIDO-2` — *"si no cambian, el sello procede sin volver a mesa; si alguna cambia, vuelve a mesa solo esa"*. Este catálogo nace **v0.1** por eso: es el objeto que esa re-verificación tendrá que mirar.

---

## 2 · La tabla — 22 momentos, derivados por comando del libro de demanda

**Regla de enumeración, declarada antes de mirar el contenido de ninguna fila** (esto es lo que la hace un pre-registro y no una selección):

1. El universo es `data/curacion-registro/necesidad-objeto-modelo.tsv` **entero** — 37 filas, fuente única por M5.
2. Se **excluyen** las 15 filas cuyo `objeto_modelo_origen` es un coeficiente de generador (`G1.`…`G6.`): son demanda sobre `B`/`Θ` — lo que el ajuste *consume*, no lo que el motor *reproduce*. Un coeficiente no es un momento.
3. Las 22 restantes **son** los momentos, en el orden del archivo, numeradas `M01`…`M22`.
4. **El reparto de rol es una función del tipo de objeto, no de su contenido:** un objeto que es una **predicción pre-registrada del Hito D** (`R*`, `forense/hitoD-preregistro-v2_0.md`) es `HOLDOUT` — es exactamente lo que no puede usarse para ajustar sin destruir su valor probatorio. Todo lo demás (desenlaces de conducta ya declarados en `milpa/tramite.yaml` y `milpa/procedencia.yaml`) es `AJUSTE`. `DIAGNÓSTICO`: vacío hoy, el vocabulario se conserva.

Re-derivación (debe reproducir la tabla exactamente):

```bash
awk -F'\t' 'NR>1 && $2 !~ /^G[1-6]\./ {n++; print n"\t"$1"\t"$2"\t"($2 ~ /^R/ ? "HOLDOUT" : "AJUSTE")}' \
  data/curacion-registro/necesidad-objeto-modelo.tsv
# → 22 filas · 8 AJUSTE · 14 HOLDOUT
```

**Reparto sellado: `AJUSTE` = 8 · `HOLDOUT` = 14 · `DIAGNÓSTICO` = 0 · total `M` = 22.**

| `id_momento` | `objeto_modelo` | `necesidad_id` | `rol_calibracion` | fuente de la regla |
|---|---|---|---|---|
| `M01` | `tramite.mordida.discrecional` | `N16` | **AJUSTE** | `milpa/tramite.yaml` |
| `M02` | `tramite.mordida.con_registro` | `N16` | **AJUSTE** | `milpa/tramite.yaml` |
| `M03` | `tramite.gobierno_digital.coercitivo` | `N17` | **AJUSTE** | `milpa/tramite.yaml` |
| `M04` | `tramite.gobierno_digital.util_sin_coercion` | `N17` | **AJUSTE** | `milpa/tramite.yaml` |
| `M05` | `tramite.evasion_norma` | `N18` | **AJUSTE** | `milpa/tramite.yaml` |
| `M06` | `dinero.ahorro.con_puente_y_respaldo` | `N19` | **AJUSTE** | `milpa/procedencia.yaml` |
| `M07` | `dinero.credito.scoring_alternativo` | `N19` | **AJUSTE** | `milpa/procedencia.yaml` |
| `M08` | `civico.denuncia.con_seguro` | `N20` | **AJUSTE** | `milpa/procedencia.yaml` |
| `M09` | `R1.4` | `N21` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |
| `M10` | `R2.1` | `N22` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |
| `M11` | `R2.2` | `N23` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |
| `M12` | `R3.4` | `N24` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |
| `M13` | `R7.1` | `N25` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |
| `M14` | `R7.3` | `N26` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |
| `M15` | `R7.4` | `N27` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |
| `M16` | `R7.5` | `N27` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |
| `M17` | `R8.1` | `N28` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |
| `M18` | `R8.2` | `N29` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |
| `M19` | `R8.3` | `N30` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |
| `M20` | `R10.1` | `N31` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |
| `M21` | `R10.2` | `N32` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |
| `M22` | `R10.3` | `N33` | **HOLDOUT** | `forense/hitoD-preregistro-v2_0.md` |

La tabla completa —con `universo_candidatos`, `universo_instrumento`, `nivel`, `instrumentos_candidatos`, `computo_pretendido`, `estatus_disponibilidad` y la `reserva` heredada del libro de demanda— vive en `milpa/catalogo-momentos-v0_1.tsv`. Los campos marcados `POR DECLARAR` **están vacíos a propósito**: llenarlos exige mirar el disco, y §3.3 de la propuesta lo prohíbe antes de sellar. Este commit sella `id` y `rol_calibracion`; nada más.

**Dos campos que este catálogo NO tiene, y por qué (fixes de `RONDA-M`, aplicados desde el nacimiento):**

- **`rol_calibracion`, no `rol`** — fix **S2**. `rol:` ya está sellado por `ADR-68(a)` con otro enum (`BASELINE | CHALLENGER | COMPLEMENTO`) y en uso en las tres celdas-D del disco. Dos vocabularios bajo la misma llave es una colisión, no un sinónimo.
- **`universo_candidatos` y `universo_instrumento`, separados** — fix **M3**. El universo de *búsqueda* (`ADR-68(a)`) y el universo *estadístico* no son el mismo objeto y `UNIVERSO` ya estaba ocupado por el segundo.
- **`computo_pretendido`, no `computable`** — fix **M10**. El commit C1 sella el momento y su cómputo **pretendido**; el veredicto de computabilidad se registra en C2 con vocabulario A.4. Las dos frases de la propuesta (§3.1 "condición de pertenencia" y §3.3 "no mirar el disco") no pueden valer a la vez; ésta es la reconciliación.

**Reserva heredada, no reescrita:** cuatro `necesidad_id` traen dos objetos bajo una misma necesidad (`N16`, `N17`, `N19`, `N27`) y `N33` trae *"Riesgo ético: solo dato secundario"*. Viajan verbatim en la columna `reserva` del TSV.

---

## 3 · π(x) y los cortes por eje — M2, sellado donde se puede y declarado donde no

`ADR-100(2)` da el sello de los cortes **a este catálogo, en este commit**. Se ejerce con una regla: **se sella el corte que el propio instrumento ya trae en su catálogo; no se inventa el que exige una decisión de datos nueva.**

| # | Eje | Nivel | Corte inicial | Estado |
|---|---|---|---|---|
| 1 | Formalidad laboral (`segsoc`) | **persona** | 1 Sí / 2 No | **SELLADO** — binario del propio instrumento |
| 2 | Edad (`edad`, entero) | **persona** | — | **PENDIENTE** — ver abajo |
| 3 | Urbanización (`tam_loc`) | **hogar** | 1 · 100 000+ / 2 · 15 000–99 999 / 3 · 2 500–14 999 / 4 · <2 500 | **SELLADO** — catálogo `tam_loc.csv` |
| 4 | Ingreso (`est_socio`) | **hogar** | 1 Bajo / 2 Medio bajo / 3 Medio alto / 4 Alto | **SELLADO** — catálogo `est_socio.csv` |
| 5 | Acceso digital (`celular`, `conex_inte`) | **hogar** | 1 Sí / 2 No, tenencia binaria | **SELLADO** — binario del propio instrumento |
| 6 | Condición migratoria (`residencia`, 34 categorías) | **persona** | — | **PENDIENTE** |

**Los dos PENDIENTE no son un olvido: son la única respuesta honesta.** Un corte de edad y un colapso de 34 categorías de residencia son decisiones sustantivas que exigen dato mexicano propio. `FP-53` (`forense/firmas-pendientes.tsv`) ya tiene abierta exactamente esa deuda — 9 sitios de *"corte PENDIENTE"* en `canon/modelo-decision-v4_0.md`, clasificados y sin definir, porque *"definir el corte exige dato mexicano propio y es acto por sí mismo"* (`ACTO CONSOLIDA-2`). Sellar aquí un corte de edad sería producir cifra nueva al canon por la puerta de atrás, que es justo lo que la ley de mesa vigente prohíbe en E0.

**Los tres ejes de hogar, respetados como manda M2.** Urbanización, ingreso y acceso digital son coordenadas **compartidas por todas las personas del hogar** (`modelo §1.1.A`, veredicto de P1 citado verbatim ahí). Consecuencia ejecutable, no decorativa: `milpa/src/celdas.py` **rechaza al construirse** —no al usarse— todo corte que pretenda contraste intra-hogar en los ejes 3, 4 o 5, y `tests/test_motor_clases.py` lo prueba. No es una celda vacía por muestra pequeña: es vacía por diseño del instrumento.

**π(x) no tiene hoy fuente cargable.** Medido: `tasa_informalidad` aparece **0 veces** en `milpa/procedencia.yaml`, y el bloque de `milpa/milpa-spec-v0_2.md:65-90` que se cita como ejemplo es documentación en fence de Markdown con `...` literales, no YAML cargable. `milpa/src/pi.py` existe, tiene contrato, y **falla ruidosamente** si se le pide construir π sin fuente declarada. Lo que sí está anclado y firme es el tick: **1 trimestre**, alineado con ENOE (`milpa/milpa-spec-v0_2.md:269`).

---

## 4 · `G1b` — M3, y el fix M9 que viaja con él

Firma: *"campo medio para G1b con estatus HIPÓTESIS"*. Aplicado con el fix **M9** de `RONDA-M`, que es lo que lo hace ejecutable: `G1` se parte en **`G1a`** (dueño del `−0.60` de `confianza_institucional` y del `−0.35` de `radio_confianza`, ya adjudicados por `ADR-20`) y **`G1b`** (sin coeficientes propios). El campo medio toca **`h`, no `B`** — no entra a la matriz de coeficientes, entra al agregador. `G1b` sigue `ASIGNADO` y no mueve el `0 de 15` por aceptarse un tratamiento.

---

## 5 · Lo que este catálogo deja abierto, nombrado

- **S1 ≈ M5 — sigue sin cerrar.** `ADR-68(a)` selló `data/curacion-registro/celdas-d/` como hogar del registro celda-D. ¿Es este catálogo **la capa de demanda** de ese registro, o **un artefacto hermano con cruce declarado**? `ADR-100(5)` firmó "fuente única del curador" pero no respondió esta pregunta, y el veredicto de `RONDA-M` §5 la marca como bloqueante del sello. **Aquí se nombra, no se responde:** este catálogo no toca `data/curacion-registro/**` ni redefine el registro celda-D.
- **M8 — heredada.** *"¿Un identified set es valor admisible de la clase `AJUSTADO`, o exige campo propio?"* — relevante porque `AJUSTADO` nace vacía (cero entradas, `ADR-49` D2) y `ADR-102` ya selló el *cómo* de sus rutas sin poblar ninguna.
- **La banda de `ASIGNADO`.** No existe en el archivo. `milpa/src/procedencia.py` devuelve el punto con `banda=None` y marca la deuda; **nunca fabrica un intervalo**.

---

## 6 · La escala de falsación — §6 de la propuesta, verbatim, con su precedencia

Es la escala de este acto, copiada entera y declarada **antes** de correr:

- **Corrobora** la arquitectura: reproducir, dentro de banda, los momentos **HOLDOUT** (no usados en el ajuste), con roles asignados en el commit 1 de §3.3.
- **Acota**: bandas de salida que no firman signo. Resultado informativo pre-declarado — mide cuánta identificación falta, y alimenta la priorización del libro de demanda (qué momento nuevo estrecharía más). No se estrecha con supuestos no listados en §4.2.
- **Refuta**: fallo sistemático de signo en momentos HOLDOUT no atribuible a huecos declarados de Θ; o un chequeo de compilación tipo ADR-30 (§1.4.c) imposible de satisfacer sin violar signos sostenidos por el corpus.
- **Precedencia**: si una corrida satisface "acota" y "refuta" a la vez, manda la fila de refutación. Declarado aquí, al sellar, no después.

**B-bis · qué significa que el falsador no refute, declarado antes de correr.** En E0 no hay calibración. Por tanto **una corrida verde de E0 no corrobora la arquitectura**: sólo establece que el compilador respeta el contrato de clases y es determinista. La corroboración de §6 exige momentos `HOLDOUT` reproducidos, y ese contador nace en `0 de 14`. Decirlo ahora es lo que impide que una salida verde de E0 se lea después como evidencia a favor del motor.

**Nota de precedencia heredada:** el `−0.60` de `familismo_obligacion` **no existe** (es `SIN MAGNITUD`) y el check obligatorio de `ADR-30` **persiste inejecutable** bajo la matriz (defecto **M1** de `RONDA-M`, aún no aplicado a la propuesta). Cualquier lectura de "refuta" que dependa del check de `ADR-30` está bloqueada hasta que M1 se aplique.

---

**Contadores de medición sobre México que este archivo mueve: cero.** `13 de 27`, `0 de 15`, `12 de 15`, `4 de 144` y `1 de 2` quedan donde están. El único contador que nace es el del programa: *momentos HOLDOUT reproducidos: 0 de 14*.
