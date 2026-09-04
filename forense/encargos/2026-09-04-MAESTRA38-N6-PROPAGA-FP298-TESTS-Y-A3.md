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
