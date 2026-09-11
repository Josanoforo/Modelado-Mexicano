# Lanzamiento · encargos posteriores a los merges #687–#693

Fecha de revisión: 11/sep/2026 UTC. Base confirmada en GitHub y fetch local: `e76f3a1d476049d0c7adcba87535e60f507c8d91` (merge #693). Los siete merges ocurrieron la noche del 10/sep en México. Preparación de encargos, **sin cambios al repo remoto ni ejecuciones nuevas en CAJA**.

## Qué cambió y qué permite

| Orden real | PR / ADR final en main | Resultado integrado | Lo que sigue abierto |
|---|---|---|---|
| 1 | [#687](https://github.com/Josanoforo/Modelado-Mexicano/pull/687) / ADR-455 | 224 capturas; U3=12/14; SIN-GANADOR-UNICO | Dos celdas con abstención válida L_CORPUS, NC-0152; publicación de TRIADA |
| 2 | [#688](https://github.com/Josanoforo/Modelado-Mexicano/pull/688) / ADR-456 | S6 v1.4, S13 v1.1, S12 v1.2 y CALC-0001-v2 | Reflejar ejecución en FP-361/363 y publicar vistas; no adopción de S12 |
| 3 | [#690](https://github.com/Josanoforo/Modelado-Mexicano/pull/690) / ADR-457 | Pruebas aisladas y columna fuente de replay implementada | Publicación bloqueada por 32 transiciones históricas, NC-0104 |
| 4 | [#689](https://github.com/Josanoforo/Modelado-Mexicano/pull/689) / ADR-458 | Eventos, dominios y usos del motor corregidos | NC-0107, fuente general NC-0153, firma RES-0028 NC-0085 |
| 5 | [#691](https://github.com/Josanoforo/Modelado-Mexicano/pull/691) / ADR-459 | ENIF A/A y población no trabajadora adoptadas; nuevo CALC | Vistas NC-0154; categoría de ahorro colapsada NC-0126 |
| 6 | [#692](https://github.com/Josanoforo/Modelado-Mexicano/pull/692) / ADR-460 | Serie ENVIPE 15/15 años-hecho 2010–2024 | Validación independiente NC-0155; serie sin adopción nueva |
| 7 | [#693](https://github.com/Josanoforo/Modelado-Mexicano/pull/693) / ADR-461 | Tres documentos, ruta mexicana de tandas, dictamen DIN | Acciones personales NC-0151 y decisión FP-371 |

**La integración de numeración quedó bien:** 461 ADR, máximo 461, sin duplicados ni huecos. Los cuerpos de algunos PR conservan candidatos antiguos; los encargos usan los IDs definitivos de main. No renumerar la historia para igualar esas descripciones.

**F5 sí terminó el encargo de captura.** Las 16 respuestas de DIN-M-01/TRA-M-07 son abstenciones válidas, no trabajo sin ejecutar. No se relanza la ronda completa para perseguir un ganador. Las tres comparaciones son inconclusas, no una prueba de equivalencia. F6 no se habilita automáticamente.

## Revisión dirigida y límites

Se consultaron estado/merge SHA y conversaciones de #687–#693 (sin comentarios/reviews devueltos por el conector), productos y reservas en main. Se ejecutaron:

- `tests/test_corrida0.py`: 84/84.
- `tests/test_cierre_acto.py`: 8/8.
- `tests/test_motor_usos_complementos.py`: 11/11.
- `tests/test_emite_m_calibracion.py`: 16/16.
- F5/runner L y ENIF población: 13 pruebas unitarias adicionales, sin errores.

Las cuatro suites principales suman 119; con F5/ENIF, 132 comprobaciones distintas pasaron. Los cinco TSV de demanda/vistas conservaron sus hashes. S12 no se pudo ejecutar aquí por dependencia local ausente `pyreadstat`; su verificación y tabulación independiente constan en #688, no se presentan como repetidas en esta revisión. No se abrieron microdatos, no se probó Windows ni se repitió baseline completo. Los PR reportan baseline verde frente a los tres FAIL históricos; eso no equivale a una ejecución nueva de esa suite aquí.

El seco de publicación reprodujo el bloqueo: 64 campos de 32 corridas cambiarían sin evidencia suficiente o por un asiento contradictorio. Vistas publicadas/derivadas: corridas **147/150**, resultados **3,209/3,335**, usos **205/207**. Son filas de vistas, no números de mediciones independientes. Faltan S12 `CALC-0001-v2`, ENIF `CALC-ENIF-0002` y tríada `CALC-TRIADA-0002`; las ocho nuevas olas ENVIPE ya están publicadas. Ninguna de las tres vistas lleva todavía `fuente_replay`.

Otro residual concreto: la cartera de #693 espera que se defina la demanda general de corrupción, pero #689 ya la definió en NC-0153. El encargo 11 continúa desde ahí. La conciliación FP-361/363 es ligera y se incluye en publicación; no se crea un proyecto administrativo aparte.

## Seis encargos para ejecutar

| Archivo | Producto | Destino | Dependencia real |
|---|---|---|---|
| [09 · Publicación y cierres](09-GEN2-PUBLICACION-POST693-Y-CIERRES.md) | Tres vistas completas, replay preservado y firmas ejecutadas reflejadas | CLI/CAJA; preparación repo-only posible | Productos ya fusionados |
| [10 · ENVIPE validación y lectura](10-GEN2-ENVIPE-VALIDACION-Y-LECTURA.md) | Ocho puntos contrastados independientemente y lectura temporal | CLI/CAJA | Corpus ENVIPE; no depende de una nueva adquisición |
| [11 · Corrupción: unidad y fuente](11-GEN2-CORRUPCION-UNIDAD-Y-FUENTE-GENERAL.md) | Tratamiento de canales ambiguos y demanda general en adquisición | CLI/CAJA; búsqueda/código preparables en Cloud | Corpus ENCIG; definición NC-0153 ya existe |
| [12 · Tandas: primera medición](12-GEN2-TANDAS-MEDICION-ACADEMICA.md) | Participación/atributos medidos con fuentes mexicanas | CLI/CAJA; documentos preparables en Cloud | Fuentes de #693 y corpus ENNViH |
| [13 · Aprendizajes de F5](13-GEN2-F5-APRENDIZAJES-Y-SUCESOR.md) | Errores por celda, prioridades de mejora y propuesta sucesora | Cloud o CLI | Sólo resultados ya versionados |
| [07R · SONDA/cron](07R-GEN2-SONDA-CRON-PRODUCCION-POST693.md) | Configuración única y operación atribuible | CLI Windows/WSL | Estado instalado y disponibilidad del ejecutor productivo |

Todos son autocontenidos, con fases, perímetro, pruebas, aceptación y cierre. 07R continúa el lote 07; no se lanza una segunda copia si ya está activo. Los otros cinco son sucesores concretos, no reejecuciones de los lotes 01–06/08.

## Qué puede correr a la vez y orden de merge

**Puedes iniciar ahora los seis en tareas/worktrees separados**, comprobando duplicados y capacidad real. Recomendación práctica: 09 en CLI, 13 en Cloud y 07R en otra sesión CLI; 10, 11 y 12 en worktrees de CAJA separados según RAM/CPU. Compartir el corpus en lectura es válido; no compartir el directorio de salidas ni escribir simultáneamente el manifiesto/censo compartido. Esto no autoriza varias sesiones del `/despacha` automático ni relaja su candado.

**No hay una dependencia científica 09→todos.** 10/11/12 pueden medir y 13 puede analizar sin esperar que las vistas se publiquen. Los recibos nuevos se entregan a 09 mientras esté abierto, o se publican por lote propio después de su merge. Evitar que varias ramas regeneren las mismas vistas globales a la vez.

Orden de integración recomendado: **09 primero**; 07R y 13 pueden fusionarse en cuanto estén listos; 10, 11 y 12 después conforme terminen, incorporando main uno por uno. No retener un producto útil por esperar una tarea independiente. Si 07R usa NC-0153 como prueba de handoff, sólo esa prueba espera el producto de 11; puede usar otra demanda elegible para comprobar el cron antes.

Antes de cada merge: main actualizado en la rama, revisión del delta sustantivo, renumeración de **ese acto** si colisiona, filas compartidas conciliadas por identidad, cascada con `cierre_acto.py`, pruebas pertinentes y comprobación del HEAD remoto según `/acto`. Una revisión anterior al último merge de main no acredita los conflictos resueltos después. El merge lo haces tú.

## Dos decisiones que aún requieren tu elección

Ninguna bloquea el arranque de los seis encargos. Recomendaciones de ChatGPT, **no firmas asentadas**:

| Pendiente | Decisión en lenguaje de RH | Recomendación | Qué habilita |
|---|---|---|---|
| **NC-0085 / RES-0028** | ¿Usamos “el resto de este grupo evaluado” o diseñamos otro indicador que cubra también respuestas excluidas? | Adoptar sólo el complemento del grupo exacto U1/U4, etiquetado y dependiente del padre; un universo mayor necesita estimando sucesor | Uso concreto de q=0.7056870125 e IC transformado, sin contarlo como medición independiente ni como código literal “Otra” |
| **FP-371 / DIN** | Tenemos la tasa, pero el margen de error usa una agrupación que no es la oficial. ¿Permitimos certificarlo como si lo fuera? | Rechazar ese uso inferencial; conservar el punto y rotular las aproximaciones sólo como sensibilidades, mientras se obtiene vía oficial | Cierre de la decisión sobre incertidumbre, sin retirar el punto descriptivo |

No adjuntar una firma ficticia a los encargos. Si eliges alguna opción después, se prepara el cambio mínimo de adopción/estado correspondiente; no hace falta rehacer el benchmark ni el cálculo vigente. D21/F6 sigue sin firma: el análisis técnico 13 no lo sustituye.

## Acciones personales que el código no sustituye

#693 ya dejó recetas para DUA ICPSR, formulario OECD, petición Reuters con consumidor preciso, solicitud ENJUVE y sesión para SSRN exacto; DIN agrega solicitud de pesos replicados/servicio oficial. Los datos WBES, ENAFIN para N19 y ENVIPE ya están cubiertos. No se vuelve a correr un encargo genérico de “descargar todo” mientras falte identidad, firma o respuesta del titular. NC-0151 conserva esos accesos. Los documentos originales y destinatarios deben verificarse al momento de tramitar; ningún envío se realizó aquí.

## Prompt de lanzamiento

```text
Ejecuta el encargo adjunto completo en Josanoforo/Modelado-Mexicano.
Actualiza contra origin/main y comprueba ramas, worktrees y PR del mismo objeto.
Continúa todas las fases cuyas compuertas estén cumplidas; no pares en un plan.
Usa un worktree y rama propios; entrega commits, push y PR revisable.
Yo hago el merge. Conserva las decisiones ya asentadas y las firmas pendientes.
Si una fase requiere CAJA, permisos del SO o identidad personal, completa el
resto y deja la continuación exacta, sin repetir productos ya fusionados.
```

Al continuar Cloud→CLI, retomar rama/PR/SHA y fases pendientes, enlazar corpus y preservar congelamientos; no reiniciar la misma tarea desde cero. El uso de Codex no necesita Claude para cinco encargos. 07R mantiene el cliente productivo actual: su disponibilidad sólo condiciona la parte de adquisición real, no el trabajo técnico.

**Resultado de esta revisión:** el proyecto queda listo para publicar tres cálculos que hoy no se ven, verificar la serie temporal, producir mediciones nuevas de corrupción/tandas y dirigir la siguiente mejora con el resultado real de F5.
