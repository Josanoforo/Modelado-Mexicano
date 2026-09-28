# Nota de cierre · ACTO GEN2-ASTRA-CONTINUIDAD-C1-1 · 28/sep/2026

**Contadores movidos: cero.** `resultados_con_validacion_independiente` antes 215, después 215, porque este acto no asienta ningún PASA nuevo. La razón está en P1 y se deriva de la regla que fija el propio encargo; no es un defecto de ejecución.

Entorno NUBE (hook: `ENTORNO-DERIVADO = NUBE`, corpus no montado, examinados 0). Cero microdato: aquí no se recalculó nada. Base `e584ee5f` (origin/main). El SHA de redacción `3a7b61db` es ancestro; main avanzó dos merges ajenos al perímetro. 0-bis `26a2f0d8`, raíz `26a2`. Modo AUTÓNOMO-AMPLIO.

## P1 · Asientos en `data/corrida0/validaciones-independientes.tsv`

**Regla, declarada antes de escribir** (la del encargo §1, aplicada tal cual). `PASA` solo si la `tolerancia_citada` se cumple en el punto **y** en los dos extremos del IC. `CONCUERDA-NO-APROBADA` si el punto concuerda pero la spec no bastó o no hay tolerancia por llave. `NO-PASA` si algo discrepa o no se pudo comparar nada. Se asienta una fila por `(spec_id, resultado_id)`. Receta: `forense/analisis/astra-continuidad-c1/asienta_p1.py`.

**Dos premisas cayeron. Las dos son de logística o estado; el procedimiento no se ajustó.**
1. **«1 873 DISCREPA-dentro-de-tolerancia» es falso bajo la regla.** [EJECUTADO] En las 1 873 SOSTENER/DISCREPA, |Δpunto| ≤ 1e-10 en las 1 873, pero |ΔIC| ≤ 1e-10 en **0** (Δ típico 2e-4 sobre IC con semilla; `artefacto = TOLERANCIA-DE-REPLAY-SOBRE-IC-ALEATORIO`). La tolerancia citada es la de replay (NC beee-06). **Por la regla del encargo, ninguna de las 1 873 es PASA**, y marcarla PASA es PARO (c). Solo 3 llaves cumplen punto e IC; las 3 están en RESULT-ENDIREH2011-MOD-TABLA, y ese RESULT tiene 683 puntos que discrepan. En la frase de producto, esas 1 873 están «dentro de la tolerancia 1e-10 en el punto; fuera de ella en el IC». No «coinciden».
2. **El esquema de la vista no admite dos validaciones por `(spec, RESULT)`.** [LEÍDO `tools/corrida0.py` `_aplica_validaciones_independientes`] Una llave repetida dispara `VALIDACION-OVERLAY-DUPLICADA` y la vista no se escribe. Por eso no se puede asentar «por RESULT × dictamen» ni «una fila ciega con ref distinta» sobre un RESULT que ya tiene fila (la rama del §5). Seis de los nueve RESULT del lote 1 ya tenían fila NO-PASA, de RECIBO-ASTRA6-1, con sus conteos en `alcance_validacion`. No se duplican ni se editan.

**Qué se asentó (271 filas, solo append; registro en seco `corrida0.py registro` → EXIT 0, sin PARO de overlay):**

| Lote | Filas | Dictamen | Qué dicen |
|---|---|---|---|
| 1 | 3 (COM, LAB, ESC) | NO-PASA | 0 recalculadas de 100/100/96. Todas NO-RECALCULABLE por PAQUETE-SIN-IDENTIDAD-DE-VENTANA (beee-01). No se comparó nada; no es discrepancia |
| 2 | 267 | CONCUERDA-NO-APROBADA | El punto coincide. El IC es NO-RECALCULABLE (256) o no tiene referencia (9), o coinciden punto e IC sin tolerancia por llave (2). **130 rotuladas NO-CIEGA-PENDIENTE** (ENBIARE 126 y ENCIG 4, NC 627e-07) |
| 2 | 1 | NO-PASA | Punto coincide; IC discrepa (las otras 7 de ese tipo ya tenían fila) |

Lote 2 re-derivado de `lote2-tabla-estimadores.tsv`: 425 filas. 92 apartadas por adenda, 56 no reconstruidas y 277 reconstruidas, de las cuales **275 coinciden en punto** (256+9+8+2). Así se confirma el [REPORTADO] de Astra. **Sin asiento:** las 56 no reconstruidas y las 92 apartadas, porque el vocabulario de la vista no tiene un estado para «no evaluado». También quedan fuera 9 llaves que ya tenían fila.

**Conteos del lote 1 por recomendación** (criterio de «hecho»), derivados de la tabla de RECIBO-ASTRA6-1: SOSTENER 1 876 · ACOTAR 689 · PROPONER-SUSPENDER 7 · SOSTENER-SIN-CORROBORACION 799. Las 9 filas del lote 1 ya existían o se asentaron aquí. En `alcance_validacion`, las 6 filas anteriores usan el vocabulario punto/IC/publicabilidad/no-recalculable y no el de recomendación. Suman las 3 371 llaves, pero no se reescribieron para que digan 1 876/689/7/799, porque editar filas ajenas queda fuera del append. El cruce recomendación × RESULT se deriva con `asienta_p1.py` y queda en P3 para las 799.

## P2 · NC de C1

Tabla: `forense/analisis/astra-continuidad-c1/nc-c1-dictamen-v1_0.tsv`, generada por `dictamina_p2.py`. Universo: 59 filas ABIERTA con ASTRA6-C1 o RECIBO-ASTRA6-1/2/3/N en el id, al 0-bis. Ids sin fila: 0. Resultado para C1: **CERRADA 6** (6c30-02, 996b-07, beee-05, ee49-04, 1653-01, 8c5c-02), **DECISIÓN 17** (van a la hoja) y **SIGUE-ABIERTA 15**, cada una con su sucesor. **AJENA 21** (C2, C3 o TUBERÍA, sin tocar). Las 6 CERRADA se asentaron en `forense/no-corrido.tsv` editando la línea (estado, cerrado_por, fecha_cierre; diff 6/6). PENDIENTES-2 no escribe esas filas.

## P3 · Las 799

`forense/validacion-independiente/specs-insuficientes-v1_0.tsv`: 7 filas, suma 799. **Hallazgo: 767 de las 799 no son D-15.** La spec y el RESULT sellados traen la ventana; la omitió el `estimandos.tsv` del paquete ciego (beee-01). Propuesta: NADA sobre la spec; los paquetes `-ventana-v1` de #1203 ya las cubren y solo falta recalcular en el lote 3. **Las 32 D-15 reales:** D15-RECODIFICACION-AUSENTE en 31 (DIS 23, NF-BC 8) y D15-IDENTIDAD-CONTRADICTORIA en 1 (AYU #115). Propuesta para las 32: ADENDA-DE-SPEC, es decir, una versión humana sucesora sin tocar el sello, dentro de GEN2-SPECS-ADENDA-1. RE-SELLAR no aplica a ninguna: no hay cifra sellada que corregir, falta texto humano. Ninguna spec se editó.

## P4 · Hoja

`forense/analisis/astra-continuidad-c1/hoja-mesa-c1-v1_0.md`, con las cuatro secciones: §a reconstructor, §b contrato v3 vs v2, §c FP de C1 y §d gates del lote 3. Cinco filas FP nuevas: `FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-01..05`.

## Módulo de auditoría v2.16 (la nota afirma qué cifras del catálogo están validadas)

- ¿Contadores movidos? Cero (arriba).
- ¿Unidad de cada cifra? Las llaves del lote 1 son proporciones de mujeres (unidad persona), ENDIREH 2011/2021. En el lote 2 la unidad es la de cada RESULT: persona, hogar o delito según el instrumento. No se promedia ninguna y no hay agregado entre llaves: solo conteos de llaves.
- ¿PROSPECTIVA o RETROSPECTIVA? Todo es RETROSPECTIVO: se recalculó después de que existían los sellados. No hay frase que mezcle las dos.
- ¿Escala y comparación? Δ en la escala del RESULT contra la tolerancia de la spec (1e-10 o 0.0). Ninguna comparación cruza escalas.
- ¿Qué afirmación de estado se escribió a mano? Ninguna: todos los conteos salen de los dos scripts.
- ¿Qué sería peligroso leído simplista? Que «275 coinciden» o «1 876 SOSTENER» se lea como «validado». Ninguna de esas llaves pasó la validación independiente bajo tolerancia citada.
- ¿Pobreza, clase o sesgo de marco? No aplica: el acto no interpreta contenido sobre México.

## NO-CORRIDO / RESERVAS

Vive en el encargo archivado (§ de cierre) y en `forense/no-corrido.tsv`.
