# Encargo Codex CLI · ASTRA-ENVIPE-EMISION-PROSPECTIVA-1

**Misión:** construir y sellar C-ASTRA para el piloto 4; no evaluar el piloto. **Base de redacción:** `43394b060538fdd7c472d7673f27b7b39229ac29`; rederiva contra origin/main vivo. **Rama:** conserva `codex/astra-interaccion-dinamica-1`, originalmente sobre `c9b67bf8`. **Entorno:** Codex CLI con acceso a historia permitida en caja; nunca abrir payload de evaluación. **Una sesión escritora.** **Modo:** diseño abierto hasta congelar procedimiento; después no ajustar por el resultado. **Contador:** `generacion: GEN2`, `cuenta_gen2: SI`, `adopta: NO`, solo corridas realmente selladas. **Publicación:** primer push después de primera spec; PR propio autorizado, merge de mesa.

## 1. Producto y objetivo verificable

Entrega hasta cuatro CALC de emisiones, uno por cruce elegible de `tramite.evasion_norma`, ENVIPE 2025:

| Cruce canónico | Sufijo propio de CALC |
|---|---|
| edad × sexo | `ENVIPE-EDADXSEXO-0001` |
| escolaridad_proxy × sexo | `ENVIPE-ESCOLARIDADPROXYXSEXO-0001` |
| dominio_urbano_rural × sexo | `ENVIPE-DOMINIOXSEXO-0001` |
| edad × escolaridad_proxy | `ENVIPE-EDADXESCOLARIDADPROXY-0001` |

Prefijo de los cuatro: `CALC-ASTRA-`. Deriva la lista de categorías/celdas exactas; ≈38 es orientación del brief, no conteo a imponer. Cada celda estimable lleva punto, intervalo y tipo de incertidumbre. Una exclusión o no-estimabilidad se conserva con causa; nunca desaparece para mejorar la puntuación.

Hecho de esta sesión = specs y código congelados, emisiones selladas, `verify` satisfactorio por CALC, evidencia de replay propia, nota y recibo de consumo, PR publicable/revisable. **Entrada al piloto** exige además que todo ello esté en main antes de su COMMIT-2 y que el piloto acepte las mismas celdas. Son estados distintos: reporta ambos.

No entregues solo un diseño, un inventario o un plan. Persiste hasta emitir y verificar las celdas alcanzables sin romper reservas. Un cruce bloqueado no frena automáticamente los otros.

## 2. Mandato y adjuntos

Lee `00-ARRANQUE-Y-COORDINACION-ASTRA-1.md` y la misión adjunta cuyo SHA es `949a0f1a9c0054a9a82a802f8a4ce4eadab6d9d9838ecd0f765f69dde7d905bc`. La adenda 4 histórica tiene SHA `441452833ef9570d65ce1d9f9457f6ceebfc1b8bddf4232b1030fd7a6edcb285`.

La instrucción posterior de Jonás fija **CALC en main antes de COMMIT-2**, sustituyendo para esta tanda el plazo «al abrir/en COMMIT-1» de la adenda antigua. Cita esa diferencia en el recibo. No edites spec de piloto ni declares unilateralmente que puede admitir cambios sobre su congelación.

La misión específica excluye la cascada de gobierno del `/acto` ordinario: entrega propia, recibo Claude. No abras NC/FP ni ADR, no uses cierre_acto para escribir en gobierno.

## 3. Arranque útil y protección de la evaluación

1. Localiza el clon y la rama existente en la máquina de Jonás; reporta ruta absoluta, rama, HEAD y status. La ruta cloud del transfer no es una ruta portable de su CLI. No clones de nuevo si el repositorio ya existe. Si la rama no está disponible, busca su referencia/commit y declara lo encontrado; no inventes continuidad ni borres trabajo ajeno.
2. `git fetch origin`. Integra main sin reescribir commits sellados. Revisa AGENTS y solo las instrucciones necesarias. Busca por archivos/objeto si otra rama/PR ya escribe estos mismos CALC, no solo por nombre de rama.
3. Antes de datos, lee `data/corrida0/decisiones.tsv` por CSV y las entradas `reserva:*`; conserva alcance y excepciones. No deduzcas liberación general porque un duelo consumió una parte. **No abrir ENVIPE 2026 ni usarla como historia**, aunque el duelo ya fusionó. Tampoco otras olas reservadas.
4. Lee solo metadatos de `marcador-segmento.tsv`, specs y cronología necesaria para identificar cruces elegibles. Trata `edad×dominio` ENVIPE 2025, NC-0328, como visto y excluido incluso para calibrar; no uses escolaridad×dominio 2025 ni resultados de otros pilotos para elegir tu modelo.
5. `envipe2025_csv` queda fuera de la lista de entradas ejecutables. No abrir su zip, ni listar miembros, ni muestrear filas, ni ejecutar exploración que lo alcance. La única excepción de evaluación son los marginales públicos ya sellados en `milpa/tramite-ola5-propuesta-v0.yaml`, en lectura y con extracción acotada. No abrir globalmente archivos con R para buscar nombres.
6. Registra exposición previa de la sesión a resultados y cruces. La ausencia de un `git log -S` no demuestra ausencia de lecturas: complementa historial de archivos con declaración explícita y trazas de ejecución. Cualquier exposición al cruce objetivo se declara y ese cruce deja de ser prospectivo.

Si la lista reservada final no basta en main, usa la verificación por objeto autorizada por el piloto, sin leer R. Puedes avanzar código y ensayos sintéticos mientras se confirma la lista; no inventes una lista final para ganar tiempo.

## 4. Contrato sustantivo: no reinterpretar el desenlace

Fuente principal: `forense/prereg-caja/ENVIPE-EVASION-NORMA-spec-v1_0.md`, encargo del piloto 4 y cuestionarios/FD de las olas históricas.

**LEÍDO al redactar:** unidad DELITO; universo de delitos con `BP1_20 ∈ {1,2}`; desenlace `BP1_20=2` y `BP1_23 ∈ {04,05,06,08}`; ponderador `FAC_DEL`. Es una probabilidad conjunta en ese universo, **no** una proporción condicionada a no denunciar. Los ejes escolares pueden requerir enlace de tablas: verifica cardinalidad y categorías por el descriptor; no traslades sin comprobar la escolaridad de otra encuesta.

Por cada ola histórica, documenta texto del reactivo, códigos, filtros, ceros/faltantes, ponderador, estrato, UPM, edad válida y uniones necesarias. No promedies delitos con personas ni imputes categorías sin regla congelada. La agregación a ejes debe coincidir con la rejilla y universo de los marginales autorizados de evaluación.

Historia mínima candidata, **LEÍDA en manifiesto; existencia local NO VERIFICADA aquí**:

| id | SHA-256 |
|---|---|
| `envipe2023_csv` | `0dcc00a7fc37b79806f1bf1b85b12cd090b5ecc8e76983a3a1a861f2ef3fb404` |
| `envipe2024_csv` | `90776b2fab6e3666dad1cb5f5f3eb7d6a7699dbfefd4f8f04f07fb01e61a6fb2` |

Relee manifiesto y verifica bytes por hash. Puedes incorporar historia anterior registrada y no reservada si es comparable y aporta identificación; fija antes de ajustar qué olas entran y por qué. No uses olas posteriores a 2024 para predecir 2025. Una rotura de comparabilidad se resuelve acotando historia, no cambiando el estimando.

Puedes reutilizar lectores/estimadores históricos verificados del repo, en lectura, por ejemplo `tools/celda_d/marginales_reproduccion.py`; inspecciona que no abran evaluación al importarse. Congela hashes de dependencias o incorpora la lógica mínima en tu espacio propio: un import mutable no es un procedimiento congelado.

## 5. Modelo que debes convertir en procedimiento ejecutable

Punto de partida común:

`C2_2025(c) = expit(logit p_2025(a) + logit p_2025(b) - logit p_2025(nacional))`.

En historia permitida deriva, sobre universos coherentes:

`I_t(c) = logit p_t(a,b) - [logit p_t(a) + logit p_t(b) - logit p_t(nacional)]`.

Construye una estimación de `I_2025(c)` con **encogimiento hacia cero dependiente del ruido de cada celda y evidencia de persistencia entre olas**. La emisión es `expit(logit C2_2025(c) + I_estimado_2025(c))`, o el funcional puntual de su distribución que dejes congelado. No presupongas que sumar una interacción preserva exactamente todos los marginales; declara esa propiedad solo si tu método la impone y comprueba.

Antes de la primera corrida histórica de ajuste, deja resueltos en spec: modelo/likelihood o criterio de ajuste; pooling y dependencia entre celdas/olas; hiperparámetros o algoritmo determinista que los fija; tratamiento de fronteras 0/1 y celdas vacías; regla de complejidad si solo hay dos olas; funcional puntual; seed, réplicas, tolerancias y fallos. No estimes una dinámica rica con dos observaciones temporales sin justificar su identificación o prior. No pruebes variantes contra 2025.

Una validación temporal histórica, si la usas, entrena solo hasta t−1, predice t con sus marginales permitidos y puntúa su cruce histórico; fija cortes, candidatos internos, métrica y desempate antes. Elige por esa regla y ajusta finalmente sobre la historia autorizada. El primer resultado de ese procedimiento completo es el reportado, aunque no mejore al piso. No usar el piloto 2 ni ENVIPE 2026 para elegir regularización.

Respecto a la C-ENCOGIDA existente, declara qué componente científico aporta C-ASTRA o si coincide. **La prohibición de reestimar λ del piloto rige su candidato; no prohíbe ajustar hiperparámetros propios de C-ASTRA con historia permitida y regla congelada.** No toques su λ ni su spec.

## 6. Incertidumbre y evaluación

La misma muestra genera marginales y cruces históricos: conserva su dependencia mediante réplicas compartidas de UPM/estratos u otro método justificado. No trates celdas superpuestas como muestras independientes sin declararlo y acotar las consecuencias.

El intervalo debe corresponder a la cantidad predicha: si es posterior/predictivo, dilo; no lo presentes como IC de muestreo de R. Explicita qué incertidumbre incorpora (historia, hiperparámetros, evolución temporal) y cuál condiciona (por ejemplo marginales 2025 tomados como puntos publicados). No inventes réplicas del microdato de evaluación para completar incertidumbre.

Deja la interfaz de RESULT e intervalo inequívoca. Si el piloto requiere réplicas externas, entrega las de tu modelo con su significado y seed; no emparejes arbitrariamente réplicas históricas/modelísticas con las de R como si fueran el mismo diseño. Claude/piloto debe declarar cómo se incorpora un candidato externo al criterio ya congelado. No cambies ese criterio para que tu intervalo encaje.

No derives R. No calcules victoria ni IC de ΔMAE usando información objetivo. La tabla final contra R la copia el piloto cuando adjudique.

## 7. Freeze → ejecución → verificación

- Spec humana por cruce: `forense/prereg-caja/ASTRA-ENVIPE-<CRUCE>-spec-v1_0.md`, más `spec.yaml` en cada CALC. Deben bastar para reproducir el procedimiento. Incluye exactamente: «el primer resultado que produzca este procedimiento es el que se reporta».
- Archiva en `forense/analisis/astra-envipe/` el encargo/mandato y las referencias/hashes de insumos. Primera spec útil → commit → primer push; no publiques una plantilla con decisiones científicas pendientes como si fuera freeze.
- Congela el código ejecutable y sus dependencias antes del ajuste, sin placeholders. Prueba primero con datos sintéticos la transformación, el aislamiento de rutas de evaluación y una falla conocida. Ensaya guardia de reserva usando una ruta ficticia, no tocando el payload real.
- Verifica la sintaxis vigente de `tools/corrida0.py` con `--help`/lectura mínima y ejecuta **preflight → run → verify** por CALC. No inventes flags. Respeta las condiciones reales de sello y repositorio limpio del runner.
- Labels: `generacion: GEN2`, `cuenta_gen2: SI`, `adopta: NO`, `origen_numerico: MICRODATO`, `exposicion_historica: CIEGO-A-ENVIPE2025-CRUCE-NO-ABIERTO`, únicamente si esa exposición es verdadera. Si consumes agregados históricos sellados, declara además su linaje; no hagas pasar una lectura de RESULT por reapertura directa de microdatos.
- Asienta replay propio como append con evidencia real; no fabriques una verificación ni borres asientos ajenos. No `registro --escribe`.
- Si falla código, conserva la traza. Un arreglo técnico que cambie el procedimiento o las emisiones exige nueva versión y declarar la exposición; no reescribir un sello ni seleccionar la corrida más favorable.

## 8. Perímetro y obstáculos

Escritura solo en `tools/astra/envipe/`, `forense/analisis/astra-envipe/`, specs `ASTRA-ENVIPE-*`, los cuatro CALC propios (incluidos archivos que el runner produce) y append propio de `forense/replay-evidencia.tsv`. Scratch sintético fuera del árbol permitido. Payload histórico faltante: localiza el corpus configurado; no dupliques zips en git. Si requiere traer bytes, hazlo por el carril de adquisición autorizado y verifica id/hash/licencia antes de usarlos. Un auxiliar nuevo exige `codex/adq-*`; no lo metas de paso en este PR.

No escribas `milpa/`, canon, decisiones, NC, FP, hallazgos, herramientas ajenas, `.github/`, vistas derivadas o sellos ajenos. No cambies infraestructura para conseguir una corrida verde. Si te encuentras escribiendo fuera de esta lista, PARA esa escritura y replantea dentro del perímetro.

Obstáculos reversibles: resolver rutas, entorno y dependencias; seguir con cruces independientes. Detener la pieza afectada si hay exposición de evaluación, input incoherente que cambia estimando, falta de dato imprescindible tras búsqueda concreta o violación del sello. Declarar lo no corrido en la nota propia; no encubrirlo con resultados sintéticos. Si necesitas decisión científica, presenta opciones y recomendación y continúa las piezas no afectadas.

## 9. Cierre concreto

`forense/analisis/astra-envipe/nota-envipe.md`: comandos con salida relevante y SHA; EJECUTADO/LEÍDO; estimador exacto; punto/intervalo/tipo por celda; exclusiones; diagnóstico solo histórico; qué no corriste y por qué; límites de afirmación. Añade inventario de entradas realmente abiertas y excepción de marginales autorizados, sin datos individuales.

`recibo-claude-envipe.md`: por CALC y RESULT, celda exacta, hashes de spec/código/sello/resultado, verificación y replay, commits de freeze/emisión, PR y estado remoto. Adjunta la diferencia de plazo de admisión. No declares EN-MAIN si solo está en rama. No declares PROSPECTIVA adjudicada antes de que el piloto verifique la secuencia.

Deja el PR listo; no lo fusiones. Si COMMIT-2 ya ocurrió, informa «VENTANA PILOTO 4 PERDIDA» con evidencia de metadatos y entrega igualmente el trabajo histórico válido; no leas R, no traslades silenciosamente el modelo a 2026 y no te quedes esperando sin producto. La selección de la siguiente evaluación vuelve a Jonás/dirección.
