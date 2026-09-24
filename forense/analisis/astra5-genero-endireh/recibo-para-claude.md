# Recibo de Claude · unidad ASTRA5-U2-GENERO-ENDIREH (#1093 + sucesor #1099)

24/sep/2026 · `ACTO GEN2-ASTRA5-U2-ENDIREH-CIERRE-1` (`ADR-260924-GEN2-ASTRA5-U2-ENDIREH-CIERRE-1-b0df-01`) · base `c12a0d87` · NUBE, cero microdato. Formato de `RECIBO-ASTRA-PRODUCTO-N` (los seis criterios de `forense/encargos/2026-09-23-GEN2-AUDITORIA-POST-HOC-ASTRA-1.md:9`). Contadores movidos por este recibo: **cero** (no mide, no adopta).

Este recibo sustituye, para la mesa, al documento de trabajo de Codex (`forense/analisis/dominios/genero/recibo-astra5-u2-endireh-codex-para-claude.md`), que se declaraba borrador. No edita ningún archivo de Astra.

## Inventario (P1) — por comando

```
ls -d data/corrida0/CALC-ENDIREH-*            → 20 carpetas
[ -f <calc>/sello.json ]                        → 16 selladas, 4 sin sello
grep cuenta_gen2 <calc>/spec.yaml (selladas)    → 16/16 «cuenta_gen2: SI»
csv.DictReader(forense/replay-evidencia.tsv)    → 16 filas calc_id CALC-ENDIREH-*, todas REPRODUCE/IDENTICO
git diff --name-only 8721d658^1 8721d658        → 10 selladas vienen de #1093; 6 de #1099 (56ca4377)
```

| CALC | PR | sello.sha256 (16 hex) | cuenta_gen2 | filas replay |
|---|---|---|---|---|
| `CALC-ENDIREH-PISOS-2006-MODULOS-0002` | #1099 | `da9275d6d70d65c8` | SI | 1 |
| `CALC-ENDIREH-PISOS-2011-MODULOS-0001` | #1099 | `13006f7d900f0c25` | SI | 1 |
| `CALC-ENDIREH-PISOS-2016-DISCRIMINACION-0001` | #1099 | `9ec9a2b95e06b849` | SI | 1 |
| `CALC-ENDIREH-PISOS-2016-PAREJA-FISICA-0002` | #1093 | `a00f379236a429c7` | SI | 1 |
| `CALC-ENDIREH-PISOS-2016-RESTANTES-0001` | #1099 | `9c2fc7830ec71915` | SI | 1 |
| `CALC-ENDIREH-PISOS-2021-AYUDA-0001` | #1093 | `38c2c5b3aece6eda` | SI | 1 |
| `CALC-ENDIREH-PISOS-2021-COMUNITARIA-0001` | #1093 | `5c7a47a33a1b7174` | SI | 1 |
| `CALC-ENDIREH-PISOS-2021-DECISIONES-0001` | #1093 | `7b33e62307842dc2` | SI | 1 |
| `CALC-ENDIREH-PISOS-2021-DISCRIMINACION-0001` | #1099 | `8f3cfe19b28dcbd8` | SI | 1 |
| `CALC-ENDIREH-PISOS-2021-ESCOLAR-0001` | #1093 | `34e66f6b6cc8ed6a` | SI | 1 |
| `CALC-ENDIREH-PISOS-2021-FAMILIAR-0001` | #1093 | `5a463f9a679de60a` | SI | 1 |
| `CALC-ENDIREH-PISOS-2021-LABORAL-0001` | #1093 | `34f57f6e532cf4fb` | SI | 1 |
| `CALC-ENDIREH-PISOS-2021-NOFISICA-BC-0001` | #1099 | `5e2268514a33702f` | SI | 1 |
| `CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0003` | #1093 | `ba6c9fbf1872feae` | SI | 1 |
| `CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-0004` | #1093 | `4de09138c1316c4d` | SI | 1 |
| `CALC-ENDIREH-PISOS-2021-PAREJA-FISICA-BC-0001` | #1093 | `36ccd2d347323ec0` | SI | 1 |

Sin sello (no se tocan; sellos de Astra intactos): `2016-PAREJA-FISICA-0001` (NO-EJECUTABLE, llave `ID_PER`), `2021-PAREJA-FISICA-0001` (NO-EJECUTABLE, UnicodeDecodeError), `2021-PAREJA-FISICA-0002` (`run` rechazó tipo `list`) — los tres declarados por Codex en las notas de #1093; `2006-MODULOS-0001` (#1099) **sin declaración en ningún archivo** fuera de su carpeta (`grep -rl 2006-MODULOS-0001 --include=*.md --include=*.tsv . | grep -v corrida0` → 0 archivos) → `NC-260924-GEN2-ASTRA5-U2-ENDIREH-CIERRE-1-b0df-01`.

## Los seis criterios

1. **Cifras sin RESULT.** `python3 tools/recibo/cifras_sin_result.py 8721d658` → `archivos_con_cifras_nuevas=21 archivos_sin_result=2`; sobre `56ca4377` → `13 / 4`. Los seis SIN-TRAZA son el dictamen documental 2003, el ADR raíz propuesto, el FP/NC y los dos recibos de Codex: numerales de pregunta (7.3, 8.3), conteos de réplicas/registros y el 70.1% de U0, que los propios textos rotulan «sin contraste directo». Ninguno está en `canon/` (`git diff --stat` de ambos merges sobre `canon/` → 0 líneas). **CUMPLE, con la reserva de que el 70.1% no es cifra ENDIREH medida.**
2. **Adendas.** La unidad no tuvo encargo de dirección con adendas; sin adendas que citar. **NO-APLICA.**
3. **Etiquetas y sellos.** 16/16 sellados con `cuenta_gen2: SI` y `generacion: GEN2`; 16/16 con asiento de replay REPRODUCE/IDENTICO; ninguno falta, por eso este acto no asienta filas nuevas en `replay-evidencia.tsv`. Un CALC sin sello sin declarar (`NC-260924-GEN2-ASTRA5-U2-ENDIREH-CIERRE-1-b0df-01`). **CUMPLE CON NC.**
4. **Perímetro.** Ningún merge tocó `milpa/`, `decisiones.tsv` ni `tramite` (`git diff --stat … | grep -E "milpa/|decisiones.tsv|tramite|canon/"` → vacío en los dos). #1093 editó `.github/workflows/verify.yml` (sincronía de CI, ya auditado en `…39d2`). Faltaba la cascada: ADR, L0 y registro-rótulos → los produce este acto. **CUMPLE tras este acto.**
5. **México §3.** Pisos descriptivos RETROSPECTIVOS por cuestionario, ámbito y ventana; no suma prevalencias entre ámbitos; separa discriminación por embarazo de violencia interpersonal; 2003 fuera por falta de diseño ligable; «no se atribuye violencia a una persona ni cultura» (recibo Codex). Unidad: mujer (persona). Ninguna frase mezcla PROSPECTIVA y RETROSPECTIVA: todo es RETROSPECTIVA. **CUMPLE.**
6. **Recomendación.** Adopción descriptiva retrospectiva: ya firmada por mesa en T (`…6a2c-01..05`) y la ejecuta `GEN2-ADOPCION-BLOQUE-Y-PINES-2`; aquí solo se cita. Sin REVERTIR. **CONFORME.**
