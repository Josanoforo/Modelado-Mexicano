# Encargo · `LOTE-RETRIAGE` — 20 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `2026-08-20-LOTE-RETRIAGE.md` |
> | **NOMBRE ESTABLE** | **`LOTE-RETRIAGE`** — cítalo así, nunca por nombre de archivo |
> | **SHA DE REDACCIÓN** | `867948c` (`origin/main` al arrancar el acto) |
> | **ESTADO** | **CONSUMIDO** — `PR` de `ACTO LOTE-RETRIAGE`, `ADR-131`, 20/ago/2026. Ejecutado **hasta `T0`**; `T1`-`T5` **NO se ejecutan**: `PARO` por ficha, cinco de cinco, por premisa refutada en la `VERIFICACIÓN A.8`. Ver `ADR-131` incisos (c)-(e). |

**Texto completo del encargo, tal como se lanzó** (verbatim, sin corregir; los rótulos pelados de su
cuerpo se conservan por la convención de `forense/encargos/` — es la cita la que se prefija, no el
documento fuente, `canon/registro-rotulos.tsv` filas 12-13):

---

2 · LOTE-RETRIAGE — UBUNTU · Opus · gate: ACT-PIL-2 fusionado
ENTORNO: UBUNTU (necesita corpus y microdato). NO nube.
Modelo: Opus; agentes sonnet supervisados para lo mecánico.
🚫 --freeze.  Dueña única: pgrep.  Doctrina de LOTE: PARO por ficha, no por lote.

Por qué va aquí y no después. Es el único acto de esta tanda que mueve un contador de medición. Hito D lleva 15 días en 13/27.

ARRANQUE (A.2 tres partes). Los cinco puntos. P3: enlaza data/raw a /home/pc0/mm-corpus/raw, reporta. P4: variable · sonda INEGI · ls data/raw/ | head -1, los tres crudos. type grep: la caja envuelve ugrep -I; usa command grep y un negativo de un comando que no examinó archivos no es un negativo (tres defectos medidos, TRANSFER §2).

VERIFICACIÓN A.8 — y trae una corrección al TRANSFER. ⚠️ Las cinco fichas B-bis ya existen en el árbol, verificado por listado: hitoD-R1_1-bbis-triage-v1_0.md · R4_1 · R4_2 · R4_3 · R7_2. Lo que falta es la corrida, no el triage. ⚠️ Y «Hito D 13→hasta 18» es optimista. Dos de las cinco ya tienen veredicto en archivo propio (hitoD-R1_1-veredicto-v1_0.md, hitoD-R7_2-veredicto-v1_0.md); las otras tres no. El techo realista es +3, no +5. ⚠️ Y no te doy el numerador de partida, a propósito. Intenté derivar cuántas de las 27 están archivadas y mi receta devolvió 3 contra el 13 que declara estado-programa:95 — la receta está mal y no te paso una cifra que no pude reproducir. T0: deriva el numerador con una receta que pruebes contra un caso cuya respuesta conozcas, y pega el comando junto al valor.

T0 · Numerador y disponibilidad. Deriva Hito D archivadas/27 con receta probada. Y por cada una de las cinco fichas, verifica que su instrumento está en data/raw con tests/manifiesto.py --verifica, una invocación por --id (A.1 — varios --id en una invocación solo verifica el último, sin aviso). Tres respuestas que no se colapsan: AUSENTE · raíz-no-configurada · hash-discordante. Si una ficha necesita ENFIH o ENSAFI, esa ficha espera a APERTURA-ENFIH-ENSAFI y las demás corren.

T1–T5 · Dos commits POR ficha, en este orden y sin excepción. COMMIT A — spec congelada: variables, universo, ponderador y diseño (FAC_*, EST_DIS, UPM_DIS de data/diseno-muestral.yaml), dicotomización, escala declarada, y qué significa que el falsador NO refute (B-bis: corroborada / acotada / falsador débil) con precedencia entre filas si dos pueden satisfacerse a la vez. Cierra con: «el primer resultado que produzca este procedimiento es el que se reporta.» Sin una sola cifra nueva. COMMIT B — la corrida: estimado · EE · IC95 · n · diseño aplicado · escala pegada · universo real (si difiere del pre-registrado se declara ACOTADO y no se compara contra un marginal poblacional, A-bis r4) · estampa A.10 · salida cruda a archivo. Marginal contra estratificado discordante → ASOCIACIÓN, se reporta, y no se «elige el bueno» (A-bis r1–r2). Un punto que satisface el umbral con un IC que no lo despeja no adjudica: propuesta con la reserva escrita. Si la spec estaba mal: tercer commit que lo dice. Nunca se corrige hacia atrás.

Cierre. ADR · filas por lo que quede abierto · nota con tabla por ficha · hallazgos · CONSUMIDO · --baseline VERDE en la caja. Contador: «Hito D archivadas: N→M de 27», los dos números dichos y derivados. PERÍMETRO. forense/hitoD-R*-veredicto-v1_0.md (las que corran) · forense/hitoD-preregistro-v2_0.md (solo el registro de veredictos) · salidas · gobernanza · tablero · estado-programa (cascada) · hallazgos · nota · encargo. Microdato solo lectura. si usas agentes que sean sonnet y tu supervisas.
