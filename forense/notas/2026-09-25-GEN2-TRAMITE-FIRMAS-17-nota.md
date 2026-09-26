# Nota · ACTO GEN2-TRAMITE-FIRMAS-17

ADR-260925-GEN2-TRAMITE-FIRMAS-17-ad95-01 · 0-bis `ad9570bb` · base `40058c09` (= SHA de redacción) · ENTORNO NUBE (hook: ENTORNO-DERIVADO = NUBE) · rama `claude/new-session-cm7sz5`.
Contadores movidos: cero.

## Premisas (§3)
- `[EJECUTADO]` 8 FP ABIERTA — `python3 tools/cierre_acto.py` → «Filas ABIERTA (8)». Sostiene.
- `celdas_validadas` 219 — misma salida: 219 → 219 (Δ0). Sostiene.
- §4: `grep -c 'FIRMAS-17' forense/firmas-pendientes.tsv` → 0 (antes de este acto). Ningún trámite previo.

## Sin firma
§2 del encargo no trae texto de mesa. Precedente FIRMAS-15: las filas quedan ABIERTA con DECISIÓN-DE-MESA-PENDIENTE. Marcar FIRMADA o asentar H4 sin firma sería adoptar a mano (PARO c). Los textos de firma vigentes son los de §1 H1–H4 del encargo; las cuatro FP llevan ahora en `dónde` el puntero a esa hoja. Mesa: contestar «firmo» (o corregir por letra) y el trámite siguiente las asienta.

## H4 preparada (PROPUESTO-POR-EJECUTOR, no asentada)
Derivado con `git log --first-parent origin/main --diff-filter=A -- data/corrida0/<CALC>/`:

| CALC | merge a main | PR |
|---|---|---|
| CALC-ENIF-0001 | 18758c07 (2026-09-23) | #1091 |
| CALC-R-DIN-M-01-v4 | 18758c07 (2026-09-23) | #1091 |
| CALC-ENCIG-0001-COMPLEMENTOS-DERIVADO-0001 | d8369190 (2026-09-24) | #1128 |
| CALC-ENCUCI-0001-COMPLEMENTO-DERIVADO-0001 | d8369190 (2026-09-24) | #1128 |

`grep -c "^<CALC>\t" data/corrida0/decisiones.tsv` → 0 para los cuatro. Fila lista: `<CALC>\tcuenta_gen2=SI · adopción por merge de mesa del PR #<n> (E.2, vía etiqueta hecha explícita)\tFIRMA DE MESA <fecha>, hoja FIRMAS-17 H4, verbatim: «…»\t<fecha>`.

## F
`.claude/commands/acto.md` paso 11: el encabezado `## CONSUMIDO` va con esas palabras aunque el ADR o la nota hagan de cierre.
