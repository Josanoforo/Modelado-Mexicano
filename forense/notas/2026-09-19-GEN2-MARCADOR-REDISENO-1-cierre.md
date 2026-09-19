# GEN2-MARCADOR-REDISENO-1 · nota de cierre

**Acto:** `forense/encargos/2026-09-19-GEN2-MARCADOR-REDISENO-1.md` (encargo
original + ADENDA 19/sep/2026, archivados verbatim por A.3) · **base:**
`843a5f9` (`origin/main` al día, 0 commits de diferencia al arrancar) ·
**entorno:** NUBE, `cloud_default`, corpus `data/raw` NO montado (0 archivos
examinados), red no sondeada — este acto no abre microdato ni toca red: lee
YAML/TSV versionados y JSON de `resultados.json` ya sellados. **COMPUERTAS**
(dos): `GEN2-VOCABULARIO-v0.6` (`champion_actual: C2` presente en 2
celdas-D) y `GEN2-REPLAY-ASIENTOS-1` (124 dirs `CALC-*` en `data/corrida0/`)
— ambas confirmadas por producto antes de arrancar, por la mesa, y
re-verificadas aquí.

---

## Qué cambió

1. **`tools/marcador_segmento.py`** (nuevo): deriva
   `data/corrida0/marcador-segmento.tsv` — CERO CIFRAS NUEVAS, solo proyecta
   valores ya sellados en cuatro fuentes (censo ADR-536, los siete ids
   `_ejes_` de `milpa/tramite-ola5-propuesta-v0.yaml`, las dos celdas-D con
   `champion_actual: C2` y `decisiones.tsv`).
2. **`milpa/estimadores-por-segmento.yaml`** (nuevo, derivado): las 20
   celdas C2 con su RESULT sellado (punto/IC95/unidad_dato/tipo_incertidumbre).
3. **`milpa/src/estimadores_segmento.py`** (nuevo) + **`milpa/src/motor.py::estimar_segmento`**
   (nuevo punto de entrada, añadido a `__all__`): consulta de solo lectura
   sobre el YAML derivado; `None` si la celda no está adoptada.
4. **`tools/corrida0.py`**: bloque nuevo al final de `_filas_registro`
   (junto a donde `status()` define `ADOPTADO_ACTIVO`) que proyecta las
   celdas de `estimadores-por-segmento.yaml` como usos activos
   `ADOPTADO-POR-FIRMA`, citando `adopcion:piso-C2-20-celdas` — nunca
   `IMPLEMENTADO-PROPUESTO`, nunca escribe `tramite.yaml`.
5. **`data/corrida0/decisiones.tsv`**: dos filas nuevas —
   `veto:pisos-866` (adenda de mesa 19/sep/2026: excluye por nombre los
   cuatro `CALC-PISOS-*` como piso) y `marcador:sobre-catalogo` (cierre de
   las cuatro NC con el diseño como cita).
6. **`forense/no-corrido.tsv`**: NC-0024, NC-0076, NC-0239, NC-0300 →
   `CERRADA` por superación (enmienda fechada 19/sep/2026, texto original
   intacto). Dos filas nuevas, `ABIERTA`: NC-0333 (gate `cuenta_gen2` de
   las 8 celdas DIN) y NC-0334 (formato de RESULT de `CALC-TRIADA-B-PISO-0001`).
7. **`tests/test_marcador_segmento.py`** + **`tests/test_estimadores_segmento.py`**
   (nuevos): tres guardias del diseño + dos casos de P2. Cableados en
   **`.github/workflows/verify.yml`** (un paso nuevo, bloqueante).
8. **`tests/gonogo_marcador.py`**: una línea nueva de salida tras `GO-MARCADOR`.
9. **`data/INFRAESTRUCTURA-v1_0.md`**: sección nueva (no numerada como
   dominio — sigue el patrón de las secciones post-hoc ya existentes, p. ej.
   `corrida0/{corridas,resultados,usos}.tsv`) documentando las dos tablas
   derivadas de este acto.
10. **`forense/notas/insumos-externos/marcador/codex-03-2d662e7.diff`**
    (P0): diff de lectura de `origin/codex/gen2-marcador-adopcion-cli-1`
    (HEAD real al arrancar, no el SHA viejo de la adenda). NO se fusionó,
    NO se hizo cherry-pick; la rama sigue en remoto, sin tocar.

## Por qué importa

El marcador por segmento (diseñado desde el 8/sep, nunca corrido) existe
hoy como tabla derivada, verificable con un comando, sin inventar ningún
número: 97 celdas nacionales del censo de identidad, 74 celdas marginales
sin piso (persistencia vetada), y 20 celdas de cruce con estimador
adoptado por firma de mesa. Cuatro deudas de no-corrido (NC-0024/0076/0239/0300)
que llevaban entre 11 días (NC-0300) y 42 días (NC-0024) abiertas cierran
por superación con un artefacto real, no con prosa.

## Qué decisión permite

Mesa puede: (a) decidir si sella `cuenta_gen2: SI` en la spec de
`CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001` para que las 8 celdas DIN
muevan `N_resultados_gen2_adoptados_activos` igual que las 12 TRA
(NC-0333); (b) autorizar o no un sucesor que serialice
`CALC-TRIADA-B-PISO-0001` (o un reemplazo) con un `RESULT` por celda en el
mismo formato que las celdas-D, para que el piso de persistencia nacional
deje de ser SIN-PISO por formato (NC-0334); (c) revisar el diff archivado
del insumo Codex y decidir si algo de él se retoma por otra vía.

## Qué falta para usarlo

Correr `python3 tools/marcador_segmento.py --escribe` tras cualquier nueva
celda-D con `champion_actual` != NINGUNO, o tras cualquier cambio en
`decisiones.tsv`/`tramite-ola5-propuesta-v0.yaml` — no hay cron todavía,
es manual (como `corrida0 registro --escribe`).

## Los tres conteos de universo (adenda P1-b)

| universo | denominador | comando |
|---|---:|---|
| (i) celdas marginales `_ejes_` (`tramite-ola5-propuesta-v0.yaml`) | **74** celdas en 24 ejes de 7 reglas `_ejes_` | `python3 tools/marcador_segmento.py --json` → `universo_i_marginal_ejes` |
| (ii) celdas nacionales/compuestas (censo ADR-536) | **97** | `python3 tools/marcador_segmento.py --json` → `universo_ii_nacional_censo` (== filas de datos de `forense/notas/2026-09-16-GEN2-EMISOR-ESTADO-1-censo.tsv`) |
| (iii) celdas de cruce (ADR-538/542 + reservadas) | **20 adoptadas** + **22 grupos RESERVADA** (176 celdas) + **1 grupo CONSUMIDA-SIN-PILOTO** (12 celdas, NC-0328) | `python3 tools/marcador_segmento.py --json` → `universo_iii_cruce` |

Suma de grano "grupo" (marginal + cruce-adoptadas + cruce-grupos, sin
contar nacional): 74 + 20 + 23 = **117**, que coincide con el número que
el propio encargo anticipaba ("20 evaluadas de 117") — coincidencia
verificada, no forzada: se llegó a ella derivando de las fuentes, no
copiando la cifra del encargo.

## Los cuatro números derivados al pie (diseño §4)

| número | valor | comando |
|---|---:|---|
| cobertura de piso | **20** | `--json` → `cobertura_de_piso` |
| valor añadido (M vs R, comparación legítima) | **0** | `--json` → `valor_anadido` (FP-383: el emisor queda fuera del marcador; hoy no hay comparación M-vs-R legítima) |
| estimador adoptado | **20** | `--json` → `estimador_adoptado` |
| `SIN-PISO` por instrumento y eje | **74** (todas las marginales) | `--json` → `sin_piso` |

## `status` antes/después de `N_resultados_gen2_adoptados_activos`

```
$ git stash && python3 tools/corrida0.py status | grep adoptados_activos
N_resultados_gen2_adoptados_activos=24
$ git stash pop && python3 tools/corrida0.py status | grep adoptados_activos
N_resultados_gen2_adoptados_activos=36
```

**24 → 36, no 24 → 44.** Solo las 12 celdas TRA (`escolaridad_proxy x
dominio_urbano_rural`) mueven el contador: su CALC
(`CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001`) declara `cuenta_gen2: SI` en su
spec. Las 8 celdas DIN (`localidad x edad`) están en
`estimadores-por-segmento.yaml` con `estado: ADOPTADO-POR-FIRMA` en la
tabla derivada, pero su CALC
(`CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001`) declara
`cuenta_gen2: PENDIENTE-DE-MESA` — un gate DISTINTO al de adopción por
firma, y `status()` exige `cuenta_gen2=SI` antes de entrar a
`ids_sellados_gen2`. Medido, no forzado; asentado en NC-0333.

## Tabla de afirmación → comando

| afirmación | comando |
|---|---|
| las dos compuertas están cumplidas | `git log --oneline origin/main \| grep -c "GEN2-VOCABULARIO-v0.6\|GEN2-REPLAY-ASIENTOS-1"` + `grep -l "champion_actual: C2" data/curacion-registro/celdas-d/*.yaml` (2) + `ls data/corrida0 \| grep -c "^CALC-"` (124) |
| la tabla y la herramienta no existían antes de este acto | `git show 843a5f9:tools/marcador_segmento.py` → error (no existía) |
| 97 celdas nacionales | `python3 tools/marcador_segmento.py --json \| grep universo_ii` |
| 74 celdas marginales, todas SIN-PISO | `python3 tools/marcador_segmento.py --json` |
| 20 celdas de cruce adoptadas por firma | `grep -c "^CRUCE::" data/corrida0/marcador-segmento.tsv` con `estado=ADOPTADO-POR-FIRMA` |
| el veto de mesa excluye los CALC-PISOS por nombre | `grep -n "CALC-PISOS" tools/marcador_segmento.py` (0 apariciones fuera de la lista de exclusión — nunca se abren) |
| `CALC-TRIADA-B-PISO-0001` no calza por formato | `python3 -c "import json; d=json.load(open('data/corrida0/CALC-TRIADA-B-PISO-0001/resultados.json')); print(list(d['resultados'])[:3])"` → `RESULT-TBP-*`, no un id por celda-D |
| `status` 24→36 | `python3 tools/corrida0.py status \| grep adoptados_activos` (antes/después con `git stash`) |
| las tres guardias pasan | `python3 tests/test_marcador_segmento.py` |
| P2 responde punto+IC+unidad y `None` | `python3 tests/test_estimadores_segmento.py` |
| `gonogo_marcador.py` sigue en GO y trae la línea nueva | `python3 tests/gonogo_marcador.py` |
| las cuatro NC cierran por superación | `awk -F'\t' '$1=="NC-0024"||$1=="NC-0076"||$1=="NC-0239"||$1=="NC-0300" {print $1,$10}' forense/no-corrido.tsv` → `CERRADA` ×4 |
| suite en línea base sin FAIL nuevo | `python3 tests/check.py --baseline` |

## Reservas materiales

- **NC-0333** (nueva): las 8 celdas DIN no mueven `ADOPTADO_ACTIVO` por un
  gate de spec (`cuenta_gen2`) distinto del de adopción por firma —
  decisión de mesa pendiente, no bloqueador de este acto.
- **NC-0334** (nueva): el piso de persistencia nacional
  (`CALC-TRIADA-B-PISO-0001`) sigue SIN-PISO por formato de id, no por
  contenido — un sucesor de serialización lo resuelve, no un veto.
- El insumo Codex (P0) queda archivado sin fusionar; su contenido no se
  evaluó más allá de guardarlo como diff de lectura (perímetro explícito
  de la adenda).
- Las filas RESERVADA/CONSUMIDA-SIN-PILOTO de cruce se agrupan por
  par-de-ejes (22 grupos, no 176 filas individuales) — grano declarado en
  el diseño de la tabla, no una celda por fila para esas dos categorías;
  las filas NACIONAL, MARGINAL y CRUCE-adoptadas sí van una por celda.
