# SPEC · MÉTRICA RECTORA `celdas_validadas` · v1.0

Spec humana de la métrica que `tools/celdas_validadas.py` deriva (D-15: esta
spec basta para recalcular sin leer el código; si no basta, es hallazgo).
Nace del ACTO GEN2-TUBERIA-METRICA-RECTORA-1 al mover la función desde
`tools/tablero_programa.py` (donde la creó ACTO GEN2-MARCADOR-E-INFORME-1,
`#969`) a un módulo propio. La spec **no** cambia la definición sellada por
`#969`: la documenta donde antes no había documento, sólo código.

## 1 · Definición

Una celda cuenta como **validada** cuando su predicción (M) se emitió ANTES
de ver el dato de contraste y se comparó contra un valor de referencia (R)
con un error sellado. **VALIDADA no quiere decir ACERTADA**: el VEREDICTO
de la celda-D (`SIN-CANDIDATO-SUPERIOR`, `FALSADOR-DEBIL`, o el que vence)
no entra al conteo — sólo que el veredicto EXISTA y esté sellado, porque un
veredicto ausente significa que nadie comparó.

## 2 · Fuentes (universo)

1. `data/corrida0/marcador-segmento.tsv` — filas del marcador, una por celda
   de cruce/persistencia comparada contra R.
2. `data/curacion-registro/celdas-d/*.yaml` — celdas-D con veredicto sellado
   (`estado_decidibilidad: PUNTUADA` + `veredicto` no vacío).
3. Los CALC referidos desde esos YAML por `momentos_holdout_refs`
   (`data/corrida0/CALC-*/resultados.json`), más
   `data/corrida0/CALC-TRIADA-0002/resultados.json` (clase 3, duelo de tres
   nacional).

Ninguna cifra se teclea: todo sale de esos tres orígenes, leídos en la
misma sesión que reporta el número (§2 de las instrucciones del proyecto).

## 3 · Tres clases, que no se funden en una cifra (§4.3/§4.4)

- **Clase 1 · cruce vs R**: celdas-D adjudicadas (`_celdas_d_adjudicadas`)
  con veredicto sellado y error por celda localizable en su CALC de
  árbitro. La escala (PUNTOS-PORCENTUALES o PROPORCION) se DERIVA contra el
  `margen_material` sellado del YAML — se prueba el factor 1 y el 100 y se
  adopta el que casa dentro de `1e-5`; si ninguno casa, la celda-D **no
  cuenta** y se declara con su motivo (nunca se adivina la escala).
- **Clase 2 · persistencia t−1 vs R**: filas del marcador con
  `error_piso_pp` no vacío, agrupadas por instrumento.
- **Clase 3 · duelo de tres, nacional**: `CALC-TRIADA-0002`, reportada
  aparte — no entra al total de la clase 1+2 porque es un dominio distinto
  (unidad y universo propios).

### 3.1 · Clase 1, dos formas de reportar el error (ACTO GEN2-CONTADORES-CONSUMO-1)

La clase 1 tiene dos formas de emitir el error, según si el CALC construye
un grid de cruce o no. Las dos cuentan por CELDA PUNTUADA (nunca 1 por
celda-D) — es la MISMA regla, no una excepción:

- **Por celda de cruce** (la forma original, §3 arriba): el CALC emite un
  RESULT por cada celda del cruce (`-C2-D-PP` sufijo, `-ARB-D-C2-`
  prefijo). `n_celdas` es el número de celdas puntuadas.
- **Por conducta agregada** (crédito, NC-260923-GEN2-DIN-CREDITO-CELDAS-D-2-f6a3-02):
  el CALC no tiene un grid de dos ejes — mide una conducta completa contra
  16 celdas marginales y sólo publica el AGREGADO del candidato
  `champion_actual`: `...-{CHAMPION}-MAE-PP` (que debe casar, factor 1 o
  100, contra `margen_material` — misma derivación que el resto de la
  clase 1) y su gemela `...-{CHAMPION}-N-CELDAS-PUNTUADAS`. `n_celdas` es
  ese N; no hay mediana/máximo por celda porque el CALC no los publica, así
  que `error_mediano_pp = error_max_pp = MAE_PP` (el único número que hay).
  Sin per-cell breakdown, se declara con `escala_cruda:
  AGREGADO-POR-CONDUCTA`.
- **Sufijo `-D-C2`** (NC-260923-GEN2-DUELO-ENCIG2025-CIERRE-1-657c-03;
  generalizado por ACTO GEN2-CONTADORES-CONSUMO-2, 23/sep/2026, P4):
  `CALC-ENCIG-DUELO-2025-ADJUDICACION-0001` emite el error por celda como
  `...-D-C2` (sin "ARB" ni "PP"). Es un archivo COMPARTIDO por varias
  celdas-D a la vez (edad_x_sexo Y escolaridad_x_sexo en el mismo
  `resultados.json`): el sufijo se localiza por celda leyendo
  `adjudicacion_por_celda` del propio YAML (nunca por posición, por nombre
  adivinado ni por `k.endswith('-D-C2')` a ciegas), quitando el sufijo
  `-{id_candidato}-P` de cada `resultado_puntual` para obtener el prefijo
  de esa celda. **Este sufijo se reconoce para TODA celda-D** — ya no está
  restringido al prefijo `GOB.gobierno_digital.encig2025.` — porque el
  scoping real es `adjudicacion_por_celda`, no el prefijo del id: una
  celda-D sin ese campo nunca produce un hit, prefijo o no. El mismo
  sufijo `-D-C2` aparece también en
  `CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001`
  (`TRA.evade_norma.envipe2025.dominio_x_sexo` y sus tres hermanas, con
  `champion_actual: NINGUNO` — verificado por comando: su promedio del
  sufijo también casa exacto con su `margen_material`), pero esas cuatro
  celdas-D no declaran `adjudicacion_por_celda` en su YAML (nadie adjudicó
  un champion ahí): la generalización no las cuenta — verificado
  antes/después, `celdas_validadas` no se mueve (219 -> 219). Si algún día
  mesa adjudica un champion ahí y alguien puebla `adjudicacion_por_celda`,
  esta misma regla las cuenta sin tocar el código de nuevo.

`total_celdas_validadas = n(clase 1) + n(clase 2)`. La clase 3 se reporta
por separado y nunca se suma al total.

## 4 · Qué NO cuenta, y por qué

- Filas `IDENTICO` del marcador (`estado == "IDENTICO"`): M y R son el
  mismo número porque `emisor_vs_arbitro = EMISOR=ARBITRO` — copiado, no
  predicción contrastada.
- Celdas de `formalidad` con piso pero SIN `error_piso_pp`: su error de
  persistencia es un CALC sucesor, no de esta métrica.
- Celdas-D sin veredicto sellado (`estado_decidibilidad != PUNTUADA` o
  `veredicto` vacío), o con veredicto sellado pero sin RESULT de error por
  celda localizable en `momentos_holdout_refs`.

## 5 · PROSPECTIVA / RETROSPECTIVA — nunca se suman (firma de mesa 21/sep/2026)

`prospectividad_del_marcador` trae el conteo crudo de la columna
`prospectividad` del marcador (derivada por `tools/prospectividad.py` desde
los sellos, orden de sellos o diff — nunca se teclea) con sus cinco valores
posibles: `PROSPECTIVA`, `RETROSPECTIVA`, `IDENTICO-EMISOR-ES-ARBITRO`,
`SIN-EMISION`, `EMITIDA-SIN-R`. Las dos primeras son las dos sub-cifras que
`corrida0 status` y `digesto --mesa` imprimen en líneas propias
(`celdas_validadas_prospectiva`, `celdas_validadas_retrospectiva`); **nunca
se suman entre sí ni con el total** — miden columnas distintas (una,
cuántas emisiones nacieron antes de ver R; otra, cuántas después) y sumarlas
sería contar dos veces la misma celda si aparece en ambos universos de
alguna corrida futura. `celdas_emitidas_sin_r` (= `EMITIDA-SIN-R`) es
demanda, no validación: emisiones que esperan su R.

## 6 · `adoptadas` — NO existe (queda fuera de este acto)

La propuesta de una sub-cifra `ADOPTADAS` (estimador adoptado por firma de
mesa) no está sellada: no hay definición ni fuente acordada. Este acto no
la deriva. Cuando mesa la selle, con su fuente, es una pieza propia (ver
`## 10 · SUCESORES` del encargo).

## 7 · Contrato de `--json`

`python3 tools/celdas_validadas.py --json` devuelve el mismo diccionario
que devolvía `tablero_programa._celdas_validadas()` (contrato leído por
`tests/test_celdas_validadas.py`, que no cambia de forma) más un bloque
`universo` con `sha` (el `HEAD` contra el que se derivó) y `archivos_leidos`
(la lista de §2 de esta spec). `--linea` imprime:

```
celdas_validadas <N> (prospectiva <P> · retrospectiva <R>) @ <sha corto>
```

## 8 · Monotonía

La métrica no baja de un merge a otro sin que una fila `VENCIDO-EN-ALCANCE`
de mesa (A.10) lo explique — buscada por objeto en
`data/corrida0/decisiones.tsv` y `forense/*.tsv`, nunca por defecto. Es la
única bajada legítima: un veredicto sellado no se borra (E.3).

## 9 · Marca de definición (ACTO GEN2-ADOPCION-BLOQUE-Y-PINES-1, 24/sep/2026, firma P)

El contador subió 92 → 219 el 23/sep/2026 por el cambio de §3.1 (crédito
por conducta agregada + sufijo `-D-C2` de ENCIG 2025), no por 127
validaciones nuevas emitidas ese día — una serie que no marca «desde cuándo
cuenta qué» lee ese salto como si fuera producción, y no lo es. La spec
declara el ancla verbatim, para que no haya que leer `git log` a mano cada
vez: `tools/celdas_validadas.py::DEFINICION_DESDE` fija el commit corto
`38dd709` (mensaje `ACTO GEN2-CONTADORES-CONSUMO-1 (P-B): celdas_validadas
cuenta credito y ENCIG 2025`, fusionado a `main` por el PR #1086 — el
encargo original citó «#1078» de memoria; ese PR no toca este archivo,
verificado por `git log --oneline -- tools/celdas_validadas.py`, y el commit
real se re-derivó por comando antes de fijarlo aquí). `corrida0 status` y
`--json`/`--linea` de este módulo imprimen
`celdas_validadas_definicion_desde=<ese commit>`, al lado del total — nunca
fundido con él. Cuando la definición cambie otra vez (una clase nueva, una
forma nueva de leer el error), este ancla se actualiza en el mismo commit
que cambia el código, con su propia entrada aquí; las anclas viejas no se
borran, se leen en `forense/hallazgos.md`/`canon/gobernanza-v1_15.md` de la
fecha correspondiente.
