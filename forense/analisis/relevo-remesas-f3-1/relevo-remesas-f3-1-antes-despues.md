# GEN2-RELEVO-REMESAS-F3-1 · antes/después de RES-0035

Base inicial: `e4f5f771b7fd9bccc88d3b6c30d0e5362b0e52a5`. Árbol combinado antes de
regenerar: `origin/main` en `fe223a9d5f14c609327d7d30181295b4469d43ae`.

La comparación se hizo ejecutando el productor anterior desde un worktree
separado de `origin/main` y el productor modificado sobre los mismos insumos.
De 207 filas, sólo `RES-0035` difiere.

| Campo | Antes | Después |
|---|---|---|
| Consumidor | `familia.seguro.volatilidad_ausencia_estado:recibe_remesas` | sin cambio |
| Veredicto vigente | `CONFLICTO-ENTRE-VEREDICTOS` | `LISTADO-PARA-MESA-REPRODUCE` de `CALC-ENIGH-0001/RESULT-ENIGH-A-ADOPCION` |
| Antecedente | `CALC-B-0001/RESULT-B-ADOPCION-P3=NO-ADOPTABLE-POR-GRANO` | `CALC-B-0001/RESULT-B-ADOPCION-P3=SUPERADO` |
| Referencia completa | las dos ramas separadas como conflicto | `CALC-B-0001/RESULT-B-ADOPCION-P3=SUPERADO->CALC-ENIGH-0001/RESULT-ENIGH-A-ADOPCION` |
| Cita del consumidor | `RESULT-B-ENIGH-2022-P` | sin cambio |
| Valor sellado citado | `0.04569409956405095` | sin cambio |
| Valor materializado | `0.045694` | sin cambio |
| Grano de adopción | seis decimales del consumidor | sin cambio; comparación exacta después de representar al grano |
| Tolerancia de reproducción | `1e-10` | sin cambio; no se usó como grano de adopción |

## Identidad científica y orden sellado

Las dos corridas usan ENIGH 2022, hogares de `concentradohogar`, universo
completo sin filtro, desenlace `remesas > 0` y ponderador `factor`. Ambas
publican el mismo punto, `0.04569409956405095`. La segunda corrida vuelve a
medir una sola ola y conserva separadas sus comparaciones contra GEN1 y B.

| CALC | Corrida sellada | Fecha de `ejecucion.json` | Sello físico |
|---|---|---|---|
| `CALC-B-0001` | `CALC-B-0001--098298ca327f` | `2026-09-09T02:01:48Z` | `COINCIDE` |
| `CALC-ENIGH-0001` | `CALC-ENIGH-0001--d13529e2e3e9` | `2026-09-15T16:23:22Z` | `COINCIDE` |

El selector exige que esas fechas coincidan entre `corridas.tsv` y el recibo
de ejecución, que los metadatos e identidades coincidan y que el sello físico
cubra los bytes. Una fecha ausente, ilegible o empatada conserva el conflicto;
no se consulta mtime, fecha de commit, nombre de archivo ni re-verificación.

## Alcance

Desaparece el bloqueo técnico de NC-0216: el escritor canónico ya materializa
la adjudicación F-3 registrada. No hay medición nueva, cambio numérico,
reemplazo de cita ni resolución de F-2/NC-0217. `RES-0047/0049` conservan
`CONFLICTO-ENTRE-CANALES` y ninguna otra pareja obtiene precedencia temporal.

