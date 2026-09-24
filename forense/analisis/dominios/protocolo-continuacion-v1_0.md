# ASTRA5-U0 · Protocolo de continuación del dictamen por afirmación

**Contexto.** La sesión Codex que ejecutaba este encargo se detuvo el 23/sep/2026 a las 22:27 (hora de CDMX) por `usage_limit_exceeded`, tras empujar `80e5af58` con 102 contratos cerrados (`mapa-parcial-v0_1.tsv`), 719 fichas de lectura y ninguna tabla canónica. El usuario pidió a Claude (Opus 5.5) retomarla y terminarla sobre la misma rama y el mismo 0-bis (`63dbb17d`), sin rehacer el recorrido. Este archivo fija cómo se completó el universo; lo que dice sobre cada afirmación está en `canon/mapa-dominios-v1_0.tsv`.

## 1 · Universo de unidades, por comando

| Tipo | Qué es | Conteo | Fuente |
|---|---|---:|---|
| G | hallazgos/secciones del índice de Codex | 474 | `afirmaciones-para-dictamen-v1_0.tsv` |
| P | pasajes con tier fuera de G (índice de 391) | 112 | `candidatas-v1_0.tsv` menos las líneas de G |
| T | líneas con marca de tier fuera de G y P, con un regex ampliado (tablas de evidencia por tier, casos, encabezados); puede traer falsos positivos | 111 | `unidades-tier-ampliado-v1_0.tsv` |
| F | fichas de lectura de Codex | 719 | `lectura-*.tsv` |
| INT | afirmaciones con tier halladas al leer íntegro cada archivo, fuera de las anteriores | según lote | `lotes/*-cobertura-v1_0.tsv` |

El regex de T es índice para leer, no censo: cada lote leyó el archivo completo. Toda unidad queda en `cobertura-unidades-v1_0.tsv` enlazada a una fila del mapa, a un contrato previo, o con una razón cerrada (`NO-AFIRMACION: …` o `DEDUP: …`).

## 2 · Ejecución por lote

Un lote por archivo del censo (37; `compass-4` se trata como complemento del forense de crédito popular y conserva su familia `CRPOP`). Cada lote lo redactó un agente ejecutor (Sonnet) con las instrucciones congeladas en `lotes/INSTRUCCIONES-LOTE-v1_0.md` (sha256 en su sidecar), y lo auditó el supervisor (Opus): validación mecánica, revisión de cada dictamen NO-MEDIBLE y MEDIBLE, correcciones y, cuando hizo falta, devolución al ejecutor con instrucciones precisas. Solo después se importó a `lotes/<clave>-filas-v1_0.tsv` con ids estables `ASTRA5-U0-<FAMILIA>-NNN` que continúan la numeración de Codex (los retirados `MER-001..003` no se reutilizan). Los registros crudos de búsqueda de cada lote (A.13) quedan en `lotes/busquedas/<clave>.log`.

Herramientas de consulta (en `herramientas/`): búsqueda en los nueve inventarios de reactivos con resolución de cada acierto a id y sha256 del manifiesto (dato y documento fuente del texto); búsqueda en el texto por página de los 349 PDF registrados (se excluyeron los reservados ENOE 2026, ENVIPE 2026 y ENCO); consulta del manifiesto por id y por alias, y de las corridas GEN2 por insumo. Ninguna abre microdato.

## 3 · Dictamen

Vocabulario cerrado del encargo, sobre el componente observable (conducta o estimando, unidad, universo, ola), nunca sobre el tier:

- **MEDIBLE-EN-CORPUS**: la pregunta o variable está en un instrumento cuyo dato tiene id en el manifiesto; se cita su texto literal con id, sha256 y hoja/fila o página; U0 no abre microdato. Para una afirmación documental, el propio documento registrado es el dato.
- **MEDIBLE-CON-ADQUISICIÓN**: el instrumento o documento está identificado con texto comprobado y falta registrar dato o documento; la fila dice `faltante: …` con la pieza exacta. En afirmaciones documentales basta comprobar la existencia e identidad del documento primario; el cotejo de la cifra queda como operación residual. Las métricas de instituciones financieras se dictaminan sobre la serie regulatoria oficial (CNBV, Banxico, CONDUSEF, BMV), no sobre calificadoras o prensa.
- **NO-MEDIBLE-POR-DISEÑO**: el diseño de los instrumentos recorridos no puede observar el componente (causalidad sin diseño identificador, constructo no preguntado, población no muestreada, proyección, contrafactual, contenido normativo). La razón dice el límite y la búsqueda explícita; «no se identificó instrumento tras este recorrido» no equivale a imposibilidad universal. Nunca por falta de un archivo.

Medibilidad, autorización de apertura y existencia de RESULT son tres ejes separados en `proyeccion-cobertura-v1_0.tsv`.

## 4 · Consumo de trabajo integrado después del corte de Codex

- #1094 (ASTRA5-U5) registró en `main` seis documentos que U0 había leído con sha físico (diseño ENADID 2023, reporte ENIGH 2024, diseño/boletín/presentación ENCIG 2025, decisión CED): `actualizaciones-contratos-v1_0.tsv` cambia esos contratos a EN-CORPUS con el mismo sha.
- #1098 (ASTRA5-U3) midió LAPOP México 2023 b18/b21 (`RESULT-LAPOP-PISOS-2023-POL001`), que corresponde exactamente al contrato POL-001.
- #1099 (ASTRA5-U2) selló RESULT ENDIREH 2006–2021 por ámbito; el agregado 70.1% sigue sin contraste directo.

## 5 · Ensamblado

`ensambla_mapa.py` construye el mapa canónico, la cobertura por unidad, la proyección por afirmación y por dominio, y la tabla report→dominio a partir de la base Codex, las actualizaciones explícitas, los lotes auditados, las fusiones entre archivos y la tabla de correspondencia exacta afirmación→RESULT. `--verifica` recalcula y compara byte a byte con lo publicado; la prueba `test_mapa_se_reproduce_byte_a_byte` lo exige.

## 6 · Cierre (24/sep/2026)

Segunda pasada documental en `lotes/segunda-pasada-v1_0.tsv`; `ensambla_mapa.py` deriva además `hoja-adquisicion-derivada-v1_0.tsv` (estado de hoja y existencia del documento por afirmación), que sucede a `hoja-adquisicion.md` como hoja completa. La pasada de acceso de la `ADENDA-1` no corrió (opción 2): las filas con existencia no comprobada están en `no-accesible-desde-sandbox-v1_0.tsv` y las rutas medidas en `receta-acceso-fuentes-2026-09-24.md`, para `GEN2-ASTRA5-U5-ADQUISICION-1`. Cierre en `ADR-260924-ASTRA5-U0-MAPA-DOMINIOS-63db-01` y `forense/notas/2026-09-24-ASTRA5-U0-MAPA-DOMINIOS-cierre.md`.
