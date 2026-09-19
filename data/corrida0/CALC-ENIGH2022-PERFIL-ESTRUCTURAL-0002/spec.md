# ENIGH2022-PERFIL-ESTRUCTURAL · especificación humana sucesora v1.1

Sucesora de v1.0 / `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0001`, preservados
intactos en commit `8f614f7`. El primer `corrida0 run` de 0001 falló antes de
abrir el ZIP y antes de producir resultados o sello: `inputs[id]` es un
descriptor y el medidor v1.0 lo pasó completo a `zipfile.ZipFile`. Esta v1.1
cambia únicamente el cableado a `inputs[id]["ruta_absoluta"]`, el `calc_id`,
la ruta del script y la declaración de sucesión. Universo, variables,
categorías, método, semilla, RESULT y decisiones de no-estimación quedan
idénticos a v1.0.

Fecha de congelamiento: 19/sep/2026. CALC propuesto:
`CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0001`. Esta versión se congela antes de
abrir cualquier miembro `conjunto_de_datos/*.csv` del payload en esta sesión.

## 1. Pregunta, alcance y no-estimación

Se describirá, a nivel persona, la distribución marginal de `segsoc`, cuatro
tramos de `edad`, `tam_loc`, `est_socio`, `conex_inte` y `celular`; y el
producto cartesiano observado `segsoc × tramo_edad × tam_loc × est_socio`.
No se construye π, no se calibra, no se ejecuta IPF/IPU, no se adjudican
cortes y no se modifica el motor.

`residencia` queda congelada como
`NO-ESTIMABLE-POR-DEFINICION-NO-ACREDITADA`. La guía oficial local
`enigh2022_descripcion_base_pdf` p. 75 define la variable como entidad o país
cinco años antes de la entrevista, pero reproduce la pregunta «Hace 5 años,
en octubre de 2005…» para ENIGH 2022; tampoco fija en esa entrada el universo
por edad ni sus saltos. El catálogo de 34 códigos no resuelve esa
contradicción. No se abrirá la columna de respuestas `residencia`.

## 2. Fuentes documentales acreditadas

- `enigh2022_descripcion_base_pdf`, SHA-256
  `7b0c4e6bd36ceb9eae7cc852fce5a38dbcf4f2da6b133d35df6b1443fc76836c`:
  pp. 3–6 (niveles, llaves y factor), pp. 45–46 (`tam_loc`, `est_socio`,
  `est_dis`, `upm`, `factor`), p. 54 (`celular`, `conex_inte`), pp. 65 y 75–76
  (`edad`, `segsoc`), pp. 186–188 (regla oficial de integrantes del hogar) y
  pp. 204–205 (catálogo de parentesco).
- `enigh2022_nota_tecnica_pdf`, SHA-256
  `4f79f457d69c1f066d7fd319b1650f7b631f4008cb74e1046e6c644c65be0647`:
  contexto de ENIGH 2022 y población/hogares.
- `enigh2022_nc_csv`, 90,030,937 bytes, SHA-256
  `3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06`.

`segsoc` significa contribución o cotización alguna vez a una institución de
seguridad social (1 Sí, 2 No), para personas de 12 o más años. No se rotula
como informalidad laboral. `celular` y `conex_inte` significan tenencia del
hogar, no uso personal, smartphone ni banca digital. `est_socio` es el
estrato socioeconómico nativo Bajo/Medio bajo/Medio alto/Alto; no es cuartil
de ingreso ni `est_dis`.

## 3. Universo, unidad, llaves y exclusiones

Marco documental: todas las filas de `poblacion`. Unidad estimada: persona.
Llave persona: `(folioviv, foliohog, numren)`, que debe ser única.

Pertenencia oficial al hogar: `parentesco` inicia con 1, 2, 3, 5 o 6, la
misma regla publicada para construir `concentradohogar.tot_integ` (guía
pp. 187–188). Se excluyen y reportan por separado prefijo 4 (trabajador
doméstico y familiares), prefijo 7 (huésped y familiares) y cualquier otro
código/no especificado. Después se exige edad base-10 entera no negativa y
se restringe a 18–96, reportando por separado edad inválida, menor de 18 y
mayor de 96. Una edad entera válida fuera del intervalo es exclusión por
edad, nunca no respuesta. Para estimar puntos se exige `factor` finito y
positivo; su falla se reporta aparte y no se fabrica masa.

Los atributos `tam_loc`/`est_socio` se unen desde `concentradohogar`, y
`celular`/`conex_inte` desde `hogares`, por `(folioviv, foliohog)`. Cada tabla
de hogar debe tener llave única (m:1 desde persona) y la unión no puede
expandir filas. Un duplicado de llave persona u hogar detiene la corrida.
El ponderador es `poblacion.factor`, documentado como factor de persona; no
se toma el factor de una tabla de hogar.

## 4. Categorías y denominadores

- `segsoc`: `1=Sí`, `2=No`.
- `tramo_edad`: `18–29`, `30–44`, `45–59`, `60–96`.
- `tam_loc`: 1 `100 000+`; 2 `15 000–99 999`; 3 `2 500–14 999`;
  4 `<2 500`.
- `est_socio`: 1 Bajo; 2 Medio bajo; 3 Medio alto; 4 Alto.
- `celular`, `conex_inte`: `1=Sí`, `2=No`.

Cada marginal P1 usa como denominador ponderado el subconjunto del universo
principal con valor válido de esa variable. Publica también el mismo
universo principal, cobertura válida y faltantes, con n y masa, para que el
denominador no cambie silenciosamente.

La conjunta P2 enumera por código las 128 combinaciones del producto
`2×4×4×4`. Su denominador es el subconjunto del universo principal con los
cuatro descriptores válidos. Publica la pérdida frente al universo principal.
Una combinación sin filas es `CERO-MUESTRAL`, con n=0, masa=0, proporción=0
y EE/IC no estimables; no se declara imposible ni ausente en población.
Se publican también las 14 marginales de la conjunta sobre exactamente el
mismo subconjunto completo y se exige coincidencia con la suma de celdas.

## 5. Precisión

Método único: bootstrap de UPM con reemplazo dentro de `est_dis`, sobre todo
el marco del universo principal. Cada dominio/categoría se representa por
indicadores (cero fuera del dominio), sin eliminar UPM por celda. Se usan
1,000 réplicas, `numpy.random.Generator(PCG64)`, semilla `20260919`, y un
único plan compartido por todos los estimandos. Un estrato de UPM única se
remuestrea a sí mismo y aporta variación cero; se reporta su número. EE es la
desviación estándar muestral de réplicas válidas e IC95 son percentiles
2.5/97.5. Fallas de denominador no se convierten en cero. Si falta diseño en
el marco, se publican puntos y `PRECISION-NO-DISPONIBLE` para toda la tabla.

## 6. Controles materiales y salidas

El medidor debe verificar: unicidad de llave persona; llaves de hogar únicas;
joins sin expansión y cobertura; reconciliación de exclusiones; particiones
ponderadas iguales a uno; 128 celdas; marginalización de conjunta; contraste
de puntos mediante agregación separada; y soporte UPM por celda. Un control
independiente congelado recalculará `segsoc=1` y la varianza de `edad=18–29`
sin importar el medidor.

RESULT congelados: estados P1/P2/P3; embudo de universo; controles de llaves
y join; diseño; tabla marginal P1 JSON canónica; tabla conjunta P2 JSON
canónica; marginales de casos completos JSON canónica; hashes SHA-256 y
conteos de esas tablas; pérdida por casos completos; tolerancias de
marginalización y contraste. En COMMIT-2 esos JSON se proyectarán sin cambio
a CSV agregados bajo `forense/analisis/enigh2022-perfil-estructural-cli-1/`.

## 7. Interpretación y reservas

La medición es composición estructural descriptiva de personas en hogares
de México, ENIGH 2022. No identifica psicología, cultura, conducta, causalidad
ni un corte migratorio. Los atributos de hogar son constantes entre sus
integrantes. No releva directamente RES-0165…RES-0170, no crea usos activos y
no adjudica `cuenta_gen2`; queda `PENDIENTE-DE-MESA`.
