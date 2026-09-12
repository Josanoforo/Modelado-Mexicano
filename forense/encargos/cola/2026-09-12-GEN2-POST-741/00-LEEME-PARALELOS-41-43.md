# Siguientes encargos GEN2 · 41, 42 y 43

Preparado para Jonás el 12 de septiembre de 2026. Base revisada: `main=6e634aaaa3dec6ed536bae1ef142a4f7ff56cfae`, después de #741, que encola 39/40. Ambos están en ejecución según Jonás. La consolidación de las ramas de 39 queda en su sesión original.

## Qué lanzar ahora

Los tres archivos son encargos autónomos para Codex CLI en CAJA Windows/WSL. Cada uno incluye apertura de spec descriptiva al despacharlo, ejecución con datos reales, comprobación material, registro y PR. No basta inventariar fuentes o entregar fixtures.

**Si hay dos sesiones disponibles, lanzar 41 y 42. Con una tercera, añadir 43.** No requieren esperar la terminación de 39/40 para producir sus resultados. 41 y 42 ofrecen evidencia mexicana; 43 aporta una comparación estadounidense con universos explícitos.

| Encargo | Trabajo y producto | Insumos | Límite que conserva |
|---|---|---|---|
| **41 · Banxico** | Medir comportamiento de pago, problemas, reclamaciones y asociación con costo percibido, por cinco productos y seis olas compatibles | Microdatos, manual e informe ya adquiridos en #734 | Población urbana usuaria; costo percibido no es CAT; asociación no es causalidad |
| **42 · N35/MOTRAL 2015** | Medir valoración declarada de seguridad social y prioridad de prestaciones; cruce viable ENOE; adquirir el experimento mexicano de elección laboral | MOTRAL 2015 ya registrado; comprobar ENOE 2015-T2 y obtener material específico faltante | Preferir seguridad social aun aportando no prueba que pese más que cualquier salario |
| **43 · SHED 2025** | Cinco mediciones de BNPL: uso, atraso, cargo, sobregiro condicional y asequibilidad × atraso | CSV y codebook ya adquiridos en #734; completar cuestionario oficial | Estados Unidos; sin traslado de tasas a México ni mezcla de denominadores |

41 y 43 aprovechan el material de #734 para producir mediciones que ese cierre no ejecutó. 42 responde a un hallazgo nuevo: el [cuestionario oficial MOTRAL 2015](https://www.inegi.org.mx/contenidos/programas/motral/2015/doc/motral2015_cuestionario.pdf) sí pregunta por preferencia de empleo con seguridad social (17) y orden de prestaciones (16). La corrección del registro será fuente-específica y conservará la carencia de comparación salarial estricta.

## Cómo repartir la propiedad

| Sesión | Propiedad |
|---|---|
| 39, en curso | Extracción, correspondencias, índice y búsqueda general |
| 40, en curso | Conciliación de demanda/NC-0165, contratos, ruteo, consumidores, emisor y conciliación global de NC-0164 |
| 41 | `CALC-BANXICO-PRODUCTO-DANO-0001`, medidor y agregados propios, relación Banxico de N34 |
| 42 | `CALC-MOTRAL2015-VALORACION-SS-0001`, medidor y agregados propios, relación N35 y adquisición del experimento mexicano |
| 43 | `CALC-SHED2025-BNPL-DANO-0001`, medidor y agregados propios, relación SHED de N34 |

Los CALC nuevos son identidades propuestas: cada sesión comprueba si ya existen antes de darlos de alta. No se establece dependencia entre los tres cálculos ni orden obligatorio de merge. Sí pueden coincidir cambios por clave en manifiesto, registros y sus proyecciones; cada PR conserva las altas ajenas y regenera sobre el árbol combinado cuando corresponda. Cada sesión usa worktree/rama/PR propio. Los merges quedan con Jonás.

Pasar este mensaje breve a la sesión 40 cuando se despachen los nuevos encargos:

> He lanzado 41, 42 y 43 en paralelo. Reserva para ellos los cálculos Banxico producto/atraso/costo percibido; MOTRAL 2015 preguntas 16/17 y su cruce ENOE; y SHED 2025 BNPL/daño. Registra esos objetos como delegados para evitar duplicar implementación. Continúa tu lote viable en los demás objetos y la conciliación general; incorpora sus resultados cuando estén disponibles, sin esperar a los tres para cerrar tu trabajo independiente. Conservas NC-0165, motor/emisor y la conciliación global de NC-0164. Sus resultados descriptivos no implican adopción automática. Si ya empezaste exactamente alguno, informa el objeto y avance para que el nuevo encargo ejecute sólo el residual.

Si sólo se despachan 41 y 42, omitir 43 del mensaje. No hace falta otra adenda extensa a 39: 42 le entregará los localizadores acreditados para su índice.

## Adquisiciones concretas

| Dueño | Material | Estado y acción |
|---|---|---|
| 41 | `gen2_banxico_satisfaccion_usuarios_2019_2024_microdatos`, `gen2_banxico_satisfaccion_usuarios_2019_2024_manual`, `gen2_banxico_satisfaccion_usuarios_2024_informe` | Adquisición acreditada en #734. Resolver en CAJA y recuperar sólo si falta físicamente alguno; no repetir lote |
| 42 | `motral2015_cuestionario`, `motral2015_bases_datos_dbf` | Registrados bajo raíz `descargas_mx`, `UNIVERSO-2026-09/MOTRAL/`. Inspeccionar todas las tablas 2015; no quedarse en la tabla de empleos 2012 |
| 42 | Descriptor MOTRAL 2015 y ENOE 2015-T2 pertinente | Comprobar disponibilidad, llaves y pesos. Si faltan, adquirir únicamente documentos/tablas necesarios para enlazar la persona del módulo con su empleo actual |
| 42 | *Do Workers Value Formal Jobs? A Discrete Choice Experiment in Mexico*; paper, presentación y anexos | Pista concreta en la [página del autor](https://sites.google.com/site/robertduvalhernandez/research) y [sesión EEA-ESEM 2026](https://eea-esem-congresses.org/sessions/migration-and-informality). Recuperar desde «Read paper»/«View» o repositorio del autor. Las páginas se verificaron; los binarios no se obtuvieron aquí |
| 42 | Cuestionario, código y datos de replicación del mismo experimento mexicano | Disponibilidad pública todavía no acreditada. Buscar de forma dirigida; adquirir sólo lo que exista. No sustituirlo por el estudio brasileño de título similar |
| 43 | `gen2_federal_reserve_shed_2025_public_csv`, `gen2_federal_reserve_shed_2025_codebook` | Adquisición acreditada en #734. Usar el corte 2025 existente |
| 43 | [SHED 2025, cuestionario oficial, apéndice A](https://www.federalreserve.gov/publications/2026-supplemental-appendixes-report-economic-well-being-us-households-2025-appendix-a.htm) | Obtener y registrar si falta. El HTML oficial acredita el filtro `BNPL1=1` y `BK2_f=1` de `BNPL1A`; no hace falta descargar otras olas |

Son adquisiciones públicas puntuales. No se propone compra ni contacto con autores. Si el experimento mexicano no ofrece microdatos públicos, 42 entrega el material y alcance verificables y completa de todos modos el cálculo MOTRAL.

## Cuándo sirve activar el cron

**Los nuevos cálculos no requieren una descarga general.** Primero cada dueño resuelve los IDs en CAJA. La adquisición directa de uno o pocos documentos dentro de 42/43 puede completar el trabajo sin otra sesión de infraestructura.

En el `main` revisado, la selección científica al 12/sep/2026 devolvió **52 necesidades activas y cero elegidas**. Es el estado de esa proyección antes de las nuevas entradas y de la conciliación de 40; no demuestra que no exista material útil. La selección de descargas no quedó verificada en este entorno porque faltó `jsonschema`; debe recalcularse en CAJA con sus dependencias habituales.

Si queremos usar el cron para los faltantes concretos:

1. El dueño acredita la ausencia física o la nueva fuente y registra identidad, URL, ruta, necesidad y contrato aplicables con el escritor canónico. No cuenta un enlace como bytes adquiridos.
2. En CAJA, comprobar qué seleccionaría cada vía:

   ```bash
   python3 tools/adq_doctor.py --selecciona --maximo 5 --json
   python3 tools/adq_investigacion.py --selecciona --maximo 3
   ```

3. Activar manualmente la tarea existente `\ModeladoMexicano\AdquiereCron` sólo cuando haya objetos pertinentes elegibles y no se estén descargando por otra sesión. Revisar el recibo y los bytes, no sólo el estado de la tarea.

No cambiar el scheduler, sus límites ni los selectores para forzar este lote. Una fuente nueva concreta se registra por su vía; no adelantar en bloque las esperas de NC-0122/NC-0126/NC-0164 ni omitir restricciones de `SIN-FETCH`. 40 integra el estado científico; las sesiones 41/42/43 completan sus adquisiciones y cálculos propios.

## Archivos que entregar

- `41-GEN2-BANXICO-PRODUCTO-ATRASO-Y-COSTO.md` → una sesión nueva.
- `42-GEN2-N35-PREFERENCIAS-LABORALES-Y-FUENTES.md` → otra sesión nueva.
- `43-GEN2-SHED-BNPL-DANO-Y-UNIVERSOS.md` → tercera sesión si hay capacidad.

Cada archivo lleva su prompt de lanzamiento al final. Estas son tareas preparadas; los cálculos y las nuevas adquisiciones se ejecutarán en sus sesiones de CAJA.
