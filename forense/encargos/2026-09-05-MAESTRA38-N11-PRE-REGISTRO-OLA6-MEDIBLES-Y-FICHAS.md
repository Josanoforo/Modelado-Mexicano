ENCARGO · ACTO MAESTRA38-N11 · PRE-REGISTRO-OLA6-MEDIBLES-Y-FICHAS — invoca /acto
SHA: b17d19bd · COMPUERTA: ninguna (no depende de FP-303: sella lo que N10 ya clasificó MEDIBLE-COMO-ESTÁ y ficha lo CON-CANDIDATA; ninguna hipótesis se toca). ENTORNO: NUBE · NO en CAJA · MODELO: Opus. CARRILES: N12 (notas y PAQUETE-RECETAS-7; N11 no escribe ahí). Único acto sobre forense/prereg-caja/ y la cola.
FIRMA — verbatim (5/sep): «Revisa Para y dame siguiente encargos de nube.» + «no quiero hacerlo al mínimo» (4/sep): este acto no persigue el criterio 2; sella lo medible porque es medible.
A.8 contra b17d19bd: ls forense/prereg-caja/ | grep -c "S[6-8]" → 0; N10 §2 filas MEDIBLE-COMO-ESTÁ: R4.4 salud.atencion.grave (ENSANUT v2, adultos: síntoma grave × busca sistema público), R9.2 salud.vacunacion.disponible (id de §3.9; ENSANUT/ENCUCI, disponibilidad × aceptación), R10.3 comunicacion.inseguridad.ver_oir_callar (LAPOP AOJ, no denuncia × contexto de inseguridad). CON-CANDIDATA: R4.3 (adultos a0313/a0314/a0405b/a0405c + cuidadora), R8.1 (comité: monitoreo/sanción visible), R8.4 (faena: sanción social en pueblo mestizo) — ficha de N10 verbatim. ya_medido.py sobre las 6 → NUNCA-MEDIDA (N10 §5a) — pegar de nuevo, es la regla. Filas de cola para las 3 candidatas: grep por nombre → reporta (esperado 0).
SPEC (un PR, un ADR; commit por pieza):
P1 · S6, S7, S8: una spec por regla medible, patrón N7 (objeto verbatim del canon, variables con texto copiado del inventario, ponderador declarado, universo, dicotomizaciones, celdas, n mínimo por celda, signo que sostiene/refuta, se_mueve_si, lista de archivos con id de manifiesto + sha, y la fila B-bis: qué significa que el falsador no refute). Frase de sello y .sha256.
P2 · Tres filas de cola por writer (PENDIENTE, ficha de N10 como nota, necesidad N de salud/cooperación que corresponda; si cooperación no tiene N, se propone en nota y no se inventa); PAQUETE-RECETAS-7 sólo si la ficha trae URL verificable desde nube (HEAD 200 pegado); si no, SIN-FETCH declarado.
P3 · canon/registro-rotulos.tsv: línea «salud.vacunacion.disponible es regla de §3.9 (información); id conserva prefijo por historia, dominio real = información» — corrección de mapa, no de canon.
PERÍMETRO. Toca: forense/prereg-caja/S6-*, S7-*, S8-* + .sha256 · cola + vista · forense/notas/…PAQUETE-RECETAS-7.md (condicional) · canon/registro-rotulos.tsv · INFRAESTRUCTURA · tablero (recibo) · A.3 · cascada. NO toca: milpa/** · canon/modelo-decision* · data/** · hipótesis de N10. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR: ADR-342 · FP-305 recibo. CONTADOR: specs selladas 5 → 8 · filas de cola +3 · medición: cero (pre-registro).

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-N11 · PRE-REGISTRO-OLA6-MEDIBLES-Y-FICHAS`
(5/sep/2026, entorno **NUBE**, rama
`claude/acto-maestra38-n11-prereg-j5u7im`), SHA de redacción `b17d19bd`
(= `origin/main` exacto al arrancar y al cerrar, sin desfase —
verificado dos veces con `git fetch origin main`).

**A.8, verificado.** `ls forense/prereg-caja/ | grep -c "S[6-8]"` → `0`
antes de arrancar. `python3 tools/ya_medido.py` corrido sobre las seis
reglas de la ficha de `N10` antes de escribir cualquier spec:
`NUNCA-MEDIDA` en las seis, sin excepción, sin discrepancia contra
`N5`/`N6`/`N10`. `grep` por nombre de las tres candidatas contra la
cola (`data/cola-adquisicion-v1_0.tsv`, exacto por id de regla, no por
substring genérico): `0` filas antes de este acto — confirma el "0
esperado" del propio encargo.

**P1 · Tres specs selladas, `forense/prereg-caja/` 5 → 8, patrón `N7`,
cada una con corrección de premisa propia (A.8/D-13), ninguna
anticipada por el encargo.** `S6-L16-spec-v1_0.md`
(`salud.atencion.grave`, `R4.4`): el árbol trae **dos**
`EXISTE-SATISFACE` ya sellados para este `id` sobre reactivos que no se
solapan — `ENNVIH`+`ENDIREH` (`MAESTRA34-N5`/`MAESTRA37-L1`) y
`ENSANUT2024` (`MAESTRA37-L3`/`L3-BIS`) —, sin que ninguna nota los
reconcilie; la afirmación de `L3` de heredar de `N5` no se sostiene
contra el texto real de `N5` (`0` menciones de `ENSANUT`/`u0201`/
`H0409`). Corrige además que `cen10*` (el desenlace que `N5`/`N10`
describen) es solo geografía del lugar de consulta, no tipo de
institución, en las tres olas de `ENNVIH` verificadas. Pre-registra las
dos ramas como falsadores paralelos, sin adjudicar cuál prevalece —
fuera del perímetro de un pre-registro. `S7-L17-spec-v1_0.md`
(`salud.vacunacion.disponible`, `R9.2`, regla de §3.9 — ver `P3`):
corrige que la ficha original de `N5`/`N10` cita variables
(`cen12_1a`/`he25c`/`ce19d_2`/`hs16d_2`) que viven en
`data/inventario-reactivos-ext-v1_0.tsv`, no en `v1_1` como el resto
del acto `N10` usó; aporta además un **hallazgo nuevo, no citado por
`N5` ni `N10`**: el bloque `a0927a1`-`a0927e4` de
`adultos_ensanut2024_w.dta` (razón de no vacunación por vacuna
nombrada) prueba el `PORQUE` de la regla ("el hueco es logístico, no
actitudinal") más directamente que la ficha original. `S8-L18-spec-v1_0.md`
(`comunicacion.inseguridad.ver_oir_callar`, `R10.3`, hallazgo nuevo de
`N10`): corrige, variable por variable y ola por ola contra el
inventario, que el desenlace del módulo `AOJ` (`aoj1`/`aoj1a`/`aoj1b`)
existe **solo en la ola 2004** — no en "las mismas cinco olas" que
`N10 §2.6` describe de corrido —; acota el falsador a esa sola ola, con
2006/2019/2021/2023 citadas solo como evidencia de estabilidad del
antecedente en el tiempo. Las tres, un commit cada una, con su
`.sha256`.

**P2 · Tres filas nuevas en la cola de adquisición, vía el escritor
canónico** (`tools/curador_registro/tsv_crudo.upsert_fila` sobre
`data/curacion-registro/cola-adquisicion-registro.tsv`, vista
regenerada con `tools/vista_cola_adquisicion.py`): `salud.adherencia.
desabasto_vs_cuidadora` (`PENDIENTE`, cita la necesidad `N36` ya
registrada desde `ADR-279`), `cooperacion.comite.monitoreo_sancion_
visible` (`PENDIENTE`, cita `N28` ya registrada), `cooperacion.faena.
sancion_social_pueblo_mestizo` (`PENDIENTE`; verificado que esta regla
**no** tiene necesidad `N` asignada en `data/curacion-registro/
necesidad-objeto-modelo.tsv` — `0` filas para `R8.4` en las 41 de la
tabla —, a diferencia de sus tres hermanas de dominio (`N28`/`N29`/
`N30`); se **propone** `N42` en la nota de la fila, sin editar esa
tabla, fuera de perímetro (`NO toca data/**`, salvo la excepción
explícita "cola + vista")). Cada fila trae, como nota, el resumen
verbatim de la ficha correspondiente de `N10 §2.2`/`§2.4`.
**`PAQUETE-RECETAS-7`: `SIN-FETCH` declarado.** `curl -I` sobre las tres
URLs que las fichas citan (`cerodesabasto.org`, `mapadecuidados.
inmujeres.gob.mx`, `inegi.org.mx/rnm/index.php/catalog/977`) desde
NUBE, 5/sep/2026 → `000` en las tres (el proxy de egreso de esta sesión
rechaza la conexión externa, política de organización — mismo
resultado que la sonda de red del ARRANQUE de este mismo acto contra
`inegi.org.mx`) — 3 URLs examinadas, 0 alcanzables, declarado por A.13.
No se crea la nota condicional (el propio SPEC la condiciona a un
`HEAD 200` que no ocurrió).

**P3 · `canon/registro-rotulos.tsv`, corrección de mapa.** Línea nueva:
`salud.vacunacion.disponible` es regla de §3.9 (información), no de
§3.4 (salud); el `id` conserva el prefijo `salud.*` por historia —
`canon/modelo-decision-v4_0.md` queda intacto, la corrección es de
mapa, no de canon.

**Cascada.** `ADR-342` (candidato derivado por el comando de la casa
contra `341`, contiguo, coincide con el que el propio encargo ya
citaba). `canon/estado-programa-v1_12.md`: `L0` gana la anotación de
`ADR-342` (insertada antes de la de `ADR-341`, sin reescribirla), sube
`341`→`342 ADR`; la tabla de nombres estables (línea 27, cita también
el conteo de `gobernanza`) recifrada igual — corrigiendo en el camino
un `FAIL` de `T15` que esa línea, no cubierta por el paso 3 del skill
`/acto`, habría dejado desincronizado. `canon/registro-rotulos.tsv`:
fila `MAESTRA38-N11` censada, junto a la fila de corrección de mapa
(`P3`). `data/INFRAESTRUCTURA-v1_0.md`: tres filas nuevas en la tabla
de `forense/prereg-caja/`. `forense/tablero/TABLERO-PROGRAMA.md` (nota
inline) y `forense/tablero/TABLERO-PROGRAMA-v1_1.md` (`§8.10`): recibo
completo de este acto. `forense/firmas-pendientes.tsv`: `FP-305`
(recibo, no requiere firma — este acto no depende de `FP-303`, que
sigue abierta por cuenta de `N10`).

**Desviación D-13, declarada.** El primer sello de la entrada de
`ADR-342` en `canon/gobernanza-v1_15.md` citó, entre comillas de código,
el nombre de archivo de la nota condicional que este acto no crea —
disparó un `WARN` nuevo de `T03` (referencia colgante a un archivo
inexistente), contado como regresión por `--baseline`. Corregido a
prosa sin nombre de archivo entre comillas de código («la nota de
recetas PAQUETE-RECETAS-7»), mismo criterio que el resto del corpus usa
para nombrar artefactos condicionales que todavía no existen — este
mismo párrafo evita repetir el defecto.

**Qué NO hace este acto.** No mueve ningún tier del motor. No sella
ninguna de las tres clasificaciones `MEDIBLE-COMO-ESTÁ` que `N10`
propone — dirección/mesa revisa esa propuesta por separado; este acto
solo pre-registra el diseño que se correría si se sellan. No adjudica
cuál de los dos linajes de `S6` prevalece. No reclasifica
`salud.vacunacion.disponible` en `canon/modelo-decision-v4_0.md` — la
corrección de `P3` es de mapa, no de canon. No adquiere ningún payload
nuevo (`Cero Desabasto`/`CNGMD`/`MACU` ya estaban `OBTENIDO` antes de
este acto). No toca `milpa/**`, `canon/modelo-decision-v4_0.md`,
`data/raw` ni ninguna hipótesis de `N10`. Cero medición de México —
pre-registro puro, declarado y cumplido.

**Verificación.** `python3 tests/check.py --baseline`: **LÍNEA BASE
VERDE**, 3 FAIL / 170 WARN — sin cambio frente a la línea base de
`MAESTRA38-N10` (los dos `FAIL` nuevos que la propia cascada de este
acto introdujo — `T03`/`T15`, ver «Desviación» arriba — se corrigieron
antes del cierre, no quedaron absorbidos). Los tres `.sha256` de
`forense/prereg-caja/` verificados con `sha256sum` al sellar cada spec.

**Contador.** Specs selladas: **5 → 8**, cumplido. Filas de cola: **+3**
(candidatas de `N10`), cumplido. Medición: **cero**, cumplido —
pre-registro puro, ningún commit de esta pieza abre microdato ni corre
censo real.

PR de este acto, contra `main`.
