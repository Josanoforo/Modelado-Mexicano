# `CALC-R-CIV-M-04` — cara mecánica

Gobierna esta corrida la spec SELLADA `forense/prereg-caja/R-ENVIPE-SERIE-DBF-spec-v1_0.md`
(**`prereg-caja-R-ENVIPE-SERIE-DBF`**, `sha256 26457cc03fc447ddd2a2f5c77210207fea08653d750be75d4ec152361f2eb991`),
sucesora por extensión de `prereg-caja-R-ENVIPE-SERIE` (`sha256 b9a29cf656b9fcfe2794eaa4e2b3de0a9df699d72af1d143e0059c64b051dba4`),
que **no se edita**. Este archivo no las sustituye: las resume en la forma que `spec.yaml` cablea.
Donde digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-R-SERIE-DBF`, 9/sep/2026, CAJA (Ubuntu) con corpus montado, sobre `4497029`.
**Celda:** `CIV-M-04` — ENVIPE 2015, **delitos de 2014**.
**Releva:** `CORR-0032` → `RES-0103`, el árbitro `R` de esta celda del marco `M`.
Consumidor natural: `forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv:CIV-M-04:R`.
**La adopción NO es de este acto**: la decide mesa por lote (`F3`).

**CONGELADO en el COMMIT-1, antes de abrir un solo registro de `TMod_Vic.dbf`.**

---

## Qué mide

**Dos estimandos sobre la misma lectura del mismo archivo:**

1. **PRIMARIO — el árbitro `R`.** Proporción ponderada de delitos con razón principal de
   no-denuncia en `{01, 02, 06}`, sobre **todos** los delitos con `BP1_23 ∈ {01…09}`,
   ponderador `FAC_DEL`, diseño `EST_DIS`/`UPM_DIS`. Codificación, universo, ponderador y
   diseño **verbatim** de `codificacion-R-v1_0.tsv`; variable y escala, de `espec-R-ciega-v1_2.tsv`.
2. **SECUNDARIO HOMOLOGADO — el punto de serie.** Mismo desenlace bajo `U1` y `C1` de
   `prereg-caja-ENVIPE-DENUNCIA`: delitos **personales** (`BPCOD ∈ {05,…,15}` **en esta ola**),
   `BP1_20 = 2`, denominador `{01…08}`. Se emite también `C2` (partición GEN1) y el delta.

**`U_R` y `U1` no se comparan entre sí** (`A-bis.4`).

## Identidad del insumo

| campo | valor |
|---|---|
| `id` de manifiesto | **`envipe_2015_bd_envipe2015_dbf`** |
| miembro del ZIP | `TMod_Vic.dbf` — literal, nunca por plantilla |
| filas (cabecera DBF) | 44,699 |
| descriptor citado | `fd_envipe2015.pdf` — `BP1_23` pagina 57 (1-based), `BPCOD` pagina 51 (1-based), diseño paginas 50 (EST_DIS, UPM_DIS) y 64 (FAC_DEL) |

## Vínculo de columnas (rol → nombre físico en ESTA ola)

| rol | nombre físico | tipo en la cabecera del `.dbf` |
|---|---|---|
| `BP1_23` | `BP1_23` | Caracter(2) |
| `BP1_20` | `BP1_20` | Caracter(1) |
| `BPCOD` | `BPCOD` | Caracter(2) |
| `FAC_DEL` | `FAC_DEL` | Numerico(12) |
| `ESTRATO` | **`EST_DIS`** | Caracter(3) |
| `UPM` | **`UPM_DIS`** | Caracter(5) |

El medidor no conoce ninguno de estos nombres por su cuenta: los recibe en
`parametros.mapa_columnas`. La guardia de columna ausente de la familia **no se edita**.

## Lo que NO hace

No mide `U4` (unidad persona): la familia no lo define — guardia de `tper_vic2` **`NO-APLICA`**
(spec sellada §5). No usa `FAC_DEL_AM`. No adopta, no mueve `tier`, no toca `milpa/`.
No abre `tools/arbitra.py` ni `corridas-R/CIV-M-04.json`: el control positivo es script
aparte, **después de sellar**.
