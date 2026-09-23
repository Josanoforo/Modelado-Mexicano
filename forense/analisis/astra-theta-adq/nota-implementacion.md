# Implementación vehicular: evidencia dirigida para ASTRA-2

22/sep/2026. Consumidor: `RES-0091 · tramite.mordida.con_registro`. Selección
consultada en `/home/pc0/mm-astra-theta-1` (rama `codex/astra-theta-1`, HEAD
`97bb1ee3`; `seleccion.md` SHA-256
`ac21d19fe724607806134f3be191af9f96e8aa20c309cc34e6454b2554753dde`).
Es la ruta prioritaria del ejecutor, todavía sin diseño congelable. La solicitud
local pide entidad×servicio×fecha para 2017–2025. El [calendario](calendario-digitalizacion-vehicular.tsv)
registra solo hechos que pudimos atribuir a fuente primaria; no asigna θ,
tratamiento ni grupo de control.

## Qué quedó acreditado

- **CDMX, anuncio frente a operación.** La Jefatura [anunció el 23/abr/2019](https://jefaturadegobierno.cdmx.gob.mx/comunicacion/nota/presentan-la-adip-y-la-semovi-la-digitalizacion-de-los-tramites-para-la-renovacion-de-licencia-tipo-y-tarjeta-de-circulacion)
  que la renovación de licencia A y refrendo de tarjeta estarían disponibles
  desde el 2/may. Es una fecha programada. El [anexo estadístico 2019–2020 de
  SEMOVI](https://semovi.cdmx.gob.mx/storage/app/media/anexo-estadistico-2do-informe-anual.pdf)
  documenta trámites digitales realizados durante agosto–diciembre de 2019:
  719 de licencia A y 23 936 de tarjeta. Esto prueba operación en ese periodo,
  pero no la fecha del primer trámite. La licencia requería recoger el plástico
  en un módulo, así que la promesa de digitalización completa no equivale a
  eliminación de todo contacto presencial.
- **CDMX, cambio de cobertura.** La [Gaceta del 16/jul/2020](https://data.consejeria.cdmx.gob.mx/portal_old/uploads/gacetas/30f6039d22b8e6011e5701aabfbdc25c.pdf)
  estableció el refrendo digital para vehículos, motocicletas y remolques de
  uso particular, con vigencia legal al día siguiente. La [comunicación de
  SEMOVI del mismo día](https://semovi.cdmx.gob.mx/comunicacion/nota/ti-tarjetas-de-circulacion)
  dice que antes el canal cubría solo autos privados de combustión. La
  [presentación de licencia digital de diciembre de 2020](https://www.semovi.cdmx.gob.mx/comunicacion/nota/conjunto-presenta-gobierno-de-la-ciudad-de-mexico-licencia-de-conducir-digital-tipo)
  anunció una modalidad adicional para licencia A: credencial digital cuando
  SEMOVI tuviera foto y datos completos; de lo contrario, constancia temporal
  y visita posterior. No debe confundirse con el canal web de renovación de
  2019.
- **Tabasco, adquisición frente a operación.** El [informe oficial de
  2022](https://publicacionperiodico.tabasco.gob.mx/media/adjuntos/documento/2022-11-23/3967/firmado_qr.pdf)
  registra compra de la plataforma el 1/jul/2022; eso no fecha atención al
  público. El [segundo informe trimestral de Finanzas de 2023](https://tabasco.gob.mx/sites/default/files/users/spftabasco/Informe-Ingresos-Egresos-2do-Trim2023_15ago23_0.pdf)
  fecha la implementación del **cobro** de renovación digital el 23/jun/2023
  y registra 1 197 renovaciones en ese trimestre. La [página estatal del
  servicio](https://tabasco.gob.mx/licencia-digital) limita la renovación por
  app a quien ya tiene licencia física, vigente o vencida, y pide CURP,
  teléfono y correo. El [informe de enero de 2024](https://tabasco.gob.mx/noticias/presentan-sspc-y-pec-avances-y-beneficios-de-app-licencias-e-infracciones-digitales)
  confirma operación posterior; sus cifras de descargas de app e infracciones
  no son renovaciones de licencia.
- **Discrepancia oficial de Tabasco.** Un [programa sectorial posterior](https://tabasco.gob.mx/sites/default/files/users/userspftabasco/19%C2%A0Seguridad%20y%20Proteccio%CC%81n%20Ciudadana.pdf)
  llama agosto de 2023 el inicio del proyecto. Finanzas ya reportó cobros y
  renovaciones desde junio. Conservamos ambas fechas con su significado y
  dejamos sin resolver qué etapa llama inicio el programa posterior. No se
  reemplazó junio por agosto ni se supuso una fecha diaria de cobertura total.

## Qué impide congelar el DiD propuesto

La evidencia permite identificar **dos entidades y dos servicios concretos**:
CDMX (licencia A y tarjeta) y Tabasco (renovación de licencia). El código `05`
de ENCIG agrupa más trámites vehiculares; no hay base para marcar como tratado
a todo `05` en esas entidades. No se encontró en el corpus ni en estas fuentes
un calendario comparable de operación, suspensiones, obligatoriedad y volumen
por servicio para las demás entidades, ni una regla de asignación de la
digitalización independiente de capacidad estatal. La etiqueta de tratamiento
y las cohortes de control siguen **NO-DEFINIBLES** con este insumo. El ejecutor
puede usar el calendario para descartar la codificación «entidad tratada desde
el anuncio para todo `05`» y solicitar las filas faltantes antes del freeze.

## Procedencia y acceso

Se buscaron los títulos/URL específicos en `data/manifiesto.yaml`, inventarios,
catálogo y reports, y los nombres de archivo en `/home/pc0/mm-corpus/raw` y
su espejo. No estaban registrados ni presentes. Las páginas oficiales se
consultaron por la vía web. La descarga directa de las fuentes falló con
`curl: (35) TLS ... unexpected eof` en sandbox y fuera de él; la Gaceta dio
además `curl: (60) unable to get local issuer certificate`; un intento con
`wget` a Tabasco terminó en `GnuTLS: The TLS connection was non-properly
terminated`. No se desactivó la validación TLS. La alternativa utilizable son
las URL primarias exactas en cada fila del TSV, más esta extracción acotada
con fuente. No hay bytes oficiales locales a los que asignar SHA-256 o bytes,
por lo que **no se agregó una entrada ficticia a `data/manifiesto.yaml`**.
Tampoco se localizó una licencia de redistribución específica para estas
páginas/informes gubernamentales; se enlazan y se parafrasean, sin rotularlas
como licencia abierta. Para preservarlas en el corpus, repetir la descarga
directa cuando el servidor TLS responda, leer términos aplicables y registrar
por ID cada archivo real mediante `tests/manifiesto.py --registra`.
