# 2026-08-13 · ENCARGO nube · construcción de `data/INFRAESTRUCTURA-v1_0.md`

## ARRANQUE (verificado antes de leer el resto del encargo)

1. **REPO.** Clon existente en `/home/user/Modelado-Mexicano` (no se clonó uno nuevo). `git log -1 --format="%h %s"` → `2b13e88 Merge pull request #189 from Josanoforo/map-b/crosswalk-fuente-puerta`. `git status` → rama `claude/new-session-pe0yj6`, árbol limpio.
2. **SHA.** Coincide con la base declarada por el encargo (`2b13e88`). Sin drift, sin re-derivación necesaria.
3. **data/raw.** Ausente — esperado en clon fresco. Este acto no descarga nada ni toca microdato: no se creó ni se enlazó.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` — firma correcta de acto de nube (ADR-59(b)), sin sonda de red (este acto no toca microdato ni red).
5. **ESPEJO.** No se usó ningún espejo del proyecto — todas las cifras de este acto salen del clon de (1), con el comando a la vista en `data/INFRAESTRUCTURA-v1_0.md`.

PASO 1 (premisas) corrido y verde: `data/*.md` mostraba solo `UNIVERSO-MINIMO-FUENTE-v1_0.md` y `catalogo-fuentes-v2_0.md` (ningún índice previo) · 28 TSV/YAML/JSON en `data/` · 19 TSV en `data/curacion-universo/` · 19 entradas en `data/curacion-registro/` · 50 `.py` combinados en `tools/curador_registro/` + `tests/` · `python3 tests/check.py --baseline` → VERDE, **22 FAIL · 104 WARN**.

## Qué se hizo

Se derivaron, con comandos reales (`ls`, `head -1`, `grep -rl`, `git log`/`git show --stat`) y no de memoria, las tablas gobernantes de los ocho dominios que PASO 2 del encargo pedía: adquirir fuente/payload, registrar puerta, activo descubierto + decisión de adquisición, producir estimación, celda-D, veredicto Hito D, sellar ADR, y hallazgo/nota. El trabajo de verificación se repartió en siete investigaciones paralelas (una por dominio, con dominio 1 y 3 fusionados por su solape real en `data/curacion-universo/`), cada una reportando comandos y salida cruda, no conclusiones sin respaldo. El resultado se sintetizó en `data/INFRAESTRUCTURA-v1_0.md`.

## Lo que atrapó, verificado (no hipotético)

- **El caso testigo que el propio encargo citaba se sostiene igual hoy**: `grep -rn "capa2" tools/ tests/` → 0, y `capa2_manifiesto` de `relaciones.tsv` tiene **105 de 197 filas** en `NO_REFERENCIADO` (recontado en este acto con `awk`, mismo resultado que el encargo citaba).
- **La instancia materializada de WVS también se sostiene**: `git show --stat 84f8e30` confirma que el registro de los 11 payloads de WVS tocó solo `manifiesto.yaml`/`manifiesto-staging.yaml`/`universo-puertas-2026-08-12.tsv` — cero tablas de `curacion-universo/`. Las 4 filas `ADESC-*` que sí existen son todas de `0e07179` (ENASIC/ENCUCI), ninguna de WVS.
- **Tres huecos nuevos, no citados por el encargo original**, ahora en `forense/hallazgos.md`: un run huérfano en `ejecucion-semantica/runs/` sin detección automática; `decisiones-adquisicion.tsv` desactualizado frente a las 2 filas `ADESC-*` más recientes; y una colisión de numeración entre el A.7 propuesto (Parte 1 del encargo) y el A.7 ya vigente en `instrucciones-proyecto-v2_6.md`.

## Cierre — siete líneas

1. Base: `origin/main = 2b13e88`, confirmada con `git log -1`.
2. Suite: `python3 tests/check.py --baseline` → VERDE, 22 FAIL · 104 WARN, sin cambios frente a `tests/baseline.json`.
3. Perímetro respetado: solo se tocó `data/INFRAESTRUCTURA-v1_0.md` (nuevo), esta nota, `forense/hallazgos.md` (append) y `forense/encargos/` (copia literal) — ninguna tabla, script ni `canon/`.
4. Ocho dominios cubiertos, cada uno con tablas/vía/contrato/lectores/trampa derivados por comando, no de memoria.
5. Dos colas de trabajo declaradas explícitamente en el índice: tablas `SIN VÍA` y tablas que nadie lee — ninguna de las dos se corrigió aquí.
6. Contadores de medición movidos: **0** — este acto no midió nada sobre México.
7. PR `infra/indice-v1`, **NO FUSIONAR sin mesa**.
