# Identidad de `CORR-0002` y `CORR-0003` — pregunta de caja, no corrección inferida del nombre

**Acto:** `ACTO GEN2-LOTE-ENVIPE-1`, pieza **P4**, 9/sep/2026, CAJA (Ubuntu), sobre `origin/main = 6e0381b`.
**Alcance:** identidad por **manifiesto, metadato y procedencia**. **Cero microdato abierto** — ni un solo `conjunto_de_datos/*` ni `*.dbf` de ENCIG o ENCUCI se leyó. **No se mide nada de ENCIG.**

---

## 0 · Lo que declara la demanda (leído, no editado — `demanda-corridas.tsv` es DERIVADO)

```
CORR-0002 | ENCIG2023 | encig25_base_datos_csv | 10 RESULT | CAJA | PARCIAL:script+spec+spec_sha
CORR-0003 | ENCIG2023 | encuci2020_bd_dbf      |  2 RESULT | CAJA | PARCIAL:script+spec+spec_sha
```

## 1 · Qué es realmente cada payload

| payload | evidencia 1 · `url_origen` del manifiesto (procedencia) | evidencia 2 · miembros del ZIP (lista de archivo, no contenido) | identidad |
|---|---|---|---|
| `encig25_base_datos_csv` | `inegi.org.mx/contenidos/programas/**encig/2025**/microdatos/encig25_base_datos_csv.zip` | 6 miembros, todos `encig2025_*.csv` | **ENCIG 2025** |
| `encuci2020_bd_dbf` | `inegi.org.mx/programas/**encuci/2020**/` | 5 miembros, todos `ENCUCI_2020_*.dbf` | **ENCUCI 2020** |

Las dos señales son independientes (una es la ruta de programa en el portal del INEGI, registrada al descargar; la otra es la nomenclatura interna que empaquetó el propio INEGI) y **coinciden**. Ninguno de los dos ZIP trae `metadatos/*.txt`, así que la tercera vía habitual no está disponible — declarado, no suplido por inferencia.

**ENCIG y ENCUCI no son la misma encuesta:** ENCIG es la Encuesta Nacional de Calidad e Impacto Gubernamental; ENCUCI, la Encuesta Nacional sobre Cultura Cívica. Son dos programas distintos del INEGI, no dos olas de uno.

## 2 · De dónde sale «ENCIG2023», que es la pregunta de verdad

**No sale del payload ni de un año mal tecleado. Sale de la derivación.** `tools/corrida0.py:_instrumento()`, para toda fila de tipo `conducta_*`, devuelve el **primer token con forma de instrumento del campo `fuente:` de la REGLA**:

```python
fuentes = [str(f) for f in (r.get("fuente") or [])]
for f in fuentes:
    if re.fullmatch(r"[A-Z][A-Z0-9]{2,}[0-9]{4}", f):
        return f
```

Las dos corridas cuelgan de la **misma regla**, `tramite.mordida.discrecional`, cuyo `fuente` en el árbol es:

```yaml
fuente: ['ENCIG2023', 'Rothstein_trampa_social', 'report:politica']
```

Esa regla tiene hoy **seis** conductas, medidas sobre **instrumentos distintos**:

| conducta | `p` | clase | payload real |
|---|---|---|---|
| `paga_mordida` / `tramite_normal` | 0.62 / 0.38 | `ASIGNADO` | — (sin medición) |
| `paga_mordida_encig2025` / `tramite_normal_encig2025` | 0.085118 / 0.914882 | `MEDIDO` | ENCIG **2025** |
| `paga_mordida_encuci2020` / `tramite_normal_encuci2020` | 0.125822 / 0.874178 | `MEDIDO` | ENCUCI **2020** |

`_instrumento()` lee la procedencia **a nivel de regla** y la aplica a **todas** sus conductas. El `fuente: ENCIG2023` es el rastro de cuando la regla era sólo `ASIGNADO` con `p: 0.62`; las mediciones que llegaron después no lo actualizaron. De ahí que las dos corridas hereden `ENCIG2023`, una de ellas para un payload que ni siquiera es ENCIG.

## 3 · Veredicto por corrida (vocabulario A.4)

| corrida | pregunta | veredicto | qué corrige |
|---|---|---|---|
| **`CORR-0002`** | ¿el payload es del instrumento declarado? | **EXISTE-NO-SATISFACE** | El payload es correcto y está bien identificado (**ENCIG 2025**); la etiqueta `ENCIG2023` de la columna `instrumento` es **derivada**, no tecleada. Se corrige la **derivación**, no la fila. |
| **`CORR-0003`** | idem | **EXISTE-NO-SATISFACE** | El payload es correcto (**ENCUCI 2020**), pero la etiqueta lo asigna a **otro programa de encuesta**, no sólo a otro año. Misma causa, consecuencia mayor: agrupa una corrida de ENCUCI bajo ENCIG. |

**Lo que NO se corrige:** ni «la fila de demanda» ni «la expectativa», que eran las dos opciones que el encargo puso sobre la mesa. `demanda-corridas.tsv` es **DERIVADO — NO EDITAR**: corregirla a mano la revierte en la siguiente corrida de `corrida0 demanda`. Y la expectativa («la columna `instrumento` describe el instrumento del payload») es la correcta: es la derivación la que no la cumple.

**Dónde vive el arreglo, y por qué no aquí.** Dos candidatos, ambos **fuera del perímetro de este acto**:

1. **`_instrumento()`** deriva por conducta y no por regla — leyendo la procedencia del `RESULT` (`demanda-resultados.tsv` ya trae el `payload` correcto **por conducta**: `encig25_base_datos_csv` para `RES-0003`, `encuci2020_bd_dbf` para `RES-0005`), o cayendo al `fuente` de la regla sólo cuando la conducta no declare payload.
2. **`milpa/tramite.yaml`** actualiza el `fuente` de `tramite.mordida.discrecional` — pero eso toca el motor, requiere firma de mesa, y no arregla el caso general (una regla con conductas de varios instrumentos seguirá teniendo un `fuente` que no puede ser correcto para todas).

**Recomendación al lote 2:** la opción 1 es la que arregla la clase, no el caso. La 2 es cosmética mientras `_instrumento()` siga colapsando por regla.

## 4 · Consecuencia para `GEN2-LOTE-ENCIG-1`

El sucesor **no** debe leer la columna `instrumento` de `demanda-corridas.tsv` como identidad de la fuente: debe leer `payload` de `demanda-resultados.tsv`, que es correcto en las dos corridas. Con eso, `CORR-0002` es un lote **ENCIG 2025** y `CORR-0003` es un lote **ENCUCI 2020** — y son **dos lotes**, no uno, aunque la demanda los presente bajo la misma etiqueta.

**A.13.** Examinado: `data/corrida0/demanda-corridas.tsv` (2 filas), `data/corrida0/demanda-resultados.tsv` (2 filas), `data/manifiesto.yaml` (2 entradas), `tools/corrida0.py:_instrumento()` (1 función), `milpa/tramite.yaml` (1 regla, 6 conductas), y la lista de miembros de 2 ZIP (6 y 5 miembros). Microdato abierto: **0 archivos**.
