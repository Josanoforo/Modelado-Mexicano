# ENCARGO · ACTO GEN2-TUBERIA-TABLERO-UNICO-1 · un solo tablero en el repo, que lea lo vigente

> ENTORNO: **NUBE**. El acto toca herramientas, CI, docs y gobierno, y no abre microdato. Si se asignara a CAJA sería el caso (e) de D-19. El hook de arranque imprime ENTORNO-DERIVADO; si no coincide, PARA en una línea.

CABECERA · SHA de redacción `5c8b42d3` · una sola sesión (D-17) · MODELO: Opus (lote con juicio) · MODO: AUTÓNOMO-AMPLIO · CONTADOR: mueve el semáforo y las siguientes acciones de los carriles (efecto buscado de P2 y P3); **no debe mover** lecturas, adopción, `celdas_validadas` ni `no_corrido_abiertas`, salvo por las NC y FP propias · FP, ADR y NC con raíz de acto, derivadas por `tools/cierre_acto.py` (D-24).

## 1 · OBJETIVO

Que el programa tenga un solo tablero: `forense/tablero/TABLERO-PROGRAMA.md`, con una sola página publicada. Hoy son cinco artefactos. El tablero debe llevar dentro los carriles y los pendientes. Sus carriles deben leer el catálogo, las reglas y las familias vigentes. No debe tomar como stopper una firma sobre el propio aparato. Además, dos asientos que el tablero necesita para no mentir: la diferencia de 16 en validación independiente y la firma de adopción del catálogo v1.4.

«Hecho», por comando sobre el commit final con `origin/main` fusionado:

1. **Un tablero con dos bloques nuevos.** `grep -c -x '<!-- TABLERO-UNICO:CARRILES:BEGIN -->' forense/tablero/TABLERO-PROGRAMA.md` da 1, y lo mismo para `TABLERO-UNICO:PENDIENTES`. Además, `python3 tools/tablero_programa.py --actualiza`, corrido dos veces seguidas, deja `git status --porcelain` vacío tras la segunda.
2. **Ningún otro tablero con cifras propias.**
   - `grep -c 'TABLERO-DERIVADO' forense/tablero/TABLERO-CARRILES.md docs/tablero-carriles.html` da 0 en los dos, o los archivos ya no existen.
   - Ningún archivo de `canon/`, `docs/` ni `README.md` enlaza a otro tablero que no sea `forense/tablero/TABLERO-PROGRAMA.md` o su página; lo verifica un comando `grep` que la nota cita.
3. **Carriles con los insumos vigentes.** Un test huérfano afirma cuatro cosas sobre la salida de `python3 tools/tablero_carriles.py --json`:
   - `procedencia.F2.archivo` es el catálogo que nombra `docs/data/catalogo-vigente.json`;
   - `F1`, `F3` y `F11` son la versión más alta de su serie en el árbol;
   - `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` no es stopper de ningún carril;
   - `FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01` sigue siéndolo de CARRIL-03 y CARRIL-18 (control positivo).
4. **Validación independiente reconciliada.** `python3 tools/corrida0.py status` y el libro `data/corrida0/validaciones-independientes.tsv` dan el mismo número de resultados con PASA. Si no lo dan, la nota lista por id los 16 de §3 con un dictamen cada uno.
5. **Firma del catálogo v1.4 asentada.** `python3 tools/consulta.py fp FP-260928-GEN2-CIERRE-Y-PRODUCTO-3-3c2e-01` da FIRMADA con PR #1337, o la nota dice por qué no (P5).

## 2 · FIRMAS DE MESA

- Ninguna viaja verbatim.
- La forma del cuerpo curado del tablero es la decisión de 5-bis. Sin firma, P1 hace (a) y la pieza del cuerpo queda como `DECISIÓN-DE-MESA-PENDIENTE`.
- `FP-260928-GEN2-TUBERIA-3-f18c-01` (el `[deriva]` no se fusiona solo) y `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01` (sacar `SIN-UNION` de la precedencia) siguen siendo de mesa y **no** son de este acto. Si mesa firma `c6aa-01` antes del cierre, su implementación entra a P3 como latitud.

## 3 · LO QUE DIRECCIÓN SABE

**Cinco artefactos de tablero.**
- [EJECUTADO] Sobre `5c8b42d3` viven cuatro:
  - `forense/tablero/TABLERO-PROGRAMA.md` (bloque derivado y un cuerpo curado);
  - `forense/tablero/TABLERO-CARRILES.md` (bloque derivado propio);
  - `docs/tablero.md` (copia del bloque del programa);
  - `docs/tablero-carriles.html`.
- [EJECUTADO] El quinto es el inventario `forense/analisis/pendientes-4/PENDIENTES-PROGRAMA-v5.md`.

**Cuerpo curado.**
- [LEÍDO] `forense/tablero/TABLERO-PROGRAMA.md` pone §2 en la línea 94 y §9 en la 231.
- [LEÍDO] El puesto de tablero entrega su propia capa curada, adjunta. En el repo esa capa no entra desde el 2/sep.

**Paso de CI.**
- [LEÍDO] `.github/workflows/verify.yml:733-738`: el job de derivados corre `tools/tablero_programa.py --actualiza`. Después corre `tools/tablero_carriles.py --actualiza` y hace `git add` de `forense/tablero/TABLERO-CARRILES.md` y `docs/tablero-carriles.html`.
- [LEÍDO] `tools/tablero_programa.py:270` y `tests/check.py:3050-3075` listan esos archivos.
- [LEÍDO] `canon/MEMORIA-OPERATIVA.md:49` cita los dos tableros.
- [LEÍDO] `README.md:11` enlaza al de carriles.
- [LEÍDO] `docs/PROTOCOLO-TABLERO.md` dice que una conversación no regenera el tablero, que eso es trabajo de CI.

**Versiones que lee el tablero de carriles.**
- [LEÍDO] `tools/tablero_carriles.py:171-180` fija por literal:
  - `canon/catalogo-del-mexicano-v1_3.tsv`,
  - `canon/reglas-contrastadas-v1_0.tsv`,
  - `forense/analisis/familias-2027/familias-2027-estado-v1_1.tsv`.
- [EJECUTADO] En el árbol existen el catálogo v1_4, las reglas v1_2 y las familias v1_2. `docs/data/catalogo-vigente.json` dice `{"catalogo": "v1_4"}`.
- [EJECUTADO] Las cabeceras de las versiones nuevas solo añaden columnas:
  - catálogo: `validacion_ciega_lote3` y `holdout_gastado`;
  - familias: `reverificacion_v1_2`;
  - reglas: cabecera idéntica.

**Simulación con las versiones vigentes.**
- [EJECUTADO] Copia del script con solo esas tres rutas cambiadas, corrida desde `tools/` y borrada después (árbol limpio).
  - Oficial: ROJO 7 · AMARILLO 21 · VERDE 0 · GRIS 3.
  - Simulado: ROJO 4 · AMARILLO 23 · VERDE 1 · GRIS 3.
  - CARRIL-03, 08 y 09 pasan de rojo a amarillo; CARRIL-19 pasa a verde.
  - Es una simulación del puesto, no un resultado: el acto re-deriva.

**Firma que el emparejador toma como stopper.**
- [LEÍDO] `tools/tablero_carriles.py:541-546` casa cada FP abierta con un carril si su texto (`qué_se_firma`, `gatea`, `dónde`, `encargo`) contiene un instrumento o un dominio del núcleo.
- [EJECUTADO] Por eso `c6aa-01` es stopper de 7 carriles (03, 08, 09, 12, 15, 19, 26) y siguiente acción de 4 (03, 09, 15, 19). Esa FP pregunta por la regla del semáforo y su texto nombra ENUT, ENCUCI y dominios.

**Diferencia de 16 en validación independiente.**
- [EJECUTADO] `status` da `resultados_con_validacion_independiente=5933`.
- [EJECUTADO] La vista `data/corrida0/resultados.tsv` tiene 215 resultados con PASA. El libro tiene 5 917 distintos con PASA.
- [EJECUTADO] Hay 16 resultados con PASA en la vista y sin fila PASA en el libro. Se listan con este comando:
  ```
  python3 -c "import csv,sys;csv.field_size_limit(sys.maxsize);rd=lambda p:list(csv.DictReader((l for l in open(p,encoding='utf-8') if not l.startswith('#')),delimiter='\t'));v={x['resultado_id'] for x in rd('data/corrida0/resultados.tsv') if x.get('validacion_independiente')=='PASA'};l={x['resultado_id'] for x in rd('data/corrida0/validaciones-independientes.tsv') if x['validacion_independiente']=='PASA'};print(sorted(v-l))"
  ```
  Los primeros son de EDER y de ENCIG 2023.
- [SUPUESTO] Son PASA anteriores al libro, heredados en la vista sin asiento.

**Firma de adopción del catálogo v1.4.**
- [LEÍDO] `forense/firmas-pendientes.tsv`, fila `FP-260928-GEN2-CIERRE-Y-PRODUCTO-3-3c2e-01`: dice que «El merge del PR es la adopción (E.2); vetar un instrumento = pedir su retiro antes del merge», y su estado es ABIERTA.
- [EJECUTADO] El PR #1337 se fusionó el 29/sep a las 09:50 −06:00 (`9a9fde23`).
- [EJECUTADO] El catálogo v1.4 marca ADOPTADO-CON-RESERVA-DE-ANCHO las filas nuevas de AUTORIDAD (142), TIEMPO (78) y RURAL_INDIGENA (77).

**Pendientes derivables hoy.**
- [EJECUTADO] `python3 tools/nc_por_clase.py --json` da 282 filas ABIERTA.
  - Por clase: DIRECCION-ENCARGO 152 · MESA-DECISION 42 · MESA-ACCION 40 · CANAL 23 · APERTURA 17 · ADQUISICION 7 · CAJA 1.
- [EJECUTADO] Las firmas abiertas son 41.
- [EJECUTADO] El adjunto `tablero_unico.py` los convierte en §11 y §12 del tablero del puesto. Es una propuesta, no una receta.

ADJUNTOS (el acto calcula su sha256 al recibirlos y lo asienta en el 0-bis):
- `TABLERO-PROGRAMA.md`: tablero único v2.24 del puesto, corte `5c8b42d3`.
- `tablero_unico.py`: generador de §11 y §12.
- `tablero_vista.py`: vista HTML con carriles y pendientes.

## 4 · YA HECHO / YA DECIDIDO

- **Búsqueda sin coincidencias útiles.** Se buscó «tablero único», «tablero unico» y `TABLERO-UNICO` en `forense/encargos`, `forense/notas`, `tools`, `canon` y `docs` (2 436 entradas). Hubo 2 coincidencias, las dos del 7/sep sobre el tablero de Gen 1 (`2026-09-07-MAESTRA38-TRAMITE-3.md`, `canon/gobernanza-v1_15.md:7748`). Se descartan por homónimas.
- **Encargos propuestos que tocan el tablero.** De los 16 en `forense/encargos/cola/PROPUESTOS/`, dos lo mencionan, y ninguno hace lo de este encargo:
  - `GEN2-PRODUCTO-CANON-2` crea `canon/mapa-dominios-v1_3.tsv` y excluye de su perímetro el bloque derivado del tablero. Por P2, el tablero lo leerá solo cuando exista.
  - `GEN2-TUBERIA-TESTS-Y-CHECK-2` quiere llevar familias de WARN a «un contador del tablero derivado».
- **Lo ya hecho.** `GEN2-TUBERIA-TABLERO-INSUMOS-1` (#1319) dejó en `status` la fecha de la vista y dueños completos en `nc_por_clase.py`. Este acto lo consume y no lo repite.
- Repite la búsqueda con tu acceso. Si algo ya está hecho, el entregable es decirlo.

## 5 · PIEZAS

- **P1 · Un solo tablero.**
  - **Qué produce.**
    - `tools/tablero_programa.py --actualiza` escribe, en el mismo archivo y en el mismo commit `[deriva]`, dos bloques nuevos: `TABLERO-UNICO:CARRILES` (de `tablero_carriles.py`) y `TABLERO-UNICO:PENDIENTES`.
    - El bloque de pendientes lleva las firmas abiertas con plazo y carriles que frenan, y la deuda abierta de `nc_por_clase.py --json` por dueño, fila por fila. Se usan los mismos nombres de marcador que el adjunto, para que el cuerpo del puesto y el del repo encajen.
    - `forense/tablero/TABLERO-CARRILES.md` y `docs/tablero-carriles.html` quedan como remisión sin cifras, o se retiran.
    - Una sola página en Pages. Portar `tablero_vista.py` o ampliar `docs/tablero.md` es decisión del ejecutor.
    - Se ajustan el paso de CI, las listas de `tablero_programa.py:270` y `check.py`, `MEMORIA-OPERATIVA` §5, `README.md:11` y `PROTOCOLO-TABLERO.md`.
  - **Cómo se sabe que quedó bien:** criterios 1 y 2.
  - **Si** retirar `TABLERO-CARRILES.md` rompe a un consumidor que no esté en §3, entonces queda como remisión y se declara el consumidor.
- **P2 · Los carriles leen lo vigente.**
  - **Qué produce.** Ninguna ruta con versión tecleada en `tablero_carriles.py`: la versión se resuelve del puntero (`catalogo-vigente.json`) o de la serie más alta. Así el parámetro vive en un solo sitio (D-15).
  - **Cómo se sabe que quedó bien:** criterio 3, primera parte.
  - **Si** una versión nueva cambia el esquema, entonces se lee por nombre de columna y la nota declara la columna.
- **P3 · El emparejador no toma firmas sobre el aparato.**
  - **Qué produce.** Una FP es stopper de un carril solo si gatea un instrumento, una ola o un payload del núcleo. Una FP sobre herramientas, reglas del tablero o gobierno no lo es. La regla la decide el ejecutor.
  - **Cómo se sabe que quedó bien:** criterio 3, segunda parte, con `c6aa-01` como caso de oro y `43d6-01` como control positivo.
  - **Gate D-14.** El defecto real es `c6aa-01`, siguiente acción de 4 carriles el 29/sep. Su costo para el lector: mesa leería que firmar una regla del tablero mide Rural Indígena.
- **P4 · La diferencia de 16.**
  - **Qué produce.** Dictamen por id de los 16 resultados con PASA en la vista y sin PASA en el libro: asiento en el libro con su evidencia, o retiro del PASA de la vista por el canal.
  - **Cómo se sabe que quedó bien:** criterio 4.
  - **Si** el SUPUESTO de §3 resulta falso, entonces la nota dice qué son.
- **P5 · Asiento de `3c2e-01` (A.12).**
  - **Qué produce.** Si el diff de #1337 no retiró ningún instrumento antes del merge, se asienta FIRMADA con PR #1337, con `INTERPRETACIÓN-DECLARADA`: el texto de la propia fila dice que el merge es la adopción. Si hubo retiros, se asienta con el «salvo» correspondiente.
  - **Cómo se sabe que quedó bien:** criterio 5.
  - **Si** mesa, al lanzar, dice que el merge no fue la adopción, entonces esta pieza no corre y queda como `DECISIÓN-DE-MESA-PENDIENTE`.

## 5-bis · OPCIONES

- **Situación.** El cuerpo curado de `forense/tablero/TABLERO-PROGRAMA.md` es de principios de septiembre. La lectura vigente (bitácora v2.24, ventanas, lectura de carriles) la tiene el puesto de tablero y no entra al repo. Mientras eso siga así, «un solo tablero» sigue siendo dos cosas.
- **Opciones.**
  - **(a) El tablero del repo queda solo con los tres bloques derivados y una cabecera corta; el cuerpo viejo se retira.** Costo: bajo. La lectura curada sigue viviendo solo en lo que entrega el puesto.
  - **(b) Lo de (a), y además este acto reemplaza el cuerpo curado por el del adjunto v2.24. Cada corte siguiente del puesto entra por `/tramite` como adjunto, que solo toca lo que queda fuera de los marcadores.** Costo: medio, un paso de trámite por corte. A cambio es el mismo archivo en todos lados.
  - **(c) No tocar el cuerpo.** Costo: el repo sigue mostrando una capa de hace cuatro semanas junto a cifras de hoy.
- **Recomendación: (b).** Es la única que deja un solo archivo para mesa, el puesto y Pages. CI ya reescribe solo lo que está entre marcadores, así que no hay dos productores de la misma línea.
- **Plazo:** antes del siguiente corte del puesto.
- **Texto de firma listo:** «Firmo la opción (b): el cuerpo curado del tablero es el del puesto, entra por /tramite como adjunto y CI solo reescribe los bloques entre marcadores.»

## 6 · LATITUD

Rige por norma la cláusula de autonomía v1.0. La sesión decide:
- el orden y cuántos PR;
- si el bloque de pendientes vive en `tablero_programa.py` o en una herramienta nueva;
- si la página es HTML o markdown;
- la regla exacta de P3.

Arreglar un defecto adyacente de ≤ 10 líneas es latitud, declarada.

## 7 · PAROS

La lista cerrada de D-19, sin añadidos.

## 8 · COMPUERTAS

- Que mesa firme 5-bis protege: **borrar**. Sin firma, el cuerpo curado del repo no se reemplaza; solo se retira lo que (a) retira.
- «Ningún catálogo, regla ni familia se edita; solo cambia cuál se lee» protege: **borrar**.

## 9 · PERÍMETRO Y CONCURRENCIA

- **Propio:**
  - `forense/tablero/TABLERO-PROGRAMA.md`, `forense/tablero/TABLERO-CARRILES.md`;
  - `tools/tablero_programa.py`, `tools/tablero_carriles.py`, una herramienta nueva de pendientes o de vista si la sesión la crea;
  - `docs/tablero.md`, `docs/tablero-carriles.html`, `docs/PROTOCOLO-TABLERO.md`;
  - `README.md`, solo el enlace al tablero;
  - `canon/MEMORIA-OPERATIVA.md` §5;
  - `.github/workflows/verify.yml`, solo el paso del tablero (733–738);
  - `tests/check.py`, solo las listas de archivos del tablero (3050–3075), y `tests/test_tablero_carriles.py`;
  - tests nuevos huérfanos;
  - `data/corrida0/validaciones-independientes.tsv`, solo las filas de P4;
  - `forense/firmas-pendientes.tsv`, la fila `3c2e-01` y las FP propias;
  - `data/INFRAESTRUCTURA-v1_0.md`.
- **Ajeno que no se toca:**
  - toda versión de `canon/catalogo-*`, `canon/reglas-contrastadas-*`, `canon/mapa-dominios-*` y `familias-2027-estado-*`;
  - el contenido que calcula `corrida0.py status`;
  - `forense/analisis/pendientes-4/`, que es historia.
- **Archivos que otro acto en vuelo está tocando:** el `[deriva]` en cola, que el canal recrea con otro nombre en cada corrida (al 29/sep 17:11 UTC es `derivados/auto-36600485698`, «trozo 3 tras 5c8b42d38: 20 CALC, quedan 53», que sustituyó a `derivados/auto-36598192555`). Toca `forense/tablero/TABLERO-PROGRAMA.md`, `forense/tablero/TABLERO-CARRILES.md`, `docs/tablero.md`, `docs/tablero-carriles.html` y otros 76 archivos. Verificado con `git diff --name-only origin/main...origin/derivados/auto-36600485698` sobre la única rama viva. Al arrancar, repite el comando sobre la `derivados/auto-*` que esté viva; si se fusiona durante el acto, se re-deriva encima.
- «Si te encuentras escribiendo fuera de esta lista, PARA.»
- Perímetro de cierre permanente según D-21.

## 10 · LO QUE NO HACE · SUCESORES · CIERRE

- **No hace:**
  - no implementa `f18c-01` ni `c6aa-01`;
  - no crea el crosswalk de dominios;
  - no adopta ni re-mide nada;
  - no corre la suite desde NUBE;
  - no edita ningún sello.
- **Sucesores:**
  - la opción (c) de `c6aa-01`, si mesa la elige;
  - `GEN2-PRODUCTO-CANON-2`, cuyo mapa v1_3 este tablero leerá solo por P2.
- **Auditoría:** no aplica, porque el acto no afirma nada sobre México.
