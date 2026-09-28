# ENCARGO · ACTO GEN2-TRAMITE-FIRMAS-21-1 · Sucesor declarado de GEN2-TRAMITE-HOJA-FIRMAS-21-1: asienta en `forense/firmas-pendientes.tsv` las firmas que mesa ya dio en chat (28/sep, 22 letras de `HOJA-FIRMAS-21-v2-opciones-2026-09-27.md`) y las que RECIBO-ASTRA6-2 firmó el 27/sep y nunca se asentaron (A.12); añade la recomendación de dirección que `HOJA-FIRMAS-21-1` P2 dejó pendiente (HOLDOUT M09–M23 y reserva de cinco olas); no firma nada nuevo

> ENTORNO: **NUBE** — lee/escribe TSV de gobierno y la hoja de FIRMAS-21. Cero microdato.

CABECERA · SHA de redacción `c0f66833` (base al abrir, re-derivado tras `git fetch`) · una sesión, rama `claude/new-session-ukfyju` (harness) · MODELO: Opus/Sonnet 5 (juicio: recomendaciones y asiento por A.12, no receta) · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0) · ids con raíz de acto (D-24) · D-21 aplica.
CONTADOR: cero mediciones; no adopta nada nuevo; asienta 22 firmas ya dadas (14 del chat de hoy vía ADENDA-1 de HOJA-FIRMAS-21-1, 7 de RECIBO-ASTRA6-2-ADENDA-1 del 27/sep, 1 SUPERADA-cerrada) y añade recomendación de dirección a 6 renglones (R01–R06).

## 1 · OBJETIVO
(P1) Sincronizar `forense/firmas-pendientes.tsv`: para cada FP cuyo `ejecutor` en `decisiones-21.tsv`/`arma_hoja.py` sea `TRAMITE-FIRMAS-21`, marcar `estado=FIRMADA` (o `FIRMADA · EJECUTADA` si ya se ejecutó antes, o `CERRADA -- SUPERADA` si el objeto ya no aplica), con `firmada_en` citando la ADENDA que la firmó, verbatim. Las firmas cuyo `ejecutor` sea otro acto (C2, tubería, curación, ENCIG) **no se tocan** (A.12: «un trámite no la asienta por separado»); siguen `ABIERTA` hasta que ese acto propio las asiente junto con su ejecución.
(P2) Añadir a `arma_hoja.py` (única fuente; `decisiones-21.tsv` y `hoja-para-mesa-firmas-21.md` se regeneran desde ahí) la recomendación de dirección para R01 (HOLDOUT M09–M23) y R02–R06 (reserva de ENCRIGE 2020, ENVE 2024, CSES Módulo 5, ENDUTIH 2025, ENIF 2024 m7), rotulada `PROPUESTO-POR-EJECUTOR (dirección, 28/sep/2026)`, con su razón. Sin firma de mesa todavía: son recomendación, no decisión.
(P3) Regenerar `decisiones-21.tsv` y `hoja-para-mesa-firmas-21.md` con `arma_hoja.py` y verificar `check.py --rapido` VERDE.

«Hecho», por comando: `python3 -c "import csv;print(sum(1 for r in csv.DictReader(open('forense/firmas-pendientes.tsv'),delimiter='\t') if r['estado']=='ABIERTA'))"` → 44 (66 − 22) · las 22 filas tocadas tienen `firmada_en` no vacío y citan su ADENDA · ninguna fila con `ejecutor` ajeno cambió de estado (diff de esas 44 líneas = 0) · `hoja-para-mesa-firmas-21.md` trae recomendación no vacía en R01–R06 (`grep -c "PROPUESTO-POR-EJECUTOR (dirección" ` ≥ 6) · `check.py --rapido` VERDE.

## 2 · FIRMAS DE MESA — dadas
Mesa, 28/sep/2026, este chat, verbatim: «a ver pues pon esta fecha del día de hoy 28 de septiembre, no me estás prompteando los pendientes y no quiero que sigamos enviando PR's con encargos no culminados» → pidió la hoja completa de las 66 FP ABIERTA; se le mostró que ya existía (`GEN2-TRAMITE-HOJA-FIRMAS-21-1`, PR #1267) y pidió «Sí, arma la hoja completa de las 66». Mesa, 28/sep/2026, chat de dirección maestra 54, verbatim: «firmado» sobre las 22 letras de `HOJA-FIRMAS-21-v2-opciones-2026-09-27.md` (ver ADENDA-1 de HOJA-FIRMAS-21-1, ya archivada). Mesa, 27/sep/2026: ADENDA-1 de `2026-09-27-GEN2-RECIBO-ASTRA6-2.md` (7 firmas + 1 cierre por producto). A.12 («toda firma dada se marca FIRMADA con su ADR/PR») y A.17 (bloqueador re-verificado de estado antes de heredarlo: las 22 FP se leyeron `ABIERTA` en el TSV vivo antes de tocarlas).

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `forense/firmas-pendientes.tsv`: 66 filas `estado=ABIERTA` al abrir (re-derivado, no el 56 del encargo de HOJA-FIRMAS-21-1 -- creció por FP nuevas de ASTRA-CONTINUIDAD-C1/C2/C3 del propio 28/sep).
- [LEÍDO] `forense/analisis/hoja-firmas-21/decisiones-21.tsv` y `arma_hoja.py`: 86 renglones (57 `PIDE-FIRMA`, 21 `FIRMADA-EN-CHAT`, 7 `YA-CUBIERTA-POR`, 1 `SUPERADA`); el script ya idempotente contra el TSV vivo (`python3 arma_hoja.py` sin diff antes de este acto).
- [LEÍDO] `forense/encargos/2026-09-28-GEN2-TRAMITE-HOJA-FIRMAS-21-1-ADENDA-1.md`: nombra, letra por letra, qué asienta `TRAMITE-FIRMAS-21` y qué asienta cada acto propio (G1/H1/H2/H5 → tubería; H4 → ENCIG; D2 → curación; E3/E4/B4 → C2).
- [LEÍDO] `arma_hoja.py` líneas 235–254 (`firmada(...)`) y 255–258 (B2/B3 fundidas con `c3fa-05`): mapeo letra → FP exacto, con el campo `ejecutor` explícito en cada llamada.

## 4 · YA HECHO / YA DECIDIDO
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'TRAMITE-FIRMAS-21'` → 0 al abrir. Homónimo `GEN2-TRAMITE-HOJA-FIRMAS-21-1` (PR #1267) produjo la hoja; no asentó (perímetro propio se lo vedaba, §9 de ese encargo).

## 5 · PIEZAS
P1 → P2 → P3.

## 6 · LATITUD
Redacción de la recomendación de dirección (P2): tuya, con razón declarada por renglón. PREGUNTA A MESA: ninguna (las 22 firmas ya están dadas; P2 es recomendación, no pide firma nueva). NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) no aplica · b) tocar una FP cuyo `ejecutor` sea otro acto, o editar un sello · c) firmar por mesa algo que mesa no firmó, o presentar P2 como decisión en vez de recomendación · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«Solo se asienta lo ya firmado, con su cita» protege **adoptar** (A.12) · «Un trámite no asienta lo que le toca a otro acto» protege **borrar** (deuda ajena).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/firmas-pendientes.tsv` (solo las 22 filas nombradas) · `forense/analisis/hoja-firmas-21/` (arma_hoja.py, decisiones-21.tsv, hoja-para-mesa-firmas-21.md) · nota, L0, cascada. Ajeno: las 44 filas ABIERTA restantes de `firmas-pendientes.tsv` · `no-corrido.tsv` · `canon/` salvo cascada · `milpa/`. «Si te encuentras escribiendo fuera de esta lista, PARA.» Archivos que otro acto en vuelo puede tocar: `forense/firmas-pendientes.tsv` (merge=union; ASTRA-CONTINUIDAD-C1/C2/C3 pueden añadir filas nuevas mientras este acto corre — no se editan esas filas nuevas, solo se leen para no chocar).

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No firma nada que mesa no haya firmado ya. No toca las 9 letras de ejecución ajena (B4,D2,E3,E4,G1,H1,H2,H4,H5): sucesores propios (C2, tubería, curación, ENCIG) las asientan al ejecutar. No decide HOLDOUT ni las cinco reservas (P2 es recomendación; la firma de mesa sobre R01–R06 queda `PIDE-FIRMA` en la hoja). El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto.

## NO-CORRIDO / RESERVAS
- Ninguno.

## CONSUMIDO
PR #1273 (mismo branch/PR que GEN2-TRAMITE-INSTRUCCIONES-V217-1-ADENDA-1 -- la rama de esta sesión está fijada por el harness a un solo PR; ver nota en el cuerpo del PR). ADR `ADR-260928-GEN2-TRAMITE-FIRMAS-21-1-ce13-01`.
