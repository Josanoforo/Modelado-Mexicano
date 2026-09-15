# ACTO GEN2-MANTENIMIENTO-Y-ARCHIVO-2 · nota de cierre

**15/sep/2026 · NUBE · `cloud_default` · cero microdato, cero red, cero descargas, cero corridas selladas, cero adopciones · CONTADOR: cero.**

Encargo archivado verbatim por A.3: `forense/encargos/2026-09-15-GEN2-MANTENIMIENTO-Y-ARCHIVO-2.md`.
`COMPUERTA: ninguna` — el encargo no declara `GATED a`, `Estado: GATED a` ni
`COMPUERTA:` en ninguna de las tres formas del Bloque D.

## §0 · Entorno (A.2, tres partes)

`python3 tools/entorno.py`, salida cruda al arrancar:

```
ENTORNO · commit=0cdbd72c4413 · git_status=LIMPIO(0) · python=3.11.15 ·
numpy=AUSENTE pandas=AUSENTE scipy=AUSENTE yaml=6.0.1 pyreadstat=AUSENTE ·
CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default ... · red=no-ejecutada ·
raices=data_raw:NO · corpus=NO(examinados=0)
```

Sonda de red **no ejecutada a propósito**: este acto no toca microdato ni red,
y una sonda que nadie pidió es I/O que nadie declaró. `data/raw` ausente es lo
esperado en NUBE y no es PARO para lo que aquí se hizo — pero **sí** es la causa
del `PARO-ENTORNO` de `NC-0228` (ver §5).

Guard de arranque, las cuatro: base `0` commits detrás de `origin/main` ·
árbol limpio · duplicado `0` coincidencias del rótulo en remoto y worktrees ·
`limpia_arbol.py --reporta` pegado (1 worktree, 1 rama fusionada viva, punto D
`NO-VERIFICABLE-SIN-GH`).

## §1 · Las dos premisas que no se cumplieron

Las dos son del propio encargo, y las dos se declaran en vez de rodearse.

**(a) La hoja de firmas 2 no viajó.** El encargo dice «Propaga la hoja de firmas 2
(**abajo**)». Abajo no hay nada: la línea del perímetro es la última del mensaje.
La copia verbatim de A.3 es la prueba. No se infiere: una firma de mesa es la
autorización del árbol, y escribirla sin haberla recibido sería fabricar
autoridad — el único defecto que `decisiones.tsv` existe para impedir.
`decisiones.tsv` **no gana ninguna fila** en este acto. → `NC-0226`.

Contraste que lo hace verificable, no una excusa: la hoja de firmas **1** sí
existe, archivada en `forense/encargos/2026-09-15-GEN2-FIRMAS-MESA-1.md` con su
firma verbatim «Si a todas.», y de ella se leyeron FP-371/FP-372 para poder
cerrar `NC-0209` en este mismo acto (§3). Así se ve una hoja que sí llegó.

**(b) Los adjuntos de `NC-0219` no viajaron.** La cláusula del encargo gobierna:
«Si un adjunto no viaja, esa pieza PARA». Re-verificado con universo (A.13):
`find . -name 'ADVERSARIAL-ASTRA-1*'` → **0**; `grep -rl "LECTURA ESTRAT"
canon/ forense/` → **7 sobre 3 694 archivos**, y las 7 son *referencias* al
documento (la propia `NC-0219`, el informe y su anexo), no el documento. Las
notas `*-astra.md` del árbol siguen siendo otras, de 8–9/sep. → `NC-0219` sigue
ABIERTA.

## §2 · Herramientas

**`NC-0199` — `repite_de` bajo `etiquetas:` (CERRADA).** `tools/corrida0.py:3259`
leía el campo sólo a nivel raíz. Ahora cae al helper `_etiqueta()`, que es la vía
que la propia fila prescribía; la raíz conserva precedencia. **Cero specs
selladas tocadas** (E.3): se corrigió el *lector*.

Medido, no supuesto — sobre las **104** `spec.yaml` del árbol: **31** lo declaran
en raíz y **6 SOLO bajo `etiquetas`** (`CALC-DINERO-FAMILIARES-VEJEZ-0001`,
`CALC-ENIGH-0001`, `CALC-ENVIPE-U4-2012-v1_1`, `CALC-EVASION-NORMA-0001`,
`CALC-HORIZONTE-VIA-DERIVADOS-0001`, `CALC-TIENE-AHORROS-0001`). La fila nombraba
**una**.

Falsador nuevo: `tests/test_corrida0.py::t_registro_superado_por_repite_de_en_etiquetas`.
Verificado **por reversión**, no por confianza — con el parche, `92 casos · 92 ok`;
revertido el parche, `91 ok · 1 FALLOS`:

```
FAIL  t_registro_superado_por_repite_de_en_etiquetas: EXCEPCION ParoRegistro:
ID-DUPLICADO: RESULT-A aparece en CALC-FIX-A--fixture, CALC-FIX-B--fixture
sin cadena `repite_de` que las una
```

**Hallazgo que corrige la fila sin absorberla:** `NC-0199` declaraba su impacto
«cosmético, no numérico». Es más grave: sin el arreglo, una sucesora que repita
ids de `RESULT` hace **PARAR** a `registro`. En el árbol real no ocurría sólo
porque las 6 sucesoras renombraron sus `RESULT`.

**`NC-0191` — el timeout de T16 (CERRADA).** `tests/check.py:818`, `120s → 300s`,
**piso medido bajo carga real de NUBE**, que es lo que la fila pedía. Tres
corridas consecutivas del hijo (`CHECK_SELFCHECK_CHILD=1 python3 tests/check.py`)
en este árbol:

```
corrida 1: 82.9 s (exit=1) :: 3 FAIL · 4353 WARN
corrida 2: 83.0 s (exit=1) :: 3 FAIL · 4353 WARN
corrida 3: 82.0 s (exit=1) :: 3 FAIL · 4353 WARN
```

Las tres con **la misma salida**: el límite cortaba una suite estable, no una
regresión de contenido. 120 s dejaba **1.45×** de margen sobre la mediana medida;
300 s deja **~3.6×**. La lógica de comparación FAIL/WARN **no se tocó**, que es lo
que la fila excluía del perímetro. Control: la suite completa de este acto corrió
en **165–167 s con T16 sin topar** y LÍNEA BASE VERDE.

## §3 · Documentos y sellos

**`NC-0176` (CERRADA).** el skill `/acto` (`.claude/commands/`) §4.3 citaba
`canon/estado-programa-v1_12.md` como única fuente de estado. Ahora cita
`v1_13` (v1_12 retirada por `T01`) y **`ADR-497`** — el ADR real que la sucedió,
no `ADR-339`, que era el de v1_12. Dos citas; cero semántica del skill tocada.

**`NC-0050` (CERRADA) — la trampa desarmada.** El texto reescrito por
`GEN2-E5-1` (`NC-0047`) se propagó a las **líneas 45 y 58** del maestro
`forense/notas/ENCARGOS-GEN2-v1_5-aparato-antes-de-calcular-2026-09-08.md`,
tomado **verbatim** del cuerpo de los dos encargos de cola — no re-redactado.

Verificado con las **propias funciones de la herramienta de la trampa**, que es
lo único que prueba que está desarmada: `secciones_maestras()['E5-0']` y `['E5']`
son ahora idénticas, línea por línea, al prefijo de `cuerpo_de_cola()` de sus dos
archivos de cola. Un `verifica_encargos_gen2.py --aplica` futuro ya **no** revierte
en silencio la reescritura de `NC-0047`.

**`NC-0170` (PARCIAL, 2 de 8) — la lista se re-derivó porque estaba vieja.**
Censo nuevo, PR por PR contra el PR real y contra los **497** encargos de
`forense/encargos/` (nivel 1):

| PR | encargo archivado | estado |
|---|---|---|
| `#739` · `#737`(→`#742`) | sí | **ya sellados** por `GEN2-CONSUMIDO-RETRO-3` (`PR #759`) |
| `#680` | `2026-09-09-GEN2-R-COMPLETA-MARCO.md` | **retro-sellado aquí** — sólo faltaba el dígito, como la fila decía; sección existente **intacta**, se le añade `· PR #680` |
| `#701` | `2026-09-10-GEN2-PUBLICACION-POST693-Y-CIERRES.md` | **retro-sellado aquí** — su `## CONSUMIDO` citaba el PR base `#696` y no la adenda `#701`; enmienda fechada, párrafo original sin reescribir |
| `#682` `#719` `#726` `#728` | **ninguno** (0 coincidencias del rótulo sobre 497) | **no retro-sellables** → `NC-0227` |

Los 4 últimos fallan por una razón **distinta** de la que `NC-0170` suponía: no
les falta la sección, les falta el archivo `A.3` entero. Y `A.3` no se rellena
hacia atrás sin el texto original del encargo, que nadie tiene — escribir uno
ahora sería redactar hacia atrás lo que ese paso existe para hacer auditable.
`#728` es además un PR de **preparación** («Estado: PENDIENTE DE FIRMA; cero
llamadas al proveedor», verbatim de su cuerpo) cuyo encargo sigue legítimamente
en cola: sellarlo como consumido sería **falso**. Mesa decide (`NC-0227`); este
acto no elige por ella. La segunda mitad de `NC-0170` (¿`[COLA]`/`[ADQ]` como
cuarta categoría exenta?) sigue sin decidir.

**`NC-0209` (CERRADA) — y por qué esta sí y `NC-0210` no.** `data/diseno-muestral.yaml`,
campo `supuesto_varianza`, recibe su enmienda fechada **por append** — el patrón
que la propia fila prescribía, junto a `CORRECCIÓN D16` y `ENMIENDA S6`; el texto
anterior queda intacto. Verificado **antes** de escribir: FP-371 y FP-372 constan
`FIRMADA` en `forense/firmas-pendientes.tsv` por la firma de mesa del 15/sep
(«Si a todas.»). La enmienda transcribe los OBJETOS 14 y 15 verbatim y fija la
lectura operativa (FP-371 = **rechazo**; FP-372 = **opción (a)**), sin reescribir
sellos ni mover tier, y deja `NC-0156` viva. El archivo **no** está sellado (sin
sidecar `.sha256`), así que el append no rompe ningún sello; YAML re-parseado
después: válido, 56 entradas de primer nivel.

La mitad **S6-L16** de la fila no se ejecuta, y la **decisión sí se toma**, que es
lo que el encargo pedía: S6-L16 **sí necesita** sucesora `v1_6` (FP-372 ya está
firmada y la `v1_5` sigue remitiéndola como pendiente en su línea 52). No se abre
aquí por regla, no por olvido: `S6-L16-spec-v1_5.md` está **sellada** con sidecar
`.sha256`, E.3 prohíbe editarla, y una sucesora de `prereg-caja` no cabe en el
perímetro de este acto. → `NC-0229`. La contradicción del árbol pasa de **dos
sitios a uno**.

**`NC-0218` — no hay sello que incorporar.** La fila decía «sin esperarlo», y no
se esperó: se midió. ACTO **D-A re-verificado AUSENTE** con universo declarado
(A.13): `git ls-remote --heads origin` sobre **4** ramas remotas → 0
coincidencias; `find forense/encargos -name '*.md'` sobre **562** archivos → 0.
`§A.3` del ANEXO sigue, correctamente, como DERIVACIÓN PROPIA con control
positivo y **no** como el sello. Ningún contador se mueve. Sigue ABIERTA.

## §4 · Lo que el perímetro no autorizaba

`NC-0212` y `NC-0213` exigen tocar una spec **sellada** o abrir su sucesión, y
`E.3` lo prohíbe: el perímetro de este acto es `tools/`, docs, notas,
`no-corrido`, `decisiones` — no `data/corrida0/*/spec.yaml`. Una sucesión además
no se sella sin CAJA, y esta sesión es NUBE con `corpus=NO`. `NC-0174` pide
explícitamente permiso sobre `data/curacion-registro/` y `milpa/demanda`, que es
justo el que este encargo no concede. `NC-0210` cae con la hoja 2 por la regla
del propio encargo — «milpa **solo donde una firma lo autorice**» —, y se
verificó que la hoja **1** no la autoriza: su tabla declara que la cifra
`0.668937` «no es una» de las cuatro glosas autorizadas.

## §5 · Suite y reserva de entorno

`python3 tests/check.py --baseline`, tras registrar el encargo A.3 en
`_T03_DEPENDENCIAS_PENDIENTES`:

```
3 FAIL · 4351 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```

Los 3 FAIL son los congelados (T06×2, T08×1). Las dos entradas T03 que aparecieron
antes las causaba el **encargo verbatim** de este acto — una cita al adjunto que no
llegó (que es `NC-0219` misma) y una a el skill `/acto`, que **sí existe** en
el skill `/acto` (`.claude/commands/`) pero que el glob `**/*.*` de T03 no ve por ser
directorio con punto. Se registraron en la lista de dependencias pendientes con el
comentario que explica cada mención: **un encargo A.3 nunca se edita para complacer
al test** (`/acto` §4.5).

**Reserva.** `NC-0199` se cierra, pero su efecto en las vistas derivadas no se
publica aquí: exige `registro --escribe` con corpus montado, y `--verifica` sin
corpus degradaría a `NO-VERIFICADO` veredictos de corridas ajenas ya publicadas
— el mismo limbo exacto que `NC-0145` declaró y que sigue ABIERTA. → `NC-0228`,
que conviene que absorba también `NC-0145`. Ningún número de este acto depende de
esa escritura.

## §6 · Contador

**Cero, y se dice.** Cero corridas selladas, cero `RESULT` nuevos, cero
adopciones, cero reglas del motor tocadas, cero filas nuevas en
`data/corrida0/decisiones.tsv` (§1a). Cierra `NC-0050`, `NC-0176`, `NC-0191`,
`NC-0199`, `NC-0209`; deja anotadas `NC-0170`, `NC-0218`, `NC-0219`; abre
`NC-0226`, `NC-0227`, `NC-0228`, `NC-0229`.

## §7 · Enmienda al integrar `origin/main` (mismo acto, 15/sep/2026)

`main` avanzó de `0cdbd72` a `ce79136` durante el acto y dos premisas de §1
cambiaron de estado. **Ninguna de las dos invalida lo que esta sesión hizo, y las
dos se declaran:**

**(a) La hoja de firmas 2 sí existía.** `PR #792` la registró y propagó
(`def4176`, `56ee620`), fusionado mientras esto corría. Lo que §1a dice sigue
siendo cierto *de esta sesión*: no viajó en el mensaje que lanzó el acto, y por
eso no se infirió — que era la decisión correcta con la información disponible.
`NC-0226` (antes `NC-0225`) se abre y se cierra en el acto con `SUSTITUIDO-POR`
el acto de `PR #792`, para que la secuencia quede auditable. **Enumerado
explícitamente, que es lo que un `SUSTITUIDO-POR` debe traer:** el sustituto
absorbe la propagación a `decisiones.tsv` y el cierre de las NC que la hoja
resuelve, íntegro; **queda huérfana `NC-0210`**, porque
`2026-09-15-GEN2-FIRMAS-MESA-2.md` **no la menciona** ni menciona `0.668937`
(0 coincidencias, verificado) — sigue ABIERTA y sin autorizar.

**(b) `NC-0219` ya está CERRADA** por `ACTO GEN2-ARCHIVO-LECTURA-F5-1`
(`PR #794`), que recibió los textos de mesa y los commiteó verbatim. Lo que §1b
dice sigue siendo cierto de esta sesión. La fila cerrada de `origin` se conserva
**intacta** y este acto **no la re-anota**: su medición ya no describe el árbol.

**Renumeración** (regla de la casa, renumera quien fusiona segundo): `NC-0225..0228`
→ **`NC-0226..0229`**, porque `PR #794` tomó `NC-0225`. `ADR-517` no colisiona
(máximo real en `origin/main` = `516`).
