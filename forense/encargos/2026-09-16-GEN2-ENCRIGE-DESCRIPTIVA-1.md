# Procedencia y consumo

- Procedencia: archivo de lanzamiento entregado por Jonás el 16 de septiembre de 2026 desde `Descargas MX`; archivado sin alterar el bloque original.
- Consumo: mandato operativo exclusivo de `GEN2-ENCRIGE-DESCRIPTIVA-1`; la integración documental serial queda diferida conforme al propio encargo.

<!-- INICIO DEL BLOQUE ORIGINAL VERBATIM -->
# ENCARGO · GEN2-ENCRIGE-DESCRIPTIVA-1

Fecha: 16 de septiembre de 2026. Repositorio: `Josanoforo/Modelado-Mexicano`.
Base consultada: `9dffd6455c67e2ca99740e79f90be59a13f250e1`; ejecución desde `origin/main` vigente.
Ejecutor: Codex CLI en CAJA/WSL, con corpus; nube sólo si ya dispone de esos documentos/tabulados.
Producto: tabla e interpretación descriptiva para el informe TRA.

## Resultado encargado

Entregar una lectura cuantitativa reproducible de **corrupción experimentada por unidades económicas en ENCRIGE 2020**, total y por tamaño cuando los tabulados oficiales lo permitan. Es la familia descriptiva R08 que mesa admitió por F-19; no es transferencia de M, una celda-D adjudicada ni validación F6.

La firma F-19 está en `forense/encargos/2026-09-15-GEN2-F6-PANEL-CAJA-1.md`, y su propagación en la nota de cierre homónima y el panel v1.3. **No abras ENCRIGE 2016**, WBES, MOCIBA o ISSP. Este encargo al lanzarse autoriza la extracción descriptiva de 2020 que se especifica abajo, sin necesitar firmas de llamadas o del piloto celda-D.

La extracción existente `data/fuentes-financieras-20/encrige2020-cumplimiento-contratos.csv` observa otro objeto: cumplimiento entre contrapartes privadas. No la presentes como corrupción en trámites. Consulta su nota para no repetirla, no para reutilizar su denominador.

## Insumos ya registrados

Consulta las entradas exactas de `data/manifiesto.yaml`:

- `conjunto_de_datos_encrige_2020_csv`: ZIP de **tabulados**, no archivo de respondentes.
- `encrige2020_cuestionario`.
- `gen2_encrige2020_diseno_muestral`.

Lee `tools/entorno.py` y resuelve sus raíces reales; un worktree sin `data/raw` no es prueba de corpus ausente. Usa la configuración existente del clon padre, sin copiar datos al repositorio. Verifica identidad de esos tres objetos, no de todo el corpus. Sin corpus accesible en CAJA, prueba la raíz configurada y una alternativa documentada; si sigue ausente entrega el adaptador/spec probado y la ruta exacta faltante. No descargues otro corpus ni inventes resultados.

## P1 · Fijar el objeto antes de extraer valores

Lee cuestionario, diseño y títulos/encabezados de cuadros. Fija en `spec.md` y `spec.yaml`, con commit anterior a la corrida:

1. Unidad de observación y universo institucional exactos: qué unidades económicas, sectores, territorios y exclusiones cubre la encuesta. El año de la edición no sustituye el periodo de referencia del desenlace: transcríbelo del instrumento.
2. Indicador primario: prevalencia de unidades que experimentaron al menos un acto de corrupción entre las unidades del **denominador publicado correspondiente**. Si el cuadro usa otra definición o expresa la tasa por 10 000 unidades, conserva su nombre y tasa oficial y declara cualquier conversión a proporción/porcentaje. No denomines prevalencia a número de actos por unidad o a percepción de corrupción.
3. Desagregación: total nacional y categorías de tamaño oficiales que realmente existan; conserva sus definiciones, sin mapearlas a cortes de persona del modelo. No fabricar cruces ausentes, ni escoger sólo tamaños con una diferencia interesante.
4. Identidad de cuadros, filas, columnas, unidades, denominadores y notas; política de celdas suprimidas, no disponibles, cero y redondeo. Un número de unidades expandido no es n muestral. Si el tabulado no ofrece n, declarar `NO-PUBLICADO`.
5. Incertidumbre: conservar IC/EE/CV publicados del mismo indicador y dominio; si no existen, emitir punto con incertidumbre no disponible. No construir IC binomial con conteos expandidos ni usar variación entre tamaños como EE.
6. Pregunta consumidora: «¿Cómo se distribuye la corrupción experimentada en unidades económicas por tamaño en el universo ENCRIGE 2020?». Consumidor documental: anexo descriptivo TRA previsto en F-19 para el informe. No cambiar el informe canónico en este acto.

Permite un máximo de dos indicadores sustantivos: el primario anterior y, sólo si los mismos cuadros lo sostienen claramente, número de actos por unidad expuesta, identificado por separado. El total y sus tamaños son dominios, no muestras independientes. Si el primario no se puede obtener, devuelve la razón; no lo sustituya por percepción o por incumplimiento privado para cumplir una cifra.

No afirmar evaluación ciega: se trata de descripción de tabulados públicos, no holdout. Si fue necesario ver un valor al localizar el cuadro, declara esa exposición; no invalida la descripción ni habilita F6.

## P2 · Implementar y ejecutar la extracción

Usa una carpeta CALC propia `data/corrida0/CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001/`, medidor con la interfaz vigente y salidas deterministas. Reutiliza el contrato de corrida0; no crees otro registro general. Inspecciona un CALC descriptivo vigente como ejemplo de interfaz, sin heredar su método, decisiones o etiquetas de medición de microdato.

Etiqueta inequívoca: `EXTRACCION-DESCRIPTIVA-TABULADOS-OFICIALES`, `UNIDAD-DISTINTA-NO-TRANSFERENCIA`, uso `CONTEXTO-INFORME-NO-CALIBRA`. No declares que se estimó nuevamente el diseño de INEGI. Conserva `cuenta_gen2` pendiente de decisión conforme al esquema vigente: el lanzamiento autoriza ejecutar el producto, no inventar una firma de contador.

Secuencia: spec/medidor fijados → preflight propio → run propio → sello/verify propio. Ningún `run` o `verify` masivo. Si el mecanismo no permite registrar sólo el CALC sin escribir vistas comunes, **difiere el registro global**; devuelve la carpeta sellada y verificable. Si una precondición material del contrato falla, no la evadas escribiendo sellos manuales: conserva el producto reproducible y distingue extracción lograda de CALC no sellado.

CSV final por indicador/dominio con: valor original/unidad, transformación explícita y valor normalizado si aplica, numerador/denominador cuando estén publicados, n muestral o ausencia, incertidumbre tipada o ausencia, periodo, cuadro y localizador, notas de supresión y procedencia. No rellenes campos desconocidos con cero.

## P3 · Lectura útil y control proporcional

Produce `lectura-TRA.md`, máximo cuatro páginas equivalentes: tabla legible, principales diferencias descriptivas, qué población cubren, qué conclusión permiten y cuál no. Añade gráfico estático sólo si aporta claridad; ejes/unidades y celdas ausentes visibles. Sin ranking de M/L, sin «validación del motor», sin causalidad y sin comparación numérica directa con tasas de personas de ENCIG.

Verificación suficiente: concordancia del total y un dominio con el cuadro original por una segunda lectura local; transformación de escala; faltantes/supresión; repetición estable. Un test sintético sólo si protege errores materiales del extractor (por ejemplo, confundir tasa por 10 000 con porcentaje). No promediar tasas de tamaños para reconstruir el total sin pesos/denominadores adecuados.

## Perímetro de escritura

- La carpeta CALC propia indicada, incluidos su medidor, spec y evidencias que el mecanismo exija.
- `forense/analisis/encrige-descriptiva-1/`: CSV, lectura y gráfico opcional.
- `tests/test_encrige_descriptiva.py` si es necesario.
- Encargo y nota exclusivos de este rótulo.

No editar el panel F6, informe canónico, inventarios, fuentes financieras previas, manifiesto, `milpa/` o helpers compartidos. No abrir adquisiciones.

## Cierre suficiente

Resultado tabular + interpretación con alcance correcto + reproducción dirigida, o ausencia material documentada del indicador exacto. Distingue extracción nueva, resultado oficial reproducido, medición propia, sello y adopción. No reportes «una nueva familia confirmatoria» ni N corridas científicas porque haya N filas. La integración posterior añade esta sección descriptiva al informe, sin tocar el piloto.

## Autoridad, arranque y concurrencia — parte integral del encargo

Este archivo es un encargo propuesto por ChatGPT para Jonás. Su prompt de lanzamiento autoriza su ejecución; no atribuyas a mesa una firma nueva por la mera existencia del archivo. Al lanzarlo se autorizan trabajo en el perímetro, pruebas pertinentes, commits, push sin force y un PR; **fusión con Jonás**. No enviar correos ni solicitudes a terceros, comprar, aceptar contratos o efectuar llamadas experimentales a modelos. El agente CLI puede implementar normalmente.

1. Lee `AGENTS.md` y este encargo completo. Localiza el clon existente, reporta ruta absoluta, rama, HEAD y estado; fetch de `origin/main`, consulta de ramas, worktrees y PR del mismo objeto. Un PR ausente no demuestra que una sesión no esté trabajando: considera los encargos ya lanzados de esta conversación. No dupliques una ejecución viva.
2. Usa un worktree propio desde `origin/main` vigente. No cambies de rama, hagas stash, limpies o descartes archivos de otra sesión. No alteres el árbol que ejecuta el cron ni el del piloto de Opus. Si el SHA avanzó, revalida únicamente las premisas materiales; la variación de conteos no es causa automática de paro.
3. Archiva este texto verbatim en `forense/encargos/2026-09-16-GEN2-ENCRIGE-DESCRIPTIVA-1.md`, con procedencia/consumo fuera del bloque original. Publica temprano la rama para visibilizar el trabajo; los commits técnicos pueden seguir antes de abrir el PR final.
4. **Excepción temporal de cascada, autorizada por el prompt de lanzamiento:** no escribir `decisiones.tsv` (ninguno), `no-corrido.tsv`, firmas, hallazgos, PARA, canon/gobernanza, canon/estado, registro de rótulos, índices generales, tableros, colas, manifiesto, rutinas, contadores o baseline. No reservar ADR/NC/FP. No ejecutar `/tramite`, `/despacha`, `/deriva`, cron ni `registro --verifica --escribe`. Esta excepción difiere su integración serial; no elimina permanentemente las reglas del proyecto ni autoriza debilitar checks.
5. Opus conserva CAREO, TRÁMITE-4, CELDA-D-PILOTO-1, corte de edad, crosswalk y firmas. F6-FACTIBILIDAD-PREPARACION-1 conserva MOCIBA/ISSP; DIGESTO-CORRECTIVO-1 conserva su generador y pruebas. **No leer ni derivar ENIF 2024 localidad × edad**, ni capturas/resultados nuevos del piloto; no abrir microdatos ni desenlaces reservados de F6. Ningún script, test o verificación masiva puede hacerlo incidentalmente. Lectura de resultados históricos ya públicos sólo donde este encargo la necesita; nunca reconstruir con ellos el cruce reservado.
6. No editar `milpa/`, motor, theta, G5, contratos sellados, medidores ajenos, scripts de adquisición o archivos de los otros encargos. Si una pieza exige una decisión material, completa las independientes y devuelve esa decisión concreta; no abandones el producto por numeraciones, nombres o cascada diferida.
7. Antes del push final, incorpora `origin/main` por un procedimiento que preserve historial compartido. Revisa diff y pruebas afectadas. No reejecutes una medición ya sellada sólo porque avanzó documentación: usa su verify dirigido si procede. CI heredado se compara con baseline bajo el mismo entorno; nunca `--freeze`, exenciones nuevas o cifras inventadas. Si un gate requiere un archivo excluido, entrega PR con producto y bloqueo exacto para integración serial.
8. Entrega SHA base/final, producto, comandos reales, pruebas/CI y reservas. En el PR: `CIERRE COMPARTIDO DIFERIDO — integrar después de CAREO/TRÁMITE-4`; lista sólo propagaciones necesarias, sin números reservados. Un PR listo no equivale a integrado, adoptado, validado o desplegado.

Auditoría y documentación auxiliar: aproximadamente 20% del esfuerzo. La definición del estimando y la verificación de escala/universo son parte sustantiva del resultado. Una o dos comprobaciones razonables ante fallo; alternativa directa y bloqueo preciso. Termina con un producto usable o con la causa material y la siguiente acción exacta, sin auditoría general.

## Prompt de lanzamiento

> Ejecuta íntegramente ENCARGO-GEN2-ENCRIGE-DESCRIPTIVA-1.md en CLI/CAJA, worktree propio. Autorizo fijar y ejecutar la extracción descriptiva de ENCRIGE 2020 desde los tres insumos ya registrados, pruebas dirigidas, sello/verify propio cuando el contrato lo permita, commits, push y un PR; fusión conmigo. Autorizo diferir cascada y registro global. Respeta F-19: unidades económicas, descripción para el informe, cero transferencia de M o evaluación F6. No abras ENCRIGE 2016, ENIF reservado ni otras familias. Entrega tabla, lectura sustantiva y reproducción; no te detengas en redactar una spec si el corpus permite terminar la extracción.
<!-- FIN DEL BLOQUE ORIGINAL VERBATIM -->
