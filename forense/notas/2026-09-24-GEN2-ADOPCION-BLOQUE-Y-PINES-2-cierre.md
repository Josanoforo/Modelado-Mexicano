# Nota de cierre · ACTO GEN2-ADOPCION-BLOQUE-Y-PINES-2 · 24/sep/2026

Encargo: `forense/encargos/2026-09-24-GEN2-ADOPCION-BLOQUE-Y-PINES-2.md` (SHA de redacción `c12a0d87`; base al abrir `origin/main = c12a0d87`, 0 detrás). NUBE (hook: `ENTORNO-DERIVADO = NUBE`, corpus montado=NO, archivos_examinados=0; cero microdato). MODO ABIERTO, COMPUERTA: ninguna. Módulo de auditoría: cero contadores movidos por este acto en `main` (ver tabla).

**Logística declarada (no PARO):**
- Rama: la sesión tiene asignada `claude/new-session-uq2blk` con instrucción de no empujar a otra; se ejecuta ahí en vez de `acto/gen2-adopcion-bloque-y-pines-2` (mismo precedente que el -1).
- Premisa de ruta: el encargo dice `milpa/decisiones.tsv`; ese archivo no existe (`ls milpa/` → 12 archivos, ninguno `decisiones.tsv`). El que lee `corrida0.py::_lee_decisiones` es `data/corrida0/decisiones.tsv`; se escribe ahí.
- Concurrencia: la rama `acto/gen2-tramite-firmas-15` (ADENDA-1, sin fusionar) asienta S y T como FIRMADA con `EJECUTA: GEN2-ADOPCION-BLOQUE-Y-PINES-2` en `forense/firmas-pendientes.tsv`. Para no chocar, este acto **no** toca `firmas-pendientes.tsv`.

## Búsqueda de ya hecho (§4 del encargo)
`git ls-remote --heads origin | grep -ci adopcion` → 0 · `grep -c ENCIG-DUELO-2025-ADJUDICACION-0001 data/corrida0/decisiones.tsv` → 0 · `grep -ci astra data/corrida0/decisiones.tsv` → 4 (ninguna fila de FP de Astra; son la fila `primer-piloto-celda-D` y las tres `catalogo:M0x` del -1).

## `status` antes → después (`python3 tools/corrida0.py status`)

| Contador | Antes (`c12a0d87`) | Después (commiteado) | Con el marcador en el árbol, sin commitear |
|---|---|---|---|
| `N_resultados_gen2_pendientes_adopcion` | 10 | 10 | 10 |
| `N_resultados_gen2_adoptados_activos` | 72 | 72 | 103 |
| `dependencias_numericas_legacy_activas` | 146 | 146 | 146 |
| `__motor` / `__procedencia` / `__catalogo_de_momentos` | 34 / 40 / 23 | 34 / 40 / 23 | 34 / 40 / 23 |
| `celdas_validadas` | 219 | 219 | — |

## P-S · Tercer CALC — filas asentadas; el «Hecho» (g) VERDE **no** se cumple, y la causa es la propia firma
16 filas `origen:CALC-ENCIG-DUELO-2025-ADJUDICACION-0001:<RESULT>-C2-P` con `origen_numerico=HEREDADO` y la firma S verbatim. Aplicación por input, leída del medidor sellado (`medidor.py:639`: `out[base-C2-P] = cand["C2"][c]`): el punto -C2-P **se copia** del RESULT -C2-P del CALC de emisiones sellado; el manifiesto (NUEVO) solo alimenta -R-P, -C2-P-RECALCULADO y controles. Firma: «CALC sellados = HEREDADO». La cadena mecánica aguas arriba lo confirma: EMISIONES → `CALC-C2-COMPUESTO-RESERVADAS-0001` → `IN-MOTOR-NACIONALES milpa/tramite.yaml [FUENTE-LEGACY]`.

Con el marcador re-derivado en el árbol, `python3 tests/check.py --baseline --parallel` (12 min 17 s): **ROJO, los mismos 16 T-REPRO(g)**, ahora con otro motivo:
```
(g) marcador:CRUCE::GOB.gobierno_digital.encig2025.edad_x_sexo::18-29x1 -> RESULT-ENCIG-DUELO-2025-ADJ-EDADXSEXO-18-29-X-1-C2-P: una medición GEN2 no adopta origen HEREDADO; cuenta_gen2 y el sello no cambian la procedencia
... (16 filas: 8 edad_x_sexo + 8 escolaridad_x_sexo)
```
El marcador consume esas celdas como `MEDICION-GEN2` (`corrida0.py`, bloque de `_estimadores_segmento_para_status`), y `milpa/src/linaje.py::aptitud_para_uso` no admite HEREDADO para ese uso. El FAIL pasó de «no acreditado» a «acreditado HEREDADO, no apto para medición». Poner NUEVO para que la suite pase contradiría la firma y la cadena (PARO c); bajar (g) es PARO b. **Decisión para mesa** (abajo). Sobre el árbol commiteado la suite no cambia: las 16 FAIL solo aparecen con el marcador re-derivado, y la vista no se commitea.

## P-T · Once filas
8 filas `adopcion-astra:<FP>` (`tipo=ADOPCION · adopta: SI · uso_predictivo: NO · vence:` ola siguiente) y 3 `dictamen-astra:<FP>` (`tipo: DICTAMEN`), cada una con el texto verbatim de FIRMAS-15 §1 T y el veredicto de la auditoría (`forense/notas/2026-09-23-GEN2-AUDITORIA-POST-HOC-ASTRA-1-auditoria.md` §P4): LIMPIO para ENDUTIH/MOCIBA (#1085) y ENOE (#1087); CON-NC para ENDIREH (#1093, cascada incompleta, no impide adoptar); las tres de U3-POLÍTICA **no aparecen** en la tabla P4 de la auditoría: se declara `NO-AUDITADA-EN-39d2`. Son dictámenes sin uso numérico. El catálogo de Astra no se edita.

## P-W · Diez pendientes — PARO-PREMISA
`N_resultados_gen2_pendientes_adopcion` = `_resultados_citados_en(PROPUESTA) ∩ sellados` menos los que **un consumidor activo** ya lee (`corrida0.py:4987-4995`). Los diez RESULT ya están etiquetados en `milpa/tramite-ola5-propuesta-v0.yaml` (`corrida0_resultado_id` + `corrida0_generacion: GEN2`, líneas 4005-4081; `grep` → 11 citas, incluye CTX-2021 no estimable). Ese archivo es la propuesta que **el motor no carga** (su cabecera; ADR-68(a)). Escribir ahí no cambia nada: el escritor daría un diff vacío. Para que el contador baje, las reglas tienen que entrar al consumidor activo `milpa/tramite.yaml` (mecanismo que ya nombraba `NC-…-369b-01`), y ese archivo **no está** en el perímetro §9. Escribirlo es «escribir fuera de la lista» → PARA. Pregunta a mesa abajo.

## P-E · Escritor a los tres consumidores — no extendido; el contrato lo impide o lo deja a mesa
Por el contrato (`forense/analisis/astra4-relevo/contratos-otros-consumidores.md`), leído, no reinterpretado:
- **Procedencia (40):** «La cita RESULT y el respaldo de clase requieren un campo/esquema acordado por mesa; el diff final no se aplica hasta tener esa decisión.» Falta esa decisión → no se escribe.
- **Catálogo (23):** el contrato pide una **cita lateral** por `Mxx` en un registro aparte, sin tocar los bytes del catálogo sellado. `T-REPRO(c)` exige que todo uso activo GEN2 **materialice** un literal comparable en el archivo consumidor (lo probó el -1 con M08). Una cita lateral no la lee `corrida0` (ajeno, §9) y no movería el contador; un pin rompe (c). Es la bifurcación que prevé §6 («dos formas de convivencia que el contrato no resuelve»). Candidatos con RESULT sellado según `plan-catalogo-23.tsv`: M05 y M23 (`DERIVADO-Y-SELLADO-GEN2`); 01/02 siguen NO-CONSTRUIBLE y 08 queda como dijo N (fila del -1).
- **Celdas-D (6):** el contrato exige sucesora adjudicada con reserva intacta. Las seis filas de su tabla dicen «champion ninguno», «sin CALC de relevo» o «no se presume sucesora»; con eso el contrato da diff vacío. Las «6 referencias de código» (`milpa/src/celdas.py`) «quedan intactas» por el mismo contrato.

Ninguna llave baja. Cada consumidor lleva su NC con `DIFERIDO-A`. No se escribió test por llave porque no hay escritor extendido que probar (D-14).

## Preguntas a mesa (sigo con el resto; ninguna es PARO del lote)
1. **S — 16 celdas HEREDADO en el marcador.** (a) *Recomendada:* aplicar la opción (ii) de FIRMAS-15 S: el marcador no consume esas 16 celdas como medición GEN2 (salen de `estimadores-por-segmento`, o se declaran con uso DESCRIPTIVO, que `aptitud_para_uso` sí admite con herencia). (b) Volver a firmar S como NUEVO: contradice la cadena medida (tramite.yaml legacy aguas arriba). (c) Esperar a que un CALC sucesor re-estime el punto C2 sin la cadena legacy.
2. **W — perímetro.** (a) *Recomendada:* un acto -3 con `milpa/tramite.yaml` en perímetro, por escritor (etiqueta en regla existente, sin número nuevo), reusando el contrato RES-0028. (b) Mantener los diez como pendientes hasta que la propuesta ola 5 entre entera al motor.
3. **E — catálogo.** (a) *Recomendada:* mesa fija que el catálogo se releva por registro lateral y que `T-REPRO(c)` lea ese registro como el lugar donde se materializa el literal (el cambio es de `corrida0`, de otro acto). (b) Añadir una columna de literal al catálogo: exige re-sellar ADR-68(a).

## Verificación
- `python3 tests/check.py --baseline --parallel` con marcador en árbol → ROJO, 17 nuevos: 16 (g) descritos arriba y 1 T25 (`M08` en este encargo; corregido añadiendo los archivos del acto a `_T25_ARCHIVOS_CONOCIDOS`).
- `python3 tests/check.py --rapido` sobre el árbol final → ver ADR.

Filas para mesa (A.12): `FP-260924-GEN2-ADOPCION-BLOQUE-Y-PINES-2-e0db-01` (S), `FP-260924-GEN2-ADOPCION-BLOQUE-Y-PINES-2-e0db-02` (W), `FP-260924-GEN2-ADOPCION-BLOQUE-Y-PINES-2-e0db-03` (catálogo), en `forense/firmas-pendientes.tsv`.
