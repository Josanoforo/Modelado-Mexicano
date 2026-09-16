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
   `cola/`. El encargo, leído literalmente, pedía escribir los dos cierres
   y mover 18 `LANZADO-COMO` a histórico. **Corregido a mitad de acto por
   FIRMA DE MESA, 16/sep/2026** (recibida después de que este acto ya había
   ejecutado ambas piezas): los dos cierres quedan ratificados verbatim;
   el movimiento físico **no** — ver `NC-0249` abajo, `## CONSUMIDO`.
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

Tres filas. (`NC-0249` no aparece aquí: la firma de mesa que llegó a mitad
de acto la decidió y la cerró — ver `## CONSUMIDO` para la corrección de
curso completa.)

| # | qué (verbatim del encargo) | por qué | impacto | sucesor |
|---|---|---|---|---|
| 1 | `NC-0210` — reconciliar (o declarar por qué se conserva) la cifra `0.668937` de `milpa/tramite-ola5-propuesta-v0.yaml:2171` | `DECISIÓN-DE-MESA-PENDIENTE` | La medición ya existe y está sellada: `CALC-ENIF-0003` (`RESULT-ENIF-COB-C-VEREDICTO-0-668937 = NO-REPRODUCE`, validado independientemente por `ACTO GEN2-VALIDACION-INDEPENDIENTE-2` — control ciego, mismo veredicto negativo replicado sin ver el sello) confirma que `0.668937` no reproduce a 6 decimales ni sin ponderar (`0.668864`) ni ponderada (`0.654976`), delta `7.3e-05`. Lo que falta no es medir — es **autorización**: `milpa/` sólo se edita con firma de mesa que nombre el objeto explícito (regla que este mismo perímetro hereda de `GEN2-MANTENIMIENTO-Y-ARCHIVO-2`), y ninguna de las dos hojas de firmas existentes la cubre — la HOJA 1 (`GEN2-FIRMAS-MESA-1`) declara expresamente que `0.668937` «no es una» de las cuatro glosas que autoriza. No se fabrica una firma que no llegó. | `NC-0210` (sigue `ABIERTA`) — acto con una firma de mesa que nombre este objeto explícitamente |
| 2 | `NC-0212` — declarar en `CALC-ENIF-0002` el enlace `RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P` → `RES-0065` | `FUERA-DE-PERÍMETRO` (sello ajeno) | `CALC-ENIF-0002` está sellado (`spec_sellada: data/corrida0/CALC-ENIF-0002/spec.md`, con `sha256`) y depende de un payload de microdato crudo (`enif_2024_bd_csv.zip`) — E.3 prohíbe reescribirlo, y una sucesión que lo suceda no se sella sin CAJA (esta sesión es NUBE: `corpus=NO`, `data/raw` ausente, confirmado con `tools/entorno.py` antes de decidir). Mismo bloqueador exacto que `GEN2-MANTENIMIENTO-Y-ARCHIVO-2` ya documentó para esta misma fila (su fila 4 de `NO-CORRIDO/RESERVAS`) — se re-verifica, no se da por superado por inercia. La adopción de `RES-0065` sigue rotulada `control_c0=NO-DERIVABLE-DESDE-LA-SPEC` en `relevo-usos-v1_0.tsv`. | `NC-0212` (sigue `ABIERTA`) — acto en CAJA con `data/corrida0/CALC-ENIF-0002/` (o su sucesión) en perímetro |
| 3 | Incorporar `CALC-AGG-marco-M-sorteado-v1_3-ola-v3` y `CALC-C0D-ALCANCE-CORPUS-CAPTURA-SUCESOR` a las vistas canónicas (`data/corrida0/corridas.tsv`/`resultados.tsv`/`decisiones.tsv`) vía `corrida0 registro --verifica --escribe` | `PARO-ENTORNO` | `registro --escribe` se negó a escribir: sin forzar nada, detectó que 39 corridas **ajenas** (`CALC-ENIF-0003`, `CALC-R-DIN-M-01*`, `CALC-R-FAM-M-0[567]*`, etc.) bajarían de `REPRODUCE`/`IDENTICO` a `NO-EJECUTABLE`/`NO-REPRODUCE`/`DISTINTO` — no porque cambiaran, sino porque esta sesión NUBE no tiene `numpy`/`pandas`/`pyreadstat` ni `data/raw` para re-verificarlas. Mismo límite, mismo mecanismo de protección, que `ACTO GEN2-RELEVO-USOS-1` ya documentó (`NC-0211`): no se fuerza `--lote` para bajar el estatus verificado de corridas que esta sesión no puede re-comprobar. Las dos corridas nuevas quedan **selladas y verificadas individualmente** (`run`/`verify` propios, `verify=REPRODUCE`) pero fuera de las tres vistas agregadas hasta que ese registro se escriba desde un entorno con corpus. | `SIN-ASIGNAR` — acto en CAJA (`numpy`/`pandas`/`pyreadstat`/`data/raw` presentes) que corra `registro --verifica --escribe` |

## Corrección de curso a mitad de acto — FIRMA DE MESA, 16/sep/2026

Recibida después de que este acto ya había cerrado `NC-0158`/`NC-0174` y
movido 18 de los 52 `LANZADO-COMO` de `cola/` a `forense/encargos/`
(interpretación propia de "mover los 18 ... a histórico rotulado" del
mensaje que abrió este acto). Tres objetos, verbatim:

> OBJETO (NC-0248): se aprueban las propuestas §2.3 de VIGENCIA-DEUDA-1 (la
> DUPLICADA se cierra apuntando a la que queda; la RESUELTA-POR-PRODUCTO se
> cierra citando su PR) y las 20 enmiendas de premisa vencida quedan como
> sucesor vigente. OBJETO (NC-0249): los 52 encargos ejecutados permanecen
> en cola/ con ESTADO corregido en sitio (patrón 2-ter), no se mueven; el
> tablero filtra por ESTADO. OBJETO (NC-0246): las 9 195 identidades se
> consumen donde ya hacen falta — enadid2023:P3_27_AG va a CORR-0013 en la
> siguiente MEDICION-DEMANDA; mociba2015/2016/2017 van a la serie del panel
> F6 (F6-PANEL-CAJA-1 o su sucesor); enut2024/enfih2019 ya están completas,
> nada que hacer.

**`NC-0248`**: ratifica verbatim lo ya ejecutado — sin cambio.

**`NC-0249`**: **contradice** la interpretación de este acto. Se revierte
íntegramente el movimiento de los 18 archivos — `git show` contra el `HEAD`
anterior al acto (`9fd59d0`) reconstruye cada uno byte a byte en su ruta
original de `cola/`; verificado `diff` vacío para los 18. Las entradas de
`_T25_ARCHIVOS_CONOCIDOS` (`tests/check.py`) que apuntaban a la ruta nueva
vuelven a apuntar a la ruta de `cola/`. `NC-0251` (que se había cerrado
citando uno de los 18 como el homónimo que le faltaba) vuelve a `ABIERTA`.
Lo que la firma pide — "el tablero filtra por ESTADO" — ya estaba
entregado por `NC-0252` de este mismo acto, sin mover ningún archivo:
`NC-0249` cierra por esa vía, no por el movimiento revertido.

**`NC-0246`**: fuera del perímetro de este acto (no toca
`data/corrida0/mapa-demanda-19-corr-v1_0.tsv` ni consume `CORR-0012/0013/
0014`); registrada verbatim en `forense/no-corrido.tsv` para el acto
sucesor, sin ejecutar.

Ningún otro punto de este acto (`NC-0250`, `NC-0252`, `NC-0229`, `NC-0241`,
`NC-0242`, `NC-0210`, `NC-0212`) queda tocado por esta firma.
