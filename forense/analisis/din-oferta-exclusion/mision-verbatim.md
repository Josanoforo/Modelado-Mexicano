<!-- Copia íntegra de MISION-ASTRA-3-mide-lo-que-falta.md; texto original a continuación. -->
# MISION-ASTRA-3 · Tercer carril: lo que el programa ya sabe que le falta y nadie ha medido
**Dirección (Claude Fable), 23/sep/2026 · main `619748f5` al redactar (re-deriva al abrir) · para Jonás (mesa) y Astra (ChatGPT, decide); Codex ejecuta hasta cerrar, en CAJA cuando toque microdato · independiente de MISION-ASTRA-1 (`949a0f1a9c0054a9`, vencer al piso) y MISION-ASTRA-2 (`df2bbebf2312b720`, identificar un θ): no comparte celdas de evaluación, ni olas reservadas, ni candidatos con ellas.**

Reglas comunes a las tres unidades, las mismas cinco de los carriles 1 y 2 y nada más: (1) spec humana + `spec.yaml` congeladas en un commit anterior a cualquier lectura del dato que miden (verificable por `git log -p -S <sha del payload>`); (2) etiquetas completas en el `spec.yaml` — `cuenta_gen2`, `adopta: NO`, `origen_numerico` — o el CALC no cuenta; (3) asiento propio en `forense/replay-evidencia.tsv` en el mismo PR; (4) nada de tablero, celdas-D, `milpa/tramite.yaml` ni derivados de main: el recibo de Claude los consume; (5) ninguna ola reservada, ni sus tabulados: ENCIG 2025, ENVIPE 2025 (salvo los cruces que un piloto ya declaró consumidos, rotulados RETROSPECTIVA), ENVIPE 2026, ENIGH 2024 en lo no abierto por el duelo, ENCO 2025/2026. Cada unidad cierra con un recibo de Codex al estándar del 23/sep (`9a1df2da0fa7e436`): EJECUTADO / LEÍDO por frase. Cada cifra con su escala, su unidad (persona, hogar, trámite) y su generación; nada se promedia entre unidades.

---

## U1 · Exclusión por oferta en ENIF: la columna que la regla §3 exige y que ninguna serie de crédito tiene

**Objetivo.** Que exista, sellada y por ola, la medida de exclusión por oferta que acompaña a todo marginal de conducta de mercado: qué fracción del no-uso (crédito formal, cuenta/ahorro formal) se atribuye a razones del lado de la oferta (rechazo, requisitos, sin sucursal o corresponsal, costo) y qué fracción a preferencia (no lo necesita, desconfía, prefiere informal), por los mismos ejes que ya usan los pisos de crédito (sexo, edad, escolaridad, localidad, formalidad laboral). Termina en una familia de RESULT `P` con IC por diseño y una tabla de conmensuración entre olas.

**Antecedentes vigentes.** Instrucciones v2.16 §3: «Oferta antes que preferencia: todo marginal de conducta de mercado (crédito, ahorro, canal) se publica con la medida de exclusión por oferta al lado» — origen PRODUCTO-DINERO (#932, #943) y FP-404. Hoy en el árbol: **0** specs en `forense/prereg-caja/` y **0** CALC en `data/corrida0/` con ese estimando (búsqueda por texto de razones: «no me lo dan», «requisitos», «sucursal»; `ls data/corrida0 | grep -i 'OFERTA\|EXCLUS'` → 0). La serie de crédito 2012–2021 (`CALC-DIN-CREDITO-PISOS-ENIF2018-0001`, `…ENIF2021-RECORTE1870-0001`, `…K2-BANCARIA-HISTORIA-0002`) está sellada y su lectura (`GEN2-DIN-CREDITO-SERIE-LECTURA-1`, en cola) pregunta si publica «con la columna vacía y rotulada» porque esta medida no existe. Recorte de universo firmado: 18–70 (firma ff56-01 (a)). Frontera de conductas: FP-404 (2).

**Perímetro.** Propio: `forense/prereg-caja/DIN-OFERTA-EXCLUSION-ENIF-spec-v1_0.md` (+sidecar), `data/corrida0/CALC-DIN-OFERTA-EXCLUSION-ENIF<ola>-0001/` por ola, `tools/astra/enif/oferta/` (medidor), tests propios (huérfanos en CI), asiento en `replay-evidencia.tsv`, nota. Ajeno: los CALC de pisos de crédito (se citan por id, no se re-miden), `tramite.yaml`, el marcador, el informe.

**Datos autorizados.** ENIF 2012, 2015, 2018, 2021 (microdato desde CAJA, ids `enif_2012_bases_enif`, `enif_2015_enif_`, `enif_2018_enif_`, `enif_2021_enif_` en `data/manifiesto.yaml`). ENIF 2024: **cruce visto** por el lote ENIF2024 — entra solo como RETROSPECTIVA, rotulado así en cada RESULT, y nunca como primera ola de calibración. Cuestionarios y FD desde nube.

**Lo que decide Astra antes de abrir el dato, y queda escrito en la spec.** (a) La partición de razones en tres clases cerradas — OFERTA · PREFERENCIA · OTRO/NS — hecha **por texto de pregunta y opción en cada ola** (A.15: el nemónico cambia entre olas; una opción ausente en una ola es NO-COMPARABLE, no cero); (b) el denominador (no-usuarios de la conducta, persona 18–70, con factor de expansión); (c) qué pasa si una ola no permite la partición: se declara NO-CONSTRUIBLE para esa ola y se sigue con las demás; (d) el IC: bootstrap por diseño con las réplicas del instrumento cuando existan, y cuando no, se dice cuál se usó. Ninguna de esas cuatro se ajusta después de ver una cifra.

**Dependencias.** Ninguna corrida ajena en vuelo toca ENIF hoy (`git ls-remote --heads origin`, 23/sep: piloto 4 = ENVIPE; Astra 1/2 = ENCIG/ENVIPE/θ). `GEN2-DIN-CREDITO-SERIE-LECTURA-1` la consumirá cuando exista; no la espera.

**Criterio de terminado.** Un CALC sellado por ola construible, cada uno con `verify` = REPRODUCE, asiento, etiquetas; una tabla `forense/analisis/din-oferta-exclusion/conmensuracion-v1_0.tsv` que dice, por ola y eje, CONSTRUIBLE / NO-COMPARABLE / NO-CONSTRUIBLE con la cita de texto; y para cada RESULT de piso de crédito de la serie 2012–2021 una fila con el id del RESULT de exclusión que lo acompaña (o el rótulo de por qué no lo hay). Verificable: `ls -d data/corrida0/CALC-DIN-OFERTA-EXCLUSION-ENIF*` ≥ 3; `grep -c 'CALC-DIN-OFERTA-EXCLUSION' forense/replay-evidencia.tsv` = ese número.

---

## U2 · IC calibrado de persistencia para ENCIG: el ancho honesto que a ENCIG le falta

**Objetivo.** Que los pisos de ENCIG (ola anterior por eje) tengan un intervalo que refleje la varianza del cambio entre olas y no solo la muestral — lo que #1009 hizo para ENIF y que para ENCIG no existe. Termina en un parámetro por eje (τ̂² del cambio 2017→2019→2021→2023 y la regla de ancho que lo consume) sellado y reutilizable por el marcador y por el piloto 5, sin adoptarlo.

**Antecedentes vigentes.** ARBITRO-MARGINALES-1/2: cobertura de los pisos ENVIPE 0.53, ENIF 0.19, **ENCIG 0.00**; MARGINALES-ADOPCION-1 (#1002): «ENCIG veta». ENIF-IC-CALIBRADO (#1009): 32/32 cobertura con IC de 35 pp, firma F2 «ADOPTAR-CON-RESERVA-DE-ANCHO»; spec plantilla `forense/prereg-caja/ENIF-PERSISTENCIA-IC-CALIBRADO-spec-v1_0.md`; su diseño nació en NC `…MARGINALES-ADOPCION-1-c45c-02`. Cobertura se reporta con intervalo binomial, por celda y por conglomerado, y rotulada RETROSPECTIVA (v2.16 §4). El piloto 3 (`FALSADOR DÉBIL`) y ENCIG-SERIE-Y-TENDENCIA-1 (#972, `SALTO-SIN-EXPLICAR`) ya midieron que la persistencia en ENCIG falla por un salto de instrumento, no por muestra: la spec debe decir qué hace con ese salto (excluir el par que lo contiene, o modelarlo como componente aparte) **antes** de abrir el dato.

**Perímetro.** Propio: `forense/prereg-caja/ENCIG-PERSISTENCIA-IC-CALIBRADO-spec-v1_0.md` (+sidecar), `data/corrida0/CALC-ENCIG-PERSISTENCIA-IC-CALIBRADO-0001/`, medidor en `tools/astra/encig/ic_calibrado/`, tests propios, asiento, nota. Ajeno: `CALC-ARBITRO-MARGINALES-*` (se citan por id como oro de la ola anterior), el marcador, cualquier celda-D, el piloto 5 y su encargo.

**Datos autorizados.** ENCIG 2017, 2019, 2021, 2023 (ids `encig_2017_encig` … `encig_2023_encig`; microdato desde CAJA). ENCIG 2025: **prohibida por entero**, incluidos tabulados y comunicados; el único par ya visto (gobierno digital, edad×escolaridad, piloto 3) no se usa para calibrar. ENCIG 2011–2015 solo si la spec demuestra por texto que las preguntas son las mismas; si no, fuera y se dice.

**Dependencias.** Los RESULT de `CALC-ARBITRO-MARGINALES-*` para ENCIG como oro de 2023 (sellados, en main). Ninguna firma nueva para medir; sí una para adoptar, que no es de este carril.

**Criterio de terminado.** CALC sellado con `verify` = REPRODUCE, asiento y etiquetas; RESULT por eje: τ̂², ancho resultante y cobertura RETROSPECTIVA 2021→2023 con IC binomial por celda y por conglomerado; la nota compara con ENIF (35 pp) en la misma escala y declara qué tan ancho tendría que ser el IC para cubrir — si el ancho necesario es inútil, ese es el hallazgo y se rotula así. `adopta: NO`; la propuesta de adopción viaja en el recibo con las opciones que mesa firmó para ENIF.

---

## U3 · Error de persistencia de las seis celdas de formalidad (ENIF): cerrar dos deudas con una medición

**Objetivo.** Medir el error del piso de formalidad (ENIF 2021 → 2024) para las seis celdas que `CALC-PISOS-ENIF2021-FORMALIDAD-0001` dejó con piso sellado y error sin medir, con el mismo procedimiento que `CALC-PISO-PERSISTENCIA-ERROR-0001` aplica a las 53 celdas de la rejilla. Termina en seis RESULT de error con IC, rotulados RETROSPECTIVA-MECÁNICA (ENIF 2024 ya está vista; no hay selección de variante).

**Antecedentes vigentes.** NC-0414 («el error de persistencia de las 6 celdas nuevas no se mide; …0001 cubre 53 celdas y no estas» — sucesor: «CALC nuevo, nube») y NC-0431 («medir el error de persistencia de las 6 celdas de formalidad»), ambas ABIERTAS, con FP-396 FIRMADA (cuenta_gen2 del piso de formalidad). Spec del piso: `forense/prereg-caja/PISOS-ENIF2021-formalidad-spec-v1_0.md` + `…-metadatos-v1_0.tsv`. Procedimiento de referencia: la spec sellada de `CALC-PISO-PERSISTENCIA-ERROR-0001` (se cita; el sello cubre el código que mide, no se copia a mano sin decirlo).

**Perímetro.** Propio: spec humana propia (o extensión declarada de la del 0001, con lo que hereda verbatim), `data/corrida0/CALC-PISO-PERSISTENCIA-ERROR-FORMALIDAD-0001/`, medidor, asiento, nota; cierre de NC-0414 y NC-0431 citando el CALC. Ajeno: el piso 0001 (input por id y sha), el marcador, celdas-D.

**Datos autorizados.** RESULT sellados del piso (input por hash) y ENIF 2024 como R (ids `enif_2024_enif_`; microdato desde CAJA, cruce visto → RETROSPECTIVA-MECÁNICA). Nada más.

**Dependencias.** Ninguna en vuelo. Si el procedimiento del 0001 exige una réplica de diseño que ENIF 2024 no trae para el corte de formalidad, la spec declara la alternativa antes de correr y el RESULT lleva el apellido del instrumento.

**Criterio de terminado.** Seis RESULT de error con IC sellados (`verify` = REPRODUCE, asiento, etiquetas), unidad persona 18–70, escala en pp; NC-0414 y NC-0431 CERRADAS en el mismo PR con el id del CALC; ninguna adopción.

---

## Lo que este carril NO hace
No abre careos ni pilotos; no evalúa candidatos contra R reservada (eso es ASTRA-1); no calibra θ ni `corte_pi` (ASTRA-2); no toca CI, `check.py`, `verify.yml`, el tablero ni los derivados de main (tubería); no hace inventarios; no adopta nada. Si una unidad descubre que su premisa es falsa (una pregunta no existe, un procedimiento no aplica), el entregable es decirlo con cita y conteo — igual vale.

## Recibo
Cada PR entra por `GEN2-RECIBO-ASTRA-N` (Claude): etiquetas, orden spec→dato por historial, asiento, perímetro, olas. Lo que cumple, mesa lo fusiona; lo que no, se devuelve con la razón por comando. La adopción de U1–U3 al marcador o al informe es firma de mesa aparte, con el nombre de Astra en el ADR.
