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
