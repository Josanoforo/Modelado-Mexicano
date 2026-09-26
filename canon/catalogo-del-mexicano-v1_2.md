# Benchmark auditable del comportamiento del mexicano · catálogo v1.2

> | | |
> |---|---|
> | **ARCHIVO** | `catalogo-del-mexicano-v1_2.md` (sucesor de `catalogo-del-mexicano-v1_1.md`; v1.0 y v1.1 quedan intactos — E.1) |
> | **NOMBRE ESTABLE** | `catálogo del mexicano` |
> | **ESTADO** | Producto consultable: solo estimadores adoptados por firma citada por id |
> | **ACTO** | `GEN2-CIERRE-SEMANAL-1` (P1; ejecuta la adopción de FIRMAS-19, «EJECUTA: GEN2-CATALOGO-V1-2-1») · generación GEN2 · cero mediciones nuevas · no adopta: consume adopciones firmadas |
> | **TABLA** | [`catalogo-del-mexicano-v1_2.tsv`](catalogo-del-mexicano-v1_2.tsv) — una fila por estimador adoptado |
> | **REGENERA** | `python3 forense/analisis/catalogo/genera_catalogo_v1_2.py` (esta portada incluida); `--sin-registro` reutiliza la vista de adoptados activos ya derivada |

**43 188 estimadores adoptados con RESULT sellado · 13 dominios del mapa medidos, en 14 de los 31 reports del corpus · 219 celdas validadas (definición vigente de `corrida0 status`), de las cuales 20 PROSPECTIVAS y 59 RETROSPECTIVAS se reportan aparte.**

**Tesis.** Lo que hoy se puede afirmar sobre el mexicano con cifra propia es **descriptivo y retrospectivo**: cuánto, dónde y en qué segmento, medido desde microdato con su intervalo de diseño. Casi todo el peso del catálogo está en trabajo (ENOE), consumo del hogar (ENIGH), violencia contra las mujeres (ENDIREH) y tecnología (ENDUTIH, MOCIBA); v1.2 añade consumo, confianza, religiosidad, capital social, familia y migración (FIRMAS-19), casi todo **con reserva de ancho**. Ninguna fila es predicción ni efecto causal. Y donde el gradiente es de localidad, escolaridad o formalidad, la primera lectura es de **estructura y oferta**, no de cultura (§3 de las instrucciones).

Contadores que mueve este acto: «estimadores en catálogo con RESULT» (43 188 adopciones citadas por firma) y «dominios MEDIDOS» (13). No mueve `adoptados_activos`, `celdas_validadas` ni ningún contador del marcador: los lee.

## Cómo leerlo

1. Cada fila es un estimador **adoptado por una firma de mesa citada por id** en la columna `firma_fp`: un `FP-…` FIRMADO en `forense/firmas-pendientes.tsv`, el objeto de su fila en `data/corrida0/decisiones.tsv` (`decisiones.tsv:<objeto>`) o la firma verbatim de un encargo archivado (`forense/encargos/<archivo>.md#firma …`).
2. `result_id` + `celda` localizan la cifra: en los CALC de pisos, `RESULT-…-TABLA#i` es el registro `i` de la tabla sellada en `data/corrida0/<calc>/resultados.json`. Los hashes de cada CALC están en `forense/analisis/catalogo/v1_2/calcs.tsv`.
3. `unidad`, `eje` y `segmento` gobiernan la lectura. Ninguna cifra de unidad delito o trámite se compara con una de unidad persona u hogar.
4. `estado_adopcion`: `ADOPTADO` o `ADOPTADO-CON-RESERVA-DE-ANCHO` (su IC es calibrado y ancho a propósito: no se llama cobertura). `alcance`: `DESCRIPTIVO-DE-OLA` (piso de una ola, sin uso predictivo), `ESTIMADOR-DE-CELDA` (piso t−1 adjudicado a una celda del marcador) o `PARAMETRO-DE-REGLA` (lo lee una regla del motor).
5. `temporalidad`: todo el catálogo es **RETROSPECTIVA** (43 188 filas). Las celdas PROSPECTIVAS del marcador que existían eran pisos de origen legacy y quedaron fuera (ver «Fuera por regla»).
6. `origen_piso`: `NUEVO` (medido desde microdato en su CALC; 43 141 filas) o `HEREDADO-DE-GEN2` (el punto de la ola t es el piso GEN2 de t−1; 47 filas). **Ninguna fila es HEREDADO-DE-LEGACY.**
7. `oferta_exclusion`: en cada fila de `DINERO` va la medida de exclusión por oferta, o la declaración de que no existe una sellada para esa ola y conducta. `GEN2-DINERO-SERIES-CNBV-BANXICO-1` (`PR #1159`) no añadió columna de oferta a ningún piso de crédito o ahorro: su pieza P4 quedó `PARO-ENTORNO` (la serie BDIF de CNBV está en host denegado; NC `8dbe`), así que la columna sigue siendo la de `CALC-DIN-OFERTA-EXCLUSION-ENIF*-0001`.
8. **Filas de mesa pendientes de fusionar.** `GEN2-SEGURIDAD-ENSU-SERIE-1` y `GEN2-COLA-LOTE-1` no estaban en `main` al abrir este acto: **en curso**, ramas `gen2-seguridad-ensu-serie-1` y `acto/gen2-cola-lote-1`. No aportan filas; entran en v1.3.

## P1 · Estimadores por dominio e instrumento

| dominio | instrumento | estimadores | firmas citadas (ids distintos) |
|---|---|---:|---:|
| `CAPITAL_SOCIAL` | LAPOP | 614 | 1 |
| `CONFIANZA` | ENCIG | 6 | 2 |
| `CONFIANZA` | ENCUCI | 3 | 3 |
| `CONFIANZA` | ENVIPE | 15 | 2 |
| `CONFIANZA` | INSTRUMENTO-NO-IDENTIFICADO | 4 | 1 |
| `CONFIANZA` | LATINOBAROMETRO | 323 | 1 |
| `CONFIANZA` | WVS | 475 | 1 |
| `CONSUMO` | ENGASTO | 330 | 1 |
| `CONSUMO` | ENIGH | 4 140 | 1 |
| `DINERO` | ENFIH | 2 | 1 |
| `DINERO` | ENIF | 97 | 6 |
| `DINERO` | ENNVIH-1 | 1 | 1 |
| `FAMILIA_CUIDADOS` | EDER | 2 | 1 |
| `FAMILIA_CUIDADOS` | ENADID | 579 | 1 |
| `FAMILIA_CUIDADOS` | ENASIC | 98 | 1 |
| `FAMILIA_CUIDADOS` | ENIF | 3 | 2 |
| `FAMILIA_CUIDADOS` | ENIGH | 26 | 7 |
| `FAMILIA_CUIDADOS` | ENUT | 1 | 1 |
| `GENERO` | ENDIREH | 6 887 | 4 |
| `MIGRACION` | PEW | 126 | 1 |
| `POLITICA` | ENCUCI | 2 | 1 |
| `POLITICA` | ENVIPE | 14 | 10 |
| `RELIGIOSIDAD` | LATINOBAROMETRO | 34 | 1 |
| `RELIGIOSIDAD` | PEW | 193 | 1 |
| `RELIGIOSIDAD` | WVS | 133 | 1 |
| `SALUD` | ENCODAT | 130 | 1 |
| `SALUD` | ENSANUT | 670 | 2 |
| `SALUD_MENTAL` | ENBIARE | 180 | 1 |
| `TECNOLOGIA` | ENDUTIH | 1 578 | 2 |
| `TECNOLOGIA` | MOCIBA | 249 | 1 |
| `TRABAJO` | ENOE | 26 273 | 1 |

**Fuentes, una por firma.**

- **Pisos por instrumento — Firma T** (`GEN2-TRAMITE-FIRMAS-15` §1 T + ADENDA-1): ENOE (`FP-260923-ASTRA5-U1-TRABAJO-ENOE-e422-01`), ENDIREH 2021, 2016, 2011 y 2006 (`FP-260923-ASTRA5-U2-ENDIREH-6a2c-01` a `-04`), ENDUTIH 2023–2025 (`FP-260923-ASTRA5-U4-TECNOLOGIA-1f30-01`: sin las celdas originales de empleo, sustituidas por `CALC-ENDUTIH-EMPLEO-15MAS-*`) y MOCIBA 2015–2017 (`-1f30-02`: 2015 no estimable). Una fila por celda publicable; cada una es piso descriptivo retrospectivo **sin uso predictivo**.
- **Marginales por piso t−1**: ENVIPE 2025 adoptada (`decisiones.tsv:adopcion:piso-t1-marginales-por-instrumento`) y ENIF 2024 **con reserva de ancho** (`FP-260922-GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1-2868-01`, IC calibrado de persistencia: conservador, un solo choque). ENCIG 2025 queda vetada en nivel (fuera).
- **Pisos de salud y bienestar — FIRMAS-16** (`GEN2-TRAMITE-FIRMAS-16`, «ejecuta GEN2-CATALOGO-V1-1-1»): ENSANUT 2021–2024 **con reserva de ancho** (`FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-01`; sobre 2024 el IC es el calibrado de persistencia), ENCODAT 2016–2017 **con reserva de ancho** (`-6d56-02`; una sola ola, IC de diseño) y ENBIARE 2021 adoptado como piso de una ola (`-6d56-03`).
- **Parámetros de reglas y celdas R/M del marco** con consumo activo (la misma vista que `corrida0 status`), cada uno con la fila de `decisiones.tsv` de su CALC, su FP o la firma del encargo que lo relevó.
- **Pisos de FIRMAS-19** (`GEN2-TRAMITE-FIRMAS-19`, J1–J10; una fila por celda `-P` publicable de cada CALC, IC calibrado de persistencia donde el CALC lo trae):
  - J1 ENIGH 2016–2022, consumo del hogar (`CALC-ENIGH-CONSUMO-PISOS-0002`, `…-2d37-01`) **con reserva de ancho**; J3 (`…-2d37-03`) veta las filas de `-0001` construidas desde `gastoshogar` 2016/2018: el catálogo solo lee `-0002`. Trae el eje `ENTIDAD` (región).
  - J2 ENGASTO 2012 (`…-2d37-02`) con reserva de ancho, descripción de 2012 sin extrapolación.
  - J4 WVS 2018, J5 Latinobarómetro 2023, J6 PEW religión y autoridad, J7 LAPOP capital social (**sin serie**: cada ola se lee sola), J9 ENASIC 2022 y J10 PEW migración: con reserva de ancho.
  - J8 ENADID 2009/2014/2018 (`…-2a0e-01`): **adoptado** sin reserva.
- **Bloque ENIGH — Firma M** (`GEN2-ADOPCION-BLOQUE-Y-PINES-1`): descriptores de intensidad de remesas 2016, 2018 y 2020 con IC bootstrap.

**Ejes.** Sexo, edad, escolaridad, localidad (tamaño) y entidad —el eje regional disponible con RESULT adoptado— salen de las tablas ENOE, ENDIREH, ENDUTIH y ENIGH-consumo; formalidad y cuenta, de las marginales ENIF. **NSE entra como eje con reserva de instrumento** (`FP-260924-GEN2-CLASE-AMAI-1-e773-01`, FIRMAS-16): ENIGH 2022 (regla AMAI reproducida), ENIF 2024 (aproximación conforme) y ENDUTIH 2023 como aproximación rotulada; ENDUTIH 2024–2025 (`DESVIADA`) quedan fuera por la letra de la firma (60 celdas). La región de seis zonas de `canon/eje-regional-v1_0.md` es propuesta sin adopción: no aporta filas.

### Pendiente de firma (no entran; no es PARO)

| id | objeto | estado de la FP |
|---|---|---|

`SIN-FP-CITABLE`: RESULT con consumo activo que el contador de adoptados cuenta por la etiqueta de su propia spec (E.2), pero sin FP firmada, sin fila de mesa en `decisiones.tsv` para su CALC y sin firma de encargo en su pin. El catálogo no les inventa firma. La firma `FP-260925-GEN2-CATALOGO-V1-1-1-afe1-01` (FIRMADA, opción a) los hace entrar en v1.2 citándola.

### Fuera por regla

Detalle por llave en `forense/analisis/catalogo/v1_2/excluidos.tsv`:

- Piso **HEREDADO-DE-LEGACY** (20 RESULT del censo de `GEN2-ENCIG-PISOS-GEN2-1`): `GEN2-PISOS-GEN2-2` cerró (`PR #1123`) re-midiéndolos con sucesores `-0002` sellados; **ninguna fila de esta tabla es HEREDADO-DE-LEGACY** (pisos por origen: `NUEVO` o `HEREDADO-DE-GEN2`).
- Celdas FIRMAS-19 con punto nulo: 144.
- Celdas ENDUTIH originales de empleo excluidas por la propia firma: 141.
- Celdas sin punto publicable: suprimidas 613 + 3 + 2, no estimables 30.
- Marginales sin adopción en nivel (ENCIG 2025, vetada): 10.
- Tablas ENIGH adoptadas por Firma M y no desagregadas en esta versión (perfil estructural y remesas en contexto): 6 CALC. La evaluación de origen móvil del duelo ENIGH (1 CALC) mide error de candidatos, no una conducta.

## P3 · Cobertura de los reports del corpus

Unidad: los 31 reports de `corpus/reports/` (el conteo de «dominios» de la ADENDA-2 y del README), cada uno asignado a su dominio primario por `forense/analisis/dominios/report-a-dominio-v1_0.tsv`; los conteos de afirmaciones salen de `canon/mapa-dominios-v1_0.tsv`. Regla, en orden (la primera que se cumple):

- `MEDIDO` — el dominio tiene al menos un estimador en esta tabla.
- `EN-MEDICIÓN` — hay CALC con `cuenta_gen2: SI` sellados para un instrumento del dominio, sin adopción todavía (ENCUP/LAPOP/INE, ENADID, ENCUCI y los demás instrumentos de la regla del generador).
- `MEDIBLE-EN-CORPUS-SIN-CALC` — el mapa dictamina afirmaciones medibles con lo que ya hay en el corpus, pero nadie corrió el mecanismo. Es un «nadie corrió» (§2), no un «no se puede»: por eso no se funde con la categoría siguiente.
- `MEDIBLE-CON-ADQUISICIÓN` — solo medible si se adquiere el instrumento.
- `NO-MEDIBLE-POR-DISEÑO` — todas sus afirmaciones lo son.

| estado | reports |
|---|---:|
| MEDIDO | 14 |
| EN-MEDICIÓN | 3 |
| MEDIBLE-EN-CORPUS-SIN-CALC | 7 |
| MEDIBLE-CON-ADQUISICIÓN | 6 |
| NO-MEDIBLE-POR-DISEÑO | 0 |
| SIN-AFIRMACIONES-EN-MAPA | 1 |

| report | dominio (mapa U0) | estado | estimadores v1.2 | CALC GEN2 sin adoptar | afirmaciones (en corpus / con adquisición / no medibles) |
|---|---|---|---:|---:|---|
| Adopción y Resistencia Tecnológica en México  La Paradoja de la Baja C | `TECNOLOGIA` | **MEDIDO** | 1827 | 0 | 49 (17 / 18 / 14) |
| Ausencia sin certeza  duelo y pérdida ambigua en familias de personas  | `DUELO` | **MEDIBLE-EN-CORPUS-SIN-CALC** | 0 | 0 | 33 (3 / 23 / 7) |
| Autoridad y jerarquía en el México contemporáneo  anatomía psicológica | `AUTORIDAD` | **MEDIBLE-EN-CORPUS-SIN-CALC** | 0 | 0 | 39 (8 / 19 / 12) |
| Behavioral Finance Mexicano  Estructura  Adaptación Racional y Cultura | `DINERO` | **MEDIDO** | 100 | 0 | 179 (40 / 89 / 50) |
| Confianza y Desconfianza en México  Anatomía Psicológica de una Socied | `CONFIANZA` | **MEDIDO** | 826 | 0 | 59 (20 / 24 / 15) |
| El Clasemediero Mexicano  Identidad  Ansiedad de Estatus y el Miedo Ra | `MOVILIDAD` | **EN-MEDICIÓN** | 0 | 7 | 56 (4 / 41 / 11) |
| El Efecto Ambiental de la Violencia Crónica en México  Cómo el Miedo R | `VIOLENCIA` | **MEDIBLE-EN-CORPUS-SIN-CALC** | 0 | 0 | 56 (11 / 36 / 9) |
| El Mexicano y el Tiempo  Estructura  no Cultura  en la Planeación y el | `TIEMPO` | **EN-MEDICIÓN** | 0 | 4 | 20 (4 / 6 / 10) |
| El México Rural e Indígena en sus Propios Términos  Comunalidad  Autor | `RURAL_INDIGENA` | **MEDIBLE-EN-CORPUS-SIN-CALC** | 0 | 0 | 56 (7 / 30 / 19) |
| Elegir  Cortejar y Amar en el México de Hoy  Díada de Pareja  Apps de  | `PAREJA` | **MEDIBLE-EN-CORPUS-SIN-CALC** | 0 | 0 | 32 (1 / 18 / 13) |
| Genetica y Conducta del Mexicano Contemporaneo  Canal Individual vs  E | `GENETICA` | **MEDIBLE-CON-ADQUISICIÓN** | 0 | 0 | 38 (0 / 35 / 3) |
| Health  Body  Food and Substance Use in Mexico  The Behavioral Layer o | `SALUD` | **MEDIDO** | 800 | 2 | 64 (13 / 31 / 20) |
| Humor in Mexican Psychological Life  2023-2026 Update | `HUMOR` | **MEDIBLE-CON-ADQUISICIÓN** | 0 | 0 | 29 (0 / 17 / 12) |
| La arquitectura invisible de la interacción social en México | `INTERACCION` | **MEDIBLE-CON-ADQUISICIÓN** | 0 | 0 | 21 (0 / 13 / 8) |
| La familia mexicana como sistema psicológico  entre el afecto  la obli | `FAMILIA_CUIDADOS` | **MEDIDO** | 709 | 0 | 46 (6 / 27 / 13) |
| Mexican Population Genomics  2025-2026 Scientific and Market Opportuni | `GENOMICA` | **MEDIBLE-CON-ADQUISICIÓN** | 0 | 0 | 33 (0 / 27 / 6) |
| Moral Emotions in Mexico  Declared Dignity  Relational Face  and Resid | `EMOCIONES_MORALES` | **MEDIBLE-CON-ADQUISICIÓN** | 0 | 0 | 26 (0 / 18 / 8) |
| Mérito  Movilidad Social y Desigualdad en México  Actualización 2025-2 | `MOVILIDAD` | **EN-MEDICIÓN** | 0 | 7 | 56 (4 / 41 / 11) |
| Non-Family Social Capital in Mexico  Cooperation  Trust  and Collectiv | `CAPITAL_SOCIAL` | **MEDIDO** | 614 | 6 | 30 (9 / 8 / 13) |
| Psicología Política y Comportamiento Cívico del Mexicano Contemporáneo | `POLITICA` | **MEDIDO** | 16 | 11 | 90 (20 / 42 / 28) |
| Psicología  Conducta y Sociedad en el México Contemporáneo  Análisis T | `SINTESIS` | **SIN-AFIRMACIONES-EN-MAPA** | 0 | 0 | 0 (0 / 0 / 0) |
| Psicología de la Juventud Mexicana Contemporánea  Gen Z y Millennials  | `JUVENTUD` | **MEDIBLE-EN-CORPUS-SIN-CALC** | 0 | 0 | 29 (4 / 14 / 11) |
| Psicología del Consumidor Mexicano  Patrones  Contradicciones y Estrat | `CONSUMO` | **MEDIDO** | 4470 | 0 | 81 (3 / 42 / 36) |
| Psicología del Trabajo en México  Un Mapa Basado en Evidencia | `TRABAJO` | **MEDIDO** | 26273 | 0 | 85 (13 / 48 / 24) |
| Psychology of Mexico-US Migration  Identity  Family  Aspiration  and W | `MIGRACION` | **MEDIDO** | 126 | 1 | 58 (5 / 29 / 24) |
| Reconfiguración de los Guiones de Género en México  Masculinidades  Fe | `GENERO` | **MEDIDO** | 6887 | 0 | 47 (7 / 26 / 14) |
| Religiosidad y Psicología del Mexicano Contemporáneo  Moral  Afrontami | `RELIGIOSIDAD` | **MEDIDO** | 360 | 0 | 39 (5 / 25 / 9) |
| Report 26  The Contemporary Mexican and Knowledge  Expertise  Educatio | `CONOCIMIENTO` | **MEDIBLE-CON-ADQUISICIÓN** | 0 | 0 | 26 (0 / 15 / 11) |
| Salud Mental en México  Prevalencia  Estigma y la Brecha entre Necesid | `SALUD_MENTAL` | **MEDIDO** | 180 | 1 | 62 (7 / 44 / 11) |
| Sanción Social Horizontal en México  Chisme  Envidia y Mal de Ojo como | `SANCION_SOCIAL` | **MEDIBLE-EN-CORPUS-SIN-CALC** | 0 | 0 | 13 (1 / 3 / 9) |
| Vejez y Cuidado Intergeneracional en México  El Debilitamiento del Seg | `FAMILIA_CUIDADOS` | **MEDIDO** | 709 | 0 | 46 (6 / 27 / 13) |

Varios reports comparten dominio (dos de movilidad, dos de familia y cuidados): un dominio medido cuenta como medido en cada report que lo tiene como primario. El conteo por dominio del mapa está en la portada.

## P2 · Reglas SI-ENTONCES

Formato §5: **SI** [segmento] **ENTONCES** [conducta] — **PORQUE** [driver] — [TIER]. El tier **FUERTE** se reserva a la frecuencia que un RESULT GEN2 adoptado sostiene. El PORQUE es un mecanismo propuesto y lleva tier propio: ninguna de estas comparaciones lo identifica. Todas las cifras son RETROSPECTIVAS.

### Revisión de las reglas de v1.0

1. **Trámites — canal (v1.0 regla 1) · CONFIRMA.** **SI** el trámite ENCIG 2025 es presencial (urbano) **ENTONCES** la proporción de eventos con mordida es 0.141 [0.116, 0.168]; **SI** es digital, 0.030 [0.021, 0.040] — **PORQUE** registro y menor discrecionalidad (mecanismo `modelo §3.3`) — **[FUERTE como frecuencia por evento; mecanismo MEDIA, no identificado]**. Mismos RESULT que en v1.0, ahora con firma citada (`decisiones.tsv:CALC-ENCIG-0001`). La unidad es el evento de trámite, no la persona. Falsador: igualar tipo de trámite y soporte entre canales y que la diferencia desaparezca.
2. **Familia — remesas (v1.0 regla 2) · MATIZA.** v1.0 daba un solo punto (ENIGH 2022, 0.046 [0.044, 0.048]). v1.1 añade la serie adoptada de prevalencia: 2016 0.047, 2018 0.047, 2020 0.044. El orden de magnitud se sostiene en cuatro olas. DONDE-CAMBIO dictamina la prevalencia `SIN-SERIE` y la participación agregada de remesas en el ingreso `ESTABLE`, así que el catálogo no afirma tendencia. **SI** el hogar recibe remesas **ENTONCES** en la mediana de receptores el ingreso por remesas es 4918.030 pesos trimestrales en 2020 — **PORQUE** la familia como seguro ante volatilidad y ausencia estatal (`modelo §3.5`) — **[FUERTE como descripción; mecanismo HIPÓTESIS en este catálogo]**. Unidad: hogar. Falsador del mecanismo: medir volatilidad y cobertura estatal junto con las transferencias.

### Reglas nuevas por dominio que entra

3. **Trabajo — informalidad por tamaño de localidad (ENOE, `TRABAJO`).** **SI** la persona ocupada vive en una localidad de menos de dos mil quinientos habitantes (`MENOS-2K5`) **ENTONCES** la proporción en empleo informal en 2025T4 es 0.791 [0.783, 0.803], contra 0.424 [0.418, 0.430] en localidades `100K+` y 0.550 [0.545, 0.555] nacional — **PORQUE** la oferta de empleo con seguridad social se concentra en ciudades (estructura, no preferencia) — **[FUERTE como gradiente descriptivo; mecanismo MEDIA]**. El gradiente ya estaba en 2005T1: 0.838 [0.831, 0.847] contra 0.459 [0.453, 0.465]. Falsador: que el gradiente se anule al condicionar por sector y tamaño de establecimiento.
4. **Trabajo — contrato escrito (ENOE).** **SI** ocupado en `MENOS-2K5` **ENTONCES** sin contrato escrito 0.694 [0.679, 0.711] (2025T4), contra 0.295 [0.288, 0.301] en `100K+` — **PORQUE** agricultura y autoempleo dominan la estructura local — **[FUERTE descriptiva; mecanismo MEDIA]**. Falsador: la misma brecha dentro de asalariados de establecimientos comparables.
5. **Género — violencia física de pareja (ENDIREH 2021, `GENERO`).** **SI** mujer de quince años o más con pareja actual **ENTONCES** violencia física de pareja alguna vez en la relación 0.156 [0.152, 0.160] y desde octubre de 2020 0.068 [0.065, 0.070] — **PORQUE** —(el catálogo no propone driver: ENDIREH mide prevalencia y no la separa de desigualdad económica ni de violencia ambiental) — **[FUERTE como prevalencia; causa sin tier]**. Las ventanas distintas no se restan ni se promedian. Falsador de la generalización: una ola con el mismo instrumento cuyo IC excluya estos puntos.
6. **Género — denuncia (ENDIREH 2021).** **SI** mujer que vivió violencia (módulo de ayuda) **ENTONCES** denuncia 0.044 [0.041, 0.048] — **PORQUE** costo y desconfianza en la institución receptora (adaptación racional, hipótesis) — **[FUERTE descriptiva; mecanismo HIPÓTESIS]**. No es rasgo cultural del silencio: sin medir el trato institucional, la hipótesis de incentivo es la primera. Falsador: una mejora medida del trato institucional sin cambio en la denuncia.
7. **Tecnología — no usar internet: costo contra preferencia (ENDUTIH 2025, `TECNOLOGIA`).** **SI** la persona sin internet vive en localidad `TLOC_4` (menos de dos mil quinientos habitantes) **ENTONCES** la razón «costo» es 0.143 [0.125, 0.161] y «no le interesa» 0.112 [0.097, 0.128]; en `TLOC_1` (cien mil o más), costo 0.068 [0.055, 0.083] y preferencia 0.218 [0.199, 0.242] — **PORQUE** la exclusión por precio pesa más abajo en la jerarquía urbana y el desinterés declarado pesa más arriba (oferta antes que preferencia, §3) — **[FUERTE descriptiva; mecanismo MEDIA]**. El uso de internet va de 0.908 [0.903, 0.913] (`TLOC_1`) a 0.756 [0.742, 0.771] (`TLOC_4`). Falsador: que la brecha de costo desaparezca al controlar por ingreso del hogar.
8. **Tecnología — ciberacoso (MOCIBA 2017).** **SI** usuario de internet de doce años o más **ENTONCES** reporta ciberacoso 0.169 [0.162, 0.176] y lo denuncia 0.054 [0.043, 0.064] — **PORQUE** —(sin driver propuesto) — **[FUERTE descriptiva, una ola; no se compara con 2015, no estimable]**.
9. **Dinero — ahorro solo informal por formalidad (ENIF 2024, `DINERO`, CON RESERVA DE ANCHO).** **SI** la persona no tiene seguridad social **ENTONCES** ahorra solo por vía informal con punto 0.441 [0.274, 0.623], contra 0.345 [0.201, 0.525] con seguridad social (IC calibrados de persistencia) — **PORQUE** la oferta formal (cuenta, nómina) sigue a la formalidad laboral — **[MEDIA: los IC calibrados se traslapan; el catálogo no afirma diferencia]**. Oferta al lado: no existe exclusión por oferta sellada para ahorro ENIF 2024 (columna `oferta_exclusion`). Falsador: igualar tenencia de cuenta y que la brecha subsista.
10. **Seguridad — denuncia con seguro (ENVIPE 2025, piso t−1, unidad delito).** **SI** el delito afecta a un bien asegurado **ENTONCES** se denuncia 0.774 [0.711, 0.833], contra 0.634 [0.585, 0.682] sin seguro — **PORQUE** la aseguradora exige la denuncia: incentivo, no confianza (adaptación racional) — **[FUERTE descriptiva; mecanismo MEDIA]**. Unidad delito: no se compara con proporciones de personas. Falsador: igual diferencia en delitos cuyo seguro no exige denuncia.

## P4 · Dónde sí cambió

El dictamen por serie vive en [`canon/donde-cambio-el-mexicano-v1_0.md`](donde-cambio-el-mexicano-v1_0.md) (`GEN2-DONDE-CAMBIO-EL-MEXICANO-1`, RETROSPECTIVA, sin adopción). Conteo por comando sobre `forense/analisis/donde-cambio/tabla-dictamen-v1_0.tsv`: 7 872 series · 583 `ESTABLE` · 8 `CAMBIO-SOSTENIDO` (3 suben, 5 bajan) · 81 `SALTO-SIN-EXPLICAR` (el `SALTO` del encargo) · 7 200 `SIN-SERIE`.

Lectura para el catálogo: los cambios sostenidos son todos ENOE y de décimas de punto; la mayoría de las series no tiene tres olas comparables. **La afirmación «el mexicano cambió en X» no tiene respaldo en este corpus fuera de esas series**, y ninguna frase de este catálogo la hace. «Cambió» es un hecho de la serie, no de la psicología.

## P4 · Cobertura por clase

Cita de [`forense/analisis/clase-amai/cobertura-por-clase-v1_0.md`](../forense/analisis/clase-amai/cobertura-por-clase-v1_0.md) (`GEN2-CLASE-AMAI-1`, RETROSPECTIVA): hay pisos por NSE AMAI en 144 celdas (`pisos-nse-v1_0.tsv`); con la firma `FP-260924-GEN2-CLASE-AMAI-1-e773-01` entran al catálogo las de ENIGH 2022, ENIF 2024 y ENDUTIH 2023 (eje `NSE`). Las cifras por clase de este catálogo son esas filas; la lectura de abajo es la del documento citado. El hallazgo que el catálogo hereda como reserva: el corte de clase solo es posible hoy en dinero (ENIF), remesas (ENIGH) y tecnología (ENDUTIH). Lo cívico y el trato con el Estado (ENVIPE, ENCIG) no admiten NSE AMAI por construcción del cuestionario, y ahí el único corte socioeconómico es la escolaridad. Varios gradientes que parecen cultura (horizonte de ahorro corto, no usar internet por costo) son de clase según ese documento; la desconfianza declarada no muestra gradiente medible.

## Módulo de auditoría de rigor extremo

- **¿Cuántos contadores movió este trabajo?** Dos del catálogo («estimadores con RESULT», «dominios MEDIDOS»). Cero mediciones; ejecuta adopciones ya firmadas (FIRMAS-19, `afe1-01`), no adopta por su cuenta.
- **¿Pobreza, informalidad o violencia confundidas con cultura?** Las reglas de trabajo y tecnología leen primero estructura y oferta; ninguna regla atribuye un gradiente a «cultura mexicana».
- **¿Sobregeneralización desde la clase media urbana?** Los ejes de localidad (ENOE `MENOS-2K5`, ENDUTIH `TLOC_4`) están en la tabla. El eje NSE adoptado corta clase solo en dinero, remesas y tecnología: en lo cívico y en el trato con el Estado sigue sin corte de clase posible.
- **¿Qué cambia con foco rural o indígena?** El gradiente rural de informalidad y costo digital es el más grande del catálogo. Lo indígena-comunal queda fuera por diseño y ningún instrumento adoptado lo identifica.
- **¿Qué parece psicológico y es incentivo?** La denuncia con seguro (regla 10) y la denuncia de violencia (regla 6).
- **¿Evidencia débil con intuición fuerte?** Todos los PORQUE. Por eso llevan tier propio.
- **¿Qué afirmación sobre el corpus se escribió a mano?** Ninguna cifra: toda cifra sale de un marcador de conteo o de RESULT de la plantilla (`forense/analisis/catalogo/v1_2/plantilla.md`), y `tests/test_catalogo_v1_2.py` falla si aparece un dígito fuera de un identificador, un año o un placeholder resuelto.
- **¿Deuda asumida que caducó?** `afe1-01` y FIRMAS-19 fusionaron y entraron. Quedan en curso ENSU y COLA-LOTE-1, y las firmas de COLA-COMPLETA-1 van a v1.3.
- **¿Sesgo de marcos o muestras importadas?** WVS, Latinobarómetro, PEW y LAPOP son marcos internacionales: sus ejes son los del cuestionario (clase subjetiva, ingreso subjetivo), no NSE AMAI, y ninguna fila se lee como rasgo nacional esencial. PEW migración mide disposiciones, no flujos.
- **¿Escala de cada cantidad y contra qué se compara?** Columna `unidad`. Solo se contrastan filas del mismo CALC, unidad y ola.
- **¿PROSPECTIVA y RETROSPECTIVA mezcladas?** No: todo el catálogo es RETROSPECTIVA. Las celdas validadas PROSPECTIVAS se citan aparte en la frase de portada.
- **¿Unidades promediadas?** No: persona (ENOE, ENDIREH, ENDUTIH, ENIF, WVS, LAPOP), hogar (ENIGH, ENGASTO), delito (ENVIPE) y evento de trámite (ENCIG) nunca se suman.
- **¿Qué sería peligroso leído simplista?** Leer la tabla de ENOE como «la informalidad es rural por cultura», o una prevalencia ENDIREH como tasa anual.
