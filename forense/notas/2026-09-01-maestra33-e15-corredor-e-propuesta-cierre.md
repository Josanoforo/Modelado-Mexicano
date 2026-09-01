# Cierre · `ACTO MAESTRA33-E15 · CORREDOR-E-PROPUESTA`, 1/sep/2026

Encargo: `forense/encargos/2026-09-01-MAESTRA33-E15-CORREDOR-E-PROPUESTA.md`
(dirección, maestra-33, formato corto v2.12, archivado por A.3 antes de
ejecutar; `SHA de redacción ee6a8a2`). Ejecutado con la skill `/acto`
(`ADR-237`, D-10) en entorno **NUBE** (`cloud_default`).

## ARRANQUE

1. **Repo.** Clon existente, `/home/user/Modelado-Mexicano`, rama
   `claude/propuesta-operativa-e-gshsnh`. `git log -1` al arrancar:
   `ee6a8a2 Merge pull request #436 from
   Josanoforo/acto/maestra33-c6-arbitra-r-lote-3`. `git status`: limpio.
2. **SHA.** `origin/main` al arrancar = `ee6a8a2` = `SHA de redacción`
   declarado por el encargo, literal. Sin drift, sin refresco necesario.
3. **`data/raw`.** Ausente — raíz gitignorada, no enlazada en este
   contenedor (`ls data/raw/` → directorio inexistente). Este acto no
   abre microdato: perímetro es `notas`, `prereg-duelo-v2` (propuesta +
   cargador sin correr) y tablero.
4. **Entorno**, tres partes (A.2): `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`
   = `cloud_default` (no `sin_variable`; desviación repetida ya vista en
   actos previos de esta serie, sin consecuencia — el acto no toca
   microdato ni corre corredores). Sonda de red,
   `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10
   https://www.inegi.org.mx/` → `000` (CONNECT rechazado por política de
   la organización del proxy de egreso; comando examinó 0 archivos —
   negativo declarado por A.13, no aplica al perímetro de este acto,
   que no abre red). Tercera parte, `ls data/raw/ 2>/dev/null | head -1`
   → vacío, corpus compartido no montado (esperado en la nube).
5. **Espejo.** No consultado; toda cifra de este cierre sale del clon de
   (1), comandos citados abajo.

## COMPUERTA

`COMPUERTA: E13 fusionado.` `E13` = `ACTO MAESTRA32-E13 ·
MARCO-M-CONGELA` (`forense/encargos/2026-08-31-MAESTRA32-E13-MARCO-M-
CONGELA.md`), fusionado en `PR #403` (commit de merge `f4d9b7f`).
Verificación mecánica:

```
$ git fetch origin main
$ git merge-base --is-ancestor f4d9b7f origin/main && echo CUMPLE
CUMPLE
```

`f4d9b7f` es ancestro de `origin/main` (`ee6a8a2`) — **CUMPLE**.
Continúa al P1.

## P1 · Conteo del criterio de activación de `E`

Criterio sellado en `canon/motor-nucleo-medible-v1_0.md` §3(b) (`ACTO
MAESTRA33-E11`, líneas 191-198), dos condiciones simultáneas:

1. `L` y `M` con puntos en ≥8 celdas comunes del marco-M
   (`marco-M-sorteado-v1_1.tsv`).
2. Scoring v1_1 sellado.

**Condición 2 — CUMPLE.** `ACTO MAESTRA33-E12 · SELLA-1` (`PR #435`)
selló `procedimiento-scoring-v1_1.md` con la firma de mesa `[sello
scoring v1_1 — cinco decisiones]` (verificado: el archivo existe,
`sha256` presente en cabecera, `mesa-pendientes.md` §S5 firmada).

**Condición 1 — NO CUMPLE.** Derivación mecánica del conteo real de
`corridas-L ∩ corridas-M` con puntos en ambos, sobre las 11 celdas de
`marco-M-sorteado-v1_1.tsv`:

```
$ cut -f1 forense/prereg-duelo-v2/marco-M-sorteado-v1_1.tsv | tail -n +2
CIV-M-01  CIV-M-06  CIV-M-08  CIV-M-09  CIV-M-11  CIV-M-12  CIV-M-13
FAM-M-01  TRA-M-03  TRA-M-05  TRA-M-07
(11 celdas)

$ ls forense/prereg-duelo-v2/corridas-L/ | sed 's/__.*//' | sort -u
CIV-08  DIN-03  DIN-05  DIN-07  DIN-11  DOC-06  EMP-02  EMP-04  EMP-05
SFT-04  SFT-06  TIC-01  TIC-06  TIC-08  TIC-12
(15 ids únicos, 120 archivos — todos del marco piloto de
`pipeline-L-adv1-m2.py`, ninguno de `marco-M-sorteado-v1_1.tsv`; mismo
hallazgo ya declarado por `ACTO MAESTRA33-E9` §4)

$ python3 -c "
import json, glob
L_ids = set(fn.split('/')[-1].split('__')[0]
            for fn in glob.glob('forense/prereg-duelo-v2/corridas-L/*.json'))
M_emite = set()
for fn in glob.glob('forense/prereg-duelo-v2/corridas-M/M-*.json'):
    d = json.load(open(fn))
    if d.get('estado_M') == 'EMITE':
        M_emite.add(d['id_celda'])
print('L ids:', len(L_ids), '| M EMITE:', len(M_emite))
print('interseccion (puntos en ambos):', sorted(L_ids & M_emite))
"
L ids: 15 | M EMITE: 13
interseccion (puntos en ambos): []
```

`corridas-M/` trae 30 archivos: 28 celdas con `id_celda` derivable
(2 archivos no son celdas — `_intento-scoring-v1_1`, script auxiliar
`intento_scoring_e9.py`, excluidos del conteo). De esas 28, 13 tienen
`estado_M: EMITE` (punto real) y coinciden exactamente con las 11 celdas
de `marco-M-sorteado-v1_1.tsv` más `CIV-M-01`/`TRA-M-03` ya cubiertas —
i.e., las 13 celdas `EMITE` son un superconjunto de las 11 del marco
v1_1 (verificado por inspección: `CIV-M-01,06,08,09,11,12,13,FAM-M-01,
TRA-M-01,02,03,05,07` ⊇ `marco-M-sorteado-v1_1`). Las 15 restantes de
`corridas-M/` tienen `estado_M: NO-EMITE` (sin regla `CANDIDATO-EMITE`
en pasada 1 — no son "puntos", son abstenciones declaradas).

`corridas-L/` (120 archivos, 15 ids) corre exclusivamente sobre el
marco piloto (`CIV-08`, `DIN-03`… — los mismos ids que `ACTO
MAESTRA33-E9` §4 ya señaló como *0 archivos del marco-M* al 1/sep).
Ninguno de esos 15 ids aparece en `marco-M-sorteado-v1_1.tsv` ni en el
conjunto `M-EMITE`.

**Intersección de celdas con puntos en `L` y `M` a la vez: 0.**
Requerido: ≥8. **El criterio no se cumple** — no por falta de scoring
sellado (eso ya está), sino porque no existe *ninguna* corrida `L`
todavía sobre las celdas donde `M` sí emite punto (`FP-219`,
`L-CORRIDA-v1_1`, sigue `ABIERTA`, vence `2026-09-04` — es la pieza que
falta para que la condición 1 tenga siquiera oportunidad de leerse).

Conforme al encargo ("Si no se cumple: lo dice con el conteo y cierra"),
**este acto no redacta la propuesta operativa de `E`** pedida
condicionalmente en P1 — no hay base (0 celdas comunes con puntos) para
que esa propuesta tenga contenido que evaluar. Se cierra con el conteo
de arriba.

## P2 · `FP-221` → resuelta con este acto

`FP-221` (`REVISION-CORREDOR-E`, dirección, `vence: 2026-09-30`) pedía
la revisión del criterio de activación de `E` "al publicarse el
agregado... o el 30/sep, lo que ocurra primero" (firma 10). Este acto
*es* esa revisión — corre antes del vencimiento, con el conteo mecánico
de arriba como resultado: **criterio no cumplido, 0 de 8 celdas
comunes**. `forense/firmas-pendientes.tsv` columna `estado` de `FP-221`
pasa de `ABIERTA` a `RESUELTA`, con fecha real `1/sep/2026` (no la
fecha límite `30/sep`) y esta nota como recibo.

## CONTADOR

Cero — ningún corredor corrido (`L`, `M`, `R`, `E`), ningún microdato
abierto (declarado en ARRANQUE-3). El único cómputo de este acto es el
conteo de intersección de arriba, sobre archivos ya existentes en el
repo (`corridas-L/`, `corridas-M/`), sin invocar ningún LLM ni pipeline.

## Perímetro tocado

`forense/firmas-pendientes.tsv` (`FP-221` → `RESUELTA`), esta nota,
`forense/encargos/2026-09-01-MAESTRA33-E15-CORREDOR-E-PROPUESTA.md`
(A.3 + `## CONSUMIDO`), cascada (`ADR` nuevo, `canon/gobernanza-v1_15.md`
§4, `canon/estado-programa-v1_10.md` L0, `canon/registro-rotulos.tsv`).
No se tocó `prereg-duelo-v2/` más allá de lectura (`ls`, `cut`, lectura
de `.json` para el conteo) — no se creó propuesta ni cargador porque la
condición que los habría pedido (P1, "si el criterio se cumple") no se
cumplió.
