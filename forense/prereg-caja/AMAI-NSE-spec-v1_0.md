# AMAI-NSE · nivel socioeconómico AMAI por instrumento y pisos por NSE · spec humana v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

Acto `GEN2-CLASE-AMAI-1` (encargo `forense/encargos/2026-09-24-GEN2-CLASE-AMAI-1.md`). Seis CALC, un medidor (`tools/dominios/amai/medidor.py`, copiado byte a byte como `medidor.py` de cada CALC). RETROSPECTIVA; `cuenta_gen2: SI`; `adopta: NO`. Esta spec basta para recalcular sin leer el código (D-15); donde no baste, es hallazgo.

## §1 · Regla

Regla NSE AMAI 2024 = regla 2022 ratificada sin cambios (nota metodológica AMAI 2024, octubre 2023, pp. 15–16; `data/raw/amai/NOTA_METODOLOGICA_NSE_AMAI_2024_v6.pdf`, sha256 `c268c3dc9f39bcc9b4de573429806fb787b141e2219501684e8bd566b87d89d1`). Unidad: **hogar**. Seis componentes y puntos, transcritos del Anexo «Códigos de Análisis en R», pp. 16–17:

| Componente | Puntos |
|---|---|
| Escolaridad de la jefatura (`educa_jefe` 01..11) | 01–02: 0 · 03: 6 · 04: 11 · 05: 12 · 06: 18 · 07: 23 · 08: 27 · 09: 36 · 10: 59 · 11: 85 |
| Baños completos | 0: 0 · 1: 24 · 2+: 47 |
| Autos (auto + van + pickup) | 0: 0 · 1: 22 · 2+: 43 |
| Internet (`conex_inte = 1`) | no: 0 · sí: 32 |
| Ocupados | 0: 0 · 1: 15 · 2: 31 · 3: 46 · 4+: 61 |
| Cuartos para dormir | 0: 0 · 1: 8 · 2: 16 · 3: 24 · 4+: 32 |

Cortes (a,b]: E ≤ 47 < D ≤ 94 < D+ ≤ 115 < C− ≤ 140 < C ≤ 167 < C+ ≤ 201 < A/B. INTERPRETACIÓN-DECLARADA: el `cut` del Anexo deja el puntaje 0 fuera de (0,47]; aquí 0 → E y la masa con puntaje 0 se reporta aparte (`masa_puntaje_cero`). Hogar con cualquier componente no válido: sin NSE (el Anexo excluye «casos en donde alguna de las variables … no contaba con datos válidos», p. 3); se reporta su conteo.

## §2 · Agrupación y umbrales — congelados aquí, antes de abrir microdato

- **Agrupación primaria de los pisos** (tres grupos): **BAJO** = E, D, D+ · **MEDIO** = C−, C · **ALTO** = C+, A/B. Los siete niveles se reportan sólo como distribución de hogares, no como pisos.
- **Supresión (F-U5-2)**: `SUPRIMIDA-N` si n < 200 personas/hogares del denominador en el grupo; `VARIANZA-NO-ESTIMABLE` en los casos del estimador U5 (réplica sin denominador, < 2 UPM, dispersión nula). No se ajusta con el resultado.
- **Validación**: referencia = distribución nacional publicada de hogares, ENIGH 2022 (nota, p. 4, Figura 1): E 8.7 · D 25.4 · D+ 14.9 · C− 16.4 · C 15.3 · C+ 12.0 · A/B 7.3 (%) → BAJO 49.0 · MEDIO 31.7 · ALTO 19.3.
  - ENIGH 2022 (CALCULABLE): `CALCULABLE-REPRODUCE-AMAI` si los siete niveles caen a ≤ 0.15 pp de la figura (redondeo a un decimal); si no, `CALCULABLE-NO-REPRODUCE-AMAI` (hallazgo, no PARO).
  - Aproximaciones: `APROXIMACION-DESVIADA` si algún grupo se desvía **más de 5.0 pp** de la referencia; si no, `APROXIMACION-CONFORME`. El umbral admite deriva 2022→2024/25 (la nota reporta movimientos de hasta ~3 pp entre ENIGH 2020 y 2022, Figura 2) y no se ajusta con el resultado. Una ola `DESVIADA` sigue midiendo sus pisos, rotulados así.
- **Factibilidad por texto** (P1): CALCULABLE = los seis componentes exactos; APROXIMABLE = al menos cuatro de seis presentes (exactos o aproximados), escolaridad de la jefatura entre ellos; NO-CONSTRUIBLE en otro caso. Tabla y citas en `forense/analisis/clase-amai/factibilidad-v1_0.md`.

## §3 · Escolaridad de la jefatura fuera de ENIGH

Jefatura: parentesco = 1 (ENIF 2024 `PAREN`, ENIF 2021 `P2_3`, ENDUTIH `PAREN`); un hogar con dos jefaturas es error (el medidor para). Nivel/grado → `educa_jefe` con la regla de construcción de ENIGH 2022 (Descripción de la base, concentradohogar #12): 00→01; 01→02; primaria grado < 6 → 03, ≥ 6 → 04; secundaria grado < 3 → 05, ≥ 3 → 06; preparatoria grado < 3 → 07, ≥ 3 → 08; licenciatura grado < 4 → 09, ≥ 4 → 10; maestría y doctorado → 11. Normal básica y estudios técnicos con secundaria terminada → 06 y técnicos con preparatoria terminada → 08 (regla ENIGH: técnica/normal al nivel de su antecedente escolar). INTERPRETACIÓN-DECLARADA: especialidad → 11. «No sabe», blanco o grado no numérico donde el nivel lo exige → sin dato. Códigos: ENIF 2024 y ENDUTIH 2023–2025 (04 normal básica, 05 técnica con secundaria, 07 técnica con preparatoria, 09 especialidad, 10 maestría, 11 doctorado); ENIF 2021 (04 técnica con secundaria, 05 normal básica, 07 técnica con preparatoria, 09 maestría o doctorado). Un código fuera del codebook detiene el medidor.

## §4 · Construcción por instrumento

**4.1 · ENIGH 2022 — CALCULABLE** (`CALC-AMAI-NSE-ENIGH-2022-0001`, payload `enigh2022_nc_csv`). Réplica del Anexo: concentradohogar ⋈ hogares por (folioviv, foliohog) ⋈ viviendas por folioviv. `educa_jefe` y `ocupados` de concentradohogar; `conex_inte`, `num_auto+num_van+num_pickup` de hogares; `cuart_dorm`, `bano_comp` de viviendas. Factor `factor`, estrato `est_dis`, UPM `upm` de concentradohogar. ENIGH 2024 está RESERVADA (`decisiones.tsv` `reserva:enigh2024`) y no se abre.

**4.2 · ENIF 2021 y 2024 — APROXIMABLE** (`CALC-AMAI-NSE-ENIF-2021-0001`, `CALC-AMAI-NSE-ENIF-2024-0001`). Vivienda (TVIVIENDA, compartida por sus hogares como el merge por folioviv del Anexo): dormitorios `P0_1`; baños completos `P0_3`; autos `P0_4_1`=2 → 0, =1 → `P0_4_1A`; internet = 1 si `P0_4_2`=1 y `P0_4_2A`=1 (fijo), 0 si `P0_4_2`=2 o `P0_4_2A`=2. Hogar (THOGAR): ocupados = `P2_8` («¿Cuántas personas de su hogar tienen trabajo remunerado?» en 2024; «… trabajan?» en 2021) — **aproximación**: no filtra 14+ y en 2024 excluye trabajo sin pago; códigos > 90 → sin dato. Factor `FAC_HOG`; diseño `EST_DIS`, `UPM_DIS`. Llaves: 2024 `LLAVEVIV`/`LLAVEHOG`; 2021 (`FOLIO`,`VIV_SEL`)/(`FOLIO`,`VIV_SEL`,`HOGAR`). ENIF 2021 no tiene conducta adoptable en el catálogo U1 (sólo pisos históricos de crédito): su CALC construye y valida el NSE y no emite pisos.

**4.3 · ENDUTIH 2023, 2024, 2025 — APROXIMABLE** (`CALC-AMAI-NSE-ENDUTIH-<ola>-0001`). Observa: jefatura `PAREN`=1 con `NIVEL`/`GRADO`; ocupados = residentes con `EDAD` 14..97 y (`P3_10` ∈ {1,2} o `P3_11` ∈ {1,2,3}); internet = 1 si `P4_4`=1 y `P4_5` ∈ {1 sólo fija, 3 ambas}, 0 si `P4_4`=2 o `P4_5`=2; auto sí/no `P1_5_3` (vivienda). No observa baños ni dormitorios, ni el número de autos. **Aproximación declarada**: los puntos de baños + dormitorios + autos se sustituyen por su media ponderada (factor de hogar) en ENIGH 2022 (hogares con los seis componentes válidos, regla exacta) dentro de la celda (educa_jefe, internet, ocupados topado en 4, con_auto); celda con < 30 hogares donantes → (educa_jefe, internet, con_auto) → (con_auto). Determinista. El payload ENIGH 2022 entra como segundo input (`input_donante`). Factor `FAC_HOG`; diseño `EST_DIS`, `UPM_DIS`; llave (UPM, VIV_SEL, HOGAR).

**Diagnóstico de la aproximación ENDUTIH** (en el CALC ENIGH): se aplica la misma aproximación a los hogares ENIGH 2022 (autos a sí/no; baños, dormitorios y autos imputados) y se reporta la concordancia ponderada con la regla exacta, por nivel y por grupo. Es descriptivo; no cambia ningún estado.

**Diagnóstico de dominio de códigos** declarado antes de correr: ninguno fuera del medidor. Las guardias del medidor (código fuera del codebook, llave no única, doble jefatura) detienen la corrida en vez de imputar.

## §5 · Pisos por NSE

Estimador: `tools/astra/region/estadistica.py::estima_dominios` (U5, sha256 declarado en cada spec.yaml) con el grupo NSE del hogar como dominio (BAJO, MEDIO, ALTO; las personas/hogares sin NSE forman el dominio `SIN-NSE`, no publicado, y sus conteos se reportan). p_g = Σ w·1(D,g)·Y / Σ w·1(D,g). Plan común de 1 000 réplicas de UPM con reposición dentro de estrato sobre el marco completo de la tabla de la conducta (no se filtra antes de las réplicas), PCG64(20260924), módulo `tools/celda_d/marginales_reproduccion.py`; IC95 percentil. Las réplicas quedan en el JSON para las diferencias entre grupos (P4).

Conductas: las adoptables del catálogo U1 (`forense/analisis/catalogo/inventario-consumo-gen2.tsv`) en instrumentos con NSE construible y ola abierta, con la definición que ya tienen sellada:

- **ENIGH 2022** (unidad hogar, factor `factor`): `recibe_remesas` = `remesas` > 0 sobre todos los hogares de concentradohogar (definición de `CALC-B-0001`).
- **ENIF 2024** (unidad persona elegida 18+, factor `FAC_PER`, tabla TMODULO enlazada a su hogar por `LLAVEHOG`): las 7 del portafolio de ahorro (`tools/astra/region/enif_portafolio.py::desenlaces`), `tiene_ahorros_enif2024` (válido y no `no_tiene_ahorros`), las 6 condicionales de horizonte por seguridad social y desconfianza (`enif_condicionales.py::dominios_condicionales`), `horizonte_corto_no_trabaja` (`enif_no_trabaja.py::dominio`) y `recibe`/`no_recibe_dinero_familiares_para_vejez` (universo de `CALC-DINERO-FAMILIARES-VEJEZ-0001-v1_1`: `FILTRO_S9_1`=2, `EDAD_V` < 71, `P9_9_4` ∈ {1,2}; numerador `P9_9_4`=1 o =2). Ninguna toca la sección de crédito (RESERVADA, `reserva:enif2024-credito`).
- **ENDUTIH 2023–2025** (unidad persona de 6+ de la tabla usuarios, factor `FAC_PER`): diez medidas adoptadas por FIRMAS-15 T (`tools/dominios/endutih/pisos.py::_status`): `internet`, `celular`, `actividad_mensajes`, `actividad_tramite`, `no_internet_acceso|costo|preferencia`, `no_celular_costo|preferencia|cobertura`; denominador SI+NO. `actividad_empleo` queda fuera (su piso adoptado es el 15+ de los CALC sucesores; se declara en NO-CORRIDO).

## §6 · Salidas por CALC

`RESULT-AMAI-NSE-<INST>-<OLA>-JSON` (construcción, distribución, validación, pisos con réplicas, sha de módulos); `-DIST-<nivel|grupo>-P`; `-N-HOGARES-CON-NSE`, `-N-HOGARES-SIN-NSE`; `-VALIDACION-ESTADO`; `-DESVIO-MAX-GRUPO-PP`, `-DESVIO-MAX-NIVEL-PP`; en ENIGH `-PROXY-ENDUTIH-CONCORDANCIA-GRUPO|NIVEL`; por conducta y grupo `-<conducta>-<GRUPO>-P|IC-LO|IC-HI|N|ESTADO`. Tolerancia de `verify`: 1e-10 (mismo payload, orden y semilla).

## §7 · P4 y FP (derivados, no CALC)

`tools/dominios/amai/cobertura.py` lee los `resultados.json` sellados y escribe `forense/analisis/clase-amai/`: tabla conducta × grupo × ola; cobertura del catálogo U1 por clase (identidades con piso por NSE / identidades del catálogo; celdas publicables por grupo); potencia medida = IC95 de la diferencia ALTO − BAJO por réplica compartida (mismo plan de réplicas en los tres grupos) y cuántas despejan 0. La recomendación de FP (¿NSE entra al marcador como eje?) sale de esa potencia. Nada de esto adopta.

## Auditoría de rigor extremo

NSE AMAI mide bienes y capital escolar del hogar, no «clase» en sentido sociológico ni ingreso; tres de sus seis componentes (autos, internet, baños) son a la vez oferta de infraestructura: un gradiente por NSE en uso de internet o en ahorro formal mezcla preferencia con cobertura de red y de sucursales (§3: oferta antes que preferencia). ENDUTIH imputa 122 de 300 puntos posibles desde otra encuesta y otro año: su clasificación hereda la estructura conjunta de ENIGH 2022 y subestima la dispersión dentro de celda; sus pisos se leen como aproximación. ENIF usa ocupados remunerados sin corte de edad. Ningún piso aquí identifica un efecto de la clase: son asociaciones descriptivas (A-bis). La unidad de cada piso es la de su conducta (hogar en ENIGH, persona en ENIF y ENDUTIH) y ninguna cifra de hogar se promedia con una de persona. ENVIPE y ENCIG quedan NO-CONSTRUIBLE: el modelo no puede decir nada por clase AMAI sobre victimización ni trámites, y ese hueco es resultado, no omisión. Todo es RETROSPECTIVA.
