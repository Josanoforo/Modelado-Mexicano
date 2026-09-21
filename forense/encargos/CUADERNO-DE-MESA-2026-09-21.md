# CUADERNO DE MESA — 2026-09-21

Producido por `ACTO GEN2-CUADERNO-DE-MESA-1` (encargo archivado en
`forense/encargos/2026-09-21-GEN2-CUADERNO-DE-MESA-1.md`, sello de cuerpo
`654fc38c…`). Base de derivación: `fc13cdc` (`origin/main` al abrir; el encargo
declaraba `55c8d57c` — main se movió y todo se re-derivó contra la base real).
Entorno NUBE; nada aquí sale del espejo.

**Este cuaderno no firma, no cierra y no adopta nada.** Mesa lee, tacha lo que no
comparte, y su envío a un trámite es la firma.

**Forma de uso.** Cada renglón trae: *qué se decide* (una frase) · *por qué está
detenido* · *qué desbloquea* · *opciones* · *recomendación y su razón* ·
*texto de firma listo para copiar* · *a quién va después*. Los grupos van por lo
que desbloquean: **§2 destraba trabajo en curso**, **§6 puede esperar**.

---

## 0 · Cómo se armó el universo, y en qué no coincide con lo que dirección creía

El encargo (§3) estimaba «~50 FP sin cerrar», con un `awk` que declara sin validar.
**No se reproduce, y el número real es mucho menor.**

| Paso | Comando | Resultado |
|---|---|---|
| Filas FP reales | lector CSV con `delimiter='\t'` sobre `forense/firmas-pendientes.tsv` | **413** filas (no 415: el archivo tiene 415 líneas físicas porque hay campos citados con saltos de línea) |
| FP no cerradas | marcador **por prefijo** del campo `estado` (A.16) | **5** con prefijo `ABIERTA`/`PENDIENTE` |
| FP con `ABIERTA` escondida tras otro prefijo | `re.search(r'\bABIERTA\b')` sobre `estado` | **1** más (`FP-332`) |
| Filas NC reales | mismo lector sobre `forense/no-corrido.tsv` | **481** filas · **176** con prefijo `ABIERTA` |
| NC abiertas cuya razón o sucesor nombra a mesa | `re.search('mesa', re.I)` sobre `razon` y `sucesor` | **87** |
| NC abiertas con el token canónico | prefijo `DECISIÓN-` **o** `DECISION-DE-MESA-PENDIENTE` (las dos grafías, como pide §3) | **28** |
| Notas de cierre desde el 18/sep | 44 archivos listados por fecha; grep de «a mesa / decisión de mesa / MESA-DECIDE» | **25** con acierto |

**Por qué el `awk` de dirección no sirve aquí, y no es un detalle:** el TSV tiene
campos citados que contienen saltos de línea y tabuladores. `awk -F'\t'` parte por
línea física, así que ve filas que no existen y corta campos a media prosa. Dos
formulaciones dan **12** y **146**; ninguna da 50. El número no se hereda: se deriva
con un lector de CSV o no se deriva. *(A.4: el «~50» queda `NO-ENCONTRADO` como
mecanismo — busqué dos reconstrucciones del comando y ninguna lo produce.)*

**Universo de este cuaderno:** las **6** FP no cerradas + las **28** NC con token de
mesa + los pendientes que §3 del encargo manda incluir. Las **59** NC restantes de las
87 mencionan «mesa» en prosa (casi todas `FUERA-DE-PERÍMETRO` nombrando de quién es la
pieza) pero **no esperan una decisión de mesa**: se examinaron una por una y se
declaran fuera del cuaderno, no ignoradas.

---

## 1 · LO QUE YA NO NECESITA A MESA — nueve renglones que se pueden tachar hoy

Estos están marcados como pendientes de mesa y **ya no lo están**. No los cierro
(PARO (a) del encargo me lo veda): los entrego con la evidencia para que el trámite
sucesor los cierre de un golpe. Es el 32 % de las 28.

| Renglón | Por qué ya no espera a mesa | Evidencia (re-verificada hoy, A.17) |
|---|---|---|
| **NC-0185** ENVIPE: texto oficial de 7 identidades | **Mesa ya firmó el 15/sep.** La propia fila trae la enmienda que lo dice. | Expediente `07-INEGI-ENVIPE-NC-0185.md` existe (7 075 B) en `forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21/`. Falta que el titular lo presente — es ejecución, no decisión. |
| **NC-0237** MOCIBA 2021/2023 | **Reasignada a otra mesa** el 21/sep (firma B5, `GEN2-TRAMITE-FIRMAS-3`): mesa MOTOR, duelo prospectivo ENVIPE 2026. | Texto en el propio campo `sucesor`. |
| **NC-0344** tier partido de `familia.union.libre` | Su sucesora **FP-387 está FIRMADA** — y la firma contesta la pregunta. | `FP-387.firmada_en`: «4.3 opción (c) — FIRMA DE MESA 21/sep §2 4.3 *dos etiquetas de solidez (cifra / mecanismo) — c*». |
| **NC-0363** qué universo gobierna RES-0028 | **FP-391 FIRMADA** con texto operativo que resuelve exactamente el universo. | `FP-391.firmada_en`: «*Ok las dos firmas*. Se conserva el estimando sobre personas (U4). RES-0028 se aparea con el complemento sobre personas, no con el de delitos.» |
| **NC-0366** adjudicación de canal RES-0047/0049 | **FP-392 FIRMADA**, adopción por nombre de los 12 candidatos. | `FP-392.firmada_en`: «*Ok las dos firmas*… Se adoptan, por nombre: RES-0025, 0026, 0031… RES-0028 no se adopta: va por FP-391.» |
| **NC-0372** firma de contador sobre 12–13 corridas | **FP-394 FIRMADA** (4.5 opción a: ratificar #897 y #901). | `FP-394.firmada_en`, firma de mesa 21/sep §2 4.5. **Ojo:** la fila también condicionaba a NC-0369, que **sigue ABIERTA** — ver §2.1, ahí va el residuo real. |
| **NC-0434** K8 sin instrumento en ENIF 2021/2024 | **FP-404 FIRMADA**, opción (i) al pie de la letra. | `FP-404.firmada_en` (ADR-581): «K8 *destino del último crédito* sale de la serie ENIF… Opción (i): se triangula en ENSAFI 2023 / ENFIH 2019 en acto propio.» |
| **NC-0435** familia bancaria 2021↔2024 | **FP-404 FIRMADA**, opción (iii) para la serie. | Mismo `firmada_en`: «(2) K2 familia bancaria: opción (iii) para la serie». |
| **NC-…-5870-01** `test_piloto3_v13_conducto.py` saltado en CI | **FP-398 FIRMADA** (4.4 «librerías en CI — a»). No falta decisión: falta que se instalen. | `FP-398.estado = FIRMADA`; `firmada_en`: «ejecución: la lleva mesa en su trabajo de CI». |

**Texto de firma para las nueve, de un golpe:**

> «Doy por resueltas y mando cerrar, con la evidencia del cuaderno del 21/sep: NC-0185,
> NC-0237, NC-0344, NC-0363, NC-0366, NC-0372, NC-0434, NC-0435 y
> NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_3-5870-01. Ninguna espera decisión mía:
> cinco ya tienen su FP firmada, una la firmé el 15/sep, una pasó a otra mesa y dos
> esperan ejecución, no dictamen. El residuo de NC-0372 que sí sigue vivo (NC-0369)
> se trata por separado.»

**A quién va después:** un trámite de firmas, que marca las nueve `CERRADA` con cita
a este cuaderno. Nada que ejecutar salvo lo ya firmado.

---

## 2 · DESTRABA TRABAJO EN CURSO — decide esto primero

### 2.1 · El contador de corridas está detenido por una sola pregunta previa

**Qué se decide.** Si las doce corridas que ya reprodujeron pueden contar como GEN2,
sabiendo que la lista de corridas cambió a mitad del acto que las juntó.

**Por qué está detenido.** `NC-0372` pedía la firma de contador y su FP (FP-394) **ya
está firmada** — pero la fila condicionaba además a `NC-0369` («la composición del
universo de corridas cambió sin autorización a mitad del acto vía #897»), y **NC-0369
sigue ABIERTA**. Mientras no se resuelva, `N_corridas_selladas` no se mueve por ninguna
de las doce.

**Qué desbloquea.** Doce corridas selladas con replay `REPRODUCE` que hoy no cuentan:
`CALC-ENIGH2022-REMESAS-CONTEXTO-0001`, `CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001-v1_1`,
`CALC-ENUT2024-DISTRIBUCION-HORAS-0002`, `CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001`,
`CALC-WBES2023-PRECISION-0001`, `CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001`,
`CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001`, `CALC-ENCRIGE-CARGA-INTENSIDAD-0001`,
`CALC-ENVIPE-RES0028-U4-DERIVADO-0001`, `CALC-ISSP2017-CONSISTENCIA-APOYO-FAMILIAR-0001`,
`CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001`. Es la señal del §1 de las instrucciones:
un contador que no se mueve.

**Opciones.** (a) Ratificar el universo tal como quedó tras #897 y firmar las doce en
bloque. · (b) Firmar sólo las que no entraron por #897 y dejar el resto esperando un
dictamen de linaje. · (c) Rehacer el censo de corridas con el universo original y
firmar sobre él.

**Recomendación: (a).** Mesa ya ratificó los dos merges del carril codex el 21/sep
(FP-394, firma 4.5 opción a: «ratificar #897 y #901 — a»). Ratificar el merge y luego
negar el universo que el merge produjo sería firmar dos veces en sentidos opuestos;
(c) además rehace trabajo que la propia ratificación dio por bueno.

**Texto de firma:**
> «El universo de corridas tras #897 queda ratificado, en coherencia con FP-394 (4.5 a).
> Firmo `cuenta_gen2 = SI` en bloque para las once corridas SELLADA con replay
> REPRODUCE listadas en NC-0372. NC-0369 se cierra con esta misma ratificación.»

**A quién va después.** Un acto de recibo (`GEN2-RECIBO-CODEX-*`, que es la vía que ha
venido firmando `cuenta_gen2` por lote) escribe las filas en `decisiones.tsv`.

---

### 2.2 · El piso del piloto 3 no fue vencido: adoptarlo o vetarlo

**Qué se decide.** Si se adopta el piso C2 del cruce edad × escolaridad en «pagar la
luz por canal digital» (ENCIG 2025), que ningún retador venció.

**Por qué está detenido.** A-bis 6 dice que un piso no vencido **es** el estimador
adjudicado de su celda y se adopta salvo veto de mesa. El acto que lo midió no adopta
por diseño, así que la celda quedó en el aire. Tres filas lo esperan
(`NC-…-3619-01`, `-3619-02`, y `NC-0410`/`NC-0432` re-apuntadas ahí).

**Qué desbloquea.** `celdas_validadas` está parado en 73 → 73 aunque el tercer dominio
ya tiene **15 celdas con R e IC selladas**. El marcador tampoco refleja que el cruce
está consumido. Con la adopción, el marcador levanta la reserva **solo**, sin escribir
código nuevo.

**Opciones.** (a) **Adoptar** el piso C2 (`champion_actual: C2` + fila en
`decisiones.tsv`). · (b) Vetar y encargar a un acto de aparato un estado nuevo
`CONSUMIDA-POR-PILOTO` (>10 líneas en `tools/` y una decisión de vocabulario A.16).
· (c) Dejarlo `RESERVADA` como registro de que el cruce está gastado.

**Recomendación: (a).** Es lo que A-bis 6 ya manda sin necesidad de acto nuevo, es la
única de las tres que mueve un contador, y la herramienta existente la ejecuta sin
escribir una línea. (b) paga aparato para registrar una no-decisión; (c) deja 15 celdas
medidas invisibles.

**Lo que mesa debe tener presente al firmar** (de la propia nota del acto, verbatim):
el veredicto pre-registrado fue **FALSADOR DÉBIL** — cada retador gana sólo 3 de 15
celdas y en 12 el duelo es indecidible dentro del IC. Adoptar el piso **no** es
declarar que la interacción no existe: es adoptar el estimador que nadie venció.

**Texto de firma:**
> «Adopto el piso C2 de `tramite.gobierno_digital.util_sin_coercion_ejes_encig2025 ::
> edadxescolaridad` por A-bis 6 (piso no vencido, falsador débil). `champion_actual: C2`
> y fila de adopción en `decisiones.tsv`. No se crea el estado CONSUMIDA-POR-PILOTO.»

**A quién va después.** El acto que escriba la adopción; `marcador_segmento.py --escribe`
levanta la reserva sin cambio de herramienta.

---

### 2.3 · Tres lecturas de remesas atrapadas por un eje del replay

**Qué se decide.** Si la guarda que exige `REPRODUCE` puede leer **sólo el eje
RESULTADO** del replay, o si hay que re-sellar el CALC de origen.

**Por qué está detenido.** Las tres lecturas citan `RESULT-B-ENIGH-2022-P` (de
`CALC-B-0001`), cuyo replay vigente es `RÉPLICA-RESULTADO · CONTEXTO-DISTINTO`. La
guarda pide `REPRODUCE` a secas, así que las tres no se escriben. **E.3 dice que
RESULTADO y CONTEXTO no se colapsan** — y aquí la guarda los colapsa de hecho.

**Qué desbloquea.** `dependencias_numericas_legacy_activas` se queda en **149 en vez
de 146**. Tres lecturas M de FAM siguen contando como legacy aunque la conducta
`recibe_remesas` ya es GEN2 en `milpa/tramite.yaml:910`.

**Opciones.** (a) La guarda lee sólo el eje RESULTADO para la vía (ii). · (b) Re-sellar
`CALC-B-0001` (CALC nuevo; E.3 prohíbe reescribir el sellado). · (c) Dejarlas legacy.

**Recomendación: (a).** Es lo que E.3 ya dice: un `CONTEXTO-DISTINTO` **no** se degrada
a `NO-REPRODUCE`. La guarda está leyendo dos ejes como uno, que es exactamente el
defecto que E.3 existe para impedir. (b) cuesta una corrida entera para no cambiar
ninguna cifra.

**Texto de firma:**
> «Para la vía (ii) de 4.1, la guarda (a) lee el eje RESULTADO del replay, no el
> compuesto: `RÉPLICA-RESULTADO · CONTEXTO-DISTINTO` la satisface (E.3, los dos ejes no
> se colapsan). `CALC-B-0001` no se re-sella. Un acto sucesor escribe los tres pines.»

**A quién va después.** Acto sucesor de `GEN2-RELEVO-TANDA-3`.

---

### 2.4 · Un contador que baja: RES-0028 derivado

**Qué se decide.** Si `CALC-ENVIPE-RES0028-U4-DERIVADO-0001` cuenta como GEN2, y de
paso si un derivado determinista sobre un resultado sellado puede relevar.

**Por qué está detenido.** El encargo que lo produjo lo excluyó expresamente. Hoy la
guarda (d) rechaza el derivado **por ingerir otro resultado**, aunque ese resultado
esté sellado.

**Qué desbloquea.** RES-0028 sigue legacy; el contador baja a 148 por una lectura que
nadie pineó. El arreglo del blocker de #914 ya está hecho y disponible, esperando esto.

**Opciones.** (a) Firmar `cuenta_gen2 = SI` y declarar que un
`DERIVADO-DETERMINISTA-SOBRE-RESULTADO-SELLADO` sí releva. · (b) Firmar sólo el
contador y dejar la guarda (d) como está. · (c) Vetar.

**Recomendación: (a).** Con la salvedad de que la segunda mitad (la regla sobre
derivados) es una **regla general**, no un caso: conviene firmarla sabiendo que aplica
a todos los derivados futuros, no sólo a éste. Si mesa prefiere no comprometerse a la
regla hoy, **(b) es segura** y desbloquea el contador igual.

**Texto de firma (variante a):**
> «`cuenta_gen2 = SI` para `CALC-ENVIPE-RES0028-U4-DERIVADO-0001`. Además: un
> DERIVADO-DETERMINISTA-SOBRE-RESULTADO-SELLADO releva bajo 4.1; la guarda (d) se
> ajusta para no rechazarlo por ingerir un resultado ya sellado.»

**A quién va después.** Acto sucesor de `GEN2-RELEVO-TANDA-3`; si mesa toma (a), el
ajuste de la guarda (d) es acto de aparato aparte.

---

### 2.5 · Ocho corridas más sin puerta (la vía (i) no se relajó)

**Qué se decide.** Si el eje del replay se lee igual en la vía **(i)** que en las
vías (ii) y (iii).

**Por qué está detenido.** El acto que abrió el eje RESULTADO lo hizo sólo para (ii) y
(iii); relajar (i) era PARO de su encargo y no se intentó. Ocho corridas con
`cuenta_gen2=SI` y replay `RÉPLICA-RESULTADO · CONTEXTO-DISTINTO`
(`CALC-R-DIN-M-01`, `-FAM-M-01`, `-FAM-M-05`, `-FAM-M-06`, `-FAM-M-07`, `-TRA-M-02`,
`-TRA-M-03`, `-TRA-M-07`) más dos de ENCIG siguen sin puerta.

**Qué desbloquea.** Ninguna lectura extra sale de legacy hasta que esto se decida.

**Opciones.** (a) Misma lectura de eje para (i). · (b) Mantener (i) estricta y tratar
las ocho una por una. · (c) Dejarlo.

**Recomendación: (a), y en la misma sentada que 2.3.** Son la misma pregunta de regla
aplicada a otra vía; resolverlas por separado produce dos criterios distintos para el
mismo eje, que es cómo nacen las incoherencias que luego cuestan un acto de careo.

**Texto de firma:**
> «La lectura del eje RESULTADO del replay vale igual para la vía (i) que para (ii) y
> (iii). Un acto sucesor aplica el criterio a las ocho corridas listadas en
> `nota-2026-09-21-gen2-relevo-tanda-4-cierre.md` §3.»

**A quién va después.** Dirección lo lleva con la lista ya hecha.

---

## 3 · LOS DOS DICTÁMENES QUE ESTE CUADERNO TRAE RESUELTOS (FP-408 y FP-409)

El encargo pedía la **categoría** del defecto y su razón — no re-correr nada. No se
re-corrió nada. Los dos salen con evidencia dura, y **salen distintos**.

Rótulo de §5 de las instrucciones (anti-post-hoc): `DECLARADO` / `INFERIDO` /
`RETROSPECTIVO`.

### 3.1 · FP-409 · ENUT 2024 distribución de horas → **DECLARADO**

**La pregunta.** ¿La corrección de `CALC-ENUT2024-DISTRIBUCION-HORAS-0002` pudo
depender de haber visto el resultado de `-0001`?

**Respuesta: no pudo, porque no hay ninguna decisión de estimación en el cambio.**

*Orden (leído de las propias corridas, no de los commits — los dos llegaron a `main`
en un solo merge, `4dedab4`, así que el orden de commits **no es derivable** desde
`main`; el dato duro es el sello):*
- `-0001` corrió **2026-09-19T23:45:54Z**
- `-0002` corrió **2026-09-19T23:59:00Z** — 13 min 6 s después.

Sí: la sucesora corrió con el resultado de la predecesora ya sobre la mesa. Eso hace
la pregunta legítima. Lo que la contesta es el contenido del cambio:

*Diff normalizado.* Reescribiendo en `-0002` el `calc_id`, el prefijo de RESULT
(`ENUTDH2-` → `ENUTDH-`) y nada más, el medidor queda **byte-idéntico** salvo **tres
líneas**, y las tres son nombres de archivo de salida:

```
- distribution_path = out_dir / "distribucion.csv"
+ distribution_path = out_dir / "enut2024-distribucion-horas-estimaciones.csv"
- contrasts_path    = out_dir / "contrastes.csv"
+ contrasts_path    = out_dir / "enut2024-distribucion-horas-contrastes.csv"
- incidence_path    = out_dir / "incidencias.json"
+ incidence_path    = out_dir / "enut2024-distribucion-horas-incidencias.json"
```

*Resultados sellados.* De los 26 RESULT, **23 son idénticos** y los 3 que difieren son
**las tres rutas de archivo**. P50, P90, concentración del decil superior, brecha
mujer-hombre, masa válida, estratos, UPM, y los **sha256 de los propios CSV** coinciden
al byte.

**Dictamen recomendado: `DECLARADO`, sin reserva.** No cambió el estimando, ni el
universo, ni el filtro, ni el ponderador, ni un umbral. No hay decisión de estimación
que pudiera haberse elegido mirando el resultado, porque no se tomó ninguna. El
`sucesor_de` está declarado en el `spec.yaml`. La sucesión es un renombre.

**Texto de firma:**
> «FP-409: `DECLARADO`. La sucesión `CALC-ENUT2024-DISTRIBUCION-HORAS-0001 → -0002` es
> un renombre: medidor byte-idéntico salvo tres nombres de archivo de salida, 23 de 26
> RESULT idénticos y los 3 restantes son rutas. Ninguna decisión de estimación pudo
> contaminarse. Admisible sin reserva.»

### 3.2 · FP-408 · ENSAFI 2023 estrategias conjuntas → **INFERIDO**

**La pregunta.** Lo mismo para `CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001-v1_1`.

**Respuesta: pudo, en el sentido estricto — pero nada se movió hacia una respuesta
deseada, y eso es verificable.**

*Orden:* `-0001` corrió **2026-09-19T23:59:54Z**; `-v1_1` corrió
**2026-09-20T00:15:24Z** — 15 min 30 s después. Misma sesión, mismo corpus (419
archivos examinados en ambas firmas de entorno).

*Qué cambió de verdad.* Aquí sí hay cambio de código con contenido estadístico, no
cosmético:
1. La media del conteo se acota a `(0., 8.)` en vez de al `(0., 1.)` por omisión.
   **Es un defecto real:** la media es un conteo de 0 a 8 y vale **1.8446**; con la cota
   vieja su IC se habría recortado a 1. Pero `-0001` **nunca publicó EE ni IC de la
   media** (no están en su lista de RESULT), así que el defecto era **invisible en su
   salida** — sólo se ve al calcularlo.
2. Las condicionales `p(B|A)` pasan de una razón de masas sin error estándar a una
   razón de dominio con EE e IC propios.
3. Se añaden diagnósticos (singleton, peso inválido, diseño faltante) y un sha256 por
   archivo de salida.

*Lo que no cambió — y es lo decisivo.* Comparando las dos corridas selladas:
- De los 14 RESULT comunes, **11 son idénticos** y los 3 que difieren son rutas de
  archivo. La media del conteo es **1.844649266183 en las dos**. Cobertura, masa
  elegible, estratos (277), UPM (2 915), gl (2 638) y los tres controles
  (`COINCIDE`) no se movieron.
- En `parejas.csv`, las **84 estimaciones puntuales** (28 parejas × `p_ambas`,
  `p_b_dado_a`, `p_a_dado_b`) son **idénticas, 84 de 84**. El estimando de las
  condicionales no cambió: lo que se añadió fue su precisión.

*El defecto que sí hay que decirle a mesa.* La spec de `-0001` traía un campo
`contaminacion_declarada` con este texto:

> «Se conocían los ocho marginales del padre antes de congelar; no los cruces, conteos
> conjuntos, sensibilidad ni límites.»

La spec de `-v1_1` **eliminó ese campo**. Es decir: la versión que sí tenía algo que
declarar sobre contaminación es la que dejó de declararlo. No hay pre-declaración de
que la sucesora vendría ni de qué corregiría.

**Dictamen recomendado: `INFERIDO`, admisible con una nota, no con reserva.**
- No es `DECLARADO`: no hubo declaración previa, y la sucesora borró el campo donde
  habría ido.
- No es `RETROSPECTIVO`: ninguna cifra compartida se movió, ningún universo, filtro,
  ponderador o umbral cambió, y los 84 puntos de las parejas son idénticos. No se
  ajustó nada hacia un resultado.
- Es `INFERIDO`: las correcciones son de una clase cuya necesidad se nota al mirar los
  números (un IC de una media 0–8 recortado a 1 se ve cuando lo calculas), sin
  declaración previa que lo cubra.

**Texto de firma:**
> «FP-408: `INFERIDO`. La sucesión es aditiva —EE/IC para la media, EE/IC para las
> condicionales, diagnósticos y sha256— y verificablemente no movió nada: 11 de 14
> RESULT comunes idénticos (los 3 restantes son rutas), media 1.844649266183 en ambas,
> y 84 de 84 estimaciones puntuales de `parejas.csv` idénticas. Admisible sin reserva
> de evaluación, **con nota**: `-v1_1` eliminó el campo `contaminacion_declarada` que
> `-0001` sí traía. Regla que dejo escrita: una sucesora no borra el campo de
> contaminación de su predecesora; lo hereda y lo amplía.»

**A quién va después.** Trámite de firmas; la regla del último renglón, si mesa la
adopta, es enmienda a §6 de las instrucciones (dos commits para actos que estiman).

---

## 4 · ALCANCE Y TERRITORIO

### 4.1 · FP-405 · ¿la adquisición sigue asignada a UBUNTU?

**Qué se decide.** Acotar `FP-67` a su universo medido: la nube **con red denegada**
(`cloud_default`), no la nube en general.

**Por qué está detenido.** `FP-67` (cerrada el 19/ago) asignó la adquisición a UBUNTU
porque la nube tenía bloqueado el egreso a INEGI. **Los dos lados están ahora medidos**,
por dos sesiones distintas:
- `cloud_default` **confirma** FP-67: red `DENEGADA-POR-POLITICA` (`http_code=000`,
  `http_connect=403`) y el descargador `NO-OBTENIDO` con «Tunnel connection failed: 403».
  *(Esta sesión lo vuelve a medir hoy, con el mismo resultado — ver §7.)*
- nube con red **Custom** (`milpa-inegi`) **vence FP-67 en alcance**: red `PERMITIDA`
  (200/200), descarga de `enif_2024_bd_csv` (3 131 148 B) con sha256 verificado, y
  `corrida0.py verify CALC-ENIF-0001` → `REPRODUCE` con `CONTEXTO=DISTINTO`.

**Qué desbloquea.** Mientras mesa no firme, **toda** la adquisición sigue asignada a
UBUNTU por FP-67 en su forma actual, aunque el carril de nube ya esté demostrado.

**Opciones.** (a) Acotar FP-67 a `cloud_default` y declarar la nube-Custom territorio
nuevo, no cubierto por FP-67. · (b) Esperar a `NUBE-PILOTO-2` (37 ids, 381.6 MB, un
host). · (c) No acotar.

**Recomendación: (a).** Es lo que A.10 manda: un sello cuyo universo creció queda
`VENCIDO EN ALCANCE`, no refutado ni borrado, y se reactiva por re-sello, nunca
editando el viejo. `FP-67` no se toca. Acotar **no** es sustituir: la adquisición no se
muda a la nube con esta firma.

**Lo que mesa pidió que fuera verbatim, y va:**
> *un `REPRODUCE` sobre un payload de 3.1 MB en un host no demuestra que 18.4 GB en 200
> hosts funcionen. El piloto prueba que el carril existe, nada más.*

**Texto de firma:**
> «FP-405: acoto FP-67 a `cloud_default` (A.10, VENCIDA EN ALCANCE para nube con red
> Custom; la fila FP-67 no se edita). Firmo el **alcance**, no la sustitución: la
> adquisición sigue asignada a UBUNTU hasta que NUBE-PILOTO-2 mida escala.»

**A quién va después.** `NUBE-PILOTO-2` como sucesor declarado.

---

### 4.2 · FP-374 — no se firma: se re-sella

**Este renglón no es una firma y conviene no tratarlo como tal.** `FP-374` está
**`VENCIDA-EN-ALCANCE`**, no `ABIERTA` (re-verificado hoy por estado, A.17). Por A.10
una vencida en alcance **no se firma ni se edita: se reactiva por re-sello**. Bloquea
cuatro filas que hoy no tienen a quién esperar, entre ellas `NC-0161` y la cadena de
`NC-0237`.

**Recomendación.** Encargar un acto de re-sello de FP-374 con su universo actual. Es el
único renglón del cuaderno que pide una acción de forma distinta a todos los demás, y
por eso se pierde: cada trámite lo lee como «pendiente de firma» y lo vuelve a poner en
la cola.

**Texto de firma:**
> «FP-374 no se firma. Encargo un acto de re-sello con su universo actual (A.10). Las
> filas que la citan como bloqueador (NC-0161 y la cadena de NC-0237) se re-verifican
> contra el sello nuevo, no contra el viejo.»

---

## 5 · VOCABULARIO Y REGLAS DEL APARATO

Cuatro renglones que no mueven ningún contador hoy pero que **cada acto vuelve a
tropezar**. Son baratos de decidir y caros de no decidir.

### 5.1 · Falta un estado: `SIN-PISO-POR-DISEÑO` (NC-0377 y NC-0411)

**Qué se decide.** Si el vocabulario de las tablas de identidad admite un estado que
distinga «nadie midió el piso» de «el diseño de la encuesta no admite piso».

**Por qué está detenido.** Las 4 celdas de `familia.union.libre_ejes_eder2017 ×
cohorte_nacimiento` **ya tienen dictamen**: EDER 2011 muestrea tres cohortes de tres
años; dos de las cuatro celdas no tienen ninguna. El dictamen existe y no se puede
escribir, porque el estado no existe en el vocabulario e inventarlo exige escribir una
tabla.

**Qué desbloquea.** 4 de 15 filas `SIN-PISO` que hoy mienten por omisión: `sin_piso` no
distingue ausencia de fuente de ausencia de sentido.

**Recomendación: adoptar el estado.** Es una palabra en un vocabulario, y la alternativa
es que un dictamen ya pagado siga sin poder asentarse. Que un contador llame igual a
«no lo medimos» y a «no tiene sentido medirlo» es exactamente el tipo de colapso que §2
de las instrucciones prohíbe («tres hallazgos que nunca se colapsan»).

**Texto de firma:**
> «Adopto `SIN-PISO-POR-DISEÑO` en el vocabulario `status` de las tablas de identidad.
> Un acto escribe la tabla EDER de 4 filas con el dictamen de #908 §2.2 como
> `metadata_source`. Resuelve NC-0377 y NC-0411.»

### 5.2 · La edición de tres sitios en el marcador (NC-0378)

**Qué se decide.** Aceptar o revertir una edición de +23/−10 líneas en tres sitios
(constante, bucle, entrada de `MAPA_CONSUMER`) que era necesaria porque
`MAPA_CONSUMER` es un dict sin *fallback*.

**Recomendación: aceptar.** `tests/test_marcador_segmento.py` pasa (10 casos) y el
diff del derivado son exactamente las 11 filas ENUT esperadas. Revertir devuelve 11
celdas a `SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD` sin ganar nada. Es la clase de renglón
que se decide al fusionar el PR.

**Texto de firma:** «Acepto la edición de tres sitios de NC-0378. Queda como está.»

### 5.3 · Las dos filas de `canales_observados` (NC-…-5573-02)

**Qué se decide.** Si el «criterio 2» de un encargo se lee literal o por sustancia.

**Situación.** Dos filas cambian **sólo** en la columna informativa
`canales_observados`. Veredicto, `calc_candidato` y pin quedan **idénticos**; medido:
**0 veredictos cambian en las 211 filas**.

**Recomendación: aceptar que `canales_observados` es informativo** y el criterio 2 está
cumplido. Revisar un acto entero porque una columna que no adjudica se repartió distinto
es el aparato cobrándose más de lo que protege (§1: *el aparato tiene costo*).

**Texto de firma:** «`canales_observados` es informativa y no forma parte del criterio 2.
El acto no se revisa.»

### 5.4 · La sesión que congeló no fue la de #944 (NC-…-5870-03)

**Qué se decide.** Si «una sola sesión» (D-17) se refería a **esa** sesión o a que no
hubiera dos.

**Situación.** F3 se cumple igual: quien congeló no ejecutó, no corrió el medidor sobre
2025, no abrió la ola. La salida no depende de qué sesión tecleó.

**Recomendación: aceptar.** D-17 existe para impedir dos escritores sobre el mismo
rótulo, no para nombrar una sesión concreta. Impacto declarado: ninguno.

**Texto de firma:** «La sesión que congeló es válida. D-17 se cumple: un solo escritor.»

---

## 6 · PUEDE ESPERAR — y lo digo así

Estos renglones están abiertos, verificados, y **ninguno bloquea trabajo en curso**.
Mesa puede pasarlos sin costo hoy.

| Renglón | Qué es | Por qué puede esperar |
|---|---|---|
| **NC-0445** `test_motor_gen2_explicito.py` | 4 fallas de dos causas nuevas: (1) el `p` de `milpa/tramite.yaml` es 0.2215 y el RESULT sellado es 0.22148146779116093 — con tolerancia 5e-07 el motor emite `NO_COVERAGE`; (2) `tramite.evasion_norma` no tiene `ola_calibracion` propia | **La guardia está funcionando bien**: detecta que un `p` materializado no identifica a su RESULT. Arreglarlo es mover una cifra de `milpa/tramite.yaml`, que ningún acto tiene autorizado. Ver §6.1. |
| **NC-0446** `test_consulta_gen2.py` | 4 fallas por respuestas de ejemplo congeladas cuando el índice era incargable | Re-sellar artefactos congelados de otro acto. Necesita dueño, no decisión. |
| **NC-…-e8fa-02** `test_c_roles_sellados…` FAIL | Fallo **anterior** a PR #883, ajeno al diff que lo reporta (verificado: `git log` sobre `matriz.py`/`motor.py`/`celdas.py` no muestra commit de ese acto) | Ningún contador de adopción se mueve por esto. La compuerta se apoyó en 5/6 y se declaró. |
| **NC-…-6e60-08** diferencia de 2 en el conteo de FP | **Error de derivación de dirección**, así asentado por el propio encargo: una premisa rotulada `EJECUTADO` que no lo era (389 declaradas contra 387 reales) | No hay nada que conciliar en el árbol. La fila se conserva como registro del error, no como trabajo. Va a bandeja de dirección, no a mesa. |
| **NC-…-2707-01** sonda de `gh` sobre protección de `main` | La sesión NUBE no tiene `gh` con credenciales | Sólo deja sin responder cuánto de la meta de re-fusiones depende de esa política. Lo contesta mesa en una línea, o cualquier sesión con `gh`. |
| **NC-0425** los 9 puntos L con diferencia | Legacy reproduce la **media** exacta de las réplicas; GEN2 coincide con la **mediana** en 1 de 9, porque re-extrae de las 224 capturas. **Son dos estimandos distintos, no una medición con otro número** | Diferido a `RELEVO-TANDA-3`. Ver §6.2: hay una pregunta de fondo aquí que conviene no resolver con prisa. |
| **NC-…-7bf5-03** qué agregador gobierna L | La misma pregunta que NC-0425, en su forma general | El relevo de L exige después un CALC propio que mida desde las capturas; `CALC-TRIADA-0001` ingiere y la guarda (d) lo rechaza. Depende de 2.4. |

### 6.1 · Por qué NC-0445 no es sólo un test rojo

Vale la pena que mesa lo vea, aunque pueda esperar: el test falla porque
`share_horas_mujeres_40mas` vale **0.2215** en `milpa/tramite.yaml` y su RESULT sellado
vale **0.22148146779116093**. La firma **F8 del 21/sep** ya dijo qué hacer con eso —
verbatim: *«El redondeo de `share_horas_mujeres_40mas` no se edita a mano: queda NC y se
mueve por el canal de relevo.»* **La decisión está tomada; lo que falta es un dueño.**
Hoy `RES-0045` está en `relevo-usos-v1_0.tsv` como `LISTADO-PARA-MESA-REPRODUCE` con la
nota «adopción no auditable desde la oferta». Recomendación: asignar dueño en el
próximo lote de relevo, no volver a preguntarlo a mesa.

### 6.2 · Por qué NC-0425 merece más de un renglón

Es el único del cuaderno donde la diferencia **no es de procedimiento sino de
estimando**. A-bis 3 y 4 prohíben aparear cifras sin enlace declarado, y aquí los 21
casos que «casaron» lo hicieron **por clave de consumidor, no por identidad de celda**.
Un acierto de clave no es un estimando casado. Recomendación: **no** resolverlo en la
misma sentada que los demás; merece su propio acto, con la pregunta planteada como «qué
agregador gobierna L» (§6, NC-…-7bf5-03) y no como «por qué difieren 9 números».

---

## 7 · RENGLONES SIN ASIENTO — dirección los conoce, el repo no

El encargo (§3, `[LEÍDO]`) manda incluir cinco pendientes. **Dos tienen asiento; tres
no lo tienen**, y eso es un hallazgo, no un descuido de este acto.

**Universo examinado (A.13):** 2 779 archivos `*.md`, `*.tsv`, `*.yaml` fuera de `.git`,
con `grep -rn` por frase literal y variantes.

| Pendiente de §3 | Asiento en el repo | Veredicto A.4 |
|---|---|---|
| Redondeo de `share_horas_mujeres_40mas` (F8) | **Sí**: `FP-…-8a1f-08` FIRMADA + `RES-0045` en `relevo-usos-v1_0.tsv` | `EXISTE-SATISFACE` — ver §6.1; falta dueño, no decisión |
| `motor.py:20` y `:129` citan BARRIDO-2 | **Sí**: `NC-260921-MOTOR-THETA-CONGELADA-1-e8fa-01`, ABIERTA | `EXISTE-SATISFACE` — ver abajo |
| «Una corrida puede contar sólo por la etiqueta de su propia spec» | **No** | `NO-ENCONTRADO` (0 archivos con acierto sobre 2 779) |
| Respaldo del corpus: 18.4 GB en una sola máquina | **No, como pendiente.** Los únicos aciertos de «18.4 GB» son la frase verbatim del piloto de nube («no demuestra que 18.4 GB en 200 hosts funcionen»), que es sobre **escala del carril**, no sobre respaldo. «Una sola máquina» aparece 2 veces, las dos sobre rutas absolutas en `MAESTRA37-INFRA`, no sobre respaldo | `NO-ENCONTRADO` |
| ¿Toda ola nueva que entra al corpus nace reservada? | **No** | `NO-ENCONTRADO` (0 archivos con acierto) |

**Recomendación.** Las tres sin asiento son **preguntas de regla**, no de caso: las tres
gobernarían actos futuros, y hoy viven sólo en la cabeza de dirección. Que no tengan
fila es el defecto que A.12 existe para atrapar («el tablero de firmas se deriva, no se
recuerda»). **No abro filas FP por ellas** — §10 del encargo dice que este acto no
tramita. Quedan asentadas en mi `## NO-CORRIDO` con sucesor nombrado.

Las tres, planteadas para que mesa pueda contestarlas aquí mismo:

1. **«Una corrida puede contar sólo por la etiqueta de su propia spec.»**
   ¿Sí o no? Si sí, la etiqueta `cuenta_gen2` de la spec basta y las firmas de contador
   por lote sobran. Si no, cada corrida necesita firma aunque su spec ya lo declare.
   *Recomendación: **no**, y por la razón de E.2 — «la adopción es por merge de mesa, y
   por bloque». Una spec que se auto-adjudica el contador es el ejecutor concediéndose
   la firma. Pero decirlo explícitamente ahorra la pregunta en cada acto.*

2. **Respaldo del corpus: 18.4 GB en una sola máquina.**
   *Recomendación: es riesgo de operación, no decisión de medición. Va a bandeja de
   dirección con una fila propia, no a este cuaderno. Lo que sí es de mesa: si el
   respaldo se considera parte del universo de un sello (A.10), perderlo vencería
   sellos en alcance.*

3. **¿Toda ola nueva que entra al corpus nace reservada?**
   *Recomendación: **sí**, por defecto, y se levanta la reserva por acto explícito. E.6
   dice que una reserva se declara **antes** de derivarla; si la ola nace abierta, la
   declaración llega siempre tarde. El costo de la regla es un acto de levantamiento por
   ola; el costo de no tenerla es una reserva rota que ya no se puede reconstruir.*

**Sobre `motor.py:20` y `:129`** (sí tiene asiento, y conviene leerlo bien): las dos
líneas citan `BARRIDO-2` donde hoy correspondería `ADR-531`. **Tocarlas mueve el contexto
de replay de dos sellos**, que es justamente por qué ningún acto las ha tocado. Las
líneas son prosa explicativa, no lógica:

- `:20` — «La ley de mesa vigente lo prohíbe en E0 y toda calibración E1+ espera el
  cierre de BARRIDO-2.»
- `:129` — el mismo texto dentro de un mensaje de error.

*Recomendación: corregirlas en el mismo acto que ya vaya a re-sellar por otra razón,
nunca en un acto propio. Pagar dos sellos de replay por dos líneas de prosa es
exactamente lo que §1 llama auditoría de la auditoría.*

---

## 8 · LO QUE NO SE PUDO RECOMENDAR SIN UN DATO QUE NO ESTÁ EN EL REPO

El encargo (§6) pide decirlo y decir cuál dato. Dos renglones:

1. **NC-…-2707-01 (sonda de `gh` sobre protección de `main`).** Falta: la salida de
   `gh api repos/.../branches/main/protection`. Esta sesión NUBE no tiene `gh` con
   credenciales — verificado: `tools/limpia_arbol.py --reporta` sale
   `NO-VERIFICABLE-SIN-GH` en su punto D. Sin ese dato no se puede estimar cuánto baja
   la meta de re-fusiones, y por tanto no se puede recomendar entre «cambiar la política»
   y «dejarla».

2. **NC-0369 (composición del universo de corridas).** Recomendé (a) en §2.1 **por
   coherencia con una firma ya dada** (FP-394 / 4.5 a), no por haber auditado los 16
   commits de `codex/gen2-enadid2023-union-sexo-edad-cli-2` uno por uno. Si mesa quiere
   la recomendación apoyada en esa auditoría y no en la coherencia, hace falta un acto
   que la corra; lo digo para que la firma se dé sabiendo sobre qué se apoya.

---

## 9 · PROCEDENCIA DE ESTE CUADERNO

- **Base:** `fc13cdc`, `origin/main` al abrir. El encargo declaraba `55c8d57c`; main se
  movió y todo se re-derivó (§2 de las instrucciones: no es PARO, es refrescar).
- **Entorno (A.2, tres partes, salida cruda del arranque):**
  `ENTORNO-DERIVADO = NUBE` · `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` ·
  `red: DENEGADA-POR-POLITICA (http_code=000, http_connect=403, x_deny_reason=ausente,
  via_proxy=SI)` · `senal-corpus: montado=NO archivos_examinados=0`.
  *(Esa medición de red es, incidentalmente, una tercera confirmación independiente del
  lado (a) de FP-405 — §4.1.)*
- **Lecturas:** todas de tipo (1) — leídas del repo en esta sesión, con commit citable.
  Ninguna cifra sale del espejo. Ninguna cifra esperada se tecleó: las de §3 se derivaron
  comparando los JSON y CSV sellados en esta sesión.
- **Qué cubría ya el digesto:** `tools/digesto_tramite.py --mesa` se corrió **primero**,
  como manda el encargo. Cubre el inventario (415 FP / 481 NC examinadas, 180 decisiones
  vivas, edad y vencimiento por fila) y lo hace bien. **No cubre** lo que este cuaderno
  añade: su universo NC es el de las 176 abiertas, no el de las que esperan a mesa; no
  re-verifica el estado de los sucesores (que es lo que produjo las nueve de §1); no
  dictamina; y no recomienda. El digesto es el censo; esto es el dictamen.
- **Lo que no se hizo, y no se disimula:** no se re-corrió ningún CALC (PARO (c)); no se
  marcó ninguna fila `FIRMADA` ni se cerró ninguna NC (PARO (a)); no se recomendó sobre
  ningún renglón cuyo estado no se re-verificara hoy (PARO (b)) — los renglones de §6
  llevan estado re-verificado aunque la recomendación sea «puede esperar».

---

## 10 · RESUMEN EN UNA PÁGINA

| # | Qué decide mesa | Mueve un contador hoy | Recomendación |
|---|---|---|---|
| §1 | Cerrar nueve renglones ya resueltos | No, pero limpia 32 % de la cola | Cerrar las nueve de un golpe |
| §2.1 | Universo de corridas tras #897 | **Sí** — 11 corridas | (a) ratificar y firmar en bloque |
| §2.2 | Adoptar el piso C2 no vencido | **Sí** — 15 celdas | (a) adoptar (A-bis 6 ya lo manda) |
| §2.3 | Eje del replay en la vía (ii) | **Sí** — 149→146 | (a) leer sólo RESULTADO (E.3) |
| §2.4 | `cuenta_gen2` de RES-0028 derivado | **Sí** | (a), o (b) si no se quiere la regla general |
| §2.5 | Eje del replay en la vía (i) | **Sí** — 8 corridas | (a), en la misma sentada que §2.3 |
| §3.1 | Dictamen FP-409 | No | `DECLARADO`, sin reserva |
| §3.2 | Dictamen FP-408 | No | `INFERIDO`, admisible con nota |
| §4.1 | FP-405, acotar FP-67 | No | (a) acotar; no sustituye la asignación |
| §4.2 | FP-374 | No | **No se firma: se re-sella** |
| §5.1 | Estado `SIN-PISO-POR-DISEÑO` | No | Adoptarlo |
| §5.2 | Edición de tres sitios | No | Aceptar |
| §5.3 | `canales_observados` | No | Informativa; el acto no se revisa |
| §5.4 | Sesión que congeló | No | Aceptar |
| §7 | Tres preguntas de regla sin asiento | No | Contestarlas aquí; abrir sus filas |
| §6 | Siete renglones | No | Pueden esperar, dicho así |

**Diecisiete grupos de decisión. Cinco mueven contadores hoy. Nueve renglones se
pueden tachar sin decidir nada.**

**Falsador de este cuaderno, a tres meses** (§10 del encargo): si mesa no resuelve al
menos la mitad de los renglones con el cuaderno en la mano, el formato no sirve y se
anota. La mitad son **ocho** de los diecisiete grupos.
