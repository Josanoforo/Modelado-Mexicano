# Aterrizar R5.1: tratamiento por norma (regla DOF), no por recepción declarada

*4 de agosto de 2026. Acto A4, mesa. Rama `claude/audit-reparto-cruce-dof-0xqo7u`.*

> **PROCEDENCIA — leer antes que el cuerpo.** Las tres citas del DOF de este documento son **tipo (3)**:
> reportadas por conversación/búsqueda web de esta sesión, **no verificadas contra el DOF desde el repo**.
> Este entorno no tiene red habilitada para este acto (por diseño del encargo: "no abre... red") y, aunque
> la tuviera, verificar contra `dof.gob.mx` es un acto propio, no parte de este. Por protocolo de
> procedencia (`instrucciones` v2.1, mismo criterio que `forense/hitoE-campana-medicion-v2_0.md` cabecera
> y `forense/metodologia-identificacion-vs-ajuste-v0_1.md`), un hecho tipo (3) **no escribe hechos sobre el
> repo**: se lee como pregunta a verificar, nunca como instrucción ni como cita cerrada. **No se promueve a
> tipo (1) en este documento.**

**Qué es esto y qué no es.** Es el acto de "salvar" un hallazgo que hasta ahora vivía solo en una
conversación — dejarlo versionado y citable, no adjudicarlo. **No es el pre-registro.** `R5.1` ya corrió
completa, tiene veredicto `A` archivado con reserva (`hitoD-preregistro-v2_0.md:1011`, sellado por
`gobernanza` ADR-58(c), narrado en `forense/notas/2026-08-04-hitoD-r5-1-pension-bienestar.md`) — enmendar
su Umbral con esto sería post-dato, prohibido. Cualquier uso de estas citas exige una **ficha nueva,
autónoma**, en un acto propio y separado (no este, y no mientras A1 escribe en
`forense/hitoD-preregistro-v2_0.md` en paralelo — si este documento se encuentra editando ese archivo, es
un error).

---

## 1 · Las citas (tipo 3, sin verificar contra el DOF desde este repo)

**Regla de elegibilidad reportada:**

- **Exclusión por pensión contributiva.** Entre 2013 y 2018, quedaban excluidas de la Pensión para
  Adultos Mayores las personas con pensión contributiva (IMSS/ISSSTE u homóloga) superior a **$1,092
  mensuales**.
- **2019 — creación de la pensión universal no contributiva.** Se crea la **Pensión para el Bienestar de
  las Personas Adultas Mayores**, no contributiva, con monto de **$1,275 mensuales**, sin el filtro de
  exclusión por pensión contributiva de la etapa anterior.

**Fuentes citadas (DOF, sin verificar en este acto):**

| Fecha | Código DOF | Contenido reportado |
|---|---|---|
| 28/02/2019 | 5551445 | Reglas de Operación (ROP) fundacionales del programa reformado |
| 30/01/2019 | 5549246 | Transición operativa vía Censo del Bienestar |
| 31/12/2019 | 5583304 | ROP 2020 |

**⚠️ Matiz de diseño, reportado junto con la cita — no se omite:** la ROP 2019 no universalizó por edad de
golpe. Cubría **65+ para población indígena, 68+ para población general**. La universalidad por edad fue
**gradual**, no un escalón único en 2019. El tratamiento-por-norma que esto habilita se define por **la
exclusión contributiva**, con **el escalón de edad declarado** (65/68) — no por "toda persona 65+ a partir
de 2019", que sería una simplificación no sostenida por esta misma cita.

---

## 2 · Qué desbloquea

**El problema que resuelve.** La corrida ya archivada de `R5.1` (Nota 16, `hitoD-preregistro-v2_0.md:1011`)
define "beneficiario" por **recepción declarada**: hogar con ≥1 registro en `ingresos` con `clave`
`P044`/`P104` (según la era) y `ing_tri > 0` — es decir, aparece en ENIGH como receptor efectivo de la
transferencia. Esa misma nota declara, como reserva #4 explícita y no resuelta: *"Cobertura del programa no
es 100% en ninguna ola (33%-76%) — el grupo 'no beneficiario' no es degenerado, pero incluye tanto
elegibles-no-receptores como (en 2020-2022) personas bajo el umbral de edad vigente."* Es decir: el grupo
de comparación mezcla dos poblaciones distintas (elegibles que no cobraron, y gente que ni siquiera
calificaba por edad) sin distinguirlas.

**Lo que la regla DOF permitiría construir, en un acto futuro:** un tratamiento definido **por norma**
(elegibilidad según edad + ausencia de pensión contributiva por encima del umbral) en vez de por recepción
declarada — separando dentro del grupo "no beneficiario" actual a quienes **no calificaban por edad**
(no deberían estar en el grupo de comparación de un experimento sobre el choque de política) de quienes
**calificaban pero no cobraron** (comparación más limpia, más cercana a "intención de tratar"). Esto
respondería directamente la reserva #4 y refinaría el control de la reserva #2 (selección residual,
hoy solo por tercil de ingreso).

**Por qué "ENIGH ya observa la variable, en disco, con estimador validado contra INEGI" — verificado, no
solo repetido:**

```
$ grep -n "jubilacion" tests/r5_1_pension_bienestar.py
        sum_jubilacion += w * float(row["jubilacion"])
        ("jubilacion promedio ponderado", sum_jubilacion / sum_factor, 5_169),
```

`concentradohogar.jubilacion` (ingreso agregado por jubilación/pensión) ya se lee en el pipeline existente
y **ya está validado contra el publicado de INEGI** (Comunicado 420/23: calculado 5,168.6 vs. publicado
5,169, dif. relativa 0.009% — `forense/notas/2026-08-04-hitoD-r5-1-pension-bienestar.md §8`). No es una
variable nueva por descargar: está en `data/raw` (mismo corpus compartido que ya usa el pipeline de R5.1)
y el estimador que la lee ya pasó su prueba de exactitud. `poblacion.edad` (para el escalón 65/68) también
ya está confirmada disponible y usada en el mismo acto (§2 de la misma nota, aunque no se filtró por ella
en esa corrida).

---

## 3 · Qué haría falta para usarla (no se hace en este acto)

1. **Verificar las tres citas del DOF contra `dof.gob.mx` por red** — este acto no tiene red habilitada;
   es un acto propio, con los códigos de edición de arriba como punto de partida.
2. **Mapear el escalón de edad exacto por ola de ENIGH.** La regla no es estática: 2013-2018 (excluye por
   pensión contributiva, sin universalidad de edad), 2019 (65+ indígena / 68+ general), 2020 en adelante
   (ROP 2020, `5583304` — verificar si el escalón de edad sigue vigente o ya se igualó). Las olas de ENIGH
   usadas en la corrida archivada (2012-2022) cruzan las tres etapas; cada ola necesitaría su propia regla
   de elegibilidad, no una sola aplicada a las seis.
3. **Encontrar o construir, dentro de `concentradohogar`/`ingresos`, la variable de "pensión contributiva
   IMSS/ISSSTE por encima de $1,092"** — `jubilacion` es un agregado (ver arriba); falta confirmar si
   desagrega por tipo de esquema (contributivo vs. no contributivo) o si hace falta una `clave` específica
   de `ingresos` para aislarla, con el mismo estándar que Nota 16 ya aplicó para separar `P044`/`P104` de
   `bene_gob`. No se abrió microdato en este acto para responder esto — queda como pregunta para el acto
   que sí abra ENIGH.
4. **Decidir, en mesa, si el tratamiento-por-norma reemplaza o complementa la recepción declarada** — un
   cambio de definición del grupo de comparación no es una corrección menor de `R5.1`, es una prueba
   distinta. Con `R5.1` ya sellado (`A` con reserva, ADR-58(c)), esto **no se aplica retroactivamente**:
   correspondería a una **ficha nueva y autónoma**, pre-registrada antes de mirar el resultado, en un acto
   que abra ENIGH limpio (no contaminado por haber leído ya esta nota ni la de Nota 16 — mismo criterio de
   `ADR-46` que la propia Nota 16 ya se auto-aplicó).

---

## Lo que este acto no hizo

No escribió ni tocó `forense/hitoD-preregistro-v2_0.md`. No editó el cruce v2.0. No abrió microdato ni red.
No selló ningún ADR. No adjudicó ningún veredicto — el archivado de `R5.1` (`A`, con reserva, ADR-58(c))
queda exactamente como estaba. No escribió el pre-registro de la ficha nueva que esto habilitaría — eso es
un acto propio, y sesión queda limpia (no contaminada) para hacerlo contra cualquier fuente.
