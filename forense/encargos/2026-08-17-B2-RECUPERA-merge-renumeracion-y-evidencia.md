# ENCARGO B2-RECUPERA · el merge y la renumeración, y después la evidencia que la redacción destruyó

- **SHA de redacción:** `origin/main = 4415e04` (merge #250) · rama `codex/barrido-2` en `d130a3f`
- **Fecha:** 2026-08-17 · **Estado:** CONSUMIDO por este acto · **PR:** #244 (borrador, no fusionado)
- **Entorno:** la misma caja Ubuntu/WSL2. Worktree `/home/pc0/Modelado-Mexicano-barrido2`. No se clonó.
  `.barrido2/` está gitignorado y sólo vive ahí. **Modelo: Opus.**
- **Ejecución:** `forense/notas/2026-08-17-b2-recupera.md`.

## Por qué existe

Los dos primeros bloques del orden que el propio ejecutor propuso al cerrar la
auditoría de BARRIDO-2, y por la razón que dio: *«todo lo demás se escribe sobre una
base que ya cambió»*, y la familia de redacción *«decide si la fase semántica tiene
evidencia con qué trabajar»*. Hacer C4 sobre metadatos destruidos habría producido
trabajo semántico sobre evidencia dañada.

## Método impuesto por el encargo, y aplicado

**Control positivo obligatorio.** Cuatro recetas rotas de dirección en la jornada,
todas con el mismo síntoma: un «no existe» que era un «no busqué bien». Antes de
usar cualquier patrón, se corre contra un caso de respuesta conocida; si el control
no da positivo, la receta está rota y el resultado no se reporta. Los controles y sus
salidas crudas están en la nota.

---

## Texto completo del encargo, verbatim

ENCARGO B2-RECUPERA · el merge y la renumeración, y después la evidencia que la redacción destruyó
SHA de redacción: origin/main = 4415e04 (merge #250) · rama codex/barrido-2 en d130a3f · Fecha: 17/ago/2026 · Estado: VIVO
Entorno: LA MISMA CAJA Ubuntu/WSL2. Worktree existente /home/pc0/Modelado-Mexicano-barrido2, rama codex/barrido-2. No clones. .barrido2/ está gitignorado y solo vive ahí.
Modelo: Opus.
Archívese en forense/encargos/ con su lanzamiento (A.3).

Qué es. Los dos primeros bloques del orden que tú mismo propusiste, y por la razón que tú diste: "todo lo demás se escribe sobre una base que ya cambió", y la familia de redacción "decide si la fase semántica tiene evidencia con qué trabajar". Este acto no hace C4. Hacer C4 sobre metadatos destruidos produciría trabajo semántico sobre evidencia dañada.

Qué NO es. No cierra BARRIDO-2. §28 seguirá en 13 de 22 o cerca. El PR #244 sigue borrador y sin fusionar.

════════ ARRANQUE ════════ 1 · REPO. pwd · git status --short --branch · git log -1 --format="%h %s". No clones. Esperado: rama codex/barrido-2, HEAD d130a3f. Si git status muestra trabajo sin commitear, inventaríalo antes de nada y no lo borres. 2 · SHA. Reporta git log -1 origin/main tras el fetch. Al redactar: 4415e04, 18 commits que la rama no tiene. 3 · data/raw + .barrido2/. ls .barrido2/private/ .barrido2/tasks-v2/ | head y wc -l .barrido2/private/e2-neutral-index.jsonl. Si .barrido2/ no existe, PARA: reconstruirlo son 672 inspecciones y es decisión de mesa. 4 · ENTORNO. echo ${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable} · unshare -Urn -- true; echo rc=$? · ls "/home/pc0/mm-corpus/raw" | head -3. 5 · ESPEJO. Prohibido para cifras. ══════════════════════════

⚠️ MÉTODO — control positivo obligatorio

Cuatro recetas rotas de dirección en esta jornada, todas con el mismo síntoma: un "no existe" que era un "no busqué bien". grep -E "A|B" busca el carácter | literal en ERE. grep "policron" pierde Polychronic y policrónica. Antes de usar cualquier patrón, córrelo contra un caso donde ya sabes la respuesta. Si el control no da positivo, la receta está rota y el resultado no se reporta. Pega control y salida en la nota.

BLOQUE 1 · El merge y la renumeración

1.1 · El merge

    git fetch origin && git merge origin/main    # LOCAL, main HACIA la rama

Merge local siempre. forense/hallazgos.md lleva merge=union y el botón de GitHub no lo honra del lado servidor. El editor web de conflictos está prohibido: ahí se borra la entrada ajena.

1.2 · Tu ADR no puede ser el 94

Derivado contra 4415e04: gobernanza en main tiene máximo 93, cero huecos. Tu rama tiene máximo 92 (el tuyo). Renumerar el tuyo a 93 choca con REGISTRA-17AGO-II.

Y 94 tampoco sirve, por una razón que no podías ver desde la rama. ADR-94 no existe en gobernanza, pero ya está citado cuatro veces en el canon de main:

canon/glosario-v5_6.md:316                              (conf.02 → "Resuelto por ADR-94")
canon/integrador-psicologia-mexicano.md:245  y  :351    ("(ADR-94)")
corpus/reports/La_arquitectura_invisible_...:155        ("(ADR-94)")

Son huérfanas: quedaron cuando se fusionó a mano el COMMIT 1 de un PR marcado "No fusionar todavía. Trabajo en curso", y el commit que iba a sellar el 94 nunca ocurrió. El número está comprometido semánticamente para la adjudicación de conf.02. Si lo tomas, esas cuatro citas apuntan a tu ADR con contenido equivocado — peor que el hueco actual.

Deriva tu número al fusionar, contra el main real de ese momento, y salta el 94. Y hay una tercera sesión en la carrera: CONSOLIDA también va a sellar ADR y a cubrir el hueco del 94. Re-deriva justo antes de escribir el número, no al arrancar el bloque. T15 falla sobre huecos, no solo sobre el máximo — no dejes hueco tú tampoco: si el 94 sigue vacío cuando selles, dilo en el ADR y no lo rellenes con el tuyo.

1.3 · Tu FP-38 también renumera

Main ya tiene FP-38 = "la procedencia de glosario:136 está mal marcada". La tuya —los cuatro expedientes ESP-OPACA-A/B/C/D— es otra cosa. Máximo en main: FP-42. Deriva el tuyo al fusionar; no lo elijas ahora, CONSOLIDA va a abrir filas también.

Y arregla lo que tu propia auditoría cazó: tu fila declara "no gatea el cierre, que se mide por --baseline y T-CABLEADO", y FP-38 es justo lo que pone --baseline en rojo mientras T-CABLEADO no existe. El razonamiento se anula solo. Reescribe la fila con lo que sí es cierto.

1.4 · El congelado

Tu rama mide contra 6f78d06; main va en 45d7d2f, recongelado dos veces desde entonces. Tras el merge, --baseline compara contra otra base. Espera ROJO y decláralo. No recongeles: --freeze exige ADR de mesa (ADR-76(f)) y este acto no lo trae firmado. Reporta por test, no agregado — un reporte agregado ya escondió dos defectos propios en #248.

1.5 · Lo que mesa te sacó del perímetro

ADR-93 firmó FP-24 con texto verbatim y adoptó como canónica la cláusula que tu verificación adversarial señaló: "la gemela NO_DETERMINADO se enlaza SOLO si su objeto es evidenciable con una entrada distinta del manifiesto". Y sacó las 20 filas con par de este acto: se adjudican "en acto propio". No las escribas. Lo que sí corresponde: dejar en la nota lo que tu medición ya sabe —que ENFIH y ENBIARE tienen dos entradas de manifiesto cada una, así que para esas filas la escapatoria existe— como insumo para ese acto, no como adjudicación.

BLOQUE 2 · La evidencia que la redacción destruyó

Todos estos defectos son de la misma familia y tú ya la nombraste: falsos positivos del detector de PII sobre metadatos que genera la máquina. Tu arreglo anterior para nombres de esquema fue demasiado estrecho. Este bloque lo ensancha con la lección puesta: el patrón no distingue un dato de persona de un identificador de máquina, y el default está del lado equivocado.

2.1 · Los value labels de SAV — 132,396 de 135,262 destruidos (97.9%)

Causa medida: el emisor escribe codigo_hex=0000000000000000;label=Sí y los 16 dígitos disparan \d{11,18}, que redacta la etiqueta entera. DTA, que emite la etiqueta sola, conserva 99.5% — ése es tu control positivo de que el arreglo funciona: SAV tiene que acercarse a DTA, no al revés.

2.2 · Los metadatos de miembro ZIP — 71.6% borrados

Causa medida: crc=3266880665 son 10 dígitos y disparan el patrón de teléfono. Con ellos se pierde la declaración zip_slip=NO por miembro, que es una garantía de seguridad, no un adorno.

Para 2.1 y 2.2 — la regla, no el parche. Los campos que la máquina emite con nombre conocido (codigo_hex, crc, y los que tu barrido encuentre) se excluyen por campo, no por longitud de dígitos. Declara la lista de campos exentos en producto durable, no en el código, para que sea auditable. Y verifica que el cegamiento sigue intacto: re-corre la comprobación de que no queda rastro de N1-N33 en los 1,342,437 registros, y que siguen en 0 las filas y valores individuales. Si el arreglo mete un solo valor de persona, PARA y revierte — la privacidad manda sobre la cobertura, sin excepción.

2.3 · Los 83 PDF marcados Encrypted: yes que sí abren

83 de 169 (49%), 5,996 páginas. pdftotext extrae 82 de 83 sin clave. Entre ellos 25 cuestionarios y 7 diccionarios: FD_ENCUCI2020, ZA5900_cdb, Censo2020_cuest_ampliado, enbiare_2021_fd.

Esto importa más que su porcentaje. Es documentación de instrumento que el programa lleva semanas persiguiendo por otras vías — FP-33/DOC-BACKFILL existe precisamente para conseguir fichas y cuestionarios. Puede estar en disco desde hace días, descartado por una bandera.

Encrypted: yes con permisos de extracción abiertos no es un descarte: es un caso a intentar. Reclasifica: intento de extracción → si sale, entra; si no, PDF_CIFRADO con la salida cruda del intento. El uno que no abre se declara con su nombre.

2.4 · Los tabulares, si el presupuesto alcanza

841 de 841 hojas XLS en excepción BIFF — cero tablas, cero diccionarios, cero columnas. 8 de 44 XLSX pierden al menos una hoja no vacía. Y tipo de variable DTA al 0.00%, que §8 exige.

Ordenados así a propósito: 2.1–2.3 recuperan documentación de instrumento, que es lo que la fase semántica consume. 2.4 recupera tabulares, que son insumo de otra etapa. Si algo se corta por presupuesto, se corta 2.4 — y se declara, no se omite.

2.5 · Lo tuyo, que tú declaraste

El CMD-MATERIAL del PRISMA apunta a la generación v2 y es irreproducible: 0 de 672 tarea_id derivan de v2, 672 de 672 derivan de v4. Corrígelo al v4 real y re-verifica que el comando reproduce — un comando que no corre no es procedencia.

Lo que este acto NO hace
No hace C4, C5 ni C6. El bloque semántico va después, sobre la evidencia ya recuperada.
No rehace la muestra adversarial. Tu auditoría la encontró de build 1.0 contra 1.1 sellado, 0 de 41 hashes coinciden, sin veredicto escrito — así que la exigencia 4 de §15 no está satisfecha y seguirá sin estarlo al cerrar este acto. Decláralo en la nota como deuda nombrada; rehacerla es acto propio.
No adjudica las 20 filas con par. Mesa las sacó (ADR-93).
No cierra BARRIDO-2 ni fusiona el PR #244. Sigue borrador.
No toca --require-cableado, la bandera que check.py ignora en silencio. Va con T-CABLEADO, en C6.
No resuelve las 10 inspecciones redundantes ni los 12→5 atributos de E0. Se declaran y se cuentan.

Cierre

python3 tests/check.py --baseline antes y después, por test. Pruebas propias de BARRIDO-2 antes y después. Y los tres controles de recuperación con su cifra: SAV value labels conservados (contra el 99.5% de DTA como referencia), metadatos ZIP conservados con zip_slip presente, y PDF abiertos de los 83. Sin esas tres cifras el bloque 2 no está reportado.

Privacidad re-verificada tras cada arreglo · nada de .barrido2/ ni staging se empuja · nota propia con cada comando, su control positivo y su salida cruda · una entrada en hallazgos.md · este encargo archivado y CONSUMIDO con su PR · git diff --check · jamás te auto-fusionas.

Contadores del programa: 0. Este acto no mide ni cierra: reconcilia la base y recupera evidencia que un patrón demasiado ancho había borrado. Dilo así, sin justificarlo.
