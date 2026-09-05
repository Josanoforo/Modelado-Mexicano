ENCARGO · ACTO MAESTRA38-N12 · SONDA-INSTRUMENTOS-DE-PERCEPCION — invoca /acto
SHA: b17d19bd · COMPUERTA: ninguna (N12 es la condición previa propuesta para FP-303, no su consecuencia). ENTORNO: NUBE con red (sonda de alcanzabilidad como control: pegar el código de https://www.inegi.org.mx/ y de https://losmexicanos.unam.mx/ — si la nube no alcanza UNAM, se declara y la parte de fetch pasa a caja: nube no persiste bytes). NO descarga microdato (anti-PR#77: nube no persiste bytes). MODELO: Opus (lectura de cuestionarios contra instrumentos mínimos; juicio de identidad). CARRILES: N11.
FIRMA — verbatim: la de N11 + §2 de este documento (propuesta de dirección sobre FP-303, no firmada: el acto explora, no declara).
A.8 contra b17d19bd: candidatas y su estado hoy — Los mexicanos vistos por sí mismos (UNAM-IIJ 2015, 25 encuestas): manifiesto 0 · cola 0 · notas 0 → NO-ENCONTRADO en el programa (grep -ic "vistos por s\|losmexicanos"); ECOPRED 2014: 0/0/0; Cultura Constitucional (UNAM-IIJ): 0/0/0; MxFLS/ENNViH: manifiesto 198, verificar si inventario-reactivos-* indexa su texto de reactivo (grep -c "ennvih\|mxfls" data/inventario-reactivos-descargas-mx-v1_1.tsv y v1_2/ext → reporta); ENADIS: 16 entradas en manifiesto (38-A1), cruzada por N10 → sin cambio. Los 19 instrumentos mínimos: N10 §2, columna «instrumento mínimo», verbatim. Todas las candidatas nuevas son SIN-FETCH hasta este acto (A.6).
SPEC — dos commits. COMMIT-1 congela: los 19 instrumentos mínimos (pregunta + población, copiados de N10), la lista cerrada de fuentes a sondear (las 4 de arriba + las que el ejecutor derive de N10 §5c por homonimia resuelta, declaradas antes de abrir nada), y el criterio de acierto: un ítem cuenta si mide el antecedente o el desenlace de la regla en la misma persona con la población de la regla — parecido nominal no cuenta (N10 §5c: “jefe”, “cortes”, “favor”, “grave”). COMMIT-2: (a) sonda de alcanzabilidad por fuente antes de contenido (v2.2; los tres hallazgos distintos); (b) cuestionario/codebook de cada fuente abierto y leído — para UNAM-IIJ, las 25 encuestas una por una, nombrando cuál; (c) por instrumento mínimo: CUBIERTO-POR (fuente, ítem, texto copiado) / PARCIAL (qué falta) / SIN-COBERTURA-EN-ESTAS-FUENTES con universo; (d) por fuente que cubra ≥1: ficha de adquisición (acceso: público / registro gratuito / solicitud), receta ≤1 min, fila de cola por writer PENDIENTE o PENDIENTE-DE-MESA; (e) MxFLS: si su texto no está indexado, el hallazgo es «fuente en corpus fuera del inventario» y se pide indexación en caja (no se indexa desde nube). Subproducto declarado, no lanzado: forense/notas/…N12-modulo-propio-v0.md — los instrumentos mínimos que quedaron SIN-COBERTURA, redactados como ítems de un módulo propio (texto, escala, población), con la nota de que levantar es adquisición con costo y decisión de mesa.
Cierre: tabla 19 × (cubierto / parcial / sin cobertura) y, por dominio, cuántas hipótesis de N10 cambiarían de clase si la fuente se adquiere. Enmienda a FP-303 (append, fechada): «N12 corrió: k de 19 con cobertura fuera del SNIEG». Hallazgos: una línea por fuente que el programa no conocía.
PERÍMETRO. Toca: forense/notas/2026-09-0X-MAESTRA38-N12-{spec,sonda,modulo-propio-v0}.md · cola + vista (filas nuevas por writer) · PAQUETE-RECETAS-8 · tablero (recibo, enmienda FP-303) · hallazgos · A.3 · cascada. NO toca: canon/** (salvo ADR) · milpa/** · forense/prereg-caja/ · data/manifiesto.yaml · inventarios. No descarga. Si te encuentras escribiendo fuera de esta lista, PARA.
FP/ADR: ADR-343 · FP-306 recibo. CONTADOR: instrumentos mínimos con cobertura conocida 0 → k de 19 · fuentes de percepción sondeadas 0 → n · medición: cero (sonda).

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-N12 · SONDA-INSTRUMENTOS-DE-PERCEPCION`
(5/sep/2026, entorno **NUBE**, rama
`claude/maestra38-n12-instrumentos-6m3fz0`), SHA de redacción declarado
`b17d19bd` (= merge de `MAESTRA38-N10`; `origin/main` real al arrancar
era `e2c7828` — un commit más, el merge de `MAESTRA38-N11` — verificado
`git merge-base --is-ancestor b17d19bd HEAD` cumplido; no PARO, ARRANQUE·2,
sin solape de perímetro entre `N11`/`N12`). PR de este acto:
**[#542](https://github.com/Josanoforo/Modelado-Mexicano/pull/542)**,
contra `main`.

**A.8, verificado antes de tratar la premisa del encargo como cierta.**
Los tres `grep` de candidatas contra los archivos exactos que el encargo
nombra (`data/manifiesto.yaml`, `data/cola-adquisicion-v1_0.tsv`,
`data/curacion-registro/cola-adquisicion-registro.tsv`,
`forense/notas/`) confirman `0/0/0` para *Los mexicanos vistos por sí
mismos*, `ECOPRED` y *Cultura Constitucional* — el encargo tenía razón.
`ennvih|mxfls` en `data/manifiesto.yaml`: **198**, coincide. En
`data/inventario-reactivos-descargas-mx-v1_1.tsv`: **0** (no la cifra
que el encargo dejaba abierta) — pero **17 181** en
`data/inventario-reactivos-ext-v1_0.tsv`: `MxFLS`/`ENNViH` **sí** está
indexada, y ya fue agotada por `MAESTRA34-N5`/`MAESTRA38-N10` contra
estas mismas 19 reglas — corrige la premisa (e) del SPEC (declarado en
`spec.md §0` y `sonda.md §6`). `ENADIS` en manifiesto: **12**, no `16`
como cita el encargo — discrepancia de conteo declarada, sin
consecuencia sobre este acto (no es una de las 4 candidatas).
`python3 tools/ya_medido.py` sobre las 19 ids del universo, antes de
escribir cualquier clasificación: `NUNCA-MEDIDA` en las 19, sin
excepción, sin discrepancia contra `N10`.

**COMMIT-1 (`forense/notas/2026-09-05-MAESTRA38-N12-spec.md`).** Congela
los 19 instrumentos mínimos `HIPÓTESIS-SIN-INSTRUMENTO` de `N10 §2`
(pregunta + población, verbatim — una excepción declarada:
`trabajo.prestaciones.formalidad_pesa_mas_que_salario` no trae
frase-pregunta verbatim en `N10`, se marca como tal en vez de
fabricarla). Lista cerrada de 4 fuentes (las nombradas por el encargo);
búsqueda de fuentes derivables por homonimia resuelta de `N10 §5c`
contra 15 catálogos locales (`data/inventarios/*`,
`data/mapa-fuentes-*.tsv`): **cero derivadas** (A.13) — la resolución de
las homonimias solo refuerza la pertinencia de una fuente ya nombrada
(*Los mexicanos vistos por sí mismos*), no suma una quinta. Criterio de
acierto congelado verbatim del encargo.

**COMMIT-2 (`…N12-sonda.md`).** Sonda de alcanzabilidad por **tres**
mecanismos independientes, más estricta que el precedente de `N11`
(que solo corrió `curl`): `curl` (`000` en ambos hosts), estado del
proxy de egreso (`403` a `CONNECT`, `policy denial`, ambos hosts) y
`WebFetch` (`EGRESS_BLOCKED`, ambos hosts) — **INEGI y UNAM bloqueados
por igual**, no solo uno. Las 3 fuentes externas quedan `SIN-FETCH`;
`MxFLS`/`ENNViH` no depende de red, ya está agotada (ver A.8 arriba).
Las 19 quedan `SIN-COBERTURA-EN-ESTAS-FUENTES`, universo declarado (`0`
de `4` fuentes con lectura nueva posible hoy) — ninguna forzada a
`PARCIAL`/`CUBIERTO-POR` sin haber leído contenido real. Cuántas de las
19 cambiarían de clase si las 3 fuentes `SIN-FETCH` se adquieren:
declarado **no estimable** sin abrirlas — no se inventa una cifra.
`PAQUETE-RECETAS-8`: `0` recetas verificadas de ≤1 minuto (declarado,
mismo patrón que `RECETAS-6`/`-7`), 3 propuestas sin ejecutar. Fichas de
adquisición para las 3 fuentes `SIN-FETCH`, 3 filas nuevas en la cola
(`tools/curador_registro/tsv_crudo.py::upsert_fila`, clave
`fuente_canonica`; vista regenerada con
`tools/vista_cola_adquisicion.py`) — las 3 `PENDIENTE`. Subproducto
`…N12-modulo-propio-v0.md`: los 19 redactados como ítem/escala/
población — **declarado, no lanzado**.

**Cascada.** `ADR-343` (candidato derivado por el comando de la casa
contra `342`, contiguo, coincide con el que el propio encargo ya
citaba). `canon/estado-programa-v1_12.md`: `L0` gana la anotación de
`ADR-343` (insertada antes de la de `ADR-342`, sin reescribirla),
`342`→`343 ADR`; la tabla de nombres estables (línea 27) y la cabecera
propia de `canon/gobernanza-v1_15.md` (línea 2, `T15` la exige aparte de
`L0` — corregido en el camino, ver «Desviación» abajo) recifradas igual.
`canon/registro-rotulos.tsv`: fila `MAESTRA38-N12` censada.
`forense/tablero/TABLERO-PROGRAMA-v1_1.md` (`§8.11`): recibo completo de
este acto, con la enmienda a `FP-303` puesta ahí — no en su fila de
`forense/firmas-pendientes.tsv`, fuera del perímetro explícito del
encargo (que solo autoriza tocar «tablero»). `forense/firmas-pendientes.tsv`:
`FP-306` (recibo, no requiere firma — este acto no depende de `FP-303`,
que sigue abierta por cuenta de `N10`).

**Desviación D-13, declarada.** El primer sello de la entrada de
`ADR-343` recifró `L0` pero no la cabecera propia de
`canon/gobernanza-v1_15.md` (línea 2, `**342 ADR**`) — disparó un `FAIL`
nuevo de `T15`, contado como regresión por `--baseline`. Corregido antes
de cerrar: la cabecera de `gobernanza-v1_15.md` es una segunda fuente
del mismo número que el paso 3 del skill `/acto` no distingue
explícitamente de `L0` — mismo defecto de clase que `MAESTRA38-N6` ya
había corregido una vez para la tabla de nombres estables de
`estado-programa`, aplicado aquí a la cabecera de `gobernanza` misma.

**Qué NO hace este acto.** No mide nada de México (medición: cero,
sonda, declarado por el propio encargo). No descarga ningún payload ni
abre microdato (`data/raw` ausente, no aplica — `ENTORNO` no lo pedía).
No sella ninguna clasificación de `N10`. No decide si las 3 fuentes
`SIN-FETCH` se adquieren — eso es de mesa, con las fichas de
`…N12-sonda.md §4` como insumo. No indexa nada nuevo en
`inventario-reactivos-*` (`MxFLS`/`ENNViH` ya estaba indexada). No toca
`canon/modelo-decision-v4_0.md`, `milpa/**`, `forense/prereg-caja/` ni
`data/manifiesto.yaml`. No firma `FP-303` en su nombre — la enmienda es
información adicional para la firma de mesa.

**Verificación.** `python3 tests/check.py --baseline`: **LÍNEA BASE
VERDE**, 3 FAIL / 170 WARN — sin cambio frente a la línea base de
`MAESTRA38-N11` (el `FAIL` nuevo de `T15` que la propia cascada de este
acto introdujo se corrigió antes del cierre, no quedó absorbido, ver
«Desviación» arriba).

**Contador.** Instrumentos mínimos con cobertura conocida: **0 de 19**,
cumplido (declarado, no forzado). Fuentes de percepción sondeadas:
**4 de 4** — 2 bloqueadas por red (`ECOPRED`, *Los mexicanos vistos por
sí mismos*), 1 sin necesidad de red y ya agotada (`MxFLS`/`ENNViH`), 1
sin host confirmado (*Cultura Constitucional*). Medición: **cero**,
cumplido — sonda pura, ningún commit de esta pieza abre microdato ni
corre censo real.
