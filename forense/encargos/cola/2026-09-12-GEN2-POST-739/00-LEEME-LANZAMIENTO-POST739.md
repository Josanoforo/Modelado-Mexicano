# Modelado Mexicano · Siguientes encargos después de #739

Preparado para Jonás el 12 de septiembre de 2026. Se revisó primero GitHub/main y después el transfer adjunto. Este paquete prepara trabajo para Codex CLI; no lo ejecuta ni modifica el repositorio.

## Estado comprobado

`main=015407b9a59359481285bf343ad561dfd7026e8b`, sin cambios posteriores respecto del transfer en esta revisión. [#739](https://github.com/Josanoforo/Modelado-Mexicano/pull/739), [#728](https://github.com/Josanoforo/Modelado-Mexicano/pull/728), [#738](https://github.com/Josanoforo/Modelado-Mexicano/pull/738) y [#740](https://github.com/Josanoforo/Modelado-Mexicano/pull/740) están fusionados.

Sólo aparece abierto [#727](https://github.com/Josanoforo/Modelado-Mexicano/pull/727): sus cambios son ocho archivos de censo, sin código ni mediciones. No bloquea estos encargos. No se auditó para recomendar su fusión.

Las únicas ramas remotas publicadas son `main` y `censo/2026-09-11`. No hay entrega publicada de 39 o NC-0165; una sesión local sin push sigue siendo posible. Si ya lanzaste 39, entrega su actualización a esa misma sesión y no abras otra.

## Qué falta realmente

#739 dejó operativo el camino descubrimiento → adquisición → suficiencia y protege los consumidores incompatibles. La siguiente prioridad es completar el significado de su demanda y ejecutar el trabajo disponible.

| Hallazgo en main | Consecuencia para el siguiente trabajo |
|---|---|
| 207 elementos, 16 adoptados y 191 preadopción | Son campos heterogéneos: motor, R, incertidumbre, supuestos y otros consumidores. No equivalen a 191 cálculos nuevos. |
| 144 etiquetas de preparación y 47 de decisión científica | La clasificación usa señales legacy; hay que cruzar decisiones, ofertas y sucesores antes de despachar o pedir firmas. |
| 45 descripciones mínimas contadas como contratos científicos incompletos | Incluyen obligaciones técnicas/documentales. Hay que separar su naturaleza, sin borrar pendientes. |
| Ofertas enlazadas buscando `RES-xxxx` en su nombre | Una nomenclatura distinta puede dejar una oferta fuera de la vista. El enlace debe acreditarse por identidad y compatibilidad. |
| RES-0028 apunta sólo a NC-0165 en la proyección | Hay una reserva específica NC-0085 que debe conservar su lugar y su decisión de adopción. |

Evidencia: [`tools/adq_investigacion.py`](https://github.com/Josanoforo/Modelado-Mexicano/blob/015407b9a59359481285bf343ad561dfd7026e8b/tools/adq_investigacion.py), [`data/adq-demanda-activa-v1_0.json`](https://github.com/Josanoforo/Modelado-Mexicano/blob/015407b9a59359481285bf343ad561dfd7026e8b/data/adq-demanda-activa-v1_0.json), [`forense/no-corrido.tsv`](https://github.com/Josanoforo/Modelado-Mexicano/blob/015407b9a59359481285bf343ad561dfd7026e8b/forense/no-corrido.tsv). Son defectos de interpretación/ruteo que justifican 40; no una razón para reabrir la auditoría del cron.

## Lanzamiento

| Prioridad | Archivo | Producto exigido | Dependencia |
|---|---|---|---|
| Principal | `forense/encargos/2026-09-12-GEN2-DEMANDA-CONCILIADA-Y-EJECUCION-NC0165.md` (despachado; copia de cola retirada) | Contratos y etapas conciliados, decisiones existentes reconocidas, ofertas enlazadas y lote disponible llevado a consumo/ejecución real. | Parte de main con #739. No espera a 39. |
| En paralelo | `39-GEN2-REACTIVOS-PENDIENTES-Y-BUSQUEDA-UTIL.md` | Texto documental residual recuperado, índice/buscador operativo y búsquedas antes/después sobre documentos reales. | Continúa #737, actualizado a #739 fusionado. No espera a 40. |

Si sólo hay una sesión libre, lanza 40 primero. Si hay dos, lanza ambos. Cada archivo incluye su prompt de lanzamiento y puede entregarse por separado. La autoridad se activa al despacharlo.

No existe un orden obligatorio de fusión. Si terminan juntos, conviene **39 → 40**, para que 40 consuma el índice final al integrar. Si 40 termina antes, puede entregar y fusionarse con el índice vigente, dejando identificado ese corte. Ambos preservan registros compartidos por clave; Jonás conserva todas las fusiones.

39 posee extracción, overlay, buscador y residual de NC-0100/NC-0136. 40 posee conciliación de NC-0165, contratos, enlace con ofertas y ruteo. Ninguno crea otra automatización. El avance de 40 no depende de inflar búsquedas: sólo manda trabajo cuya necesidad y elegibilidad estén acreditadas.

## Decisiones y accesos que permanecen separados

No hace falta resolver una firma nueva para iniciar estos dos encargos. Al ejecutar 40 pueden aparecer elecciones concretas todavía abiertas; se preparan con evidencia mientras avanza lo independiente.

- **FP-373/F5:** #728 preparó fuentes y ejecución; la firma de modelo/cliente/costo y llamadas sigue pendiente. No se vuelve a encargar preparación ni se lanza el experimento por inferencia.
- **FP-371 y FP-372:** reservas inferenciales DIN/S6; no anulan el uso descriptivo ya permitido.
- **FP-374:** transferencia reservada; no habilitada por mejorar demanda o documentación.
- **Accesos personales:** reutilizar los expedientes pertinentes y distinguir listo, enviado y obtenido; estos encargos no envían solicitudes.

Estado respaldado por [`firmas-pendientes.tsv`](https://github.com/Josanoforo/Modelado-Mexicano/blob/015407b9a59359481285bf343ad561dfd7026e8b/forense/firmas-pendientes.tsv).

## Resultado esperado de la tanda

Saber qué consumidor puede avanzar y hacerlo avanzar; reconocer lo ya resuelto; alimentar investigación con preguntas verificables; presentar sólo las decisiones que sigan siendo humanas. El éxito se mide por consumidores, mediciones y bloqueos resueltos, no por más archivos descargados o más filas de control.
