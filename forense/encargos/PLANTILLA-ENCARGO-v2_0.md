# PLANTILLA DE ENCARGO v2.0
**Norma: instrucciones v2.15 §0, §2, D-18 a D-23. Sucede a `PLANTILLA-LOTE-v1_0.md` (31/ago/2026), que se conserva como historia. Vive en el repo (`forense/encargos/PLANTILLA-ENCARGO-v2_0.md`) y en el conocimiento del proyecto de dirección: las dos copias son la misma, byte a byte (sha256 en el sidecar).**

**Para qué existe.** Entre el 16 y el 20/sep/2026, 75 de 160 NC nuevas fueron `FUERA-DE-PERÍMETRO` (48) o `PARO-PREMISA`/`PARO-ENTORNO` (27, en 18 actos). Tres causas, las tres de redacción: premisas afirmadas sin leer («código congelado» que estaba vacío), PARA donde el remedio era reversible y barato, y perímetros que no dejaban al acto terminar lo suyo.

**Cinco principios.** (1) El encargo dice QUÉ y PARA QUÉ; el ejecutor decide CÓMO. (2) Toda premisa lleva rótulo de cómo se obtuvo. (3) Premisa falsa ≠ PARO: si el objetivo sigue alcanzable, se replantea y se sigue. (4) Una compuerta declara qué protege. (5) Todo acto puede terminar lo suyo.
**Lo que no se afloja.** En `MODO: RÍGIDO` (reserva de evaluación o spec congelada) la latitud es sobre logística, nunca sobre el procedimiento.

---

```
# ENCARGO · ACTO <RÓTULO> · <una frase: qué habrá cuando termine>

> ENTORNO: **<NUBE | CAJA>** — el hook de arranque imprime ENTORNO-DERIVADO; si no coincide, PARA en una línea.

CABECERA · SHA de redacción · una sola sesión · MODELO · MODO: <ABIERTO | RÍGIDO (mide con
reserva/spec congelada)> · CONTADOR (qué mueve; qué NO debe moverse) · CALC-id reservado si aplica

## 1 · OBJETIVO
Qué debe existir al cerrar, y qué decisión o medición habilita. Dos a cuatro líneas.
«Hecho» significa: <criterio verificable por comando>.

## 2 · FIRMAS DE MESA
Verbatim, con fecha. Propuestas marcadas como tales. Sin texto → PARA esa pieza, no el acto.

## 3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo
  [EJECUTADO]  lo corrí; comando y salida cruda.
  [LEÍDO]      abrí el archivo y leí la parte que cito; archivo:líneas.
  [EXISTE]     solo comprobé que está (ls/grep). NO sé si funciona ni qué contiene.
  [SUPUESTO]   no lo verifiqué. Por qué lo creo.
  [REPORTADO]  lo dijo otra sesión o mesa; fuente.
Prohibido: un verbo de funcionamiento («mide», «cubre», «congela», «autoriza», «reproduce»)
sobre una línea [EXISTE], [SUPUESTO] o [REPORTADO].

## 4 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO, no por frase
Qué busqué, dónde, con qué términos, cuántos archivos examiné, qué encontré:
  decisiones.tsv · firmas-pendientes.tsv · ADR · corridas.tsv (por instrumento y por regla) ·
  relevo-usos · no-corrido.tsv (NC con sucesor que apunte aquí) · ramas vivas · encargos archivados.
Al ejecutor: **repítela tú con tu acceso, que es mejor que el mío.** Si está hecho, el
entregable es decirlo y hacer solo lo que falte. Si está decidido, manda la decisión.

## 5 · PIEZAS — resultado esperado de cada una, no receta
Por pieza: qué produce · cómo se sabe que quedó bien · «si <premisa [SUPUESTO]> resulta
falsa, entonces <rama prevista>». Las ramas previstas son parte del encargo, no una desviación.

## 6 · LATITUD
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
  e) entorno equivocado
  f) el OBJETIVO dejó de ser alcanzable o dejó de tener sentido → PARO, y eso es el entregable
En MODO RÍGIDO se añade: g) el código congelado no corre → no se parcha.

## 8 · COMPUERTAS — cada una declara qué protege
«<condición> protege: <abrir dato | congelar spec | adoptar | borrar>». Lo que no proteja
una de esas cuatro se escribe como orden sugerido, no como compuerta.

## 9 · PERÍMETRO
Propio: <lista>. Ajeno que no se toca: <lista corta, con el porqué>.
PERÍMETRO DE CIERRE — permanente, no hay que pedirlo: cablear en CI el test propio · publicar
en la vista las filas propias y su asiento de replay · registrar en INFRAESTRUCTURA la tabla
propia · la cascada de /acto · hallazgos, NC y FP propios.
Fuera del perímetro y necesario para terminar → es LATITUD (≤ 10 líneas, declarado) o es
PREGUNTA. «FUERA-DE-PERÍMETRO» como razón de una NC queda para lo que de verdad es de otro acto.

## 10 · LO QUE NO HACE · SUCESORES · AUDITORÍA (si afirma sobre México) · CIERRE
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

## FALSADOR (§9 de las instrucciones)
Si `PARO-PREMISA` + `PARO-ENTORNO` + `FUERA-DE-PERÍMETRO` no bajan de 47 % a menos de un tercio de las NC nuevas en los tres meses siguientes a su sello, la plantilla no resolvió el defecto y se revisa. Se mide con un comando sobre `forense/no-corrido.tsv`, por token de prefijo (A.16).
