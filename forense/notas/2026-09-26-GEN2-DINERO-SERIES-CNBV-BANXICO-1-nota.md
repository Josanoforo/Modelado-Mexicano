# Nota de cierre · ACTO GEN2-DINERO-SERIES-CNBV-BANXICO-1

**10 afirmaciones de DINERO con RESULT** (de 30 en la cola v1.1: CNBV 21 +
BANXICO 9) · 5 NO-CONSTRUIBLE · 15 NO-ACCESIBLE (red denegada; NC a caja) ·
0 sin dictamen. Contadores movidos: 2 CALC sellados `cuenta_gen2: SI`,
`adopta: NO`, `tipo: SERIE-ADMINISTRATIVA` (56 RESULT: 44 + 12), 2 asientos
de replay REPRODUCE. `celdas_validadas: 219 → 219 (Δ0) @ 910eab04`. Pisos de
crédito/ahorro con columna de oferta nueva: **0** (ver §5).

ADR: `ADR-260926-GEN2-DINERO-SERIES-CNBV-BANXICO-1-8dbe-01`. Encargo:
`forense/encargos/2026-09-25-GEN2-DINERO-SERIES-CNBV-BANXICO-1.md` (0-bis
`8dbe1f9`, SHA de redacción `aa36232a` = base; main sin moverse).

## 1 · Arranque

- Repo `/home/user/Modelado-Mexicano`, rama `claude/new-session-ill5zp`,
  `aa36232 Merge pull request #1157`, árbol limpio, 0 detrás.
- Hook: `ENTORNO-DERIVADO = NUBE`, `senal-corpus: montado=NO
  archivos_examinados=0`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`,
  INEGI 200.
- **Premisa de red que cayó (logística, no qué se mide).** El encargo asignó
  NUBE «con red para portales públicos (CNBV/Banxico)». El proxy de esta
  sesión responde **403 a CONNECT** en `www.banxico.org.mx`,
  `portafolioinfo.cnbv.gob.mx`, `www.cnbv.gob.mx`, `www.gob.mx`,
  `datos.gob.mx` y `web.archive.org` (`curl: (56) CONNECT tunnel failed,
  response 403`; estado del proxy: `connect_rejected … policy denial`). Es
  política del entorno, no la cadena TLS de U0. El encargo previó la rama:
  «si la sesión no tiene red, CAJA». Replanteo declarado: lo alcanzable desde
  **constancias ya en el repo** se sella aquí; lo que exige portal va a caja
  como NC. No es PARO: el objetivo sigue alcanzable en parte y el resto tiene
  sucesor.
- A.8 · ya hecho: `ls data/corrida0 | grep -ic 'CNBV\|BANXICO\|IMOR'` → **2**
  (`CALC-BANXICO-PRODUCTO-DANO-0001`, encuesta de persona;
  `CALC-IMOR-CONTEXTO-0001`, resumen por régimen, `cuenta_gen2:
  NO-DERIVACION-CONTEXTUAL`). Se citan; ninguno emite nivel por mes citado
  ni por producto en los periodos de las afirmaciones.
  `git ls-remote --heads origin | grep -ic 'cnbv\|banxico\|DINERO-SERIES'` →
  0; PR abiertos con `DINERO-SERIES` → 0.

## 2 · P1 · afirmación → serie

Tabla: `forense/analisis/dinero-series/afirmacion-serie-v1_0.tsv`, generada
por `tools/dominios/dinero-series/dictamina.py` (valores leídos de los
`resultados.json` sellados; `--verifica` byte a byte). Por cada fila: serie,
tabla/id, periodicidad, unidad, URL, fecha de descarga de la constancia,
RESULT citados, veredicto y razón.

| dictamen | n |
|---|---|
| RESULT | 10 |
| NO-ACCESIBLE (la serie existe; host denegado) | 15 |
| NO-CONSTRUIBLE (no es serie administrativa) | 5 |

«No pude alcanzar la fuente» (NO-ACCESIBLE) y «la fuente no tiene el dato»
(NO-CONSTRUIBLE) no se colapsan (§2). La «verificación de texto» de una serie
es su definición oficial, citada en la spec §2; **no** se añadió a
`verificaciones-texto-v1_1.tsv` porque su compuerta A.15 exige casar con un
inventario de reactivos de encuesta, y una serie no tiene reactivo (NC-04).

## 3 · P2–P3 · constancias y CALC

Spec humana `forense/prereg-caja/DINERO-SERIES-IMOR-spec-v1_0.md` (+ sidecar)
congelada en COMMIT-1 `07b10ef`; cableado de preflight (bloque `parametros`,
espejo de §3–§4) en commit propio antes de toda ejecución. Sin ejecución
diagnóstica.

| CALC | insumo (`insumos/`, sha256) | fuente · descarga | RESULT | verify |
|---|---|---|---|---|
| `CALC-BANXICO-SERIES-IMOR-0001` | `banxico-imor-consumo-mensual.csv` `772f9d0b…` | Banxico Informe Trimestral ene–mar 2026 · 2026-09-11 | 44 | REPRODUCE · IDENTICO (aislado, 44/44, Δ 0.0) |
| `CALC-CNBV-SERIES-IMOR-R16-0001` | `cnbv-imor-consumo.csv` `e61c97a3…` | CNBV 040-1A-R16, foto 2021-12 · 2026-09-11 | 12 | REPRODUCE · IDENTICO (aislado, 12/12, Δ 0.0) |

Las dos constancias son copias byte a byte de
`data/fuentes-financieras-20/` (extraídas el 11/sep de payloads del
manifiesto); ninguna serie viva se selló. Evidencia:
`forense/analisis/dinero-series/evidencia-replay-dinero-series.json`; filas
en `forense/replay-evidencia.tsv`. La vista (`corridas.tsv`,
`resultados.tsv`) **no** se reescribió: `registro --escribe` regeneraba
~146 mil líneas ajenas (la vista no se regenera en main desde #1076); se
revirtió y se siguió el patrón vigente de los actos recientes (asiento de
replay por acto) — declarado, NC-05.

Unidad: **porcentaje de saldo de cartera**, rotulado en cada RESULT
(`…-G-UNIDAD`): no es encuesta ni persona, y ningún RESULT se promedia con un
piso de ENIF (§4).

## 4 · P5 · CONFIRMA / MATIZA / ROMPE (RETROSPECTIVA)

Regla pre-registrada en spec §5 (CONFIRMA ≤ 0.5 pp mismo mes y producto;
MATIZA si orden o signo se sostiene y cifra/universo/definición difieren;
manda MATIZA si las dos). Todo es RETROSPECTIVA; CRFAC-007 además
**no estaba en §5** y se rotula RETROSPECTIVO-NO-PREREGISTRADO.

- **CONFIRMA (3)**: CRPOP-012 y CRPOP-044 (IMOR de consumo del sistema ~3.1%
  dic-2024; ~3% vigente a mar-2026), CRPOP-055 (3.4% dic-2023).
- **MATIZA (7)**:
  - CRPOP-006: «IMOR sistémico de créditos personales ~10.8% feb-2024» no es
    el IMOR de personales de banca comercial, que la serie da en menos de la
    mitad; solo cabría como IMORA u otro universo. Es la corrección más
    grande del lote.
  - CRPOP-002: el techo por producto se sostiene para personales > tarjeta >
    ABCD, pero en R16 2021-12 «adquisición de bienes muebles» bancaria está
    **por encima** de personales; el crédito de tienda con cobranza
    domiciliaria no está en ninguna serie bancaria.
  - CRPOP-001: con el sistema como denominador, el ~5% de Azteca que cita el
    propio report queda debajo del «2–4 veces».
  - APUEST-008, CRPOP-007, CRPOP-018: solo el lado de sistema; las cifras
    por institución quedan NO-ACCESIBLE.
  - CRFAC-007: morosidad interanual a mar-2026 sube en todos los productos
    salvo nómina (el único negativo), como dice el REF; el periodo difiere.
- **ROMPE (0)**. **NO-CONTESTA (1)**: CRFAC-003 es IMORA; las series son IMOR.

Por report: *Crédito Popular* (compass-4 y el largo) recibe 3 CONFIRMA de
sistema y 4 MATIZA; su tesis central, el diferencial de los bancos populares
frente al sistema, sigue sin medir porque exige R16 por institución. *Crédito
Fácil* recibe 1 MATIZA y 1 NO-CONTESTA; *Apuestas* 1 MATIZA; *Clasemediero*,
*Confianza*, *Violencia* y *Consumidor*: sin RESULT (NO-ACCESIBLE o
NO-CONSTRUIBLE).

## 5 · P4 · columna de oferta

**0 pisos** ganan columna. Las series de oferta (BDIF de CNBV: sucursales,
corresponsales y puntos de acceso por municipio o por 10 mil adultos) están
en un host denegado, y en el repo no hay constancia de oferta
(`rg -l -i 'corresponsal|sucursal|puntos de acceso|10 mil adultos' data
--glob '*.csv' --glob '*.tsv'` → 10 archivos, todos inventarios de reactivos
de encuesta o colas, ninguno serie). NC-03 a caja.

## 6 · Módulo de auditoría (§5)

- ¿Contadores movidos? 2 CALC, 56 RESULT, 2 asientos; celdas_validadas Δ0.
- ¿Escala? Todo en % de saldo; ninguna comparación contra persona.
- ¿PROSPECTIVA/RETROSPECTIVA? Todo RETROSPECTIVA; ninguna frase las mezcla.
- ¿Unidad? Saldo de cartera (unidad crédito, no persona ni hogar).
- ¿Pobreza confundida con cultura? La MATIZA de CRPOP-002 y CRPOP-006 empuja
  en contra de leer la mora del crédito popular como rasgo: el nivel de
  sistema es bajo y la cifra alta de las afirmaciones depende de la
  definición (IMORA) y de la institución. Queda como hipótesis hasta R16 por
  institución.
- ¿Clase media urbana? La banca comercial sobrerrepresenta al cliente
  formal; lo popular no bancario (SOFIPO, ENR, tienda) está fuera de estas
  dos series: lo dice cada fila.
- ¿Afirmación de estado escrita a mano? Los conteos de esta nota salen de
  `dictamina.py` y de `resultados.json`.
- ¿Qué sería peligroso leído en simple? Que «IMOR ~3%» diga que el crédito
  popular es sano: es el sistema bancario, no el segmento.

## 7 · Verificación

`corrida0 verify` de ambos CALC → REPRODUCE; `dictamina.py --verifica` →
COINCIDE; `redictamina_v1_1.py --verifica` → COINCIDE (mapa sin cambio, NC-04);
`tests/check.py --rapido` → 0 FAIL.
