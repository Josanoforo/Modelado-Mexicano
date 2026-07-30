<!-- PROCEDENCIA — leer antes que el cuerpo.

Este archivo NO lo produjo la sesión que lo recogió al repo (CAL-G3 / Fase B,
rama sesion/calg3, 30/jul/2026). Lo produjo la SESIÓN DE ENSANUT, que trabajó
el mismo día sobre el portal del INSP; su identificador de origen es
`originSessionId: 779162ce-49c1-4db6-85bb-d958050c3e75`, conservado en el
frontmatter de abajo sin alterar.

Lo que hizo la sesión que lo recoge: copiarlo literalmente desde la memoria de
proyecto (`~/.claude/projects/-home-pc0-Modelado-Mexicano/memory/fetch-vs-html-crudo.md`) a
`forense/notas/`, para que deje de vivir sólo en memoria de agente y quede en
el repo, versionado y citable. **Ni una palabra del cuerpo se editó.** La
sesión que recoge NO verificó de forma independiente los hechos que se afirman
aquí -- no tocó el portal del INSP -- y por tanto no los avala: los transcribe
con su autoría declarada. Quien quiera usarlos como evidencia los verifica
contra la fuente, o cita esta nota como lo que es: el reporte de otra sesión.
-->

---
name: fetch-vs-html-crudo
description: Un WebFetch que resume vía modelo intermedio no es fuente verificable para afirmar la estructura literal de una página — usar HTML crudo (curl) cuando la afirmación depende de markup exacto.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 779162ce-49c1-4db6-85bb-d958050c3e75
  modified: 2026-07-30T17:19:15.197Z
---

Nunca usar el resumen de WebFetch (pasa el HTML por un modelo intermedio antes de devolver texto) como
evidencia para afirmar la estructura literal de una página — hrefs, forms, atributos exactos. Verificar
siempre con HTML crudo (curl u otra descarga directa) antes de aseverar cómo está construida una página.

**Why:** en la inspección de la tabla de descargas de ENSANUT Continua 2024, componente SALUD
(2026-07-30), WebFetch reportó `<a href="../../descargas/SALUD/Catalogo.csv">` como si existiera un
enlace estático a archivo. El HTML crudo (curl, TLS activo) no contiene ese `href` en absoluto: la región
de la tabla tiene 1 sola `<a>` ajena (de navegación, no de descarga) y 168 `<button type='submit'>`
dentro de un único formulario POST autodirigido. El resumen fue una alucinación plausible, no una
lectura real del markup. Es la misma clase de defecto que el caso "pelón": afirmar el contenido de algo
sin haberlo leído directamente. Ver [[ensanut2024-salud-post-autodirigido]] para el caso concreto donde
se detectó.

**How to apply:** cuando la tarea depende de saber si algo es un enlace directo vs. un formulario/JS, o
de cualquier detalle exacto de markup (atributos, valores, presencia/ausencia de un elemento), no te
conformes con el resumen de WebFetch — baja el HTML con curl/requests y grep/lee el markup literal tú
mismo. Aplica en general a cualquier fuente externa cuya estructura vaya a determinar una decisión
operativa (p. ej., "¿esto se puede automatizar con requests o requiere navegador?").
