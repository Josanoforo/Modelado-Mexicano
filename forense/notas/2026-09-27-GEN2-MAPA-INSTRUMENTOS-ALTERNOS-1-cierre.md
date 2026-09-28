# Cierre · GEN2-MAPA-INSTRUMENTOS-ALTERNOS-1

**Contadores movidos: cero.** No mide, no adopta, no abre reservas y no deriva ninguna cifra de una base.

- **Fecha:** 27/sep/2026.
- **Rama:** `acto/gen2-mapa-instrumentos-alternos-1`. 0-bis `4b11076a` sobre `origin/main` `eda5bb9f`, que es el SHA de redacción.
- **Entorno:** `tools/entorno.py --arranque` → `ENTORNO-DERIVADO = CAJA`, `montado=SI archivos_examinados=512`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, red `http_code=200`. Coincide con el asignado.
- **Modelo:** Opus en el hilo principal (dictámenes); cuatro lectores Sonnet para recolectar reactivos.

## 1 · Productos

| producto | qué es |
|---|---|
| `canon/mapa-instrumentos-alternos-v1_0.tsv` | 64 filas incógnita × instrumento × ola, 17 incógnitas; lo produce `forense/analisis/mapa-instrumentos-alternos/arma_mapa.py` (`--verifica` = IDENTICO) |
| `forense/analisis/mapa-instrumentos-alternos/hoja-para-mesa-mapa-instrumentos-alternos.md` | hoja para mesa, en lenguaje RH, sobre A1, A2, D1 e I1, con texto de firma listo y llaves de CALC |
| `…/propuesta-R03.md` | P2: propuesta de re-especificación de R03 |
| `…/universo-por-instrumento.tsv` | P1: 107 entradas de manifiesto por instrumento, ola, tipo y reserva |
| `…/acceso-rnm.tsv` | condición de acceso al microdato en el RNM (4 catálogos; URL, fecha, sha de la respuesta) |
| `…/lotes/` | las cuatro tablas de lectura, el barrido del índice y `AUDITORIA-LOTES.md` |
| `data/manifiesto.yaml` (+51 líneas, 0 borradas) | 3 DDI del RNM: `encrige2020_rnm691_ddi`, `enve2024_rnm1058_ddi`, `enve2016_rnm227_ddi` (payload en `data/raw/inegi_rnm_ddi/`, corpus compartido; `--verifica` COINCIDE ×3) |

**Conteo (una línea).** 64 pares:

- 2 EXISTE-SATISFACE;
- 36 EXISTE-SATISFACE-PARCIAL;
- 15 EXISTE-NO-SATISFACE;
- 10 NO-ENCONTRADO;
- 1 NO-VERIFICABLE-SIN-ABRIR-RESERVA.

11 de 17 incógnitas tienen al menos una vía en el corpus. 11 pares piden OBTENER o SOLICITUD y van a OBTENCION-EXTERNA-1, igual que las 5 incógnitas sin nada en el corpus (M09, M10, M11, M20, M21).

## 2 · «Hecho» por comando (sobre el árbol de este commit)

- **Incógnitas.** `tail -n +2 canon/mapa-instrumentos-alternos-v1_0.tsv | cut -f1 | sort -u | wc -l` → **17**. El comando literal del encargo, `cut -f1 | sort -u | wc -l`, da **18** porque cuenta la cabecera `incognita`; es un defecto de la receta, no del mapa.
- **Fórmula prohibida.** `grep -c "no existe" canon/mapa-instrumentos-alternos-v1_0.tsv` → **0**.
- **Dictámenes.** 0 filas con `dictamen_A4` vacío; 0 filas NO-ENCONTRADO sin `seccion_o_pagina`.
- **Ids.** Los 49 ids distintos que cita el mapa existen en `data/manifiesto.yaml`: 0 ausentes (por lector YAML, id por id).
- **Verbatim.** 49 filas con texto de pregunta verificadas contra el documento fuente (texto plegado): 0 fallas. Control positivo: una pregunta inventada se detecta como falla.
- **Adjuntos. NO cumplido:** los dos adjuntos no llegaron (§4).
- **Hoja para mesa:** presente.
- **Suite:** `check.py`, en §7.

## 3 · Premisas verificadas

- **[EJECUTADO] «el microdato ENCRIGE 2020 ya está en el corpus» → FALSO.** Lo que hay es un zip de **tabulados de datos abiertos**: 392 miembros `conjunto_de_datos/…/t*.csv` e índices de títulos. Lo mismo pasa con `conjunto_de_datos_enve_2024_csv` (413 miembros de tabulados). ENVE 2016 es solo un esquema de columnas. #826 usó tabulados (`t6_33`, `t6_36`). El RNM (catálogo 691) dice «Data Access Not Available» para ENCRIGE 2020. Es logística: el objetivo sigue alcanzable porque los DDI del RNM documentan las variables del microdato sin abrirlo.
- **[EJECUTADO] Campo `reserva` de ENCRIGE 2020.** No tiene `estado_reserva`. Por la letra de E.6 sería la ola a reservar, sus tabulados ya los vio #826 y F5 R08 guarda 2016 como reserva. Va a mesa (hoja, aviso 2).
- **[EJECUTADO] RNM.** ENCRIGE tiene olas 2016 y 2020 (más ECRIGE-CDMX 2019). ENVE tiene 2012–2024; 2020 y 2022 no están en el corpus.
- **[LEÍDO] Catálogo.** M09–M22 corresponden a R1.4…R10.3, como dice el encargo. Además, **M09–M23 son HOLDOUT**: todo CALC propuesto consume ese papel (hoja, aviso 1).
- **[LEÍDO] Firma F-19 (mesa, 15/sep/2026; ADR-529).** No admite pasar de persona a establecimiento. Eso fija la forma de la propuesta de R03: familia descriptiva junto a R08/R02, no celda.
- **[REPORTADO → verificado donde toca el mapa].** CSES M5 incluye México 2018 (`MEX_2018`, n de diseño 1 239, levantado del 12 al 18/jul/2018), que fue elección concurrente. MEXWF1_19 excluye pensiones de jubilación o retiro. VB20, M1 y CLIEN existen (CLIEN solo en 2018/19). Las cifras de prensa del informe no se usaron.

## 4 · Lo que no salió como pedía el encargo (declarado)

1. **Adjuntos no recibidos.** Ni «Benchmark del Mexicano…» ni `REVISION-repo-y-fuentes-alternas-2026-09-27.md` están en `Descargas MX` ni en `Downloads`. Busqué por contenido en los `.md/.txt/.zip` modificados el 27/sep: solo aparecen mencionados dentro de los dos encargos del día. Como prevé el encargo, el acto siguió sin ellos.
2. **ENCRIGE 2016 no se leyó ni en documentación.** F5 R08 lo preserva así. Dictamen: NO-VERIFICABLE-SIN-ABRIR-RESERVA, con el comando que lo haría.
3. **La confirmación «en la base» de P2 no es posible.** El microdato de ENCRIGE y ENVE no está en el corpus. Se confirmó por los DDI del RNM (variable, etiqueta, texto literal y categorías).
4. **Nombre de la hoja.** `hoja-para-mesa.md` colisiona por nombre normalizado (T02) con `forense/analisis/familias-2027/astra6-envipe/hoja-para-mesa.md`. Se llama `hoja-para-mesa-mapa-instrumentos-alternos.md`.
5. **ENVE 2016, muestra de registros.** El extractor del hilo principal metió en el texto los miembros `*_esq_2016.csv`, que traen unos 12 registros de ejemplo además de los encabezados. La ola 2016 no está reservada (ENVE figura como EXPUESTA en F5 E04), no se derivó ninguna cifra y el texto se recortó a los encabezados. Metadatos de CIDE-CSES 2015 (tres `.sav`): solo `metadataonly=True` (nombres, etiquetas y valores; ninguna respuesta).
6. **Error de lector corregido.** El lote D dio M19 × ENCUCI como NO-ENCONTRADO; ENCUCI trae `AP5_1_*`. Detalle en `lotes/AUDITORIA-LOTES.md`.
7. **`.claude/` espurio.** Un `cd` a `forense/analisis/obtencion-previa-1/` hizo que el cliente creara ahí `.claude/.cc-writes/`. Se borró fuera del sandbox antes de cualquier `git add`; nunca estuvo en el índice.

## 5 · Defecto adyacente arreglado (D-21, ≤ 10 líneas)

`tests/manifiesto.py --registra` rechazaba **todo** registro nuevo porque dos entradas ENOE 2026T1 llevan `estado_reserva = RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO-ABRIR`, un valor fuera de `ESTADOS_RESERVA`. La NC `NC-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-07` está ABIERTA y la FP `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-02` está FIRMADA con la opción (a): «añadirla a `ESTADOS_RESERVA` con raíz `data_raw`; no toca la guardia de U1».

Se aplicó exactamente (a): +1 valor y un mapa de raíces permitidas por estado (`None`/`data_raw` para ese valor). Son 6 líneas en `tests/manifiesto.py`. Sin esto, el append de documentación que el encargo pide por `/adquiere` era imposible. La NC ajena **no se editó** (PARO b); queda para el trámite que la cierre, citando este acto.

**Efecto colateral evitado.** `--registra` re-serializa todo el YAML: 89 líneas ajenas re-envueltas. Con `merge=union` eso duplicaría filas al fusionar con OBTENCION-EXTERNA-1. Se reconstruyó el archivo como el original más las tres entradas nuevas: 0 líneas borradas.

## 6 · Espejo de descargas_mx

Para leer desde el sandbox, 17 payloads de `descargas_mx` se copiaron a `mm-corpus/descargas_mx_espejo/`, con sha256 COINCIDE contra el manifiesto las 17 veces: ENCRIGE 2020 ×2, ENVE 2024 ×3, CSES ×6 y LAPOP ×6. `data/raices.local.yaml` (gitignorado) apunta ahí. No se tocó ningún payload de `descargas_mx`.

## 7 · Suite

`python3 tests/check.py --rapido` se corre antes del push; su salida cruda va en el cuerpo del PR. El juez es el CI del push.

## 8 · Módulo de auditoría (v2.16)

Se aplica en la hoja (§ «Módulo de auditoría»). Resumen:

- procedencia (a) en todas las filas;
- ninguna cifra propia;
- nada PROSPECTIVO;
- unidades separadas (persona / hogar / delito / empresa / establecimiento) y ningún CALC propuesto las promedia;
- sesgo urbano de ENCIG declarado.
