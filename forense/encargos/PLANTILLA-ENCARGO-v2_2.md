# PLANTILLA DE ENCARGO v2.2
**Norma: instrucciones v2.17 §0, §2, D-10, D-11, D-15 a D-24. Sucede a `PLANTILLA-ENCARGO-v2_1.md` (21/sep/2026), que se conserva como historia y no se edita. Vive en el repo (`forense/encargos/PLANTILLA-ENCARGO-v2_2.md`) y en el conocimiento del proyecto de dirección: las dos copias son la misma, byte a byte (sha256 en el sidecar).**

**Qué cambia sobre v2.1** (`GEN2-TRAMITE-INSTRUCCIONES-V217-1`, 28/sep/2026). Seis piezas: (1) bloque ADJUNTOS con el sha que el acto **calcula al recibir**, no uno que mesa pase por el chat (mesa 28/sep: «deja de darme sha's aquí, eso se supone ya va dentro del encargo»). (2) «Archivos que otro acto en vuelo está tocando» pasa a campo obligatorio. (3) ENTORNO con la regla de caja: microdato o corpus montado → CAJA; documentación, portales y gobierno → NUBE. (4) Sección de OPCIONES cuando el encargo lleva una decisión a mesa: situación · opciones con costo · recomendación · texto de firma (mesa 27/sep: «ni opciones me diste»). (5) `AUTÓNOMO-AMPLIO` como valor de MODO, con la cláusula de autonomía v1.0 incorporada (ya no se pega a mano en §6). (6) PARO (e) se lee en los dos sentidos según el entorno asignado.

**Qué cambió en v2.1 sobre v2.0 (historia).** Cinco piezas, todas de `GEN2-V216`: (1) ids con raíz de acto (D-24) — nada se renumera nunca, así que la plantilla deja de sugerir que alguien "renumera al fusionar" o "deriva ids al cierre"; el candidato de raíz lo deriva `tools/cierre_acto.py` contra el 0-bis ya commiteado. (2) el cuerpo no trae campos que se rellenen al cierre ni líneas de estado (`SIDECAR-CUERPO-1`): el encargo se archiva verbatim con su sello de CUERPO (`X.cuerpo.sha256`) en el 0-bis y ese sello no se regenera nunca — un hueco tipo «PR: ___» lo rompe. (3) las adendas de mesa que lleguen con el acto ya corriendo aterrizan como archivo propio (`<encargo>-ADENDA-N.md`, sellado al recibirse) y se citan sólo desde el CIERRE, nunca pegadas al cuerpo (firma `ADENDAS`). (4) el test propio de un acto entra a CI como huérfano (`ci_guardias --ejecuta-huerfanos`), no como una edición de `verify.yml`/`check.py` que el encargo pida (D-21). (5) «hecho» se verifica por comando sobre el commit final con `origin/main` fusionado, nunca por revisión de dirección sesión por sesión.

**Para qué existe (heredado de v2.0, vigente).** Entre el 16 y el 20/sep/2026, 75 de 160 NC nuevas fueron `FUERA-DE-PERÍMETRO` (48) o `PARO-PREMISA`/`PARO-ENTORNO` (27, en 18 actos). Tres causas, las tres de redacción: premisas afirmadas sin leer («código congelado» que estaba vacío), PARA donde el remedio era reversible y barato, y perímetros que no dejaban al acto terminar lo suyo.

**Cinco principios (heredados).** (1) El encargo dice QUÉ y PARA QUÉ; el ejecutor decide CÓMO. (2) Toda premisa lleva rótulo de cómo se obtuvo. (3) Premisa falsa ≠ PARO: si el objetivo sigue alcanzable, se replantea y se sigue. (4) Una compuerta declara qué protege. (5) Todo acto puede terminar lo suyo.
**Lo que no se afloja.** En `MODO: RÍGIDO` (reserva de evaluación o spec congelada) la latitud es sobre logística, nunca sobre el procedimiento.

---

```
# ENCARGO · ACTO <RÓTULO> · <una frase: qué habrá cuando termine>

> ENTORNO: **<NUBE | CAJA>** — se asigna por lo que el acto toca (v2.17 §6): microdato o corpus
> montado → CAJA; documentación, portales, gobierno → NUBE. El hook de arranque imprime
> ENTORNO-DERIVADO; si no coincide, PARA en una línea.

CABECERA · SHA de redacción · una sola sesión (D-17) · MODELO (D-13) · MODO: <ABIERTO | RÍGIDO
(mide con reserva/spec congelada) | AUTÓNOMO-AMPLIO (la sesión decide orden, agrupación y
profundidad; una hoja de firmas al cierre)> · CONTADOR (qué mueve; qué NO debe moverse) ·
CALC-id reservado si aplica · FP/ADR/NC candidatos: raíz de acto (D-24) — no se derivan aquí,
los deriva `tools/cierre_acto.py` contra el 0-bis; no se renumeran nunca.

## 1 · OBJETIVO
Qué debe existir al cerrar, y qué decisión o medición habilita. Dos a cuatro líneas.
«Hecho» significa: <criterio verificable POR COMANDO sobre el commit final con origin/main
fusionado> — nunca una revisión de dirección sesión por sesión.

## 2 · FIRMAS DE MESA
Verbatim, con fecha, y con archivo y fila si la firma ya está en el repo (evita el doble
asiento de A.12: una firma que viaja aquí verbatim la asienta este acto, no un trámite aparte).
Propuestas marcadas como tales. Sin texto → PARA esa pieza, no el acto.

## 3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo
  [EJECUTADO]  lo corrí; comando y salida cruda.
  [LEÍDO]      abrí el archivo y leí la parte que cito; archivo:líneas.
  [EXISTE]     solo comprobé que está (ls/grep). NO sé si funciona ni qué contiene.
  [SUPUESTO]   no lo verifiqué. Por qué lo creo.
  [REPORTADO]  lo dijo otra sesión o mesa; fuente.
Prohibido: un verbo de funcionamiento («mide», «cubre», «congela», «autoriza», «reproduce»)
sobre una línea [EXISTE], [SUPUESTO] o [REPORTADO].
ADJUNTOS: lista por nombre. El sha256 de cada uno va DENTRO del encargo o de su sidecar, nunca
en el chat; si el encargo no lo trae, el acto lo calcula al recibir y lo asienta en el 0-bis.
Lo que no cabe en el adjunto puede viajar EMBEBIDO entre marcadores, con el sha256 del
contenido embebido — la sesión lo extrae y lo verifica antes de usarlo (evita el defecto de
`CI-MEDICION-1`: texto renderizado archivado como si fuera el `.md` fuente).

## 4 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO, no por frase
Qué busqué, dónde, con qué términos, cuántos archivos examiné, qué encontré:
  decisiones.tsv · firmas-pendientes.tsv · ADR · corridas.tsv (por instrumento y por regla) ·
  relevo-usos · no-corrido.tsv (NC con sucesor que apunte aquí) · ramas vivas · encargos archivados.
Al ejecutor: **repítela tú con tu acceso, que es mejor que el mío.** Si está hecho, el
entregable es decirlo y hacer solo lo que falte. Si está decidido, manda la decisión.

## 5 · PIEZAS — resultado esperado de cada una, no receta
Por pieza: qué produce · cómo se sabe que quedó bien · «si <premisa [SUPUESTO]> resulta
falsa, entonces <rama prevista>». Las ramas previstas son parte del encargo, no una desviación.
Spec congelable por pieza, cuando aplique: qué queda fijo en COMMIT-1 (D-15, D-22).

## 5-bis · OPCIONES — solo si el encargo lleva una decisión a mesa
Situación (una línea) · opciones, cada una con su costo · recomendación y por qué · plazo ·
texto de firma listo. Una recomendación sin opciones no es hoja (v2.17 §0).

## 6 · LATITUD
Cláusula de autonomía v1.0 (`forense/encargos/CLAUSULA-AUTONOMIA-v1_0.md`) vigente por norma
(v2.17 §0): no se pega aquí. Discrepancias con el repo, interpretación declarada
(`INTERPRETACIÓN-DECLARADA`), redacción rotulada (`PROPUESTO-POR-EJECUTOR`), opción
recomendada: del ejecutor.
DECIDES TÚ, y lo dices en la nota: el cómo · el orden · herramientas · nombres de archivo ·
remover obstáculos reversibles y baratos (enlazar data/raw, `fetch --unshallow`, instalar una
dependencia, regenerar un derivado por comando, corregir una cita rota) · arreglar un defecto
adyacente de ≤ 10 líneas que te impide terminar, declarándolo.
PREGUNTAS A MESA, con 2–3 opciones y tu recomendación, y SIGUES con lo demás mientras tanto:
bifurcaciones no previstas que cambian qué se entrega.
NO DECIDES: nada de la sección 7.

## 7 · PAROS — lista cerrada. Fuera de ella, no se para: se resuelve o se pregunta.
  a) abrir, derivar o imprimir dato de una ola reservada fuera del código autorizado
  b) borrar, forzar (`-D`, `--force`, `clean`) o reescribir algo sellado
  c) adoptar, o mover un contador que el encargo dice que no debe moverse
  d) cambiar estimando, universo, umbral, candidato o código de un procedimiento congelado
  e) entorno equivocado — en los dos sentidos: microdato o corpus en NUBE; gobierno o
     documentación asignado a CAJA sin razón (se invierte según el ENTORNO de la cabecera)
  f) el OBJETIVO dejó de ser alcanzable o dejó de tener sentido → PARO, y eso es el entregable;
     leído estricto (D-19): solo sin ruta legítima
En MODO RÍGIDO se añade: g) el código congelado no corre → no se parcha.
Enmienda de cableado (D-18): mientras el CALC no tenga `ejecucion.json`, un bloqueo de
preflight de cableado puro (ruta de spec, sha de un input origen-repo, `dependencias_materiales`,
constancia en lugar de archivo vivo, `permite_no_estimable`) se corrige en commit propio,
declarado, y NO es PARO — nada de esa lista toca estimando, umbral, λ, candidatos ni B-bis.

## 8 · COMPUERTAS — cada una declara qué protege
«<condición> protege: <abrir dato | congelar spec | adoptar | borrar>». Lo que no proteja
una de esas cuatro se escribe como orden sugerido, no como compuerta.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: <lista>. Ajeno que no se toca: <lista corta, con el porqué>.
ARCHIVOS QUE OTRO ACTO EN VUELO ESTÁ TOCANDO (obligatorio): <lista, o «ninguno verificado»,
con el comando que lo verificó> — evita el choque que cuatro encargos del 21/sep resolvieron
cada uno a su manera.
«Si te encuentras escribiendo fuera de esta lista, PARA.»
PERÍMETRO DE CIERRE — permanente, no hay que pedirlo: el test propio entra a CI como
HUÉRFANO (`ci_guardias --ejecuta-huerfanos`), sin editar `verify.yml` ni `check.py` (D-21) ·
publicar en la vista las filas propias y su asiento de replay (E.7) · registrar en
INFRAESTRUCTURA la tabla propia · dejar el fragmento L0 propio en `canon/L0/<ADR-raíz>.md`,
nunca en la línea `L0` compartida ni en `canon/estado-programa-v1_N.md` · la cascada de /acto ·
hallazgos, NC y FP propios, con ids de raíz de acto (D-24) — nunca "el siguiente número libre".
Fuera del perímetro y necesario para terminar → es LATITUD (≤ 10 líneas, declarado) o es
PREGUNTA. «FUERA-DE-PERÍMETRO» como razón de una NC queda para lo que de verdad es de otro
acto, y se nombra ese acto — si no se puede nombrar, no era de otro acto (D-21).

## 10 · LO QUE NO HACE · SUCESORES · AUDITORÍA (si afirma sobre México) · CIERRE
El cuerpo de este encargo no lleva campos para rellenar ni líneas de estado: `## NO-CORRIDO /
RESERVAS` y `## CONSUMIDO` las añade /acto al final del archivo archivado (A.3, D-a1 a D-a6),
nunca editando lo de arriba. Adendas de mesa recibidas durante la ejecución: archivo propio
`<este-encargo>-ADENDA-N.md`, sellado al recibirse, citado sólo aquí en el CIERRE.
```

---

## LISTA DE DIRECCIÓN — antes de entregar cualquier encargo

1. ¿Cada verbo de funcionamiento descansa en `[EJECUTADO]` o `[LEÍDO]`? Si no, lo bajo a `[EXISTE]`/`[SUPUESTO]` y escribo la rama «si resulta falso».
2. ¿Busqué por **objeto** si ya está hecho o decidido, y declaré universo y conteo?
3. ¿Cada PARA está en la lista cerrada? Si el remedio es reversible y barato, es latitud.
4. ¿Cada compuerta dice qué protege?
5. ¿El acto puede **terminar lo suyo** sin pedir otro acto?
6. ¿Hay alguna cifra esperada tecleada? Fuera.
7. ¿MODO correcto? Rígido solo si hay reserva o spec congelada.
8. ¿El cuerpo tiene algún campo para rellenar al cierre o una línea de estado? Fuera — rompe el sello de CUERPO (A.3).
9. ¿Cada adjunto trae su sha256, o va embebido con el suyo si no cabe?
10. ¿Listé los archivos que otro acto en vuelo esté tocando ahora?
11. ¿«Hecho» está escrito como comando sobre el commit final, no como «yo lo reviso»?
12. ¿El ENTORNO corresponde a lo que el acto toca (microdato → CAJA)?
13. ¿Si llevo una decisión a mesa, di opciones con costo, no solo la recomendación?
14. ¿Algún sha quedó en el chat en vez de en el encargo?

## FALSADOR (§9 de las instrucciones)
Si `PARO-PREMISA` + `PARO-ENTORNO` + `FUERA-DE-PERÍMETRO` no bajan de 47 % a menos de un tercio de las NC nuevas en los tres meses siguientes a su sello, la plantilla no resolvió el defecto y se revisa. Se mide con un comando sobre `forense/no-corrido.tsv`, por token de prefijo (A.16). El mismo falsador de v2.0 sigue vigente; ni v2.1 ni v2.2 reinician la ventana de medición. Falsador propio de v2.2: si en tres meses mesa vuelve a recibir un sha por chat o una recomendación sin opciones de un encargo hecho con esta plantilla, las piezas (1) o (4) no bastaron.
