ENCARGO · ACTO MAESTRA38-N7 · PRE-REGISTRO-CIVICO-LAPOP — invoca /acto
SHA: a0e06da4 · COMPUERTA: ninguna · ENTORNO: NUBE · NO en CAJA · MODELO: Opus (spec que después no se corrige hacia atrás). CARRILES: N6 (propuesta/tablero), N8 (estado). Este acto sólo escribe en forense/prereg-caja/.
FIRMA — verbatim: la de N6 + §2 (#6 y #8 aceptadas como REFORMULABLE).
A.8: forense/prereg-caja/ tiene S1–S3 (N3); ls forense/prereg-caja/ | grep -c "S4\|S5" → 0. Insumos en repo: N5 §2.6 (clien1n/clien1na/clien4a/clien4b, LAPOP 2019) y §2.8 (PROT1/PROT2/prot3, VIC1/vicbar4a, AOJ12, CP6/CP9/LAPOP-E8, TAMANO, multi-ola 2004-2023); FD de LAPOP en manifiesto (cuestionarios 2019/2021/2023 registrados); data/inventario-reactivos-descargas-mx-v1_1.tsv (texto de reactivo por variable); precedentes de spec: L9/L11 (LAPOP, ponderador wt/weight1500, celdas por ola).
SPEC — dos specs, un commit cada una, frase de sello y .sha256:
	•	S4 · civico.voto.clientelar_si_observable (reformulada): objeto de N5 §2.6 verbatim; variables con texto de reactivo copiado del inventario (no parafraseado); universo (votantes 2018 encuestados en 2019, país); ponderador (el de la ola, declarado por nombre y con la incertidumbre de N3 sobre el codebook si aplica); dicotomizaciones; celdas: recepción de oferta clientelar × observabilidad percibida × voto declarado; cota de n mínima por celda; qué signo sostiene la regla y qué signo la refuta; se_mueve_si.
	•	S5 · civico.protesta.agravio_urbano (reformulada): ídem, multi-ola (lista cerrada de olas y de la variable de protesta por ola, con su recodificación si cambió), TAMANO como estrato, agravio (VIC1/vicbar4a) × falla estatal (AOJ12) × red previa (CP6/CP9) × urbano; falsador pre-registrado con las dos filas que B-bis exige (qué pasa si no refuta).
Cada spec cierra con la lista de archivos que la caja necesita abrir (id de manifiesto + sha) y con la línea «medición: caja, acto MAESTRA38-L4/L5».
PERÍMETRO. Toca: forense/prereg-caja/S4-*, S5-* + .sha256 · INFRAESTRUCTURA (dos líneas) · tablero (recibo) · A.3 · cascada. NO toca: milpa/** · canon · data/** · tests/**. Si te encuentras escribiendo fuera de esta lista, PARA.
FP/ADR: ADR-339 · FP-300 recibo. CONTADOR: specs selladas 3 → 5 · medición: cero (pre-registro).

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-N7 · PRE-REGISTRO-CIVICO-LAPOP` (4/sep/2026,
entorno NUBE, rama `claude/civico-voto-protesta-specs-qm5ypr`). Dos specs
selladas en `forense/prereg-caja/` (3 → 5), un commit cada una, cada una
con su `.sha256`:

- `S4-L4-spec-v1_0.md` (`658f3c9…`, sellado en un solo commit, sin
  necesidad de re-sello — el `T25` que sí golpeó a `S5` no aplica aquí)
  — `civico.voto.clientelar_si_observable`, objeto verbatim de `N5 §2.6`: LAPOP México
  2019, tratamiento `clien1n`/`clien1na` (exposición a oferta clientelar)
  × desenlace `vb3n` (voto PRI/MORENA 2018), control `vb10`. Universo,
  ponderador (`wt`, verificado constante = 1 por una corrida real de
  `L9`, no por prosa), dicotomizaciones, cuatro celdas, cota de numerador
  `<10`, signo que sostiene/refuta la regla y `se_mueve_si` — los seis
  elementos que el `SPEC` pedía.
- `S5-L5-spec-v1_0.md` (`10aa8de…` inicial → re-sellado a `f68f4b0…`
  por el fix de `T25`, ver «Desviaciones») — `civico.protesta.
  agravio_urbano`, objeto verbatim de `N5 §2.8`: multi-ola **cerrada**
  2004/2006/2019 (2021/2023 excluidas — verificado que ninguna trae
  variable de protesta), `TAMANO` como estrato, agravio × falla estatal
  × red previa × urbano, con la recodificación de `PROT1`/`PROT2`
  (escala de frecuencia, 2004/2006) contra `prot3` (ya binaria, 2019)
  declarada antes de abrir nada. Falsador con las dos filas que `B-bis`
  exige: qué pasa si `C_completo` es estimable y qué pasa si cae por
  guardia de numerador (entonces el veredicto sale de tres celdas
  diagnósticas, declarando que el corazón de la regla no se midió).

**Hallazgo central de este acto, por A.8/D-13 — corrección de premisa que
ni el encargo ni `N5` traían.** `MAESTRA35-L9`/`L11`
(`forense/notas/2026-09-02-MAESTRA35-L9-*`, `-L11-*`, 2/sep/2026, dos
días antes de que `N5` clasificara estas mismas dos reglas como
`REFORMULABLE`) **ya pre-registraron y corrieron** falsaciones reales de
los mismos dos `id` de canon que este encargo pedía "pre-registrar" como
si fueran territorio virgen:

- `civico.voto.clientelar_si_observable` — `L9 §3`/`L11 §1` midieron el
  brazo de **observabilidad percibida** (LAPOP 2023 + réplica ENCUCI
  2020): veredicto **`CONTRARIA`**, dos veces, contra una `[FUERTE]`
  vecina (`R7.3`). `S4` ataca el **otro** brazo de la disyunción del
  `SI` — proximidad/focalización del reparto —, único medible en la ola
  2019, y declara por qué la celda de tres factores que el encargo pedía
  (oferta × observabilidad × voto) **no es construible en una sola ola**:
  ningún payload LAPOP del corpus trae los dos ítems sobre la misma
  persona (`clien1n`/`clien1na` sólo en 2019; `countfair3` sólo en 2023).
- `civico.protesta.agravio_urbano` — `L9 §4`/`L11 §2` midieron dos de
  cuatro antecedentes (agravio × entorno): veredicto
  **`CORROBORADA-PARCIAL`**, dos veces, y `L9` declaró explícitamente que
  "red previa" y "falla estatal" **no estaban en el instrumento** que
  examinó. `S5` completa el diseño de cuatro factores con los dos
  reactivos (`AOJ12`, `CP6`/`CP9`) que `data/inventario-reactivos-
  descargas-mx-v1_1.tsv` —nacido el 3/sep, **un día después** de `L9`—
  sí trae. Corrige además la caracterización de `N5 §2.8` sobre
  `LAPOP-E8`: por su texto verbatim, es un ítem de aprobación normativa
  de que otros participen, no de asistencia propia — familia distinta de
  reactivo que `CP6`/`CP9`, que sí preguntan asistencia en primera
  persona.

Las dos corridas de `L9`/`L11` siguen `PENDIENTE-DE-MESA` en `FP-298`
(`ABIERTA`) — ningún sello de canon se ha movido. `S4`/`S5` no las
repiten ni las reabren: se citan como lo que son, evidencia ya corrida
sobre el mismo `id`, y las dos piezas nuevas se presentan como intentos
de falsación **independientes y complementarios**, no como primera
medición.

**Cascada** (`0695a41` y `2bf39c2`). `data/INFRAESTRUCTURA-v1_0.md` gana
dos líneas bajo `forense/prereg-caja/` (una por spec), cada una
declarando la corrección de premisa contra `L9`/`L11`.
`forense/tablero/TABLERO-PROGRAMA.md`: nota de recibo. `forense/tablero/
TABLERO-PROGRAMA-v1_1.md`: `§8.5` (recibo completo) y `B24` anotado
**parcial** — `#6`/`#8` de la tabla `PENDIENTE-DE-MESA` de `N5` quedan
aceptadas como `REFORMULABLE` por la `FIRMA` de este encargo; los otros
7 ítems (`#1,#2,#3,#4,#5,#7,#9`) siguen sin decidir, sin que este acto
los toque — fuera de su perímetro. `forense/firmas-pendientes.tsv`:
`FP-299` (recibo, no requiere firma).

**Desviaciones D-13, declaradas.** (1) **Numeración re-derivada, no
heredada.** El encargo citaba `ADR-339`/`FP-300`. Comando de la casa
contra el árbol al escribir esta pieza: `grep -oE '^\*\*ADR-[0-9]+'
canon/gobernanza-v1_15.md | ...` → máximo real **`ADR-337`**;
`grep -oE '^FP-[0-9]+' forense/firmas-pendientes.tsv | ...` → máximo
real **`FP-298`**. Números disponibles: `ADR-338` (libre — `N5` lo dejó
sin usar por la misma razón que aplica aquí) y `FP-299` (contiguo). Este
acto usa **`FP-299`** y **ningún `ADR`** — mismo off-by-one que `N5` ya
declaró para su propio par (`FP-297`/`FP-298` citado como `FP-298`/
`FP-299`), y misma razón: el `PERÍMETRO` explícito excluye `canon` sin
la excepción "salvo ADR" que sí traía `N3`. (2) **`T25` — rótulo pelado
`E8`.** Primer sello de `S5` disparó `T25` (D-6/`ADR-128`): la variable
LAPOP `E8` sin prefijo colisiona con el patrón letra-más-dígito
reservado a rótulos de espacio de acto — mismo defecto que `N5` ya tuvo
que corregir para la misma variable. Corregido a `LAPOP-E8`/`lapop-e8`
en las siete apariciones bare del documento, re-sellado. (3) **Main se
movió 2 commits** entre el `SHA` de redacción (`a0e06da4`) y el momento
de escribir esta pieza (`2b9c90e`) — un `[TRAMITE] digesto 2026-09-04`
ajeno al perímetro de este acto. No PARO, declarado en el `Acto` de cada
spec.

**Verificación.** `python3 tests/check.py --baseline`: **LÍNEA BASE
VERDE** (3 FAIL / 171 WARN, sin entradas nuevas frente a
`tests/baseline.json` congelado, tras el fix de `T25`). Ambos `.sha256`
verificados con `sha256sum -c` al sellar. MODELO real de esta sesión:
`claude-sonnet-5` (el encargo pedía Opus — declarado, no escondido, mismo
criterio que `N5`).

**Contador.** Specs selladas 3 → 5, cumplido. Medición: cero, cumplido —
ningún commit de esta pieza abre microdato, corre censo real ni mueve
tier alguno; los dos veredictos `CONTRARIA`/`CORROBORADA-PARCIAL` citados
en §0 de cada spec son de `L9`/`L11`, no de este acto.

PR de este acto, contra `main`.
