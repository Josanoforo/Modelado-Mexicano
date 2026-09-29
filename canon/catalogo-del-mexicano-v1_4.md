# Benchmark auditable del comportamiento del mexicano · catálogo v1.4

> | | |
> |---|---|
> | **ARCHIVO** | `catalogo-del-mexicano-v1_4.md` (sucesor de `catalogo-del-mexicano-v1_3.md`; v1.0–v1.3 quedan intactos — E.1) |
> | **NOMBRE ESTABLE** | `catálogo del mexicano` |
> | **ESTADO** | Producto consultable. Lo firmado hasta v1.3 entra citando su firma; lo sellado del `27–28/sep` entra como **bloque de adopción propuesto por instrumento**: el merge de mesa del PR que trae esta versión **es** la adopción (E.2). Sin merge, esta versión no existe en `main` |
> | **ACTO** | `GEN2-CIERRE-Y-PRODUCTO-3` (P1) · generación GEN2 · cero mediciones nuevas · consume lo sellado y registrado |
> | **TABLA** | [`catalogo-del-mexicano-v1_4.tsv`](catalogo-del-mexicano-v1_4.tsv) — una fila por estimador |
> | **BLOQUE** | [`bloque-adopcion-cifras-v1_4.tsv`](../forense/analisis/catalogo/v1_4/bloque-adopcion-cifras-v1_4.tsv) — propuesta por instrumento (ADOPTAR / CON-RESERVA-DE-ANCHO / NO-ENTRA); mesa veta un instrumento pidiendo su retiro antes del merge |
> | **REGENERA** | `python3 forense/analisis/catalogo/genera_catalogo_v1_4.py` (esta portada incluida; los generadores v1.2 y v1.3 quedan intactos); `--sin-registro` reutiliza las constancias ya derivadas del registro (`adoptados-activos-v1_4.tsv`, `registro-semana-v1_4.tsv`, `status-v1_4.json`) |

**65 480 estimadores con RESULT sellado · 21 de los 28 dominios del mapa v1.1 con estimador (eran 17 en v1.3) · 23 de los 31 reports del corpus con dominio medido · 219 celdas validadas (definición vigente de `corrida0 status`), de las cuales 20 PROSPECTIVAS y 75 RETROSPECTIVAS se reportan aparte.**

**Tesis.** Lo que hoy se puede afirmar sobre el mexicano con cifra propia sigue siendo **descriptivo y retrospectivo**. v1.4 añade 1 722 filas de 16 CALC sellados esta semana, todas propuestas **con reserva de ancho**: 1 556 pisos de una ola (confianza institucional ENCIG 2023 y los pisos de dominio PDR1 que dan estimador por primera vez a AUTORIDAD, SANCION_SOCIAL, TIEMPO y RURAL_INDIGENA) y 166 contrastes de momento (CALC-ALT-*), 92 de ellos con su holdout ya gastado. Rotula además las 404 llaves del tercer lote de validación ciega y suspende, por firma, las 15 llaves ENVIPE 2024 retiradas del universo C1. Ninguna fila es predicción.

Contadores que mueve este acto, si mesa fusiona: «estimadores en catálogo con RESULT» (65 480), «dominios del mapa con estimador» (`mapa11_dominios_medidos`: 17 → 21). No mueve `adoptados_activos` (128 en el registro de este commit), `celdas_validadas` ni ningún contador del marcador: los lee. La vista publicada (`data/corrida0/corridas.tsv`) va atrasada respecto del disco (el `[deriva]` publica por trozos); el catálogo lee el registro derivado **del commit** con la misma función que `corrida0 status` y lo deja como constancia.

## Cómo leerlo

1. Cada fila cita su adopción en `firma_fp`: un `FP-…` FIRMADO en `forense/firmas-pendientes.tsv`, el objeto de su fila en `data/corrida0/decisiones.tsv` (`decisiones.tsv:<objeto>`), la firma verbatim de un encargo archivado (`forense/encargos/<archivo>.md#firma …`) o, **nuevo en v1.4**, `MERGE-DE-MESA:GEN2-CIERRE-Y-PRODUCTO-3` (1 722 filas): adopción por el merge del PR que trae el bloque (E.2), con la propuesta por instrumento en el TSV del bloque.
2. `result_id` + `celda` localizan la cifra: en los CALC de pisos, `RESULT-…-TABLA#i` es el registro `i` de la tabla sellada en `data/corrida0/<calc>/resultados.json`. En los CALC-ALT, `RESULT-…-TABLA#<ruta>` es el nodo de la tabla sellada por referencia (`tablas/tabla.json`, hash verificado al leer). Los hashes de cada CALC están en `forense/analisis/catalogo/v1_4/calcs-v1_4.tsv`.
3. `unidad`, `eje` y `segmento` gobiernan la lectura. Ninguna cifra de unidad delito o trámite se compara con una de unidad persona u hogar.
4. `estado_adopcion`: `ADOPTADO`, `ADOPTADO-CON-RESERVA-DE-ANCHO` (su IC es calibrado y ancho a propósito: no se llama cobertura) o `SUSPENDIDA-POR-FIRMA` (22 filas: la cifra sellada no mide el estimando de su spec humana; la fila se conserva con su `sucesor` y **no se usa como piso**). `alcance`: `PISO-DESCRIPTIVO-DE-OLA` (bloque v1.4: piso de una ola), `CONTRASTE-DE-MOMENTO` (bloque v1.4: diferencia entre dos grupos de una ola; **no es línea a vencer** y no entra a la tabla de piso), `DESCRIPTIVO-DE-OLA` (piso de una ola, sin uso predictivo), `ESTIMADOR-DE-CELDA` (piso t−1 adjudicado a una celda del marcador) o `PARAMETRO-DE-REGLA` (lo lee una regla del motor).
5. `temporalidad`: **RETROSPECTIVA** 65 460 filas y **PROSPECTIVA** 20, en columnas que no se suman. Las PROSPECTIVAS son parámetros de regla que el marcador marca así: los árbitros sucesores `-0002` (`CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002`, `CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002`) de celdas cuya emisión se selló antes de existir su árbitro; entran por el relevo de consumidores de la semana, no por el bloque. No son predicciones del catálogo: son la `R` contra la que se comparó una predicción sellada. Las celdas PROSPECTIVAS de origen legacy siguen fuera (ver «Fuera por regla»).
6. `origen_piso`: `NUEVO` (medido desde microdato en su CALC; 65 433 filas) o `HEREDADO-DE-GEN2` (el punto de la ola t es el piso GEN2 de t−1; 47 filas). **Ninguna fila es HEREDADO-DE-LEGACY.**
7. `oferta_exclusion`: en cada fila de `DINERO` va la medida de exclusión por oferta, o la declaración de que no existe una sellada para esa ola y conducta. `GEN2-DINERO-SERIES-CNBV-BANXICO-1` (`PR #1159`) no añadió columna de oferta a ningún piso de crédito o ahorro: su pieza P4 quedó `PARO-ENTORNO` (la serie BDIF de CNBV está en host denegado; NC `8dbe`), así que la columna sigue siendo la de `CALC-DIN-OFERTA-EXCLUSION-ENIF*-0001`.
8. **Validación ciega (columna `validacion_ciega`).** Las 3 371 llaves del primer lote de validación ciega llevan el rótulo de la tabla del recibo `GEN2-RECIBO-ASTRA6-1` (firma `FP-260927-GEN2-RECIBO-ASTRA6-1-beee-02`): `SOSTENER` 1 876, `SOSTENER-SIN-CORROBORACION` 799, `ACOTADA` 689 (`DELTA-PUNTO-EN-VALIDACION-CIEGA` 679, `PUBLICABILIDAD-FRAGIL-AL-RNG` 10) y `SUSPENDIDA` 7. El sello de su CALC no se toca: el sucesor es un CALC nuevo, nombrado en `sucesor` y no abierto aquí. Todas son RETROSPECTIVAS; unidad mujer.

| rótulo de validación ciega (lote 1) | estado de adopción | filas |
|---|---|---:|
| `ACOTADA:DELTA-PUNTO-EN-VALIDACION-CIEGA` | `ADOPTADO` | 679 |
| `ACOTADA:PUBLICABILIDAD-FRAGIL-AL-RNG` | `ADOPTADO` | 10 |
| `SIN-VALIDACION-CIEGA` | `ADOPTADO` | 33 428 |
| `SIN-VALIDACION-CIEGA` | `ADOPTADO-CON-RESERVA-DE-ANCHO` | 28 666 |
| `SIN-VALIDACION-CIEGA` | `SUSPENDIDA-POR-FIRMA` | 15 |
| `SOSTENER` | `ADOPTADO` | 1 876 |
| `SOSTENER-SIN-CORROBORACION` | `ADOPTADO` | 799 |
| `SUSPENDIDA:PUBLICABILIDAD:DISCREPA` | `SUSPENDIDA-POR-FIRMA` | 1 |
| `SUSPENDIDA:PUNTO:DISCREPA` | `SUSPENDIDA-POR-FIRMA` | 6 |

9. **Validación ciega, tercer lote (columna `validacion_ciega_lote3`).** Las 404 llaves de `forense/validacion-independiente/catalogo-1-lote3/dictamen-lote3-v1_1.tsv` (`GEN2-C1-SUCESORES-Y-LOTE-3`) llevan su dictamen: `SOSTENER` 278, `SOSTENER-SIN-CORROBORACION` 120 (incluye las del tercer lote que el gate de acceso no dejó lanzar: sostener sin corroborar no es validar), `ACOTADA` 4 (CESD-7 de ENBIARE: `R26 (a)` excluye `EDAD=98`; sucesora `--R26A`) y `ACOTADA-PROPUESTA` 2 (ENDIREH 2016, `60+` incluye `EDAD=98`; `FP-260928-GEN2-ASTRA6-C1-LOTE-3-0c1f-01` ABIERTA: el rótulo es propuesta, no firma). El rótulo lleva `punto=` tal como lo escribe el dictamen: `DENTRO` es dentro de la tolerancia absoluta del comparador (`1e-10`), **no** igualdad exacta; `FUERA` trae su Δ en el dictamen. El IC no adjudica en ninguna fila (`IC-DIAGNOSTICO-R23-NO-ADJUDICA`). Todas RETROSPECTIVAS.
10. **Suspendidas por R21.** Las 15 llaves `RESULT-PISOS-ENVIPE2024-V2-*` (denuncia con seguro y evasión), retiradas del universo C1 por `FP-260926-GEN2-ASTRA6-C1-IMPEDIMENTOS-LOTE2-fb50-02` (FIRMADA), pasan a `SUSPENDIDA-POR-FIRMA` con su `sucesor` por llave. Suspender no es borrar: la fila se queda, rotulada, y **no se usa como piso**.
11. **`holdout_gastado`** (solo contrastes de momento): el momento cuyo holdout consumió el CALC (`M13`, `M19`, `M22`, `M23`) o `NINGUNO`. Un momento con holdout gastado ya no sirve para validar prospectivamente ese momento; sirve para describir (E.6).

| rótulo del lote 3 | estado de adopción | filas |
|---|---|---:|
| `ACOTADA-PROPUESTA:60+-INCLUYE-EDAD-98` | `ADOPTADO` | 2 |
| `ACOTADA:R26A-EXCLUYE-EDAD-98` | `ADOPTADO` | 4 |
| `LOTE3:SOSTENER-SIN-CORROBORACION:punto=DENTRO` | `ADOPTADO` | 18 |
| `LOTE3:SOSTENER-SIN-CORROBORACION:punto=FUERA` | `ADOPTADO` | 12 |
| `LOTE3:SOSTENER-SIN-CORROBORACION:punto=NO-COMPARADO` | `ADOPTADO` | 90 |
| `LOTE3:SOSTENER:punto=DENTRO` | `ADOPTADO` | 148 |
| `LOTE3:SOSTENER:punto=DENTRO` | `ADOPTADO-CON-RESERVA-DE-ANCHO` | 130 |
| `SUSPENDIDA:RETIRADA-DEL-UNIVERSO-C1` | `SUSPENDIDA-POR-FIRMA` | 15 |

## P1 · Estimadores por dominio e instrumento

| dominio | instrumento | estimadores | firmas citadas (ids distintos) |
|---|---|---:|---:|
| `AUTORIDAD` | ENCUCI | 142 | 1 |
| `CAPITAL_SOCIAL` | ENVIPE | 47 | 1 |
| `CAPITAL_SOCIAL` | LAPOP | 614 | 1 |
| `CONFIANZA` | ENCIG | 1 113 | 5 |
| `CONFIANZA` | ENCRIGE | 27 | 1 |
| `CONFIANZA` | ENCUCI | 40 | 4 |
| `CONFIANZA` | ENVE | 9 | 1 |
| `CONFIANZA` | ENVIPE | 27 | 3 |
| `CONFIANZA` | INSTRUMENTO-NO-IDENTIFICADO | 4 | 1 |
| `CONFIANZA` | LATINOBAROMETRO | 323 | 1 |
| `CONFIANZA` | WVS | 477 | 2 |
| `CONOCIMIENTO` | ENIGH | 128 | 1 |
| `CONOCIMIENTO` | ENPECYT | 280 | 1 |
| `CONSUMO` | ENGASTO | 330 | 1 |
| `CONSUMO` | ENIGH | 4 140 | 1 |
| `DINERO` | ENFIH | 2 | 1 |
| `DINERO` | ENIF | 105 | 7 |
| `DINERO` | ENNVIH-1 | 1 | 1 |
| `DINERO` | ENSAFI | 16 | 1 |
| `FAMILIA_CUIDADOS` | CCPV | 640 | 1 |
| `FAMILIA_CUIDADOS` | EDER | 2 | 1 |
| `FAMILIA_CUIDADOS` | ENADID | 679 | 2 |
| `FAMILIA_CUIDADOS` | ENASIC | 98 | 1 |
| `FAMILIA_CUIDADOS` | ENIF | 3 | 2 |
| `FAMILIA_CUIDADOS` | ENIGH | 26 | 7 |
| `FAMILIA_CUIDADOS` | ENUT | 1 | 1 |
| `GENERO` | ENDIREH | 6 887 | 4 |
| `GENERO` | ENDISEG | 424 | 1 |
| `MIGRACION` | PEW | 126 | 1 |
| `MOVILIDAD` | ENASEM | 14 | 1 |
| `MOVILIDAD` | MMSI | 158 | 1 |
| `PAREJA` | EMAT | 3 304 | 1 |
| `POLITICA` | CIDE-CSES | 4 | 1 |
| `POLITICA` | ENCUCI | 2 | 1 |
| `POLITICA` | ENVIPE | 14 | 10 |
| `POLITICA` | LAPOP | 38 | 1 |
| `POLITICA` | LATINOBAROMETRO | 68 | 1 |
| `RELIGIOSIDAD` | LATINOBAROMETRO | 34 | 1 |
| `RELIGIOSIDAD` | PEW | 237 | 2 |
| `RELIGIOSIDAD` | WVS | 133 | 1 |
| `RURAL_INDIGENA` | ENADID | 51 | 1 |
| `RURAL_INDIGENA` | ENUT | 26 | 1 |
| `SALUD` | ENCODAT | 130 | 1 |
| `SALUD` | ENSANUT | 670 | 2 |
| `SALUD_MENTAL` | EDR | 2 578 | 1 |
| `SALUD_MENTAL` | ENBIARE | 180 | 1 |
| `SANCION_SOCIAL` | ENSU | 9 | 1 |
| `TECNOLOGIA` | ENDUTIH | 1 578 | 2 |
| `TECNOLOGIA` | MOCIBA | 249 | 1 |
| `TIEMPO` | ENUT | 78 | 1 |
| `TRABAJO` | ENOE | 26 409 | 2 |
| `VIOLENCIA` | ENSU | 12 634 | 1 |
| `VIOLENCIA` | ENVIPE | 171 | 2 |

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
- **Pisos de FIRMAS-20** (`GEN2-TRAMITE-FIRMAS-20` §1 A1–A6; una fila por celda `-P` con punto, IC calibrado de persistencia donde el CALC lo trae):
  - A1 ENSU (`FP-260926-GEN2-SEGURIDAD-ENSU-SERIE-1-5916-01`): pisos 2024T1/2025T3/2025T4 y serie trimestral, **con reserva de ancho**; los cuatro hábitos con «No aplica» en el denominador no se comparan con comunicados.
  - A2 CCPV 2010, A3 EMAT, A4 EDR, A5 ENPECYT (`FP-260926-GEN2-COLA-LOTE-1-3a49-01` a `-04`), **con reserva de ancho**. EMAT es matrimonio civil inscrito, no unión; EDR es composición de defunciones registradas (unidad defunción), nunca tasa por habitante; ninguno de los dos tiene IC de diseño (registro completo).
  - A6 (`FP-260926-GEN2-COLA-COMPLETA-1-0d4a-01`): ENDISEG 2021, MMSI 2016, ENASEM 2021, ENVIPE 2024 (percepción; unidad persona) y ENOE 2024T4 **adoptados**; Latinobarómetro 2023 (complemento), PEW 2024 y ENADID 2018 **con reserva de ancho**; **Intercensal 2015 VETADA** (payload solo del Estado de México): fuera, con fila por RESULT en `data/corrida0/decisiones.tsv`.
- **Bloque de adopción v1.4 — merge de mesa** (`MERGE-DE-MESA:GEN2-CIERRE-Y-PRODUCTO-3`; solo CALC que el registro del commit ve `SELLADA` con `cuenta_gen2=SI`, constancia `registro-semana-v1_4.tsv`). Dominio: PROPUESTO-POR-EJECUTOR, leído de la nota del acto emisor.

| CALC | instrumento · ola | dominio | unidad | propuesta | alcance | holdout gastado | filas |
|---|---|---|---|---|---|---|---:|
| `CALC-ENCIG2023-CONFIANZA-PISOS-0001` | ENCIG 2023 | `CONFIANZA` | proporcion (persona 18+  ciudades de 100 000+) | **CON-RESERVA-DE-ANCHO** | PISO-DESCRIPTIVO-DE-OLA | — | 1 075 |
| `CALC-PDR1-ENCUCI2020-0002` | ENCUCI 2020 | `AUTORIDAD` | proporcion (persona) | **CON-RESERVA-DE-ANCHO** | PISO-DESCRIPTIVO-DE-OLA | — | 142 |
| `CALC-PDR1-ENSU2024-0001` | ENSU 2024 | `SANCION_SOCIAL` | proporcion (persona 18+ urbana) | **CON-RESERVA-DE-ANCHO** | PISO-DESCRIPTIVO-DE-OLA | — | 9 |
| `CALC-PDR1-ENUT2024-0001` | ENUT 2024 | `TIEMPO` | proporcion (persona) | **CON-RESERVA-DE-ANCHO** | PISO-DESCRIPTIVO-DE-OLA | — | 104 |
| `CALC-PDR1-ENADID2023-0001` | ENADID 2023 | `RURAL_INDIGENA` | diferencia de proporciones (persona) | **CON-RESERVA-DE-ANCHO** | PISO-DESCRIPTIVO-DE-OLA | — | 51 |
| `CALC-PDR1-ENIGH2022-0001` | ENIGH 2022 | `CONOCIMIENTO` | proporcion (hogar) | **CON-RESERVA-DE-ANCHO** | PISO-DESCRIPTIVO-DE-OLA | — | 128 |
| `CALC-PDR1-ENVIPE2025-0001` | ENVIPE 2025 | `CAPITAL_SOCIAL` | puntos porcentuales (diferencia en diferencias; persona  estrato del área) | **CON-RESERVA-DE-ANCHO** | PISO-DESCRIPTIVO-DE-OLA | — | 47 |
| `CALC-ALT-M05-LAPOP2019-0001` | LAPOP 2019 | `POLITICA` | proporcion (persona) | **CON-RESERVA-DE-ANCHO** | CONTRASTE-DE-MOMENTO | NINGUNO | 13 |
| `CALC-ALT-M05-LAPOP2021-0001` | LAPOP 2021 | `POLITICA` | proporcion (persona) | **CON-RESERVA-DE-ANCHO** | CONTRASTE-DE-MOMENTO | NINGUNO | 25 |
| `CALC-ALT-M13-CIDECSES2015-0001` | CIDE-CSES 2015 | `POLITICA` | proporcion (persona) | **CON-RESERVA-DE-ANCHO** | CONTRASTE-DE-MOMENTO | M13 | 4 |
| `CALC-ALT-M19-ENCUCI2020-0001` | ENCUCI 2020 | `CONFIANZA` | proporcion (persona) | **CON-RESERVA-DE-ANCHO** | CONTRASTE-DE-MOMENTO | M19 | 37 |
| `CALC-ALT-M19-WVS2018-REPRO-0001` | WVS 2018 | `CONFIANZA` | proporcion (persona) | **CON-RESERVA-DE-ANCHO** | CONTRASTE-DE-MOMENTO | M19 | 2 |
| `CALC-ALT-M22-ENVIPE2025-0001` | ENVIPE 2025 | `VIOLENCIA` | proporcion (delito) | **CON-RESERVA-DE-ANCHO** | CONTRASTE-DE-MOMENTO | M22 | 33 |
| `CALC-ALT-M23-ENSAFI2023-0001` | ENSAFI 2023 | `DINERO` | proporcion (persona) | **CON-RESERVA-DE-ANCHO** | CONTRASTE-DE-MOMENTO | M23 | 16 |
| `CALC-ALT-R03-ENCRIGE2020-0001` | ENCRIGE 2020 | `CONFIANZA` | proporcion (empresa) | **CON-RESERVA-DE-ANCHO** | CONTRASTE-DE-MOMENTO | NINGUNO | 27 |
| `CALC-ALT-R03-ENVE2024-0001` | ENVE 2024 | `CONFIANZA` | proporcion (unidad económica) | **CON-RESERVA-DE-ANCHO** | CONTRASTE-DE-MOMENTO | NINGUNO | 9 |
| `CALC-PISO-PERSISTENCIA-ERROR-0002` |   | `—` | — | **NO-ENTRA** | EVALUACION-NO-ESTIMADOR | — | 0 |
| `CALC-DIN-OFERTA-EXCLUSION-ENIF2024-0001` |   | `—` | — | **NO-ENTRA** | MEDIDA-DE-OFERTA-NO-ESTIMADOR | — | 0 |

- **Bloque ENIGH — Firma M** (`GEN2-ADOPCION-BLOQUE-Y-PINES-1`): descriptores de intensidad de remesas 2016, 2018 y 2020 con IC bootstrap.

**Ejes.** Sexo, edad, escolaridad, localidad (tamaño) y entidad —el eje regional disponible con RESULT adoptado— salen de las tablas ENOE, ENDIREH, ENDUTIH y ENIGH-consumo; formalidad y cuenta, de las marginales ENIF. **NSE entra como eje con reserva de instrumento** (`FP-260924-GEN2-CLASE-AMAI-1-e773-01`, FIRMAS-16): ENIGH 2022 (regla AMAI reproducida), ENIF 2024 (aproximación conforme) y ENDUTIH 2023 como aproximación rotulada; ENDUTIH 2024–2025 (`DESVIADA`) quedan fuera por la letra de la firma (60 celdas). La región de seis zonas de `canon/eje-regional-v1_0.md` es propuesta sin adopción: no aporta filas.

### Pendiente de firma (no entran; no es PARO)

| id | objeto | estado de la FP |
|---|---|---|

`SIN-FP-CITABLE`: RESULT con consumo activo que el contador de adoptados cuenta por la etiqueta de su propia spec (E.2), pero sin FP firmada, sin fila de mesa en `decisiones.tsv` para su CALC y sin firma de encargo en su pin. El catálogo no les inventa firma. La firma `FP-260925-GEN2-CATALOGO-V1-1-1-afe1-01` (FIRMADA, opción a) los hace entrar en v1.2 citándola.

### Propuestas de reglas recibidas (no son filas del catálogo)

Heredado de v1.3 (FIRMAS-20 C: propuestas editoriales recibidas **sin adopción**). Las reglas con cifra de esta semana van al bloque de reglas [`canon/reglas-bloque-adopcion-1.md`](reglas-bloque-adopcion-1.md), no a esta tabla. Ninguna entra como regla SI-ENTONCES en v1.4: cada una necesita su comparador y su falsador antes de integrarse.

| id | qué se recibe |
|---|---|
| `FP-260926-GEN2-ASTRA6-C3-CONSUMO-FAMILIA-1-edf7-01` | Adopción futura de las reglas; no bloquea reports v2 |
| `FP-260926-ASTRA6-C3-SOCIAL-1-5803-01` | adopción por contenido; no bloquea reports |
| `FP-260926-GEN2-ASTRA6-C3-TRABAJO-MOVILIDAD-1-ed83-01` | adopción de reglas; no bloquea propuesta editorial |
| `FP-260926-GEN2-ASTRA6-C3-TRABAJO-MOVILIDAD-1-ed83-02` | adjudicación de incidente y uso de reports clase y movilidad; no autoriza abrir ola |
| `FP-260926-GEN2-ASTRA6-C3-CONSUMO-FAMILIA-2-9d28-01` | Adopción futura de contenido; no bloquea corrección de reports ni constituye firma dada |
| `FP-260926-ASTRA6-C3-GENERO-VIOLENCIA-SALUD-1-92f8-01` | Adopción futura por contenido; no bloquea reports |
| `FP-260927-GEN2-RECIBO-ASTRA6-1-beee-02` | CATALOGO-V1-3-1 |

### Fuera por regla

Detalle por llave en `forense/analisis/catalogo/v1_4/excluidos-v1_4.tsv`:

- Piso **HEREDADO-DE-LEGACY** (0 RESULT del censo de `GEN2-ENCIG-PISOS-GEN2-1`): `GEN2-PISOS-GEN2-2` cerró (`PR #1123`) re-midiéndolos con sucesores `-0002` sellados; **ninguna fila de esta tabla es HEREDADO-DE-LEGACY** (pisos por origen: `NUEVO` o `HEREDADO-DE-GEN2`).
- Celdas FIRMAS-19 con punto nulo: 1 306.
- Celdas ENDUTIH originales de empleo excluidas por la propia firma: 141.
- Celdas sin punto publicable: suprimidas 613 + 3 + 2, no estimables 30.
- Intercensal 2015, vetada por FIRMAS-20 A6: 160 celdas.
- Marginales sin adopción en nivel (ENCIG 2025, vetada): 10.
- Sellados de la semana que no son estimador de conducta: la evaluación `CALC-PISO-PERSISTENCIA-ERROR-0002` (2 evaluaciones en total, con el duelo ENIGH) y la medida de oferta de cuenta ENIF 2024 (1; va citada en `oferta_exclusion`).
- Nodos de tablas de momento sin punto estimable: 8.
- Tablas ENIGH adoptadas por Firma M y no desagregadas en esta versión (perfil estructural y remesas en contexto): 6 CALC. La evaluación de origen móvil del duelo ENIGH mide error de candidatos, no una conducta.

## P3 · Cobertura de los reports del corpus

Unidad: los 31 reports de `corpus/reports/` (el conteo de «dominios» de la ADENDA-2 y del README), cada uno asignado a su dominio primario por `forense/analisis/dominios/report-a-dominio-v1_0.tsv`; los conteos de afirmaciones salen de `canon/mapa-dominios-v1_1.tsv`. Regla, en orden (la primera que se cumple):

- `MEDIDO` — el dominio tiene al menos un estimador en esta tabla.
- `EN-MEDICIÓN` — hay CALC con `cuenta_gen2: SI` sellados para un instrumento del dominio, sin adopción todavía (ENCUP/LAPOP/INE, ENADID, ENCUCI y los demás instrumentos de la regla del generador).
- `MEDIBLE-EN-CORPUS-SIN-CALC` — el mapa dictamina afirmaciones medibles con lo que ya hay en el corpus, pero nadie corrió el mecanismo. Es un «nadie corrió» (§2), no un «no se puede»: por eso no se funde con la categoría siguiente.
- `MEDIBLE-CON-ADQUISICIÓN` — solo medible si se adquiere el instrumento.
- `NO-MEDIBLE-POR-DISEÑO` — todas sus afirmaciones lo son.

| estado | reports |
|---|---:|
| MEDIDO | 23 |
| EN-MEDICIÓN | 0 |
| MEDIBLE-EN-CORPUS-SIN-CALC | 3 |
| MEDIBLE-CON-ADQUISICIÓN | 4 |
| NO-MEDIBLE-POR-DISEÑO | 0 |
| SIN-AFIRMACIONES-EN-MAPA | 1 |

| report | dominio (mapa U0) | estado | estimadores v1.4 | CALC GEN2 sin adoptar | afirmaciones (en corpus / con adquisición / no medibles) |
|---|---|---|---:|---:|---|
| Adopción y Resistencia Tecnológica en México  La Paradoja de la Baja C | `TECNOLOGIA` | **MEDIDO** | 1827 | 0 | 49 (19 / 16 / 14) |
| Ausencia sin certeza  duelo y pérdida ambigua en familias de personas  | `DUELO` | **MEDIBLE-EN-CORPUS-SIN-CALC** | 0 | 0 | 33 (3 / 23 / 7) |
| Autoridad y jerarquía en el México contemporáneo  anatomía psicológica | `AUTORIDAD` | **MEDIDO** | 142 | 0 | 39 (9 / 18 / 12) |
| Behavioral Finance Mexicano  Estructura  Adaptación Racional y Cultura | `DINERO` | **MEDIDO** | 124 | 0 | 179 (41 / 82 / 50) |
| Confianza y Desconfianza en México  Anatomía Psicológica de una Socied | `CONFIANZA` | **MEDIDO** | 2020 | 0 | 59 (22 / 19 / 15) |
| El Clasemediero Mexicano  Identidad  Ansiedad de Estatus y el Miedo Ra | `MOVILIDAD` | **MEDIDO** | 172 | 7 | 56 (5 / 37 / 11) |
| El Efecto Ambiental de la Violencia Crónica en México  Cómo el Miedo R | `VIOLENCIA` | **MEDIDO** | 12805 | 0 | 56 (17 / 30 / 9) |
| El Mexicano y el Tiempo  Estructura  no Cultura  en la Planeación y el | `TIEMPO` | **MEDIDO** | 78 | 5 | 20 (4 / 6 / 10) |
| El México Rural e Indígena en sus Propios Términos  Comunalidad  Autor | `RURAL_INDIGENA` | **MEDIDO** | 77 | 0 | 56 (8 / 28 / 19) |
| Elegir  Cortejar y Amar en el México de Hoy  Díada de Pareja  Apps de  | `PAREJA` | **MEDIDO** | 3304 | 0 | 32 (3 / 16 / 13) |
| Genetica y Conducta del Mexicano Contemporaneo  Canal Individual vs  E | `GENETICA` | **MEDIBLE-CON-ADQUISICIÓN** | 0 | 0 | 38 (0 / 35 / 3) |
| Health  Body  Food and Substance Use in Mexico  The Behavioral Layer o | `SALUD` | **MEDIDO** | 800 | 3 | 64 (13 / 31 / 20) |
| Humor in Mexican Psychological Life  2023-2026 Update | `HUMOR` | **MEDIBLE-EN-CORPUS-SIN-CALC** | 0 | 0 | 29 (1 / 16 / 12) |
| La arquitectura invisible de la interacción social en México | `INTERACCION` | **MEDIBLE-CON-ADQUISICIÓN** | 0 | 0 | 21 (0 / 13 / 8) |
| La familia mexicana como sistema psicológico  entre el afecto  la obli | `FAMILIA_CUIDADOS` | **MEDIDO** | 1449 | 0 | 46 (7 / 25 / 13) |
| Mexican Population Genomics  2025-2026 Scientific and Market Opportuni | `GENOMICA` | **MEDIBLE-CON-ADQUISICIÓN** | 0 | 0 | 33 (0 / 26 / 6) |
| Moral Emotions in Mexico  Declared Dignity  Relational Face  and Resid | `EMOCIONES_MORALES` | **MEDIBLE-CON-ADQUISICIÓN** | 0 | 0 | 26 (0 / 17 / 8) |
| Mérito  Movilidad Social y Desigualdad en México  Actualización 2025-2 | `MOVILIDAD` | **MEDIDO** | 172 | 7 | 56 (5 / 37 / 11) |
| Non-Family Social Capital in Mexico  Cooperation  Trust  and Collectiv | `CAPITAL_SOCIAL` | **MEDIDO** | 661 | 8 | 30 (9 / 8 / 13) |
| Psicología Política y Comportamiento Cívico del Mexicano Contemporáneo | `POLITICA` | **MEDIDO** | 126 | 13 | 90 (21 / 41 / 28) |
| Psicología  Conducta y Sociedad en el México Contemporáneo  Análisis T | `SINTESIS` | **SIN-AFIRMACIONES-EN-MAPA** | 0 | 0 | 0 (0 / 0 / 0) |
| Psicología de la Juventud Mexicana Contemporánea  Gen Z y Millennials  | `JUVENTUD` | **MEDIBLE-EN-CORPUS-SIN-CALC** | 0 | 0 | 29 (4 / 12 / 11) |
| Psicología del Consumidor Mexicano  Patrones  Contradicciones y Estrat | `CONSUMO` | **MEDIDO** | 4470 | 0 | 81 (3 / 42 / 36) |
| Psicología del Trabajo en México  Un Mapa Basado en Evidencia | `TRABAJO` | **MEDIDO** | 26409 | 0 | 85 (13 / 47 / 24) |
| Psychology of Mexico-US Migration  Identity  Family  Aspiration  and W | `MIGRACION` | **MEDIDO** | 126 | 3 | 58 (6 / 27 / 24) |
| Reconfiguración de los Guiones de Género en México  Masculinidades  Fe | `GENERO` | **MEDIDO** | 7311 | 0 | 47 (10 / 22 / 14) |
| Religiosidad y Psicología del Mexicano Contemporáneo  Moral  Afrontami | `RELIGIOSIDAD` | **MEDIDO** | 404 | 0 | 39 (7 / 20 / 9) |
| Report 26  The Contemporary Mexican and Knowledge  Expertise  Educatio | `CONOCIMIENTO` | **MEDIDO** | 408 | 0 | 26 (0 / 15 / 11) |
| Salud Mental en México  Prevalencia  Estigma y la Brecha entre Necesid | `SALUD_MENTAL` | **MEDIDO** | 2758 | 1 | 62 (8 / 43 / 11) |
| Sanción Social Horizontal en México  Chisme  Envidia y Mal de Ojo como | `SANCION_SOCIAL` | **MEDIDO** | 9 | 0 | 13 (2 / 2 / 9) |
| Vejez y Cuidado Intergeneracional en México  El Debilitamiento del Seg | `FAMILIA_CUIDADOS` | **MEDIDO** | 1449 | 0 | 46 (7 / 25 / 13) |

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
10. **Seguridad — denuncia con seguro (ENVIPE 2025, piso t−1, unidad delito) · SUSPENDIDA EN v1.4.** Sus dos RESULT quedan `SUSPENDIDA-POR-FIRMA` (R21, `fb50-02`): la regla **no se sostiene con cifra en esta versión** hasta que su sucesor se mida. Texto de v1.3, conservado para auditoría: **SI** el delito afecta a un bien asegurado **ENTONCES** se denuncia 0.774 [0.711, 0.833], contra 0.634 [0.585, 0.682] sin seguro — **PORQUE** la aseguradora exige la denuncia: incentivo, no confianza (adaptación racional) — **[FUERTE descriptiva; mecanismo MEDIA]**. Unidad delito: no se compara con proporciones de personas. Falsador: igual diferencia en delitos cuyo seguro no exige denuncia.

### Reglas nuevas con el bloque v1.4 (todas RETROSPECTIVAS, una ola, con reserva de ancho)

Las reglas contrastadas de la semana (`canon/reglas-contrastadas-v1_1.tsv`) tienen su propio bloque de adopción: [`canon/reglas-bloque-adopcion-1.md`](reglas-bloque-adopcion-1.md). Aquí solo se leen las cifras que dan estimador a un dominio por primera vez.

11. **Sanción social — `SANCION_SOCIAL` (ENSU 2024T1, persona `18+` urbana).** La proporción que declara lo que mide SANC-007 es 0.474 [0.465, 0.483]; mujeres 0.537 [0.525, 0.549] contra hombres 0.400 [0.387, 0.413] — **PORQUE** —(sin driver identificado: una ola urbana) — **[MEDIA descriptiva, CONFIRMA en conducta; universo urbano]**. Falsador: una ola rural o no urbana con IC que excluya el punto.
12. **Autoridad — `AUTORIDAD` (ENCUCI 2020, persona).** Confía mucho (`8–10`) en servidores públicos 0.139 [0.132, 0.146]; rural 0.167 [0.154, 0.181] contra urbano 0.131 [0.121, 0.141] — **[MEDIA descriptiva; una ola]**. No es «deferencia a la autoridad» como rasgo: mide confianza declarada, sin trato observado.
13. **Tiempo y comunidad — `RURAL_INDIGENA` (ENUT 2024, persona).** Participación en trabajo comunitario, rural menos urbano: 0.056 [0.047, 0.065] — **PORQUE** la organización comunitaria es institución, no preferencia (hipótesis) — **[HIPÓTESIS RAZONABLE: una ola; el tamaño del efecto acota la «comunalidad» a unos puntos]**. Falsador: que la diferencia se anule al condicionar por tamaño de localidad y régimen de tenencia.
14. **Brecha rural e indígena en tecnología — `RURAL_INDIGENA` (ENADID 2023, diferencia de proporciones).** Brecha total de TEC-010 0.052 [0.048, 0.056]; crece con la edad: `15–29` 0.006 [0.004, 0.008], `60+` 0.134 [0.123, 0.145] — **[MEDIA descriptiva; MATIZA el report: sus `19 %` y `24.2 %` no reproducen]**. Es una brecha de acceso (oferta) antes que de disposición.
15. **Educación privada — `CONOCIMIENTO` (ENIGH 2022, hogar).** Diferencia de asistencia a escuela privada, deciles V–VIII menos I–IV, urbano: 0.073 [0.063, 0.082]; rural 0.043 [0.034, 0.052] — **PORQUE** el ingreso compra oferta privada donde la hay (estructura) — **[HIPÓTESIS RAZONABLE]**. Unidad hogar.
16. **Ahorro informal por tamaño de localidad — `DINERO` (ENSAFI 2023, contraste de momento M23, holdout gastado).** Ahorro solo informal: menos de `2 500` habitantes 0.313 [0.296, 0.331] contra `100 mil` y más 0.228 [0.214, 0.242]; contraste rural−urbano 0.085 [0.064, 0.108] — **PORQUE** oferta formal ausente en localidades chicas (oferta antes que preferencia) — **[MEDIA descriptiva]**. Oferta al lado: la exclusión por oferta sellada es de crédito ENIF y de cuenta ENIF 2024, no de ENSAFI (columna `oferta_exclusion`).
17. **Denuncia y miedo — `VIOLENCIA` (ENVIPE 2025, unidad DELITO, momento M22, holdout gastado).** Proporción de delitos no denunciados por miedo: 0.080 [0.072, 0.091] — unidad delito: no se compara con proporciones de personas.

## P4 · Dónde sí cambió

El dictamen por serie vive en [`canon/donde-cambio-el-mexicano-v1_0.md`](donde-cambio-el-mexicano-v1_0.md) (`GEN2-DONDE-CAMBIO-EL-MEXICANO-1`, RETROSPECTIVA, sin adopción). Conteo por comando sobre `forense/analisis/donde-cambio/tabla-dictamen-v1_0.tsv`: 7 872 series · 583 `ESTABLE` · 8 `CAMBIO-SOSTENIDO` (3 suben, 5 bajan) · 81 `SALTO-SIN-EXPLICAR` (el `SALTO` del encargo) · 7 200 `SIN-SERIE`.

Lectura para el catálogo: los cambios sostenidos son todos ENOE y de décimas de punto; la mayoría de las series no tiene tres olas comparables. **La afirmación «el mexicano cambió en X» no tiene respaldo en este corpus fuera de esas series**, y ninguna frase de este catálogo la hace. «Cambió» es un hecho de la serie, no de la psicología.

## P4 · Cobertura por clase

Cita de [`forense/analisis/clase-amai/cobertura-por-clase-v1_0.md`](../forense/analisis/clase-amai/cobertura-por-clase-v1_0.md) (`GEN2-CLASE-AMAI-1`, RETROSPECTIVA): hay pisos por NSE AMAI en 144 celdas (`pisos-nse-v1_0.tsv`); con la firma `FP-260924-GEN2-CLASE-AMAI-1-e773-01` entran al catálogo las de ENIGH 2022, ENIF 2024 y ENDUTIH 2023 (eje `NSE`). Las cifras por clase de este catálogo son esas filas; la lectura de abajo es la del documento citado. El hallazgo que el catálogo hereda como reserva: el corte de clase solo es posible hoy en dinero (ENIF), remesas (ENIGH) y tecnología (ENDUTIH). Lo cívico y el trato con el Estado (ENVIPE, ENCIG) no admiten NSE AMAI por construcción del cuestionario, y ahí el único corte socioeconómico es la escolaridad. Varios gradientes que parecen cultura (horizonte de ahorro corto, no usar internet por costo) son de clase según ese documento; la desconfianza declarada no muestra gradiente medible.

## Módulo de auditoría de rigor extremo

- **¿Cuántos contadores movió este trabajo?** Cero mediciones. Si mesa fusiona: «estimadores con RESULT» y `mapa11_dominios_medidos` (17 → 21); la adopción es el merge, no una decisión del ejecutor.
- **¿Qué cifra es PROSPECTIVA y cuál RETROSPECTIVA?** El bloque v1.4 y el tercer lote son RETROSPECTIVOS (olas vistas); las 20 filas PROSPECTIVAS son árbitros de celdas prospectivas del marcador, en su propia columna. Los momentos con holdout gastado lo dicen en su fila: ya no pueden servir de prueba prospectiva de ese momento.
- **¿Pobreza, informalidad o violencia confundidas con cultura?** Las reglas de trabajo y tecnología leen primero estructura y oferta; ninguna regla atribuye un gradiente a «cultura mexicana».
- **¿Sobregeneralización desde la clase media urbana?** Los ejes de localidad (ENOE `MENOS-2K5`, ENDUTIH `TLOC_4`) están en la tabla. El eje NSE adoptado corta clase solo en dinero, remesas y tecnología: en lo cívico y en el trato con el Estado sigue sin corte de clase posible.
- **¿Qué cambia con foco rural o indígena?** El gradiente rural de informalidad y costo digital es el más grande del catálogo. Lo indígena-comunal queda fuera por diseño y ningún instrumento adoptado lo identifica.
- **¿Qué parece psicológico y es incentivo?** La denuncia con seguro (regla 10) y la denuncia de violencia (regla 6).
- **¿Evidencia débil con intuición fuerte?** Todos los PORQUE. Por eso llevan tier propio.
- **¿Qué afirmación sobre el corpus se escribió a mano?** Ninguna cifra: toda cifra sale de un marcador de conteo o de RESULT de la plantilla (`forense/analisis/catalogo/v1_4/plantilla-v1_4.md`), y `tests/test_catalogo_v1_4.py` falla si aparece un dígito fuera de un identificador, un año o un placeholder resuelto.
- **¿Deuda asumida que caducó?** La regla 10 (denuncia con seguro) se sostenía en v1.3 con dos RESULT que R21 retiró del universo C1: queda suspendida, con texto conservado. La desagregación de las tablas ENIGH de Firma M, prometida para v1.4, no entra (NC re-diferida). Una fila `SOSTENER-SIN-CORROBORACION` del tercer lote no es una fila validada.
- **¿Qué cambia con foco rural o indígena?** v1.4 da por primera vez estimador al dominio `RURAL_INDIGENA` (ENUT, ENADID): diferencias de pocos puntos, que acotan cualquier lectura de «comunalidad» como rasgo; la huella indígena difusa se mapea, el sistema comunal vivo sigue fuera por diseño.
- **¿Sesgo de marcos o muestras importadas?** WVS, Latinobarómetro, PEW y LAPOP son marcos internacionales: sus ejes son los del cuestionario (clase subjetiva, ingreso subjetivo), no NSE AMAI, y ninguna fila se lee como rasgo nacional esencial. PEW migración mide disposiciones, no flujos.
- **¿Escala de cada cantidad y contra qué se compara?** Columna `unidad`. Solo se contrastan filas del mismo CALC, unidad y ola.
- **¿PROSPECTIVA y RETROSPECTIVA mezcladas?** No: la columna `temporalidad` las separa y ninguna frase las suma; la validación ciega es RETROSPECTIVA (se comparó contra cifras ya selladas). Las celdas validadas PROSPECTIVAS se citan aparte en la frase de portada.
- **¿Unidades promediadas?** No: persona (ENOE, ENDIREH, ENDUTIH, ENIF, ENSU, ENPECYT, WVS, LAPOP), hogar (ENIGH, ENGASTO, CCPV), matrimonio o contrayente (EMAT), defunción (EDR), delito (ENVIPE marginales, momento M22), empresa y unidad económica (ENCRIGE, ENVE: tabulados sin IC), puntos porcentuales de diferencia en diferencias (`RG-b913`) y evento de trámite (ENCIG) nunca se suman ni se comparan sin función de enlace.
- **¿Qué sería peligroso leído simplista?** Leer la tabla de ENOE como «la informalidad es rural por cultura», una prevalencia ENDIREH como tasa anual, la composición EDR como tasa de suicidio, o EMAT como «los mexicanos se casan menos» (mide inscripción civil, no unión).
