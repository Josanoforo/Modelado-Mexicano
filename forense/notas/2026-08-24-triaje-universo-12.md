# Nota · TRIAGE-UNIVERSO-12 — 24/ago/2026

Acto: `ACTO TRIAGE-UNIVERSO-12`. Entorno **NUBE** (`cloud_default`), modelo Sonnet. Clon propio, `HEAD=22d792f` (`fb02421` confirmado ancestro — la cabeza del encargo se movió por fusiones posteriores, sin conflicto con el gate: el acto arranca sobre el mismo `main`, refrescado). `REPARA-PROPAGA-15` confirmado fusionado (`ADR-147`, `canon/gobernanza-v1_15.md:3023`); suite `pytest tests/` **VERDE, 32 passed, 0 archivos con fallo**. `data/manifiesto.yaml` = 760 entradas (confirmado, `grep -c "^- id:"`). `data/censo-explotacion-2026-08-17.tsv` = 627 filas de datos. `data/raw` ausente — no se abrió, no aplica a este acto.

**Parte 0 — SALTADA.** `FP-112` y `FP-113` (`forense/firmas-pendientes.tsv:113-114`) están `ABIERTA`. Ninguna firma de mesa F1/F4 vino adjunta a este lanzamiento. No se archiva `R7.3`, no se toca `FP-112`, no se commitea ningún `.md` de coerción, `FP-113` no se toca. El contador de Hito D **no se mueve** en este acto — sigue en `15 de 27`.

**Re-derivación del perímetro de 12** (encabezados `## R` en `forense/hitoD-preregistro-v2_0.md` menos las 15 del bloque append-only, líneas 1078-1093): confirma exactamente `R1.4, R2.1, R2.2, R3.4, R7.3, R7.4, R7.5, R8.2, R8.3, R10.1, R10.2, R10.3`. Coincide con la lista de dirección.

## Triaje por ficha

Ver `data/triaje-hitoD-2026-08-24.tsv` para la tabla completa (regla · cierre_original · clase · veredicto_hoy · ruta_payload · siguiente_acto · prioridad). Resumen del razonamiento:

- **R1.4** — ESTRUCTURAL (paywall Kantar/NielsenIQ sigue vigente para el dato de mercado). Candidato fresco verificado: `ENNViH1-3`/`MxFLS` (panel "D/E") está en el manifiesto desde `2026-07-30`, 137 líneas examinadas, pero su único `usado_para` registrado es `CAL-G3` (elasticidad de ahorro) — nadie lo ha cruzado contra el ítem de marca/consumo compensatorio que R1.4 pide. No se marca VENCIDO EN ALCANCE: es un candidato sin confirmar, no un cierre superado.
- **R2.1** — ESTRUCTURAL. 4 fuentes ya agotadas (ENCUP, ELCOS, ECCO íntegro). El único candidato vivo, `RNM`/`ENAPROCE`-`ENESTYC`, exige trámite ante el Laboratorio de Microdatos INEGI — no es una receta de acceso de un minuto, es trámite institucional de días, fuera del alcance de un acto de repo.
- **R2.2** — ESTRUCTURAL (dato de clima organizacional/rotación, propietario por clase, no por falta de búsqueda). 2 fuentes íntegras agotadas.
- **R3.4** — ESTRUCTURAL, la de mayor madurez técnica: el emisor ya corrió (`hallazgos.md:160`, series Banxico `CF881-CF885` identificadas), `ADR-138` diagnosticó `H1/H2` sin adjudicar. Solo falta firma de mesa sobre `FP-104` reformulada (`ADR-145(D3)`).
- **R7.3** — ESTRUCTURAL, la más lista de las 12: veredicto ya corrido y propuesto (fila `C`), `FP-106` ya firmada fija el criterio caso-por-caso. Solo falta la firma de `FP-112`, exactamente la que la Parte 0 saltada de este acto habría podido ejecutar.
- **R7.4/R7.5** — **INFORMACIONAL**, falsador compartido. `ACLED_HDX` ya está abierto pero degradado a `EXISTE-NO-SATISFACE` (agregado nacional-mes, sin granularidad de evento/geografía). `GDELT`, `UCDP` y `Mass Mobilization` están en `data/cola-adquisicion-2026-08-12.tsv` (líneas 12, 14-17), marcados `CANDIDATA(APERTURA_INDETERMINADA)` / `FUERA-DE-ALCANCE-ADQ15`, aún sin descargar. Son las dos únicas fichas de las 12 con un camino de adquisición ya diseñado y priorizado.
- **R8.2** — ESTRUCTURAL (propietario, plataformas de tandas digitales). Sin candidato nuevo desde 05/ago.
- **R8.3** — ESTRUCTURAL. La marca `C3` de circularidad ENCUCI (`conf.06`: cinco cifras en circulación, dos que dicen ser la misma ENCUCI 2020 con 10.3 puntos de diferencia) **sigue vigente** — verificado contra la ficha (`hitoD-preregistro-v2_0.md:244`), no se disuelve en este acto. Candidato fresco confirmado: `WVS7` México (`data/manifiesto.yaml:11071` en adelante) e `ISSP 2017 Social Networks` `ZA6980` (`data/manifiesto.yaml:11313`, `za6980_q_mx`), ambos con `fecha_descarga: '2026-08-12'`. Presentes en el manifiesto (`EXISTE`) pero **ninguno cruzado contra el falsador exacto** (puente personal vs. enforcement) — `EXISTE` no es `EXISTE-SATISFACE`. Este acto **no abre microdato**; solo confirma la ruta.
- **R10.1** — ESTRUCTURAL (spec defectuosa, `forense/hitoD-R10_1-defecto-spec-v1_0.md` ya declaró "no se corrige hacia atrás"). Espera spec sucesora v2.0, `FP-108` sigue abierta.
- **R10.2** — ESTRUCTURAL (propietario, mismo agotamiento que R2.2 vía ECCO).
- **R10.3** — ESTRUCTURAL, límite ético. La propia ficha pre-declara `D` como preferible a poner en riesgo a un testigo. No se reabre.

## Vocabulario A.4 y regla A.13

Todo negativo de este triaje declara archivos examinados: R1.4 (137 líneas manifiesto), R2.1 (4 fuentes íntegras), R2.2 (2 fuentes íntegras), R7.4/R7.5 (1 archivo, cola-adquisición), R8.2 (sin recuento nuevo — se apoya en el barrido de 05/ago, no repetido hoy), R10.2 (1 archivo, ECCO). Ninguna ruta de payload encontrada (`R1.4`, `R8.3`) fue abierta como microdato — este acto clasifica rutas, no abre datos, conforme a NUBE.

## Enmienda in situ — NO aplicada

Ninguna de las 12 fichas se marca `VENCIDO EN ALCANCE` en `forense/hitoD-preregistro-v2_0.md`. Los dos candidatos frescos (`R1.4` vía ENNViH/MxFLS, `R8.3` vía WVS/ISSP) tienen **ruta confirmada pero verificación pendiente** — su cierre estructural (paywall / circularidad ENCUCI) no quedó superado por la sola presencia del payload en el manifiesto. Marcar vencido en alcance exigiría que el falsador ya corriera contra el dato; eso es trabajo de UBUNTU, no de este acto.

## Tablero (A.12)

Filas propuestas para el tablero de gobernanza — todas exigen firma o visto de mesa antes de correr:

| regla | acción propuesta | gate | firma requerida |
|---|---|---|---|
| R7.3 | archivar → C | FP-112 | visto de mesa sobre corrobora-motor |
| R3.4 | adjudicar H1/H2 sobre emisor ya construido | FP-104 (reformulada) | firma de mesa sobre ADR-138 |
| R7.4/R7.5 | autorizar descarga GDELT/UCDP/Mass Mobilization (hoy `FUERA-DE-ALCANCE-ADQ15`) | ninguna FP existente — requiere nueva | visto de mesa para levantar `FUERA-DE-ALCANCE-ADQ15` |
| R8.3 | autorizar apertura de cuestionario WVS7/ISSP contra el falsador (sin tocar C3) | ninguna FP existente | visto de mesa, entorno UBUNTU |

No se creó una fila `FP-` nueva en `forense/firmas-pendientes.tsv` en este acto: las cuatro filas de arriba son propuesta de tablero para que mesa decida cuál autoriza primero; crear la FP formal se deja al acto que la ejecute (consistente con no forzar estructurales).

## Cierre a mesa

De las 12 reglas faltantes, **ninguna quedó archivada hoy** (Parte 0 saltada, contador sigue en 15 de 27) y **ninguna se marcó vencida en alcance** (los dos candidatos frescos — R1.4/ENNViH, R8.3/WVS-ISSP — tienen ruta confirmada pero no falsador corrido). **Dos quedaron ejecutables mañana sin más firma** (`R7.4`/`R7.5`, cola de adquisición ya priorizada) y **dos quedaron firmes con estampa lista para sellar en cuanto llegue la firma de mesa** (`R7.3` vía `FP-112`, `R3.4` vía `FP-104` reformulada — ambas puramente de gobernanza, cero trabajo técnico pendiente). Las ocho restantes (`R2.1`, `R2.2`, `R8.2`, `R10.2` propietarias/agotadas; `R10.1` esperando spec sucesora; `R10.3` límite ético) se quedan anotadas sin forzar. **Corrida #1 recomendada para mañana en UBUNTU: `R7.4`/`R7.5` juntas** (mismo falsador, cola de adquisición ya diseñada por `ACTO O` el 12/ago, camino más corto y ya autorizado técnicamente) — seguida, si mesa autoriza abrir cuestionario, por `R8.3` contra `WVS7`/`ISSP` sin tocar la marca `C3`.

Este encargo (`forense/encargos/2026-08-24-TRIAGE-UNIVERSO-12.md`) **no existe como archivo en el árbol** — llegó como instrucción de conversación, no como archivo commiteado. No hay archivo que marcar `CONSUMIDO`.
