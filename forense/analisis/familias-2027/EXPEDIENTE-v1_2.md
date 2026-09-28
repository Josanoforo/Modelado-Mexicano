# Expediente de familias 2027 · v1.2

`ACTO GEN2-VALIDACION-Y-2027-1` (P3) · 28/sep/2026 · CAJA · base `9d2550b9` · sucesor de `EXPEDIENTE-v1_1.md` (queda intacto, E.1). Tabla: [`familias-2027-estado-v1_2.tsv`](familias-2027-estado-v1_2.tsv), con las mismas 8 filas y columnas de v1.1 más `reverificacion_v1_2`.

**Contadores movidos: cero.** Ninguna emisión nueva, ninguna emisión previa cambiada (`git diff --stat origin/main -- 'data/corrida0/CALC-FAMILIA-2027-*'` vacío) y ningún retador nuevo.

| Estado | Familias |
|---|---|
| LISTA-PARA-ABRIR-CUANDO-LLEGUE-LA-OLA | ENIF-AHORRO-FORMAL · ENIF-HORIZONTE-AHORRO · ENCIG-SOLICITUD-MORDIDA · ENVIPE-DENUNCIA-U4 · ENVIPE-EVASION-NORMA |
| NO-LANZAR-TODAVIA (sin contrato firmado) | ENOE-INFORMALIDAD · ENSU-CAMPECHE-INSEGURIDAD |
| SUSPENDIDA bajo gate (no se reactiva) | ENCIG-PAGO-DIGITAL (`FP-260926-GEN2-ASTRA6-C2-ENCIG-1-fde0-01`) |

**Re-verificación de las cinco de C2-EJECUCION-1 (EJECUTADO):**
- sha de la spec humana y del spec.yaml contra v1.1: 16/16 CASA.
- `sello.sha256` OK.
- Archivos listados en cada `sello.json`: 43/43 COINCIDE (siete sellos, contando el oro ENIF-0002 y la suspendida).
- Los archivos de potencia existen.

La fila en vista queda **NO-VERIFICABLE-AQUÍ**. `data/corrida0/corridas.tsv` en `origin/main` viene de un `[deriva]` por trozos (#1268: «20 CALC, quedan 101»), y el control positivo `CALC-CCPV-FAM-PISOS-0001`, adoptado en el catálogo, tampoco aparece: sobre 357 filas examinadas, el negativo no dice nada.

**ENOE / ENSU.** La premisa del encargo («contrato firmado, R27 (2)») no se sostiene: el texto verbatim de R27 (2) deja ENOE en NO-LANZAR-TODAVIA y exige firma propia para cualquier regla nueva. Para ENSU-Campeche no hay contrato firmado. No se hizo COMMIT-1 ni emisión. Las opciones están en `forense/validacion-independiente/validacion-continua-1/hoja-mesa.md` §3.

**Candidatos y comparación primaria.** No cambian respecto de v1.1: cada familia sellada declaró sus candidatos juntos con una sola comparación primaria en su COMMIT-1, y este acto no añade ninguno.

**Atestación externa.** Manifiesto `forense/sellos/manifiesto-sellos-2026-09-28.tsv` (sha256 `ff020b94…a6e0`, 578 filas) preparado; el `.ots` lo sube mesa (hoja §2).

## Módulo de auditoría (v2.16)
- **Unidad por instrumento.** La declara la spec humana de cada familia (columna `spec_humana_ruta`). Este acto no la re-deriva y no promedia unidades entre familias.
- **PROSPECTIVA / RETROSPECTIVA.** Las seis emisiones selladas son PROSPECTIVAS: selladas antes de que exista su R 2027. Este expediente no contiene ninguna cifra RETROSPECTIVA y no mezcla las dos columnas.
- **Escrito a mano / no derivado.** Los estados de la tabla salen de la fila v1.1 más los comandos citados. La potencia se cita, no se recalcula.
- **Clase media urbana, cultura vs estructura.** No aplica: no hay cifra nueva.
