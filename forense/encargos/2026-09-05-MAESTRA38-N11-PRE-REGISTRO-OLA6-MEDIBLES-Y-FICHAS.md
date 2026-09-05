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
(5/sep/2026, entorno **NUBE**, rama `claude/acto-maestra38-n11-prereg-lauyln`),
SHA de redacción `b17d19bd` (= `origin/main` exacto al arrancar, sin
desfase — verificado dos veces: al ARRANQUE y de nuevo antes de la cascada,
`origin/main` no se movió). `COMPUERTA: ninguna`, declaración explícita del
encargo, sin verificación de gate. `data/raw` ausente (esperado en NUBE);
`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (no `sin_variable` como
anticipa el `ARRANQUE` de `/acto` — discrepancia declarada, no bloqueante:
el encargo mismo declara `ENTORNO: NUBE`, y este acto no abre microdato ni
depende de la variable); red externa bloqueada por política del entorno
(`curl` contra `inegi.org.mx`/`google.com` → `403` del proxy de agente,
`CONNECT tunnel failed`) — verificado con dos hosts distintos, no un solo
negativo sin examinar (A.13).

**A.8, verificado y con una corrección de premisa que el propio encargo no
tenía cruzada.** `ls forense/prereg-caja/ | grep -c "S[6-8]"` → `0`,
confirmado. `python3 tools/ya_medido.py` corrido en las 6 reglas (por `id`
y por `R-n`) → `NUNCA-MEDIDA` en las 6, pegado en cada spec y en las notas
de cola — pero **leído, no sólo pegado**: el cruce por fuente de
`canon/modelo-decision-v4_0.md §7` sí encuentra línea para `R9.2`, `R4.3` y
`cooperacion.comite.monitoreo_sancion_visible` (`R8.1`) — las tres tienen
veredicto `D` archivado en Hito D (`ADR-56`, 4/ago/2026, y `ADR-138`/
`ADR-143`, 20/ago/2026), que el vocabulario final de `ya_medido.py`
(`CORROBORADA`/`CONTRARIA`, el de espacio `L`) no cuenta como "medición" —
declarado en `S7 §0.2` y en las notas de cola de `R4.3`/`R8.1` (P2), sin
reabrir ningún veredicto (registro congelado, D-13). `R4.4`, `R10.3` y
`cooperacion.faena.sancion_social_pueblo_mestizo` confirmados **sin**
veredicto archivado en Hito D — primer intento de falsación pre-registrado
sobre esos tres `id`. **Corrección de premisa del propio encargo:** su
línea de A.8 describe `R4.4` como `(ENSANUT v2, adultos)` y `R9.2` como
`(ENSANUT/ENCUCI)` — verificado contra `forense/notas/2026-09-05-MAESTRA38-N10-cobertura-ola6.md`
§2.2/§2.5, el instrumento real que `N10` documenta para ambas es **ENNViH**
(`es09`/`es09a`×`cen10*` para `R4.4`; `ce19d_2`/`hs16d_2`×`cen12_1a`/`he25c`
para `R9.2`), con ENSANUT 2024 citado sólo como corroboración del desenlace
de `R9.2`, nunca como fuente primaria de ninguna de las dos, y `ENCUCI` no
aparece en la nota de `N10` en absoluto (`grep` exhaustivo, cero
apariciones). `S6`/`S7` se escribieron contra el instrumento que `N10`
realmente documenta, no contra el que el encargo resumía. Filas de cola
para las 3 candidatas, `grep` por nombre de `id` contra
`data/curacion-registro/cola-adquisicion-registro.tsv` antes de escribir →
`0`, confirmado (aunque las **fuentes** `CERO_DESABASTO` y `CNGMD` sí
tenían fila `OBTENIDO` previa, por otro propósito — declarado en P2).

**P1 — tres specs selladas (`forense/prereg-caja/`, 5 → 8), un commit cada
una.** `S6-L6-spec-v1_0.md` (`salud.atencion.grave`, `R4.4`), `S7-L7-spec-v1_0.md`
(`salud.vacunacion.disponible`, `R9.2`, con la corrección de premisa de
Hito D declarada en `§0.2`) y `S8-L8-spec-v1_0.md`
(`comunicacion.inseguridad.ver_oir_callar`, `R10.3`) — cada una con objeto
verbatim del canon, variables con texto de reactivo copiado del inventario,
universo, ponderador (declarado por precedente citado — `S7` deja la ola de
ENNViH pendiente de CAJA, declarado no adivinado), dicotomizaciones,
celdas, cota de numerador `< 10`, tabla de signo y la fila `NO-ESTIMABLE`
que `B-bis` exige, lista de archivos con id de manifiesto + `sha256`, frase
de sello y `.sha256` verificado con `sha256sum -c` al sellar. Nombres de
acto futuro `MAESTRA38-L6`/`L7`/`L8`, nuevos, asignados por este
pre-registro (D-13), sin colisión verificada.

**P2 — tres filas `PENDIENTE`.** Vía `tools/curador_registro/tsv_crudo.upsert_fila`
(mismo escritor canónico que `tools/arbitra.py`, nunca a mano sobre la
vista), `fila_origen` prefijado `MAESTRA38-N11:<id-de-regla>`:
`salud.adherencia.desabasto_vs_cuidadora` (necesidad `N36`, ya asignada
desde `ADR-279`), `cooperacion.comite.monitoreo_sancion_visible` y
`cooperacion.faena.sancion_social_pueblo_mestizo` (dominio cooperación sin
necesidad `N` asignada — verificado, `0` filas en
`data/curacion-registro/necesidad-objeto-modelo.tsv`, máximo actual `N41` —
se **propone** `N42`/`N43` en la nota de cada fila, **no se inventa ni se
inserta** la fila: ese archivo no está en el perímetro de este acto). Cada
nota declara honestamente que `PENDIENTE` aquí es evaluación de la
candidatura (abrir bytes en CAJA / desenlace faltante), no adquisición:
`CERO_DESABASTO` y `CNGMD` ya están `OBTENIDO` en el mismo registro, con
`id`s de manifiesto y `sha256` citados. Vista `data/cola-adquisicion-v1_0.tsv`
regenerada con `tools/vista_cola_adquisicion.py` (128 → 129 filas);
`tests/test_cola_writer.py` (5/5) en verde. **`PAQUETE-RECETAS-7`: no
creado.** Red externa confirmada bloqueada (arriba) — ningún `HEAD 200`
posible desde esta sesión; `SIN-FETCH` declarado explícitamente en las tres
notas de cola, tal como el `SPEC` de este encargo anticipa para este caso.

**P3 — corrección de mapa.** `canon/registro-rotulos.tsv` gana la línea
«`salud.vacunacion.disponible` es regla de `§3.9` (información); id
conserva prefijo por historia, dominio real = información» — corrección de
mapa, no de canon (`canon/modelo-decision-v4_0.md` intocado, la anomalía ya
la declaraba el propio canon en línea y `forense/hallazgos.md:40`).

**Cascada.** `ADR-342` (`canon/gobernanza-v1_15.md` §4, candidato derivado
contra el máximo real `341`, contiguo — coincide con el que el propio
encargo ya citaba). `canon/estado-programa-v1_12.md`: `L0` gana la
anotación de `ADR-342` (insertada antes de la de `ADR-341`, sin
reescribirla) y sube `341`→`342 ADR`; cabecera de conteo de `gobernanza`
(línea 27) recifrada igual. `canon/registro-rotulos.tsv`: fila
`MAESTRA38-N11` censada, junto a N2/N3/N4/N6/N8/N9/N10 (fila separada de la
corrección de P3). `data/INFRAESTRUCTURA-v1_0.md`: tres filas nuevas en la
tabla de `forense/prereg-caja/`, cabecera de la sección ampliada. `forense/
firmas-pendientes.tsv`: `FP-305` (recibo, no requiere firma). `forense/
tablero/TABLERO-PROGRAMA.md` (nota inline) y `forense/tablero/
TABLERO-PROGRAMA-v1_1.md` (`§8.10`): recibo completo.

**Anti-PR#77.** No aplica: este acto no descargó ningún payload nuevo — las
tres filas de cola citan `id`s de manifiesto ya `OBTENIDO` por actos
anteriores (`MAESTRA34-A1`, 2026-09-01), verificados por lectura de
`data/manifiesto.yaml`, no adquiridos aquí.

**Qué NO decide.** No mide nada de México (medición: cero, pre-registro,
declarado). No sella ninguna de las 3 reglas `MEDIBLE-COMO-ESTÁ` en canon —
siguen `(propuesta)`, dirección revisa, mismo estándar que las 2 originales
de `N5` y la de `N10`. No reabre ni discute ningún veredicto de Hito D
(`R9.2`, `R4.3`, `R8.1`) — registro congelado, citado, no tocado. No
inventa ni inserta necesidad `N` para cooperación — la propone en nota. No
crea `PAQUETE-RECETAS-7` — `SIN-FETCH` declarado con la razón (red
bloqueada, comando y salida a la vista). No toca `milpa/**`,
`canon/modelo-decision-v4_0.md` (salvo la cascada de `gobernanza`/`estado`),
`data/**` fuera de `cola`+vista e `INFRAESTRUCTURA` (explícitamente dentro
de perímetro), ni ninguna hipótesis de `MAESTRA38-N10`.

**Verificación.** `python3 tests/check.py --baseline`, corrido después de
cada pieza (P1, P2, P3, cascada): **LÍNEA BASE VERDE**, 3 FAIL / 170 WARN en
las cuatro corridas, sin entradas nuevas frente a `tests/baseline.json`
congelado (`accf688c`) — sin cambio frente a la línea base de `MAESTRA38-N10`.
`T25`/`T-YAMEDIDO` no disparan: ningún archivo nuevo trae rótulo `M`/`E`
pelado, y el encargo, cada spec (`§0.4`) y cada nota de cola citan
`NUNCA-MEDIDA` verbatim. Los tres `.sha256` verificados con `sha256sum -c`
al sellar. `tests/test_cola_writer.py`: 5/5 en verde.

**Contador.** Specs selladas: **5 → 8**, cumplido. Filas de cola: **+3**,
cumplido. Medición: **cero** — pre-registro, declarado, cumplido.

PR de este acto, contra `main`.
