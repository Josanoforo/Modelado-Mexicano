# Nota de cierre · ACTO GEN2-TRAMITE-FIRMAS-6

ADR raíz: `ADR-260922-GEN2-TRAMITE-FIRMAS-6-7c2c-01`. Encargo: `forense/encargos/2026-09-22-GEN2-TRAMITE-FIRMAS-6.md`.

## P3 · tabla — firma · fila · lo que desbloquea · quién lo ejecuta

| Firma (id FP) | Fila en `decisiones.tsv` | Lo que desbloquea | Quién lo ejecuta |
|---|---|---|---|
| `…e8fa-01` MOTOR-THETA-CONGELADA-1 | `FP-260921-MOTOR-THETA-CONGELADA-1-e8fa-01` | La adopción del acto MOTOR-THETA-CONGELADA-1 ya no espera a `test_c_roles_sellados…`; NC-`…e8fa-02` sigue ABIERTA (test en rojo, sucesor SIN-ASIGNAR). | nadie (declarativo); el FAIL lo resuelve un acto sucesor sin asignar con permiso de mesa sobre `motor.py` |
| `…852f-01` ENCIG-SERIE-Y-TENDENCIA-1 | `FP-260921-GEN2-ENCIG-SERIE-Y-TENDENCIA-1-852f-01` | Nada hoy sobre el piso adjudicado. Determina que TENDENCIA-SERIE **no** entra como retador en el duelo ENVIPE 2026 actual — su COMMIT-1 ya está CONGELADO (NC-`…8796-01`, cerrada 21/sep) — y queda para el **siguiente** duelo. | acto sucesor del siguiente duelo ENVIPE, si mesa lo pide |
| `…a98a-02` DIN-LOTE-ENIF2024-A | `FP-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-02` | Fija Opción A: ENIF 2018 no entra como segunda ola histórica mientras el lote 2024 no cierre. | nadie hoy; re-examinar si/cuando el lote 2024 cierre del todo |
| `…ed7d-01` ARBITRO-MARGINALES-1 | `FP-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-01` | Ratifica `cuenta_gen2 = SI` de `CALC-ARBITRO-PERSISTENCIA-ERROR-0001` (fila objeto=CALC ya existía desde el 21/sep como propuesta; ésta es la firma propia de la FP, A.12). | nadie; sólo registro |
| `…6c10-02` (Q1, C2 5 pares formalidad) | `FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-1-6c10-02` | Mesa elige opción (B): sella C2-restringido al universo trabaja antes del COMMIT-2. NC-`…6c10-01` enmendada, sigue ABIERTA — el sucesor (`acto/gen2-din-lote-c2-restringido-1`) está EN VUELO (0-bis en origin) pero no ha corrido su COMMIT. | acto/gen2-din-lote-c2-restringido-1 (en vuelo) |
| `…6c10-03` (Q2, régimen de universo) | `FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-1-6c10-03` | Fija régimen ARBITRO-2024 para comparaciones contra el árbitro; PILOTO-1 sólo dentro de sus celdas-D ya selladas. | nadie hoy; regla queda fijada |
| `…6c10-04` (Q3, agregador de L) | `FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-1-6c10-04` | Cierra NC-`…6c10-03` por superación: #973 fusionó (verificado: merge `8adc773`, `tools/agrega_l_v1_0.py` presente), el agregador queda fijado. | nadie; consumido |
| `…8e53-01` DIN-LOTE-ENIF2024-COMMIT-2-3 | `FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3-8e53-01` | Cierra NC-`…8e53-01`: NO se corre L1/L2 sobre los 14 cruces (presupuesto), decisión definitiva. | nadie; consumido |
| `…7866-01` DIN-CREDITO-PREDICCION-2024-COMMIT-1 | `FP-260921-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1-7866-01` | Ratifica K6-P-TENEDORES (unidad P) para el lote de predicción de crédito 2024. | nadie; consumido |
| `…ff56-01` DIN-CREDITO-HISTORIA-1 | `FP-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-01` | Mesa elige opción (a): sucesor con el medidor genérico sobre ENIF 2021, recorte 18-70, CALC nuevo. NC-`…ff56-03` enmendada, sigue ABIERTA (sucesor SIN-ASIGNAR, no ha corrido). | acto sucesor sin asignar |

## Corrección de premisa declarada (A.12/§0, logística — no PARO)

El §2 del encargo citó el verbatim de mesa bajo los rótulos «Q3» para `…6c10-03` y «Q2»/«Q1» para `…6c10-04`/`…6c10-02`. Al leer `forense/firmas-pendientes.tsv` con acceso directo (§4 del Bloque D), el contenido real de cada fila desambigua: `…6c10-02` es Q1 (C2 de los 5 pares con formalidad), `…6c10-03` es Q2 (régimen de universo del lote) y `…6c10-04` es Q3 (agregador de L). El encargo intercambió las etiquetas Q2/Q3 entre `…6c10-03` y `…6c10-04` sin cambiar el contenido de la firma en sí. Se asentó cada verbatim de mesa contra el id cuyo contenido de FP realmente responde (por Q-número, no por el rótulo mal citado), y se declara aquí explícitamente — objetivo del encargo sigue alcanzable, es logística de citación, no una premisa sobre qué se mide ni sobre el contenido de una firma de mesa.

## Latitud ejercida (§6 del encargo)

Pregunta a mesa del encargo: «una firma cuyo objeto ya cambió (p. ej. el duelo ENVIPE 2026 congelado antes de (b)) — ¿asentar con la condición escrita (recomendado) o dejar ABIERTA?» Se verificó: el COMMIT-1 del duelo ENVIPE 2026 SÍ está CONGELADO (NC-`…8796-01`, cerrada 21/sep, D-22 ampliada demostrada en PR #968/#971-adyacente). Se tomó la opción recomendada por el propio encargo: se asienta `…852f-01` FIRMADA con la condición escrita tal cual la firma la declara — «si está congelada, queda para el siguiente duelo» — sin necesidad de nueva pregunta a mesa, porque la propia firma ya cubre el caso condicional.

## Ramas E1–E4 / FP374-RESELLO-1 en vuelo al lanzar este acto (§4 del Bloque D)

Verificado por `git ls-remote --heads origin` y `git log origin/main..origin/<rama>` el 22/sep: `acto/gen2-din-lote-c2-restringido-1` (sólo 0-bis, sin COMMIT), `claude/gen2-fp374-resello-1` (con `## CONSUMIDO`, PR #998, **no fusionada** en `origin/main`), `claude/gen2-marco-m-consumidor-1` (PR #999, no fusionada), `claude/gen2-pendientes-caja-1`, `claude/gen2-pendientes-reconcilia-1`. Ninguna de las cuatro filas «consumidas por E1–E4» que el encargo listó como ya resueltas (`…8e53-02`, `…ff56-02`, `…ed7d-02`, `…958c-01`) está de hecho `FIRMADA` en `origin/main` a la fecha de este acto (todas siguen `ABIERTA`); la única SUPUESTA-consumida que sí lo está es `…95ec-01`-adyacente (`FP-260921-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1-7866-02`, `FIRMADA` vía `ADR-260922-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3-95ec-01`). Este acto **no** toca esas cuatro filas: no son suyas (§9, ajeno) y su consumo real no se verifica hasta que las ramas fusionen.

## Hallazgo sobre el criterio de «hecho» (duplicados de `objeto` en `decisiones.tsv`)

`cut -f1 data/corrida0/decisiones.tsv | sort | uniq -d` no sale vacío: hay 14 objetos `CALC-*` duplicados **preexistentes**, ninguno de los cuales es un id FP ni fue tocado por este acto. Los 10 objetos que este acto añadió (ids FP de §2) son todos únicos (`grep -c` = 1 cada uno). El criterio de «hecho» del encargo, leído literalmente sobre el archivo completo, no se satisface por una condición preexistente fuera de perímetro; leído sobre las filas que este acto controla, sí.
