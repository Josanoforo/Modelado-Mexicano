# ASTRA6-C1-PAQUETES-1 · preparación y lanzamiento

Cero mediciones y adopciones nuevas. Celdas validadas: 219 → 219 (Δ0), derivado por cierre_acto.py sobre 6007e495. No se asientan validaciones inexistentes.

Worktree: `/home/pc0/mm-astra6-c1-paquetes-1`. Rama `codex/astra6-c1-paquetes-1`, HEAD de recuperación a1447a286e58ab49c844e0fae289f381f4ccc05e, árbol limpio. 0-bis `6c304584b96980795cfdb0ea5a42840e3036edc2` ya archivado; se retomó por instrucción explícita, sin abrir otro escritor. Main se actualizó de 34949751 a `4f125e709d3b3830078fe749c82068b3d55e6e70` y se incorporó mediante merge 6007e495. No se modificaron productores ni el catálogo. Los otros cinco encargos archivados siguen sin ejecutarse.

Entorno derivado: CAJA; corpus montado, 511 archivos examinados; variable de nube sin_variable. La red restringida rechazó fetch; el fetch escalado funcionó. PR abierto del mismo rótulo: consulta sin resultados; rama remota existente a1447a28 corresponde a este mismo trabajo retomado.

## Resultado y uso

Universo exacto: 36143 filas/estimadores, 68 CALC, 1210 RESULT, 36 referencias de adopción verificadas (desglose en adopciones-al-corte.json). La tabla conserva unidad, ola, CALC/RESULT/celda y firma; NO-EVALUADO en todas. No se confunde con decisiones del programa ni afirmaciones. No hay reutilizaciones de identidad en este corte.

9 paquetes disponibles, 3371 estimadores. 59 paquetes incompletos, 32772 estimadores, con causas concretas compartidas. El primer lote (ENDIREH 2021 comunitaria) cubre 100 estimadores y está materializado fuera del clon. Pasó `lanza.sh --prueba`: SEPARACION-EFECTIVA, solo /entrada /raw /work; sin clon, reservas ajenas ni historial. No se ejecutó una sesión validadora. El recibo de entrega mantiene por defecto la reserva NO-CIEGA hasta que el responsable conserve la prueba y la sesión nueva real.

Se entrega comando por paquete, allowlist de archivos, SHA antes de entrega y comparador separado que exige hash/commit previo y cobertura exacta. No ajusta tolerancias ni interpreta una diferencia de RNG como defecto demostrado. La coincidencia numérica no contesta validez, adopción ni predicción.

## Hallazgos que cambian la entrega

Las specs humanas mezclan método y valores: extracciones por rangos y supresiones, con procedencia fuera de entradas. Referencias a código no se sustituyeron leyendo el productor. Lo insuficiente conserva una brecha de método; no se adjudica NO-RECALCULABLE sin prueba. Documentación no identificada no se declara ausente de todas las raíces. Hash de insumo no autoriza todos sus campos: ENIF 2024 crédito sigue reservado, bloqueando entrega del ZIP completo; hace falta proyección autorizada. ENDIREH 2006 mezcla tabulados y cuestionarios; ENUT cita N observado; tampoco se entregan como completos.

Durante la preparación local, regenerar un manifiesto incluyó su propia versión previa y produjo un hash circular. Se corrigió antes de archivar o entregar a validadores, excluyendo manifiesto.json de su propia allowlist. La comprobación de puntos contra tablas se cacheó por RESULT para evitar parsear la tabla completa por cada registro. Ningún sello productor se tocó.

INTERPRETACIÓN-DECLARADA: cierre_acto.py deriva raíz ASTRA6-C1-PAQUETES-1, pero la gramática vigente de ids requiere prefijo GEN2; el prefijo técnico se añadió por derivación a la raíz, sin cambiar el rótulo del encargo. Id de cierre `ADR-260926-GEN2-ASTRA6-C1-PAQUETES-1-6c30-01`.

## Comprobación

Pruebas dirigidas: seis casos negativos pasaron (filtración, productor, archivo extra, alteración de hash y revelación sin congelación). `--verifica` pasó para universo, hashes, RESULT/punto y referencias. Primer lanzamiento probado sin recálculo. El comparador no se ejecutó contra reconstrucciones reales ni se simularon COINCIDE.

El censo global de guardias se interrumpió al comprobar que su implementación ejecuta todos los huérfanos, a diferencia de la descripción estática; se reutilizó su clasifica únicamente para derivar la fila del test propio (CORRE-EN-CI), conservando las filas ajenas. No se reparó deuda de otros carriles. Suite rápida y guard de remoto se reportan en el cierre del PR con su salida real.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| P2 · Partición completa y entradas separadas | DIFERIDO-A:SIN-ASIGNAR: 59 paquetes con faltantes documentales, método mixto, tolerancia ausente o proyección autorizada pendiente; lista exacta en lotes.json y faltantes.json. | 32772 estimadores sin paquete completo; no cambia validación ni adopción. | SIN-ASIGNAR; continuación de preparación descrita en lanzamientos.md |
| Perímetro de cierre · recibo técnico de Claude | DIFERIDO-A:SIN-ASIGNAR: el recibo requiere revisión real por el circuito de mesa. | PR sin recibo; no se declara aceptado ni se fusiona. | SIN-ASIGNAR; GEN2-RECIBO-ASTRA-PRODUCTO-N por asignar en mesa |

## CONSUMIDO

Preparación entregada por esta rama y PR propio; el encargo llevará el número real después de crear el PR. La validación total y el recibo siguen pendientes.
