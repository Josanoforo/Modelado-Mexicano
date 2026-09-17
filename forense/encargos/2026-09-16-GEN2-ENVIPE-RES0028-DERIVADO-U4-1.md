# GEN2-ENVIPE-RES0028-DERIVADO-U4-1

Encargo propuesto para Jonás · 16/sep/2026 · Codex CLI o Claude Cloud, sin corpus.
Repositorio: Josanoforo/Modelado-Mexicano. Base revisada: 85a2e77a; PR de referencia: #829, 15d6683f. Ejecutar desde origin/main vigente.

## Producto y motivo

Entregar el complemento de la partición C2 **a nivel persona U4**, con intervalo transformado y procedencia verificable, como candidato para RES-0028. El PR #829 detectó correctamente que la oferta actual a nivel delito U1 no puede compararse con el consumidor a nivel persona. No recalcular ENVIPE ni adoptar el resultado.

El padre ya está publicado: `data/corrida0/CALC-ENVIPE-0001/resultados.json`, claves `RESULT-ENVIPE-DEN-P-C2-U4`, `RESULT-ENVIPE-DEN-IC-LO-C2-U4` y `RESULT-ENVIPE-DEN-IC-HI-C2-U4`. La spec del mismo CALC identifica FAC_ELE y la agregación por persona. Verificarlo en la revisión ejecutada; los nombres no sustituyen el contrato.

La nota `forense/notas/2026-09-15-GEN2-E11-RES0028-PARTICION-cierre.md` usa un padre U4 y propone un nombre U1. Conserva esa nota histórica, pero explica la discrepancia en el nuevo producto. No copies su nombre de RESULT ni modifiques el CALC sellado para añadirle una salida.

## Trabajo

1. Leer AGENTS.md, este encargo, la fila viva RES-0028, su consumidor en milpa y spec/resultados/sello del padre. Buscar si el derivado exacto ya se entregó. Si existe y satisface el contrato, verificar y devolver su referencia; no duplicarlo.
2. Escribir y comprometer una spec sucesora breve **antes de ejecutar el derivado**. Es una transformación de resultados publicados, sin pretensión de cegamiento o pre-registro de datos nuevos. Fijar unidad persona, población U4, partición C2, escala [0,1], padre y tratamiento de no-estimable.
3. Crear un CALC derivado independiente, sugerido `CALC-ENVIPE-RES0028-U4-DERIVADO-0001`, previa comprobación de unicidad. Reutilizar el contrato GEN2 existente para derivaciones; no inventar otra infraestructura. Su entrada es el resultado sellado del padre, no microdato. Declarar expresamente que no agrega información muestral independiente.
4. Implementar `q=1-p` y `IC(q)=[1-IC_hi(p),1-IC_lo(p)]`. Heredar método y limitaciones del IC del padre. Rechazar límites invertidos/fuera de escala, padre no-estimable y referencias de U1. No transformar un NS/NR en cero.
5. Explicar qué significa q: complemento de la clasificación de persona que utiliza el padre, incluyendo su regla de agregación sobre delitos elegibles. No llamarlo automáticamente «confianza», ni tasa por delito, ni probabilidad de denunciar. Determinar documentalmente si coincide con la rama residual exacta de RES-0028. Si no coincide, publicar el derivado correcto y declarar SIN-RELEVO con la discrepancia concreta.
6. Generar resultados, recibo y sello con las herramientas existentes y verificar exclusivamente esta cadena. Comparar con el valor legacy sólo si escala, codificación y universo coinciden. Usar el delta canónico si aplica; no reemplazar la incompatibilidad histórica del PR #829. Una tabla nueva debe separar el candidato antiguo U1 del nuevo U4.
7. Entregar la correspondencia propuesta `RES-0028 → CALC::RESULT`, p y q con su denominador común, delta admisible, limitaciones y decisión pendiente. La oferta no cambia ningún consumidor ni snapshot del emisor.

## Perímetro y concurrencia

Worktree y rama propios. Permitidos: nuevo CALC, medidor pequeño dentro de él, una prueba focal, encargo verbatim y nota propia. Sin cambios al padre, a herramientas generales, a resultados/usos/decisiones globales ni a los archivos del PR #829. Si #829 sigue vivo, no esperar su merge para derivar desde el padre en main; citar su diagnóstico como propuesta revisada.

Excepción temporal de cascada al lanzar: diferir registros compartidos — decisiones, firmas, no-corrido, hallazgos, gobernanza, estado, rótulos, manifiesto, tableros y contadores. No asignar ADR/NC/FP ni congelar baseline. Registrar en la nota las propagaciones estrictamente necesarias para integración serial después de CAREO/TRÁMITE-4. El contador GEN2 queda pendiente de mesa; no declarar una nueva medición independiente.

Opus conserva CAREO, TRÁMITE-4, piloto celda-D, crosswalk y edad. No abrir ENIF 2024, el cruce localidad × edad, capturas del piloto o reservas F6. Cero descargas, llamadas experimentales o envíos a terceros. No ejecutar cron, deriva, despacho o registro global con escritura.

## Verificación y cierre

Pruebas suficientes: complemento y suma uno; inversión correcta de extremos; rechazo de padre con unidad errónea/no-estimable. Añadir comprobación de que la derivación no modifica los bytes del CALC padre. Usar fixtures sintéticos donde se prueba lógica; verificar el resultado real contra las claves publicadas, sin rerun de microdato.

Antes del push final, sincronizar main sin descartar trabajo ajeno y sin force. Revalidar sólo premisas afectadas; no repetir el cálculo por cambios documentales. Revisar diff y CI. Si aparecen fallos nuevos, resolver dentro del perímetro; no ocultarlos con exenciones o baseline. Informar cualquier gate externo preciso y entregar el producto completo.

Retorno: PR, SHA base/final, referencia exacta del derivado, valor e IC, compatibilidad de RES-0028, comandos/pruebas reales, estado CI y decisión pendiente. No basta una nueva ficha de diagnóstico: debe haber derivado reproducible o evidencia concreta de que ya existe.

## Prompt de lanzamiento

> Ejecuta íntegramente este encargo desde origin/main en worktree propio. Autorizo derivar el complemento U4 desde el resultado ENVIPE publicado, crear el CALC sucesor y sus pruebas, commits, push y PR; fusión conmigo. Autorizo diferir la cascada compartida. No reabras microdatos, no modifiques el padre sellado, no adoptes ni edites consumidores. Entrega el derivado y determina si satisface RES-0028, conservando la distinción persona/delito. Si ya existe, verifica y devuelve la referencia en lugar de duplicarlo.
