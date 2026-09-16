# ACTO GEN2-MANTENIMIENTO-3

> Archivado por A.3 (0-bis) — texto **verbatim** del mensaje de dirección
> que lanzó este acto, 16/sep/2026. No se edita en ningún otro punto salvo
> las secciones `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` que la cascada
> añade al final (pasos 10 y 11 de `/acto`).

---

NUBE · ACTO GEN2-MANTENIMIENTO-3 (Sonnet; un solo trámite integral, después
de tu firma sobre la auditoría): NC-0248 — escribir los cierres que
VIGENCIA propuso (la duplicada, la resuelta-por-producto, y mover los 18
LANZADO-COMO de la cola a histórico rotulado); NC-0250 (encargos fuera de
cola/), NC-0252 (tablero), NC-0241/0242 (los dos RESULT sucesores del
marcador), NC-0210/0212, NC-0229 (S6-L16-spec v1_6)

---

## Lectura del encargo, antes de ejecutar

Mensaje corto (formato v2.12, D-12) que cita ocho filas de
`forense/no-corrido.tsv` por número, sin repetir su texto. El "tu firma
sobre la auditoría" es la aprobación de mesa sobre
`forense/notas/2026-09-16-GEN2-VIGENCIA-DEUDA-1-cierre.md` (`ACTO
GEN2-VIGENCIA-DEUDA-1`, `PR #806`, fusionado — verificado antes de arrancar,
§0 del ARRANQUE de este mismo acto). Cada fila se leyó completa en
`forense/no-corrido.tsv` antes de decidir qué hacer con ella; el detalle de
cada una vive en su propia entrada de esa tabla y no se transcribe aquí dos
veces.

Las ocho piezas, con lo que cada una pedía y por qué:

1. **`NC-0248`** — VIGENCIA propuso dos cierres a mesa sin aplicarlos
   (`NC-0158` DUPLICADA de `NC-0161`; `NC-0174` RESUELTA-POR-PRODUCTO) y
   dejó evidenciada, sin ejecutar, la disposición de los `LANZADO-COMO` de
   `cola/`. El encargo pide escribir los dos cierres y mover los 18
   `LANZADO-COMO` cuya copia de cola es su único registro (disposición
   `ARCHIVAR`, distinta de los 30 `RETIRAR` — redundantes contra un
   homónimo externo ya con `## CONSUMIDO` — que NC-0249 sigue dejando para
   mesa, porque este encargo pide *mover a histórico*, no *retirar/borrar*).
2. **`NC-0250`** — el trasplante erróneo `## CONSUMIDO · PR #742` (real:
   `#737`) en el encargo **archivado** (`forense/encargos/`, fuera de
   `cola/`); VIGENCIA solo corrigió la copia de cola por perímetro.
3. **`NC-0252`** — `tools/tablero_programa.py::cola_encargos` clasifica por
   el substring literal `"## CONSUMIDO"` del cuerpo crudo en vez de la
   cabecera `ESTADO:` real, y ningún test lo cruza contra el árbol.
4. **`NC-0241`/`NC-0242`** — los dos hallazgos que `ACTO GEN2-MARCADOR-C0-D`
   dejó como "RESULT sucesor" pendiente, ambos sobre sellos ajenos que ese
   acto no tocó por perímetro: `NC-0241` (el filtro de `ic95` que
   `RESULT-AGGOLA-PUNTOS-POR-EJE-CON-IC` prometía y no aplicaba) y
   `NC-0242` (la derivación de alcance sobre las 648 capturas de
   `corridas-L` que `NC-0078` pedía).
5. **`NC-0210`/`NC-0212`** — dos filas `FUERA-DE-PERÍMETRO` de actos
   previos que citan explícitamente a este acto como su propio sucesor
   (`GEN2-MANTENIMIENTO-Y-ARCHIVO-2`, filas 2 y 4 de su
   `## NO-CORRIDO / RESERVAS`): se re-verifican contra el árbol de hoy, no
   se dan por resueltas por inercia.
6. **`NC-0229`** — la mitad de `NC-0209` que `GEN2-MANTENIMIENTO-Y-ARCHIVO-2`
   dejó declarada y sin abrir: `forense/prereg-caja/S6-L16-spec-v1_6.md`
   sucesora de `v1_5` (sellada, intacta), que retire la remisión a `FP-372`
   como decisión pendiente — `FP-372` ya está `FIRMADA` (opción a).

Perímetro: `forense/no-corrido.tsv`, `forense/encargos/` (dentro y fuera de
`cola/`), `tools/tablero_programa.py` + su test, `forense/prereg-caja/`
(spec sucesora nueva, nunca las selladas), `data/corrida0/` (solo CALC
sucesores nuevos, `repite_de` declarado, nunca un sello ajeno reescrito) y
la cascada de cierre. `milpa/` solo donde una firma lo autorice
explícitamente (mismo criterio que `GEN2-MANTENIMIENTO-Y-ARCHIVO-2`) — no
hay firma nueva adjunta a este mensaje.

## NO-CORRIDO / RESERVAS

Tres filas.

| # | qué (verbatim del encargo) | por qué | impacto | sucesor |
|---|---|---|---|---|
| 1 | `NC-0210` — reconciliar (o declarar por qué se conserva) la cifra `0.668937` de `milpa/tramite-ola5-propuesta-v0.yaml:2171` | `DECISIÓN-DE-MESA-PENDIENTE` | La medición ya existe y está sellada: `CALC-ENIF-0003` (`RESULT-ENIF-COB-C-VEREDICTO-0-668937 = NO-REPRODUCE`, validado independientemente por `ACTO GEN2-VALIDACION-INDEPENDIENTE-2` — control ciego, mismo veredicto negativo replicado sin ver el sello) confirma que `0.668937` no reproduce a 6 decimales ni sin ponderar (`0.668864`) ni ponderada (`0.654976`), delta `7.3e-05`. Lo que falta no es medir — es **autorización**: `milpa/` sólo se edita con firma de mesa que nombre el objeto explícito (regla que este mismo perímetro hereda de `GEN2-MANTENIMIENTO-Y-ARCHIVO-2`), y ninguna de las dos hojas de firmas existentes la cubre — la HOJA 1 (`GEN2-FIRMAS-MESA-1`) declara expresamente que `0.668937` «no es una» de las cuatro glosas que autoriza. No se fabrica una firma que no llegó. | `NC-0210` (sigue `ABIERTA`) — acto con una firma de mesa que nombre este objeto explícitamente |
| 2 | `NC-0212` — declarar en `CALC-ENIF-0002` el enlace `RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P` → `RES-0065` | `FUERA-DE-PERÍMETRO` (sello ajeno) | `CALC-ENIF-0002` está sellado (`spec_sellada: data/corrida0/CALC-ENIF-0002/spec.md`, con `sha256`) y depende de un payload de microdato crudo (`enif_2024_bd_csv.zip`) — E.3 prohíbe reescribirlo, y una sucesión que lo suceda no se sella sin CAJA (esta sesión es NUBE: `corpus=NO`, `data/raw` ausente, confirmado con `tools/entorno.py` antes de decidir). Mismo bloqueador exacto que `GEN2-MANTENIMIENTO-Y-ARCHIVO-2` ya documentó para esta misma fila (su fila 4 de `NO-CORRIDO/RESERVAS`) — se re-verifica, no se da por superado por inercia. La adopción de `RES-0065` sigue rotulada `control_c0=NO-DERIVABLE-DESDE-LA-SPEC` en `relevo-usos-v1_0.tsv`. | `NC-0212` (sigue `ABIERTA`) — acto en CAJA con `data/corrida0/CALC-ENIF-0002/` (o su sucesión) en perímetro |
| 3 | `NC-0249` — disposición física de los 30 `RETIRAR` (homónimo externo ya con `## CONSUMIDO`) y de 4 candidatos con cabecera propia contradictoria (`LISTO-CAJA`/`NO LANZADO`/`LISTO PARA FIRMA`/sin sello confirmado en ningún lado: `GEN2-SONDA-3-PILOTO-CAJA`, `GEN2-F5-DOCUMENTAL-EJECUCION-PENDIENTE`, `POST-723/31-…-PARA-FIRMA`, `POST-723/29-…-CONTRATO`) | `DECISIÓN-DE-MESA-PENDIENTE` | Este encargo pedía **mover a histórico** los `LANZADO-COMO` cuya copia de cola es su único registro — los 18 `ARCHIVAR` se ejecutaron. Retirar/borrar una copia redundante es una acción distinta y más destructiva que este mensaje no pidió, y los 4 excluidos necesitan que mesa confirme si de verdad pertenecen al lote de 52 antes de tocarlos (sus propias cabeceras dicen lo contrario de `LANZADO-COMO`). Ninguno de estos 34 archivos se movió ni se borró. | `NC-0249` (sigue `ABIERTA` con el residuo) — mesa decide `RETIRAR` sí/no y resuelve los 4 casos ambiguos |
| 4 | Incorporar `CALC-AGG-marco-M-sorteado-v1_3-ola-v3` y `CALC-C0D-ALCANCE-CORPUS-CAPTURA-SUCESOR` a las vistas canónicas (`data/corrida0/corridas.tsv`/`resultados.tsv`/`decisiones.tsv`) vía `corrida0 registro --verifica --escribe` | `PARO-ENTORNO` | `registro --escribe` se negó a escribir: sin forzar nada, detectó que 39 corridas **ajenas** (`CALC-ENIF-0003`, `CALC-R-DIN-M-01*`, `CALC-R-FAM-M-0[567]*`, etc.) bajarían de `REPRODUCE`/`IDENTICO` a `NO-EJECUTABLE`/`NO-REPRODUCE`/`DISTINTO` — no porque cambiaran, sino porque esta sesión NUBE no tiene `numpy`/`pandas`/`pyreadstat` ni `data/raw` para re-verificarlas. Mismo límite, mismo mecanismo de protección, que `ACTO GEN2-RELEVO-USOS-1` ya documentó (`NC-0211`): no se fuerza `--lote` para bajar el estatus verificado de corridas que esta sesión no puede re-comprobar. Las dos corridas nuevas quedan **selladas y verificadas individualmente** (`run`/`verify` propios, `verify=REPRODUCE`) pero fuera de las tres vistas agregadas hasta que ese registro se escriba desde un entorno con corpus. | `SIN-ASIGNAR` — acto en CAJA (`numpy`/`pandas`/`pyreadstat`/`data/raw` presentes) que corra `registro --verifica --escribe` |
