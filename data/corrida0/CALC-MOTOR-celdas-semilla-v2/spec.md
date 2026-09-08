# `CALC-MOTOR-celdas-semilla-v2` — el motor matricial, ejercido de punta a punta

`ACTO AUTO-MOTOR-1 · RECUPERA-Y-EJERCITA`, 8/sep/2026, P2.
Sucesora declarada (`repite_de`) de `CALC-MOTOR-celdas-semilla`
(`ACTO GEN2-T9 · EL MOTOR ES LA MATRIZ`, P3(e)). Entorno **NUBE**, sin
corpus y sin red. **CONTADOR: cero GEN2.**

## 1 · Qué pregunta responde

La predecesora midió que la ruta matricial sellada por `ADR-91` **no
arrancaba**: `procedencia.cargar()` lanzaba `ClaseDesconocida` sobre dos
valores de `clase:` (`REFUTADO-POR-COTA`, `EVIDENCIA_EXPERIMENTAL_TERCEROS`)
que `milpa/src/clases.py` no reconocía por prefijo (`NC-0023`). Esta corrida
pregunta: **con las dos clases reparadas, ¿la ruta real —
`procedencia.cargar()` → `matriz.cargar_B()` → `motor.evaluar()` — corre
sobre las tres celdas-D semilla?**

## 2 · Qué cambió, y dónde

`milpa/src/clases.py` (commit `acd1ffb`, ver `git log`): dos prefijos
nuevos en el enum `Clase`, `REFUTADO_POR_COTA` y
`EVIDENCIA_EXPERIMENTAL_TERCEROS`, sin caso por defecto que admita
cualquier valor.

`milpa/src/procedencia.py`, mismo commit: `_recorrer()` da precedencia
semántica a la `clase:` explícita de un nodo sobre la clase implícita del
bloque que lo contiene — el prior `REFUTADO-POR-COTA` de
`tramite.gobierno_digital.coercitivo` ya no produce una segunda `Entrada`
`ASIGNADO` con la misma llave, y `REFUTADO_POR_COTA` queda excluida de
`consumibles()`. `EVIDENCIA_EXPERIMENTAL_TERCEROS` valida al cargar que
trae `cita` y `llave_id` (contrato `ADR-204`/`FP-164`).

`milpa/procedencia.yaml` **no se tocó** — mismo `sha256` que declaró la
predecesora (`556eb8e9…`). El cambio es del cargador, no del dato.

## 3 · Qué corre, y qué no

| pieza | estado | cómo se comprueba |
|---|---|---|
| `momentos.cargar_catalogo()` | **corre** | 22 momentos, 8 `AJUSTE` / 14 `HOLDOUT` |
| el muro `AJUSTE`/`HOLDOUT` | **se ejerce** | se toca cada `HOLDOUT` por el único camino permitido y se comprueba que `valor_de` LANZA; 14 de 14 intocados |
| `motor.celdas_semilla()` | **corre** | las tres celdas-D del disco, por `listdir` |
| `celdas.CORTES_C1` | **corre** | 4 ejes sellados bajo M2, 2 `PENDIENTE` (`FP-53`) |
| `procedencia.cargar()` | **corre** — antes lanzaba `ClaseDesconocida` | `RESULT-MOTOR-ESTADO-B = CARGA` |
| `matriz.cargar_B()` | **corre** | 15 celdas no-cero, 14 puntuales, 1 `SinMagnitud` (`G5×familismo_obligacion`, sin cambio: sigue sin magnitud, correctamente) |
| `motor.evaluar()` × 3 celdas-D | **corre** | ver §4 — tres veredictos reales, ninguno fabricado |

## 4 · Los tres veredictos, y por qué ninguno es "favorable" ni tiene que serlo

```
G5.familismo_obligacion.actitud    = EXISTE-NO-SATISFACE   (SinMagnitud: G5×familismo_obligacion no tiene número — ADR-30)
G5.obligacion_medida.conducta      = EXISTE-NO-VERIFICADO   (universo_candidatos POR DECLARAR — calibración E1+/BARRIDO-2)
G5.radio_confianza.encuci_vs_enbiare = EXISTE-NO-VERIFICADO (misma razón)
```

`motor.py` declara desde su propio docstring que E0 no calibra ni estima:
esta corrida ejercita el camino real hasta donde el contrato de cada celda
lo permite, y un veredicto de insuficiencia de evidencia aquí **es** el
resultado correcto — no una falla de esta corrida ni del medidor. Ninguna
magnitud se fabricó para convertir `SinMagnitud` en un número, y ninguna
excepción inesperada se sustituyó por un `RESULT` tranquilizador (el
medidor no envuelve estas cinco llamadas en `except Exception`).

## 5 · El contrato de las dos clases nuevas, medido

- `RESULT-MOTOR-REFUTADO-POR-COTA-N = 1` — la única entrada
  `REFUTADO-POR-COTA` del árbol (`tramite.gobierno_digital.coercitivo`).
- `RESULT-MOTOR-REFUTADO-POR-COTA-CONSUMIBLE = 0` — no aparece en
  `procedencia.consumibles()`: el prior refutado no reingresa como
  parámetro utilizable, ni por su propia clase ni por la clase implícita
  del bloque que lo contiene.
- `RESULT-MOTOR-EVIDENCIA-TERCEROS-N = 1` — `EXP-COMPARTAMOS-1`, cargada
  con `cita` y `llave_id` verificados por `procedencia.py` al leerla
  (`EvidenciaTercerosIncompleta` si faltara alguno). No se extrajo ningún
  número de su texto: `matriz.cargar_B()` no lee
  `evidencia_experimental_terceros` — nunca lo hizo, ese bloque no es uno
  de sus inputs.

## 6 · Por qué `cuenta_gen2: NO`

Regla E.1 (`ACTO GEN2-T9`, D-1): el motor consume `milpa/procedencia.yaml`
entre sus inputs, así que esta corrida cae bajo la regla mecánicamente,
igual que la predecesora. Que ahora cargue con cadena completa no cambia
la procedencia del número — sigue sin haber ningún número de México aquí.

## 7 · Relación con el diagnóstico anterior

Sucesión declarada (`repite_de: CALC-MOTOR-celdas-semilla`), no reemplazo:
la predecesora **no se reescribe** — sus bytes, su sello y su
`RESULT-MOTOR-ESTADO-B = NO-EJECUTABLE` quedan intactos como evidencia
histórica de lo que el árbol permitía correr en su commit. Esta corrida
explica el cambio de estado; no lo borra.

## 8 · Determinismo

No hay estocasticidad: `seed.aplica: false`. Todas las lecturas son de
archivos versionados del repo, con SHA declarado. Dos corridas sobre el
mismo árbol producen los mismos bytes, y `verify` debe dar
`REPRODUCE` / `IDENTICO`.

## 9 · A.13 — cuántos archivos examinó el negativo

`RESULT-MOTOR-ARCHIVOS-EXAMINADOS` lleva la cuenta de los archivos/fuentes
que el medidor abrió para producir su veredicto.
