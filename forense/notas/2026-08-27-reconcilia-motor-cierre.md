# Nota de cierre · ACTO MAESTRA31-E10 · RECONCILIA-MOTOR

Fecha: 2026-08-27. Clon `/home/user/Modelado-Mexicano`, rama `claude/reconcilia-motor-contador-field-uktyd7`. Entrega principal: `forense/estado-motor-v1_0.md` (tabla de 15 pares, cuatro columnas, mapeo A×B×C). Esta nota trae los conteos A.13, la fila `FP-177`, y el resto del cierre que el encargo pide (`hallazgos.md`, ADR, recifrado, rótulo, T25).

---

## A.13 — conteos y comandos de cada afirmación

| # | Afirmación | Tipo | Comando | Resultado |
|---|---|---|---|---|
| 1 | `coeficientes_generador_medidos` tiene 6 entradas, 5 con `beta_hat` y 1 GATE | positiva | `python3 -c "import yaml; d=yaml.safe_load(open('milpa/procedencia.yaml')); A=d['coeficientes_generador_medidos']; print(len(A)); print([k for k,v in A.items() if 'beta_hat' in v]); print([k for k,v in A.items() if v.get('clase','').startswith('GATE')])"` | 6 claves; 5 con `beta_hat` (`G1_radio_confianza`, `G1_confianza_institucional`, `G3_familismo_apoyo`, `G4_exposicion_violencia`, `G4_confianza_institucional_justicia`); 1 GATE (`G3_horizonte_temporal`) |
| 2 | `rutas_estimabilidad_coeficiente.detalle` tiene 15 filas: 5 `RUTA-A` · 1 `RUTA-I` · 0 `RUTA-C` · 9 `SIN-RUTA` | positiva | `python3 -c "import yaml,collections; d=yaml.safe_load(open('milpa/procedencia.yaml')); B=d['rutas_estimabilidad_coeficiente']['detalle']; print(len(B)); print(collections.Counter(r['ruta'] for r in B))"` | 15 filas; `RUTA-A: 5, RUTA-I: 1, SIN-RUTA: 9` (`RUTA-C: 0`, no aparece por ausencia) |
| 3 | `escala_derivada` (campo completo, no primer token) de las 15 filas: 7 `ELEGIDA-CIEGA` · 8 `SUBDETERMINADA-PERSISTENTE` | positiva | script Python que busca la subcadena `ELEGIDA-CIEGA`/`SUBDETERMINADA-PERSISTENTE` en el string completo de cada fila (`assert` de que aparece exactamente una de las dos, nunca ambas ni ninguna) | 7 `ELEGIDA-CIEGA`, 8 `SUBDETERMINADA-PERSISTENTE`, suma 15 — coincide con lo que dirección citó, pero derivado aquí por comando propio, no heredado |
| 4 | `asignados_coeficiente.detalle` (6 filas-generador) contiene exactamente los mismos 15 pares `gen.coef` que B, sin diferencia | positiva | `python3` — construye `set()` de pares desde `B` y desde los `coefs.keys()` de cada fila de `C`, imprime la diferencia simétrica | `B - C = set()`, `C - B = set()` — 15 pares en ambos lados, idénticos |
| 5 | `canon/modelo-decision-v4_0.md` nombra el coeficiente de G4 como `confianza_institucional[justicia]`, no como un genérico sin calificador | positiva | `grep -n "confianza_institucional\[financiera\]\|^| G4 " canon/modelo-decision-v4_0.md` | línea 454: `G1a | confianza_institucional[financiera] −0.60 ...`; línea 458: `G4 | exposicion_violencia 0.70 · confianza_institucional[justicia] −0.40 ...` — calificador presente en ambos, mismo patrón |
| 6 | Ningún generador declara escala/unidad numérica para su salida (columna 3) | negativa | lectura íntegra de `canon/modelo-decision-v4_0.md` §2.1-2.2 (líneas 422-460, 39 líneas) + `forense/escalas-eleccion-ciega-v1_0.md` líneas 17 y 30 (criterio 2 aplicado a las 15 filas) + `forense/firmas-pendientes.tsv` fila `FP-149` (columna `qué_se_firma`, vía `csv.DictReader`) | tres fuentes independientes, ninguna de este acto, coinciden: cero declaraciones de escala del generador — universo examinado: 39 líneas de canon + 52 líneas de `escalas-eleccion-ciega` + 1 fila de 172 de `firmas-pendientes.tsv` |
| 7 | `forense/cobertura-motor.md` y `forense/censo-estimabilidad-coeficientes-v1_2.md` nunca citan `coeficientes_generador_medidos` | negativa | `grep -c "coeficientes_generador_medidos" forense/cobertura-motor.md forense/censo-estimabilidad-coeficientes-v1_2.md` | `0` en ambos (110 líneas y 65 líneas respectivamente, archivos completos) |
| 8 | El reparto real de las 15 filas de B, re-derivado, es `RUTA-A=5 · RUTA-I=1 · RUTA-C=0 · SIN-RUTA=9` | positiva | mismo comando de la fila 2 de esta tabla, aplicado sobre el archivo antes de editar `reparto:` | coincide exacto con lo que dirección citó en la VERIFICACIÓN DE EXISTENCIA — sin delta que reportar (paso 5 del encargo) |
| 9 | La línea `reparto:` (`procedencia.yaml:1127`) decía `RUTA-A=3 · RUTA-C=2` antes de este acto | positiva | `git show 17c12bd^:milpa/procedencia.yaml \| sed -n '1127p'` | confirmado verbatim, stale desde `ACTO MAESTRA31-E9` (`PR #390`) |
| 10 | Ningún acto entre el 4/ago y hoy cruzó A contra B contra C en un solo artefacto | negativa | `grep -rl "coeficientes_generador_medidos" forense/*.md forense/notas/*.md canon/*.md 2>/dev/null` | única coincidencia antes de este acto: el propio `milpa/procedencia.yaml` (autorreferencia) y menciones de acto puntuales (`estima-rutac-*`, `gobernanza-v1_15.md` ADR-218) que citan una fila de A, no las tres secciones cruzadas — universo: todo `.md` de `forense/` y `canon/`, sin `data/raw` |

Todo comando corrido contra el clon real de este worktree (`/home/user/Modelado-Mexicano`), nunca contra el espejo.

---

## `FP-177`

Ver fila nueva en `forense/firmas-pendientes.tsv`. Pone ante mesa la tabla completa de `forense/estado-motor-v1_0.md`: 5 de 15 pares con β̂ medido y escala de θ declarada (los mismos 5 `RUTA-A`), 0 de 15 con escala del generador declarada, intersección de las tres condiciones = 0. Cita `FP-176` (si escribir un β̂ ya medido en la escala ya declarada requiere adjudicación de mesa aparte) **sin re-abrirla ni contestarla** — `FP-177` es la vista de conjunto sobre las 15 filas; `FP-176` sigue siendo la pregunta puntual sobre las 2 filas de G4 que la originaron. Mesa puede resolver ambas juntas o por separado; este acto no decide cuál.

---

## Qué NO hizo este acto

No estimó ningún coeficiente ni corrió ningún modelo. No adjudicó `FP-176`. No escribió ningún coeficiente en `milpa/`. No tocó ningún campo de `milpa/procedencia.yaml` salvo la línea `1127` (`reparto:`). No tocó `canon/modelo-decision-v4_0.md`, `forense/perimetro-alcanzable-v1_0.md`, `forense/cobertura-motor.md`, `forense/censo-estimabilidad-coeficientes-v1_*.md` ni `forense/escalas-eleccion-ciega-v1_0.md` (solo lectura de los cinco). No editó `FP-149`, `FP-152` ni `FP-176` (se citan, no se tocan). No re-corrió ningún censo, aunque `forense/estado-motor-v1_0.md` §3 declare que `cobertura-motor.md` y `censo-estimabilidad-coeficientes-v1_2.md` están vencidos en alcance. No forzó el mapeo de `G4_confianza_institucional_justicia` — lo resolvió con evidencia textual de `canon/modelo-decision-v4_0.md`, declarada en `forense/estado-motor-v1_0.md` §0.2. No tocó `data/**`, `tools/**`, `forense/prereg-duelo-v2/**` ni `forense/hitoD-preregistro-v2_0.md`.

---

## Las tres cosas stale que `ACTO MAESTRA31-E9` documentó y no pudo tocar

Ver también `forense/hallazgos.md` (entrada de este acto). Estado de cada una después de este acto:

1. **`reparto:` (`procedencia.yaml:1127`)** — **resuelta por este acto** (paso 5, arriba). Ya no está stale.
2. **La cita interna `procedencia.yaml:396-413 (limite_c2)`**, repetida 3 veces (líneas 996, 1021, 1056) — **sigue stale**. Fuera del perímetro de este acto (autorización acotada a `reparto:` únicamente); no se corrige aquí.
3. **`FP-152`**, columna final con *"Paso 2 sigue sin ejecutar"* — **sigue stale** (Paso 2 sí se ejecutó el 25/ago, ver `forense/escalas-eleccion-ciega-v1_0.md`). Fuera del perímetro de este acto (`FP-149`/`FP-152` explícitamente no se tocan); no se corrige aquí.
