<!-- CABECERA DE PROCEDENCIA · añadida por ACTO GEN2-CELDA-D-CAREO-1 (A.3).
     El cuerpo que sigue a la línea de guiones es VERBATIM: no se editó una coma.
     Esta cabecera es del archivo, no del documento. -->

> **PROCEDENCIA (A.3 · archivo verbatim)**
> - **Clase:** INSUMO DE DIRECCIÓN tipo 3 — no entra al canon sin un acto de verificación posterior.
> - **Autor:** Dirección (Fable)
> - **Fecha nominal:** 17/sep/2026 · **fecha de archivo:** 2026-09-16 (fecha de ejecución del entorno; las dos se conservan, no se infiere una firma futura).
> - **sha256 del cuerpo verbatim, verificado por comando en este acto:** `c7d55e61bdf929c099f9c0a97c5ff3695f0749be11636cc903af715de893b8b8`
>   — coincide con el prefijo `c7d55e61bdf929c0…` que el encargo declara.
>   Comando: `sha256sum <adjunto>` antes de copiar, y `sha256sum` del cuerpo extraído después.
> - **Archivado por:** `ACTO GEN2-CELDA-D-CAREO-1`, encargo `forense/encargos/2026-09-17-GEN2-CELDA-D-CAREO-1-TRES-DISENOS-UN-CAREO.md`, P0.
> - **Nota:** Diseño ciego de dirección, escrito sin leer el retorno de Astra ni la nota de Opus (#823). HISTORIA: superado por el v1.1 post-careo; no se edita.

---

# CELDA-D-PILOTO · Diseño de dirección · v1.0 · CIEGO
**Dirección (Fable) → careo · 17/sep/2026 · derivado contra `Josanoforo/Modelado-Mexicano @ b881ee6` (merge de #820) con comando a la vista.**

**Qué es.** La propuesta de dirección para el primer piloto celda-D bajo la firma de mesa del 16-17/sep (*"cada celda tiene su estimador, su ruta y su dato"*). Escrita **sin leer** el retorno de Astra sobre el mismo encargo; se carea contra él en `GEN2-CELDA-D-CAREO-1`. No es encargo, no es pre-registro sellado, no adjudica nada: es el objeto que el careo compara.

**Procedencia (v2.1).** Todo lo citado `archivo:línea` se leyó del clon en esta sesión. Dos afirmaciones vienen de adjuntos fuera del repo (D-θ v1.1, sha256 `8a6472a7…`) y se marcan [ADJ]. Ninguna cifra de este documento entra al canon: las proporciones citadas son las del árbitro ya sellado y se reproducen para nombrar celdas, no para comparar.

---

## 0 · Qué decide este diseño y qué no

Decide: **qué celda-D corre primero**, con qué candidatos, bajo qué criterio declarado antes del dato, y qué cuenta como éxito. No decide: ningún número del modelo; la forma de `G5 × familismo_obligacion`; la forma de `h_r` para ninguna regla; ninguna adopción al motor (eso es merge de mesa); ni la política general de adjudicación multi-celda (eso es lo que el piloto enseña).

## 1 · Elección de la celda — tabla de eliminación

**Universo examinado** (comando y conteo, A.4/A.13): las 3 celdas-D registradas (`data/curacion-registro/celdas-d/*.yaml`, 3 archivos); las 7 entradas del árbitro con puntos **por eje** (`milpa/tramite-ola5-propuesta-v0.yaml`, patrón `- id: *_ejes_*`, líneas 1415, 1595, 1667, 1759, 1993, 2041, 2089, 2159 examinadas); el catálogo de momentos (`milpa/catalogo-momentos-v0_1.tsv`, 22 filas, todas `NO-VERIFICADO`, 8 `AJUSTE` + 14 `HOLDOUT` con instrumento `POR DECLARAR`); la demanda activa (`data/corrida0/demanda-resultados.tsv`, 207 filas: 42 `conducta_p_medido` con consumidor en `tramite.yaml`); el crosswalk (`data/crosswalk-ejes-arbitro-modelo-v1_0.tsv`, 15 filas); el manifiesto (`data/manifiesto.yaml`, 22 entradas ENIF: olas 2012/2015/2018/2021/2024).

**Siete criterios**, todos necesarios: (a) estimando con escala y universo declarados; (b) población expresable en cortes del modelo **y** en celdas del árbitro (vía crosswalk), o al menos en celdas del árbitro para candidatos que no necesitan cortes del modelo; (c) dato ya adquirido y registrado en el manifiesto — **incluida la ola anterior** para persistencia; (d) ≥2 candidatos elegibles de familias distintas; (e) persistencia construible (misma serie, mismo reactivo); (f) consumidor identificado en la demanda; (g) evaluación no vista por el candidato que se evalúa.

| candidata | falla | evidencia |
|---|---|---|
| `G5.familismo_obligacion.actitud` (celda-D) | (d): un solo candidato, "nada que comparar" | `celdas-d/G5.familismo_obligacion.actitud.yaml:68` |
| `G5.obligacion_medida.conducta` (celda-D) | (d), (f): un candidato; ningún coeficiente se llama así | `…obligacion_medida.conducta.yaml:110,124` |
| `G5.radio_confianza.encuci_vs_enbiare` (celda-D) | (e), (f): es un insumo θ, no una conducta; sin serie; su consumidor es un coeficiente `ASIGNADO SOLO-SIGNO` | `…encuci_vs_enbiare.yaml:25,163`; `modelo-decision-v4_0.md:466` |
| `tramite.evasion_norma × dominio` (ENVIPE 2025) | (b) para la matriz: `dominio` NO-EQUIVALENTE a `urbanizacion`, sin mapeo construible; unidad = DELITO | crosswalk fila `dominio_urbano_rural`; FP-376 (2) |
| `tramite.gobierno_digital.util_sin_coercion` (ENCIG 2025) | (b): ejes `sexo/edad/escolaridad` sin corte del modelo; unidad = TRÁMITE | crosswalk filas `sexo`, `escolaridad`, `edad`; `tramite-ola5-propuesta-v0.yaml:1595` |
| `civico.denuncia.con_seguro` (ENVIPE 2025) | (b): `cobertura_seguro` es el seguro del vehículo, no un corte | crosswalk fila `cobertura_seguro` |
| `familia.union.libre × cohorte` (EDER 2017) | (c),(e): una sola ola; panel retrospectivo sin serie comparable | `tramite-ola5-propuesta-v0.yaml:1993` |
| `familia.cuidado.reparto_mujeres40` (ENUT 2024) | (b),(e): 1 celda de unidad HOGAR; sin ola anterior comparable en manifiesto | crosswalk fila `reparto_hogar` |
| `dinero.ahorro.horizonte_corto × formalidad` (ENIF 2024) | pasa (a)–(g) pero con **un solo eje** mapeable | `tramite-ola5-propuesta-v0.yaml:2159` |
| **`dinero.ahorro.via_informal` (ENIF 2024)** | **pasa (a)–(g)**: dos ejes mapeables (`formalidad`, `localidad`, ambos MAPEO-N-A-1), cinco olas en manifiesto, ≥3 familias de candidatos, consumidor real, dominio DIN **fuera de U3** (nunca visto por L en F5) | `tramite-ola5-propuesta-v0.yaml:1415-1440`; `tramite.yaml:1306`; crosswalk filas `formalidad`/`localidad`; manifiesto `enif2021_csv`, `enif2024_csv` |

**Ganadora: `dinero.ahorro.via_informal`, desenlace `ahorra_solo_informal`** ("alguna P5_1_1..P5_1_6 == 1 y ninguna P5_6_1..P5_6_9 == 1", `tramite-ola5-propuesta-v0.yaml:1426`). Segunda: `dinero.ahorro.horizonte_corto` (misma tabla, mismo instrumento — candidata natural al segundo piloto, no al primero). Reserva sobre (g): las celdas del árbitro en ENIF 2024 **ya fueron observadas por dirección** el 2/sep (`ACTO MAESTRA35-L1`); no por L. Se declara en §2.8, no se esconde.

## 2 · Pre-registro de la celda (borrador, contrato v0.5)

### 2.1 Estimando, población, unidad
- **Estimando:** `p(ahorra_solo_informal | x)` — proporción ponderada `[0,1]` de personas elegidas de 18+ que ahorran por alguna vía informal y por ninguna formal. Escala: proporción; **no** se compara contra ningún índice ni coeficiente sin función de enlace (A-bis 3).
- **Población objetivo:** personas 18+ residentes en viviendas particulares (ENIF), en **diez celdas del árbitro** organizadas en cuatro ejes: `formalidad` {sin seguridad social, con seguridad social} — **universo restringido a quien trabaja** (`P3_13` ≠ blanco/9; cobertura 0.689676), declarado y no reconciliable contra el marginal poblacional (A-bis 4) · `localidad` {<15 000, ≥15 000} · `edad` {18-29, 30-44, 45-59, 60+} · `sexo` {hombre, mujer}. Solo `formalidad` y `localidad` tienen corte del modelo (MAPEO-N-A-1, FP-376 pendiente de firma); `edad` y `sexo` son celdas del árbitro sin corte, válidas para candidatos que no necesitan cortes.
- **Unidad:** persona. **Árbitro R:** las diez celdas con IC95 bootstrap ya selladas en `tramite-ola5-propuesta-v0.yaml:1415-1480` (FAC_PER, EST_DIS/UPM_DIS, 10 000 réplicas, seed 42). R **no** es candidato: es la vara.

### 2.2 Candidatos (cuatro; uno entra como inejecutable, y eso es entregable)

**C1 · `BASELINE_INGENUO` · b_persistencia (ENIF 2021).** Mismo desenlace, misma definición, mismas celdas, sobre la ola anterior. Construibilidad: el inventario canónico lista los catálogos `p5_1_1`…`p5_6_1` de ENIF 2021 (`data/inventario-reactivos-v1_2.tsv`, 214 filas `enif2021` con `P5_`); **A.15c: la equivalencia de códigos se verifica por archivo antes de congelar**, incluidos `P3_13` y `tloc` en 2021. Estrategia: `transversal_con_seleccion` con `regla_composicion: identidad temporal (p_2021 → p_2024)`. *Hueco de vocabulario declarado:* "persistencia" no está en el enum `estrategia` de v0.3 §3; se registra como falsador del vocabulario (v0.4 §3), no se inventa un valor.

**C2 · `CHALLENGER` · L, dos variantes (`variante_corredor: L-solo | L+corpus`).** Elicitación ciega de las diez proporciones con intervalo de 80 % declarado por el propio L, bajo el protocolo ADV1 (marco + filtros, scoring propio, `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B). Control de memoria obligatorio: ENIF 2024 se publicó en 2025; se verifica por búsqueda qué cifras nacionales y por sexo circularon, y las celdas cuya cifra sea pública se marcan `CONTROL-MEMORIA`, no `PUNTUADA`.

**C3 · `CHALLENGER` · matriz `B·θ(x) → h_r`, `estrategia: momentos`.** Entra con **`resultado: INEJECUTABLE`** y la lista exacta de lo que le falta para competir en **esta** celda — que es el entregable de M1 en el piloto: (i) `h_r` para `dinero.ahorro.via_informal` no existe ("OLA futura", `milpa/src/emisor.py:364`; `matriz.py:23-31`); (ii) `G3.horizonte_temporal` está bajo `GATE·ID-X`, "inalcanzable por construcción" (`milpa/procedencia.yaml:1116`); (iii) `G3.aversion_riesgo` `SIN-RUTA` (`procedencia.yaml:1172`); (iv) `G3.familismo_apoyo` tiene β̂ marginal `0.0279` con enlace identidad (`modelo-decision-v4_0.md:466`) pero su θ **por celda de formalidad** debe leerse de las corridas estratificadas del 4/ago (ADR-57(a): condicionar invirtió el signo) — a verificar, no a asumir. La regla del contrato: la matriz "gana o pierde esa celda por el mismo criterio que cualquier otro challenger, no por adopción arquitectónica previa" (`propuesta-motor-adaptativo-celda-v0_3.md` §4). Hoy no puede ni presentarse; el piloto lo escribe con nombre y apellido.

**C4 · `COMPLEMENTO` · emisor M (snapshot de reglas, x = ∅) · `resultado: NO-APLICA`.** No compite: su `p` nacional se midió sobre ENIF 2024 (`RES-0057/0058`, `CORR-0009`), la misma ola que el árbitro — sería circular — y con x = ∅ es una constante en las diez celdas. Se reporta como **diagnóstico**: cuánto pierde una `p` nacional al bajar a segmento (|p_nacional − p_celda| por celda). Es la misma lectura que ya hizo `MARCADOR-C0-D` y aquí queda cuantificada en un dominio nuevo.

### 2.3 Criterio de adjudicación (antes del dato)
- **Por celda:** error absoluto en puntos porcentuales contra R. `INDECIDIBLE` si se cumple **cualquiera** de las dos condiciones del programa, citadas verbatim: *"si ambos caen dentro del IC de R o si |d_L−d_M| < 0.5·EE(R)"* (`CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B, M3; aquí los dos son C1 y C2). `PUNTUADA` si no. `CONTROL-MEMORIA` según §2.2. Escala de decidibilidad: pp; EE(R) = (IC95 sup − inf)/3.92.
- **Skill:** `skill = 1 − MAE/MAE(b)` sobre las celdas `PUNTUADA` (M3 del careo). Se reporta; **no** adjudica por sí solo.
- **A nivel celda-D:** un candidato **gana** solo si vence a b en ≥ 8 de las celdas `PUNTUADA` y las `PUNTUADA` son ≥ 8 de 10. Cualquier otro resultado → `estado_decidibilidad: INDECIDIBLE` a nivel celda-D, y el piloto es **factibilidad**, no desempeño. Sin valor-p: las diez celdas salen de una misma muestra y no son independientes; se dice.
- **Precedencia (B-bis):** si dos filas pueden satisfacerse a la vez, manda `INDECIDIBLE`.

### 2.4 Qué significa que nadie refute a b (B-bis)
Si ningún challenger gana: **persistencia corroborada como piso en dominio DIN**, y L no añade valor a nivel segmento en esta celda. Es el resultado *más* informativo para el informe ("valor por demostrar" deja de ser frase y pasa a tener un dominio con dato), no un fracaso. Se declara antes de correr para que nadie lo lea como tal.

### 2.5 Incertidumbre, tipada por candidato (D-θ v1.1 §5 [ADJ])
| objeto | contiene | tipo |
|---|---|---|
| R (árbitro) | error de muestreo, bootstrap de conglomerados | IC muestral |
| C1 b_persistencia | error de muestreo de 2021, misma receta | IC muestral |
| C2 L | intervalo de elicitación declarado por L (80 %) — **no** es IC; su cobertura empírica se mide contra R y se reporta | intervalo de elicitación |
| C3 matriz | n/a (inejecutable) | — |
| C4 emisor | ninguna (constante diagnóstica) | — |

Ninguna banda universal; ninguna suma de anchuras.

### 2.6 Emitir ≠ decidir
El piloto **emite** las diez estimaciones de cada candidato con su intervalo, aunque un intervalo cruce el valor nacional. Para el consumidor (`tramite.yaml:1306`, que hoy lee una `p` nacional), la pregunta útil es **el signo de la modulación por x**: ¿la celda está por encima o por debajo del nacional? Decisión **estable** si todo el intervalo del candidato ganador queda del mismo lado del nacional que R; **ambigua** si cruza; **fuera de soporte** si la celda tiene n < 200 en 2021 (ninguna lo tiene en 2024: mínimo n = 2 896). Ningún resultado se adopta al motor por este acto.

### 2.7 Universo de la estampa (A.10)
SHA `b881ee6`; instrumentos: ENIF 2021 y 2024 (`enif2021_csv`, `enif2024_csv` en manifiesto, ambos con FD); celdas: las diez de §2.1; corpus para L+corpus: el mismo de F5 (`construye_corpus_f5_v2.py`) sin ENIF 2024. Denominador de celdas del árbitro disponibles: 74 (crosswalk, columna `n_celdas_total_arbitro`); este piloto cubre 10.

### 2.8 Desarrollo vs evaluación — dicho sin adorno
- **Desarrollo:** ENIF 2021 (C1), corpus y priors (C2). Nada para C3.
- **Evaluación:** las diez celdas de ENIF 2024, **ya publicadas en el árbitro y ya vistas por quien escribe este diseño** (2/sep). No vistas por L (verificar por control de memoria). Mitigación, la única honesta: las celdas son las que el árbitro ya selló — no se eligen aquí —, los candidatos y el criterio se congelan en COMMIT-1 antes de calcular nada, y el primer resultado que produzca el procedimiento es el que se reporta. Consecuencia: **el piloto es factibilidad por diseño**; solo pasaría a desempeño con una celda no vista, que hoy no existe en este dominio.

### 2.9 Parada
- **Factibilidad cumplida** si: C1 calculado con cadena GEN2 completa (spec → CALC → RESULT sellado); C2 elicitado a ciegas y puntuado; C3 asentado como `INEJECUTABLE` con sus cuatro faltantes nombrados; C4 cuantificado; adjudicación por celda escrita; **una entrada del catálogo de momentos** poblada con estimador adjudicado (la primera con `estatus_disponibilidad ≠ NO-VERIFICADO`); y el consumidor puede leerla sin cambiar código.
- **Desempeño** solo bajo §2.3, y solo se llama así si además existe evaluación no vista (hoy no).

### 2.10 Borrador YAML (v0.5)
```yaml
celda_d:
  id: DIN.ahorro_solo_informal.enif2024.x10
  estimando: "p(ahorra_solo_informal | x) -- proporcion ponderada [0,1], personas 18+ (ENIF, TMODULO, FAC_PER)"
  tipo_adjudicacion: COMPARACION
  dominio: FIN
  poblacion_objetivo: "10 celdas del arbitro: formalidad{2, universo trabajadores}, localidad{2}, edad{4}, sexo{2}; ver diseno §2.1"
  unidad_objetivo: persona
  universo_candidatos: "barrido 17/sep/2026 @ b881ee6 sobre demanda (207), catalogo (22), celdas-D (3), arbitro _ejes_ (7), manifiesto ENIF (22)"
  candidatos:
    - {rol: BASELINE_INGENUO, fuentes: [ENIF], edicion_periodo: "2021", universo_instrumento: "personas 18+ elegidas, TMODULO 2021", diseno_datos: transversal, estrategia: transversal_con_seleccion, regla_composicion: "identidad temporal p_2021 -> p_2024 (declarada 2026-09-17)", production_spec_refs: [], resultado: NO-EJECUTADO}
    - {rol: CHALLENGER, variante_corredor: L-solo, fuentes: [L], edicion_periodo: "elicitacion 2026-09", universo_instrumento: "memoria del modelo hasta su corte; control de memoria obligatorio", diseno_datos: transversal, estrategia: composicion, regla_composicion: "protocolo ADV1 marco+filtros", production_spec_refs: [], resultado: NO-EJECUTADO}
    - {rol: CHALLENGER, variante_corredor: L+corpus, fuentes: [L], edicion_periodo: "elicitacion 2026-09", universo_instrumento: "idem + corpus F5 sin ENIF 2024", diseno_datos: transversal, estrategia: composicion, regla_composicion: "protocolo ADV1", production_spec_refs: [], resultado: NO-EJECUTADO}
    - {rol: CHALLENGER, fuentes: [matriz_B, procedencia.yaml], edicion_periodo: "n/a", universo_instrumento: "n/a", diseno_datos: transversal, estrategia: momentos, regla_composicion: "B·theta(x) -> h_r (h_r inexistente)", production_spec_refs: [], resultado: INEJECUTABLE}
    - {rol: COMPLEMENTO, fuentes: [emisor, tramite.yaml], edicion_periodo: "2024", universo_instrumento: "p nacional ENIF 2024 (RES-0057/0058) -- circular, x vacio", diseno_datos: transversal, estrategia: composicion, regla_composicion: NO-APLICA, production_spec_refs: [], resultado: NO-APLICA}
  criterio_adjudicacion: {texto: "error absoluto por celda vs R; INDECIDIBLE si ambos caen dentro del IC de R o si |d_1-d_2| < 0.5·EE(R); gana quien vence a b en >=8 de >=8 PUNTUADA; precedencia: INDECIDIBLE", escala: "puntos porcentuales; EE(R)=(IC95sup-IC95inf)/3.92"}
  estado_decidibilidad: NO-APLICA        # se escribe al adjudicar
  margen_material: PENDIENTE-DERIVACION
  momentos_holdout_refs: []
  champion_actual: NINGUNO
  output_nativo: {tipo: proporcion, escala: "[0,1] ponderada", valor_ref: "milpa/tramite-ola5-propuesta-v0.yaml:1415"}
  incertidumbre: {tipo: "por candidato (diseno §2.5)", ref: "este documento"}
  supuesto_transporte: "ACOTADO-CON-SUPUESTO: formalidad restringida a quien trabaja (cobertura 0.689676); identidad de codigos 2021/2024 verificada por archivo antes de COMMIT-1"
  fuerza_coeficiente: NO-APLICA
  procedencia_condicional: MEDICION_DIRECTA_MICRODATO
  calibrado: false
  estado_operativo: PENDIENTE
  vocabulario_version: 0.5
  requiere_decision_mesa: true          # dos cosas: FP-376 (formalidad/localidad) y el hueco 'persistencia' en el enum estrategia
  fecha_declaracion: 2026-09-17
  commit_declaracion: b881ee6
  relacion_complemento: NO-APLICA
```

## 3 · Qué le rinde al programa, contado sin inflar
1. **La primera entrada del catálogo de momentos con estimador adjudicado** — hoy las 22 están `NO-VERIFICADO`.
2. **La primera lista con nombre de lo que la matriz necesita para competir en una celda** (cuatro faltantes, §2.2 C3). Es la prueba material de M1 tal como quedó firmada: la matriz compite si puede, y hoy no puede.
3. **Un piso de persistencia en dominio DIN**, donde hasta ahora solo había cívico y remesas (`TRIADA-B-PISO`).
4. **Una celda de segmento real para el marcador**, sobre `formalidad` vía `P3_13` — exactamente la fila que FP-376 lleva a firma.
5. **Cuantificar cuánto pierde el emisor x = ∅** en un dominio nuevo (C4).

## 4 · Fallas propias que este diseño ya ve
- **Jardín de senderos:** las celdas fueron vistas. Mitigación: celdas heredadas del árbitro, no elegidas; congelación en COMMIT-1; primer resultado = resultado reportado.
- **No independencia entre celdas:** diez celdas de una muestra; por eso no hay valor-p y el umbral es de conteo.
- **Universo restringido** en `formalidad` (trabajadores): C1 debe restringirse **igual** en 2021 o la comparación cruza universos (A-bis 4).
- **Memoria de L:** INEGI publicó ENIF 2024 en 2025; el control de memoria puede vaciar celdas. Si quedan < 8 `PUNTUADA`, el piloto lo dice y sigue siendo factibilidad.
- **Códigos 2021 ≠ 2024** en `tloc` o `P3_13`: si la verificación por archivo falla, `localidad` o `formalidad` salen del piloto y se declara `NO-CONSTRUIBLE` (A.15), no se adivina.
- **Lo que el piloto no puede decir:** nada sobre el motor matricial como estimador — solo que hoy no compite y qué le falta.

## 5 · Lo que va a mesa antes de congelar
1. FP-376 (formalidad y localidad como MAPEO-N-A-1): sin ella, las celdas de `formalidad`/`localidad` existen para C1/C2 pero no entran al marcador.
2. El hueco de vocabulario "persistencia" en `estrategia` (v0.3 §3): registrar como falsador del vocabulario o admitir `transversal_con_seleccion` + `regla_composicion` como aquí.
3. Si mesa quiere que `edad` y `sexo` entren aunque no tengan corte del modelo (este diseño dice sí: son celdas del árbitro y C1/C2 no necesitan cortes).

## 6 · Contador y módulo de auditoría (acotado: este artefacto afirma sobre México solo lo que el árbitro ya selló)
**Contadores movidos: cero** — es diseño. **Pobreza/estructura vs cultura:** el estimando es una conducta financiera condicionada a formalidad y localidad, ambos estructurales; el piloto no atribuye mecanismo. **Clase media urbana:** el universo de `formalidad` sobre-representa a quien trabaja formalmente por construcción (cobertura 0.69); declarado. **Marcos importados:** ninguno; L+corpus hereda el sesgo del corpus F5, declarado en su variante. **Rural/popular:** `localidad` <15 000 está en las celdas. **Racional vs psicológico:** el piloto mide, no interpreta. **Peligro simplista:** leer "sin seguridad social ahorra más informal" como preferencia cultural; el propio árbitro lo registró como ASOCIACIÓN (A-bis 1). **v2.1 — qué afirmación describe el estado del corpus y fue escrita a mano:** ninguna: los conteos (3 celdas-D, 7 entradas `_ejes_`, 22 momentos, 207 filas, 22 ENIF, 214 filas de inventario) se derivaron por comando en esta sesión y el comando se cita. **Escala (v2.4):** proporción ponderada `[0,1]` en todos los candidatos y en R; ninguna comparación cruza escalas.
