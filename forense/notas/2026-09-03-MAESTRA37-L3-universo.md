# MAESTRA37-L3 · P0 — universo de lectura congelado (COMMIT-1)

**Este commit se hace ANTES de emitir un solo veredicto.** El criterio que
congela es: *el primer resultado que produzca este procedimiento es el que se
reporta.* No hay segunda pasada, no hay reformulación, no se eligen términos:
esto es **censo, no búsqueda** — se lee todo lo que la lista cerrada de abajo
enumera, y el veredicto A.4 de `P1` sale de ese texto.

Por qué importa que el orden sea éste: `MAESTRA37-L1` (ADR-321) dio salud
**1 de 5** corriendo formulaciones congeladas en vocabulario INEGI, y el
propio encargo de este acto exhibe que el negativo era **de las
formulaciones, no del corpus**. Un acto que primero mira y luego decide qué
cuenta como universo puede fabricar el resultado que quiera. Congelar el
universo primero es lo que hace falsable a `P1`.

## Universo declarado en una línea (A.13)

**11 archivos examinados** — 1 inventario + 5 catálogos `.xlsx` + 5 PDF de
cuestionario — que rinden **121 etiquetas de variable** (utilizadores,
microdato), **1 914 variables de catálogo** con **8 790 filas
`variable → código → etiqueta`** (utilizadores, hogar, integrantes, adultos,
menores) y **8 973 líneas de texto de cuestionario** sobre **136 páginas**.

### (a) Las 121 variables etiquetadas de `utilizadores` 2024

Fuente: `data/inventario-reactivos-descargas-mx-v1_0.tsv` (producido por
`MAESTRA37-L1`; este acto **lo lee, no lo re-extrae**), filtrando
`payload_id = utilizadores_ensanut2024_w.stata.stata.zip`.

```
awk -F'\t' '$1=="utilizadores_ensanut2024_w.stata.stata.zip"{print $6"\t"$7}' \
  data/inventario-reactivos-descargas-mx-v1_0.tsv   # -> 121 filas
```

Advertencia de honestidad que gobierna `P1`: **Stata trunca la etiqueta a 80
caracteres**, y se ve a simple vista en el volcado (`u0202b` corta en
*"¿Entonces tiene(s) derecho/puede(s) atenderse(te) en los siguientes
servi"*). Ninguna regla se falla por una etiqueta truncada: se completa antes
con (b) o (c).

### (b) Catálogos de valores — anexo `data/l3-ensanut2024-catalogos-v1_0.tsv`

Los cinco `.Catlogo.xlsx` de INEGI en la raíz `descargas_mx`
(`data/raices.local.yaml` → `/mnt/c/Users/PC0/Descargas MX`), hojas
`Variables` (etiqueta de variable) y `Valores` (código → etiqueta de
respuesta), extraídos con `openpyxl 3.1.5`:

| módulo | archivo | variables | filas de valor | variables sin catálogo de valores |
|---|---|---:|---:|---:|
| `utilizadores` | `utilizadores_ensanut2024_w.Catlogo.xlsx` | 122 | 398 | 81 |
| `hogar` | `hogar_ensanut2024_w_ICB.Catlogo.xlsx` | 204 | 550 | 68 |
| `integrantes` | `integrantes_ensanut2024_w_ICB.Catlogo.xlsx` | 261 | 2 353 | 65 |
| `adultos` | `adultos_ensanut2024_w.Catlogo.xlsx` | 843 | 3 332 | 244 |
| `menores` | `menores_ensanut2024_w.Catlogo.xlsx` | 484 | 1 546 | 153 |
| **total** | | **1 914** | **8 179** | **611** |

El anexo trae **8 790 filas de dato** = 8 179 filas de valor + 611 filas de
variable **sin** catálogo de valores (continua, abierta o identificador). Ese
segundo bloque está ahí a propósito: si sólo se anexaran las variables con
códigos, el censo perdería en silencio 611 variables y un `NO-ENCONTRADO`
posterior no sería auditable. `sha256_12 = 725185c6bd64`.

**`menores` entra al anexo aunque ninguna regla de salud lo interpele.** Es
censo: se lee todo el catálogo disponible, y dejar fuera un módulo por
anticipar que "no va a servir" es exactamente elegir términos.

### (c) Texto de los 5 cuestionarios — anexo `data/l3-ensanut2024-cuestionarios-v1_0.txt`

`pdftotext -layout <pdf> -` sobre cada uno, concatenado con una cabecera por
PDF que lleva su `sha256_12` y su número de páginas. `sha256_12 = 94f454ffc893`,
768 KB, 8 979 líneas (8 973 de texto + 6 de cabecera del anexo).

| # | PDF | `sha256_12` | páginas |
|---|---|---|---:|
| 1 | `1 VFINAL Cuestionario Hogar ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` | `adc873843b79` | 28 |
| 2 | `2 VFINAL Cuestionario nios 0 a 9 ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` | `af65f922094c` | 29 |
| 3 | `3 VFINAL Cuestionario adolescentes ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` | `344f32ef0f87` | 28 |
| 4 | `4 VFINAL Cuestionario adultos ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` | `0bc30c3b7f08` | 44 |
| 5 | `5 VFINAL Cuestionario utilizadores ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` | `004aacee3729` | 7 |

Estos 5 PDF produjeron **0 filas** en el inventario de `L1` (defecto DE2, que
registra `MAESTRA37-N4`). Que el extractor no los leyera no dice nada sobre lo
que contienen: por eso entran aquí con texto a la vista, y por eso la
cobertura retroactiva del encargo (A.8 punto 3) es correcta —
**ningún acto anterior había leído este texto**.

### (d) `adultos` microdato — **AUSENTE-EN-RAIZ**

Verificado al arrancar el acto, 3/sep/2026, **antes** de cualquier lectura:

```
ls "/mnt/c/Users/PC0/Descargas MX" | grep -i ensanut2024   # 14 aciertos de 149 archivos
```

De `adultos` la raíz tiene **sólo catálogo** — `adultos_ensanut2024_w.Catlogo.xlsx`
y `adultos_ensanut2024_w.Catlogo.csv.csv.zip`. **`adultos_ensanut2024_w.stata.stata.zip`
no está.** Mesa no lo depositó hoy. Por la regla del encargo se declara
`AUSENTE-EN-RAIZ` y **no se espera**: no hay alta A.7, no se toca
`data/manifiesto.yaml` ni las tres capas del curador, y `P1` acota el
veredicto de las reglas que dependen de `adultos` a esa ausencia.

Matiz que sí cambia el alcance de `P1`, y que conviene fijar aquí antes de
mirar: **el catálogo de `adultos` sí está, con 843 variables etiquetadas y
3 332 filas de valor, y el cuestionario de `adultos` también (44 páginas).**
Es decir: de `adultos` se puede leer **qué se preguntó**, aunque no se puedan
contar respuestas. Eso permite distinguir dos cosas que un `NO-ENCONTRADO`
plano confunde — *"el instrumento no lo pregunta"* frente a *"lo pregunta pero
el microdato no está en el corpus"* —, y esa distinción es justamente la que
decide si lo que falta es **adquisición** o **instrumento** (P2). No es una
licencia para dar `EXISTE-SATISFACE` sin microdato: una regla cuyo desenlace
sólo consta en el cuestionario de `adultos` no puede medirse, y `P1` lo dirá
con ese nombre.

## Lo que este universo NO incluye, dicho antes de mirar

- Los `.csv.csv.zip` de microdato: son el mismo dato que los `.stata` ya
  inventariados (`utilizadores` 121 = 121, `menores` 483 = 483,
  `adolescentes` 478 = 478) y no aportan etiqueta.
- `hogar` e `integrantes` **microdato**: sus 203 y 260 variables entraron al
  inventario de `L1` sin texto de reactivo (0 filas con texto, formato CSV).
  Su **catálogo** sí está en (b) con etiqueta y códigos, que es lo que `P1`
  necesita para leerlos.
- Cualquier fuente fuera de ENSANUT 2024. Este acto es lectura dirigida a un
  instrumento, no un barrido.
- Ninguna descarga. El acto no baja nada.

## Cierre de P0

Con esto queda congelado el universo. `P1` emite los cinco veredictos A.4
contra **este** texto y ningún otro; si un veredicto necesitara algo que no
esté en la lista de arriba, la respuesta correcta es decir que falta —
no ampliar el universo después de haber mirado.
