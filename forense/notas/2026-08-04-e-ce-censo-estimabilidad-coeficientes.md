# Nota propia — Encargo E-CE, censo de estimabilidad de los 15 coeficientes de generador

*4 de agosto de 2026. Acto de escritorio, entorno nube (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, sin sonda de red — el propio encargo exime el punto 4 del Bloque D: "no toca microdato ni red"). Base: `origin/main` = `8cdabcb` (merge PR #106), verificado con `git fetch origin main` contra el SHA declarado por el encargo — coinciden exactamente, cero deriva que reportar antes de editar.*

**Qué es este documento y qué no es.** Nota de cierre de sesión sobre `forense/censo-estimabilidad-coeficientes-v1_0.md` (nuevo). No abre ningún microdato, no corre ninguna estimación, no adjudica ningún veredicto de Hito D, no cambia ningún valor `ASIGNADO`. Perímetro del encargo, verificado al cerrar: `forense/censo-estimabilidad-coeficientes-v1_0.md` (nuevo) · `milpa/procedencia.yaml` (solo campo `ruta:` nuevo, sección paralela, `detalle` sin tocar) · esta nota · `forense/hallazgos.md` (append). No se escribió nada fuera de esa lista.

---

## 1 · Qué pedía el encargo, y qué se entregó

Para cada uno de los 15 coeficientes de generador (leídos de `milpa/procedencia.yaml:612-639`): θ y clase citada textual; desenlace co-observado candidato, cruzando `data/manifiesto.yaml` + `data/diseno-muestral.yaml` + `data/catalogo-fuentes-v2_0.md` + `forense/cruce-catalogo-fichas-v2_0.md`; cruce obligatorio contra `forense/descartes-forenses-registro.md` y ADR-49 D1; marca (b) si aplica; palanca ADR-57(c) con estado citado (`gobernanza-v1_15.md:623`); ruta (`RUTA-C`/`RUTA-I`/`RUTA-A`/`SIN-RUTA`, taxonomía nueva de este acto, declarada como tal) + prioridad. Las 15 filas están en `forense/censo-estimabilidad-coeficientes-v1_0.md` §5, con fuente citable en cada una.

## 2 · El hallazgo que no estaba en el encargo

El encargo asumía implícitamente, por el estado previo de `procedencia.yaml` (línea 642: *"Ningún coeficiente de generador tiene ruta hoy"*), un reparto probablemente cargado hacia `SIN-RUTA`. No es así: **3 de 15 ya tienen una asociación corrida (Encargo W) y 1 de 15 tiene una llave de identificación sellada y parcialmente ejercida (`CAL-G3`, ENNViH/MxFLS, `gobernanza:623`)** — ambos hechos ya vivían en el corpus, dispersos entre `procedencia.yaml`, `gobernanza` y `hitoD-preregistro-v2_0.md`, y esta es la primera vez que se cuentan juntos contra los 15. La frase de la línea 642 queda desactualizada por Encargo W (04/ago) y por este censo, no por este acto en particular — se deja sin tocar (append-only, no se edita retroactivamente) y se marca en `rutas_estimabilidad_coeficiente` con la fecha y el archivo que la sustituye.

## 3 · Verificación de premisas antes de ejecutar

**RUTA-C/RUTA-I/RUTA-A/SIN-RUTA no existían en el repo.** Búsqueda exhaustiva (`grep -rni` sobre `*.md`/`*.yaml`, variantes con y sin guion, mayúsculas/minúsculas) antes de usarlas: cero resultados. Se declaran como definición nueva de este censo (§1 del censo), no como canon heredado — Regla de oro de `instrucciones-proyecto-v2_4.md`: no hay que fingir que se leyó una taxonomía que no estaba escrita.

**`descartes-forenses-registro.md` cruzado completo:** cubre descartes de casos de los cinco forenses verticales (V1-V5, dominio financiero/electoral) — cero traslape de dominio con los 15 coeficientes o sus instrumentos candidatos. **ADR-49 D1 cruzado:** la ruta ENOE → `G3.horizonte_temporal` está descartada — la fila `G3·horizonte_temporal` del censo reporta una ruta distinta (ENNViH/MxFLS vía `CAL-G3`), y lo declara explícitamente para que quede visible que la descartada fue vista, no pasada por alto. Ninguna de las 15 filas re-propone un descarte de ninguna de las dos fuentes.

## 4 · Cifras derivadas, no tecleadas — y el error que la propia disciplina atrapó

Primer intento de comando de verificación del reparto (`grep -oE 'RUTA-[CIA]|SIN-RUTA' censo... | sort | uniq -c`) dio **8/6/5/15**, no 3/1/2/9 — inflado porque cuenta las menciones de la definición (§1), del propio §6 y del bloque de verificación (§7) del censo, no solo las 15 filas de la tabla. Se detectó al correr el comando de verdad en vez de escribir el resultado esperado, y se corrigió con una receta que ancla el patrón al inicio de fila de la tabla (`^\| [0-9]+ \|`), probada por separado contra el conteo de filas (`grep -cE` da 15). Queda en el censo §7 como evidencia de que la receta se verificó, no solo se corrió — mismo criterio que v2.3 exige (`forense/notas/2026-08-04-a3-f1-cruce-catalogo-manifiesto.md` ya documentó el mismo tipo de defecto sobre otro archivo).

## 5 · Qué queda declarado y no resuelto, para la tanda

- **`G4·exposicion_violencia` y `G4·confianza_institucional[justicia]`** (`RUTA-C`): el candidato `BP1_23`/`comunicacion.inseguridad.ver_oir_callar` tiene una limitación estructural ya declarada en `procedencia.yaml` (`limite_c2`, líneas 396-413) que exige adjudicación de mesa antes de correr nada — no se adjudica en este acto, es de escritorio.
- **ENDIREH, 20 secciones completas**, para cerrar si trae o no `civico.protesta.agravio_urbano`/`civico.autodefensa.agravio_rural` — abrir el instrumento completo es trabajo de una sesión con microdato, fuera de este modo.
- **`CAL-G3` → identificación**: la llave está sellada y la Fase C descriptiva ya corrió; falta el diseño intra-persona que promovería la estimación de descriptiva a identificada — es el candidato de mayor prioridad del censo (`RUTA-I`, único), y tampoco se ejecuta aquí.

Ningún ZIP de microdato se abrió en este acto. Ninguno de los tres puntos de arriba se resuelve aquí — se declaran, como el encargo pide, y se dejan a la tanda.

## 6 · Cierre

`tests/check.py` corrido después de escribir `milpa/procedencia.yaml`: **18 FAIL · 95 WARN**, idéntico al baseline citado en actos previos (`forense/hallazgos.md:117-118`) — sin regresión introducida por el campo `ruta:` nuevo. `python3 -c "import yaml; ..."` confirma que `milpa/procedencia.yaml` sigue siendo YAML válido y que `rutas_estimabilidad_coeficiente.detalle` tiene exactamente 15 entradas con el mismo reparto que el censo. **Contadores movidos: 0 — censo.** Ningún valor `ASIGNADO`, ninguna clase de procedencia, ningún veredicto de Hito D cambia por este acto.
