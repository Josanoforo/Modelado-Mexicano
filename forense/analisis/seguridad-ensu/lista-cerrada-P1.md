# Lista cerrada P1 · ENSU 2013T3–2025T4 · conductas por texto de pregunta

`ACTO GEN2-SEGURIDAD-ENSU-SERIE-1` · 25/sep/2026 · CAJA · rama `gen2-seguridad-ensu-serie-1` ·
0-bis `591689ab`. Parte de la spec `forense/prereg-caja/ENSU-SERIE-spec-v1_0.md` (COMMIT-1).
Escrita **antes** de leer un solo valor de microdato ENSU: sólo descriptores (FD) y nombres de
columna. Exposición declarada en la spec §0.

## 1 · Payloads por identidad (A.15, manifiesto por id)

`data/manifiesto.yaml`: 30 entradas cuyo id o archivo contiene `ensu` (13 bases de datos
2013–2025, 13 FD, el DDI 2025, dos entradas de 2026 y una de Banxico que sólo casa por
subcadena). El «164» del encargo cuenta **menciones** de `ensu` en el texto del manifiesto, no
payloads (comando: `grep -ic ensu data/manifiesto.yaml` → 164). Bases de datos usadas, una por
año, verificadas en disco:

| año | id del manifiesto | trimestres con tabla CB |
|---|---|---|
| 2013 | `cc1_inegi_ensu_2013__ensu_bd_2013_dbf` | T3, T4 (ENSU arranca en sep 2013) |
| 2014–2019 | `cc1_inegi_ensu_<año>__ensu_bd_<año>_dbf` | T1–T4 |
| 2020 | `cc1_inegi_ensu_2020__ensu_bd_2020_dbf` | T1, T3, T4 (T2 cancelado por COVID-19, FD sep 2020) |
| 2021 | `cc1_inegi_ensu_2021__ensu_bd_2021_csv` | T2, T3, T4 |
| 2022–2023 | `cc1_inegi_ensu_<año>__ensu_bd_<año>_csv` | T1–T4 |
| 2024 | `ensu2024_bd_csv_zip` | T1–T4 |
| 2025 | `ensu2025_bd_csv_zip` | T1–T4 |

**2021T1 NO-ENCONTRADO en la publicación de INEGI:** el zip anual publicado hoy
(`https://www.inegi.org.mx/contenidos/programas/ensu/microdatos/ensu_bd_2021_csv.zip`, bajado en
esta sesión a `$TMPDIR`, sha256 `ce04637d…fbda`) es **idéntico** al del corpus y trae sólo
junio, septiembre y diciembre; la URL por trimestre `ensu_bd_marzo_2021_csv.zip` responde 200 con
2 263 bytes (página, no zip). El FD de marzo 2021 sí existe. No es hueco del corpus sino de la
publicación: se asienta, no se adquiere.

**2026 RESERVADO (E.6, F-ASTRA-5-3):** `cc1_inegi_ensu_2026__ensu_bd_2026_csv` y su FD llevan
`estado_reserva: RESERVADA-NO-ABIERTA-NO-INDEXAR-L` y no están en disco;
`tabla-final-v1_0.tsv` los lista en `olas_reservadas_al_entrar`. El medidor para si una ruta
resuelve a 2026. Último trimestre abierto: **2025T4**.

## 2 · Tres eras de cuestionario (por nombre de columna y FD)

| era | trimestres | reactivos | llave CB→CS para sexo/edad | ponderador · estrato · UPM |
|---|---|---|---|---|
| E1 | 2013T3–2015T4 | `P1`, `P3_x`, `P4_x` | `ENT CON V_SEL N_HOG H_MUD N_REN` → CS `SEX EDA` | `FACTOR` · `CD`+`EDIS` · `UPM_DIS` |
| E2 | 2016T1–2020T4 | `BP1_*`, `BP3_*` | `UPM VIV_SEL H_MUD R_SEL` → CS `UPM VIV_SEL H_MUD N_REN`, `SEX` y `EDA`/`EDAD` | `FAC_SEL` · `CD`+`EST_DIS` · `UPM_DIS` |
| E3 | 2021T2–2025T4 | `BP1_*`, `BP3_*` | `SEXO`, `EDAD` en CB | igual que E2 |

Entidad: E1 `ENT`; E2/E3 los dos primeros dígitos de `UPM` (FD: «0100001,…,3299999»).
2020T3 publica la CB en dos tablas; se usa `ENSU_CB_sec1_2_3_0920` (secciones 1–3), la de la
sección 4 no lleva reactivos de esta lista.

## 3 · Conductas (texto del FD ENSU 2025T3 salvo que se diga; unidad: persona 18+ urbana)

Proporción ponderada. «Sí» = numerador; «universo» = denominador; el resto de códigos
(blanco, fuera de catálogo) sale del universo.

| id | reactivo 2016+ / 2013–15 | texto | sí | universo | disponible |
|---|---|---|---|---|---|
| C01-INSEG-CIUDAD | `BP1_1` / `P1` | 1.1 En términos de delincuencia, ¿considera que vivir actualmente en (CIUDAD), es… 1 seguro? 2 inseguro? 9 NS/NR | 2 | 1,2,9 | 2013T3–2025T4 |
| C02-INSEG-CALLE | `BP1_2_03` | 1.2 En términos de delincuencia, dígame si en (LUGAR) se siente seguro(a) o inseguro(a). — la calle | 2 | 1,2,9 (3 No aplica fuera) | 2016T2–2025T4 |
| C03-INSEG-CAJERO | `BP1_2_08` | 1.2 … — el cajero automático localizado en la vía pública | 2 | 1,2,9 | 2016T2–2025T4 |
| C04-INSEG-TRANSPORTE | `BP1_2_09` | 1.2 … — el transporte público | 2 | 1,2,9 | 2016T2–2025T4 |
| C05-EXPECT-EMPEORA | `BP1_3` | 1.3 Pensando en las condiciones de delincuencia en (CIUDAD), ¿considera que en los próximos 12 meses… 1 mejorará? 2 seguirá igual de bien? 3 seguirá igual de mal? 4 empeorará? | 4 | 1,2,3,4,9 | 2016T1–2025T4 |
| C06-TESTIGO-ROBOS | `BP1_4_3` / `P3_3` | 1.4 En los últimos tres meses, ¿ha escuchado o ha visto en los alrededores de su vivienda situaciones como… robos o asaltos? | 1 | 1,2,9 | 2013T3–2025T4 |
| C07-TESTIGO-PANDILLAS | `BP1_4_4` / `P3_4` | 1.4 … bandas violentas o pandillerismo? | 1 | 1,2,9 | 2013T3–2025T4 |
| C08-TESTIGO-DISPAROS | `BP1_4_6` / `P3_6` | 1.4 … disparos frecuentes con armas? | 1 | 1,2,9 | 2013T3–2025T4 |
| C09-HABITO-OBJETOS-VALOR | `BP1_5_1` / `P4_1` | 1.5 En este mismo periodo de tres meses, por temor a sufrir algún delito (robo, asalto, secuestro, entre otros), ¿usted cambió sus hábitos respecto a… llevar cosas de valor como joyas, dinero o tarjetas de crédito? | 1 | 1,2,3,9 | 2013T3–2025T4 |
| C10-HABITO-CAMINAR-NOCHE | `BP1_5_2` / `P4_2` | 1.5 … caminar por los alrededores de su vivienda, pasadas las ocho de la noche? | 1 | 1,2,3,9 | 2013T3–2025T4 |
| C11-HABITO-VISITAR | `BP1_5_3` / `P4_3` | 1.5 … visitar a parientes o amigos(as)? | 1 | 1,2,3,9 | 2013T3–2025T4 |
| C12-HABITO-MENORES | `BP1_5_4` / `P4_4` | 1.5 … permitir que los (las) menores de edad que viven en el hogar salgan solos(as)? (E1: «permitir que salgan de su vivienda sus hijos menores?») | 1 | 1,2,3,9 | 2013T3–2025T4 |
| C13-POLICIA-MUN-CONFIANZA | `BP1_9_1` | 1.9 ¿Cuánta confianza le inspira la (el) Policía Preventiva Municipal? 1 Mucha 2 Algo de confianza 3 Algo de desconfianza 4 Mucha desconfianza | 1,2 | 1,2,3,4,9 (blanco = no la identifica, fuera) | 2017T1–2025T4 |
| C14-POLICIA-MUN-EFECTIVA | `BP1_8_1` | 1.8 ¿Qué tan efectivo considera el desempeño de la (del) Policía Preventiva Municipal? 1 Muy 2 Algo 3 Poco 4 Nada efectivo | 1,2 | 1,2,3,4,9 (blanco fuera) | 2016T3–2025T4 |
| C15-CORRUPCION-POLICIA | `BP3_6` si `BP3_5`=1 | 3.6 En los últimos seis meses, ¿la policía u otras autoridades de seguridad pública le insinuó, le pidió de forma directa o generó las condiciones para que les diera dinero, un regalo o favor para agilizar, aprobar, o bien, evitar infracciones o detenciones? — entre quienes en 3.5 tuvieron contacto directo con policías o autoridades de seguridad pública. [trimestre II y IV] | 1 | `BP3_5`=1 y `BP3_6` ∈ 1,2,9 | 2019T2, 2019T4, 2020T3, 2020T4, 2021T2, 2021T4, … 2025T4 (14) |

**Reserva ETIQUETA-INFERIDA-E1.** Los FD 2013 y 2015 dan rangos (`1, 2, 9`; `1 - 3, 9`) pero no
etiquetas de código. Se toma la etiqueta del mismo texto de pregunta en el FD 2016 (1 Sí/seguro,
2 No/inseguro, 3 No aplica, 9 NS). `P2` (expectativa, cuatro categorías ordinales) **no** entra en
E1: su orden no es verificable por texto. Mismo trato en la nota: toda cifra E1 lleva la reserva.

**Denominadores.** C01 y C05–C12 dejan «NS/NR» y «No aplica» en el denominador, que es la
convención de los comunicados ENSU («porcentaje de la población de 18 años y más»); C02–C04
sacan «No aplica» (no usa ese lugar). Declarado para el cotejo contra los reports (Bloque C).

## 4 · Segmentos

SEXO (`HOMBRE`, `MUJER`) · EDAD (`18-29`, `30-44`, `45-59`, `60-MAS` = 60–96; 98/99 «no
especificada» fuera del eje; `60-MAS` es el segmento VEJEZ del encargo) · ENT (`01`–`32`) ·
CIUDAD (`CD` `01`–`96`, unión de los catálogos del FD 2016 —01–54— y del FD 2025T4 —01–14,
19–23, 25–33, 35–96—). E1 no trae catálogo de ciudades en su FD (sólo «01–43 Ciudad
Autorepresentada»): **sin eje CIUDAD en 2013–2015**. Escolaridad, formalidad, NSE: ENSU no los
capta en CB → NO-CONSTRUIBLE (spec §7). Región: ENSU no trae regionalización y el repo no tiene
una oficial para ENSU → se segmenta por ENT y CIUDAD; región NO-CONSTRUIBLE sin inventar una.

**Códigos de ciudad (A.15, por texto):** 01–54 nombran las mismas ciudades en los FD 2016T1 y
2025T4 (Campeche → San Francisco de Campeche, León → León de los Aldama, etc., mismo nombre
propio); **excepción marcada: `07` Torreón (2016) → La Laguna (2025)**, posible redefinición de
área (auditoría). 15–18 (DF Norte/Sur/Oriente/Poniente), 24 (Guadalajara) y 34 (Monterrey)
desaparecen en 2025: se partieron en alcaldías/municipios con código nuevo (71–86, 59–63, 64–70).
Una serie de ciudad termina cuando su código deja de aparecer.

## 5 · Afirmaciones del mapa que esta lista cubre (cola v1.1)

| afirmación | conducta(s) | trimestre citado |
|---|---|---|
| ASTRA5-U0-VIOL-001 | C09–C12 | 2025T3, 2025T4 |
| ASTRA5-U0-VIOL-003 | C01 | 2025T3 |
| ASTRA5-U0-VIOL-014 | C01 y C03 por SEXO | 2025T3 |
| ASTRA5-U0-VIOL-035 | C01 por CIUDAD | 2025T3 |
| ASTRA5-U0-VIOL-038 | C15 | sin ola (se mide 2025T4, la última abierta; serie 2019T2+) |
| ASTRA5-U0-INTER-034 | C01, C09, C10 | 2024T1 |
| ASTRA5-U0-SANC-007 | C09 | 2024T1 |
