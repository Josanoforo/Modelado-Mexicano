# Cierre · `ACTO GEN2-YA-MEDIDO-TASAS`

**Fecha:** 10/sep/2026 · **Entorno:** NUBE/WSL2, cero microdato y cero
llamadas nuevas a modelos · **Base inicial:** `a63fd4c` · **Base integrada:**
`0d8e056` · **Encargo A.3:**
`forense/encargos/cola/2026-09-11-GEN2-POST-694/14-GEN2-YA-MEDIDO-SIN-FALSOS-NEGATIVOS.md`.

Al integrar `origin/main=0d8e056`, PR #695, #697, #702, #704 y #706 ocuparon
ADR-464 a ADR-468; este cierre queda reconciliado como **ADR-469**.

## 1 · Resultado útil

`tools/ya_medido.py` deja de tratar las tasas ejecutadas como si nunca se
hubieran medido. Los dos falsos negativos reproducidos por el encargo ahora
terminan en `MEDIDA-EN` y citan su evidencia sustantiva sellada:

| regla | fuente exacta | ejecución/sello | salida final |
|---|---|---|---|
| `tramite.mordida.con_registro` | `data/corrida0/CALC-ENCIG-0001/resultados.json:62,68` | `ejecucion.json:27`, exit 0; `sello.json:4`, válido | `MEDIDA-EN: CALC-ENCIG-0001, tramite.yaml` |
| `dinero.ahorro.horizonte_no_corto_con_seguridad_social` | `data/corrida0/CALC-ENIF-0001/resultados.json:23` | `ejecucion.json:26`, exit 0; `sello.json:4`, válido | `MEDIDA-EN: CALC-ENIF-0001, tramite.yaml` |

Esto acredita ejecución, no validez, adopción ni apoyo a la regla. El primer
caso conserva en el motor dos ramas históricas no adoptables y dos tasas r2
adoptadas; el segundo conserva su antecedente GEN1 y cita la tasa GEN2. La
herramienta no cambia ninguna de esas decisiones.

## 2 · Contrato de evidencia aplicado

| clase | qué exige la herramienta | efecto |
|---|---|---|
| tasa ejecutada | `clase: MEDIDO...` estructurado con procedencia, o referencia `corrida0_resultado_id` resuelta exactamente a RESULT + ejecución exitosa + sello verificable | acredita medición |
| intento `NO-ESTIMABLE` | veredicto/situación de resultado con procedencia de ejecución | acredita el intento sin inventar `p` |
| adopción al motor | se lista separadamente; no se infiere de `MEDIDA-EN` | no altera la clasificación |
| hipótesis/propuesta | `p`, palabra MEDIDO o RESULT futuro sin ejecución | no acredita |
| mera mención | término fuera del `id` exacto o de un campo de alias declarado | no acredita ni presta el veredicto vecino |

La antigua ventana de ±260 caracteres se retira. Cada entrada YAML se
delimita por su propio `- id:`; se inspecciona el bloque completo de esa
identidad, sin barrer el resto del archivo. Los ids con sufijos no son aliases
por parecido. Sólo cuentan el id exacto, el puente R-n/id ya congelado en el
canon o los campos explícitos `alias_de`, `enmienda_de`,
`misma_regla_motor`, `referida_a` y `regla_base`.

`canon/modelo-decision-v4_0.md` §7, las specs y
`canon/registro-rotulos.tsv` siguen apareciendo como antecedentes, pero no
acreditan por sí solos una ejecución: pueden contener varias reglas o una
receta todavía no corrida. Las notas de resultados/cierre conservan su valor
histórico; cuando existe una referencia corrida0, la fuente sellada queda
visible en la propia salida.

## 3 · Pruebas

`tests/test_ya_medido.py` aporta ocho regresiones dirigidas, sin depender del
conteo total del repositorio:

1. tasa con RESULT, ejecución y sello exactos;
2. propuesta con `p`, `MEDIDO` y RESULT declarado, pero no ejecutado;
3. dos reglas vecinas con veredictos distintos;
4. evidencia pertinente a más de 260 caracteres dentro del mismo bloque;
5. alias declarado frente a un nombre sólo parecido;
6. intento `NO-ESTIMABLE` sin parámetro disponible;
7. los dos positivos reales con cita corrida0;
8. controles históricos positivo y negativo.

Salida dirigida: `Ran 8 tests ... OK`. La línea base completa terminó con
código 0 y `LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json`;
conserva los 3 `FAIL` y 2756 `WARN` ya registrados, sin introducir ninguno
nuevo. En particular, T02, T15, T25, T30/T-YAMEDIDO y T30b quedaron `[ok]`.
El negativo legítimo
`familia.cortejo.urbano_joven_apps` conserva `NUNCA-MEDIDA`; los positivos
históricos `civico.voto.clientelar_si_observable`,
`civico.protesta.agravio_urbano` y `R4.4` conservan `MEDIDA-EN`.

Sonda de solo lectura: se tomaron SHA-256 antes y después de ejecutar los dos
positivos y el negativo sobre `demanda-corridas.tsv`,
`demanda-resultados.tsv`, `corridas.tsv`, `resultados.tsv` y `usos.tsv`;
`HUELLAS_IDENTICAS=SI`. No se modificó demanda ni ninguna vista corrida0.

## 4 · Cierre administrativo

- `NC-0109`: **CERRADA** por reconocimiento estructural de tasa y resolución
  de evidencia sellada.
- `NC-0129`: **CERRADA** por el mismo arreglo; su enlace histórico a
  `NC-0110` se rectifica dentro de la fila y se conserva como antecedente.
- `NC-0110`: permanece **CERRADA** por `GEN2-MOTOR-SEMANTICA`; no se reabre ni
  se vuelve a cerrar.
- Cambios científicos: cero. Sin cambios a `milpa/*.yaml`, CALC,
  `tools/corrida0.py`, inventario, cron o vistas.

La reparación satisface D-14: protege dos falsos negativos ya observados y
evita repetir sondeos/cálculos, sin crear base, índice persistente ni motor de
búsqueda nuevo.
