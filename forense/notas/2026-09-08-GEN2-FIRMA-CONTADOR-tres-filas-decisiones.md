NOTA · ACTO GEN2-FIRMA-CONTADOR · propaga la firma de mesa 8/sep/2026

Encargo: `forense/encargos/2026-09-08-GEN2-FIRMA-CONTADOR-PROPAGA-FIRMA.md` (0-bis A.3).
COMPUERTA: PR #634 fusionado — verificado (`git cat-file -e origin/main:data/corrida0/CALC-0003-v2/sello.json` → EXISTE).

## P1 · las tres filas, por la vía directa

Se escribieron, primero, tres filas nuevas en `data/corrida0/decisiones.tsv`
(`CALC-0001`, `CALC-0002`, `CALC-0003-v2`, `cuenta_gen2=SI`, fuente =
FIRMA DE MESA 2026-09-08 citando este encargo), y solo después se corrió
`corrida0 registro` y `corrida0 status`, en ese orden, en el mismo commit
(commit `bfe9fee`). En ningún commit del acto existió un estado simulado.

Verificación:
- `grep -c "PENDIENTE-DE-MESA" data/corrida0/corridas.tsv` → 1 (la única
  fila restante es `CALC-0003` v1, `SUPERADO→CALC-0003-v2`, fuera de
  perímetro por diseño del propio encargo); `data/corrida0/resultados.tsv`
  → 0.
- `grep -rlI "FIRMA SIMULADA" data/ forense/ canon/` → 0 archivos de datos
  reales (la frase solo aparece en prosa: `firmas-pendientes.tsv`,
  `no-corrido.tsv` y notas que la citan como historia, y en el propio
  encargo de este acto, que la cita al describir la trampa que evita).

## P2 · el contador

`python3 tools/corrida0.py status`:

```
N_corridas_requeridas=86
N_corridas_selladas=3
N_resultados_activos=205
N_resultados_sellados=211
N_resultados_pendientes=205
dependencias_numericas_legacy_activas=205
N_resultados_gen2_sellados=211
N_resultados_gen2_pendientes_adopcion=5
N_resultados_gen2_adoptados_activos=0
resultados_con_validacion_independiente=0
diferencias_materiales=0
no_corrido_abiertas=26
replays_legacy_sellados=2
corredores_envueltos_legacy=8
# derivado de 100 corridas · 601 resultados · 205 usos
```

`N_corridas_selladas` 0→3 y `N_resultados_sellados` 0→211 (83+128), exactamente
lo esperado por la nota de PR #634. Cifras iguales a las esperadas: no hubo
que pegar una diferencia.

## P3 · el registro

- FP-356 → **FIRMADA**, citando la firma de mesa verbatim y este encargo.
- NC-0045, NC-0046 y NC-0049 → **CERRADAS** (las tres tenían la misma causa
  raíz — la ausencia de esta firma — y las tres quedan resueltas por el
  mismo commit).
- T35 (`T-REPRO`) se ejerció por primera vez sobre cadena GEN2 real. Es
  noticia, y la noticia es: **MUERDE**. `python3 tests/check.py --baseline`
  sale ROJO con:

  ```
  [FAIL]  T25 T-ROTULOS  (1 fail)      -- corregido en este mismo acto
                                            (exención por ARCHIVO, ya conocida
                                            en el patrón de E5/E5-1/E5-0)
  [FAIL]  T32 T-CORRIDA0  (2 fail)     -- NC-0053, fuera de perímetro
  [FAIL]  T35 T-REPRO     (211 fail)   -- NC-0053, fuera de perímetro
  ```

  Los 211 fallos de T35 son, en su totalidad, del ramal (a) («activo GEN2 y
  sin consumidor»): los 211 RESULT ahora activos GEN2 no tienen ningún
  consumidor en `milpa/` que los cite por `corrida0_resultado_id` — el
  mismo hecho que NC-0048 (`delta` sin insumos, control positivo vacío en
  los 205 usos) ya había medido desde el otro lado. No es un defecto de
  esta firma: es la cadena de adopción (E.2) que el propio encargo declara
  fuera de su objeto («no adopta al motor»).

  T-CORRIDA0 falla en `t_status_arbol_real_no_cuenta_smokes`
  (`T-STATUS-SMOKES`): ese falsador afirma, con la premisa pre-firma
  todavía en su docstring, que `N_corridas_selladas==0` y
  `N_resultados_sellados==0` son la cifra correcta. Esta firma vuelve esa
  premisa falsa por diseño — es exactamente lo que P2 pedía que pasara.
  Actualizar el falsador queda fuera del perímetro de este acto (no incluye
  `tests/`) — asentado como **NC-0053**.

  T25 (`T-ROTULOS`) marcó el propio encargo archivado por citar `E5-1`
  pelado; se corrigió en el mismo commit de cascada con la exención por
  ARCHIVO en `_T25_ARCHIVOS_CONOCIDOS` (mismo patrón que E5/E5-0/E5-1/
  TRAMITE-FIRMAS-1), porque las dos apariciones son procedencia al acto
  predecesor ya censado, no un rótulo nuevo.

## Perímetro respetado

Solo se tocó: `data/corrida0/decisiones.tsv` · `data/corrida0/{corridas,
resultados,usos}.tsv` (usos.tsv sin cambios de contenido) ·
`forense/{firmas-pendientes,no-corrido}.tsv` · esta nota · el 0-bis ·
`tests/check.py` (`_T25_ARCHIVOS_CONOCIDOS`, parte de la cascada estándar,
paso 5) · la cascada de cierre (gobernanza, registro-rotulos,
estado-programa §L0). No se tocaron sellos, specs, milpa ni el tablero.

## Lo que NO hace

No adopta al motor (E.2 es de otro día) · no corre `delta` (B-7, sin
implementar) · no toca `CALC-0003` v1 (SUPERADO, historia) · no simuló
absolutamente nada.
