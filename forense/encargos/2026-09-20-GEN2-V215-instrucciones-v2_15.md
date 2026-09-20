# ENCARGO · ACTO GEN2-V215 · INSTRUCCIONES v2.15 EN DOS CUERPOS, LA PLANTILLA DE ENCARGO v2.0 EN EL REPO, Y `/acto` ENSEÑANDO AL EJECUTOR QUÉ HACER CUANDO UNA PREMISA CAE

ENTORNO: NUBE — el hook de arranque imprime `ENTORNO-DERIVADO`; si dice `CAJA` puedes correrlo igual: dilo en la primera línea de la nota.

CABECERA · SHA de redacción `cb1945ff`; re-deriva al abrir · una sola sesión, rama propia · MODELO: Opus (redacta norma y toca el comando que gobierna todos los actos) · MODO: ABIERTO, con una pieza verbatim (P1) · CONTADOR: `cuenta_gen2 = NO`; no mide; ningún contador del programa debe moverse · primer encargo escrito con la plantilla que instala: si la plantilla te estorba para ejecutarlo, eso es hallazgo y va a la nota.

1 · OBJETIVO

Que a partir de este merge toda sesión de Claude Code y toda conversación de dirección lean las mismas reglas nuevas: premisas rotuladas, paros en lista cerrada, latitud, compuertas que declaran qué protegen, perímetro de cierre. Habilita que los encargos dejen de parar por logística y de afirmar lo que no leyeron. «Hecho» significa: `instrucciones-proyecto-v2_15.md` en el árbol con su HISTORIA · `CLAUDE.md` la importa · `forense/encargos/PLANTILLA-ENCARGO-v2_0.md` presente y byte-idéntica al adjunto · `/acto` trae la sección de ejecución · `instrucciones_vigentes = v2.15` donde se derive · suite VERDE por FAIL.

2 · FIRMAS DE MESA

Plantilla y delta (20/sep/2026, verbatim): «Esta ok, dame todos los lugares donde debe de ir, instrucciones, modificar el template de "acto" en el repo, guardarlo aquí en el proyecto. Quiero que quede completamente permeado.» A.9 — lado proyecto (propuesta; mesa la confirma o corrige la fecha al lanzar; sin ella P1 sella solo el lado repo y lo dice, como hizo ADR-544): "El cuerpo operativo v2.15 quedó pegado en las instrucciones del proyecto de Claude el 20/sep/2026, y `PLANTILLA-ENCARGO-v2_0.md` subida al conocimiento del proyecto el mismo día."

ADJUNTOS (A.3; verifica sha256/16 al recibir; si falta uno, pídelo — no lo reconstruyas): `instrucciones-proyecto-v2_15-OPERATIVA.md` `237255dbe6da598d` · `PLANTILLA-ENCARGO-v2_0.md` `3574daacec8c22ac` · `ACTO-MD-bloque-ejecucion-v2_15.md` `7d81cce9ef1cefb7`.

3 · LO QUE DIRECCIÓN SABE

* `[EJECUTADO]` El cuerpo v2.15 se generó por script sobre `instrucciones-proyecto-v2_14.md` de `cb1945ff`: 117 líneas (eran 108), 17 líneas cambiadas o nuevas; cada sustitución con `assert` de que el texto original existía. Queda una mención legítima a «v2.14» (§1: "Desde v2.14, una medición sin fila…").
* `[LEÍDO]` `instrucciones-proyecto-v2_14.md` líneas 1, 3, 7, 21, 65, 72, 90, 101, 102, 107, 108: son las que el delta toca.
* `[LEÍDO]` `.claude/commands/acto.md` (376 líneas): cuatro secciones — `1 · ARRANQUE`, `2 · COMPUERTA`, `3 · 0-bis A.3`, `4 · CIERRE` (pasos 1–13). No tiene ninguna sección sobre cómo tratar una premisa falsa durante la ejecución; `PARO-PREMISA` solo aparece como token de A.14 (`:305`).
* `[LEÍDO]` `CLAUDE.md` (11 líneas) importa `@instrucciones-proyecto-v2_14.md`.
* `[EJECUTADO]` `grep -c "PARA-v2.1[56]" forense/hallazgos.md` → 17 semillas. El cuerpo adjunto promueve a norma las que tocan redacción y ejecución de encargos, E.5, E.6 y A.15.
* `[EJECUTADO]` `no-corrido.tsv`, fecha ≥ 16/sep: 160 NC; 48 `FUERA-DE-PERÍMETRO`, 27 `PARO-PREMISA`/`PARO-ENTORNO` en 18 actos. Parser de dirección por prefijo con variantes con y sin tilde; re-derívalo bien: es la línea base del falsador.
* `[EXISTE]` `instrucciones-proyecto-v2_14-HISTORIA.md`; `forense/encargos/PLANTILLA-LOTE-v1_0.md` (66 líneas; leí solo encabezados); `tests/test_arnes_sesion.py`.
* `[SUPUESTO]` que `tests/test_arnes_sesion.py` falla si `CLAUDE.md` no nombra el archivo de instrucciones de versión más alta (dirección lo pidió en `GEN2-ARNES-SESION-1`; no leyó el test). Si es falso: añádelo aquí, es perímetro de cierre.
* `[SUPUESTO]` que `tools/tablero_programa.py` ya deriva `instrucciones_vigentes` del árbol (pedido en `GEN2-TABLERO-SENAL-1` P2; no verificado). Si es falso: actualiza el valor donde viva y deja NC con sucesor para derivarlo.
* `[REPORTADO]` por ADR-544: V214 selló solo el lado repo porque la fecha de pegado llegó sin llenar.

4 · YA HECHO / YA DECIDIDO

Busqué por objeto «v2.15», «v2_15», «PLANTILLA-ENCARGO» en `git ls-files` (5 800+ archivos) y en `decisiones.tsv`, `firmas-pendientes.tsv`: 0 archivos con ese nombre; ninguna firma ni ADR de v2.15. Las 17 semillas existen como líneas de hallazgos, no como norma. Precedente de procedimiento: `GEN2-V214` (#867, ADR-544) — léelo y repite su mecánica (retiro de la versión anterior por T01, sidecars, `instrucciones_vigentes`), no la reinventes. Repite la búsqueda tú.

5 · PIEZAS

P1 · Las instrucciones, en dos cuerpos — la única pieza VERBATIM. El adjunto operativo entra como `instrucciones-proyecto-v2_15.md` byte a byte; no le cambies una coma: es texto firmado. `instrucciones-proyecto-v2_15-HISTORIA.md` = la HISTORIA v2.14 + una entrada por regla nueva o enmendada (§0, §2, D-18 a D-23, A.15, E.5, E.6) con el defecto que la motivó, fecha, PR y hallazgo, tomados de `hallazgos.md` y de las notas — no de memoria. Las semillas que el cuerpo no promovió se listan en la HISTORIA con una línea de por qué (ya cubierta por otra regla · es de una herramienta, no de norma · sin defecto repetido). v2.14 se retira como V214 retiró v2.13. Si crees que el cuerpo operativo tiene un error, no lo corrijas: FP a mesa y sigue. P2 · La plantilla. `forense/encargos/PLANTILLA-ENCARGO-v2_0.md`, byte-idéntica al adjunto, con sidecar sha256. `PLANTILLA-LOTE-v1_0.md` gana una línea de cabecera «SUCEDIDA POR…» y no se borra. P3 · `/acto`. Inserta el bloque adjunto como sección nueva entre `0-bis` y `CIERRE`, renumera, y ajusta el estilo al del archivo sin cambiar el sentido. Revisa el resto de `acto.md` y de `tramite.md` buscando frases que contradigan la nueva semántica (un «PARA» ante algo reversible y barato) y alinéalas; lista cada cambio en la nota con antes/después. En el CIERRE, el paso de `NO-CORRIDO` gana una frase: `FUERA-DE-PERÍMETRO` exige decir de qué otro acto es. P4 · Punteros. `CLAUDE.md` importa la v2.15. Todo archivo vivo (no encargos archivados, no notas, no ADR) que cite `instrucciones-proyecto-v2_14.md` por nombre: actualízalo — es el defecto T03, que ya ocurrió con v2.13. `AGENTS.md`: solo si cita la versión. P5 · Línea base del falsador. Un comando reproducible (en la nota, o como subcomando de una herramienta existente si cabe en ≤ 10 líneas) que cuente NC por token de razón en una ventana de fechas. Corre la ventana 16–20/sep y asienta el resultado: contra eso se medirá la plantilla en tres meses. P6 · ADR y A.9. El ADR cita la firma de A.9 verbatim si mesa la dio; si no, declara sellado solo el lado repo. Tablero: `instrucciones_vigentes`.

6 · LATITUD

Decides tú: redacción de la HISTORIA; estilo y ubicación exacta del bloque en `acto.md`; qué frases viejas alinear; si P5 es comando suelto o subcomando. Preguntas a mesa, y sigues: si una semilla no promovida te parece que sí debía ser norma (propón texto; no lo metas). No decides: el contenido del cuerpo operativo ni de la plantilla.

7 · PAROS (lista cerrada)

Editar el cuerpo operativo o la plantilla adjuntos · borrar versiones anteriores de instrucciones que V214 no borró · mover cualquier contador del programa · objetivo inalcanzable. No es PARO: un adjunto con sha discordante (pídelo), un test que falla por una cita vieja (arréglala), main movido (refresca).

8 · COMPUERTAS

Ninguna. Orden sugerido: P1 → P4 → P2 → P3 → P5 → P6.

9 · PERÍMETRO

Propio: `instrucciones-proyecto-v2_15*.md` y sidecars · retiro de `v2_14*.md` según V214 · `forense/encargos/PLANTILLA-ENCARGO-v2_0.md` · `PLANTILLA-LOTE-v1_0.md` (una línea) · `.claude/commands/acto.md`, `tramite.md` · `CLAUDE.md` · archivos vivos con la cita vieja · tests de arnés/T03 · tablero. Ajeno: `tools/corrida0.py`, `tests/check.py` salvo una cita · cualquier CALC, spec, `milpa/`, marcador. Perímetro de cierre: el permanente.

10 · NO HACE · SUCESORES · CIERRE

No reescribe encargos ya archivados al formato nuevo · no toca `AGENTS.md` más allá de una cita · no instrumenta ningún linter de encargos (D-14: aún no hay defecto que lo pida). Sucesor: a tres meses, el falsador de P5. Cascada de `/acto` · `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

- **qué:** el sello pleno de A.9 — el cuerpo operativo v2.15 y `PLANTILLA-ENCARGO-v2_0.md` pegados en el conocimiento del proyecto de Claude, con fecha confirmada por mesa.
  **por qué:** `DECISIÓN-DE-MESA-PENDIENTE`. La firma del lado proyecto viajó en este encargo como **propuesta** («mesa la confirma o corrige la fecha al lanzar»), no como firma dada; el ejecutor no tiene superficie de escritura fuera del repo. Precedente idéntico y por la misma causa: `ADR-544` / `GEN2-V214`.
  **impacto:** `instrucciones_vigentes = v2.15` queda sellado y derivado del lado repo, y la v2.15 rige ya en el repo y en toda sesión de Claude Code vía `CLAUDE.md`; falta la copia del proyecto de dirección para que A.9 esté cumplida en los dos lados.
  **sucesor:** `NC-0407` · `FP-399` — mesa pega los dos archivos y confirma la fecha; una enmienda fechada sobre `ADR-564` cierra la fila citándola verbatim.

- **qué:** reescribir los encargos ya archivados al formato de `PLANTILLA-ENCARGO-v2_0.md`.
  **por qué:** `FUERA-DE-PERÍMETRO` — de ningún otro acto, y es deliberado: §10 de este encargo lo excluye y A.3 prohíbe editar un encargo archivado. Se asienta para que la ausencia no se lea como olvido.
  **impacto:** ninguno — la sección `4 · EJECUCIÓN` de `/acto` define el default de `MODO` para los encargos anteriores a v2.15, así que ningún acto queda sin regla aplicable.
  **sucesor:** `SIN-ASIGNAR`; no lo requiere. `NC-0408`, CERRADA en este mismo acto.

- **qué:** la medición del falsador de la plantilla a tres meses del sello.
  **por qué:** `DIFERIDO-A:` el acto sucesor de diciembre/2026 — la ventana no ha transcurrido.
  **impacto:** sin ella no se sabe si la plantilla resolvió el defecto que la motiva (75/160 NC = 46.9 % en la ventana 16–20/sep/2026). No bloquea nada hoy: la línea base existe y es reproducible por comando.
  **sucesor:** `NC-0409` — `python3 tools/nc_por_razon.py --desde 2026-09-20 --hasta 2026-12-20`.

## CONSUMIDO

Ejecutado sobre la rama `claude/wonderful-johnson-8qs9qj`. `ADR-564` (número en disputa: dos ramas remotas vivas lo traen redactado — renumera quien fusione segundo, junto con `NC-0407`-`NC-0409` y `FP-399`). Cierre: `forense/notas/2026-09-20-GEN2-V215-cierre.md`.
