# HITO D · Paso 2 · Corrida **R3.1** — propuesta de veredicto, no adjudicada
### `hitoD-R3.1` · **v1.0** · 4 de agosto de 2026 · **Trámite presencial discrecional sin registro → mordida**

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R3.1-veredicto-v1.0.md` |
> | **REEMPLAZA A** | — *(nuevo)* |
> | **VERIFICAS ASÍ** | la propuesta es fila `B`, trae los seis cómputos (dos interpretaciones de `P8_4` × sin ponderar/`FAC_TRA`/`FAC_P18`), la validación de canalización contra el techo de `hitoD-R3.2` (13.38%), y el chequeo de composición por `N_TRA` |
> | **NOMBRE ESTABLE** | **`hitoD-R3.1`** |
> | **ESPECIFICACIÓN CONGELADA** | `forense/hitoD-R3_1-especificacion-v1_0.md`, commit previo a este — no se editó tras ver el resultado |

> ⚠️ **ARTEFACTO FORENSE FECHADO — append-only.** Registra lo hallado el 4/ago/2026 contra ENCIG 2023 (microdatos, tablas `encig2023_04_sec_7` y `encig2023_05_sec_8`, mismos payloads que `hitoD-R3.2` ya usó — `data/manifiesto.yaml`, verificados COINCIDE antes de abrir el ZIP). No se actualiza: reescribirlo para que cuadre con el estado posterior sería la racionalización post-hoc que el Bloque C prohíbe. **Este veredicto NO está archivado** — es una propuesta para que mesa adjudique (ver §4).

---

## 1 · Lo que estaba pre-registrado *(citado literal, para probar que no se movió)*

> **Regla.** `modelo §3.3`: *"SI el trámite es presencial con funcionario discrecional y sin registro ENTONCES alta probabilidad de mordida — PORQUE trampa social (G1)"* — `[FUERTE]`, `tramite.yaml: tramite.mordida.discrecional`.
>
> **Regla de selección de pregunta ejecutada:** Respaldo 1 (`N_TRA` como proxy de discrecionalidad, clasificación externa declarada en `hitoD-R3.1-especificacion-v1.0.md §2`, ANTES de abrir el ZIP). No existía candidata primaria (verificado contra el diccionario, mismo documento §1).
>
> **Umbral.** Brecha de incidencia ≥20pp en la dirección predicha, dentro de la rama presencial (`P7_3=1`) — declarado `ASIGNADO`, no derivado (ficha, línea 752).
>
> **Techo de veredicto fijado ANTES de correr:** Respaldo 1 **nunca produce `A`** (ficha, línea 762; resuelto contra la fila `A` de la escala en `hitoD-R3.1-especificacion-v1.0.md §4`). Solo `B` o `C` son alcanzables por esta corrida.

---

## 2 · Veredicto propuesto: **B**

### 2.1 · Validación de canalización — reproduce el techo archivado de `R3.2`, a los dos decimales

Antes de correr el contraste ALTA/BAJA, se recomputó la incidencia presencial agregada (`P7_3=1`, sin distinguir grupo) sobre el mismo par de tablas, para verificar que la unión/filtros/ponderadores de este acto están bien construidos:

| interpretación | ponderador | este acto | `hitoD-R3.2` (archivado) |
|---|---|---|---|
| (a) restrictiva | sin ponderar | 12.21% | 12.21% |
| (a) restrictiva | `FAC_TRA` | 10.81% | 10.81% |
| (a) restrictiva | `FAC_P18` | 13.38% | 13.38% |
| (b) NA→0 | sin ponderar | 1.84% | 1.84% |
| (b) NA→0 | `FAC_TRA` | 1.42% | 1.42% |
| (b) NA→0 | `FAC_P18` | 2.04% | 2.04% |

Coincidencia exacta en los seis regímenes. No hay ancla académica externa para el estimando específico de esta ficha (declarado como límite en la especificación, §6) — esta es la validación de canalización que sustituye a esa ancla ausente, no una validación del estimando en sí.

### 2.2 · Dirección confirmada en seis cómputos, brecha 9.28pp–32.73pp, razón 5.05x–21.81x

Universo: `P7_3=1` ∩ `N_TRA` clasificado (ALTA={11,12,13,17,18,20}, BAJA={01,02,03,04,07,09,10,14,15,16}), llave `CVE_ENT+UPM+V_SEL+R_ELE+N_TRA`, duplicados de `NT_TIPO` colapsados si `P7_3` consistente (7,101) o excluidos si divergente (543) — mismo tratamiento que `R3.2 §2.6.4`, recalculado sobre este subconjunto (no reutiliza el conteo de `R3.2`, que era sobre el universo completo).

| interpretación | ponderador | ALTA (n / p̂ / IC95%) | BAJA (n / p̂ / IC95%) | brecha (pp) | razón |
|---|---|---|---|---|---|
| (a) restrictiva | sin ponderar | 961 / 32.57% / [29.73,35.41] | 5964 / 6.46% / [5.85,7.06] | **26.11** | 5.045x |
| (a) restrictiva | `FAC_TRA` | 961 / 38.31% / [31.67,44.95] | 5964 / 5.58% / [4.28,6.88] | **32.73** | 6.870x |
| (a) restrictiva | `FAC_P18` | 961 / 36.84% / [31.68,41.99] | 5964 / 7.13% / [5.89,8.37] | **29.70** | 5.165x |
| (b) NA→0 | sin ponderar | 3096 / 10.11% / [9.02,11.20] | 46185 / 0.83% / [0.75,0.92] | **9.28** | 12.128x |
| (b) NA→0 | `FAC_TRA` | 3096 / 14.09% / [10.61,17.58] | 46185 / 0.65% / [0.49,0.81] | **13.45** | 21.806x |
| (b) NA→0 | `FAC_P18` | 3096 / 12.05% / [9.80,14.30] | 46185 / 0.94% / [0.75,1.13] | **11.11** | 12.827x |

En los seis, dirección predicha (ALTA > BAJA), y en **ninguno de los seis el IC95% de ALTA traslapa con el de BAJA** — la separación es limpia, no hay caso donde el intervalo de la brecha cruce cero (reserva de tipo `R5.2` **no aplica aquí**: la señal no es un punto límite, es una separación clara en las seis lecturas). Cuatro de seis cómputos cruzan el umbral de 20pp declarado (interpretación (a), las tres ponderaciones); los tres cómputos de interpretación (b) NA→0 no lo cruzan (9.28–13.45pp) — **esto no cambia el veredicto**: el techo de `B` ya estaba fijado antes de ver el resultado (Respaldo 1 nunca produce `A`, §1), así que la magnitud de la brecha no se evalúa contra el umbral de 20pp para efectos de la fila — solo la dirección y la ausencia/presencia de brecha importan para decidir entre `B` y `C`.

### 2.3 · Por qué `B` y no `C`: la brecha no está ausente ni invertida en ningún cómputo

Regla de la ficha (línea 784): `C` exige brecha ausente o invertida. Los seis cómputos muestran ALTA > BAJA, con separación de IC no traslapada en los seis. `C` no se satisface bajo ninguna lectura.

### 2.4 · Confundidor 1 (composición de trámites) — no aislado por pareo, pero contextualizado

El techo de `B` ya asume que este camino no aísla el confundidor 1 (línea 762: Respaldo 1 "no aísla discrecionalidad de tipo de trámite"). Como contexto, no como intento de subir a `A`, incidencia por `N_TRA` individual (interpretación (a), `FAC_P18`):

| grupo | `N_TRA` | n | incidencia |
|---|---|---|---|
| ALTA | 11 (servicios municipales) | 100 | 21.00% |
| ALTA | 12 (permisos locales) | 76 | 28.95% |
| ALTA | 13 (uso de suelo/construcción) | 125 | 32.00% |
| ALTA | 17 (MP/Fiscalía) | 372 | 38.71% |
| ALTA | 18 (juzgado/tribunal) | 288 | 29.86% |
| BAJA | 01 (luz) | 399 | 3.51% |
| BAJA | 02 (agua) | 991 | 2.02% |
| BAJA | 03 (predial) | 792 | 2.65% |
| BAJA | 04 (tenencia vehicular) | 912 | 11.95% |
| BAJA | 07 (citas médicas) | 1098 | 3.55% |
| BAJA | 09 (educación) | 501 | 5.59% |
| BAJA | 10 (Registro Civil) | 732 | 13.66% |
| BAJA | 14 (créditos vivienda/Bienestar) | 98 | 9.18% |
| BAJA | 15 (CFE) | 140 | 10.71% |
| BAJA | 16 (pasaporte) | 301 | 9.97% |

Los cinco `N_TRA` de ALTA están todos por encima de 21%; nueve de diez `N_TRA` de BAJA están por debajo de 14%. **Excepción notable, declarada sin maquillar:** `N_TRA=04` (tenencia/impuesto vehicular, clasificado BAJA por ser pago de tarifa fija con recibo) tiene 11.95%, y `N_TRA=10` (Registro Civil, BAJA) tiene 13.66% — ambos más altos que el resto del grupo BAJA, aunque siguen por debajo del piso de ALTA (21.00%). No cambian la dirección ni el veredicto, pero indican que la clasificación BAJA no es perfectamente homogénea — se declara como límite (§3).

### 2.5 · Confundidores 2-4 — no ejecutados en este acto

**Confundidor 2 (composición del usuario)** y **confundidor 3 (endogeneidad geográfica/institucional)**: la ficha (líneas 769-770) los declara a aislar "si ENCIG lo permite"/"comparando dentro de la misma entidad" — no se ejecutaron en esta corrida por alcance (el techo ya está fijado en `B` independientemente de su resultado; ejecutarlos no podría mover el veredicto a `A`, solo describir mejor un `B` ya alcanzado). Se declara como trabajo no hecho, no como hueco oculto. **Confundidor 4 (sesgo de reporte)**: se aplica como descuento declarado, no como duda a resolver (línea 771) — no infla `B` hacia arriba, ya está incorporado como lectura conservadora.

---

## 3 · Límites declarados

1. **Heterogeneidad dentro de BAJA** (§2.4): `N_TRA` 04 y 10 tienen incidencia más alta que el resto del grupo BAJA — la clasificación por conocimiento externo no captura toda la varianza dentro del grupo.
2. **Correlación, no mecanismo** (ficha, línea 774): un veredicto `B` no confirma que "trampa social" (equilibrio de creencias) sea el mecanismo causal — solo que existe un patrón de discrecionalidad-incidencia.
3. **Sin pareo por tipo de trámite individual** (§1, §2.2): es la razón declarada de antemano del techo `B`, no un hallazgo posterior.
4. **Códigos excluidos** (05, 06, 08, 19, 21, 22A-22E — especificación §2): 10 de 26 códigos de `N_TRA` quedan fuera de ambos grupos por heterogeneidad interna del código o por no encajar el mecanismo de la ficha. No se fuerza su clasificación.
5. **Cobertura poblacional de ENCIG** (mismo límite que `R3.2 §2.6.6`): población de 18 años y más en ciudades de 100,000 habitantes y más — no dice nada sobre población rural o de ciudades menores.
6. **Sin ancla académica externa** para este estimando específico (especificación §6) — la validación de canalización (§2.1) sustituye, no reemplaza, esa ausencia.

---

## 4 · Por qué **B** y no A / C / D — y por qué esto es una PROPUESTA, no un archivo

| | Por qué no / por qué sí |
|---|---|
| **A · Confirmada** | Estructuralmente inalcanzable por este camino (Respaldo 1, ficha línea 762) — no se evalúa aunque 4/6 cómputos crucen 20pp |
| **B · Sostenida, no cerrada** ✅ | Brecha real (9.28–32.73pp), dirección predicha en 6/6, IC no traslapado en ningún cómputo — degrada a `[MEDIA]` por la letra de la ficha, no refuta |
| **C · Refutada** | La brecha no está ausente ni invertida en ningún cómputo (6/6 en la dirección predicha); refutar exigiría lo contrario |
| **D · Inejecutable** | ENCIG 2023 sí permitió la prueba vía Respaldo 1 |

**Esta propuesta NO se escribe en `## Registro de veredictos archivados`** (`forense/hitoD-preregistro-v2_0.md`, ADR-40) — ese bloque es append-only y solo mesa adjudica, mismo criterio que `R5.1`/Nota 16, `R5.2`/Nota 18. El contador de Paso 2 (`estado-programa`, actualmente "11 de 27") no cambia por este documento.

---

## 5 · Declaración ADR-46

Al abrir `encig23_base_datos_csv.zip` en este acto, esta sesión queda **inhabilitada para pre-registrar ninguna otra ficha contra ENCIG** (ADR-46). No se abrieron `encig2023_01_sec_11.csv`, `encig2023_01_sec1_A_3_4_5_8_9_10.csv`, `encig2023_02_residentes_sec_2.csv` ni `encig2023_03_sec_6.csv` — solo `sec_7` y `sec_8`, misma restricción de lectura que `R3.1`/`R5.1`/`R7.2` comparten (`data/manifiesto.yaml:40`).
