# Registro de recálculo
### `registro-recalculo` · **v1.0** · 13 de agosto de 2026 · ENCARGO ADR-PROVISIONALIDAD (nube) · abre la cola que ADR-72 instituye

> | | |
> |---|---|
> | **ARCHIVO** | `registro-recalculo-v1_0.md` |
> | **NOMBRE ESTABLE** | **`registro-recalculo`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Registro append-only, una fila por entrada de recálculo (ADR-72, `canon/gobernanza-v1_15.md`). Cola de todo veredicto, coeficiente, contador, reparto o cierre de búsqueda declarado `PROVISIONAL` por ADR-72, ordenada por palanca — no por número de ADR. |
> | **QUÉ NO ES** | No adjudica ningún veredicto por sí mismo — cada entrada se cierra en acto propio, uno por entrada (Método, ADR-72). No es el censo de estimabilidad (`forense/censo-estimabilidad-coeficientes-v1_0.md`), que es la entrada 1 de aquí, acto aparte. No es el registro de llaves de identificación (`forense/registro-llaves-identificacion-v1_0.md`), población de conteo distinta — ninguna fila de aquí mueve `llaves de identificación ejercidas`. |
> | **VERIFICAS ASÍ** | §1 trae las cinco entradas iniciales (1-5), en el mismo orden y el mismo texto con que ADR-72 §2.4 las declaró al sellarse, más la entrada `0` que su enmienda de COMMIT 2 (ADDENDA 5) añadió el mismo día. |

---

## 0 · Qué es una entrada

`ADR-72` declara `PROVISIONAL` todo veredicto, coeficiente, contador, reparto y cierre de búsqueda producido por este programa antes del 13/ago/2026, por haberse derivado contra un universo de corpus que no era el universo real y que ninguno declaró. Este archivo es la cola citable donde cada entrada provisional se re-examina, un acto a la vez.

**Regla de señal, verbatim de ADR-72:** "cada acto de recálculo produce un veredicto de los tres, o produce nada. Un acto que vuelve con 'sigue pendiente' no cierra su entrada."

**Los tres veredictos de cierre — los tres cierre válido:**

| veredicto | significa |
|---|---|
| `RECALCULADO — SIN CAMBIO` | se re-examinó contra el universo declarado completo y se sostiene, ahora con universo declarado |
| `RECALCULADO — CAMBIA` | se re-examinó y cambia; se propaga con su propio ADR |
| `RECALCULADO — INDECIDIBLE` | se re-examinó y no se pudo decidir; se dice qué haría falta |

**No es cierre** *"se revisó y parece bien"* sin universo escrito — eso es exactamente lo que produjo la situación que ADR-72 declara.

---

## 1 · Tabla — seis entradas iniciales: cinco verbatim de ADR-72 §2.4, más la entrada `0` de su enmienda

| # | entrada | clase | por qué va aquí | gate | estado |
|---|---|---|---|---|---|
| 0 | **Cotejo censo ↔ relaciones.tsv** — las 15 filas del censo de coeficientes contra `capa4_apertura_mapeo` de las necesidades correspondientes en `data/curacion-registro/relaciones.tsv` | A | mide el desacuerdo entre las dos tablas consolidadas del programa; hoy son **≥3 filas confirmadas** (12·`familismo_apoyo`, 13·`familismo_obligacion`, 14·`radio_confianza` — las tres `SIN-RUTA` en el censo, las tres `EXISTE-SATISFACE`/`CONFIRMADA` en `relaciones.tsv` para N12/N13/N14) y nadie lo vigila — `grep -rln "censo-estimabilidad" tests/ tools/` → 0 | ninguno | `ABIERTA — la absorbe CENSO-v1.1 (entrada 1, mismo acto)` |
| 1 | **Censo v1.1** — cruce de ENASEM (3 olas, 6 payloads) contra los 15 coeficientes, y universo de llaves declarado en las 9 `SIN-RUTA` | A | única entrada que puede mover un **denominador**; la nombró el propio censo v1.0 | ninguno | `ABIERTA — encargo emitido 13/ago` |
| 2 | **ADR-52 A y ADR-54** — reapertura acotada de las dos búsquedas cerradas | C | gatean 4 `SIN-RUTA`; APERTURA-ISSP produce el reporte con el que se deciden | reporte de APERTURA-ISSP fusionado | `ABIERTA` |
| 3 | **Los 7 veredictos `D` del Hito D** — uno por acto, ficha B-bis propia | B | archivo por hueco de diseño: hay que preguntar si el hueco era de instrumento y el instrumento estaba en disco | entradas 1 y 2 | `ABIERTA` |
| 4 | **Censo de explotación** — apertura por payload sobre los 550 | A | instituye el contador del ADR y evita la repetición | ninguno | `ABIERTA` |
| 5 | **ADR-50 / ADR-51 / ADR-57(c)** | D | dependen del reparto de la entrada 1 | entrada 1 | `ABIERTA` |

**Cada entrada cierra con:** el acto que la cerró (PR), el veredicto de los tres, y **el universo declarado en la misma línea.**

---

## 2 · Contador instituido por ADR-72

`payloads con apertura registrada / payloads en manifiesto` — al sellar ADR-72, **8 de 550 = 1.45%**.

Derivación (verbatim de ADR-72): cruzar los `id_manifiesto` de los TSV de apertura a nivel variable (`data/abrir4-variables-2026-08-08.tsv` + `data/verif3-variables-2026-08-08.tsv`) contra las entradas con `archivo`+`sha256` del manifiesto.

Este es un contador de medición sobre México y **ADR-72 no lo mueve — lo instituye.** Su primer movimiento, si lo hay, lo produce la entrada 4 de este registro.

---

## 3 · Segundo contador, instituido por la enmienda de COMMIT 2 (ADDENDA 5)

`filas de consolidación en desacuerdo entre sí` — el censo de coeficientes (`forense/censo-estimabilidad-coeficientes-v1_0.md`) y el registro de demanda (`data/curacion-registro/relaciones.tsv`) no se cotejan entre sí por ningún mecanismo (`grep -rln "censo-estimabilidad" tests/ tools/` → 0), y hoy se contradicen en al menos **3 filas verificadas**: las filas 12/13/14 del censo (`familismo_apoyo`/`familismo_obligacion`/`radio_confianza`) declaran `SIN-RUTA`, "Ninguna llave aplica", mientras `relaciones.tsv` trae `capa4_apertura_mapeo=EXISTE-SATISFACE` + `clasificacion_relacion=CONFIRMADA` para las mismas necesidades (`N12`/`N13`/`N14` — `REL-4a609c6633a4bafac14a6930` · `REL-fe202a3fa76f0516a6e27f8b` · `REL-5741e12ce3e0a0e076ee48fc`).

**Cotejo parcial, declarado, no las 15.** El censo no trae un campo `necesidad_id` cruzable por máquina contra `relaciones.tsv` — identificar la necesidad conceptual de cada una de sus 15 filas exige la misma lectura semántica que resolvió estas tres. Ese cotejo completo es la entrada `0` de §1, que este mismo acto abre y no cierra — cerrarla aquí habría abierto el censo en bloque, lo que el Método de ADR-72 prohíbe ("un acto por entrada").

Justificación bajo el impuesto de v2.3 (misma que el contador de §2): el defecto ya ocurrió — tres coeficientes clasificados sin ruta mientras su reactivo estaba `EXISTE-SATISFACE` en la otra tabla consolidada del programa, sin que nada lo señalara — y es derivable con un cruce de dos archivos, no con un módulo de auditoría nuevo.

---

*Append-only. Nueva entrada = nueva fila, nunca edición de una fila existente salvo para llenar `estado` al cerrarla. Este archivo no adjudica — registra.*
