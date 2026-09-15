# El mapa completo de las 19 `CORR` sin candidato — y las tres decisiones que le faltan a mesa

**Acto:** `ACTO GEN2-SPECS-DEMANDA-1`, 15/sep/2026, entorno **NUBE**, sobre
`origin/main = f5a52272a8208eaf56f3b6d5db9531786d0d6534`.
**Mapa legible por máquina:** `data/corrida0/mapa-demanda-19-corr-v1_0.tsv`.
**Contador: cero mediciones.** Un acto de specs congeladas produce contratos,
no números.

---

## 1 · El resultado en una tabla

De las 19 corridas que `data/corrida0/demanda-corridas.tsv` marca
`SIN-CANDIDATO-EN-EL-REGISTRO`:

| estado | n | qué significa |
|---|---|---|
| **`SPEC-CONGELADA`** | **4** | este acto escribió y congeló las dos capas de `D-15`; falta el medidor, que es de CAJA |
| `EXISTE-SATISFACE` | 2 | ya relevadas por spec congelada anterior — **no se re-especifican** |
| `EXISTE-NO-SATISFACE` | 3 | hay spec o `CALC`, pero no releva esta corrida (o la releva en parte) |
| `BLOQUEADA` | 10 | bloqueador nombrado; 6 de ellas esperan una **decisión**, no una descarga |

Las cuatro congeladas:

| `CORR` | instrumento | `CALC` | spec humana sellada |
|---|---|---|---|
| `CORR-0011` | ENIGH 2022 · remesas | `CALC-ENIGH-0001` | `prereg-caja-ENIGH-REMESAS-R51` |
| `CORR-0012` | ENFIH 2019 · Afore | `CALC-ENFIH-0001` | `prereg-caja-ENFIH-AFORE` |
| `CORR-0013` | EDER 2017 · primera unión | `CALC-EDER-0003` | `prereg-caja-EDER-UNION-LIBRE` |
| `CORR-0014` | ENUT 2024 · reparto del cuidado | `CALC-ENUT-0001` | `prereg-caja-ENUT-CUIDADO` |

Estado mecánico de las cuatro, con el comando a la vista — el **único**
bloqueo en las cuatro es el medidor, que este acto deliberadamente no escribe:

```
$ python3 tools/corrida0.py preflight CALC-ENIGH-0001 | tail -1
PRE-FLIGHT: BLOQUEADO script_ausente=data/corrida0/CALC-ENIGH-0001/medidor.py
    (idem CALC-ENFIH-0001, CALC-EDER-0003, CALC-ENUT-0001)
```

Todo lo demás pasa: esquema **`ENDURECIDO`** reconocido, `seed` con `rng`
declarado, `tolerancia` con tipo, `inputs` de repo `COINCIDE` por `sha256`,
`inputs` de manifiesto resueltos a su raíz lógica con el `sha256` esperado
(`NO-VISIBLE-EN-ESTE-CONTEXTO` es el aviso `FP-352` correcto en nube, no un
fallo). `E.5` respetado sin excepción: se abrieron **codebook** (el FD, vía
`data/inventario-fd-v1_1.tsv`) y **metadato** (manifiesto e inventarios
canónicos de reactivos), y **cero bytes de microdato** — el entorno no tiene
`data/raw` montado y este acto no lo pidió.

---

## 2 · Lo que el recorrido encontró y nadie había mirado

Tres de estos cuatro hallazgos cambian lo que haría un medidor. El cuarto
cambia lo que mesa cree que le falta.

### 2.1 · `CORR-0014` — el ponderador no está donde la regla dice

`milpa/tramite.yaml:1036` declara el ponderador `FAC_HOG` y `:1038` sitúa el
universo en *«los 29 181 hogares de `tvar_crea.csv`»*. Verificado por archivo:

```
$ awk -F'\t' '$5=="tvar_crea.csv"{print $6}' data/inventario-reactivos-v1_2.tsv | grep -c '^FAC_HOG$'
0            # 60 columnas reales, las mismas 60 que el FD declara para TVAR_CREA
$ awk -F'\t' 'toupper($6) ~ /^FAC/ {print $5"  "$6}'  …enut2024_bd_csv.zip…
  thogar.csv FAC_HOG · tsdem.csv FAC_HOG · tvar_crea.csv FAC_PER · tmodulo.csv FAC_PER · tvivienda.csv FAC_VIV
```

**`FAC_HOG` vive en dos archivos, en ninguno de los cuales están las horas.**
Un medidor que siguiera la letra de la regla falla en la primera línea; uno
que resolviera `FAC_HOG` por nombre tomaría el de cualquiera de los dos sin
que nada se queje. La spec fija `tsdem.csv` (precedente de
`tools/medidor_cuidado_enut.py`) **y** añade la guarda que nadie había
corrido: `G-FAC-HOG-TSDEM-IGUAL-THOGAR`, los dos comparados hogar por hogar.
Si difieren, la elección de archivo cambia la cifra.

### 2.2 · `CORR-0013` — el payload declarado no produjo el número

`demanda-resultados.tsv`, `RES-0043`/`RES-0044`:
`payload = eder_2017_eder2017_bases_csv` (`sha bcc7eb90…`),
`clase = MEDIDO·p(… ENADID 2023, p3_27_ag)`, y `milpa/tramite.yaml:1005` da
`n = 152 950`, que es el `n` de ENADID (EDER aporta 18 687).

Un `verify` resolvería el ZIP de EDER como INPUT de una cifra calculada sobre
otro instrumento, **y el hash coincidiría**. Además,
`grep ENADID data/corrida0/demanda-corridas.tsv` → **0 aciertos**: el
instrumento que produjo la cifra activa no aparece en ninguna corrida, pese a
estar en el manifiesto. Consecuencia en la spec:
`A-DELTA-VS-GEN1 = NO-APLICA-ESTIMANDO-DISTINTO`, **declarado y no calculado**
— comparar *tipo de primera unión* con *situación conyugal actual* sería el
promedio de preguntas distintas que la propia regla prohíbe.

### 2.3 · `CORR-0011` — el bloqueo era de autorización, no de medición

`CALC-B-0001` ya produjo el punto 2022 con sello válido
(`RESULT-B-ENIGH-2022-P = 0.04569409956405095`, IC de diseño, `n = 90 102`), y
su propia spec sellada declara `reglas_bajo_prueba: NINGUNA … T9, verbatim: es
modelo nuevo y ninguna cifra suya entra a un veredicto`. **El número existe y
no puede usarse.** La spec nueva no levanta `T9` —es una firma de mesa sobre
un ensayo cuyo objeto era otro— sino que abre la corrida que `T9` dejó
vacante, y añade lo que el ensayo no tiene: el complemento **contado** (con
`1 − p`, una fila fuera del mapa es invisible por construcción) y una
reejecución rotulada `REPLICA-RESULTADO`, **nunca** `REPRODUCE` (`E.3`).

### 2.4 · Dos «payload faltante» que no faltan

`A.8` contra el manifiesto, resuelto **por hash y no por nombre**:

| `CORR` | lo que el registro dice | lo que el manifiesto tiene |
|---|---|---|
| `CORR-0001` | «ENCIG2023, **sin payload**» (`ENCIG-MORDIDA-spec-v1_0.md:142`) | `encig23_base_datos_csv` (`af733d86…`, 38 309 647 B, 29/jul/2026) **+ cuatro gemelos** RData/DBF/DTA/SAV (5/ago/2026) |
| `CORR-0010` | `payload_manifiesto_id: "NO-LOCALIZADO"` | `enif_2024_enif_2024_bd_csv` → `enif_2024_bd_csv.zip`, cuyo `sha256` **coincide exacto** con el `sha256_payload` que la propia regla declara (`00e4b0b4…f039`) |

En `CORR-0010` el acto de entonces buscó el id `enif2024_csv` — que es
**otro** ZIP (`a3507b40…`) — y concluyó `NO-LOCALIZADO` con razón, dado lo que
buscó. El hash lo resuelve sin descargar nada. Es el mismo patrón que `NC-0188`
ya corrigió para ENNViH. **Ninguno de los dos va a cola de adquisición.**

Ninguna spec sellada se edita por esto (`E.3`): el defecto se asienta con su
comando y la corrección de `milpa/` es de mesa o del acto de CAJA que la tome.

---

## 3 · Las tres decisiones, armadas

El encargo pide que las que no se puedan congelar lleguen con la decisión
**preparada, no pendiente**. Son tres, y cubren 6 de las 10 bloqueadas.

### D1 · `CORR-0001` — ENCIG 2023: qué hacer con cuatro celdas ASIGNADAS cuya ola 2025 ya está medida

**La pregunta que el encargo anticipaba** («adquirir vs. celda sin fuente»)
**no es la que hay**: el payload está adquirido desde el 29/jul/2026, en cinco
formatos. La pregunta real:

`CORR-0001` son 4 celdas **ASIGNADAS** de dos reglas:

| `RESULT` | celda | ASIGNADO | la misma regla, MEDIDA en ENCIG 2025 (`CORR-0002`) |
|---|---|---|---|
| `RES-0001` / `RES-0002` | `tramite.mordida.discrecional` | 0.62 / 0.38 | `paga_mordida_encig2025` = **0.085118** |
| `RES-0007` / `RES-0008` | `tramite.mordida.con_registro` | 0.12 / 0.88 | ramas presencial/digital, 0.116 – 0.029868 |

La distancia entre `0.62` asignado y `0.085118` medido no es ruido: es un
factor de siete. Tres opciones, y **ninguna es obvia**:

| | opción | qué cuesta | qué deja |
|---|---|---|---|
| **(a)** | **Retirar** las 4 celdas asignadas; el motor se queda con las medidas de ENCIG 2025 | nada de cómputo; es una edición de `milpa/` con firma | El modelo pierde la celda «sin ola declarada» y gana coherencia. Riesgo: si algún consumidor usa la celda genérica sin sufijo de ola, se queda sin valor |
| **(b)** | **Medir ENCIG 2023** y sustituir las asignadas por la ola 2023 | una corrida de CAJA; el payload ya está, el medidor de `CALC-ENCIG-0001` es reutilizable casi entero (mismo instrumento, secciones equivalentes) | Da una **serie** 2023→2025 sobre el mismo reactivo, que es lo que `R3.1`/`R3.2` necesitan para distinguir nivel de tendencia. Coste real, valor real |
| **(c)** | **Conservarlas** como prior declarado, rotuladas `ASIGNADO·PRIOR`, y no tocarlas | nada | Honesto, pero deja conviviendo 0.62 y 0.085118 para la misma conducta. Es lo que hay hoy, sin decirlo |

**Recomendación de este acto: (b)**, y la razón es que es la única que produce
una medición nueva en vez de mover una etiqueta. `A.8` ya pagó el
descubrimiento de que el payload está; el trabajo restante es una tanda de
CAJA sobre un instrumento que el programa ya sabe leer. **(a)** es el
sustituto barato si mesa no quiere abrir CAJA para esto.

> **Firma de mesa (marcar una):**  ☐ (a) retirar  ☐ (b) medir ENCIG 2023  ☐ (c) conservar como prior

### D2 · `CORR-0004`, `CORR-0005`, `CORR-0006`, `CORR-0019` — el ASIGNADO que convive con su MEDIDO

Las cuatro son la **misma decisión a distinta escala**, y por eso van juntas y
no en cuatro actos:

| `CORR` | celdas | ASIGNADO | ¿hay MEDIDO de la misma regla? |
|---|---|---|---|
| `CORR-0005` | `tramite.gobierno_digital.util_sin_coercion:adopta` | 0.71 | **Sí** — `adopta_encig2025_luz` = 0.673393 (`CORR-0002`) |
| `CORR-0006` | `tramite.evasion_norma:evade_norma` | 0.66 | **Sí** — `evade_norma_envipe2025` = 0.562774 (`CORR-0007`) |
| `CORR-0004` | `tramite.gobierno_digital.coercitivo:adopta` | 0.09 | **No** — y la fuente que el registro nombra (`validacion:CoDi`) es serie administrativa agregada |
| `CORR-0019` | 21 celdas de `procedencia.yaml` | varias | Caso por caso |

Y el hallazgo de unidad, que es el que cierra la puerta a la salida fácil:
`validacion:CoDi` y `validacion:SPEI` **no son instrumentos**. Lo que hay en
corpus es `banxico_codi_cuentas_validadas_x_mil_hab` (XLSX trimestral) y
`banxico_sie_cf890/cf891` (series diarias 2009-2026). **Una serie de cuentas
por mil habitantes no produce `p(adopta | le ofrecen servicio)`** sin un
supuesto de identificación que nadie ha firmado. El bloqueador es de **unidad
de observación**, no de adquisición: adquirir más no lo levanta.

**La decisión, en una línea:** ¿el programa mantiene celdas ASIGNADAS de una
regla cuando esa misma regla ya tiene celda MEDIDA en una ola concreta?

| | opción | consecuencia |
|---|---|---|
| **(a)** | **Precedencia del MEDIDO**: la celda asignada se retira en cuanto existe una medida de la misma regla, sea cual sea la ola | Cierra `CORR-0005`, `CORR-0006` de golpe y da criterio para las 21 de `CORR-0019`. Es una regla de gobierno, no un acto |
| **(b)** | **Convivencia declarada**: asignado y medido coexisten con rótulos distintos y el consumidor elige | No cierra nada; requiere que cada consumidor declare cuál usa |
| **(c)** | Caso por caso | Lo que hay hoy. 6 `CORR` siguen abiertas indefinidamente |

**Recomendación de este acto: (a)**, porque es lo único que escala a las 21
celdas de `CORR-0019` sin 21 decisiones. `CORR-0004` queda fuera de (a) —no
tiene medido— y se resuelve por separado: o se le busca instrumento de unidad
persona (ENIF tiene adopción de pago digital; ENCIG 2025 familia C ya midió la
rama no coercitiva), o se rotula `ASIGNADO·SIN-INSTRUMENTO` y se deja quieta.

> **Firma de mesa (marcar una):**  ☐ (a) precedencia del MEDIDO  ☐ (b) convivencia declarada  ☐ (c) caso por caso
> **Y para `CORR-0004`:**  ☐ buscar instrumento de unidad persona  ☐ rotular `ASIGNADO·SIN-INSTRUMENTO`

### D3 · `CORR-0018` — los siete coeficientes sin procedencia

Los 7 de `milpa/procedencia.yaml:coeficientes_generador_sellados` (G1, G3, G4,
G5) traen `fuente` **en prosa** (p. ej. *«coeficientes_generador_medidos.
G1_confianza_institucional, 4/ago/2026»*) y **ningún** `payload_id`, **ningún**
hash, **ningún** script. Son literalmente los *«7 coeficientes sin hash ni
script»* del diagnóstico que motivó `v2.13`.

**No se les puede escribir spec sin antes trazar qué instrumento produjo cada
uno**, y eso es arqueología, no especificación: el trabajo es leer las notas
de agosto y reconstruir la cadena, con el riesgo de que alguna no se pueda
reconstruir. La decisión es de presupuesto:

| | opción | consecuencia |
|---|---|---|
| **(a)** | Un acto de arqueología dedicado, uno por coeficiente, con `A.4` explícito cuando la cadena no se reconstruya | Caro. Es la única vía a `E.2` completa para el generador |
| **(b)** | Rotular los 7 `SIN-PROCEDENCIA-VERIFICABLE` en el registro derivado de `CORRIDA-0` (`E.1` ya prevé ese rótulo) y no tocarlos | Barato y honesto. El generador sigue corriendo con cifras cuya cadena se declara incompleta |
| **(c)** | Re-medirlos de cero bajo spec GEN2 | Lo más caro; sólo vale si sus valores son materiales para alguna decisión |

**Recomendación de este acto: (b) ahora, (a) o (c) cuando un consumidor los
haga materiales.** `E.4` es explícita: *«materialidad por consumidor, no por
spec: sólo lo material sube a mesa»*, y hoy nadie ha medido si estos 7 mueven
algún resultado.

> **Firma de mesa (marcar una):**  ☐ (a) arqueología por coeficiente  ☐ (b) rotular `SIN-PROCEDENCIA-VERIFICABLE`  ☐ (c) re-medir

---

## 4 · Qué sigue, sin decisión de mesa de por medio

Cuatro corridas se pueden congelar en una tanda 2 **en nube**, sin esperar
ninguna firma, y en este orden de coste creciente:

1. **`CORR-0017`** — la capa humana ya está sellada (`prereg-caja-S7-L17`,
   v1.0 y v1.1). Falta sólo el `spec.yaml`. No hay reactivos que resolver.
2. **`CORR-0016`** — el «payload» es un artefacto del repo
   (`data/l8-resultados-tipo-boleta-v1_0.json`, 43 545 B, versionado): la spec
   se construye entera con `inputs: origen: repo`, **sin tocar `data/raw`**.
3. **`CORR-0009` (residuo)** — `RES-0031`, `RES-0032`, `RES-0065`: mismo
   payload que la spec ya sellada, otros tres desenlaces.
4. **`CORR-0007` (residuo)** — `RES-0025`/`RES-0026` (evasión) no tienen nada;
   `RES-0039`…`RES-0042` tienen propuesta no firmada (`NC-0088`), que es
   decisión, no spec.

Y dos quedan condicionadas a algo que no es una decisión de alcance:
**`CORR-0008`** espera `NC-0156` (sin diseño muestral publicado, el punto es
especificable pero el IC de diseño no — congelar una spec hoy fijaría un
método de varianza que mesa no ha elegido) y **`CORR-0015`** espera a que su
corrida padre `CORR-0009` esté relevada entera, porque sus 7 `RESULT` son
complementos y particiones de ella.

---

## 5 · Reservas de este acto

- **Los cuatro medidores no se escriben aquí.** El encargo pide *«md humana +
  `spec.yaml`»*, que son las dos capas de `D-15`; el medidor es del acto de
  CAJA. Consecuencia declarada en cada `spec.yaml` y verificada arriba:
  `preflight` reporta `BLOQUEADO:script_ausente` en los cuatro. Es el estado
  correcto de una spec congelada sin corrida, no un defecto.
- **`cuenta_gen2 = PENDIENTE-DE-MESA` en los cuatro.** El encargo autoriza
  **congelar**, no contar; `FP-367`/`FP-368` piden OBJETO explícito sobre el
  contador y el encargo no lo trae. Se dice aquí en vez de darlo por concedido.
- **Ninguna de las cuatro specs es ciega**, y las cuatro lo declaran bajo
  `ADR-46` con lo que se había leído y lo que quedaba genuinamente desconocido.
  En dos casos (`CORR-0011` y `CORR-0014`) la contaminación es **inevitable
  por construcción**: leer `CALC-B-0001` y leer `tools/medidor_cuidado_enut.py`
  es lo que `A.8` obliga a hacer antes de escribir la spec, y es también lo que
  produjo los hallazgos de §2.1 y §2.3.
- **Ninguna cifra de `milpa/` se movió, ningún `CALC` sellado se tocó, ningún
  byte de microdato se abrió.**
