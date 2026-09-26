# Nota · GEN2-TRAMITE-FIRMAS-18 · ADR-260926-GEN2-TRAMITE-FIRMAS-18-6cf3-01

Cero mediciones (CONTADOR del encargo: H4 hace explícitas cuatro adopciones que `status` ya contaba por etiqueta; ningún contador cambia).

## Arranque
NUBE (`ENTORNO-DERIVADO = NUBE`, corpus montado=NO, archivos_examinados=0; red DENEGADA-POR-POLITICA) — coincide con el encargo. SHA de redacción `4f3713cb`; base `ac3cb4d1` (main se movió: #1150 FIRMAS-17 y #1151 MAPA v1.1 fusionados; no es PARO). 0-bis `6cf3b2bd`. `grep -c 'FIRMAS-18' forense/firmas-pendientes.tsv` → 0 al abrir.

## P1 · firmas
e760-01/02/03 y afe1-01 → FIRMADA, texto verbatim de §2 del encargo (mesa no corrigió ninguna letra), con `EJECUTA:` (H1–H3: GEN2-RELEVO-CONSUMIDORES-3; H4: este trámite).

## P2 · H4 — premisa corregida (logística, D-19 fuera de lista)
La nota de FIRMAS-17 atribuía CALC-ENIF-0001 y CALC-R-DIN-M-01-v4 a PR #1091. Re-derivado con `git log --first-parent origin/main --diff-filter=A -- data/corrida0/<CALC>/`: los añade a main el merge `8721d658` (**PR #1093**). El merge de #1091 (`18758c07`) no es ancestro de origin/main y el PR #1091 cambió un solo archivo documental. La firma dice «citando el PR de fusión», no un número: se cita #1093. Los dos derivados ENCIG/ENCUCI: `d8369190`, PR #1128 (confirmado).

| CALC | merge | PR |
|---|---|---|
| CALC-ENIF-0001 | 8721d658 | #1093 |
| CALC-R-DIN-M-01-v4 | 8721d658 | #1093 |
| CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001 | d8369190 | #1128 |
| CALC-ENCUCI-0001-COMPLEMENTO-DERIVADO-0001 | d8369190 | #1128 |

## P3 · NC
NC-260925-GEN2-TRAMITE-FIRMAS-17-ad95-01..04 → CERRADA con `DECISIÓN-DADA`. Las NC e760-* de RELEVO-CONSUMIDORES-2 siguen ABIERTA: su sucesor es RELEVO-CONSUMIDORES-3.

## Derivado regenerado (latitud: regenerar por comando, D-21)
CI `guardias` falló en `tests/test_catalogo_v1_1.py::test_regenera_identico`: el catálogo v1.1 se deriva de `decisiones.tsv` y las 4 filas H4 lo cambian. Regenerado con `python3 forense/analisis/catalogo/genera_catalogo_v1_1.py --sin-registro` (fuera de la lista §9, pero es el derivado que H4 mueve; nada se teclea): `pendientes-de-firma.tsv` pierde las filas SIN-FP-CITABLE, `calcs` 65→68, `alcance:PARAMETRO-DE-REGLA` 48→61. No es medición.
