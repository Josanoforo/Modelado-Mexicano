# FP-373 · ejecución documental v1.2 — sucesión de v1.1 (`--verify` acotado a las fuentes del duelo)

Este archivo es una **sucesión** de `F5-documental-ejecucion-v1_1.md`, que a
su vez sucede a `F5-documental-ejecucion-v1_0.md`. **v1.1 y v1.0 quedan
intactos** — no se editan, no se enmiendan, no se borran. v1.2 los sucede
como contrato vigente sólo en la pieza (e) que v1.1 dejó explícitamente
fuera de su alcance.

- **Autoridad:** FIRMA DE MESA, 15 de septiembre de 2026, verbatim «Si a
  todas.», sobre la HOJA DE FIRMAS DE MESA 2026-09-15, OBJETO 6, archivada
  por A.3 en `forense/encargos/2026-09-15-GEN2-FIRMAS-MESA-1.md`.
- **OBJETO 6 verbatim:** «NC-0178 — sucesión v1.2 del verificador F5:
  `sha256_manifiesto_fuentes` cubre solo las entradas del manifiesto que el
  duelo usa (A.7); v1.1 intacto. No reabre ningún veredicto.»
- **Propagado por:** `ACTO GEN2-FIRMAS-MESA-1` (15/sep/2026, NUBE).
- **Este acto redacta, no ejecuta.** Cero solicitudes al proveedor gastadas
  contra el techo por este archivo. `tools/f5_documental.py` **no se toca
  aquí** (está fuera del perímetro del acto): lo ajusta el acto sucesor que
  relance el runner apuntando a v1.2, exactamente como v1.1 hizo con v1.0.

---

## El defecto que v1.2 corrige

`--verify` comparaba `sha256_manifiesto_fuentes` contra el **archivo
completo** `data/manifiesto.yaml`:

```python
"sha256_manifiesto_fuentes": sha_archivo(MANIFIESTO_FUENTES),   # v1.0/v1.1
```

`data/manifiesto.yaml` es el registro vivo de adquisición: **crece con cada
payload que entra al corpus**, por actos que no tienen ninguna relación con
este duelo. Medido en `NC-0178`: el manifiesto pasó de 1 599 a 1 608 filas
por **seis commits ajenos** desde `c9f714e`, y `--verify` falló por ese
único campo — mientras las 8 filas del contrato eran **idénticas campo a
campo** y `validar_fuente`, `verificar_paquete` y `comprobar_ancestros`
pasaban.

Es decir: el verificador no estaba detectando una alteración de la evidencia
del duelo. Estaba detectando **actividad de adquisición**. Un verificador que
falla por algo que no es su objeto deja de verificar: enseña a ignorarlo.

## La corrección (A.7)

`sha256_manifiesto_fuentes` cubre **sólo las entradas del manifiesto que el
duelo usa**, no el archivo entero. El conjunto no se enumera a mano ni se
teclea en este contrato: se **deriva** de la materialización congelada
(`F5-documental-materializacion-v1_0.json`), recorriendo `celdas[*].fuentes[*].id`.
Un `id` que no esté en el manifiesto es **PARO**, no una fila que se salta.

Derivado al redactar este contrato, son **8** entradas — las mismas 8 que
`NC-0178` ya declaraba idénticas campo a campo:

| celda | `id` de manifiesto |
|---|---|
| `DIN-M-01` | `ennvih1_2002_hogar_q` |
| `DIN-M-01` | `ennvih1_2002_hogar_cb` |
| `DIN-M-01` | `ennvih1_2002_hogar_dta` |
| `DIN-M-01` | `ennvih1_2002_ponderador` |
| `DIN-M-01` | `ennvih1_muestra_diseno` |
| `TRA-M-07` | `encig2021_cuestionario_pdf` |
| `TRA-M-07` | `encig2021_estructura_base_datos_pdf` |
| `TRA-M-07` | `encig_2021_encig21_base_datos_csv` |

### Serialización canónica — declarada, no implícita

Un hash sobre un subconjunto sólo es reproducible si el orden y el formato
están fijados. Se fijan aquí, y el runner sucesor los implementa tal cual:

1. Cargar `data/manifiesto.yaml` y quedarse con las entradas cuyo `id` esté
   en el conjunto derivado arriba.
2. Ordenar por `id` ascendente (orden total: los `id` son únicos).
3. Serializar la lista completa de esas entradas con
   `json.dumps(..., sort_keys=True, ensure_ascii=False, separators=(',', ':'))`.
4. `sha256` de esa cadena en UTF-8.

Equivalente ejecutable, para que no haya ambigüedad de lectura:

```python
sel = [e for e in manifiesto if e.get("id") in ids_del_duelo]
assert len(sel) == len(ids_del_duelo)          # un id ausente es PARO
canon = json.dumps(sorted(sel, key=lambda e: e["id"]),
                   sort_keys=True, ensure_ascii=False, separators=(",", ":"))
sha256_manifiesto_fuentes = hashlib.sha256(canon.encode("utf-8")).hexdigest()
```

**Valor derivado al redactar este contrato** (`origin/main` = `582d4e9`,
manifiesto de 1 608 filas):

```
sha256_manifiesto_fuentes (v1.2, 8 filas del contrato) =
    b811a57f3b7cf2a243717b5ca68142783c7da2af80295bbf6c1f402814f488df
```

Se registra como **evidencia de redacción, no como valor esperado
congelado**: el runner lo re-deriva al correr y compara contra lo que la
materialización declare. Si las 8 filas cambian de verdad, `--verify` debe
fallar — para eso existe.

## Lo que v1.2 NO hace

- **No reabre ningún veredicto.** `TRIADA-0002` no se re-adjudica; los 12
  `PUNTO` y 10 `ABSTENCION` de la corrida bajo v1.1 quedan como están; las
  10 posiciones `NO-CORRIDA` siguen `NO-CORRIDA`.
- **No reabre la firma.** `F5-documental-firma-v1_0.md` (sha256
  `aa7135c8ad53053592798141d1ea91f4c37d467cd10f640522578e5298583f60`) sigue
  siendo válida: v1.2 corrige un verificador, no la autorización.
- **No cambia la escala del criterio** (`≥6/8`, cero sustituciones, mejora
  de cobertura `≥4/8`) sellada en v1.0.
- **No toca `sha256_manifiesto_contexto`**, que es otro campo y otro objeto.
- **No autoriza `FP-374` ni `F6`**, ni gasta solicitudes contra el techo
  (ledger en 94/96 al cerrar v1.1, sin cambio aquí).
- **No edita `tools/f5_documental.py`.** Fuera de perímetro: este contrato
  dice qué debe hacer el runner; el acto que lo relance lo escribe.

## Qué cierra y qué queda

`NC-0178` **cierra** con esta sucesión: su sucesor pedía literalmente «fija
`sha256_manifiesto_fuentes` a las 8 filas del contrato, no al archivo
entero», y eso es lo que este contrato fija.

Queda vivo, y no lo cierra este acto: **`--verify` no se ha vuelto a correr
bajo v1.2** — el runner todavía implementa la versión de archivo completo.
Hasta que el acto sucesor lo ajuste y corra, el `OK` de `--verify` sigue sin
imprimirse. Eso es una pieza de CAJA, no de NUBE, y va a `NO-CORRIDO` con su
sucesor nombrado.
