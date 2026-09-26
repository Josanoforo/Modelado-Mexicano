# Lista cerrada P1 · consumo y gasto por segmento (ENIGH 2016–2022, ENGASTO 2012)

`ACTO GEN2-CONSUMO-Y-GASTO-PISOS-1`, 25/sep/2026, CAJA, rama `acto/gen2-consumo-y-gasto-pisos-1`,
0-bis `2d37b23b`. Encargo: `forense/encargos/2026-09-25-GEN2-CONSUMO-Y-GASTO-PISOS-1.md` (P1).
Congelada en el COMMIT-1, **antes** de leer un solo valor de microdato. Esta lista es parte de
las dos specs (`forense/prereg-caja/CONSUMO-ENIGH-PISOS-spec-v1_0.md`,
`forense/prereg-caja/CONSUMO-ENGASTO-PISOS-spec-v1_0.md`); después del COMMIT-1 no se cambia
(PARO d).

## 0 · Qué se leyó para escribirla (declaración ADR-46, nivel ESTRUCTURA)

- ENIGH 2016/2018/2020/2022 (`enigh{2016,2018,2020,2022}_nc_csv`): lista de miembros del ZIP,
  **primera línea** (encabezado) de `concentradohogar`, `hogares`, `gastoshogar`,
  `gastospersona`, `poblacion`; catálogos `lugar_comp`, `forma_pag`, `educa_jefe`, `tam_loc`,
  `gastoscontarjeta`, `gastos` (prefijos de clave), `producto` de erogaciones (claves Q);
  diccionarios de `concentradohogar`, `gastoshogar` y `hogares` (definición de `ali_fuera`,
  `comunica`, `pago_tarje`, `deudas`, `prestamos`, `gasto_mon`, `ing_cor`, `tarjeta`,
  `pagotarjet`, `celular`, `conex_inte`; notas de trimestralización de `gasto_tri`).
  **Ninguna fila de datos.** Tamaños de miembro (`ZipInfo.file_size`) para prever memoria.
- ENIGH 2024: nada. RESERVADA (`decisiones.tsv:192`), no es input.
- ENGASTO: `engasto12_fd.pdf` completo (`pdftotext -layout`, 8 411 líneas); metadatos `.dta`
  (`pyreadstat.read_dta(metadataonly=True)`: nombres, etiquetas de variable, tipos de
  almacenamiento, número de filas) de `hogar`, `lugar_compra`, `vivienda`,
  `gasto_de_consumo_ajustado`, `gasto`, `persona` de las carpetas `engasto2012/` y
  `engasto2013/`; sha256 de todos los ZIP de ambas carpetas. **Ninguna fila de datos.** Los
  `.dta` no traen etiquetas de valor: el FD es la autoridad de códigos.
- `canon/mapa-dominios-v1_0.tsv` (dominios CONSUMO y DINERO), `canon/catalogo-del-mexicano-v1_1.md`,
  especificación y `resultados.json` (sólo ids) de `CALC-DIN-OFERTA-EXCLUSION-ENIF2021-0001`.

## 1 · Identidad de ola ENGASTO (hallazgo de estructura; decide qué se abre)

El manifiesto trae **dos** juegos de archivos bajo rótulos de 2012: los 28 `engasto_*`
(24 de ellos con `archivo: engasto2013/…` aunque `url_origen` diga `/2012/`) y 20 huérfanos
registrados por REPAIR-1 como `engasto2012_*` en `engasto2012/`. Por **identidad**, no por
rótulo:

| carpeta | HOGAR | campos | casa con `engasto12_fd.pdf` | lectura |
|---|---|---|---|---|
| `engasto2012/` | sha `03c47fde…`, 58 951 filas | 161 (`num_cel`, `factor_hog` #161) | SÍ, campo a campo | **ENGASTO 2012** |
| `engasto2013/` | sha `bb17939d…`, 58 371 filas | 173 (`num_cel1/2`, `recurso_1…6`, `cubr_gasto`, `ahorro`) | NO | otra ola (2013), sin FD en corpus |

`viviendas_*` (plural) sólo existe en `engasto2013/` y su `url_origen` es `/2013/`. Los
sha256 de todos los pares de archivos homónimos difieren. Conclusión: ENGASTO tiene **dos
olas** en corpus, 2012 y 2013. **E.6: la más reciente (2013) queda RESERVADA** — ninguno de
sus bytes es input; `recurso_*` (cómo completa el hogar su gasto: préstamos, tarjeta,
ahorro) y `cubr_gasto` quedan sin medir (NC). Se abre 2012 por los ids que apuntan a
`engasto2012/`: `engasto2012_hogar_dta`, `engasto_2012_vivienda_dta`,
`engasto_2012_lugar_compra_dta`, `engasto2012_gasto_de_consumo_ajustado_dta`. La medidora
PARA si alguna ruta resuelve a `engasto2013/`. El defecto de rotulación del manifiesto se
declara (hallazgo), no se edita aquí.

## 2 · ENIGH 2016–2022 · unidad HOGAR (nunca persona)

Tablas: `concentradohogar` (ponderador `factor`, diseño `est_dis`/`upm`, variables del
jefe, agregados trimestrales), `hogares` (equipamiento y tarjeta), `gastoshogar` (partida
por partida: `clave`, `tipo_gasto`, `forma_pag1..3`, `lugar_comp`, `gasto_tri`). Llave
`folioviv`+`foliohog`. Trazado idéntico en las cuatro olas (encabezados comparados) salvo
que `gastoshogar` 2022 añade `entidad, est_dis, upm, factor` (no se usan: el diseño sale de
`concentradohogar` en todas las olas).

| id | texto (definición del diccionario / pregunta) | estimando | universo | reports / afirmaciones |
|---|---|---|---|---|
| PART-ALIMENTOS … PART-TRANSF-GAS (9) | `gasto_mon = alimentos + vesti_calz + vivienda + limpieza + salud + transporte + educa_espa + personales + transf_gas` (diccionario) | Σw·rubro / Σw·gasto_mon | hogares con `gasto_mon > 0` | CONS (estructura), CONS-023 |
| PART-COMUNICA | `comunica` = Σ gasto_tri de claves F001–F006, R005–R008, R010, R011 (teléfono, celular, internet) | Σw·comunica / Σw·gasto_mon | `gasto_mon > 0` | CONS-038, APUEST-035 |
| PART-ALI-FUERA-EN-ALIMENTOS | `ali_fuera` = claves A243–A247 (A243 «Desayuno» … A247 «Otros eventos fuera de casa») | Σw·ali_fuera / Σw·alimentos | `alimentos > 0` | CONS |
| PART-BEBIDAS-EN-ALIMENTOS | `bebidas` = claves A215–A238 (bebidas alcohólicas y no alcohólicas); `alimentos = ali_dentro + ali_fuera + tabaco` | Σw·bebidas / Σw·alimentos | `alimentos > 0` | SALUD-001, SALUD-026 |
| PART-EFECTIVO-EN-GASTO-DIRECTO | `forma_pag1` = 1 «Efectivo» | Σw·gasto_tri(efectivo) / Σw·gasto_tri, partidas `tipo_gasto` G1 | hogares con gasto G1 > 0 | CONS-017, CONS-033 |
| PART-CANAL-{MERCADO, TIANGUIS-AMBULANTE, ABARROTES, ESPECIFICAS-DEL-RAMO, SUPER-MEMBRESIA, CONVENIENCIA, OTRO} | `lugar_comp` (catálogo 01–18, idéntico 2016–2022): 1 · 2+3 · 4 · 5 · 6+9 · 10 · resto | Σw·gasto_tri(canal) / Σw·gasto_tri(con lugar 1–18), partidas G1, claves A001–A242 (alimentos, bebidas y tabaco para el hogar) | hogares con denominador > 0 | APUEST-003, APUEST-042/043, CONS-016, CONS-017 |
| HOG-ALI-FUERA | `ali_fuera > 0` | proporción | todos | CONS |
| HOG-GASTO-COMUNICA | `comunica > 0` | proporción | todos | CONS-038 |
| HOG-TIENE-CELULAR | `celular` «servicio de teléfono móvil aunque sea un solo integrante» 1/2 | proporción | 1 o 2 | CONS-038 |
| HOG-CONEX-INTERNET | `conex_inte` 1/2 | proporción | 1 o 2 | CONS-038 |
| HOG-TIENE-TARJETA-CREDITO | `tarjeta` «tarjeta de crédito … propiedad de algún integrante» 1/2 | proporción | 1 o 2 | CONS-011, FIN-034 |
| HOG-USA-TARJETA-ALIMENTOS-SI-TIENE | `pagotarjet` «utilización en el mes de tarjeta de crédito bancario … para alimentos, bebidas o tabaco» 1/2 | proporción | `tarjeta` = 1 (**condicional a oferta**) | CONS-033 |
| HOG-PAGO-TARJETA-CREDITO | `pago_tarje` = erogación Q003 «Pagos a tarjeta de crédito bancaria o comercial (incluye intereses)» > 0 | proporción | todos | CONS-011, CLASE-015 |
| HOG-PAGO-DEUDAS | `deudas` = Q004 «Pago de deudas a la empresa … y/o a otras personas o instituciones (excluya hipotecarios)» > 0 | proporción | todos | FIN-023/024, CLASE-014 |
| HOG-RECIBE-PRESTAMO | `prestamos` = ingreso P053 «Préstamos recibidos de personas ajenas al hogar o instituciones, se excluyen préstamos hipotecarios» > 0 | proporción | todos | FIN-024 |
| HOG-GASTO-MAYOR-INGRESO | `gasto_mon > ing_cor` (trimestral, ambos) | proporción | ambos definidos | CLASE-014 («72% gasta más de lo que gana») |
| HOG-COMPRA-FIADO | alguna partida G1 con `forma_pag1..3` = 2 «Fiado» | proporción | todos | CONS-025 (BNPL), FIN-019 |
| HOG-COMPRA-TARJETA-CREDITO | alguna partida G1 con `forma_pag1..3` = 5 «Tarjeta de crédito» | proporción | todos | CONS-011, CONS-021 |
| HOG-COMPRA-INTERNET | alguna partida G1 con `lugar_comp` = 18 «Internet» | proporción | todos | CONS-015, CONS-016, APUEST-035 |
| HOG-COMPRA-INTERNET-SI-CONEXION | ídem | proporción | `conex_inte` = 1 (**condicional a oferta**) | CONS-015/016 |
| MEDIA-GASTO-MON-MENSUAL | `gasto_mon / 3` | media ponderada, pesos corrientes de cada ola | `gasto_mon` definido | CONS-023 |

**Remesas:** no se re-miden. Se citan `CALC-ENIGH{2016,2018,2020,2022}-REMESAS-CONTEXTO-0001`
y `…-INTENSIDAD-REMESAS-0001` (encargo §1).

## 3 · ENGASTO 2012 · unidad HOGAR

| id | pregunta textual (FD) | estimando | universo |
|---|---|---|---|
| GRAN-COMPRA-{SUPER-MEMBRESIA (6,9), MERCADO (1), TIANGUIS-AMBULANTE (2,3), ABARROTES (4), CONVENIENCIA (10), DEPARTAMENTAL (7), INTERNET (18), OTRO (5,8,11–17)} | `lc_granc` «¿Dónde realiza generalmente la gran compra para el consumo del hogar?» (Cuestionario de gastos mensuales, Apartado E, p. 1) | proporción de hogares | `lc_granc` en 01–18 (97 y nulo fuera) |
| {CARNE, FRUTA, VERDURA, PAN, LECHE}-EN-{SUPER-MEMBRESIA (6,9), MERCADO-TIANGUIS-AMBULANTE (1,2,3)} | `lc_carne`, `lc_fruta`, `lc_verdura`, `lc_pan`, `lc_leche` «¿Dónde realiza generalmente la compra de …?» | proporción | la variable en 01–18 |
| COMPRA-INTERNET-ALGUN-RUBRO | algún `lc_*` (76) = 18 «Internet» | proporción | hogares con algún `lc_*` en 01–18 |
| COMPRA-INTERNET-SI-CONEXION | ídem | proporción | ídem y `conex_inte` = 1 (**condicional a oferta**) |
| TIENE-CELULAR | `num_cel` «¿Cuántos tiene?» (celulares; Apartado E, p. 2) ≥ 1 | proporción | 0–50 |
| CONEX-INTERNET | `conex_inte` «¿En este hogar tienen conexión a Internet?» 1/2 | proporción | 1 o 2 |

Catálogo de lugar de compra del FD (01 Mercado … 18 Internet, 97 No especificado) =
catálogo `lugar_comp` de ENIGH; los grupos son los mismos que §2.

## 4 · Columna de oferta (§3 v2.16, oferta antes que preferencia)

| marginal | columna de oferta | estado |
|---|---|---|
| crédito (tarjeta, pago a tarjeta, deudas, compra con tarjeta) | exclusión por oferta de crédito, persona, ENIF: `RESULT-DIN-OFERTA-EXCLUSION-ENIF{2012,2015,2018,2021}-CREDITO-*` (`CALC-DIN-OFERTA-EXCLUSION-ENIF*-0001`, #1042) | CITADA; unidad distinta (persona vs hogar), no se combinan en una cifra |
| uso de tarjeta en alimentos | HOG-USA-TARJETA-ALIMENTOS-SI-TIENE (universo = hogares con tarjeta) | CONSTRUIDA |
| compra por internet | HOG-COMPRA-INTERNET-SI-CONEXION; COMPRA-INTERNET-SI-CONEXION (ENGASTO) | CONSTRUIDA (conexión del hogar; no mide cobertura de entrega) |
| canal físico (mercado, tianguis, súper, conveniencia) | presencia de cada formato en la localidad | **NO-CONSTRUIBLE**: ni ENIGH ni ENGASTO miden oferta de establecimientos; TLOC es eje de segmentación, no columna de exclusión |
| fiado | oferta de fiado del comercio | **NO-CONSTRUIBLE** |

## 5 · Ejes (uno a la vez, nunca cruces)

ENIGH: TOTAL · SEXO-JEFE (`sexo_jefe` 1/2) · EDAD-JEFE (`edad_jefe` ≤29, 30–44, 45–59, 60+) ·
ESCOLARIDAD-JEFE (`educa_jefe` 1–4 HASTA-PRIMARIA, 5–6 SECUNDARIA, 7–8 MEDIA-SUPERIOR, 9–11
SUPERIOR) · TLOC (`tam_loc` 1–4) · DECIL (deciles de hogares por `ing_cor`, construidos en la
ola, spec §3) · ENTIDAD (dos primeros dígitos de `folioviv`, 01–32) **sólo** para
PART-ALIMENTOS, PART-CANAL-SUPER-MEMBRESIA, HOG-TIENE-TARJETA-CREDITO, HOG-COMPRA-INTERNET y
MEDIA-GASTO-MON-MENSUAL.

ENGASTO: TOTAL · SEXO-JEFE (`sexo_je`) · EDAD-JEFE (`edad_je`, mismos cortes) ·
ESCOLARIDAD-JEFE (`ned_je` 1 primaria incompleta, 2 primaria completa, 3 secundaria
completa, 4 media superior y superior — cortes de INEGI, **no** comparables con los de
ENIGH) · TLOC (`tam_loc` de VIVIENDA).

**No construidos** (NC): FORMALIDAD (atributo de persona ocupada; el hogar no tiene
formalidad única), REGIÓN agrupada (el encargo no fija regionalización; ENTIDAD la
sustituye donde importa), NSE AMAI (sólo existe `CALC-AMAI-NSE-ENIGH-2022-0001`, una ola; su
cruce con estas conductas es otro CALC), DECIL en ENGASTO (sin ingreso en las tablas 2012).
