# Medición de `exposicion_violencia` con ENVIPE — Encargo K (mesa #18)

Contadores movidos: 1 (8 → 9 de 14)

Sin módulo de auditoría — es medición, no afirmación interpretativa sobre México (v2.3)

*4 de agosto de 2026.*

**Resultado de este acto, dicho antes que nada: MEDIDO·PARCIAL(edad,dominio,formalidad,ESTRATO).**
Núcleo de cinco ítems limpios de `TPer_Vic2` (ENVIPE 2025) —
`AP7_3_10` (amenaza) · `AP7_3_11` (agresión física con lesión) ·
`AP7_3_12` (secuestro) · `AP7_3_13` (agresión sexual) · `AP7_3_14`
(violación) — binario "sufrió al menos uno, durante 2024", ponderado.
`AP7_3_09` (extorsión) medida aparte, condicional con/sin. Estimador
validado contra un caso conocido publicado por INEGI, con 0.09% de
diferencia. C3 limpio. C2 sellado, no resuelto. Contador: **8/14 → 9/14**.

---

## 0 · Verificación de entorno (protocolo §0)

```
$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable

$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
200
```

Sin `cloud_default`, INEGI responde `200`. Entorno correcto.

`data/raw` reportó ausente en el primer chequeo de este worktree (checkout
nuevo, `sesion/cal-conf-faseb-pos4-envipe-tpervic2-tmodvic-paso2` — ausente
no es PARO, es la trampa que el protocolo §0 anticipa). Se enlazó a la raíz
externa ya integrada al resto de la organización de trabajo (ruta real no
citada, por disciplina de §0): `ls data/raw | wc -l` → 133.

`python3 tests/bitacora.py --abre` confirmó, en el worktree de este acto:
HEAD == `origin/main` (`642be976c748f6e91a7888aceeb532e881fa100a`), sin
divergencia; `check.py --baseline` VERDE; `validador_registro_ids.py` OK
(49 reglas, 27 en perímetro).

**Base verificada.** El encargo pide `main` = `642be97`; mi checkout
inicial (`Modelado-Mexicano`, rama de otra sesión en curso) tenía `main`
local en `2a218a1`, **atrás** de `origin/main`. Se abrió worktree nuevo
(`/home/pc0/mm-envipe-tpervic2-medicion`) directamente desde
`origin/main` tras `git fetch`, confirmando `git rev-parse origin/main`
== `642be97` antes de tocar nada. Un intento de `git worktree add` fuera
del directorio de trabajo activo del sandbox falló con "could not lock
config file" — no era un lock real de git (el archivo resultante era un
nodo de dispositivo, artefacto del sandbox de escritura, no una sesión
concurrente reteniendo el lock); reintentado con el sandbox desactivado
para esa operación puntual, correcto en el segundo intento.

## 1 · Premisas (PK-1 a PK-7), verificadas contra archivo, no citadas a ciegas

| # | Verificación | Resultado |
|---|---|---|
| PK-1 | `forense/notas/2026-08-04-envipe-tper-vic2-tmod-vic-paso1.md` §5.1/§6 + CSV re-abierto esta sesión | Confirmado: `AP7_3_09`-`_14` sobre universo completo de `TPer_Vic2` (persona seleccionada 18+, `n`=91 182, sin condicionar a `RESUL_H`). Blancos re-contados directamente del CSV esta sesión: **cero** en las seis variables |
| PK-2 | misma nota §5.1 | Confirmado: `AP7_1`/`AP7_2` mezclan delito patrimonial (grupo B, 11 códigos) con violencia, agregados impuros, no sirven para el núcleo |
| PK-3 | misma nota §5.1 | Confirmado: `AP7_3_09` (extorsión) es coerción por amenaza consumada, pero con fin patrimonial (dinero/bienes) declarado y no resuelto — se mide aparte |
| PK-4 | Re-derivado con `grep -inE` sobre `forense/notas/2026-07-31-inventario-segmentacion.md` (esta sesión, independiente de la nota citada) | Confirmado: cero hits de `AP7_3_09`-`_14` en las 41 filas de Tabla B. Único hit es `AP7_1` — de **ENCUCI** (trabajo voluntario/comunidad), colisión de mnemónico entre encuestas distintas, no la `AP7_1` de ENVIPE de este acto |
| PK-5 | misma nota §8 | Confirmado, ABIERTO con riesgo concreto: `BP1_23` solo se pregunta a quien disparó el Instrumento B, es decir a quien contestó `AP7_3_XX`=1. No independientes por diseño. **Este acto lo sella como límite, ver §3.4** |
| PK-6 | misma nota §9, re-derivado con join propio a `TSDem` esta sesión | Confirmado y ampliado: edad y `DOMINIO` nativos; formalidad por join a `TSDem` (`AP3_8`/`AP3_10`, join por `ID_PER`, **100% de coincidencia**, 91182 de 91182); `ESTRATO` de área; sin acceso digital ni migración |
| PK-7 | `milpa/procedencia.yaml`, cabecera de clases (líneas 26-37) | Confirmado: `MEDIDO·PARCIAL(x)` exige declarar los ejes efectivos entre paréntesis y que la marca C3 viaje con el número |

Las siete premisas (1) se sostienen. Se procede.

## 2 · Composición del constructo

**Núcleo (los cinco limpios):** `AP7_3_10` (amenaza) · `AP7_3_11`
(agresión física con lesión) · `AP7_3_12` (secuestro) · `AP7_3_13`
(agresión sexual) · `AP7_3_14` (violación).

**`AP7_3_09` (extorsión) se mide aparte, no dentro del núcleo.** Razón:
su matiz patrimonial no está resuelto (§1, PK-3) y meterlo al agregado
impediría verlo después. Se reporta la condicional con y sin, para que
la diferencia sea visible.

**Forma:** binario "sufrió al menos uno de los del núcleo durante 2024",
más el desglose por los cinco ítems. `AP7_4_XX` (frecuencia) se reporta
como intensidad en la validación del estimador (§3.2), no entra al
binario del constructo.

## 3 · La medición

### 3.0 · Insumos, verificados

`data/raw/envipe2025_csv.zip` — sha256 `8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa`,
**coincide** con `data/manifiesto.yaml:308`. Extraído con `zipfile` de
Python (no hay `unzip` en el entorno). El CSV de `TPer_Vic2`
(`conjunto_de_datos_tper_vic2_envipe2025.csv`, 91 182 filas) usa
terminador de línea `\r` puro (sin `\n`) — `wc -l` reporta 0 por esta
razón, no por archivo vacío; leído con `csv.DictReader` en modo texto
(`newline=""`), que lo resuelve correctamente. `TSDem` extraída para el
join de formalidad, mismo zip.

### 3.1 · Estimador

- **Peso:** `FAC_ELE` ("Factor de personas elegidas", diccionario de
  datos de `TPer_Vic2`) — no `FAC_ELE_AM`, que es del área urbana de
  interés (subconjunto de 34 áreas, no el nacional). Verificado en el
  diccionario, no supuesto.
- **Universo:** las 91 182 filas, sin excluir ninguna — cero blancos en
  las seis variables candidatas (re-verificado, §1 PK-1).
- **Dispersión:** método de razón sobre conglomerado último
  ("ultimate cluster", Woodruff), `EST_DIS` como estrato de diseño y
  `UPM_DIS` como PSU. 746 estratos con ≥2 UPM, **cero estratos
  singleton** (ningún estrato quedó sin varianza estimable).
- **Distribución, no media puntual**, con intervalo al 95%.

### 3.2 · Estimador, validado contra caso conocido

Contrastado contra una cifra publicada de ENVIPE 2025 reproducible:
INEGI, *Encuesta Nacional de Victimización y Percepción sobre Seguridad
Pública (ENVIPE) 2025 — presentación nacional* (septiembre 2025), tema
"Caracterización del delito", slide "Delitos sexuales": **"violación
sexual = 279 delitos por cada 100 mil mujeres, 2024"**
(`https://www.inegi.org.mx/contenidos/programas/envipe/2025/doc/envipe2025_presentacion_nacional.pdf`,
también en el Reporte de Resultados 33/25,
`https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/ENVIPE/ENVIPE_25_RR.pdf`,
p.8).

Esa cifra es **incidencia** (delitos, no víctimas) — para reproducirla
hace falta la frecuencia (`AP7_4_14`), no solo el binario. Sobre mujeres
(`SEXO`=2) de `TPer_Vic2`, ponderado por `FAC_ELE`:

| Medida | Fórmula | Resultado | Publicado | Diferencia |
|---|---|---|---|---|
| Incidencia | Σ(`AP7_4_14`×`FAC_ELE`) / Σ`FAC_ELE` × 100 000 | **279.3** | 279 | **0.09%** |
| Prevalencia | Σ(`AP7_3_14`=1 × `FAC_ELE`) / Σ`FAC_ELE` × 100 000 | 197.4 | *(no publicado por tipo)* | — |

**Pipeline validado**: mismo peso (`FAC_ELE`), mismo universo
(`TPer_Vic2`, `SEXO`=2), misma variable de este acto (`AP7_3_14`/
`AP7_4_14`), reproduce el número publicado con 0.09% de diferencia —
dentro del redondeo. El constructo de este acto usa **prevalencia**
(binario "al menos uno"), no incidencia; INEGI no publica prevalencia
por tipo de delito a nivel nacional (solo incidencia y el agregado de
"cualquier delito"), así que la validación usa la mecánica de ponderación
ya probada sobre la variable que sí tiene contraste — la prevalencia es
una agregación más simple sobre la misma mecánica validada (indicador
binario en vez de suma de frecuencia).

**Negativo descartado, declarado para que no se reintente.** Se probó
`RESUL_H` (`descrip`: "Entrevista completa con/sin victimización")
ponderado por `FAC_ELE` como posible ancla de validación contra el
titular "23.1 millones de víctimas, tasa 24 135 por 100 mil habitantes,
2024" (mismo reporte, Cuadro 1). Resultado: **26 114.8** por 100 mil,
**+8.2%** sobre lo publicado — no valida. Razón, verificada: el propio
nombre del campo es "Resultado de la **visita al hogar**", no de la
persona; `RESUL_H` se dispara si **cualquier** integrante del hogar
reportó un delito en Sección VI (`AP6_*`, wording *"algún(a) integrante
de este hogar incluido(a) usted"*), no solo si la persona seleccionada
lo fue. Sobrecuenta relativo al titular de "personas víctimas" (que
cuenta solo delitos personales vía Sección VII, `AP7_3_XX`). Se probó
también el catálogo completo `AP7_3_05`-`_15` (todos los delitos
personales, incluidos los patrimoniales) contra el mismo titular:
**18 186.1** por 100 mil, **−24.6%** — tampoco valida, porque el titular
de 23.1 millones mezcla ponderación por persona (`FAC_ELE`) y por hogar
(`FAC_HOG`, para robo de vehículo/casa habitación, nota al pie del
reporte) de un modo que este acto no reproduce ni necesita reproducir
para su propio constructo.

### 3.3 · Ejes efectivos

`MEDIDO·PARCIAL(edad,dominio,formalidad,ESTRATO)`.

- **Edad × dominio, conjunto** (12 celdas: 4 bandas × 3 dominios).
- **Formalidad, marginal, vía join a `TSDem`** (`ID_PER`, 100% de
  coincidencia: 91 182 de 91 182). Proxy rugoso: posición en la
  ocupación (`AP3_10`: jornalero/empleado-obrero/cuenta propia/patrón/
  sin pago), condicionado a haber trabajado (`AP3_8`=1) — **no** es
  verificación de registro formal ante seguridad social. `n`=56 829
  (62.3%) — el n aguanta.
- **ESTRATO de área, marginal** (1-4, no ingreso individual).
- **NO DISPONIBLES**: acceso digital, migración — mismo límite que
  `TPer_Vic1`/ENDIREH, declarado y no forzado.

### 3.4 · C2 — sellado, no resuelto

Dos salidas aceptables por el encargo, elegida **(b): sellar como límite
declarado**, no (a) resolver.

**Argumento.** Resolver (a) exigiría afirmar, en este acto, que
`exposicion_violencia` nunca se usará junto a `comunicacion.inseguridad.
ver_oir_callar` en la misma ecuación — eso es una decisión sobre CÓMO SE
OPERACIONALIZA `ver_oir_callar` (si con `BP1_23` o con otra cosa), y esa
decisión no le corresponde a un acto de medición de
`exposicion_violencia`: es adjudicación de la otra variable, prohibida
aquí igual que adjudicar CP-1 estaba prohibido en el acto de búsqueda
(protocolo §4.1). Sellar (b) es la salida honesta: la dependencia queda
escrita, pegada al número en `milpa/procedencia.yaml` (`limite_c2`), y
`hitoE §22`, para que quien opere `BP1_23`/`ver_oir_callar` la encuentre
sin tener que releer esta nota.

**La dependencia, en sus propios términos.** `BP1_23` (`TMod_Vic`) solo
se pregunta a quien ya contestó `BP1_20`=No (no denunció), que a su vez
solo se pregunta a quien ya disparó el Instrumento B — es decir, a quien
contestó `AP7_3_XX`=1 (o `AP6_6`=1) en `TPer_Vic2`. Si ambas variables
entran a la misma ecuación, no son independientes por diseño del
instrumento — dependencia **estructural de aplicación**, no de contenido
(C3, §3.5, pasa limpio).

### 3.5 · C3 — pegada al número

Re-derivado con `grep -inE` directo sobre
`forense/notas/2026-07-31-inventario-segmentacion.md` (independiente de
la nota de paso 1, comando propio de esta sesión, §1 arriba): **cero**
hits de `AP7_3_09`-`_14` en las 41 filas de Tabla B. Único hit de
mnemónico es `AP7_1` de **ENCUCI** (trabajo voluntario/comunidad,
`inventario-segmentacion.md:272`) — colisión de nombre entre encuestas
distintas, ya documentada por la nota de paso 1 §7, re-confirmada aquí.
Limpio, viaja con el número en `milpa/procedencia.yaml` (`marca_c3`).

## 4 · Distribución

| Medida | Proporción ponderada | IC 95% | n crudo | Población ponderada | Tasa/100k |
|---|---|---|---|---|---|
| **Núcleo (sin extorsión)** | **5.675%** | [5.427%, 5.924%] | 4 822 | 5 436 874 | 5 675.5 |
| **Con extorsión (`AP7_3_09` sumada)** | **9.668%** | [9.358%, 9.977%] | 8 464 | 9 261 225 | 9 667.7 |

**Desglose por ítem** (ponderado, tasa/100k): `AP7_3_09` (extorsión)
4 750.4 · `AP7_3_10` (amenaza) 3 472.5 · `AP7_3_11` (lesión) 1 340.3 ·
`AP7_3_12` (secuestro) 77.6 · `AP7_3_13` (agresión sexual) 1 473.7 ·
`AP7_3_14` (violación) 128.2.

**Por DOMINIO** (núcleo, sin extorsión): Urbano 6.861% · Complemento
urbano 5.104% · Rural 2.868%.

**Por ESTRATO de área** (marginal, no ingreso individual): 1 → 3.776% ·
2 → 5.464% · 3 → 6.757% · 4 → 6.733%.

**Por banda de edad**: 18-29 → 9.680% · 30-44 → 6.277% · 45-59 → 4.056%
· 60+ → 2.022%.

**Por posición en la ocupación** (formalidad, marginal, solo ocupados,
`n`=56 829): jornalero 2.230% · empleado/obrero 6.683% · cuenta propia
6.336% · patrón 6.015% · sin pago 5.168%.

**Periodo:** 2024, 12 meses (enero-diciembre) — eventos consumados
durante el año, **no** ventana de vida. Distinto de ENDIREH, que trae
ventana de vida para algunos tipos; nunca se suman ni promedian (CP-1).

## 5 · Cascada ejecutada

- `milpa/procedencia.yaml`: entrada nueva `exposicion_violencia` en
  `condicionales_escalares_exposicion_violencia`, clase
  `MEDIDO·PARCIAL(edad,dominio,formalidad,ESTRATO)`, con `marca_c3` y
  `limite_c2` pegados al número.
- `canon/modelo-decision-v4_0.md`: §1.1.F Paso 5 (tabla de reparto,
  criterio, fila MEDIDAS) — contador ~~8~~ **9** de 14, reparto
  9+0+2+3; §6.1 y §7 (callouts del contador); H-12 — cita del reactivo
  corregida (el anterior, `BP1_20`/`23`/`28`, estaba retirado desde
  `PR #57`), tier e hipótesis **no re-evaluados** (adjudicación, fuera
  de alcance).
- `forense/hitoE-campana-medicion-v2_0.md` §22: adenda fechada,
  cierra fila 4 de §14.3 (no se edita la fila).
- `forense/hallazgos.md`: línea de cierre, append-only.
- Gobernanza: **sin ADR nuevo**. Patrón de casa verificado: los ocho
  `MEDIDO·PARCIAL(x)` previos (`radio_confianza`, `familismo_apoyo`, los
  seis componentes de `confianza_institucional`) se propagaron sin ADR
  — solo `canon/` + `milpa/` + `hitoE`. El patrón que sí requirió ADR
  (ADR-54, `sens_estatus`) fue un **juicio de cierre de búsqueda**
  (agotamiento), no una medición exitosa. Este acto es lo segundo, no lo
  primero: propagación directa, sin inventar ADR.

**La clase "búsqueda abierta" queda vacía**, dicho explícito: no por
agotar los tres actos de la condición de caducidad de ADR-52 A (que
sigue intacta como criterio para cualquier búsqueda futura que caiga
ahí), sino porque el segundo acto de búsqueda
(`forense/notas/2026-08-04-envipe-tper-vic2-tmod-vic-paso1.md`) encontró
candidato válido y este acto lo midió.

## 6 · Qué NO se hizo

- No se adjudicó H-12 (la hipótesis ingreso-exposición) — se corrigió
  su cita de reactivo, no se probó contra el nuevo dato.
- No se resolvió C2 — se selló, con argumento (§3.4).
- No se tocó ENDIREH.
- No se inventó ADR.
- No se fusionó el PR de este acto.

## 7 · Suite, corrida tras la última edición

```
$ python3 tests/check.py --baseline
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json

$ python3 tests/validador_registro_ids.py
OK — 49 reglas · 27 en perímetro · 49 IDs verificados
```

VERDE. Ningún rojo nuevo que explicar.
