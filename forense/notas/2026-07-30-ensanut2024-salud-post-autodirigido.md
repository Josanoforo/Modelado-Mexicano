<!-- PROCEDENCIA — leer antes que el cuerpo.

Este archivo NO lo produjo la sesión que lo recogió al repo (CAL-G3 / Fase B,
rama sesion/calg3, 30/jul/2026). Lo produjo la SESIÓN DE ENSANUT, que trabajó
el mismo día sobre el portal del INSP; su identificador de origen es
`originSessionId: 779162ce-49c1-4db6-85bb-d958050c3e75`, conservado en el
frontmatter de abajo sin alterar.

Lo que hizo la sesión que lo recoge: copiarlo literalmente desde la memoria de
proyecto (`~/.claude/projects/-home-pc0-Modelado-Mexicano/memory/ensanut2024-salud-post-autodirigido.md`) a
`forense/notas/`, para que deje de vivir sólo en memoria de agente y quede en
el repo, versionado y citable. **Ni una palabra del cuerpo se editó.** La
sesión que recoge NO verificó de forma independiente los hechos que se afirman
aquí -- no tocó el portal del INSP -- y por tanto no los avala: los transcribe
con su autoría declarada. Quien quiera usarlos como evidencia los verifica
contra la fuente, o cita esta nota como lo que es: el reporte de otra sesión.
-->

---
name: ensanut2024-salud-post-autodirigido
description: "ENSANUT Continua 2024, componente SALUD — confirmado POST autodirigido (no hay enlaces estáticos); inventario de las 10 filas de descarga."
metadata: 
  node_type: memory
  type: project
  originSessionId: 779162ce-49c1-4db6-85bb-d958050c3e75
  modified: 2026-07-30T17:19:06.369Z
---

El componente SALUD de ENSANUT Continua 2024 (`https://ensanut.insp.mx/encuestas/ensanutcontinua2024/descargas.php`)
NO expone enlaces estáticos: las 168 celdas de descarga de la tabla (SALUD + NUTRICIÓN) son botones
`<button type='submit' name='ArchId<base64-ruta>'>` dentro de UN solo
`<form action='/encuestas/ensanutcontinua2024/descargas.php' method='POST'>` que envuelve toda la página,
sin campos ocultos ni CSRF visible. Confirmado leyendo HTML crudo (curl, TLS activo) el 2026-07-30: en la
región de la tabla hay 1 sola `<a>` ajena (menú de navegación) y 168 `<button>`.

**Why:** re-verifica la clasificación ya registrada en `data/manifiesto.yaml`/bitácora como "requiere
navegador" (id `hitoD_fase1_ediciones_requieren_navegador`, cubre R4.2/ENSANUT) — esa clasificación era
correcta. Una inspección manual anterior notó "iconos por celda que bajan archivo" y se interpretó como
enlace directo; era el icono decorativo dentro del botón submit, no un `href`. Ver
[[fetch-vs-html-crudo]] para el defecto de método relacionado (WebFetch alucinó un `href` que no existe
en el HTML real).

**How to apply:** no replicar el POST contra este formulario sin instrucción explícita de una sesión que
decida deliberadamente hacer ingeniería del formulario contra el servidor del INSP — es decisión de mesa
del autor, no de sesión. Ninguna sesión debe asumir que puede automatizar esta descarga sin ese visto
bueno explícito.

Inventario de las 10 filas del componente SALUD (nombres de archivo tomados del atributo `title` de cada
botón — metadata de página tal como la sirve el sitio, no contenido de archivo leído):

| Fila | CSV | CATÁLOGO | CUESTIONARIOS |
|---|---|---|---|
| Cuestionario de hogar | — | — | `1 VFINAL Cuestionario Hogar ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` |
| ↳ Información sobre el hogar | `hogar_ensanut2024_w_ICB.csv.csv.zip` | `hogar_ensanut2024_w_ICB.Catálogo.xlsx` | — |
| ↳ Información sobre los residentes | `integrantes_ensanut2024_w_ICB.csv.csv.zip` | `integrantes_ensanut2024_w_ICB.Catálogo.xlsx` | — |
| ↳ Indice de bienestar | — | — | `Indice de Bienestar.Cuestionarios.docx` |
| ↳↳ Información sobre el hogar | `NSE_Hogar_ENSANUT_2024.csv.csv.zip` | `NSE_Hogar_ENSANUT_2024.Catálogo.xlsx` | — |
| ↳↳ Información sobre los residentes | `NSE_Integrantes_ENSANUT_2024.csv.csv.zip` | `NSE_Integrantes_ENSANUT_2024.Catálogo.xlsx` | — |
| Cuestionario de salud de niños (0-9 años) | `menores_ensanut2024_w.csv.csv.zip` | `menores_ensanut2024_w.Catálogo.xlsx` | `2 VFINAL Cuestionario niños 0 a 9 ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` |
| Cuestionario de salud de adolescentes (10-19 años) | `adolescentes_ensanut2024_w.csv.csv.zip` | — (sin celda Catálogo en esta fila) | `3 VFINAL Cuestionario adolescentes ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` |
| Cuestionario de salud de adultos (20 años o más) | `adultos_ensanut2024_w.Catálogo.csv.csv.zip` ⚠️ | `adultos_ensanut2024_w.Catálogo.xlsx` | `4 VFINAL Cuestionario adultos ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` |
| Cuestionario de utilizadores de servicios de salud | `utilizadores_ensanut2024_w.csv.csv.zip` | `utilizadores_ensanut2024_w.Catálogo.xlsx` | `5 VFINAL Cuestionario utilizadores ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` |

⚠️ Anomalía "adultos": el propio sitio nombra el archivo de la columna CSV con `.Catálogo.` incrustado
en el nombre (`adultos_ensanut2024_w.Catálogo.csv.csv.zip`) — es así en el sitio, no un error de lectura
de esta sesión.
