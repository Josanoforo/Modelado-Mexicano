ENCARGO · ACTO MAESTRA38-N5 · DISEÑO-9-REGLAS-SIN-INSTRUMENTO — invoca /acto

SHA: 0ff3d710 · COMPUERTA: ninguna · ENTORNO: NUBE · NO en CAJA · MODELO: Fable (diseño de fase; Opus como mínimo). CARRILES: N3 (append en propuesta — coordinar: N5 escribe una nota, no la propuesta).
FIRMA — verbatim: la de N3. Insumo: 38-A1 §censo-9: 48 payloads nuevos no movieron 8 de 9 reglas NO-ENCONTRADO; la 9ª (N34) tiene señal adyacente en ENCRIGE.
A.8: forense/notas/2026-09-03-MAESTRA38-A1-censo-9-no-encontrado.md (las 9 con su búsqueda); data/inventario-reactivos-descargas-mx-v1_1.tsv en repo → tools/busca_reactivos.py --tablas descargas_mx_v1_1 corre en nube sin bytes; canon/modelo-decision-v4_0.md §3 (texto de cada regla, driver, tier); Ola 6 criterio 2 (ADR-265: ≥3 EXISTE-SATISFACE por dominio). Ninguna de las 9 tiene hoy un falsador ejecutable escrito.
SPEC — dos commits. COMMIT-1: las 9 reglas con su objeto medible tal como está escrito, y antes de proponer nada, el criterio de clasificación: (a) REFORMULABLE — existe en el inventario un reactivo que mide el mismo driver con otro desenlace; (b) SIN-INSTRUMENTO — el objeto exige una condición que ningún instrumento nacional mide (se escribe cuál, con el busca_reactivos a la vista, universo y términos); (c) CON-CANDIDATA — fuente nombrada, pendiente de adquisición (N34/ENCRIGE). COMMIT-2: por regla, la clasificación con evidencia, y para (a) el objeto reformulado + reactivo + instrumento + se_mueve_si; para (b) el instrumento hipotético mínimo que la haría medible (una pregunta, una población) y la recomendación RETIRAR-DE-OLA6 / MANTENER-COMO-HIPÓTESIS; para (c) la ficha de adquisición. Producto: forense/notas/2026-09-0X-MAESTRA38-N5-diseno-9-reglas.md + propuesta PENDIENTE-DE-MESA por regla en una tabla, sin tocar canon ni propuesta — mesa decide con la tabla y N-siguiente propaga.
PERÍMETRO. Toca: la nota · tablero (recibo + una fila «mesa decide las 9») · A.3 · cascada. NO toca: canon/** · milpa/** · data/**. Si te encuentras escribiendo fuera de esta lista, PARA.
FP/ADR: ADR-338 · FP-298 recibo · FP-299 decisión de mesa (vence 7 días). CONTADOR: reglas NO-ENCONTRADO con clasificación y falsador 0 → 9 · medición: cero — es diseño.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-N5 · DISEÑO-9-REGLAS-SIN-INSTRUMENTO` (4/sep/2026,
entorno NUBE, rama `claude/maestra38-9-reglas-clasificacion-2fzsa9`). Dos commits en
`forense/notas/2026-09-04-MAESTRA38-N5-diseno-9-reglas.md`, tal como pedía el SPEC:

**COMMIT-1.** Las 9 reglas `NO-ENCONTRADO` (§censo-9 de `MAESTRA38-A1`) transcritas
verbatim contra `canon/modelo-decision-v4_0.md` §3 (id, cita de línea, tier, texto
SI…ENTONCES…PORQUE), su objeto medible sin clasificar aún, y el criterio de
clasificación (a) REFORMULABLE / (b) SIN-INSTRUMENTO / (c) CON-CANDIDATA con la regla
operativa declarada para no contar ruido de substring como (a). Nota metodológica
añadida: `tools/busca_reactivos.py` indexa reactivo de hogar, nunca serie
administrativa — importa para la regla 3.

**COMMIT-2.** Clasificación con evidencia, 33 corridas de `busca_reactivos.py --tablas
descargas_mx_v1_1` (42536 filas, superset de la tabla `descargas_mx` v1_0 que
`MAESTRA38-A1` examinó). Resultado, **distinto del "8 de 9 en cero" que A.8 citaba
contra el universo de A1** — la premisa se corrige contra el universo de HOY, no se
hereda (D-13): **2 REFORMULABLE** (`civico.voto.clientelar_si_observable`, vía LAPOP
AmericasBarometer México 2019, `clien1n`/`clien1na`/`clien4a`/`clien4b`, ya en corpus;
`civico.protesta.agravio_urbano`, vía LAPOP multi-ola 2004-2023, outcome+agravio+falla
estatal+red previa+urbano cada uno con reactivo propio), **5 SIN-INSTRUMENTO**
(`tramite.evasion.norma_inutil_sancion_improbable`, `dinero.ahorro.
seguro_deposito_atenua_aversion`, `civico.voto.agencia_con_secreto`, `civico.
transferencia.atribucion_lider`, `familia.cortejo.urbano_joven_apps` — cada una con
instrumento hipotético mínimo y recomendación `MANTENER-COMO-HIPÓTESIS`, ninguna se
recomienda `RETIRAR-DE-OLA6`: en las 5, la ausencia de instrumento es hueco de
diseño, no imposibilidad estructural), **2 CON-CANDIDATA** (`dinero.credito.
scoring_alternativo`, objeto administrativo/IMOR vía CNBV, estructuralmente invisible
al buscador; `dinero.credito.baja_friccion_usura_dano_downstream`/`N34`, vía ENCRIGE
FD completo + CONDUSEF). Tabla `PENDIENTE-DE-MESA` completa en la nota, §3. Cero
regla cerrada, cero falsador corrido, cero microdato abierto — el contador declarado
por este encargo (medición: cero) se cumple.

**Cascada.** `forense/firmas-pendientes.tsv`: `FP-297` (recibo) y `FP-298` (decisión
de mesa sobre la tabla, vence 11/sep/2026). `forense/tablero/TABLERO-PROGRAMA.md`
(nota de recibo) y `TABLERO-PROGRAMA-v1_1.md` (bloqueador `B24` en §5, recibo §8.4 en
la bitácora).

**Desviaciones D-13, declaradas.** (1) **No se abre `ADR-338`.** El PERÍMETRO de este
encargo excluye `canon/**` sin la excepción "salvo ADR" que sí traía `MAESTRA38-N3`
— toda entrada de gobernanza vive en `canon/gobernanza-v1_15.md`, bajo `canon/`;
abrirla habría violado el perímetro explícito. La propagación a canon queda para el
acto sucesor que mesa dispare tras firmar `FP-298`, como el propio SPEC ordena. (2)
**`FP-297`/`FP-298`, no `FP-298`/`FP-299`** como citaba el encargo — comando de la
casa contra `forense/firmas-pendientes.tsv` al escribir esta pieza:
`grep -oE '^FP-[0-9]+' forense/firmas-pendientes.tsv | sort -t- -k2 -n | tail -1` →
`FP-296` (máximo real de filas; `FP-297` solo aparecía en prosa de
`canon/gobernanza-v1_15.md`, candidato descartado de `MAESTRA38-N4`, nunca como fila
propia) — contiguo, `FP-297`/`FP-298`, off-by-one contra lo citado. (3) Un fix de
`T25` (D-6, `ADR-128`): la variable de encuesta LAPOP `LAPOP-E8` (ítem de
organización, `civico.protesta.agravio_urbano`) colisiona, sin el prefijo, con el
patrón letra-más-dígito pelado que vigila `T25` — se reescribe con prefijo de fuente
en las 6 citas, razón declarada en la nota misma.

**Verificación.** `python3 tests/check.py --baseline`: LÍNEA BASE VERDE (3 FAIL / 171
WARN, sin entradas nuevas frente al `baseline.json` congelado — el WARN sube de 170 a
171 por el archivo nuevo de esta pieza entrando al censo de reportes, no por defecto
nuevo). MODELO real de esta sesión: `claude-sonnet-5` (el encargo pedía Fable con
Opus como mínimo — MODELO es una preferencia de asignación de la sesión que ejecuta,
no algo que este acto pueda cambiar retroactivamente sobre sí mismo; declarado, no
escondido).

PR de este acto, contra `main`.
