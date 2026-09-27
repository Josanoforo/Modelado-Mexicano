# GEN2-RECIBO-ASTRA6-N · recibo de los cuatro PR abiertos de MISION-ASTRA-6 (C2 ENVIPE · C2 ENCIG · C3 CONSUMO-FAMILIA · C2 ENIF)

Cero mediciones; no adopta; no mueve `cuenta_gen2`. Contadores movidos: 0.

`ADR-260926-GEN2-RECIBO-ASTRA6-N-996b-01` · 0-bis `996b2173` · NUBE (hook: `ENTORNO-DERIVADO = NUBE`, corpus no montado, 0 archivos examinados; red denegada por política). Cero microdato abierto. Base: `origin/main` `acf62514`, fusionada en la rama antes del 0-bis (62 commits de atraso, `git merge origin/main`). Encargo: `forense/encargos/2026-09-26-GEN2-RECIBO-ASTRA6-N.md` (sha256 `108b720e…2e05a7`, igual al adjunto recibido). SHA de redacción del encargo: `4f125e70`. Main se movió después; no es PARO, se re-derivó todo sobre `acf62514`.

## Veredicto por PR (para mesa)

| N | PR | carril | recomendación | por qué, en una línea |
|---|---|---|---|---|
| 3 | [#1170](https://github.com/Josanoforo/Modelado-Mexicano/pull/1170) ENVIPE | C2 | **DEVOLVER** | `check.py --baseline` sale **ROJO sobre el HEAD del PR**: 2 FAIL nuevos de T-REPRO 11.2, uno por cada `CALC-FAMILIA-2027-ENVIPE-*`. Su `sello.json` anidado (`tipo`, `archivos: {…}`) choca con `tools/corrida0.py:2842`, que recorre el sello como mapa plano archivo→sha (LEÍDO por esta sesión). El contenido estadístico cumple. |
| 4 | [#1172](https://github.com/Josanoforo/Modelado-Mexicano/pull/1172) ENCIG | C2 | **FUSIONAR-CON-NC** | Toda cifra trazada (12/12), 0 sellos reescritos, suite VERDE sobre el HEAD. Conflicto mecánico solo en `data/INFRAESTRUCTURA-v1_0.md`: los dos lados añadieron bloque. La enmienda de `evaluar.py`/`cierre.py` posterior a COMMIT-2 queda sin hash en el inventario → NC. |
| 5 | [#1173](https://github.com/Josanoforo/Modelado-Mexicano/pull/1173) CONSUMO-FAMILIA | C3 | **DEVOLVER** | Falla el criterio central del carril, el dictamen razonado por afirmación. 93 filas de consumo se dictaminan por plantilla de rango de línea o heredan el dictamen (`consumo-genera.py:98-114`, LEÍDO por esta sesión). 5 de 6 ROMPE de familia sin RESULT. La muestra de 10 da 1 FALLA (CONS-V1-L086: SIN-CIFRA cuando el RESULT existe). HEAD rojo en T02; el merge local queda VERDE. |
| 6 | [#1174](https://github.com/Josanoforo/Modelado-Mexicano/pull/1174) ENIF | C2 | **FUSIONAR-CON-NC** | Merge limpio y `check.py --baseline` VERDE sobre la vista previa. 41/41 cifras re-derivadas; COMMIT-1 → COMMIT-2 en los dos pares. ORO-0001 → ORO-0002 declarado como ejecución previa descartada por el conducto (no emitió valores; procedimiento y semilla intactos). NC: 3 `.pyc` en el inventario de sellos, auditoría de pathlib, frase N/M/K tecleada. |

Números de N: propuestos por dirección en esta sesión y aceptados por mesa al decir «Arranca»: 1 = #1166 (C1), 2 = #1171 (C3-SOCIAL), 3–6 = esta tabla. Lote D-11: cuatro piezas del mismo entorno, un PR y un ADR (INTERPRETACIÓN-DECLARADA: el encargo es una plantilla «una instancia por PR»; los cuatro PR abiertos se reciben en un solo acto, con veredicto separado por PR).

### Condiciones exactas para volver a recibir

**#1170 (DEVOLVER):**
1. Suite sin FAIL nuevos: el sello de las emisiones debe ser el mapa plano que lee `corrida0._verifica_sello`, o vivir fuera de `data/corrida0/`. Re-sellar en commit nuevo, declarado; el sello viejo queda VENCIDO EN ALCANCE, nunca editado.
2. Resolver el conflicto en `tests/check.py` (línea `nombre_indice` de T02) y adjuntar `check.py --baseline` VERDE sobre el merge.
3. `forense/replay-evidencia.tsv:335-336` usa REPRODUCE con `corrida_id` NO-APLICABLE y un contexto fuera de E.3, sin que salga de `corrida0 verify` (que da NO-EJECUTABLE): retirar o re-asentar con vocabulario E.3.
4. `cierre.py --verifica` exige numpy 2.3.5, que `requirements.txt` no fija.

**#1173 (DEVOLVER):**
1. Reclasificar las 5 ROMPE de familia sin RESULT (`familia-afirmaciones.json:488, :1017, :2005, :2027, :2069`).
2. Dictaminar una por una las 93 filas de consumo con plantilla o dictamen heredado, corrigiendo CONS-V1-L086 y CONS-024.
3. Productor por comando para familia y para el índice local.
4. Rutas rotas: `canon/L0/ADR-…-edf7-01.md:3` cita un `indice.md` que no existe; `data/INFRAESTRUCTURA-v1_0.md:1020` cita rutas `{consumo,familia}/afirmaciones.json` que no son las reales.
5. Auditoría rotulada con las preguntas [v2.16] (la sustancia está; el lote hermano SOCIAL sí las rotula).
6. Traer origin/main y adjuntar `check.py --baseline` VERDE (3 FAIL T02 en el HEAD).

**#1172 y #1174 (FUSIONAR-CON-NC):** resolver el conflicto de `INFRAESTRUCTURA` conservando ambos bloques (solo #1172; #1174 fusiona limpio) y asentar las NC de abajo. Ninguna bloquea el merge.

## Criterios usados

La plantilla `GEN2-RECIBO-ASTRA-PRODUCTO-N` que cita el encargo (`6773bbcdf2ada478`) **no está en el repo**:
```
$ git ls-tree -r --name-only origin/main | grep -ciE 'RECIBO-ASTRA-PRODUCTO'
0
```
Tampoco en `forense/encargos/fuentes/TRANSFER-ASTRA-2026-09-23.md`, que solo cita el circuito `GEN2-RECIBO-ASTRA-N`. Se redactaron los seis criterios comunes K1–K6 desde la línea 4 del encargo, la sección «Recibo» de la MISION (`MISION-ASTRA-6-integridad-y-frontera.md:59-60`) y la ADENDA-1, rotulados **PROPUESTO-POR-EJECUTOR** (cláusula de autonomía, punto 3): `2026-09-26-GEN2-RECIBO-ASTRA6-N/criterios-PROPUESTO-POR-EJECUTOR.md`. Donde la MISION pide acreditar ceguera con `git log -p -S` y la ADENDA-1 pide separación, manda la ADENDA-1 («donde chocan, manda esta adenda»).

Adjuntos archivados en el 0-bis, con su lista de sha (nació como `SHA256SUMS.txt` en `996b2173`; renombrada a `ASTRA6-mision-SHA256SUMS.txt` en el commit de cierre porque T02 la hacía chocar por nombre con la de `ASTRA6-lanzamiento-20260926/`; contenido intacto), en `forense/encargos/fuentes/ASTRA6-mision-20260926/`: MISION `ecd8cf1b…` y ADENDA-1 `6d678178…` (los dos casan con los sha declarados en los encargos ASTRA6), PROPUESTA `2e943c8d…` y TRANSFER del 26/sep `7222341f…` (sin sha previo contra el cual comparar).

## Cómo se hizo

Cuatro subagentes, uno por PR (regla de lectura: lote de ≥ 3 piezas). Cada uno trabajó en un worktree desechable, retirado al cerrar, con solo lectura: ninguno escribió en la rama de Astra ni comentó en GitHub. Sus informes, con comando y salida por criterio y la distinción EJECUTADO/LEÍDO por frase, van como anexos: `2026-09-26-GEN2-RECIBO-ASTRA6-N/pr-{1170,1172,1173,1174}.md`. Esta sesión re-verificó por su cuenta los tres puntos que deciden un DEVOLVER o un criterio duro:
- T-REPRO de #1170: forma del `sello.json` (`git show recibo-pr-1170:data/corrida0/CALC-FAMILIA-2027-ENVIPE-DENUNCIA-U4/sello.json`) contra `tools/corrida0.py:2830-2846`.
- Plantilla de #1173: `consumo-genera.py:98-114` y la fila CONS-V1-L086 por `jq`.
- ENIF 2024 en #1174 como oro: `data/manifiesto.yaml:5595` (id `enif_2024_enif_2024_bd_csv`, 1 entrada examinada) no trae marca de reserva. Ya la leyeron el lote ENIF2024 y el paquete AMAI de C1. Usarla como oro de calibración es «cruce visto sirve para calibrar» (E.6).

Identidades (HEAD del PR · merge-base · `git merge-tree --write-tree origin/main`):
- #1170 `c3593116` · `2c646cba` · conflicto (`tests/check.py`)
- #1172 `e45dca29` · `2c646cba` · conflicto (`data/INFRAESTRUCTURA-v1_0.md`)
- #1173 `8971116c` · `2c646cba` · conflicto (`data/INFRAESTRUCTURA-v1_0.md`)
- #1174 `722cdb51` · `948f024a` · limpio

## Hallazgos que cruzan PR (para quien diseñe el siguiente acto)

- **Specs FAMILIA-2027 sin módulo de auditoría [v2.16] ni etiqueta (a)/(b)/(c):** 0 de 12 lo traen, según el informe de #1174. Es herencia de v1.2, no defecto de un PR. En ENIF falta además la medida de exclusión por oferta junto a marginales de ahorro (§3, «oferta antes que preferencia»).
- **Frase de producto N/M/K tecleada** en `cierre.py` de ENCIG (`:82`) y de ENIF (`:135`). Los valores son correctos al re-derivarlos, pero no se derivan por comando.
- **`corrida0 verify` emite `VALOR-REF-FUERA-DE-TABLAS` en falso** en ENCIG y ENIF (`tools/corrida0.py:3013`, `d=None`). Es de tubería, fuera de los PR.
- **#1170: la búsqueda del calendario ENVIPE devolvió de rebote extractos de noticias de resultados ENVIPE 2026** (`calendario.md:22` del PR), que es una ola RESERVADA. E.6 prohíbe leer comunicados de una ola reservada. No toca las emisiones 2027; sí toca la ceguera de quien compita sobre 2026. Va a mesa.
- **T02 de `check.py`:** #1170 y #1174 lo editan para admitir `recibo-para-claude.md` y `medidor.py` repetidos por nombre. Una excepción genérica por ruta ahorraría la edición en cada recibo.
- **#1171 (C3-SOCIAL) se fusionó sin recibo** (merged 26/sep 20:49Z). R(a) de FIRMAS-15 lo exige. Queda como NC para el siguiente N.
- **#1166 (C1)** tiene `/revisa --post-hoc` (FUSIONABLE-CON-RESERVA, 0 BLOQUEA · 4 RESERVA) en `forense/notas/2026-09-26-revisa-post-hoc-1166.md`, pero no el recibo con los criterios C1 de este encargo.

## NC abiertas por este acto

Las NC que Astra no abrió van a `forense/no-corrido.tsv`, agrupadas por causa, no una por fila (A.14 · una causa, una fila). Las NC internas de cada PR (#1170: 7 · #1172: 3 · #1173: 6 · #1174: 7) están en los anexos. Aquí se asientan las que tienen sucesor fuera del PR o gatean el merge:

| id | qué | razón | sucesor |
|---|---|---|---|
| NC-…-996b-01 | #1170 · suite ROJA (T-REPRO) y replay fuera de E.3 | DIFERIDO-A:ASTRA6-C2-ENVIPE-1 (corrección) | ASTRA6-C2-ENVIPE-1 |
| NC-…-996b-02 | #1173 · dictamen por plantilla, 5 ROMPE sin RESULT, rutas rotas, auditoría sin [v2.16] | DIFERIDO-A:ASTRA6-C3-CONSUMO-FAMILIA-1 (corrección) | ASTRA6-C3-CONSUMO-FAMILIA-1 |
| NC-…-996b-03 | #1172 · enmienda de `evaluar.py`/`cierre.py` posterior a COMMIT-2 sin hash en `inventario-sellos.json`, y «hecho» CAJA no re-verificado sobre el commit fusionado | DIFERIDO-A:FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-02 | acto de manifiesto de sellos/OTS + sesión CAJA post-merge |
| NC-…-996b-04 | #1174 · 3 `__pycache__/*.pyc` en `inventario-sellos.json` (falla en clon limpio); auditoría no cubre pathlib en el lector v2/medidor ORO-0002; contrato v2 no declarado como gobernante del COMMIT-3 | DIFERIDO-A:COMMIT-3 ENIF 2027 | acto COMMIT-3 ENIF |
| NC-…-996b-05 | Serie de specs FAMILIA-2027 sin módulo [v2.16], (a)/(b)/(c) ni medida de oferta | DECISIÓN-DE-MESA-PENDIENTE | FP-…-996b-01 |
| NC-…-996b-06 | #1170 · exposición de rebote a noticias de resultados ENVIPE 2026 (ola reservada) al buscar calendario | DECISIÓN-DE-MESA-PENDIENTE | FP-…-996b-01 |
| NC-…-996b-07 | Recibo de #1166 (C1, criterios C1) y de #1171 (C3-SOCIAL, fusionado sin recibo) | DIFERIDO-A:GEN2-RECIBO-ASTRA6-N (N=1, N=2) | siguiente instancia del recibo |
| NC-…-996b-08 | `corrida0 verify` · `VALOR-REF-FUERA-DE-TABLAS` espurio (`tools/corrida0.py:3013`) | FUERA-DE-PERÍMETRO: de un acto de TUBERÍA (corrida0) | acto TUBERÍA sobre `tools/corrida0.py` (por abrir en mesa) |

## Firma pendiente para mesa

`FP-260926-GEN2-RECIBO-ASTRA6-N-996b-01` · qué: recibir los cuatro PR según la tabla (#1172 y #1174 FUSIONAR-CON-NC; #1170 y #1173 DEVOLVER con la lista exacta de arriba) y decidir dos cosas: (i) si §5 v2.16 (módulo de auditoría, (a)/(b)/(c), medida de oferta) aplica a la serie de specs FAMILIA-2027 (recomendación: sí, en la v1.4, antes de cualquier COMMIT-3); (ii) qué hacer con la exposición de #1170 a noticias de ENVIPE 2026 (recomendación: declararla en la nota de ENVIPE 2026 como lectura incidental de comunicado, sin reabrir nada, porque las emisiones 2027 no dependen de ella). Alternativa: FUSIONAR-CON-NC también #1170 tras corregir la suite y el conflicto, que son mecánicos. No se recomienda fusionar un PR que deja la suite roja.

Texto de firma listo: «Recibo ASTRA6 N=3..6: fusiono #1172 y #1174 con sus NC; devuelvo #1170 y #1173 con la lista de la nota; §5 aplica a FAMILIA-2027 desde v1.4; la exposición ENVIPE 2026 se declara incidental.»

## Módulo de auditoría (aplica solo a lo que el recibo afirma sobre México)

Cero contadores movidos. Toda cifra de esta nota es un conteo sobre el repo (filas, archivos, commits), con su comando en los anexos; ninguna es una cifra sobre México. PROSPECTIVA/RETROSPECTIVA: las emisiones C2 son PROSPECTIVAS (selladas antes de que exista la R de 2027), y esta nota no las mezcla con nada retrospectivo. Escala y unidad: las cifras de los reports de #1173 que la muestra re-verificó son de unidad hogar (ENIGH) y no se promedian con otras.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| «check.py --baseline VERDE sobre la rama fusionada localmente» para #1170, #1172 y #1173 | NO-VERIFICABLE-AQUÍ: los tres chocan con origin/main. #1172 y #1173 se resolvieron por union en local (#1173: VERDE). #1170 y #1172 se midieron sobre su HEAD (#1170 ROJO, #1172 VERDE). Resolver un conflicto de la rama de Astra es editarla (PARO b). | El VERDE de #1172 es sobre el HEAD, no sobre el merge. | Astra, al resolver el conflicto |
| Replay de oro y firma CAJA de los CALC de #1170, #1172 y #1174 | NO-VERIFICABLE-AQUÍ: NUBE sin microdato. `verify` da INPUT AUSENTE o NO-EJECUTABLE. | El oro se LEYÓ de `ejecucion.json`/`oro.json`, no se re-ejecutó. | sesión CAJA post-merge (NC-…-996b-03) |
| Citas externas de los reports de #1173 | NO-VERIFICABLE-AQUÍ: red denegada por política (EGRESS_BLOCKED). | La trazabilidad de literatura se verificó por forma, no por contenido de la fuente. | siguiente recibo C3 |
| Plantilla GEN2-RECIBO-ASTRA-PRODUCTO-N | SUSTITUIDO-POR:criterios K1–K6 PROPUESTO-POR-EJECUTOR (absorbe los seis criterios comunes nombrados en el encargo; queda huérfano cualquier criterio de la plantilla que no esté en esa lista) | Si la plantilla aparece, la diferencia se declara. | mesa / dirección |
| Recibo de #1166 y #1171 (N=1, N=2) | DIFERIDO-A:GEN2-RECIBO-ASTRA6-N (siguiente instancia; D-11 limita el lote a cuatro piezas) | #1171 sigue en main sin recibo (R(a)). | NC-…-996b-07 |
