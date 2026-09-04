# S3 · Pre-registro de `MAESTRA38-C1 · RE-ASIENTO` — congelado antes de que caja escriba `relaciones.tsv`

### `prereg-caja-S3-C1` · **v1.0** · 4 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S3-C1-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S3-C1`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La spec congelada del futuro re-asiento de relaciones bajo `N36`: cuántas y cuáles tienen `N`-destino adjudicado, la entrada ya llenada para `alta_relacion.py` con su `relacion_id` esperado (computado y verificado por control), y el estado de las 4 filas `ENFIH` pendientes. |
> | **QUÉ NO ES** | No es un alta — no corre `alta_relacion.py`. No escribe `relaciones.tsv`/`evidencias.tsv`/`utilidad-modelo.tsv`. No resuelve `FP-288`. |
> | **VERIFICAS ASÍ** | Caja, al correr `alta_relacion.py` con la entrada de §3, compara el `relacion_id` que el script produzca contra el esperado aquí; cualquier discrepancia se declara antes de aceptar el alta. |

**Acto:** `ACTO MAESTRA38-N3 · PRE-REGISTRO-DE-CAJA`, 4/sep/2026, entorno **NUBE**, sobre `origin/main = 0ff3d7106793e7352df92bd658e3e25293a025db`.

---

## 0 · Discrepancia crítica entre el encargo y el registro — declarada antes de fijar nada

El encargo (`forense/encargos/2026-09-04-MAESTRA38-N3-PRE-REGISTRO-DE-CAJA.md:9`) pide: *"las 7 relaciones bajo N36 con su N destino (adjudicación de L3-BIS, verbatim)."*

**Verificado contra el registro real: L3-BIS no adjudica destino a 7 — adjudica destino a exactamente 1 de 8.** `forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:213-234`, tabla "Adjudicación regla ↔ componente", verbatim:

> | componente dado de alta por A1 | regla a la que sirve | por qué |
> |---|---|---|
> | **etiquetado** | **R4.5** `salud.consumo.sellos_precio_similar` | es el único componente que toca el desenlace de la regla |
> | actividad física / antropometría / frecuencias / rec24h / lactancia / plomo / sangre (7 componentes) | **ninguna** de R4.1–R4.5 | ... |
>
> **"1 de 8 altas tiene regla (etiquetado→R4.5); 7 de 8 no la tienen y su `clasificacion_relacion = CANDIDATA` es correcta y se queda."**

Es decir: **las 7 relaciones no-etiquetado no se mueven — L3-BIS dice explícitamente que se quedan bajo `N36`.** Ningún documento del registro (`necesidad-objeto-modelo.tsv`, `relaciones.tsv`, la tabla de adjudicación citada arriba) da un `N`-destino distinto a esas 7. `necesidad-objeto-modelo.tsv:43-45` (`N38`/`N39`/`N40`, para `R4.1`/`R4.2`/`R4.4`) no cita ningún `relacion_id` de las 7 restantes.

**Este pre-registro fija la premisa corregida, no la del encargo:** el re-asiento de `C1` es **una** alta (etiquetado → `N41`), no siete. Las 7 restantes quedan documentadas en §4 como "no se tocan, y por qué" — declarar la corrección es, en sí, parte del entregable de un pre-registro (A.8: verificar qué ya existe antes de fijar el encargo).

---

## 1 · Universo — las 11 filas `N36`

`data/curacion-registro/relaciones.tsv`, `awk -F'\t' '$2=="N36"'` → **11 filas** (no 7, no 8):

| relacion_id | fuente | objeto | origen |
|---|---|---|---|
| `REL-ff6da3b0a22322433d42b4eb` | `CERO_DESABASTO` | `OE-9ccc0aa9606acf5881179a4e` | pre-A1, objeto de evidencia original de `N36`/`R4.3` — **fuera de alcance de C1** |
| `REL-78d3eaddcfc8a517125b409d` | `DGIS_URGENCIAS_CUBO_IMSS_INEGI` | `OE-7438fff65fa626a4e19b3e22` | pre-A1 — **fuera de alcance** |
| `REL-52ba7751632b1b331b5758d0` | `DGIS_URGENCIAS_CUBO_IMSS_INEGI` | `OE-e89c229b5ee0267e65454546` | pre-A1 — **fuera de alcance** |
| `REL-54b26887b70cada846e1207c` | `ENSANUT_CONTINUA_2024` | `OE-591e527de7590585cde47973` | A1 §5.1, **etiquetado** — **el único que se re-asienta, §3** |
| `REL-9e0e8f3c127ec9d3a7870a89` | `ENSANUT_CONTINUA_2024` | `OE-417c0f58aa8ae56c2b91195d` | A1 §5.1, actividad física — no se mueve, §4 |
| `REL-1f78b8310506dc8b3f7c7a4e` | `ENSANUT_CONTINUA_2024` | `OE-ad980f70b39472375185468f` | A1 §5.1, antropometría — no se mueve, §4 |
| `REL-f383264aea4a5444c88c269d` | `ENSANUT_CONTINUA_2024` | `OE-ae81722b77479548c30b1391` | A1 §5.1, frecuencias — no se mueve, §4 |
| `REL-64fabef42ccca1d9acdad65d` | `ENSANUT_CONTINUA_2024` | `OE-9849dbefa7eede5e2df4f85b` | A1 §5.1, rec24h — no se mueve, §4 |
| `REL-866ae722e828dddcf074c9b1` | `ENSANUT_CONTINUA_2024` | `OE-d8ab69706e13f926bf4f94d9` | A1 §5.1, lactancia — no se mueve, §4 |
| `REL-4df6299b7ddef985518f256b` | `ENSANUT_CONTINUA_2024` | `OE-09547bdada3c01d6d862537e` | A1 §5.1, plomo — no se mueve, §4 |
| `REL-cb194034d433bf9347a2de41` | `ENSANUT_CONTINUA_2024` | `OE-f65c9a690bddd8ee941ae8e5` | A1 §5.1, sangre/micronutrimentos — no se mueve, §4 |

---

## 2 · Lo que `alta_relacion.py` puede y no puede hacer — verificado con `--help` y lectura completa del script

Verificado en esta sesión (`python3 tools/curador_registro/alta_relacion.py --help`):

- El script **da de alta relaciones nuevas**, en las tres tablas acopladas (`relaciones.tsv`, `evidencias.tsv`, `utilidad-modelo.tsv`) más recifrado de `baseline.json` — invocación: `python3 tools/curador_registro/alta_relacion.py <entrada.yaml> --registro data/curacion-registro [--dry-run]`.
- **No mueve ni edita una fila existente.** Docstring verbatim: *"este módulo NUNCA reserializa una fila que ya existe... conserva cada línea existente byte a byte, y solo AÑADE una línea nueva al final."*
- **No asigna una `N` nueva** — la necesidad debe existir ya en `necesidad-objeto-modelo.tsv`.
- **No fusiona ni permite alta duplicada** — si `(necesidad_id, fuente, objeto)` ya produce un `relacion_id` existente, para siempre.

**Consecuencia para el "re-asiento":** con este script, re-asentar `etiquetado` de `N36` a `N41` **no es un UPDATE** de `REL-54b26887b70cada846e1207c` — es un **ALTA nueva** bajo `N41` (que produce un `relacion_id` distinto, §3), y la fila vieja bajo `N36` **queda intacta, huérfana**, salvo que un paso aparte (§4) la anote.

---

## 3 · La única alta pre-registrada — entrada ya llenada, `relacion_id` esperado verificado por control

**Derivación determinista** (`tools/curador_registro/baseline.py:48-50`): `relacion_id = "REL-" + sha256("\x1f".join((necesidad_id, fuente, objeto)))[:24]`.

**Verificación de control, corrida en esta sesión:** aplicando la fórmula a `(N36, ENSANUT_CONTINUA_2024, OE-591e527de7590585cde47973)` se reproduce exactamente `REL-54b26887b70cada846e1207c` (la fila real, línea 213) — la fórmula está confirmada contra el dato real, no sólo copiada del código.

**`relacion_id` esperado para el re-asiento** — `(N41, ENSANUT_CONTINUA_2024, OE-591e527de7590585cde47973)`:

```
REL-e7c3700e98be2d9aa7bbd55e
```

**Entrada YAML ya llenada para `tools/curador_registro/alta_relacion.py`**, construida copiando los valores reales de la fila `N36` (`relaciones.tsv:213`, `evidencias.tsv:214`, `utilidad-modelo.tsv` fila `REL-54b26887b70cada846e1207c`) donde el contenido no cambia con el re-asiento, y fijando lo que sí cambia (`necesidad_id`, `procedencia_nota`, referencias a `N41`/`R4.5`):

```yaml
necesidad_id: N41
fuente_canonica_normalizada: ENSANUT_CONTINUA_2024
objeto_evidencia_id_canonico: OE-591e527de7590585cde47973
procedencia_nota: >
  Re-asiento pre-registrado por prereg-caja-S3-C1 (ACTO MAESTRA38-N3, 4/sep/2026):
  adjudicación de MAESTRA37-L3-BIS (forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md,
  tabla "Adjudicación regla <-> componente") asigna el componente de etiquetado de
  ENSANUT Continua 2024 a R4.5/N41. Mismo payload, misma fuente, mismo objeto que
  REL-54b26887b70cada846e1207c (N36) -- el alta bajo N41 es una fila NUEVA, no una
  edición de esa fila (alta_relacion.py no reescribe filas existentes; ver S3-C1 §2/§4).
relacion:
  fuente_nombre: "Encuesta Nacional de Salud y Nutricion Continua 2024 (INSP), version publicada 2026-09-01"
  tipo_fuente: FUENTE_DATOS
  id_manifiesto: "etiquetado_ensanut2924_w_cat_logo__v2026_09_01;etiquetado_ensanut2924_w_csv_csv__v2026_09_01;etiquetado_ensanut2924_w_cuestionarios__v2026_09_01;etiquetado_ensanut2924_w_stata_stata__v2026_09_01"
  sha256_fuente: "NO_APLICA (el componente son 4 payloads; el sha256 de cada uno vive en su entrada del manifiesto)"
  capa1_universo_indexado: "SI"
  capa2_manifiesto: "SI"
  capa3_disco_real: "EXISTE;COINCIDE;INTEGRO"
  capa4_apertura_mapeo: NO_DETERMINADO
  clasificacion_relacion: CANDIDATA
  reason_code: APERTURA_INDETERMINADA
  evidencia_ref: "MAIN:forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md"
  evidencia_textual_breve: NO_DETERMINADO
  confianza: MEDIA
  conflicto_material: "NO"
  nota: >
    Re-asentado bajo N41/R4.5 por adjudicacion de MAESTRA37-L3-BIS (etiquetado -> unico
    componente de las 8 altas de A1 que sirve a una regla de salud). Payload identico al
    de REL-54b26887b70cada846e1207c (N36): 4 entradas de manifiesto, doble descarga A.7
    COINCIDE, capa3_disco_real verificado en MAESTRA37-A1 (descargas_mx: coincide=267,
    no_coincide=0, ausente=0). Ninguna variable leida en este acto ni en el de origen --
    la lectura de eti21/eti25/eti27/eti33 (variables que sirven a R4.5 segun L3-BIS) es
    trabajo de C1, no de este pre-registro.
evidencia:
  procedencia_necesidad_id: N41
  procedencia_fuente: ENSANUT_CONTINUA_2024
  procedencia_objeto_evidencia_id: OE-591e527de7590585cde47973
  accion_normalizacion: SIN_CAMBIO
  clasificacion_relacion: CANDIDATA
  tipo_evidencia: PAYLOAD_ADQUIRIDO
  evidencia_ref: "MAIN:forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md"
  evidencia_localizador: "data/manifiesto.yaml (4 entradas: etiquetado_ensanut2924_w_cat_logo__v2026_09_01 ... etiquetado_ensanut2924_w_stata_stata__v2026_09_01)"
  variable_reactivo_tabla: "eti21;eti25;eti27;eti33 (candidatas, segun L3-BIS; no leidas todavia)"
  texto_evidencia: >
    Componente de etiquetado frontal de alimentos de ENSANUT Continua 2024 (version
    publicada 2026-09-01). Re-asentado desde N36 a N41 por adjudicacion de L3-BIS
    (unico de 8 componentes que sirve a una regla de salud: R4.5). Ninguna variable
    se ha leido en este acto.
  unidad_observacion: NO_DETERMINADO
  periodo: "2024 (levantamiento continuo); version publicada 2026-09-01"
  universo_muestra: NO_DETERMINADO
  codificacion: NO_DETERMINADO
  parte_necesidad_cubierta: NO_DETERMINADO
  parte_necesidad_no_cubierta: "NO_DETERMINADO -- este acto no abre el microdato."
  uso_potencial_modelo: NO_DETERMINADO
  transformacion_requerida: NO_DETERMINADO
  incertidumbre: "Alta por adjudicacion documental (L3-BIS), no por lectura de variable. eti21/eti25/eti27/eti33 son candidatas de L3-BIS, no confirmadas por apertura."
  siguiente_accion: "C1 (o sucesor): abrir el componente, leer eti21/eti25/eti27/eti33, confirmar que sirven a R4.5."
  objeto_modelo_origen: R4.5
  objeto_modelo_origen_ref: "canon/modelo-decision-v4_0.md:411 (salud.consumo.sellos_precio_similar)"
utilidad:
  estado_productivo: PENDIENTE_EVIDENCIA
  uso_actual: "Ninguno. Payload adquirido y verificado; no se ha leido."
  evidencia_disponible: "SI (payload en descargas_mx, 4 entradas de manifiesto, --verifica COINCIDE, verificado en MAESTRA37-A1)"
  reserva: "Re-asentado por adjudicacion documental de L3-BIS, no por lectura de variable. Requiere abrir el componente y confirmar eti21/eti25/eti27/eti33 antes de parametrizar R4.5."
  verificacion_requerida: "Abrir el componente etiquetado, mapear eti21/eti25/eti27/eti33, confirmar que cubren R4.5 (sellos_precio_similar)."
  requiere_decision: "NO"
  decision_id: NO_APLICA
  siguiente_accion: "C1 (o sucesor): lectura de eti21/eti25/eti27/eti33 y parametrizacion de R4.5."
  evidencia_ref: "MAIN:forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md"
```

**Verificación al ejecutar:** caja corre `alta_relacion.py --dry-run` primero; si el `relacion_id` que el script deriva **no** es `REL-e7c3700e98be2d9aa7bbd55e`, el acto se detiene y declara la discrepancia antes de aplicar (A.8 contra el propio pre-registro).

---

## 4 · La fila vieja bajo `N36`, y las 7 que no se mueven — mecanismo declarado, no ejecutado

**`alta_relacion.py` no puede tocar `REL-54b26887b70cada846e1207c` (§2)** — tras el alta de §3, esa fila queda huérfana bajo `N36` salvo anotación aparte. Este pre-registro fija el mecanismo, sin ejecutarlo: **anotación manual, texto-preservando**, mismo patrón ya usado en este proyecto para dedup (`ACTO` que cerró `ADR-335`, dedup de la fila `CSES` duplicada: *"la `PENDIENTE` pasa a `estado_A4A5=SUPERADA-POR` con nota, vista regenerada con el writer oficial"*). El campo `nota` de `REL-54b26887b70cada846e1207c` se edita a mano (no vía `alta_relacion.py`, que no reescribe filas) para anotar `SUPERADA-POR REL-e7c3700e98be2d9aa7bbd55e (N41)`, preservando el resto de la fila byte a byte, exactamente como `alta_relacion.py` mismo hace con las filas que no toca.

**Las 7 relaciones no-etiquetado (actividad física, antropometría, frecuencias, rec24h, lactancia, plomo, sangre) NO se re-asientan.** L3-BIS ya adjudicó: *"su `clasificacion_relacion = CANDIDATA` es correcta y se queda"* (§0). `C1` no las toca, no las mueve, no les inventa un `N`-destino — quedan bajo `N36`, sin cambio, con la adjudicación de L3-BIS citada como razón de por qué no se tocan.

---

## 5 · Los 4 `ENFIH` pendientes (`FP-288`)

`forense/firmas-pendientes.tsv` (fila `FP-288`, `estado = ABIERTA`, no resuelta): 4 filas de `relaciones.tsv` con `id_manifiesto = NO_DETERMINADO` que citan `enfih2019_bd_csv_zip` en su nota como el payload de registro:

| relacion_id | necesidad_id | línea (`relaciones.tsv`) | `id_manifiesto`/`sha256_fuente` actual |
|---|---|---|---|
| `REL-16d3c66af7fc856df2130139` | N10 | 28 | `NO_DETERMINADO` / `NO_DETERMINADO` |
| `REL-3b746c49c7c051083df6ee81` | N3 | 57 | `NO_DETERMINADO` / `NO_DETERMINADO` |
| `REL-50e6d069fd121a8a7cd64fc5` | N14 | 76 | `NO_DETERMINADO` / `NO_DETERMINADO` |
| `REL-6b52ae9ea4b72a9f27f01260` | N13 | 91 | `NO_DETERMINADO` / `NO_DETERMINADO` |

**`id`/`sha256` esperados si mesa autoriza la resolución** — verificado directamente contra `data/manifiesto.yaml:4102-4116`:

```
id_manifiesto esperado: enfih2019_bd_csv_zip
sha256 esperado:        be372533d5043920892142e8bf792b7293a5f20ab466a6441bc89925b42ef4d5
```

**Declarado, no ejecutado:** estas 4 son filas **existentes** con campo vacío (`NO_DETERMINADO`) — resolverlas es un **UPDATE**, no un alta, y `alta_relacion.py` **tampoco** puede escribir esto (§2: nunca reescribe una fila existente). `FP-288` deja a mesa dos opciones (verbatim, `forense/firmas-pendientes.tsv:280`): *(i) autorizar una corrida dirigida de `via_capa2.py --vincula` sobre esas 4 filas, o (ii) aceptar la exclusión y dejarlas en `NO_DETERMINADO`.* `C1` pre-registra el valor esperado **para el caso en que mesa elija (i)** — no decide cuál de las dos opciones toma mesa, y no ejecuta ninguna.

---

## 6 · Qué NO hace este acto

No corre `alta_relacion.py` ni en modo real ni en `--dry-run`. No escribe `relaciones.tsv`, `evidencias.tsv`, `utilidad-modelo.tsv` ni `baseline.json`. No edita la nota de `REL-54b26887b70cada846e1207c`. No resuelve `FP-288`. No abre `eti21`/`eti25`/`eti27`/`eti33` ni ninguna otra variable — la lectura del componente etiquetado queda para el acto que ejecute §3, no para este pre-registro.

---

**el primer resultado que produzca este procedimiento es el que se reporta.**
