ENCARGO · ACTO MAESTRA38-N8 · ESTADO-PROGRAMA-v1_12 — invoca /acto
SHA: a0e06da4 · COMPUERTA: fusión de N6 (para que los contadores que lee incluyan FP-298). ENTORNO: NUBE · NO en CAJA · MODELO: Sonnet (todo se deriva por comando; cero juicio). CARRILES: ninguno sobre canon/estado-programa*.
FIRMA — verbatim: la de N6. Razón medida: estado-programa-v1_11.md (2/sep) declara «motor de 10 reglas (9 medidas, 1 sin dato)»; grep -cE '^\s+- id:' milpa/tramite.yaml → 20. La «única fuente de estado» está a la mitad del estado.
A.8: v1_11 es «PROPUESTA — firma de mesa pendiente» (nunca sellada); las cifras que cita: motor, corredor, Hito D, manifiesto, relaciones, dominios, Ola 6. Cada una tiene comando en la casa (tramite.md, digesto_tramite.py, baseline.py, corpus.py en nube sin raíces → sólo lo que no exige bytes).
SPEC — un commit: canon/estado-programa-v1_12.md = v1_11 con cada cifra re-derivada y su comando al lado (motor 20 · manifiesto 1 281 · relaciones/procedencias/utilidad por baseline.py · ADR/FP máximos · dominios activos 4 · Ola 6 0/6 con salud 2/5 · reglas NO-ENCONTRADO 9 clasificadas 2/5/2 · specs selladas 5 · FAIL absorbidos 3 · descargas pendientes de mesa según PAQUETE-RECETAS-5/-6), sección «Qué espera a la caja» (A2 recenso, L2, C1, L4/L5) y «Qué no se sabe sin caja» (C1 físico real, [CENSO], ENFIH-4). v1_11 queda intacta (historia). Cabecera: «PROPUESTA — se sella con el merge de mesa». Enmienda in situ en v1_11: «superada por v1_12».
PERÍMETRO. Toca: canon/estado-programa-v1_12.md (nuevo) · v1_11 (una línea) · INFRAESTRUCTURA · tablero (recibo) · A.3 · cascada. NO toca: nada más. Si te encuentras escribiendo fuera de esta lista, PARA.
FP/ADR: ADR-340 · FP-301 recibo. CONTADOR: cifras de estado con comando 0 → todas · medición: cero.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-N8 · ESTADO-PROGRAMA-v1_12` (4/sep/2026, entorno
NUBE, rama `claude/estado-programa-v1-12-o79v07`).

**ARRANQUE.** Clon existente en `/home/user/Modelado-Mexicano`, `HEAD` al
arrancar `aaaaf2e` (== `origin/main`). `data/raw` ausente (esperado en NUBE).
`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (no `sin_variable` —
declarado, no PARO). Sonda de red a `inegi.org.mx` → `000` (bloqueada, NUBE).
`ls data/raw/` vacío. Este acto no abre microdato ni red.

**COMPUERTA.** `fusión de N6` verificada por producto: `git merge-base
--is-ancestor a0e06da4 HEAD` cumplido; `FP-298` → `EJECUTADA` en
`canon/gobernanza-v1_15.md` `ADR-338` (grep verificado, no por mención de
commit). Cumplida.

**SPEC.** `canon/estado-programa-v1_12.md` creado: §2 reescrita con cada
cifra re-derivada por comando (motor 20, manifiesto 1 281, relaciones
222/procedencias 223/utilidad 1:1 por `tools/curador_registro/baseline.py`,
ADR máximo 339/FP máximo 301, dominios activos 4, Ola 6 0/6 con `salud` 2/5,
las 9 reglas `NO-ENCONTRADO` clasificadas 2/5/2, specs de caja selladas 5,
FAIL absorbidos 3, 6 filas `PENDIENTE-DE-MESA` de `PAQUETE-RECETAS-5`/`-6`).
§9 «Qué espera a la caja» y §10 «Qué no se sabe sin caja» añadidas. §11 nota
de cierre propia con la tabla completa afirmación→comando. Detalle íntegro de
cada cifra y su comando: `canon/estado-programa-v1_12.md` §2/§11.

**Desviaciones D-13, declaradas (A.8, antes de fijar nada):**

1. **`estado-programa-v1_11.md` no queda intacta; se retira del árbol (`git rm`), no una
   enmienda de una línea.** El encargo repetía la misma premisa que su propio
   predecesor (`v1_10`→`v1_11`) ya tuvo que corregir: `tests/check.py::
   t01_single_source` exige una sola versión viva de
   `canon/estado-programa-v*.md`; dejar las dos hubiera sido un `FAIL` nuevo
   no baselineado. Se confirmó con el usuario antes de ejecutar (el `git rm`
   fue bloqueado por el clasificador de permisos como acción sensible;
   confirmado explícitamente antes de proceder). Historia recuperable con
   `git show 7574008:canon/estado-programa-v1_11.md` (el commit de A.3 de
   este mismo acto).
2. **ADR de este acto: `339`, no el `340` que citaba el encargo.** Re-derivado
   contra el árbol real al escribir la entrada: máximo `338` (`ADR-338`,
   `MAESTRA38-N6`); `MAESTRA38-N7` no tomó ningún ADR. Candidato contiguo
   `339`.
3. **FP de este acto: `301`, coincide con el encargo — pero como `ABIERTA`,
   no `RECIBO`.** `grep -oE '^FP-[0-9]+' forense/firmas-pendientes.tsv | ...`
   → máximo real `300`; candidato `301`, coincide. Se marcó `ABIERTA` (no
   `RECIBO -- no requiere firma`) siguiendo el precedente exacto de `FP-251`
   (la firma de mesa sobre `estado-programa-v1_11.md` en su propio nacimiento): un archivo
   `canon/` nuevo con cabecera `PROPUESTA — se sella con el merge de mesa`
   dispara `T22`(b) (marcador `PROPUESTA.*mesa` sin fila `ABIERTA`/`FIRMADA`
   que lo cite) — una fila `RECIBO` no lo satisface, sólo `ABIERTA`/`FIRMADA`
   cuentan para la auto-protección del tablero de firmas. La fusión del PR de
   este acto es la firma (regla 1 de maestra-34); no requiere acción
   adicional de mesa más allá de fusionar o rechazar.
4. **Cascada de citas, acotada a lo mecánicamente vivo, no a las 51 líneas
   totales.** `grep -rln "estado-programa-v1_11" tests/ .claude/ canon/` da 6
   archivos. `tests/check.py` usa `newest()` (glob, auto-adapta) en toda su
   lógica de test — sólo sus dos listas de exención (`HISTORICOS` de T03,
   `_T25_ARCHIVOS_CONOCIDOS` de T25) se actualizaron. `.claude/commands/
   acto.md` tenía una cita viva de ejemplo (CIERRE·3) que se actualizó a
   `v1_12`/`ADR-339`. Las citas de `canon/gobernanza-v1_15.md` (registro de
   decisiones ya selladas, §"Registro de artefactos" incluida — esta última
   sí se actualizó porque describe estado vigente, no historia fechada) y
   `canon/registro-rotulos.tsv` quedan tratadas caso por caso, no en bloque.

**Cascada.** `canon/gobernanza-v1_15.md`: `ADR-339` (§4), cabecera de conteo
`338`→`339 ADR` (línea 2), fila del "Registro de artefactos" (§2) actualizada
de `estado-programa-v1_11.md` a `estado-programa-v1_12.md`. `canon/
estado-programa-v1_12.md` §3 L0 recifrado (`338`→`339 ADR`, nueva anotación
insertada antes de la anterior, sin reescribirla; la anotación vieja marcada
`{cita-historica}` donde quedó desincronizada). `canon/registro-rotulos.tsv`:
fila `N · MAESTRA38-N8` censada. `data/INFRAESTRUCTURA-v1_0.md`: recibo de dos
párrafos. `forense/tablero/TABLERO-PROGRAMA.md`: nota de recibo. `forense/
tablero/TABLERO-PROGRAMA-v1_1.md`: `§8.7` recibo completo. `forense/
firmas-pendientes.tsv`: `FP-301` (`ABIERTA`, ver desviación 3).

**Verificación.** `python3 tests/check.py --baseline`: **LÍNEA BASE VERDE**,
3 FAIL / 171 WARN, sin entradas nuevas frente a `tests/baseline.json`
congelado (`accf688c`). `python3 tools/tablero_programa.py` corrido al cierre
confirma `adr_max=339`, `fp_max=301`, `encargos_archivados=317` (316→317, este
encargo). MODELO real de esta sesión: `claude-sonnet-5` (el encargo pedía
Sonnet — coincide).

**Contador.** Cifras de estado con comando 0 → todas: cumplido, `canon/
estado-programa-v1_12.md` §2/§11 trae comando o cita de archivo:línea para
cada afirmación de estado. Medición: cero — cumplido, ningún commit de esta
pieza abre microdato, corre censo real ni mueve tier alguno del motor.

PR de este acto, contra `main`.
