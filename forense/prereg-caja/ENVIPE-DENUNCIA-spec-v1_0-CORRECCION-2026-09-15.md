# Corrección de cita · `ENVIPE-DENUNCIA-spec-v1_0` · CORR-0009 → CORR-0007

**Fecha:** 15 de septiembre de 2026 · **Acto:** `ACTO GEN2-SANEA-REGISTRO-Y-RESCATE` (NC-0130)

Sucesión fechada, no edición. `forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0.md` queda
**intacto** como historia sellada — este archivo únicamente asienta la corrección,
citado desde su lugar, sin tocar el sellado.

## Qué está mal

`ENVIPE-DENUNCIA-spec-v1_0.md` cita `CORR-0009` en tres lugares (línea 9,
línea 10 y línea 292) al referirse a la corrida `RES-0027`/`RES-0028` y a
los cuatro `RESULT` restantes `RES-0039..0042` (denuncia condicional a
seguro, `BPCOD=01`). La demanda vigente (`data/corrida0/demanda-corridas.tsv`)
dice otra cosa:

```
$ grep -n "CORR-0007\|CORR-0009" data/corrida0/demanda-corridas.tsv
CORR-0007	ENVIPE2025	envipe2025_csv	...	RES-0025;RES-0026;RES-0027;RES-0028;RES-0039;RES-0040;RES-0041;RES-0042	...
CORR-0009	ENIF2024	enif_2024_enif_2024_bd_csv	...	RES-0031;RES-0032;RES-0046;RES-0048;RES-0057;RES-0058;RES-0059;RES-0060;RES-0065	...
```

`CORR-0007` es ENVIPE2025 y cubre exactamente `RES-0025..0028` y
`RES-0039..0042` — los mismos `RESULT` que la spec cita bajo `CORR-0009`.
`CORR-0009` es **ENIF2024**, otra fuente por completo, y no tiene relación
con `RES-0027`/`RES-0028`/`RES-0039..0042`.

## Corrección

Donde `ENVIPE-DENUNCIA-spec-v1_0.md` dice `CORR-0009`, la cita correcta —
verificada contra la demanda vigente citada arriba — es `CORR-0007`. Esto
aplica a las tres menciones (línea 9: relevo de la demanda para
`RES-0027`/`RES-0028`; línea 10: los cuatro `RESULT` restantes;
línea 292: `RES-0039..0042` en `## NO-CORRIDO`).

Ningún `RESULT`, estimando, universo, codificación o veredicto de la spec
cambia. Es una referencia cruzada corregida, no una re-medición.

## Qué no hace esta sucesión

No edita `ENVIPE-DENUNCIA-spec-v1_0.md`. No abre `CALC-ENVIPE-0001` de
nuevo. No adopta ni cierra `RES-0039..0042`, que siguen en `## NO-CORRIDO`
de la spec sellada, sólo bajo el `CORR` correcto.

## Cierre

Cierra `NC-0130`.
