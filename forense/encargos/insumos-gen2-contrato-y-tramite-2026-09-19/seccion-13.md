
## 13 · GEN2 · 14–17 de septiembre — el estimador es de la celda (sección nueva, dirección, 17/sep/2026)

Retrata, no opina. Cada afirmación trae comando o cita de nota sellada; nada tecleado. Derivado contra `origin/main = 9eff694` (merge de `PR #860`, 17/sep/2026 15:22 −06:00).

**Status completo, íntegro de `python3 tools/corrida0.py status` (17/sep, `9eff694`):**

```
N_corridas_requeridas=83
N_corridas_selladas=82
N_resultados_activos=208
N_resultados_sellados=5006
N_resultados_pendientes=208
dependencias_numericas_legacy_activas=184
N_resultados_gen2_sellados=4405
N_resultados_gen2_pendientes_adopcion=12
N_resultados_gen2_vetados_por_decision=2
N_resultados_gen2_adoptados_activos=24
resultados_con_validacion_independiente=215
diferencias_materiales=0
no_corrido_abiertas=109
replays_legacy_sellados=5
corredores_envueltos_legacy=22
```

**La cifra cabecera y la cifra en disco son dos cifras, y hoy difieren en dieciséis.** `N_corridas_selladas=82` cuenta filas de la vista publicada `data/corrida0/corridas.tsv`, no sellos en disco (`tools/corrida0.py:4282`). En disco hay 120 `CALC-*`, 115 con `sello.json`, y **16 sellados sin fila en la vista** (`for d in data/corrida0/CALC-*/; do …; done` → 16). La vista no se puede escribir: `registro --escribe` re-proyecta el replay de todas las corridas desde `forense/replay-evidencia.tsv` (77 asientos) y **24 corridas publicadas con `REPRODUCE` no tienen asiento**, así que la proyección las degradaría y el guardia `REPLAY-PISADO` (`NC-0094`) se niega — bien negado (`ADR-540`, `forense/notas/nota-2026-09-17-gen2-registro-caja-1.md` §P2; reproducido por `ADR-542` §5). Las 14 corridas de esa nota verifican en caja (13 `REPRODUCE` limpio); ninguna entró. Sucesor nombrado: `GEN2-REPLAY-ASIENTOS-1` (caja: asentar 40 = 16 + 24, escribir una vez). Hasta entonces, **82 es un número de la vista, no del programa**; el CONTADOR de cada acto lo dice desde `ADR-540` ("sellada en disco, no registrada").

**`N_resultados_pendientes = N_resultados_activos` por construcción.** Las filas DEMANDA nacen `PENDIENTE` (`tools/corrida0.py:3757`, `:243`) y no existe transición que las saque (`grep "SATISFECH\|ATENDID\|CUBIERT" tools/corrida0.py` → 0 sobre 1 archivo). Es una constante disfrazada de contador; se registró como NC de aparato en `ADR-534` (`GEN2-TRAMITE-4`, P3). La lectura real de "qué falta" está en `data/corrida0/relevo-usos-v1_0.tsv` (153 `SIN-CANDIDATO`, 12 `CANDIDATO-GEN2`), no en ese contador.

**Régimen de estimación: M1 precisada, no revocada.** `ADR-531` (16/sep, `PR #822`, firma de mesa rama B, verbatim en `data/corrida0/decisiones.tsv` objeto `M1:ADR-91`): el cómputo matricial (`ADR-91`, 17/ago) es la forma de **composición** del ejecutable, no el estimador de ninguna celda; la estimación de cada insumo la gobierna el contrato celda-D (`ADR-68`) y la matriz compite en él como candidato, nunca por defecto. `milpa/src/matriz.py::g()` dejó de recorrer toda `B` antes de emitir: `SinMagnitud` solo para los generadores pedidos (`ADR-531`, P3). La ley E0 ("no calibra") quedó `VENCIDA EN ALCANCE` por `F-18` (`ADR-529`); la capa E1 la sustituye (abajo).

**Dos pilotos celda-D con cadena GEN2 completa, y el mismo veredicto.** `ADR-538` (`PR #849`, DIN: `ahorra_solo_informal` × `localidad × edad`, ENIF 2021→2024, 8 celdas) y `ADR-542` (`PR #858`, TRA: `evade_norma` × `escolaridad_proxy × dominio`, ENVIPE anual, 12 celdas). Tres commits en orden en los dos (spec sin microdato → emisiones selladas → R del cruce), reserva de evaluación intacta en los dos, control de reproducción contra los marginales sellados en los dos (`|Δp| ≤ 4.8e-07`). Veredicto: **`SIN-CANDIDATO-SUPERIOR`** en ambos; `champion_actual: NINGUNO`; nada adoptado. MAE en puntos porcentuales, citado de las notas de cierre (`forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md` §2; `…-PILOTO-2-cierre.md` §2.1):

| candidato | DIN (8 celdas) | TRA (12 celdas) |
|---|---|---|
| marginales públicos de la misma ola, sin interacción (`C2`) | **1.47** | **1.57** |
| persistencia del cruce de la ola anterior (`C1`) | 2.64 | 4.31 |
| `C2` + interacción de la ola anterior (`C6`) | — | 2.85 |
| `C2` + interacción promediada de dos olas (`C7`) | — | 2.67 |
| L-solo (`C3`, elicitación) | 10.64 | no entró (firma `FP-385`) |
| emisor nacional, x = ∅ (`C5`, diagnóstico) | 2.3–13.4 | 0–13 |

Lo que dice y lo que no (H5, declarado en las dos specs antes de correr): un piso no vencido acota a los **retadores**, no al fenómeno. Lo que sí quedó medido: en TRA las interacciones por celda son inestables entre olas (4/12 `I₂₄` y 5/12 `I₂₃` con IC que excluye 0; una cambia de signo), y añadirlas al piso marginal lo empeora. Reservas: `localidad × edad` (ENIF 2024) consumida limpiamente; `edad × dominio` (ENVIPE 2025) **consumida sin piloto** por un script exploratorio antes de COMMIT-1 (`NC-0328`, sin números en el canon); `escolaridad × dominio` (ENVIPE 2025) consumida por el piloto 2 con guardia estructural (`marginal(ola, grupo: str)`, `tests/test_marginales_una_variable.py`).

**El emisor es el árbitro.** `ADR-536` (`PR #844`, `GEN2-EMISOR-ESTADO-1`): censo celda por celda, **89 de 97 celdas del emisor son copia verbatim del árbitro** (`milpa/tramite.yaml`, 12 líneas `origen: … copiada verbatim`; 5 sin contraparte; 3 "independientes" por descarte sobre el mismo payload). `FP-383` (firmada 17/sep, `decisiones.tsv` objeto `marcador:emisor-fuera`): las celdas IDÉNTICO salen de la comparación M-vs-R; el emisor queda fuera del marcador por segmento; el marcador se rediseña sobre el catálogo de momentos (estimadores adjudicados por celda-D contra R). Las 15 salidas `conducta_p_medido` sin `escala` la tienen declarada desde ese acto.

**Ejes: por primera vez uno es EQUIVALENTE.** `data/crosswalk-ejes-arbitro-modelo-v1_0.tsv` (`ADR-530`, firmado `FP-376`): 1 `EQUIVALENTE` (`edad`, tras `ADR-537` — `CORTES_C1.edad = 18-29/30-44/45-59/60+`, que deja de citar `FP-53`, firmada desde el 18/ago para otro objeto), 2 `MAPEO-N-A-1` (`localidad`, `formalidad` — y `formalidad` **no** es identidad: el árbitro corta por ENIF `P3_13` sobre quien trabaja; F-17 enmendada), 1 `NO-EQUIVALENTE` (`dominio`, sin mapeo construible), 11 `SIN-CORRESPONDENCIA`. Con `edad`, 16 celdas del árbitro tienen por primera vez celda del modelo.

**Capa E1: 43 θ con estado legible por máquina, cero identificadas.** `milpa/theta-esquema-e1-v1_0.yaml` (`ADR-535`): `identificacion` — 24 `AUSENCIA_DE_FACTO(censo E1 §3)` (token propio, `NC-0293` cerrada), 8 `AUSENCIA_DECLARADA(A-bis 1/2)`, 4 `ASOCIACION-MEDIDA·*`, **0** `ARGUMENTO_EXPLICITO`; `dispersion:` con las 15 familias `NO-DECLARADA` (enmienda a E1 §4.4: son 15 familias, no 90 parámetros). `tests/test_theta_esquema_e1.py` falla el día que una θ alcance `ARGUMENTO_EXPLICITO`, para que se vea.

**Catálogo de momentos.** `milpa/catalogo-momentos-v0_1.tsv`: 2 `DERIVADO-Y-SELLADO-GEN2` (`M05`, y la fila del piloto 1), 21 `NO-VERIFICADO` (`awk -F'\t' 'NR>1{print $10}' … | sort | uniq -c`). Celdas-D registradas: **5** (`ls data/curacion-registro/celdas-d/*.yaml | wc -l`; las tres G5 de agosto sin evaluación, más las dos de los pilotos, adjudicadas).

**Aparato.** T16 dejó de asertar el total de WARN y `--baseline` adjudica solo por FAIL (`ADR-539`, `PR #854`): antes de eso, cada merge movía la cifra y costó tres renumeraciones en una noche y un PARO de rutina (`forense/rutinas.tsv`, 17/sep). Cuatro guardias corregidas y dos tests cableados en CI (`ADR-543`, `PR #860`). Dos recibos en lote del carril Codex (`ADR-534`: `#824–#831`; `ADR-541`: `#832–#843`), que por diseño no escribe tablero ni ADR; sin recibo al corte: `#851–#853` (rutinas) y `#855`. `TRÁMITE-4` corrió en **dos sesiones** del mismo entorno (`#845` cerrado sin aporte, `#848` fusionado) — `PARA-v2.14`, `hallazgos.md:863`. Firmas: **0 FP `ABIERTA`** de 385; `FP-374` `VENCIDA-EN-ALCANCE` por su propia premisa (7 → 2 → 0 familias elegibles; F6 en espera de acreditación de R09, `NC-0161/0162` en ESPERA). NC: 109 `ABIERTA` de 332 (era 64 el 16/sep: los recibos abren una por pieza que Codex deja a mesa); 15 con sucesor `SIN-ASIGNAR`; 11 rotuladas decisión de mesa, 4 de ellas de la bandeja del titular (`NC-0151/0153/0156/0185`, identidad humana).

**Rutinas.** `/deriva` entrega a diario (`data/curacion-universo/derivados/universo-2026-09-17.json`); el digesto entregó el 16 y el 17 (`forense/digesto/DIGESTO-2026-09-17.md`); la huella `PARO:suite inestable` del 17/sep en `forense/rutinas.tsv` **no tiene enmienda** "resuelto por `ADR-539`" (`grep -c "ADR-539" forense/rutinas.tsv` → 0): pendiente de trámite. El despacho registró `CANDADO` por ramas no exentas que ya no existen.

**Tabla afirmación → comando/cita, de esta sección:**

| Afirmación | Comando / cita |
|---|---|
| Status completo (bloque de arriba) | `python3 tools/corrida0.py status` |
| 16 CALC sellados sin fila; 24 publicados sin asiento | `for d in data/corrida0/CALC-*/; …` (16); cruce `corridas.tsv` × `forense/replay-evidencia.tsv` (24); `ADR-540` §P2 |
| `N_resultados_pendientes` constante | `tools/corrida0.py:3757`, `:243`; `ADR-534` P3 |
| M1 precisada, `g()` por generador | `ADR-531`; `decisiones.tsv` objeto `M1:ADR-91`; `milpa/src/matriz.py` |
| Pilotos: veredictos y MAE | `forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md` §2; `…2026-09-17-GEN2-CELDA-D-PILOTO-2-cierre.md` §2.1 |
| Emisor = árbitro, 89/97 | `ADR-536`; `grep -c "copiada verbatim" milpa/tramite.yaml` → 12 |
| Crosswalk: 1/2/1/11 | `awk -F'\t' 'NR>1{print $12}' data/crosswalk-ejes-arbitro-modelo-v1_0.tsv \| sort \| uniq -c` |
| Capa E1: 24/8/4/0 | `python3 -c "import yaml…"` sobre `milpa/theta-esquema-e1-v1_0.yaml`, campo `identificacion` |
| Catálogo 2/21; celdas-D 5 | `awk` sobre `milpa/catalogo-momentos-v0_1.tsv`; `ls data/curacion-registro/celdas-d/` |
| 0 FP abiertas; 109 NC abiertas; 15 SIN-ASIGNAR | `forense/firmas-pendientes.tsv`, `forense/no-corrido.tsv`, columna `estado` |
| ADR máximo `543`, conteo `543`, sin huecos | `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md \| grep -oE '[0-9]+' \| sort -n \| tail -1` |
| 9 entradas `PARA-v2.14` | `grep -c "PARA-v2.14" forense/hallazgos.md` |
| Huella de rutina sin enmienda | `grep -c "ADR-539" forense/rutinas.tsv` → 0 |
| `estado-programa-v1_13.md` retirada del árbol por `T01` | commit de A.3 del acto que selle esta versión; historia por SHA |

**Lo que este estado deja de decir, a propósito.** "El motor por celda no existe" (§12, `MARCADOR-C0-D`) queda **superado**: existe como conjunto de estimadores adjudicados por celda-D, dos hoy, con el estimador ganador más barato de todos. Lo que sigue sin existir es el motor matricial como estimador — y por `ADR-531` ya no tiene que existir.

**NO-DERIVADO en esta sección (declarado, no tecleado):** (1) el diseño del marcador por segmento sobre el catálogo — es sucesor de dirección con `FP-383` firmada, no de este estado; (2) el tamaño real de la interacción en la población para las dos familias piloteadas — los pilotos solo acotan a los candidatos (H5); (3) cuántas de las 16 corridas sin fila son `cuenta_gen2 = SI` — lo dirá `GEN2-REPLAY-ASIENTOS-1` al asentarlas; (4) las cuatro `decisiones.tsv` que faltan (FP-379 con su enmienda de nueve códigos, FP-385) — están `FIRMADA` en el tablero de firmas y sin fila de decisión; se derivan en el trámite que selle esta versión, no aquí.
