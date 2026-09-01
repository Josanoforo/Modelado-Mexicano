# Scoreboard marco-M v1.1 — primera corrida real

`ACTO MAESTRA33-E8 · SCORE-M-1`, 1/sep/2026. Producido por
`python3 tools/score_marco_m.py` sobre
`forense/prereg-duelo-v2/marco-M-sorteado-v1_1.tsv` (11 celdas), leyendo
`corridas-M/`, `corridas-R/` y `corridas-L/` tal como existen hoy en el
árbol — no se emitió ningún M, R ni L para producir este tablero.

## 0 · Terreno movido contra el encargo (A.8), declarado antes de puntuar

El encargo (redactado contra `d353d82`) asumía "probablemente 0 celdas
puntuables hasta que C3 entregue R". Entre la redacción y esta corrida,
`ACTO MAESTRA33-C3 · CODIFICA-R-1` (`PR #423`) fusionó y produjo R real
para 4 de las 11 celdas del marco v1.1 (`CIV-M-01/06/08/09`, más 15
celdas del marco anterior a F-DD que no forman parte de este universo).
**El resultado real de esta corrida es 4 celdas puntuables, no 0** — se
reporta tal cual sale, sin forzar la cifra que el encargo anticipaba.

## 1 · Universo (marco-M-sorteado-v1_1.tsv, 11 celdas)

| id_celda | M | R | L | puntuable | VERIFICACION-NO-PUNTUA (F-DD) |
|---|---|---|---|---|---|
| CIV-M-01 | SI | SI | NO | **SI** | NO |
| CIV-M-06 | SI | SI | NO | **SI** | NO |
| CIV-M-08 | SI | SI | NO | **SI** | NO |
| CIV-M-09 | SI | SI | NO | **SI** | NO |
| CIV-M-11 | SI | NO | NO | NO | NO |
| CIV-M-12 | SI | NO | NO | NO | NO |
| CIV-M-13 | SI | NO | NO | NO | NO |
| FAM-M-01 | SI | NO | NO | NO | NO |
| TRA-M-03 | SI | NO | NO | NO | NO |
| TRA-M-05 | SI | NO | NO | NO | NO |
| TRA-M-07 | SI | NO | NO | NO | NO |

**0 de 11 celdas marcadas `VERIFICACION-NO-PUNTUA` bajo F-DD** (todas
traen `grado_DD = "P1 PUNTUA"` en `marco-M-sorteado-v1_1.tsv`; las 5
celdas de ola/instrumento de calibración que sí quedaron marcadas
`P0 VERIFICACION-NO-PUNTUA` en `marco-M-congelado-v1_1.tsv` no fueron
sorteadas en v1.1 y no aparecen aquí).

**L pendiente: 11 celdas** — ninguna de las 120 corridas de
`corridas-L/` trae un `id_celda` del marco-M (todas usan los ids del
marco anterior a F-DD: `CIV-08`, `DIN-03`, etc.). El "11" no se copió
del encargo: es el conteo real de este universo, recalculado contra el
árbol de hoy (que también dio 11 por casualidad de tamaño, no por
herencia del texto del encargo).

Nota aparte, fuera del universo v1.1 pero visible en el árbol:
`marco-M-sorteado-v1_0.tsv` trae 2 filas más (`TRA-M-01`, `TRA-M-02`) de
un esquema anterior a F-DD (sin columna `grado_DD`/`elegible_v1_1`).
Ambas tienen M (`estado_M = EMITE`) pero ninguna tiene R en
`corridas-R/` — no puntuables tampoco, y no se cuentan en el universo de
11 de arriba porque el encargo cita explícitamente `v1_1` como universo.

## 2 · Las 4 celdas puntuables — aritmética directa (M vs. R), sin `ejecutar_scoring`

`ejecutar_scoring` de `scoring-adv1-m3.py` **no corrió** sobre estas 4
celdas (ver §3, `delta` sigue sin sello) — esto es la misma aritmética
declarada de `procedimiento-scoring-v1_0.md §5` (`dif`, banda
`±0.5·EE(R)`), aplicada a `M` en vez de `L-solo` porque `L` no existe
para ninguna de las 4:

| id_celda | p (M) | R | EE(R) | dif = p − R | banda ±0.5·EE(R) | dentro de banda |
|---|---|---|---|---|---|---|
| CIV-M-01 | 0.294313 | 0.258999 | 0.006971 | +0.035314 | ±0.003485 | NO |
| CIV-M-06 | 0.294313 | 0.222668 | 0.004907 | +0.071645 | ±0.002453 | NO |
| CIV-M-08 | 0.294313 | 0.234696 | 0.004945 | +0.059617 | ±0.002473 | NO |
| CIV-M-09 | 0.294313 | 0.203809 | 0.005374 | +0.090504 | ±0.002687 | NO |

Las cuatro reciben el mismo `p = 0.294313` de `M` porque `emitir_binaria`
toma el punto medido de la regla `civico.denuncia.miedo_desconfianza`
(`milpa/tramite.yaml:202`), no una estimación por ola — las 4 celdas son
transferencias de ola distintas de la misma regla y conducta bajo F-DD
(`ADR-237`), no cuatro mediciones independientes de `M`. Ninguna de las
4 cae dentro de su banda TOST: `M` sobre-estima a `R` en las cuatro,
consistente con la magnitud (~3.5 a ~9 puntos porcentuales).
**Esto no es un veredicto** — es la lectura celda-por-celda contra el
árbitro, sin pasar por `adjudicar_secuencia` (que exige `delta`, seguro
inexistente).

## 3 · Por qué `ejecutar_scoring` sigue sin producir un agregado, hoy

`nivel_ic=0.95`/`seed=42` ya están sellados (`FP-168`, FIRMADA
30/ago/2026, `ACTO MAESTRA32-E9 · PROPAGA-2`) — se incluyeron en la
`entrada_scoring` que `tools/score_marco_m.py` construye. Verificado en
vivo, invocando `ejecutar_scoring` sobre esa entrada real (11 celdas
universo, 4 con `mediciones={}` porque no hay baseline `B`
normalizable — mismo hallazgo estructural de `E9`, `procedimiento-scoring
-v1_0.md §4):

```json
{"resultado": "ErrorScoring", "codigo": "CONFIGURACION_INVALIDA", "mensaje": "faltan parámetros obligatorios: delta"}
```

**Un parámetro menos que en v1.0** (`delta, nivel_ic, seed` → solo
`delta`): el sello de `FP-168` sí quitó una capa real. `delta` sigue sin
cita como escalar único de corrida — nadie lo ha sellado — así que este
acto no lo inventa, igual que `E9` no lo inventó.

## 4 · CONTADOR

**Celdas puntuadas: 0 → 4** (sobre el universo de 11 de
`marco-M-sorteado-v1_1.tsv`), declarado, no maquillado contra el
"probablemente 0" del encargo. `ejecutar_scoring` agregado: sigue sin
producir salida (bloqueado en `delta`, no en `nivel_ic`/`seed`, que ya
se sellaron). `L pendiente: 11 celdas` de 11.

## LO QUE ESTE ACTO NO HACE

No edita `scoring-adv1-m3.py`. No emite `M`, `R` ni `L` nuevos. No activa
el corredor `E`. No inventa `delta`. No cambia la Configuración sellada
(`FP-168`, `M-ENLACE=A`, `M-AGREGA=a′`).
