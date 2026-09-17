# `ACTO GEN2-CORTE-EDAD-1` · P1 — el corte de `edad`, por definición, sobre tres FD

**Acto:** `ACTO GEN2-CORTE-EDAD-1` (`ADR-533`) · **encargo:** `forense/encargos/2026-09-16-GEN2-CORTE-EDAD-1.md`
**Base:** `e4f5f77` (= `origin/main` HEAD al abrir; `git rev-list --count HEAD..origin/main` = 0).
**Entorno:** NUBE. `python3 tools/entorno.py --sonda-red` → `acceso_corpus.montado=NO`,
`archivos_examinados=0`, `raices=data_raw:NO`, `red=000`. **No se abrió un solo microdato
en este acto.** Censo de raíz vigente citado por A.8/`ADR-326`:
`forense/censo-raiz/2026-09-15-cron-1047.txt` — «Total en disco: 524 · nuevos: 62 ·
ya registrados: 462».

**Firma que autoriza (D4, mesa, 16/sep/2026, verbatim en el encargo §FIRMA DE MESA):**
adopta los cuatro tramos del árbitro — `18-29 / 30-44 / 45-59 / 60+` — sobre edad en
años cumplidos, y declara el objeto **distinto de `FP-53`**.

---

## 1 · La función del árbitro, leída aquí, línea por línea

`tools/ejes_maestra35_l1.py:54-61` (leído en este clon, no heredado):

```python
def tramos_edad(serie):
    e = pd.to_numeric(serie, errors="coerce")
    out = pd.Series(FUERA, index=serie.index, dtype=object)
    out[(e >= 18) & (e <= 29)] = "18-29"
    out[(e >= 30) & (e <= 44)] = "30-44"
    out[(e >= 45) & (e <= 59)] = "45-59"
    out[(e >= 60) & (e <= 96)] = "60+"
    return out
```

`FUERA = "(fuera)"` (`:35`). `ORD_EDAD = ["18-29", "30-44", "45-59", "60+"]` (`:49`).

**HALLAZGO 1.a — `60+` no es «60 y más»: es `60-96`.** La cuarta rama está acotada
por arriba en **96**. Todo valor `≥ 97` cae a `(fuera)`, igual que un blanco. La
spec que congeló la definición lo dice y es la lectura que sostiene el tope —
`forense/notas/2026-09-02-MAESTRA35-L1-spec.md` §1.3, verbatim:

> `18-29` · `30-44` · `45-59` · `60+` (60 a 96 años cumplidos). Fuera: códigos de
> no especificada (`97`/`98`/`99` según la encuesta) y blanco.

Es decir: el tope de 96 **es** el mecanismo que implementa la no-respuesta, no un
descuido. Pero el **rótulo** `60+` y su **operación** `60-96` no son la misma cosa, y
el dato sellado en `CORTES_C1` guarda el rótulo. Queda escrito en el comentario del
sello (P2) y en la fila del crosswalk (P3) para que ningún consumidor futuro lea
`60+` como «60 y más» sin ver el tope.

**Consecuencia de alcance:** la equivalencia que este acto verifica es *entre los tres
instrumentos y la función*, y es la misma función para los tres. El tope de 96 **no**
diferencia a un instrumento de otro; diferencia al **rótulo** de su **operación**.

---

## 2 · Instrumento por instrumento — por archivo, no por nombre (A.15c)

### 2.1 ENIF 2024 — la única con FD legible desde la nube

| campo | valor | de dónde (archivo:variable) |
|---|---|---|
| variable que usa el árbitro | `EDAD_V` | `data/crosswalk-ejes-arbitro-modelo-v1_0.tsv` fila `edad` |
| tabla | `TMODULO` | `data/inventario-fd-v1_1.tsv` |
| texto del FD | «Edad verificada de la persona elegida» | `enif_2024_fd.xlsx` (`sha256_12 17e2ad86ce9e`) |
| variable hermana, nivel persona | `TSDEM.EDAD` — «**2.5 ¿Cuántos años cumplidos tiene (NOMBRE)?**» | mismo FD, misma sha |
| unidad | **años cumplidos**, *verbatim en el FD* para `TSDEM.EDAD` | ídem |
| rango observado | `18-98`, **cero menores de 18** | `forense/notas/2026-09-02-MAESTRA35-L1-P0-censo.md` §4.4 |
| `tramos_edad` aplicada | 18-29 2 924 · 30-44 4 256 · 45-59 3 411 · 60+ 2 896 · **(fuera 15)** | ídem — cobertura **99.8889 %** |

**Veredicto: `EQUIVALENTE`.** Misma variable en años cumplidos, mismos cuatro cortes,
mismo arranque en 18. **Reserva de alcance, escrita:** la unidad «años cumplidos» está
certificada por el FD para `TSDEM.EDAD`; para `EDAD_V` el FD dice «Edad verificada»,
sin nombrar la unidad, y la unidad se sostiene en el rango entero `18-98` medido en
caja, no en una lectura de la etiqueta. El **catálogo de códigos** de `EDAD_V` no está
en el repo (ver §3).

### 2.2 ENCIG 2025

| campo | valor | de dónde |
|---|---|---|
| variable | `EDAD` | crosswalk fila `edad` |
| tabla de persona | `encig2025_02_residentes_sec_2` | `forense/notas/2026-09-02-MAESTRA35-L1-P0-censo.md` §2 |
| payload | `encig25_base_datos_csv.zip` (`sha256_12 47daf2f73236`) / `.dbf` (`fa92a6ea4119`) | `data/inventario-reactivos-v1_2.tsv` |
| texto del FD | **VACÍO en el inventario** | ídem — `texto_reactivo` en blanco |
| universo del instrumento | «18 años y más», 82 áreas urbanas de 100 mil hab. o más, ref. 2025 | `forense/notas/2026-09-09-GEN2-LOTE-ENCIG-1-cierre.md:35` |
| `tramos_edad`, universo `P1` | 18-29 4 177 · 30-44 8 697 · 45-59 4 767 · 60+ 1 839 · (fuera 61) — **99.6878 %** | P0 censo §4.2 |
| `tramos_edad`, universo `P3` | 18-29 2 806 · 30-44 7 008 · 45-59 5 799 · 60+ 4 475 · (fuera 115) — **99.4308 %** | P0 censo §4.3 |

**Veredicto: `EQUIVALENTE`**, con la **evidencia REGISTRADA, no abierta aquí** (idioma
de `FP-376`/`NC-0270`, mismo patrón). ENCIG 2025 **no tiene una sola fila** en
`data/inventario-fd-v1_1.tsv` — verificado: el inventario FD cubre 30 payloads y
`encig2025` no es uno de ellos. La unidad «años cumplidos» se apoya en el censo `P0`,
que la leyó en caja, y en el universo declarado de 18 y más.

### 2.3 ENVIPE 2025 — la base que `CORTES_C1` corta

| campo | valor | de dónde |
|---|---|---|
| variable, **nivel persona** | `TSDem.EDAD` | `data/inventario-reactivos-v1_2.tsv` |
| payloads | `envipe2025/bd_envipe_2025_csv.zip` (`ecb39b8624b7`) · `.dbf` (`e83c22c5d08b`) · `envipe2025_csv.zip` (`8a7a99fd90ce`) | ídem |
| tabla de persona | `TSDem` — 300 654 personas, `ID_PER` llave única | P0 censo §3 |
| catálogo de la variable | `tsdem_envipe2025/catalogos/edad.csv` (columnas `EDAD`, `descrip`) | `data/inventario-reactivos-v1_2.tsv` — **existe en el corpus, NO en el repo** |
| texto del FD | **VACÍO en el inventario** | ídem |
| `tramos_edad` (medida sobre `tmod_vic.EDAD`, unidad delito) | 18-29 11 871 · 30-44 15 214 · 45-59 8 620 · 60+ 4 481 · (fuera 94) — **99.7666 %** | P0 censo §4.5 |

**Veredicto: `EQUIVALENTE`**, con **evidencia REGISTRADA** y **dos reservas escritas**:

1. La medición de cobertura que existe se corrió sobre `tmod_vic.EDAD` (unidad
   **delito**, universo `P4`), no sobre `TSDem.EDAD` (unidad **persona**). El P0 censo
   §3 verifica que `sexo` y `edad` viven nativamente en `tmod_vic` y que hay
   **0 huérfanos de 22 295** contra `tsdem`, así que las dos columnas son la misma
   edad de la misma persona; pero la cifra de cobertura publicada **es la de la unidad
   delito**, y no se re-etiqueta como si fuera de persona.
2. El catálogo `catalogos/edad.csv` —el archivo que dice qué códigos son
   no-respuesta— **está en `data/raw` y no en el repo**.

---

## 3 · Lo que este entorno NO puede certificar — `NO-ACCESIBLE-AQUÍ`, no adivinado

La cabecera del encargo lo fija: «si un FD necesario solo está en `data/raw`, esa pieza
se declara `NO-ACCESIBLE-AQUÍ` y se rutea a caja, no se adivina».

`EQUIVALENTE` se define en el propio encargo como «misma variable en años cumplidos,
mismos cortes, **mismos no-respuesta**». La tercera cláusula **no es verificable desde
la nube para ninguno de los tres instrumentos**:

- **Negativo con su universo declarado (A.13).** Filas con `texto_reactivo` NO vacío
  para una variable `EDAD*` de `envipe2025` o `encig2025`, buscadas sobre los **cuatro**
  inventarios de reactivos del repo (`v1_0`, `v1_1`, `v1_2`, `ext-v1_0`): **0**.
  Control positivo sobre el mismo comando: `enif2024` sí devuelve texto
  («2.5 ¿Cuántos años cumplidos tiene (NOMBRE)?»), y `data/inventario-fd-v1_1.tsv`
  devuelve 2 filas `EDAD*` para `enif2024`.
- `data/inventario-fd-v1_1.tsv` **no contiene** `envipe2025` ni `encig2025` (contiene
  `envipe2013`). Payloads censados: 30, listados por `awk` sobre la columna 3.
- El único catálogo de edad que el inventario nombra —
  `envipe2025_csv.zip::tsdem_envipe2025/catalogos/edad.csv`— está marcado
  `PRESENTE_EN_DATA_RAW`, y `data/raw` no está montada aquí
  (`acceso_corpus.montado=NO`, `archivos_examinados=0`).

**Qué queda para caja, exactamente:** abrir `catalogos/edad.csv` de ENVIPE 2025, el
catálogo equivalente de ENCIG 2025 y el de `EDAD_V` de ENIF 2024, y confirmar
**código por código** que `97`/`98`/`99` (o los que cada encuesta use) son
no-especificada y no edades reales. Si en alguna de las tres resultaran edades reales,
el tope de 96 de `tramos_edad` estaría **truncando población viva** y el veredicto de
ese instrumento bajaría de `EQUIVALENTE` a `NO-EQUIVALENTE`. Se rutea, no se adivina.

---

## 4 · Resumen

| instrumento | variable (archivo:variable) | unidad | veredicto | evidencia |
|---|---|---|---|---|
| **ENVIPE 2025** | `TSDem.EDAD` (`envipe2025_csv.zip`, `8a7a99fd90ce`) | años cumplidos | **`EQUIVALENTE`** | REGISTRADA · catálogo en caja |
| **ENCIG 2025** | `encig2025_02_residentes_sec_2.EDAD` (`47daf2f73236`) | años cumplidos | **`EQUIVALENTE`** | REGISTRADA · sin fila en inventario FD |
| **ENIF 2024** | `TMODULO.EDAD_V` (`enif_2024_fd.xlsx`, `17e2ad86ce9e`) | años cumplidos | **`EQUIVALENTE`** | ABIERTA aquí (FD) para variable/unidad hermana |

Ninguno sale `MAPEO-N-A-1` ni `NO-EQUIVALENTE`: ninguno de los tres reporta edad en
tramos — los tres la reportan **en años**, y la partición la hace `tramos_edad`, una
sola función, idéntica para los tres. **Los tres veredictos quedan con la cláusula de
no-respuesta pendiente de caja** (§3), que es la única parte que este entorno no puede
cerrar.

**Cero mediciones nuevas en este acto.** Toda cifra de cobertura citada arriba es
**heredada con su fuente a la vista** del censo `P0` de `ACTO MAESTRA35-L1`
(2/sep/2026), no re-derivada aquí — no hay corpus montado con el que re-derivarla.
