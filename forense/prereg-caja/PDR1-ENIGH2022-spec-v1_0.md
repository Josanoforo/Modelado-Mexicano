# PDR1 · pieza P-ENIGH2022 · spec v1.0 · CALC-PDR1-ENIGH2022-0001

ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1, pieza P-ENIGH2022, entorno CAJA. Rótulo: **RETROSPECTIVA**
(ENIGH 2022 es ola ya vista). PISO-DESCRIPTIVO-RETROSPECTIVO; no adopta; adopción por merge de mesa.
Universo de la pieza (tabla de apertura P1, `forense/analisis/pisos-dominios-1/tabla-apertura-v1_0.tsv`,
filas con `pieza = P-ENIGH2022`): **una** regla, `RG-cc1c9ab8f1` (dominio CONSUMO), payload
`enigh2022_nc_csv`. Nada fuera de ella se mide.

## 0 · Premisas verificadas antes del COMMIT-1

- `[EJECUTADO]` `corpus_loader.motivo_reserva('enigh2022_nc_csv', …)` → `LIBRE`.
- `[EJECUTADO]` Reserva E.6: existe en el manifiesto una ola posterior del programa (`enigh2024_nc_csv`,
  RESERVADA), luego 2022 **no** es la ola más reciente; y CALC sellados ya abrieron `enigh2022_nc_csv`
  (`rg -l enigh2022_nc_csv data/corrida0/*/spec.yaml`, con `sello.json`: CALC-ENIGH-CONSUMO-PISOS-0001/0002,
  CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0001/0002/0003, CALC-ENIGH2022-INTENSIDAD-REMESAS-0001,
  CALC-ENIGH2022-REMESAS-CONTEXTO-0001, CALC-ENIGH-0001, CALC-AMAI-NSE-ENIGH-2022-0001). ENIGH 2024
  (microdato, tabulados, comunicados) no se toca; el medidor lleva guardia contra `2024` en la ruta.
- `[EJECUTADO]` `python3 tools/ya_medido.py RG-cc1c9ab8f1` → `NUNCA-MEDIDA`. `rg -l -i 'tipoesc|colegia|E001'`
  sobre `data/corrida0/*/{spec.yaml,medidor.py}` → 0 de 724 archivos examinados (374 CALC previos, sin contar este): ningún RESULT sellado mide
  asistencia a escuela privada ni colegiaturas.
- **Lectura de estructura (permitida, no es dato)**: cabeceras de columnas de los miembros
  `concentradohogar`, `poblacion`, `gastospersona` y `gastoshogar` del ZIP (primera línea), y el descriptor
  `enigh2022_descripcion_base_pdf` (INEGI, *ENIGH 2022 Nueva serie. Descripción de la base de datos*, 2023).
  No se contó ninguna fila ni se tabuló ningún valor del microdato antes de este commit.

## 1 · E.5 · lo ya sellado se cita, no se re-mide

`CALC-ENIGH-CONSUMO-PISOS-0002` publica `RESULT-ENIGH-CONSUMO-PISOS-PART-EDUCA-ESPA-2022-DECIL-D01..D10-P`
(participación de *educación y esparcimiento* en el gasto monetario, por decil, ENIGH 2022). No es
equivalente (otro numerador —incluye esparcimiento y educación pública—, otro denominador —gasto, no
ingreso—, otro universo —todos los hogares—), por lo que no la sustituye: se cita como contexto en el
fragmento de dictámenes. La función de deciles se copia **idéntica** de ese CALC (misma regla de corte),
para que los deciles de ambos CALC sean el mismo objeto.

## 2 · Motivo no observable

La regla dice «SI el hogar es clase media urbana **con miedo a caer** ENTONCES elige escuela privada aunque
duela el bolsillo — PORQUE la privada opera como seguro anticaída y credencial». **El motivo («miedo a
caer», «seguro anticaída») NO es observable en ENIGH**: no hay reactivo de expectativa de movilidad ni de
temor. Se contrasta solo la **conducta observable** que la regla implica: (a) la frecuencia de pagar
colegiatura privada crece de los deciles bajos a los medios en lo urbano, y (b) la carga relativa de ese
pago en los deciles medios no es menor que en los altos («aunque duela»). Un CONFIRMA no confirma el
motivo; un ROMPE sí refuta la conducta que la regla predice.

## 3 · Códigos por texto (A.15), con página del descriptor

Páginas: «PDF p» = página del archivo; «impresa» = folio al pie.

| Uso | Variable (tabla) | Texto de pregunta / etiqueta | Códigos | Página |
|---|---|---|---|---|
| universo | `asis_esc` (POBLACION) | Cuestionario Hogares y vivienda, Sección III, P.15: «¿(NOMBRE) asiste actualmente a la escuela?» | 1 = Sí | PDF p76 / impresa 71 |
| privada | `tipoesc` (POBLACION) | Sección III, P.17: «¿La escuela a la que asiste (NOMBRE) es...» | 2 = «Privada o de paga» (1 Pública o de gobierno; 3 De otro tipo) | PDF p77 / impresa 72 |
| partida | `clave` (GASTOSPERSONA) | Catálogo de gastos, «EDUCACIÓN, CULTURA Y RECREACIÓN — GASTOS EN EDUCACIÓN BÁSICA, MEDIA O SUPERIOR» | E001 Preescolar, E002 Primaria, E003 Secundaria, E004 Preparatoria o bachillerato, E005 Profesional, E006 Maestría y doctorado, E007 Educación Técnica | PDF p219 / impresa 214 |
| monto | `inscrip` (GASTOSPERSONA) | Gastos del hogar, Sección I, Apartado 1.3, P.2: «De este gasto ¿cuánto pagó de inscripción?» | > 0 | PDF p128 / impresa 123 |
| monto | `colegia` (GASTOSPERSONA) | Apartado 1.3, P.3: «De este gasto ¿cuánto pagó de colegiatura?» | > 0 | PDF p128 / impresa 123 |
| monetario | `tipo_gasto` (GASTOSPERSONA) | «Tipo de gasto monetario y no monetario» | G1 = gasto monetario (G4 en especie: fuera) | PDF p125 / impresa 120 |
| carga, num. | `gasto_tri` (GASTOSPERSONA) | gasto trimestral de la partida (incluye el material de esa misma partida; declarado) | — | tabla GASTOSPERSONA |
| carga, den. | `ing_cor` (CONCENTRADOHOGAR) | «#23 ing_cor: Ingreso corriente» (trimestral) | > 0 | PDF p194 / impresa 189 |
| urbano/rural | `tam_loc` (CONCENTRADOHOGAR) | «Tamaño de localidad» | 1 ≥100 000; 2 15 000–99 999; 3 2 500–14 999; 4 < 2 500 hab. URBANO = 1–3, RURAL = 4 (umbral INEGI de 2 500) | PDF p45 / impresa 40 |
| segmentación | `sexo_jefe`, `edad_jefe` (CONCENTRADOHOGAR) | sexo y edad del jefe (1 hombre, 2 mujer; grupos HASTA-29, 30-44, 45-59, 60-MAS) | — | tabla CONCENTRADOHOGAR |

E015 (cuotas a padres de familia) y E016 (imprevistos) **no** entran: no son inscripción ni colegiatura.
La privacidad no sale del catálogo (que no distingue pública/privada) sino de `tipoesc` de **la misma
persona** (`numren`) que genera la partida: así una cuota de inscripción en escuela pública no se cuenta
como gasto privado.

## 4 · Estimandos, universo, unidad, ponderador, diseño

- **Unidad**: HOGAR (llave `folioviv`+`foliohog`; `folioviv` a 10 dígitos). Ponderador `factor`
  (CONCENTRADOHOGAR). Diseño: estrato `est_dis`, UPM `upm` (llaves opacas). Hogares con `factor>0` y
  diseño no vacío.
- **Universo U**: hogares con al menos un integrante con `asis_esc = 1` («al menos un integrante estudiando»;
  se prefiere a «edad escolar» porque la conducta solo existe donde alguien asiste).
- **PRIV** (0/1): hogar en U con ≥ 1 partida G1 de GASTOSPERSONA con clave E001–E007 y (`inscrip>0` o
  `colegia>0`) cuyo `numren` asiste a escuela con `tipoesc = 2`. Proporción ponderada Σw·PRIV / Σw en U.
- **ASIPRIV** (0/1, descriptivo, no decide): hogar en U con ≥ 1 integrante que asiste con `tipoesc = 2`
  (paga o no en el trimestre).
- **CARGA**: razón de totales Σw·G / Σw·ing_cor sobre hogares PRIV con `ing_cor>0`, G = Σ `gasto_tri` de las
  partidas que definen PRIV. Ambas cantidades trimestrales, pesos corrientes de 2022, escala proporción de
  ingreso. Agregador (E.1): razón de totales, no media de razones.
- **Deciles** de ingreso corriente sobre **todos** los hogares con diseño válido (no solo U): orden estable por
  `ing_cor`, participación acumulada de `factor`, decil = ceil(10·acumulada) acotado a 1..10 (idéntico a
  CALC-ENIGH-CONSUMO-PISOS-0002). Bloques: B1-IV = I–IV, B2-VIII = V–VIII, B3-X = IX–X.
- **Celdas**: PRIV y ASIPRIV por {TOTAL, URBANO, RURAL} × {TODOS, D01…D10, B1-IV, B2-VIII, B3-X}; CARGA por
  {TOTAL, URBANO} × las mismas; PRIV por TLOC (4), SEXO-JEFE (2), EDAD-JEFE (4) — segmentación mínima §3.
- **Diferencias** (misma réplica para minuendo y sustraendo): PRIV B2−B1 en URBANO, TOTAL, RURAL; ASIPRIV
  B2−B1 URBANO; CARGA B2−B3 en URBANO y TOTAL.
- **IC**: bootstrap de UPM con reemplazo dentro de estrato (n_h de n_h), estrato de una sola UPM = certeza
  (varianza cero, rotulado), **2000 réplicas, semilla 42**, PCG64, percentiles 2.5/97.5; contrato conservador:
  si alguna réplica es no finita, la celda sale sin IC (null declarado). Receta: `tools/dominios/salud/pisos_diseno.py`
  (`bootstrap`, `resumen`, `num`), ejecutada desde bytes hasheados, sin editar.
- **Filtros**: blanco/`NA`/no numérico → falta (nunca cero) en `asis_esc`, `tipoesc`, `ing_cor`; `inscrip`/`colegia`
  blanco = 0 (el cuestionario deja blanco cuando no pagó ese concepto). Sin no-sabe/no-responde codificado
  en estas variables según el descriptor.
- **Lectura**: por chunks de 200 000 filas con `usecols` (máquina compartida); GASTOSPERSONA se filtra por
  clave E001–E007 al leer.

## 5 · Pre-registro de falsación B-bis (fijado antes del dato)

Unidad de la regla: proporción de hogares (parte 1) y proporción del ingreso corriente (parte 2), ambos
en lo URBANO (la regla nombra «clase media urbana»; «clase media» se opera como deciles V–VIII, no como
estrato AMAI, que no es el objeto de la regla).

- **Parte 1** se sostiene si el **IC95 inferior** de `DIF-PRIV-URBANO-B2-MENOS-B1` es **> 0** (la
  proporción urbana de hogares que pagan colegiatura privada en V–VIII supera a la de I–IV y el IC de la
  diferencia despeja 0).
- **Parte 2** se sostiene si el **punto** de `DIF-CARGA-URBANO-B2-MENOS-B3` es **≥ 0** (carga en V–VIII no
  menor que en IX–X). Umbral ajustado respecto al encargo con justificación: la regla predice «duele más en
  medios»; se exige el signo en el punto y no un IC que despeje 0 porque la carga de IX–X se estima sobre
  pocos hogares por decil urbano y un IC ancho no debe convertir la ausencia de potencia en MATIZA. Su IC se
  reporta al lado.
- **CONFIRMA** = parte 1 y parte 2. **MATIZA** = parte 1 sin parte 2. **ROMPE** = parte 1 falla (IC incluye 0
  o signo contrario), sea cual sea la parte 2. **NO-CONSTRUIBLE** = la diferencia de la parte 1 sale sin IC
  (null), o la parte 1 se sostiene y la parte 2 sale null. **Manda la parte 1**: si la parte 1 falla, ROMPE
  aunque la parte 2 se sostenga.
- El dictamen lo emite el medidor como `RESULT-PDR1-ENIGH2022-DICTAMEN-RG-cc1c9ab8f1` y se copia
  mecánicamente al fragmento de P3.
- Descriptivo (no decide): TOTAL, RURAL, ASIPRIV, segmentos.

## 6 · Salida y límites

Todo RESULT es escalar por celda (ids `RESULT-PDR1-ENIGH2022-...`, derivados del medidor sobre corrida
sintética, `tests/test_pdr1_enigh2022.py`); ningún texto > 1024 bytes. Flotantes con `permite_no_estimable`.
Tolerancia de replay 1e-10 absoluta (semilla fija, sumas float64).

## 7 · Módulo de auditoría v2.16

- **Contadores movidos**: uno propuesto (regla SIN-CIFRA → dictamen), sin adoptar.
- **Unidad/escala**: HOGAR; proporciones de hogares y razón gasto/ingreso trimestral; ninguna se promedia
  con unidad persona. PRIV y CARGA no se comparan entre sí.
- **RETROSPECTIVA**: toda cifra; no hay PROSPECTIVA.
- **Segmentación**: decil × urbano/rural, tamaño de localidad, sexo y edad del jefe; México no es bloque.
- **¿Incentivo o psicología?**: pagar privada en deciles medios es compatible con adaptación racional
  (calidad percibida de la oferta pública, oferta local, jornada, costos de oportunidad) tanto como con
  «miedo a caer»; el dato no separa motivos. **Oferta antes que preferencia**: en lo rural la oferta privada
  es escasa; un PRIV rural bajo es oferta, no preferencia.
- **¿Clase media urbana?**: la regla es sobre ella; «clase media» = deciles V–VIII de ingreso, operación
  declarada y discutible (no es estrato AMAI ni autopercepción).
- **Peligroso leído simplista**: «la clase media se sacrifica por miedo» — la ENIGH no mide miedo; y una
  carga alta en V–VIII puede reflejar ingreso bajo del denominador, no sacrificio.
- **Afirmación escrita a mano sobre el corpus**: ninguna; premisas por comando (§0).

el primer resultado que produzca este procedimiento es el que se reporta.
