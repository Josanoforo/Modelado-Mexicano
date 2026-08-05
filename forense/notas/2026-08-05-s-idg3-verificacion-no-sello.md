# ACTO S-IDG3 · Verificación de sello de la ficha `ID-G3` (`G3·horizonte_temporal`, RUTA-I)

**Estado: NO SELLADA. Declarado por qué, no fracaso — instrucción explícita del encargo.** Este acto revisó el borrador de `forense/notas/2026-08-04-e-mxfls-ficha-borrador.md` (Encargo E-MXFLS, marcado explícitamente NO SELLADA por su propio autor) contra las cuatro condiciones de sello que el encargo fija. Tres se verifican limpias. La cuarta — payloads en disco con hash coincidente — **no se pudo ejecutar en esta sesión**: el corpus compartido no es alcanzable desde este entorno de nube. No se sella mientras esa verificación quede pendiente. No se corrió ninguna estimación, no se abrió ningún microdato, no se tocó `milpa/procedencia.yaml` ni `canon/`.

Contador: cero. No habilita nada nuevo — el borrador queda exactamente donde estaba.

---

## 0 · ARRANQUE (Bloque D)

1. **REPO.** Clon existente en `/home/user/Modelado-Mexicano` (no home). Rama `claude/g3-horizonte-temporal-id-s88z1w`, ya creada al abrir. `git log -1`: `06d04be Merge pull request #118 from Josanoforo/claude/encargo-m4-r1-3-adjudicacion-czqze3`. `git status`: working tree limpio.
2. **SHA.** `git fetch origin main`: `origin/main` real = `06d04be` — coincide exactamente con la base del encargo. `git merge-base --is-ancestor 06d04be HEAD` → sí, es ancestro directo de la rama de trabajo. Sin diferencia que reportar.
3. **`data/raw`.** Ausente en este worktree (esperado, gitignorado). Este acto **sí lo usa** — el punto 2 de la verificación exige hash de payload en disco — así que se intentó enlazar al corpus compartido con el patrón documentado (`ln -s /home/pc0/mm-corpus/raw data/raw`, citado en `forense/notas/2026-08-04-e-mxfls-nota-proceso.md:7` y `forense/notas/2026-08-04-hitoD-r5-1-pension-bienestar.md:31`). **`/home/pc0` no existe en este contenedor** — verificado con `find / -maxdepth 3 -iname "*mm-corpus*"` (cero resultados), `ls /home/` (solo `claude`, `ubuntu`, `user`), y `df -h`/`mount` (un único disco `ext4` de trabajo más los montajes de solo-lectura del harness; ningún volumen de corpus). Tampoco existe `data/raices.local.yaml` (gitignorado, por máquina) que declare una raíz alterna. **Hallazgo de terreno, reportado como exige el bloque de arranque:** este entorno de nube concreto no tiene el corpus compartido montado — a diferencia de las sesiones locales Ubuntu-con-red donde se redactó el borrador (`nota-proceso:7`) y a diferencia de otras sesiones de nube que no necesitaron tocar `data/raw` (`forense/notas/2026-08-05-m4-adjudicacion-adr-63.md:18`: *"`data/raw`: no aplica"* — pero ese acto no abría microdato ni verificaba payload; éste sí lo necesita). Detalle y consecuencia en §2 más abajo.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` — firma correcta de nube (ADR-59(b), `gobernanza-v1_15.md:661`). Este acto no descarga nada nuevo y su red declarada es "solo git" (`git fetch` ya corrido arriba); se salta la sonda `curl` contra INEGI/otro host, como el propio punto 4 permite cuando el acto no toca red nueva.
5. **ESPEJO.** No se usó ningún espejo del proyecto. Toda cifra de este documento sale del clon de (1), con archivo:línea o comando citado.

---

## 1 · Lectura del borrador y su nota de proceso

Leídos completos, sin resumir: `forense/notas/2026-08-04-e-mxfls-ficha-borrador.md` (165 líneas — Paso 0 inventario de contaminación, Paso 1 elección de `AH`/`ah03h`, Paso 2 ficha `ID-G3` completa) y `forense/notas/2026-08-04-e-mxfls-nota-proceso.md` (34 líneas — arranque, perímetro, cierre de esa sesión).

## 2 · Verificación contra el archivo (las cuatro condiciones de §8)

### (1) Llave de identificación — VERIFICADA

El borrador declara llave **(i)** de `ADR-57(c)`, citando `canon/gobernanza-v1_15.md:623` (ficha, línea 87). Verificado directamente contra el archivo: `gobernanza-v1_15.md:623` (ADR-57(c)) nombra **tres** clases, textual — *"(i) panel con el desenlace en el instrumento (mismos sujetos entre olas); (ii) experimento natural con grupo de comparación sobre encuestas repetidas; (iii) diseño experimental de terceros"* — y la (i) es exactamente la que el borrador invoca, en la línea exacta que cita. El mismo ADR nombra explícitamente la ruta: *"ENNViH/MxFLS — panel de tres olas, dominio público; ruta viva vía `CAL-G3` ... la promoción de descriptivo a identificado exige su propio diseño intra-persona, no está concedida aquí"* — es literalmente el encargo que este borrador ejecuta. Confirmado además, de forma independiente, en `forense/censo-estimabilidad-coeficientes-v1_0.md:69` (fila G3, columna de llave: *"SÍ — llave (i) nombrada explícitamente ... (`gobernanza:623`, verbatim)"*). Tres documentos independientes coinciden verbatim. **Pasa.**

### (2) Payloads ENNViH/MxFLS en disco, hash coincidente — NO VERIFICABLE EN ESTA SESIÓN

Identificadas las entradas de `data/manifiesto.yaml` que cubren los materiales que el borrador cita (códigos/cuestionarios de las olas 2-3, módulos `TB`/`AH` — ver Declaración de exploración, ficha líneas 162-164): `ennvih2_2005_hogar_cb` (línea 632, `archivo: ennvih/ehh05cb_all.zip`, línea 640), `ennvih3_2009_hogar_cb` (línea 807, `archivo: ennvih/ehh09cb_all.zip`, línea 815), `ennvih3_2009_hogar_q` (línea 827, `archivo: ennvih/ehh09q_all.zip`, línea 835).

Verificado, un `--id` por invocación (regla del encargo):

```
$ python3 tests/manifiesto.py --verifica --id ennvih2_2005_hogar_cb
ennvih2_2005_hogar_cb [data_raw]: AUSENTE -- ennvih/ehh05cb_all.zip no está en la raíz 'data_raw'

$ python3 tests/manifiesto.py --verifica --id ennvih3_2009_hogar_cb
ennvih3_2009_hogar_cb [data_raw]: AUSENTE -- ennvih/ehh09cb_all.zip no está en la raíz 'data_raw'

$ python3 tests/manifiesto.py --verifica --id ennvih3_2009_hogar_q
ennvih3_2009_hogar_q [data_raw]: AUSENTE -- ennvih/ehh09q_all.zip no está en la raíz 'data_raw'
```

Las tres, `AUSENTE` — consecuencia directa y determinista de §0.3: sin corpus compartido montado, `data/raw` está vacío, y las 27 entradas `ennvih*` del manifiesto resolverían igual (mismo mecanismo, no hace falta correrlas una por una para saberlo). **No es error del script ni defecto de la ficha** — es, textualmente, "un hecho sobre el entorno" (`tests/manifiesto.py:21`). Pero tampoco es `COINCIDE`: la condición que el encargo exige — *"están en disco y su hash coincide"* — no se puede afirmar hoy, en esta sesión, con este entorno. **No pasa — bloqueado por terreno, no por contenido.**

Nota aparte, verificada al correr el script: la advertencia del encargo (*"con varios `--id` en la misma invocación solo verifica el último, sin aviso"*) describe una versión anterior. `tests/manifiesto.py` actual (`_id_unico`, líneas 258-272; `cmd_verifica`, líneas 346-368) ya acumula `--id` con `action='append'` y verifica **todos** los pedidos, reportando **todos** los faltantes — corregido por `ADR-62` (Encargo MT-mantenimiento, 4/ago/2026, citado en `gobernanza:§4` vía la nota de ADR-63). Se siguió la instrucción literal (un `--id` por invocación) de todos modos; se declara la discrepancia porque el propio encargo pide verificar contra el archivo, no contra lo heredado.

### (3) La ficha declara qué la refutaría, no solo qué mide — VERIFICADA

Paso 2(8): `ID-C` (signo contrario o nulo estricto, RR≤1 con IC95%sup<1.25, en la submuestra con oferta local verificada) se declara explícitamente *"la fila informativa por excelencia de esta ficha"* — precisamente porque el confundidor AFORE↔IMSS (Paso 1, tratamiento) empuja hacia el signo que `G3` predice, así que un resultado que **no** confirme es evidencia genuina, no ausencia de señal. `ID-A` (confirma) se declara explícitamente **degradado** de antemano — *"NO corrobora `horizonte_temporal` por sí solo"* — para que no se lea como éxito disfrazado. Y la fila `E` prospectiva (`ADR-58(a)`) fija, antes de ver dato, qué significaría un resultado sin potencia: *"el panel ENNViH 2005-2012 no tiene, para este constructo, las transiciones necesarias para decidir por la vía intra-persona"* — no "la regla sobrevive fortalecida". Es una declaración de falsación real, con las tres salidas (confirma-degradado / refuta-informativo / sin potencia) fijadas antes de abrir dato, no una lista de qué se mediría. **Pasa.**

### (4) Precedente `CAL-G3`/`ADR-49 D1`/`D-09` — no repite el modo de falla, con margen que hay que declarar

Verificado contra fuente primaria, no contra el borrador ni contra el encargo:

- `ADR-49 D1` (`gobernanza-v1_15.md:456,805`, `forense/censo-estimabilidad-coeficientes-v1_0.md:49`): retiró `unico_calibrable_hoy` porque la vía **ENOE** no trae reactivo de conducta financiera — ruta distinta a la que esta ficha usa (ENNViH/MxFLS). No aplica por identidad de ruta; aplica como antecedente de que este programa sí ha visto rutas prometedoras morir al mirar de cerca.
- `D-09` (`gobernanza-v1_15.md:402`, ADR-47; `hitoD-preregistro-v2_0.md:640`, Nota 9): el criterio de falsación de `CAL-G3` (`CAL-C`/`9b` sobre `CRH01`) **no podía refutar por construcción** — verificado con `tests/calx_g3.py`, el **mejor caso teórico posible** (escenario A, ICC=0, tres olas apiladas, "cota imposible") dio `IC95%sup=1.281`, **por encima** del `<1.25` exigido; los escenarios reales (B: olas 2-3, 1.461; C: olas 1 y 3, 1.401) quedaron todavía más lejos. Ningún nivel de ejecución real podía mejorar el mejor caso teórico. Confirmado empíricamente al correr Fase C: 7-14 hogares informativos, dos órdenes de magnitud por debajo del `n` necesario (`hitoD-preregistro-v2_0.md:675`).
- **`ID-G3`, mismo tipo de chequeo (Paso 2(8), fila `ID-X`), aplicado a `ah03h`:** techo de discordantes olas 2-3 = 2,253 (cota más floja posible, traslape cero) → `IC95%sup=1.237`. **A diferencia de `CRH`, esto sí cruza el `<1.25`** — por el mismo tipo de prueba (cota teórica más generosa) que para `CRH` fallaba incluso en su mejor caso. Por la definición literal del precedente ("no podía refutar por construcción"), `ID-G3` **no repite el modo de falla exacto**: su compuerta no está cerrada de antemano.

**Lo que sí hay que declarar, sin suavizarlo:** el margen es de 0.013 sobre 1.25 (~1%), calculado con un solo escenario — el más generoso posible — y no con el barrido que `calx_g3.py` sí corrió para `CRH` (múltiples supuestos de ICC, más los dos pares de olas reales). La propia ficha lo admite, Paso 2(8): *"es plausible ... que el número real de hogares informativos quede de nuevo por debajo de lo necesario"*. Si `ID-G3` sufriera, de la cota floja a un escenario realista, una degradación proporcional a la que `CRH` sufrió (1.281→1.401-1.461, +9% a +14%), el resultado quedaría por encima de 1.25 — es decir, el mismo desenlace de `CRH`, solo que sin haberlo corrido todavía. La ficha no fuerza esa lectura (por eso declaró la fila `E` con su significado exacto para este caso, algo que `CAL-G3` nunca tuvo disponible — `ADR-58` es del 4/ago, posterior a `D-09` del 30/jul), pero el chequeo de alcanzabilidad que trae, tal como está, es más delgado que el que el propio precedente exige como estándar. **No bloquea el sello por sí solo — el gate no está cerrado por construcción, que es la condición literal — pero es un hallazgo que cualquier acto que retome esto debe resolver antes de confiar en `ID-C` como desenlace practicable:** extender `ID-X` con el mismo barrido de escenarios que `calx_g3.py` aplicó a `CRH`, no solo la cota más floja.

## 3 · Decisión

**No se sella.** La condición (2) — payloads en disco, hash coincidente — no se puede afirmar desde esta sesión: `tests/manifiesto.py --verifica` devuelve `AUSENTE`, no `COINCIDE`, para los tres ids representativos verificados (exposición `TB` y desenlace `AH`, olas 2-3), y el mecanismo (ausencia total de corpus compartido montado en este contenedor de nube) es determinista para las 27 entradas `ennvih*` restantes. Las condiciones (1) y (3) verifican limpias contra archivo. La condición (4) verifica, con un margen que queda declarado para que nadie lo hereda a ciegas.

Esto es exactamente "declara qué falta y qué lo desbloquearía" — no fracaso del borrador, que en sus propios términos (llave, falsador, corrección de cita de estrato/UPM) sigue siendo un trabajo sólido.

## 4 · Qué lo desbloquearía

1. **Repetir la verificación (2) desde una sesión donde el corpus compartido sea alcanzable** — una sesión local Ubuntu-con-red (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` vacío/no seteado, patrón de `nota-proceso:7`) o una sesión de nube que sí tenga el volumen de corpus montado — y correr `tests/manifiesto.py --verifica --id <id>` (uno por invocación) sobre las mismas tres entradas citadas arriba hasta obtener `COINCIDE`, no solo repetir lo que este acto ya dejó verificado (1) y (3).
2. **Extender el chequeo `ID-X` de la ficha** con el mismo barrido de escenarios de ICC/pares-de-olas que `tests/calx_g3.py` aplicó a `CRH`, para que la condición (4) quede verificada con el mismo estándar del precedente que la puede matar, no solo con la cota más generosa.
3. Con (1)-(4) las cuatro limpias, el acto de sello mueve el borrador de `forense/notas/` a `forense/` como artefacto propio, con cabecera `ARCHIVO`/`REEMPLAZA A`/`VERIFICAS ASÍ`/`NOMBRE ESTABLE` (`ADR-36(a)`, `gobernanza-v1_15.md:257`) y su propia nota de sello — acto aparte del que corre la estimación (ADR-46: correr contaminaría la sesión contra MxFLS).

## 5 · Perímetro y lo que no se hizo

Tocado: este archivo (nuevo). **No tocado:** `forense/notas/2026-08-04-e-mxfls-ficha-borrador.md` (el borrador queda intacto, no promovido), `forense/notas/2026-08-04-e-mxfls-nota-proceso.md`, `canon/`, `milpa/procedencia.yaml`, `forense/hitoD-preregistro-v2_0.md`, `tests/`. No se corrió ninguna estimación. No se abrió ningún `.dta`/`.zip` de microdato — solo se corrió `tests/manifiesto.py --verifica` (hashea y hace `stat`; no abre contenido, mismo criterio que `tests/manifiesto.py` ya declara para `--escanea`) y se leyeron `.md`/`.yaml` de gobernanza y forense. No se selló ningún ADR — este acto no es `E-ENCIG`; si el sello de la ficha llegara a exigir uno, sería decisión de mesa, no de este acto.

No impidió medir (este acto nunca iba a medir — no corre estimación en ningún desenlace). Contadores movidos: 0.
