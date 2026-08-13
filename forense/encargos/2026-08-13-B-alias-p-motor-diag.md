- **SHA de redacción:** `dcc4f6a`
- **Entorno asignado:** cualquiera, SIN red, SIN corpus. NO en los dos.
- **Estado:** CONSUMIDO — ejecutado en la rama `alias-p/motor-diag` (worktree `/home/pc0/mm-alias-p-motor-diag`, clon `/home/pc0/Modelado-Mexicano`). PR aún no abierto al escribir este archivo — ningún acto de esta convención exige que lo esté para marcar `CONSUMIDO`; el registro es el commit, no el PR (mismo criterio que `forense/encargos/2026-08-13-adr-provisionalidad.md`). Detalle completo de la ejecución: `forense/notas/2026-08-13-alias-p-motor-diag.md`.
- **Nota de ejecución, para quien audite después:** durante ARRANQUE se recibió una VENTANA 5 (mensaje de seguimiento) con tres correcciones sobre terreno que había avanzado entre la redacción y la ejecución — (a) el barrido de alcanzabilidad de §3.2 se redefine porque `data/censo-explotacion-2026-08-13.tsv` (PR #201, fusionado) ya mide una pregunta relacionada por `id_manifiesto` exacto; este acto mide una pregunta distinta, por nombre canónico, y reporta ambas más la brecha; (b) el número de ADR se confirma 73, no 72 (ADR-72 lo tomó `PR #199`, ya fusionado); (c) nombre de archivo de este mismo registro, con prefijo para no colisionar con la nota (T02). Las tres, verificadas contra `origin/main` real antes de aplicarlas — ninguna se tomó de la palabra del mensaje sin comprobar. Ver la nota forense §0 para el detalle y la verificación de cada una.

---

Texto completo del encargo, tal como se lanzó (verbatim):

---

ENCARGO B · ALIAS-P + MOTOR-DIAG — la identidad payload→fuente, y el parche de la vía
SHA de redacción: dcc4f6a. Entorno: cualquiera, SIN red, SIN corpus. NO en los dos.
Requiere ADR (ver §3.1). Repo-only.
§0 · Por qué

data/inventarios/alias-fuentes.yaml (128 entradas) declara en su cabecera que fue "Generado por ENCARGO MAP-1 a partir del diagnóstico de tests/catalogo.py:acron() sobre los 11 inventarios". Mapea cómo se nombra una fuente entre inventarios documentales. No mapea fuente → payload. No tiene entrada para ISSP, CSES, GPS, CCPV, FINANZAS, BIARE.

Consecuencia medida: el diagnóstico auxiliar de via_capa2.py compara el nombre canónico contra la prosa de usado_para, y produce falsos positivos verificados (SE→"falsador", PI→"estimación propia", INE→"diccionario"). Y LATINOBARÓMETRO no casa con latinobarometro2024_bd_stata.zip por el acento — un microdato de 6.7 MB que está en el corpus y que la cola de adquisición lista como pendiente en palanca 53.

Precisión que este encargo hereda de una verificación de código, no de la intuición: la vía promueve a SI leyendo id_manifiesto directo del manifiesto, sin tocar el archivo de alias (via_capa2.py:130-136). El alias NO bloquea ENLACE-2. Lo que arregla es que su alcance sea honesto.

§1 · PERÍMETRO

ESCRIBE: data/inventarios/alias-fuentes.yaml (EXTIENDE, jamás archivo paralelo) · data/curacion-registro/aliases-fuentes.tsv (ídem si su formato lo exige) · tools/curador_registro/via_capa2.py (§3.1) · canon/gobernanza-v1_15.md (el ADR + cascada) · canon/estado-programa-v1_10.md (contador de ADR) · forense/notas/2026-08-13-alias-p-motor-diag.md · hallazgos · encargos (A.3).

NO ESCRIBE: data/curacion-registro/relaciones.tsv · data/manifiesto.yaml · data/universo-declarado-t0.tsv · milpa/** · tests/**. Fuera de la lista, PARA.

⚠️ COLISIÓN REAL con el acto en vuelo de ADR-provisionalidad, que también escribe canon/gobernanza y canon/estado-programa. Coordina: si ese PR no ha fusionado cuando llegues a §3.1, espera o rebasa — no edites canon/ en paralelo con él. Y el número de ADR se deriva al sellar contra el main real, nunca se fija: si el de provisionalidad tomó 72, este va a 73 sin dejar hueco (T15 falla sobre huecos).

§2 · ARRANQUE

El bloque de cinco puntos del ENCARGO A, con el punto 3 igual (sin corpus, decláralo y salta).

PREMISAS (script, crudas):

```
set -u; cd "$(git rev-parse --show-toplevel)"
wc -l data/inventarios/alias-fuentes.yaml data/curacion-registro/aliases-fuentes.tsv
python3 tools/curador_registro/via_capa2.py | head -4      # el diagnóstico VIGENTE — NO heredes "78" ni "97"
git log --oneline -3 -- canon/gobernanza-v1_15.md          # ¿el ADR de provisionalidad ya fusionó?
grep -oE '\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -nu | tail -1
```

Lee entero: la cabecera de alias-fuentes.yaml (líneas 1-40 — declara su método y dos exclusiones deliberadas por ambigüedad de truncamiento; respétalas) · forense/notas/2026-08-13-map-b-crosswalk.md §duplicados · via_capa2.py completo.

§3 · COMMIT 1 — criterio y parche, antes de escribir alias
3.1 · El parche de via_capa2.py, y su ADR

Tres cambios. Ninguno toca la regla de qué es SI.

Imprimir el desglose de estados de verificar_entrada() —COINCIDE / NO_COINCIDE / AUSENTE / SIN_PAYLOAD / RAIZ_NO_CONFIGURADA— con su conteo, antes de los diffs.
Salir con código ≠ 0 si COINCIDE == 0 habiendo ≥1 fila con id_manifiesto, con el mensaje "cero payloads verificables — ¿está data/raw montada?".
Frontera de letra + normalización de acentos en el diagnóstico auxiliar (línea 149), en vez de in.

Por qué (1) y (2): verificado corriendo la vía sin corpus — devuelve 0 diffs idénticos a un entorno sano, porque la línea 136 (derivado = "SI" if estado == "COINCIDE" else actual) nunca degrada. Un ejecutor no puede distinguir "ya está hecho" de "no hay corpus".

Prueba obligatoria del cambio (3), contra casos de respuesta conocida: SE debe dejar de casar con "falsador" · PI con "estimación propia" · INE con "diccionario" · y LATINOBARÓMETRO debe empezar a casar con latinobarometro2024_bd_stata. Si no invierte los cuatro, el parche está mal.

ADR-<N derivado> propuesto: "Mantenimiento acotado de via_capa2.py bajo la ventana de ADR-70(d): diagnóstico de estados, paro por corpus ausente, y frontera de token en el diagnóstico auxiliar. No modifica la regla de promoción a SI." ADR-70(d) exige ADR explícito: "el mantenimiento del aparato previo a esa apertura queda permitido únicamente con ADR que lo selle".

3.2 · El criterio de identidad de alias

Un payload P es de la fuente F cuando concurre y se cita cuál: (a) url_origen de P pertenece al portal institucional de F; (b) usado_para de P nombra el instrumento de F sin ambigüedad; (c) archivo de P lleva el identificador de catálogo que el portal publica. Parecido de cadena no es evidencia.

Los cuatro casos de arranque — verifícalos, no los copies:

```
canónico    payloads    evidencia    ampara
ISSP    16 × za6980_* za5900_* za7600_*    (c) ZA-number + (b) ACTO R″ verificó México en el dato real    microdato + documentación
LATINOBARÓMETRO    3 × latinobarometro2024_*    (c); la brecha es de acento    microdato + cuestionario
CCPV    8 × cpv2020_*    (b)+(c)    microdato + documentación
EARLY_CHILDHOOD_..._2012_2014    7 × wb2661_*    (c) catálogo 2661 + (a)    SOLO documentación — declararlo
```

La reserva obligatoria. Por cada alias, declara qué clase de objeto ampara (microdato / documentación / instrumento). Un alias que hace que la vía promueva a SI una fila cuyo objeto_evidencia pide microdato mientras el payload es documentación mete un número falso al ejecutable — regla 1 del Bloque A-bis.

Barrido completo: corre la alcanzabilidad de los 550 payloads contra los canónicos de relaciones.tsv. En esta redacción dieron 321 huérfanos. Reporta el tuyo. Los bloques grandes (mociba 48, engasto 46, endireh 41…) NO son defectos de alias: son corpus sin demanda. Nómbralos y no les inventes canónico.

Frase de cierre de siempre.

§4 · COMMIT 2

Vía en lectura antes → escribe alias → vía en lectura después → reporta: diagnóstico de N a M, y la lista nominal de filas que la vía promovería con --escribe.

NO corras --escribe. relaciones.tsv es de otro carril. Entrega el diff exacto.

Suite: --baseline VERDE contra 948ad70. T15 vigila la contigüidad del ADR. Si un test truena, ese es el hallazgo.

§5 · NO HACE

No escribe relaciones.tsv. No cambia la regla de promoción a SI. No promueve por nombre. No amplía las dos exclusiones deliberadas de la cabecera del archivo de alias. No toca el archivo paralelo de demanda (ALIAS-D sigue siendo acto aparte).

---

VENTANA 5 (recibida a mitad de ARRANQUE, verbatim):

---

VENTANA 5 · ALIAS-P + MOTOR-DIAG — dos ajustes al vuelo

No reescribas commits sellados. Esto entra donde toque o en un commit propio; si contradice tu pre-registro, PARA y repórtalo.

(a) El barrido de alcanzabilidad de tu §3.2 ya está hecho, y por otro acto. data/censo-explotacion-2026-08-13.tsv fusionó en main como PR #201: 550 payloads censados, uno por fila, con estado. No lo repitas — léelo.

Pero lee esto antes: el censo y tú miden cosas distintas, y la diferencia es tu hallazgo. El censo cruza por id_manifiesto resuelto (identidad exacta) y da SIN-DEMANDA = 538 de 550 (97.82%). Tu barrido cruza por nombre canónico (identidad de alias) y en mi derivación previa daba ≈321. Ninguna de las dos está mal: responden preguntas distintas. El censo dice "ninguna fila cita este payload"; el tuyo dice "ningún nombre canónico lo alcanza". Reporta las dos y la diferencia entre ellas — esa brecha es exactamente el tamaño del problema que tus alias resuelven.

Y hay un dato del censo que te va a servir de prueba: la demanda entera cita 8 payloads distintos de 550, y siete de los ocho son cuestionarios o descriptores — solo ensafi2023_bd_csv_zip es microdato.

(b) Tu ADR es el 73, no el 72. ADR-72 lo tomó el acto de provisionalidad (PR #199, ya en main). Deriva el tuyo al sellar contra el main real: grep -oE '\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -nu | tail -1 → hoy 72, únicos 72, contiguo. Sin dejar hueco: T15 falla sobre huecos, no solo sobre el máximo, y ADR-70/71 se renumeraron tres veces por fijar el número antes de fusionar.

(c) El nombre de tu archivo de encargo, antes de que te muerda como a cinco actos. T02 normaliza sin distinguir directorio: si tu encargo y tu nota se llaman igual, la suite se pone ROJA por construcción. Convención de main: el encargo lleva código de acto como prefijo (2026-08-13-A-censo-explotacion.md, 2026-08-13-A7-indice-infraestructura.md), la nota no. Ponle prefijo al tuyo.

(d) Lo que no cambia. La prueba obligatoria del parche sigue en pie: SE debe dejar de casar con "falsador", PI con "estimación propia", INE con "diccionario", y LATINOBARÓMETRO debe empezar a casar con latinobarometro2024_bd_stata. Si no invierte los cuatro, el parche está mal. Y no corras --escribe: relaciones.tsv es de otro carril, entrega el diff.
