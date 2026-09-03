# Descargas pendientes — v3 (2/sep/2026)

Producido por el **relanzamiento** de `ACTO MAESTRA35-A1 · REGISTRA-Y-EVALUA-DESCARGAS-3`
(encargo `forense/encargos/2026-09-02-MAESTRA35-A1-REGISTRA-Y-EVALUA-DESCARGAS-3.md`,
enmienda `e2`, P4). Sucede a la primera pasada del mismo acto (`PR #481`), que
cerró P0-bis con `P1-P4 GATED` porque la compuerta se abrió a mitad de sesión.
La compuerta se cumplió (30 archivos nuevos, 16:56–17:10) y este relanzamiento
ejecuta P1-P4 íntegros.

**Derivado del registro, no de memoria.** Cada línea sale de
`data/curacion-registro/cola-adquisicion-registro.tsv` (estado real de la fila
tras este acto) y de `data/manifiesto.yaml` (los `id` de payload que
efectivamente existen). `python3 tests/manifiesto.py --verifica` sobre los 30
`id` nuevos: **30/30 COINCIDE** (anti-PR#77, salida cruda en el commit de
cierre).

**A.13 — universo examinado.** `find "/mnt/c/Users/PC0/Descargas MX" -type f`
= **190 archivos**; `-newermt 2026-09-02` = **30 nuevos** (28 ZIP + 2 PDF, los
28 ZIP con `zipfile.testzip()` limpio).

---

## 1 · Lo que este relanzamiento cerró

| fila / fuente | estado antes | estado después | qué cambió |
|---|---|---|---|
| `IEEH_HIDALGO_SERIE_MUNICIPAL` | `OBTENIDO-SIN-DENOMINADOR` | **`OBTENIDO`** | 4 zips SICEE locales de Hidalgo traen `LISTA_NOMINAL` a nivel municipio (84 filas = 84 municipios) |
| `IEE_AGUASCALIENTES_SERIE_MUNICIPAL` | `OBTENIDO-SIN-DENOMINADOR` | **`OBTENIDO`** | 5 zips SICEE locales de Aguascalientes traen `LISTA_NOMINAL` a nivel municipio (11 filas = 11 municipios) |
| `SICEE_LOCAL_AYUNTAMIENTOS_VERACRUZ` (fila nueva) | sin fila | **`OBTENIDO`** | 4 zips SICEE, denominador municipal disponible por primera vez (212 municipios en 2021) |
| `SICEE_FEDERAL_DIP_2018` / `_2021` (filas nuevas) | sin fila | **`OBTENIDO`** | denominador federal por casilla para las patas concurrentes 2018/2021 de `civico.participacion.tipo_boleta_federal_2016_2024` |
| `EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6` (CompraNet) | `NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)`, dominio caído | `NO-OBTENIDO-POR-ESTE-AGENTE(2 intentos)` | dominio nuevo confirmado y sondeado (200/200); sigue SPA gateada, sin catálogo accesible por `curl` |

**Fuente nueva dada de alta**: SICEE (INE) — `sicee_ine` en `aliases-fuentes.tsv`,
necesidad `N37` (`civico.participacion.tipo_boleta_federal_2016_2024`, sin `N`
previa), relación `REL-6c677146f183f594c0649a61` `CONFIRMADA`. 12 filas nuevas
en la cola (3 locales + 9 federales, `NUEVA-A1`, `sicee-1`..`sicee-12`).

**Sin cambio de estado** (contenido evaluado, receta no satisfecha):

| fila / fuente | estado | qué llegó | qué falta |
|---|---|---|---|
| `MEXICO_PANEL_STUDY_2012` | `NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)` | paquete ICPSR completo (10 archivos) — **otra vez documentación**: 6 PDF (cuestionarios + 4 codebooks), 2 txt, 2 html; 0 `.dta`/`.sav`/`.tab` | login ICPSR para el microdato |
| `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` | `NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)` | 2 PDF de Bauchet sobre microseguros en México, pero **no** el paper pedido (`abstract_id=2474620`); son `2589578` («Modalities matter») y `2689238` («Asymmetric information…», 2017) | el PDF exacto — `cenfri.org`/SSRN siguen con reto Cloudflare para un agente |

**Intocadas por este acto** (no llegó nada nuevo que las toque):

- `TEPJF_ELECCIONES_CONCURRENTES_1991_2018` — sigue `NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)`; receta de navegador en `te.gob.mx/publicaciones/`, buscador → «Elecciones concurrentes».
- `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` (LAOMS) — sigue `NO-OBTENIDO-POR-ESTE-AGENTE(15 intentos)`; receta de navegador en `laoms.org`.

---

## 2 · Lo que el relanzamiento agregó sin que ninguna regla lo pida hoy

9 payloads SICEE federales (senadurías 2018/2021-ext-Nayarit/2023-ext-Tamaulipas/2024,
presidencia 2018/2024, diputaciones 2024) quedan registrados y `OBTENIDO` en su
fila de cola, pero **sin disparador vigente que los reclame** — `usado_para`
declara «sin necesidad declarada — mesa lo bajó el 2026-09-02» en el manifiesto
y la nota de cada fila lo repite. No se fuerza ninguna relación en
`relaciones.tsv` para estos: la única relación nueva (`REL-6c677146f183f594c0649a61`)
cubre el agregado de las 27 fuentes SICEE contra `N37`, no una fila por
consulta — inflar `relaciones.tsv` con filas sin necesidad real sería
`APERTURA_INDETERMINADA` de utilidad nula, no una alta legítima.

---

## 3 · Lo que sigue vivo para el acto sucesor

1. **Verificar el join municipio↔SICEE 1:1** antes de usar el denominador
   promovido de Hidalgo/Aguascalientes/Veracruz para cualquier cálculo — la
   fila de `utilidad-modelo.tsv` de `N37` lo deja como `verificacion_requerida`
   explícita, no como hecho. Candidato natural: sucesor de `MAESTRA35-L3` o
   `MAESTRA35-L6`.
2. **`FP-245`** (mesa, sin resolver): con el denominador federal 2018/2021 ya
   `OBTENIDO` por esta vía, los dos disparadores candidatos de
   `civico.participacion.tipo_boleta_federal_2016_2024` siguen esperando
   decisión de mesa — este acto no la toma.
3. **CompraNet** — dominio vigente confirmado y sondeado, pero la SPA no
   expone catálogo ni API sin renderizar JS. Receta de navegador anotada en
   la fila (§1 de arriba); `≤1 min` si falla.
4. **TEPJF y LAOMS** — recetas de navegador vigentes, sin tocar.
5. **ICPSR 35024 / Bauchet 2474620** — ambos exigen credencial o esquivar
   Cloudflare desde un navegador real; ningún camino de agente nuevo.

**Contador**: payloads registrados **+30** (con sha, 30/30 `--verifica`
COINCIDE) · filas de la cola que cambian de estado **+3** (`IEEH_HIDALGO`,
`IEE_AGUASCALIENTES`, `EXT_OF_07`) · filas nuevas en la cola **+12** (3
locales + 9 federales SICEE, todas `OBTENIDO`) · descargas pendientes
v2 → v3: de las 2 «parciales»/3 «no ejecutadas» de v2 que tocan este acto,
**0 pasan a cumplidas** (ICPSR y Bauchet siguen sin el objeto exacto,
CompraNet sigue sin catálogo accesible) — el avance real está en el
denominador municipal/federal de la pieza cívica, no en el paquete original
de 15 recetas.
