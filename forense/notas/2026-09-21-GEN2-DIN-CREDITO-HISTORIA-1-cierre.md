# ACTO GEN2-DIN-CREDITO-HISTORIA-1 · nota de cierre · 21/sep/2026

Encargo: `forense/encargos/2026-09-21-GEN2-DIN-CREDITO-HISTORIA-1.md` (A.3, 0-bis
`ff564229`, sello de cuerpo `a66577f1…`). Entorno **CAJA** (`ENTORNO-DERIVADO =
CAJA`, corpus montado, 420 archivos examinados, `sin_variable`, sonda 200), Opus 5
(1M), sin sub-agentes, **MODO ABIERTO** hasta cada COMMIT-1. Rama
`acto/gen2-din-credito-historia-1` sobre `fc13cdcc` = `origin/main` al abrir (12
commits después del SHA de redacción `55c8d57c`; no PARO). Guards 0.a-0.d en verde
(0 detrás, árbol limpio, sin duplicado, 4 ramas remotas ajenas fuera de política).

**Contadores que movió este acto:** `N_corridas_selladas` +4 (`CALC-DIN-CREDITO-
PISOS-ENIF2018-0001`, `-ENIF2015-0001`, `-ENIF2012-0001`, `CALC-DIN-CREDITO-K8-
ENFIH2019-0001`), las cuatro `cuenta_gen2 = SI`, `envuelto_legacy = NO`, replay
REPRODUCE/IDENTICO asentado; `adoptados_activos` no se mueve; `NO-VERIFICABLE-AQUÍ`
en la tabla de comparabilidad de crédito 16 → 0.

## 1 · Lo hecho, pieza por pieza

**P0.** La reserva de crédito de ENIF 2024 no existía por objeto en
`data/corrida0/decisiones.tsv` (dirección sólo halló ENVIPE 2026): asentada como
`reserva:enif2024-credito` (fila 186), verbatim. `enif_2012_cuestionario_pdf` y
`enif_2015_cuestionario_pdf` traídos por id (`tests/manifiesto.py --descarga --id`),
2/2 `COINCIDE`, en el corpus compartido `/home/pc0/mm-corpus/raw` (anti-PR#77).

**P1 · `data/credito-comparabilidad-texto-v1_1.tsv`** (v1.0 intacta). Las 16 filas
de 2012/2015 dejan `NO-VERIFICABLE-AQUÍ` leyendo los cuestionarios (pdftotext
-layout, pases de dos columnas verificados por recorte de página): por ola, **K1
K2 K3 K5 K6 `CAMBIO-MENOR` · K4 K8 `CAMBIO-DE-INSTRUMENTO` · K7 `NO-ESTIMABLE`**;
conteo total 8/21/6/5/0. Lo que el cuestionario añadió al FD: 2015 6.4 Sí→6.8,
No→6.5, 6.5 Sí→6.7, No→6.6 (K4 sobre «nunca tuvo», como 2018+, pero multirrespuesta);
2012 6.4 Sí→6.6, No→6.5→6.17 (K4 sobre «no tiene hoy», sin ex usuarios); 2012 6.1.1
«caja de ahorro entre amigos o conocidos» (otro referente: se excluye de K3, no se
colapsa); ventanas «de abril de 2011» y «de julio del año pasado». Test extendido
(`TestSintéticoV11`, `TestTablaRealV11`: 24 filas heredadas verbatim, sha del
cuestionario en cada fila de 2012/2015).

**P2 · pisos históricos, tres CALC, un medidor byte a byte.** Spec
`DIN-CREDITO-PISOS-HISTORIA-spec-v1_0.md`; mapa de roles por ola
`DIN-CREDITO-PISOS-HISTORIA-mapa-v1_0.tsv` (80 filas: variable, códigos, regla y
fuente por rol y ola, resuelto por texto —A.15— y por descriptor DBF, que trae
`UPM_DIS` en 2015 aunque el FD no lo documente). **ORO:** el mismo `medir()` con
`ola = 2021` reproduce los **2 939/2 939 RESULT de #943, `max |Δ| = 0.0`**
(`DIN-CREDITO-PISOS-HISTORIA-oro-2021.json`). D-22 ampliada: sintético con la forma
real de cada ola (CSV 2018 en minúsculas; pares DBF 2015/2012 con cabecera dBase),
`_valida_outputs` OK sobre normal y celda rara, preflight VERDE ×3 sobre el commit
de COMMIT-1 empujado (`0db0314a`) antes de abrir dato. Ejes: sexo, edad, escolaridad,
localidad y cuenta construibles en las tres olas; **formalidad construible sólo en
2018** (3.11 «Por parte de su trabajo…»); en 2015 (3.10) y 2012 (3.9) es
derechohabiencia general con Seguro Popular como código 1: NO-CONSTRUIBLE por texto
(«por parte de su trabajo»: 0 aciertos en ambos cuestionarios).

| ola | conductas | celdas | RESULT | filas persona | filas producto | tenedores | UPM en plan | BAJO-N |
|---|---|---|---|---|---|---|---|---|
| 2018 | 14 (K1, K2×3, K3, K4×5, K5×2, K6×2) | 18 | 2 100 | 12 446 | 6 001 | 4 117 | 1 908 | 0 |
| 2015 | 9 (sin K4) | 15 | 1 140 | 6 039 | 2 737 | 1 752 | 826 | 2 (K6 × 60+) |
| 2012 | 9 (sin K4; K3 sin caja) | 15 | 1 140 | 6 113 | 2 378 | 1 616 | 847 | 3 (K5-solic., K6 × 60+) |

Diagnóstico limpio en las tres: `FILTRO-SI-BATERIA-TODO-NO-N = 0`,
`TENENCIA-INDEFINIDO-N = 0`, 2012 join con TSDEM sin filas huérfanas ni llaves
duplicadas, 2015 join uno a uno, `B-VALIDAS = 10 000` en todas, coherencia
|Δ| ≤ 3.7e-09. Nacionales (18-70, **no conmensurables con el nacional 18+ de #943
sin recorte**): K1 0.275 (2012) · 0.291 (2015) · 0.312 (2018) [#943 18+: 0.313];
K3 0.304 · 0.380 · 0.386 [0.292]; K5 0.129 · 0.152 · 0.166 [0.160]; K6-PR 0.272 ·
0.305 · 0.226 [0.224]; K4A 2018 0.581 [0.591]; K4B 2018 0.258 [0.283]. **Celdas
conmensurables sin recorte** (misma edad en las cuatro olas), K1: 18-29 0.242 →
0.259 → 0.255 → 0.281; 30-44 0.322 → 0.330 → 0.369 → 0.381; 45-59 0.281 → 0.302 →
0.348 → 0.340 (IC95 en `resultados.json`). K6-P-TENEDORES 30-44 baja 0.380 → 0.421
→ 0.302 → 0.273. Toda RESULT de conducta lleva `-VEREDICTO-TEXTO` y `-MATIZ` (firma:
«entra a la serie con su matiz escrito»). Tablas de identidad
`DIN-CREDITO-PISOS-ENIF{2018,2015,2012}-metadatos-v1_0.tsv` (224 + 126 + 126 filas,
`target_edition = 2021`, `consumer = PENDIENTE:lote-prospectivo-credito-2024`).

**P3 · K8 fuera de ENIF.** `data/credito-k8-triangulacion-texto-v1_0.tsv`:
**ENSAFI 2023 `NO-ESTIMABLE`** (cuestionario de 24 páginas y FD: «destin» 0, «para
qué» 0, «último crédito» 0; 6.10.6 es un medio para cubrir gastos, no destino);
**ENFIH 2019 `CAMBIO-DE-INSTRUMENTO`** frente a K8 de mesa: destino **principal** (un
código) de **cada** crédito de nómina (8.31) y personal (8.47) vigentes —unidad PR y
respuesta única, más cerca de mesa que ENIF—, pero no «el último», sólo dos familias
y **sin «negocio» en el catálogo**. No comparables entre sí → **se mide sólo ENFIH,
por separado, rotulado, sin serie** (PARO d). `CALC-DIN-CREDITO-K8-ENFIH2019-0001`:
2 777 créditos (1 126 nómina + 1 651 personal) de 2 494 personas, 36 «No sabe» fuera
del denominador, 1 426 UPM. Nacional: consumo **0.231** [0.213, 0.250] · emergencia
0.081 [0.068, 0.094] (+salud 0.175) · refinanciar deuda 0.145 [0.132, 0.159] · alguno
de la lista de mesa 0.457 [0.434, 0.480] · vivienda 0.181 · vehículo 0.068 · salud
0.094 · educación 0.080 · otro 0.119. Nómina vs personal: consumo 0.206 vs 0.251;
vivienda 0.215 vs 0.155; lista de mesa 0.418 vs 0.488. 30/30 celdas con n ≥ 200.

**P4 · K2-bancaria, descriptivo rotulado con frontera.** La frase: *la familia
bancaria no se compara 2021↔2024 porque 6.2.2 de 2024 amplía «tarjeta de crédito
bancaria» a «u otra institución financiera» (CAMBIO-DE-INSTRUMENTO, fila K2·2024);
«bancaria +5.2 pp desde 2021» mezcla cambio de conducta con cambio de familia y no se
cita*. Entre 2012 y 2021 el ítem es idéntico (6.6.1 · 6.9.2 · 6.8.2 · 6.2.2).
`CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001` queda **congelado (COMMIT-1, preflight
VERDE, sintético D-22 sobre cuatro olas) y sin correr**: sería la quinta corrida y el
CONTADOR del encargo dice «sella hasta cuatro» → pregunta a mesa (§3). Mapa v1.1 (=
v1.0 + rol `k2_bancaria`; v1.0 intacto). ENIF 2024 no se abrió en ninguna forma.

## 2 · Cuántas olas de historia tiene cada conducta (entregable del encargo §1)

| conducta | olas comparables por texto (además de 2021) | pisos sellados | notas |
|---|---|---|---|
| K1 tenencia formal | 2012, 2015, 2018 (`CAMBIO-MENOR`) + 2024 | 3 | 18-70 hasta 2018; batería gateada por filtro |
| K2 departamental · nómina · automotriz | 2012, 2015, 2018 + 2024 | 3 | 2012 invierte bancaria/departamental |
| K2 bancaria | 2012, 2015, 2018 (texto idéntico); **2024 NO** | 0 (COMMIT-1 congelado) | frontera FP-404 (2) |
| K3 informal | 2012 (sin caja), 2015, 2018 + 2024 | 3 | 2015 reordena ítems |
| K4 motivo de no tener | 2018 + 2024 | 1 | 2012/2015 multirrespuesta |
| K5 rechazo | 2012, 2015, 2018 + 2024 (MISMO) | 3 | — |
| K6 atraso | 2012, 2015, 2018 + 2024 | 3 | 2012/2015 una variable de 5 códigos |
| K7 canal | ninguna histórica (NO-ESTIMABLE ×3) + 2024 | 0 | sólo 2021→2024 |
| K8 destino | ninguna en ENIF; ENFIH 2019 rotulado, ENSAFI NO-ESTIMABLE | 1 (ENFIH, sin serie) | FP-404 (1) |

Conmensurabilidad con #943 (18+): exacta en las celdas de edad 18-29/30-44/45-59;
`NACIONAL`, `60+`, sexo, escolaridad, localidad, cuenta y formalidad exigen recortar
2021 a 18-70 (§3).

## 3 · Preguntas a mesa (D-19: se preguntó y se siguió con lo demás)

1. **Recorte 18-70 de 2021.** 2012/2015/2018 son comparables sólo bajo el universo
   18-70, que #943 no tiene (encargo §6). Opciones: (a) sucesor que corra el mismo
   medidor sobre 2021 con `recorte_edad = 18-70` como CALC nuevo (recomendada: no
   reejecuta #943 ni lo edita; ~10 s); (b) comparar sólo las celdas de edad
   18-29/30-44/45-59 y declarar el resto no conmensurable; (c) reconstruir 2018
   como ola de referencia del lote prospectivo. `FP-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-01`.
2. **Quinta corrida (P4).** `CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001` está
   congelado y no corre por el CONTADOR «sella hasta cuatro corridas». Opciones:
   (a) autorizar la corrida en el sucesor inmediato (recomendada), (b) diferirla al
   lote prospectivo, (c) dejar sólo la frontera. `FP-…-ff56-02`.

## 4 · Premisas verificadas y lo que cayó (logística, sin PARO)

`[EXISTE]` molde #943: verificado y reproducido (oro). `[REPORTADO]` marco de #943
(FAC_ELE, EST_DIS × UPM_DIS, 10 000 PCG64(42), un plan): confirmado por bytes.
`[EJECUTADO]` ids del manifiesto: 9/9 presentes, PDFs 2/2 COINCIDE tras `--descarga`.
Cayeron por texto, no por premisa: **ENSAFI 2023 no tiene K8** (la firma FP-404
decía «se triangula en ENSAFI 2023 / ENFIH 2019»: el primer paso del encargo —«primero
por texto»— es el que lo decide; queda con una fuente); **formalidad no construible
en 2012/2015**; **2018 no trae `FAC_ELE`** (es `fac_per`; el mapa lo resuelve). El
contador «cuatro corridas» choca con cinco piezas medibles: se respetó (P4 congelado).

## 5 · Auditoría (afirma sobre México — encargo §10)

No tener crédito formal no es «preferir» el informal: K4(b) exclusión por oferta es
0.258 en 2018 y 0.283 en 2021 entre quienes nunca han tenido crédito, y K5 rechazo
0.129 → 0.166 (2012 → 2018): por eso K4(b) y K5 viajan al lado de todo marginal de
tenencia en este acto. ENIF es adulto elegido y sub-representa a quien no decide el
dinero del hogar; hasta 2018 además 18-70. ENSAFI y ENFIH tienen otro universo y otra
unidad (ENFIH: crédito vigente de la persona seleccionada) y **no se promedian con
ENIF**. Toda la evidencia es clase (a), datos primarios en México. Nada aquí es causa:
son niveles ponderados con IC por celda.

## 6 · Perímetro y pisadas

Propio: tabla v1.1 y test; 4 CALC sellados + 1 congelado con specs, mapas, tests;
filas propias de `corridas.tsv`/`resultados.tsv` (+4 653) y `replay-evidencia.tsv`
(+4); decisiones (`reserva:enif2024-credito`, `cuenta_gen2` ×4); tablas de identidad
×3; INFRAESTRUCTURA; CI (`verify.yml`, censo de guardias); cascada. **No tocado:**
`#943` y todo sello; `milpa/`; `tools/corrida0.py`; celdas-D; `marcador-segmento.tsv`;
`data/credito-comparabilidad-texto-v1_0.tsv`; mapa v1.0 tras su sello; ENIF 2024;
`envipe2026*`. Pisada ajena en las vistas: ninguna (diferencia de conjuntos contra
HEAD: sólo filas propias añadidas o re-derivadas).

Hallazgo de método: `Write` de un TSV desde el cliente recorta las celdas vacías
finales de cada fila (T-INFRA/tests lo atrapan); se rellenó a 9 columnas por script.
