# Operacionalización pre-registrada · `R5.2` · ENUT 2024 · Encargo Y, commit 1

*(Escrita antes de correr ninguna estadística de resultado sobre `enut2024_bd_csv.zip`. Los ZIP de microdato y de documentación (`enut2024_fd.xlsx`, `enut2024_diccionario_variables.html`, `enut2024_der.zip`) sí se abrieron para inspección estructural — nombres de variable, categorías, universo — sin calcular ningún cruce ni estadística de resultado. Se declara aquí, no se disimula, mismo criterio que `enif2024_csv.zip` en W.)*

**Umbral de la ficha (línea 158):** "Reducción **<20%** en horas de cuidado de la mujer 40+ cuando pasa de no ocupada a ocupada formal de tiempo completo, con varón adulto disponible en el hogar."

**ENUT 2024 es transversal** (sin variable de ronda/ola/panel en ninguna de las 5 tablas; llaves `LLAVEVIV/LLAVEHOG/LLAVESDE/LLAVEMOD` identifican una sola medición; sin llave de enlace entre ediciones). No hay transición individual observable. Se opera por **comparación transversal entre grupos** — mismo diseño que la ficha prevé en su propia fila `C` ("ENUT cruzada con ocupación y composición del hogar") y el mismo criterio que ya usó este programa para R5.1 (Pensión del Bienestar, beneficiarios vs. no beneficiarios comparables, transversal).

## Unidad de análisis y universo

Mujeres de 40+ años (`tsdem.csv`: `SEXO=2`, `EDAD≥40`) que caen dentro del universo de `tmodulo.csv`/`tvar_crea.csv` (personas de 12-96 años, 74,053 de 76,988 personas de 12+ años del roster completo — **cobertura 96.2%** del grupo relevante; el 3.8% de exclusión no es un módulo de opinión restringido como `familismo_obligacion` — que no existe en ENUT 2024, verificado por búsqueda exhaustiva en `enut2024_fd.xlsx`/diccionario/`enut2024_der.zip`, cero coincidencias — sino la definición estándar de universo de `TMODULO` (12-96 años); se declara, no se trata como hallazgo).

## Construcción de los dos grupos comparados

- **Grupo tratamiento (ocupada formal tiempo completo):** `COND_AEE=1` (ocupada) **∧** `TRAB_MERC_PV≥35` horas/semana (convención estándar INEGI/ENOE de tiempo completo) **∧** `P5_6_7=1` ("¿tiene derecho a servicio médico por su trabajo?" = Sí).
  ⚠️ **Declaración de proxy (regla del descriptor, no del nombre de variable):** ENUT no tiene pregunta de afiliación activa IMSS/ISSSTE como ENOE. `P5_6_7` mide **derecho a prestación**, no afiliación activa verificada — es el proxy de formalidad más cercano disponible y se usa como tal, declarado, no como equivalente literal.
- **Grupo comparación (no ocupada):** `COND_AEE≠1` (2 Desocupada, 3 Jubilada/pensionada, 4 Estudiante, 5 Quehaceres del hogar, 6 Otra) — lectura literal de "no ocupada" en el Umbral, sin restringir a una sola subcategoría.
- **Filtro común a ambos grupos — "varón adulto disponible":** al menos un integrante `SEXO=1` (hombre) **∧** `EDAD≥18` en el mismo hogar (`LLAVEHOG`), distinto de la mujer sujeto. Lectura literal y mínima de la ficha (presencia, sin condición adicional de relación de parentesco ni de ocupación del varón — la ficha no la pide).

## Desenlace — horas de cuidado

`tvar_crea.csv`, variables ya agregadas (horas/semana), sumando las categorías que caen dentro del alcance textual de la regla ("cuidado de mayores, niños, enfermos"):

`horas_cuidado = CUID_ESP_INT_HOG_CON_CP + CUID_INT_0A5_CON_CP + CUID_INT_6A14_CON_CP + CUID_INT_60MAS_CON_CP`

- `CON_CP` ("con cuidado pasivo") se usa en vez de `SIN_CP`: la variante con cuidado pasivo incluye vigilancia/estar al pendiente (`P6_11_14`), que la literatura de uso del tiempo trata como carga real de cuidado, no como tiempo libre.
- **Se excluye `CUID_INT_15A59`** (cuidado a personas de 15-59 años sin marca de enfermedad crónica/discapacidad): no cae dentro de "mayores, niños, enfermos" tal como la ficha los nombra — es una categoría residual de adultos en edad laboral, distinta de las tres que la regla declara. Decisión tomada por alcance textual, antes de ver ninguna cifra.
- No se suma nada de `thogar.csv` (personal doméstico/de cuidado **contratado** — sustituto pagado, concepto distinto del cuidado no remunerado propio que mide la regla).

## Diseño muestral

Ponderador `FAC_PER` (individuo, `tmodulo`/`tvar_crea`); estrato `EST_DIS`; UPM `UPM_DIS`. Estimación de la brecha con error estándar del diseño complejo (no i.i.d.).

## Métrica y umbral

`reducción% = (media_ponderada(horas_cuidado | no ocupada) − media_ponderada(horas_cuidado | ocupada formal TC)) / media_ponderada(horas_cuidado | no ocupada)`, ambos grupos restringidos a hogares con varón adulto disponible.

- **`reducción% ≥ 20%`** → satisface literalmente la fila `A` de la ficha ("la estructura basta y el guion sale del `PORQUE`").
- **`reducción% < 20%`, con el control de varón disponible YA incluido en el diseño** (no ausente) → la ficha no tiene una fila que nombre este caso exactamente: la fila `A` exige ≥20%; la fila `B` ("reducción parcial **sin control de disponibilidad del varón**") describe una versión inferior del diseño que este commit no usa, porque el control SÍ está construido. Se declara aquí, **antes de ver el resultado**, como ambigüedad conocida de la escala propia — no se resuelve por adivinanza en el commit 2; se resuelve citando la "Nota de asimetría" de la propia ficha (línea 160), que declara explícitamente que la confirmación del guion **es un resultado válido** y "el primer dato mexicano" a su favor, y no un fracaso del falsador.

## Controles

Ninguno adicional a los ya construidos en el diseño (varón disponible es el único control que la ficha pide, vía su fila `B`). No se agregan controles socioeconómicos: aunque el "Módulo de auditoría de rigor extremo" (línea 342) señala el riesgo de confundir estructura con cultura en R5.2 vía corresidencia/ingreso, la ficha **no** declara ese control como parte del Umbral (a diferencia de R4.3-mitad-B, que sí lo exige explícitamente) — no se inventa un control que el Umbral no pide.

## Compromiso de pre-registro

**El primer resultado que produzca este procedimiento es el que se reporta.** No se recalculará la definición de grupo, el desenlace, ni el umbral de tiempo completo después de ver la brecha estimada.
