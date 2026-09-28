# PDR1-ENVIPE2025 · spec v1.0 · regla RG-b91375cbd5 (CAPITAL_SOCIAL)

Acto GEN2-PISOS-DOMINIOS-Y-REGLAS-1 · pieza P-ENVIPE2025 · entorno CAJA · **RETROSPECTIVA**
(ENVIPE 2025 es ola ya vista: CALC sellados previos la abrieron, p. ej.
CALC-ENVIPE2025-PISOS-EVADE-NORMA-SXD-0001 y CALC-REGION-ENVIPE-SEGURO-2025-0001).
CALC: `data/corrida0/CALC-PDR1-ENVIPE2025-0001`. No adopta; adopción por merge de mesa.

## 0 · Reserva y E.5

- `motivo_reserva('envipe2025_csv')` = LIBRE. E.6: existe ola posterior en el manifiesto
  (`envipe2026_*`, RESERVADA — no se toca, ni tabulados ni comunicados) y hay CALC sellados que ya
  abrieron `envipe2025_csv` (sha256 8a7a99fd…16fa). ENVIPE 2025 ABIERTA (MEMORIA-OPERATIVA §1).
- E.5: `tools/ya_medido.py RG-b91375cbd5` → NUNCA-MEDIDA; `rg AP4_11_06|AP4_9_5` sobre
  `data/corrida0/*/{spec.yaml,medidor.py}` sin coincidencias. Nada que citar; se mide.
- Lectura de estructura antes del COMMIT-1 (permitida): cabeceras de columnas de los miembros CSV
  del zip, cuestionario principal 2025, cuestionario del módulo y descriptor (FD) 2025. No se contó
  ni tabuló ninguna fila del microdato.

## 1 · Regla (texto, canon/reglas-contrastadas-v1_0.tsv:117)

«SI clase media/alta con amenaza de inseguridad ENTONCES se suma (coordinación defensiva, a veces
punitiva); SI barrio popular en crisis (sismo, pandemia) ENTONCES se suma (ayuda mutua).»

Se contrasta **sólo la primera mitad** (observable). La segunda mitad es NO-CONSTRUIBLE (§6).

## 2 · Fuente, archivo, reactivos (por texto, con página)

Payload `envipe2025_csv`, miembro
`tper_vic1_envipe2025/conjunto_de_datos/conjunto_de_datos_tper_vic1_envipe2025.csv`
(CSV con BOM, cabecera entrecomillada, fin de línea `\r` solo; se decodifica utf-8-sig y si
falla latin-1, `\r`→`\n`, y se leen sólo las 12 columnas listadas: proyección de columnas).
Páginas = página del PDF (visor), `cuest_principal_envipe2025.pdf` y `fd_envipe2025.pdf`.

| rol | texto de la pregunta | códigos | página |
|---|---|---|---|
| Y1 desenlace principal | 4.11 «Durante 2024, para protegerse de la delincuencia, ¿en este hogar se realizó algún tipo de medida como… 06. realizar acciones conjuntas con sus vecinos(as)?» | 1 Sí, 2 No, 9 NS/NR | cuest. p.5; FD p.26 (campo 105) |
| filtro Y2 | 4.8 «¿En su (COLONIA/LOCALIDAD) han tenido problemas de… 5. robos?» | 1 Sí, 2 No, 3 No aplica, 9 NS/NR | cuest. p.5; FD p.24 (campo 80) |
| Y2 desenlace secundario | 4.9 «¿Se han organizado la mayoría de los (las) vecinos(as) para resolverlos?» (renglón robos) | 1 Sí, 2 No, 9 NS/NR, blanco | cuest. p.5; FD p.24 (campo 81) |
| amenaza | 4.3 «¿En términos de delincuencia, considera que vivir en (COLONIA, LOCALIDAD) es… seguro? / inseguro?» | 1 seguro, 2 inseguro, 9 NS/NR | cuest. p.4; FD p.19 (campo 31) |
| clase | «Estrato» (ESTRATO) | 1 Bajo, 2 Medio bajo, 3 Medio alto, 4 Alto | FD p.43–44 (campo 238) |
| ponderador | «Factor de personas elegidas… preguntas de percepción de la seguridad pública… población de 18 años y más» (FAC_ELE) | entero >0 | FD p.43 (campo 234) |
| diseño | «Estrato de diseño muestral» EST_DIS; UPM_DIS | texto opaco | FD p.44 |
| segmentación | SEXO (1 Hombre, 2 Mujer); EDAD (años cumplidos 18–96); DOMINIO (U urbano, C complemento urbano, R rural) | | FD p.17 (SEXO, EDAD); p.43 (DOMINIO) |

Nombres de variable sólo como localizador; la identidad es el texto de arriba (A.15).
Límite de lectura declarado: ESTRATO es el estrato sociodemográfico **de la vivienda/área**
asignado por el marco, no la clase del individuo; es el mejor proxy de «clase media/alta» que
ENVIPE publica. Y1 es una medida **del hogar** reportada por la persona elegida (18+): la unidad
estimada es «personas 18+ que viven en un hogar que realizó acciones conjuntas con vecinos para
protegerse de la delincuencia», no «personas que se sumaron personalmente». Y2 es percepción de
la persona sobre si «la mayoría de los vecinos» se organizó, no participación propia.

## 3 · Universo, filtros, estimando

- Universo: filas de tper_vic1 (persona elegida 18+, cuestionario completo) con FAC_ELE > 0.
- Y1: denominador AP4_11_06 ∈ {1,2} (NS/NR fuera); numerador = 1.
- Y2: denominador AP4_8_5 = 1 (robos en la colonia) y AP4_9_5 ∈ {1,2}; numerador = 1.
- Amenaza: INSEGURA = 4.3 colonia «inseguro» (2); SEGURA = «seguro» (1); TOTAL = todos (incl. NS/NR).
- Estratos: E1, E2, E3, E4 y ALTO34 = {3,4}. Clase «media/alta» de la regla = ALTO34; «baja» = E1.
- Estimando por celda (Y × amenaza × estrato): proporción ponderada FAC_ELE (razón de sumas,
  sin normalizar) con IC95; n sin ponderar.
- Contraste D34M1 = p(ALTO34) − p(E1), en puntos porcentuales, con IC95 de la diferencia sobre
  las mismas réplicas. DID-INS-SEG = D34M1(INSEGURA) − D34M1(SEGURA), pp.
- Segmentación mínima (§3, México no es bloque): D34M1 de Y1 dentro de INSEGURA por sexo
  (H, M), edad (18–29, 30–44, 45–59, 60+; un valor fuera de 18–97 no entra en ningún grupo) y
  dominio (U, C, R), con n de cada lado.
- Agregador (E.1): razón de sumas ponderadas; un eje a la vez; sin modelos.

## 4 · IC

Bootstrap de UPM (pares EST_DIS/UPM_DIS) con reemplazo dentro de EST_DIS sobre el marco completo,
2000 réplicas, semilla 42 (numpy PCG64, multinomial por estrato, como la plantilla
CALC-ARBITRO-MARGINALES-2-ENCUCI2020-0001); estrato con una sola UPM se autorremuestrea (varianza
cero, se cuenta en N-SINGLETON). Percentiles 2.5/97.5; réplicas con denominador 0 se descartan.
Celda sin masa → null (NO-ESTIMABLE).

## 5 · B-bis (fijado antes del dato)

Decide **un solo** número: D = D34M1 de Y1 dentro de INSEGURA (pp), IC95 [lo, hi]. X = 3 pp.

| fila | condición | dictamen |
|---|---|---|
| B1 | D ≥ 3 y lo > 0 | CONFIRMA |
| B2 | D < 0 y hi < 0 | ROMPE |
| B3 | cualquier otro caso (incluye D>0 con IC que toca 0, o 0 ≤ D < 3) | MATIZA |
| B0 | D o su IC null | NO-ESTIMABLE (se reporta como INCOMPARABLE en P3) |

Las filas son mutuamente excluyentes. Justificación de X = 3 pp: la regla afirma una diferencia
de conducta por clase, no una diferencia estadísticamente detectable cualquiera; con tamaños de
celda de miles de personas el IC de la diferencia es del orden de ±1–2 pp, así que 3 pp exige
algo más que ruido y es a la vez un efecto pequeño en términos absolutos para una medida de
hogar. Y2, las celdas SEGURA/TOTAL, DID y los segmentos son PISO-DESCRIPTIVO: no cambian el
dictamen. Lectura adicional pre-registrada (no decisoria): si DID > 0 con IC que despeja 0, la
«amenaza» amplifica la brecha de clase como dice la regla; si no, la brecha (si existe) no
depende de la amenaza percibida.

## 6 · Parte NO-CONSTRUIBLE: «barrio popular en crisis (sismo, pandemia) → ayuda mutua»

No observable en ENVIPE 2025. Buscado por texto (`sismo|terremoto|pandemia|covid|desastre|
inundaci|huracán|ayuda mutua`) en cuestionario principal (secciones I–VII: identificación,
integrantes, IV percepción sobre seguridad pública, V desempeño institucional, VI victimización
en el hogar, VII victimización personal), cuestionario del módulo de victimización y FD completo.
Únicas apariciones: «Desastres naturales» como opción 06 de la tarjeta 1 del reactivo 4.2 (temas
que más le preocupan; cuest. p.4, FD p.19 AP4_2_06) y «desastres naturales» como ejemplo de
trámite ante autoridad en la sección V. Ninguna capta (a) que el barrio viviera una crisis (sismo,
pandemia) ni (b) conductas de ayuda mutua entre vecinos ante esa crisis. Control positivo: el
mismo barrido encuentra «vecinos» en el cuestionario principal (6 líneas) y en el FD (21), así
que la búsqueda funciona. Además ENVIPE sólo pregunta por acciones vecinales **frente a la
delincuencia o problemas de servicios** (4.8/4.9: alumbrado, agua, baches, pandillerismo, robos,
delincuencia en escuelas; 4.11_06), no frente a desastres. Tampoco hay forma de fechar un choque
(2024 no tiene sismo/pandemia comparable) ni una marca de «barrio popular en crisis». Dictamen
de esa mitad: NO-CONSTRUIBLE.

## 7 · Resultados (ids en spec.yaml, derivados del medidor sobre corrida sintética)

Prefijo `RESULT-PDR1-ENVIPE2025-RGB913`. Escalares por celda: `-{Y1|Y2}-{INSEGURA|SEGURA|TOTAL}-
{E1|E2|E3|E4|ALTO34}-{P|LO|HI|N}`; `-{Y}-{amenaza}-D34M1-{PP|LO|HI}`; `-{Y}-DID-INS-SEG-{PP|LO|HI}`;
`-Y1-INSEGURA-D34M1-{segmento}-{PP|LO|HI|NA|NB}`; metadatos N-FILAS, N-ESTRATOS, N-UPM,
N-SINGLETON, METODO-IC; y `-DICTAMEN` (B-bis aplicado mecánicamente en el medidor). Ningún valor
de texto supera 1024 bytes.

## 8 · Módulo de auditoría v2.16

- Unidad: persona 18+ (FAC_ELE) viviendo en hogar que realizó la acción (Y1); percepción de
  la persona sobre la mayoría de los vecinos (Y2). Escala: proporción 0–1; contrastes en pp.
- RETROSPECTIVA: sí (ola abierta y usada antes).
- Segmentación: sexo, edad, dominio urbano/complemento/rural; estrato es el eje de la regla.
- ¿Incentivo o psicología? La regla es estructural (inseguridad + recursos de clase); ENVIPE no
  separa incentivo (costo de organizarse) de disposición; el contraste es asociativo, no causal.
- ¿Clase media urbana? Riesgo directo: la regla habla de ella; ESTRATO es de área, y el estrato
  alto se concentra en lo urbano; por eso se segmenta por dominio.
- Peligroso leído simplista: «los ricos se organizan y los pobres no» — Y1 mezcla acciones
  conjuntas pacíficas con vigilancia vecinal; no mide punitivismo ni linchamiento («a veces
  punitiva» NO es observable aquí); y la ausencia de la mitad «crisis» no dice que los barrios
  populares no practiquen ayuda mutua.

el primer resultado que produzca este procedimiento es el que se reporta.
