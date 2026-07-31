> **Qué es.** Diagnóstico y plan de salida acordados en mesa con el autor el 30/jul/2026, tras una jornada de 15 PR y cero mediciones. Su regla central quedó sellada como ADR-48.
> **Estado.** Propuesta sin sello. Se sube **verbatim**, sin corregir sus cifras: el campo `casos` de `I-13` dice **1**, no los 3 que el plan le atribuye, y así se congeló.

# RECOVERY · del aparato al número
### v1.0 · 30/jul/2026 · propuesta sin sello

---

## El diagnóstico, en una línea

Hoy: 15 PR, 40 entradas de cola, 3 ADR, 54 payloads bajados — y **cero mediciones**. `2 de 27` y `0 de 15` están donde amanecieron.

El aparato se construyó contra una falla real y la resolvió. Lo que creció después audita la contabilidad del programa sobre sí mismo, no la evidencia sobre México. Ningún defecto catalogado hoy habría dañado a un lector.

---

## La regla que sustituye a los módulos de auditoría

> **Cada sesión produce una medición, o produce nada.**
> Si encuentra un defecto: una línea en `hallazgos.md` y sigue.
> Si el defecto impide medir: se para y reporta.
> Si no impide medir: no se cataloga.

---

## R0 · Congelar el aparato — una sesión, hoy

**Se corta:**

| Qué | Por qué |
|---|---|
| `cola.yaml` | 40 entradas, 24+ abiertas, ninguna mueve un contador. **Se mueve a `forense/hallazgos-congelados-2026-07-30.yaml`.** No se borra: sale del canon |
| Módulo de auditoría en todo artefacto | Solo en los que afirman algo sobre México |
| ADR para toda decisión | Solo para lo reversible que alguien pueda deshacer sin saber por qué. Van 47 |
| Nombres de archivo versionados | Cada `v1.14→v1.15` dispara retropropagación y una corrección de cabecera que ya falló 3 veces. El versionado vive en git |
| `bitacora.py --cierra` por sesión | Tiene 3 defectos conocidos, nadie lo lee. Se apaga hasta que alguien lo arregle o lo entierre |
| Sesiones concurrentes | Hoy costaron media jornada en conflictos y no compraron nada. **Una a la vez** |

**Se conserva, y es todo:**

`check.py` en CI · el pre-registro antes de abrir dato · las marcas de procedencia y tier · `forense/` append-only.

**Excepción única para no perder trabajo hecho:** de las 40 entradas congeladas, dos se cierran de verdad porque su solución es trivial y su costo es recurrente — **`I-13`**, con IDs que no requieran coordinación entre sesiones (`D-20260730-1423` o hash corto), e **`I-01`**, con la marca explícita de cita ilustrativa. Tres casos con hash cada una. Lo demás se congela.

---

## R1 · La primera medición — `CAL-G3` Fase C

**No falta ninguna decisión. Falta correrla.** Las tres olas están en disco con `sha256` derivado, la spec está sellada, `D-09` y `D-10` resueltas, ADR-47 sellado, `CAL-X` corrido.

**Entorno:** Ubuntu local. **Modelo:** Opus — es la primera y fija el patrón para el lote.

**Sale:** una elasticidad con banda, fuente y ventana temporal. No calibra el `-0.60`, no falsa nada, no lo necesita.

---

## R2 · El lote — cuatro mediciones con dato ya en disco

El cruce de fuentes las identificó y **los payloads ya están registrados**:

| Ficha | Qué mide | Fuente en disco |
|---|---|---|
| `R8.2` | tandas entre desconocidos | **ENIF** · 3 olas |
| `R10.3` | silencio ante inseguridad | **ENVIPE** · 8 olas |
| `R1.4` | consumo compensatorio por decil | **ENIGH** · 6 olas |
| `R1.3` | canal de confianza → adopción | **ENIF** · cubre 2/3 del umbral |

**Antes de cada una, una decisión de una línea (ADR-47):** ¿es falsación o es medición? Si el umbral pide poder para refutar y el desenlace es raro, es medición — y entonces no lleva veredicto, lleva banda.

**Modelo:** Sonnet. Es mecánico una vez que R1 fijó el patrón. **Una sesión por ficha, una a la vez.**

---

## R3 · El benchmark — lo que decide si algo sirvió

Tres brazos, mismo modelo, preguntas pre-registradas: **LLM solo** · **LLM + reglas** · **LLM + reglas + capa medida**.

Si el brazo 3 no le gana al 2, y el 2 no le gana al 1, el motor no aporta sobre un LLM. Ese resultado se publica.

**Tiene reloj:** el repo es público. Cuando se indexe, el brazo 1 deja de ser limpio.

---

## Condición de parada del propio plan

**Si R1 no produce un número, el problema no es el plan.** Sería que el aparato no puede producir mediciones ni con el dato en disco, la spec sellada y todas las decisiones tomadas. En ese caso lo que sobra no es la ceremonia: es el modelo de decisión.

---

## Lo que queda fuera a propósito

`R3.1` y `R3.4` (`D1`) · las 15 fichas huérfanas · ENSANUT y ENUT sin registrar · el Hito E completo · la reclasificación del perímetro de 27 · las 38 entradas congeladas.

Nada de eso desaparece. Espera a que existan cinco números medidos.
