# ENIF · enmienda de forma antes del COMMIT-3 · v1.0

Acto `GEN2-ASTRA6-C2-EJECUCION-1` · 28/sep/2026 · CAJA · 0-bis `e897d3df`.
Familias: `ENIF-AHORRO-FORMAL`, `ENIF-HORIZONTE-AHORRO`. Cara mecánica: `enmienda-firmas-c2-v1_0.yaml` (mismo directorio; ningún parámetro vive en los dos).

**Contadores movidos: cero.** No abre ola, no cambia estimando, universo, códigos, pesos, banda, soporte, semilla ni remuestreo. No edita `forense/prereg-caja/FAMILIA-2027-ENIF-*-spec-v1_3.md`, ni `spec.yaml`, ni `resultados.json`, ni `sello.json` de los CALC de emisión.

## 1 · Firma de mesa que se ejecuta (verbatim)

Mesa, 28/sep/2026, «firmado» sobre la línea «… B4 las tres · … · E3 1 · E4 1 …» (`forense/encargos/2026-09-28-GEN2-TRAMITE-HOJA-FIRMAS-21-1-ADENDA-1.md`). Texto de la opción firmada para ENIF, B4-(i) = E3 opción 1, control (`forense/analisis/nc-decisiones/hoja-2026-09-27.md` §B4 y §E3; `forense/analisis/familias-2027/hoja-c2-para-mesa-v1_0.md` l.25):

> «Apruebo la envoltura de rutas exactas de adenda-auditoria-propuesta.md, con la identidad de paquete-control-hashes.json, para integración antes del COMMIT-3 ENIF; no autoriza apertura de ola ni altera cálculo estadístico.»

FP que resuelve: `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-06` (B4) y `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-14` (E3).

## 2 · Qué queda integrado (regla para el COMMIT-3)

1. El conducto de apertura de ENIF 2027 (COMMIT-3, acto propio, cuando exista ola autorizada) **ejecuta el lector futuro sólo dentro de** `tools/familias-2027/cierre-material-1/auditoria_sucesora.py`, en un proceso propio de una tarea, con la lista de inputs que fija el conducto desde identidades ya acreditadas.
2. Antes de invocarlo, el conducto verifica por sha256 las **18 identidades** de `forense/analisis/familias-2027/astra6-cierre-material-1/paquete-control-hashes.json` y las **231** de `inventario-portable.json`. Un solo `DISCORDA` o `AUSENTE` es PARO (g) del COMMIT-3: el código congelado no corre, no se parcha.
3. La envoltura no es sandbox para código hostil (lo dice su propia adenda). No añade gate, muestra, semilla, estadístico ni RESULT. El dictamen sigue siendo el de la spec v1_3.

## 3 · Verificación sobre el árbol del acto (EJECUTADO, 28/sep, base `16ba3d02`)

```
$ python3 - (sha256 de las rutas de paquete-control-hashes.json["archivos"])
OK 18 NO-OK 0
$ python3 tools/familias-2027/cierre-material-1/verifica_cierre_material.py --verifica --hoja --pruebas
.......................                                                  [100%]
23 passed in 0.83s
INVENTARIO: VERDE; 231 archivos efectivos, identidad COMMIT-1/enmienda intacta
CONTROL-SUCESOR: VERDE; 18 identidades propuestas
6 familias con emisiones congeladas para 3 olas futuras; 0 con atestación externa verificada; fechas no confirmadas o ventanas esperadas. 5 con soporte histórico; 0 autorizadas para apertura hoy.
```

Las 23 pruebas incluyen las de mutación de enmienda, drivers, lector v2, ORO-0002, piso, inventario/ruta e input raw que enumera `adenda-auditoria-propuesta.md` §«Pruebas materiales».

## 4 · Oferta antes que preferencia (E4, asignada a ENIF por mesa)

Mesa, 28/sep/2026, a pregunta de este acto sobre a qué marginal va «la medida de exclusión por oferta» del texto E4: **«ENIF ahorro (Recomendado)»**. Origen de la pieza: `1178-ENIF-NC-F` (`astra6-cierre-material-1/matriz-nc-1178.tsv` l.15) e `interpretacion-y-oferta.md` («junto a cada marginal de ahorro o canal»). La medida se congela como CALC propio y descriptivo, con spec humana `forense/analisis/familias-2027/astra6-enif/DIN-OFERTA-EXCLUSION-ENIF2024-spec-v1_0.md` (en el perímetro del acto; `prereg-caja/` es de RELEVO-TRAMITE-CAJA-1): ENIF 2024, que es la ola del piso de las dos familias, con universo U_B de la familia. **No es candidato, no es retador y no entra al dictamen de la familia**: se publica al lado del marginal de ahorro. Los números que produzca son RETROSPECTIVA-descriptiva sobre una ola vista y no se mezclan con la emisión PROSPECTIVA.

## 5 · Módulo de auditoría v2.16

- PROSPECTIVA: sólo las emisiones selladas del 26/09. Esta enmienda no emite cifras.
- Unidad: persona elegida de 18 años y más (U_B). La medida de oferta usa la misma unidad y no se promedia con otra.
- Oferta antes que preferencia: el marginal de ahorro formal no se lee como preferencia por la formalidad hasta que tenga su medida de oferta al lado (§4).
- Riesgo de lectura simplista: tomar «ahorro formal» como rasgo cultural. Es un uso declarado, condicionado a oferta, ingreso e infraestructura, y ENIF adulta urbana y rural no se transporta a menores.
