# Respaldo de literatura — colapso de categorías, cobertura de canal, IC de familia (D1–D4)

`ACTO GEN2-MOTOR-SEMANTICA`, 9/sep/2026. Archiva el respaldo que
NC-0108/0110/0112/0113 pedían y que no estaba en el repo (búsqueda previa:
`NO-ENCONTRADO`). Síntesis corta, evidencia externa marcada tipo (3)
(A.4/A.5) — rotulada, no mueve ningún contador ni cita `corrida0_*`.

## D1 · Los seis complementos (NC-0108) — por qué NO se adoptan como medidos

Colapsar dos o más categorías de un reactivo politómico en un binario
`p`/`1-p` solo preserva la estructura si las categorías colapsadas son
**homogéneas** respecto al desenlace — condición de independencia marginal
o conjunta (criterio de Goodman/Gilula; Kateri & Iliopoulos muestran que
colapsar entre categorías homogéneas no altera la estructura de asociación,
pero colapsar entre heterogéneas sí la distorsiona). En la práctica esa
homogeneidad es **rara**, no el caso por defecto: agregar sin verificarla
arriesga una inversión tipo Simpson — el signo o la magnitud de la
asociación en el agregado puede no corresponder a ninguna de las categorías
que lo componen. Los seis complementos de este acto (`tramite_normal_*`)
son `1 - p` del primario sobre denominadores con residuo heterogéneo
declarado en la spec sellada (P7_3 con categorías fuera del par
presencial/digital, o el resto de un desenlace binario con "no sabe" fuera
de universo): el complemento aritmético es correcto como aritmética, pero
no es una medición independiente — hereda el residuo sin declarar si ese
residuo es homogéneo con lo que sí se midió. Por eso el emisor los deriva
(`clase: MEDIDO`, sin `corrida0_resultado_id` propio) y no se adoptan como
si tuvieran corrida propia.

## D2 · Cobertura de canal (NC-0110) — por qué el mapeo no se amplía sin medir

Dicotomizar una variable categórica (aquí, ocho categorías de P7_3 a un par
presencial/digital) pierde potencia estadística frente a usar la variable
completa, pero **no pierde control del error tipo I** siempre que el
residuo excluido quede acotado y declarado — es la razón por la que
dicotomizar es una práctica aceptada y no un error, mientras la pérdida de
información se declare y no se entierre. El código 08 (precedente interno)
midió ese costo antes de decidir: +3.3–3.9 pp de diferencia según se incluya
o no la categoría intermedia. Ampliar hoy el mapeo canal↔disparador de
`tramite.mordida.con_registro` para cubrir el 21.98% de residuo (P7_3 = 2, 6)
exigiría el mismo tipo de argumento de homogeneidad de D1 — que esas dos
categorías se comporten como el par ya mapeado — y ese argumento no está
medido. Mesa decide no asumirlo: la cobertura del 78.02% queda declarada,
no ampliada.

## D3 · Estándar de IC (NC-0112) — por qué celdas escasas colapsadas dan tests conservadores

Cuando un estrato de diseño tiene una sola UPM, la varianza de diseño para
ese estrato es cero por construcción del método (bootstrap que se remuestrea
a sí mismo); tratar esos estratos sin colapsarlos ni descartarlos —como
hace §3.7 de la spec ENCIG— produce un IC que se lee como **límite
inferior** de la anchura verdadera, nunca como IC exacto: es el patrón
general de que colapsar (o, en este caso, no colapsar y aceptar la
varianza-cero local) celdas escasas produce inferencia conservadora, no
liberal — el error no se subestima. Es el mismo principio que sostiene
tratar la varianza-cero de un estrato de UPM única como "conservador
declarado" en vez de "sesgado": el método no inventa precisión que no
tiene. Sobre esa base, mesa ratifica el método de §3.7 como estándar de
familia para ranuras sin método propio (enmienda fechada en
`forense/prereg-caja/ENCIG-MORDIDA-spec-v1_0.md` §8).

## D4 · Semántica de la mordida (NC-0113) — por qué el nombre se conserva con reserva anotada

No es un asunto de colapso de categorías sino de validez de constructo: el
reactivo 8.3 de ENCIG (y su análogo ENCUCI) preguntan si a la persona **le
solicitaron** un pago informal, no si lo pagó. El pago consumado lo mide un
reactivo distinto (P8_6/P8_5, con `X-P-DIO-ALGO = 0.662933` de quienes
llegan a esa pregunta). Renombrar la conducta introduciría un cambio de
identificador en un YAML con historial de olas y enmiendas encadenadas por
`aplica_a`; anotar la semántica en la cita, sin tocar el nombre, es el
tratamiento mínimo que no rompe ese historial y que deja el hecho donde el
lector del motor lo ve. El reactivo 8.3 completo (los tres incisos,
`A-P-SOLANY = 0.115702`) queda **descriptivo sin consumidor** — disponible,
no adoptado— hasta que un caso de uso concreto lo reclame.

## Referencias (evidencia externa, tipo 3 — A.4/A.5, no mueve contadores)

- Goodman, L. A. (1981). *Association models and canonical correlation in
  the analysis of cross-classifications.* JASA — criterio de homogeneidad
  para colapso sin distorsión estructural.
- Gilula, Z. (1986). *Grouping and association in contingency tables: an
  exploratory canonical correlation approach.* JASA.
- Kateri, M. & Iliopoulos, G. (2003). *On collapsing categories in
  two-way contingency tables.* Statistics — condiciones exactas bajo las
  que colapsar preserva vs. distorsiona la asociación; base directa de D1.
- Simpson, E. H. (1951). *The interpretation of interaction in contingency
  tables.* JRSS-B — riesgo de inversión al agregar sin restricción.
- Cohen, J. (1983). *The cost of dichotomization.* Applied Psychological
  Measurement — pérdida de potencia al dicotomizar sin pérdida de control
  del error cuando el residuo queda acotado; base de D2.
- Agresti, A. (2013). *Categorical Data Analysis* (3rd ed.), cap. 3 —
  conservadurismo de tests sobre tablas con celdas escasas colapsadas; base
  de D3.

## Precedentes internos citados

- **Código 08** (medido, +3.3–3.9 pp según inclusión/exclusión de categoría
  intermedia, antes de decidir) — precedente directo de D2.
- **Corrimiento BPCOD-2012** con residuo nulo declarado — precedente de que
  un residuo se declara aunque sea cero, no se omite la declaración.
- **Dicotomizaciones congeladas D-15** — precedente de dicotomizar con
  residuo acotado y declarado, sin re-abrir la decisión acto por acto.

## 8.3 completo — disponible sin consumidor

`A-P-SOLANY = 0.115702` (los tres incisos del reactivo 8.3, `RESULT-ENCIG-MOR-A-P-SOLANY`)
queda anotado aquí como **disponible-sin-consumidor**: la decisión de mesa
del 9/sep/2026 ya lo resolvió (D4) — no nace fila nueva en `milpa/tramite.yaml`
ni en `forense/no-corrido.tsv` por esto; el día que un caso de uso lo
reclame, ese acto cita esta nota y la anotación `SEMANTICA` ya escrita en
la conducta primaria.
