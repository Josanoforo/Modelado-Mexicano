# ACTO RES · la reserva de encuadre de género (ADR-67(b)) — adjudicación, sella ADR-75

**Acto:** ACTO RES · **Entorno:** repo-only, `cloud_default`, sin `data/raw`, sin sonda HTTP (no aplica) · **SHA de redacción del encargo:** `fd788a9` (`origin/main`) · **Depende de:** ADR-67(b) (`canon/gobernanza-v1_15.md:866`, sellado 10/ago) y `forense/notas/2026-08-13-enasic-split-verificacion.md` (fusionado antes de este acto). Este acto no corre ningún diseño, no estima nada, no abre ningún payload — adjudica sobre resultados ya calculados y verificados por actos previos.

## §0 · ARRANQUE

1. **REPO.** Clon existente en uso: `/home/user/Modelado-Mexicano`. `git log -1`: `fd788a9 Merge pull request #211 from Josanoforo/claude/registro-efimeros-forense-mm9sra`. `git status`: rama `claude/new-session-b0pwaf` (la designada), árbol limpio. Ningún clon nuevo.
2. **SHA.** `origin/main` = `fd788a9`, idéntico al declarado por el encargo — sin divergencia, no hizo falta refrescar.
3. **data/raw.** Ausente (`test -d data/raw` → no existe) — declarado por el encargo como no necesario para este acto; confirmado y saltado.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`. Sonda HTTP saltada — el encargo declara que este acto no toca microdato ni red.
5. **ESPEJO.** Ninguna cifra de este acto sale de otro sitio que no sea este clon, comando a la vista en cada caso.
6. **Colisión.** `git fetch origin gu/gdelt-ucdp-recon`: 6 commits sin fusionar sobre `origin/main`, ninguno toca `canon/` (verificado: rama de recomposición GDELT/UCDP, ajena a `celdas-d`/`gobernanza`/`modelo-decision`). No colisiona con el perímetro de este acto.

## §1 · Verificación de la premisa de §0 del encargo

El encargo afirma que firmar la enmienda de ENASIC-SPLIT **no** mueve `condicionales 9 → 10 de 14`, y que son dos decisiones distintas. Verificado directo contra `forense/notas/2026-08-13-enasic-split-verificacion.md`:

- §6, verbatim: *"No se resolvió la reserva de encuadre de género de `P7_12_7` (`requiere_decision_mesa: true` sigue como está)."*
- §4 (el diff propuesto) no toca `requiere_decision_mesa` — desdobla `P6_38` en medida propia y renombra la θ atitudinal, nada más.
- §5, verbatim: `obligación_medida`, si mesa la registra como condicional nueva, sería "un **cambio de denominador** (`D` pasaría de 14 a 15)".

Confirmado en archivo: `data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml:95` (antes de este acto) → `requiere_decision_mesa: true`; línea 91 → `estado_operativo: PENDIENTE`. Celda hermana `G5.radio_confianza.encuci_vs_enbiare.yaml:169,171` → `LISTO`/`false` — el contraste que fija el criterio. **Premisa confirmada.** Mesa firma dos cosas, en orden, y puede firmar la primera sin la segunda — este acto firma las dos.

## §2 · Cascada de `N de 14` — derivada antes de decidir nada

```
grep -rn "de 14" README.md canon/*.md | grep -vE "\{cita-historica\}|\{cita-ilustrativa\}"
```

Salida cruda comparada contra los 13 sitios que el encargo declara verificados. Coincide, con una reconciliación necesaria: `gobernanza-v1_15.md:938` **no** aparece en la salida cruda del comando (el filtro `-v` descarta la línea completa porque comparte renglón físico con `` `71 ADR` {cita-historica} `` — una cita histórica ajena, no relacionada con `condicionales`), pero sí contiene una mención vigente y legítima de `9 de 14` dentro del propio texto sellado de ADR-71 ("Cascada — historia completa de la numeración"). Verificado leyendo la línea directo: el filtro produce un falso negativo por-línea, no una discrepancia de terreno — `gobernanza-v1_15.md:551` ("No mueve `8 de 14`...") es el caso contrario y correcto: cifra histórica real (anterior a la corrección 8→9 del 4/ago), nunca debió incluirse, y no se incluye. **Nada se movió entre la redacción del encargo y este acto** — la reconciliación explica el hueco aparente, no lo corrige.

## §3 · Decisión A — adjudicación de la reserva

**Firma: `RESUELTA-ACOTA`.** Razonamiento:

1. **ENASIC-SPLIT cierra la vía de "esperar más dato".** Confirmó lectura (ii) sobre `P7_12_7`: fórmula única, capturada como una sola cadena por persona, sin marca de qué paréntesis ("a la mujer"/"al hombre") se leyó — no hay manera de reconstruir una partición por sexo del informante con este instrumento. La reserva ya no espera evidencia nueva.
2. **El reactivo, pese a eso, sigue siendo un enunciado normativo marcado por género, no una creencia genérica.** Texto verbatim (`enasic_2022_fd.xlsx`, fila 713, vía §2.1 de ENASIC-SPLIT): *"Se debe enseñar a la mujer (al hombre) que su deber es cuidar a los padres, cónyuge, hijas e hijos."* Es un enunciado sobre quién **debe** cargar el deber de cuidar, diferenciado por el sexo del sujeto enseñado — no un autorreporte ni una creencia de obligación familiar sin marca de género.
3. **El propio criterio de separabilidad de ENASIC-SPLIT (§1.3.b) ya nombra este constructo con precisión:** *"norma de género: creencia normativa/general sobre quién debe cargar un deber de cuidado, dirigida a una tercera persona genérica según su sexo."* Y la Decisión B (abajo, firmada en el mismo acto) independientemente propone renombrar esta misma medida a `norma_de_género` — dos líneas de razonamiento distintas llegando al mismo límite de constructo.
4. **Por qué no `RESUELTA-ADMITE`:** admitir la θ (0.6933, IC95 [0.6725,0.7140], n=5,579) bajo la sola etiqueta `familismo_obligacion`, sin restricción, dejaría un nombre de generador genérico cargando una creencia específicamente marcada por género — exactamente el defecto que la reserva existía para vigilar (el encargo, verbatim: "admitirlo sin decir qué mide sería exactamente el defecto que la reserva vigila").
5. **Por qué no `NO-RESUELTA-CON-RAZÓN`:** el encargo advierte que la reserva "ya no espera información nueva: espera una firma." No hay una vía de evidencia futura que resolvería esto de otra manera — el contenido del ítem es legible hoy, completo, desde su propio texto y ubicación de sección (Sección 7, "Percepción cultural de los cuidados"). Declarar "no resuelta" sin poder nombrar qué evidencia la resolvería sería exactamente el "eufemismo permanente" que ADR-52 A ya rechazó para otra clase de búsqueda.

**Límite de constructo escrito** (`data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml`, campo `supuesto_transporte`): la θ representa acuerdo con una norma de deber de cuidado diferenciada por sexo, no obligación familiar genérica.

## §4 · Decisión B — enmienda de ENASIC-SPLIT

Firmada **tal cual la propuso** `forense/notas/2026-08-13-enasic-split-verificacion.md` §4 (texto verbatim, sin cambios de mesa) — aplicada como enmienda in situ fechada sobre `canon/gobernanza-v1_15.md:866` (el párrafo (b) de ADR-67), mismo criterio que ADR-48 a ADR-74: la versión no sube, el archivo no se renombra.

**Pregunta del denominador, resuelta como política:** `obligación_medida`, cuando se registre, entra como **condicional nueva** (`D`:14→15), no como sub-componente. Razón: el criterio de separabilidad de ENASIC-SPLIT (§1.3.b, §2.3.b) establece que `norma_de_género` y `obligación_medida` son constructos distintos — una norma-sobre-terceros y un motivo-propio-reportado, no dos facetas de lo mismo. El único precedente real de este modelo para "varias mediciones bajo un mismo casillero de `D`" es `confianza_institucional`, cuyos seis componentes cuentan cada uno su propio lugar en `D` (`modelo-decision-v4_0.md:253`) — y lo hacen porque, aun siendo mediciones distintas, comparten un solo tipo de constructo (confianza en la institución X). `norma_de_género`/`obligación_medida` no comparten ese tipo, y ninguna regla de composición que las fusionara está propuesta en ningún acto de este corpus. Esta es una decisión de política sobre cómo se contará **cuando** `obligación_medida` se registre — no registra la celda-D (pendiente de mesa, fuera de perímetro), no mueve `D` hoy.

## §5 · El contador que NO se movió — hallazgo de perímetro

El encargo declara, sin cita de código: *"Contador que mueve una firma `RESUELTA-*`: condicionales medidas sobre atributos: 9 → 10 de 14. Ninguna otra."* Verificado contra el propio test que el encargo cita para vigilar la cascada (`T19b`, `tests/check.py:869-908`) y contra `README.md:37`, esto **no es correcto tal como está escrito**, y este acto no lo hereda sin verificar:

- `README.md:37` trae su propia procedencia declarada en comentario HTML: `<!-- grep -c 'clase: "MEDIDO·PARCIAL' milpa/procedencia.yaml -->`. El número no es una cifra narrada libremente en `canon/` — es un conteo mecánico sobre `milpa/procedencia.yaml`.
- `T19b`/T-CONTADOR-14-CRUZADO (`tests/check.py:871-908`) hace **tres** verificaciones, no dos: cabecera de `modelo-decision-v4_0.md` == §6.1 == `read("milpa/procedencia.yaml").count('clase: "MEDIDO·PARCIAL')`. El encargo solo describía la primera igualdad.
- `milpa/procedencia.yaml` no tiene, hoy, ninguna línea `clase: "MEDIDO·PARCIAL"` para `familismo_obligacion`/`norma_de_género` — verificado por lectura completa de las 9 líneas que sí la tienen (líneas 135,146,156,180,192,203,232,252,317: los 6 componentes de `confianza_institucional` + `radio_confianza` + `familismo_apoyo` + `exposicion_violencia`). El único rastro de `familismo_obligacion` en ese archivo es `ruta: SIN-RUTA` (`procedencia.yaml:899`) — un campo del **coeficiente**, no de la **condicional**; objetos distintos, ya distinguidos por este mismo corpus (`vocabulario_version: 0.4` en ambas celdas-D).
- `milpa/procedencia.yaml` **no está** en el perímetro que el propio encargo declaró.
- `ADR-68(a)` (`gobernanza:878`) ya tenía la doctrina escrita, sin que el encargo la citara: *"ningún estado de celda-D mueve por sí mismo contadores de canon; promover exige el sello que ya rige (ADR-57(c), ADR-49/51)."*

**Resolución:** el perímetro estaba mal calculado en ese punto específico — se para ahí en vez de escribir en `milpa/procedencia.yaml` fuera de lo declarado (ARRANQUE, regla explícita del encargo). Se ejecutan íntegras las Decisiones A y B (celda-D, `produccion-modelo.tsv`, enmienda in situ, `ADR-75`), y se deja **exactamente donde estaba** todo lo que depende del titular `condicionales 9 de 14`: `README.md:37`, `estado-programa-v1_10.md:97`, `modelo-decision-v4_0.md:11,277,621,725` — sin editar, el número no cambió. `gobernanza-v1_15.md:736,872,904,938,1026,1028` — sin editar: son historia sellada de ADRs previos (`61`,`67`,`68`,`71`,`74`), declaraciones verdaderas en el momento en que cada uno se selló, mismo criterio que ya protege `gobernanza:551` tras el movimiento 8→9 del 4/ago (nunca se reescribió). `gobernanza:952` (alcance de ADR-72, que declara `condicionales 9 de 14` `PROVISIONAL`) — sin editar: no hay movimiento que enmendar todavía. Denominador `D`:14→15 de la Decisión B — decidido como política, no ejecutado, mismo motivo.

**Pendiente, nombrado para acto futuro:** sellar el movimiento de `9 de 14` → `10 de 14` requiere un acto con perímetro propio que alcance `milpa/procedencia.yaml` (añadir la línea `clase: "MEDIDO·PARCIAL(...)"` que hoy falta para esta condicional) y verifique T19b antes/después. Si además mesa registra `G5.obligación_medida` como celda-D, ese mismo acto (u otro) movería `D`:14→15 por la política ya fijada aquí.

## §6 · Lo ejecutado (perímetro respetado)

- `data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml`: `requiere_decision_mesa` true→false, `estado_operativo` PENDIENTE→LISTO, `supuesto_transporte` reescrito a `ACOTADO-CON-SUPUESTO` con el límite de constructo, nota fechada añadida al encabezado. `champion_actual`/`criterio_adjudicacion`/`fecha_adjudicacion` **no tocados** — son del eje BASELINE/CHALLENGER, no de esta reserva (sigue sin haber challenger).
- `data/curacion-registro/produccion-modelo.tsv`: fila `PROD-cca3ea0bccd54d70083728b2` (especificación `ESP-OPACA-B-d13ec4fe`), columna `estado_uso_modelo` `NO_LISTA_DECISION_HUMANA_PENDIENTE`→`LISTA_PARA_USO_MODELO`, columna `requiere_decision` `SI`→`NO`. Editado por script con verificación de valor antes/después (no por sustitución de texto libre) — 51 columnas antes y después, ninguna otra fila tocada.
- `canon/gobernanza-v1_15.md`: cabecera `74 ADR`→`75 ADR`; enmienda in situ fechada sobre el párrafo (b) de ADR-67 (`:866`) con el texto completo de las Decisiones A y B, la pregunta de denominador, y el hallazgo de §5; nueva entrada `ADR-75` insertada tras ADR-74, antes de "## 5. Deuda declarada".
- `canon/estado-programa-v1_10.md`: fila de catálogo `74 ADR`→`75 ADR` (línea 27); narrativa `L0 · Gobierno` (línea 101) extendida con la entrada de `ADR-75`, mismo formato que las 74 anteriores.
- `forense/hallazgos.md`: una entrada nueva, sella el acto y el hallazgo de perímetro de §5, más un hallazgo menor declarado y no perseguido (`modelo-decision-v4_0.md:271` cita "ENUT 6.11/6.11a, M2" como candidato pendiente de `familismo_obligacion` — desactualizado desde ADR-67(b), que fijó `P7_12_7`/ENASIC como la θ real; no se corrige aquí porque la tabla de §1.1.F no se toca en este acto, el titular no cambió).

**No tocados, declarado:** `README.md`, `canon/modelo-decision-v4_0.md`, `milpa/procedencia.yaml`, `data/curacion-registro/especificaciones-produccion.json`, cualquier archivo de `forense/` anterior a este (append-only).

## §7 · Verificación de cierre — dos defectos propios, encontrados y corregidos, no solo declarados

`python3 tests/check.py --baseline`, corrido antes, a mitad y después de todos los cambios — no se asume verde sin correrlo:

- **Antes de editar:** `18 FAIL · 104 WARN` — `LÍNEA BASE: VERDE`. `T15 T-ADR-COUNT`: `[ ok ]`. `T19b contador 14 cruzado (modelo)`: `[ ok ]`.
- Recuento de ADR contra `fd788a9` (receta T15, corrida antes de escribir el primer commit): `únicos: 74 · max: 74 · dups: [] · huecos: []` → siguiente ADR = **75**, sin colisión.
- **Primera corrida tras editar todos los archivos: `LÍNEA BASE: ROJO`, 5 entradas nuevas.** Dos defectos propios de este acto, ninguno del terreno:
  1. `T15 T-ADR-COUNT`: `estado-programa-v1_10.md:101` abre con *"**L0 · Gobierno — completo y al día.** 74 ADR..."* — la cascada de este acto solo tocó el cierre de esa misma línea (el listado histórico) y se saltó esta segunda cita de "74 ADR" al **inicio** de la oración. Corregido a 75.
  2. `T03` (referencias colgantes): la enmienda in situ sobre `gobernanza:866` citó, en un punto, `` `enasic-split-verificacion.md` `` sin el prefijo de fecha — T03 solo resuelve nombres de archivo sin ruta (`` `([A-Za-z0-9_\-áéíóúñÁÉÍÓÚÑ.]+\.(?:md|yaml))` ``, `tests/check.py:218`), y ese basename no existe (el archivo real es `2026-08-13-enasic-split-verificacion.md`). Corregido a la cita con ruta completa, mismo patrón que las otras tres citas de la misma nota en el mismo párrafo.
  3. Las otras 3 entradas (`T16`, autorreferencia de FAIL/WARN vigente en `estado-programa:129,221` y `gobernanza:760,852`) eran consecuencia mecánica de (1)+(2), no un tercer defecto — se resolvieron solas al corregir los dos anteriores, sin tocar esas cuatro líneas.
- **Corrida final, tras los dos arreglos:** `18 FAIL · 104 WARN` — `LÍNEA BASE: VERDE`. Diff byte a byte contra la corrida de antes de editar: **idéntico**. `T15`, `T16`, `T19b` los tres `[ ok ]`.

Ningún archivo fuera del perímetro declarado fue escrito. Los dos defectos de esta sección no salieron de un descuido de perímetro — fueron un sitio de cascada perdido (T15) y una cita abreviada mal (T03), ambos dentro de archivos ya en perímetro, encontrados exactamente porque el checklist de cierre no se saltó.
