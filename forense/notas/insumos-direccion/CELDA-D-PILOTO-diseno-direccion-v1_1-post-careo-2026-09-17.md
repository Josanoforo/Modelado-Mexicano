<!-- CABECERA DE PROCEDENCIA · añadida por ACTO GEN2-CELDA-D-CAREO-1 (A.3).
     El cuerpo que sigue a la línea de guiones es VERBATIM: no se editó una coma.
     Esta cabecera es del archivo, no del documento. -->

> **PROCEDENCIA (A.3 · archivo verbatim)**
> - **Clase:** INSUMO DE DIRECCIÓN tipo 3 — no entra al canon sin un acto de verificación posterior.
> - **Autor:** Dirección (Fable)
> - **Fecha nominal:** 17/sep/2026 · **fecha de archivo:** 2026-09-16 (fecha de ejecución del entorno; las dos se conservan, no se infiere una firma futura).
> - **sha256 del cuerpo verbatim, verificado por comando en este acto:** `68a794936ef2ca47cf052b3a1e64ca002c87fb7d9e8cefb8ae998220c99f19cb`
>   — coincide con el prefijo `68a794936ef2ca47…` que el encargo declara.
>   Comando: `sha256sum <adjunto>` antes de copiar, y `sha256sum` del cuerpo extraído después.
> - **Archivado por:** `ACTO GEN2-CELDA-D-CAREO-1`, encargo `forense/encargos/2026-09-17-GEN2-CELDA-D-CAREO-1-TRES-DISENOS-UN-CAREO.md`, P0.
> - **Nota:** EL DISEÑO VIGENTE, por la firma de mesa del 17/sep/2026. Su §9 es el YAML que este acto registra como celda-D.

---

# CELDA-D-PILOTO · Diseño de dirección · v1.1 · POST-CAREO
**Dirección (Fable) → mesa · 17/sep/2026 · derivado contra `9dffd64` (merge de #823) con comando a la vista. Supera a v1.0 (`c7d55e61…`, ciego, historia: no se edita). Aceptado por mesa en conversación el 17/sep ("aceptado", punto 1 del careo); la firma verbatim viaja en el encargo `GEN2-CELDA-D-CAREO-1`.**

**Procedencia (v2.1).** Todo `archivo:línea` leído del clon en esta sesión. Los tres hechos que cambian el diseño los midió otro (Opus, #823; Astra, retorno `2b813f43…`) y dirección los **re-verificó por comando** antes de aceptarlos; se dice quién los encontró.

---

## 0 · Qué cambió respecto de v1.0, y quién lo encontró

| # | v1.0 decía | hallazgo | quién | verificado hoy |
|---|---|---|---|---|
| 1 | `formalidad` {sin SS, con SS} entre las celdas, con persistencia desde ENIF 2021 | `P3_13` **no existe** en ENIF 2021 | Opus, §1.7 | `grep enif2021 … p3_13` → **0** filas; `enif2024` → 4 (`data/inventario-reactivos-v1_2.tsv`) |
| 2 | desenlace "ninguna P5_6_1..P5_6_9 == 1", idéntico en las dos olas | `P5_6_6` y `P5_6_7` **no existen** en 2021 (2021: 1-5, 8, 9) | Opus, §1.6 | catálogos `enif2021`: `p5_6_{1,2,3,4,5,8,9}`; `enif2024`: `p5_6_{1..9}` |
| 3 | emisor excluido "por circular" (una regla, `CORR-0009`) | es **estructural**: en 5 de 7 entradas `_ejes_` el emisor copió el árbitro verbatim | Opus, §1.5 | `milpa/tramite.yaml:712` *"copiada verbatim"*, `:1026`; `RES-0041 = 0.672` vs árbitro `0.672014` (`tramite-ola5-propuesta-v0.yaml:2012`) |
| 4 | (g) "declarable": las celdas ya vistas por dirección, no por L → factibilidad | quien **selecciona** las vio: no hay evaluación ciega, y partir la misma ola no la devuelve (el total publicado reconstruye la reserva) | Astra, §1.2, §3.6-3.7 | no requiere comando: es lógica, y es correcta |
| 5 | brief externo decía "23 momentos" y columna `reglas_impacto` en la demanda | son **22** momentos (M01-M22 + cabecera) y la columna es `consumidor` (`reglas_impacto` vive en `usos.tsv`) | Astra, §1.1 | `wc -l` → 23 líneas; cabecera de `demanda-resultados.tsv` | 

**Lo que ninguno de los tres diseños vio, y es lo que reconcilia (4) con la ausencia de ola nueva:** el árbitro solo derivó **marginales** por eje. Las celdas de **cruce** `localidad × edad` nunca se han calculado: son 8 números que nadie ha visto — ni dirección, ni L, ni el emisor. Si se derivan **después** de congelar candidatos y de sellar sus emisiones, (g) se cumple bajo la lectura estricta de Astra (el selector solo conoce marginales) y bajo la vía (iii) de Opus (ola retenida en la persistencia), sin descargar nada. Verificado: `grep "localidad × edad|reserva por interacci"` sobre 2 262 archivos → 2 coincidencias, ambas del 12/ago sobre clustering de R5.1, no sobre reserva de evaluación.

## 1 · La celda, corregida

- **Estimando:** `p(ahorra_solo_informal | localidad, edad)` — proporción ponderada `[0,1]`, personas elegidas 18+ (ENIF, TMODULO, `FAC_PER`). **Definición del desenlace, idéntica en las dos olas:** alguna `P5_1_1..P5_1_6 == 1` **y ninguna** `P5_6_k == 1` para `k ∈ {1,2,3,4,5,8,9}` — los siete códigos comunes. Consecuencia declarada: **no es el mismo estimando que el marginal del árbitro** (`tramite-ola5-propuesta-v0.yaml:1426` usa 1..9): quien ahorra solo por `P5_6_6/7` cuenta aquí como "sin vía formal". Es EXISTE-NO-SATISFACE respecto de la entrada del árbitro, con la diferencia escrita; la alternativa (definir por ola) rompería la persistencia. A.15c: los códigos se verifican **por archivo** en los FD de 2021 y 2024 antes de COMMIT-1 (`enif2021_fd_zip`, `enif2024_fd_xlsx` en manifiesto).
- **Población objetivo:** las **8 celdas de cruce** `localidad` {<15 000 = `tloc ∈ {3,4}`, ≥15 000 = `tloc ∈ {1,2}`} × `edad` {18-29, 30-44, 45-59, 60+}. `localidad` tiene corte del modelo (MAPEO-N-A-1, **FP-376 ABIERTA**); `edad` usa los tramos del árbitro (sin corte del modelo; no lo necesita: la matriz no compite). Sale `formalidad` (hallazgo 1). n esperado por celda en 2024, derivado de los marginales del árbitro (`:1437-1470`): mínimo ≈ 4 646 × 0.21 ≈ **980** (<15 000 × 60+); ninguna celda por debajo del umbral de soporte (§2.4).
- **Unidad:** persona. **Árbitro R:** las 8 celdas de cruce en ENIF 2024, misma receta que el árbitro marginal (`FAC_PER`, `EST_DIS`/`UPM_DIS`, bootstrap 10 000, seed 42) — **NO DERIVADAS HOY. Se derivan en el tercer commit del piloto, después de que las emisiones estén selladas.** Cualquier acto que las derive antes rompe la reserva y se reporta como defecto.

## 2 · Candidatos

**C1 · `BASELINE_INGENUO` · b_persistencia.** Mismo desenlace (siete códigos), mismo cruce, ENIF 2021 (`tloc`, `edad` existen en 2021: catálogos `tloc.csv`, `edad.csv`). Estrategia `transversal_con_seleccion`, `regla_composicion: identidad temporal p_2021 → p_2024`. Hueco de vocabulario ("persistencia" no está en el enum `estrategia` de v0.3 §3) registrado como falsador del vocabulario, no como valor inventado.

**C2 · `BASELINE_INGENUO` · b_marginales.** `p̂(l,e) = p̂(l)·p̂(e)/p̂` bajo independencia, con los tres marginales **públicos** de ENIF 2024 (`:1437-1470`). Dieta declarada: usa lo que todos ya vieron; por eso es piso, no challenger. Es la vara que dice si la **interacción** contiene información que alguien sepa explotar.

**C3 · `CHALLENGER` · L, dos dietas (`variante_corredor: L-solo | L+corpus`).** Elicitación ciega de las 8 proporciones con intervalo de 80 % declarado por L, protocolo ADV1 (`CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B). Control de memoria: los marginales son públicos y L puede conocerlos; el cruce no ha sido publicado por INEGI en ese detalle — se verifica por búsqueda antes de elicitar y se anota. L recibe los marginales como parte de su dieta, explícitamente: la prueba es si añade algo a C2.

**C4 · `CHALLENGER` · matriz `B·θ(x) → h_r`, `estrategia: momentos`.** `resultado: INEJECUTABLE`, cuatro faltantes con nombre: `h_r` inexistente (`milpa/src/emisor.py:364`); `G3.horizonte_temporal` bajo `GATE·ID-X` (`procedencia.yaml:1116`); `G3.aversion_riesgo` `SIN-RUTA` (`:1172`); θ de `G3.familismo_apoyo` por celda de localidad × edad no medido (solo β̂ marginal `0.0279`, `modelo-decision-v4_0.md:466`). Bajo ADR-531 compite si puede; no puede; se escribe.

**C5 · `COMPLEMENTO` · emisor M (x = ∅) · `resultado: NO-APLICA`.** Fuera de la competencia por el hallazgo 3: es el árbitro con otro nombre. Se reporta solo como diagnóstico: |p_nacional − p_celda| por celda.

## 3 · Criterio de adjudicación, antes del dato
- **Por celda:** error absoluto en pp contra R. `INDECIDIBLE` si cualquiera de las dos condiciones del programa, verbatim: *"si ambos caen dentro del IC de R o si |d_L−d_M| < 0.5·EE(R)"* (`CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:38`; aquí los pares son challenger vs **cada** piso). `CONTROL-MEMORIA` según §2 C3. EE(R) = (IC95 sup − inf)/3.92.
- **Skill** contra cada piso: `1 − MAE/MAE(b)`; se reporta, no adjudica.
- **A nivel celda-D:** un challenger **gana** solo si vence a **los dos pisos** en ≥ 6 de las celdas `PUNTUADA` y las `PUNTUADA` son ≥ 6 de 8. Familia de afirmaciones declarada (F2 de Opus, §3.2 de Astra): 8 celdas × 2 challengers; por eso el umbral es de conteo y no hay valor-p (celdas de una misma muestra, no independientes).
- **Precedencia:** si dos filas se satisfacen, manda `INDECIDIBLE`.
- **B-bis:** si nadie vence a C1 → persistencia corroborada como piso en DIN. Si nadie vence a C2 → **la interacción no aporta información explotable a este n**, que es un resultado del programa, no un fracaso del piloto. Los dos se declaran antes de correr.

## 4 · Incertidumbre, emisión, soporte
| objeto | contiene | tipo |
|---|---|---|
| R | muestreo, bootstrap de conglomerados | IC muestral |
| C1 | muestreo 2021, misma receta | IC muestral |
| C2 | muestreo de los marginales 2024, propagado bajo independencia (delta) | IC muestral propagado |
| C3 | intervalo declarado por L (80 %); cobertura empírica medida contra R | intervalo de elicitación |
| C4 | — | — |

**Emitir ≠ decidir:** se emiten las 8 estimaciones de cada candidato con intervalo. Para el consumidor (`tramite.yaml:1306`) la pregunta útil es el **signo de la modulación** por celda respecto del nacional: estable si todo el intervalo del ganador queda del mismo lado que R; ambigua si cruza. **Soporte:** celda fuera de soporte si n_2021 < 200 (ninguna lo está por lo esperado; se verifica en COMMIT-1 sin abrir microdato, con los marginales del FD). Nada se adopta al motor por este piloto.

## 5 · Desarrollo, evaluación, orden de commits (E.3/E.5)
- **Desarrollo:** ENIF 2021 (C1); marginales públicos 2024 (C2, C3); corpus F5 sin ENIF 2024 (C3 L+corpus).
- **Evaluación:** las 8 celdas de cruce de ENIF 2024 — **no derivadas hasta el commit 3**.
- **COMMIT-1 (spec congelada, sin abrir microdato):** variables, códigos leídos del FD de cada ola, universo, ponderador, cruce, dicotomización de los siete códigos, seed, tolerancias; frase de sello: *"el primer resultado que produzca este procedimiento es el que se reporta"*. **COMMIT-2:** emisiones de C1, C2, C3 selladas como RESULT GEN2 con cadena completa. **COMMIT-3:** derivación de R en el cruce y adjudicación por celda. El orden del diff es el sello; mesa lo audita. Un R derivado antes del commit 2 invalida el piloto como evaluación y lo degrada a factibilidad — se declara, no se esconde.

## 6 · Parada
- **Factibilidad:** C1 y C2 calculados con cadena GEN2; C3 elicitado y puntuado; C4 asentado como `INEJECUTABLE` con sus cuatro faltantes; C5 cuantificado; adjudicación por celda escrita; **una entrada del catálogo de momentos** poblada con estimador adjudicado (hoy 22 de 22 `NO-VERIFICADO`); consumidor la lee sin cambiar código.
- **Desempeño local, ahora sí reclamable:** sobre la interacción, bajo §3, con la reserva de que son 8 celdas de una encuesta y una ola.

## 7 · Lo que va a mesa antes de congelar
1. **FP-376** — `localidad` como MAPEO-N-A-1: sin firma, la celda con corte del modelo no entra al marcador (el piloto puede correr igual; el marcador no lo consume).
2. **La definición por siete códigos comunes** (§1): es un estimando distinto del marginal del árbitro y se acepta con la diferencia escrita, o se rechaza y el piloto pierde la persistencia.
3. **Admitir C2 (marginales + independencia) como segundo piso.** Recomendado: sin él, "L vence a la persistencia" no distingue información de interacción de información de marginales.

## 8 · Universo de la estampa (A.10) · contador · auditoría
SHA `9dffd64`; instrumentos: ENIF 2021 y 2024 (`enif2021_csv`, `enif2024_csv`, FD de ambas en manifiesto); celdas: 8 de cruce, no derivadas; corpus L+corpus: el de F5 sin ENIF 2024. **Contadores movidos: cero.** **Auditoría (acotada):** el estimando es una conducta financiera condicionada a dos ejes estructurales; el piloto mide, no atribuye mecanismo; `localidad` <15 000 está en las celdas (rural/popular representado); ninguna afirmación sobre el estado del corpus fue escrita a mano — cada conteo trae su comando; escala: proporción `[0,1]` en todos los objetos, ninguna comparación cruza escalas.

## 9 · Borrador YAML (v0.5) para el registro de la celda-D
```yaml
celda_d:
  id: DIN.ahorro_solo_informal.enif2024.localidad_x_edad
  estimando: "p(ahorra_solo_informal | localidad, edad) -- proporcion ponderada [0,1], personas 18+ (ENIF TMODULO, FAC_PER); vias formales = P5_6_{1,2,3,4,5,8,9} (siete codigos comunes 2021/2024)"
  tipo_adjudicacion: COMPARACION
  dominio: FIN
  poblacion_objetivo: "8 celdas de cruce: localidad{<15000 tloc in {3,4}; >=15000 tloc in {1,2}} x edad{18-29,30-44,45-59,60+}; ver diseno v1.1 §1"
  unidad_objetivo: persona
  universo_candidatos: "careo de tres disenos ciegos (direccion v1.0, Opus #823, Astra 2b813f43) @ b881ee6-9dffd64, 17/sep/2026"
  candidatos:
    - {rol: BASELINE_INGENUO, fuentes: [ENIF], edicion_periodo: "2021", universo_instrumento: "personas 18+ elegidas, TMODULO 2021, mismo cruce", diseno_datos: transversal, estrategia: transversal_con_seleccion, regla_composicion: "identidad temporal p_2021 -> p_2024 (declarada 2026-09-17)", production_spec_refs: [], resultado: NO-EJECUTADO}
    - {rol: BASELINE_INGENUO, fuentes: [ENIF], edicion_periodo: "2024 (marginales publicos del arbitro)", universo_instrumento: "marginales localidad, edad y nacional ya sellados", diseno_datos: transversal, estrategia: composicion, regla_composicion: "independencia: p(l,e) = p(l)*p(e)/p (declarada 2026-09-17)", production_spec_refs: [], resultado: NO-EJECUTADO}
    - {rol: CHALLENGER, variante_corredor: L-solo, fuentes: [L], edicion_periodo: "elicitacion 2026-09", universo_instrumento: "memoria del modelo + marginales publicos; control de memoria sobre el cruce", diseno_datos: transversal, estrategia: composicion, regla_composicion: "protocolo ADV1", production_spec_refs: [], resultado: NO-EJECUTADO}
    - {rol: CHALLENGER, variante_corredor: L+corpus, fuentes: [L], edicion_periodo: "elicitacion 2026-09", universo_instrumento: "idem + corpus F5 sin ENIF 2024", diseno_datos: transversal, estrategia: composicion, regla_composicion: "protocolo ADV1", production_spec_refs: [], resultado: NO-EJECUTADO}
    - {rol: CHALLENGER, fuentes: [matriz_B, procedencia.yaml], edicion_periodo: "n/a", universo_instrumento: "n/a", diseno_datos: transversal, estrategia: momentos, regla_composicion: "B*theta(x) -> h_r (h_r inexistente)", production_spec_refs: [], resultado: INEJECUTABLE}
    - {rol: COMPLEMENTO, fuentes: [emisor, tramite.yaml], edicion_periodo: "2024", universo_instrumento: "p nacional ENIF 2024 = arbitro (tramite.yaml:712); solo diagnostico", diseno_datos: transversal, estrategia: composicion, regla_composicion: NO-APLICA, production_spec_refs: [], resultado: NO-APLICA}
  criterio_adjudicacion: {texto: "error absoluto por celda vs R derivado en COMMIT-3; INDECIDIBLE si ambos caen dentro del IC de R o si |d_1-d_2| < 0.5*EE(R); gana el challenger que vence a los dos pisos en >=6 de >=6 PUNTUADA; precedencia INDECIDIBLE; B-bis declarado (diseno v1.1 §3)", escala: "puntos porcentuales; EE(R)=(IC95sup-IC95inf)/3.92"}
  estado_decidibilidad: NO-APLICA
  margen_material: PENDIENTE-DERIVACION
  momentos_holdout_refs: ["RESERVADA: cruce localidad x edad, ENIF 2024 -- NO DERIVADO; se deriva en COMMIT-3 de GEN2-CELDA-D-PILOTO-1"]
  champion_actual: NINGUNO
  output_nativo: {tipo: proporcion, escala: "[0,1] ponderada", valor_ref: "NO-PRODUCIDO"}
  incertidumbre: {tipo: "por candidato (diseno v1.1 §4)", ref: "diseno v1.1"}
  supuesto_transporte: "ACOTADO-CON-SUPUESTO: desenlace sobre siete codigos comunes (difiere del marginal del arbitro); identidad de tloc/edad 2021/2024 verificada por archivo antes de COMMIT-1"
  fuerza_coeficiente: NO-APLICA
  procedencia_condicional: MEDICION_DIRECTA_MICRODATO
  calibrado: false
  estado_operativo: PENDIENTE
  vocabulario_version: 0.5
  requiere_decision_mesa: true   # FP-376; siete codigos comunes; admision de C2
  fecha_declaracion: 2026-09-17
  commit_declaracion: 9dffd64
  relacion_complemento: NO-APLICA
```
