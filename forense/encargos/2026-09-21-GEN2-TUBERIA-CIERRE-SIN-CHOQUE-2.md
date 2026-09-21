# ENCARGO · ACTO GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2 · EL REGISTRO DE RÓTULOS DEJA DE CHOCAR · `estado-programa` DEJA DE TOCARSE EN CADA CIERRE · Y SE ASIENTAN LAS CUENTAS PENDIENTES DE `#962`

**CABECERA** · redactado contra `fc13cdcc` (merge de `#962`; re-deriva al abrir; si `main` se movió no es PARO) · **ENTORNO: NUBE**, `cloud_default`, con credenciales de Git y publicación de PR; cero microdato; no usa la API de GitHub · una sola sesión, rama propia (D-17) · **MODO: ABIERTO** · **MODELO SUGERIDO: Opus** · **COMPUERTA: ninguna** (D-20) · **CONTADOR: `cuenta_gen2 = NO`** · vehículo: `/acto`.

**EL PR NO SE FUSIONA EN ESTE ACTO**: queda propuesto; mesa central fusiona.

**IDS.** Todo con raíz de acto, `ADR` incluido (`#962`): `ADR-<AAMMDD>-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-<hhhh>-<NN>`. Este acto **no renumera nada**; si al fusionar `main` choca algo, se resuelve por el mecanismo, no a mano.

---

## 1 · FIRMA QUE LO HABILITA, verbatim (21/sep/2026, asentada por `#962`)

> «La línea L0 de estado-programa deja de escribirse a mano: se deriva por comando, como el tablero, o se escribe en un fragmento por acto. Los ids de ADR, NC y FP pasan todos a raíz de acto (D-2, ya en uso desde #939 con FP-260921-…); la forma se congela ya y no se renumera nunca más. Lo que se añade a los archivos de gobierno deja de poder chocar entre PR; TUBERÍA elige el mecanismo.»

Autoriza a este acto sobre los sitios de mecanismo que la firma nombra: `.gitattributes`, las guardas de la suite, y en `.claude/commands/acto.md` **sólo** los pasos de la cascada que escriben en `estado-programa` o en el registro de rótulos.

## 2 · LO QUE TUBERÍA MIDIÓ — `EJECUTADO` contra `fc13cdcc`

- **`#962` cumplió.** `estado-programa` bajó de 27.7 MB a **550 KB**; la línea más larga de `canon/` es de 92 KB. Las guardas `T48` (ninguna línea de `canon/` supera 1 MB), `T49` (hash del histórico fijado) y `T50` (líneas repetidas en archivos `union`) están en la suite, y sus mutaciones en `tests/test_tuberia_ids_union.py`, que el CI corre. `cierre_acto.py --aplica` corrido sobre `main` deja **cero** archivos modificados. Suite en LÍNEA BASE VERDE en **167 s** —antes de `#962`, 228 s en el mismo entorno: la línea de 27 MB también frenaba la suite—.
- **La prueba de no-pérdida de `#962` examinó 5 versiones**, por debajo del mínimo que pedía su encargo (las de antes y después de cada salto). **TUBERÍA la rehízo sobre las 49 versiones distintas** de la línea L0 en el primer padre de `main` desde el 19/sep: **149 fragmentos distintos, los 149 presentes en `canon/L0/HISTORICO.md`**, comprobado con tres trozos del medio de cada fragmento. No se perdió nada; falta asentarlo (P0).
- **El mapa de lo que sigue chocando.** En los 198 PR fusionados a `main` en 7 días, los archivos **existentes** que más PR modifican: `canon/gobernanza-v1_15.md` 49 % *(ya `union`)*, `forense/no-corrido.tsv` 49 % *(`union`)*, **`canon/registro-rotulos.tsv` 47 % — sin `union` y sin guarda**, `forense/hallazgos.md` 32 % *(`union`)*, `forense/firmas-pendientes.tsv` 27 % *(`union`)*, **`canon/estado-programa-v1_14.md` 25 %**, `tests/check.py` 22 %, `data/corrida0/corridas.tsv` 17 %, `data/corrida0/resultados.tsv` 16 %.
- **`registro-rotulos.tsv`, de cerca.** 436 líneas. De los PR recientes que lo tocan, **35 sólo añaden filas y 4 editan una existente**. Su identidad natural es el par `(espacio, valor)`: ningún test exige que sea único. Por eso `#962` lo dejó fuera de `union`, con razón. **Y trae un defecto de forma:** su primera línea es una fila de datos (`C · MAESTRA33-C4 · …`) y la cabecera (`espacio · valor · que_significa · donde_vive`) está en la **segunda**.
- **`NC` que `#962` podría haber cerrado**, candidatas a verificar: `NC-260921-GEN2-TUBERIA-SIDECAR-CUERPO-1-3d08-03` (el hueco que deja el asignador de `ADR`: sin `max+1`, ya no aplica) y `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-04` (recetas que derivan el máximo numérico: `#962` tocó `revisa.md`, **no** `tools/tablero_programa.py:517`). Y dos que quedaron sin objeto: `…6e60-05` (evaluar el esquema C: **sustituido** por la raíz de acto que ya rige) y `…6e60-08` (la diferencia de dos filas `FP`: fue un conteo de líneas en vez de filas, de TUBERÍA).
- **`SUPUESTO`** · no se sabe si `main` exige ramas al día; `#962` no pudo sondearlo desde la nube. **Mesa lo contesta** o queda como pregunta: no es PARO.

## 3 · PIEZAS — resultado esperado, no receta

**P0 · 0-bis y asientos.** Este encargo verbatim **desde el `.md` recibido**, con su sello de cuerpo. Chequeo de duplicado por contenido. Luego:
1. **La prueba de no-pérdida sobre las 49 versiones**, re-corrida por este acto con su propio comando y su salida cruda en la nota, asentada en hallazgos como complemento de `#962`.
2. **Las cuatro `NC` de §2**: cada una se **cierra con su evidencia** —el comando que muestra que ya no aplica— o se deja abierta diciendo qué falta. `…6e60-04` sólo se cierra si `tablero_programa.py:517` también dejó de derivar el máximo numérico; si no, se arregla aquí (defecto adyacente de ≤10 líneas, D-21) o se deja abierta con el diff.

**P1 · `registro-rotulos.tsv` deja de chocar, por la misma regla que usó `#962`.**
1. **La forma primero:** la cabecera vuelve a la primera línea y la fila de datos que estaba ahí pasa a su lugar, **sin perder ni cambiar ninguna fila** —mismo conjunto de filas antes y después, verificado por comando—. Antes de moverla, confirma que ningún lector del archivo dependía de ese orden.
2. **La guarda:** el par `(espacio, valor)` es único. Extiende `T47` o añade la guarda equivalente; si hoy hay pares repetidos, **no se borra ninguno**: se listan y se declaran como estado, y la guarda falla sólo sobre repeticiones **nuevas**, con la lista actual congelada como exención.
3. **La mutación de `#962`**, con el caso exacto: una rama edita en su sitio la última fila, otra añade debajo, se fusiona con `union`, y la guarda nueva **debe fallar**. Si falla, el archivo **entra** a `merge=union`; si no, queda fuera y la nota dice por qué.
4. `T46` y `T50` lo cubren solos en cuanto entre a `.gitattributes`.

**P2 · `estado-programa` deja de tocarse en cada cierre.** Tras `#962`, un cierre estándar ya no escribe la L0 ni los contadores. **Mide qué más escribe todavía un acto en `canon/estado-programa-v1_14.md`** —en los PR posteriores a `#962` y leyendo los pasos de `acto.md` que lo mencionan—. Cada escritura que quede recibe el mismo trato que la L0: fragmento por acto o vista por comando. **Criterio:** una cascada de cierre corrida sobre un acto sintético no modifica `estado-programa` (verificado con `git status`).

**P3 · Lo que queda fuera, medido y dicho.** No se toca, pero la nota lo deja con cifras para el sucesor:
- **Las vistas derivadas** (`corridas.tsv`, `resultados.tsv` y compañía, 16-17 % de los PR). Chocan porque cada acto que sella las re-deriva. Cambiar eso toca E.7 —«toda corrida sellada entra a la vista en el mismo acto que la sella»—, que es una regla de instrucciones: **decisión de mesa**.
- **`tests/check.py`** (22 %): los actos añaden su test a una sola lista de registro. Es código: `union` no le sirve.

**P4 · Cierre.** Cascada, `python3 tests/check.py --baseline --parallel` en **LÍNEA BASE VERDE**, `## NO-CORRIDO / RESERVAS` al final, `## CONSUMIDO` con el PR real. La nota lista, por archivo del mapa de §2, si hoy **choca**, **se resuelve solo** (`union` con guarda) o **no se toca** (fragmento o vista).

## 4 · CRITERIO DE «HECHO» — por comando, con salida cruda en la nota

1. La prueba de no-pérdida sobre las 49 versiones pasa y está asentada.
2. Cada una de las cuatro `NC` está cerrada con evidencia o abierta con lo que falta.
3. `registro-rotulos.tsv`: cabecera en la línea 1, mismo conjunto de filas, guarda de unicidad en la suite, su mutación falla, y —si la mutación lo justifica— el archivo está en `merge=union`.
4. Una cascada sobre un acto sintético no modifica `estado-programa`.
5. Suite en LÍNEA BASE VERDE.

## 5 · LATITUD · PAROS · PERÍMETRO

**Latitud:** el cómo es tuyo; un obstáculo reversible y barato se resuelve y se declara (D-19).

**PAROS — lista cerrada:** perder o cambiar una fila de `registro-rotulos.tsv` · borrar un par repetido que ya existe · poner `union` a un archivo cuya mutación no atrape ninguna guarda · tocar las vistas derivadas o E.7 · editar `acto.md` fuera de los pasos de §1 · reescribir la historia · abrir microdato · objetivo inalcanzable.

**Perímetro:** `canon/registro-rotulos.tsv` · `canon/estado-programa-v1_14.md` y `canon/L0/` (sólo lo que P2 migre) · `.gitattributes` · `tests/check.py` (la guarda nueva) · `tests/test_tuberia_ids_union.py` · `tools/tablero_programa.py` (sólo si P0 lo exige) · `.claude/commands/acto.md` (los pasos de §1) · `forense/encargos/`, `forense/notas/`, `forense/hallazgos.md`, `forense/no-corrido.tsv` · y la cascada. Más D-21. **Si te encuentras escribiendo fuera de esta lista, PARA.**

## 6 · FALSADOR

Si en dos semanas `registro-rotulos.tsv` sigue apareciendo en conflictos de fusión, o un cierre vuelve a modificar `estado-programa`, el mecanismo no hizo lo que dice.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| **P3 · las vistas derivadas de `corrida0`** (`data/corrida0/corridas.tsv` 8 PR / 12.9 %, `data/corrida0/resultados.tsv` 7 PR / 11.3 %, re-derivado aquí sobre 62 merges de primer padre desde el 14/sep) | `DECISIÓN-DE-MESA-PENDIENTE` — el propio encargo las pone en su lista cerrada de PAROS, y cambiarlas toca **E.7** de las instrucciones («toda corrida sellada entra a la vista en el mismo acto que la sella»), que no se enmienda desde un acto | Dos vistas siguen produciendo conflicto de fusión en ~12 % de los PR. Ningún contador de programa se mueve por esto | mesa — decisión sobre E.7; después, acto sucesor de TUBERÍA (`NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-01`) |
| **P3 · `tests/check.py`** (12 PR / 19.4 %) | `FUERA-DE-PERÍMETRO` — es del **acto sucesor de TUBERÍA sobre el registro de tests**: es código, no un registro append-only, así que `merge=union` no le sirve, y partir su lista única de registro es un cambio de arquitectura de la suite, no un defecto adyacente de ≤ 10 líneas | La suite sigue siendo fuente de conflicto en ~19 % de los PR. Ninguna medición se afecta | `NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-02` — acto sucesor de TUBERÍA, `SIN-ASIGNAR` |
| **`forense/analisis/ci-guardias/censo-tests.tsv`** (14 PR / 22.6 %) — **hallazgo nuevo de este acto**: séptima fuente de choque del árbol, por delante de `tests/check.py`, y el mapa de §2 del encargo no la nombra | `FUERA-DE-PERÍMETRO` — es del **mismo acto sucesor que trate las vistas derivadas** (es una vista derivada por `tools/ci_guardias.py --censo`, misma clase que las de `corrida0`); el perímetro de este encargo no incluye `forense/analisis/` ni `tools/ci_guardias.py` | La séptima fuente de choque queda sin tratar y fuera del mapa que dirección usa para priorizar. Ningún contador se mueve | `NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-03` — junto con `…-8e53-01` |
| **§2, última viñeta · el `SUPUESTO` de `#962`: si `main` exige ramas al día antes de fusionar** | `DECISIÓN-DE-MESA-PENDIENTE` — el encargo dice literalmente que mesa lo contesta o queda como pregunta, y que no es PARO. No es observable desde aquí: es configuración del repositorio en GitHub, y la cabecera de este encargo declara que el acto **no usa la API de GitHub** | Los actos siguen sin saber si deben traer `main` antes de pedir merge. No afecta ninguna medición; afecta cuánto cuesta cada cierre | `NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-04` — mesa, una línea |

**Corrido distinto de lo pedido, declarado (D-19, logística — ninguno toca qué se mide ni una firma de mesa):**

1. **P0.1, el universo.** El encargo pide «las 49 versiones distintas de la línea `L0` en el primer padre de `main` desde el 19/sep». `canon/estado-programa-v1_14.md` tiene **44** commits de primer padre en toda su historia y **44** versiones distintas: 49 no es alcanzable. En vez de ajustar el procedimiento para que cuadrara, se corrió sobre el **universo máximo** (`git rev-list --all`: 161 commits, **92** versiones), que lo domina estrictamente. Veredicto idéntico y más fuerte: **SIN PÉRDIDA**, 142/142 fragmentos, 426/426 trozos del medio.
2. **P0.1, los «149 fragmentos».** `#962` no dejó nota ni definición de fragmento. La unidad se **derivó del texto** (una anotación `*( … )*`) y da **142**, no 149. La definición está escrita en la nota junto al comando.
3. **P2, el universo.** El encargo pide medir «en los PR posteriores a `#962`». **No hay ninguno**: `fc13cdc` (el merge de `#962`) es la cabeza de `origin/main`. Se midió sobre los **11** PR de primer padre **anteriores**, más los pasos de `acto.md`.
4. **P0.2, `…-6e60-04`: se arregló, no se dejó abierta.** El encargo preveía las dos ramas. `tools/tablero_programa.py:517` seguía derivando el máximo del espacio cerrado y publicándolo como `adr_max`/`fp_max`; al verificarlo apareció que el defecto **ya se había materializado** en `tools/estado_comun.py::fp_max` (FP fantasma `260921`). Las dos correcciones son de ≤ 10 líneas cada una y sin ellas la `NC` no podía cerrarse con evidencia: **D-21**, se arreglan y se declaran. `tools/estado_comun.py` no está en la lista del perímetro; se declara aquí explícitamente.
5. **Censo de rótulos, fila extra.** Además del rótulo propio se censó `GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1`, que **su propio acto (`#962`) no censó** — hueco encontrado al censar el sucesor, una fila añadida, ninguna tocada.

**PAROS:** ninguno. Ninguna de las seis causas de la lista cerrada del §5 del encargo se presentó: no se perdió ni cambió ninguna fila de `registro-rotulos.tsv` (436 → 436 antes de añadir las dos del censo, mismo multiconjunto), no se borró ningún par repetido (los 7 quedan congelados como exención), el archivo entró a `union` **sólo después** de que su mutación hiciera fallar a `T51`, no se tocaron las vistas derivadas ni E.7, `acto.md` se editó sólo en el paso 3 de la cascada (el que escribe en `estado-programa`), no se reescribió historia y no se abrió microdato.

## CONSUMIDO

**PR [#966](https://github.com/Josanoforo/Modelado-Mexicano/pull/966)** ·
`ACTO GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2` ·
`ADR-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-01` · 21/sep/2026 · NUBE
(`cloud_default`), Opus 5, MODO ABIERTO, COMPUERTA: ninguna, cero microdato ·
**CONTADOR: `cuenta_gen2 = NO`** · rama `claude/untitled-session-gowmwp`,
0-bis `8e53c0e`.

**El PR queda PROPUESTO, no fusionado: el merge es de mesa** (instrucción
explícita de este encargo).

Los cinco criterios de «hecho» del §4, cumplidos por comando: (1) prueba de
no-pérdida **SIN PÉRDIDA** sobre el universo máximo (161 commits, 92 versiones,
142 fragmentos, 426/426 trozos del medio) y asentada en `forense/hallazgos.md`;
(2) las cuatro `NC` **CERRADAS** con evidencia —`…-6e60-04` por arreglo: `fp_max`
devolvía el FP fantasma `260921`—; (3) `canon/registro-rotulos.tsv` con cabecera
en la línea 1, 436 → 436 filas, guarda `T51`, mutación `G3-bis`/`G3-ter`
fallando como debe, y `merge=union` en `.gitattributes`; (4) `cierre_acto.py
--aplica` deja `estado-programa` sin tocar, ahora de forma permanente bajo `T52`;
(5) suite en **LÍNEA BASE VERDE**, sin FAIL nuevos.

Nota de cierre:
`forense/notas/nota-2026-09-21-gen2-tuberia-cierre-sin-choque-2-cierre.md`.
