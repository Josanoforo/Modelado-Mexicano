# PDR1-LATINOBAROMETRO · spec v1.0 · ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1 · pieza P-LATINOBAROMETRO

Entorno CAJA. RETROSPECTIVA: las dos olas (2023 y 2024) son olas ya vistas por el proyecto; nada aquí
es predicción. Contrato ejecutable: `data/corrida0/CALC-PDR1-LATINOBAROMETRO-0001/{spec.yaml,medidor.py}`.
No adopta; adopción por merge de mesa.

## 0 · Universo de la pieza y decisión de agrupación

Filas `pieza = P-LATINOBAROMETRO` de `forense/analisis/pisos-dominios-1/tabla-apertura-v1_0.tsv`:

| id | dominio | componente contrastable (mapa v1.1) | ola |
|---|---|---|---|
| ASTRA5-U0-HUM-006 | HUMOR | «En México, Latinobarómetro 2024 publicó 50% muy o más bien satisfecho con el funcionamiento de la democracia, frente a 37% en la edición 2023.» | 2024 (y 2023 como comparación) |
| ASTRA5-U0-AUTOR-026 | AUTORIDAD | «Convergencia declarada de Latinobarómetro OLA 2023 como fuente de baja confianza institucional/alta confianza interpersonal en México.» | 2023 |

Reserva por id (`corpus_loader.motivo_reserva`, 28/sep/2026): `latinobarometro2024_bd_stata` → LIBRE;
`latinobarometro2023_bd_stata_zip` → LIBRE. Nota: los CALC de 2023 sellados antes (25–26/sep) trataban
2024 como RESERVADA (E.6); el manifiesto vigente la da LIBRE por id y ésa es la comprobación que manda
el procedimiento de la pieza.

**Lo ya sellado se cita (E.5), no se re-mide.** `python3 tools/ya_medido.py` devuelve NUNCA-MEDIDA para
ambos ids (el índice busca rótulos, no reactivos), pero por reactivo, universo y unidad ya existen:

- `CALC-LATINOBAROMETRO-COLA-2023-0001` · `RESULT-LATINOBAROMETRO-COLA-2023-SATISFECHO-CON-LA-DEMOCRACIA-2023-TOTAL-TODOS-{P,IC-LO,IC-HI,N}`:
  P11STGBS.A 2023, México, 18+, `wt`, códigos 1+2 sobre 1–4. Es exactamente el componente 2023 de HUM-006.
- `CALC-LATINOBAROMETRO-PISOS-2023-0001` · `RESULT-LATINOBAROMETRO-PISOS-2023-CONFIA-{FFAA,POLICIA,IGLESIA,CONGRESO,GOBIERNO,PODER-JUDICIAL,PARTIDOS,INSTITUCION-ELECTORAL,PRESIDENTE}-2023-TOTAL-TODOS-P`
  (P13STGBS A–I, mucha+algo sobre 1–4) y `...-CONFIANZA-INTERPERSONAL-2023-TOTAL-TODOS-P` (P9STGBS):
  es la totalidad de AUTOR-026.

Decisión (latitud §6 del encargo, reversible): **un CALC con un solo input de dato**, la ola 2024, que
mide lo único nuevo: P12STGBS.A 2024 México. La ola 2023 no es input (se cita). AUTOR-026 no genera
medición nueva: su dictamen se decide sobre los RESULT sellados citados arriba, con la regla B-bis del §5.
**Declaración de contaminación (AUTOR-026 y componente 2023 de HUM-006):** al redactar esta spec el
ejecutor ya había impreso los puntos TOTAL de esos RESULT sellados (paso E.5). Esas dos reglas B-bis NO
son ciegas; se fijan aquí por escrito con la lectura más literal del texto, y el dictamen resultante debe
leerse como cita de lo sellado, no como prueba pre-registrada. El componente 2024 sí es ciego: el
microdato 2024 no se ha abierto más que para estructura.

Lectura de estructura antes del COMMIT-1 (permitida, no es dato): lista de miembros del ZIP 2024,
metadatos del `.dta` (`pyreadstat.read_dta(..., metadataonly=True)`: nombres, etiquetas de variable y de
valor) y texto del cuestionario `Latinobarometro_2024_Cuestionario_esp.pdf` (dentro del payload) con
`pdftotext -layout`. Ninguna fila leída, contada ni tabulada.

## 1 · Fuente, universo, unidad, ponderador, diseño

- Payload: `latinobarometro2024_bd_stata` (sha256 `469a94c5…5e97`), miembro
  `Latinobarometro_2024_Stata_esp_v20250817.dta`.
- Filas de México: `IDENPA = 484` (etiqueta de valor del archivo: «[%484%] Mexico»); el lector descarta
  los otros 16 países antes de devolver filas.
- Universo: persona de 18 años o más (`EDAD` ≥ 18) entrevistada en México. Unidad: persona.
- Ponderador: `WT` («Ponderación» en el archivo). Válido: `WT` finito > 0.
- Diseño: el archivo **no** trae estrato ni UPM (ni en 2023 ni en 2024). Se usa bootstrap ponderado de
  entrevistas (cada entrevista su propia unidad, estrato único; etiqueta «MAS-PONDERADO-SIN-ESTRATO»),
  2000 réplicas, semilla 42 (numpy PCG64), IC95 por percentiles 2.5/97.5, contrato conservador de la
  receta sellada. **Limitación:** Latinobarómetro es muestra probabilística por conglomerados con cuotas
  en la última etapa; ignorar la conglomeración subestima la varianza: el IC95 publicado es un piso de
  la incertidumbre, no el IC de diseño.
- Estimación: razón ponderada Σw·y / Σw sobre los válidos del reactivo (receta
  `tools/dominios/salud/pisos_diseno.py`, motor `tools/dominios/confianza/motor_pisos.py`, ambos
  cargados por sha256 desde sus bytes; los mismos que usaron los CALC 2023 sellados).
- Agregador (E.1): proporción ponderada de personas; no hay agregación entre reactivos en el CALC.

## 2 · Reactivo y códigos (por texto de pregunta, A.15)

Cuestionario `Latinobarometro_2024_Cuestionario_esp.pdf`, p. 1 (columna derecha), verbatim:
«P12STGBS.A En general, ¿Diría Ud. que está muy satisfecho, más bien satisfecho, no muy satisfecho o
nada satisfecho con el funcionamiento de la democracia en (PAÍS)? (MARQUE UNA EN P12STGBS.A)».
Respuestas: 1 Muy satisfecho · 2 Más bien satisfecho · 3 No muy satisfecho · 4 Nada satisfecho ·
No sabe / No responde (en el `.dta` como faltantes extendidos de Stata `.a`/`.b`).

Conducta `SATISFECHO-CON-LA-DEMOCRACIA`: y = 1 si código ∈ {1, 2}; y = 0 si ∈ {3, 4}; todo otro valor
(NS, NR, faltante) fuera del denominador. Es el mismo recorte que el sellado de 2023 (P11STGBS.A, mismo
texto). **Advertencia de denominador:** el informe de Latinobarómetro suele porcentuar sobre el total
de entrevistas incluyendo NS/NR; aquí NS/NR quedan fuera (procedimiento del acto). El punto medido
queda, si acaso, por encima del publicado en la proporción de NS/NR; lo mismo vale para el sellado 2023.

## 3 · Segmentación mínima (§3: México no es bloque)

TOTAL-TODOS; SEXO (`SEXO` 1 Hombre / 2 Mujer); EDAD (18–29, 30–44, 45–59, 60+ sobre `EDAD`);
ESCOLARIDAD (`REEDUC.1` recodificado: 1–3 HASTA-BASICA, 4–5 MEDIA, 6–7 SUPERIOR); TAMLOC (`TAMCIUD`:
1–3 MENOS-20MIL, 4–6 20MIL-100MIL, 7–8 100MIL-MAS, 8 = capital); CLASE-SUBJETIVA (`S2`: 1–2
ALTA-MEDIA-ALTA, 3 MEDIA, 4 MEDIA-BAJA, 5 BAJA). Un eje a la vez, nunca cruces. Por celda: P, EE, IC-LO,
IC-HI, N sin ponderar. Diagnósticos: filas leídas (México), filas con diseño válido, filas 18+.

## 4 · Resultados que produce el CALC

Ids `RESULT-PDR1-LATINOBAROMETRO-SATISFECHO-CON-LA-DEMOCRACIA-2024-<EJE>-<CAT>-{P,EE,IC-LO,IC-HI,N}` más
`RESULT-PDR1-LATINOBAROMETRO-G-*` (diagnósticos, diseño, réplicas, semilla, sha de inputs de código,
declaración de ola). La lista exacta está en `resultados:` del spec.yaml y la deriva el medidor
(`esquema_resultados()`), verificada por `tests/test_pdr1_latinobarometro.py` sobre un payload sintético.

## 5 · Pre-registro de falsación B-bis

Unidad de todas las reglas: proporción de personas 18+ en México (0–1).

**HUM-006 · componente 2024 (ciego; manda).** Sea P24 = `...-2024-TOTAL-TODOS-P` con IC95 [L24, H24] y
P23 = 0.3773592805059565 (punto sellado de COLA-2023, citado).
- CONFIRMA-24: 0.50 ∈ [L24, H24].
- MATIZA-24: 0.50 ∉ [L24, H24] y P24 > P23 (sube respecto de 2023, cifra distinta).
- ROMPE-24: P24 ≤ P23 (no sube: orden contrario al de la afirmación).
Precedencia: ROMPE-24 se evalúa primero; luego CONFIRMA-24; lo restante es MATIZA-24.

**HUM-006 · componente 2023 (citado; no ciego).** CONFIRMA-23 si 0.37 ∈ [IC-LO, IC-HI] del sellado
COLA-2023; si no, MATIZA-23 (mismo reactivo, cifra fuera).

**HUM-006 · dictamen de la afirmación:** ROMPE si ROMPE-24; CONFIRMA si CONFIRMA-24 y CONFIRMA-23; en
otro caso MATIZA. La parte «máximo de esa serie publicada» no es medible con dos olas y queda fuera del
dictamen (se dice en el detalle).

**AUTOR-026 (citado; no ciego, ver §0).** Sea I = media simple de los 9 puntos TOTAL de confianza
institucional sellados (FFAA, POLICIA, IGLESIA, CONGRESO, GOBIERNO, PODER-JUDICIAL, PARTIDOS,
INSTITUCION-ELECTORAL, PRESIDENTE; mucha+algo) y T = punto TOTAL sellado de CONFIANZA-INTERPERSONAL.
- ROMPE: T ≤ I (la confianza interpersonal no supera a la institucional: orden contrario) o I ≥ 0.50
  (la institucional no es baja).
- CONFIRMA: I < 0.50, T > I y T ≥ 0.50 (institucional minoritaria, interpersonal mayoritaria).
- MATIZA: I < 0.50, T > I y T < 0.50 (el orden se sostiene pero la interpersonal no es «alta»).
Precedencia: ROMPE primero. Advertencia de escala: I viene de un reactivo de 4 puntos colapsado y T de
un reactivo dicotómico; el contraste es de orden, no de magnitud equivalente. No se calcula IC de I ni
de T − I (no hay réplicas conjuntas selladas): el dictamen usa sólo puntos, y se dice.

## 6 · Módulo de auditoría v2.16

- Unidad: persona 18+ entrevistada en México; no hogar, no municipio. Escala: proporción 0–1.
- RETROSPECTIVA: ambas olas vistas; nada se proyecta.
- Segmentación: sexo, edad, escolaridad, tamaño de localidad, clase subjetiva (§3); n≈1200 por ola, las
  celdas pequeñas tendrán IC anchos.
- ¿Incentivo o psicología?: ni uno ni otro directamente; es una evaluación declarada del desempeño del
  régimen, sensible al ciclo político (2024 es año de elección presidencial y cambio de gobierno) — no es
  un rasgo psicológico estable ni se relaciona con el humor como tal (la fila vive en el dominio HUMOR
  por el informe, no por el reactivo).
- ¿Clase media urbana?: muestra nacional cara a cara con cuotas; la segmentación por TAMLOC y clase
  subjetiva lo expone.
- ¿Qué sería peligroso leído simplista?: leer el salto 2023→2024 como cambio de cultura política o
  efecto causal de algo (son dos muestras independientes, sin IC de diseño); leer la satisfacción con el
  funcionamiento como apoyo normativo a la democracia (P11STGBS es otro reactivo); leer «baja confianza
  institucional / alta interpersonal» como rasgo nacional sin ver que la interpersonal medida es baja.

el primer resultado que produzca este procedimiento es el que se reporta.
