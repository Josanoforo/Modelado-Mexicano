# Expediente de apertura · ENIF 2024 · cruces reservados de `informal_cualquiera` · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), pieza ENIF-2024 (subagente), sobre `7393b17e`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: entorno NUBE, sin
corpus; ningún microdato, tabulado ni comunicado de ENIF 2024 se leyó. Las celdas siguen RESERVADA
(E.6); las levanta el código congelado de este expediente, en caja, en el commit que mesa autorice, o
mesa por escrito.

## 0 · Premisas

- [EJECUTADO] `data/corrida0/marcador-segmento.tsv` (csv.DictReader, tab, sin líneas `#`): 327 filas,
  19 con `estado = RESERVADA`: ENIF 2024 14 (9 `emision = EMITIDA-SIN-EVALUAR`,
  `decision_ref = emision:c2-compuesto-reservadas`; 5 sin emisión), ENVIPE 2025 4, ENUT 2024 1.
  Los 9 ids de este expediente: `CRUCE-GRUPO::dinero.ahorro.via_informal_ejes_enif2024::<par>` con
  `<par>` ∈ {cuenta_formalxedad, cuenta_formalxescolaridad, cuenta_formalxlocalidad, cuenta_formalxsexo,
  edadxescolaridad, edadxsexo, escolaridadxlocalidad, escolaridadxsexo, localidadxsexo}.
- [EJECUTADO] **Premisa corregida**: el piso no está en las columnas del marcador — las 19 filas RESERVADA
  traen `piso_tipo = SIN-PISO` y `piso`, `piso_ic95` vacíos (`tools/marcador_segmento.py:1172`). El piso
  de un cruce es el compuesto de marginales de la misma ola sin interacción (v2.16 §4, instrucciones
  l. 40): es **el propio contendiente** C2 (las 52 celdas `ADOPTADO-POR-FIRMA` del marcador llevan
  `piso_tipo = MARGINAL-SIN-INTERACCION` con `M` = C2; en el precedente
  `RESULT-DIN-LOTE24-ADJ-EDADXSEXO-C2-ROL = PISO`).
- [EJECUTADO] **Premisa caída a medias**: cada fila del marcador agrupa dos desenlaces. Para el PRINCIPAL
  `ahorra_solo_informal` (68 celdas), R ya está sellada: `CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001`
  (`ejecucion.json` 2026-09-22T02:19:11Z) publica `…-R-<celda>-P` en los 14 pares y su C2 coincide con
  el punto de `CALC-C2-COMPUESTO-RESERVADAS-0001` a 1e-4 pp. E.5: lo sellado se cita, no se re-mide; E.6:
  un cruce visto no se relanza. **Fuera de este expediente** (sucesor, §5).
- [EJECUTADO] Para el SECUNDARIO `informal_cualquiera` (68 celdas) **ninguna R de cruce está sellada**:
  de 390 carpetas `data/corrida0/CALC-*`, 16 `spec.yaml` nombran `informal_cualquiera|INFORMAL-CUALQUIERA`;
  ninguna agrupa dos ejes (marginales, persistencia, región, NSE; `CALC-C2-COMPUESTO-IC-ENIF2024-0001`
  declara `G-CRUCE-DERIVADO = NO`), y ninguna clave de `resultados.json` de otro CALC es de celda de cruce
  de ese desenlace. NO-ENCONTRADO (A.4) con ese universo y ese patrón.
- [LEÍDO] Contendientes sellados (regla 6, MEMORIA §1 l. 10: ningún contendiente nuevo): el piso C2,
  punto en `CALC-C2-COMPUESTO-RESERVADAS-0001` (2026-09-19T22:17:43Z) e IC95 por réplica en
  `CALC-C2-COMPUESTO-IC-ENIF2024-0001` (2026-09-20T03:23:54Z; 136 celdas con IC, 0 no construibles;
  controles 1 y 2 `REPRODUCE`). Ningún retador sellado para `informal_cualquiera` en estos pares: los
  retadores del lote (P2, R1, R2, R3, L1, L2) son sólo de `ahorra_solo_informal`
  (`CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001/spec.yaml:517`).
- [LEÍDO] Payload: `enif_2024_enif_2024_bd_csv` (`TMODULO.csv`), el que leyeron el árbitro y el contendiente;
  sin `estado_reserva` en el manifiesto: la reserva es **de celda** (marcador), no de archivo.
- Fuera de este expediente, **sólo mesa por escrito**: las 5 filas RESERVADA sin emisión (formalidad:
  `cuenta_formalxformalidad`, `edadxformalidad`, `escolaridadxformalidad`, `formalidadxlocalidad`,
  `formalidadxsexo`; C2 NO-EMITIBLE por universo restringido, A-bis 4) — sin contendiente sellado que la
  espere; y la reserva de **ENIF 2024 módulo 7** (firma R06, `forense/encargos/2026-09-28-GEN2-TRAMITE-FIRMAS-21-ADENDA-1.md:11`):
  este medidor no nombra ninguna columna del módulo 7 y las descarta al leer (§3).

## 1 · Estimandos

Por cada una de las 68 celdas de `CELDAS_AUTORIZADAS` (9 pares × categorías de la rejilla del árbitro):
**R(a,b) = Σ FAC_PER·y / Σ FAC_PER** sobre las personas de la celda, con
`y = informal_cualquiera` = alguna `P5_1_1..P5_1_6 == "1"` (`desenlaces()` del árbitro,
`tools/medidor_ahorro_enif24.py`, sha256 `58c42959…`, el mismo que fijó el contendiente). Ejes del
árbitro: sexo (`SEXO`), edad (`EDAD_V` en 18-29/30-44/45-59/60+, 60–96; 97+ fuera), escolaridad (`NIV` por
`ESC_ENIF`; 99 fuera), localidad (`TLOC` {1,2} = 15 000 y más, {3,4} = menor de 15 000), cuenta_formal
(alguna `P5_4_k == "1"` vs ninguna; todas en blanco fuera). Id de celda = `<PAR>-<slug(a)>-X-<slug(b)>`,
la regla de `tools/c2_compuesto.py::_slug` que acuñó los ids sellados.

## 2 · Universo, unidad, ponderador, diseño

Unidad **persona elegida de 18 años y más**. Universo = el de `carga()` del árbitro, que es el del
contendiente: todas las filas de `TMODULO.csv` con `EDAD_V` numérica ≥ 18, `FAC_PER` > 0 y alguna de las
15 variables de la sección 5 no en blanco; cualquier violación **PARA** (`ParoDeGuardia`). Diferencia con
el precedente del lote (régimen PILOTO-1: edad ≤ 97, `TLOC` ∈ 1..4): se sigue el universo **del candidato**
(A-bis: un estimando se compara contra el candidato en su mismo universo), declarado.
Ponderador `FAC_PER`. R es un punto; no se calcula IC de R (la cobertura se mide contra el IC del piso).
**Soporte**: celda con n < 200 personas sin ponderar → R NO-ESTIMABLE, no puntúa (umbral del precedente,
`forense/prereg-caja/DIN-lote-enif2024-spec-v1_0.md:175`, `CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001/spec.yaml:163`).
Tras leer, sólo sobreviven las columnas de §1 más `FAC_PER`, `EST_DIS`, `UPM_DIS` y `P5_6_*` (guardias
del árbitro); el resto de `TMODULO.csv` se descarta sin agregarse.

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo`, llamado **una vez por par** con UNA variable de
agrupación: la etiqueta de celda ya construida (`etiquetas_de_par`); una persona con algún eje `(fuera)` o
una etiqueta que no esté en `CELDAS_AUTORIZADAS` recibe `None` y no se agrega. `r_por_celda` levanta
`ParoDeGuardia` si se pide una celda fuera de la lista cerrada (p. ej. de `ahorra_solo_informal` o de
formalidad). Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo; `groupby`/
`value_counts` con dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack` o una lectura fuera de
`lee_payload_reservado` → PARO. Probado por mutación (las 9 de `expediente_apertura.MUTACIONES`, más una
corrida de `medir()` con el archivo mutado que PARA sin tocar el payload) en `tests/test_apertura_enif_2024.py`
y `tests/test_prereg_aperturas.py`.

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

**Regla de v2.16 §4 (instrucciones l. 42) y precedente de la ola.** La comparación primaria entre piso y
retador es `Δ = MAE(piso) − MAE(retador)` en pp con IC por réplica; el precedente sellado de ENIF 2024 fija
umbral **0.5 pp** y vocabulario **VENCE-RETADOR** (IC95 inferior > 0.5) · **PROPUESTA-CON-RESERVA**
(0 < inferior ≤ 0.5) · **NADIE-VENCE** (incluye 0)
(`forense/prereg-caja/DIN-lote-enif2024-spec-v1_0.md:181-194`;
`CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001/spec.yaml:515-517`). **Aquí esa fila no la ocupa nadie**: el único
contendiente sellado es el piso, no hay retador sellado para `informal_cualquiera` en estos pares y la regla
6 veda crearlo. Se dictamina ahora, antes de abrir: **ΔMAE primaria = NADIE-OCUPÓ-LA-FILA** («nadie corrió
el mecanismo», §2; no es una derrota de nadie). Si mesa autoriza un retador sellado antes de la apertura,
este expediente sale v1_1 **antes** de abrir, con la regla del precedente verbatim.

**Medición primaria de la apertura** (una sola): cobertura del piso, «R dentro del IC del candidato»
(v2.16 §4, l. 43): celda puntuada si lo, hi del piso y R son finitos; k/n = #celdas con lo ≤ R ≤ hi, con
IC de Wilson al 95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si 0.95 ∈ Wilson; **SUBCUBRE** si
Wilson_hi < 0.95; **SOBRECUBRE** si Wilson_lo > 0.95; **NO-ESTIMABLE** si n = 0; si dos filas pudieran
satisfacerse a la vez manda NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE > CALIBRADO (excluyentes por
construcción). Secundarias, descriptivas, no adjudican: error absoluto medio punto-del-piso vs R (escala
proporción) y cobertura por conglomerado (par: las celdas de un par comparten muestra), derivable de las R
por celda y del IC sellado. B-bis: CALIBRADO = piso **corroborado en alcance** para estas 68 celdas;
SOBRECUBRE = piso **acotado** (IC conservador); SUBCUBRE = el supuesto sin-interacción no anticipa el cruce.
Una apertura sirve a todos los sellados antes: los dos CALC del piso son los únicos que la esperan.

## 5 · Diferencias y lo que queda fuera (se declaran, no se corrigen)

- `ahorra_solo_informal` × 9 pares (68 celdas): R sellada en `CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001`;
  su evaluación contra el piso ya está allí (`…-C2-ERROR-PP-*`, `…-C2-R-DENTRO-IC-CAND-*`). No se reabre.
- Información parcial: `ahorra_solo_informal ⊂ informal_cualquiera`, y la primera ya se vio por celda
  (22/sep). Los contendientes se sellaron el 19–20/sep, antes: la marca PROSPECTIVA se sostiene por orden de
  sellos; ninguna selección posterior tocó la emisión.
- Columna ausente o con códigos distintos en el FD de 2024 (preflight documental, receta §3): esa celda
  sale NO-ESTIMABLE; no se recodifica ad hoc.

## 6 · Salidas

`RESULT-APERTURA-ENIF-2024-<celda>-R` (68, proporción, NO-ESTIMABLE permitido), `-DICTAMEN`, `-K`, `-N`,
`-WILSON-LO/HI`, `-MAE-PUNTO`, `-MARCA` (= PROSPECTIVA). Ningún None/NaN fuera de R de celdas sin soporte,
Wilson y MAE cuando n = 0. Contrato `APERTURA-ENIF-2024-spec.yaml` (calc_id `CALC-APERTURA-ENIF-2024-0001`;
payload con sha del manifiesto; árbitro, sus dos dependencias, los dos `resultados.json` del piso, la guardia
y la plantilla como inputs `origen: repo` con sha). La apertura es copiarlo a
`data/corrida0/CALC-APERTURA-ENIF-2024-0001/spec.yaml` y correr (receta).

## 7 · Módulo de auditoría (v2.16)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA: el piso se selló (19–20/sep) antes de que exista R de `informal_cualquiera` por cruce; ninguna
  frase mezcla esta cobertura con la RETROSPECTIVA del lote.
- Unidad: **persona elegida 18+** en R y en el piso; nada se promedia con hogar, delito o trámite.
- Escala: proporción 0..1 en R y en el piso; se compara «R dentro del IC del piso», no punto contra punto.
- Oferta antes que preferencia (§3): ahorrar por vía informal convive con exclusión por oferta (sin cuenta,
  localidad < 15 000); el eje `cuenta_formal` es medida de acceso, no de preferencia, y así se lee.
- Segmentación: cruces de dos ejes de estructura (edad, sexo, escolaridad, tamaño de localidad, cuenta);
  la rejilla no ve región, condición indígena ni clase — límite declarado; el sesgo de clase media urbana no
  se corrige aquí.
- Qué sería peligroso leído simplista: un SUBCUBRE no dice que «el mexicano ahorra informal por cultura»;
  dice que el compuesto sin interacción no anticipa la celda — la interacción puede ser de oferta.
- Cifras escritas a mano: ninguna; las constantes son hashes fijados, la lista cerrada (probada contra el
  `resultados.json` sellado) y los umbrales de la regla (0.95, z = 1.959964, n ≥ 200).
