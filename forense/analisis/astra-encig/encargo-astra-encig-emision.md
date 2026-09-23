# Encargo Codex CLI · ASTRA-ENCIG-EMISION-PROSPECTIVA-1

**Misión:** construir y sellar C-ASTRA para el piloto 5; no ejecutar su árbitro. **Base de redacción:** `43394b060538fdd7c472d7673f27b7b39229ac29`; rederiva contra origin/main vivo. **Rama:** `codex/astra-encig-1`, worktree propio, sin tocar la rama ENVIPE `codex/astra-interaccion-dinamica-1`. **Entorno:** Codex CLI con acceso a historia permitida; caja si hace falta leer microdato histórico. **Una sesión escritora.** **Contador:** `generacion: GEN2`, `cuenta_gen2: SI`, `adopta: NO`, solo corridas selladas. **Publicación:** primera spec concreta antes del primer push; PR propio autorizado, merge de mesa.

## 1. Producto y objetivo verificable

Entrega dos CALC propios para `tramite.gobierno_digital.util_sin_coercion`, ENCIG 2025:

- `CALC-ASTRA-ENCIG-EDADXSEXO-0001`.
- `CALC-ASTRA-ENCIG-ESCOLARIDADXSEXO-0001`.

El brief propone 16 celdas en total. Deriva categorías y llaves exactas de fuentes autorizadas, no fuerces el número. **Edad×escolaridad no entra**: lo evaluó el piloto 3 y su resultado no es una validación nueva ni sirve para elegir tu regularización.

Hecho = spec y código congelados, resultados sellados con punto/intervalo/tipo para cada celda estimable, verificación y asiento de replay, nota y recibo, PR listo. Estar elegible para piloto 5 exige además CALC en main antes de su COMMIT-2, compatibilidad exacta con su spec y cronología prospectiva. No confundas entrega con admisión.

Este encargo es independiente del de ENVIPE. No esperes sus modelos ni sus resultados; no tomes su mejor variante como ajuste de ENCIG. No entregues solo un diseño o un inventario: termina las emisiones alcanzables y su verificación.

## 2. Mandato, adjuntos y situación real

Lee `00-ARRANQUE-Y-COORDINACION-ASTRA-1.md` y `MISION-ASTRA-1-vence-al-piso-2026-09-22.md`, SHA `949a0f1a9c0054a9a82a802f8a4ce4eadab6d9d9838ecd0f765f69dde7d905bc`. La adenda 5 histórica tiene SHA `5d2e7a0ea21c02bfe2e13424c43ea93afa71b9698723a11da275baebef093497`.

El mandato posterior de Jonás fija **antes de COMMIT-2** y prevalece sobre «al abrir/en COMMIT-1» de la adenda antigua. La discrepancia viaja en el recibo; no te autoriza a editar una spec congelada del piloto. Claude/mesa trasladan el mandato a su sesión.

**LEÍDO al redactar:** la misión identifica el piloto 5 y sus cruces; su encargo no estaba en main. No inventes sus umbrales, candidatos, variables ni número final de celdas. Puedes producir una predicción propia conforme al contrato autorizado mientras llega la spec; antes de declarar admisión, compara celda por celda. Si difiere sustantivamente el universo, no relabeles un resultado para hacerlo pasar.

La misión específica gobierna el perímetro: no hagas la cascada de gobierno de un acto ordinario; entrega recibo a Claude.

## 3. Arranque y barrera de evaluación

1. Localiza clon, reporta ruta absoluta, rama, HEAD y status; `git fetch origin`. Crea/retoma un worktree propio desde main actualizado, sin reset de ramas ajenas ni doble escritor. Lee AGENTS y lo necesario para esta medición.
2. Busca por objeto/archivos si ya existen tus CALC en main o una sesión los está escribiendo. No dupliques un trabajo sellado por ignorar un nombre autogenerado de rama.
3. Lee `data/corrida0/decisiones.tsv` (`reserva:*`) con lector CSV y el estado de reserva por id del manifiesto. Lee alcance y excepciones; una liberación parcial no abre toda la ola.
4. Tu programa no puede abrir ENCIG 2025, ni para estructura, miembros de zip o primeras filas. La lista permitida de entradas ejecutables contiene únicamente historia anterior autorizada y una extracción explícita de marginales públicos sellados de `milpa/tramite-ola5-propuesta-v0.yaml`. No explorar globalmente R ni resultados de pilotos objetivo. Ninguna ola posterior a 2023 se usa como historia para predecir 2025.
5. Identifica celdas por metadatos de marcador/specs y consumos declarados, sin leer R. El marcador aislado puede estar desfasado: el piloto 3 ya vio edad×escolaridad y no entra aunque una fila vieja dijera RESERVADA. Documenta la elegibilidad de tus dos grupos.
6. Declara exposición previa de la sesión; un cruce visto se excluye de prospectiva. Git no registra toda lectura: usa historial más inventario/trazas y declaración, nunca «cero coincidencias de git log» como demostración absoluta de ceguera.

## 4. Contrato de medida y fuentes útiles

Lee `forense/prereg-caja/ENCIG-CRUCES-HISTORICOS-spec-v1_0.md`, los cuestionarios/FD de olas históricas y la documentación autorizada del desenlace. **LEÍDO al redactar:** proporción de TRÁMITES de pago ordinario de luz (`N_TRA=01`), `P7_3` válido en {01,02,04,05,06}, evento digital {04,05}, ponderador `FAC_TRA`. No personas, no «cualquier trámite», no población que no realizó trámites. Verifica el texto de las categorías de canal: no equipares automáticamente un kiosco con otra noción de digitalización.

Verifica mapeo de edad/sexo/escolaridad, universo común para marginales y cruces, cardinalidad del enlace por persona entre tabla de residentes y trámites, estrato/UPM, ponderadores positivos y códigos faltantes. En historia hay edad 60–96: demuestra que la etiqueta 60+ del objetivo corresponde al mismo universo, no la declares equivalente por nombre.

Historia mínima candidata, registrada pero sin comprobación de disponibilidad local en esta preparación:

| id | SHA-256 |
|---|---|
| `encig2021_csv` | `c92ea34c7c57237c49ca3d8d99382e340b5939c371ce820332876f7c4c62c56a` |
| `encig23_base_datos_csv` | `af733d867a568cbb0dadef4a5a793b02488a71728d1157860f14501f3d4c393d` |

**EXISTEN en main** `CALC-ENCIG2021-CRUCES-HISTORICOS-0003` y `CALC-ENCIG2023-CRUCES-HISTORICOS-0002`, además de versiones anteriores. Verifica cuál rige, sellos, semántica y compatibilidad; no uses «el número mayor» como único criterio. La existencia de estas piezas permite una vía rápida si contienen exactamente la historia que necesita el modelo.

Preferencia operativa: aprovechar estadísticas históricas selladas cuando bastan estadísticamente, manteniendo RESULT/sha/linaje. Si faltan covarianzas o réplicas imprescindibles, usa el microdato histórico autorizado con diseño muestral; no suplas esa dependencia fingiendo independencia exacta. No necesitas recalcular todo por ceremonia ni llamar microdato directo a lo que es lectura de un agregado.

Puedes ampliar a historia ENCIG anterior registrada si la comparabilidad se sostiene y aporta identificación. Congela qué olas usar antes del ajuste. No incorpores ENVIPE al ajuste de ENCIG: instrumentos, unidades y procesos distintos.

## 5. Modelo que debes congelar y ejecutar

Base objetivo:

`C2_2025(c) = expit(logit p_2025(a) + logit p_2025(b) - logit p_2025(nacional))`.

Señal histórica:

`I_t(c) = logit p_t(a,b) - [logit p_t(a) + logit p_t(b) - logit p_t(nacional)]`.

Construye `I_estimado_2025(c)` mediante **regularización hacia cero que distinga incertidumbre por celda y persistencia entre olas**, y emite sobre `logit C2_2025(c) + I_estimado_2025(c)`. Escoge y congela la formulación exacta dentro de esa familia antes de ajustar. No afirmes preservación exacta de marginales por el mero hecho de usar C2 como base.

Resuelve en spec: distribución/criterio de ajuste, pooling entre celdas, dependencia histórica, hiperparámetros o regla determinista que los aprende, seed/réplicas/tolerancias, fronteras y celdas vacías, funcional puntual e intervalo, no-estimabilidad y fallos. Con solo dos olas no atribuyas una dinámica compleja a información que no puede identificarla; usa menor complejidad o un prior declarado. Si usas una aproximación de independencia, identifica su alcance y cómo afecta el intervalo.

Si haces selección temporal histórica, fija antes cortes, conjunto finito de alternativas, función de pérdida y desempate; entrena hasta t−1, predice t con sus marginales y evalúa únicamente cruces históricos permitidos. Ajuste final con toda la historia pre-2025 autorizada. No seleccionar por la victoria publicada del piloto 3, no mirar edad×escolaridad 2025 y no probar hasta que guste un resultado.

Describe la diferencia real frente a C-ENCOGIDA y C7 si existen en la spec de piloto. Si el procedimiento coincide, dilo. Los hiperparámetros de tu candidato pueden aprenderse con historia y regla propia congelada; eso no cambia ni reestima el λ del candidato del piloto.

## 6. Incertidumbre e interfaz de adjudicación

Los marginales y el cruce de una ola comparten muestra. Conserva dependencia mediante bootstrap de UPM dentro de estrato, réplicas compartidas u otra construcción justificada. No generes pseudorréplicas independientes por celda y luego las llames diseño de encuesta.

Separa incertidumbre muestral de historia, del ajuste y predictiva por cambio de ola. Etiqueta el intervalo como muestral/posterior/predictivo según lo que realmente represente. Si condicionas a marginales 2025 publicados, decláralo. No abras 2025 para obtener su EE ni inventes esa incertidumbre.

Un intervalo posterior de la interacción media no es automáticamente un intervalo predictivo del cruce futuro. Un método condicional aproximado es admisible si está etiquetado honestamente; no promete cobertura fuera de su alcance.

Entrega punto, límites, nivel, tipo y RESULT estable por celda. Si entregas réplicas propias, documenta significado, dependencia y seed. No mezcles índices de réplicas del modelo con R como si compartieran diseño. El piloto importa los RESULT, aplica su criterio ya fijado y calcula ΔMAE; tú no cambias sus umbrales ni derives R. Su integración del candidato externo debe quedar explícita en el recibo si exige una decisión de método de evaluación.

## 7. Freeze y corrida

- Spec humana por cruce: `forense/prereg-caja/ASTRA-ENCIG-<CRUCE>-spec-v1_0.md` más `spec.yaml` del CALC. Incluye fuentes/hash, equivalencia de códigos, contrato completo y la frase «el primer resultado que produzca este procedimiento es el que se reporta».
- Guarda encargo/mandato y procedencia en `forense/analisis/astra-encig/`. Primera spec concreta → commit → primer push. No vender como congelada una spec con decisiones científicas por resolver.
- Congela medidor y dependencias antes del primer ajuste; no dependas de imports ajenos sin hash. Implementación propia bajo `tools/astra/encig/`; no imports del código ENVIPE en vuelo.
- Ensayo sintético mínimo con transformación, caso frontera y rechazo de ruta ficticia reservada antes de abrirla. Nunca ensayes la guardia con el archivo real de 2025.
- Consulta sintaxis actual de `tools/corrida0.py` y cumple **preflight → run → verify**, sello y estado limpio que requiera el runner. No inventes flags ni relajaciones.
- Etiquetas: `generacion: GEN2`, `cuenta_gen2: SI`, `adopta: NO`, `origen_numerico: MICRODATO`, `exposicion_historica: CIEGO-A-ENCIG2025-CRUCE-NO-ABIERTO`, solo si verdaderas. Si la entrada es un RESULT histórico, registra también esa fuente derivada y su linaje a microdato; no inventes acceso a bytes que no usaste.
- Append propio de `forense/replay-evidencia.tsv` después de verificación real. No ejecutar `registro --escribe` ni regenerar vistas.
- Fallos y revisiones se conservan. Si un cambio altera procedimiento/resultados, versiona y declara exposición; no sobrescribas sellos ni elijas entre corridas por cercanía al futuro R.

## 8. Perímetro, obstáculos y autonomía

Escritura solo en `tools/astra/encig/`, `forense/analisis/astra-encig/`, specs `ASTRA-ENCIG-*`, los dos CALC propios y append propio de replay. Scratch sintético permitido fuera del árbol; nunca microdatos al git. Herramientas/lectores históricos ajenos se leen, no se editan. Ninguna utilidad compartida con ENVIPE es requisito para cerrar.

No canon, milpa, decisiones, hallazgos, NC/FP, `.github/`, herramientas ajenas, vistas derivadas, CALC o sellos de otros. Si te encuentras escribiendo fuera de esta lista, PARA esa escritura y replantea. La regla específica de misión sustituye la cascada general de cierre.

Si falta dato histórico, primero comprueba las estadísticas selladas suficientes y el corpus configurado. Si realmente hacen falta bytes, adquisición autorizada por id/hash/licencia; nueva fuente auxiliar por rama `codex/adq-*`, sin bloquear la vía base por una mejora opcional. El campo de licencia de ENCIG 2023 conserva una referencia cuyo texto completo no fue verificado según el propio manifiesto: no declares licencia leída por ti si solo leíste ese campo. Una nueva adquisición sí requiere leer los términos.

No pares por ausencia del encargo del piloto 5 si puedes terminar el candidato; entrega incompatibilidades/preguntas de integración concretas. Para cambios de estimando, otra ola de evaluación o método fuera de esta familia, lleva opciones y recomendación a Jonás/dirección y continúa piezas independientes. Si accidentalmente ves R, declara y excluye la celda/cruce afectado; no se puede desver.

## 9. Cierre y recibo

`forense/analisis/astra-encig/nota.md`: EJECUTADO/LEÍDO por afirmación, comandos/resultados, diseño final, punto/intervalo/tipo por celda, procedencia, exposición, diagnóstico histórico, no-corrido con razones y límites de inferencia. No afirmar «vence» desde entrenamiento, ni «no existe estimador mejor» si pierde.

`recibo-claude.md`: CALC/RESULT por celda exacta, hashes de spec/código/sello/resultado, verify y replay, commits/PR, estado EN-RAMA o EN-MAIN, elegibilidad de plazo y comparación con spec piloto 5 cuando exista. Declara en una línea cualquier incertidumbre de integración de réplicas y la sustitución del plazo antiguo por antes de COMMIT-2.

Publica PR listo sin fusionarlo. Si la ventana pasó, termina y conserva la evidencia propia, informa la pérdida de admisión sin leer R y espera aquí la selección de la siguiente evaluación reservada; no cambies por tu cuenta la ola ni retoques el candidato después de conocer resultados.
