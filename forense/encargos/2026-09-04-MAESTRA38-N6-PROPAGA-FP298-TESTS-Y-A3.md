ENCARGO · ACTO MAESTRA38-N6 · PROPAGA-FP298-TESTS-Y-A3 — invoca /acto

SHA: a0e06da4 · COMPUERTA: ninguna · ENTORNO: NUBE · NO en CAJA · MODELO: Sonnet. CARRILES: N7 (specs, forense/prereg-caja/ — disjunto), N8 (canon/estado-programa — disjunto). Este acto es el único que toca tablero, cola, milpa/propuesta, tests/check.py.
FIRMA — verbatim (4/sep): «Revisa los últimos PRs y dame los siguientes encargos para nube.» + §2 de este documento, archivado con el 0-bis.
A.8 contra a0e06da4: FP-298 ABIERTA; grep -c "T-A3\|FIRMAS-2" tests/check.py → 0; ls forense/encargos/ | grep -c "N1-lite" → 0; filas CNBV_PORTAFOLIO\|ENCRIGE_2020_FD en la cola → reporta (esperado 0; si >0, se enmienda la existente); situacion: HIPÓTESIS-SIN-INSTRUMENTO en propuesta → 0 (vocabulario nuevo: se documenta en mapea.md §4 junto a A.4).
SPEC (un PR, un ADR, commit por pieza):
P1 · FP-298: las 9 según §2 (append en propuesta, línea §7 en modelo-decision, dos filas de cola por writer, PAQUETE-RECETAS-6). FP-298 → EJECUTADA.
P2 · T-A3 y T-FIRMAS-2 en tests/check.py con docstring citando el defecto real (#518 encargo en commit no empujado; #530 sin encargo; FP-290/291 perdidas en merge). Control positivo obligatorio: contra a0e06da4 T-A3 debe FALLAR (existe ADR-335 sin encargo archivado) y T-FIRMAS-2 debe PASAR; después de P3, ambos VERDE. Pegar las dos salidas.
P3 · A.3 retroactivo de N1-lite con el texto pegado abajo, verbatim, como forense/encargos/2026-09-04-MAESTRA38-N1-lite-REPARA-TABLERO-Y-COLA.md, cabecera «archivado post-hoc por N6; ejecutado por PR #530 (ADR-335)», ## CONSUMIDO con #530. Hallazgo: una línea.
P4 · baseline.json recifrado sólo si P2 cambia conteos; hallazgos: N4 P3/P4 (razón correcta, omisión de dirección).
Texto de N1-lite, verbatim (dirección, 4/sep/2026), para P3:
ENCARGO · ACTO MAESTRA38-N1-lite · REPARA-TABLERO-Y-COLA (sólo repo) — invoca /acto. SHA: 68ce2a8d · COMPUERTA: ninguna · ENTORNO: NUBE · NO en CAJA · MODELO: Sonnet · CARRIL: N2 en paralelo. FIRMA — verbatim (4/sep): «Se me fue el internet y caja quedó fuera temporalmente fuera de servicio. La sesión se cortó y no pudo pushear nada. Algún encargo que podamos correr en nube?» Alcance reducido a propósito: nada que dependa de saber qué hay en disco (FP-286, FP-282, depósitos de mesa, ENFIH-4) queda fuera y se declara. A.8 contra 68ce2a8d: grep -c '^FP-291' forense/firmas-pendientes.tsv → 0 · filas CSES → 2 · ## INDETERMINADO → 46 · acto.md punto 3 sin la línea de enlace previo a compuerta. SPEC: P1 restaurar filas de 38-A1 como FP-291/FP-292 (creado=2026-09-03, nota «perdidas en merge #527»), enmienda in situ al encargo 38-A1, pegar T-FIRMAS; P2 CSES dedup (queda OBTENIDO, la PENDIENTE → SUPERADA-POR); P3 FP-290: 46 INDETERMINADO por dos reglas mecánicas (rótulo compartido hereda; resto ## CERRADO-POR-HISTORIA), FP-290 → EJECUTADA, FP-289 enterada; P4 línea en acto.md punto 3 (enlazar data/raw y raices.local.yaml antes de compuerta); P5 listar los 19 FAIL absorbidos → FP-293; hallazgos (A.12 no atrapó fila perdida; A2 ejecutado dos veces); receta de abiertas por prefijo en tramite.md. PERÍMETRO: tablero · cola (2 filas) + vista · encargo 38-A1 · 46 encargos (append) · nota N9 · acto.md · tramite.md · hallazgos · A.3 · cascada. NO toca: data/manifiesto.yaml · tests/** · tools/** · milpa/** · relaciones · estados de FP-286/282/288. FP/ADR: ADR-334 · FP-291/292 · FP-293 · FP-294 recibo. CONTADOR: abiertas 6 → 4 · medición: cero.
PERÍMETRO. Toca: tablero · cola + vista · milpa/tramite-ola5-propuesta-v0.yaml (append) · canon/modelo-decision-v4_0.md (append §7, una línea) · .claude/commands/mapea.md §4 · tests/check.py · tests/baseline.json · forense/encargos/2026-09-04-MAESTRA38-N1-lite-*.md (nuevo) · forense/notas/…PAQUETE-RECETAS-6.md · hallazgos · A.3 · cascada. NO toca: milpa/tramite.yaml · data/manifiesto.yaml · tools/** · forense/prereg-caja/ · canon/estado-programa*. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR: ADR-338 · FP-299 recibo. CONTADOR: abiertas 4 → 3 · tests con defecto real +2 · encargos sin archivar bajo MAESTRA38 1 → 0 · filas de cola +2 · medición: cero.

## Bloque VERIFICACIÓN DE EXISTENCIA (A.8, Parte 2 — `convencion.md`)

Contestado al archivar, 4/sep/2026, contra `a0e06da4`:

```
$ awk -F'\t' '$1=="FP-298"{print $6}' forense/firmas-pendientes.tsv
ABIERTA
$ grep -c "T-A3\|FIRMAS-2" tests/check.py
0
$ ls forense/encargos/ | grep -c "N1-lite"
0
$ grep -c "CNBV_PORTAFOLIO\|ENCRIGE_2020_FD" data/cola-adquisicion-v1_0.tsv
0
$ grep -c "CNBV_PORTAFOLIO\|ENCRIGE_2020_FD" data/curacion-registro/cola-adquisicion-registro.tsv
0
$ grep -c "HIPÓTESIS-SIN-INSTRUMENTO" milpa/tramite-ola5-propuesta-v0.yaml
0
```

Las cinco líneas del encargo confirman contra el árbol real: `FP-298` sigue `ABIERTA`
(mesa no la había firmado); ni `T-A3` ni `FIRMAS-2` aparecen en `tests/check.py`; ningún
encargo `N1-lite` está archivado; ninguna fila de cola trae `CNBV_PORTAFOLIO`/
`ENCRIGE_2020_FD` (el `P1` de abajo las crea, no las enmienda); el vocabulario
`HIPÓTESIS-SIN-INSTRUMENTO` no existe todavía en la propuesta (nuevo, se documenta en
`.claude/commands/mapea.md` §4 junto a A.4). Estado: `VIVO`.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-N6 · PROPAGA-FP298-TESTS-Y-A3` (4/sep/2026, entorno
NUBE, rama `claude/maestra38-n6-tablero-cola-ws89pf`), `ADR-338` (candidato derivado
contra el máximo real `337`, contiguo — coincide con el que el propio encargo ya
citaba). PR de este acto, contra `main`.

**P1.** `FP-298` → `EJECUTADA`. Mesa acepta, sin excepción de origen, la
clasificación con evidencia de `MAESTRA38-N5` (§3 de su nota). Cargadas en
`milpa/tramite-ola5-propuesta-v0.yaml`: 3 `HIPÓTESIS-SIN-INSTRUMENTO`
(`tramite.evasion.norma_inutil_sancion_improbable`,
`civico.transferencia.atribucion_lider`, `familia.cortejo.urbano_joven_apps`) y 2
`REFORMULABLE` como tercera formulación complementaria
(`civico.voto.clientelar_si_observable_lapop2019`,
`civico.protesta.agravio_urbano_multiola`), sin reabrir los sellos ya vigentes de
`MAESTRA35-L9`/`L11` (`D2-d`/`D2-f`, `canon/modelo-decision-v4_0.md` §7). Una línea
nueva en `canon/modelo-decision-v4_0.md` §7. Vocabulario `HIPÓTESIS-SIN-INSTRUMENTO`
documentado en `.claude/commands/mapea.md` §4. Dos filas nuevas de cola
(`CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO`, `ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF`)
vía el writer canónico (`tools/curador_registro/tsv_crudo.py::upsert_fila`, clave
`fuente_canonica`, sobre `data/curacion-registro/cola-adquisicion-registro.tsv`;
vista regenerada con `python3 tools/vista_cola_adquisicion.py`, nunca escrita a
mano). `forense/notas/2026-09-04-MAESTRA38-N6-PAQUETE-RECETAS-6.md`: **0 de 2**
recetas verificables — la red de este entorno NUBE bloquea `www.inegi.org.mx`
(`curl` → `000`; `$HTTPS_PROXY/__agentproxy/status` → `403` de política), así que
ninguna URL de `cnbv.gob.mx`/`condusef.gob.mx` pudo verificarse en esta sesión;
declarado en vez de fabricar una URL sin verificar (A.4/A.13).

**Hallazgo (D-13, de este mismo acto, no heredado).** `MAESTRA38-N5` clasificó las
9 reglas buscando solo con `busca_reactivos.py` contra `descargas_mx*`, sin cruzar
la propuesta ya acumulada ni `canon/modelo-decision-v4_0.md` §7: 2 de las 5
`SIN-INSTRUMENTO` (`dinero.ahorro.seguro_deposito_atenua_aversion`/`R1.5`,
`civico.voto.agencia_con_secreto`/`R7.3`) ya tenían instrumento medido por
`MAESTRA35-L9`/`L11` — `dinero.ahorro.seguro_deposito_enif2024` (`NO-DISCRIMINA`,
ENIF 2024 `P5_20`/`P5_23`, "acota, no cierra" `R1.5`) y `R7.3` ya
`CONTRARIA-REPLICADA` en dos instrumentos (LAPOP 2023 + ENCUCI 2020), degradada
`[FUERTE]`→`[MEDIA]` por la Enmienda D2-f. Ninguna de las dos se carga como
`HIPÓTESIS-SIN-INSTRUMENTO` — declarado en `canon/modelo-decision-v4_0.md` §7, la
fila `FP-298` de `forense/firmas-pendientes.tsv` y `forense/hallazgos.md` (entrada
del 4/sep/2026, dos líneas).

**P2.** `T-A3` (`T28`) y `T-FIRMAS-2` (`T29`) en `tests/check.py`, con docstring
citando el defecto real: el encargo `MAESTRA38-N1-lite` nunca llegó a un commit
empujado (firma verbatim de dirección: "se me fue el internet... la sesión se
cortó y no pudo pushear nada"), y `PR #530`/`ADR-335` ejecutó su restauración sin
encargo archivado — confirmado por la búsqueda exhaustiva de `MAESTRA38-N4`
(`git log --all -S "N1-lite"` vacío; 11 commits de `PR #530` revisados uno por
uno). La cita suelta de "`#518`" que circuló en prosa de mesa NO es este defecto —
el `PR #518` real es `MAESTRA37-A1`, sin relación (ya verificado por
`MAESTRA38-N4`). **Control positivo, salida pegada (contra el árbol de este acto
tras `P1`, antes de `P3`):**

```
$ python3 tests/check.py
  ...
  [FAIL]  T28 T-A3  (1 fail)
  [ ok ]  T29 T-FIRMAS-2
  ...
  · T-A3: 1
      ningún archivo `forense/encargos/*N1-lite*.md` trae una sección `## CONSUMIDO`
      que cite `PR #530`/`ADR-335` -- A.3 exige un encargo archivado para todo acto
      que ejecuta, y `PR #530` no tiene uno
```

**P3.** `forense/encargos/2026-09-04-MAESTRA38-N1-lite-REPARA-TABLERO-Y-COLA.md`
archivado, verbatim (texto pegado inline arriba, en este mismo encargo), cabecera
«archivado post-hoc por N6; ejecutado por PR #530 (ADR-335)», `## CONSUMIDO`
citando `PR #530`. Dos hallazgos de una línea en `forense/hallazgos.md` (el
defecto de `MAESTRA38-N4` era exactamente el que declaró; el hallazgo de `P1` de
arriba). **Después de `P3`, salida pegada:**

```
$ python3 tests/check.py
  ...
  [ ok ]  T28 T-A3
  [ ok ]  T29 T-FIRMAS-2
  ...
```

**P4.** `python3 tests/check.py --baseline`: LÍNEA BASE **VERDE**, sin entradas
nuevas frente a `tests/baseline.json` (3 FAIL / 170 WARN) — `P2` no cambia el
conteo final una vez `P3` archiva `N1-lite`, así que `tests/baseline.json` **no**
se recifra. Hallazgo `N4` P3/P4: la razón que dio (`N1-lite` no existe en ningún
lugar accesible del repositorio) era correcta — la omisión fue de dirección (no
pegar el texto inline la primera vez), no del ejecutor de `N4`; confirmado
verbatim en `forense/hallazgos.md`, entrada del 4/sep/2026, `MAESTRA38-N4`.

**Cascada.** `ADR-338` (`canon/gobernanza-v1_15.md` §4). `canon/estado-programa-
v1_11.md` L0 recifrado (337→338 ADR, anotación nueva insertada antes de la
anterior, sin reescribirla; dos cabeceras adicionales de conteo corregidas,
líneas 27 y 342). `canon/registro-rotulos.tsv`: fila `MAESTRA38-N6` censada.
`forense/tablero/TABLERO-PROGRAMA.md` (nota de recibo) y
`TABLERO-PROGRAMA-v1_1.md` (`B24` cerrado en §5, §8.5 nueva). `FP-299` recibo.
`python3 tests/check.py --baseline`: VERDE (verificación final, post-cascada).

**Anti-PR#77.** Este acto no descargó ningún payload — las dos fichas
`CON-CANDIDATA` quedan en la cola sin URL verificada (red bloqueada en NUBE);
no aplica.

