# ACTO MAESTRA38-A6 · COMMIT-1 · La lista congelada

**Universo (A.10).** `origin/main` = `ef9ba36`, 6/sep/2026, worktree
`acto/maestra38-a6-resondeo-negativos`. Derivada de
`data/curacion-registro/cola-adquisicion-registro.tsv` (132 filas de datos)
por el comando que el encargo fija, más las 2 altas de P0.

```
$ awk -F'\t' 'NR>1 && $5!~/^OBTENIDO$|CERRADA|SUPERADA/' \
    data/curacion-registro/cola-adquisicion-registro.tsv | wc -l
23
```

**23 + 2 (P0) = 25 objetos.**

---

## §0 · Declaración de contaminación de orden — lo que ya se sondeó ANTES de congelar

El encargo ordena P0 → COMMIT-1 → P2. **Este acto rompió ese orden en tres
objetos** y lo declara aquí en vez de esconderlo, porque un COMMIT-1 que
finge no saber lo que ya midió no congela nada.

Entre P0 y este commit se corrieron sondas de red sobre:

| objeto | qué se supo ya | efecto sobre este COMMIT-1 |
| --- | --- | --- |
| `SICEE` | el bundle Angular declara `apiUrl:"https://sicee-api.ine.mx/api/v1/"` (host distinto del sondeado antes); la API responde `200 application/json` sin cuenta; el catálogo cubre **1991–2024** | su criterio de éxito se escribe SABIENDO que baja. No se le puede acreditar ceguera |
| `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` | MMAD en Harvard Dataverse expone 3 archivos por API pública; el CSV trae **153 filas de México, 1990–2020** | ídem |
| `PI` (CNBV) | `curl 60` (cadena TLS incompleta: el host no manda el intermedio GlobalSign), NO barrera de acceso; con el intermedio, `portafolioinfo.cnbv.gob.mx` sirve `200`/139 844 B | ídem |

Los **22 objetos restantes** se congelan sin haber corrido una sola sonda
sobre ellos en esta sesión, y para ellos la frase de abajo rige entera.

**Por qué se declara y no se corrige.** ADR-46: la unidad de contaminación
es la sesión. Reescribir el orden ya no lo restaura; lo único que queda es
decir con exactitud qué se supo antes de cada línea. Este acto **no mide
ninguna regla** (contador declarado: medición cero), así que la
contaminación no alcanza ningún falsador del Hito D — alcanza sólo la
credibilidad de tres criterios de éxito, y eso es lo que queda dicho.

---

## §1 · Regla de cierre — manda sobre todo lo demás

Ningún objeto vuelve a un rótulo negativo sin **≥ 4 rutas distintas** con
comando y salida cruda pegados:

- **(i)** URL directa
- **(ii)** API o descarga masiva
- **(iii)** formato alterno o espejo institucional
- **(iv)** espejo académico / Wayback / datos.gob.mx

más la receta manual ≤ 1 min cuando la última barrera sea cuenta o sesión.
Cuatro intentos de la misma ruta **no** son cuatro rutas.

**Tres hallazgos por ruta, nunca colapsados** (A.13, con bytes y
`Content-Type` en cada uno):

- **RED** — `000`, timeout, `curl 6/7/35/60`
- **SERVIDOR** — 4xx/5xx con cuerpo
- **VACÍO** — `200` sin contenido útil (shell SPA, nginx default, `[]`)

Y las tres lecciones que A4 midió, que aquí son regla:
una raíz de host que responde vacío **no es evidencia sobre sus rutas** ·
un 403 de directorio **no es evidencia sobre sus archivos** ·
un «mantenimiento» de API **no es evidencia sobre la URL por convención**.

A esas tres, este acto añade una cuarta ya medida en §0:
**un fallo de TLS no es evidencia sobre el acceso** — `curl 60` es una
cadena rota del servidor, no una barrera de credencial.

Vocabulario: A.4 (`EXISTE-SATISFACE` · `EXISTE-NO-SATISFACE` ·
`NO-ENCONTRADO` · `NO-ACCESIBLE`) + `D5` tal como el encargo lo gloso:
**`NO-ACCESIBLE` = pago, afiliación o ley.** (Nota: no se localizó una
definición canónica de `D5` con ese contenido en el árbol —
`command grep -rn "D5" --include=*.md .` devuelve 19 líneas, todas del
veredicto `D5 — INESTABLE` del LCA o de la tabla D5 de INFRA, ninguna de
vocabulario de acceso. Se usa la glosa del encargo, declarada como tal.)

---

## §2 · Los 25 objetos, con ruta y criterio de éxito

### Clase A1 · `NO-OBTENIDO-POR-ESTE-AGENTE` (2)

| # | objeto | estado hoy | pregunta que responde | rutas específicas | criterio de éxito |
| --- | --- | --- | --- | --- | --- |
| 1 | `SICEE` | NO-OBTENIDO(1 intento) | N25→`R7.1`, N26→`R7.3` | receta de navegador de `2026-09-01-MAESTRA34-L1-MORDIDA-SERIE-cierre.md` l.183-198 → curl con cookie jar; bundle Angular → API real; `datos.ine.mx`/cómputos como espejo | payload con participación y/o resultados por unidad geográfica, ≥1 año, verificable; `EXISTE-SATISFACE` sólo si trae la unidad que N25/N26 piden |
| 2 | `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` | NO-OBTENIDO(31 intentos) | N27→`R7.4` | MMAD (`massmobilization.github.io`), ACLED (registro gratuito = permitido), GDELT (`api.gdeltproject.org`), Cline Center; **contar cuántas rutas distintas fueron los 31 intentos**, pegando la nota origen | evento-nivel de protesta en México con fecha y ubicación; cada fuente con `EXISTE-SATISFACE`/`-NO-SATISFACE` contra la pregunta de la fila |

### Clase A2 · `NO-ENCONTRADO` — universo declarado (2)

| # | objeto | rutas específicas | criterio de éxito |
| --- | --- | --- | --- |
| 3 | `CANAL_DE_ADQUISICION_REFERIDOS_FINTECH` | A.4: universo declarado (qué, dónde, con qué términos); paralelas por constructo: ENIF 2021, ENSAFI 2023 (ambas en corpus) | o un dataset público con canal de adquisición por referido, o `NO-ENCONTRADO` con universo en una línea + veredicto `PARALELA-CUBRE/-PARCIAL/-NINGUNA` |
| 4 | `SFT-06_ACUERDO_CUIDADO_ENTRE_HERMANOS_SIN_CANDIDATA` | ídem; paralela por constructo: ENASIC 2022 (en corpus) | ídem |

### Clase A3 · `NO-ACCESIBLE` — **verificar la etiqueta** (3)

`D5`: `NO-ACCESIBLE` = pago, afiliación o ley. Si baja sin ninguna de las
tres, **la etiqueta estaba mal y se dice.**

| # | objeto | rutas específicas | criterio de éxito |
| --- | --- | --- | --- |
| 5 | `OECD` | OECD Data Explorer y su API SDMX (`sdmx.oecd.org/public/rest/`) son públicos | si baja microdato o serie del Trust Survey sin cuenta → etiqueta mal, se corrige a `OBTENIDO`/`OBTENIDO-PARCIAL`; si sólo baja estructura → se dice exactamente eso |
| 6 | `PI` | leer primero qué es (la fila lo dice: Portafolio de Información, CNBV, N19), luego rutas | ídem |
| 7 | `DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO` | CONDUSEF / ENVIPE como paralelas | el cruce a nivel registro, o `PARALELA-*` con la necesidad que la fila cita |

### Clase A4 · `OBTENIDO-PARCIAL` — qué falta exactamente (5)

| # | objeto | qué falta (según la fila) | rutas específicas |
| --- | --- | --- | --- |
| 8 | `EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6` | persona-con-id + sanción | CompraNet 951 MB y PDN bulk **ya en corpus** → probablemente completable hoy sin red nueva |
| 9 | `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` | el objeto exacto (Bauchet, SSRN 2474620) | WB / J-PAL dataverse, RePEc, NBER, IPA |
| 10 | `ENAFIN` | microdato firma-a-firma | hermana WB Enterprise Surveys (catálogo 6453) |
| 11 | `ENJUVE` | microdato 2000/2005/2010 | IMJUVE, `datos.gob.mx`, Wayback de `imjuventud.gob.mx` |
| 12 | `REUTERS_DNR` | microdato individual | depósitos académicos; los 9 topline ya obtenidos no cambian |

Criterio de éxito común a la clase: **o baja lo que falta, o se dice qué
falta exactamente y si eso ya está por otra vía.** No se sube el estado por
haber bajado material adyacente.

### Clase A5 · `PENDIENTE-DE-MESA` (3)

| # | objeto | rutas específicas | criterio de éxito |
| --- | --- | --- | --- |
| 13 | `CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO` | Portafolio de Información CNBV: público, sin cuenta | serie IMOR desagregada por tipo de cartera de consumo. **Si baja, sale de `PENDIENTE-DE-MESA` sin firma intermedia (decidido por el encargo)** |
| 14 | `ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF` | FD en INEGI por URL de convención; CONDUSEF en `datos.gob.mx` | ídem |
| 15 | `IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016` | **no nombrado por el encargo en A5** — se declara y se somete igual, porque está entre las 23 | `EXIGE-CREDENCIAL` ya confirmado 3 veces; se corren las 4 rutas y se reporta, sin forzar el estado (es decisión de mesa) |

### Clase A6 · `PENDIENTE` con `SIN-FETCH` en la nota (3)

**Corrección de premisa, declarada.** El encargo escribe la clase A6 como
«`INE` · `FINTECH_LENDING_TO_BORROWERS…` — abrir byte a byte. Y corregir las
6 etiquetas caducas». Medido en P0 §3: los seis objetos que nombra ya están
`OBTENIDO` en `estado_A4A5`; `SIN-FETCH` sobrevive sólo en la columna `nota`,
que es historia fechada. **La clase A6 del encargo no tiene objeto en el
árbol de hoy.** Lo que sí existe, y lleva `SIN-FETCH` de verdad, son las 3
filas `PENDIENTE`, que además están entre las 23. La clase se reasigna a
ellas y se dice.

| # | objeto | por qué `SIN-FETCH` | criterio de éxito |
| --- | --- | --- | --- |
| 16 | `salud.adherencia.desabasto_vs_cuidadora` | HEAD desde NUBE → `000` (proxy de egreso). **Esta caja no es la nube** | re-sondear desde CAJA: si responde, el `SIN-FETCH` era del entorno, no del host |
| 17 | `cooperacion.comite.monitoreo_sancion_visible` | ídem (`inegi.org.mx/rnm/.../977`) | ídem; el payload CNGMD ya está OBTENIDO — sólo se verifica la URL |
| 18 | `cooperacion.faena.sancion_social_pueblo_mestizo` | ídem, misma URL | ídem |

### Clase B · `NO-ADQUIRIDA-POR-COSTO` — **no se re-bajan** (5)

Una sonda por objeto (¿muestra pública, reporte abierto, dataset académico
derivado?) y paralelas. Resultado por objeto:
`PARALELA-CUBRE` / `-PARCIAL` / `-NINGUNA`, contra la necesidad que la fila cita.

| # | objeto | paralela declarada |
| --- | --- | --- |
| 19 | `HOMESCAN_CONSUMER_PANEL_SERVICES` (NielsenIQ) | ENIGH / ENCO (panel de compra) |
| 20 | `PANEL_DE_COMPRA_DE_HOGARES` (Kantar Worldpanel) | ENIGH / ENCO |
| 21 | `REGISTRO_DE_TANDAS_Y_REPUTACION` (Tanda+) | ENIF 2021 (tandas, en corpus) |
| 22 | `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` (Tanda+) | ENIF 2021 |
| 23 | `MERCER_GPTW_CLIMA_DESEMPENO` | módulos ENOE (clima laboral) |

### Clase D · altas de P0 — `SIN-FILA` (2)

| # | objeto | origen | criterio de éxito |
| --- | --- | --- | --- |
| 24 | `RUPC` | `forense/notas/2026-09-03-MAESTRA36-A2-P1-P3-compranet-llaves.md:96` | alta en la cola con `NO-OBTENIDO-POR-ESTE-AGENTE` heredado + 4 rutas |
| 25 | `DD_COMPRANET_DICCIONARIOS_DE_DATOS` | ídem `:258` | ídem |

### Clase C · las 28 relaciones `NO-ENCONTRADO` — **no se reabren aquí**

No es fallo de descarga: es contenido. Entran al `LOTE-CRUCE` como pieza
`N16-bis`. Este acto sólo pega la lista derivada, para que el cruce no la
vuelva a derivar.

---

## §3 · Lo que este acto NO hace

No mide ninguna regla · no reabre las 28 relaciones · no toca los tiers ·
no pide credenciales a nadie: donde la barrera es cuenta o solicitud,
entrega receta en `PAQUETE-RECETAS-11`.

---

**El primer resultado que produzca este procedimiento es el que se reporta**
— entero para los 22 objetos que ninguna sonda de esta sesión tocó antes de
esta línea, y con la salvedad nominal de §0 para `SICEE`,
`BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` y `PI`.
