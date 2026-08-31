# COMMIT-1 · Receta de cobertura-15 (ACTO MAESTRA32-E11)

Congelada antes de tocar `data/inventario-reactivos-v1_2.tsv` / `data/inventario-fd-v1_1.tsv` con propósito de búsqueda dirigida (ya se leyeron sus cabeceras y conteos generales durante el ARRANQUE — eso no cuenta como "tocar las tablas" en el sentido que COMMIT-1 protege: ninguna fila fue buscada por contenido de celda hasta después de escribir esta receta). Fecha: 30/ago/2026. Emisión ciega: este acto no abre `forense/prereg-duelo-v2/corridas-R/` ni ningún archivo con valores publicados de las 15 celdas.

## (a) Extracción del id de regla desde `frase_discriminacion`

Regex `[a-z_]+(?:\.[a-z_]+)+` (minúsculas, sin acentos, ≥1 punto) aplicado a la columna `frase_discriminacion` de las 15 filas del marco congelado. Cruzado contra el catálogo real de 49 ids de regla, re-derivado hoy con:

```
grep -n '· \*\*id:\*\* `[a-z_]*\.[a-z_.]*`' canon/modelo-decision-v4_0.md
```

(49 líneas, dominios: dinero §3.1, trabajo §3.2, tramite §3.3, salud §3.4, familia §3.5, tiempo §3.6, civico §3.7, cooperacion §3.8, informacion §3.9, comunicacion §3.10). Si la frase no nombra un id con esa forma, se deriva del generador por dominio: se listan las reglas SI-ENTONCES del dominio propio de la celda (columna `dominio` del marco) cuyo `PORQUE` cite el mismo generador (G1-G6) que el término que la frase sí nombra, y se declara explícitamente que la asociación es derivación de este acto, no del marco ni de `modelo-decision`. Si ninguna regla del dominio propio (ni, cuando la propia frase apunta a otro dominio, del dominio citado) produce una conducta que corresponda al desenlace descrito, se registra `regla_existe = NO` por derivación de dominio agotada — no se inventa.

## (b) Criterio de "regla existe"

`regla_existe = SI` si el id aparece como clave `id:` en `milpa/tramite.yaml` (único YAML de reglas del motor — `milpa/procedencia.yaml` no tiene bloque `reglas:`, es el libro de procedencia de coeficientes/condicionales) **o** como regla SI-ENTONCES en `canon/modelo-decision-v4_0.md` §3, citada `archivo:línea`. `regla_existe = NO` si ninguna de las dos lo trae, incluido el caso en que la propia `frase_discriminacion` lo declara explícitamente ("M no tiene ninguna regla que...", "ninguna regla del motor...").

## (c) θ y operacionalización

Por regla con `regla_existe = SI`: la θ que la mueve es el parámetro de §2.1-2.2 (`canon/modelo-decision-v4_0.md:396-462`) que el `PORQUE` de la regla cita por generador (`PORQUE G#`), tomando el/los coeficientes de ese generador de la tabla §2.2. Si el `PORQUE` no cita ningún `G#` explícito, se declara `theta = NO-IDENTIFICADA (sin cita G# en modelo-decision §2.1-2.2)`; un candidato derivado por semántica del `PORQUE` (p.ej. "confianza radial" → `radio_confianza`) se reporta aparte, marcado `via=DERIVADO`, nunca como si fuera cita del modelo.

Operacionalización: se filtran `inventario-reactivos-v1_2.tsv` + `inventario-fd-v1_1.tsv` (ambas, cabecera `#` saltada) a `instrumento == <código de la celda>` (familia+año en minúsculas sin espacios, p.ej. `enif2012`; para ENOE, además `payload_id` contiene `_<trimestre>t_` cuando la celda declara trimestre) y se buscan, sobre `variable_id`+`texto_reactivo` normalizados sin acentos, los términos cerrados de cada θ candidata, derivados de su propia ficha en `milpa/procedencia.yaml:condicionales_escalares*`/`condicionales_confianza_institucional` (el contenido real del reactivo que la opera en el instrumento donde SÍ está medida, no un sinónimo libre):

| θ | términos (regex, ya sin acentos) | ficha fuente |
|---|---|---|
| `radio_confianza` | `mayoria de las personas` · `personas que conoce` · `vecinos de (su\|la)` | `procedencia.yaml:280-299` (ENCUCI AP5_1_1/2/3) |
| `familismo_apoyo` | `cubrir.{0,25}vejez` · `dinero de familiares` · `\bp9_9` | `procedencia.yaml:300-320` (ENIF P9.9, ítem p9_9_4) |
| `confianza_institucional[financiera]` | `confia.{0,25}(banco\|institucion(es)? financiera)` | `procedencia.yaml:204-213` (ENIF P11_1_1-5) |
| `norma_de_género`/`familismo_obligacion` | `obligaci\w*.{0,30}cuidad` · `deber.{0,20}cuidad` · `\bp7_12` | `modelo-decision:256` nota + ENASIC P7_12_7 |
| `exposicion_violencia` | `amenaza` · `agresion fisica` · `secuestro` · `agresion sexual` · `violacion` | `procedencia.yaml:390-423` (ENVIPE AP7_3_10-14) |

Cuando el instrumento filtrado tenga `texto_reactivo` vacío en el 100% de sus filas (verificado caso por caso, ver COMMIT-2), la búsqueda de texto es censurada por el propio inventario, no una confirmación de ausencia (A.13): se declara así y se complementa con un barrido del listado completo de `variable_id` distintos de ese instrumento (códigos, no prosa) para juzgar por familia de código si existe una batería plausible del constructo.

## (d) CANDIDATO y exclusión de circularidad

`CANDIDATO` = al menos un término de la θ hace match dentro del instrumento+ola filtrado, en una fila cuyo `variable_id` **no** sea la variable de la propia celda. `CIRCULAR-EXCLUIDO` = la θ solo se operacionaliza, en el instrumento+ola de la celda, mediante la misma variable de la celda, **o** existe un precedente ya sellado en `milpa/procedencia.yaml` que declare esa θ inválida para identificar esa clase de regla/desenlace — precedente aplicado en este acto: `procedencia.yaml:315-320`, *"NO USAR para identificar G5·familismo_apoyo... el desenlace de G5 en ENIF es `familia.seguro.volatilidad_ausencia_estado`, observado con la misma batería P9_9_1..6 — circular"* (el precedente `ENIF p9_9_4` que el encargo cita).

## (e) Celdas fuera de unidad persona/hogar

`EMP-02`, `EMP-04` (unidad: empresa, ENAFIN) y `DOC-06` (unidad: documento, cartera de crédito de una emisora) reciben `EXISTE-NO-SATISFACE` directo, razón `"unidad de análisis fuera del dominio del motor"`, **sin correr (a)-(c)** — declarado aquí, antes de abrir ninguna tabla, tal como exige el encargo.

## (f) B-bis y falsador del acto

Umbrales de `EXISTE-SATISFACE` sobre los 15: ≥8 lote de caja completo; 3-7 parcial (se dice cuáles y por qué las otras no); ≤2 D1=(i) no viable con el corpus abierto hoy. Falsador del acto (declarado en el encargo, no de este documento): si (a)-(c) resulta inaplicable —`regla_existe = NO` por derivación de dominio agotada, sin el escape de (e)— en ≥5 de las 15 celdas, se reporta como hallazgo sobre el alcance del motor, no se parcha la receta.

**El primer resultado que produzca este procedimiento es el que se reporta.**
