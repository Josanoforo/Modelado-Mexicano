# ACTO GEN2-ADOPCION-COLA-5

**SHA de redacción:** `38d25ad2` (`origin/main`, PR #745 fusionado — `Merge pull
request #745 from Josanoforo/acto/gen2-shed-bnpl-dano-universos`).

**Entorno asignado:** NUBE, Opus. **NO** se lanza en CAJA — adopción es
escritura de citas y sondas de consumo en solo-lectura, cero microdato.

**Estado:** VIVO

## VERIFICACIÓN DE EXISTENCIA (A.8, parte 2 — la contesta quien archiva)

**(1) ¿Existe ya la estructura?** Sí. `data/corrida0/{resultados.tsv,
usos.tsv, decisiones.tsv}` + `tools/corrida0.py status/registro` son la
estructura vigente que gobierna "adopción GEN2"; `milpa/tramite.yaml` es la
estructura vigente que gobierna "consumidores del motor" (patrón ya usado en
línea 613 y línea 1303-1304, entre otras). Ambas existen y gobiernan este
dominio.

**(2) ¿Existe ya el contenido?**

```
$ python3 tools/corrida0.py status
...
N_resultados_gen2_pendientes_adopcion=5
N_resultados_gen2_adoptados_activos=16
...
```

Los 5 ids concretos se derivan re-ejecutando la misma lógica que `status`
usa internamente (`ids_pendientes = _resultados_citados_en(PROPUESTA) &
ids_sellados_gen2 - ids_adoptados`, `tools/corrida0.py:4174-4187`):
`RESULT-C1-POSEL-AMENAZA-VEREDICTO`, `RESULT-C1-POSEL-OFERTA-VEREDICTO`,
`RESULT-CTX-2019-P-ALTO`, `RESULT-CTX-2021-P-ALTO`,
`RESULT-CTX-2023-P-ALTO` — EXISTE-SATISFACE.

Para la pieza P4 (adenda): `grep -n "RES-0063\|RES-0064"
data/adq-demanda-activa-v1_0.json` → EXISTE-SATISFACE, con
`situacion=MEDICION_ADOPTADA_SIN_COBERTURA_CONTRATO_GEN2` y
`siguiente_accion=["motor-gen2: registrar en corrida0 la medición ya
adoptada; no volver a medir ni pedir decisión científica"]` ya declarado en
el propio contrato.

**(3) ¿La estructura es posterior al trabajo que va a tocar?**
`data/corrida0/resultados.tsv` nació con `ACTO GEN2-E2` / `ACTO GEN2-E3` (7/sep/2026);
`CALC-0001`/`CALC-0002` (los 5 de P1-P3) se sellaron el 8/sep/2026,
**posteriores** a la estructura — sin hueco de cobertura retroactiva. Para
P4: el contrato de `data/adq-demanda-activa-v1_0.json` nació de `PR #739`/
`NC-0165` (11/sep/2026); la medición ENSANUT L17 subyacente es del
6/sep/2026, **anterior** a esa estructura — exactamente el caso (3) que A.8
exige declarar con las dos fechas, y es por lo que el propio contrato trae
la etiqueta `MEDICION_ADOPTADA_SIN_COBERTURA_CONTRATO_GEN2` en vez de
`SIN_RESULTADO`.

---

## Texto verbatim del encargo (lanzado por dirección, 14/sep/2026)

ENCARGO · ACTO GEN2-ADOPCION-COLA-5 · NINGÚN RESULT SE QUEDA ENVEJECIENDO EN LA VENTANILLA — los cinco sellados-sin-adoptar se adoptan con cita y consumo probado, o declaran por escrito por qué no

CABECERA · NUBE, Opus · NO se lanza en CAJA — adopción es escritura de citas y sondas de consumo en solo-lectura, cero microdato · COMPUERTA: ninguna (archivos disjuntos de 1/3 y 2/3 — corre en paralelo desde ya) · redactado contra 38d25ad2 · candidatos: deriva al cierre, no heredes.

FIRMA DE MESA, 12/sep/2026, verbatim (adentro; su merge sella): «Dame los encargos para nube. Todo lo que sea alineación, ajuste. Hicimos lo que pudimos en códex.» — despacho 3/3. La adopción por lote es firma de mesa POR MERGE (regla de la casa, F3: lote = PR = firma): este PR ES la firma de las adopciones que proponga, y las que exijan decisión previa distinta se PROPONEN sin ejecutar.

VERIFICACIÓN DE EXISTENCIA (A.8, dirección, contra 38d25ad2): corrida0.py status → N_resultados_gen2_pendientes_adopcion = 5 contra 16 adoptados activos; el patrón de adopción está maduro y probado (líneas con corrida0_resultado_id + corrida0_generacion, sonda de consumo del emisor en solo-lectura — precedentes #656, #664, #667). QUÉ cinco son: se deriva del registro en tu arranque (corrida0.py con la vista que los lista, o el cruce oferta↔usos) y se pega la lista con su consumidor y materialidad — dirección NO los enumera aquí a propósito: enumerarlos de memoria sería el defecto que A.8 existe para impedir, y el registro los sirve en un comando.

PIEZAS: P1 · EL CENSO DE LA VENTANILLA. Deriva los 5 con: RESULT id · CALC de origen · consumidor declarado · estimando y grano · reglas_impacto · qué decisión previa los toca (D1 complementos, NC-0085, cobertura parcial D2, o ninguna). Pega la tabla cruda. P2 · ADOPCIÓN O DECLARACIÓN, uno por uno. Para cada uno, exactamente una de tres salidas: (a) ADOPTA — la cita en su consumidor (el valor NO se mueve; patrón línea-583), compatibilidad de estimando/grano demostrada, sonda de consumo del emisor en solo-lectura con salida pegada; (b) NO-ADOPTABLE-POR-DECISIÓN — si cae bajo D1/NC-0085/NC-0110 u otra regla vigente: se declara con la cita de la decisión y queda fuera de la cola (el contador de pendientes debe reflejarlo — si el registro no distingue «pendiente» de «excluido por decisión», esa carencia es hallazgo con fila NC y la distinción se propone, no se improvisa); (c) DECISIÓN-DE-MESA — si la adopción cambiaría semántica, grano o consumidor: se propone en la tabla con la pregunta exacta y NO se ejecuta. Cero adopciones a medias: o entra con consumo probado o queda declarado. P3 · EL CIERRE CONTABLE. adoptados_activos, pendientes_adopcion y dependencias_legacy antes/después, crudo, sin esperados (E.4) — y si alguna dependencia legacy baja, la línea que explica cuál relevo la bajó.

PERÍMETRO Y CONCURRENCIA. Toca: milpa/*.yaml (SOLO las líneas de cita de los consumidores derivados en P1) · data/corrida0/decisiones.tsv si el vehículo de adopción lo exige + TSV re-derivados por el comando de la casa (la protección NC-0094 vigila sola) · forense/notas/ (tabla y salidas de sonda) · forense/no-corrido.tsv · 0-bis · cascada. EN PARALELO: CONCILIACION-TANDA-2 y DOCS-ALINEACION — intersección solo en no-corrido/TSV derivados: append/re-deriva, reporta pisadas. «Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.»

CONTADOR: no mide — mueve adopción, que es su propio contador, y se dice en una línea. LO QUE NO HACE: no re-mide nada · no adopta complementos ni nada vetado por decisión vigente · no toca el veredicto de la tríada (SIN-GANADOR-UNICO: ningún brazo se adopta — esa puerta está cerrada por su propia regla) · no firma FP. SUCESORES: si algún (c) queda propuesto, la vista --mesa lo sirve con este PR como contexto · el siguiente lote de caja hereda una ventanilla limpia. CIERRE · Cascada + ## NO-CORRIDO / RESERVAS + ## CONSUMIDO con el PR.

### ADENDA (dirección, 14/sep, recibida mientras el acto ya corría)

ADENDA al ACTO GEN2-ADOPCION-COLA-5 (dirección, 12/sep): pieza nueva P4 — registro ENSANUT (RES-0063/0064): registrar la evidencia existente de medición/adopción previa y probar AMBOS consumidores hasta emisión GEN2, sin re-medir ni pedir otra decisión científica (contrato en data/adq-demanda-activa-v1_0.json, responsable MOTOR_GEN2_REGISTRO); enlaza las NC históricas al contrato preservando antecedente. Es exactamente la clase de este acto: cadena hasta el emisor, no ciencia nueva.

---

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Adopción de `RESULT-CTX-2019-P-ALTO`/`RESULT-CTX-2023-P-ALTO`/`RESULT-CTX-2021-P-ALTO` como estimando descriptivo nuevo (contexto institucional alto entre víctimas de extorsión, LAPOP) | `DECISIÓN-DE-MESA-PENDIENTE` | Los 3 `RESULT` siguen sin consumidor en `milpa/tramite.yaml`; `N_resultados_gen2_pendientes_adopcion` no baja por estos 3. `R10.3`/`D2-h` no se tocan. | `NC-0167`; mesa decide si "contexto institucional alto" es un estimando propio con consumidor nuevo |
| Distinguir en `tools/corrida0.py::status()` "pendiente de adopción" de "excluido por decisión vigente" | `DECISIÓN-DE-MESA-PENDIENTE` | `N_resultados_gen2_pendientes_adopcion` sigue contando `RESULT-C1-POSEL-AMENAZA/OFERTA-VEREDICTO` como pendientes pese a quedar `NO-ADOPTABLE-POR-DECISIÓN` en este acto — el contador sobreestima la cola real | `NC-0168`; mesa autoriza el vocabulario/categoría nueva antes de escribirlo |
| Registro en `corrida0` (preflight/run/verify + `registro --escribe`) del `CALC` ENSANUT L17 para `RES-0063`/`RES-0064`, y cita `corrida0_resultado_id`+`corrida0_generacion:GEN2` en `milpa/tramite.yaml:1303-1304` (P4, adenda) | `PARO-ENTORNO` | `dependencias_numericas_legacy_activas` no baja por estas 2 filas; el motor ya consume los valores adoptados pero siguen `LEGACY-NO-DECLARADO` | `NC-0169`; acto en CAJA con corpus ENSANUT montado, sin volver a decidir nada científico |

## CONSUMIDO

Ejecutado en `PR #753`, `GEN2-ADOPCION-COLA-5`. La rama entrega el censo
P1, las declaraciones P2 (2 `NO-ADOPTABLE-POR-DECISIÓN`, 3
`DECISIÓN-DE-MESA` propuesta), el cierre contable P3 (cero adopciones,
declarado), la adenda P4 (`PARO-ENTORNO`) y `NC-0167`/`NC-0168`/`NC-0169`;
Jonás conserva la fusión.
