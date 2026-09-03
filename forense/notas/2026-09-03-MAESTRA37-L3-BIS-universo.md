# ACTO MAESTRA37-L3-BIS · SALUD-A4-SOBRE-v2 — P0, universo congelado (COMMIT-1)

**3/sep/2026.** Encargo archivado por A.3 en
`forense/encargos/2026-09-03-MAESTRA37-L3-BIS-SALUD-A4-SOBRE-V2.md`
(SHA de redacción `27647ac4`). Base del acto: `27647ac` (merge PR #518,
MAESTRA37-A1), que es exactamente el SHA que el encargo declara.

**El primer resultado que produzca este procedimiento es el que se reporta.**
Este commit se escribe ANTES de mirar un solo reactivo con intención de
veredicto. El universo de abajo es lista cerrada: se lee TODO lo que
contiene. Es censo, no búsqueda — no se eligen términos, no se corre
`/mapea`, no hay formulaciones.

## Universo, en una línea (A.13)

> **8 636 filas** del inventario `data/inventario-reactivos-descargas-mx-v1_1.tsv`
> con `payload_id` bajo `ENSANUT2024-v2026-09-01/` (76 payloads con filas, 38 con
> `texto_reactivo` no vacío) · **19 598 filas** de los **38** `*.Catálogo.xlsx` de
> esa subcarpeta (`data/l3bis-ensanut2024v2-catalogos-v1_0.tsv`) · **11** de los
> **16** PDF de cuestionario de esa subcarpeta transcritos con `pdftotext -layout`
> (`data/l3bis-ensanut2024v2-cuestionarios-v1_0.txt`; los otros 5 son byte-idénticos
> a payloads de julio ya transcritos por L3).

Comandos que lo producen, todos sobre esta caja y este commit:

```
# (a) filas del inventario v1_1 bajo la subcarpeta
awk -F'\t' '!/^#/ && NR>1 && $1 ~ /^ENSANUT2024-v2026-09-01\//' \
    data/inventario-reactivos-descargas-mx-v1_1.tsv | wc -l      -> 8636
# (b) catalogos
ls "$DESCARGAS_MX/ENSANUT2024-v2026-09-01/"*.Catálogo.xlsx | wc -l -> 38
wc -l data/l3bis-ensanut2024v2-catalogos-v1_0.tsv                  -> 19643 (19598 datos + 45 cabecera)
# (c) cuestionarios
ls "$DESCARGAS_MX/ENSANUT2024-v2026-09-01/"*.pdf | wc -l           -> 16
```

`$DESCARGAS_MX` = `/mnt/c/Users/PC0/Descargas MX`, de `data/raices.local.yaml`
(gitignorada; raíz declarada en el manifiesto como `descargas_mx`).

## (a) Inventario v1_1 — los 38 payloads con texto

`v1_1` tiene **42 536 filas de dato** y 208 `payload_id` distintos; **8 636**
filas caen bajo la subcarpeta v2. El `payload_id` es la ruta relativa a la
raíz, **no** lleva el sufijo `__v2026_09_01` (ese sufijo vive en el `id` del
manifiesto, no en el inventario): filtrar por el sufijo sobre el inventario da
**0** y sería un falso negativo. Los que traen texto son los 38 `INSPECT_STATA`;
los `INSPECT_ZIP` (CSV) dan 0 filas con texto — es DE2 conocido y aquí no se
repara.

Los seis mayores, que son los que cargan el juicio de este acto:

| payload (subcarpeta v2) | filas | con texto |
|---|---|---|
| `adultos_ensanut2024_w.stata.stata.zip` | 841 | **841** |
| `menores_ensanut2024_w.stata.stata.zip` | 482 | 482 |
| `adolescentes_ensanut2024_w.stata.stata.zip` | 477 | 477 |
| `integrantes_ensanut2024_w_icb.stata.stata.zip` | 258 | 258 |
| `hogar_ensanut2024_w_icb.stata.stata.zip` | 203 | 203 |
| `etiquetado_ensanut2924_w.stata.stata.zip` | 140 | **140** |
| `utilizadores_ensanut2024_w.stata.stata.zip` | 120 | 120 |

El encargo dice «adultos_ensanut2024_w.stata 1 682 filas con texto». **El real
es 841.** 1 682 = 841 × 2, y 841 es también el conteo de `adultos` en el CSV
(851 filas, 0 con texto) más el STATA: la cifra del encargo suma dos veces el
mismo módulo. Se corrige aquí y no se hereda.

## (b) Catálogos v2 — 38 archivos, 19 598 filas

`etiquetado_ensanut2924_w` (así, con el typo `2924` del portal): 141 variables,
578 filas de valor. `adultos_ensanut2024_w`: 842 variables, 3 333 filas de valor.
El listado completo por módulo está en la cabecera del TSV.

`actividad_fisica_…-adultos` y `…-niños` traen **el mismo conteo** (127/631):
son dos archivos distintos con estructura de catálogo gemela, no un duplicado
—sus sha256 difieren (`108aaee45530` vs `bfd8ab3de190`)—.

## (c) Cuestionarios v2 — 16 PDF, 11 transcritos

**5 son byte-idénticos a payloads ya registrados antes de v2** y su texto ya
está en `data/l3-ensanut2024-cuestionarios-v1_0.txt` (L3, julio); no se
reproducen:

| PDF en la subcarpeta v2 | sha256\[:12] | entrada previa del manifiesto |
|---|---|---|
| `hogar_ensanut_2024_etiquetas.Cuestionarios.pdf` | `adc873843b79` | `1_vfinal_cuestionario_hogar_…` |
| `menores_ensanut2024_w.Cuestionarios.pdf` | `af65f922094c` | `2_vfinal_cuestionario_nios_0_a_9_…` |
| `adolescentes_ensanut2024_w.Cuestionarios.pdf` | `344f32ef0f87` | `3_vfinal_cuestionario_adolescentes_…` |
| `adultos_ensanut2024_w.Cuestionarios.pdf` | `0bc30c3b7f08` | `4_vfinal_cuestionario_adultos_…` |
| `utilizadores_ensanut2024_w.Cuestionarios.pdf` | `004aacee3729` | `5_vfinal_cuestionario_utilizadores_…` |

Concuerda con lo que A1 midió, con una precisión: A1 dice «6 idénticos», y son
**5 PDF + 1 `.docx`** (`indice_bienestar.Cuestionarios.docx` `6913725196ae` =
`indice_de_bienestar_cuestionarios`). Aquí sólo cuentan los PDF, de ahí el 5.

Los 11 transcritos incluyen los tres que L3 no pudo tener: `adultos` (45 pág.),
`etiquetado_ensanut2924_w` (14 pág.) y `actividad_fisica_…-adultos` (7 pág.).

**Nota de honestidad sobre este mismo censo (A.13).** La primera corrida de (c)
declaró «0 idénticos, 16 nuevos». Era falso: el parser suponía que
`fecha_descarga` precede a `sha256` dentro de la entrada del manifiesto, y el
orden real es el inverso, así que el conjunto de comparación salió vacío. Un
negativo producido por un comando que no comparó contra nada no es un negativo.
Se rehízo con un parser por entrada completa y control positivo (1 103 entradas
pre-v2 con sha, 125 entradas v2 con sha, suma 1 228 = total de `sha256:` del
manifiesto). El archivo comiteado es el de la segunda corrida.

## Regla de honestidad heredada de L3, vigente en este acto

- Etiqueta de Stata truncada a 80 caracteres → se completa con el PDF del
  cuestionario antes de fallar.
- Nombre de variable sin etiqueta y sin catálogo → **CANDIDATO-ABRIR-EN-CAJA**,
  no veredicto.
- Un desenlace que sólo se aproxima (no se mide) → **EXISTE-NO-SATISFACE** con
  lo que falta escrito, nunca SATISFACE.

## Criterio congelado

D8 (FP-268, 3/sep) se mantiene: el criterio 2 no se toca. Este acto lo evalúa.
El techo de L3 —«una sola descarga lleva salud de 1 a 2, no a 3»— queda
**VENCIDO EN ALCANCE** (A.10): fue medido sobre cinco módulos de julio y el
universo creció por debajo del sello. No se refuta, no se borra, no se edita
ninguna línea de la nota de L3; se re-sella contra el universo de arriba.
