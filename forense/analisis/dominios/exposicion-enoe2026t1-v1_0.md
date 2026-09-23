# Exposición documental U0: ENOE 2026T1

**Estado: exposición constatada; uso suspendido; decisión de mesa pendiente.** Este registro conserva la procedencia sin reabrir el documento ni presentar los contratos derivados como preparación ciega.

## Regla aplicable y búsqueda de autorización

El encargo archivado `forense/encargos/2026-09-23-ASTRA5-U0-MAPA-DOMINIOS.md`, sección «Perímetro y aceptación», establece: «Reports/canon científico/manifiesto solo lectura». En «Mandato de ejecución y cierre común» dispone: «La última ola ENOE se conserva reservada según el mandato específico» y «No incluyas tabulados/comunicados reservados en la preparación». También aclara: «El merge futuro no levanta hoy una reserva de datos explícita».

El cierre específico `forense/notas/2026-09-23-ASTRA5-U1-TRABAJO-ENOE-cierre.md`, sección «NO-CORRIDO / RESERVAS», identifica 2026T1 como última ola reservada y exige «acto que levante reserva y preregistre nuevo CALC». `canon/L0/ADR-260923-ASTRA5-U1-TRABAJO-ENOE-e422-01.md` mantiene esa reserva en ambos ids. Se revisaron esas fuentes, el encargo archivado y los commits locales pertinentes; **no se encontró autorización posterior aplicable al boletín 301/26**. La disponibilidad pública y los Términos de Libre Uso de INEGI no sustituyen el acto interno requerido.

## Rastro de exposición

| Elemento | Registro |
|---|---|
| Documento | INEGI, boletín 301/26, ENOE primer trimestre 2026, archivo de origen `enoe2026_05.pdf`; copia física ya descargada en `/home/pc0/mm-corpus/raw/enoe2026_t1_comunicado.pdf` y copia temporal `/tmp/ASTRA5-ENOE2026T1-comunicado.pdf`. No se volvió a abrir para esta corrección. |
| SHA256 físico verificado en la operación anterior | `edde714757e5967d0a312aa8f53afb8d80f6671adf70d9af0bc2f32e44e4ace0`; tamaño 528030 bytes. |
| Primer commit que expuso la lectura | `7c6e184282a65981d5b507dde419b16fa3fe834d`, 2026-09-23 16:45:01 −06:00, «Dictamina agregados de mérito ENOE y ENIGH», rama de PR #1079. Continuación `4270328c3c154c3f683d48d0397fa6138bf24d44`, 16:53:13 −06:00. |
| Variables ya conocidas por U0 | TIL1 2026T1 54.8%; comparador 2025T1 54.3%; personas ocupadas informales 32.6 millones; variación anual +583 mil. Son valores expuestos, **no insumo autorizado para nuevo diseño ni RESULT**. |
| Contratos derivados | `ASTRA5-U0-MER-001..003` en versiones anteriores de `corte-merito-v1_0.py/.tsv` y `mapa-parcial-v0_1.tsv`; `LECTURA-f8ef1dd3-03` en `lectura-merito-v1_0.tsv`; cruce `MER-ENOE2026-TIL1` en `deduplicacion-v1_0.tsv`; fila de `hoja-adquisicion.md`; síntesis y conteo de `estado-u0-2026-09-23.md`; prueba de conteo y cuerpo anterior de PR #1079. |
| Manifiesto | U0 añadió el id propuesto `enoe2026_t1_comunicado_pdf` en los commits citados; se revierte esa alta en esta rama. El diff y el historial de Git conservan su procedencia. |
| Microdatos | U0 no descargó ni abrió microdatos de 2026T1. `RESULT-ENOE-PISOS-TABLA` de #1087 corresponde a 2024T3; no resuelve esta exposición. |

## Alcance propuesto a mesa

Quedan fuera del corte activo los tres MER-001..003, sus citas del boletín y cualquier proyección que los cuente como medibles. La fila de lectura y la hoja quedan como señal de exposición, sin instrucción ni cifras para U1. La copia física se conserva para trazabilidad, sin nueva apertura, registro como insumo activo ni traslado de cifras a la sesión reservada. Mesa debe decidir si mantiene cuarentena, dispone el documento en carril restringido o emite un acto explícito que habilite un uso posterior con alcance preciso. Ningún paso futuro podrá llamarse preparación ciega respecto de las variables ya conocidas por U0.

La exposición comprobada es de esta pieza y de sus derivados identificados. No se extiende automáticamente a ENOE 2024T3, ENIGH 2024, ENCIG 2025 u otras familias con procedencia independiente. Las afirmaciones ya impresas en los reports de solo lectura permanecen en el corpus; su dictamen 2026T1 queda reservado.

## Altas indebidas de manifiesto y traslado documental

El mismo encargo hace `data/manifiesto.yaml` de solo lectura para U0. No se encontró autorización posterior para cinco altas hechas en `7c6e1842`/`4270328c`; esta corrección las retira de la rama sin borrar los commits ni las copias físicas. El boletín ENOE queda solo en el registro de exposición. Las otras cuatro piezas pasan como **solicitudes, no ids activos**, a `hoja-adquisicion.md` para ASTRA5-MESA-DOCUMENTAL: ENIGH 2024 reporte SHA `6b091e2d640b6682ca568203637d2a327fbcae950ba7ef66c441c5970568903d`; ENCIG 2025 diseño SHA `de74a89623696e54e2d409a5cb5ae2b41dcd54a73c9deef1102b5793d875175e`, boletín SHA `6515cb698a8a7f0821a225827ac2402d06cd6405cabf76208f0d6c529b29eaa4` y presentación SHA `476cf06ee8cb18727f2326c0d80e5f113ca3554a0851f89f3414ab1a03113548`. Cada uno conserva URL, archivo, hash y condición en la hoja. U0 no presume registro en rama ni en `main`.
