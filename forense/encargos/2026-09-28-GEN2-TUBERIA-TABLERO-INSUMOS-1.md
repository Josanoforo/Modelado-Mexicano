# ENCARGO · ACTO GEN2-TUBERIA-TABLERO-INSUMOS-1 · que cada corte del tablero se derive sin leer a mano lo que hoy se infiere

> ENTORNO: **NUBE** (herramientas, CI y gobierno; no abre microdato). NO: CAJA.

CABECERA · SHA de redacción 9d2550b9 · una sola sesión · MODELO: Opus · MODO: AUTÓNOMO-AMPLIO ·
CONTADOR: no mueve lecturas, adopción ni celdas; mueve la clasificación de NC y añade
líneas nuevas a `status`.

## 1 · OBJETIVO
El puesto de tablero debe poder derivar, en cada corte y sin inferencia manual, cuatro cosas:
la fecha de la vista, el estado de la suite, el dueño real de cada NC y los stoppers reales
de cada carril.
«Hecho», por comando sobre el commit final con origin/main fusionado:
 (1) `python3 tools/corrida0.py status` imprime `vista_publicada_commit`,
     `vista_publicada_fecha` y `deriva_en_cola`;
 (2) `python3 tools/resumen_suite.py lee` imprime un estado, no «ausente», o el acto
     documenta por qué el nocturno no lo publicó;
 (3) `python3 tools/nc_por_clase.py --json` no devuelve ninguna fila EN-CURSO cuyo acto
     tenga el encargo CONSUMIDO y la rama no viva;
 (4) toda fila ADQUISICION nombra su solicitud y toda fila APERTURA nombra su FP, o cada
     excepción queda listada con id por una guardia huérfana.

## 2 · FIRMAS DE MESA
Ninguna verbatim. La pieza P5 depende de la hoja de mesa del 28/sep, renglón 1
(FP-260928-GEN2-TUBERIA-3-f18c-01). Sin esa firma, P5 queda DECISIÓN-DE-MESA-PENDIENTE.

## 3 · LO QUE DIRECCIÓN SABE
[EJECUTADO] `ls data/derivados/suite-resumen.tsv` da ausente en 9d2550b9;
            `git log --all -- data/derivados/suite-resumen.tsv` no da ningún commit;
            no hay rama de resumen en origin.
[LEÍDO] .github/workflows/verify.yml:104-115 y 785-830: el resumen se construye solo en
        schedule o dispatch, y el job `resumen-suite` abre su propio PR.
[EJECUTADO] `nc_por_clase.py --json`: 42 filas EN-CURSO. Sus actos (TUBERIA-3,
            CALC-ALTERNOS-LOTE-1, PISOS-DOMINIOS-Y-REGLAS-1, C1-SUCESORES-Y-LOTE-3) tienen
            el encargo CONSUMIDO y la rama no está viva según `git ls-remote`.
[EJECUTADO] 19 de 27 filas ESPERA-ADQUISICION sin SOLICIT ni FP; 18 de 18
            ESPERA-APERTURA sin FP; NC-260928-GEN2-TUBERIA-3-f18c-04 SIN-ASIGNAR.
[EJECUTADO] `status` no declara la fecha de su vista; el último [deriva] fusionado es del
            28/sep 10:20 y derivados/auto-36495085433 está en cola.
[LEÍDO] canon/MEMORIA-OPERATIVA.md §5 da la ruta canon/TABLERO-PROGRAMA.md, que no existe.
[EJECUTADO] tablero_carriles: SIN-UNION es stopper ADQUISICION en 31 de 31 carriles.
[SUPUESTO] el nocturno no corrió o falló desde #1224. No verificable aquí: la API da 403.

## 4 · YA HECHO
Búsqueda en 1 088 encargos, en tools/ y en forense/notas de «vista_publicada»,
«deriva_en_cola», «fecha de la vista» y «rama no viva»: 0 coincidencias.
«lista cerrada de dueños» y «SIN-UNION»: solo en PENDIENTES-3 y TABLERO-CARRILES-1, que los
crearon. Repítela con tu acceso.

## 5 · PIEZAS
P1 · Fecha de la vista en `status`: commit y fecha del último [deriva] que tocó
     data/corrida0/usos.tsv, más el número de ramas derivados/auto-* abiertas.
     Si leer origin desde `status` rompe D-23, se deriva sin red o se declara NO-VERIFICABLE.
P2 · Resumen de la suite en main: diagnosticar por qué no hay ningún commit del TSV (run
     no ocurrido, job fallido o PR cerrado) y corregirlo. Si es por el auto-merge (P5),
     se dice y se deja listo.
P3 · Cierre hacia atrás de los cuatro actos: dictaminar las 42 NC y hacer que
     nc_por_clase marque VENCIDA-CANDIDATA cuando la rama no está viva y el encargo está
     consumido.
P4 · Dueños completos: nombrar la solicitud o la FP en las 37 filas y dar dueño a f18c-04.
     Guardia huérfana que liste las filas sin esos datos, justificada por D-14 con este
     defecto de 38 filas.
P5 · (depende de f18c-01) Dejar implementada la opción que firme mesa.
P6 · ≤ 10 líneas: corregir la ruta del tablero en MEMORIA-OPERATIVA y reasignar
     NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-02 a dirección.

## 5-bis · OPCIONES (regla del semáforo; decide mesa a propuesta de dirección)
Situación: SIN-UNION cuenta como stopper en todos los carriles, y los 7 rojos lo son porque
el catálogo no usa la etiqueta de dominio de su núcleo.
 (a) No tocar la regla. Costo: el tablero ordena mal la palanca de cada carril.
 (b) Sacar SIN-UNION de la precedencia y del conteo, y mostrarlo aparte. Costo: bajo;
     cambia la siguiente acción de unos 15 carriles.
 (c) (b) más un crosswalk de núcleo a catálogo (segmento joven, ENUT, ENCUCI) en una spec
     nueva. Costo: medio; puede mover rojos a amarillo.
Recomendación: (b) ahora y (c) como acto propio con spec.
Texto de firma: «Firmo la opción (b) para tools/tablero_carriles.py.»

## 7 · PAROS
Los de la lista cerrada D-19.

## 9 · PERÍMETRO
Propio: tools/corrida0.py (solo líneas nuevas de status), tools/nc_por_clase.py,
forense/no-corrido.tsv (dueños y dictámenes), .github/workflows/automerge-rutinas.yml
(solo P5), canon/MEMORIA-OPERATIVA.md (P6), un test huérfano nuevo.
Otro acto en vuelo toca: acto/GEN2-VALIDACION-Y-2027-1 escribe forense/no-corrido.tsv y
forense/firmas-pendientes.tsv; verificado con `git diff --name-only`.
«Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE
No cambia la regla del semáforo sin la firma de 5-bis. No mueve contadores de adopción.
No corre la suite desde NUBE.
Sucesores: el crosswalk de dominios (opción c), si mesa la elige.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| (P5) «Dejar implementada la opción que firme mesa» (auto-merge del `[deriva]`) | DECISIÓN-DE-MESA-PENDIENTE: `FP-260928-GEN2-TUBERIA-3-f18c-01` sigue ABIERTA (`firmada_en` vacío; la «hoja de mesa del 28/sep, renglón 1» no está en el repo) y fusionar sin revisión humana es regla de mesa; no se tocó `.github/workflows/automerge-rutinas.yml` | el PR `[deriva]` que abre el canal (incluido el del resumen de la suite) lo fusiona mesa a mano; la fecha de la vista sigue atrasada hasta entonces | NC `NC-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` (MESA 2026-10-05, FP f18c-01) |
| (§5-bis) opción (b) para `tools/tablero_carriles.py` | DECISIÓN-DE-MESA-PENDIENTE: §10 del encargo prohíbe cambiar la regla del semáforo sin la firma de 5-bis y ninguna vino verbatim; queda el texto de firma listo y la simulación de (b) sin escribir | el semáforo sigue con SIN-UNION como stopper de ADQUISICION en 31 de 31 carriles; con (b) cambiarían 15 siguientes acciones (matiz: CARRIL-13 y CARRIL-17 son ROJO) | NC `NC-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-02` y FP `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` (ABIERTA) |
| (P2) «`python3 tools/resumen_suite.py lee` imprime un estado» con el resumen publicado | NO-VERIFICABLE-AQUÍ: publicarlo exige el nocturno o un `workflow_dispatch` sobre `main` tras fusionar este PR y la suite no corre desde NUBE; el criterio se cumple por su segunda vía (el acto documenta por qué no se publicó: T27 y PR #1278 cerrado) | `resumen_suite.py lee` sigue diciendo «sin resumen publicado» hasta el primer nocturno con T27 resuelto | NC `NC-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-03` (MESA 2026-10-05) |
| (P4) «nombrar la solicitud o la FP en las 37 filas»: 13 ADQUISICION sin solicitud que sostenga la adquisición (no hay fila de cola, solicitud, expediente ni FP) | SUSTITUIDO-POR: excepción declarada por id con su razón en `tests/test_tablero_insumos.py` (`EXCEPCIONES`), que es la segunda vía del criterio (4); inventar una solicitud sería nombrar un objeto que no existe. Incluye `…LICENCIAS-1-1997-01`, que modifica el PR #1312 (acto en vuelo) | 13 filas ADQUISICION siguen sin objeto que las gatee; la guardia las lista por id y falla si aparece una nueva | quien registre la solicitud edita el dueño de la fila y la saca de `EXCEPCIONES` |
| (P4) FP para las 9 APERTURA sin FP | DECISIÓN-DE-MESA-PENDIENTE: abrir una ola reservada la levanta un pre-registro futuro o mesa por escrito (E.6); acuñar siete FP de mesa nuevas (N1–N7, texto listo en `forense/analisis/tablero-insumos-1/resultado-p4-apertura.tsv`) no lo revisó dirección (D-19) y `GEN2-APERTURAS-PREREGISTRADAS-1` (PR #1313) inventaría esas olas | 9 filas APERTURA sin FP; la guardia las lista por id | mesa decide cuáles N1–N7 se acuñan (hallazgo en `forense/hallazgos.md`) |
