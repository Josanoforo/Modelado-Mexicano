# Cierre local · Autoridad

**EJECUTADO.** Se escribió el homónimo v2 completo y la tabla producida desde decisiones editoriales explícitas. Corte de lectura: `7748208614570a50a97c1ba830aee72a972185f9`; encargo archivado por sesión responsable en commit `3a1f0be1`. Original verificado: blob `ccc69a348f34fd6457b81797ee9e7fe7f36d6378`. Este subexpediente no modifica v1, mapa, catálogo, motor, CALC, reservas ni contadores.

| Objeto | SHA-256 / resultado |
|---|---|
| Homónimo v2 | `a48943e64621e1c8d3414bca529d159c6e576f68eeb7bed9b56a960668a09557` |
| Tabla `afirmaciones.tsv` | `9726df3aaf87310ec83cee00dbd1f487302980e22a8adf2191859d122557e58b` |
| Productor `produce_tabla.py` | `49dcd57e0bc0561711fa72914516a13845124bed3ab815511a2ec636af06e0e6` |

**Cobertura ejecutada.** Las 30 afirmaciones del mapa con identidad exacta del report están presentes. Se añadieron 29 unidades materiales, incluidas separaciones de cláusulas compuestas: 59 registros en total; CONFIRMA 1, MATIZA 16, ROMPE 1, SIN-CIFRA 41. Los dictámenes de SIN-CIFRA indican falta de RESULT compatible, instrumento inadecuado, falta de adquisición o identificación de mecanismo, según la fila. Ausencia de dato no se trató como refutación.

**Fuente principal y cambio de tesis.** La nota primaria OCDE24 sobre adultos urbanos de México muestra diferenciación entre instituciones; se retira «confianza solo personal». La misma nota confirma el 27% externo para percepción de empleados públicos que rechazarían soborno a cambio de acelerar un servicio; no se confunde con el 27% de políticos que rechazarían un favor por empleo privado. GLOBE distingue práctica, valor deseado e ideal gerencial; se retira su uso para afirmar simulación u obediencia nacional. ENCUCI permite contrastar preferencias políticas, pero sus marginales no prueban simultaneidad de respuestas ni conducta. El valor PDI es índice histórico importado, no atributo individual. Se preservó FP-293: correlación de perfiles, sin multiplicador causal.

### Revisión manual de los siete ROMPE iniciales

| Unidad | Dictamen final | Razón precisa |
|---|---|---|
| AUTOR-009, jefe formal «vacío» | SIN-CIFRA | Confianza en gobierno no compara influencia de jefe y compadre en una empresa. |
| AUTOR-013, confianza solo interpersonal | ROMPE | La exclusividad institucional sí contradice confianza positiva declarada en varias instituciones de la misma encuesta OCDE. Es la única cláusula rota. |
| AUTOR-020, regiones tan distintas como países | SIN-CIFRA | No hay métrica común ni comparación, tampoco evidencia contraria a la magnitud. |
| AUTOR-023, percepción de rechazo de soborno | CONFIRMA | OCDE24 figura 4 sí publica el escenario exacto; figura 5 publica otro 27% para favor político. |
| EXTRA-011, mayoría laboral joven | SIN-CIFRA | Sin fuente y denominador verificables; no se demostró porcentaje opuesto. |
| EXTRA-012, tres culturas regionales | SIN-CIFRA | Tipología sin instrumento, no refutación empírica de cada diferencia. |
| EXTRA-022, utilidad de Ramos | SIN-CIFRA | Utilidad predictiva no validada; la crítica conceptual no mide su falsedad. |

**LEÍDO.** Original completo en bloques; filas correspondientes de `canon/mapa-dominios-v1_1.tsv`; páginas primarias INEGI ENCUCI, OCDE24/OCDE25, GLOBE, The Culture Factor y portal WVS. Fuente, método, población, ola y localizador se consignan al pie del report. OCDE25 reutiliza la observación 2023; no se leyó la publicación de la ola más reciente para actualizar cifras. No se usó snippet como prueba de un resultado no leído. La visualización web GLOBE no expone en texto sus decimales mexicanos; se retiran como dato contrastado. La página WVS consultada es un portal documental, no una lectura del cuestionario o microdato suficiente para certificar el porcentaje de v1.

**EJECUTADO · gate.** `python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/autoridad/produce_tabla.py` y `python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/autoridad/verifica.py`: `VERDE: mapa 30/30, tabla 59, fuentes 6, reserva respetada, prosa y tabla presentes`. `git diff --check`: salida vacía. Compilación de los dos scripts Python: sin error. El verificador comprueba identidades, decisiones, referencias primarias nombradas y coherencia básica prosa–tabla; la adjudicación semántica fue manual.

**PROPUESTO-POR-EJECUTOR.** Tres reglas de interpretación y prueba local aparecen en el report con consumidor, condición y falsador. No están adoptadas ni poseen parámetro numérico. **NO-VERIFICADO.** Porcentajes históricos de ENCUCI/WVS, decimales GLOBE, movilidad, empresa familiar y magnitudes de subordinación laboral del v1 carecen de RESULT o fuente/denominador compatible en este corte. Un sucesor con instrumento abierto y autorización puede recalcularlos, fijando diseño de incertidumbre y reserva antes de abrir la ola. C1 ciego pendiente no bloquea esta conclusión editorial.
