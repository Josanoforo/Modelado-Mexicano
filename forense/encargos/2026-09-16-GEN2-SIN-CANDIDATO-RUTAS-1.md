<!-- PROCEDENCIA (fuera del bloque original): recibido como archivo local
`/mnt/c/Users/PC0/Descargas MX/ENCARGO-GEN2-SIN-CANDIDATO-RUTAS-1.md` y lanzado
por el prompt del usuario el 16/sep/2026. SHA-256 del original:
5d538aea9669b7ce02a3ac327a86d657800df76174e68a6d9b59763d3ab8a8d4. -->

# ENCARGO · GEN2-SIN-CANDIDATO-RUTAS-1

Fecha: 16 de septiembre de 2026. Repositorio: `Josanoforo/Modelado-Mexicano`.
Base consultada: `9dffd6455c67e2ca99740e79f90be59a13f250e1`; ejecución desde `origin/main` vigente.
Ejecutor: Codex CLI o Claude Cloud, sin corpus.
Producto: mapa accionable del residual y hasta tres paquetes siguientes para producción.

## Resultado encargado

Convertir NC-0256 en una decisión de producción: explicar por qué los slots actualmente `SIN-CANDIDATO` no tienen relevo y entregar **hasta tres paquetes siguientes concretos**, ordenados por resultado útil y con dependencias explícitas. Este es el diagnóstico autónomo que aquella NC proponía; **no redefine ni relanza GEN2-MEDICION-DEMANDA-3**, cuyo perímetro ya está reservado.

No es una auditoría de las 80 corridas ni un nuevo tablero general. Un slot sin candidato puede tener dato medido, carecer de enlace, necesitar una decisión o pertenecer a una salida computada. El trabajo debe separar esas causas y producir la próxima acción ejecutable; no terminar con un inventario sin uso.

Comprobado al emitir con el derivador vigente: 153 `SIN-CANDIDATO`. Por `tipo_uso`: 28 celda_L; 14 celda_R; 14 celda_M; 14 celda_AGREGADO; 22 momento; 13 asignado_probabilidad; 12 condicional_theta; 10 conducta_p_asignado; 8 coeficiente_asignado; 7 coeficiente_ejecutable; 6 corte_pi; 3 celda_D; 2 conducta_p_medido. Son valores del corte, no objetivos de control. Los **84 M/R/L/agregado** explican por qué no podemos traducir 153 automáticamente a encuestas faltantes.

## Insumos mínimos

- NC-0256 en `forense/no-corrido.tsv` y P3 de `forense/notas/2026-09-16-GEN2-PINS-REPRODUCE-1-cierre.md`.
- Enmienda de alcance en `forense/encargos/2026-09-15-GEN2-SPECS-DEMANDA-1.md`.
- `tools/relevo_usos.py`, demanda de corridas/resultados, usos y registro de oferta; sellos/specs sólo cuando hacen falta para resolver una correspondencia.
- Mapa `data/corrida0/mapa-demanda-19-corr-v1_0.tsv` como contexto fechado, no sustituto de demanda vigente.
- Declaraciones de consumidores, firmas y NC pertinentes a las rutas realmente seleccionadas. `data/manifiesto.yaml` e índices documentales sólo para establecer disponibilidad sin abrir microdatos.

## P1 · Derivación única y clasificación dirigida

Deriva con `tools/relevo_usos.py --json` sin `--escribe`; filtra `SIN-CANDIDATO`. Captura SHA y conteos por tipo. Cruza por identidades declaradas: slot → consumidor → corrida natural → CALC/spec → RESULT/sello. No infieras equivalencia científica por parecido de nombre, número o correlación.

Para cada slot registra **una causa principal accionable**, con subcausa opcional:

- `OFERTA-EXISTE-ENLACE-NO-DECLARADO`: sólo si hay candidato sustantivamente identificable; la ausencia del enlace no lo adopta.
- `SPEC-LISTA-EJECUCION-PENDIENTE`: spec congelada y disponibilidad documentada; distingue disponibilidad en manifiesto de bytes comprobados en CAJA.
- `SPEC-O-MEDIDOR-FALTANTE`: consumidor y fuente delimitados, falta implementación.
- `DATO-O-DOCUMENTACION-FALTANTE`: objeto exacto, no «falta investigar».
- `DECISION-O-ESTIMANDO-PENDIENTE`: decisión que cambia qué medir/consumir.
- `RESERVADO-O-YA-ENCARGADO`: Opus, F6, MEDICION-DEMANDA-3 u otro acto identificado.
- `SIN-RUTA-ACREDITADA`: evidencia insuficiente; no declarar que el dato no existe.

Estas categorías son una salida local de este diagnóstico; no crear un catálogo global de estados ni reemplazar el registro. Si conviene una etiqueta adicional, explica su necesidad en una línea.

Conserva identificadores y **consumidor exacto**; escala, universo y periodo sólo cuando importan para juzgar la ruta. Para salidas de marcador, cruza metadatos/IDs de corridas públicas previas; no inspecciones nuevos resultados reservados ni ejecutes emisiones. No conviertas una fuente legacy envolvida o un CALC con objeto distinto en medición GEN2 apta.

## P2 · Concentrar el juicio donde cambia la siguiente acción

Agrupa por dependencia compartida, no por cada slot como encargo separado. El censo mecánico cubre todos; la lectura sustantiva profunda se limita a los grupos que podrían producir el siguiente resultado. Reutiliza dictámenes vigentes, no los audites por tercera vez.

En particular:

- Distingue huecos de oferta de huecos de correspondencia del marcador; un marcador completo en otro corte no prueba relevo automático de cada slot actual.
- No proponer cargar theta entera, un «ensamble E» o una nueva interfaz general antes de identificar una salida y consumidor concretos. El piloto de Opus conserva esa decisión.
- CORR-0004, la sucesora ENADID/CORR-0013 y las cuatro celdas sin B pertenecen al remanente reservado de MEDICION-DEMANDA-3: no apropiarse del nombre ni duplicar sus specs.
- No tratar los 12 CANDIDATO-GEN2 como trabajo pendiente de este lote: tienen el encargo hermano RELEVO-CANDIDATOS-DELTA-1.
- No reabrir datos reservados, adquirir paquetes o llamar modelos para «comprobar que se podría». La disponibilidad documental permite una ruta propuesta, no una ejecución acreditada.

## P3 · Hasta tres paquetes listos para despachar

Entrega únicamente los paquetes que tengan consumidor, resultado, entradas y alcance distintos de los trabajos vivos. Cada ficha, máximo dos páginas, contiene:

1. Resultado sustantivo que entrega y pregunta/consumidor que lo usará.
2. Lista exacta de slots y fuentes; qué dato existe y dónde está acreditado.
3. Cambio mínimo necesario: enlazar con respaldo, escribir/ejecutar medidor, decidir un universo o adquirir un documento específico. Nunca «revisar todo».
4. Perímetro de archivos, entorno CLI/nube, dependencia de otro acto y compatibilidad con los encargos actuales.
5. Definición de terminado, comprobación material mínima y secuencia para llegar a un resultado.
6. Decisión pendiente, si la hay, con opciones y recomendación fundada; presupuesto de llamadas sólo si es realmente necesario, sin autorizarlo.

Prioriza salida/decisión que se habilita, reuso de insumos y costo real; no maximices número de slots ni fabriques una puntuación ponderada. Separa `LANZABLE-SIN-DECISION-NUEVA`, `ESPERA-MERGE` y `DECISION-REQUERIDA`. Estas fichas son propuestas: este acto no las lanza, no firma y no modifica la cola. Si sólo hay una útil o todas pertenecen al piloto, dilo con evidencia y no rellenes tres por obligación.

## Perímetro de escritura

- `forense/produccion/sin-candidato-rutas-1/`: TSV de rutas, resumen máximo tres páginas y hasta tres fichas ejecutables.
- `tools/rutas_sin_candidato.py` sólo si un script pequeño hace el cruce reproducible; sin modificaciones a componentes compartidos. Debe aceptar directorio de salida, no escribir por defecto en vistas canónicas.
- `tests/test_rutas_sin_candidato.py` sólo si hay lógica material nueva (p.ej. impedir tomar un RESULT homónimo de otro universo o perder slots por join).
- Encargo y nota de cierre propios.

No crear un dashboard, esquema general, índice o registro paralelo de decisiones. No editar las fuentes leídas.

## Cierre suficiente

Una fila por slot actual sin duplicados ni omisiones, reconciliación mecánica de los grupos y rutas propuestas respaldadas. Esa reconciliación es una comprobación simple, no una suite nueva. Cada propuesta permite lanzar una tarea concreta o tomar una decisión; «seguir investigando» no es un entregable.

Devuelve en primer lugar: qué puede producirse ahora, qué espera al piloto y qué necesita dato o decisión; después el detalle tabular. No presentes el número de archivos leídos como avance. Si el número de slots cambió, usa el universo vigente y explica el cambio sólo si afecta las prioridades.

## Autoridad, arranque y concurrencia — parte integral del encargo

Este archivo es un encargo propuesto por ChatGPT para Jonás. Su prompt de lanzamiento autoriza su ejecución; no atribuyas a mesa una firma nueva por la mera existencia del archivo. Al lanzarlo se autorizan trabajo en el perímetro, pruebas pertinentes, commits, push sin force y un PR; **fusión con Jonás**. No enviar correos ni solicitudes a terceros, comprar, aceptar contratos o efectuar llamadas experimentales a modelos. El agente CLI puede implementar normalmente.

1. Lee `AGENTS.md` y este encargo completo. Localiza el clon existente, reporta ruta absoluta, rama, HEAD y estado; fetch de `origin/main`, consulta de ramas, worktrees y PR del mismo objeto. Un PR ausente no demuestra que una sesión no esté trabajando: considera los encargos ya lanzados de esta conversación. No dupliques una ejecución viva.
2. Usa un worktree propio desde `origin/main` vigente. No cambies de rama, hagas stash, limpies o descartes archivos de otra sesión. No alteres el árbol que ejecuta el cron ni el del piloto de Opus. Si el SHA avanzó, revalida únicamente las premisas materiales; la variación de conteos no es causa automática de paro.
3. Archiva este texto verbatim en `forense/encargos/2026-09-16-GEN2-SIN-CANDIDATO-RUTAS-1.md`, con procedencia/consumo fuera del bloque original. Publica temprano la rama para visibilizar el trabajo; los commits técnicos pueden seguir antes de abrir el PR final.
4. **Excepción temporal de cascada, autorizada por el prompt de lanzamiento:** no escribir `decisiones.tsv` (ninguno), `no-corrido.tsv`, firmas, hallazgos, PARA, canon/gobernanza, canon/estado, registro de rótulos, índices generales, tableros, colas, manifiesto, rutinas, contadores o baseline. No reservar ADR/NC/FP. No ejecutar `/tramite`, `/despacha`, `/deriva`, cron ni `registro --verifica --escribe`. Esta excepción difiere su integración serial; no elimina permanentemente las reglas del proyecto ni autoriza debilitar checks.
5. Opus conserva CAREO, TRÁMITE-4, CELDA-D-PILOTO-1, corte de edad, crosswalk y firmas. F6-FACTIBILIDAD-PREPARACION-1 conserva MOCIBA/ISSP; DIGESTO-CORRECTIVO-1 conserva su generador y pruebas. **No leer ni derivar ENIF 2024 localidad × edad**, ni capturas/resultados nuevos del piloto; no abrir microdatos ni desenlaces reservados de F6. Ningún script, test o verificación masiva puede hacerlo incidentalmente. Lectura de resultados históricos ya públicos sólo donde este encargo la necesita; nunca reconstruir con ellos el cruce reservado.
6. No editar `milpa/`, motor, theta, G5, contratos sellados, medidores ajenos, scripts de adquisición o archivos de los otros encargos. Si una pieza exige una decisión material, completa las independientes y devuelve esa decisión concreta; no abandones el producto por numeraciones, nombres o cascada diferida.
7. Antes del push final, incorpora `origin/main` por un procedimiento que preserve historial compartido. Revisa diff y pruebas afectadas. No reejecutes una medición ya sellada sólo porque avanzó documentación: usa su verify dirigido si procede. CI heredado se compara con baseline bajo el mismo entorno; nunca `--freeze`, exenciones nuevas o cifras inventadas. Si un gate requiere un archivo excluido, entrega PR con producto y bloqueo exacto para integración serial.
8. Entrega SHA base/final, producto, comandos reales, pruebas/CI y reservas. En el PR: `CIERRE COMPARTIDO DIFERIDO — integrar después de CAREO/TRÁMITE-4`; lista sólo propagaciones necesarias, sin números reservados. Un PR listo no equivale a integrado, adoptado, validado o desplegado.

Auditoría y documentación auxiliar: aproximadamente 20% del esfuerzo. La definición del estimando y la verificación de escala/universo son parte sustantiva del resultado. Una o dos comprobaciones razonables ante fallo; alternativa directa y bloqueo preciso. Termina con un producto usable o con la causa material y la siguiente acción exacta, sin auditoría general.

## Prompt de lanzamiento

> Ejecuta íntegramente ENCARGO-GEN2-SIN-CANDIDATO-RUTAS-1.md desde origin/main vigente, worktree propio. Autorizo este diagnóstico autónomo de NC-0256, archivos/scripts del perímetro, pruebas pertinentes, commits, push y un PR; fusión conmigo. Autorizo diferir cascada compartida. No redefinas MEDICION-DEMANDA-3 ni dupliques encargos de Opus/F6/digesto/relevos. No midas, no adquieras, no llames modelos experimentales ni abras datos reservados. Entrega el cruce mecánico y hasta tres paquetes siguientes realmente ejecutables, con consumidores, entradas, archivos y compuertas concretas; no otro censo sin siguiente acción.

<!-- CONSUMO (fuera del bloque original): ejecutado en
`acto/gen2-sin-candidato-rutas-1`; producto en
`forense/produccion/sin-candidato-rutas-1/` y cierre en
`forense/notas/2026-09-16-GEN2-SIN-CANDIDATO-RUTAS-1-cierre.md`. -->
