<!-- CABECERA DE PROCEDENCIA · añadida por ACTO GEN2-CELDA-D-CAREO-1 (A.3).
     El cuerpo que sigue a la línea de guiones es VERBATIM: no se editó una coma.
     Esta cabecera es del archivo, no del documento. -->

> **PROCEDENCIA (A.3 · archivo verbatim)**
> - **Clase:** INSUMO EXTERNO tipo 3 — no entra al canon sin un acto de verificación posterior.
> - **Autor:** Astra (asistente ChatGPT/Codex), rol solicitado por dirección
> - **Fecha nominal:** 17/sep/2026 · **fecha de archivo:** 2026-09-16 (fecha de ejecución del entorno; las dos se conservan, no se infiere una firma futura).
> - **sha256 del cuerpo verbatim, verificado por comando en este acto:** `2b813f430fd3ad4f0176e3ff962677136662209830c36f9296108dafa1924356`
>   — coincide con el prefijo `2b813f430fd3ad4f…` que el encargo declara.
>   Comando: `sha256sum <adjunto>` antes de copiar, y `sha256sum` del cuerpo extraído después.
> - **Archivado por:** `ACTO GEN2-CELDA-D-CAREO-1`, encargo `forense/encargos/2026-09-17-GEN2-CELDA-D-CAREO-1.md`, P0.
> - **Nota:** Retorno externo al encargo ENCARGO-EXTERNO-ASTRA-celda-d-piloto-2026-09-17.md. Derivado contra el árbol fijo b881ee6. Sus 87 citas `archivo:línea` se verifican en P1 de este acto; sus tres fuentes externas quedan SIN-FETCH (A.6).

---

# Astra · Primer piloto celda-D y adversarial del selector por celda

**Investigador:** Astra, rol solicitado, asistente ChatGPT/Codex. **Fecha nominal del encargo:** 17/sep/2026. **Fecha de ejecución del entorno:** 16/sep/2026; se conservan ambas, sin inferir una firma futura. **Herramientas:** lectura HTTPS de archivos raw, Python para metadatos/tablas y hashes, búsqueda web de fuentes metodológicas primarias. **Árbol exclusivo de evidencia:** `b881ee699521fee69707c563e3f00134e7257708`. **Retorno:** insumo externo v1.0; no adopta, no adjudica, no modifica el repositorio y no propone valores del modelo.

**Qué leyó:** las rutas y el alcance de lectura están en el inventario final. Todos los enlaces del repositorio de este informe apuntan al árbol fijo; las líneas son las del archivo raw, contadas desde 1. **SIN-FETCH:** `data/curacion-registro/necesidades.tsv`, ruta auxiliar tentativa, HTTP 404; no se utiliza como evidencia. Los 17 archivos concretos de la lista principal —incluidos los tres YAML— sí se descargaron. El lector web falló con una URL raw; la lectura HTTPS por Python sí obtuvo ese archivo.

**Insumos externos:** se leyó completo `D-THETA-DOCUMENTO-v1_1-post-adversarial.md`, recuperado por su nombre exacto (135 líneas; la lectura nativa no verifica su SHA de bytes). Se leyó `ADVERSARIAL-D-THETA-v1_0.md`; su SHA-256 local es `850f9cefe4334acd679d7eaa38eceafa4da19d903bd38997f448534b32d082e7`, coincidente con el prefijo aportado. No se usaron los ZIP de agosto para establecer estado. La firma M1 del mensaje es todavía el marcador `[FIRMA M1 — A o B]`: se analiza la política sustantiva solicitada como hipótesis, sin convertir ese marcador en firma.

**Límite de independencia:** esta misma conversación ya conocía la adversarial anterior y el resumen de un PR posterior al corte. No es posible desleer ese contexto. No se consultó `main` ni ese PR durante este encargo, ni se utilizó su cambio como evidencia o capacidad disponible. No se leyó el nuevo diseño independiente de Dirección para este careo. La ceguera que sí se preservó es respecto de microdatos y resultados nuevos: no se abrió ni pidió ninguno. Los resultados históricos incluidos en documentos proporcionados sí son visibles; no se presentan como reservados.

## Dictamen

**No hay una primera celda que pueda certificar como elegible bajo los siete requisitos simultáneos del encargo.** Hay datos adquiridos, salidas descriptivas y familias reservadas aprovechables, pero no una combinación documentada de mismo estimando, población compatible, dos familias de estimadores ejecutables y evaluación independiente preservada. Este es un resultado de elegibilidad documental en el universo inspeccionado, no la afirmación de que ningún diseño futuro sea posible.

Por ello, §1 termina sin ganadora. §2 entrega un **borrador parametrizado, no instanciado ni ejecutable**, para dejar resuelto el método sin inventar la celda que falta. §§3–4 sí tienen dictamen: la política es defendible si selecciona procedimientos para un mismo objeto, conserva un árbitro final fuera de la selección y compone salidas con tipos y soporte explícitos. Es perjudicial si produce una colección de ganadores locales sin esas condiciones.

## 1 · Elegibilidad: ninguna ganadora acreditada

### 1.1 Universo y criterios

Se revisaron los tres YAML completos, las 207 filas de demanda y el catálogo completo. El catálogo contiene **22 momentos, M01–M22, más cabecera**: 23 líneas no son 23 momentos. La demanda tampoco contiene una columna `reglas_impacto`; contiene `consumidor`. Se usa esa referencia real para examinar el requisito (f), sin inventar una columna ni equiparar una referencia de archivo con una regla decisional ya definida. [milpa/catalogo-momentos-v0_1.tsv:1-23](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/milpa/catalogo-momentos-v0_1.tsv#L1-L23) [data/corrida0/demanda-resultados.tsv:1-2](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/corrida0/demanda-resultados.tsv#L1-L2)

Leyenda: **P** = evidencia suficiente para el requisito; **F** = incompatibilidad constatada; **NE** = no acreditado, no equivale a ausencia universal. En (e), tanto una persistencia construible como una ausencia explicada satisfacen la obligación informativa; no se exige inventar una serie.

| Candidata concreta | (a) Estimando/escala/universo | (b) Corte y árbitro | (c) Adquirido | (d) Dos familias elegibles | (e) Persistencia | (f) Consumidor | (g) Reserva independiente |
|---|---|---|---|---|---|---|---|
| G5, actitud de deber de cuidado | P, con restricción de constructo | NE | P | F: un candidato | No construible con la única edición declarada | Referencia de demanda; uso restringido | NE; resultado ya reproducido |
| G5, motivo del cuidado realizado | P, proporciones entre cuidadores | NE | P | F: un candidato | No construible con la única edición declarada | Referencia de demanda | NE; resultado ya reproducido |
| G5, radio de confianza | F para comparación sustitutiva: no equivalencia métrica | NE | P | F: dos instrumentos no equivalen a dos familias admisibles | ENCUCI↔ENBIARE no es persistencia de una serie equivalente | Referencia de demanda | NE; vinculación ya evaluada |
| Ahorro sólo informal, ENIF 2024, localidad <15 mil | P | Mapeo 4→2, propuesta pendiente | P | NE | Serie adquirida; comparabilidad exacta previa NE | P: `dinero.ahorro.via_informal` | F como objetivo ciego: resultado publicado en el árbol |

**Evidencia de las tres semillas:** actitud: estimando/población/candidato y escala en las líneas 31–45 y 66–83; conducta: 54–77 y 108–123; confianza: población y candidatos en 31–101, falta de sustitución métrica en 110–138. Sus referencias de demanda son RES-0171–0173, y las condicionales relacionadas reaparecen como RES-0202, RES-0206 y RES-0207: son referencias del mismo material, no nuevos candidatos. [data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml:31-83](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml#L31-L83) [data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml:54-123](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml#L54-L123) [data/curacion-registro/celdas-d/G5.radio_confianza.encuci_vs_enbiare.yaml:31-138](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/curacion-registro/celdas-d/G5.radio_confianza.encuci_vs_enbiare.yaml#L31-L138) [data/corrida0/demanda-resultados.tsv:173-175](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/corrida0/demanda-resultados.tsv#L173-L175) [data/corrida0/demanda-resultados.tsv:204-209](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/corrida0/demanda-resultados.tsv#L204-L209)

**Adquisición registrada, sin volver a verificar bytes de microdato:** ENASIC 2022, ENCUCI 2020 y ENBIARE 2021 constan con archivo y SHA. ENIF tiene microdatos 2021 y 2024 registrados, distintos de los ZIP de datos abiertos: se cita la entrada de microdatos. [data/manifiesto.yaml:4015-4029](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/manifiesto.yaml#L4015-L4029) [data/manifiesto.yaml:1011-1040](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/manifiesto.yaml#L1011-L1040) [data/manifiesto.yaml:3976-3989](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/manifiesto.yaml#L3976-L3989) [data/manifiesto.yaml:5500-5514](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/manifiesto.yaml#L5500-L5514) [data/manifiesto.yaml:5543-5558](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/manifiesto.yaml#L5543-L5558)

**Caso más cercano, sin elegirlo:** el ahorro sólo informal tiene evento binario, persona elegida 18+, ponderador y regla consumidora explícitos; RES-0053 identifica la salida asignada. El árbitro ya publica sus dos tasas por localidad e IC. El mapeo colapsa `tam_loc={1,2}` y `{3,4}`: se pierden las diferencias internas 100 mil+ frente a 15–99 mil, y 2.5–14.9 mil frente a <2.5 mil. La fila de localidad no tiene firma; puede analizarse como diseño, no consumirse como mapeo aprobado. [milpa/tramite-ola5-propuesta-v0.yaml:1415-1427](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/milpa/tramite-ola5-propuesta-v0.yaml#L1415-L1427) [milpa/tramite-ola5-propuesta-v0.yaml:1464-1473](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/milpa/tramite-ola5-propuesta-v0.yaml#L1464-L1473) [data/corrida0/demanda-resultados.tsv:55](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/corrida0/demanda-resultados.tsv#L55) [data/crosswalk-ejes-arbitro-modelo-v1_0.tsv:4-10](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/crosswalk-ejes-arbitro-modelo-v1_0.tsv#L4-L10)

### 1.2 Tabla de eliminación, sin contar duplicados como oportunidades

| Candidata o grupo examinado | Criterio que falla o queda NE | Evidencia y consecuencia |
|---|---|---|
| `G5.familismo_obligacion.actitud` | (d), (g); (b) NE | Único candidato y holdout vacío; no sustituirlo por conducta, que es otro estimando. [data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml:66-83](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml#L66-L83) |
| `G5.obligacion_medida.conducta` | (d), (g); (b) NE | Único candidato, holdout vacío y universo de cuidadores; no es la norma actitudinal. [data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml:108-123](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml#L108-L123) |
| `G5.radio_confianza.encuci_vs_enbiare` | (a)/(d), (g); (b) NE | La convergencia configural no autoriza sustitución métrica; holdout vacío. [data/curacion-registro/celdas-d/G5.radio_confianza.encuci_vs_enbiare.yaml:110-153](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/curacion-registro/celdas-d/G5.radio_confianza.encuci_vs_enbiare.yaml#L110-L153) |
| M01–M08; RES-0174–0181 | (a), (c), (d), (g) NE en el catálogo | Son objetivos de ajuste; instrumentos por declarar y disponibilidad no verificada. Que existan mediciones relacionadas no completa automáticamente el contrato del momento. [milpa/catalogo-momentos-v0_1.tsv:2-9](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/milpa/catalogo-momentos-v0_1.tsv#L2-L9) [data/corrida0/demanda-resultados.tsv:176-183](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/corrida0/demanda-resultados.tsv#L176-L183) |
| M09–M22; RES-0182–0195 | (a), (c), (d), (g) NE | La etiqueta HOLDOUT no identifica instrumento, escala, partición o aislamiento. No se interpreta como prueba de ceguera. [milpa/catalogo-momentos-v0_1.tsv:10-23](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/milpa/catalogo-momentos-v0_1.tsv#L10-L23) |
| Conductas RES-0001–0066 | Falta documentar la conjunción (b)+(d)+(g) | Incluyen salidas asignadas, medidas y complementos, no 66 concursos preparados. El caso ENIF más próximo falla (g) por exposición; para los restantes no se acreditó una pareja elegible y una partición reservada en la demanda y sus superficies de árbitro. [data/corrida0/demanda-resultados.tsv:3-68](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/corrida0/demanda-resultados.tsv#L3-L68) [data/crosswalk-ejes-arbitro-modelo-v1_0.tsv:9-20](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/crosswalk-ejes-arbitro-modelo-v1_0.tsv#L9-L20) |
| Coeficientes/probabilidades RES-0067–0094 y θ RES-0196–0207 | (a)/(d)/(g) NE para concurso de conducta | Son insumos con escalas heterogéneas, no salidas intercambiables; la ruta matricial no ejecuta θ. [data/corrida0/demanda-resultados.tsv:69-96](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/corrida0/demanda-resultados.tsv#L69-L96) [data/corrida0/demanda-resultados.tsv:198-209](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/corrida0/demanda-resultados.tsv#L198-L209) [milpa/src/theta.py:35-54](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/milpa/src/theta.py#L35-L54) |
| Corredores de 14 celdas previas, RES-0095–0164 | (g) NE/F por historia disponible | Son 70 filas de R/M/L/agregado, no 70 objetivos nuevos. U3 está expuesta; el diagnóstico de persistencia declara expresamente que su resultado ya se conocía. No se presume que las otras celdas sean nuevas reservas. [data/corrida0/demanda-resultados.tsv:97-166](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/corrida0/demanda-resultados.tsv#L97-L166) [forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md:21-30](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md#L21-L30) |
| Cortes π, RES-0165–0170 | (a)/(f) como celda de conducta | Son seis especificaciones de ejes; no seis estimandos de conducta con consumidores y candidatos propios. [data/corrida0/demanda-resultados.tsv:167-172](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/corrida0/demanda-resultados.tsv#L167-L172) [milpa/src/celdas.py:74-83](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/milpa/src/celdas.py#L74-L83) |
| MOCIBA e ISSP, contraste auxiliar con el panel reservado | (b), y equivalencia de estimando/candidato (a)/(d) NE | El panel los llama congelables para F6, pero sus cortes sexo/edad o sexo/URBRURAL no reciben un mapeo propio en este crosswalk. ISSP pregunta a quién acudiría por un préstamo grande; su regla asociada mide apoyo familiar recibido para vejez. Ser reservado no los convierte en el mismo estimando. [forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv:2](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv#L2) [forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv:16](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv#L16) [data/crosswalk-ejes-arbitro-modelo-v1_0.tsv:9-23](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/crosswalk-ejes-arbitro-modelo-v1_0.tsv#L9-L23) |

Los grupos de demanda cubren 66+28+70+6+3+22+12=207 filas; las semillas y los momentos reaparecen dentro de ellas. El campo `validacion_independiente=NO-HECHA`, presente en las 207, **no demuestra** que todos los datos estén contaminados ni que todos estén ciegos: sólo informa que ese registro no acredita validación. La exclusión aquí es por falta de evidencia suficiente para los siete requisitos, no por ese token aislado. [data/corrida0/demanda-resultados.tsv:2-209](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/corrida0/demanda-resultados.tsv#L2-L209)

**NO-ENCONTRADO, alcance preciso:** no se encontró una especificación completa de partición independiente vinculada a una candidata elegible en los tres YAML (`momentos_holdout_refs`), las 22 filas de momentos (`HOLDOUT`, `instrumentos_candidatos`, `estatus_disponibilidad`), las 207 demandas (`consumidor`, `validacion_independiente`, `spec_legacy`), el crosswalk completo y las filas `RETENIDA` del panel auxiliar. No se buscó por todo el repositorio ni se certifica quién vio qué en conversaciones externas. “Nadie la vio” sólo puede operacionalizarse como ausencia de exposición del equipo que selecciona/ajusta, con una trazabilidad de acceso acotada; no como desconocimiento de los productores de la encuesta.

**Ganadora: NINGUNA ACREDITADA. Se detiene aquí la elección.**

## 2 · Diseño v1.0 condicionado, sin celda seleccionada

### 2.1 Qué entrega este apartado

No sería honesto emitir un pre-registro ciego de “esa celda” después del resultado de §1. El siguiente YAML es una **plantilla de diseño**, con campos pendientes visibles; no se registra, no habilita una corrida y no satisface por sí solo los siete requisitos. Incluye los campos de v0.3, el cambio de `fuerza` de v0.4 y las extensiones de v0.5. Los campos bajo `extension_diseno` son propuesta externa, no vocabulario que se afirme adoptado. [propuesta-motor-adaptativo-celda-v0_3.md:40-82](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_3.md#L40-L82) [propuesta-motor-adaptativo-celda-v0_4.md:35-82](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_4.md#L35-L82) [propuesta-motor-adaptativo-celda-v0_5.md:33-73](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_5.md#L33-L73)

El producto propuesto es **estimación descriptiva contemporánea de una proporción**, con evaluación externa de su error; no efecto causal ni pronóstico futuro. El estimando sería p(S,T)=P(Y=1 | U,S,T), con evento Y, universo U, periodo T y segmento S fijados nominalmente antes de abrir la evaluación. Se elige una sola escala: proporción [0,1]. Los parámetros S/Y/U/T siguen sin instanciar porque ninguna candidatura pasó. Una celda nacional no satisface de oficio la exigencia de cortes; un dominio agregado requiere unión explícita de celdas-x.

```yaml
celda_d:
  id: BORRADOR_NO_INSTANCIADO
  estimando: "p(S,T)=P(Y=1|U,S,T); Y, U, S y T pendientes de elegibilidad"
  tipo_adjudicacion: COMPARACION
  dominio: FIN  # sólo caso de uso de la plantilla; no elección de una celda
  poblacion_objetivo: "PENDIENTE: U restringido y unión explícita S de cortes sellados"
  unidad_objetivo: persona
  universo_candidatos: "Tres familias requeridas; ninguna elegibilidad nueva se declara"
  candidatos:
    - rol: BASELINE
      fuentes: [PENDIENTE_ID_MANIFIESTO_TRANSVERSAL_T]
      edicion_periodo: "T, por fijar"
      universo_instrumento: "U y S, exactamente el estimando objetivo"
      diseno_datos: transversal
      estrategia: NO-APLICA
      regla_composicion: NO-APLICA
      production_spec_refs: []
      resultado: NO-EJECUTADO
      extension_diseno:
        id_candidato: D_DIRECTO
        elegibilidad: NO_ACREDITADA
        estimador: "razón ponderada de indicador Y en muestra D_T"
        incertidumbre: {familia: IC_MUESTRAL, nivel: 0.95}
    - rol: CHALLENGER
      fuentes: [PENDIENTE_IDS_MANIFIESTO_DESARROLLO]
      edicion_periodo: "corte de información previo al arbitraje"
      universo_instrumento: "U y S; transporte pendiente de declarar"
      diseno_datos: transversal
      estrategia: momentos
      regla_composicion: "h_r(B*theta(x),C(x)); forma y dependencias por congelar"
      production_spec_refs: []
      resultado: INEJECUTABLE
      extension_diseno:
        id_candidato: M_MATRIZ
        elegibilidad: NO_ACREDITADA
        incertidumbre: {familia: ENVOLVENTE_ESCENARIOS, cobertura: NO_ATRIBUIBLE}
        requiere: [ruta_ejecutable, theta_consumidas, B_participante, h_r, contexto]
    - rol: BASELINE_INGENUO
      fuentes: [PENDIENTE_ID_MANIFIESTO_OLA_ANTERIOR]
      edicion_periodo: "t_anterior<T, conocida al corte"
      universo_instrumento: "mismo evento Y, U y S; continuidad por verificar"
      diseno_datos: transversal
      estrategia: NO-APLICA
      regla_composicion: "p_b(S,T)=p_directa(S,t_anterior)"
      production_spec_refs: []
      resultado: NO-EJECUTADO
      extension_diseno:
        id_candidato: B_PERSISTENCIA
        elegibilidad: NO_ACREDITADA
        incertidumbre: {familia: PREDICTIVO, estimacion_intervalo: NO_ACREDITADA}
  criterio_adjudicacion:
    escala: "proporción [0,1]; errores absolutos en unidades de proporción"
    texto: "Aplicar §2.3; sólo puntuación de piloto, sin promoción de champion"
  momentos_holdout_refs: []  # vacío bloquea ejecución: no se inventa reserva
  champion_actual: NINGUNO
  output_nativo:
    tipo: Intervalo
    escala: "proporción [0,1] sobre U,S,T"
    valor_ref: "NO-PRODUCIDO; interfaz propuesta en §4"
  incertidumbre: {tipo: "POR_CANDIDATO; no banda común", ref: "§2.4 de este borrador"}
  supuesto_transporte: "NO-TRANSPORTABLE: equivalencia aún no acreditada para una celda"
  fuerza_coeficiente: NO-APLICA
  sin_coeficiente_asociado: true
  razon_sin_coeficiente: "Plantilla de salida descriptiva sin parámetro adjudicado"
  procedencia_condicional: SIN_ESTIMACION_TODAVIA
  vocabulario_version: 0.5
  margen_material: PENDIENTE-DERIVACION
  estado_decidibilidad: "SKIP:SIN-CELDA-ELEGIBLE"
  calibrado: false
  estado_operativo: PENDIENTE
  requiere_decision_mesa: true
  fecha_declaracion: "PENDIENTE; fecha del informe no es sello"
  commit_declaracion: "PENDIENTE; no usar el SHA del árbol como firma"
  fecha_adjudicacion: NO-APLICA
  commit_adjudicacion: NO-APLICA
  relacion_complemento: NO-APLICA
  extension_diseno:
    ejecutable: false
    consumidor: PENDIENTE_REFERENCIA_REAL
    regla_decision: PENDIENTE_FUNCION_Y_UMBRAL
    corte_modelo: PENDIENTE
    celda_arbitro: PENDIENTE
    crosswalk_aprobado: false
    desarrollo_ids: []
    evaluacion_ids: []
    verificacion_acceso: NO_ACREDITADA
    prohibido: [usar_U3_como_reserva_nueva, adoptar_resultados, calibrar_con_R_final]
```

La plantilla usa `NO-APLICA` para estrategia directa/persistencia y coeficiente sin asociación, coherente con las excepciones presentes en el registro y el validador; no convierte una proporción medida en un β ajustado. [data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml:72-82](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml#L72-L82) [data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml:124-143](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml#L124-L143) [tests/test_celdas_d.py:99-117](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/tests/test_celdas_d.py#L99-L117) [propuesta-motor-adaptativo-celda-v0_4.md:61-72](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_4.md#L61-L72)

### 2.2 Candidatos, disponibilidad y dieta

**D, directo transversal.** Estima el evento en una muestra de desarrollo contemporánea `D_T`; el árbitro estima el mismo objeto en una muestra o reserva `E_T` separada. Deben fijarse unidad de muestreo, elegibilidad, tratamiento de no respuesta, pesos y diseño de varianza. El árbitro no puede ser la misma proporción de D con otro nombre. La presencia de una medición directa dentro de un concurso de estimadores es razonable; darle el dato que los demás intentan pronosticar y presentarlo como victoria predictiva no lo es. Una evaluación de pronóstico futuro exigiría otro diseño y otro corte de información.

**M, matriz.** Necesita una ruta desde las distribuciones consumidas hasta el estimando, no sólo valores de θ. A este SHA `g()` revisa B entera y no admite un argumento de selección de generadores: incluso una ruta conceptual ajena a G5 requiere un cambio explícito de implementación o una matriz participante construida bajo contrato. Si la ruta sí toca G5, se debe especificar y sostener la forma/magnitud de `familismo_obligacion`; cero no es ausencia. También faltan θ computables y la forma concreta de `h_r`; no se infieren de haber registrado un candidato. [milpa/src/matriz.py:138-160](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/milpa/src/matriz.py#L138-L160) [milpa/src/theta.py:35-54](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/milpa/src/theta.py#L35-L54) [propuesta-motor-matriz-v0_1.md:73-79](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-matriz-v0_1.md#L73-L79)

**b, persistencia.** Exige misma definición, población, dominio y ventana, con una ola anterior disponible al corte. Otra encuesta de confianza no cuenta como ola previa por parecido temático. Si no hay serie comparable, se declara `INEJECUTABLE`; no se rellena con el promedio nacional ni con otro constructo. El baseline de la tríada es diagnóstico previo, no autorización para adoptar sus cifras. [forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md:10](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md#L10) [forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md:42-59](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md#L42-L59)

**L no entra en el piloto mínimo.** Es una decisión de diseño externo para limitar costo y contaminación no verificable; no un juicio sobre su capacidad. Si Dirección lo incorpora, debe fijar L-solo y L+corpus separadamente, modelo/versión/corte, prompts, réplicas y agregación; ninguna dieta puede contener E_T ni los resúmenes que la revelan. Un corpus sin R no prueba ausencia de R en preentrenamiento. La dispersión entre respuestas no se trataría como IC muestral ni intervalo predictivo calibrado. El contrato distingue dieta y rol, y el careo exige comprometer emisiones antes de R. [propuesta-motor-adaptativo-celda-v0_5.md:35-43](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_5.md#L35-L43) [forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:34-36](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md#L34-L36)

### 2.3 Criterio antes del dato: puntuar no es coronar

1. **Admisión primero:** mismo p(S,T), misma unidad/escala, apoyo del crosswalk al grano elegido, fuentes adquiridas y acceso separado. Un candidato inelegible es SKIP, no error infinito ni derrota estadística. Si quedan menos de dos familias, se termina en factibilidad.
2. **Regla descriptiva primaria propuesta:** para candidatos con punto legítimo q_j, publicar e_j=|q_j−R̂| y sensibilidad `E[|q_j−R*|]` sobre réplicas de diseño de R, si existen. Todas las distancias quedan en proporción. Si sólo hay IC de R, no se inventa su distribución ni un EE a partir de una fórmula normal sin justificarla. Estos son diagnósticos; un error contra R̂ no es error observado contra la verdad poblacional.
3. **Banda sin punto:** M no recibe un punto medio automático. Publicar mínimo/máximo de e sobre sus escenarios; ordenar robustamente sólo si todos sus escenarios permiten la misma conclusión bajo los márgenes declarados. Esto es una comparación conservadora de escenarios, no un scoring probabilístico propio ni una prueba de identificación. Si M no entrega una distribución predictiva, CRPS no se aplica a su banda como si la entregara.
4. **Regla vigente del careo, una cita textual:** “si ambos caen dentro del IC de R o si |d_L−d_M| < 0.5·EE(R)”. Son condiciones disyuntivas, no dos requisitos simultáneos. [forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:38](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md#L38)
5. **Alcance de esa regla:** fue escrita para el par L/M. Este borrador propone aplicarla conservadoramente a cada contraste de dos puntos elegibles; esa extensión requiere decisión, no se atribuye al contrato. Define d_j=|q_j−R̂| en proporción, separadamente de cualquier CRPS/Brier. Con más de dos candidatos no hay desempate automático por transitividad. Para una banda se informa si la condición vale para todos, algunos o ningún escenario; si no hay orden robusto, no se adjudica. `NO-APLICA` fuera de ADV-DUELO y la insuficiencia del validador de enum están declarados en v0.5. [propuesta-motor-adaptativo-celda-v0_5.md:51-59](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_5.md#L51-L59) [propuesta-motor-adaptativo-celda-v0_5.md:130](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_5.md#L130)
6. **Umbrales:** 0.5·EE(R) es un umbral heredado de indecidibilidad, no una mejora material ni un nivel de significación. El margen material queda `PENDIENTE-DERIVACION`; para emitir una decisión tendría que derivarse y aprobarse usando precisión previa y pérdida del consumidor, antes de abrir E_T. Sin consumidor y margen no se completa un concurso decisional. No se inventa aquí un 1% universal. [propuesta-motor-adaptativo-celda-v0_5.md:61-69](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_5.md#L61-L69)
7. **Skill:** se adopta sólo como diagnóstico `1−e_j/e_b`, mismo universo y pérdida para todos; si e_b=0, skill es indefinido y se publican los errores y su diferencia, sin epsilon oculto. Cuando e_b es pequeño se muestra su magnitud. Para bandas se entrega un rango de skill condicionado al baseline, sin interpretarlo como IC. Un intervalo de escenario y un IC no se convierten en distribuciones por compartir dos extremos. La dependencia del denominador debe viajar en cualquier inferencia posterior. El careo incluye skill, pero la ejecución histórica de B-piso no adjudica. [forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:38-42](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md#L38-L42) [forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md:93-99](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md#L93-L99)

**Consecuencias B-bis propuestas, exhaustivas:**

| Resultado del piloto | Lo que significa | Acción permitida |
|---|---|---|
| No corre la ruta o no hay comparación admisible | Factibilidad fallida o parcial | Entregar el bloqueo nominal; ninguna refutación de la conducta |
| Todos los candidatos compatibles con R / contraste indecidible | Sobreviven las comprobaciones declaradas; no equivalencia demostrada | Publicar resultados e incertidumbre; no elegir por preferencia |
| Alguno es incompatible con R | Incompatibilidad local bajo el criterio fijado | Informar qué candidato/alcance falla; no refutar todo el motor |
| Ninguno añade mejora material frente a b | El costo adicional no se justifica en ese uso con esta evidencia | Mantener b como referencia; adopción operativa de b es decisión separada |
| Alguno obtiene menor pérdida en la evaluación reservada | Desempeño local del procedimiento congelado | Informar diferencia y alcance, sin campeón global ni identificación causal |

No refutado no significa verdadero, equivalente ni validado. El contrato separa comparación/falsación/calibración y el careo declara piloto sin ganador; una comparación de una celda no hereda por analogía potestad de adopción. [propuesta-motor-adaptativo-celda-v0_3.md:44](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_3.md#L44) [forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:40-42](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md#L40-L42)

### 2.4 Incertidumbre tipada, emisión y decisión

| Candidato | Única familia de intervalo prevista | Qué queda fuera |
|---|---|---|
| D | IC muestral sobre la proporción, con diseño complejo | Heterogeneidad individual, sesgo de no respuesta no modelado, cambio temporal |
| M | Envolvente de escenarios de parámetros/mecanismo predefinidos | No tiene cobertura frecuentista ni probabilidades sobre escenarios por defecto |
| b | Intervalo predictivo, sólo si errores de pronósticos previos comparables permiten estimarlo | El IC de la ola anterior no es, por sí solo, un intervalo de la ola objetivo; si falta calibración, emitir punto con incertidumbre predictiva no estimada |

El árbitro conserva su IC muestral por separado. La posibilidad de informar un punto sin intervalo predictivo no autoriza a tratarlo como certeza. La distinción entre evaluación en datos de prueba y ajuste está desarrollada por Hyndman y Athanasopoulos, [FPP3, §5.8](https://otexts.com/fpp3/accuracy.html); la receta concreta aquí es propuesta propia.

Se emite el objeto completo, con `estado_decision=AMBIGUA` si atraviesa el umbral τ del consumidor. Ejemplo sintético: p∈[0.42,0.58], τ=0.50, emite el intervalo pero se abstiene de activar la acción. Si toda la región admitida está por encima o por debajo, la acción es estable bajo ese tipo de incertidumbre y esos supuestos, no universalmente segura. Si τ o la función de pérdida no están definidos, se emite descripción y `SIN-REGLA-DECISION`. Fuera de soporte se distingue `NO-TRANSPORTABLE`, sin ocultarlo como mera banda ancha.

### 2.5 Desarrollo, evaluación y parada

**No hay partición concreta acreditada en §1.** El procedimiento condicional exige primero identificar una reserva ya adquirida y no utilizada por selección, por L o por ajuste. En una transversal, la separación debe respetar conglomerados y estratos, con pesos adaptados a las probabilidades de asignación; separar personas del mismo hogar/UPM como si fueran independientes no garantiza un test externo. Si se usa una ola distinta, mantener periodo objetivo y comparabilidad declarados. Ninguna de estas operaciones borra una exposición previa. Tampoco la ausencia de solapamiento garantiza independencia probabilística: en una partición de la misma muestra hay que considerar el diseño conjunto y la covarianza pertinente al comparar los dos estimadores.

La selección de candidatos, hiperparámetros, escenarios y crosswalk pertenece a desarrollo. **Si se elige el champion viendo E_T, E_T pasa a ser selección y ya no puede certificar por segunda vez el desempeño del champion elegido.** Para medir el procedimiento completo se requiere un nivel externo preservado o una validación anidada apropiada; no basta renombrar el mismo holdout. Este mecanismo es el riesgo de selección documentado por [Cawley y Talbot (2010)](https://jmlr.org/papers/volume11/cawley10a/cawley10a.pdf). La aplicación al piloto es nuestra propuesta, no una nueva obligación retroactiva del canon.

**Parada de factibilidad:** termina con una ruta que produce un objeto bien tipado y sus dependencias comprobadas, o un bloqueo específico; no afirma desempeño nuevo si los datos ya fueron vistos. **Parada de desempeño:** termina tras una única apertura de la evaluación preservada del procedimiento previamente congelado, con errores y abstenciones completos. Una sola celda permite desempeño local, no estimar cobertura empírica de 95% ni validar todos los segmentos.

**Este diseño NO decide:** M1/A/B; cuál es la ganadora; adopción de un estimador; magnitud de G5; nuevos cortes; firma del crosswalk; umbral del consumidor; margen material; corrección de parámetros del modelo; causalidad; apertura de F6; nueva adquisición; ni que las 15 distribuciones o el motor completo queden resueltos. El cascarón v0.5 por sí solo tampoco autoriza ejecución. [propuesta-motor-adaptativo-celda-v0_5.md:118-130](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_5.md#L118-L130)

## 3 · Adversarial de «cada celda su estimador»

Todos los números de este apartado son **contraejemplos sintéticos**, no estimaciones mexicanas ni propuestas de parámetros. `YA-PREVISTO` significa que el contrato nombra una regla operativa para el riesgo; no que su ejecución esté acreditada. `PREVISTO-SIN-MECANISMO` significa que lo nombra pero la prescripción no basta para detectarlo/controlarlo en este uso. `NO-PREVISTO` significa **NO-ENCONTRADO** en el corpus contractual indicado, no inexistencia en todo el repositorio.

### 3.1 Selección post-hoc del resultado deseado

**Mecanismo:** elegir método, criterio o población después de ver cuál produce la conclusión preferida.

**Ejemplo:** R=0.40; A=0.39 y B=0.60. Se elige B porque activa una acción a 0.50, o se cambia de MAE a una función que sólo penaliza subestimar. **Síntoma:** el método o criterio final difiere del comprometido antes de R. **Mínimo:** una comprobación de identidad del procedimiento ejecutado contra el pre-registro y publicación de todos los candidatos previstos, incluidos los fallidos. No impide toda selección informal anterior, pero detecta el cambio documentable.

**Estado: YA-PREVISTO.** Declaración previa y prohibición de elegir por signo esperado; Ronda1 advierte incluso sobre criterios hechos a medida. [propuesta-motor-adaptativo-celda-v0_1.md:117-119](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_1.md#L117-L119) [forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md:71](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md#L71)

### 3.2 Multiplicidad de adjudicaciones

**Mecanismo:** cada concurso tolera un falso hallazgo, y el conjunto publica sólo sus victorias.

**Ejemplo:** con 20 contrastes nulos independientes y α=0.05, P(al menos uno falso)=1−0.95²⁰≈0.642; con 100, se esperan 5 falsos. **Síntoma:** muchos champions marginales, pocos que repliquen. **Mínimo:** antes de abrir datos, definir la familia de afirmaciones y controlar su error; una opción simple es Bonferroni α/K para declaraciones confirmatorias, manteniendo las otras como exploratorias. Esta cota conservadora sale de la desigualdad de la unión; no requiere independencia. FDR sería otra decisión, no sustituto automático cuando se quiere proteger cada acción. [Benjamini–Hochberg (1995)](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x) distingue FDR de FWER; aquí no se usa su procedimiento sin revisar sus supuestos.

**Estado: PREVISTO-SIN-MECANISMO suficiente.** Contar patrones y cerrar el menú no controla por sí mismo una tasa global. La corrección fina fue diferida en el careo: aceptable para exploración sin coronación, insuficiente al pasar a política masiva de adjudicación. [forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md:68](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md#L68) [forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:26](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md#L26) [forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:50](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md#L50)

### 3.3 Champions conjuntamente imposibles: qué alcanza D8

**Mecanismo:** concursos locales asignan valores incompatibles a un parámetro declarado compartido o a probabilidades vinculadas.

**Ejemplo:** para el mismo β global y la misma escala, A exige β∈[0.10,0.20] y B exige β∈[−0.20,−0.10]; no hay β que satisfaga ambas. Otro caso: p(Y)=0.30 y p(Y∩Z)=0.40. **Síntoma:** intersección vacía de restricciones, probabilidades conjuntas mayores que marginales o agregado incoherente. **Mínimo:** exigir que el conjunto de restricciones compartidas sea no vacío antes de componer; si no, conservar resultados locales sin agregarlos y devolver el conflicto nominal.

**Estado: PREVISTO-SIN-MECANISMO completo.** D8 pide cierre global y signos; eso es necesario, pero no fija todas las identidades ni garantiza factibilidad conjunta. Signos opuestos **no son contradicción** si son β(x) de poblaciones diferentes, previamente definidos como heterogéneos. El test debe comparar el mismo `parametro_compartido_id`, no imponer homogeneidad por cercanía de celdas. [propuesta-motor-adaptativo-celda-v0_3.md:98-102](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_3.md#L98-L102) [forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md:40](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md#L40) [propuesta-motor-matriz-v0_1.md:199](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-matriz-v0_1.md#L199)

### 3.4 Persistencia imbatida y presión para fabricar valor añadido

**Mecanismo:** se oculta b o se cambia el universo para obtener una victoria del modelo complejo.

**Ejemplo:** errores b=0.01, M=0.03, D=0.02: skills −2 y −1. **Síntoma:** b desaparece del resumen o se comparan MAE de universos distintos. **Mínimo:** tabla común de casos y regla explícita “sin mejora material → ninguna promoción por este piloto”. b puede seguir como referencia; sustituir una medición contemporánea por un pronóstico requiere un consumidor que realmente necesite pronóstico.

**Estado: YA-PREVISTO.** El careo tiene consecuencia propia para que ninguno venza b; B-piso exige mismo universo. [forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:42](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md#L42) [forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md:59-67](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md#L59-L67)

### 3.5 Ajuste clandestino al árbitro

**Mecanismo:** R se filtra a parámetros, a la elección de escenarios o al corpus, aunque la corrida diga “sin calibración”.

**Ejemplo:** una salida inicial 0.25 se desplaza a 0.49 después de leer R=0.50; MAE aparente pasa de 0.25 a 0.01. **Síntoma:** cambios de código/insumos tras la apertura, R o equivalentes entre dependencias, o nuevos prompts que contienen su resumen. **Mínimo:** congelar código, insumos y emisiones antes de liberar R y comprobar el DAG de dependencias más el momento de acceso; con exposición conocida, degradar a diagnóstico. Un hash anterior no prueba ignorancia si la cifra ya se conocía por otro canal.

**Estado: YA-PREVISTO como prohibición y secuencia; verificación de acceso limitada.** El contrato declara antes del ajuste y el careo compromete emisiones antes de R. La prohibición propia de ajustar θ al árbitro también está en el insumo externo D-θ v1.1, §4/§6, sin atribuirle por eso un sello de este SHA. [propuesta-motor-matriz-v0_1.md:128-130](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-matriz-v0_1.md#L128-L130) [forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:36](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md#L36)

### 3.6 Una ola: el mismo dato calibra y evalúa

**Mecanismo:** ajustar la media de la única muestra y “validar” contra esa misma media.

**Ejemplo:** 40 éxitos/100 observaciones → θ=0.40; árbitro=0.40; error=0 por construcción, aunque en otra muestra sea 0.25. **Síntoma:** mismos IDs o mismas UPM en ajuste y evaluación, o total publicado que permite reconstruir la reserva. **Mínimo:** partición declarada y respetada al nivel de dependencia del diseño; cuando hubo exposición previa, etiquetar factibilidad y no recertificar ceguera mediante un split nuevo.

**Estado: YA-PREVISTO en principio; necesita concretarse por celda.** Ronda1 prescribe holdout intocado, pero no vuelve independiente una partición cuyo resultado ya influyó en la selección. [forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md:65](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md#L65) [propuesta-motor-adaptativo-celda-v0_2.md:80-81](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_2.md#L80-L81)

### 3.7 El holdout usado para elegir deja de ser prueba final

**Mecanismo:** escoger el menor error entre muchos candidatos en el holdout y publicar ese mínimo como desempeño independiente del seleccionado.

**Ejemplo:** dos métodos con error real 0.10 dan estimaciones 0.08 y 0.12 por azar; siempre se publica 0.08 como “validado”. **Síntoma:** no hay conjunto externo al proceso que eligió al ganador. **Mínimo:** evaluar selección+método como un procedimiento único en un nivel externo preservado; si no lo hay, informar selección exploratoria. No hace falta fabricar otra partición para una tarea meramente descriptiva.

**Estado: PREVISTO-SIN-MECANISMO inequívoco.** El riesgo de doble uso se nombra, pero evaluar el criterio sobre holdout no distingue selección de evaluación final. [forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md:65](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md#L65) La justificación estadística y evaluación anidada están en [Cawley–Talbot](https://jmlr.org/papers/v11/cawley10a.html); no se afirma que el contrato ya las exija.

### 3.8 Mezcla de banda, punto y distribución

**Mecanismo:** el agregador convierte silenciosamente formas de salida diferentes en escalares.

**Ejemplo:** peso 0.5 para p₁∈[0.2,0.8] y 0.5 para p₂=0.4 produce [0.3,0.6], no una certeza en 0.45. **Síntoma:** se pierde el tipo de incertidumbre o aparece un resultado preciso donde el insumo era parcial. **Mínimo:** despachar por tipo; si falta operador válido para esa combinación, devolver no componible sin descartar los resultados locales.

**Estado: YA-PREVISTO; receta general incompleta.** Ronda1 exige un dry-run con salidas no puntuales sin colapso; los tipos nativos están enumerados. [forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md:101](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md#L101) [propuesta-motor-adaptativo-celda-v0_1.md:121-133](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_1.md#L121-L133)

### 3.9 Dependencia entre celdas e intervalos marginales

**Mecanismo:** intervalos de celdas que comparten muestra se combinan suponiendo independencia.

**Ejemplo:** dos estimaciones con EE=0.10, correlación 1 y pesos 0.5 tienen EE agregado 0.10; asumir independencia da 0.0707. Dos IC marginales 95% independientes tienen cobertura conjunta 0.9025, no 0.95. **Síntoma:** error agregado demasiado pequeño o cobertura atribuida sin réplica conjunta. **Mínimo:** compartir índices de réplicas cuando la muestra es común, o usar cotas declaradas sin etiqueta de IC conjunto.

**Estado: PREVISTO-SIN-MECANISMO suficiente.** Grafo de fuentes y quitar una fuente detectan sensibilidad, pero no sustituyen covarianzas o réplicas alineadas. [forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md:66](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md#L66)

### 3.10 Extrapolación fuera de soporte en celdas pequeñas

**Mecanismo:** el ganador local se usa para una combinación x sin observaciones comparables.

**Ejemplo:** se estima sobre edades 30–50 y 200 casos urbanos; se emite para 18 años rural con n=0 y una banda artificialmente estrecha. **Síntoma:** vacío de soporte, pesos extremos o denominador efectivo insuficiente. **Mínimo:** máscara de soporte previa al cómputo y prueba de denominador/diseño; fuera del dominio, abstenerse o emitir escenario explícito. No fijar aquí un n mínimo universal desconectado de la pérdida y del diseño.

**Estado: PREVISTO-SIN-MECANISMO genérico suficiente.** Hay declaración de transporte y disponibilidad por celda; no se encontró una máscara ejecutable de soporte común en v0.3/v0.5/Ronda1 (`soporte`, `extrapol`, `support`, `n_efectivo`). [propuesta-motor-adaptativo-celda-v0_3.md:72](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_3.md#L72) [propuesta-motor-adaptativo-celda-v0_1.md:101-109](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_1.md#L101-L109)

### 3.11 Falsa desagregación del árbitro

**Mecanismo:** una media sobre dos categorías se copia a cada categoría fina y luego se presenta como heterogeneidad medida.

**Ejemplo:** pesos internos iguales y p del grupo=0.60 admiten p₁=0.20 y p₂=1.00, o ambos 0.60. El agregado no elige entre ellos. **Síntoma:** dos salidas finas idénticas derivadas de un único punto grueso, sin supuesto de homogeneidad. **Mínimo:** rango de la aplicación de agregación y prohibición de inversa sin identificación; componer en grano común o conservar el conjunto de soluciones.

**Estado: NO-PREVISTO como mecanismo de inversión en v0.3/v0.5/Ronda1**, búsqueda `N-a-1`, `resolución`, `desagreg`, `crosswalk`, `inversa`. El crosswalk posterior dentro del corte sí declara la pérdida: por eso hoy no puede tratarse como detalle cosmético. [data/crosswalk-ejes-arbitro-modelo-v1_0.tsv:10](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/crosswalk-ejes-arbitro-modelo-v1_0.tsv#L10)

### 3.12 Universos o constructos distintos bajo la misma escala

**Mecanismo:** dos proporciones 0–1 se comparan como estimadores del mismo parámetro aunque difiera su denominador/evento.

**Ejemplo:** 0.70 de acuerdo con una norma general y 0.08 de cuidadores que dicen actuar por obligación; restarlos no mide sesgo de un estimador. **Síntoma:** candidato y árbitro tienen filtros, periodos o eventos distintos. **Mínimo:** igualdad del contrato semántico o enlace explícito con supuesto de transporte; de lo contrario son celdas distintas.

**Estado: YA-PREVISTO.** El contrato separa constructos y añade universo/escala; la celda de conducta contiene el límite concreto. [propuesta-motor-adaptativo-celda-v0_3.md:84-86](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_3.md#L84-L86) [data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml:123](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml#L123)

### 3.13 Elegir por disponibilidad y borrar los SKIP

**Mecanismo:** sólo se muestra desempeño de celdas fáciles, aunque el consumidor necesite la malla completa.

**Ejemplo:** diez celdas: dos fáciles con error 0.01, ocho sin salida; publicar “MAE=0.01” sin cobertura convierte 20% en éxito general. **Síntoma:** denominadores variables y motivos de omisión ausentes. **Mínimo:** publicar cobertura y SKIP sobre el universo fijado junto al error de los casos comunes; no imputar ceros a faltantes.

**Estado: YA-PREVISTO.** Universo de candidatos, indecidibles/SKIP y conteo visible ya tienen lugar contractual. [propuesta-motor-adaptativo-celda-v0_3.md:48](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_3.md#L48) [propuesta-motor-adaptativo-celda-v0_5.md:51-59](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_5.md#L51-L59) [forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:40](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md#L40)

### 3.14 Costo del contrato y capacidad real de adjudicación

**Mecanismo:** crear un expediente completo por fila de registro antes de comprobar si la elección puede cambiar una salida útil.

**Ejemplo:** 100 celdas ×4 horas de adjudicación=400 horas; con 20 horas disponibles sólo caben 5 incluso sin costo común. Si 90 carecen de segundo candidato, la mayor parte no compra una decisión. **Síntoma:** crecen expedientes y no cambian consumidores ni resultados utilizables. **Mínimo:** criba a–g con parada al primer defecto decisivo y registrar horas por celda terminada, reutilizando receta cuando el estimando y el diseño lo permitan.

**Estado: PREVISTO-SIN-UMBRAL de costo/beneficio.** Ronda1 pide horas/celda; v0.3 acepta los umbrales del piloto. No fija cuántas adjudicaciones valen lo que cuestan para cada uso. [forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md:98-105](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md#L98-L105) [propuesta-motor-adaptativo-celda-v0_3.md:193](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_3.md#L193)

**Respuesta cuantitativa honesta:** con los siete criterios de este encargo, hay **0 celdas inmediatamente certificables**, no “207 posibles adjudicaciones” ni “23 listas”. El número potencial tras resolver reservas es **no estimable con estos metadatos**: faltan horas observadas, acceso efectivo y reservas asignadas. Para un presupuesto H, costo común C₀ y costos marginales cᵢ, el máximo operativo satisface Σcᵢ≤H−C₀, además de elegibilidad; si fueran iguales, K≤min(N_elegibles,⌊(H−C₀)/c⌋). Es una restricción de planificación, no una estimación del repo. No se exige abrir 10–15 celdas para aprender si una ruta calcula; esos eran los umbrales del piloto amplio de Ronda1, no un costo mínimo para este encargo de una celda.

### 3.15 Sobrevivir, empatar y adquirir falsa precisión decisional

**Mecanismo:** una banda ancha siempre solapa R y se interpreta como validación o licencia de acción.

**Ejemplo:** candidato [0,1], R=0.40, τ=0.50: no queda refutado por cobertura, pero no discrimina la decisión. **Síntoma:** “dentro de banda” sin anchura, utilidad ni consecuencia para el consumidor. **Mínimo:** separar compatibilidad, precisión útil y decisión estable; un escenario que contiene R no gana automáticamente frente a un punto.

**Estado: PREVISTO-SIN-MECANISMO universal de consumidor.** Ronda1 ya admite empate sin adjudicación y v0.5 abre `margen_material`; no se encontró un operador genérico intervalo→acción en v0.3/v0.5/Ronda1 (`umbral`, `consumidor`, `abst`, `decisión automática`). [forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md:67](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md#L67) [propuesta-motor-adaptativo-celda-v0_5.md:61-69](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_5.md#L61-L69)

### 3.16 ¿Cuándo es peor que un estimador único con etiqueta?

Para quien compara salidas entre celdas, **sí puede ser peor** por selección post-hoc/multiplicidad, inestabilidad de ganadores, incoherencia de parámetros compartidos y manejo desigual de soporte/incertidumbre. Cada celda añade libertad de selección y puede introducir saltos que parecen diferencias de población. Ejemplo sintético: el mismo p=0.50 en dos segmentos recibe estimador A=0.40 en uno y B=0.60 en otro por ruido de sus concursos; el lector ve una brecha 0.20 creada por el selector. Un procedimiento único previamente fijado reduce ese grado de libertad y facilita comparar, aunque no garantice exactitud.

La falta de soporte, la fuga de R y los denominadores incompatibles también dañan a un estimador único: una etiqueta no los cura. Y un estimador único puede imponer sesgo sistemático o una escala incorrecta a todas las celdas. Por tanto, **la comparación justa es política completa contra política completa**, con idénticos objetivos, presupuesto y evaluación externa: selección incluida como parte del método. Mientras no se acrediten controles de selección y composición, prefiero para lectura transversal un método común predefinido donde sea admisible, con abstenciones explícitas, y candidatos locales como diagnóstico. Donde el dato exija estimadores distintos, la diversidad es razonable; lo que debe ser común es el contrato semántico y el criterio de comparación. No se infiere causalidad de ninguna de las dos arquitecturas.

## 4 · Interfaz mínima para composición — especificación breve

**Viable con límites.** Mezclar puntos y bandas no impide componer; impide prometer un punto o IC común sin reglas. La propuesta matricial define `m=Σπ·h_r(Bθ,C)` y exige declarar `h_r`; v0.3 sitúa el catálogo en la frontera entre estimación y composición. [propuesta-motor-matriz-v0_1.md:73-79](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-matriz-v0_1.md#L73-L79) [propuesta-motor-adaptativo-celda-v0_3.md:98-102](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/propuesta-motor-adaptativo-celda-v0_3.md#L98-L102)

### 4.1 Campos mínimos por entrada

| Bloque | Campos mínimos propuestos | Por qué hacen falta |
|---|---|---|
| Identidad semántica | `id`, `estimando`, `slot` (β/θ/contexto/respuesta/momento), evento, unidad de observación, periodo, filtro de universo | Una probabilidad final no puede entrar como β sólo porque sea numérica |
| Dominio y soporte | coordenadas y versión de cortes; unidad persona/hogar; máscara de soporte; n/diseño efectivo pertinente; restricciones de transporte | Evita dar salida a x no observado o mezclar personas con hogares |
| Escala | unidad numérica, rango, orientación, codificación, `link_id` y versión con dominio/codominio | Distingue proporción, porcentaje, logit, índice y coeficiente |
| Valor y forma | punto, intervalo, conjunto, función o distribución; referencia al artefacto; familia de incertidumbre; cobertura sólo si está justificada | No transforma una banda en una distribución ni un punto en certeza |
| Dependencia | `parametro_compartido_id`, `fuente_grupo`, réplicas/covarianza alineadas o dependencia desconocida | Hace comprobable D8 y evita sumar IC como si fueran independientes |
| Agregación | operador A del crosswalk; firmas/alcance; masa π por dominio y su universo; normalización; incertidumbre de π; población excluida | Distingue pérdida de resolución de falta de cobertura |
| Procedencia y uso | fuentes/SHAs, transformación/ejecutable, rol desarrollo/evaluación, estado de adopción, consumidor y regla de abstención | El compositor sabe qué puede consumir y qué sigue siendo diagnóstico |

Son **campos propuestos**, no columnas que se afirme existentes. El TSV actual sólo tiene 12 columnas, entre ellas nivel, cómputo pretendido y disponibilidad; no contiene una representación de valores, covarianzas, operadores de escala o soporte como ésta. [milpa/catalogo-momentos-v0_1.tsv:1](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/milpa/catalogo-momentos-v0_1.tsv#L1)

### 4.2 Reglas de cálculo

1. **Despacho semántico antes que numérico.** `slot=respuesta` de una medición directa alimenta el agregado de respuestas; no se aplica `h_r` otra vez. Si la celda entrega θ o β, entra a esa ranura sólo si el estimando y la escala coinciden. Un β ajustado, una proporción de conducta y una prevalencia de atributo no son intercambiables.
2. **Puntos:** se computan como valores condicionados a los supuestos declarados. Sin incertidumbre, sólo hay resultado puntual condicional; no IC degenerado acreditado. **Bandas de escenarios:** se propagan mediante el conjunto de parámetros admisibles y el operador completo, con mínimos/máximos cuando sean computables. Si h_r no es monótona, evaluar extremos aislados no basta.
3. **IC muestrales:** propagar réplicas conjuntas o una aproximación con covarianza justificada. No sumar intervalos marginales atribuyendo cobertura 95%. Si falta dependencia, emitir cotas de sensibilidad o abstenerse de atribuir cobertura. La incertidumbre de los pesos también se propaga cuando π es estimada.
4. **No linealidad:** h_r(Eθ) no equivale a E[h_r(θ)]. Ejemplo sintético con logística: θ=0 o 2 equiprobables da respuesta media ≈0.6904; usar θ media=1 da ≈0.7311. Si el modelo pretende distribución de agentes, hay que conservar la distribución conjunta necesaria, no sólo la media de cada atributo.

### 4.3 Resolución y pesos

Para una celda gruesa S, `p_S=Σ_{x∈S}π_x p_x / Σ_{x∈S}π_x`. La medición gruesa restringe esa suma, no cada p_x. Si sólo se pretende el agregado en el mismo grano, se puede componer directamente con π_S. Si el consumidor exige cortes finos, se mantienen los valores desconocidos como conjuntos o se declara un supuesto de homogeneidad; no se atribuye ese supuesto al dato.

Ejemplo sintético: π₁=π₂=0.25 y p_S=0.60 implican p₁+p₂=1.20; por [0,1], cada tasa está entre 0.20 y 1.00. Su contribución total es 0.30, identificada a ese grano; las dos tasas no. La media gruesa de ENIF tampoco se puede reponderar automáticamente a una mezcla ENIGH distinta: o se acepta transporte del promedio grueso o se necesitan tasas internas. El crosswalk declara que igualar catálogos no iguala marginales. [data/crosswalk-ejes-arbitro-modelo-v1_0.tsv:10](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/crosswalk-ejes-arbitro-modelo-v1_0.tsv#L10)

En formalidad el problema es mayor que 2→2: derechohabiencia por cualquier vía y servicio médico por trabajo no determinan el mismo conjunto de personas. No basta un renombre ni una matriz de dos etiquetas; hace falta un puente poblacional verificable o una restricción de uso. [data/crosswalk-ejes-arbitro-modelo-v1_0.tsv:9](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/data/crosswalk-ejes-arbitro-modelo-v1_0.tsv#L9)

### 4.4 Prohibiciones y una comprobación previa

Prohibido: punto medio silencioso; convertir [0,1] en cobertura estadística; copiar un promedio a subceldas como dato; renormalizar π sobre las celdas disponibles ocultando excluidas; cambiar escala por cercanía numérica; recalibrar al árbitro final para que D8 pase; tratar IC de la media como dispersión individual; inventar independencia.

**Una comprobación de contrato antes de componer**, con un fixture correcto y sus variantes inválidas: cada arista productor→consumidor debe conservar `(estimando, universo, periodo, unidad, slot, escala)` o declarar un operador válido; A y π deben cubrir exactamente el dominio anunciado y sumar la masa prevista; toda celda solicitada debe tener soporte y valor/estado admisible; las restricciones compartidas deben ser compatibles.

Caso sintético: `valor=35, escala=porcentaje` sólo entra a un consumidor de proporción con conversión /100 declarada; sin ella falla. `valor=0.35, escala=beta_logit` también falla aunque esté dentro de [0,1]. Un rango numérico no detecta una mentira de metadatos: la escala debe vincularse a reactivo/codificación y fórmula productora; comprobar una transformación conocida protege lo verificable, no certifica semántica por magia. Ésta es la implementación mínima propuesta para los huecos que el esquema actual reconoce no validar. [tests/test_celdas_d.py:49-64](https://github.com/Josanoforo/Modelado-Mexicano/blob/b881ee6/tests/test_celdas_d.py#L49-L64)

**Salida si falla composición:** conservar estimaciones locales con su alcance y devolver `NO-COMPONIBLE:<causa>`. No mutilar intervalos para obtener un agregado y no llamar fracaso científico a una interfaz todavía incompleta.

## Cierre para el careo con Dirección

Las diferencias que vale la pena resolver en el careo son cuatro: si Dirección acredita una celda que sí cumpla (a)–(g); cuál es su evidencia de reserva; si compara estimadores del mismo parámetro o distintos productos; y cómo conserva incertidumbre y población al componer. Ninguna se resuelve eligiendo una celda por obligación de entregar una ganadora.

**¿El proyecto queda más cerca de una medición o decisión mejor? Sí:** este retorno evita un piloto falsamente ciego, deja un procedimiento condicionado reutilizable y precisa qué contrato mínimo permite leer y agregar estimadores heterogéneos. No acredita todavía desempeño nuevo ni adjudicación. La siguiente acción útil es contrastar una candidatura nominal de Dirección contra esta tabla; si tampoco pasa, decidir explícitamente un piloto de factibilidad con datos expuestos, sin disfrazarlo de evaluación ciega ni ordenar nuevas descargas.

## Apéndice · Fuentes y comprobaciones

Las citas con `archivo:línea` remiten únicamente a `b881ee6`. Se analizaron registros/documentos, no microdatos. Las declaraciones de adquisición son lectura del manifiesto, no comprobación del disco de CAJA. No se ejecutaron modelos, LLM, descargas de encuestas, cambios de canon ni adjudicaciones.

Fuentes externas abiertas utilizadas, sin citas textuales:

- Cawley, G. C. y Talbot, N. L. C. (2010), *On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation*, JMLR 11:2079–2107. [Artículo completo](https://jmlr.org/papers/volume11/cawley10a/cawley10a.pdf). Uso: selección como parte del ajuste y separación de evaluación externa; no se extrapolan sus magnitudes al programa.
- Benjamini, Y. y Hochberg, Y. (1995), *Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing*. [DOI 10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x). Se abrió la página primaria con resumen; uso limitado a la distinción FDR/FWER y condiciones de la propuesta original, no una revisión exhaustiva del método.
- Hyndman, R. J. y Athanasopoulos, G., *Forecasting: Principles and Practice*, 3.ª ed., [§5.8](https://otexts.com/fpp3/accuracy.html). Uso: separar errores de evaluación y ajuste y declarar un baseline comparable. Los ejemplos numéricos, cotas y reglas específicas de este informe son elaboración propia.

Inventario de lecturas del árbol fijo, búsquedas negativas y verificación del borrador: se completa abajo a partir de los archivos efectivamente obtenidos.


### Inventario de rutas leídas @ b881ee6

Lectura completa del contrato v0.3/v0.5, Ronda1, careo, YAML y tablas pequeñas; lectura dirigida de remisiones v0.1/v0.2/v0.4, código, notas y manifiesto. Para los archivos grandes se buscaron nombres de candidata, campos de contrato, rutas, ejes y reservas; no se siguieron enlaces a payloads. El inventario distingue obtención y alcance de lectura.

| Ruta @ b881ee6 | Líneas | Alcance |
|---|---:|---|
| [propuesta-motor-adaptativo-celda-v0_3.md](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/propuesta-motor-adaptativo-celda-v0_3.md) | 224 | Completa |
| [propuesta-motor-adaptativo-celda-v0_5.md](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/propuesta-motor-adaptativo-celda-v0_5.md) | 159 | Completa |
| [propuesta-motor-matriz-v0_1.md](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/propuesta-motor-matriz-v0_1.md) | 231 | Dirigida a las secciones citadas y búsquedas descritas |
| [forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md) | 131 | Completa |
| [forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md) | 56 | Completa |
| [forense/theta-cargable-por-celda-diseno-e1-v1_0.md](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/forense/theta-cargable-por-celda-diseno-e1-v1_0.md) | 236 | Dirigida a las secciones citadas y búsquedas descritas |
| [forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/forense/prereg-caja/TRIADA-B-PISO-spec-v1_0.md) | 125 | Dirigida a las secciones citadas y búsquedas descritas |
| [forense/notas/2026-09-15-GEN2-MARCADOR-C0-D-A8-hueco.md](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/forense/notas/2026-09-15-GEN2-MARCADOR-C0-D-A8-hueco.md) | 394 | Dirigida a las secciones citadas y búsquedas descritas |
| [milpa/catalogo-momentos-v0_1.tsv](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/milpa/catalogo-momentos-v0_1.tsv) | 23 | Completa |
| [data/corrida0/demanda-resultados.tsv](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/data/corrida0/demanda-resultados.tsv) | 209 | Completa |
| [data/crosswalk-ejes-arbitro-modelo-v1_0.tsv](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/data/crosswalk-ejes-arbitro-modelo-v1_0.tsv) | 23 | Completa |
| [data/manifiesto.yaml](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/data/manifiesto.yaml) | 30065 | Dirigida a las secciones citadas y búsquedas descritas |
| [milpa/src/matriz.py](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/milpa/src/matriz.py) | 176 | Dirigida a las secciones citadas y búsquedas descritas |
| [milpa/src/celdas.py](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/milpa/src/celdas.py) | 110 | Dirigida a las secciones citadas y búsquedas descritas |
| [data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml) | 140 | Completa |
| [data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml) | 171 | Completa |
| [data/curacion-registro/celdas-d/G5.radio_confianza.encuci_vs_enbiare.yaml](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/data/curacion-registro/celdas-d/G5.radio_confianza.encuci_vs_enbiare.yaml) | 207 | Completa |
| [propuesta-motor-adaptativo-celda-v0_4.md](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/propuesta-motor-adaptativo-celda-v0_4.md) | 148 | Dirigida a las secciones citadas y búsquedas descritas |
| [propuesta-motor-adaptativo-celda-v0_2.md](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/propuesta-motor-adaptativo-celda-v0_2.md) | 201 | Dirigida a las secciones citadas y búsquedas descritas |
| [propuesta-motor-adaptativo-celda-v0_1.md](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/propuesta-motor-adaptativo-celda-v0_1.md) | 240 | Dirigida a las secciones citadas y búsquedas descritas |
| [tests/test_celdas_d.py](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/tests/test_celdas_d.py) | 296 | Dirigida a las secciones citadas y búsquedas descritas |
| [milpa/src/theta.py](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/milpa/src/theta.py) | 71 | Dirigida a las secciones citadas y búsquedas descritas |
| [milpa/catalogo-momentos-v0_1.md](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/milpa/catalogo-momentos-v0_1.md) | 146 | Dirigida a las secciones citadas y búsquedas descritas |
| [forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv) | 28 | Completa |
| [forense/prereg-duelo-v2/F6-falta-conseguir-v1_0.tsv](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/forense/prereg-duelo-v2/F6-falta-conseguir-v1_0.tsv) | 10 | Completa |
| [milpa/tramite-ola5-propuesta-v0.yaml](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/milpa/tramite-ola5-propuesta-v0.yaml) | 4111 | Dirigida a las secciones citadas y búsquedas descritas |
| [forense/prereg-duelo-v2/F5-aprendizajes-sucesor-v1_0/traza-motor.tsv](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/b881ee6/forense/prereg-duelo-v2/F5-aprendizajes-sucesor-v1_0/traza-motor.tsv) | 7 | Completa |

### Comprobaciones realizadas

- Conteos por `csv.DictReader`: 22 registros del catálogo y 207 demandas; agrupación de demanda por rangos de ID, sin sumar duplicados como celdas independientes.
- Comprobación de todas las referencias `archivo:línea` contra los archivos raw obtenidos del árbol fijo: rangos existentes.
- YAML parseable y sin errores bajo `errors_for` de `tests/test_celdas_d.py` del corte. **Pasar el esquema no acredita elegibilidad**: conserva placeholders, reserva vacía y `ejecutable: false`; no se ejecutó ni se registró la celda.
- Búsquedas contractuales de §3 efectuadas sobre v0.3/v0.5/Ronda1, con los términos allí declarados. Las coincidencias de palabras como “umbral” no se interpretaron como un operador completo de decisión.
- Única cita textual en prosa: condición de indecidibilidad del careo. Los demás pasajes se parafrasean; nombres de campos, códigos y fórmulas se conservan como identificadores técnicos.
- Los ejemplos sintéticos de §3–4 no son resultados del modelo y no se incorporan a sus parámetros. No se alteró ningún archivo del repositorio.
