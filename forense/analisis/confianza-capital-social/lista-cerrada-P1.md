# Lista cerrada P1 · ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1

Congelada en el COMMIT-1 (25/sep/2026), **antes** de abrir un solo valor de microdato de WVS,
Latinobarómetro, PEW o LAPOP para estos reactivos. Fuente de cada reactivo: el texto de la
pregunta (A.15), leído de las etiquetas de variable y de valor (`pyreadstat`,
`metadataonly=True`) y de los cuestionarios; informes de estructura en esta carpeta
(`estructura-{wvs,latinobarometro,pew,lapop}.md`, hechos por agentes Sonnet sólo con metadatos) y
**auditoría propia** de todos los códigos que se usan abajo (la sesión releyó con
`metadataonly=True` cada variable citada abajo, archivo por archivo). Cambiar esta lista
después del COMMIT-1 es PARO (d).

## 0 · Dominios del mapa y alcance

Mapa: `canon/mapa-dominios-v1_0.tsv`. Dominios del encargo: CONFIANZA (59 afirmaciones),
CAPITAL_SOCIAL (30), RELIGIOSIDAD (39), AUTORIDAD (39), EMOCIONES_MORALES (26; «sólo lo
medible»). **VALORES no es un dominio del mapa** (0 filas con `dominio = VALORES`; el
recuento: `csv.DictReader` sobre `canon/mapa-dominios-v1_0.tsv`, 1 396 filas, columna `dominio`): los reactivos de valores que el
encargo nombra (tolerancia, costumbres vs. diversidad, cualidades infantiles) se asignan aquí a
AUTORIDAD o CONFIANZA según el report que los cita. EMOCIONES_MORALES: ningún reactivo de
culpa, vergüenza o dignidad existe en los cuatro instrumentos con texto de emoción (búsqueda
en los cuatro informes de estructura); no se mide aquí (NC).

## 1 · Olas abiertas y reservadas (E.6)

| instrumento | olas con microdato en corpus (id de manifiesto) | reservada | se abre aquí |
|---|---|---|---|
| WVS | 2018 (`f00013084_wvs_wave_7_mexico_stata_v5_1`) | — (una sola ola: no hay historia que reservar; se abre y se declara) | 2018 |
| Latinobarómetro | 2023 (`latinobarometro2023_bd_stata_zip`), 2024 (`latinobarometro2024_bd_stata`) | **2024** | 2023 |
| PEW Global Attitudes | 2013, 2015, 2017, 2018, 2023, 2024, 2025 (`pew_gas_spring<año>`) | **2025** | 2013, 2015, 2017, 2018, 2023, 2024 |
| LAPOP | 2004, 2006, 2019, 2021, 2023 | **2023** (para los reactivos de este acto; sus marginales nacionales de `b18`/`b21`/`eff`/`pol1`/`d1–d4` ya están sellados por ASTRA5-U3 y se citan) | 2004, 2006, 2019 |

**LAPOP 2021 fuera (declarado):** telefónica CATI con RDD móvil (ruptura de modo y población
ya dictaminada en `forense/prereg-caja/LAPOP-PISOS-OLAS-spec-v1_0.md`), y el archivo no trae
`q1`, `ed`, `ur` bajo esos nombres y, de los reactivos de esta lista, sólo conserva `b12`,
`b13` y `jc13` (informe de estructura §3) → NC.

**Ninguna ola reservada se abre ni se nombra como input.** Los agentes de estructura no
abrieron Latinobarómetro 2024, PEW 2025 ni LAPOP 2023 (sólo leyeron el TEXTO de los
cuestionarios 2023/2024 para comparar redacción). Los medidores de PEW y LAPOP traen una
guardia que PARA si un payload reservado aparece entre los inputs (prueba de mutación en
`tests/test_confianza_pisos_gen2.py`).

## 2 · Regla común de recodificación

Cada conducta es `bin(col, UNO, CERO)` → 1 si el código ∈ UNO, 0 si ∈ CERO, **fuera** en otro
caso (no sabe, no responde, no aplica, faltante extendido de Stata `.a/.b/.c`, códigos 8/88/98/99
y todo lo no listado); o `media(col, lo, hi)` → el valor si está en [lo, hi], fuera si no.
Universo: personas de **18 años o más** (edad declarada) con peso válido y diseño válido.
Estimando: razón ponderada Σw·y/Σw (proporción o media). **Unidad: persona.** Cada instrumento
se reporta en su escala; ninguna cifra se compara entre instrumentos sin función de enlace
(§4 v2.16; dictamen de equivalencia en §6).

## 3 · Conductas por instrumento

### WVS 2018 → `CALC-WVS-PISOS-2018-0001`

Diseño: peso `W_WEIGHT`; UPM `I_PSU`; **sin estrato en el archivo público** (la ficha de diseño
dice estratificación urbano-rural-mixto por el INE, pero la variable no viaja) → bootstrap de UPM
con un solo estrato. Ejes, uno a la vez: SEXO (`Q260` 1/2) · EDAD (`Q262`: 18–29 / 30–44 /
45–59 / 60+) · ESCOLARIDAD (`Q275` ISCED 2011: HASTA-PRIMARIA {0,1}, SECUNDARIA {2},
MEDIA-SUPERIOR {3,4}, SUPERIOR {5–8}) · TAMLOC (`G_TOWNSIZE2`: <5 mil {1}, 5–20 mil {2},
20–100 mil {3}, 100–500 mil {4}, 500 mil+ {5}) · INGRESO-SUBJETIVO (`Q288R` bajo/medio/alto).

| conducta | var | texto (cuestionario MX 2018) | 1 | 0 |
|---|---|---|---|---|
| CONFIANZA-INTERPERSONAL | Q57 | «¿diría usted que se puede confiar en la mayoría de las personas o que se tiene que ser muy cuidadoso…?» | 1 | 2 |
| CONFIA-FAMILIA / -VECINOS / -CONOCIDOS / -DESCONOCIDOS | Q58–Q61 | «¿…si usted confía completamente, algo, no mucho o nada…?» su familia / sus vecinos / sus conocidos / gente que conoce por primera vez | 1, 2 | 3, 4 |
| CONFIA-IGLESIAS / -EJERCITO / -POLICIA / -TRIBUNALES / -GOBIERNO / -PARTIDOS / -CONGRESO / -ELECCIONES | Q64, Q65, Q69, Q70, Q71, Q72, Q73, Q76 | «¿…cuánta confianza tiene usted en…: mucha, algo, poca o nada?» | 1, 2 | 3, 4 |
| MIEMBRO-ORG-RELIGIOSA | Q94 | «Iglesia u organización religiosa: miembro activo, miembro no activo, no pertenece» | 1, 2 | 0 |
| MIEMBRO-ACTIVO-ORG-RELIGIOSA / -ORG-DEPORTIVA / -PARTIDO / -AYUDA-MUTUA | Q94, Q95, Q98, Q103 | ídem (religiosa, deportiva o recreativa, partido político, grupo de auto-ayuda o ayuda mutua) | 2 | 0, 1 |
| RELIGION-MUY-IMPORTANTE | Q6 | «…qué tan importante es en su vida… la religión» | 1 | 2, 3, 4 |
| IMPORTANCIA-DE-DIOS | Q164 | «¿Qué tan importante es Dios en su vida? 10 muy importante, 1 nada» | media 1–10 | |
| ASISTE-SERVICIO-MENSUAL | Q171 | «Dejando aparte bodas, funerales, bautismos… ¿con qué frecuencia asiste a servicios religiosos?» | 1, 2, 3 (más de 1×sem., 1×sem., 1×mes) | 4–7 |
| PERSONA-RELIGIOSA | Q173 | «Independientemente de si va o no a la iglesia, ¿diría que usted es…?» | 1 | 2, 3 |
| PERTENECE-DENOMINACION | Q289 | «¿Pertenece usted a alguna religión o denominación religiosa?» | 1–7 | 0 |
| CATOLICO | Q289 | ídem | 1 | 0, 2–7 |
| OBEDIENCIA-CUALIDAD-INFANTIL | Q17 | «…cualidades que pueden fomentarse en el hogar… especialmente importante… Obediencia» | 1 mencionó | 2 |
| MAS-RESPETO-AUTORIDAD-BUENO | Q45 | «…cambios… Mayor respeto por la autoridad: bueno, le da igual, malo» | 1 | 2, 3 |
| LIDER-FUERTE-BUENO | Q235 | «Tener un líder fuerte que no se moleste por el congreso y las elecciones» | 1, 2 | 3, 4 |
| GOBIERNO-MILITAR-BUENO | Q237 | «Tener un gobierno militar» | 1, 2 | 3, 4 |
| RECHAZA-VECINO-HOMOSEXUAL | Q22 | «…aquellos que usted preferiría NO tener como vecinos… Homosexuales» | 1 mencionó | 2 |
| HOMOSEXUALIDAD-JUSTIFICABLE | Q182 | «…si cree usted que siempre puede justificarse, nunca… La homosexualidad» (1 nunca … 10 siempre) | media 1–10 | |
| FIRMO-PETICION / ASISTIO-MANIFESTACION | Q209, Q211 | «…formas de acción política… la ha hecho, la podría hacer, nunca la haría» | 1 | 2, 3 |

`Q289`: el cuestionario en español lista «8) Otros (anotar)»; las etiquetas Stata sólo traen
0–7. Un código fuera de 0–7 queda **fuera** (no se imputa a ninguna religión); el conteo de
fuera por conducta sale en `-N` contra el total.

### Latinobarómetro 2023 (México) → `CALC-LATINOBAROMETRO-PISOS-2023-0001`

Filas `idenpa = 484`. Diseño: peso `wt`; **sin estrato ni UPM en el archivo** (búsqueda
`estrat|upm|psu|conglom|cluster|segmento` sobre 274 columnas: sólo `wt`) → bootstrap ponderado
de entrevistas («MAS-PONDERADO»), declarado como **cota inferior** de la varianza de diseño.
Ejes: SEXO (`sexo`) · EDAD (`edad`) · ESCOLARIDAD (`REEEDUC_1`: HASTA-BASICA {1 analfabeto,
2 básica incompleta, 3 básica completa}, MEDIA {4, 5}, SUPERIOR {6, 7}; 0 «sin dato» fuera) ·
TAMLOC (`tamciud`: <20 mil {1–3}, 20–100 mil {4–6}, 100 mil+ {7, 8 capital}) · CLASE-SUBJETIVA
(`S2`: alta/media-alta {1,2}, media {3}, media-baja {4}, baja {5}).

| conducta | var | texto | 1 | 0 |
|---|---|---|---|---|
| CONFIANZA-INTERPERSONAL | P9STGBS | «¿…se puede confiar en la mayoría de las personas o uno nunca es lo suficientemente cuidadoso…?» | 1 | 2 |
| CONFIA-FFAA / -POLICIA / -IGLESIA / -CONGRESO / -GOBIERNO / -PODER-JUDICIAL / -PARTIDOS / -INSTITUCION-ELECTORAL / -PRESIDENTE | P13STGBS_A, _B, P13ST_C … _I | «¿…cuánta confianza tiene usted en…: mucha, algo, poca, ninguna?» | 1, 2 | 3, 4 |
| CATOLICO | S1 | «¿Cuál es su religión?» | 1 | 2–14, 96, 97 |
| SIN-RELIGION | S1 | ídem | 13 agnóstico, 14 ateo, 97 ninguna | 1–12, 96 |
| PRACTICANTE | S1A | «Práctica religiosa» (muy practicante … no practicante) | 1, 2 | 3, 4 |
| DEMOCRACIA-PREFERIBLE | P10STGBS | «…la democracia es preferible a cualquier otra forma de gobierno / en algunas circunstancias un gobierno autoritario… / nos da lo mismo» | 1 | 2, 3 |
| AUTORITARISMO-A-VECES-PREFERIBLE | P10STGBS | ídem | 2 | 1, 3 |
| NO-IMPORTA-GOBIERNO-NO-DEMOCRATICO | P18STM_B | «No me importaría que un gobierno no democrático llegara al poder si resuelve los problemas» | 1, 2 (de acuerdo) | 3, 4 |
| APOYARIA-GOBIERNO-MILITAR | P20STM | «Apoyaría a un gobierno militar… si las cosas se ponen muy difíciles / en ninguna circunstancia» | 1 | 2 |
| PREFIERE-SOCIEDAD-DE-COSTUMBRES | P19N | «Prefiero una sociedad que defienda nuestras costumbres / abierta a la diversidad» | 1 | 2 |
| TRABAJA-POR-COMUNIDAD | P44ST_B | «Frecuencia en que trabaja por un tema que lo afecta a Ud. o a su comunidad» | 1, 2 (muy frec., frec.) | 3, 4 |
| FIRMO-PETICION / ASISTIO-MANIFESTACION | P45ST_A, P45S_B | «Acción política: firmar una petición / asistir a manifestaciones autorizadas» | 1 la ha realizado | 2, 3 |

`S1A` en 2023 no trae un código «sin religión»: la persona sin religión queda fuera por salto
(el universo de PRACTICANTE es «con religión declarada», declarado).

### PEW Global Attitudes 2013–2024 (México) → `CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001`

Filas de México por país: 2013 `COUNTRY`=25 · 2015 `COUNTRY`=21 · 2017 `Country`=20 · 2018
`COUNTRY`=15 · 2023 `country`=24 · 2024 `country`=35. Diseño por ola: 2013 peso `WEIGHT`, sin
estrato/UPM · 2015 `WEIGHT`, estrato `STRATUM_MEX`, UPM `PSU` · 2017 y 2018 `weight`,
`STRATUM_MEX`, `PSU_MEX` · 2023 y 2024 `weight`, sin estrato/UPM (sólo `region_mexico`, que
no se declara estrato). **Regla fijada antes de abrir:** si la UPM declarada de una ola tiene
algún faltante en filas de México, esa ola se estima sin conglomerados (estratificada si hay
estrato); la etiqueta `-G-DISENO` lo dice. Ejes: SEXO (2013 `Q164`, 2015 `Q145`, 2017/18/23
`sex`, 2024 `gender`; 1/2) · EDAD (2013 `Q165`, 2015 `Q146`, resto `age`; 97+ entra como 97,
98/99 fuera) · ESCOLARIDAD sólo 2017+ (`d_educ_mexico_2017` 2017/18, `d_educ_mexico` 2023/24;
HASTA-PRIMARIA {1–3}, SECUNDARIA {4, 5}, MEDIA-SUPERIOR {6–9}, SUPERIOR {10–12}).

*Nota de auditoría:* el informe de estructura dijo que 2013 y 2015 no tienen edad; la
auditoría encontró `Q165`/`Q146` «How old were you at your last birthday?». Se usan.

| conducta | variable por ola | texto | 1 | 0 | olas |
|---|---|---|---|---|---|
| RELIGION-MUY-IMPORTANTE | Q178 / Q152 / religion_import | «How important is religion in your life – very, somewhat, not too, not at all important?» | 1 | 2, 3, 4 | 2013, 15, 17, 18, 23, 24 — **texto idéntico** |
| ORA-DIARIO | Q176 / Q151 (5 cat.) · pray_several (7 cat.) | 2013/15: «…do you pray several times a day, once a day, a few times a week, once a week or less, or never?» · 2017: «Aside from religious services, do you pray ___?» · 2018/23: «How often do you pray in normal days aside from religious services…?» | 1, 2 (varias al día, una al día) | resto | 2013, 15, 17, 18, 23 — **escala y texto cambian: sin serie** |
| CONFIANZA-INTERPERSONAL | trustpeople | «…most people can be trusted or that you can't be too careful…» | 1 | 2, 3 (otra/ambas, voluntaria) | 2017 |
| CONFIA-GOBIERNO-NACIONAL | trust_gov | «How much do you trust the national government to do what is right…» 2017: a lot/somewhat/not much/not at all; 2024: a lot/some/not too much/not at all | 1, 2 | 3, 4 | 2017, 2024 — **texto cambia: sin serie** |
| GOBIERNO-MILITAR-BUENO / LIDER-FUERTE-BUENO / EXPERTOS-DECIDEN-BUENO | polsys_junta / _autocracy / _technocracy | «…would it be a very good, somewhat good, somewhat bad or very bad way of governing this country? the military rules / a strong leader can make decisions without interference from parliament or the courts / experts, not elected officials, make decisions» | 1, 2 | 3, 4 | 2017, 2023, 2024 — **texto idéntico** |

Series con IC calibrado de persistencia (≥ 3 olas, texto idéntico): RELIGION-MUY-IMPORTANTE
(6 olas; ejes TOTAL, SEXO, EDAD) y las tres de sistemas de gobierno (2017→2023→2024; ejes
TOTAL, SEXO, EDAD, ESCOLARIDAD). τ² = media de Δ² en logit entre olas **consecutivas de la
lista** (no años consecutivos), sin centrar; IC calibrado aplicado a 2024. Parámetro
reutilizable; aquí no se evalúa contra ninguna R.

### LAPOP 2004 / 2006 / 2019 → `CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001`

Diseño por ola, idéntico al de `LAPOP-PISOS-OLAS-spec-v1_0.md` (ASTRA5-U3): 2004 peso 1,
estrato `mestrat`, UPM `mprov`×`msec` · 2006 peso 1, `ESTRATOPRI`, `UPM` · 2019 `wt`,
`estratopri`, `upm`. Ejes: SEXO (`q1`) · EDAD (`q2`) · ESCOLARIDAD (`ed`, años aprobados:
0–6 HASTA-PRIMARIA, 7–9 SECUNDARIA, 10–12 MEDIA-SUPERIOR, 13+ SUPERIOR; 88 fuera) · UR (`ur`
1 urbano / 2 rural). Cortes de escala: los mismos que la spec sellada fijó para b18/b21 (6 ó 7
de 1–7) y d1–d4 (6–10 de 1–10), para no elegir umbral por reactivo.

| conducta | var | texto | 1 | 0 | olas |
|---|---|---|---|---|---|
| CONFIANZA-INTERPERSONAL | it1 | «…¿diría que la gente de su comunidad es muy, algo, poco o nada confiable?» | 1, 2 | 3, 4 | 04, 06, 19 |
| CONFIA-FFAA / -CONGRESO / -IGLESIA-CATOLICA / -MEDIOS | b12, b13, b20, b37 | «¿Hasta qué punto tiene confianza en…?» (1 nada … 7 mucho) | 6, 7 | 1–5 | 04, 06, 19 |
| CONFIA-JUSTICIA / -GOBIERNO | b10a, b14 | ídem (sistema de justicia; gobierno nacional) | 6, 7 | 1–5 | 04, 06 |
| ASISTE-ORG-RELIGIOSA / -ASOC-PADRES / -COMITE-MEJORAS / -PARTIDO | cp6, cp7, cp8, cp13 | «¿Asiste a reuniones de…? una vez a la semana, una o dos veces al mes, una o dos veces al año, nunca» | 1, 2 | 3, 4 | 04, 06, 19 |
| ASISTE-ASOC-PROFESIONAL | cp9 | ídem (asociación de profesionales, comerciantes, productores) | 1, 2 | 3, 4 | 04, 06 |
| AYUDO-RESOLVER-PROBLEMA-COMUNIDAD | cp5 | «¿En el último año usted ha contribuido… para la solución de algún problema de su comunidad…?» | 1 | 2 | 04, 06 |
| GOLPE-JUSTIFICADO-DELINCUENCIA / -CORRUPCION | jc10, jc13 | «¿se justificaría que hubiera un golpe de estado por los militares frente a mucha delincuencia / corrupción?» | 1 | 2 | 04, 06, 19 |
| LIDER-FUERTE-NO-ELEGIDO | aut1 | «…necesitamos un líder fuerte que no tenga que ser elegido… / la democracia electoral es lo mejor» | 1 | 2 | 04, 06 |
| APRUEBA-JUSTICIA-PROPIA-MANO | e16 | «¿Con qué firmeza aprobaría… que las personas hagan justicia por su propia mano cuando el Estado no castiga…?» (1–10) | 6–10 | 1–5 | 04, 06 |
| APRUEBA-HOMOSEXUALES-CANDIDATOS | d5 | «¿Con qué firmeza aprueba… que los homosexuales puedan postularse para cargos públicos?» (1–10) | 6–10 | 1–5 | 04, 06, 19 |
| RELIGION-MUY-IMPORTANTE | q5b | «¿qué tan importante es la religión en su vida?» | 1 | 2, 3, 4 | 19 |
| ASISTE-SERVICIO-MENSUAL | q5a | «Asistencia a servicios religiosos» (más de 1×sem., 1×sem., 1×mes, 1–2×año, nunca) | 1, 2, 3 | 4, 5 | 19 |

2006 `e16` y `d5` sólo traen la etiqueta del código 88; la escala 1–10 se sostiene por el texto
idéntico a 2004 y por el diseño «idéntico a 2004». Si 2006 trae valores fuera de 1–10 que no
sean 88, quedan fuera y se ven en `-N` (no se recodifican).

## 4 · Lo que ya está sellado y se cita, no se re-mide (E.5)

- ENBIARE 2021 (#1124, `CALC-ENBIARE-PISOS-BIENESTAR-0001`): confianza 0–10 en la mayoría de la
  gente, en gente conocida, en policía municipal y en partidos; apoyo de familia/amistades;
  tiene religión; asiste a servicio religioso.
- LAPOP nacional (ASTRA5-U3, `CALC-LAPOP-PISOS-{2004,2006,2019-0002,2021,2023}-0001`):
  `b18` (policía), `b21` (partidos), `eff1/eff2`, `pol1`, `d1–d4`, `clien1n`.
- ENCUP 2012 (`CALC-ENCUP-PISOS-2012-0001/0003`): confianza 0–10 en IFE, vecinos y otras.
- ENCIG: **ningún CALC sellado mide confianza en instituciones** (premisa del encargo `[EJECUTADO]`
  que no se sostiene: `grep -oi '"RESULT[^"]*CONFIA[^"]*"'` sobre los `resultados.json` de los 41
  directorios `data/corrida0/*ENCIG*` da 0 ids). No se mide aquí (ENCIG fuera del perímetro §9) → NC.

## 5 · Reglas que no cambian con el resultado

- No se construye serie entre instrumentos. Dentro de un instrumento, sólo las series marcadas
  «texto idéntico» (PEW) llevan τ²; LAPOP no lleva serie (FIRMAS-15 T).
- `n < 1` en una celda → sin estimación (el conducto publica `null`). No hay umbral de n para
  publicar: el IC dice el tamaño. Una réplica degenerada → sin EE ni IC (contrato conservador).
- Semilla por CALC, 2 000 réplicas, percentiles 2.5/97.5.

## 6 · Dictamen de equivalencia textual (por ola, vocabulario cerrado)

`IDÉNTICO` · `CAMBIA-TEXTO` · `CAMBIA-ESCALA` · `CAMBIA-OBJETO` · `AUSENTE`. Sólo `IDÉNTICO`
en ≥ 3 olas abre serie (y sólo dentro del instrumento).

| instrumento | reactivo | dictamen |
|---|---|---|
| PEW | importancia de la religión | IDÉNTICO 2013–2024 (6 olas) |
| PEW | sistemas de gobierno (3) | IDÉNTICO 2017, 2023, 2024 |
| PEW | oración | CAMBIA-ESCALA 2013/15 → 2017+; CAMBIA-TEXTO 2017 → 2018/23; 2024 CAMBIA-TEXTO (no se usa) |
| PEW | confianza en gobierno nacional | CAMBIA-TEXTO 2017 → 2024 (categorías «somewhat/not much» → «some/not too much») |
| LAPOP | it1, b12, b13, b20, b37, cp6, cp7, cp8, cp13, jc10, jc13, d5 | IDÉNTICO 2004–2006; 2019 texto de etiqueta corto con mismo objeto y escala; **sin serie hasta dictamen de mesa (FIRMAS-15 T)** |
| LAPOP | d6 | CAMBIA-OBJETO 2004 (salir en TV) vs 2019/2023 (matrimonio) — no se usa |
| Latinobarómetro | todos | una ola abierta; 2024: P9→P10 IDÉNTICO, P13 A–I → P14 A–N CAMBIA-TEXTO (batería ampliada), P19N/P20STM/P44/P45 AUSENTE |
| WVS | todos | una ola |
