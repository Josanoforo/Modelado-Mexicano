# Censo de estimabilidad de los 15 coeficientes de generador
### `censo-estimabilidad-coeficientes` · **v1.2** · generado por comando · `tools/censo_estimabilidad.py`, ENCARGO CENSO-CMD

> | | |
> |---|---|
> | **ARCHIVO** | `censo-estimabilidad-coeficientes-v1_2.md` |
> | **QUÉ ES** | El mismo censo de `censo-estimabilidad-coeficientes-v1_1.md` (sellado `ADR-89`), **derivado por comando en vez de escrito a mano**: `tools/censo_estimabilidad.py` lee `milpa/procedencia.yaml:rutas_estimabilidad_coeficiente` (la foto tabular de v1.0) y `data/curacion-registro/relaciones.tsv`, y aplica la única regla de reclasificación v1.0→v1.1 (`SIN-RUTA` sube a `RUTA-C` si `relaciones.tsv` trae, para la misma necesidad, `capa4_apertura_mapeo=EXISTE-SATISFACE` + `clasificacion_relacion=CONFIRMADA`) — la misma regla que `forense/registro-recalculo-v1_0.md` §1 Entrada 0 verificó a mano. No abre microdato, no toca `data/curacion-registro/**` ni `milpa/procedencia.yaml` (solo lee). |
> | **QUÉ NO ES** | No es una redeterminación independiente de las rutas: la clasificación base (RUTA-A/RUTA-I/RUTA-C de v1.0) se lee de `procedencia.yaml`, no se recalcula desde el corpus crudo — ese trabajo ya lo hizo `censo-estimabilidad-coeficientes-v1_0.md`. No cambia ningún valor `ASIGNADO`, no adjudica ningún veredicto de Hito D. |
> | **VERIFICAS ASÍ** | `python3 tools/censo_estimabilidad.py` reproduce este archivo completo; `python3 tools/censo_estimabilidad.py --reparto` reproduce solo §2. `tests/test_censo_derivado.py` falla si el derivador diverge de este archivo o del reparto sellado por `ADR-89` sin que medie un ADR nuevo. |
> | **SELLADA POR** | Hereda el sello de `ADR-89` (`canon/gobernanza-v1_15.md`) sobre el reparto y la taxonomía — este acto (`ENCARGO CENSO-CMD`, `FP-37`) no reabre ninguna fila, solo verifica por comando que el mecanismo reproduce exacto lo ya sellado (15/15 filas, mismo reparto). |

---

## 1 · Las 15 filas

Columna `Comando de verificación`: corre desde la raíz del repo, reproduce la evidencia citada en `Llave/instrumento citado` para esa fila sola — para que una ficha (F3) que cite un coeficiente pueda apuntar a instrumento+comando, no solo al veredicto.

| # | necesidad_id | Gen.coeficiente | Ruta | Llave/instrumento citado | Comando de verificación |
|---|---|---|---|---|---|
| 1 | `N1` | `G1.confianza_institucional` | **RUTA-A** | β̂ marginal ya corrido, Encargo W -- no re-abre ruta, ver ADR-57(a) | `python3 -c "import yaml; d=yaml.safe_load(open('milpa/procedencia.yaml')); print([r for r in d['rutas_estimabilidad_coeficiente']['detalle'] if r['gen']=='G1' and r['coef']=='confianza_institucional'])"` |
| 2 | `N2` | `G1.radio_confianza` | **RUTA-A** | β̂ marginal ya corrido, Encargo W -- ASIGNADO · asociación estable a la partición policial, inestable a formalidad/edad/ingreso (ADR-61, resuelve la condición de ADR-60 e con W1-P) | `python3 -c "import yaml; d=yaml.safe_load(open('milpa/procedencia.yaml')); print([r for r in d['rutas_estimabilidad_coeficiente']['detalle'] if r['gen']=='G1' and r['coef']=='radio_confianza'])"` |
| 3 | `N3` | `G2.sens_estatus` | **SIN-RUTA** | búsqueda de reactivo cerrada, ADR-54 | `python3 -c "import csv; r=[x for x in csv.DictReader(open('data/curacion-registro/relaciones.tsv'), delimiter='\t') if x['necesidad_id']=='N3']; print(r)"` |
| 4 | `N4` | `G2.aversion_riesgo` | **SIN-RUTA** | búsqueda de reactivo cerrada, ADR-52 A | `python3 -c "import csv; r=[x for x in csv.DictReader(open('data/curacion-registro/relaciones.tsv'), delimiter='\t') if x['necesidad_id']=='N4']; print(r)"` |
| 5 | `N5` | `G3.horizonte_temporal` | **RUTA-I** | llave sellada ENNViH/MxFLS vía CAL-G3, Fase C descriptiva ya corrida, gobernanza:623 -- ruta ENOE de ADR-49 D1 NO se re-propone | `grep -n 'CAL-G3' canon/gobernanza-v1_15.md` |
| 6 | `N6` | `G3.aversion_riesgo` | **SIN-RUTA** | misma búsqueda cerrada que G2·aversion_riesgo, ADR-52 A | `python3 -c "import csv; r=[x for x in csv.DictReader(open('data/curacion-registro/relaciones.tsv'), delimiter='\t') if x['necesidad_id']=='N6']; print(r)"` |
| 7 | `N7` | `G3.familismo_apoyo` | **RUTA-A** | β̂ marginal ya corrido, Encargo W -- marca (b) | `python3 -c "import yaml; d=yaml.safe_load(open('milpa/procedencia.yaml')); print([r for r in d['rutas_estimabilidad_coeficiente']['detalle'] if r['gen']=='G3' and r['coef']=='familismo_apoyo'])"` |
| 8 | `N8` | `G4.exposicion_violencia` | **RUTA-C** | candidato BP1_23/ver_oir_callar con limitación estructural declarada, procedencia.yaml:396-413 (limite_c2) -- pendiente adjudicación de mesa | `python3 -c "import yaml; d=yaml.safe_load(open('milpa/procedencia.yaml')); print([r for r in d['rutas_estimabilidad_coeficiente']['detalle'] if r['gen']=='G4' and r['coef']=='exposicion_violencia'])"` |
| 9 | `N9` | `G4.confianza_institucional` | **RUTA-C** | mismo candidato y misma limitación que G4·exposicion_violencia | `python3 -c "import yaml; d=yaml.safe_load(open('milpa/procedencia.yaml')); print([r for r in d['rutas_estimabilidad_coeficiente']['detalle'] if r['gen']=='G4' and r['coef']=='confianza_institucional'])"` |
| 10 | `N10` | `G4.horizonte_temporal` | **SIN-RUTA** | sin reactivo dedicado; único proxy (ENIF P4_10) es de G3 y cruza instrumento distinto de los desenlaces de G4 | `python3 -c "import csv; r=[x for x in csv.DictReader(open('data/curacion-registro/relaciones.tsv'), delimiter='\t') if x['necesidad_id']=='N10']; print(r)"` |
| 11 | `N11` | `G4.sens_estatus` | **SIN-RUTA** | misma búsqueda cerrada que G2·sens_estatus, ADR-54 | `python3 -c "import csv; r=[x for x in csv.DictReader(open('data/curacion-registro/relaciones.tsv'), delimiter='\t') if x['necesidad_id']=='N11']; print(r)"` |
| 12 | `N12` | `G5.familismo_apoyo` | **RUTA-C** | reclasificada desde la clase sin ruta de v1.0: relaciones.tsv trae capa4_apertura_mapeo=EXISTE-SATISFACE + clasificacion_relacion=CONFIRMADA para N12 (REL-4a609c6633a4bafac14a6930, fuente: ENBIARE 2021) | `python3 -c "import csv; r=[x for x in csv.DictReader(open('data/curacion-registro/relaciones.tsv'), delimiter='\t') if x['necesidad_id']=='N12' and x['capa4_apertura_mapeo']=='EXISTE-SATISFACE' and x['clasificacion_relacion']=='CONFIRMADA']; print(r)"` |
| 13 | `N13` | `G5.familismo_obligacion` | **RUTA-C** | reclasificada desde la clase sin ruta de v1.0: relaciones.tsv trae capa4_apertura_mapeo=EXISTE-SATISFACE + clasificacion_relacion=CONFIRMADA para N13 (REL-fe202a3fa76f0516a6e27f8b, fuente: ENASIC 2022) | `python3 -c "import csv; r=[x for x in csv.DictReader(open('data/curacion-registro/relaciones.tsv'), delimiter='\t') if x['necesidad_id']=='N13' and x['capa4_apertura_mapeo']=='EXISTE-SATISFACE' and x['clasificacion_relacion']=='CONFIRMADA']; print(r)"` |
| 14 | `N14` | `G5.radio_confianza` | **RUTA-C** | reclasificada desde la clase sin ruta de v1.0: relaciones.tsv trae capa4_apertura_mapeo=EXISTE-SATISFACE + clasificacion_relacion=CONFIRMADA para N14 (REL-5741e12ce3e0a0e076ee48fc, fuente: ENBIARE 2021) | `python3 -c "import csv; r=[x for x in csv.DictReader(open('data/curacion-registro/relaciones.tsv'), delimiter='\t') if x['necesidad_id']=='N14' and x['capa4_apertura_mapeo']=='EXISTE-SATISFACE' and x['clasificacion_relacion']=='CONFIRMADA']; print(r)"` |
| 15 | `N15` | `G6.deferencia` | **SIN-RUTA** | único proxy (Latinobarómetro P4NOIJ) sin desenlace de G6 documentado en el mismo instrumento; SIN_DISEÑO_PUBLICADO | `python3 -c "import csv; r=[x for x in csv.DictReader(open('data/curacion-registro/relaciones.tsv'), delimiter='\t') if x['necesidad_id']=='N15']; print(r)"` |

---

## 2 · Reparto — comando y resultado

Receta de conteo, verbatim de `censo-estimabilidad-coeficientes-v1_1.md` §7 (misma clase de fallo ya corregido ahí: solo filas de datos, patrón `^\| [0-9]+ \|`):

```
$ python3 tools/censo_estimabilidad.py --write /tmp/censo-v1_2.md
$ grep -E '^\| [0-9]+ \|' /tmp/censo-v1_2.md | grep -oE 'RUTA-[CIA]|SIN-RUTA' | sort | uniq -c
      3 RUTA-A
      5 RUTA-C
      1 RUTA-I
      6 SIN-RUTA
```

**3 + 5 + 1 + 6 = 15.** Coincide exacto con el reparto sellado por `ADR-89` sobre `censo-estimabilidad-coeficientes-v1_1.md` (`3 RUTA-A · 5 RUTA-C · 1 RUTA-I · 6 SIN-RUTA`).

---

## 3 · Filas reclasificadas por la regla v1.0→v1.1 (3 de 15)

- fila 12 (`N12`, `G5.familismo_apoyo`): reclasificada desde la clase sin ruta de v1.0: relaciones.tsv trae capa4_apertura_mapeo=EXISTE-SATISFACE + clasificacion_relacion=CONFIRMADA para N12 (REL-4a609c6633a4bafac14a6930, fuente: ENBIARE 2021)
- fila 13 (`N13`, `G5.familismo_obligacion`): reclasificada desde la clase sin ruta de v1.0: relaciones.tsv trae capa4_apertura_mapeo=EXISTE-SATISFACE + clasificacion_relacion=CONFIRMADA para N13 (REL-fe202a3fa76f0516a6e27f8b, fuente: ENASIC 2022)
- fila 14 (`N14`, `G5.radio_confianza`): reclasificada desde la clase sin ruta de v1.0: relaciones.tsv trae capa4_apertura_mapeo=EXISTE-SATISFACE + clasificacion_relacion=CONFIRMADA para N14 (REL-5741e12ce3e0a0e076ee48fc, fuente: ENBIARE 2021)

---

## 4 · Lo que este acto no hace

No re-audita las 12 filas no reclasificadas — hereda su ruta de `procedencia.yaml:rutas_estimabilidad_coeficiente`, que a su vez hereda de `censo-estimabilidad-coeficientes-v1_0.md` §5. No abre microdato. No escribe en `data/curacion-registro/**` ni en `milpa/procedencia.yaml`. Si el derivador diverge del reparto sellado, `tests/test_censo_derivado.py` falla y la divergencia se investiga con su propio ADR antes de declarar nada — no aquí.
