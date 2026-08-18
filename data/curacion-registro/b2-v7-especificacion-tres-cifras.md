# Especificación congelada · las tres cifras del bloque 2 de BARRIDO-2, generación v7

**Acto:** B2-V7 · **Fecha:** 2026-08-18 · **Base:** `origin/main = 997482b` (merge #244)
**Procedimiento:** `data/curacion-registro/b2-v7-medir-tres-cifras.py`, mismo commit,
`sha256 = 94e0b5ebdd9fb6b5c5c241aef28fcde2d5c95f46e513f764895a35af7e75a7aa`

Este documento y el procedimiento que lo acompaña se commitean **antes de abrir un solo
resultado**. COMMIT B traerá las cifras y no editará este archivo. Si la especificación
resulta equivocada, lo dice un tercer commit; no se corrige hacia atrás.

---

## 0 · Universo, y por qué es éste

Las tres cifras se miden sobre **el índice E2 neutral de la generación v7**: los 672
expedientes de `.barrido2/staging-v7/*/e2-neutral-index.jsonl`, 1 833 802 registros.

No se miden sobre los productos durables de `data/curacion-universo/` porque **no se
pueden regenerar en este acto**. El gate material de la generación v7 está en rojo y su
arreglo cae fuera del perímetro (ver §4). Los expedientes, en cambio, existen, están
completos y los produjo el escritor ya corregido del bloque 2 — que es exactamente lo que
las tres cifras interrogan: **qué conservó el escritor**. Que el validador después lo
rechace es un hecho distinto, se mide aparte y se reporta aparte.

**Estampa de universo (A.10).** Las tres cifras se sellan contra: el SHA del worktree al
medir, la generación `v7`, y el número de expedientes examinados (672). Si la generación
cambia, el sello queda **VENCIDO EN ALCANCE** — no refutado, no borrado, y no vigente para
el territorio nuevo.

**Selección por `objeto_tipo`, no por `format`.** Medido antes de congelar: `format` es el
formato del **contenedor**, no del objeto. Un `.sav` dentro de un `.zip` lleva
`format=".zip"`, y 9 204 de los registros con `value_labels` no vacío llevan `format=".zip"`
contra 391 con `format=".sav"`. Seleccionar por `format` perdería la mayoría del universo
de la cifra 1. Toda selección de familia va por sufijo de `objeto_tipo`.

---

## 1 · CIFRA 1 · value labels de SAV conservados

- **Qué se cuenta:** entradas individuales de la lista `value_labels`, no registros.
- **Universo:** entradas de `value_labels` de todo registro cuyo `objeto_tipo` **termine en
  `-SAV`** (`VALUE-LABEL-COLLECTION-SAV`, `VARIABLE-SAV`, `EXTENSION-DICCIONARIO-SAV`,
  `TABLA-SAV`).
- **Denominador:** el total de esas entradas.
- **Numerador — CONSERVADA:** la entrada **no contiene** la subcadena
  `[REDACTADO-PRIVACIDAD]`. Sobrevivir entera es el criterio; sobrevivir a medias no cuenta.
- **Escala declarada:** `PORCENTAJE-DE-CONSERVACION`, dos decimales, **acompañado siempre
  del par absoluto numerador/denominador**. Un porcentaje sin su par no es reportable.

**Contraste con DTA, que es la referencia declarada ("DTA conserva 99.5 %").** Se mide la
misma tasa, con la misma regla, sobre `objeto_tipo` terminado en `-DTA`, y se reporta como
cifra propia con **su propio denominador**. Se dirá si reproduce el 99.5 % o no, sin
ajustar el resultado hacia la referencia.

**Advertencia de forma, para que el contraste no engañe.** Las dos familias no escriben
igual. SAV emite `codigo_hex=<16 hex>;label=<texto>`; DTA emite sólo el texto
(`Aprueba firmemente`). El porcentaje **no compara las cadenas**: compara la tasa de
supervivencia a la redacción. Que SAV cargue un código de 16 dígitos y DTA no es
precisamente la causa histórica de que SAV se redactara y DTA no, así que la comparación es
informativa, no simétrica.

---

## 2 · CIFRA 2 · metadatos de miembro ZIP conservados, con `zip_slip` presente

- **Qué se cuenta:** registros con `objeto_tipo = MIEMBRO-ZIP`.
- **Denominador:** el total de esos registros.
- **Numerador — CONSERVADO ENTERO:** su `definicion` no contiene `[REDACTADO-PRIVACIDAD]`
  **y** contiene las cuatro claves `bytes=`, `comprimidos=`, `crc=` y `zip_slip=`.
- **Escala declarada:** `PORCENTAJE-DE-CONSERVACION`, dos decimales, con par absoluto.

**Se reporta además, por separado y con el mismo denominador,** la conservación de sólo la
declaración `zip_slip=` — que es la que el control nombra explícitamente
(`crc=3266880665;zip_slip=NO sobrevive entero`). Son dos cifras, no una: "el metadato
completo sobrevivió" y "la declaración de seguridad sobrevivió" pueden diferir y mezclarlas
las haría inauditables.

**Se reporta aparte el reparto `zip_slip=SI|NO`, en escala `CONTEO-ABSOLUTO`.** Es una
medición de seguridad del corpus, no de conservación del metadato, y no se promedia con
las anteriores.

---

## 3 · CIFRA 3 · PDF abiertos

**Desviación declarada antes de medir, no descubierta después.** El control que el encargo
cita declara los marcadores `rc=`, `stderr=` y `bytes_texto=`. Verificado por barrido
completo del índice v7 el 18/ago: **ninguno de los tres existe**. `bytes_texto=` y
`stderr=` tienen cero apariciones; las 25 713 de `rc=` son un falso positivo de subcadena
— es el `crc=` de los miembros ZIP, no un código de retorno. La generación v7 declara la
apertura de PDF con otra forma, en `definicion` de los registros `PAGINA-PDF`:

```
lineas_texto=<n>;texto_extraible=SI|NO;cifrado=NO|SI-EXTRAIBLE
```

La cifra se mide sobre **esa** forma. La desviación se reporta como tal: la referencia
"77 de 78" pertenece a un control corrido sobre otra generación y otro vocabulario.

- **Unidad de conteo:** el **documento PDF**, no la página ni el archivo contenedor. Se
  identifica por `(representacion_id, prefijo del localizador antes de "pagina=")`. Un PDF
  suelto cuelga de su representación (`localizador="pagina=12"`); uno dentro de un ZIP
  cuelga de su miembro. La clave identifica el mismo documento en los dos casos sin
  privilegiar ninguno.
- **Universo A — el que corresponde a "los 83":** documentos PDF con al menos una página
  `cifrado=SI-EXTRAIBLE`.
- **Universo B — el que corresponde a "los que abrieron":** los de A con al menos una
  página `texto_extraible=SI`.
- **La cifra 3 es `|B|` sobre `|A|`**, ambos en `CONTEO-ABSOLUTO`, más el porcentaje.
- **Se declarará explícitamente** si `|A|` reproduce 83 y `|B|` reproduce 77. Si no lo
  reproducen, se dice el número real y no se ajusta.
- **Se reportan aparte, rotulados como denominadores ajenos:** el total de documentos PDF
  del universo v7 y el total de los que abrieron. Existen para que "de los 83" nunca se
  confunda con "de todos los PDF" — que es la mezcla que el propio control ya cometió.

---

## 4 · Lo que ya se sabía antes de congelar

Se declara para que el sello valga. Antes de escribir este documento se conocía:

- el vocabulario completo de `format`, `objeto_tipo`, `estado`, `privacidad`, `parser` y
  `frontera_inspeccion`;
- que `cifrado=` aparece en 53 895 registros, repartidos `cifrado=NO` 36 976 y
  `cifrado=SI-EXTRAIBLE` 16 919 — reparto que abarca miembros ZIP y páginas PDF a la vez;
- que `[REDACTADO-PRIVACIDAD]` marca 1 167 024 registros contra 666 778 `DEPURADO`;
- el veredicto del gate material (§5).

**No se había calculado ninguna de las tres cifras**, ni la tasa de conservación de SAV,
ni la de DTA, ni la de los miembros ZIP, ni el conteo de documentos PDF de ningún universo.

---

## 5 · El gate material, medido y declarado aquí porque cambia la lectura de las cifras

`tools/curador_registro/validate.py --barrido2-material … --require-complete` → `rc=1`,
`ok:false`, sobre 672 representaciones y 672 expedientes completos, 1 833 802 registros E2:

```
E2_PII_NO_REDACTADA  13 953
LEDGER_NO_TERMINAL      376
E2_ERRORES_TRUNCADOS     51
```

Las 13 953 activaciones son **cero PII real**. Son tres combinaciones (campo, patrón), las
tres metadato de máquina, medidas una por una:

| campo | patrón | activaciones | qué es |
|---|---|---|---|
| `value_labels` | `\d{11,18}` | 100 841 | `codigo_hex=3120202020202020`, código IEEE-754 |
| `value_labels` | teléfono, 10 dígitos | 31 555 | `codigo_hex=0000000000c05840` |
| `definicion` | teléfono, 10 dígitos | 18 418 | `crc=2719796586;zip_slip=NO` |

Cero activaciones en cualquier otro campo y en cualquier otro patrón.

**Los dos campos que el gate rechaza son exactamente los dos que las cifras 1 y 2 miden.**
El escritor conserva lo que el bloque 2 se propuso conservar; el validador lo deshace. El
remedio de `exento_estructural()` cerró el eje **estructural** (`nombre`/`hoja`/`tabla`) y
dejó abierto el eje **durable** (`value_labels`, `definicion`) — tercera instancia de la
misma clase de defecto que ya costó dos reejecuciones.

Arreglarlo exige editar `tools/curador_registro/barrido2_material.py`, que está **fuera del
perímetro** de este acto (`tools/` sólo para el §1) y además cambiaría
`MATERIAL_BUILD_SHA256`, invalidando los 672 expedientes. Se PARA ahí y se propone acto
propio.

---

**el primer resultado que produzca este procedimiento es el que se reporta**
