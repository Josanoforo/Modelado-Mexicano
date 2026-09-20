# ACTO GEN2-RELEVO-TANDA-1 · informe

Corte: `a92126f0a930dc31614c5c8f58f09b29b395962a` (el SHA que el encargo declara; re-derivado al abrir, sin desfase).
Entorno: NUBE · `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` · corpus `data/raw` NO montado (archivos examinados = 0) · no se abrió microdato: todo insumo es un `RESULT` sellado, como el encargo exige.

## Contadores, antes y después — derivados, no tecleados

| contador | comando | antes | después |
|---|---|---:|---:|
| `dependencias_numericas_legacy_activas` | `generacion_hoy == LEGACY-GEN1` en `relevo-usos-v1_0.tsv` | **182** | **182** |
| `adoptados_activos` | `generacion_leida == GEN2` en `usos.tsv` | **46** | **46** |
| `cuenta_gen2` | — | NO-APLICA | NO-APLICA |

**El contador no se movió, y esta vez se sabe exactamente por qué.** No es que falte trabajo: es que la regla firmada que gobierna la adopción autoriza cero slots. Ver P4.

## A.8 · verificación de existencia (dirección contra el árbol)

La dirección cuadra al renglón. `relevo-usos-v1_0.tsv` = 208 filas de datos; `veredicto`: `SIN-CANDIDATO` 154 · `YA-ADOPTADO` 24 · `CANDIDATO-GEN2` 12 · `NO-ADOPTABLE-POR-VEREDICTO-SELLADO` 8 · `LISTADO-PARA-MESA` 7 · `CONFLICTO-ENTRE-CANALES` 2 · `VETADO-POR-DECISION` 1 (la dirección lo abrevia `VETADO`). `generacion_hoy`: `LEGACY-GEN1` 182 · `GEN2` 26. Los 12 candidatos son los que la dirección lista. `grep` de las siete encuestas del 19/sep sobre la vista → **0**.

Una corrección de hecho, menor y sin consecuencia para el acto: la dirección dice que las columnas `delta`, `cambia_signo` y `materialidad` están vacías en las 12 y que «la comparación por script que E.1 exige no se ha corrido». Vacías sí están —`relevo_usos.py` no las llena—, pero **la comparación por script sí se corrió**: el `ACTO GEN2-RELEVO-CANDIDATOS-DELTA-1` (16/sep) la dejó en `forense/relevo-usos/candidatos-delta-1/`. Se re-derivó hoy y reproduce **bit a bit**.

---

## P1 · Delta por script — CORRIDO, reproduce idéntico

```
python3 tools/relevo_candidatos_delta.py --destino forense/analisis/relevo-tanda-1/p1-delta
python3 tools/corrida0.py delta --entrada .../contrato-gen2-delta-1.yaml --formato json --salida-dir .../_corrida0_delta
python3 tools/relevo_candidatos_delta.py --destino .../p1-delta --delta-json .../delta.json
  → seleccion=12 · bins=1:0,2:10,3:2
diff contra forense/relevo-usos/candidatos-delta-1/tabla-decision.tsv → sin diferencias
```

12 pares · comparables 11 · incompatible 1 (RES-0028) · **deltas materiales 0**. Los once deltas comparables van de `5.55e-17` a `4.79e-07`: ruido de redondeo del sexto decimal con que `milpa/` materializa, no movimiento.

**Criterio de bloque, escrito antes de correr** (como el encargo manda): entra al bloque el slot con estimando casado por texto (P2) **y** `|Δ|` dentro de la tolerancia del tipo de RESULT. Los once comparables cumplen ambas. **Y aun así el bloque sale vacío** — porque la tolerancia no es el único filtro que la regla firmada impone. Ver P4.

## P2 · Mismo estimando, por texto — 11 CASA, 1 NO-CASA

Tabla completa: `P2-mismo-estimando.tsv` (evento · universo · unidad · ola · denominador, por slot, contra la spec del CALC candidato; derivada de `relevo_candidatos_delta.py::_familia`, que es donde esas correspondencias viven acreditadas contra spec y consumidor).

- **11 CASA**: RES-0025/0026 (delito, ENVIPE 2025, `FAC_DEL`, n=40 280) · RES-0031/0032 y RES-0053–0056 (persona 18+, ENIF 2024, `FAC_PER`, n=13 502) · RES-0033/0034 (persona, ENIF 2024, n=11 895) · RES-0066 (persona no trabajadora, ENIF 2024, n=3 462). En los once, las cinco dimensiones coinciden por texto: el número igual **es** el mismo cálculo.
- **1 NO-CASA**: RES-0028, con ruptura en cuatro de las cinco (`unidad`, `universo`, `evento`, `denominador`). Fila para mesa. Ver P3.

La lección de `matrimonio_directo` se sostiene en el único caso donde podía fallar: RES-0028 coincide a *dos* decimales con su candidato y aun así no es la misma afirmación.

## P3 · RES-0028 — el universo es U4 contra U1, y la aritmética lo cierra

`RES-0028` es `civico.denuncia.miedo_desconfianza:denuncia_por_otra_razon`, complemento declarado (`complemento_de`), legacy `0.705687`.

Con los `RESULT` sellados de `CALC-ENVIPE-0001`, sin abrir microdato:

```
RESULT-ENVIPE-DEN-P-C2-U4            = 0.29431298745731216   (persona)
1 - P-C2-U4                          = 0.7056870125426878  → 6d: 0.705687  ==  legacy RES-0028  ✔
RESULT-ENVIPE-DEN-P-C2-U1            = 0.2672433874042781    (delito)
RESULT-ENVIPE-DEN-P-COMPLEMENTO-C2-U1= 0.7327566125957219  = 1 - P-C2-U1     (candidato de la vista)
P-C2-U4 - P-C2-U1                    = 0.02706960  =  2.707 pp   ==  la brecha observada  ✔
```

**Qué universo explica la diferencia: el legacy vive en `U4`, el candidato en `U1`.** Cita de spec, `data/corrida0/CALC-ENVIPE-0001/spec.md:26-30` («Unidad de observación — declarada, porque cambia el denominador»):

| universo | unidad | filtro | ponderador |
|---|---|---|---|
| `U1` (PRIMARIO) | **delito** (`ID_DEL`, `tmod_vic`) | `BPCOD ∈ {05..15}` · `BP1_20=2` · `BP1_23 ∈ {01..08}` | `FAC_DEL` |
| `U4` | **persona** (`ID_PER`, `tper_vic2`) | persona con ≥1 delito en `U1`; colapso GEN1 (`máx`) | `FAC_ELE` |

Y la spec lo dice ella misma, `spec.md:65`: «`P-C2-U4` (**única celda que comparte codificación y unidad con GEN1**)». La vista propuso `…-COMPLEMENTO-C2-U1`; la spec nombra `U4`. La brecha de 2.7 pp no es un delta: es el precio de cambiar de denominador —de persona a delito— sin decirlo. No se interpreta como movimiento y no entra al bloque.

**Dos opciones para mesa (FP):**
- **(a) Conservar el estimando, cambiar el RESULT.** Emitir un sucesor `RESULT-ENVIPE-DEN-P-COMPLEMENTO-C2-U4` en una versión nueva del CALC y aparear RES-0028 con él. Conserva la afirmación (persona) y el valor `0.705687`. **Costo:** exige tocar un CALC — fuera del perímetro de este acto.
- **(b) Conservar el RESULT, cambiar el estimando.** Adoptar `…-COMPLEMENTO-C2-U1` y asumir que RES-0028 pasa de persona a delito. **Costo:** deja de ser la misma afirmación; obliga al renombre que `ADR-509` ya propuso y arrastra a `RES-0124:celda_AGREGADO`, que depende de este slot.

Recomendación del ejecutor, no decisión: **(a)**. (b) mueve el contador cambiando lo que la cifra dice, que es exactamente lo que el módulo de auditoría de este encargo advierte que no se confunda.

## P4 · Adopción del bloque — **PARO-PREMISA, cero adopciones**

El mecanismo existe y está entendido: la adopción se escribe como `corrida0_resultado_id` + `corrida0_generacion: GEN2` en la conducta de `milpa/tramite.yaml` (sin tocar `p`), y `usos.tsv` y `relevo-usos` se re-derivan de ahí — ambos son `# DERIVADO — NO EDITAR`. No es `relevo_usos.py` quien adopta: ese módulo **deriva**, y su CLI no tiene verbo de adopción. Es lo mismo que `decisiones.tsv:133` ya había asentado para RES-0043/0044: «`tools/relevo_usos.py` no admite esta decisión por comando (PARA)».

Lo que impide adoptar no es el mecanismo, es la **regla firmada**. La ADENDA de adopción en bloque (firma de mesa, 15/sep/2026, `forense/encargos/2026-09-15-GEN2-RELEVO-USOS-1-ADENDA-REGLA-ADOPCION-EN-BLOQUE.md`) pone en bin 1 —el único bin que un merge adopta— sólo lo que cumple las tres condiciones, y su inciso (iii) excluye expresamente «una regla con `p` medida» y «insumo del marcador (M/R/L/agregado)»: «ésos son siempre bin 2». Corrido el script:

| bin | slots | por qué |
|---:|---|---|
| **1 — adoptados por este merge** | **0** | — |
| 2 — a mesa, uno por uno | 10 · RES-0025, 0026, 0031, 0032, 0033, 0034 (reglas con `p` medida) · RES-0053, 0054, 0056, 0066 (insumos de `RES-0149`, `RES-0154`, `RES-0164` `celda_AGREGADO`) | inciso (iii): «para el generador y el marcador, la adopción se firma aunque no cambie nada, porque cambia quién manda» |
| 3 — bloque a mesa con tabla | 2 · RES-0055 (sin `se_mueve_si` ni IC legacy propio) · RES-0028 (no comparable) | sin criterio / ruptura de estimando |

Los doce candidatos caen, sin excepción, en el conjunto que la propia regla reserva a la firma. **Bin 1 está vacío, y por eso este acto adopta cero.**

La PROPAGACIÓN de esa misma ADENDA es explícita en su paso 3: «bin 1 (**adoptados por este merge**), bin 2 (**a mesa**, uno por uno), bin 3 (**bloque a mesa** con tabla)». Adoptar bin 2 por merge en bloque sería derogar la regla firmada del 15/sep desde un acto de ejecución — que es precisamente lo que la casa no hace.

**Sobre la firma que el encargo invoca.** `decisiones.tsv:132-133` se leyó verbatim. Dice: «MEDICION-DEMANDA-3 se redefine al universo real de `relevo-usos-v1_0.tsv`: 153 `SIN-CANDIDATO`, con los 12 `CANDIDATO-GEN2` primero. Ambas cierran con ese sucesor.» Esa firma redefine **el universo y el orden de la demanda de medición**, y cierra NC-0255/NC-0256. No es una firma de adopción y no nombra ningún slot como adoptado. La firma que gobierna la adopción sigue siendo la ADENDA del 15/sep, y bajo ella el bloque está vacío. El «texto de resolución propuesto para mesa — no firmado» que DELTA-1 dejó redactado el 16/sep sigue sin firmar: es el instrumento que falta, y se sube hoy a `firmas-pendientes.tsv` con los doce renglones ya servidos, uno por slot, con su delta a la vista — que es exactamente lo que el bin 2 pide.

Con esa firma, la tanda siguiente adopta los diez de bin 2 y el bloque de bin 3 en un solo movimiento y el contador baja de 182 a 171 (los diez, más RES-0055; RES-0028 depende del FP).

## P5 · La vista aprende las mediciones del 19/sep — y lo que aprende es que ninguna ofrece

Se re-derivó la vista completa a `a92126f0` (`tools/relevo_usos.py --json`): **208 filas, los mismos siete veredictos, los mismos conteos, 0 slots con veredicto distinto**. La vista está en punto fijo.

Eso no es un desfase de la vista: es una lectura correcta de lo que las specs declaran. Se examinaron **los 42 CALC** tocados entre el 18 y el 20/sep (`P5-cobertura-19sep.tsv`). Ninguno fija una pareja `consumidor ← RESULT`:

| `adopcion` declarada en `spec.yaml` | CALC |
|---|---:|
| sin clave `adopcion` | 21 |
| `NINGUNA` | 9 |
| `PENDIENTE-DE-MESA` | 8 |
| `NO-ADOPTADO` | 4 |
| **con mapa C1 o pin C2 a un slot legacy** | **0** |

`CALC-ENUT2024-PARTICIPACION-INTENSIDAD-0001` lo escribe sin rodeos: `releva: "NINGUNO; ampliacion descriptiva, no relevo automatico"`. `CALC-ENFIH2019-SALDOS-AFORE-0001`: «el encargo autoriza medir y publicar, no inventar firma ni adopcion». La vista no infiere y hace bien: las 22 mediciones de ayer son **ampliación descriptiva**, no relevo. El 182 tampoco se mueve por aquí, y la cobertura retroactiva que el encargo suponía derivable no existe porque nadie la declaró.

**La pista de dirección, verificada — y es media verdad.** El mapeo de slots es correcto: `CORR-0076` agrupa exactamente `RES-0165`…`RES-0170`, los seis cortes de `milpa/src/celdas.py:CORTES_C1` (`formalidad`, `edad`, `urbanizacion`, `ingreso`, `acceso_digital`, `migracion`). Pero los seis salen `SIN-CANDIDATO` con razón `CORR-SIN-CALC-DECLARADA`: **`CORR-0076` no tiene ningún CALC declarado**. El encargo Codex de ENIGH podrá enlazar los slots, pero ese enlace no está en ninguna spec sellada, y mientras no lo esté la vista no puede verlo. Sucesor concreto, no suposición.

**Demanda de medición de caja** (`P5-demanda-agrupada.tsv`): los **154** `SIN-CANDIDATO` siguen sin oferta —los 154, ninguno ganó— agrupados en **71 corridas naturales**. 138 por `CORR-SIN-CALC-DECLARADA`, 16 por `CORR-CON-CALC-SIN-RESULT-FIJADO`. Concentración: `CORR-0019` (21), `CORR-0082` (14), `CORR-0083` (12), `CORR-0081` (8), `CORR-0018` (7), `CORR-0076` (6). Esas seis corridas son 68 de los 154 — el 44% de la demanda en seis encargos de caja. Ahí salen los siguientes.

Esta pieza **no adopta**: la tanda 2 sale de esta lista, y hoy esa lista de ofertas nuevas está vacía por la razón anterior.

## P6 · Los 7 `LISTADO-PARA-MESA` y los 2 `CONFLICTO` — una línea cada uno

Los siete no son un mismo caso: los `RESULT-…-ADOPCION` sellados los parten en dos.

- `RES-0039` `civico.denuncia.con_seguro:denuncia` — falta el pin **y** el veredicto sellado dice `LISTADO-PARA-MESA-NO-REPRODUCE`. El punto sí reproduce (GEN2 `0.7909064` vs legacy `0.7909`); lo que no reproduce es el IC: sellado `[0.752301, 0.827811]` vs GEN2 `[0.749985, 0.831673]`. Mesa decide sobre la anchura, no sobre el punto.
- `RES-0040` `con_seguro:no_denuncia` — igual; GEN2 `0.2090936` vs legacy `0.2091`. Complemento del anterior, misma decisión.
- `RES-0041` `sin_seguro:denuncia` — igual; GEN2 `0.6720144` vs legacy `0.672`, IC sellado `[0.642490, 0.701624]` vs GEN2 `[0.636621, 0.704492]`.
- `RES-0042` `sin_seguro:no_denuncia` — igual; GEN2 `0.3279856` vs legacy `0.328`. Complemento del anterior.
- `RES-0050` `participacion.concurrencia_presidencial_conversion:participa_p0_minimo` — veredicto sellado `LISTADO-PARA-MESA-REPRODUCE` y `RESULT-L8CONV-A-DELTA-VS-GEN1-MINIMO = 0.0` **exacto**. Aquí sí: falta el pin, no la corrida.
- `RES-0051` `…:participa_p0_maximo` — igual; `DELTA-VS-GEN1-MAXIMO = 0.0` exacto. Falta el pin.
- `RES-0052` `…:participa_p0_media` — igual; `DELTA-VS-GEN1-MEDIA = 0.0` exacto. Falta el pin.
- `RES-0047` `dinero.ahorro.horizonte_corto:horizonte_no_corto` — **CONFLICTO**: C1-MAPA fija `RESULT-ENIF-AHO-A-P-NOCORTO-SIN-P` (`CALC-ENIF-0001`) y C2-RESULTADO fija `RESULT-HVD-A-HORIZONTE-NO-CORTO-SIN-SS` (`CALC-HORIZONTE-VIA-DERIVADOS-0001`, `SELLO-NO-COINCIDE:AUSENTE`). Falta que mesa adjudique el canal; el registro no decide.
- `RES-0049` `dinero.ahorro.horizonte_no_corto_con_seguridad_social:horizonte_no_corto` — mismo conflicto, par `…-CON-P` / `…-CON-SS`, mismo sello ausente. Misma adjudicación.

**La nota sobre `GEN2-PISOS-REJILLA`, verificada por ola — NO sirve a esos slots.** `CALC-PISOS-ENVIPE2024-EJES-0001/0002` toman `envipe2024_csv` (**ENVIPE 2024**). Los consumidores `civico.denuncia.con_seguro` / `sin_seguro` de `RES-0039`–`0042` declaran `payload_manifiesto_id: envipe2025_csv` (**ENVIPE 2025**), universo `BPCOD='01' ∧ BP2_1∈{1,2} ∧ cobertura_seguro`, n=402 y n=614 de 1 016. **Ola distinta: no releva.** Y además el tipo no calza: esos CALC son `PISO-PERSISTENCIA-POR-EJE`, un piso de persistencia, no el punto de denuncia condicional a seguro. Dos razones independientes, ninguna supuesta.

---

## Lectura de auditoría — qué afirma esto sobre México

Nada nuevo. Este acto no midió: leyó procedencia. Los once deltas de `5.55e-17` a `4.79e-07` dicen que el motor GEN2 **reproduce el mismo cálculo** que la cifra legacy ya hacía — no que la cifra sea válida. Una cifra GEN2 idéntica a la legacy hereda intacto su estimando, su universo y sus sesgos: ENIF y ENVIPE sobre-representan población con contacto financiero e institucional, y `evasion_norma` (RES-0025/0026) es por **delito**, no por persona, con lo que «el 56% evade la norma» no se lee sobre personas. P2 existe para eso, y en RES-0028 atrapó exactamente el caso que buscaba: dos cifras a 2.7 pp que **no son la misma afirmación** porque una cuenta personas y la otra delitos.

Clase (a) en los 12. Ninguna cifra esperada: el 182 de partida y el 182 de salida se derivaron los dos.

Y la lectura simplista que hay que rechazar es la que este acto podría haber alimentado: **«bajamos el legacy» no es «el motor mejoró»**. Hoy no bajó nada, y eso tampoco significa que el motor empeorara. Lo que hay es trazabilidad: se sabe, slot por slot, de dónde sale cada número y quién tiene que firmar para que la autoridad numérica cambie de manos. La validez sigue siendo otra pregunta, y este acto no la tocó.
