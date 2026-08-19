# ENCARGO · ACTO CORTE-EDAD-CONVENCION — propagar el corte de «edad joven» a los nueve sitios

SHA de redacción: derivar al lanzar (escrito el 18/ago/2026 por `ACTO MESA-19AGO`). Entorno asignado: **NUBE** (repo-only, no toca microdato). Estado: ~~**VIVO**, sin gate~~ → **CONSUMIDO** · SHA de redacción re-derivado al lanzar: `35c9c9f` (`origin/main`, `PR #278` ya fusionado) · Ejecutado contra `35c9c9f` · Cierre: `ADR-114` · Detalle comando por comando: `forense/notas/2026-08-19-corte-edad-convencion-cierre.md`. Origen: firma de mesa D-2 de `MESA-19AGO` — vía **(c) ambas** —, `ADR-110(b)`, fila `FP-53`.

## 1 · Lo que la mesa firmó (verbatim)

D-2: **`(c) Ambas`** — *"Convención declarada ahora para desbloquear los 9 sitios, más derivación empírica con dato mexicano propio como acto en cola que puede corregirla."*

Corte oficial adoptado: **15-29 años**, convención de INEGI/ENOE para «población joven» en estadística laboral — el registro en que se mide `R2.4` (rotación) y en que el perfil 5 se observa. Alterno declarable: **12-29 años**, Ley del Instituto Mexicano de la Juventud art. 2.

⚠️ **Aviso de procedencia, escrito en el prompt de mesa y que este acto debe honrar:** ninguna de las dos fuentes está hoy citada en el árbol. **La procedencia se cita al propagar, con URL y fecha de consulta — no se hereda de este encargo ni del prompt.** Si la cita oficial no se puede fijar, el sitio se deja `PENDIENTE` y se reporta; no se propaga un corte sin fuente.

## 2 · Los nueve sitios (derivados por comando, no tecleados)

Receta probada (`CONSOLIDA-2`, control positivo 9/9; control negativo contra el falso positivo conocido "cortes iniciales" de `FP-02`: cero coincidencias) — **dos redacciones distintas**:

```
grep -niE "corte PENDIENTE|Corte de .?edad.? PENDIENTE" canon/modelo-decision-v4_0.md
```

Contra `f3d3f95`: `:189` (descriptor del perfil 5) · `:215` (H-02) · `:219` (H-06) · `:220` (H-07) · `:355` (R1.4) · `:357` (R2.4) · `:361` (R5.4, la redacción larga) · `:457` (regla operativa R2.4) · `:482` (regla operativa R5.4). **Re-derívalos al ejecutar por contenido, no por número de línea.**

## 3 · Qué hace este acto

1. Sustituye `corte PENDIENTE` / `Corte de \`edad\` PENDIENTE` por el corte firmado en los nueve sitios, **cada uno con su procedencia citada**.
2. Escribe, en el mismo `modelo`, la marca de que el corte es **convención declarada, no derivación empírica**, y que `CORTE-EDAD-EMPIRICO` puede corregirlo — la vía (c) obliga a dejar esa puerta abierta por escrito.
3. Propaga a lo que el corte desbloquea: definición completa del perfil 5; `H-02`/`H-06`/`H-07` salen de `NO DETERMINABLE`/forma `PENDIENTE`; disparo de `R2.4` (:457) y `R5.4` (:482); indirectamente `R1.4` (hitoD-preregistro Nota 30, rama estatus de `conf.05`).
4. Re-cuenta por comando lo que quede `PENDIENTE` y lo reporta; el número honesto es el derivado, no el esperado.

## 4 · Lo que NO hace

No deriva el corte de dato propio (eso es `CORTE-EDAD-EMPIRICO`) · no toca `milpa/*.yaml` · no re-adjudica ninguna hipótesis: cambia su estatus de determinabilidad, no su veredicto.
