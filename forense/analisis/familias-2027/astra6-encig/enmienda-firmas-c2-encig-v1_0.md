# ENCIG · reconocimiento de identidad antes del COMMIT-3 · v1.0

Acto `GEN2-ASTRA6-C2-EJECUCION-1` · 28/sep/2026 · CAJA · 0-bis `e897d3df`.
Familia: `ENCIG-SOLICITUD-MORDIDA`. `ENCIG-PAGO-DIGITAL` sigue SUSPENDIDA por `FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01` (FIRMADA): este reconocimiento no la reactiva. Cara mecánica: `enmienda-firmas-c2-encig-v1_0.yaml`.

**Contadores movidos: cero.** No modifica reglas, gates, sellos, `spec-v1_3.md/.yaml`, ni la enmienda de verificación. No autoriza apertura.

## 1 · Firma de mesa que se ejecuta (verbatim)

Mesa, 28/sep/2026, «firmado» sobre la línea «… B4 las tres · … · E3 1 · E4 1 …» (`forense/encargos/2026-09-28-GEN2-TRAMITE-HOJA-FIRMAS-21-1-ADENDA-1.md`). Texto de la opción firmada, B4-(ii) = E3 opción 1, reconocimiento ENCIG (`forense/analisis/nc-decisiones/hoja-2026-09-27.md` §B4 y §E3; `hoja-c2-para-mesa-v1_0.md` l.26):

> «Reconozco la identidad efectiva de evaluar.py/cierre.py y enmienda-verificacion.json fijada en inventario-portable.json, con antecedente COMMIT-1 y enmienda preservados; no modifico reglas ni autorizo apertura.»

FP que resuelve: `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06` (B4) y `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-14` (E3).

## 2 · Identidad reconocida

Corte de `inventario-portable.json`: `1eeb855272b933642177e3f32d51adc89f1009a0`. Estado del inventario: SELLADO-INTERNAMENTE (no es atestación externa).

| archivo | sha256 (inventario) | cotejo 28/sep |
|---|---|---|
| `tools/familias-2027/encig/evaluar.py` | `143cd5b451821080…` | OK |
| `tools/familias-2027/encig/cierre.py` | `3f1989c2596cd938…` | OK |
| `forense/analisis/familias-2027/astra6-encig/enmienda-verificacion.json` | `22f9857ee05b238a…` | OK |
| `forense/analisis/familias-2027/astra6-encig/enmienda-verificacion.md` | `a21345263b85a6a9…` | OK |

Los sha completos están en el yaml y en el inventario, que es la fuente. EJECUTADO: se leyó `inventario-portable.json["archivos"]`, se calculó sha256 de cada ruta del árbol y se comparó. `verifica_cierre_material.py --verifica` dice «INVENTARIO: VERDE; 231 archivos efectivos, identidad COMMIT-1/enmienda intacta».

## 3 · Regla para el COMMIT-3

El conducto de apertura de ENCIG 2027 cotejará estas cuatro identidades antes de ejecutar `evaluar.py`. Un `DISCORDA` es PARO (g): no se parcha. El antecedente COMMIT-1 (`md:0dbe658d`) y la enmienda se preservan como están.

## 4 · Módulo de auditoría v2.16

- Unidad de ENCIG-SOLICITUD-MORDIDA: persona. ENCIG-PAGO-DIGITAL (suspendida) es trámite/evento de pago; no se promedian.
- Riesgo de lectura simplista: leer «mordida» como rasgo cultural. Es una solicitud reportada, condicionada a la oferta institucional y al trámite, en un marco urbano de 100 mil habitantes o más que no se transporta a lo rural ni a lo indígena.
- PROSPECTIVA: sólo la emisión sellada del 26/09. Este reconocimiento no emite cifras.
