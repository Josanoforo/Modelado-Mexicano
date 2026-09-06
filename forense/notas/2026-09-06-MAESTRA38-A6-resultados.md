# ACTO MAESTRA38-A6 · COMMIT-2 · Resultados

**Universo (A.10).** `origin/main` = `ef9ba36`, 6/sep/2026, caja UBUNTU
(`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable`), red real
verificada (`https://www.inegi.org.mx/` → `200`, 153 615 B), corpus
compartido montado (`data/raw` → `/home/pc0/mm-corpus/raw`, 393 entradas al
arrancar). Toda petición de red fuera del sandbox de bash: **dentro** del
sandbox `inegi.org.mx` da `000`, **fuera** da `200` — medido, no supuesto.

Este acto **no mide ninguna regla**. Contador de medición: **cero**.

---

## §1 · Tabla de resultados — los 25 objetos

| # | objeto | estado antes | rutas | estado después | bytes | dónde |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `SICEE` | NO-OBTENIDO(1) | 4 | **OBTENIDO** | 942 828 | `A6_SICEE_INE_ELECCIONES/` (4 ids) |
| 2 | `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` | NO-OBTENIDO(31) | 4 | **OBTENIDO** | 45 145 330 | `A6_MMAD_PROTESTA_MEXICO/` (2 ids) |
| 3 | `CANAL_DE_ADQUISICION_REFERIDOS_FINTECH` | NO-ENCONTRADO | 4 | NO-ENCONTRADO *(universo declarado, 653 archivos)* | — | — |
| 4 | `SFT-06_ACUERDO_CUIDADO_ENTRE_HERMANOS…` | NO-ENCONTRADO | 4 | NO-ENCONTRADO *(universo declarado, 3 113 archivos)* | — | — |
| 5 | `OECD` | NO-ACCESIBLE | 4 | **OBTENIDO-PARCIAL** | 14 717 343 | `A6_OECD_GOV_TRUST_INTEGRIDAD/` (2 ids) |
| 6 | `PI` (CNBV Portafolio) | NO-ACCESIBLE | 4 | **NO-OBTENIDO-POR-ESTE-AGENTE(4 rutas)** *(etiqueta corregida)* | — | receta 3 |
| 7 | `DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO` | NO-ACCESIBLE | 4 | **OBTENIDO-PARCIAL** | *(ver 14)* | `A6_CONDUSEF_DATOS_ABIERTOS/` |
| 8 | `EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6` | OBTENIDO-PARCIAL | 4 | OBTENIDO-PARCIAL *(sus 2 huecos ya tienen fila)* | — | — |
| 9 | `PRICE_AND_INFORMATION_TYPE…` | OBTENIDO-PARCIAL | 4 | OBTENIDO-PARCIAL | — | SSRN 403 (Cloudflare) |
| 10 | `ENAFIN` | OBTENIDO-PARCIAL | 4 | OBTENIDO-PARCIAL | — | WB exige cuenta |
| 11 | `ENJUVE` | OBTENIDO-PARCIAL | 4 | OBTENIDO-PARCIAL | — | 3 hosts muertos |
| 12 | `REUTERS_DNR` | OBTENIDO-PARCIAL | 3 | OBTENIDO-PARCIAL | — | exige solicitud |
| 13 | `CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO` | PENDIENTE-DE-MESA | 4 | PENDIENTE-DE-MESA *(URL exacta localizada)* | — | receta 3 |
| 14 | `ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF` | PENDIENTE-DE-MESA | 4 | **OBTENIDO-PARCIAL** | 15 759 195 | `A6_CONDUSEF_DATOS_ABIERTOS/` (26 ids) |
| 15 | `IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016` | PENDIENTE-DE-MESA | 2 | PENDIENTE-DE-MESA | — | `EXIGE-CREDENCIAL` 4ª vez |
| 16 | `salud.adherencia.desabasto_vs_cuidadora` | PENDIENTE `SIN-FETCH` | 2 | PENDIENTE — **`SIN-FETCH` retirado** | — | 2 URLs, 2 alcanzables |
| 17 | `cooperacion.comite.monitoreo_sancion_visible` | PENDIENTE `SIN-FETCH` | 1 | PENDIENTE — **`SIN-FETCH` retirado** | — | 1 URL, alcanzable |
| 18 | `cooperacion.faena.sancion_social_pueblo_mestizo` | PENDIENTE `SIN-FETCH` | 1 | PENDIENTE — **`SIN-FETCH` retirado** | — | 1 URL, alcanzable |
| 19 | `HOMESCAN_CONSUMER_PANEL_SERVICES` | NO-ADQUIRIDA-POR-COSTO | 1 sonda | sin cambio · **PARALELA-NINGUNA** | — | 8 archivos |
| 20 | `PANEL_DE_COMPRA_DE_HOGARES` | NO-ADQUIRIDA-POR-COSTO | 1 sonda | sin cambio · **PARALELA-NINGUNA** | — | 15 archivos |
| 21 | `REGISTRO_DE_TANDAS_Y_REPUTACION` | NO-ADQUIRIDA-POR-COSTO | 1 sonda | sin cambio · **PARALELA-NINGUNA** | — | 11 archivos |
| 22 | `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES` | NO-ADQUIRIDA-POR-COSTO | 1 sonda | sin cambio · **PARALELA-NINGUNA** | — | 2 803 archivos |
| 23 | `MERCER_GPTW_CLIMA_DESEMPENO` | NO-ADQUIRIDA-POR-COSTO | 1 sonda | sin cambio · **PARALELA-NINGUNA** | — | 19 archivos |
| 24 | `RUPC` | *(sin fila)* | 4 | **alta** · NO-OBTENIDO(4 rutas) | — | receta 1 |
| 25 | `DD_COMPRANET_DICCIONARIOS_DE_DATOS` | *(sin fila)* | 4 | **alta** · NO-OBTENIDO(4 rutas) | — | receta 2 |

**Total depositado: 34 payloads, 76 564 696 bytes**, todos en el corpus
compartido y registrados por las tres capas.

---

## §2 · Por qué cayeron los que cayeron — cuatro mecanismos, no cuatro suertes

Los cierres previos no fallaron por falta de insistencia. Fallaron porque
**la sonda midió otra cosa que la que creía medir**. Los cuatro casos:

### 2.1 · `SICEE` — la API vivía en otro host

`sicee.ine.mx/api/` devuelve el mismo shell Angular que la raíz, y eso se
había leído como «no hay API REST bajo esa ruta». El bundle dice otra cosa:

```
$ command grep -oE '.{60}sicee-api\.ine\.mx.{40}' main-6CQJB35E.js
… d1={production:!0,apiUrl:"https://sicee-api.ine.mx/api/v1/",version:2} …
$ command grep -oE 'SiceenUrl\+"[^"]+"' main-6CQJB35E.js | sort -u | wc -l
124
```

**124 rutas POST públicas, host distinto, sin cuenta ni cookie.** Y el
catálogo desmiente de paso la premisa que bloqueó a `MAESTRA34-L1` P4
(«sistema oficial declarado sin cobertura pre-2015»):

```
getEleccionesFederalesDIPMR: 12 filas; años: [1991,1994,1997,2000,2003,
  2006,2009,2012,2015,2018,2021,2024]
```

Cosechados 94 registros nacionales y 2 468 por entidad, 8 cargos, 1991-2024.

### 2.2 · `PI` / CNBV — la barrera era TLS, no acceso

```
$ curl https://www.cnbv.gob.mx/
curl: (60) SSL certificate … unable to get local issuer certificate (20)
$ echo | openssl s_client -connect www.cnbv.gob.mx:443 … | grep " s:"
 0 s:… CN=*.cnbv.gob.mx          ← sólo la hoja; no manda el intermedio
```

El servidor omite `GlobalSign RSA OV SSL CA 2018`. `curl` aborta **antes de
hablar HTTP**; los navegadores lo salvan solos por AIA. Con el intermedio
bajado de su propio AIA, `portafolioinfo.cnbv.gob.mx` responde `200` con
139 844 B y es navegable. El cierre previo («dashboard JS, no renderiza vía
fetch») describía un fallo de cadena, no un muro.

**Regla nueva que este acto propone, por analogía con las tres de A4:** *un
fallo de TLS no es evidencia sobre el acceso.* `curl 60` es una cadena rota
del servidor, no una barrera de credencial. Aplicó tres veces hoy: CNBV,
CONDUSEF (`webapps`, GeoTrust) y Kantar (DigiCert).

### 2.3 · `datos.gob.mx` — la base de la API había cambiado

```
$ curl ".../busca/api/3/action/package_search?q=condusef"   → 404, 14 347 B
$ curl ".../api/3/action/package_search?q=condusef"         → 200, 70 578 B
```

El prefijo `/busca/` está muerto. Actos previos lo usaron y leyeron el `404`
como «no hay datasets». Hay **15 paquetes CONDUSEF con 29 CSV públicos**,
entre ellos los registros de usuarios de seguro de vida y automóvil, el
índice de reclamaciones por institución, las cláusulas abusivas y el
registro de despachos de cobranza — este último justo el lado consumidor que
`N34` pedía.

### 2.4 · `BASE_DE_EVENTOS_DE_PROTESTA` — 31 intentos contra un solo depósito

Los 31 intentos fueron **contra `laoms.org`**, que sigue sin publicar el
archivo. La regla del encargo («N ≥ 4 rutas distintas, no N intentos de la
misma») es exactamente lo que faltaba: MMAD en Harvard Dataverse sirve el
dato por API pública, sin cuenta.

```
$ awk -F',' 'NR>1 && $2=="Mexico"' mmALL_073120_csv.csv | wc -l
153
$ awk -F',' 'NR>1 && $2=="Narnia"' mmALL_073120_csv.csv | wc -l   ← control negativo
0
```

153 eventos, 1990-2020, a nivel evento. A.7 doble descarga curl+wget,
`sha256` idéntico.

---

## §3 · Controles de soft-404 que este acto deja medidos

Un `200` no es éxito. Dos controles nuevos, para que nadie los vuelva a derivar:

| host / ruta | ruta inexistente devuelve | tamaño |
| --- | --- | --- |
| `www.inegi.org.mx/programas/<inexistente>/2020/` | `200 text/html` | **13 370 B** |
| `www.inegi.org.mx/contenidos/…/<inexistente>.pdf` | `200 text/html` | **2 263 B** |
| `www.inegi.org.mx/programas/encrige/2020/` (real) | `200 text/html` | 2 855 B |

El 2 263 B confirma la firma que `/adquiere` ya documentaba. El 13 370 B es
**nuevo**: la cifra de 2 263 B que circulaba no aplica a `/programas/`.

---

## §4 · Contra las premisas del encargo — lo que no se reprodujo

Tres, y las tres se declaran en vez de heredarse:

1. **«1 294 archivos examinados»** (P0). No se reproduce: son **2 788** bajo
   `forense/` + `data/` con `command find`. Los **43 archivos** sí se
   reproducen exactos, y la conclusión de P0 depende de esos, no del
   denominador.
2. **Clase A6 «6 etiquetas caducas»**. Los seis objetos que el encargo nombra
   (`INE`, `FINTECH_LENDING…`, UNAM, ECOPRED, Cultura Constitucional, CNGMD)
   ya están `OBTENIDO` en `estado_A4A5`. `SIN-FETCH` sobrevive sólo en la
   columna `nota`, que es historia fechada. **Etiquetas caducas corregidas: 0**
   — no había ninguna que corregir. La clase se reasignó a las 3 filas
   `PENDIENTE` que sí llevaban `SIN-FETCH` real, y las tres se resolvieron.
3. **Clase C «28 relaciones»**. Son **29**, verificado sobre
   `data/curacion-registro/relaciones.tsv`. Desglose real: ENFIH 7 ·
   ENSAFI 6 · ENBIARE 3 · ENASIC 3 · CSES 2 · MMAD 2 (bajo dos nombres
   distintos) · ISSP 1 · MICROCREDIT ×2 · ECEPIE 1 ·
   `DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO` 1 ·
   `CANAL_DE_ADQUISICION_REFERIDOS_FINTECH` 1. La lista queda derivada aquí
   para que el `LOTE-CRUCE` (pieza `N16-bis`) no la vuelva a derivar.

---

## §5 · `VENCIDO EN ALCANCE` — cierres previos que este acto supera

A.10, corolario 1: se marca, no se edita. Los originales quedan verbatim.

| cierre previo | dónde | por qué queda vencido en alcance |
| --- | --- | --- |
| `SICEE` → `NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)`, «SPA sin API pública» | `forense/notas/2026-09-03-MAESTRA37-A2-revision-cola.md` §2.23 | la API existe en `sicee-api.ine.mx`; universo de aquel cierre = `sicee.ine.mx` solamente |
| `MAESTRA34-L1` P4: «sistema oficial declarado sin cobertura pre-2015» | `forense/notas/2026-09-01-MAESTRA34-L1-MORDIDA-SERIE-cierre.md:177` | el catálogo SICEE trae DIP_MR desde **1991** |
| `PI`: «portal es dashboard JS, no renderiza vía fetch» | nota de la fila `PI` | era `curl 60` (cadena TLS), no render |
| `BASE_DE_EVENTOS_DE_PROTESTA` → 31 intentos | `forense/notas/2026-09-02-PAQUETE-RECETAS-2026-09-02.md:31` | los 31 fueron un solo depósito; MMAD lo sirve |
| `OECD` → `NO-ACCESIBLE` | `forense/notas/2026-09-03-MAESTRA37-A2-revision-cola.md` §2.7 | correcto para el PUM, demasiado ancho para los indicadores |

---

## §6 · Contador del acto

- filas negativas de la cola: **23 → 23** *(composición distinta: −2 cerradas, +2 altas de P0)*
- **objetos OBTENIDO desde un rótulo negativo: 2** (`SICEE`, `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO`)
- objetos que subieron a `OBTENIDO-PARCIAL` desde `NO-ACCESIBLE`/`PENDIENTE-DE-MESA`: **3**
- **etiquetas corregidas: 3** — `OECD` y `DENUNCIA…` (`NO-ACCESIBLE` → `OBTENIDO-PARCIAL`) y `PI` (`NO-ACCESIBLE` → `NO-OBTENIDO-POR-ESTE-AGENTE`, porque D5 no aplicaba). **Etiquetas caducas de la clase A6 del encargo: 0**, ya estaban saldadas.
- `SIN-FETCH` retirados: **3** (las 3 filas `PENDIENTE`, re-sondeadas desde CAJA)
- **payloads: +34** (76 564 696 B), manifiesto **1 533 → 1 567**
- payloads deduplicados por A.8 (ya estaban en corpus bajo otro id): **4**
- notas históricas sin fila en cola: **2** (`RUPC`, `DD_*`), ambas dadas de alta
- notas históricas con etiqueta vieja ya OBTENIDA: **14**, una línea cada una en `hallazgos.md`
- rutas con salida cruda pegada: **≥ 4 por objeto negativo**, más controles positivos y negativos
- recetas nuevas: **5** (`PAQUETE-RECETAS-11`)
- **medición: cero** (adquisición)
