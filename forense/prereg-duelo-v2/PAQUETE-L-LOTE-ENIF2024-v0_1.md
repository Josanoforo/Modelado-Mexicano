# Paquete de la corrida `L` — lote de cruces ENIF 2024, `ahorra_solo_informal`

**Acto que lo produce:** `ACTO GEN2-DIN-LOTE-ENIF2024-A` · pieza P4 · 21/sep/2026 ·
entorno **NUBE** (`milpa-inegi`) · rama `acto/gen2-din-lote-enif2024-a`.
**CONTADOR: cero.** Este acto **no corre ninguna `L`**: produce el paquete que **mesa**
ejecuta, por **CLI y sin `ANTHROPIC_API_KEY`** (`FP-228`), en una sesión limpia fuera de
este proyecto.

**Orden sagrado:** hashes → `L` → `R` → scoring. **Las sesiones `L` jamás ven `R`.**

> ⚠️ **Este paquete todavía no se puede lanzar.** Depende del **COMMIT-1 del lote**, que
> es el que congela `spec.yaml` y, con él, los tramos de `edad` y `escolaridad` que
> definen las celdas. Lo que este documento fija —y fija para siempre— es **el prompt,
> el número de repeticiones, el formato de captura y la regla de agregación**. Lo que
> falta es sustituir la rejilla, que **se lee del árbitro, no se teclea** (§3).

---

## 0 · Prohibición explícita — léela antes de arrancar

**Durante esta corrida NO se abre, ni se pega en ningún prompt:**

- `forense/prereg-duelo-v2/corridas-R/` y cualquier `scoreboard-*.md`;
- `forense/prereg-duelo-v2/corridas-M/`;
- **`milpa/tramite-ola5-propuesta-v0.yaml`** — contiene los marginales sellados del
  árbitro de ENIF 2024, que son justo lo que `L2` recibe **curado y sólo curado** (§2),
  y lo que `L1` **no puede ver en absoluto**;
- **cualquier microdato de ENIF**, de cualquier ola;
- los resultados de los pilotos 1, 2 y 3.

**Quien corre `L1` y quien corre `L2` no comparten sesión.** `L1` es la dieta viva
«solo»; `L2` recibe exactamente el bloque de marginales de §2 y nada más.

---

## 1 · Qué se elicita, y de qué celdas

**Estimando, idéntico al de la spec** (`DIN-lote-enif2024-spec-v0_1-PROPUESTA.md` §1):
la proporción, **entre las personas de 18 años y más de México**, que **en los 12 meses
previos a junio de 2024 ahorró o guardó dinero por alguna vía informal y por ninguna vía
formal**.

**Celdas del paquete: las 44 de los 5 pares primarios.**

| par | celdas |
|---|---|
| `sexo × edad` | 8 |
| `sexo × escolaridad` | 8 |
| `sexo × localidad` | 4 |
| `edad × escolaridad` | 16 |
| `escolaridad × localidad` | 8 |
| **total** | **44** |

**Las 52 celdas de los 9 pares no primarios quedan fuera de este paquete, y se dice por
qué:** `L1` y `L2` son contendientes **secundarios**, y los pares de `formalidad` y de
`cuenta_formal` **también** lo son. Elicitar un contendiente secundario sobre un par
secundario cuesta 52 × 2 × 8 = 832 llamadas y no puede mover ninguna adjudicación. Si
mesa quiere ampliarlo, es una decisión suya y se declara antes de correr.

**Si hay que recortar, se recortan CELDAS, nunca `k`.** Bajar las repeticiones cambia el
estimador (la mediana de 8 no es la mediana de 3); quitar celdas sólo reduce el alcance,
y el alcance se declara. Esta regla es parte del paquete.

---

## 2 · Los dos prompts, verbatim

Los dos son idénticos salvo el bloque `CONTEXTO`, que **sólo** `L2` lleva. Los campos
entre `«…»` los sustituye el generador del COMMIT-1 desde `spec.yaml`; **ningún texto
por celda se redacta a mano**.

### 2.1 · `L1` — LLM solo

```
Eres un analista de encuestas de hogares en México. Responde solo con el JSON pedido.

DEFINICIÓN. Una persona "ahorra solo por vías informales" si, en los 12 meses previos a
junio de 2024, (a) ahorró o guardó dinero por al menos una de estas seis vías: prestando
dinero; comprando animales o bienes; en una caja de ahorro del trabajo o de personas
conocidas; con familiares o personas conocidas; en una tanda; en su casa; Y ADEMÁS
(b) NO guardó ni ahorró en ninguna de estas nueve: cuenta o tarjeta de nómina; de
pensión; para recibir apoyos de gobierno; cuenta de ahorro; cuenta de cheques; depósito
a plazo fijo; fondo de inversión; cuenta contratada por internet o aplicación no
bancaria; otro tipo de cuenta.

UNIVERSO. Personas de 18 años y más residentes en México, una por hogar (la persona
elegida de la Encuesta Nacional de Inclusión Financiera 2024 del INEGI).

CELDA. «eje_A» = «categoría_A» Y «eje_B» = «categoría_B».

TAREA. Da tu mejor estimación puntual de la proporción de personas de esa celda que
ahorran solo por vías informales.

REGLAS. Es una proporción entre 0 y 1, con tres decimales. No expliques. No des un
rango. No digas que no puedes saberlo: da tu mejor número. Si tu estimación es
incierta, el número sigue siendo tu mejor estimación.

FORMATO DE SALIDA. Exactamente un objeto JSON, sin texto alrededor:
{"celda_id": "«celda_id»", "p": 0.000}
```

### 2.2 · `L2` — LLM con corpus

Idéntico al anterior, con este bloque insertado **entre `UNIVERSO.` y `CELDA.`**:

```
CONTEXTO. De la misma encuesta, ya publicados, los porcentajes de personas que ahorran
solo por vías informales en cada categoría por separado (no en el cruce):
  «eje_A» = «categoría_A»: «p_A» — «eje_A» = «otras categorías del eje A con su p»
  «eje_B» = «categoría_B»: «p_B» — «eje_B» = «otras categorías del eje B con su p»
  Nacional: «p».
Úsalos como quieras. No son la respuesta: la celda del cruce no está publicada.
```

**Qué entra en `CONTEXTO` y qué no.** Sólo los **marginales públicos de un eje** de ENIF
2024 —los que el árbitro ya tiene sellados— y el nacional. **No** entra el cruce, **no**
entra ningún resultado de los pilotos, **no** entra el valor de `C2` ni de ningún otro
contendiente. Un `CONTEXTO` que trajera el cruce convertiría a `L2` en un lector, no en
un estimador.

---

## 3 · Lo que el COMMIT-1 sustituye, y de dónde lo saca

| campo | de dónde sale |
|---|---|
| `«eje_A»`, `«eje_B»`, `«categoría_A»`, `«categoría_B»` | **del árbitro**, vía `spec.yaml`. La rejilla **se lee, no se teclea**. Las etiquetas en el prompt van en castellano llano (p. ej. «localidades de menos de 15 000 habitantes»), no con el código del catálogo |
| `«celda_id»` | identificador estable de la celda, el mismo que usan los emisores mecánicos |
| `«p_A»`, `«p_B»`, `«p»` | marginales públicos sellados de ENIF 2024, citados por su `RESULT` |

**El generador es mecánico.** Se importa la plantilla de este documento y se aplica a la
rejilla; **ningún prompt por celda se redacta a mano**, como en `PAQUETE-L-v1_2`.

---

## 4 · Repeticiones, agregación y modelo

- **Repeticiones: `k = 8` por celda y por variante.** Mismo `k` que la spec sellada de
  `L`. Total de llamadas: **44 celdas × 2 variantes × 8 = 704**.
- **Agregación declarada: la MEDIANA** de las `k` respuestas válidas, por celda y por
  variante. Es lo que la spec sellada de `L` ya usa; **no se cambia aquí ni se decide
  después de ver las capturas**.
- **Respuesta inválida** (no es JSON, `p` fuera de `[0,1]`, falta `celda_id`, o el
  `celda_id` no es el pedido): se marca `estado_captura = RECHAZO`, **se conserva** y
  **no se sustituye con un reintento**. Si una celda queda con menos de 5 respuestas
  válidas, se emite como `L-INSUFICIENTE` con su conteo, no como un número.
- **Modelo, versión y temperatura se fijan AL CORRER**, y se anotan en cada captura con
  **cita del proveedor para la fecha de corte de entrenamiento**. Razón, escrita en el
  diseño v0.1 §2: una reserva no caduca para un contendiente mecánico que todavía no
  existe, pero **sí caduca para un LLM**, que acabará leyendo la ola en su entrenamiento.
  Por eso los `L` entran ahora y por eso la fecha de corte es parte del dato.
- **Temperatura**: la que el CLI use por defecto, **declarada**, no ajustada por celda.

---

## 5 · Formato de captura

Un `JSON Lines` por variante, en `forense/prereg-duelo-v2/corridas-L/`, una línea por
llamada, con **exactamente** estos campos:

```json
{"celda_id": "...", "variante": "L1", "rep": 1, "p": 0.412,
 "estado_captura": "OK", "modelo": "...", "version": "...", "temperatura": 0.0,
 "corte_entrenamiento": "... (cita del proveedor)", "prompt_sha256": "...",
 "ts_utc": "2026-..-..T..:..:..Z"}
```

`prompt_sha256` es el sha256 del prompt **exacto** que se envió, para que cualquiera
pueda reconstruir qué se preguntó sin confiar en la plantilla.

---

## 6 · Sellado — cuándo, y contra qué

**Las capturas se sellan ANTES de que exista el COMMIT-2 mecánico.** Es la condición que
hace de `L` un contendiente y no un comentario: una captura producida después de ver una
emisión mecánica no cuenta, y no hay forma de demostrar que no la vio salvo el orden del
diff. **El orden del diff es el sello.**

Al sellar se emite, en el mismo commit: el `JSON Lines` de cada variante, su `sha256`, el
conteo de `OK` / `RECHAZO` por celda, y la mediana por celda y variante. **Este acto no
corre nada de eso.**

---

## 7 · Lo que este paquete NO hace

No corre las llamadas · no congela `spec.yaml` · no fija la rejilla · no abre microdato ·
no toca `corridas-R/` ni `corridas-M/` · no adjudica: `L1` y `L2` son **retadores
secundarios y se rotulan así**.
