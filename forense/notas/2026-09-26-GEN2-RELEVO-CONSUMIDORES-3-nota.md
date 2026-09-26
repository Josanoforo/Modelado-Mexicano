# Nota · ACTO GEN2-RELEVO-CONSUMIDORES-3 · FIRMAS-18 H1–H3

26/sep/2026 · entorno **NUBE** (hook: `ENTORNO-DERIVADO = NUBE`, corpus no montado, 0 archivos examinados; este acto no abre microdato ni red) · rama `claude/new-session-p3kone` (fijada por la plataforma) · base `aa36232a` = SHA de redacción (0 commits detrás) · 0-bis `72d9735` · ADR-260926-GEN2-RELEVO-CONSUMIDORES-3-72d9-01.

Módulo de auditoría, primera línea: contadores movidos — `dependencias_numericas_legacy_activas` 123 → **67**; ninguna cifra nueva medida.

## 1 · Firmas ejecutadas (verbatim, FIRMAS-18, 25/sep/2026)

- **H1** «Mesa declara HISTÓRICO-SIN-RELEVO las 8 entradas asignados_coeficiente de milpa/procedencia.yaml; las 12 asignados_probabilidad siguen la regla de FIRMAS-16 B1/B2; ejecuta RELEVO-CONSUMIDORES-3.»
- **H2** «Para M01–M07 y M23 rige la regla de M08: acotar a la unidad medida donde el cotejo sea PARCIAL; HISTÓRICO-SIN-RELEVO donde sea NO-EQUIVALENTE; ejecuta RELEVO-CONSUMIDORES-3.»
- **H3** «Mesa declara HISTÓRICO-SIN-RELEVO las 42 lecturas L/AGREGADO de marco-M-sorteado-v1_3 y las saca del contador legacy; ejecuta RELEVO-CONSUMIDORES-3.»

Filas: `forense/firmas-pendientes.tsv` FP-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-01/02/03, FIRMADA (asentadas por FIRMAS-18; este acto no las re-asienta, A.12).

## 2 · Premisas re-verificadas

| premisa | rótulo | verificación | resultado |
|---|---|---|---|
| legacy 123 a `aa36232a` | EJECUTADO | `corrida0.py status` (status-antes-consumidores3.txt) | se sostiene: procedencia 39 · catálogo 22 · marco 43 · celdas-D 6 · motor 13 |
| ya hecho | — | `git ls-remote --heads origin \| grep -i relevo` → 0; PR abiertos «RELEVO-CONSUMIDORES-3» → 0; `grep -c HISTÓRICO-SIN-RELEVO milpa/procedencia.yaml` → 0 | nada hecho |
| el contador distingue HISTÓRICO-SIN-RELEVO | SUPUESTO | `tools/corrida0.py`: solo `TIPOS_FUERA_DEL_CONTADOR = {corte_pi}` (B3) y `rol_uso: historico` de tramite (B2) | **no se sostiene**: se extendió (ver §3) |
| el archivo del marco se edita | — | H3 dice «las saca del contador»; el marco v1_3 es artefacto sellado del duelo | **no se edita**: H3 va por `tipo_uso` en el contador, como B3 |
| B1/B2 para las 12 probabilidades: «donde no, `rol_historico` con rótulo» (§1 P1 del encargo) | LEÍDO | letra de a157-01 (B1): «donde no coinciden, **se conserva con rótulo**»; B2 aplica solo a NO-ADOPTAR-NC-0107 | **INTERPRETACIÓN-DECLARADA**: rige la letra de B1 (conservar con rótulo, sigue contando); ninguna de las 12 es NO-ADOPTAR-NC-0107, así que B2 no saca ninguna |

## 3 · Lo que se hizo

- **Contador** (`tools/corrida0.py`, perímetro §9 «solo si exige distinguir HISTÓRICO»): `_consumidores_historico_sin_relevo()` lee la marca por fila en el archivo vivo (H1: `historico_sin_relevo` en la línea `detalle` de su generador; H2: columna `estado_relevo` del catálogo); H3 por `tipo_uso ∈ {celda_L, celda_AGREGADO}` sobre `marco-M-sorteado-v1_3`. Salen de `usos_activos` y se cuentan aparte en `legacy_fuera_del_contador_por_firma__historico_sin_relevo` (54 = 8 + 4 + 42). No se borran del registro.
- **Escritor V6** `tools/escribe_relevo_consumo.py --relevo-consumidores-3` (diff seco por defecto, `--apply` escribe, idempotente: segunda corrida `SIN-DIFF`; rechazo atómico ante marca previa distinta):
  - H1 coeficientes: G2.sens_estatus, G2.aversion_riesgo, G3.aversion_riesgo, G4.horizonte_temporal, G4.sens_estatus, G5.familismo_obligacion, G5.radio_confianza, G6.deferencia → `HISTÓRICO-SIN-RELEVO` con cita de H1; **el valor no cambia** (sigue en `coefs`, `milpa/src/matriz.py` lo lee igual).
  - H1 probabilidades (regla B1): `tramite.gobierno_digital.util_sin_coercion` [0.71, 0.29] → [0.673393, 0.326607] = `RESULT-ENCIG-MOR-C-P-ADOPTA` (CALC-ENCIG-0001, vía i) y su complemento `RESULT-ENCIGDER-C-Q` (CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001, vía iii), ambos SELLADA, cuenta_gen2 SI, REPRODUCE; es el mismo par que B1 (a157-01) ya reconoció como coincidente en `tramite.yaml`. Las otras 11 se conservan con `rotulo_relevo: ASIGNADO-CONSERVADO-H1 …` y la razón por regla (8 sin regla hermana medida; mordida ×2: el hermano es SOLICITUD/proxy, no PAGO; coercitivo: sin conducta GEN2; formal_estable: el hermano ENFIH 2019 es tasa base y el disparador de formalidad no es construible).
  - H2 (redacción por momento **PROPUESTO-POR-EJECUTOR**, fuente `forense/analisis/astra4-relevo/cotejo-documental-catalogo.md`): columna nueva `estado_relevo` al final del TSV (las 19 previas intactas: cada línea nueva empieza con la vieja + tab).
    - M01, M02 (NO-EQUIVALENTE-PAGO), M07 (NO-EQUIVALENTE) → HISTÓRICO-SIN-RELEVO.
    - M06 (cotejo: «INSTRUMENTO SIN IDENTIDAD») → HISTÓRICO-SIN-RELEVO. **INTERPRETACIÓN-DECLARADA**: el instrumento declarado no coobserva las preguntas, lo que es no-equivalencia del instrumento.
    - M04 (PARCIAL) → **acotado** a la unidad medida: valor_gen2 = RESULT-ENCIG-MOR-C-P-ADOPTA (CALC-ENCIG-0001, sello en la fila), `discrepancia_gen1` NO-REPRODUCE-GEN1: persona en universo sin coerción (pago digital de luz, ENCIG 2025), no registro PERSONA ENIGH 2022. Mismo contrato que M08 (#1115).
    - M03 (PARCIAL) → **no se acota**: no hay RESULT GEN2 de `tramite.gobierno_digital.coercitivo` en ninguna unidad; escribir un valor sin RESULT es PARO (b). Sigue legacy; NC.
    - M05, M23 (cotejo: «DERIVADO SELLADO, SIN ADOPCIÓN») → **no se tocan**: no son PARCIAL ni NO-EQUIVALENTE, las dos ramas de H2. Probé el acotamiento al marginal: M05 → RESULT-EVASIONNORMA-A-P-EVADE pasa la guarda, pero B1 ya firmó que ese RESULT (conjunta) no coincide con la condicional de la regla; M23 → el único RESULT de `ahorra_solo_informal` es derivado (la guarda vía (i) lo rechaza: ingiere). Sacar esas dos del contador sin firma es la compuerta «borrar» de §8. NC con recomendación a mesa: HISTÓRICO-SIN-RELEVO (reserva consumida, champion NINGUNO).
- **Tests** `tests/test_escribe_relevo_consumidores3.py`: una prueba por llave (8 coeficientes, 1 citada, 11 conservadas, 4 momentos HISTÓRICO, M04 acotado), residuo M03/M05/M23 intacto, H3 por tipo, suma del desglose, idempotencia y dos rechazos atómicos.

## 4 · Tabla final (P4) y status antes/después

`forense/analisis/relevo-consumidores/tabla_final_c3.py` → `tabla-consumidores-v1_1.tsv` (reglas de -2 más las de este acto antepuestas; 0 `SIN-DICTAMEN`). Status en árbol: `status-antes-consumidores3.txt` / `status-despues-consumidores3.txt`.

| consumidor | antes | después | HISTÓRICO (fuera) | relevadas este acto | residuo (NC) |
|---|---|---|---|---|---|
| procedencia | 39 | **30** (esperado ≤ 32 ✔) | 8 (H1) | 1 (util_sin_coercion) | 7 β̂ CAJA · 11 ASIGNADO-CONSERVADO-H1 · 12 θ |
| catálogo | 22 | **17** (esperado ≤ 15 ✘) | 4 (M01, M02, M06, M07) | 1 (M04 acotado) | M03 · M05, M23 · 14 HOLDOUT |
| marco | 43 | **1** (esperado ≤ 1 ✔) | 42 (H3) | 0 | DIN-M-01:M (CAJA) |
| celdas-D | 6 | 6 | — | — | fuera de §9 |
| motor | 13 | 13 | — | — | fuera de §9 |
| **legacy total** | **123** | **67** | 54 | 2 | |

`adoptados` 81 → 81: los dos RESULT citados ya los adoptaba `tramite.yaml`.

**Catálogo 17 > 15**: el esperado de dirección suponía que 7 de los 8 momentos salían. Salen 5; M03 no tiene RESULT con que acotar y M05/M23 caen fuera de las dos ramas de H2. No se rebaja el «Hecho»; se declara y se deja NC con sucesor.

## 5 · Módulo de auditoría (§5)

- Escala y unidad: M04 y util_sin_coercion quedan en unidad **persona**, universo acotado (pago digital de luz, ENCIG 2025), rotulado en `discrepancia_gen1`/`clase_respaldo`; no se promedian con cifras de unidad delito. Los coeficientes HISTÓRICO siguen en la escala del índice del generador, sin enlace con β̂.
- Ninguna cifra tecleada: los valores salen de `resultados.json` de CALC sellados, leídos por el escritor.
- PROSPECTIVA / RETROSPECTIVA: no aplica; nada se emitió ni adjudicó.
- Riesgo de mala lectura: HISTÓRICO-SIN-RELEVO **no** es relevo ni validación; los 8 coeficientes siguen siendo ASIGNADO y el motor los usa igual. Solo salen del contador de deuda por decisión firmada.

## 6 · NC

`NC-260926-GEN2-RELEVO-CONSUMIDORES-3-72d9-01` (11 ASIGNADO-CONSERVADO-H1), `-02` (M03), `-03` (M05, M23; decisión de mesa pendiente), `-04` (residuo heredado de -2 que nombraba «-3» como sucesor: 7 β̂, 12 θ, 6 celdas-D; no está en el perímetro de este acto). Las NC de -2 que este acto resuelve o re-asigna no se editan en su sitio (D-21: gobierno se añade, no se edita): `e760-02` (8 coeficientes → HISTÓRICO, cerrada por este acto), `e760-03` (12 probabilidades → 1 relevada, 11 pasan a `-01`), `e760-04` (42 L/AGREGADO → HISTÓRICO, cerrada), `e760-08` (6 AJUSTE → 4 HISTÓRICO, M04 acotado, M03 pasa a `-02`), `e760-09` (M05, M23 → `-03`). `e760-10` (14 HOLDOUT) sigue como está.
