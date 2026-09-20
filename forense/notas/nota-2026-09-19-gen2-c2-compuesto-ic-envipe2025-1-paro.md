# ACTO GEN2-C2-COMPUESTO-IC-ENVIPE2025-1 · cierre por hallazgo en P0

**19/sep/2026 · CAJA (Ubuntu/WSL2), Opus 5 · corpus montado (`tools/entorno.py`: `montado=SI`, `archivos_examinados=419`, `raices data_raw:SI descargas_mx:SI`, `red=200`) · cero microdato abierto por este acto.**
Encargo archivado verbatim por 0-bis A.3 en `forense/encargos/2026-09-19-GEN2-C2-COMPUESTO-IC-ENVIPE2025-1.md`.
**Contadores movidos: cero.** No se congeló spec, no se congeló medidor, no se selló corrida, no se quemó el CALC-id reservado.

Universo del encargo, para el lector: los 4 pares `EMITIBLE` de ENVIPE 2025 en `data/corrida0/c2-compuesto-dictamen-v1_0.tsv` (38 celdas); unidad del dato **DELITO** (universo restringido a delitos `BP1_20 ∈ {1,2}`, no persona); escala proporción; clase de evidencia **(a)**. Celdas que quedaron con IC — derivado: **0 de 38**.

## 0 · Veredicto

`PARO-PREMISA` en P0, suficiente por sí solo para que `COMMIT-1` no se congele hoy:

**El módulo guardado no admite ninguno de los 4 pares.** `tools/celda_d/marginales_reproduccion.py:99` declara
`EJES = ("escolaridad_proxy", "dominio_urbano_rural", "nacional")`; `marginal(ola, grupo)` lanza `ValueError`
para cualquier otro `grupo`, y las columnas `SEXO`/`EDAD` ni siquiera se cargan (`COLUMNAS_TMOD`, línea 101;
`COLUMNAS_TSDEM = ("ID_PER", "NIV")`, línea 103; `grep -ci sexo` → 0, `grep -ci edad` → 0 sobre 432 líneas). Los
4 pares del dictamen para ENVIPE 2025 son `dominio_urbano_rural × sexo` (6), `edad × escolaridad_proxy` (16),
`edad × sexo` (8) y `escolaridad_proxy × sexo` (8): **los cuatro llevan `sexo` o `edad`**, así que en ninguno se
puede obtener `p_k(a)` y `p_k(b)` por `marginal()` — una variable por llamada — como el método de la casa exige.

El encargo previó el caso celda por celda (P0: «si `marginal()` no admite alguno de los ejes […] no lo parches:
esa celda sale `IC-NO-CONSTRUIBLE` con causa, y el hueco es entregable»). Aquí el caso es total, 38 de 38, y
eso cambia la naturaleza de lo que se congelaría: una spec + medidor cuyo procedimiento no puede aplicarse a
ninguna celda es una spec degenerada por construcción, y congelarla a sabiendas para sellar 38 `IC-NO-CONSTRUIBLE`
quemaría `CALC-C2-COMPUESTO-IC-ENVIPE2025-0001` en una corrida que no mide nada. Regla de señal: el acto
produce medición o produce nada. Produce nada, y lo dice.

Lo que **no** se hizo y por qué, una línea cada uno:

- **No se extendió `EJES` a `sexo`/`edad`.** Fuera de perímetro («No toca `marginales_reproduccion.py`») y
  contra P0 verbatim («no lo parches»). Ese módulo es «el único código autorizado a tocar ENVIPE 2025» (docstring)
  y su guardia nació de `NC-0328` (reserva `edad × dominio` quemada por un script de scratch): ampliar los ejes
  admitidos es un cambio de contrato del guardián, no un detalle de implementación, y es de mesa.
- **No se derivaron `sexo`/`edad` en el medidor por fuera del módulo** (leyendo `tmod_vic` por cuenta propia
  y agrupando por una variable). Pasaría el AST-guard de una sola variable y aun así sería exactamente la clase
  de código que `NC-0328` prohíbe: una segunda lectura de la ola reservada fuera del guardián.
- **No se selló un CALC con 38 × `IC-NO-CONSTRUIBLE` + controles.** El único contenido medible que quedaba —
  que los marginales de la réplica base del módulo reproduzcan los R sellados del árbitro para los tres ejes que
  sí admite — **ya está sellado** en `CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001` (piloto 2, `ADR-542`):
  `RESULT-TRA-SXD12-G-CTRL-ARBITRO-VEREDICTO = REPRODUCE`, `DELTA-P-MAX 4.79e-07`, `DELTA-IC-MAX 4.70e-07`,
  `DELTA-N 0` en NAC/S1–S4/D1–D3. Volver a sellarlo no mueve nada.
- **No se abrió ningún payload.** El hallazgo es sobre el código, no sobre el dato; `data/raw` se enlazó para
  el A.2 y nada más. Cero contaminación adicional sobre la ola reservada.

## 1 · ARRANQUE (Bloque D) — salida cruda

| paso | comando | salida |
|---|---|---|
| 0.a | `git rev-list --count HEAD..origin/main` | `0` (base `a92126f` = SHA de redacción; nada que re-derivar) |
| 0.b | `git status --porcelain` | vacío (`git_status=LIMPIO(0)`) |
| 0.c | `git ls-remote --heads origin \| grep -i ic-envipe2025` · `git worktree list \| grep -i ic-envipe` · `gh pr list --state open` | 0 · 0 · 0 PR abiertos en total (6 heads remotos al abrir) |
| 0.c-bis | `git grep -l CALC-C2-COMPUESTO-IC-ENVIPE2025 <cada rama remota>` | 0 en las 6 ramas (`main`, `acto/gen2-pisos-enut2019-ejes-1`, 4× `claude/*`) → el id reservado está libre y **sigue libre al cierre** |
| 0.d | `python3 tools/limpia_arbol.py --reporta` | 159 worktrees vivos; base al día; 5 ramas remotas sin PR abierto (`fuera_de_politica`) |
| A.2 | `python3 tools/entorno.py --sonda-red` | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable` · `red=200` · `corpus=SI(examinados=419)` |
| 3 | `ln -s /home/pc0/mm-corpus/raw data/raw`; `data/raices.local.yaml` copiado del clon padre | enlazado (worktree nuevo nace sin ambos, no es PARO) |

## 2 · COMPUERTA — por producto

`git cat-file -e origin/main:data/corrida0/CALC-C2-COMPUESTO-RESERVADAS-0001/resultados.json` → existe; el
directorio trae `sello.json` y `sello.sha256`; merge `#889` = `e4ec384` (19/sep/2026). **Cumplida.**

## 3 · Verificación de existencia (contra `a92126f0`, re-derivada)

| afirmación del encargo | comando | salida |
|---|---|---|
| 38 celdas en 4 pares de ENVIPE 2025 | `awk -F'\t' 'NR>2 && $12=="ENVIPE 2025"{s+=$9} END{print s}' data/corrida0/c2-compuesto-dictamen-v1_0.tsv` | `38` (6+16+8+8; 4 filas, todas `EMITIBLE`; 25 `EMITIBLE` / 11 `NO-EMITIBLE` en total) |
| puntos ya sellados para esas 38 | `resultados.json` del CALC compuerta: claves `RESULT-C2COMP-EVADE-NORMA-ENVIPE2025-*` sin `-DIAG-` | `38`, 0 `null`; `N-CELDAS-CON-IC = 0`; `TIPO-INCERTIDUMBRE = NO-PROPAGADA-COVARIANZA-NO-SELLADA` |
| (2) `ls data/corrida0 \| grep -i "C2-COMPUESTO-IC"` | ídem | `0` de 183 CALC → NO-ENCONTRADO |
| ejes del árbitro para 2025 | `milpa/tramite-ola5-propuesta-v0.yaml:1672-1731` (`tramite.evasion_norma_ejes_envipe2025`) | `sexo` (2 celdas), `edad` (4), `escolaridad_proxy` (4), `dominio_urbano_rural` (3); «sexo y edad viven en tmod_vic y no necesitan el join» |
| ejes que el módulo admite | `sed -n 99p tools/celda_d/marginales_reproduccion.py` | `EJES = ("escolaridad_proxy", "dominio_urbano_rural", "nacional")` |
| pares cubiertos por el módulo | intersección de las dos filas anteriores | **0 de 4** (`escolaridad_proxy × dominio_urbano_rural` sí estaría cubierto, pero es el par del piloto 2 y no está entre los `RESERVADA`) |
| precedente de método (réplicas, semilla) | `data/corrida0/CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001/spec.yaml:102,140` | `seed 42`, `bootstrap_replicas: 10000`, `numpy.random.PCG64` — leído y citado; no usado |
| `edad × dominio` quemado | `grep NC-0328 forense/no-corrido.tsv` | `RESERVA-CONSUMIDA-SIN-PILOTO`; no está entre los 4 pares (dictamen), no se tocó |

## 4 · Lo que se deja a mesa (FP-390)

Tres caminos, sin que este acto elija:

1. **Acto propio que amplíe `tools/celda_d/marginales_reproduccion.py`** — `EJES` + `sexo`/`edad` (tramos
   `18-29/30-44/45-59/60+` con la MISMA construcción del árbitro, `tools/ejes_maestra35_l1.py`, importada),
   `COLUMNAS_TMOD` + `SEXO`/`EDAD`, `_orden()`, y un control de reproducción contra
   `tramite-ola5-propuesta-v0.yaml:1683-1704` (`sexo` en 1683, `edad` en 1693) para los dos ejes nuevos, congelado como código en su COMMIT-1
   sin abrir la ola. Después, relanzar este encargo tal cual (el id `CALC-C2-COMPUESTO-IC-ENVIPE2025-0001`
   sigue libre).
2. **Aceptar que las 38 celdas queden `NO-PROPAGADA-COVARIANZA-NO-SELLADA`** hasta que un piloto evalúe esos
   pares, y cerrar el sucesor de nube del marcador sin IC que tomar.
3. **Sellar un CALC de 38 × `IC-NO-CONSTRUIBLE`** con el id reservado, si mesa prefiere el hueco como corrida
   y no como NC — este acto no lo hizo por las razones de §0.

Aviso lateral, una línea, fuera de mi perímetro: `tools/celda_d/` contiene **un solo módulo y es de ENVIPE**;
el acto gemelo sobre ENIF 2024 (`acto/gen2-c2-compuesto-ic-enif2024-1`, 0-bis ya en origin) no tiene módulo
guardado que importar, salvo que su spec lo cree.

## 5 · Módulo de auditoría (afirma sobre México)

Nada cambia para el lector: las 38 celdas compuestas de ENVIPE 2025 siguen siendo pisos sin intervalo, y aun
con intervalo medirían ruido muestral de un estimador que supone no-interacción, no el error de ese supuesto.
Un IC estrecho no es una celda bien estimada; una celda sin IC no es una celda «sin validar» que un IC
arreglaría. La unidad es el delito declarado, no la persona; los ejes son marcadores de estructura.
