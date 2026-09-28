# MC2 · ENSANUT 2024 · búsqueda de atención, barreras de acceso y abandono de tratamiento · spec v1.0

ACTO GEN2-MEDICION-CARRILES-2, hija ENSANUT 2024, entorno CAJA, rama
`acto/gen2-medicion-carriles-2--ensanut2024`. CALC: `data/corrida0/CALC-MC2-ENSANUT2024-0001`
(medidor `medidor.py`; prueba sintética `tests/test_mc2_ensanut2024.py`). Encargo:
`forense/encargos/2026-09-28-GEN2-MEDICION-CARRILES-2.md`. Todo es **RETROSPECTIVA**. No adopta.

## 0 · Premisas, reserva y lectura previa

- `[EJECUTADO]` Payloads (manifiesto, raíz `descargas_mx`, leídos del espejo durable
  `/home/pc0/mm-corpus/descargas_mx_espejo/ENSANUT2024-v2026-09-01/`; el preflight compara sha256):
  `integrantes_ensanut2024_w_icb_stata_stata__v2026_09_01` (miembro `integrantes_ensanut2024_w_icb.dta`,
  36 021 filas) y `adultos_ensanut2024_w_stata_stata__v2026_09_01` (`adultos_ensanut2024_w.dta`, 12 924 filas).
- `[EJECUTADO]` Reserva E.6: ENSANUT 2025 es la ola RESERVADA del programa (24 payloads
  `RESERVADA-NO-ABIERTA-NO-INDEXAR-L`; `SALUD-ENSANUT-PISOS-spec-v1_0.md:13-15`) y no es input.
  ENSANUT 2024 es ola vista: `CALC-ENSANUT-0001` (adultos) y `CALC-ENSANUT-PISOS-SALUD-0001`
  (integrantes, adultos, utilizadores, adolescentes 2024) están sellados.
  `corpus_loader.motivo_reserva` → vacío para los dos ids. La republicación del 1/sep no es
  instrumento nuevo.
- Lectura de estructura antes del COMMIT-1 (permitida, declarada): cuestionarios de hogar
  (sección IV, 4.1–4.8), utilizadores y adultos (sección III, 3.1–3.14a) por `pdftotext`, y los
  **metadatos** de los dos `.dta` (`pyreadstat.read_dta(metadataonly=True)`: nombres, etiquetas de
  variable y de valor, número de filas). Ningún registro leído, contado ni tabulado. Los valores
  sellados de `CALC-ENSANUT-PISOS-SALUD-0001` **no** se leyeron antes de este COMMIT-1 (sólo los
  ids de sus RESULT).
- E.5: `CALC-ENSANUT-PISOS-SALUD-0001` ya trae, 2021–2024 por sexo/edad/estrato/escolaridad,
  NECESIDAD-SALUD-3M (h0401), BUSCO-ATENCION (h0404 | h0401 = 1), FUE-ATENDIDO, ATENCION-CURANDERO,
  IDEACION-SUICIDA-ADULTOS (a1211) e -ADOLESCENTES (d0817), DX-DIABETES. No mide los motivos de
  no búsqueda (H0405A–C), la búsqueda para necesidades de salud mental, las **diferencias**
  rural − metropolitano con IC de la misma réplica, ni nada del tratamiento de diabetes (a0307,
  a0310a, a0313, a0314). Aquí `BUSCO-*` se recalcula sólo como insumo de las diferencias
  (misma réplica); sus marginales 2024 por estrato deben coincidir en punto con las selladas y se
  reportan como control, no como cifra nueva.
- `tools/ya_medido.py RG-41d71be87f` → NUNCA-MEDIDA. Motivo nuevo frente al NO-CONSTRUIBLE de
  `reglas-contrastadas` v1.0/v1.1 («deferencia al experto por accesibilidad no medida»): la
  sección IV del hogar de ENSANUT 2024 sí mide, en la misma persona, necesidad, búsqueda y el
  motivo de no búsqueda con tres categorías de acceso (no hay dónde, muy lejos, caro/sin dinero)
  frente a «decidió que no era necesario». No estaba en el censo de v1.0.

## 1 · Variables por texto (A.15)

**Integrantes (todas las edades, persona):**
- `h0401` «En los últimos 3 meses ¿(USTED/NOMBRE) ha tenido alguna necesidad de salud?» 1 Sí 2 No.
- `h0402` «¿Podría decirme cuál fue la última necesidad de salud que tuvo…?» — SALUD MENTAL =
  {47 Depresión, 48 Ansiedad, 50 Estrés, 59 Otro de salud mental} (bloque «SALUD MENTAL» del
  catálogo impreso, cuestionario de hogar p. sección IV).
- `h0404` «¿(USTED/NOMBRE) buscó atención por esa necesidad de salud?» 1 Sí 2 No; sólo con h0401 = 1.
- `H0405A`, `H0405B`, `H0405C` «¿Por qué motivo (USTED/NOMBRE) no buscó atención?» (hasta tres
  opciones): 01 Decidió que no era necesario buscar atención porque no era tan grave · 02 No hay
  dónde atenderse · 03 Está muy lejos el lugar más cercano donde se brinda atención · 04 Es caro/No
  tenía dinero · 05–13 otros · 99 No sabe. **ACCESO** = alguna de {02, 03, 04}; **NO-GRAVE** = 01;
  denominador = h0401 = 1, h0404 = 2 y al menos un motivo 01–13 (sólo 99 o vacío: fuera, contado).
- `estrato` «Estrato urbanidad/ruralidad»: 1 Rural (<2 500), 2 Urbano (2 500–99 999),
  3 Metropolitano (100 000+); NORURAL = 2–3. `h0302` sexo; `h0303` edad (0-19, 20-59, 60+).

**Adultos (20+, persona seleccionada):**
- `a0301` «¿Algún médico le ha dicho que tiene diabetes (o alta el azúcar en la sangre)?» 1 SÍ
  (2 «durante el embarazo» y 3 NO fuera).
- `a0307` «¿Actualmente toma pastillas o le aplican insulina para controlar su azúcar?» 1–3 = con
  tratamiento; 4 Ninguno fuera.
- `a0310a` «Normalmente, ¿cuánto paga por sus pastillas y/o tratamiento de insulina para controlar
  su diabetes en un mes?» monto; 00 «No pagó». PAGA = monto > 0; NOPAGA = 0; monto ≥ 99 999 o
  vacío = no sabe, fuera (contado `DIAG-ADUL-MONTO-FUERA`).
- `a0313` «En los últimos seis meses ¿ha suspendido algún(os) de los medicamentos más de una vez a
  la semana?» 1 Sí 2 No (9 fuera).
- `a0314` «¿Cuál fue la causa principal de haber dejado de tomar sus medicamentos?» 01 Se le
  olvidó · 02 Consideró que no lo necesitaba · 09 Miedo a efectos secundarios · 04 Temor sobre la
  seguridad · 05 No le surtieron los medicamentos en la unidad médica · 06 No encontró el
  medicamento en la farmacia · 10 Se le terminó antes de surtir su siguiente receta · 07 No tuvo
  dinero para comprarlo(s) · 08 Otro. **ECON-ACCESO** = {05, 06, 07, 10}.

## 2 · Universo, unidad, ponderador, diseño, IC, agregador

- Unidades: persona integrante del hogar (todas las edades) para búsqueda/motivos; persona
  adulta 20+ con diabetes diagnosticada y en tratamiento para suspensión. Nunca se mezclan.
- Ponderador `ponde_f`; estrato de selección `est_sel`; UPM `upm` (llaves opacas). Fila sin
  ponderador positivo o sin diseño sale de todo.
- Agregador (E.1): razón ponderada Σw·y/Σw por celda; diferencias en la misma réplica.
- IC95: bootstrap de UPM con reemplazo dentro de `est_sel`, **2 000 réplicas**, `PCG64(42)`,
  bloques de 50; percentiles 2.5/97.5. Celda vacía → null; N se conserva.
- Segmentos: estrato (RURAL, URBANO, METRO, NORURAL), sexo y edad para ACCESO/NO-GRAVE; estrato
  para BUSCO; PAGA/NOPAGA, estrato y sexo para suspensión. Sin cruces dobles.

## 3 · Pre-registro de falsación B-bis (fijado antes del dato)

- **RG-41d71be87f** («SI el experto es accesible, cercano y asequible ENTONCES defiere; SI es caro,
  lejano o ya falló antes ENTONCES prevalece "yo sé por experiencia" y el consejo del allegado»).
  Parte observable: deferencia = buscar atención ante una necesidad; accesibilidad aproximada por
  el estrato (rural = lejano) y por el motivo declarado. Dos componentes:
  (i) `BUSCO-DIF-RURAL-METRO`: CONFIRMA si IC95-SUP < 0; ROMPE si punto ≥ 0; MATIZA en otro caso.
  (ii) `ACCESO-DIF-RURAL-METRO`: CONFIRMA si IC95-INF > 0; ROMPE si punto ≤ 0; MATIZA en otro caso.
  Dictamen = el peor. «Ya falló antes», el consejo del allegado y «adaptación racional, no
  anti-ciencia» **no son observables**; el estrato también mueve gravedad y oferta, así que el
  dictamen no identifica el mecanismo. Se reporta `ACCESO-MENOS-NOGRAVE-NAC` como contexto
  («no era tan grave» frente a acceso), no decide.
- **SALUD-032** («SI desabasto en unidad pública + gasto de bolsillo alto ENTONCES abandono o
  intermitencia — PORQUE barrera económica/acceso»). (i) `DM-SUSPENDE-DIF-PAGA-NOPAGA`: CONFIRMA
  si IC95-INF > 0; ROMPE si punto ≤ 0; MATIZA en otro caso. (ii) `DM-ECON-ACCESO-NAC` (causa
  principal de la suspensión es desabasto o dinero): CONFIRMA si IC95-INF ≥ 0.5; ROMPE si punto
  < 0.25; MATIZA en otro caso. Dictamen = el peor. «Gasto alto» se lee como pagar algo (> 0); el
  monto no se discretiza más (declarado).
- **SALMEN-032** («la búsqueda de un especialista de la salud mental es muy improbable entre los
  pobladores rurales por acceso geográfico, costo y distancia cultural»). ENSANUT mide búsqueda de
  cualquier atención, no de especialista: proxy, **tope MATIZA**. `BUSCO-MENTAL-DIF-RURAL-NORURAL`:
  ROMPE si punto ≥ 0; MATIZA en otro caso.
- **JUV-009** («7.6 % de adolescentes y 7.7 % de adultos pensó alguna vez en suicidarse», ENSANUT
  2022). Mismo reactivo (d0817 adolescentes, a1211 adultos) ya sellado para 2024 en
  `CALC-ENSANUT-PISOS-SALUD-0001` (E.5; valores no vistos al fijar esta regla):
  `…IDEACION-SUICIDA-ADOLESCENTES-2024-TOTAL-TODOS` vs 0.076 y `…-ADULTOS-2024-TOTAL-TODOS` vs 0.077
  con la regla de nivel de la hija ENIF (∈ IC → CONFIRMA; |Δ| ≤ 0.10 → MATIZA; si no ROMPE), **tope
  MATIZA** por ser otra ola. El intento de suicidio no se toca: `PARCIAL`.
- **RURAL-021** («coexisten sistemas médicos propios … con lógica interna coherente»):
  **NO-CONSTRUIBLE por texto** — la «lógica interna» no es observable; la presencia de curandero
  como lugar de atención ya está sellada (ATENCION-CURANDERO, E.5) y se cita.
- Fuera de esta pieza: SALUD-024 (tres recomendaciones de movimiento; módulo de actividad física,
  otra spec), SALUD-028/-029 (módulo de etiquetado × NSE; payload fuera del espejo), SALUD-031
  (atención grave → sistema público: `S6-L16`, linajes sin reconciliar, no se repite),
  APUEST-025 (hallazgo de instrumento, no afirmación de cifra).

Contraste de regla que se escribe en `canon/reglas-contrastadas-v1_2.tsv`: sólo RG-41d71be87f,
con el `resultado_id` que manda de (i).

## 4 · Módulo de auditoría v2.16

- Unidad: persona (integrante; adulto 20+ con diabetes). No hay hogar.
- RETROSPECTIVA; nada es predicción.
- Segmentación por estrato de urbanidad, sexo, edad y condición de pago; México no es bloque.
- ¿Incentivo o psicología? La regla se contrasta en su parte de **oferta y costo** (lejos, caro,
  no hay dónde); el «yo sé por experiencia» no se infiere de no buscar atención. La suspensión se
  lee primero como desabasto/dinero, no como adherencia psicológica.
- Oferta antes que preferencia: el motivo «no era tan grave» se reporta junto a los de acceso,
  nunca solo.
- Firewall genético: ninguna variable de ascendencia; nada de ascendencia → conducta.

El primer resultado que produzca este procedimiento es el que se reporta.
