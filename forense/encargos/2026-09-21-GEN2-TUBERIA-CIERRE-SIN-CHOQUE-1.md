# ENCARGO · ACTO GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1 · v1.1 · LA LÍNEA L0 SE REPARA SIN PÉRDIDA, SE CONGELA Y QUEDA VIGILADA · LOS CONTADORES DE ADR DEJAN DE EDITARSE · `ADR` PASA A RAÍZ DE ACTO · `union` SÓLO DONDE UNA MUTACIÓN LO JUSTIFIQUE

**Sustituye a la v1.0, que no se lanzó.** Incorpora las cinco críticas de mesa del 21/sep; cada una se verificó contra el repo antes de entrar (§3).

**CABECERA** · redactado contra `9abc7a19` (re-deriva al abrir; si `main` se movió no es PARO) · **ENTORNO: NUBE**, `cloud_default`, con credenciales de Git y publicación de PR; cero microdato. **No es CAJA**: la caja está ocupada por el piloto 3, y lo único que la pedía era una sonda de `gh` que aquí es opcional (P0) · una sola sesión, rama propia (D-17) · **MODO: ABIERTO** · **MODELO SUGERIDO: Opus** · **COMPUERTA: ninguna** — no abre dato, no congela spec, no adopta, y **no borra información**: la reparación se demuestra sin pérdida contra la historia (D-20) · **CONTADOR: `cuenta_gen2 = NO`** · vehículo: `/acto`.

**URGENTE** (§1). **El PR no se fusiona en este acto**: queda propuesto; mesa central fusiona, y puede darle prioridad sobre cualquier otro.

**LOTE (D-11)**, en este orden, que es parte del encargo: **A → B → C → D**. `union` (P-D) sólo es seguro donde, después de A a C, nadie edite una línea compartida en su sitio sin que una guarda lo atrape.

**IDS.** Este acto es **el primero que acuña `ADR` con raíz de acto** —en cuanto P-C esté en su rama—, y por eso su propio `ADR` no se renumerará al fusionar. `NC`/`FP` con raíz, como ya rige.

---

## 1 · POR QUÉ ES URGENTE — `EJECUTADO` por TUBERÍA

`canon/estado-programa-v1_14.md`, la «ÚNICA FUENTE DE ESTADO vigente», pesa ~27.7 MB, y ~27.2 MB son **una sola línea**: la L0 (`**L0 · Gobierno — completo y al día.** N ADR (…`).

- **Casi todo son copias.** 47 785 anotaciones, **273 textos distintos**, 185 ADR. Con cada anotación una vez ocuparía ~230 KB: **más del 99 % es repetición**.
- **Causa: merges que conservan «los dos lados» de una línea que editan todos.** Cada acto inserta su anotación y reconcilia su conteo en esa misma línea; dos ramas chocan en una línea, y «conservar ambos» concatena la línea entera. En el primer padre de `main`: 797 824 caracteres el 20/sep a las 16:48 → **×2.00** en `#929` → **×3.00** en `#936` → **×2.67** en `#938` → **×2.12** en `#947` → 27.2 M hoy.
- **Nada lo detecta.** La suite pasa en VERDE con esta línea.
- **Plazo.** Una o dos duplicaciones más superan 100 MB, y GitHub rechaza el empuje de archivos de más de 100 MB *(límite documentado por GitHub; `SUPUESTO`, no verificado en esta sesión)*. Todas las ramas contienen este archivo.
- **Y hay ramas en vuelo que cargan la línea vieja** (`EJECUTADO`, `origin`, al redactar): `acto/gen2-celda-d-piloto-3-commit-2-3-v1_3` y `claude/tramite-2026-09-21-b`, ambas con la línea de ~27 MB y el `acto.md` con la regla vieja. Mesa reporta cuatro; las otras dos no están empujadas a `origin`. **Cuando fusionen `main` después de este acto van a chocar en la L0**, y si conservan los dos lados meten 27 MB encima de la línea reparada. Por eso la reparación sin guarda no basta (P-A.4).

## 2 · FIRMA DE MESA, verbatim (21/sep/2026)

> «La línea L0 de estado-programa deja de escribirse a mano: se deriva por comando, como el tablero, o se escribe en un fragmento por acto. Los ids de ADR, NC y FP pasan todos a raíz de acto (D-2, ya en uso desde #939 con FP-260921-…); la forma se congela ya y no se renumera nunca más. Lo que se añade a los archivos de gobierno deja de poder chocar entre PR; TUBERÍA elige el mecanismo.»

**No está todavía en el repo: este acto la asienta en P0 (A.12).** Sustituye la secuencia de la firma 1 del 20/sep («ADR después, con careo propio»); el careo del esquema de `NC`/`FP` ya estudió el mecanismo y la forma es la misma.

**Autorización que se deriva de la firma** («TUBERÍA elige el mecanismo»): los sitios de mecanismo que la firma nombra —en `.claude/commands/acto.md`, el paso de recifrado L0, el paso de la entrada nueva de gobernanza y la regla de renumeración (línea 353 al redactar)—; `tools/cierre_acto.py`; y los consumidores que leen números de `ADR`. **Nada más de `acto.md`.**

## 3 · LO QUE TUBERÍA SABE — con rótulo, incluidas las críticas de mesa verificadas

- `EJECUTADO` · las cifras de §1; 22 commits de renumeración en 12 horas; el PR #955 renumeró su `ADR` cuatro veces en 40 minutos.
- `LEÍDO` · **quién edita en su sitio:** el paso «Recifrado L0» de `acto.md` manda insertar a mano la anotación en la L0 y reconciliar con `cierre_acto.py --aplica` **tres contadores** —el conteo de la propia L0 (`cierre_acto.py:149`, `L0_ADR_RE`), la cabecera `**N ADR**` de gobernanza (línea 2, `:145`) y la fila `gobernanza` de la tabla §0 de `estado-programa`—.
- `LEÍDO` · **dónde entra un `ADR`:** `canon/gobernanza-v1_15.md` §4, arriba. Asignador: `cierre_acto.py`, `max+1`.
- `EJECUTADO` · **consumidores** de la L0, de los contadores o de números `ADR`: 21 archivos en `tools/`, `tests/` y `.claude/commands/`. **46 171 citas** `ADR-<n>`: con el esquema prospectivo no se toca ninguna.
- `LEÍDO` · **la forma congelada** de `NC`/`FP` desde `#939`: `<PREFIJO>-<AAMMDD>-<RÓTULO>-<4 hex del 0-bis>-<NN>`. **`ADR` adopta la misma.**
- `LEÍDO` · **`T47`** (`tests/check.py:7748-7812`, `_T47_REGISTROS`) exige ids únicos en `forense/no-corrido.tsv` y `forense/firmas-pendientes.tsv`, y nació de un duplicado real (crítica 2 de mesa: **confirmada**). **`canon/registro-rotulos.tsv` y `canon/gobernanza-v1_15.md` no tienen guarda equivalente**: `T15` sólo atrapa encabezados de `ADR` repetidos, no líneas repetidas dentro de una entrada.
- `LEÍDO` · **`no-corrido.tsv` y `firmas-pendientes.tsv` se editan en su sitio por diseño**: al marcar una firma FIRMADA (A.12) y al cerrar una `NC` (crítica 2: **confirmada**). Si una rama edita la última fila y otra añade debajo, `union` deja la fila dos veces, con dos estados.
- `EJECUTADO` · **la regla «renumera quien fusiona segundo» vive en `.claude/commands/acto.md:353`** (normativo) y en las instrucciones v2.15 (§6, cabecera del encargo). **En `forense/encargos/PLANTILLA-ENCARGO-v2_0.md` no aparece**: cero coincidencias de «renumer» o «fusiona segundo». La crítica 5 de mesa **no se sostiene para la plantilla**: no hay línea que cambiar ahí. La línea de las instrucciones va como semilla de v2.16, y la lleva mesa. `forense/agente-revisor-v1_0.md:102` la menciona como relato de un caso, no como regla: no se toca.
- `EJECUTADO` · **47 versiones** de `estado-programa` en el primer padre de `main` desde el 19/sep: es el universo de la prueba histórica de no-pérdida (crítica 3).
- `LEÍDO` · **el texto de la línea que no es anotación**: un encabezado (`**L0 · Gobierno — completo y al día.** N ADR (`) y un cierre (`…)*`). Se conserva.
- `SUPUESTO` · no sé si `main` exige ramas al día. P0.

## 4 · YA HECHO — por OBJETO (A.8)

Reparación o guarda de la L0: **NO-ENCONTRADO**. `ADR` con raíz de acto: **NO-ENCONTRADO** (el esquema existe para `NC`/`FP` y su test de gramática vive en `tests/test_tuberia_ids_union.py`). Guarda de tamaño de línea en `canon/`, o de líneas repetidas en archivos `union`: **NO-ENCONTRADO**.

## 5 · PIEZAS — resultado esperado, no receta

**P0 · 0-bis, firma y sonda.** Este encargo verbatim **desde el archivo `.md` recibido**, con su sello de cuerpo. Chequeo de duplicado por contenido. **Asienta la firma de §2 verbatim** (A.12). Si la sesión tiene `gh` con credenciales, sonda si la protección de `main` exige ramas al día; **si no lo tiene, no es PARO**: queda como pregunta a mesa en la nota, porque la respuesta sólo afecta cuánto baja la meta de re-fusiones (§8).

**P-A · La línea L0: reparada, demostrada, congelada y vigilada.**

1. **Reparación.** Cada anotación distinta una sola vez, en el orden de su primera aparición, **conservando el encabezado y el cierre** de la línea.
2. **Prueba de no-pérdida contra la historia** (crítica 3), por comando y con salida cruda en la nota. Se unen las anotaciones de **las 47 versiones** de la línea en el primer padre de `main` desde el 19/sep —si el volumen lo impide, como mínimo la versión anterior y la posterior a cada salto (×2, ×3, ×2.67, ×2.12) y la cabeza, **declarando cuáles**—, y **toda anotación que aparezca en alguna de ellas debe estar en la línea reparada**. Así se detecta no sólo lo duplicado, sino lo que una resolución de conflicto haya perdido tomando un solo lado. Si falta alguna, **se restaura desde la versión donde aparece** y se declara en hallazgos, con la versión. La segmentación en anotaciones la deriva el ejecutor; la de TUBERÍA (`` `ADR-<n>` `` como inicio de cada anotación, 273 textos distintos en la cabeza) es **referencia para comparar, no valor esperado**.
3. **Congelamiento.** El contenido reparado queda como **histórico**, y la línea L0 de `estado-programa` pasa a ser **un puntero corto**: las anotaciones posteriores viven en fragmentos. Dónde vive el contenido histórico —un archivo propio bajo `canon/L0/`, sellado, o la propia línea— lo decide el ejecutor; **lo que no es negociable es P-A.4**.
4. **Las dos guardas permanentes, en CI** (crítica 1), cada una probada por mutación:
   - **Ninguna línea de ningún archivo de `canon/` supera 1 MB.** Es el criterio 2 de la v1.0 convertido en test.
   - **El hash del contenido histórico congelado está fijado.** Es una constancia congelada a propósito, no un libro vivo. Si una rama lo toca —por ejemplo, conservando los dos lados de la L0 al fusionar `main`—, el CI falla **con un mensaje que diga qué hacer**: *«la L0 histórica cambió; si fusionaste `main` y chocó la L0, toma la versión de `main` completa y pon tu anotación en `canon/L0/<tu ADR>.md`»*.
   - La mutación de prueba es **exactamente el caso de las ramas en vuelo**: fusionar una rama con la línea de 27 MB sobre la línea reparada, conservando ambos lados. Las dos guardas deben fallar.
5. **Fragmentos.** Desde este acto, cada acto escribe su anotación L0 en `canon/L0/<ADR-raíz-del-acto>.md`. La vista completa —histórica más fragmentos— se obtiene **por comando** (en `cierre_acto.py` o en la herramienta del tablero); **no se escribe a un archivo compartido**.

**P-B · Los tres contadores dejan de editarse.** Quedan con su valor al congelar, **marcados como históricos**, con un puntero al comando que da el conteo vigente. `cierre_acto.py --aplica` deja de escribirlos. `T15` sigue verificando toda cifra vigente que se cite; si no queda ninguna, lo dice.

**P-C · `ADR` con raíz de acto.**
1. **Forma**, congelada por la firma: `ADR-<AAMMDD>-<RÓTULO>-<hhhh>-<NN>`. Prospectivo: ningún `ADR` existente cambia; ninguna cita se reescribe.
2. **Asignación:** `cierre_acto.py` deja de calcular `max+1` y deriva la raíz del commit de 0-bis, que existe antes de acuñar.
3. **Consumidores:** todo lo que parsea números de `ADR` —`T15`, `estado_comun.py`, `tablero_programa.py`, las recetas de `revisa.md` y los demás del censo— acepta **las dos épocas**, probado con un test que pina **un `ADR` de cada época en el mismo caso**; el test de gramática de `tests/test_tuberia_ids_union.py` se extiende a `ADR`.
4. **`acto.md:353`** («renumera quien fusiona segundo») se sustituye por: *un id con raíz de acto no se renumera nunca; un id numérico acuñado antes del cierre que choque se re-acuña con raíz*.
5. **La entrada nueva de gobernanza** sigue en §4, con `ADR` de raíz y **sin tocar la cabecera** (P-B).

**P-D · `union` sólo donde una mutación lo justifique** (crítica 2).
1. **Candidatos:** `canon/gobernanza-v1_15.md`, `forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv`, `canon/registro-rotulos.tsv`. **Fuera sin discusión:** `data/corrida0/decisiones.tsv` (superficie de firma de mesa: sus conflictos deben seguir siendo ruidosos) y `hitoD-preregistro` (ya excluido por sus contadores).
2. **Una prueba por mutación por candidato, del caso exacto:** una rama edita **en su sitio** la última fila o entrada (marca FIRMADA, cierra una `NC`, enmienda un `ADR`); otra rama **añade** debajo; se fusiona con `union`. **Si una guarda existente falla** —`T47` para los dos TSV que cubre; la que corresponda para los otros—, el archivo **entra** a `union`. **Si ninguna guarda lo atrapa, el archivo queda fuera de `union` hasta el sucesor**, y la nota dice por qué. Según `T47` y `T15` tal como están, lo esperable es que entren los dos TSV y queden fuera gobernanza y rótulos; **lo decide la mutación, no esta línea**.
3. **La guarda de líneas repetidas** en los archivos que sí entren a `union`: falla si una línea de 200 caracteres o más aparece dos veces o más. La lista se deriva de `.gitattributes`, como hace `T46`.
4. Riesgo residual, **declarado, no instrumentado**: dos ramas que enmiendan a la vez la misma línea con textos distintos en un archivo `union`.

**P-E · Cierre.** La cascada con el mecanismo nuevo —es la primera vez, y es la prueba—. `python3 tests/check.py --baseline --parallel` en **LÍNEA BASE VERDE**. `## NO-CORRIDO / RESERVAS` al **final** del encargo; `## CONSUMIDO` con el PR real. Hallazgos: la L0 con sus cifras; la tabla de P-D con el veredicto de cada archivo; y como **semilla PARA-v2.16**, *una línea que editan todos los actos no puede vivir en un archivo compartido*. Y una línea que se anota sin arreglo: **los blobs de 0.8, 1.6, 4.7, 12.8 y 27 MB se quedan en la historia de git para siempre** —el acto no reescribe la historia—; el CI, que clona con profundidad 1, no los sufre; los clones completos sí.

## 6 · CRITERIO DE «HECHO» — por comando, con salida cruda en la nota

1. `canon/estado-programa-v1_14.md` pesa menos de 1 MB, y **la prueba de no-pérdida contra la historia pasa**, con el número de versiones examinadas.
2. **Las dos guardas de P-A.4 están en CI**, y la mutación de la rama en vuelo las hace fallar a las dos, con el mensaje que dice qué hacer.
3. Este acto acuñó su propio `ADR` con raíz, y al fusionar `main` **no renumeró nada**.
4. `cierre_acto.py --aplica` no escribe la L0 ni los tres contadores (verificado con `git status` tras correrlo).
5. El test que pina un `ADR` de cada época pasa, y `T15` reconoce las dos.
6. La tabla de P-D: cada candidato con su mutación y su veredicto; **ningún archivo en `union` cuya mutación no atrape una guarda**.
7. Suite en LÍNEA BASE VERDE.

## 7 · LATITUD

El cómo es tuyo. Un obstáculo reversible y barato se resuelve y se declara (D-19). Si `main` se mueve, fusiona hacia la rama: **si choca la L0, no se conservan los dos lados** —se toma la de `main`, se repara con P-A y la anotación propia va como fragmento—.

## 8 · LO QUE LOGRA DE LAS METAS DE DIRECCIÓN, Y LO QUE NO

**Logra:** PR con renumeración → **0** por construcción; la L0 y los contadores dejan de chocar, y no pueden volver a inflarse sin que el CI lo diga; los conflictos de los archivos que entren a `union` se resuelven solos en la fusión local. **No logra por sí solo** la meta de re-fusiones: si `main` exige ramas al día, un PR sigue fusionando `main` cada vez que otro entra, y el botón de GitHub no aplica `union`. Eliminar la re-fusión exige que los actos sólo **añadan archivos nuevos** a gobierno: es el sucesor.

## 9 · PAROS — lista cerrada

Perder cualquier anotación que aparezca en alguna versión histórica de la línea · reescribir un `ADR`, `NC` o `FP` existente o cualquiera de las 46 171 citas · poner `union` a un archivo cuya mutación de edición-en-sitio no atrape ninguna guarda · tocar `decisiones.tsv` o `hitoD-preregistro` · editar `acto.md` fuera de los tres sitios de §2 · reescribir la historia de la rama · abrir microdato · objetivo inalcanzable. **Fuera de esta lista no se para** —en particular, no tener `gh` no es PARO—.

## 10 · PERÍMETRO

Escribes en: `canon/estado-programa-v1_14.md` (la línea L0 y la fila §0) · `canon/L0/` (nuevo) · `canon/gobernanza-v1_15.md` (la cabecera de conteo y la entrada nueva de este acto) · `tools/cierre_acto.py` · los consumidores que parsean números de `ADR` (derivados por grep, listados en la nota) · `tests/` (`check.py` en `T15` y las guardas nuevas; `test_cierre_acto.py`, `test_tuberia_ids_union.py` y los tests de los consumidores) · `.github/workflows/verify.yml` (sólo los pasos de las guardas nuevas) · `.gitattributes` · `.claude/commands/acto.md` (los tres sitios de §2) · `forense/encargos/`, `forense/notas/`, `forense/hallazgos.md`, `forense/no-corrido.tsv` · y lo que asienta la firma (P0). Más el perímetro de cierre permanente (D-21). **Si te encuentras escribiendo fuera de esta lista, PARA.**

## 11 · LO QUE NO HACE · SUCESORES

No migra ningún id existente · no convierte gobernanza ni los TSV en un archivo por entrada · no cambia el texto de ninguna anotación, sólo quita sus copias y restaura lo perdido · no toca la plantilla de encargos (no contiene la regla) ni las instrucciones (semilla de mesa) · no reescribe la historia · no fusiona su propio PR. **Sucesor:** un archivo por entrada para todo lo que los actos añaden a gobierno, que es el que elimina la re-fusión, incluidos los archivos que P-D deje fuera de `union`.

## 12 · FALSADOR (§9)

Si en dos semanas hay un solo commit de renumeración de un id con raíz de acto, o alguna línea de `canon/` vuelve a pasar de 1 MB sin que el CI lo haya atrapado, el mecanismo no hace lo que dice y se revisa.
