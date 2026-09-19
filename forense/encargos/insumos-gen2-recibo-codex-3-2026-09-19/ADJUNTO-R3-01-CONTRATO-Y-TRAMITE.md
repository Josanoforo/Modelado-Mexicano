# ENCARGO CODEX CLI · GEN2-CONTRATO-Y-TRAMITE-CLI-1

Fecha de preparación: 19/sep/2026. Repositorio: `Josanoforo/Modelado-Mexicano`.
Base revisada: `9eff694ecff8e74d2aed05fe5fac9e4d530363fc` (merge de #860).

## Resultado que debes entregar

Un PR con el contrato celda-D v0.6 capaz de representar correctamente al piso C2 adjudicado en los dos pilotos y con sus firmas y trámites pendientes propagados. Absorbe íntegramente `GEN2-TRAMITE-5` y `GEN2-VOCABULARIO-v0.6`, salvo la adopción efectiva, que pertenece exclusivamente a `GEN2-MARCADOR-ADOPCION-CLI-1` (encargo 03). Cero mediciones y cero llamadas a modelos.

El cambio deja representada la decisión de mesa; no afirma que el consumidor ya use los valores. Este encargo puede correr en paralelo con el 02, en otro worktree.

## Operación en Codex CLI

1. Lee este documento completo, `AGENTS.md` y solo los contratos necesarios. Localiza el clon existente. Reporta ruta absoluta, rama, HEAD y `git status --short`. Haz `git fetch --prune`; parte de `origin/main` actualizado en worktree y rama propios. Conserva cambios ajenos; no limpies ni descartes su trabajo.
2. Busca duplicados tanto por este rótulo como por los dos originales en worktrees, ramas remotas y PR abiertos. Retoma trabajo equivalente cuando sea seguro; no crees un segundo PR de la misma tarea. Los PR de rutinas no son duplicados.
3. Este lanzamiento autoriza implementar el perímetro, hacer commits, push de la rama de trabajo y abrir/actualizar un PR contra main. No autoriza fusionarlo. Archiva el encargo y los insumos utilizados con sus bytes y SHA-256 reales. No dependas de que Codex tenga un comando `/acto`: ejecuta los pasos aplicables del procedimiento del repo mediante sus herramientas normales, subordinados a `AGENTS.md` y a este encargo.
4. No hay compuerta de merge para iniciar. Si main avanzó, ejecuta solo el delta material pendiente. Deriva identificadores al cierre; no heredes los máximos del 17/sep. Hasta aproximadamente 20% del esfuerzo en control/documentación. Una discrepancia cosmética se anota y no detiene el resultado.
5. No abras microdatos. Los archivos de `fuentes/` se entregan junto a este encargo. Son insumos de dirección y evidencia histórica, no sustitutos de main.

## Insumos que sí debes leer

En `fuentes/`: los originales `ENCARGO-GEN2-TRAMITE-5-2026-09-17.md` y `ENCARGO-GEN2-VOCABULARIO-v0_6-2026-09-17.md`; `FIRMA-2026-09-17-piso-adoptado-y-MARCADOR-v1_1-delta.md`; `cabecera-v1_14.md`; `seccion-13.md`. El estado v1.14 completo adjunto es referencia: **no lo copies sobre el estado vigente**.

En main: contrato v0.5, los dos YAML de los pilotos, sus CALC de emisiones, `tests/test_celdas_d.py`, `tools/corrida0.py`, tableros de firmas/decisiones/NC y las notas concretas que sustentan cada trámite. Localiza documentos por objeto; las líneas de los originales pueden haberse movido.

## Firma sustantiva que se propaga, sin inventar otra

> Un piso no vencido en su celda-D es el estimador adjudicado de esa celda y se adopta salvo veto de mesa. Se adoptan las 20 celdas de ADR-538 y ADR-542 (piso C2) como estimadores por celda de sus reglas consumidoras. El vocabulario celda-D v0.6 lo escribe. Los retadores son credencial para emitir donde no hay piso, no sustitutos del piso donde lo hay.

La fecha histórica de esa firma es 17/sep; la fecha de esta ejecución será la real. Un registro de la firma no equivale a una nueva medición ni al merge del PR.

## P1 · Contrato y representación de las 20 estimaciones

Crea `propuesta-motor-adaptativo-celda-v0_6.md` conservando v0.5. Implementa los cuatro cambios originales: adjudicación del piso no vencido, `estrategia: persistencia`, alias de rol `PISO` para `BASELINE_INGENUO` y referencia al vocabulario de identificación de `milpa/theta-esquema-e1-v1_0.yaml`. No dupliques esos tokens. Define persistencia por mismo estimando, texto/semántica del reactivo, universo y categorías comparables; los nombres técnicos pueden diferir entre olas.

**Ajuste necesario al original:** una celda-D de piloto contiene 8 o 12 segmentos; `champion_actual` no puede ser un único RESULT arbitrario de todos ellos. Usa una representación mínima compatible con los contratos anteriores:

- Identificador explícito del candidato C2 dentro de cada piloto (`id_candidato: C2`, o reutiliza el equivalente si main ya lo incorporó).
- `champion_actual: C2`, que identifica al candidato adjudicado; no es el id de una observación.
- Un mapa `adjudicacion_por_celda` con 8 o 12 claves de segmento. Cada entrada enlaza al candidato, CALC, RESULT puntual primario y los dos RESULT del IC95; lleva la referencia de decisión. No duplica valores numéricos editables.
- La identidad conserva regla/estimando, instrumento-ola, desenlace, ejes, categorías y universo. Un código de segmento se decodifica usando la spec, nunca por intuición.

En los resultados de main están los puntos `RESULT-DIN-LXE8-C2-P-L…xE…` y `RESULT-TRA-SXD12-C2-P-S…xD…`, junto a sus `IC95INF`/`IC95SUP`. Resuélvelos por spec y claves exactas. Excluye `P-REDERIVADO`, controles, conteos y sensibilidades: un simple filtro que contenga `C2` incluiría resultados distintos. Produce exactamente la correspondencia 8 + 12 para los pilotos existentes; si el contenido cambió, explica el delta.

Enmienda los dos YAML de pilotos y su `vocabulario_version: 0.6`, conservando sus comentarios históricos y el veredicto `SIN-CANDIDATO-SUPERIOR`. Si el veredicto solo existe en prosa, añade un campo estructurado respaldado por su resultado sellado; no lo infieras del texto de un test. Enmienda también la estrategia de C1 a `persistencia` cuando corresponda, manteniendo la regla de composición y la procedencia de su clasificación anterior. Las tres celdas-D de agosto permanecen intactas.

Validación proporcional: v0.4/v0.5 siguen siendo válidas; v0.6 conserva las exigencias de v0.5 y añade sus campos. Piso adjudicado solo bajo decisión existente, candidato de rol admisible, estado permitido y veredicto pertinente; no adjudicar por mero valor `INDECIDIBLE`. Valida referencias, cobertura y ausencia de duplicados o intercambio de segmentos. La validación no debe permitir que una fila `IC95INF` se use como punto. NC-0305 cierra cuando contrato y uso estén corregidos.

## P2 · Firmas y cierres del trámite original

Escribe una sola vez la decisión de adopción C2, con la firma anterior y referencias a los 20 puntos. No intentes activar consumidores aquí. Si ya existe, reutilízala.

Completa las tres filas faltantes originales: FP-379 (objeto `piloto-1:C2-tres-decisiones`), su enmienda D9 (`piloto-1:FP-379-enmienda-D9`) y FP-385 (`piloto-2:firma`). Recupera sus verbatim del tablero y del encargo archivado del piloto; no reconstruyas de memoria los nueve códigos ni las decisiones. El original alterna “tres” y “cuatro” filas: manda el conjunto de objetos efectivamente faltantes, no una cuota.

Propaga estas siete decisiones ya dadas en TRÁMITE-5, sin ampliar su alcance:

| NC | Decisión a propagar |
|---|---|
| NC-0274 | Rige 16/sep/2026 para la firma ADR-531/FP-377; no se editan sellos; se registra la discrepancia y cierra. |
| NC-0328 | `edad × dominio` ENVIPE 2025 queda consumida sin piloto y no se usa como celda-D; cierra la NC, permanece la reserva consumida. |
| NC-0227 | #682, #719, #726 y #728 son huérfanos aceptados; una nota, ningún encargo retrospectivo fabricado. |
| NC-0255 y NC-0256 | MEDICION-DEMANDA-3 sigue el universo vigente de relevo-usos, priorizando CANDIDATO-GEN2; 153 y 12 son foto histórica, no metas ni números inmutables. |
| NC-0237 | R01-MOCIBA diferido a F6 mientras no exista acreditación; cerrar la NC no ejecuta ni acredita F6. |
| NC-0254 | RES-0043/0044 no se corroboran con EDER: primera unión y situación conyugal actual son estimandos distintos; quedan SIN-CANDIDATO, sucesor ENADID 2023. Cierra NC, no los slots. |

Para el registro conserva el verbatim completo del original, disponible en `fuentes/`, y añade el estado actual por separado cuando haya cifras vencidas. Cambia `relevo-usos` por su generador/fuente de decisión. Si este no soporta la corrección firmada, está permitido añadir el caso mínimo en `tools/relevo_usos.py` o en su fuente canónica; no edites manualmente la tabla derivada ni construyas un framework nuevo.

Las NC-0024/0076/0239/0300 reciben la enmienda de sucesor hacia el marcador; siguen abiertas hasta el encargo 03. Corrige la huella de rutina del 17/sep con la causa/resolución ADR-539. Actualiza el índice de infraestructura para celdas-D, capa E1, replay y catálogo según los archivos realmente existentes. Recibo acotado de #851, #852, #853 y #855: producto y decisión residual material; revisa la acción de mesa de #855. No absorbas ni cierres los nuevos PR #861–#864.

## P3 · Estado v1.14, preservando historia y corrigiendo errores de contenido

Reconstruye sobre el estado vigente en main: sustituye la cabecera por el fragmento adjunto y añade la sección nueva, preservando el cuerpo y todas las anotaciones L0 existentes. El archivo v1.13 de main mide 1 269 470 bytes al corte revisado: ni el tamaño ni un número de línea del encargo antiguo garantizan que el adjunto completo conserve la historia. Usa anclas verificadas, no “primeras 12 líneas” a ciegas. Si ya existe una versión posterior, aplica la enmienda sobre la vigente, sin rebajar versión.

**Este encargo corrige expresamente la orden de incorporar §13 sin correcciones materiales.** Archiva el fragmento original intacto, pero en la sección que publiques corrige, con una nota breve fechada de procedencia, estos errores:

1. `status()` llama `_filas_registro(verifica=False)`: deriva en memoria desde demanda, oferta en disco y decisiones; `N_corridas_selladas` filtra OFERTA, `cuenta_gen2=SI` y estado sellado/superado. No cuenta simplemente filas publicadas. Separa total de sellos físicos, corridas GEN2 que cuenta status, publicadas y selladas sin publicar. No presentes 82 + 16 = 98 como total físico: el anexo original reportaba 115 sellos y otros filtros.
2. 97 es el tamaño del censo del emisor, con cinco SIN-CONTRAPARTE; 117 no es todavía un universo válido del marcador. Déjalo pendiente de la derivación del encargo 03.
3. Decisión firmada de adoptar 20 segmentos, representación en contrato y consumo activo son etapas diferentes. Después de este PR las dos primeras pueden estar hechas; no declares 20 adopciones activas sin consumidor.
4. En el mismo texto hay afirmaciones incompatibles sobre escalas “15→11” frente a “todas declaradas”: conserva el resultado efectivamente respaldado, sin completar el faltante por suposición.

Para cifras restantes conserva la foto fechada donde sea correcta y agrega el estado al ejecutar solo cuando afecte su lectura. No reaudites todo el estado histórico. Retira únicamente la versión viva sustituida según T01. Actualiza referencias operativas mutables; **no hagas reemplazo global dentro de CALC/spec/scripts sellados, encargos históricos o firmas verbatim**. Incluye las referencias de herramientas de cierre que la renominación realmente afecte. Verifica que el cuerpo heredado no perdió contenido, descontando únicamente las adiciones de cierre autorizadas. No publiques todavía el informe v1.1 adjunto como si describiera adopción efectiva: se revisó como contexto, no como un producto que ya corrió.

## Perímetro y cierre

Contrato v0.6; dos YAML de pilotos; test de celdas-D; fuentes firmadas archivadas; decisiones/firmas/NC/hallazgos/rutinas; estado vigente y citas operativas imprescindibles; infraestructura; registro de rótulos; nota y cascada existente. `tests/check.py` solo ajustes estrictamente necesarios de rótulos; `tools/relevo_usos.py` solo la corrección RES-0043/0044; herramientas que referencien el estado renombrado solo su referencia operativa. No se modifican números ni bytes sellados, `tramite.yaml`, capa E1, crosswalk, replay, catálogo ni el motor numérico.

Pruebas: validador v0.4/0.5/0.6 y correspondencia de las 20 estimaciones; diff del cuerpo del estado; generador de relevo si se tocó; baseline una vez al cierre y otra solo si un cambio posterior lo requiere. No congeles un baseline nuevo para esconder fallos.

Entrega un PR, con contrato usable y decisiones propagadas. Reporta cobertura de las piezas originales y la única dependencia deliberada: adopción efectiva por el encargo 03. Regenera derivados desde fuentes tras sincronizar; no resuelvas conflictos eligiendo una tabla vieja. Quien fusione segundo renumera lo necesario. Incluye `NO-CORRIDO / RESERVAS` y `CONSUMIDO` conforme al procedimiento existente, con número real de PR. No declares listo un PR cuyo último commit no esté remoto. No fusiones.

La tarea termina cuando el contrato representa los 20 segmentos sin ambigüedad, el trámite material está propagado y el estado no atribuye al programa resultados todavía no consumidos.
